# HK-20261105-15 — dunun son saatinde yeni seans dibi/tepesi -> bugun 09:45 donus. motor_cok 1.00, geri 1.
# Fiyat duzeyi gunler arasi karsilastirilmaz (olay dunun kendi icinde); yine de ayni_vade[-1] sart.
import numpy as np


def sinyal(s, onceki, bilgi, son_bas=1025, yon="ikisi", kontrol=False, H=45):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    idx = np.where(dk >= 584)[0]
    if len(idx) == 0:
        return out
    j = int(idx[0])
    if kontrol:
        out[j] = 1
        return out
    if len(onceki) < 1 or not bool(bilgi["ayni_vade"][-1]):
        return out
    d = onceki[-1]
    ddk = d.dk.to_numpy()
    once = ddk < son_bas
    son = (ddk >= son_bas) & (ddk <= 1085)
    if once.sum() < 60 or son.sum() < 10:
        return out
    lo, hi = d.low.to_numpy(float), d.high.to_numpy(float)
    dip = lo[son].min() < lo[once].min()
    tepe = hi[son].max() > hi[once].max()
    if dip and tepe:
        return out
    y = 0
    if dip and yon in ("ikisi", "uzun"):
        y = 1
    elif tepe and yon in ("ikisi", "kisa"):
        y = -1
    out[j] = y
    return out
