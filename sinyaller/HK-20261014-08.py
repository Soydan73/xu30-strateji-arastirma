# HK-20261014-08 — VPIN (1 dk kova, gerçek bayraklı hacim) koşullu akış takibi (yalnız sinyal)
import numpy as np

def sinyal(s, W=30, q=0.44):
    dk = s.dk.to_numpy()
    b = s.buy_volume.to_numpy(float); se = s.sell_volume.to_numpy(float)
    d = b - se; ad = np.abs(d); v = b + se
    out = np.zeros(len(s))
    for i in range(len(s)):
        if dk[i] < 615 or dk[i] > 1020:
            continue
        j = i - W + 1
        if j < 0 or dk[j] < 570:          # pencere seans başını / açılış açık artırmasını aşamaz
            continue
        V = v[j:i + 1].sum()
        if V <= 0:
            continue
        if ad[j:i + 1].sum() / V >= q:
            y = np.sign(d[j:i + 1].sum())
            if y != 0:
                out[i] = y
                break                      # seans başına ilk koşul (motor zaten 1 işlem)
    return out
