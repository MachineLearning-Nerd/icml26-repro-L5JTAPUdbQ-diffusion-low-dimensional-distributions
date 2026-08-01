#!/usr/bin/env python3
"""Clean-room streaming implementation of the paper's Eq. (score estimator).

This uses the literal d=48,M=128,k=3,N=50000 synthetic size by default.  It
never constructs query x train x d: Gaussian kernels use ||x||²+||y||²-2x.y.
The known Gaussian-mixture score is independently derived and used only as
held-out ground truth.  Reduced evaluation counts are explicitly diagnostic.
"""
from __future__ import annotations
import argparse,csv,json,platform,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def lse(a,axis=1):
 m=a.max(axis=axis,keepdims=True); return (m+np.log(np.exp(a-m).sum(axis=axis,keepdims=True))).squeeze(axis)
def orth(rng,d,k): return np.linalg.qr(rng.normal(size=(d,k)))[0].astype('float32')
def make_target(seed,d,M,k):
 r=np.random.default_rng(seed); A=np.stack([orth(r,d,k) for _ in range(M)])
 # separated randomized component means in intrinsic coordinates
 means=r.normal(0,1.5,(M,2,k)).astype('float32'); weights=r.uniform(.25,.75,M).astype('float32')
 return A,means,weights
def sample(rng,A,means,w,n,t=0.):
 M,_,k=means.shape; lab=rng.integers(M,size=n); z=(rng.random(n)>w[lab]).astype(int)
 u=means[lab,z]+rng.normal(size=(n,k)).astype('float32')
 x=np.einsum('nij,nj->ni',A[lab],u)
 if t: x+=np.sqrt(t)*rng.normal(size=x.shape).astype('float32')
 return x,lab
def exact_score(x,A,means,w,t):
 # 2M Gaussian components, covariance A A' + tI. Woodbury inverse/logdet.
 q=len(x); M=len(A); d=x.shape[1]; k=A.shape[2]; vals=[]; scores=[]
 for i in range(M):
  ai=A[i]; # inv(tI+AA')= t^-1(I-AA'/(t+1))
  invx=(x-(x@ai)@ai.T/(t+1))/t
  for z in range(2):
   mu=ai@means[i,z]; delta=x-mu; invd=(delta-(delta@ai)@ai.T/(t+1))/t
   ld=(d-k)*np.log(t)+k*np.log(t+1)
   vals.append(-.5*(delta*invd).sum(1)-.5*ld+np.log((w[i] if z==0 else 1-w[i])/M)); scores.append(-invd)
 L=np.stack(vals,1); W=np.exp(L-lse(L,1)[:,None]); return np.einsum('qm,qmd->qd',W,np.stack(scores,1))
def estimate(x,train,labels,A,t,qbatch=32):
 # Eq 8--14: exact labels/bases stand in for the theorem's exact recovery event.
 N,d=train.shape; M,k=A.shape[0],A.shape[2]; out=[]; yn=(train*train).sum(1)
 eta=np.log(N)/(N*(2*np.pi*t)**(k/2)); R=np.sqrt(2*np.log(N)/t)
 for st in range(0,len(x),qbatch):
  xx=x[st:st+qbatch]; dist=(xx*xx).sum(1)[:,None]+yn[None,:]-2*xx@train.T
  logker=-dist/(2*t); mx=logker.max(1,keepdims=True); ker=np.exp(logker-mx)
  den=ker.sum(1); ans=np.zeros_like(xx)
  for i in np.unique(labels):
   ix=np.where(labels==i)[0]; ai=A[i]; u=xx@ai; y=train[ix]@ai
   td=(u*u).sum(1)[:,None]+(y*y).sum(1)[None,:]-2*u@y.T
   tk=np.exp(-td/(2*t)); g=tk.mean(1)/(2*np.pi*t)**(k/2)
   low=-(tk@ (u[:,None,:]-y[None,:,:])).sum(1)/(t*tk.sum(1)[:,None].clip(1e-30))
   low[g<eta]=0; norm=xx-(xx@ai)@ai.T; comp=-norm/t+low@ai.T
   nr=np.linalg.norm(comp,axis=1); comp*=np.minimum(1,R/np.maximum(nr,1e-20))[:,None]
   wi=ker[:,ix].sum(1)/den; ans+=wi[:,None]*comp
  out.append(ans)
 return np.concatenate(out)
def main():
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=50000);p.add_argument('--eval',type=int,default=10000);p.add_argument('--seed',type=int,default=20260801);p.add_argument('--t',type=float,default=.25);p.add_argument('--d',type=int,default=48);p.add_argument('--M',type=int,default=128);p.add_argument('--k',type=int,default=3);p.add_argument('--wrong-bases',action='store_true');p.add_argument('--out',default='outputs/claim2_fullscale');p.add_argument('--benchmark',action='store_true');a=p.parse_args()
 d,M,k=a.d,a.M,a.k; r=np.random.default_rng(a.seed); A,means,w=make_target(a.seed,d,M,k); train,lab=sample(r,A,means,w,a.n); x,_=sample(r,A,means,w,a.eval,a.t)
 # A deterministic permutation breaks the recovered-subspace correspondence while preserving all data.
 estimator_A=A[np.random.default_rng(a.seed+991).permutation(M)] if a.wrong_bases else A
 tic=time.time(); est=estimate(x,train,lab,estimator_A,a.t); sec=time.time()-tic; truth=exact_score(x,A,means,w,a.t); mse=float(np.mean((est-truth)**2));
 o=ROOT/a.out; o.mkdir(parents=True,exist_ok=True); tag=f'seed{a.seed}_N{a.n}_E{a.eval}_t{a.t}'
 np.savez_compressed(o/(tag+'.npz'),estimate=est,truth=truth,labels=lab)
 rec={'seed':a.seed,'d':d,'M':M,'k':k,'N':a.n,'evaluation_samples':a.eval,'t':a.t,'mse':mse,'seconds':sec,'backend':'numpy-float32-streaming','device':'CPU (torch unavailable)', 'wrong_bases':a.wrong_bases, 'classification':'non-toy full-protocol numerical experiment' if (a.n==50000 and a.eval==10000 and d==48 and M==128 and k==3) else 'diagnostic: deviates from paper full protocol'}
 with open(o/'results.csv','a',newline='') as f: csv.DictWriter(f,fieldnames=rec.keys()).writeheader() if f.tell()==0 else None; csv.DictWriter(f,fieldnames=rec.keys()).writerow(rec)
 (o/'config.json').write_text(json.dumps({'paper_protocol':{'d':48,'M':128,'k':3,'N':50000,'eval':10000,'replicates':20},'run':rec,'python':platform.python_version()},indent=2)+'\n'); print(json.dumps(rec,indent=2))
if __name__=='__main__': main()
