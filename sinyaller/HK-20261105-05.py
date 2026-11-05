# HK-20261105-05 — kolay hareketin sonmesi: buyuk M15 hareketi + saat profiline gore dusuk hacim -> ters.
# Yalniz hacim/oynaklik istatistigi onceki seanslardan; fiyat duzeyi karsilastirmasi yok. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _dilimler(d):
    """{dilim_basi_dk: (m, v, son_bar_indeksi)} yalniz TAMAMLANMIS (son dakikasi mevcut) dilimler."""
    dk = d.dk.to_numpy(); o = d.open.to_numpy(float); c = d.close.to_numpy(float); v = d.volume.to_numpy(float)
    out = {}
    bas = 570 + ((dk - 570) // 15) * 15
    for b in np.unique(bas[dk >= 570]):
        ix = np.flatnonzero(bas == b)
        if dk[ix[-1]] != b + 14:
            continue
        out[int(b)] = (c[ix[-1]] - o[ix[0]], v[ix].sum(), int(ix[-1]))
    return out


def sinyal(s, onceki, bilgi, k=1.0, h=0.7, n_gecmis=20, H=30):   # H yalniz cikis parametresi (motor_cok varyant sozlugunu sinyale de iletir)
    n = len(s); out = np.zeros(n)
    if n < 2 or len(onceki) < n_gecmis:
        return out
    gec = [_dilimler(d) for d in onceki[-n_gecmis:]]
    bugun = _dilimler(s)
    for b, (m, v, i) in bugun.items():
        if not (585 <= b <= 1020):
            continue
        ms = np.array([g[b][0] for g in gec if b in g]); vs = np.array([g[b][1] for g in gec if b in g])
        if len(ms) < n_gecmis // 2:
            continue
        sg = ms.std(ddof=1)
        if not sg > 0 or abs(m) < k * sg or m == 0:
            continue
        if h is not None and not v < h * np.median(vs):
            continue
        out[i] = -np.sign(m)
    return out
