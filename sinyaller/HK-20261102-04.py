# HK-20261102-04 — Seans ucunda oynaklık bobini (uç bölgede sıkışma → bobin dışına kapanış)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. i. barda yalnız 0…i barları.
import numpy as np


def sinyal(s, r=0.6, konum=True, N=10, z=0.2):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    rg = h - l
    cs = np.concatenate([[0.0], np.cumsum(rg)])
    for i in range(N + 50, n):
        if not (630 <= dk[i] <= 1050):
            continue
        arka = cs[i - N] / (i - N)            # 0…i−N−1 barları
        bob = (cs[i] - cs[i - N]) / N         # i−N…i−1
        if arka <= 0 or bob > r * arka:
            continue
        CH = h[i - N:i].max(); CL = l[i - N:i].min()
        SH = h[:i].max(); SL = l[:i].min(); R = SH - SL
        if konum:
            if CL - SL <= z * R and c[i] > CH:
                out[i] = 1
            elif SH - CH <= z * R and c[i] < CL:
                out[i] = -1
        else:
            if c[i] > CH:
                out[i] = 1
            elif c[i] < CL:
                out[i] = -1
    return out
