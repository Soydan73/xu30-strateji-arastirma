# HK-20261105-06 — zayif tepe / zayif dip (poor high / low) yeniden ziyareti. Tek seans; i. bar icin yalniz s.iloc[:i+1].
# Hedef/stop sinyalde izlenir: kosul bar kapanisinda gorulunce ters sinyal (-y); motor ters=True ile kapatir.
import numpy as np

TOL = 1.0


def _uc_sayilari(dk, h, l, Hs, Ls):
    p = (dk - 570) // 30
    ust = len(np.unique(p[h >= Hs - TOL])); alt = len(np.unique(p[l <= Ls + TOL]))
    return ust, alt


def sinyal(s, T=840, d=0.3, stop=True, kuyruk=False, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    idx = np.flatnonzero(dk == T - 1)
    if not len(idx):
        return out
    i = int(idx[0])
    m = (dk[:i + 1] >= 570)
    if m.sum() < 30:
        return out
    Hs, Ls = h[:i + 1][m].max(), l[:i + 1][m].min(); R = Hs - Ls
    if R <= 0:
        return out
    ust, alt = _uc_sayilari(dk[:i + 1][m], h[:i + 1][m], l[:i + 1][m], Hs, Ls)
    C = c[i]; y = 0
    if kontrol:
        if Hs - C >= C - Ls and Hs - C >= d * R:
            y = 1
        elif C - Ls > Hs - C and C - Ls >= d * R:
            y = -1
    else:
        uzun = ust >= 2 and (Hs - C) >= d * R and (not kuyruk or alt == 1)
        kisa = alt >= 2 and (C - Ls) >= d * R and (not kuyruk or ust == 1)
        if uzun and not kisa:
            y = 1
        elif kisa and not uzun:
            y = -1
    if y == 0:
        return out
    out[i] = y
    hedef = Hs - TOL if y > 0 else Ls + TOL
    st = Ls if y > 0 else Hs
    for j in range(i + 1, n):          # i+1 giris bari dahil izle (motor ters cikisi j>g sartiyla)
        if (y > 0 and h[j] >= hedef) or (y < 0 and l[j] <= hedef):
            out[j] = -y; break
        if stop and ((y > 0 and l[j] <= st) or (y < 0 and h[j] >= st)):
            out[j] = -y; break
    return out
