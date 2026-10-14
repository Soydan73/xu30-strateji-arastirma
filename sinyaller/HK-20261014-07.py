# HK-20261014-07 — öğleden sonra diliminin son yarım saatte tersine dönmesi (yalnız sinyal)
import numpy as np

def sinyal(s, W=30, teta=0.0):
    """Sinyal barı dk == 1054 (17:34) kapanışı; motor 17:35 açılışında girer.
    r = close(17:34) / open(pencere başı: 17:05 ya da 16:35) - 1 ; |r|% >= teta ise -sign(r)."""
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    b = np.flatnonzero(dk == 1054)
    a = np.flatnonzero(dk == 1055 - W)
    if not len(a) or not len(b):
        return out
    r = s.close.iloc[b[0]] / s.open.iloc[a[0]] - 1.0
    if r != 0 and abs(r) * 100 >= teta:
        out[b[0]] = -np.sign(r)
    return out
