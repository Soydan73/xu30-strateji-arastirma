# HK-20261103-07 — Sıralı örüntü zaman-tersinmezliği (Bandt-Pompe d=3) yüksekse pencere yönünde (trend rejimi).
# Kaynak: mql5 makale 23451 (Qamar 2026). Eğitim YOK. Yalnız s.iloc[:i+1] kullanılır.
import numpy as np

# d=3 örüntüleri: argsort sırası -> indeks. Zaman tersi (x3,x2,x1) örüntüsü eşlemesi.
_PERM = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
_IDX = {p: k for k, p in enumerate(_PERM)}


def _kod(a, b, c):
    return _IDX[tuple(np.argsort(np.array([a, b, c]), kind="stable"))]


def _js2(p, q):
    m = 0.5 * (p + q)
    def kl(x, y):
        k = x > 0
        return float(np.sum(x[k] * np.log2(x[k] / y[k])))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def tersinmezlik(x):
    """x: fiyat penceresi. ileri örüntü histogramı ile ters çevrilmiş serinin histogramı arasında JS (log2)."""
    n = len(x)
    if n < 4:
        return np.nan
    ileri = np.zeros(6); ters = np.zeros(6)
    xr = x[::-1]
    for j in range(n - 2):
        ileri[_kod(x[j], x[j + 1], x[j + 2])] += 1
        ters[_kod(xr[j], xr[j + 1], xr[j + 2])] += 1
    return _js2(ileri / ileri.sum(), ters / ters.sum())


def sinyal(s, W=90, theta=0.03, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    bas = np.flatnonzero(dk >= 570)
    if len(bas) == 0:
        return out
    b = bas[0]
    for i in range(b, n):
        if dk[i] % 15 != 14 or dk[i] < 600 or dk[i] > 1064:   # tamamlanmış M15 kapanışı, 10:00–17:45 arası karar
            continue
        if i - W < b:                                        # pencere seans başını aşamaz
            continue
        yon = np.sign(c[i] - c[i - W])
        if yon == 0:
            continue
        if kontrol:
            out[i] = yon; continue
        irr = tersinmezlik(c[i - W:i + 1])
        if irr >= theta:
            out[i] = yon
    return out
