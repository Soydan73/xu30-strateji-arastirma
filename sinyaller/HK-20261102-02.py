# HK-20261102-02 — Sabah POC'sine (11:00'te dondurulmuş) seans içi ilk dönüşte sekme
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Sabah profili yalnız dk 570–659 barlarından; i. barda s.iloc[:i+1].
import numpy as np


def _sabah(s):
    dk = s.dk.to_numpy()
    m = (dk >= 570) & (dk < 660)
    if m.sum() < 80:
        return None
    h = s.high.to_numpy(float)[m]; l = s.low.to_numpy(float)[m]; v = s.volume.to_numpy(float)[m]
    c = s.close.to_numpy(float)[m]; d = dk[m]
    hk = np.floor(h).astype(int); lk = np.floor(l).astype(int)
    taban = lk.min(); prof = np.zeros(hk.max() - taban + 1)
    for a, b, x in zip(lk - taban, hk - taban, v):
        if x > 0:
            prof[a:b + 1] += x / (b - a + 1)
    adaylar = np.flatnonzero(prof == prof.max()) + taban
    poc = float(adaylar[np.argmin(np.abs(adaylar - np.floor(c[-1])))])
    blok = []
    for b0 in range(570, 660, 15):
        mm = (d >= b0) & (d < b0 + 15)
        if mm.sum() >= 10:
            blok.append(h[mm].max() - l[mm].min())
    if len(blok) < 6:
        return None
    return poc, (h.max() + l.min()) / 2.0, float(np.mean(blok))


def sinyal(s, k=1.0, seviye="poc"):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    if n == 0 or dk[-1] < 660:
        return out
    r = _sabah(s)
    if r is None:
        return out
    poc, orta, A = r
    X = poc if seviye == "poc" else orta
    if A <= 0:
        return out
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    S = 0
    for i in range(n):
        if dk[i] < 660:
            continue
        if S == 0:
            if abs(c[i] - X) >= k * A:
                S = int(np.sign(c[i] - X))
            continue
        if (S > 0 and l[i] <= X + 2) or (S < 0 and h[i] >= X - 2):
            if dk[i] <= 990:
                out[i] = S
            break
    return out
