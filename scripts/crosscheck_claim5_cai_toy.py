#!/usr/bin/env python3
"""Independent raw-sample histogram crosscheck for the Claim-5 TV toy."""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).parents[1]; OUT=ROOT/'outputs/claim5_cai_probability_flow_tv_toy'
def htv(a,b,d):
    e=[np.linspace(-5,5,17)]*d
    x,_=np.histogramdd(a,bins=e); y,_=np.histogramdd(b,bins=e)
    return float(.5*np.abs(x/len(a)-y/len(b)).sum())
rows=[]
for f in sorted(OUT.glob('seed*_d*_n*.npz')):
    z=np.load(f); d=z['generated'].shape[1]
    rows.append({'file':f.name,'d':d,'generated_vs_target_hist_tv':htv(z['generated'],z['target_a'],d),
                 'target_vs_target_hist_tv':htv(z['target_a'],z['target_b'],d),
                 'generated_max_abs':float(np.abs(z['generated']).max())})
result={'method':'independent raw-sample fixed-bin histogram-TV crosscheck; distinct from primary d=1/2 KDE-grid quadrature', 'rows':rows,
        'all_generated_escape_target_grid':all(r['generated_max_abs']>5 for r in rows)}
(OUT/'independent_histogram_crosscheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cells':len(rows),'all_generated_escape_target_grid':result['all_generated_escape_target_grid']}))
