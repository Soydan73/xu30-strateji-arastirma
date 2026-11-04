# HK-20261104-04 — Tatil oncesi son tam gun gun ici uzun (pre-holiday effect) — motor 1.00 (tek seans).
# Takvim parametre olarak verilir (resmi tatil / bayram takvimi onceden ilan edilir; fiyat icermez).
# Giris: giris_dk-1 barinda +1 -> giris_dk acilisi. Cikis: cikis_dk-1 barinda -1 (motor ters=True) ya da seans sonu.
import numpy as np


def sinyal(s, gunler=(), giris_dk=600, cikis_dk=1080, kontrol=False):
    n = len(s); out = np.zeros(n)
    gun = str(s.time.iloc[0].date())
    if (gun in gunler) == bool(kontrol):
        return out
    dk = s.dk.to_numpy()
    g = np.flatnonzero(dk == giris_dk - 1)
    if not len(g):
        return out
    g = int(g[0])
    out[g] = 1.0
    if cikis_dk is not None:
        e = np.flatnonzero(dk == cikis_dk - 1)
        if len(e) and e[0] > g:
            out[int(e[0])] = -1.0
    return out
