# HK-20261014-13 — ABD spot açılışı sonrası ilk W dk yönünde (yalnız sinyal)
import numpy as np, pandas as pd

def _us_dst(d):
    y = d.year
    mar = pd.Timestamp(y, 3, 1); s2 = mar + pd.Timedelta(days=(6 - mar.weekday()) % 7 + 7)
    nov = pd.Timestamp(y, 11, 1); s1 = nov + pd.Timedelta(days=(6 - nov.weekday()) % 7)
    return s2 <= d < s1

def sinyal(s, W=10, teta=0.0):
    out = np.zeros(len(s)); dk = s.dk.to_numpy()
    d = s.time.iloc[0].normalize()
    o = 990 if _us_dst(d) else 1050
    a = np.flatnonzero(dk == o); b = np.flatnonzero(dk == o + W - 1)
    if not len(a) or not len(b):
        return out
    r = s.close.iloc[b[0]] / s.open.iloc[a[0]] - 1.0
    if r != 0 and abs(r) * 100 >= teta:
        out[b[0]] = np.sign(r)
    return out
