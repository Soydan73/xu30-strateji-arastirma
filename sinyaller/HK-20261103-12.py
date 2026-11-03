# HK-20261103-12 — Dünün son 3 (2) saatinin tersine bugün T'de gir, 18:05'e kadar tut (motor_cok).
# Yalniz onceki[-1] fiyat getirisi (tek seans ici, vade gecisinden etkilenmez); esik tabani onceki 20 seans |R|.
# Egitim YOK. i. bar icin yalniz s.iloc[:i+1] kullanilir (sinyal yalniz T-1 barinda, bilgi yalniz onceki'den).
import numpy as np


def _R(p, bas):
    c = p.close.to_numpy(float); dk = p.dk.to_numpy()
    i0 = np.flatnonzero(dk <= bas - 1); i1 = np.flatnonzero(dk <= 1085)
    if not len(i0) or not len(i1) or i1[-1] <= i0[-1]:
        return np.nan
    return c[i1[-1]] / c[i0[-1]] - 1.0


def sinyal(s, onceki, bilgi, T=905, dun_bas=905, esik=None, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    j = np.flatnonzero(dk == T - 1)
    if not len(j):
        return out
    j = j[0]
    if kontrol:
        out[j] = 1
        return out
    if not len(onceki):
        return out
    R = _R(onceki[-1], dun_bas)
    if not np.isfinite(R) or R == 0:
        return out
    if esik is not None:
        if len(onceki) < 20:
            return out
        taban = np.array([_R(p, dun_bas) for p in onceki[-20:]])
        taban = np.abs(taban[np.isfinite(taban)])
        if len(taban) < 20:
            return out
        if abs(R) < np.percentile(taban, esik):
            return out
    out[j] = -np.sign(R)
    return out
