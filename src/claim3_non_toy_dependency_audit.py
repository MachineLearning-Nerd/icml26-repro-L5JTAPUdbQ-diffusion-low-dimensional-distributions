#!/usr/bin/env python3
"""Independent executable dependency audit for Claim 3 (local CPU only).

This script does not copy paper code.  It independently checks (i) the
component-count event used in the proof, (ii) the normal/tangent score identity
for a 48-D, 128-component, 3-D union-of-subspaces Gaussian mixture, and (iii)
three assumption-removal controls.  It is evidence about the stated analysis,
not an end-to-end diffusion-training result.
"""
from __future__ import annotations
import argparse, json, math, platform, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parents[1]


def stable_logsumexp(a: np.ndarray, axis: int = -1) -> np.ndarray:
    m = np.max(a, axis=axis, keepdims=True)
    return np.squeeze(m + np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True)), axis=axis)


def make_bases(rng: np.random.Generator, d=48, m=128, k=3) -> np.ndarray:
    # Independent Haar bases: distinct k-subspaces have zero-dimensional
    # intersections almost surely when 2k < d.
    bases = np.empty((m, d, k))
    for i in range(m):
        q, _ = np.linalg.qr(rng.normal(size=(d, k)))
        bases[i] = q[:, :k]
    return bases


def score_identity(seed: int, d=48, m=128, k=3, n_eval=4096, t=0.25) -> dict:
    rng = np.random.default_rng(seed)
    A = make_bases(rng, d, m, k)
    # A full-dimensional Gaussian arises after smoothing a N(A mu, A diag(v) A')
    # component.  This permits an analytic score independent of the decomposition.
    means_low = rng.normal(scale=.7, size=(m, k))
    variances = rng.uniform(.35, 1.1, size=(m, k))
    weights = rng.dirichlet(np.full(m, 3.0))
    covs = np.empty((m, d, d)); invs = np.empty_like(covs); logdets = np.empty(m)
    means = np.einsum('mdk,mk->md', A, means_low)
    for i in range(m):
        covs[i] = t*np.eye(d) + (A[i] * variances[i]) @ A[i].T
        invs[i] = np.linalg.inv(covs[i]); logdets[i] = np.linalg.slogdet(covs[i])[1]
    z = rng.choice(m, size=n_eval, p=weights)
    x = np.empty((n_eval, d))
    for j, c in enumerate(z): x[j] = rng.multivariate_normal(means[c], covs[c])
    diff = x[:, None, :] - means[None, :, :]
    logq = np.log(weights)[None, :] - .5*(d*math.log(2*math.pi)+logdets[None, :] + np.einsum('nmd,mde,nme->nm',diff,invs,diff))
    logp = stable_logsumexp(logq, 1); posterior = np.exp(logq-logp[:,None])
    direct = -np.einsum('nm,mde,nme->nd', posterior, invs, diff)
    # Independently assembled paper-form normal+tangent score.  In the tangent
    # coordinates covariance is diag(v+t), and normal covariance is t I.
    component = np.empty((n_eval,m,d))
    for i in range(m):
        proj = x @ A[i] @ A[i].T
        low = x @ A[i]
        slow = -(low-means_low[i])/(variances[i]+t)
        component[:,i] = -(x-proj)/t + slow @ A[i].T
    decomposed = np.einsum('nm,nmd->nd', posterior, component)
    err = np.linalg.norm(direct-decomposed,axis=1)
    return {"seed":seed,"d":d,"M":m,"k":k,"n_eval":n_eval,"t":t,
            "max_abs_score_identity_error":float(err.max()),"mean_abs_score_identity_error":float(err.mean()),
            "posterior_row_sum_max_error":float(np.abs(posterior.sum(1)-1).max()),
            "generic_subspace_intersection_dimension_upper_bound":max(0,2*k-d)}


