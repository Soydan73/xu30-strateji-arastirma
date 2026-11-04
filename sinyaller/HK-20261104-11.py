# HK-20261104-11 — Seans araligi / ATR(7 seans) kapsama orani >= c iken yeni seans ucunda ters yon (tukenme sonumu).
# ATR7 = onceki 7 gunduz seansinin (yuksek - dusuk) ortalamasi (oynaklik ortalamasi -> tum onceki; fiyat duzeyi kullanilmaz).
# i. bar icin yalniz s.iloc[:i+1]. Sinyal penceresi dk 630-1020 (10:30-17:00), seans basina ilk tetik.
import numpy as np


def sinyal(s, onceki, bilgi, c=0.8, kontrol=False, etiket=0):
    # etiket: yalniz varyant kimligi (cikis H farki icin), sinyale etkisi yok
    n = len(s); out = np.zeros(n)
    atr = 0.0
    if not kontrol:
        if len(onceki) < 7:
            return out
        atr = float(np.mean([float(x.high.max()) - float(x.low.min()) for x in onceki[-7:]]))
        if not atr > 0:
            return out
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    if n < 2:
        return out
    hh = h[0]; ll = l[0]
    for i in range(1, n):
        yeni_y = h[i] > hh; yeni_d = l[i] < ll
        hh = max(hh, h[i]); ll = min(ll, l[i])
        if not (630 <= dk[i] <= 1020) or (yeni_y and yeni_d):
            continue
        if not (yeni_y or yeni_d):
            continue
        if kontrol or (hh - ll) >= c * atr:
            out[i] = -1 if yeni_y else 1
            return out
    return out
