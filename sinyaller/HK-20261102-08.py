# HK-20261102-08 — Öğle profil şekli (P/b/D): POC'nin aralık içi konumu ve kuyruk hacim payı
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Profil yalnız 0…i barlarından.
import numpy as np


def sinyal(s, T=780, a=0.7, b=0.15, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk >= T)
    if len(idx) == 0:
        return out
    i = int(idx[0])
    if dk[i] >= T + 5:
        return out
    hh = s.high.to_numpy(float)[:i + 1]; ll = s.low.to_numpy(float)[:i + 1]
    c = float(s.close.iloc[i]); v = s.volume.to_numpy(float)[:i + 1]
    H = hh.max(); L = ll.min(); R = H - L
    if R < 10:
        return out
    if kontrol:
        pos = (c - L) / R
        if pos >= a:
            out[i] = 1
        elif pos <= 1 - a:
            out[i] = -1
        return out
    fh = np.floor(hh).astype(int); fl = np.floor(ll).astype(int)
    taban = fl.min(); prof = np.zeros(fh.max() - taban + 1)
    for k in range(i + 1):
        if v[k] > 0:
            prof[fl[k] - taban: fh[k] - taban + 1] += v[k] / (fh[k] - fl[k] + 1)
    top = prof.sum()
    if top <= 0:
        return out
    m = prof.max(); ad = np.flatnonzero(prof == m)
    ck = np.floor(c) - taban
    poc = ad[np.argmin(np.abs(ad - ck))] + taban
    pos = (poc - L) / R
    fiyat = np.arange(len(prof)) + taban
    alt = prof[fiyat < L + 0.3 * R].sum() / top
    ust = prof[fiyat > H - 0.3 * R].sum() / top
    uz = pos >= a and (b is None or alt <= b)
    ks = pos <= 1 - a and (b is None or ust <= b)
    if uz and not ks:
        out[i] = 1
    elif ks and not uz:
        out[i] = -1
    return out
