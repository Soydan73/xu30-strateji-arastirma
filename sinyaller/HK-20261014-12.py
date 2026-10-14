# HK-20261014-12 — seans içi filtre kuralı, aralık oynaklığı koşullu (yalnız sinyal)
import numpy as np

def sinyal(s, k=10.0, q=None):
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    rng = (s.high.to_numpy(float) - s.low.to_numpy(float))
    out = np.zeros(len(s))
    m = np.flatnonzero(dk >= 570)
    if not len(m):
        return out
    cs = np.cumsum(rng[m[0]:]); A = np.full(len(s), np.nan)
    A[m[0]:] = cs / np.arange(1, len(cs) + 1)
    yon = 0; dip = tepe = None
    for i in range(len(s)):
        if dk[i] < 599:
            continue
        if dip is None:                 # 09:59 barı (ya da ilk ≥ 599 bar) başlangıç
            dip = tepe = c[i]
            continue
        X = k * A[i]
        kos = True if q is None else (A[i] / c[i] * 1e4 >= q)
        if yon <= 0 and c[i] >= dip + X:
            yon = 1; tepe = c[i]
            if kos: out[i] = 1
        elif yon >= 0 and c[i] <= tepe - X:
            yon = -1; dip = c[i]
            if kos: out[i] = -1
        else:
            if yon == 1: tepe = max(tepe, c[i])
            elif yon == -1: dip = min(dip, c[i])
            else: tepe = max(tepe, c[i]); dip = min(dip, c[i])
    return out
