# HK-20261104-13 — Onceki N seansin sabah (dk<600) OFI dizisi kesin azalansa bugun 09:46 uzun -> 18:05.
# OFI akis olcusudur (fiyat duzeyi degil) -> tum onceki kullanilir. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _ofi(b, sv, dk):
    m = dk < 600
    top = float(b[m].sum() + sv[m].sum())
    if not top > 0:
        return None
    return float(b[m].sum() - sv[m].sum()) / top


def sinyal(s, onceki, bilgi, N=3, negatif=False, bugun=False, kontrol=False, H=400):
    n = len(s); out = np.zeros(n)
    if n < 1:
        return out
    dk = s.dk.to_numpy()
    if kontrol:
        idx = np.flatnonzero(dk >= 585)
        if len(idx):
            out[idx[0]] = 1
        return out
    k = N - 1 if bugun else N
    if len(onceki) < k:
        return out
    dizi = []
    for x in onceki[len(onceki) - k:]:
        v = _ofi(x.buy_volume.to_numpy(float), x.sell_volume.to_numpy(float), x.dk.to_numpy())
        if v is None:
            return out
        dizi.append(v)
    if bugun:
        idx = np.flatnonzero(dk >= 599)
        if not len(idx):
            return out
        i = int(idx[0])
        v = _ofi(s.buy_volume.to_numpy(float)[:i + 1], s.sell_volume.to_numpy(float)[:i + 1], dk[:i + 1])
        if v is None:
            return out
        dizi.append(v)
    else:
        idx = np.flatnonzero(dk >= 585)
        if not len(idx):
            return out
        i = int(idx[0])
    if not all(dizi[j] > dizi[j + 1] for j in range(len(dizi) - 1)):
        return out
    if negatif and not dizi[-1] < 0:
        return out
    out[i] = 1
    return out
