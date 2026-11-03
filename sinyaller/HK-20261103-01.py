# HK-20261103-01 — işaretli hacim patlaması (M1 delta z) sonrası ters yön. Eğitim YOK.
# i. barda yalnız 0…i barları; ölçek (std) yalnız i'den önceki barlardan; bar 0 (ACILIS) dışarıda.
import numpy as np


def sinyal(s, k=1, z=4.0, fiyat=True, dk_bas=600, dk_son=1065, min_gecmis=30):
    n = len(s); out = np.zeros(n)
    d = (s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float))
    c = s.close.to_numpy(float); dk = s.dk.to_numpy()
    d[0] = 0.0
    cs = np.cumsum(d)
    D = np.full(n, np.nan)
    for i in range(k, n):                      # pencere bar i-k+1 … i, hepsi ≥ 1
        D[i] = cs[i] - cs[i - k]
    for i in range(k, n):
        if not (dk_bas <= dk[i] <= dk_son):
            continue
        gec = D[k:i]
        if len(gec) < min_gecmis:
            continue
        sd = gec.std(ddof=1)
        if not sd > 0:
            continue
        zi = D[i] / sd
        if abs(zi) < z:
            continue
        yon = np.sign(D[i])
        if fiyat and np.sign(c[i] - c[i - k]) != yon:
            continue
        out[i] = -yon
    return out
