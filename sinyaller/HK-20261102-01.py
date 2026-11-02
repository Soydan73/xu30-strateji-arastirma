# HK-20261102-01 — Koşu uzunluğu: kısa koşuda devam (M15) / uzun koşuda dönüş (M5)
# Yalnız sinyal fonksiyonu; model eğitimi YOK. Tek seans; i. barda yalnız s.iloc[:i+1] kullanılır.
import numpy as np


def sinyal(s, P=15, L=2, mod="devam"):
    n = len(s); out = np.zeros(n)
    if n == 0:
        return out
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    yon = 1 if mod == "devam" else -1
    isaretler = []          # tamamlanmış blok gövde işaretleri
    blok_ac = None; blok_id = None
    for i in range(n):
        if dk[i] < 570:
            continue
        b = (dk[i] - 570) // P
        if b != blok_id:
            blok_id = b; blok_ac = o[i]
        if dk[i] == 570 + P * (b + 1) - 1:      # blok bu barla tamamlandı
            isaretler.append(np.sign(c[i] - blok_ac))
            son = isaretler[-1]
            if son == 0:
                continue
            k = 0
            for x in reversed(isaretler):
                if x == son:
                    k += 1
                else:
                    break
            if k == L and 600 <= dk[i] + 1 <= 1050:
                out[i] = yon * son
    return out
