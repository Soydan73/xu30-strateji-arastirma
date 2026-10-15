# HK-20261015-03 — seans yeni ucunun gerçek CVD yeni ucuyla teyitli kırılımı → takip (yalnız sinyal)
import numpy as np

BAS = 570          # 09:30, M15 hizası
SON = 1004         # son karar barı 16:44


def sinyal(s, g=644, mod="c1", esik=0.15):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    b = s.buy_volume.to_numpy(float); sv = s.sell_volume.to_numpy(float)
    ref_h = -np.inf; ref_l = np.inf          # önceki tamamlanmış kovalar
    cvd_max = -np.inf; cvd_min = np.inf
    cvd = 0.0
    kova = None; kh = -np.inf; kl = np.inf; kb = 0.0; ks = 0.0
    for i in range(n):
        d = dk[i]
        if d < BAS:
            continue
        cvd += b[i] - sv[i]
        k = (d - BAS) // 15
        if k != kova:
            kova = k; kh = -np.inf; kl = np.inf; kb = 0.0; ks = 0.0
        kh = max(kh, h[i]); kl = min(kl, l[i]); kb += b[i]; ks += sv[i]
        if (d - BAS) % 15 != 14:
            continue
        # kova tamamlandı: karar
        if g <= d <= SON and np.isfinite(ref_h):
            oran = (kb - ks) / (kb + ks) if (kb + ks) > 0 else 0.0
            uzun = c[i] > ref_h and cvd > cvd_max and cvd > 0
            kisa = c[i] < ref_l and cvd < cvd_min and cvd < 0
            if mod == "c2":
                uzun = uzun and oran >= esik
                kisa = kisa and oran <= -esik
            if uzun != kisa:
                out[i] = 1 if uzun else -1
        # referansları bu kovayla güncelle (sonraki kararlar için)
        ref_h = max(ref_h, kh); ref_l = min(ref_l, kl)
        cvd_max = max(cvd_max, cvd); cvd_min = min(cvd_min, cvd)
    return out
