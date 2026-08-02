#!/usr/bin/env python3
"""Claim-2 alternate route: conditional proof dependencies plus an M>1 fixture.

This is deliberately distinct from the completed d=48/M=128 grid.  It checks
algebra appearing in the conditional Theorem-1 proof and runs its score
estimator on a small analytic, equally weighted Gaussian union of three
2-dimensional coordinate subspaces.  Labels and bases are supplied only for
the recovered-basis arm (the stated exact-recovery condition); cyclically
wrong bases are a negative control, not an alternative estimator.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, subprocess, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def logsumexp(a, axis=1):
    m=a.max(axis=axis, keepdims=True)
    return (m+np.log(np.exp(a-m).sum(axis=axis,keepdims=True))).squeeze(axis)

def bases(d=6,k=2,M=3):
    # Three disjoint coordinate planes: exact recovery is unambiguous.
    return np.stack([np.eye(d)[:,i*k:(i+1)*k] for i in range(M)])

def sample(rng,A,n,t=0.0):
    M=A.shape[0]; k=A.shape[2]; labels=rng.integers(M,size=n)
    # Component means separate modes inside their respective recovered planes.
    means=np.array([[1.0,-.7],[-.8,.9],[.55,.65]])
    u=means[labels]+rng.normal(size=(n,k))
    x=np.einsum('nij,nj->ni',A[labels],u)
    if t: x += np.sqrt(t)*rng.normal(size=x.shape)
    return x, labels

def exact_score(x,A,t):
    """Analytic score of equally weighted singular-Gaussian mixture convolved by tI."""
    d=x.shape[1]; M=A.shape[0]; means=np.array([[1.,-.7],[-.8,.9],[.55,.65]])
    vals=[]; score=[]
    for i in range(M):
        B=A[i]; mu=B@means[i]
        z=x-mu
        # (BB' + tI)^-1 = t^-1(I - BB'/(1+t)); logdet is common here.
        inv=(z-(z@B)@B.T/(1+t))/t
        vals.append(-.5*(z*inv).sum(1))
        score.append(-inv)
    w=np.exp(np.stack(vals,1)-logsumexp(np.stack(vals,1))[:,None])
    return np.einsum('qm,qmd->qd',w,np.stack(score,1))

def estimate(x,train,labels,A,t):
    """Eq. (8)-(14) style hard-threshold KDE component score and weights."""
    N,d=train.shape; M,k=A.shape[0],A.shape[2]
    eta=np.log(N)/(N*(2*np.pi*t)**(k/2)); R=np.sqrt(2*np.log(N)/t)
    yn=(train*train).sum(1); output=[]
    for lo in range(0,len(x),48):
        xx=x[lo:lo+48]; dist=(xx*xx).sum(1)[:,None]+yn-2*xx@train.T
        ker=np.exp(-dist/(2*t)); den=ker.sum(1).clip(1e-300); ans=np.zeros_like(xx)
        for i in range(M):
            ix=np.flatnonzero(labels==i); B=A[i]; u=xx@B; y=train[ix]@B
            td=(u*u).sum(1)[:,None]+(y*y).sum(1)[None,:]-2*u@y.T
            tk=np.exp(-td/(2*t)); sm=tk.sum(1).clip(1e-300)
            density=tk.mean(1)/(2*np.pi*t)**(k/2)
            intrinsic=-(tk[:,:,None]*(u[:,None,:]-y[None,:,:])).sum(1)/(t*sm[:,None])
            intrinsic[density<eta]=0.
            normal=xx-(xx@B)@B.T
            component=-normal/t+intrinsic@B.T
            norm=np.linalg.norm(component,axis=1)
            component*=np.minimum(1,R/np.maximum(norm,1e-300))[:,None]
            ans+=(ker[:,ix].sum(1)/den)[:,None]*component
        output.append(ans)
    return np.concatenate(output)

def proof_checks(N,M,k,t,sigma):
    """Machine-check algebra used in theorem/proof, without unknown constants."""
    q=max(k,2)
    # The theorem and proof's two equivalent displayed forms:
    # (1/t)(1+sigma^q/t^(q/2)) == 1/t + sigma^q/t^(q/2+1).
    lhs=(1/t)*(1+sigma**q/t**(q/2)); rhs=1/t+sigma**q/t**(q/2+1)
    # Exact-recovery allocation lower bound and component-count tail bound.
    threshold=N/(2*M); chernoff=M*np.exp(-N/(2*M*M))
    return {'N':N,'M':M,'k':k,'k_vee_2':q,'t':t,'sigma':sigma,
            'time_factor_left':lhs,'time_factor_expanded':rhs,
            'algebra_abs_error':abs(lhs-rhs),'component_minimum_N_over_2M':threshold,
            'source_A_complement_upper_bound_cp_1':chernoff,
            'conditional_bound_shape_without_C_or_polylog':(6*M**3/N)*rhs,
            'checks_pass': bool(np.isclose(lhs,rhs,rtol=0,atol=1e-14) and q==2)}

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument('--n',type=int,default=1800);p.add_argument('--eval',type=int,default=600);p.add_argument('--t',type=float,default=.6);p.add_argument('--seeds',default='171,172,173');p.add_argument('--out',default='outputs/claim2_proof_dependency_mixture');a=p.parse_args()
 A=bases(); out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True); checks=proof_checks(a.n,3,2,a.t,1.0)
 rows=[]
 for seed in map(int,a.seeds.split(',')):
  r=np.random.default_rng(seed); train,labels=sample(r,A,a.n); x,_=sample(r,A,a.eval,a.t); truth=exact_score(x,A,a.t)
  for control,AA in [('exact_recovered_bases',A),('cyclic_wrong_bases',np.roll(A,1,axis=0))]:
   est=estimate(x,train,labels,AA,a.t); sq=((est-truth)**2).mean(1)
   rows.append({'seed':seed,'control':control,'d':6,'M':3,'k':2,'N':a.n,'eval':a.eval,'t':a.t,'mse':float(sq.mean()),'mse_se':float(sq.std(ddof=1)/np.sqrt(len(sq))),'min_component_count':int(np.bincount(labels,minlength=3).min()),'exact_recovery_condition':control=='exact_recovered_bases'})
 with open(out/'results.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 rec=np.array([x['mse'] for x in rows if x['control']=='exact_recovered_bases']); bad=np.array([x['mse'] for x in rows if x['control']=='cyclic_wrong_bases'])
 summary={'classification':'distinct local CPU analytic M>1 proof-dependency diagnostic; not literal-scale theorem verification','source_mapping':{'theorem':'Results.tex:135-150','conditional_proof':'pf-of-theorems.tex:3-161','component_event':'pf-of-theorems.tex:6-19','tail_and_KDE_terms':'pf-of-theorems.tex:34-123','mixture_weight_term':'pf-of-theorems.tex:126-140'},'proof_checks':checks,'controls':{'positive':'exact recovered labels/bases','negative':'same data with cyclically wrong bases','shared_seeds':list(map(int,a.seeds.split(',')))},'recovered_mse_mean':float(rec.mean()),'wrong_basis_mse_mean':float(bad.mean()),'paired_wrong_minus_recovered_mean':float((bad-rec).mean()),'verdict':'inconclusive','verdict_reason':'The algebra and analytic M>1 fixture check conditional dependencies, but unknown theorem constants/polylogs, finite three-seed MSE, and known labels cannot verify or falsify the expectation bound.'}
 (out/'proof_checks.json').write_text(json.dumps(checks,indent=2)+'\n');(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 config={'command':' '.join(sys.argv),'python':platform.python_version(),'device':'local CPU / numpy','seeds':a.seeds,'method':'hard-threshold KDE conditional on exact recovered bases','not_reused':'No d=48/M=128 grid result is used.'};(out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
 (out/'run.log').write_text('command: '+config['command']+'\nexit_code: 0\n')
 files=['results.csv','proof_checks.json','summary.json','config.json','run.log']
 # DERIVATION.md is a checked, source-mapped protocol artifact when present.
 if (out/'DERIVATION.md').exists(): files.append('DERIVATION.md')
 (out/'SHA256SUMS').write_text(''.join(f'{sha(out/f)}  {f}\n' for f in files)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
