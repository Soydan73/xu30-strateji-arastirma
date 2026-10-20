# HK-20261020-05 — Gelişen POC'den (dVPOC) aşırı uzaklaşmada dVPOC'ye dönüş (NexusFi dVA/dVPOC kuralı)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Tek seans, i. bara kadar olan M1 barları.
import numpy as np


def _dvpoc_dizisi(s, dagitim="aralik", bin_oran=0.0003):
    """Her bar i için o bara kadarki (dahil) hacim profilinin POC'u. Kova genişliği = ilk açılış × bin_oran.
    dagitim 'aralik': bar hacmi [low, high] kovalarına eşit dağıtılır; 'kapanis': tümü kapanış kovasına."""
    o = s.open.to_numpy(float); h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    c = s.close.to_numpy(float); v = s.volume.to_numpy(float)
    n = len(s)
    B = max(o[0] * bin_oran, 1e-9)
    taban = np.floor(l.min() / B) - 1 if n else 0
    lo_k = (np.floor(l / B) - taban).astype(int); hi_k = (np.floor(h / B) - taban).astype(int)
    c_k = (np.floor(c / B) - taban).astype(int)
    prof = np.zeros(int(hi_k.max()) + 2 if n else 1)
    poc = np.full(n, np.nan)
    for i in range(n):
        if dagitim == "kapanis":
            prof[c_k[i]] += v[i]
        else:
            a, b = lo_k[i], hi_k[i]
            prof[a:b + 1] += v[i] / (b - a + 1)
        k = int(np.argmax(prof))          # eşitlikte en düşük kova (deterministik)
        poc[i] = (k + taban + 0.5) * B
    return poc


def sinyal(s, mod="poc", k=1.5, bas=630, son=960, dagitim="aralik"):
    """mod 'poc': |C − dVPOC| ≥ k·IB → dVPOC yönünde. mod 'acilis' (KONTROL): |C − seans açılışı| ≥ k·IB → açılış yönünde.
    IB = dk 570–629 (09:30–10:29) barlarının yüksek−düşük aralığı; sinyal yalnız dk ∈ [bas, son]."""
    n = len(s)
    out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    ib_idx = np.flatnonzero(dk < 630)
    if len(ib_idx) < 30:
        return out
    son_ib = ib_idx[-1]
    if son_ib >= n - 1 and dk[-1] < 630:
        return out
    IB = h[ib_idx].max() - l[ib_idx].min()
    if IB <= 0:
        return out
    ref = _dvpoc_dizisi(s, dagitim) if mod == "poc" else np.full(n, s.open.iloc[0])
    for i in range(n):
        if dk[i] < max(bas, 630) or dk[i] > son:
            continue
        d = c[i] - ref[i]
        if abs(d) >= k * IB:
            out[i] = -np.sign(d)
    return out
