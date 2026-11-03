# HK-20261103-10 — Son 15 dk seans ucu kırılımı → kırılım yönünde kısa tutuş.
# Kaynak: daytradingtoolkit.com final 15 minutes. Eğitim YOK. i. bar için yalnız s.iloc[:i+1] kullanılır
# (uç = 09:30'dan i−1. bara kadar).
import numpy as np


def sinyal(s, bas=1065, son=1072, delta=False, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    o = s.open.to_numpy(float); hi = s.high.to_numpy(float); lo = s.low.to_numpy(float); c = s.close.to_numpy(float)
    dl = s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float)
    b = np.flatnonzero(dk >= 570)
    if not len(b):
        return out
    b = b[0]
    if kontrol:
        i = np.flatnonzero(dk == 1064); j0 = np.flatnonzero(dk == 1050)
        if len(i) and len(j0):
            y = np.sign(c[i[0]] - o[j0[0]])
            out[i[0]] = y
        return out
    for i in range(b + 1, n):
        if dk[i] < bas:
            continue
        if dk[i] > son:
            break
        yk = hi[b:i].max(); dsk = lo[b:i].min()
        y = 1 if c[i] > yk else (-1 if c[i] < dsk else 0)
        if y == 0:
            continue
        if delta and np.sign(dl[i]) != y:
            continue
        out[i] = y
        break
    return out
