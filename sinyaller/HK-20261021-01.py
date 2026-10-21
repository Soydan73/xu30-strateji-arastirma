# HK-20261021-01 — ABD 08:30 ET veri penceresi (15:30 / kış 16:30 TR) ilk 5 dk sıçramasının dönüşü
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Tek seans; yalnız t0+4 barına kadarki barlar kullanılır.
import numpy as np, pandas as pd


def _us_dst(d):
    y = d.year
    mar = pd.Timestamp(y, 3, 1); s2 = mar + pd.Timedelta(days=(6 - mar.weekday()) % 7 + 7)
    nov = pd.Timestamp(y, 11, 1); s1 = nov + pd.Timedelta(days=(6 - nov.weekday()) % 7)
    return s2 <= d < s1


def sinyal(s, k=1.5, kaydir=0):
    n = len(s); out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy()
    d = s.time.iloc[0].normalize()
    t0 = (930 if _us_dst(d) else 990) + kaydir
    a = np.flatnonzero(dk == t0); b = np.flatnonzero(dk == t0 + 4)
    if not len(a) or not len(b):
        return out
    h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    blok = []
    for b0 in range(570, t0 - 4, 5):
        m = (dk >= b0) & (dk < b0 + 5) & (dk < t0)
        if m.sum() == 5:
            blok.append(h[m].max() - l[m].min())
    if len(blok) < 6:
        return out
    A = float(np.mean(blok))
    R = s.close.iloc[b[0]] - s.open.iloc[a[0]]
    if A > 0 and R != 0 and abs(R) >= k * A:
        out[b[0]] = -np.sign(R)
    return out
