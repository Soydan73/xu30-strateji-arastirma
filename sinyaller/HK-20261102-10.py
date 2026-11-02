# HK-20261102-10 — Son saat trend günü: M5 EMA9 geri çekilmesi sonrası trend yönünde. Eğitim YOK.
# i. barda yalnız 0…i barları; M5 yalnız tamamlanmış kovalar (sinyal dk%5==4 barında).
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5_ortak import m5_tamam


def sinyal(s, theta=0.005, vwap=True, T0=1025, Tson=1065, kontrol=False):
    n = len(s); out = np.zeros(n)
    O0 = float(s.open.iloc[0])
    tp = (s.high.to_numpy(float) + s.low.to_numpy(float) + s.close.to_numpy(float)) / 3
    v = s.buy_volume.to_numpy(float) + s.sell_volume.to_numpy(float)   # tik bayraklı gerçek hacim
    cv = np.cumsum(v); vw = np.where(cv > 0, np.cumsum(tp * v) / np.where(cv > 0, cv, 1), np.nan)
    dk = s.dk.to_numpy()
    _, _, _, C, J = m5_tamam(s, n - 1)
    if len(C) < 2:
        return out
    ema = np.empty(len(C)); ema[0] = C[0]
    for t in range(1, len(C)):
        ema[t] = ema[t - 1] + 0.2 * (C[t] - ema[t - 1])
    ilk = True
    for t in range(1, len(C)):
        j = J[t]
        if not (T0 <= dk[j] <= Tson):
            continue
        r = C[t] / O0 - 1
        uz = r >= theta and (not vwap or C[t] > vw[j])
        ks = r <= -theta and (not vwap or C[t] < vw[j])
        if kontrol:
            if ilk:
                ilk = False
                if uz: out[j] = 1
                elif ks: out[j] = -1
            continue
        if uz and C[t - 1] < ema[t - 1] and C[t] > ema[t]:
            out[j] = 1
        elif ks and C[t - 1] > ema[t - 1] and C[t] < ema[t]:
            out[j] = -1
    return out
