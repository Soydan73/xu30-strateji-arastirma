# HK-20261020-04 — M15 İç Bar Gücü (IBS, kapanış konumu) dönüşü: tamamlanmış M15 kovası kendi aralığının
# alt ucunda kapandıysa uzun, üst ucunda kapandıysa kısa (yalnız sinyal fonksiyonu; model eğitimi YOK)
import numpy as np


def m15_kovalar(s):
    """Tamamlanmış M15 kovaları: (sinyal_bar_indeksi, açılış, yüksek, düşük, kapanış). Kova dk//15, dk>=570,
    dk%15==14 olan M1 barı kapanınca tamamlanır; >= 12 bar içermeli. Yalnız o bara kadarki veri kullanılır."""
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); h = s.high.to_numpy(float)
    l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    out = []
    for i in range(len(s)):
        if dk[i] < 570 or dk[i] % 15 != 14:
            continue
        k = dk[i] // 15
        idx = np.flatnonzero((dk[: i + 1] >= 570) & (dk[: i + 1] // 15 == k))
        if len(idx) < 12:
            continue
        out.append((i, o[idx[0]], h[idx].max(), l[idx].min(), c[i]))
    return out


def sinyal(s, mod="ibs", e=0.2, r_esik=0.0, yalniz_uzun=False, H=45):
    """mod: 'govde' (KONTROL: her kovada gövde işaretinin tersi), 'ibs' (IBS <= e uzun, >= 1-e kısa).
    r_esik: kova aralığı (yüksek-düşük)/kapanış*1e4 bps alt sınırı. Sinyal kovaları 09:59–16:59 (dk 599–1019)."""
    n = len(s)
    out = np.zeros(n)
    dk = s.dk.to_numpy()
    for i, o, h, l, c in m15_kovalar(s):
        if not (599 <= dk[i] <= 1019):
            continue
        R = h - l
        if R <= 0 or R / c * 1e4 < r_esik:
            continue
        if mod == "govde":
            y = -np.sign(c - o)
        else:
            ibs = (c - l) / R
            y = 1 if ibs <= e else (-1 if ibs >= 1 - e else 0)
        if yalniz_uzun and y < 0:
            y = 0
        out[i] = y
    return out
