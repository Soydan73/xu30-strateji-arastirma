# HK-20261102-09 — Markov trend durumu geçiş olasılığı + Brier kapısı (M5). Eğitim YOK; yalnız geçmiş sayım.
# i. barda yalnız 0…i barları; M5 yalnız tamamlanmış kovalar (sinyal dk%5==4 barında).
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5_ortak import m5_tamam


def _durumlar(H, L, C, e, n_atr=14):
    k = len(C); st = np.full(k, -9)
    pc = np.r_[np.nan, C[:-1]]
    tr = np.nanmax(np.c_[H - L, np.abs(H - pc), np.abs(L - pc)], axis=1)
    for t in range(n_atr, k):
        atr = tr[t - n_atr + 1:t + 1].mean()
        if atr <= 0:
            continue
        m = (C[t] - C[t - n_atr]) / atr
        st[t] = 1 if m > e else (-1 if m < -e else 0)
    return st


def _p(st, t, W, cur, hedef):
    """t anında, son W geçiş (j→j+1, j+1 ≤ t) içinde cur'dan çıkanların hedef'e gidenlerin payı."""
    j0 = t - W
    if j0 < 0 or (st[j0:t + 1] == -9).any():
        return np.nan
    a = st[j0:t]; b = st[j0 + 1:t + 1]
    m = a == cur
    if m.sum() == 0:
        return np.nan
    return (b[m] == hedef).mean()


def sinyal(s, e=0.5, W=33, p=0.6, b=0.20, brier=True, kontrol=False):
    n = len(s); out = np.zeros(n)
    O, H, L, C, J = m5_tamam(s, n - 1)
    st = _durumlar(H, L, C, e)
    k = len(C)
    for t in range(k):
        if st[t] == -9:
            continue
        y = 0
        for yon in (1, -1):
            if st[t] != yon:
                continue
            if kontrol:
                y = yon; break
            pt = _p(st, t, W, yon, yon)
            if np.isnan(pt) or pt <= p:
                continue
            if brier:
                # son W adımda tahmin P(sonraki=yon | durum_u) ile gerçekleşen 1{st[u+1]==yon}
                err = []
                for u in range(t - W, t):
                    pu = _p(st, u, W, st[u], yon)
                    if np.isnan(pu) or st[u + 1] == -9:
                        err = None; break
                    err.append((pu - (st[u + 1] == yon)) ** 2)
                if err is None or np.mean(err) >= b:
                    continue
            y = yon
        if y:
            out[J[t]] = y
    return out
