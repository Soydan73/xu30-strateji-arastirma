# HK-20261020-02 — beklenen/beklenmeyen M15 akış dengesizliği işaret uyumu → akış yönünde devam (yalnız sinyal fonksiyonu)
import numpy as np


def sinyal(s, mod="uyum", L=4, e=0.0, u=0.0, en=0.0, H=60):
    """Her M15 kovası, son M1 barı (dk % 15 == 14) kapanınca tamamlanır; sinyal o barda üretilir.
    Yalnız tamamlanmış kovalar (o bar dahil geçmiş) kullanılır."""
    n = len(s)
    out = np.zeros(n)
    dk = s.dk.to_numpy()
    bv = s.buy_volume.to_numpy(float)
    sv = s.sell_volume.to_numpy(float)
    nk = {}
    for i in range(n):
        if dk[i] < 570 or dk[i] % 15 != 14:
            continue
        k = dk[i] // 15
        m = (dk[: i + 1] >= 570) & (dk[: i + 1] // 15 == k)
        tot = bv[: i + 1][m].sum() + sv[: i + 1][m].sum()
        if m.sum() < 12 or tot <= 0:
            continue
        nk[k] = (bv[: i + 1][m].sum() - sv[: i + 1][m].sum()) / tot
        if not (644 <= dk[i] <= 1004):
            continue
        prev = [nk.get(k - j) for j in range(1, L + 1)]
        if any(p is None for p in prev):
            continue
        E = float(np.mean(prev)); U = nk[k] - E
        if mod == "uyum":
            if np.sign(E) != 0 and np.sign(E) == np.sign(U) and abs(E) >= e and abs(U) >= u:
                out[i] = np.sign(E)
        elif mod == "uyumsuz":
            if np.sign(E) != 0 and np.sign(E) == -np.sign(U) and abs(E) >= e and abs(U) >= u:
                out[i] = np.sign(E)
        elif mod == "kosulsuz":
            if abs(nk[k]) >= en and nk[k] != 0:
                out[i] = np.sign(nk[k])
    return out
