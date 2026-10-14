# HK-20261014-05 — Drift burst (Christensen-Oomen-Renò) M1 uyarlaması: patlayıcı 5 dk sürüklenme → ters yönde gir (yalnız sinyal)
import numpy as np

L_DRIFT, L_VOL = 5, 25

def t_istatistigi(c, i):
    """i. bar kapanışında: T = log(c[i]/c[i-5]) / (sigma1 * sqrt(5)); sigma1 = önceki 25 bar (i-29..i-5) 1 dk log getiri std'si."""
    if i < L_DRIFT + L_VOL:
        return np.nan
    lr = np.diff(np.log(c[i - L_DRIFT - L_VOL: i - L_DRIFT + 1]))   # 25 getiri, sürüklenme penceresinden önce
    sd = lr.std(ddof=1)
    if not np.isfinite(sd) or sd <= 0:
        return np.nan
    return np.log(c[i] / c[i - L_DRIFT]) / (sd * np.sqrt(L_DRIFT))

def sinyal(s, tau=4.0, yon="her", hacim_kat=0.0):
    c = s.close.to_numpy(float); dk = s.dk.to_numpy(); v = s.volume.to_numpy(float)
    out = np.zeros(len(s))
    ilk = np.flatnonzero(dk >= 570)
    if not len(ilk):
        return out
    b0 = ilk[0]                                    # 09:30 sonrası ilk bar; açılış açık artırması penceresi dışarıda
    for i in range(b0 + L_DRIFT + L_VOL, len(s)):
        if dk[i] < 584 or dk[i] > 1079:
            continue
        T = t_istatistigi(c[b0: i + 1], i - b0)
        if not np.isfinite(T) or abs(T) < tau:
            continue
        if yon == "neg" and T > 0:
            continue
        if hacim_kat > 0:
            v5 = v[i - 4: i + 1].mean(); v25 = v[i - 29: i - 4].mean()
            if v25 <= 0 or v5 < hacim_kat * v25:
                continue
        out[i] = -np.sign(T)
    return out
