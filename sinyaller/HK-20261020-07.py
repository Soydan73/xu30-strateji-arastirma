# HK-20261020-07 — Seans içi fiyat–CVD salınım ayrışması (M15 kovaları), yeni seans ucu + zayıf CVD → ters
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Tek seans, i. bara kadar olan M1 barları; yalnız tamamlanmış M15 kovaları.
import numpy as np


def sinyal(s, mod="ayrisma", m=2, bas=629, son=989):
    n = len(s)
    out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy()
    h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    d = (s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float))
    d = np.where(dk >= 570, d, 0.0)
    cvd = np.cumsum(d)
    kova = np.where(dk >= 570, (dk - 570) // 15, -1)
    # her kova için: kapanış barı indeksi (dk = 570+15b+14), kova tepe/dip (yalnız o kovanın barları)
    bitis = {}
    for i in range(n):
        b = kova[i]
        if b >= 0 and dk[i] == 570 + 15 * b + 14:
            bitis[int(b)] = i
    tepe_b = None; dip_b = None          # önceki seans tepesi/dibi olan tamamlanmış kova
    kov_h = {}; kov_l = {}; kov_c = {}
    bas_i = 0
    for b in sorted(bitis):
        i = bitis[b]
        idx = np.flatnonzero((kova == b) & (np.arange(n) <= i))
        if len(idx) == 0:
            continue
        kh, kl, kc = h[idx].max(), l[idx].min(), cvd[i]
        y = 0
        if tepe_b is not None and len(kov_h) >= 4 and bas <= dk[i] <= son:
            if kh > kov_h[tepe_b] and b - tepe_b >= m:
                if mod == "ayrisma" and kc < kov_c[tepe_b]: y = -1
                elif mod == "onay" and kc > kov_c[tepe_b]: y = -1
                elif mod == "uc": y = -1
            if y == 0 and kl < kov_l[dip_b] and b - dip_b >= m:
                if mod == "ayrisma" and kc > kov_c[dip_b]: y = 1
                elif mod == "onay" and kc < kov_c[dip_b]: y = 1
                elif mod == "uc": y = 1
        if y != 0:
            out[i] = y
        kov_h[b], kov_l[b], kov_c[b] = kh, kl, kc
        if tepe_b is None or kh > kov_h[tepe_b]: tepe_b = b
        if dip_b is None or kl < kov_l[dip_b]: dip_b = b
    return out
