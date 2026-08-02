#!/usr/bin/env python3
"""C1 alternate route: coupled 1-D hard-threshold KDE reverse-SDE check.

This is deliberately not the earlier d=48 Euler sampler.  It uses the paper's
KDE threshold form on a d=k=M=1 standard-normal (hence subgaussian, single
subspace) target.  Euler and stochastic-Heun paths share Brownian increments
with a fine Euler reference.  It can diagnose numerical stability, but cannot
prove or disprove Theorem 2's expectation/rate statement.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def kde_score_hard(x, train, h):
    """Eq.-style 1-D Gaussian KDE score, hard zero below eta, then clipped."""
    t=max(h, 1e-300); z=(x[:,None]-train[None,:])
    ker=np.exp(-0.5*z*z/t)
    den=ker.sum(1)
    # normalized KDE and source schedule eta=log(N)/(N sqrt(2 pi h)).
    g=den/(len(train)*np.sqrt(2*np.pi*t))
    raw=-(ker*z).sum(1)/(t*np.maximum(den,1e-300))
    eta=np.log(len(train))/(len(train)*np.sqrt(2*np.pi*t))
    thresholded=np.where(g>=eta,raw,0.0)
    R=np.sqrt(2*np.log(len(train))/t)
    return np.clip(thresholded,-R,R), g, eta

def drift(y, train, s):
    # Forward OU time s; h=(1-e^-2s)/e^-2s and score_X(y)=score_h(y/e^s)/e^s.
    c=np.exp(-s); h=np.expm1(2*s)
    sc, g, eta=kde_score_hard(y/c,train,h)
    return y+2*sc/c, g, eta

def integrate(train, y0, increments, T, tau, method):
    """Reverse-time r integrator, where forward time is s=T-r."""
    y=y0.copy(); L=len(increments); dt=(T-tau)/L; crossings=0; max_jump=0.
    for j,dw in enumerate(increments):
        s=T-j*dt; b,g,eta=drift(y,train,s)
        # Count cells close enough to the discontinuity to make a direct audit.
        crossings += int(np.count_nonzero(np.abs(g-eta) <= max(1e-12,eta*1e-3)))
        if method=='euler': y=y+b*dt+np.sqrt(2.)*dw
        elif method=='heun':
            yp=y+b*dt+np.sqrt(2.)*dw
            bp,_,_=drift(yp,train,max(tau,s-dt))
            max_jump=max(max_jump,float(np.max(np.abs(bp-b))))
            y=y+0.5*(b+bp)*dt+np.sqrt(2.)*dw
        else: raise ValueError(method)
    return y, {'near_threshold_evaluations':crossings,'max_adjacent_drift_change':max_jump,'dt':dt}

def w1(a,b): return float(np.mean(np.abs(np.sort(a)-np.sort(b))))
def main():
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=512);p.add_argument('--particles',type=int,default=64);p.add_argument('--fine-steps',type=int,default=2048);p.add_argument('--coarse-steps',type=int,default=256);p.add_argument('--seed',type=int,default=20260802);p.add_argument('--out',default='outputs/claim1_threshold_stability_1d_toy');a=p.parse_args()
 if a.fine_steps%a.coarse_steps: raise ValueError('fine-steps must divide coarse-steps')
 # Pre-registered acceptance thresholds: both coarse integrators must be within
 # 0.15 W1 of coupled fine reference; their mutual W1 <= .15.  These diagnose
 # this finite fixture only, and are not a theorem-rate threshold.
 prereg={'target':'N(0,1), d=k=M=1 (subgaussian theorem-domain fixture)','tolerances':{'euler_to_reference_w1_max':0.15,'heun_to_reference_w1_max':0.15,'euler_heun_w1_max':0.15},'reference':'Euler-Maruyama with fine_steps','controls':'shared Brownian path; threshold-adjacency count; unthresholded score is intentionally not substituted'}
 r=np.random.default_rng(a.seed); train=r.normal(size=a.n); y0=r.normal(size=a.particles)
 T=float(np.log(a.n)); tau=float(a.n**-2); q=a.fine_steps//a.coarse_steps; dtfine=(T-tau)/a.fine_steps
 fine_dw=r.normal(scale=np.sqrt(dtfine),size=(a.fine_steps,a.particles))
 ref, refdiag=integrate(train,y0,fine_dw,T,tau,'euler')
 coarse_dw=fine_dw.reshape(a.coarse_steps,q,a.particles).sum(1)
 eu, eudiag=integrate(train,y0,coarse_dw,T,tau,'euler')
 he, hediag=integrate(train,y0,coarse_dw,T,tau,'heun')
 metrics={'euler_to_fine_w1':w1(eu,ref),'heun_to_fine_w1':w1(he,ref),'euler_to_heun_w1':w1(eu,he),'fine_to_target_empirical_w1':w1(ref,r.normal(size=a.particles))}
 passes=all(metrics[k]<=v for k,v in [('euler_to_fine_w1',.15),('heun_to_fine_w1',.15),('euler_to_heun_w1',.15)])
 # Mathematical limitation: at g=eta hard selection switches raw score to 0.
 # A generic sample has nonzero raw score at that surface, so drift is not globally
 # Lipschitz; standard strong-error theorem cannot be invoked from this audit.
 conclusion=('inconclusive: coupled finite fixture meets preregistered stability tolerances but hard threshold is discontinuous, so this does not establish a uniform finite-time error bound or Theorem 2; no theorem-domain counterexample is demonstrated.' if passes else 'inconclusive: the independently coupled Euler and stochastic-Heun coarse paths fail the preregistered finite-fixture stability tolerances against the fine Euler reference. This numerical discrepancy plus hard-threshold discontinuity is not a defensible counterexample to the idealized theorem; no theorem-domain counterexample is demonstrated.')
 out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
 rec={'config':vars(a),'preregistration':prereg,'schedule':{'T':T,'tau':tau},'metrics':metrics,'passes_fixture_tolerances':passes,'diagnostics':{'fine':refdiag,'euler':eudiag,'heun':hediag},'derivation':{'reverse_drift':'b_r(y)=y+2 score_{X_s}(y), s=T-r; score_{X_s}(y)=exp(-s)^{-1} score_h(exp(s)y), h=exp(2s)-1','threshold_discontinuity':'At g_h(u)=eta_h, estimator changes from raw KDE score to 0. Unless raw score is zero on that surface, drift is discontinuous. Thus a global-Lipschitz Euler/Heun strong-error certificate is unavailable without an additional argument.'},'verdict':'inconclusive','conclusion':conclusion,'runtime':{'python':platform.python_version(),'device':'local CPU numpy'}}
 np.savez_compressed(out/'raw_paths.npz',train=train,y0=y0,fine_reference=ref,euler=eu,heun=he,fine_increments=fine_dw)
 (out/'PROTOCOL.json').write_text(json.dumps(prereg,indent=2)+'\n');(out/'summary.json').write_text(json.dumps(rec,indent=2)+'\n')
 with open(out/'results.csv','w',newline='') as f: csv.DictWriter(f,fieldnames=metrics.keys()).writeheader();csv.DictWriter(f,fieldnames=metrics.keys()).writerow(metrics)
 (out/'run.log').write_text(' '.join(__import__('sys').argv)+'\n'+json.dumps(rec,indent=2)+'\n')
 files=['PROTOCOL.json','summary.json','results.csv','run.log','raw_paths.npz'];(out/'SHA256SUMS').write_text(''.join(hashlib.sha256((out/x).read_bytes()).hexdigest()+'  '+x+'\n' for x in files))
 print(json.dumps(rec,indent=2))
if __name__=='__main__': main()
