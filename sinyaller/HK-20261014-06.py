# HK-20261014-06 — Açılıştaki büyük fiyat değişiminin gün içi dönüşü (Grant-Wolf-Yu 2005) (yalnız sinyal)
import numpy as np

def sinyal(s, T=600, teta=0.5):
    """T: giriş dakikası (09:00'dan). Sinyal barı dk == T-1 kapanışı.
    r = close[T-1] / open(seansın ilk barı, açılış açık artırması) - 1. |r|% >= teta ise ters yönde."""
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    if dk[0] > 570:                      # açılışı 09:30'dan sonra başlayan seanslar (ör. 09:40) karşılaştırılamaz
        return out
    if T <= 590 and dk[0] != 565:        # 15 dk varyantı açılış açık artırması barını ister
        return out
    j = np.flatnonzero(dk == T - 1)
    if not len(j):
        return out
    i = j[0]
    r = s.close.iloc[i] / s.open.iloc[0] - 1.0
    if abs(r) * 100 >= teta:
        out[i] = -np.sign(r)
    return out
