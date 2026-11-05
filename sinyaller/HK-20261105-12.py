# HK-20261105-12 — M15 cift dip/tepe ve OBO boyun kirilimi, nedensel Gauss duzlestirme + gecikmeli onayli uclar. motor 1.00.
# Yalniz bugunun TAMAMLANMIS M15 kovalari (son M1'i dk%15==14). i. bar icin yalniz s.iloc[:i+1].
# Hedef/stop her M1 kapanisinda denetlenir; cikis = karsi isaretli tek bar (motor 'ters').
import numpy as np


def _kovalar(s):
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    kova = dk // 15
    out = []; bas = 0
    for j in range(len(dk)):
        if j == len(dk) - 1 or kova[j + 1] != kova[j]:
            if dk[j] % 15 == 14:
                out.append((j, h[bas:j + 1].max(), l[bas:j + 1].min(), c[j]))
            bas = j + 1
    return out


def _uclar(Hs, Ls, Cs, t, h, w):
    """t. M15 kovasina kadar (dahil) onaylanmis alternatif uclar: [(tur, fiyat, sira)]; tur +1 tepe, -1 dip."""
    C = np.asarray(Cs[:t + 1], float)
    S = np.empty(len(C))
    for u in range(len(C)):
        d = np.arange(u + 1)[::-1]
        K = np.exp(-0.5 * (d / h) ** 2)
        S[u] = (K * C[:u + 1]).sum() / K.sum()
    uc = []
    for j in range(w, len(C) - w):
        pen = S[j - w:j + w + 1]
        diger = np.delete(pen, w)
        if S[j] > diger.max():
            uc.append((1, float(max(Hs[j - w:j + w + 1])), j))
        elif S[j] < diger.min():
            uc.append((-1, float(min(Ls[j - w:j + w + 1])), j))
    alt = []
    for u in uc:
        if alt and alt[-1][0] == u[0]:
            if (u[0] == 1 and u[1] > alt[-1][1]) or (u[0] == -1 and u[1] < alt[-1][1]):
                alt[-1] = u
        else:
            alt.append(u)
    return alt


def sinyal(s, desen="ikisi", h=2.0, w=2, tol=0.5, H=600):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    if n < 2:
        return out
    kov = _kovalar(s)
    if not kov:
        return out
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    J = [k[0] for k in kov]; Hs = [k[1] for k in kov]; Ls = [k[2] for k in kov]; Cs = [k[3] for k in kov]
    kov_son = {j: t for t, j in enumerate(J)}
    poz = 0; hedef = stop = None; kullanilan = set()
    for i in range(n):
        if poz != 0:
            if int(dk[i]) >= 1065 or (poz == 1 and (c[i] >= hedef or c[i] <= stop)) or (poz == -1 and (c[i] <= hedef or c[i] >= stop)):
                out[i] = -poz; poz = 0
            continue
        if i not in kov_son:
            continue
        t = kov_son[i]
        d_ = int(dk[i])
        if not (704 <= d_ <= 1034) or t < 4:
            continue
        atr = float(np.mean(np.asarray(Hs[:t + 1]) - np.asarray(Ls[:t + 1])))
        if not atr > 0:
            continue
        U = _uclar(Hs, Ls, Cs, t, h, w)
        Cb, Cp = Cs[t], Cs[t - 1]
        y = 0; aday = None
        if desen in ("cift", "ikisi") and len(U) >= 3:
            a, b, e = U[-3], U[-2], U[-1]
            if a[0] == e[0] == -b[0] and abs(a[1] - e[1]) <= tol * atr and e[2] + w <= t:
                boyun = b[1]
                if a[0] == -1 and Cp <= boyun < Cb:
                    uc = min(a[1], e[1]); aday = (1, boyun + (boyun - uc), uc - 0.2 * atr, ("C", b[2]))
                elif a[0] == 1 and Cp >= boyun > Cb:
                    uc = max(a[1], e[1]); aday = (-1, boyun - (uc - boyun), uc + 0.2 * atr, ("C", b[2]))
        if aday is None and desen in ("obo", "ikisi") and len(U) >= 5:
            T1, D2, T3, D4, T5 = U[-5:]
            if T1[0] == T3[0] == T5[0] == -D2[0] == -D4[0] and T5[2] + w <= t:
                sg = T1[0]   # +1: OBO (tepeler), -1: ters OBO (dipler)
                bas_uc = (T3[1] > max(T1[1], T5[1])) if sg == 1 else (T3[1] < min(T1[1], T5[1]))
                if bas_uc and abs(T1[1] - T5[1]) <= tol * atr and abs(D2[1] - D4[1]) <= tol * atr:
                    boyun = (D2[1] + D4[1]) / 2.0
                    if sg == 1 and Cp >= boyun > Cb:
                        aday = (-1, boyun - (T3[1] - boyun), T5[1] + 0.2 * atr, ("O", D4[2]))
                    elif sg == -1 and Cp <= boyun < Cb:
                        aday = (1, boyun + (boyun - T3[1]), T5[1] - 0.2 * atr, ("O", D4[2]))
        if aday is not None and aday[3] not in kullanilan:
            y, hedef, stop, anahtar = aday
            kullanilan.add(anahtar)
            out[i] = y; poz = y
    return out
