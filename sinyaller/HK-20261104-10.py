# HK-20261104-10 — Llorente korunma islemi vekili: yuksek hacim + dengeli bayrakli delta ile buyuk M15 hareketi -> donus
# (kontrol: dengesiz delta -> devam). Yalniz tamamlanmis M15 kovalari (dk%15==14 son dakikasi gelmis). i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, v_esik=0.5, k=1.0, d_esik=0.10, devam=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    v = s.volume.to_numpy(float); b = s.buy_volume.to_numpy(float); sv = s.sell_volume.to_numpy(float)
    kova = dk // 15
    gecmis_lv = []; gecmis_ar = []
    bas = 0
    for i in range(n):
        if i > 0 and kova[i] != kova[i - 1]:
            bas = i
        if dk[i] % 15 != 14:
            continue
        r = c[i] - o[bas]; V = v[bas:i + 1].sum()
        dl = b[bas:i + 1].sum() - sv[bas:i + 1].sum()
        if V <= 0:
            continue
        lv = np.log(V); imb = abs(dl) / V
        if 614 <= dk[i] <= 1034 and len(gecmis_lv) >= 4 and r != 0:
            Vz = lv - np.mean(gecmis_lv); A = np.mean(gecmis_ar)
            if Vz >= v_esik and abs(r) >= k * A:
                if devam and imb >= d_esik:
                    out[i] = np.sign(r)
                elif (not devam) and imb <= d_esik:
                    out[i] = -np.sign(r)
        gecmis_lv.append(lv); gecmis_ar.append(abs(r))
    return out
