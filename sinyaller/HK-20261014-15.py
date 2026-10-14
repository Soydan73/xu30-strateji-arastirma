# HK-20261014-15 — göreli işaretli sıçrama varyasyonu (RSJ) dönüşü (yalnız sinyal)
import numpy as np

def sinyal(s, T=720, teta=0.0):
    out = np.zeros(len(s)); dk = s.dk.to_numpy()
    m = np.flatnonzero(dk >= 570); b = np.flatnonzero(dk == T - 1)
    if not len(m) or not len(b) or b[0] < m[0] + 2:
        return out
    c = s.close.to_numpy(float); o = s.open.to_numpy(float)
    r = np.diff(np.log(c[m[0]:b[0] + 1]), prepend=np.log(o[m[0]]))
    rp = (r[r > 0] ** 2).sum(); rn = (r[r < 0] ** 2).sum()
    if rp + rn <= 0:
        return out
    rsj = (rp - rn) / (rp + rn)
    if rsj != 0 and abs(rsj) >= teta:
        out[b[0]] = -np.sign(rsj)
    return out
