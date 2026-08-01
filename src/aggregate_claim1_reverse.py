#!/usr/bin/env python3
"""Deterministically rebuild Claim 1's checked summary from raw JSON rows."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

def build(out: Path) -> dict:
    # Run logs are immutable per invocation and retain the otherwise overwritten
    # seed/step configurations; results.csv is the raw row ledger.
    rows=[]
    for p in sorted(out.glob('run_*.log')):
        row=json.loads(p.read_text())
        for key in ('seed','N','d','M','k','sliced_w1','target_split_sliced_w1','wrong_bases','schedule'):
            assert key in row, (p,key)
        rows.append(row)
    assert len(rows)==9, f'expected nine retained invocation logs, found {len(rows)}'
    chosen=[r for r in rows if r['N']==50000 and r['schedule']['steps']==16 and not r['wrong_bases']]
    assert len(chosen)==3, 'expected three N=50k/16-step/matched-basis invocation logs'
    vals=np.array([r['sliced_w1'] for r in chosen],dtype=float)
    ratios=np.array([r['ratio_to_mc_floor'] for r in chosen],dtype=float)
    result={
      'protocol': {'d':48,'M':128,'k':3,'N_values':sorted({r['N'] for r in rows}),
        'T':'log N','tau':'N^(-2/k)','sampler':'Euler-Maruyama reverse OU SDE with Eq. (8)-(14) clean-room KDE score',
        'metric':'64-projection sliced W1 plus held-out target-split floor'},
      'rows':len(rows),'full_N50000_steps16_seeds':[r['seed'] for r in chosen],
      'full_N50000_steps16_mean_sliced_w1':float(vals.mean()),
      'full_N50000_steps16_sd_sliced_w1':float(vals.std(ddof=1)),
      'full_N50000_steps16_mean_ratio_to_target_split_floor':float(ratios.mean()),
      'interpretation':'The full-scale Euler implementation is numerically unstable/poor and does not demonstrate convergence. This finite practical-sampler failure cannot falsify Theorem 2 because the paper proves an idealized continuous-time process and explicitly defers discretization error.'}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='outputs/claim1_reverse_full'); ap.add_argument('--write',action='store_true')
    a=ap.parse_args(); out=Path(a.out); result=build(out)
    rendered=json.dumps(result,indent=2)+'\n'
    if a.write: (out/'summary.json').write_text(rendered)
    else: print(rendered,end='')
if __name__=='__main__': main()
