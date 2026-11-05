# HK-20261105-01 — Acilis Kyle lambda (09:30-09:59, getiri ~ net delta) rejimi; gecmis lambda dagilimi onceki seanslardan.
# Fiyat duzeyi karsilastirmasi yok. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _lam(d, son):
    dk = d.dk.to_numpy()
    k = np.flatnonzero((dk >= 570) & (dk <= 599))
    if son is not None:
        k = k[k <= son]
    if len(k) < 5:
        return None, 0.0, 0.0
    c = d.close.to_numpy(float)[k]
    o0 = float(d.open.iloc[int(k[0])])
    onc = np.concatenate([[o0], c[:-1]])
    r = np.log(c / onc)
    q = (d.buy_volume.to_numpy(float) - d.sell_volume.to_numpy(float))[k]
    qq = float((q * q).sum())
    if qq <= 0:
        return None, 0.0, 0.0
    return float((r * q).sum() / qq), float(c[-1] - o0), float(q.sum())


def sinyal(s, onceki, bilgi, kosul="alt_medyan", yon=1, geri=60, kontrol=False, H=120):
    n = len(s); out = np.zeros(n)
    if n < 1 or len(onceki) < geri:
        return out
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk == 599)
    if not len(idx):
        return out
    i = int(idx[0])
    lam, M, Q = _lam(s, i)
    if lam is None:
        return out
    if kontrol:
        if Q != 0:
            out[i] = np.sign(Q)
        return out
    gec = [ _lam(d, None)[0] for d in onceki[-geri:] ]
    gec = np.array([x for x in gec if x is not None])
    if len(gec) < geri // 2 or M == 0:
        return out
    if kosul == "alt_medyan" and not lam < np.median(gec):
        return out
    if kosul == "ust75" and not lam > np.percentile(gec, 75):
        return out
    if kosul == "alt25" and not lam < np.percentile(gec, 25):
        return out
    out[i] = yon * np.sign(M)
    return out
