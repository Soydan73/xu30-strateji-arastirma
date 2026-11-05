# HK-20261105-04 — Acilis fiyat etkisinin kalicilik payi. Tek seans; i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, mod="kalici", delta_sart=True, e=0.001, kontrol=False, H=120):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk == 599)
    if not len(idx):
        return out
    i = int(idx[0])
    w1 = np.flatnonzero((dk >= 570) & (dk <= 584))
    k1 = np.flatnonzero(dk == 584)
    if len(w1) < 5 or not len(k1):
        return out
    o1 = float(s.open.iloc[int(w1[0])]); c1 = float(s.close.iloc[int(k1[0])]); c2 = float(s.close.iloc[i])
    M = c1 - o1
    if M == 0 or abs(M) / o1 < e:
        return out
    D1 = float((s.buy_volume.iloc[w1] - s.sell_volume.iloc[w1]).sum())
    if delta_sart and np.sign(D1) != np.sign(M):
        return out
    g = (c1 - c2) * np.sign(M) / abs(M)
    if kontrol:
        out[i] = np.sign(M); return out
    if mod == "kalici" and g < 0.3:
        out[i] = np.sign(M)
    elif mod == "gecici" and g > 0.7:
        out[i] = -np.sign(M)
    return out
