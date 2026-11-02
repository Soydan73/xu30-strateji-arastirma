# HK-20261102-05 — NFP günü duyuru öncesi belirsizlik primi (gündüz uzun, 08:30 ET'den 5 dk önce çık)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Sinyal yalnız tarih ve i. barın dakikasına bakar.
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from takvim_ortak import NFP, abd_yaz_saati


def sinyal(s, giris=585, cikis="t0-5", gun="nfp"):
    n = len(s); out = np.zeros(n)
    g = s.time.iloc[0].date()
    if g.weekday() != 4:
        return out
    if gun == "nfp" and g not in NFP:
        return out
    if gun == "nfp_disi" and g in NFP:
        return out
    t0 = 930 if abd_yaz_saati(g) else 990
    son = t0 - 5 if cikis == "t0-5" else None          # None: 18:05 zorla kapanışa kadar tut
    dk = s.dk.to_numpy()
    girdi = False
    for i in range(n):
        if not girdi and dk[i] >= giris - 1 and (i == 0 or dk[i - 1] < giris - 1):
            out[i] = 1; girdi = True                     # giriş i+1 açılışı (≈ giris)
        elif girdi and son is not None and dk[i] >= son - 1 and dk[i - 1] < son - 1:
            out[i] = -1                                  # ters sinyal → i+1 açılışında (≈ t0−5) kapanış
            break
    return out
