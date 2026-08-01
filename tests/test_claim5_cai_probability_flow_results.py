import csv, json
from pathlib import Path

ROOT=Path(__file__).parents[1]
OUT=ROOT/'outputs/claim5_cai_probability_flow_tv_toy'

def test_raw_grid_is_complete_and_summary_matches_rows():
    rows=list(csv.DictReader((OUT/'results.csv').open()))
    assert len(rows)==5*3*4
    summary=json.loads((OUT/'summary.json').read_text())
    assert summary['kind']=='scoreable_toy_candidate'
    for d in (1,2,3):
        for n in (250,500,1000,2000):
            key=f'd{d}_n{n}'; vals=[float(r['tv']) for r in rows if int(r['d'])==d and int(r['n'])==n]
            assert len(vals)==5
            assert abs(sum(vals)/len(vals)-summary['groups'][key]['mean_tv']) < 1e-12

def test_primary_artifacts_are_present_for_every_cell():
    for seed in (20261101,20261102,20261103,20261104,20261105):
        for d in (1,2,3):
            for n in (250,500,1000,2000):
                assert (OUT/f'seed{seed}_d{d}_n{n}.npz').is_file()
