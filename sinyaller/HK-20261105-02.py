# HK-20261105-02 — Foster-Stewart rekor sayisi (son N M1 kapanis), tamamlanmis M15 sonunda karar.
# i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, N=40, t=6, d=9, yon=1, kontrol=False):
    n = len(s); out = np.zeros(n)
    c = s.close.to_numpy(float); dk = s.dk.to_numpy()
    for i in range(N - 1, n):
        if dk[i] % 15 != 14:
            continue
        w = c[i - N + 1:i + 1]
        if kontrol:
            r = w[-1] - w[0]
            if r != 0:
                out[i] = np.sign(r)
            continue
        mx = np.maximum.accumulate(w); mn = np.minimum.accumulate(w)
        Hs = int((w[1:] > mx[:-1]).sum()); Ls = int((w[1:] < mn[:-1]).sum())
        T = Hs - Ls; D = Hs + Ls
        if abs(T) >= t and D >= d:
            out[i] = yon * np.sign(T)
    return out
