# HK-20261105-07 — "kolay gun": dunku kapanis dunku HLC/3'un altinda -> bugun uzun, ustunde -> kisa.
# Fiyat duzeyi yalniz ayni vadedeki dunden. i. bar icin yalniz s.iloc[:i+1] (karar ilk dk >= giris-1 barinda).
import numpy as np


def sinyal(s, onceki, bilgi, giris=585, m=0.0, taraf="iki", kontrol=False, H=600):   # H yalniz cikis parametresi
    n = len(s); out = np.zeros(n)
    if n < 1 or len(onceki) == 0 or not bool(bilgi["ayni_vade"][-1]):
        return out
    d0 = onceki[-1]
    H_, L_, C_ = float(d0.high.max()), float(d0.low.min()), float(d0.close.iloc[-1])
    R = H_ - L_
    if not R > 0:
        return out
    dk = s.dk.to_numpy()
    ix = np.flatnonzero(dk >= giris - 1)
    if len(ix) == 0:
        return out
    i = int(ix[0])
    if kontrol:
        out[i] = 1.0
        return out
    d = (C_ - (H_ + L_ + C_) / 3.0) / R
    if d < -m:
        out[i] = 1.0
    elif d > m and taraf == "iki":
        out[i] = -1.0
    return out
