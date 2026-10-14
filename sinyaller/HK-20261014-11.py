# HK-20261014-11 — hacim koşullu 30 dk dönüş/devam (yalnız sinyal)
import numpy as np

def sinyal(s, mod="rev", rv_esik=0.559, teta=0.158):
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float); v = s.volume.to_numpy(float)
    out = np.zeros(len(s))
    son = dk[-1] if len(dk) else 0
    pencereler = []                     # (a, V) tamamlanmış pencereler
    for a in range(600, 1020, 30):      # 10:00 … 16:30 başlangıç
        if a + 29 > son:
            break                       # pencere henüz tamamlanmadı (bitmemiş veri kullanılmaz)
        idx = np.flatnonzero((dk >= a) & (dk <= a + 29))
        if len(idx) < 25 or dk[idx[-1]] != a + 29:
            continue
        V = v[idx].sum()
        if a >= 630 and len(pencereler) >= 2:
            RV = V / np.median([x[1] for x in pencereler])
            r = c[idx[-1]] / o[idx[0]] - 1.0
            if r != 0 and abs(r) * 100 >= teta:
                if mod == "rev" and RV <= rv_esik:
                    out[idx[-1]] = -np.sign(r)
                elif mod == "dev" and RV >= rv_esik:
                    out[idx[-1]] = np.sign(r)
        pencereler.append((a, V))
    return out