def allocation_grid(seed: int, trials=100000) -> tuple[list[dict], dict[str,np.ndarray]]:
    rng=np.random.default_rng(seed); rows=[]; raw={}
    # Exact lower-mass case p_i=1/M, plus a larger-M setting.  The independent
    # Chernoff/union proof is P[min Ni < N/(2cpM)] <= M exp(-N/(8cpM)).
    for M,N,cp in [(8,800,1.),(32,6400,1.),(128,51200,1.)]:
        p=np.full(M,1/M); threshold=N/(2*cp*M)
        counts=rng.multinomial(N,p,size=trials); mins=counts.min(axis=1)
        observed=float(np.mean(mins<threshold)); bound=min(1., M*math.exp(-N/(8*cp*M)))
        key=f'M{M}_N{N}'; raw[key]=mins.astype(np.int16)
        rows.append({"M":M,"N":N,"c_p":cp,"trials":trials,"threshold":threshold,
                     "observed_event_failure_rate":observed,"chernoff_union_upper_bound":bound,
                     "mean_min_component_count":float(mins.mean())})
    # Lower-mass violation: a component has expected five observations but the
    # claimed cp=1 threshold is 195.3.  This is an explicit dependence control.
    M,N=128,50000; p=np.full(M,(1-.0001)/(M-1)); p[0]=.0001
    counts=rng.multinomial(N,p,size=trials); mins=counts.min(1); raw['vanishing_mass_M128_N50000']=mins.astype(np.int16)
    rows.append({"M":M,"N":N,"c_p":1.,"trials":trials,"threshold":N/(2*M),
                 "observed_event_failure_rate":float(np.mean(mins<N/(2*M))),
                 "chernoff_union_upper_bound":"not_applicable_mass_assumption_violated",
                 "mean_min_component_count":float(mins.mean()),"control":"vanishing_component_mass"})
    return rows,raw


def controls(seed: int) -> dict:
    rng=np.random.default_rng(seed)
    # Atom at origin belongs to every linear subspace, so labels are not unique.
    n=100000; atom_prob=.10; atoms=rng.random(n)<atom_prob
    # Student t has no finite psi_2 norm; finite-sample exponential moment gives
    # a visible diagnostic using sigma=2.5, alongside a Gaussian reference.
    sigma=2.5
    normal=rng.normal(size=n); heavy=rng.standard_t(df=3,size=n)
    def empirical_exp(v):
        q=np.clip((v/sigma)**2,0,700); return float(np.mean(np.exp(q)))
    return {"positive_intersection_atom_control":{"n":n,"atom_probability":atom_prob,
             "observed_intersection_mass":float(atoms.mean()),"ambiguous_labels_at_origin":int(atoms.sum()),
             "zero_intersection_condition":False},
            "heavy_tail_control":{"n":n,"distribution":"Student-t(df=3)","sigma_probe":sigma,
             "normal_reference_empirical_mgf":empirical_exp(normal),"student_t_empirical_mgf":empirical_exp(heavy),
             "subgaussian_condition_certified":False,
             "note":"Student-t(df=3) has no finite exponential-square moment; finite sample statistic is diagnostic only."}}


def main():
 p=argparse.ArgumentParser(); p.add_argument('--seed',type=int,default=20260830); p.add_argument('--trials',type=int,default=100000); a=p.parse_args()
 start=time.time(); ident=score_identity(a.seed); alloc,raw=allocation_grid(a.seed+1,a.trials); ctrl=controls(a.seed+2)
 out=ROOT/'outputs'/'claim3_fullscale'; out.mkdir(parents=True,exist_ok=True)
 np.savez_compressed(out/'allocation_raw_min_counts.npz',**raw)
 result={"protocol":"independent local CPU Claim 3 dependency and identity audit","source_dependency_map":{
  "component_mass_to_count_event":"pf-of-theorems.tex:4-17; pf-of-lemmas.tex:95-104", "zero_intersection_to_labeling":"pf-of-lemmas.tex:85-93", "subgaussian_to_tail_bound":"Auxiliary_lemmas.tex:3-12; pf-of-theorems.tex:102", "normal_tangent_score":"Results.tex:37-61"},
  "allocation_derivation":"For Ni~Bin(N,pi), pi>=1/(cp M), Chernoff P[Ni < N/(2cpM)] <= exp(-N/(8cpM)); union bound gives M exp(-N/(8cpM)).",
  "score_identity":ident,"allocation_grid":alloc,"assumption_removal_controls":ctrl,
  "environment":{"python":sys.version,"numpy":np.__version__,"platform":platform.platform(),"runtime_seconds":time.time()-start},
  "verdict":"inconclusive","scope":"Non-toy d=48/M=128/k=3 executable identities and 100k-trial concentration checks independently support specific proof dependencies, but do not independently prove the entire theorem."}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
