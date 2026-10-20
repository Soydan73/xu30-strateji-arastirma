# HK-20261020-06 — Sabah realize çarpıklığı → öğleden sonra ters yön (Amaya vd. işareti, gün içi uyarlama)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Tek seans, i. bara kadar olan M1 barları.
import numpy as np


def sinyal(s, mod="rs", T=780, bas=570, q_alt=-0.491, q_ust=0.496):
    """T−1 barının kapanışında, dk ∈ [bas, T−1] M1 log getirilerinin realize çarpıklığı:
    RS = √n·Σr³/(Σr²)^1,5. mod 'rs': RS ≥ q_ust → −1, RS ≤ q_alt → +1.
    mod 'getiri' (KONTROL): aynı uç-RS günlerinde yön = −sign(close(T−1) − open(ilk bar ≥ bas))."""
    n = len(s)
    out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy()
    c = s.close.to_numpy(float); o = s.open.to_numpy(float)
    karar = np.flatnonzero(dk == T - 1)
    if len(karar) == 0:
        return out
    i = int(karar[0])
    idx = np.flatnonzero((dk >= bas) & (dk <= T - 1))
    idx = idx[idx <= i]
    if len(idx) < 60:
        return out
    r = np.diff(np.log(c[idx]))
    rv = float((r ** 2).sum())
    if rv <= 0:
        return out
    rs = np.sqrt(len(r)) * float((r ** 3).sum()) / rv ** 1.5
    if q_alt < rs < q_ust:
        return out
    if mod == "rs":
        out[i] = -1.0 if rs >= q_ust else 1.0
    else:
        out[i] = -np.sign(c[i] - o[idx[0]])
    return out
