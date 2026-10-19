# HK-20261019-02 — ITSM, bilgi kesikliği (ID) koşullu (yalnız sinyal fonksiyonu)
import numpy as np


def sinyal(s, e=-0.20, kosul="surekli", teta=0.0, T=1054):
    """kosul: 'surekli' (ID <= e), 'kesikli' (ID > e), 'yok'. T: sinyal barının dakikası.
    Yalnız s.iloc[:i+1] kullanılır; pencere 09:30–09:59, T'den önce biter."""
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    out = np.zeros(len(s))
    ii = np.flatnonzero(dk == T)
    if not len(ii):
        return out
    i = ii[0]
    o0 = o[0]
    w = np.flatnonzero((dk[: i + 1] >= 570) & (dk[: i + 1] <= 599))
    if len(w) < 15 or w[-1] > i:
        return out
    r1 = c[w[-1]] - o0
    if r1 == 0 or abs(r1) / o0 < teta:
        return out
    onceki = c[w[0] - 1] if w[0] > 0 else o0
    seri = np.r_[onceki, c[w]]
    d = np.diff(seri)
    ID = np.sign(r1) * ((d < 0).mean() - (d > 0).mean())
    if kosul == "surekli" and not (ID <= e):
        return out
    if kosul == "kesikli" and not (ID > e):
        return out
    out[i] = np.sign(r1)
    return out
