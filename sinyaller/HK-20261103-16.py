# HK-20261103-16 — Dunku aralik icinde acilis boslugu + SMA5 uyumu -> bosluk doldurma yonunde.
# Fiyat duzeyi -> son 5 onceki seansin hepsi bilgi["ayni_vade"] True olmali. i. bar icin yalniz s.iloc[:i+1].
# Hedef/stop kapanis bazli: seviyeye ulasan ilk M1 kapanisinda ters sinyal (motor ters=True).
import numpy as np


def sinyal(s, onceki, bilgi, sma=True, hedef="uc", stop=True, pzt_cuma_haric=True, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    j = np.flatnonzero(dk == 584)  # yalniz 09:44 bari; kesik seansta yoksa sinyal yok
    if not len(j) or n < 2:
        return out
    j = j[-1]
    acilis = float(s.open.iloc[0])
    if kontrol:
        r = c[j] - acilis
        if r != 0:
            out[j] = -np.sign(r)
        return out
    if len(onceki) < 5 or not bool(np.all(bilgi["ayni_vade"][-5:])):
        return out
    if pzt_cuma_haric and bilgi["gun"].dayofweek in (0, 4):
        return out
    d = onceki[-1]
    PC = float(d.close.iloc[-1]); PH = float(d.high.max()); PL = float(d.low.min())
    son5 = onceki[-5:]
    SMA5 = float(np.mean([float(o.close.iloc[-1]) for o in son5]))
    ATR5 = float(np.mean([float(o.high.max() - o.low.min()) for o in son5]))
    y = 0
    if PL < acilis < PC and (not sma or c[j] > SMA5):
        y = 1
    elif PC < acilis < PH and (not sma or c[j] < SMA5):
        y = -1
    if y == 0:
        return out
    out[j] = y
    if hedef == "uc":
        hed = PH if y > 0 else PL
    else:
        hed = PC
    sev = acilis - y * 0.5 * ATR5 if stop else None
    for k in range(j + 1, n):
        if (y > 0 and c[k] >= hed) or (y < 0 and c[k] <= hed):
            out[k] = -y; break
        if sev is not None and ((y > 0 and c[k] <= sev) or (y < 0 and c[k] >= sev)):
            out[k] = -y; break
    return out
