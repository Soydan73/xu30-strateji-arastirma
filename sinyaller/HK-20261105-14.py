# HK-20261105-14 — M15 pencere alt ucu + gercek hacim artisi (JKX ikinci ozellik, egitimsiz). motor 1.00.
# Yalniz TAMAMLANMIS M15 kovalari (son bari dk%15==14, kovada >= 8 bar), bugunun 09:30 kovasindan itibaren.
import numpy as np


def _kovalar(s):
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    c = s.close.to_numpy(float); v = s.volume.to_numpy(float)
    kova = dk // 15
    out = []; bas = 0
    for j in range(len(dk)):
        if j == len(dk) - 1 or kova[j + 1] != kova[j]:
            if dk[j] % 15 == 14 and dk[j] >= 584 and (j - bas + 1) >= 8:
                out.append((j, h[bas:j + 1].max(), l[bas:j + 1].min(), c[j], v[bas:j + 1].sum()))
            bas = j + 1
    return out


def sinyal(s, w=5, kt=0.2, m=1.2, yon="uzun", H=60):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    kov = _kovalar(s)
    dk = s.dk.to_numpy()
    for q in range(2 * w - 1, len(kov)):
        j = kov[q][0]
        if dk[j] > 1064:
            break
        pen = kov[q - w + 1:q + 1]; onc = kov[q - 2 * w + 1:q - w + 1]
        Hw = max(x[1] for x in pen); Lw = min(x[2] for x in pen); C = pen[-1][3]
        if Hw - Lw <= 0:
            continue
        k = (C - Lw) / (Hw - Lw)
        vo = sum(x[4] for x in onc); vp = sum(x[4] for x in pen)
        if m > 0:
            if vo <= 0 or vp / vo < m:
                continue
        if k <= kt:
            out[j] = 1
        elif yon == "ikisi" and k >= 1 - kt:
            out[j] = -1
    return out
