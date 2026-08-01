#!/usr/bin/env python3
"""Independent Claim-5 rate inversion and reduced empirical KDE comparator.

This is intentionally *not* an implementation of either prior paper's complete
DDPM/DDIM sampler.  It independently checks their printed TV error exponent and
runs a clearly labelled reduced full-dimensional kernel-score diagnostic.
"""
import argparse, csv, json, math, platform, sys
from pathlib import Path
import numpy as np


def posterior_score(x):
    """Exact score for p=.5 N(-1,I)+.5 N(1,I), independently derived."""
    means = np.stack([-np.ones(x.shape[1]), np.ones(x.shape[1])])
    logw = -0.5 * ((x[:,None,:] - means[None,:,:])**2).sum(2)
    w = np.exp(logw - logw.max(1,keepdims=True)); w /= w.sum(1,keepdims=True)
    return (w[:,:,None] * (means[None,:,:] - x[:,None,:])).sum(1)


def kde_score(train, x, bandwidth, chunk=128):
    out=[]; d=train.shape[1]
    for q in range(0,len(x),chunk):
        z=x[q:q+chunk]
        dist=((z[:,None,:]-train[None,:,:])**2).sum(2)
        a=np.exp(-dist/(2*bandwidth*bandwidth))
        # score of isotropic Gaussian KDE: weighted (Xi-x)/h^2
        out.append(((a[:,:,None]*(train[None,:,:]-z[:,None,:])).sum(1)
                    / np.maximum(a.sum(1)[:,None],1e-300) / bandwidth**2))
    return np.concatenate(out)


def run(out, seed, dims, ns, eval_n):
    rng=np.random.default_rng(seed); rows=[]
    for d in dims:
        for n in ns:
            signs=rng.integers(0,2,size=n)*2-1
            train=rng.normal(size=(n,d))+signs[:,None]
            s2=rng.integers(0,2,size=eval_n)*2-1
            test=rng.normal(size=(eval_n,d))+s2[:,None]
            # Silverman dimension-dependent full-dimensional KDE bandwidth.
            h=n**(-1.0/(d+4))
            mse=float(np.mean((kde_score(train,test,h)-posterior_score(test))**2))
            rows.append({'seed':seed,'d':d,'n':n,'bandwidth':h,'score_mse':mse})
    out.mkdir(parents=True,exist_ok=True)
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    # The two independently pinned priors print TV error n^{-beta/(d+2beta)}.
    inversion=[]
    for d in dims:
        for beta in (1,2):
            rate=beta/(d+2*beta)
            inv=(d+2*beta)/beta
            # algebraic check: n=eps^-inv gives n^-rate=eps
            eps=1e-3; n=eps**(-inv)
            inversion.append({'d':d,'beta':beta,'tv_rate_exponent':rate,
                              'sample_exponent':inv,'identity_error':abs(n**(-rate)-eps)})
    summary={'kind':'toy_empirical_comparator',
             'scope':'Reduced full-dimensional Gaussian-mixture KDE score diagnostic; not a DDPM/DDIM sampler and not a verification of either prior theorem.',
             'seed':seed,'dims':dims,'ns':ns,'eval_n':eval_n,
             'prior_rate_derivation':'If TV <= C n^{-beta/(d+2beta)} polylog(n), ignoring logarithms, choosing n=epsilon^{-(d+2beta)/beta} gives TV <= C epsilon.',
             'inversion':inversion,'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,required=True); p.add_argument('--seed',type=int,default=20260801)
    p.add_argument('--dims',type=int,nargs='+',default=[2,4,6]); p.add_argument('--ns',type=int,nargs='+',default=[500,1000,2000]); p.add_argument('--eval',type=int,default=512)
    a=p.parse_args(); run(a.out,a.seed,a.dims,a.ns,a.eval)
