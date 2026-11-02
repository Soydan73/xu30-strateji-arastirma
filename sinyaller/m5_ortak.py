# Ortak: M1 seansından yalnız TAMAMLANMIŞ M5 barlarını kurar (i. bara kadar). Eğitim YOK.
import numpy as np


def m5_tamam(s, i):
    """0…i M1 barlarından tamamlanmış M5 barları (kova dk//5; son dakikası dk%5==4 olan bar gelmişse tamam).
    Döner: (o, h, l, c, son_m1_indeksi) dizileri."""
    dk = s.dk.to_numpy()[:i + 1]
    o = s.open.to_numpy(float)[:i + 1]; h = s.high.to_numpy(float)[:i + 1]
    l = s.low.to_numpy(float)[:i + 1]; c = s.close.to_numpy(float)[:i + 1]
    kova = dk // 5
    O, H, L, C, J = [], [], [], [], []
    bas = 0
    for j in range(len(dk)):
        if j == len(dk) - 1 or kova[j + 1] != kova[j]:
            if dk[j] % 5 == 4:
                O.append(o[bas]); H.append(h[bas:j + 1].max()); L.append(l[bas:j + 1].min()); C.append(c[j]); J.append(j)
            bas = j + 1
    return (np.array(O), np.array(H), np.array(L), np.array(C), np.array(J, dtype=int))
