# HK-20261013-03 — gün içi LeBaron: beklenmedik oynaklık → momentum / düşük sürpriz → dönüş (yalnız sinyal)
import numpy as np

KONTROL = (720, 780, 840, 900, 960)   # 12:00 13:00 14:00 15:00 16:00 (giriş dakikası)

def sinyal(s, mod="mom", u=2.0):
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    out = np.zeros(len(s))
    lr = np.full(len(s), np.nan); lr[1:] = np.diff(np.log(c))
    for T in KONTROL:
        ii = np.flatnonzero(dk == T - 1)          # T-1 barı T'de kapanır
        if not len(ii):
            continue
        i = ii[0]
        son = (dk > T - 61) & (dk <= T - 1) & (np.arange(len(s)) <= i)
        onc = (dk >= 600) & (dk <= T - 61) & (np.arange(len(s)) <= i)   # 10:00'dan pencere başına
        if son.sum() < 40 or onc.sum() < 40:
            continue
        rv_son = np.nansum(lr[son] ** 2)
        rv_bek = np.nanmean(lr[onc] ** 2) * son.sum()
        if rv_bek <= 0:
            continue
        U = rv_son / rv_bek
        j0 = np.flatnonzero(son)[0]
        R = c[i] - c[j0 - 1] if j0 >= 1 else 0.0
        if R == 0:
            continue
        if mod == "mom" and U >= u:
            out[i] = np.sign(R); break
        if mod == "rev" and U <= u:
            out[i] = -np.sign(R); break
    return out
