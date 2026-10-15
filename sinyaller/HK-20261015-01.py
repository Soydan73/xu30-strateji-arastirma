# HK-20261015-01 — OU uyumu + DF durağanlık kapısı, z-skor ortalamaya dönüş (yalnız sinyal)
import numpy as np


def sinyal(s, P=5, L=12, z=1.5):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    kap = []                                   # tamamlanmış kova kapanışları
    for i in range(n):
        if dk[i] < 570 or (dk[i] - 570) % P != P - 1:
            continue
        kap.append(c[i])                       # bu barın kapanışında kova tamamlandı
        if len(kap) < L + 1:
            continue
        x = np.asarray(kap[-(L + 1):])
        y, xl = x[1:], x[:-1]
        X = np.column_stack([np.ones(L), xl])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        a, b = beta
        e = y - X @ beta
        s2 = (e @ e) / (L - 2)
        sxx = ((xl - xl.mean()) ** 2).sum()
        if sxx <= 0 or s2 <= 0 or not (0 < b < 1):
            continue
        t_df = (b - 1) / np.sqrt(s2 / sxx)
        if t_df >= -2.86:
            continue
        mu = a / (1 - b)
        sig = np.sqrt(s2) / np.sqrt(1 - b * b)
        zz = (x[-1] - mu) / sig
        maliyet = 6.0 * x[-1] / 16500.0 + 2.4
        if abs(x[-1] - mu) <= maliyet:
            continue
        if zz >= z: out[i] = -1
        elif zz <= -z: out[i] = 1
    return out
