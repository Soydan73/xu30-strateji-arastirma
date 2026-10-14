# HK-20261014-10 — 2. ve 3. yarım saat getirisi → son yarım saat (yalnız sinyal)
import numpy as np

def _r(dk, o, c, a, z):
    ia = np.flatnonzero(dk == a); iz = np.flatnonzero(dk == z)
    if not len(ia) or not len(iz):
        return None
    return c[iz[0]] / o[ia[0]] - 1.0

def sinyal(s, ongorucu="r23", teta=0.361, mod="yalin", T=1054):
    """Sinyal barı dk == T (17:34) kapanışı; 17:35 açılışında giriş. Öngörücüler 10:00–10:59 barlarından."""
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    ii = np.flatnonzero(dk == T)
    if not len(ii):
        return out
    i = ii[0]
    d = dk[: i + 1]; o = s.open.to_numpy(float)[: i + 1]; c = s.close.to_numpy(float)[: i + 1]
    r2 = _r(d, o, c, 600, 629); r3 = _r(d, o, c, 630, 659); r23 = _r(d, o, c, 600, 659)
    x = {"r2": r2, "r3": r3, "r23": r23}[ongorucu]
    if x is None or x == 0 or abs(x) * 100 < teta:
        return out
    if mod == "uyum" and (r2 is None or r3 is None or np.sign(r2) != np.sign(r3)):
        return out
    out[i] = np.sign(x)
    return out
