# HK-20261019-01 — seans içi TTM sıkışması (BB Keltner içinde) çözülünce kırılım / momentum yönünde (yalnız sinyal)
# Yalnız tamamlanmış M5 kovaları (09:30 hizalı) ve karar barına kadarki veri kullanılır.
import numpy as np


def _linreg_son(y):
    x = np.arange(len(y), dtype=float)
    b, a = np.polyfit(x, y, 1)
    return a + b * x[-1]


def sinyal(s, mod="kirilim", L=5, kc=1.5, n=20, bekle=3, ilk=670, son=1019):
    N = len(s); out = np.zeros(N)
    if N == 0:
        return out
    dk = s.dk.to_numpy().astype(int)
    o = s.open.to_numpy(float); h = s.high.to_numpy(float)
    l = s.low.to_numpy(float); c = s.close.to_numpy(float)

    K_H, K_L, K_C = [], [], []      # tamamlanmış kovalar
    cur = None                       # [kova_no, H, L]
    kosu = 0; RH = RL = None         # açık sıkışma koşusu
    bekleyen = None                  # (RH, RL, kalan) çözülmeden sonra kırılım beklemesi
    for i in range(N):
        if dk[i] < 570:
            continue
        k = (dk[i] - 570) // 5
        if cur is None or cur[0] != k:
            cur = [k, h[i], l[i]]
        else:
            cur[1] = max(cur[1], h[i]); cur[2] = min(cur[2], l[i])
        if (dk[i] - 570) % 5 != 4:
            continue
        K_H.append(cur[1]); K_L.append(cur[2]); K_C.append(c[i])
        m = len(K_C)
        karar_ok = ilk <= dk[i] <= son

        if L == 0:   # KONTROL: sıkışma şartı yok, son 5 kova (k hariç) aralığı kırılımı
            if m >= 6 and karar_ok:
                rh = max(K_H[-6:-1]); rl = min(K_L[-6:-1])
                if K_C[-1] > rh:
                    out[i] = 1.0
                elif K_C[-1] < rl:
                    out[i] = -1.0
            continue

        if m < n:
            continue
        C = np.array(K_C[-n:]); H = np.array(K_H[-n:]); Lw = np.array(K_L[-n:])
        onc = np.array(K_C[-n - 1:-1]) if m > n else None
        if onc is not None:
            tr = np.maximum(H, onc) - np.minimum(Lw, onc)
        else:
            tr = H - Lw
            tr[1:] = np.maximum(H[1:], C[:-1]) - np.minimum(Lw[1:], C[:-1])
        atr = tr.mean(); sd = C.std(); mid = C.mean()
        sikisma = 2.0 * sd < kc * atr

        if sikisma:
            bekleyen = None
            if kosu == 0:
                RH, RL = K_H[-1], K_L[-1]
            else:
                RH = max(RH, K_H[-1]); RL = min(RL, K_L[-1])
            kosu += 1
            continue

        # sıkışma değil
        if kosu >= L:     # bu kova çözülme kovası
            if mod == "momentum":
                if karar_ok:
                    x = C - ((H.max() + Lw.min()) / 2.0 + mid) / 2.0
                    v = _linreg_son(x)
                    out[i] = 1.0 if v > 0 else (-1.0 if v < 0 else 0.0)
            else:
                bekleyen = [RH, RL, bekle]
        kosu = 0; RH = RL = None

        if bekleyen is not None and mod == "kirilim":
            if karar_ok:
                if K_C[-1] > bekleyen[0]:
                    out[i] = 1.0; bekleyen = None; continue
                if K_C[-1] < bekleyen[1]:
                    out[i] = -1.0; bekleyen = None; continue
            bekleyen[2] -= 1
            if bekleyen[2] <= 0:
                bekleyen = None
    return out
