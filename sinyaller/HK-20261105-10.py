# HK-20261105-10 — DC nowcast (Tsang vd. 2024): uzamis trendde (aTMV >= a) theta teyidinden ONCE geri cekilme b*theta'ya
# ulasinca trendin tersine gir. Cikis: yeni uc (trend devam -> sanal stop) ya da tahmin edilen donusten sonraki karsi DC
# teyidi, ya da 18:05. motor.py (tek seans). Sanal pozisyon motoru taklit eder; cikis = karsi isaretli tek bar ('ters').
# Durum makinesi yalniz kapanislarla ileri yurur -> i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, theta=0.003, a=1.6, b=0.65, son_giris=1050, H=600):
    n = len(s); out = np.zeros(n)
    if n < 2:
        return out
    c = s.close.to_numpy(float); dk = s.dk.to_numpy()
    mode = 0                       # +1 yukari trend, -1 asagi trend, 0 belirsiz
    hi = lo = c[1]                 # surekli islem 2. bardan
    bas = c[1]                     # mevcut trendin baslangic ucu
    poz = 0; ref = 0.0; asama = 0  # asama 0: donus bekleniyor; 1: donus teyit edildi, karsi DC bekleniyor
    ext2 = 0.0                     # asama 1'de yeni trendin ucu
    for i in range(1, n):
        x = c[i]
        # --- DC izleyici ---
        teyit = 0
        if mode == 0:
            hi = max(hi, x); lo = min(lo, x)
            if x >= lo * (1 + theta):
                mode, bas, hi = 1, lo, x; teyit = 1
            elif x <= hi * (1 - theta):
                mode, bas, lo = -1, hi, x; teyit = -1
        elif mode == 1:
            if x > hi:
                hi = x
            elif x <= hi * (1 - theta):
                mode, bas, lo = -1, hi, x; teyit = -1
        else:
            if x < lo:
                lo = x
            elif x >= lo * (1 + theta):
                mode, bas, hi = 1, lo, x; teyit = 1
        # --- sanal pozisyon yonetimi ---
        if poz != 0:
            cik = False
            if asama == 0:
                if teyit == poz:
                    asama = 1                       # tahmin edilen donus teyit edildi
                elif (poz == -1 and x > ref) or (poz == 1 and x < ref):
                    cik = True                      # yeni uc: trend surdu (sanal stop)
            else:
                if teyit == -poz:
                    cik = True                      # karsi DC teyidi
            if cik:
                out[i] = -poz; poz = 0
            continue
        # --- giris (teyit oncesi, yalniz motorun girebilecegi saatlerde) ---
        if teyit != 0 or dk[i] < 584 or dk[i] >= son_giris or mode == 0:
            continue
        if mode == 1:
            tmv = (hi - bas) / (bas * theta); bm = (hi - x) / (hi * theta)
            if tmv >= a and b <= bm < 1.0:
                out[i] = -1.0; poz = -1; ref = hi; asama = 0
        else:
            tmv = (bas - lo) / (bas * theta); bm = (x - lo) / (lo * theta)
            if tmv >= a and b <= bm < 1.0:
                out[i] = 1.0; poz = 1; ref = lo; asama = 0
    return out
