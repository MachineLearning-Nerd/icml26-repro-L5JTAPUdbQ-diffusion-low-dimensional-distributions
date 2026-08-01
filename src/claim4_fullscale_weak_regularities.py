#!/usr/bin/env python3
"""Clean-room full-scale Claim 4 experiment: discontinuous UoS cube mixture.

The target is uniform on 128 separated intrinsic 3-cubes in R^48.  It meets
UoS/nonintersection/equal-mass/bounded-tail assumptions but its unsmoothed
law has discontinuous cube-boundary densities, ambient density gaps, and is
not globally log-concave.  Gaussian smoothing gives an independently derived
closed-form score used only as held-out truth.
"""
from __future__ import annotations
import argparse, csv, json, math, platform, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SQRT2PI=math.sqrt(2*math.pi)
def phi(x): return np.exp(-.5*x*x)/SQRT2PI
def Phi(x): return .5*(1+np.vectorize(math.erf)(x/math.sqrt(2)))
def lse(a):
 m=a.max(1,keepdims=True); return (m+np.log(np.exp(a-m).sum(1,keepdims=True))).ravel()
def bases(seed,d,M,k):
 r=np.random.default_rng(seed); return np.stack([np.linalg.qr(r.normal(size=(d,k)))[0].astype('float32') for _ in range(M)])
def sample(r,A,n,t,a=1.):
 M,_,k=A.shape; lab=r.integers(M,size=n); u=r.uniform(-a,a,size=(n,k)).astype('float32'); x=np.einsum('nij,nj->ni',A[lab],u)
 if t: x+=math.sqrt(t)*r.normal(size=x.shape).astype('float32')
 return x,lab
def exact_score(x,A,t,a=1.):
 # product of convolved uniform-coordinate densities in tangent, Gaussian normal density.
 n,d=x.shape; M,_,k=A.shape; logs=np.empty((n,M)); comps=np.empty((n,M,d)); s=math.sqrt(t)
 for i in range(M):
  B=A[i]; u=x@B; hi=(a-u)/s; lo=(-a-u)/s; Z=np.maximum(Phi(hi)-Phi(lo),1e-300)
  # d/du log [(Phi(hi)-Phi(lo))/(2a)]
  slow=(phi(lo)-phi(hi))/(s*Z)
  normal=x-(x@B)@B.T
  comps[:,i]=-normal/t+slow@B.T
  logs[:,i]=np.log(Z).sum(1)-k*math.log(2*a)-(d-k)*.5*math.log(2*math.pi*t)-(normal*normal).sum(1)/(2*t)-math.log(M)
 w=np.exp(logs-lse(logs)[:,None]); return np.einsum('nm,nmd->nd',w,comps)
def estimate(x,train,labels,A,t,qbatch=24):
 # independent clean-room Eq(8-14)-style tangent KDE, streamed over full N.
 N,d=train.shape; M,k=A.shape[0],A.shape[2]; yn=(train*train).sum(1); out=[]
 eta=np.log(N)/(N*(2*np.pi*t)**(k/2)); R=np.sqrt(2*np.log(N)/t)
 for st in range(0,len(x),qbatch):
  xx=x[st:st+qbatch]; ds=(xx*xx).sum(1)[:,None]+yn[None]-2*xx@train.T; lk=-ds/(2*t); mm=lk.max(1,keepdims=True); ker=np.exp(lk-mm); den=ker.sum(1); ans=np.zeros_like(xx)
  for i in range(M):
   ix=np.flatnonzero(labels==i); B=A[i]; u=xx@B; y=train[ix]@B; td=(u*u).sum(1)[:,None]+(y*y).sum(1)[None]-2*u@y.T; tk=np.exp(-td/(2*t)); tsum=tk.sum(1).clip(1e-30); g=tsum/len(ix)/(2*np.pi*t)**(k/2)
   low=-(tk@(u[:,None,:]-y[None,:,:])).sum(1)/(t*tsum[:,None]); low[g<eta]=0
   comp=-(xx-(xx@B)@B.T)/t+low@B.T; nr=np.linalg.norm(comp,axis=1); comp*=np.minimum(1,R/np.maximum(nr,1e-20))[:,None]
   ans+=(ker[:,ix].sum(1)/den)[:,None]*comp
  out.append(ans)
 return np.concatenate(out)
def violations(A,a=1.):
 # The density is exactly zero off its union of subspaces; midpoint of two generic support points is off it.
 x=A[0,:,0]*.5; y=A[1,:,0]*.5; mid=(x+y)/2
 residual=min(np.linalg.norm(mid-A[i]@(A[i].T@mid)) for i in range(len(A)))
 return {'target':'equal-weight uniform intrinsic cubes','UoS_conditions':{'d':48,'M':128,'k':3,'component_mass':1/128,'mass_lower_bound_1_over_cpM':1/128,'generic_intersection_dimension_upper_bound':0,'bounded_support_subgaussian':True},'regularity_violations':{'ambient_density_exists':False,'density_lower_bound':False,'boundary_discontinuity_witness':'uniform cube density jumps from 1/(2a)^k inside to 0 outside at every intrinsic boundary','holder_continuity':False,'global_log_concavity':False,'midpoint_off_union_distance':float(residual),'support_gap_density':0.0}}
def main():
 p=argparse.ArgumentParser(); p.add_argument('--seed',type=int,default=20261001);p.add_argument('--n',type=int,default=50000);p.add_argument('--eval',type=int,default=10000);p.add_argument('--t',type=float,default=.25);p.add_argument('--out',default='outputs/claim4_fullscale');a=p.parse_args()
 A=bases(a.seed,48,128,3); r=np.random.default_rng(a.seed); train,lab=sample(r,A,a.n,0); x,_=sample(r,A,a.eval,a.t); start=time.time(); est=estimate(x,train,lab,A,a.t); truth=exact_score(x,A,a.t); sec=time.time()-start; mse=float(np.mean((est-truth)**2));
 o=ROOT/a.out;o.mkdir(parents=True,exist_ok=True);np.savez_compressed(o/f'seed{a.seed}_N{a.n}_E{a.eval}_t{a.t}.npz',estimate=est,truth=truth,labels=lab)
 rec={'seed':a.seed,'d':48,'M':128,'k':3,'N':a.n,'evaluation_samples':a.eval,'t':a.t,'mse':mse,'seconds':sec,'device':'local CPU numpy float32 streaming','classification':'non-toy literal paper-scale synthetic protocol','violations':violations(A)}
 (o/'result.json').write_text(json.dumps(rec,indent=2)+'\n');(o/'config.json').write_text(json.dumps({'protocol':'full d=48,M=128,k=3,N=50000,eval=10000','ground_truth':'closed-form score of Gaussian-smoothed uniform-cube mixture'},indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
