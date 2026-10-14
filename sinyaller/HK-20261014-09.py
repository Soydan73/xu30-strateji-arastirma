# HK-20261014-09 — ilk yarım saat gerçek akış dengesizliği (FOIB) → günün geri kalanı (yalnız sinyal)
import numpy as np

def sinyal(s, teta=0.1938, mod="yalin", T=599):
    """Sinyal barı dk == T (09:59) kapanışı; motor 10:00 açılışında girer.
    FOIB = Σ(buy−sell)/Σ(buy+sell), seansın ilk barından T'ye (dahil). Yalnız s.iloc[:i+1] kullanılır."""
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    ii = np.flatnonzero(dk == T)
    if not len(ii):
        return out
    i = ii[0]
    b = s.buy_volume.to_numpy(float)[: i + 1]; v = s.sell_volume.to_numpy(float)[: i + 1]
    tot = (b + v).sum()
    if tot <= 0:
        return out
    f = (b - v).sum() / tot
    if f == 0 or abs(f) < teta:
        return out
    y = np.sign(f)
    if mod == "uyum":
        r = s.close.iloc[i] - s.open.iloc[0]
        if np.sign(r) != y:
            return out
    out[i] = y
    return out
