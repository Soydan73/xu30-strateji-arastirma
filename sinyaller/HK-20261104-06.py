# HK-20261104-06 — Fitil/RV patlayici trend kapisi (Realized Candlestick Wicks) — motor 1.00 (tek seans).
# Son 30 M1 bar: RV30 = sum(diff(close)^2), WV30 = sum(ust_fitil^2 + alt_fitil^2), r30 = c_i - c_{i-30}.
# Karar yalniz M15 sinirinda (dk % 15 == 14), dk 644..1004 (10:44-16:44). Q = RV30/WV30 > Qe ve |r30| > k*sqrt(WV30).
# i. bar icin yalniz s.iloc[:i+1] kullanilir.
import numpy as np

D0, D1, L = 644, 1004, 30


def sinyal(s, Qe=3.0, k=2.0, kontrol=False, H=30):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    o = s.open.to_numpy(float); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    for i in range(n):
        if dk[i] % 15 != 14 or dk[i] < D0 or dk[i] > D1 or i < L:
            continue
        if dk[i] - dk[i - L] != L:          # pencerede eksik bar varsa atla
            continue
        cc = c[i - L:i + 1]
        rv = float(np.sum(np.diff(cc) ** 2))
        oo = o[i - L + 1:i + 1]; hh = h[i - L + 1:i + 1]; ll = l[i - L + 1:i + 1]; c2 = c[i - L + 1:i + 1]
        ust = hh - np.maximum(oo, c2); alt = np.minimum(oo, c2) - ll
        wv = float(np.sum(ust ** 2 + alt ** 2))
        if wv <= 0:
            continue
        r30 = c[i] - c[i - L]
        if abs(r30) <= k * np.sqrt(wv):
            continue
        if not kontrol and rv / wv <= Qe:
            continue
        out[i] = np.sign(r30)
    return out
