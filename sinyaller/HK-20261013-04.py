# HK-20261013-04 — gerçek delta işaret dizisinin koşullu entropisi (düşük = düzenli akış) → akış yönünde (yalnız sinyal)
import numpy as np

def kosullu_entropi(z):
    """z: -1/0/+1 dizisi. H(X_t | X_{t-1}) bit cinsinden, 3 durum."""
    a = z[:-1] + 1; b = z[1:] + 1
    m = np.zeros((3, 3))
    np.add.at(m, (a.astype(int), b.astype(int)), 1)
    n = m.sum()
    if n == 0:
        return np.nan
    p_ab = m / n; p_a = m.sum(1) / n
    H = 0.0
    for x in range(3):
        for y in range(3):
            if m[x, y] > 0:
                H -= p_ab[x, y] * np.log2(p_ab[x, y] / p_a[x])
    return H

def ozellik(s, i, W):
    dk = s.dk.to_numpy(); T = dk[i] + 1
    pen = (dk > T - 1 - W) & (dk <= dk[i]) & (np.arange(len(s)) <= i)
    if pen.sum() < 0.8 * W or (dk[pen] < 585).any():
        return np.nan, 0.0
    d = (s.buy_volume.to_numpy(float) - s.sell_volume.to_numpy(float))[pen]
    return kosullu_entropi(np.sign(d)), d.sum()

def sinyal(s, h=0.9, W=30):
    dk = s.dk.to_numpy(); out = np.zeros(len(s))
    for T in range(630, 1006, 15):               # 10:30 … 16:45 giriş dakikası (tamamlanmış M15 sınırı)
        ii = np.flatnonzero(dk == T - 1)
        if not len(ii):
            continue
        i = ii[0]
        H, cd = ozellik(s.iloc[: i + 1], i, W)
        if np.isnan(H) or cd == 0:
            continue
        if H <= h:
            out[i] = np.sign(cd); break
    return out
