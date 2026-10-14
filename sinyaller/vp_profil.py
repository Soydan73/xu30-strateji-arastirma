# Gelişen hacim profili (tek seans, M1 yaklaşık) — HK-20261014-17/18 ortak yardımcı (yalnız geçmiş barlar)
import numpy as np

_ONBELLEK = {}

def gelisen_profil(s, va_oran=0.70):
    """Her i barı için (bar i dahil) POC, VAH, VAL. Kova 1 p, çapa mutlak sıfır.
    Bar hacmi floor(low)..floor(high) kovalarına eşit dağıtılır. Önbellek anahtarı (ilk zaman, uzunluk, son zaman)."""
    anahtar = (s.time.iloc[0], len(s), s.time.iloc[-1], va_oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    h = np.floor(s.high.to_numpy(float)).astype(int); l = np.floor(s.low.to_numpy(float)).astype(int)
    c = s.close.to_numpy(float); v = s.volume.to_numpy(float)
    n = len(s); taban = l.min() - 1; ust = h.max() + 2
    prof = np.zeros(ust - taban)
    poc = np.full(n, np.nan); vah = np.full(n, np.nan); val = np.full(n, np.nan)
    lo_k, hi_k = None, None
    for i in range(n):
        a, b = l[i] - taban, h[i] - taban
        if v[i] > 0:
            prof[a:b + 1] += v[i] / (b - a + 1)
        lo_k = a if lo_k is None else min(lo_k, a); hi_k = b if hi_k is None else max(hi_k, b)
        top = prof.sum()
        if top <= 0:
            continue
        seg = prof[lo_k:hi_k + 1]
        m = seg.max(); adaylar = np.flatnonzero(seg == m) + lo_k
        ck = np.floor(c[i]) - taban
        p = int(adaylar[np.argmin(np.abs(adaylar - ck))])   # eşitlikte kapanışa en yakın, sonra alttaki (argmin ilkini verir)
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
        poc[i] = p + taban; vah[i] = u + taban + 1; val[i] = d + taban
    r = (poc, vah, val)
    if len(_ONBELLEK) > 4000:
        _ONBELLEK.clear()
    _ONBELLEK[anahtar] = r
    return r
