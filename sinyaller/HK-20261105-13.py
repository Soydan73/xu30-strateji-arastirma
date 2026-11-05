# HK-20261105-13 — onceki gun aralik rejimi -> sabah penceresi yonu. motor_cok 1.00, geri 20.
# Goreli aralik (H-L)/C: fiyat duzeyi karsilastirmasi yok (tum onceki kullanilir). Karar yalniz dk == 614 (10:14 kapanisi).
import numpy as np


def _r(x):
    c = float(x.close.iloc[-1])
    if c <= 0:
        return np.nan
    return (float(x.high.max()) - float(x.low.min())) / c


def sinyal(s, onceki, bilgi, a=1.2, b=0.8, yon="ikisi", N=20, kontrol=False, H=120):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    idx = np.where(dk == 614)[0]
    if len(idx) == 0:
        return out
    j = int(idx[0])
    if kontrol:
        out[j] = 1
        return out
    if len(onceki) < N:
        return out
    rr = np.array([_r(x) for x in onceki[-N:]], float)
    if not np.all(np.isfinite(rr)):
        return out
    med = float(np.median(rr)); r1 = rr[-1]
    y = 0
    if a is not None and yon in ("ikisi", "uzun") and r1 > a * med:
        y = 1
    elif b is not None and yon in ("ikisi", "kisa") and r1 < b * med:
        y = -1
    out[j] = y
    return out
