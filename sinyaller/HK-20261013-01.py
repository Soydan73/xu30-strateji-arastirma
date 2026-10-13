# HK-20261013-01 — piyasa gün içi momentumu, yüksek oynaklık koşullu (yalnız sinyal fonksiyonu)
import numpy as np

def sinyal(s, ongorucu="r1", teta=0.004, T=1054):
    """T: sinyal barının dakikası (1054=17:34, 1024=17:04). Yalnız s.iloc[:i+1] kullanılır."""
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    out = np.zeros(len(s))
    ii = np.flatnonzero(dk == T)
    if not len(ii):
        return out
    i = ii[0]; o0 = o[0]
    j = np.flatnonzero(dk[: i + 1] <= 599)          # 09:59 kapanışı (veya öncesindeki son bar)
    if ongorucu in ("r1", "r1r12"):
        if not len(j) or dk[j[-1]] < 590:
            return out
        x = c[j[-1]] - o0
    elif ongorucu == "rod":
        x = c[i] - o0
    else:
        raise ValueError(ongorucu)
    if abs(x) / o0 < teta:
        return out
    y = np.sign(x)
    if ongorucu == "r1r12":
        k = np.flatnonzero((dk[: i + 1] >= 1025))      # 17:05 → 17:34
        if not len(k):
            return out
        r12 = c[i] - o[k[0]]
        if np.sign(r12) != y:
            return out
    out[i] = y
    return out
