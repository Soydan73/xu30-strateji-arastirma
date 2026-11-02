# HK-20261102-07 — Trend günü: seans ucu ilk saatte oluşup korunmuşsa son saatte devam
# Yalnız sinyal fonksiyonu; model eğitimi YOK. i. barda yalnız 0…i barları.
import numpy as np


def sinyal(s, T=1025, W=630, q=0.5, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    O = float(s.open.iloc[0])
    idx = np.flatnonzero(dk >= T)
    if len(idx) == 0:
        return out
    i = int(idx[0])
    if dk[i] >= T + 5:
        return out
    H = h[:i + 1].max(); L = l[:i + 1].min(); R = H - L
    if R <= 0:
        return out
    dkL = dk[int(np.argmin(l[:i + 1]))]; dkH = dk[int(np.argmax(h[:i + 1]))]
    uz = (c[i] - L) / R >= q and c[i] > O
    ks = (H - c[i]) / R >= q and c[i] < O
    if not kontrol:
        uz = uz and dkL < W
        ks = ks and dkH < W
    if uz and not ks:
        out[i] = 1
    elif ks and not uz:
        out[i] = -1
    return out
