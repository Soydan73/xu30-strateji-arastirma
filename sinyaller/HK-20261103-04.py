# HK-20261103-04 — Sabah 09:49–11:44 tamamlanmış M5 barı R ≥ k·R̄ ve |gövde| ≥ 0,6R → gövde yönünde. Eğitim YOK.
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5_ortak import m5_tamam


def sinyal(s, k=2.0, govde=0.6, dk_bas=589, dk_son=704):
    n = len(s); out = np.zeros(n)
    O, H, L, C, J = m5_tamam(s, n - 1)
    dk = s.dk.to_numpy()
    gec = [t for t in range(len(C)) if dk[J[t]] - 4 >= 570]     # kova başı >= 09:30
    for q, t in enumerate(gec):
        j = J[t]
        if not (dk_bas <= dk[j] <= dk_son) or q < 3:
            continue
        R = H[t] - L[t]
        if R <= 0:
            continue
        Rbar = np.mean([H[u] - L[u] for u in gec[:q]])
        g = C[t] - O[t]
        if R >= k * Rbar and abs(g) >= govde * R:
            out[j] = np.sign(g)
    return out
