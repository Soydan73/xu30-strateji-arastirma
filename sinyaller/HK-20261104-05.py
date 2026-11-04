# HK-20261104-05 — Beklenmedik illikidite soku (ilk saat RVol/hacim) -> ilk saat hareketinin tersi — motor_cok 1.00.
# Ilk saat = dk 585..644 (09:45-10:44). Karar 10:44 barinin kapanisinda -> giris 10:45 acilisi (motor).
# ILLIQ = sqrt(sum(diff(close)^2)) / sum(volume). Esik yalniz onceki seanslardan (son N tam seans).
# Yalniz oynaklik/hacim orani -> fiyat duzeyi karsilastirmasi yok, ayni_vade gerekmez.
import numpy as np

A0, A1 = 585, 644


def _illiq(o):
    dk = o.dk.to_numpy()
    m = (dk >= A0) & (dk <= A1)
    if not ((dk == A0).any() and (dk == A1).any()) or m.sum() < 50:
        return None
    c = o.close.to_numpy(float)[m]; v = o.volume.to_numpy(float)[m].sum()
    if v <= 0:
        return None
    return float(np.sqrt(np.sum(np.diff(c) ** 2))) / v


def sinyal(s, onceki, bilgi, N=60, q=0.8, kontrol=False, H=120):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    a = np.flatnonzero(dk == A0); b = np.flatnonzero(dk == A1)
    if not len(a) or not len(b):
        return out
    a, b = int(a[0]), int(b[0])
    r = float(s.close.iloc[b]) - float(s.open.iloc[a])
    if r == 0:
        return out
    if kontrol:
        out[b] = -np.sign(r)
        return out
    if len(onceki) < N:
        return out
    gecmis = [x for x in (_illiq(o) for o in list(onceki)[-N:]) if x is not None]
    if len(gecmis) < int(0.9 * N):
        return out
    bugun = _illiq(s.iloc[:b + 1])
    if bugun is None:
        return out
    if bugun > np.quantile(np.array(gecmis), q):
        out[b] = -np.sign(r)
    return out
