# HK-20261105-08 — devir sonrasi ilk seanslar gunduz uzun. Yalniz takvim bilgisi (devir_bugun, ayni_vade); fiyat duzeyi yok.
import numpy as np


def sinyal(s, onceki, bilgi, d_min=1, d_max=5, giris=585, H=600):   # H yalniz cikis parametresi
    n = len(s); out = np.zeros(n)
    if n < 1:
        return out
    if bool(bilgi["devir_bugun"]):
        d = 1
    else:
        av = np.asarray(bilgi["ayni_vade"], dtype=bool)
        if len(av) == 0 or av.all():
            return out
        d = int(av.sum()) + 1
    if not (d_min <= d <= d_max):
        return out
    dk = s.dk.to_numpy()
    ix = np.flatnonzero(dk >= giris - 1)
    if len(ix):
        out[int(ix[0])] = 1.0
    return out
