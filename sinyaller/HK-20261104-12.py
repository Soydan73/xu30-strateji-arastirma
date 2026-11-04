# HK-20261104-12 — Sabah sicrama payi dusukse (surekli bilesen baskin) ogleden sonra sabah yonunde devam (RV/BV).
# Karar 11:59 bari (dk 719) kapanisinda; yalniz 09:45-11:59 barlari (dk 585-719). i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, j_esik=0.10, m=1.5, kontrol=False, etiket=0):
    # etiket: yalniz varyant kimligi (cikis H farki icin), sinyale etkisi yok
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    k = np.flatnonzero(dk == 719)
    if not len(k):
        return out
    i = int(k[0])
    sab = np.flatnonzero((dk >= 585) & (dk <= 719))
    sab = sab[sab <= i]
    if len(sab) < 60:
        return out
    o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    p0 = o[sab[0]]
    kova = (dk[sab] - 585) // 5
    son = np.r_[kova[1:] != kova[:-1], True]
    kap = c[sab][son]
    seri = np.r_[p0, kap]
    if np.any(seri <= 0):
        return out
    r = np.diff(np.log(seri))
    RV = float(np.sum(r ** 2))
    if RV <= 0:
        return out
    BV = float(np.pi / 2 * np.sum(np.abs(r[1:]) * np.abs(r[:-1])))
    J = max(RV - BV, 0.0) / RV
    R = float(np.log(c[i] / p0))
    if abs(R) > m * np.sqrt(BV) and (kontrol or J < j_esik):
        out[i] = np.sign(R)
    return out
