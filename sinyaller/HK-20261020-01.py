# HK-20261020-01 — VWAP tek taraflı tutunma (sıfır kesişim) → trend günü devamı (yalnız sinyal fonksiyonu)
import numpy as np


def sinyal(s, W=30, sinif="sifir", giris="hemen", cikis="seans", son_bekle=900):
    """sinif: 'sifir' (pencerede tüm M5 kapanışları VWAP'ın aynı tarafında) | 'kontrol' (koşulsuz VWAP tarafı).
    giris: 'hemen' | 'geri' (ilk ±1σ bant teması, kapanış VWAP tarafında).
    cikis: 'seans' | 'vwap' (girişten sonra kapanış VWAP'ın karşı tarafında → ters sinyal).
    Her bar i için yalnız s.iloc[:i+1] kullanılır (kümülatif VWAP/σ geçmişe bakar)."""
    n = len(s)
    out = np.zeros(n)
    dk = s.dk.to_numpy()
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    v = s.volume.to_numpy(float)
    tp = (h + l + c) / 3.0
    cv = np.cumsum(v)
    with np.errstate(invalid="ignore", divide="ignore"):
        vw = np.cumsum(tp * v) / cv
        m2 = np.cumsum(v * tp * tp) / cv
    sd = np.sqrt(np.maximum(m2 - vw * vw, 0.0))
    sur = np.flatnonzero(dk >= 570)
    if not len(sur):
        return out
    dk0 = dk[sur[0]]
    ii = np.flatnonzero(dk == dk0 + W - 1)
    if not len(ii):
        return out
    i0 = ii[0]
    if not np.isfinite(vw[i0]):
        return out
    if sinif == "sifir":
        m5 = np.flatnonzero((dk >= dk0 + 5) & (dk <= dk0 + W - 1) & ((dk - dk0) % 5 == 4))
        m5 = m5[m5 <= i0]
        if len(m5) < 2:
            return out
        isr = np.sign(c[m5] - vw[m5])
        if not (np.all(isr == isr[0]) and isr[0] != 0):
            return out
        y = isr[0]
    else:
        y = np.sign(c[i0] - vw[i0])
        if y == 0:
            return out
    e = None
    if giris == "hemen":
        e = i0
    else:
        for j in range(i0 + 1, n):
            if dk[j] > son_bekle:
                break
            if y * (c[j] - vw[j]) < 0:
                break  # karşı tarafta kapanış: kurulum iptal
            if y > 0 and l[j] <= vw[j] + sd[j] and c[j] > vw[j]:
                e = j; break
            if y < 0 and h[j] >= vw[j] - sd[j] and c[j] < vw[j]:
                e = j; break
    if e is None:
        return out
    out[e] = y
    if cikis == "vwap":
        for j in range(e + 1, n):
            if y * (c[j] - vw[j]) < 0:
                out[j] = -y
    return out
