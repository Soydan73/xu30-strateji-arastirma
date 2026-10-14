# HK-20261014-18 — dVPOC sabah göçü → öğleden sonra aynı yön (yalnız sinyal)
import numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vp_profil import gelisen_profil

def sinyal(s, oran=0.0, t0=600, t1=630, t2=690):
    n = len(s); out = np.zeros(n); dk = s.dk.to_numpy()
    i2 = np.flatnonzero(dk == t2)
    if not len(i2): return out
    i2 = i2[0]
    i0 = np.flatnonzero(dk[:i2 + 1] == t0); i1 = np.flatnonzero(dk[:i2 + 1] == t1)
    if not len(i0) or not len(i1): return out
    poc, _, _ = gelisen_profil(s.iloc[:i2 + 1])     # yalnız 11:30'a kadarki barlar
    d1 = poc[i1[0]] - poc[i0[0]]; d2 = poc[i2] - poc[i0[0]]
    th = oran * s.close.iloc[i2]
    if oran == 0:
        if d1 > 0 and d2 > 0: out[i2] = 1
        elif d1 < 0 and d2 < 0: out[i2] = -1
    else:
        if d1 >= th and d2 >= th: out[i2] = 1
        elif d1 <= -th and d2 <= -th: out[i2] = -1
    return out
