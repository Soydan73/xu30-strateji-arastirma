# HK-20261103-09 — Açılış atağı sonrası VWAP'a ilk geri çekilme (hacim kuruması şartlı) → test barı ucu kırılımı.
# Kaynak: daytradingtoolkit.com first pullback to VWAP. Eğitim YOK. i. bar için yalnız s.iloc[:i+1] kullanılır
# (kümülatif VWAP; atak penceresi 09:45–10:14 tamamlanmadan karar verilmez).
import numpy as np


def sinyal(s, a=0.004, h=0.5, delta=False, d=0.10, kontrol=False, bekle=15):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    o = s.open.to_numpy(float); hi = s.high.to_numpy(float); lo = s.low.to_numpy(float); c = s.close.to_numpy(float)
    v = s.volume.to_numpy(float)
    dl = s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float)
    tp = (hi + lo + c) / 3.0
    cv = np.cumsum(v)
    with np.errstate(invalid="ignore", divide="ignore"):
        vw = np.cumsum(tp * v) / cv
    ab = np.flatnonzero(dk == 585)          # 09:45 barı
    ae = np.flatnonzero(dk == 614)          # 10:14 barı
    if not len(ab) or not len(ae):
        return out
    ab, ae = ab[0], ae[0]
    y = np.sign(c[ae] - o[ab])
    if y == 0 or abs(c[ae] - o[ab]) / o[ab] < a:
        return out
    seg = slice(ab, ae + 1)
    uc = ab + (int(np.argmax(hi[seg])) if y > 0 else int(np.argmin(lo[seg])))
    atak_v = v[seg].mean()
    # ilk VWAP dokunuşu 10:15–12:00
    t = None
    for j in range(ae + 1, n):
        if dk[j] > 720:
            break
        if not np.isfinite(vw[j]):
            continue
        if (y > 0 and lo[j] <= vw[j]) or (y < 0 and hi[j] >= vw[j]):
            t = j; break
    if t is None:
        return out
    if not kontrol:
        geri = slice(uc + 1, t + 1)
        gv = v[geri]
        if len(gv) == 0 or gv.mean() >= h * atak_v:
            return out
        if delta:
            sv = gv.sum()
            if sv <= 0 or (-y * dl[geri].sum() / sv) >= d:
                return out
    for k in range(t + 1, min(t + 1 + bekle, n)):
        if (y > 0 and c[k] > hi[t]) or (y < 0 and c[k] < lo[t]):
            out[k] = y
            break
    return out
