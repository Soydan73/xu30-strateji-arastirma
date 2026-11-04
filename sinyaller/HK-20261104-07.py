# HK-20261104-07 — Dunku ucun sahte kirilimi: karar bari kapanisi dunku araligin disina cikip SONRAKI bir karar barinda
# yeniden iceri kapanirsa ters yon (asagi kirilim + geri alis -> uzun; yukari kirilim + geri veris -> kisa). 18:05 / H.
# Fiyat duzeyi karsilastirmasi -> yalniz bilgi["ayni_vade"][-1] True iken. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def sinyal(s, onceki, bilgi, adim=15, acilis_icinde=False, kontrol=False, gezinti_stop=False, etiket=0):
    # etiket: yalniz varyant kimligi (cikis H farki icin), sinyale etkisi yok
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    h = s.high.to_numpy(float); l = s.low.to_numpy(float)
    if kontrol:
        ib = np.flatnonzero((dk >= 585) & (dk <= 644))
        if not len(ib):
            return out
        kayit_bas, sin_bas = 659, 660
    else:
        if not len(onceki) or not bool(bilgi["ayni_vade"][-1]):
            return out
        PH = float(onceki[-1].high.max()); PL = float(onceki[-1].low.min())
        kayit_bas, sin_bas = 599, 614
        if acilis_icinde:
            j0 = np.flatnonzero(dk <= 584)
            if not len(j0) or not (PL <= c[j0[-1]] <= PH):
                return out
    asagi = None; yukari = None          # ilk kirilim karar barinin indeksi
    for i in range(n):
        if dk[i] < kayit_bas or dk[i] > 1019 or dk[i] % adim != adim - 1:
            continue
        if kontrol:
            PH = h[ib].max(); PL = l[ib].min()     # ib barlari dk <= 644 < kayit_bas: hepsi tamamlanmis
        y = 0
        if dk[i] >= sin_bas:
            if asagi is not None and c[i] > PL:
                y, k0 = 1, asagi
            elif yukari is not None and c[i] < PH:
                y, k0 = -1, yukari
        if y != 0:
            out[i] = y
            if gezinti_stop:
                uc = l[k0:i + 1].min() if y > 0 else h[k0:i + 1].max()
                for k in range(i + 1, n):
                    if (y > 0 and c[k] < uc) or (y < 0 and c[k] > uc):
                        out[k] = -y; break
            return out
        if asagi is None and c[i] < PL:
            asagi = i
        if yukari is None and c[i] > PH:
            yukari = i
    return out
