# HK-20261102-03 — Gelişen profilde LVN geçişi (devam) / düşük hacimli taze ret (dönüş)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. i. barın profili yalnız 0…i−1 barlarından.
import numpy as np


def sinyal(s, kural="gecis", m=2.0):
    n = len(s); out = np.zeros(n)
    if n < 30:
        return out
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    v = s.volume.to_numpy(float); d = s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float)
    b = max(2, int(round(s.open.iloc[0] / 3300.0)))
    hk = np.floor(h / b).astype(int); lk = np.floor(l / b).astype(int); ck = np.floor(c / b).astype(int)
    taban = lk.min() - 2; L = hk.max() - taban + 3
    prof = np.zeros(L)
    for i in range(n):
        if i >= 21 and 630 <= dk[i] <= 1050 and prof.sum() > 0:
            sm = prof.copy(); sm[1:] += prof[:-1]; sm[:-1] += prof[1:]
            # üst/alt maksimumlar (j hariç)
            ust = np.maximum.accumulate(sm[::-1])[::-1]; ust = np.append(ust[1:], 0.0)
            alt = np.maximum.accumulate(sm); alt = np.insert(alt[:-1], 0, 0.0)
            lvn = (sm <= 0.25 * np.minimum(ust, alt)) & (np.minimum(ust, alt) > 0)
            ort = v[i - 20:i].mean()
            if kural in ("gecis", "kontrol"):
                k0 = ck[i - 1] - taban; k1 = ck[i] - taban
                if k1 != k0 and ort > 0 and v[i] >= m * ort:
                    y = 1 if k1 > k0 else -1
                    if np.sign(d[i]) == y:
                        if kural == "kontrol":
                            out[i] = y
                        else:
                            a, z = (k0 + 1, k1) if y > 0 else (k1, k0 - 1)
                            if lvn[a:z + 1].any():
                                out[i] = y
            else:  # ret
                if ort > 0 and v[i] <= 1.0 * ort:
                    kc = ck[i] - taban; kh = hk[i] - taban; kl = lk[i] - taban
                    lo30 = lk[max(0, i - 30):i] - taban; hi30 = hk[max(0, i - 30):i] - taban
                    def taze(j):
                        return not np.any((lo30 <= j) & (hi30 >= j))
                    yuk = [j for j in range(kc + 1, kh + 1) if lvn[j] and taze(j)]
                    asg = [j for j in range(kl, kc) if lvn[j] and taze(j)]
                    sinyal_ = 0
                    if yuk and not asg and d[i] <= 0:
                        sinyal_ = -1
                    elif asg and not yuk and d[i] >= 0:
                        sinyal_ = 1
                    out[i] = sinyal_
        if v[i] > 0:
            a, z = lk[i] - taban, hk[i] - taban
            prof[a:z + 1] += v[i] / (z - a + 1)
    return out
