import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from claim1_reverse_diffusion import sliced_w1

def test_sliced_w1_zero_for_identical_samples():
    x=np.array([[0.,1.],[2.,3.],[4.,5.]],dtype='float32')
    assert sliced_w1(x,x,4,16)==0.

def test_sliced_w1_detects_translation():
    x=np.zeros((32,3),dtype='float32'); y=x.copy(); y[:,0]=2.
    assert sliced_w1(x,y,9,128)>0.2
