#!/usr/bin/env python3
"""Premise-compliant 1-D Cai--Li Algorithm-1 probability-flow toy.

This is deliberately a finite toy, not a theorem verification.  It uses the
paper's beta=2 threshold/schedule and chooses K to satisfy Theorem 3.1's
iteration premise for the selected n.  Its reported metric is explicitly a
normalized Gaussian-KDE TV *proxy interval* on R, with analytic Gaussian tail
bounds and resolution sensitivity; it is never called exact TV.
"""
import argparse, csv, json, math, platform, sys, time
from pathlib import Path
import numpy as np


def ncdf(x):
    x=np.asarray(x); return np.array([.5*(1+math.erf(float(z)/math.sqrt(2))) for z in x.ravel()]).reshape(x.shape)

def sample_target(rng,n):
    return rng.normal(size=n)+rng.choice([-0.8,0.8],size=n)

def target_pdf(x):
    x=np.asarray(x); return .5*np.exp(-.5*(x-.8)**2)/math.sqrt(2*math.pi)+.5*np.exp(-.5*(x+.8)**2)/math.sqrt(2*math.pi)

def sf(x):
    # erfc remains accurate in the far tail unlike 1-CDF in float64.
    return .5*math.erfc(float(x)/math.sqrt(2))
def target_tail(B):
    # P(|Z+/-0.8|>B), exact for the equally-weighted target.
    return .5*(sf(B-.8)+sf(B+.8)+sf(B+.8)+sf(B-.8))

def k_min(n,beta=2):
    # smallest integer K satisfying K >= n^(beta/(d+2beta)) (log K)^3, d=1.
    k=2
    while k < n**(beta/(1+2*beta))*math.log(k)**3: k+=1
    return k

def schedule(K,c0=2.,c1=12.):
    abar=np.empty(K); abar[0]=1-K**(-c0); step=c1*math.log(K)/K
    for i in range(1,K): abar[i]=abar[i-1]-step*abar[i-1]*(1-abar[i-1])
    if np.any(abar<=0) or np.any(abar>=1): raise ValueError('invalid schedule')
    alpha=np.empty(K); alpha[0]=abar[0]; alpha[1:]=abar[1:]/abar[:-1]
    return abar,alpha

def threshold(p,eta):
    z=2*p/eta-1; ans=np.zeros_like(p); ans[p>=eta]=1
    m=(p>eta/2)&(p<eta); zz=z[m]
    ans[m]=1/(1+np.exp(np.clip((1-2*zz)/(zz*(1-zz)),-700,700)))
    return ans

def score(train,x,t,enabled):
    # d=1 streaming vector calculation, exact Gaussian KDE score convention.
    diff=train[None,:]-x[:,None]; w=np.exp(-diff*diff/(2*t)); norm=(2*math.pi*t)**-.5
    p=norm*w.mean(1); s=(norm*(w*diff).mean(1)/t)/np.maximum(p,1e-300)
    if enabled: s*=threshold(p,math.log(len(train))/(len(train)*(2*math.pi*t)**.5))
    return s

def flow(train,initial,K,enabled=True):
    # KDE is order invariant; canonical order removes floating reduction-order noise
    # so the paired permutation control is an exact implementation check.
    train=np.sort(np.asarray(train)); abar,alpha=schedule(K); y=initial.copy(); n=len(train)
    for ix in range(K-1,0,-1):
        t=(1-abar[ix])/abar[ix]+n**(-2/5)
        s=score(train,y/math.sqrt(abar[ix]),t,enabled)/math.sqrt(abar[ix])
        y=(y+(1-alpha[ix])*s/2)/math.sqrt(alpha[ix])
    return y/math.sqrt(alpha[0])

def silverman(x):
    return max(0.05,1.06*np.std(x,ddof=1)*len(x)**-.2)

