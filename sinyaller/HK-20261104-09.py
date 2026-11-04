# HK-20261104-09 — 5 oylu seans rejimi (VWAP tarafi, 75 dk VWAP egimi, acilis araligi, H1 SMA20, dunku uc).
# >= E oy ayni yonde ve D ardisik M1 bari surerse o yonde (10:45-16:30, seans basina ilk tetik).
# Fiyat duzeyi (H1 SMA20, dunku uc) yalniz bilgi["ayni_vade"] True olan onceki seanslardan. i. bar icin yalniz s.iloc[:i+1].
import numpy as np


def _saat_kapanislari(x):
    dk = x.dk.to_numpy(); c = x.close.to_numpy(float)
    kova = dk // 60
    son = np.r_[kova[1:] != kova[:-1], True]
    return list(c[son])


def sinyal(s, onceki, bilgi, E=4, D=25, kontrol=False, etiket=0):
    # etiket: yalniz varyant kimligi (cikis H farki icin), sinyale etkisi yok
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); v = s.volume.to_numpy(float)
    tp = (h + l + c) / 3.0
    cv = np.cumsum(v); vw = np.where(cv > 0, np.cumsum(tp * v) / np.where(cv > 0, cv, 1.0), c)
    orb = np.flatnonzero((dk >= 570) & (dk <= 599))
    if not len(orb):
        return out
    ORH = h[orb].max(); ORL = l[orb].min()
    if not kontrol:
        if not len(onceki):
            return out
        av = np.asarray(bilgi["ayni_vade"], dtype=bool)
        if not av[-1]:
            return out
        PH = float(onceki[-1].high.max()); PL = float(onceki[-1].low.min())
        gecmis = []
        for x, a in zip(onceki, av):
            if a:
                gecmis += _saat_kapanislari(x)
        bugun_tam = []   # (indeks, kapanis) tamamlanmis saat kovalari
    seri = 0; yon = 0
    for i in range(n):
        if not kontrol and dk[i] % 60 == 59:
            bugun_tam.append(c[i])
        if dk[i] < 600:
            continue
        o1 = 1 if c[i] > vw[i] else (-1 if c[i] < vw[i] else 0)
        o2 = int(np.sign(vw[i] - vw[i - 75])) if i >= 75 else 0
        o3 = 1 if c[i] > ORH else (-1 if c[i] < ORL else 0)
        oylar = [o1, o2, o3]
        if not kontrol:
            hc = gecmis + bugun_tam
            if len(hc) < 20:
                seri = 0; yon = 0
                continue
            sma = float(np.mean(hc[-20:]))
            o4 = 1 if c[i] > sma else (-1 if c[i] < sma else 0)
            o5 = 1 if c[i] > PH else (-1 if c[i] < PL else 0)
            oylar += [o4, o5]
        art = sum(1 for o in oylar if o > 0); eks = sum(1 for o in oylar if o < 0)
        y = 1 if art >= E else (-1 if eks >= E else 0)
        if y != 0 and y == yon:
            seri += 1
        else:
            seri = 1 if y != 0 else 0; yon = y
        if y != 0 and seri >= D and 645 <= dk[i] <= 990:
            out[i] = y
            return out
    return out
