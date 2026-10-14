# HK-20261014-16 — M15 başarısız yükseliş/düşüş + iç bar sonrası braket kırılımı (yalnız sinyal)
import numpy as np

def sinyal(s, ic=False, mod="braket"):
    n = len(s); out = np.zeros(n); dk = s.dk.to_numpy()
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    blok = np.where(dk >= 570, (dk - 570) // 15, -1)
    onceki = None          # (H, L) tamamlanmış önceki blok
    kur = None             # (H_k, L_k, izinli_yonler, bitis_dk)
    for i in range(n):
        if kur is not None:
            if dk[i] > kur[3]:
                kur = None
            else:
                y = 1 if c[i] > kur[0] else (-1 if c[i] < kur[1] else 0)
                if y != 0:
                    if y in kur[2]:
                        out[i] = y
                    kur = None
        k = blok[i]
        if k >= 0 and dk[i] == 570 + 15 * k + 14:
            sel = (blok[:i + 1] == k)
            Hk, Lk, Ck = h[:i + 1][sel].max(), l[:i + 1][sel].min(), c[i]
            if onceki is not None and onceki[2] == k - 1 and 599 <= dk[i] <= 1049:
                Hp, Lp = onceki[0], onceki[1]
                up = Hk > Hp and Ck <= Hp; dn = Lk < Lp and Ck >= Lp
                ib = Hk <= Hp and Lk >= Lp
                izin = None
                if mod == "braket":
                    if up or dn or (ic and ib):
                        izin = (1, -1)
                else:
                    if up and not dn:
                        izin = (-1,)
                    elif dn and not up:
                        izin = (1,)
                if izin is not None:
                    kur = (Hk, Lk, izin, dk[i] + 15)
            onceki = (Hk, Lk, k)
    return out
