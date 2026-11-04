# HK-20261104-01 — Gun-arasi deger gocu: gelisen VA/POC dunku VA disinda -> o yonde 18:05'e (motor_cok).
# Profil tanimi sinyaller/vp_profil.py ile ayni (kova 1 p, VA %70); statik denetim yuzunden onbelleksiz kopya.
# Fiyat duzeyi -> bilgi["ayni_vade"][-1] True olmali. i. bar icin yalniz s.iloc[:i+1] (profil karar barina kadar).
import numpy as np


def _profil(s, son, va_oran=0.70):
    """s'nin 0..son (dahil) barlarindan POC, VAH, VAL."""
    h = np.floor(s.high.to_numpy(float)[:son + 1]).astype(int)
    l = np.floor(s.low.to_numpy(float)[:son + 1]).astype(int)
    c = s.close.to_numpy(float)[:son + 1]; v = s.volume.to_numpy(float)[:son + 1]
    taban = l.min() - 1; prof = np.zeros(h.max() + 2 - taban)
    for a, b, w in zip(l - taban, h - taban, v):
        if w > 0:
            prof[a:b + 1] += w / (b - a + 1)
    top = prof.sum()
    if top <= 0:
        return None
    lo_k, hi_k = int((l - taban).min()), int((h - taban).max())
    seg = prof[lo_k:hi_k + 1]; m = seg.max(); ad = np.flatnonzero(seg == m) + lo_k
    ck = np.floor(c[-1]) - taban
    p = int(ad[np.argmin(np.abs(ad - ck))])
    hedef = va_oran * top; birik = prof[p]; u = p; d = p
    while birik < hedef:
        yu = prof[u + 1] if u + 1 <= hi_k else -1.0
        yd = prof[d - 1] if d - 1 >= lo_k else -1.0
        if yu < 0 and yd < 0:
            break
        if yu >= yd:
            u += 1; birik += yu
        else:
            d -= 1; birik += yd
    return p + taban, u + taban + 1, d + taban   # POC, VAH, VAL


def sinyal(s, onceki, bilgi, T=720, kosul="siki", stop=False, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    jj = np.flatnonzero(dk == T - 1)
    if not len(jj):
        return out
    j = int(jj[0])
    g = _profil(s, j)
    if g is None:
        return out
    gpoc, gvah, gval = g
    if kontrol:
        a = float(s.open.iloc[0])
        if gpoc != a:
            out[j] = np.sign(gpoc - a)
        return out
    if not len(onceki) or not bool(bilgi["ayni_vade"][-1]):
        return out
    d = onceki[-1]
    dp = _profil(d, len(d) - 1)
    if dp is None:
        return out
    dpoc, dvah, dval = dp
    y = 0
    if kosul == "siki":
        if gval > dvah and gpoc > dpoc:
            y = 1
        elif gvah < dval and gpoc < dpoc:
            y = -1
    else:
        if gpoc > dvah:
            y = 1
        elif gpoc < dval:
            y = -1
    if y == 0:
        return out
    out[j] = y
    if stop:
        for k in range(j + 1, n):
            if (y > 0 and c[k] < dvah) or (y < 0 and c[k] > dval):
                out[k] = -y; break
    return out
