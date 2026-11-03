# HK-20261103-06 — Öğleden sonra IB kırılımı, önce oluşan uca göre yön. Eğitim YOK. Yalnız s.iloc[:i+1].
import numpy as np


def sinyal(s, ib_bas=965, ib_son=1024, sira="ib", min_bar=50, kir_son=1079):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    ib = np.flatnonzero((dk >= ib_bas) & (dk <= ib_son))
    if len(ib) < min_bar or ib[-1] >= n - 1:
        return out
    son = ib[-1]
    IBH = h[ib].max(); IBL = l[ib].min()
    if sira == "ib":
        iH = ib[np.argmax(h[ib])]; iL = ib[np.argmin(l[ib])]
    elif sira == "seans":
        sb = np.flatnonzero(dk >= 570)
        if len(sb) == 0:
            return out
        r = np.arange(sb[0], son + 1)
        iH = r[np.argmax(h[r])]; iL = r[np.argmin(l[r])]
    else:
        iH = iL = None
    if sira in ("ib", "seans"):
        if iL < iH: izin = 1
        elif iH < iL: izin = -1
        else: return out
    else:
        izin = 0
    for i in range(son + 1, n):
        if dk[i] > kir_son:
            break
        y = 1 if c[i] > IBH else (-1 if c[i] < IBL else 0)
        if y == 0:
            continue
        if izin == 0 or y == izin:
            out[i] = y
        break   # yalnız ilk kırılım
    return out
