#!/usr/bin/env python3
"""Clean-room Euler--Maruyama implementation of Algorithm 1 (OU reverse SDE).

This is an empirical sampling test, not a proof.  It uses the repository's
Eq. (8)--(14) streaming KDE score estimator and the paper's T=log(n),
tau=n**(-2/k) schedule.  The scorer is evaluated in the VE coordinates
h=(1-exp(-2s))/exp(-2s), as in the paper proof, then transformed back to the
OU marginal score.  Sliced W1 is the declared practical high-dimensional W1
proxy; a target-vs-target split supplies its Monte Carlo floor.
"""
from __future__ import annotations
import argparse,csv,json,platform,time
from pathlib import Path
import numpy as np
from claim2_fullscale_cleanroom import make_target,sample,estimate
ROOT=Path(__file__).resolve().parents[1]

def sliced_w1(a,b,seed,projections=64):
    """Mean 1-D empirical W1 over random unit directions (equal sample sizes)."""
    r=np.random.default_rng(seed); v=r.normal(size=(projections,a.shape[1])).astype('float32')
    v/=np.linalg.norm(v,axis=1,keepdims=True)
    aa=np.sort(a@v.T,axis=0); bb=np.sort(b@v.T,axis=0)
    return float(np.mean(np.abs(aa-bb)))

def reverse(train,labels,A,n,k,seed,generated,steps,qbatch,wrong_bases=False):
    r=np.random.default_rng(seed+17); d=train.shape[1]; T=float(np.log(n)); tau=float(n**(-2.0/k))
    y=r.normal(size=(generated,d)).astype('float32')
    dt=(T-tau)/steps
    estA=A[np.random.default_rng(seed+991).permutation(len(A))] if wrong_bases else A
    # Reverse time r runs 0 -> T-tau, while forward time s=T-r runs T -> tau.
    for j in range(steps):
        s=T-j*dt
        c=np.exp(-s); sig2=-np.expm1(-2*s); h=sig2/(c*c)
        # score_Xs(y) = score_h(y/c)/c, using exact labels as the theorem event.
        score=estimate(y/c,train,labels,estA,h,qbatch=qbatch)/c
        y += (y+2*score)*dt + np.sqrt(2*dt)*r.normal(size=y.shape).astype('float32')
        if not np.isfinite(y).all(): raise FloatingPointError('nonfinite reverse sample')
    return y,{'T':T,'tau':tau,'steps':steps,'dt':dt}

def one(a):
    r=np.random.default_rng(a.seed); A,means,w=make_target(a.seed,a.d,a.M,a.k)
    train,lab=sample(r,A,means,w,a.n)
    tic=time.time(); gen,sch=reverse(train,lab,A,a.n,a.k,a.seed,a.generated,a.steps,a.qbatch,a.wrong_bases); seconds=time.time()-tic
    target,_=sample(r,A,means,w,a.generated); target2,_=sample(r,A,means,w,a.generated)
    sw=sliced_w1(target,gen,a.seed+43,a.projections); floor=sliced_w1(target,target2,a.seed+43,a.projections)
    rec={'seed':a.seed,'N':a.n,'d':a.d,'M':a.M,'k':a.k,'generated_samples':a.generated,'sliced_w1':sw,'target_split_sliced_w1':floor,'ratio_to_mc_floor':sw/max(floor,1e-12),'seconds':seconds,'wrong_bases':a.wrong_bases,'backend':'numpy-float32-streaming CPU','device':'local CPU','classification':'non-toy full-paper d/M/k/N cell' if (a.n==50000 and a.d==48 and a.M==128 and a.k==3) else 'reduced end-to-end toy'}
    out=ROOT/a.out; out.mkdir(parents=True,exist_ok=True); tag=f"seed{a.seed}_N{a.n}_wrong{int(a.wrong_bases)}"
    np.savez_compressed(out/(tag+'.npz'),generated=gen,target=target,target2=target2,projection_seed=a.seed+43)
    with open(out/'results.csv','a',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=rec.keys());
        if f.tell()==0: wr.writeheader()
        wr.writerow(rec)
    (out/(tag+'.json')).write_text(json.dumps({**rec,'schedule':sch,'command':vars(a),'python':platform.python_version()},indent=2)+'\n')
    print(json.dumps({**rec,'schedule':sch},indent=2)); return rec

def main():
 p=argparse.ArgumentParser(); p.add_argument('--n',type=int,default=50000);p.add_argument('--d',type=int,default=48);p.add_argument('--M',type=int,default=128);p.add_argument('--k',type=int,default=3);p.add_argument('--seed',type=int,default=20260901);p.add_argument('--generated',type=int,default=128);p.add_argument('--steps',type=int,default=12);p.add_argument('--qbatch',type=int,default=16);p.add_argument('--projections',type=int,default=64);p.add_argument('--wrong-bases',action='store_true');p.add_argument('--out',default='outputs/claim1_reverse'); a=p.parse_args(); one(a)
if __name__=='__main__': main()
