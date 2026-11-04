# HK-20261104-08 — Vade haftasi gunduz uzun (takvim). gunler: calistirma betiginde seans listesinden bir kez cikarilan
# tarih kumesi (onceden bilinen vade takvimi, fiyat icermez). Secili gunde giris dakikasindan itibaren +1 (yalniz saat).
import numpy as np


def sinyal(s, gunler=(), giris_dk=584, kontrol=False):
    out = np.zeros(len(s))
    secili = str(s.time.iloc[0].date()) in gunler
    if secili == bool(kontrol):
        return out
    out[s.dk.to_numpy() >= giris_dk] = 1.0
    return out
