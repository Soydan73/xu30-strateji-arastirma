# HK-20261103-05 — "Open Drive" konum kuralı (T anına kadarki seans aralığında açılış bir uçta, kapanış karşı uçta).
# Eğitim YOK. Yalnız s.iloc[:i+1] kullanılır.
import numpy as np


def sinyal(s, T=629, a=0.2, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    bas = np.flatnonzero(dk >= 570)
    if len(bas) == 0 or dk[bas[0]] > 585:
        return out
    b = bas[0]
    idx = np.flatnonzero(dk == T)
    if len(idx) == 0:
        return out
    i = idx[0]
    if i < b:
        return out
    O0 = float(s.open.iloc[b]); C = float(s.close.iloc[i])
    Hs = float(s.high.iloc[b:i + 1].max()); Ls = float(s.low.iloc[b:i + 1].min()); R = Hs - Ls
    if kontrol:
        out[i] = np.sign(C - O0); return out
    if R <= 0:
        return out
    if O0 <= Ls + a * R and C >= Ls + (1 - a) * R:
        out[i] = 1
    elif O0 >= Hs - a * R and C <= Hs - (1 - a) * R:
        out[i] = -1
    return out
