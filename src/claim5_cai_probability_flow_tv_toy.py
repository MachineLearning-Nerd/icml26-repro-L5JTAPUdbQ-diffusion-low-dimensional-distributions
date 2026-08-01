#!/usr/bin/env python3
"""Reduced, clean-room Cai--Li (arXiv:2503.09583) probability-flow TV toy.

Implements their Algorithm 1 / Eqs. (p_hat), (score-estimate),
(score-estimator-X), and DDIM update: Gaussian KDE score with the paper's
eta_t=log(n)/(n(2*pi*t)^(d/2)) soft threshold, then deterministic reverse
updates.  It deliberately uses a small K and smooth two-Gaussian target, so it
is an empirical *toy*, not a replication of their asymptotic theorem.
"""
import argparse, csv, json, math, platform, sys, time
from pathlib import Path
import numpy as np


def normal_cdf(x):
    # numpy builds used here do not expose erf consistently.
    return np.asarray([0.5 * (1.0 + math.erf(float(z) / math.sqrt(2.0))) for z in np.ravel(x)]).reshape(np.shape(x))


def schedule(K, c0=2.0, c1=12.0):
    """Paper's cumulative-alpha recurrence, with alpha_k recovered by ratio."""
    abar = np.empty(K)
    abar[0] = 1.0 - K ** (-c0)
    step = c1 * math.log(K) / K
    for i in range(1, K):
        abar[i] = abar[i-1] - step * abar[i-1] * (1.0 - abar[i-1])
    if np.any(abar <= 0) or np.any(abar >= 1):
        raise ValueError("toy K/c constants give invalid cumulative alphas")
    alpha = np.empty(K); alpha[0] = abar[0]; alpha[1:] = abar[1:] / abar[:-1]
    return abar, alpha


def soft_threshold(p, eta):
    """Smooth 0-to-1 bump; literal endpoint behavior of Eq. (soft-thre-defn)."""
    z = 2.0 * p / eta - 1.0
    ans = np.zeros_like(p)
    ans[p >= eta] = 1.0
    mid = (p > eta / 2.0) & (p < eta)
    # Stable smooth bump equivalent to the source expression on (0,1).
    zz = z[mid]
    ans[mid] = 1.0 / (1.0 + np.exp(np.clip((1.0 - 2.0 * zz) / (zz * (1.0 - zz)), -700, 700)))
    return ans


def kde_score(train, x, t, thresholded, batch=256):
    """grad p_hat/p_hat, optionally times the exact paper soft threshold."""
    d = train.shape[1]; n = len(train); out = np.empty_like(x)
    norm = (2.0 * math.pi * t) ** (-d / 2.0)
    eta = math.log(n) / (n * (2.0 * math.pi * t) ** (d / 2.0))
    for start in range(0, len(x), batch):
        q = x[start:start+batch]
        diff = train[None, :, :] - q[:, None, :]
        w = np.exp(-np.sum(diff * diff, axis=2) / (2.0 * t))
        denom = norm * w.mean(axis=1)
        grad = norm * (w[:, :, None] * diff).mean(axis=1) / t
        score = grad / np.maximum(denom[:, None], 1e-300)
        if thresholded:
            score *= soft_threshold(denom, eta)[:, None]
        out[start:start+len(q)] = score
    return out


def sample_target(rng, n, d):
    signs = rng.choice(np.array([-1.0, 1.0]), size=n)
    # Smooth, bounded-subgaussian Gaussian mixture satisfying the intended beta=2 toy class.
    return rng.normal(size=(n, d)) + signs[:, None] * 0.8


def probability_flow(train, rng, d, K, generated_n, thresholded=True):
    abar, alpha = schedule(K)
    y = rng.normal(size=(generated_n, d))
    for idx in range(K - 1, 0, -1):
        t = (1.0 - abar[idx]) / abar[idx] + len(train) ** (-2.0 / (d + 4.0))
        score_x = kde_score(train, y / math.sqrt(abar[idx]), t, thresholded)
        score_y = score_x / math.sqrt(abar[idx])
        y = (y + (1.0 - alpha[idx]) * score_y / 2.0) / math.sqrt(alpha[idx])
    return y / math.sqrt(alpha[0]), abar, alpha


def gaussian_density(x):
    d = x.shape[-1]; means = np.stack([-0.8 * np.ones(d), 0.8 * np.ones(d)])
    z = x.reshape(-1, d)
    e = np.exp(-0.5 * np.sum((z[:, None, :] - means[None, :, :]) ** 2, axis=2))
    return (e.mean(axis=1) / (2.0 * math.pi) ** (d / 2.0)).reshape(x.shape[:-1])


def kde_density(samples, grid, h=0.35, batch=128):
    out=[]; d=samples.shape[1]; c=(2*math.pi*h*h)**(-d/2)
    flat=grid.reshape(-1,d)
    for s in range(0,len(flat),batch):
        q=flat[s:s+batch]; dist=np.sum((q[:,None,:]-samples[None,:,:])**2,axis=2)
        out.append(c*np.exp(-dist/(2*h*h)).mean(axis=1))
    return np.concatenate(out).reshape(grid.shape[:-1])


