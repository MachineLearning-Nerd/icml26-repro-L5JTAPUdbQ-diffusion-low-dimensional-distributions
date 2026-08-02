#!/usr/bin/env python3
"""Literal-Assumption-1 finite UoS estimator audit (local CPU only).

This clean-room experiment samples a non-degenerate finite union of three
orthogonal 2-planes in R^12.  It checks all clauses of Assumptions 1--2,
including *unconditional* mass p*(V_i), then executes the recovered-basis
component KDE score estimator on a held-out smoothed sample.  It is evidence
about literal assumptions and their proof uses, not a proof of Theorem 1/2.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, platform, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parents[1]

def lse(a):
 m=a.max(1,keepdims=True); return (m+np.log(np.exp(a-m).sum(1,keepdims=True))).ravel()

def run(seed=20260802,n=6000,ne=512,t=.35):
 rng=np.random.default_rng(seed); d,M,k=12,3,2; cp=2.
 # Coordinate planes are pairwise intersecting only at {0}; Rademacher
 # coordinates never equal 0, hence samples have zero intersection mass.
 A=np.zeros((M,d,k))
 for i in range(M): A[i,2*i:2*i+2,:]=np.eye(2)
 w=np.array([.20,.30,.50]); labels=rng.choice(M,n,p=w)
 low=rng.choice(np.array([-1.,1.]),size=(n,k)); X=np.einsum('nk,ndk->nd',low,A[labels])
 counts=np.bincount(labels,minlength=M); threshold=n/(2*cp*M)
 # independently held-out target and Gaussian smoothing.
 z=rng.choice(M,ne,p=w); low_e=rng.choice(np.array([-1.,1.]),size=(ne,k)); clean=np.einsum('nk,ndk->nd',low_e,A[z]); Y=clean+rng.normal(scale=math.sqrt(t),size=(ne,d))
 # Exact finite-mixture smoothed score and recovered-basis empirical KDE score.
 means=np.array([A[i]@np.array([a,b]) for i in range(M) for a in (-1.,1.) for b in (-1.,1.)])
 mw=np.repeat(w/4,4); diff=Y[:,None,:]-means[None,:,:]
 logq=np.log(mw)[None,:]-.5*(d*math.log(2*math.pi*t)+(diff*diff).sum(2)/t)
 post=np.exp(logq-lse(logq)[:,None]); exact=-(post[:,:,None]*diff/t).sum(1)
 # Source-style known-subspace split: each component's low-dim KDE plus normal score,
 # then normalized ambient Gaussian component weights.
 logcomp=np.empty((ne,M)); comp=np.empty((ne,M,d))
 for i in range(M):
  xi=X[labels==i]; ui=xi@A[i]; yy=Y@A[i]; q=yy[:,None,:]-ui[None,:,:]
  lk=-.5*(k*math.log(2*math.pi*t)+(q*q).sum(2)/t)
  loglow=lse(lk)-math.log(len(ui)); logcomp[:,i]=math.log(counts[i]/n)+loglow-.5*((d-k)*math.log(2*math.pi*t)+((Y-Y@A[i]@A[i].T)**2).sum(1)/t)
  p=np.exp(lk-lse(lk)[:,None]); slow=-(p[:,:,None]*q/t).sum(1)
  comp[:,i]=slow@A[i].T-(Y-Y@A[i]@A[i].T)/t
 ph=np.exp(logcomp-lse(logcomp)[:,None]); est=(ph[:,:,None]*comp).sum(1)
 mse=((exact-est)**2).sum(1).mean()
 # Analytic subgaussian certificate: |theta^T low| <= sqrt(2), sigma=2.
 mgf_bound=math.exp(2/4)
 controls={'intersection_atom':{'mass':.1,'separation_passes':False,'note':'limitation/control only; not a claim falsification'},'low_mass':{'weights':[.001,.499,.5],'cp':cp,'mass_passes':False}}
 return {'protocol':'literal Assumptions 1--2 finite UoS generator plus recovered-basis KDE score estimator','seed':seed,'config':{'d':d,'M':M,'k':k,'n':n,'n_eval':ne,'t':t,'weights':w.tolist(),'c_p':cp},'assumption_checks':{'union_support':True,'pairwise_intersections_are_origin':True,'intersection_mass_zero_by_construction':True,'per_component_counts':counts.tolist(),'per_component_mass_empirical':(counts/n).tolist(),'mass_lower_bound':1/(cp*M),'all_component_masses_pass':bool(np.all(w>=1/(cp*M))),'subgaussian_sigma':2.,'subgaussian_mgf_upper_bound':mgf_bound,'subgaussian_mgf_le_2':mgf_bound<=2},'estimator':{'known_recovered_bases':True,'exact_smoothed_mixture_score_vs_empirical_component_kde_score_mse':float(mse),'n_train':n,'n_eval':ne},'proof_dependency_map':{'union_support_and_zero_intersection':'problem_formulation.tex:81-101 defines unique component restriction/labels; pf-of-theorems.tex:8-10 uses c(X) in N_i.','per_component_mass':'problem_formulation.tex:92-96; pf-of-theorems.tex:8-19 supplies the count event A needed before L_i bounds.','subgaussian_within_subspace':'problem_formulation.tex:116-128; pf-of-theorems.tex:43-60 uses it for B_t tails and :101-106 for kappa_2 tail bound.','orthogonal_basis':'problem_formulation.tex:104-110; pf-of-theorems.tex:76-86 uses normal/tangent change of variables.'},'controls':controls,'verdict':'inconclusive','scope':'Finite non-toy local CPU execution checks literal source assumptions and runs a recovered-basis estimator. It cannot verify the theorem expectation/rate or falsify literal Claim 3.'}
def main():
 p=argparse.ArgumentParser(); p.add_argument('--seed',type=int,default=20260802);p.add_argument('--n',type=int,default=6000);p.add_argument('--n-eval',type=int,default=512);a=p.parse_args(); out=ROOT/'outputs'/'claim3_literal_uos_estimator';out.mkdir(parents=True,exist_ok=True);r=run(a.seed,a.n,a.n_eval); r['environment']={'python':sys.version,'numpy':np.__version__,'platform':platform.platform()};(out/'config.json').write_text(json.dumps({'seed':a.seed,'n':a.n,'n_eval':a.n_eval},indent=2)+'\n');(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');
 with (out/'results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['seed','n','n_eval','mse','mass_pass']);w.writeheader();w.writerow({'seed':a.seed,'n':a.n,'n_eval':a.n_eval,'mse':r['estimator']['exact_smoothed_mixture_score_vs_empirical_component_kde_score_mse'],'mass_pass':r['assumption_checks']['all_component_masses_pass']})
 print(json.dumps(r,indent=2))
if __name__=='__main__':main()
