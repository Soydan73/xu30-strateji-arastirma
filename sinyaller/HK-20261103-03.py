# HK-20261103-03 — M1 getiri ACF1 (son W) ≥ ρ iken SMA15−SMA60 yönünde; M15 karar barında. Eğitim YOK.
import numpy as np


def sinyal(s, W=60, rho=0.10, kapi=True, dk_bas=660, dk_son=1004):
    n = len(s); out = np.zeros(n)
    c = s.close.to_numpy(float); dk = s.dk.to_numpy()
    ilk = np.searchsorted(dk, 570)          # 09:30 ilk sürekli işlem barı
    for i in range(n):
        if dk[i] % 15 != 14 or not (dk_bas <= dk[i] <= dk_son):
            continue
        if i - ilk < max(W + 1, 60):
            continue
        sma15 = c[i - 14:i + 1].mean(); sma60 = c[i - 59:i + 1].mean()
        yon = np.sign(sma15 - sma60)
        if yon == 0:
            continue
        if kapi:
            r = np.diff(c[i - W - 1:i + 1])          # W+1 getiri, hepsi dk>=570 barlarından
            a, b = r[1:], r[:-1]
            if a.std() == 0 or b.std() == 0:
                continue
            if np.corrcoef(a, b)[0, 1] < rho:
                continue
        out[i] = yon
    return out
