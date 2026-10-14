# HK-20261014-17 — gelişen VA dışına başarısız taşma → içeri dönüş (yalnız sinyal)
import numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vp_profil import gelisen_profil

def sinyal(s, mod="kapanis", k=2.0, M=5, bas=630, son=1020):
    n = len(s); out = np.zeros(n)
    poc, vah, val = gelisen_profil(s)
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float); dk = s.dk.to_numpy()
    ust = None; alt = None    # (j, bitis)
    for i in range(1, n):
        if np.isnan(vah[i - 1]):
            continue
        yeni_ust = h[i] >= vah[i - 1] + k and (mod == "fitil" or c[i] >= vah[i - 1])
        yeni_alt = l[i] <= val[i - 1] - k and (mod == "fitil" or c[i] <= val[i - 1])
        if yeni_ust: ust = (i, i + M - 1)
        if yeni_alt: alt = (i, i + M - 1)
        kisa = uzun = False
        if ust is not None:
            if i > ust[1]: ust = None
            elif (mod == "fitil" or i > ust[0]) and c[i] < vah[i - 1]:
                kisa = True; ust = None
        if alt is not None:
            if i > alt[1]: alt = None
            elif (mod == "fitil" or i > alt[0]) and c[i] > val[i - 1]:
                uzun = True; alt = None
        if bas <= dk[i] <= son and kisa != uzun:
            out[i] = -1 if kisa else 1
    return out
