# HK-20261015-05 — emilim barı (yüksek hacim, küçük gövde) VWAP'tan uzakta → VWAP yönüne (yalnız sinyal)
# Yalnız tamamlanmış M15 kovaları (09:30 hizalı) ve karar barına kadarki veri kullanılır.
import numpy as np


def sinyal(s, m=1.5, d=0.5, govde=0.3, atr_n=4, g=644, son=1019):
    n = len(s); out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy().astype(int)
    o = s.open.to_numpy(float); h = s.high.to_numpy(float)
    l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    v = s.volume.to_numpy(float)
    gecerli = dk >= 570
    tp = (h + l + c) / 3.0
    cum_pv = np.cumsum(np.where(gecerli, tp * v, 0.0))
    cum_v = np.cumsum(np.where(gecerli, v, 0.0))

    kova_bilgi = []          # tamamlanmış kovalar: (O, H, L, C, V)
    cur = None               # (kova_no, O, H, L, V)
    for i in range(n):
        if not gecerli[i]:
            continue
        k = (dk[i] - 570) // 15
        if cur is None or cur[0] != k:
            cur = [k, o[i], h[i], l[i], v[i]]
        else:
            cur[2] = max(cur[2], h[i]); cur[3] = min(cur[3], l[i]); cur[4] += v[i]
        if (dk[i] - 570) % 15 != 14:
            continue
        # kova k bu barın kapanışında tamamlandı
        onceki_v = [b[4] for b in kova_bilgi]
        kova_bilgi.append((cur[1], cur[2], cur[3], c[i], cur[4]))
        if len(kova_bilgi) < 5 or not (g <= dk[i] <= son):
            continue
        son_k = kova_bilgi[-atr_n:]
        atr = np.mean([b[1] - b[2] for b in son_k])
        if atr <= 0 or cum_v[i] <= 0:
            continue
        O, H, L, C, V = kova_bilgi[-1]
        med = np.median(onceki_v)
        if m > 0 and not (V >= m * med):
            continue
        if abs(C - O) > govde * atr:
            continue
        vwap = cum_pv[i] / cum_v[i]
        if C - vwap >= d * atr:
            out[i] = -1.0
        elif vwap - C >= d * atr:
            out[i] = 1.0
    return out
