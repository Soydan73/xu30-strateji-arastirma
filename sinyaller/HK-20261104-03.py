# HK-20261104-03 — IVU suzgecli son yarim saat momentumu (Yang-He, CSI300) — motor_cok 1.00.
# IVU = hacim(09:45-10:14 barlari) / hacim(09:45-17:34 barlari); r_acilis = close(10:14) - open(09:45).
# Karar 17:34 barinin kapanisinda (dk 1054) -> giris 17:35 acilisi, cikis 18:05 (motor).
# Esikler yalniz onceki seanslardan (son N tam seans); bugunun IVU/hacmi yalniz s.iloc[:i+1] ile hesaplanir.
# Yalniz hacim oranlari -> fiyat duzeyi karsilastirmasi yok, ayni_vade gerekmez.
import numpy as np

A0, A1, KARAR = 585, 614, 1054


def _olc(o):
    dk = o.dk.to_numpy(); v = o.volume.to_numpy(float)
    if not ((dk == A0).any() and (dk == A1).any() and (dk == KARAR).any()):
        return None
    ac = v[(dk >= A0) & (dk <= A1)].sum(); tum = v[(dk >= A0) & (dk <= KARAR)].sum()
    if tum <= 0:
        return None
    return ac / tum, tum


def sinyal(s, onceki, bilgi, N=60, kosul="ikili", q=0.5, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    a = np.flatnonzero(dk == A0); b = np.flatnonzero(dk == A1); k = np.flatnonzero(dk == KARAR)
    if not len(a) or not len(b) or not len(k):
        return out
    a, b, k = int(a[0]), int(b[0]), int(k[0])
    r = float(s.close.iloc[b]) - float(s.open.iloc[a])
    if r == 0:
        return out
    if kontrol:
        out[k] = np.sign(r)
        return out
    gecmis = [m for m in (_olc(o) for o in list(onceki)[-N:]) if m is not None]
    if len(onceki) < N or len(gecmis) < int(0.9 * N):
        return out
    v = s.volume.to_numpy(float)
    ac = v[a:b + 1].sum(); tum = v[a:k + 1].sum()
    if tum <= 0:
        return out
    ivu = ac / tum
    ivus = np.array([m[0] for m in gecmis]); Vs = np.array([m[1] for m in gecmis])
    c_ivu = ivu < np.quantile(ivus, q)
    c_v = tum > np.median(Vs)
    ok = {"ikili": c_ivu and c_v, "ivu": c_ivu, "hacim": c_v}[kosul]
    if ok:
        out[k] = np.sign(r)
    return out
