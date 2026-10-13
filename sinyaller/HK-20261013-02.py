# HK-20261013-02 — seans VWAP sapması × gerçek kümülatif delta (yalnız sinyal fonksiyonu)
import numpy as np

def sinyal(s, mod="devam", teta=0.0025, T=779):
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    ii = np.flatnonzero(dk == T)
    if not len(ii):
        return out
    i = ii[0]
    h, l, c, v = (s[k].to_numpy(float)[: i + 1] for k in ("high", "low", "close", "volume"))
    if v.sum() <= 0:
        return out
    vwap = ((h + l + c) / 3 * v).sum() / v.sum()
    dev = (c[-1] - vwap) / vwap
    cd = (s.buy_volume.to_numpy(float)[: i + 1] - s.sell_volume.to_numpy(float)[: i + 1]).sum()
    if abs(dev) < teta:
        return out
    y = np.sign(dev); uyum = np.sign(cd) == y
    if mod == "devam":
        out[i] = y
    elif mod == "akis":
        out[i] = y if uyum else -y
    elif mod == "uyum":
        out[i] = y if uyum else 0
    else:
        raise ValueError(mod)
    return out
