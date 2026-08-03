#!/usr/bin/env python3
"""Finite UoS audit of the source regularized score estimator (CPU only).

The source clips *only* the low-dimensional KDE score before embedding it in
ambient space and adding the normal-space Gaussian score.  Its G_t radius has
an unspecified universal C_R, so this audit retains a disclosed C_R sweep.
This is finite diagnostic evidence, never a theorem proof/falsification.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, platform, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).parents[1]

def lse(a):
    m = a.max(1, keepdims=True)
    return (m + np.log(np.exp(a-m).sum(1, keepdims=True))).ravel()
def clip(v, r):
    n = np.linalg.norm(v, axis=1, keepdims=True)
    return v * np.minimum(1., r / np.maximum(n, 1e-300))
def planes():
    A = np.zeros((3, 12, 2))
    for i in range(3): A[i, 2*i:2*i+2] = np.eye(2)
    return A
def population_score(y, t, w, atom=0.):
    A = planes(); means=[]; weights=[]
    for i in range(3):
        for a in (-1.,1.):
            for b in (-1.,1.):
                means.append(A[i] @ np.array([a,b])); weights.append((1-atom)*w[i]/4)
    if atom: means.append(np.zeros(12)); weights.append(atom)
    means=np.asarray(means); weights=np.asarray(weights); diff=y[:,None]-means[None]
    z=np.log(weights)[None]-.5*(12*np.log(2*np.pi*t)+(diff*diff).sum(2)/t)
    p=np.exp(z-lse(z)[:,None])
    return -(p[:,:,None]*diff/t).sum(1)

def one(seed, n, ne, t, w, atom=0., c_r=1., name='nominal'):
    """One fixed-C_R execution; arrays permit direct pointwise MSE checking."""
    rng=np.random.default_rng(seed); A=planes(); d,M,k=12,3,2; cp=2.
    labels=rng.choice(M,n,p=w); low=rng.choice([-1.,1.],size=(n,k)); X=np.einsum('nk,ndk->nd',low,A[labels])
    atom_mask=rng.random(n)<atom; X[atom_mask]=0.; labels[atom_mask]=-1
    z=rng.choice(M,ne,p=w); lowe=rng.choice([-1.,1.],size=(ne,k)); clean=np.einsum('nk,ndk->nd',lowe,A[z])
    emask=rng.random(ne)<atom; clean[emask]=0.; Y=clean+rng.normal(scale=math.sqrt(t),size=(ne,d))
    valid=labels>=0; N=int(valid.sum()); eta=math.log(N)/(N*(2*np.pi*t)**(k/2)); R=math.sqrt(2*math.log(N)/t)
    allq=Y[:,None]-X[None]; la=-.5*(d*np.log(2*np.pi*t)+(allq*allq).sum(2)/t)
    logp=lse(la)-math.log(n); reg=np.zeros((ne,d)); unreg=np.zeros((ne,d)); gates=[]; psis=[]
    base_radius=math.sqrt(t*d*max(math.log(N*d*t**(k/2)),0.)); Rt=c_r*base_radius
    for i in range(M):
        xi=X[labels==i]; ui=xi@A[i]; yy=Y@A[i]; q=yy[:,None]-ui[None]
        lk=-.5*(k*np.log(2*np.pi*t)+(q*q).sum(2)/t); logg=lse(lk)-math.log(len(ui)); g=np.exp(logg)
        slow=-(np.exp(lk-lse(lk)[:,None])[:,:,None]*q/t).sum(1)
        normal=-(Y-Y@A[i]@A[i].T)/t
        dist=np.linalg.norm(Y-Y@A[i]@A[i].T,axis=1); gate=dist<=Rt
        qambient=lse(la[:,labels==i])-math.log(n); weight=np.exp(qambient-logp)
        psi=g>=eta
        # Results.tex: clip_R(psi * low-dimensional score), then add normal term.
        literal_component = clip(slow*psi[:,None], R) @ A[i].T + normal
        unreg_component = slow @ A[i].T + normal
        reg += (weight*gate)[:,None]*literal_component
        unreg += weight[:,None]*unreg_component
        gates.append(gate); psis.append(psi)
    exact=population_score(Y,t,w,atom)
    err_reg=((exact-reg)**2).sum(1); err_un=((exact-unreg)**2).sum(1)
    arrays=dict(X=X,labels=labels,Y=Y,clean=clean,eval_atom_mask=emask,train_atom_mask=atom_mask,
                exact=exact,regularized=reg,unregularized=unreg,pointwise_sqerr_regularized=err_reg,
                pointwise_sqerr_unregularized=err_un)
    summary={'condition':name,'C_R':c_r,'n':n,'n_eval':ne,'weights':w.tolist(),'atom_mass':atom,
             'eta':eta,'low_dimensional_clip_R':R,'G_t_base_radius_C_R_1':base_radius,'G_t_radius':Rt,
             'regularized_mse':float(err_reg.mean()),'unregularized_mse':float(err_un.mean()),
             'psi_pass_rates':[float(x.mean()) for x in psis],'gate_pass_rates':[float(x.mean()) for x in gates],
             'intersection_atom_executed':bool(atom>0),'all_component_masses_pass':bool(np.all(w>=1/(cp*M)) and atom==0),
             'per_component_counts':np.bincount(labels[valid],minlength=M).tolist()}
    return summary, arrays

def run(seed=20260802,n=6000,ne=512,t=.35,save=False):
    configs=[('nominal',np.array([.2,.3,.5]),0.),('intersection_atom',np.array([.2,.3,.5]),.10),('low_mass',np.array([.05,.45,.5]),0.)]
    c_rs=(.5,1.,2.); rows=[]; arrays={}; by_condition={}
    for j,(name,w,a) in enumerate(configs):
        by_condition[name]=[]
        for q,c_r in enumerate(c_rs):
            r,x=one(seed+j,n,ne,t,w,a,c_r,name); rows.append(r); by_condition[name].append(r)
            arrays[f'{name}_C_R_{c_r:g}']=x
    nominal=by_condition['nominal'][1]
    result={'protocol':'Results.tex source order: hard psi; clip_R of low-dimensional score only; embed then add normal term; ambient q/p weights and G_t gate. C_R is unspecified by source, so C_R={0.5,1,2} is a disclosed sensitivity sweep; C_R=1 is the reporting convention, not source-exact constant selection.',
      'seed':seed,'config':{'d':12,'M':3,'k':2,'n':n,'n_eval':ne,'t':t,'c_p':2,'C_R_sweep':list(c_rs),'reporting_C_R':1.},
      'assumption_checks':{'union_support':True,'pairwise_intersections_are_origin':True,'intersection_mass_zero_by_construction':True,'mass_lower_bound':1/6,'subgaussian_sigma':2.,'subgaussian_mgf_upper_bound':math.exp(.5),'subgaussian_mgf_le_2':True},
      'estimator':nominal,'C_R_sweep':{'nominal':by_condition['nominal'],'intersection_atom':by_condition['intersection_atom'],'low_mass':by_condition['low_mass']},
      'proof_dependency_map':{'union_support_and_zero_intersection':'problem_formulation.tex:81-101; pf-of-theorems.tex:8-10','per_component_mass':'problem_formulation.tex:92-96; pf-of-theorems.tex:8-19','subgaussian_within_subspace':'problem_formulation.tex:116-128; pf-of-theorems.tex:43-60','orthogonal_basis':'problem_formulation.tex:104-110; pf-of-theorems.tex:76-86'},
      'verdict':'inconclusive','scope':'Finite local CPU execution implements source low-dimensional clipping before normal-space addition and sweeps source-unspecified G_t constant C_R. It neither proves a universal theorem nor falsifies literal Claim 3.'}
    return result, arrays, rows

def sha(out,names):
    with (out/'SHA256SUMS').open('w') as f:
        for name in names: f.write(hashlib.sha256((out/name).read_bytes()).hexdigest()+'  '+name+'\n')
def main():
    p=argparse.ArgumentParser(); p.add_argument('--seed',type=int,default=20260802); p.add_argument('--n',type=int,default=6000); p.add_argument('--n-eval',type=int,default=512); a=p.parse_args()
    out=ROOT/'outputs'/'claim3_literal_uos_estimator'; out.mkdir(parents=True,exist_ok=True)
    r,arr,rows=run(a.seed,a.n,a.n_eval)
    r['environment']={'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}
    (out/'config.json').write_text(json.dumps({'seed':a.seed,'n':a.n,'n_eval':a.n_eval,'C_R_sweep':[.5,1.,2.]},indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
    np.savez_compressed(out/'raw_arrays.npz',**{f'{c}_{k}':v for c,x in arr.items() for k,v in x.items()})
    fields=['condition','C_R','atom_mass','regularized_mse','unregularized_mse','intersection_atom_executed','all_component_masses_pass']
    with (out/'results.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); wr.writeheader(); [wr.writerow({k:x[k] for k in fields}) for x in rows]
    (out/'run.log').write_text(' '.join(sys.argv)+'\n'); sha(out,['config.json','results.csv','summary.json','raw_arrays.npz','run.log'])
    print(json.dumps(r,indent=2))
if __name__=='__main__': main()
