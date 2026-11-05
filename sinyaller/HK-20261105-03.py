# HK-20261105-03 — RFSV puruzluluk (log-oynaklik yerel Hurst) suzgecli sabah momentumu.
# Yalniz oynaklik istatistigi onceki seanslardan; fiyat duzeyi karsilastirmasi yok. i. bar icin yalniz s.iloc[:i+1].
import numpy as np

N_BLOK, D_MAX, N_GECMIS, GEREKEN = 100, 13, 20, 30


def _bloklar(d, son_dk):
    """Seansin dk < son_dk icindeki TAMAMLANMIS 30 dk bloklarinin 0.5*log(RV) degerleri."""
    dk = d.dk.to_numpy(); c = d.close.to_numpy(float)
    if len(c) < 2:
        return []
    r = np.diff(np.log(c)); rdk = dk[1:]
    b = (rdk - 570) // 30
    out = []
    for k in np.unique(b[(rdk >= 570)]):
        bitis = 570 + 30 * (k + 1)
        if bitis > son_dk:
            continue
        rv = float((r[b == k] ** 2).sum())
        if rv > 0:
            out.append(0.5 * np.log(rv))
    return out


def _hurst(x):
    x = np.asarray(x[-N_BLOK:], float)
    if len(x) < N_BLOK:
        return None
    lags = np.arange(1, D_MAX + 1)
    m = np.array([np.mean((x[l:] - x[:-l]) ** 2) for l in lags])
    if np.any(m <= 0):
        return None
    return float(np.polyfit(np.log(lags), np.log(m), 1)[0] / 2.0)


def sinyal(s, onceki, bilgi, suzgec="ust_medyan", T=660, H=120):
    n = len(s); out = np.zeros(n)
    if n < 2 or len(onceki) < GEREKEN:
        return out
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk == T - 1)
    if not len(idx):
        return out
    i = int(idx[0])
    bas = np.flatnonzero(dk >= 585)
    if not len(bas) or bas[0] > i:
        return out
    yon = np.sign(float(s.close.iloc[i]) - float(s.open.iloc[int(bas[0])]))
    if yon == 0:
        return out
    if suzgec == "yok":
        out[i] = yon
        return out
    tam = [_bloklar(d, 10 ** 6) for d in onceki]          # onceki seanslarin tum bloklari
    kismi = [_bloklar(d, T) for d in onceki]              # ayni karar anina kadar
    bugun = _bloklar(s.iloc[:i + 1], T)
    def h_at(j, bugun_bl):
        seri = [v for q in tam[:j] for v in q] + bugun_bl
        return _hurst(seri)
    hb = h_at(len(onceki), bugun)
    if hb is None:
        return out
    gec = [h_at(j, kismi[j]) for j in range(len(onceki) - N_GECMIS, len(onceki))]
    gec = np.array([g for g in gec if g is not None])
    if len(gec) < N_GECMIS // 2:
        return out
    if suzgec == "ust_medyan" and not hb > np.median(gec):
        return out
    if suzgec == "ust75" and not hb > np.percentile(gec, 75):
        return out
    if suzgec == "alt_medyan" and not hb < np.median(gec):
        return out
    out[i] = yon
    return out
