# HK-20261103-02 — M5 verim oranı ER20 ≥ e iken 20 M5 bar getirisi yönünde. Eğitim YOK.
# Yalnız tamamlanmış M5 kovaları (m5_ortak); sinyal dk%5==4 barında.
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5_ortak import m5_tamam


def sinyal(s, e=0.5, N=20, suzgec=True, dk_bas=660, dk_son=1020):
    n = len(s); out = np.zeros(n)
    O, H, L, C, J = m5_tamam(s, n - 1)
    dk = s.dk.to_numpy()
    for t in range(N, len(C)):
        j = J[t]
        if not (dk_bas <= dk[j] <= dk_son):
            continue
        net = C[t] - C[t - N]
        yol = np.abs(np.diff(C[t - N:t + 1])).sum()
        if yol <= 0 or net == 0:
            continue
        if suzgec and abs(net) / yol < e:
            continue
        out[j] = np.sign(net)
    return out
