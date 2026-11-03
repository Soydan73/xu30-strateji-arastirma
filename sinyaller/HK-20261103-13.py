# HK-20261103-13 — CGW kati surum: ayni 30 dk diliminin onceki 20 seans hacim ortalamasina gore goreli hacim (motor_cok).
# rev: RV <= lo ve |r| >= teta -> -sign(r); dev: RV >= hi ve |r| >= teta -> sign(r). Egitim YOK.
# Karar a+29 barinda; yalniz o bara kadarki bugunku barlar + onceki seanslar kullanilir.
import numpy as np

PENCERELER = list(range(600, 991, 30))


def _V(p, a):
    dk = p.dk.to_numpy(); m = (dk >= a) & (dk <= a + 29)
    if m.sum() < 25:
        return np.nan
    return float(p.volume.to_numpy(float)[m].sum())


def sinyal(s, onceki, bilgi, mod="rev", lo=0.612, hi=1.227, teta=0.00158, H=None):  # H yalniz cikis icin
    n = len(s); out = np.zeros(n)
    if len(onceki) < 20:
        return out
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float); v = s.volume.to_numpy(float)
    for a in PENCERELER:
        m = (dk >= a) & (dk <= a + 29)
        e = np.flatnonzero(dk == a + 29); b = np.flatnonzero(dk >= a)
        if m.sum() < 25 or not len(e) or not len(b):
            continue
        e = e[0]; b = b[0]
        taban = np.array([_V(p, a) for p in onceki[-20:]])
        taban = taban[np.isfinite(taban)]
        if len(taban) < 20 or taban.mean() <= 0:
            continue
        RV = v[m].sum() / taban.mean()
        r = c[e] / o[b] - 1.0
        if abs(r) < teta or r == 0:
            continue
        if mod == "rev" and RV <= lo:
            out[e] = -np.sign(r)
        elif mod == "dev" and RV >= hi:
            out[e] = np.sign(r)
    return out
