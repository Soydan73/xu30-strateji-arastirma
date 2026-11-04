# HK-20261104-02 — Vade son islem gunu: 09:45->12:29 getirisinin tersine 12:30'da gir, 17:30 (ya da 18:05) cik (motor).
# Takvim (gunler) parametre olarak verilir: veri setindeki cift aylarin son seanslari (onceden bilinen takvim, fiyat icermez).
# i. bar icin yalniz s.iloc[:i+1]: karar 12:29 barinda, cikis sinyali 17:29 barinda (yalniz zaman).
import numpy as np


def sinyal(s, gunler=(), esik=0.0, cikis_dk=1050, kontrol=False):
    n = len(s); out = np.zeros(n)
    gun = str(s.time.iloc[0].date())
    vade = gun in gunler
    if vade == bool(kontrol):
        return out
    dk = s.dk.to_numpy()
    a = np.flatnonzero(dk == 585); b = np.flatnonzero(dk == 749)
    if not len(a) or not len(b):
        return out
    a, b = int(a[0]), int(b[0])
    r = float(s.close.iloc[b]) / float(s.open.iloc[a]) - 1.0
    if r == 0 or abs(r) < esik:
        return out
    y = -np.sign(r)
    out[b] = y
    if cikis_dk is not None:
        e = np.flatnonzero(dk == cikis_dk - 1)
        if len(e) and e[0] > b:
            out[int(e[0])] = -y
    return out
