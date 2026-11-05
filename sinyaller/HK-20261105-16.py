# HK-20261105-16 — M15 Wide Range 2-bar (seans ici) -> devam. motor 1.00. Yalniz tamamlanmis M15 kovalari.
import numpy as np


def sinyal(s, L=12, kontrol=False, H=60):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    o, h, l, c = (s[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    kova = dk // 15
    bas = 570 // 15
    # tamamlanmis kovalar, i. barin kapanisinda yalniz s[:i+1] kullanilir
    K = {}  # kova -> (O,H,L,C), yalniz kapanmis olanlar
    say = {}
    ilk = {}
    for i in range(n):
        b = int(kova[i])
        if b < bas:
            continue
        say[b] = say.get(b, 0) + 1
        if b not in ilk:
            ilk[b] = i
        if dk[i] % 15 != 14:
            continue
        if say[b] >= 8:
            a = ilk[b]
            K[b] = (o[a], h[a:i + 1].max(), l[a:i + 1].min(), c[i])
        if not (764 <= dk[i] <= 1004) or b not in K:
            continue
        if kontrol:
            out[i] = 1 if K[b][3] > K[b][0] else (-1 if K[b][3] < K[b][0] else 0)
            continue
        if (b - 1) not in K:
            continue
        def R2(k):
            return max(K[k - 1][1], K[k][1]) - min(K[k - 1][2], K[k][2])
        r = R2(b)
        if L == "tumu":
            onc = [k for k in range(bas + 1, b) if k in K and (k - 1) in K]
            if len(onc) < 6:
                continue
        else:
            onc = list(range(b - L, b))
            if not all(k in K and (k - 1) in K for k in onc):
                continue
        if r > max(R2(k) for k in onc):
            y = c[i] - K[b - 1][0]
            out[i] = 1 if y > 0 else (-1 if y < 0 else 0)
    return out