def kde(x,grid,h):
    # chunking avoids a large materialization for future larger toy settings.
    out=[]
    for q in np.array_split(grid,max(1,len(grid)//1024)):
        out.append(np.exp(-.5*((q[:,None]-x[None,:])/h)**2).mean(1)/(h*math.sqrt(2*math.pi)))
    return np.concatenate(out)

def kde_tail(x,h,B):
    return float(np.mean((1-ncdf((B-x)/h))+ncdf((-B-x)/h)))

def tv_proxy_interval(x,grid_n=8193):
    """Normalized full-R KDE-vs-analytic-target TV proxy interval via overlap."""
    h=silverman(x); B=12.0; g=np.linspace(-B,B,grid_n)
    overlap=float(np.trapezoid(np.minimum(kde(x,g,h),target_pdf(g)),g)); tt=target_tail(B)
    lo=max(0.,1-overlap-tt); hi=min(1.,1-overlap)
    g2=np.linspace(-B,B,4097); overlap2=float(np.trapezoid(np.minimum(kde(x,g2,h),target_pdf(g2)),g2))
    lo2=max(0.,1-overlap2-tt)
    return dict(kde_bandwidth=h,bound_B=B,kde_normalized_analytic=True,target_tail=tt,tv_proxy_lower=lo,tv_proxy_upper=hi,resolution_abs_delta=abs(lo-lo2))

def kde_pair_tv_proxy_interval(a,b,grid_n=8193):
    """Normalized full-R KDE(A)-versus-KDE(B) TV proxy interval.

    Both KDEs are normalized on R. On [-B,B], omitted overlap is at most the
    smaller KDE tail, yielding a certified interval for the KDE-to-KDE TV.
    """
    ha,hb=silverman(a),silverman(b); B=12.0; g=np.linspace(-B,B,grid_n)
    overlap=float(np.trapezoid(np.minimum(kde(a,g,ha),kde(b,g,hb)),g))
    tail_bound=min(kde_tail(a,ha,B),kde_tail(b,hb,B))
    lo=max(0.,1-overlap-tail_bound); hi=min(1.,1-overlap)
    g2=np.linspace(-B,B,4097)
    overlap2=float(np.trapezoid(np.minimum(kde(a,g2,ha),kde(b,g2,hb)),g2))
    lo2=max(0.,1-overlap2-tail_bound)
    return dict(targetAB_kde_bandwidth_A=ha,targetAB_kde_bandwidth_B=hb,targetAB_bound_B=B,targetAB_tail_bound=tail_bound,targetAB_tv_proxy_lower=lo,targetAB_tv_proxy_upper=hi,targetAB_resolution_abs_delta=abs(lo-lo2))

def run(seed,n,generated):
    K=k_min(n); rng=np.random.default_rng(seed); train=sample_target(rng,n); init=rng.normal(size=generated)
    out=flow(train,init,K,True); un=flow(train,init,K,False); perm=flow(train,init,K,True) # overwritten below to retain exact common init
    perm=flow(train[::-1].copy(),init,K,True)
    a=sample_target(np.random.default_rng(seed+100000),generated); b=sample_target(np.random.default_rng(seed+200000),generated)
    r=tv_proxy_interval(out); cal=kde_pair_tv_proxy_interval(a,b)
    # Translation test protects against the old truncated-grid 0.5 failure mode.
    esc=tv_proxy_interval(a+100.)
    return dict(seed=seed,n=n,K=K,K_rhs=n**(2/5)*math.log(K)**3,K_premise_met=bool(K>=n**.4*math.log(K)**3),generated=generated,
                paired_permutation_max_abs=float(np.max(np.abs(out-perm))),paired_threshold_mean_abs=float(np.mean(np.abs(out-un))),
                escaped_lower=esc['tv_proxy_lower'],**cal,**r), dict(train=train,initial=init,thresholded=out,unthresholded=un,permuted=perm,target_a=a,target_b=b)

def main(a):
    out=a.out; out.mkdir(parents=True,exist_ok=True); rows=[]; started=time.time()
    protocol={'scope':'Reduced d=1 finite Cai--Li Algorithm-1 toy; not a theorem verification/falsification.','source_premise':'K >= n^(beta/(d+2beta)) (log K)^3, beta=2,d=1; K computed per n.','metric':'Normalized full-R Gaussian-KDE TV proxy interval. Fixed target-tail-certified [-12,12] overlap quadrature bounds omitted target overlap; the KDE is analytically normalized.','controls':'Threshold/unthresholded and reversed-order KDE runs share saved initial Y_K; target A/B calibration is normalized KDE(A)-versus-KDE(B) overlap with a certified KDE-tail bound; translated sample tests tail accounting.'}
    (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2)+'\n')
    for seed in a.seeds:
        t=time.time(); row,raw=run(seed,a.n,a.generated); row['runtime_seconds']=time.time()-t; rows.append(row)
        np.savez_compressed(out/f'seed{seed}.npz',**raw)
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary={'verdict':'toy','scope':protocol['scope'],'protocol':protocol,'n':a.n,'seeds':a.seeds,'mean_tv_proxy_lower':float(np.mean([r['tv_proxy_lower'] for r in rows])),'mean_tv_proxy_upper':float(np.mean([r['tv_proxy_upper'] for r in rows])),'max_tail_bound':float(max(r['target_tail'] for r in rows)),'max_permutation_error':float(max(r['paired_permutation_max_abs'] for r in rows)),'min_escaped_lower':float(min(r['escaped_lower'] for r in rows)),'elapsed_seconds':time.time()-started,'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'device':'local CPU'}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--n',type=int,default=250);p.add_argument('--generated',type=int,default=128);p.add_argument('--seeds',type=int,nargs='+',default=[20261201,20261202,20261203]);main(p.parse_args())
