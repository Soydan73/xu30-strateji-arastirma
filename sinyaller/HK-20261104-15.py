# HK-20261104-15 — Gece boslugu (g) ve dunku gunduz getirisi (r_dun) isaretine gore bugun 09:46 -> 18:05.
# Fiyat duzeyi: yalniz ayni_vade dunku seans. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, onceki, bilgi, mod="ters", kosul="yok", esik=0.0, kontrol=False, H=400):
    n = len(s); out = np.zeros(n)
    if n < 1:
        return out
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk >= 585)
    if not len(idx):
        return out
    i = int(idx[0])
    o0 = float(s.open.iloc[0])
    if kontrol:
        onc = np.flatnonzero(dk[:i + 1] < 585)
        if not len(onc):
            return out
        r = float(s.close.iloc[int(onc[-1])]) - o0
        if r != 0:
            out[i] = -np.sign(r)
        return out
    if len(onceki) < 1 or not bool(bilgi["ayni_vade"][-1]):
        return out
    d = onceki[-1]
    c1 = float(d.close.iloc[-1]); o1 = float(d.open.iloc[0])
    r_dun = c1 - o1
    g = o0 - c1
    if mod == "momentum":
        if r_dun != 0:
            out[i] = np.sign(r_dun)
        return out
    if g == 0:
        return out
    if kosul == "ayni" and not (np.sign(g) == np.sign(r_dun) and r_dun != 0):
        return out
    if kosul == "farkli" and not (np.sign(g) != np.sign(r_dun) and r_dun != 0):
        return out
    if abs(g) < esik * c1:
        return out
    out[i] = -np.sign(g)
    return out