def grid_tv(generated, d, shift=0.0):
    # Deterministic quadrature (d=1/2 only) with a shifted-grid crosscheck.
    m = 201 if d == 1 else 71
    axis=np.linspace(-5.0+shift,5.0+shift,m); mesh=np.meshgrid(*([axis]*d),indexing='ij')
    grid=np.stack(mesh,axis=-1); dx=(axis[1]-axis[0])**d
    return float(0.5*np.abs(kde_density(generated,grid)-gaussian_density(grid)).sum()*dx)


def hist_tv(a, b, d):
    bins=[np.linspace(-5,5,17)]*d
    ha,_=np.histogramdd(a,bins=bins); hb,_=np.histogramdd(b,bins=bins)
    return float(0.5*np.abs(ha/len(a)-hb/len(b)).sum())


def run_cell(out, seed, d, n, K, generated_n):
    rng=np.random.default_rng(seed * 1009 + d * 37 + n)
    train=sample_target(rng,n,d); generated,abar,alpha=probability_flow(train,rng,d,K,generated_n,True)
    # Controls must use same target/train size; only score regularization or pairing is destroyed.
    rng_control=np.random.default_rng(seed * 1009 + d * 37 + n + 99)
    unthresholded,_a,_b=probability_flow(train,rng_control,d,K,generated_n,False)
    permuted_train=train.copy(); rng_control.shuffle(permuted_train) # invariant KDE control documented explicitly
    permuted,_a,_b=probability_flow(permuted_train,rng_control,d,K,generated_n,True)
    target_a=sample_target(rng_control,generated_n,d); target_b=sample_target(rng_control,generated_n,d)
    if d <= 2:
        tv=grid_tv(generated,d); tv_shift=grid_tv(generated,d,0.5*(10/(201 if d==1 else 71)))
        tv_un=grid_tv(unthresholded,d); tv_perm=grid_tv(permuted,d)
        floor=grid_tv(target_a,d); metric='deterministic_gaussian_KDE_grid_quadrature_TV'
    else:
        tv=hist_tv(generated,target_a,d); tv_shift=hist_tv(generated,target_b,d)
        tv_un=hist_tv(unthresholded,target_a,d); tv_perm=hist_tv(permuted,target_a,d)
        floor=hist_tv(target_a,target_b,d); metric='heldout_histogram_TV_proxy_d3'
    np.savez_compressed(out / f'seed{seed}_d{d}_n{n}.npz', train=train, generated=generated,
                        unthresholded=unthresholded, permuted=permuted, target_a=target_a, target_b=target_b)
    return {'seed':seed,'d':d,'n':n,'K':K,'generated_n':generated_n,'tau':n**(-2/(d+4)),
            'metric':metric,'tv':tv,'tv_shift_crosscheck':tv_shift,'tv_unthresholded_control':tv_un,
            'tv_permuted_train_control':tv_perm,'tv_target_target_floor':floor,
            'abar_first':float(abar[0]),'abar_last':float(abar[-1]),'runtime_seconds':None}


def main(a):
    out=a.out; out.mkdir(parents=True,exist_ok=True); rows=[]; started=time.time()
    for seed in a.seeds:
        for d in a.dims:
            for n in a.ns:
                t=time.time(); row=run_cell(out,seed,d,n,a.K,a.generated); row['runtime_seconds']=time.time()-t; rows.append(row)
    fields=list(rows[0]);
    with (out/'results.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
    groups={}
    for d in a.dims:
        for n in a.ns:
            vals=[r['tv'] for r in rows if r['d']==d and r['n']==n]
            groups[f'd{d}_n{n}']={'mean_tv':float(np.mean(vals)),'sd_tv':float(np.std(vals,ddof=1)), 'seeds':len(vals)}
    summary={'kind':'scoreable_toy_candidate','verdict':'toy_pending_independent_review','scope':'Reduced local clean-room Cai--Li Algorithm 1 probability-flow ODE. It uses Eqs. p_hat, score-estimate, score-estimator-X and DDIM update, but K=64, d<=3, n<=2000 and empirical TV estimators deviate radically from the theorem asymptotics.',
      'source_pin':'Cai & Li arXiv:2503.09583 source archive retained at evidence/claim5_attempt1/prior_sources/cai2503.09583.tar.gz; results.tex Eqs. (p_hat), (score-estimate), (soft-thre-defn), (score-estimator-X), Algorithm 1.',
      'assumptions':'Smooth two-component unit-covariance Gaussian mixture; beta=2 toy; target has subgaussian tails. This is not the paper general Holder class proof.',
      'deviations':['K=64 rather than theorem-selected asymptotic K','finite d=1,2,3 and n<=2000','grid KDE TV estimator for d=1,2; histogram proxy separately for d=3','permuting IID KDE training points is intentionally invariant, an implementation invariance check not a destructive performance control'],
      'groups':groups,'elapsed_seconds':time.time()-started,'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'device':'local CPU'}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,required=True); p.add_argument('--seeds',type=int,nargs='+',default=[20261101,20261102,20261103,20261104,20261105]); p.add_argument('--dims',type=int,nargs='+',default=[1,2,3]); p.add_argument('--ns',type=int,nargs='+',default=[250,500,1000,2000]); p.add_argument('--K',type=int,default=64); p.add_argument('--generated',type=int,default=1024); main(p.parse_args())
