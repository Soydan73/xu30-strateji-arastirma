# HK-20261104-14 — Seans ici "kazanan kurali izle" (egitimsiz; fit/train yok).
# M15 kovalar k=(dk-585)//15; yalniz tamamlanmis kovalar. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _kovalar(dk, c, i):
    """0..i barlarindan tamamlanmis M15 kova kapanislari {k: son kapanis}, ve 09:45 oncesi son kapanis."""
    onc = None
    kap = {}
    for j in range(i + 1):
        if dk[j] < 585:
            onc = c[j]; continue
        k = (dk[j] - 585) // 15
        kap[k] = (c[j], dk[j])
    tam = {k: v[0] for k, v in kap.items() if v[1] >= 585 + 15 * (k + 1) - 1}
    return tam, onc


def sinyal(s, K=9, coklu=False, kontrol=False, H=60):
    n = len(s); out = np.zeros(n)
    if n < 2:
        return out
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float); o = s.open.to_numpy(float)
    son = 585 + 15 * K - 1
    idx = np.flatnonzero(dk >= son)
    if not len(idx):
        return out
    i = int(idx[0])
    tam, onc = _kovalar(dk, c, i)
    if any(k not in tam for k in range(K)):
        return out
    ilk = np.flatnonzero(dk >= 585)
    taban = onc if onc is not None else o[ilk[0]]
    kap = [tam[k] for k in range(K)]
    r = np.diff(np.r_[taban, kap])
    A = float(np.sum(np.sign(r[:-1]) * r[1:]))
    if kontrol:
        kaz = 1
    else:
        if A == 0:
            return out
        kaz = 1 if A > 0 else -1
    y = np.sign(r[-1]) * kaz
    if y != 0:
        out[i] = y
    if not coklu:
        return out
    # coklu: 12:00-17:45 her tamamlanan kovanin (son dakikasi gelmis) sonunda ayni donusum (kazanan sabit).
    # Son dakikasi eksik kova: sinyal yok, kapanisi sonraki kovanin ilk barinda referans olarak alinir.
    ref = kap[-1]; kb = K; sonc = None
    for j in range(i + 1, n):
        kj = (dk[j] - 585) // 15
        if kj != kb:
            if sonc is not None:
                ref = sonc
            kb = kj; sonc = None
        sonc = c[j]
        if dk[j] == 585 + 15 * (kb + 1) - 1:
            yy = np.sign(c[j] - ref) * kaz
            ref = c[j]; sonc = None
            if dk[j] <= 1064 and yy != 0:
                out[j] = yy
    return out
