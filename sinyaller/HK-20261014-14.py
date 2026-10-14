# HK-20261014-14 — asimetrik dönüş: düşen M30 sonrası uzun, seans oynaklığı koşullu (yalnız sinyal)
import numpy as np

def sinyal(s, teta=0.1794, q=None):
    out = np.zeros(len(s)); dk = s.dk.to_numpy()
    c = s.close.to_numpy(float); o = s.open.to_numpy(float)
    m = np.flatnonzero(dk >= 570)
    if not len(m):
        return out
    lr = np.diff(np.log(c[m[0]:]), prepend=np.log(o[m[0]]))
    for T in range(600, 1051, 30):
        b = np.flatnonzero(dk == T - 1); a = np.flatnonzero(dk == T - 30)
        if not len(a) or not len(b):
            continue
        r = (c[b[0]] / o[a[0]] - 1) * 100
        if r > -teta:
            continue
        if q is not None:
            k = b[0] - m[0] + 1
            if k < 3 or np.std(lr[:k], ddof=1) * 1e4 < q:
                continue
        out[b[0]] = 1
    return out
