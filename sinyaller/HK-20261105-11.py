# HK-20261105-11 — VWAP bandinda ATR rejimine gore mod (sakinde donus, oynakta kirilim). motor_cok 1.00, geri 60.
# Karar yalniz TAMAMLANMIS M15 kovalarinda (son M1'i dk%15==14). Rejim: M15 goreli aralik (H-L)/C, kayan 14'lu ortalama,
# dagilim tum onceki seanslardan (fiyat duzeyi karsilastirmasi yok). i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _kovalar(s):
    """Tamamlanmis M15 kovalari: (bitis_indeksi, H, L, C) listesi; kova = dk//15, tamam = dk%15==14 bari var."""
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    kova = dk // 15
    out = []; bas = 0
    for j in range(len(dk)):
        if j == len(dk) - 1 or kova[j + 1] != kova[j]:
            if dk[j] % 15 == 14:
                out.append((j, h[bas:j + 1].max(), l[bas:j + 1].min(), c[j]))
            bas = j + 1
    return out


def _g(k):
    return [(H - L) / C for (_, H, L, C) in k if C > 0]


def sinyal(s, onceki, bilgi, k=2.0, q_alt=1/3, q_ust=2/3, mod="ikisi", rejimsiz=False, H=600):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    if n < 2 or len(onceki) < 40:
        return out
    # --- rejim dagilimi (onceki seanslar) ---
    gg = []
    for x in onceki:
        gg += _g(_kovalar(x))
    gg = np.asarray(gg, float)
    if len(gg) < 200:
        return out
    cs = np.cumsum(np.r_[0.0, gg])
    roll = np.sort((cs[14:] - cs[:-14]) / 14.0)
    kuyruk = list(gg[-14:])
    # --- bugun ---
    dk = s.dk.to_numpy()
    c = s.close.to_numpy(float)
    tp = (s.high.to_numpy(float) + s.low.to_numpy(float) + c) / 3.0
    v = s.volume.to_numpy(float)
    cv = np.cumsum(tp * v); cv2 = np.cumsum(tp * tp * v); cvol = np.cumsum(v)
    kov = _kovalar(s)
    gun_g = []
    onc = None          # onceki karar barinin (C, VWAP, sigma)
    poz = 0; pmod = None
    for (j, Hb, Lb, Cb) in kov:
        if Cb > 0:
            gun_g.append((Hb - Lb) / Cb)
        if cvol[j] <= 0:
            continue
        vw = cv[j] / cvol[j]
        sg = np.sqrt(max(cv2[j] / cvol[j] - vw * vw, 0.0))
        d_ = int(dk[j])
        simdi = (Cb, vw, sg)
        if poz != 0:
            if pmod == "D":
                cik = (Cb >= vw or Cb < vw - (k + 1) * sg) if poz == 1 else (Cb <= vw or Cb > vw + (k + 1) * sg)
            else:
                cik = (Cb < vw or Cb < vw + 1 * sg) if poz == 1 else (Cb > vw or Cb > vw - 1 * sg)
            if cik:
                out[j] = -poz; poz = 0
            onc = simdi
            continue
        if 614 <= d_ <= 1064 and onc is not None and sg > 0 and onc[2] > 0:
            if rejimsiz:
                rej = "D"
            else:
                son = (kuyruk + gun_g)[-14:]
                atr = float(np.mean(son))
                pct = np.searchsorted(roll, atr, side="right") / len(roll)
                rej = "D" if (q_alt is not None and pct <= q_alt) else ("Y" if (q_ust is not None and pct >= q_ust) else None)
                if mod == "donus" and rej != "D":
                    rej = None
                if mod == "kirilim" and rej != "Y":
                    rej = None
            Cp, vwp, sgp = onc
            ust, alt = vw + k * sg, vw - k * sg
            ustp, altp = vwp + k * sgp, vwp - k * sgp
            y = 0
            if rej == "D":
                if Cp > ustp and Cb <= ust:
                    y = -1
                elif Cp < altp and Cb >= alt:
                    y = 1
            elif rej == "Y":
                if Cp <= ustp and Cb > ust:
                    y = 1
                elif Cp >= altp and Cb < alt:
                    y = -1
            if y != 0:
                out[j] = y; poz = y; pmod = rej
        onc = simdi
    return out
