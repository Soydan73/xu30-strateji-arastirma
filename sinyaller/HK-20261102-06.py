# HK-20261102-06 — FOMC açıklama günü gündüz seansı uzun (pre-FOMC sürüklenmesinin gündüz payı)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Sinyal yalnız tarih ve i. barın dakikasına bakar.
import os, sys, datetime as _dt
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from takvim_ortak import FOMC


def _onceki_is_gunu(g):
    d = g - _dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= _dt.timedelta(days=1)
    return d


FOMC_ONCESI = {_onceki_is_gunu(g) for g in FOMC}


def sinyal(s, giris=585, gun="fomc"):
    n = len(s); out = np.zeros(n)
    g = s.time.iloc[0].date()
    if gun == "fomc" and g not in FOMC:
        return out
    if gun == "fomc_oncesi" and g not in FOMC_ONCESI:
        return out
    if gun == "carsamba_disi" and (g.weekday() != 2 or g in FOMC):
        return out
    dk = s.dk.to_numpy()
    for i in range(n):
        if dk[i] >= giris - 1 and (i == 0 or dk[i - 1] < giris - 1):
            out[i] = 1                                   # giriş i+1 açılışı; çıkış 18:05 zorla kapanış
            break
    return out
