# HK-20261103-15 — Dunun gunduz yuksek/dusugu kirilimi yonunde, 18:05'e kadar.
# Fiyat duzeyi karsilastirmasi -> yalniz bilgi["ayni_vade"][-1] True iken. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, onceki, bilgi, m15=True, acilis_icinde=False, kontrol=False, stop_oran=None):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    if kontrol:
        ib = np.flatnonzero((dk >= 585) & (dk <= 644))
        if not len(ib):
            return out
        bas = 659
    else:
        if not len(onceki) or not bool(bilgi["ayni_vade"][-1]):
            return out
        PH = float(onceki[-1].high.max()); PL = float(onceki[-1].low.min())
        bas = 599
        if acilis_icinde:
            j0 = np.flatnonzero(dk <= 584)
            if not len(j0) or not (PL <= c[j0[-1]] <= PH):
                return out
    for i in range(n):
        if dk[i] < bas or dk[i] > 1019:
            continue
        if m15 and dk[i] % 15 != 14:
            continue
        if kontrol:
            # ilk saat araligi: yalniz 09:45-10:44 barlari (i'den once tamamlanmis)
            if dk[i] < 659:
                continue
            PH = h[ib].max(); PL = l[ib].min()
        y = 1 if c[i] > PH else (-1 if c[i] < PL else 0)
        if y == 0:
            continue
        out[i] = y
        if stop_oran is not None:
            # kapanis bazli stop: tetik kapanisindan stop_oran x dunku aralik aleyhte kapanis -> ters sinyal (motor ters=True ile cikar)
            sev = c[i] - y * stop_oran * (PH - PL)
            for k in range(i + 1, n):
                if (y > 0 and c[k] <= sev) or (y < 0 and c[k] >= sev):
                    out[k] = -y; break
        return out
    return out
