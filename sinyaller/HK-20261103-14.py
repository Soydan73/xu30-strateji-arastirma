# HK-20261103-14 — Sabah yolu analogu (kNN, egitimsiz): sabah M15 yoluna en yakin K onceki seansin T -> 18:05 getirisi.
# Kitaplik YALNIZ onceki seanslardan; bugun icin yalniz s.iloc[:i+1] (sinyal yalniz T-1 barinda).
import numpy as np


def _son_kapanis(dk, c, sinir):
    j = np.flatnonzero(dk <= sinir)
    return c[j[-1]] if len(j) else np.nan


def _yol(p, T, znorm):
    dk = p.dk.to_numpy(); c = p.close.to_numpy(float)
    r0 = _son_kapanis(dk, c, 584)
    if not np.isfinite(r0) or r0 <= 0:
        return None
    noktalar = list(range(599, T, 15))
    x = np.array([_son_kapanis(dk, c, q) for q in noktalar]) / r0 - 1.0
    if not np.all(np.isfinite(x)):
        return None
    if znorm:
        sd = x.std()
        if sd == 0:
            return None
        x = (x - x.mean()) / sd
    return x


def _sonuc(p, T):
    dk = p.dk.to_numpy(); c = p.close.to_numpy(float)
    a = _son_kapanis(dk, c, T - 1); b = _son_kapanis(dk, c, 1084)
    if not (np.isfinite(a) and np.isfinite(b)) or a <= 0:
        return np.nan
    return b / a - 1.0


def sinyal(s, onceki, bilgi, T=780, K=20, znorm=True, pay=0.6, kontrol=False, min_kitap=40):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    j = np.flatnonzero(dk == T - 1)
    if not len(j) or len(onceki) < min_kitap:
        return out
    j = j[0]
    X, Y = [], []
    for p in onceki:
        x = _yol(p, T, znorm); y = _sonuc(p, T)
        if x is None or not np.isfinite(y):
            continue
        X.append(x); Y.append(y)
    if len(Y) < min_kitap:
        return out
    X = np.array(X); Y = np.array(Y)
    if kontrol:
        w = np.ones(len(Y)); yk = Y
    else:
        x0 = _yol(s.iloc[:j + 1], T, znorm)
        if x0 is None:
            return out
        d = np.sqrt(((X - x0) ** 2).sum(axis=1))
        idx = np.argsort(d, kind="stable")[:K]
        dK = d[idx]; med = np.median(dK)
        w = np.exp(-dK / med) if med > 0 else np.ones(len(dK))
        yk = Y[idx]
    m = (w * yk).sum() / w.sum()
    if m == 0:
        return out
    oran = (w * (np.sign(yk) == np.sign(m))).sum() / w.sum()
    if oran >= pay:
        out[j] = np.sign(m)
    return out
