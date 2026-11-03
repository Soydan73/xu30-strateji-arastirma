# HK-20261103-08 — İşaretli hacimde Bayesçi çevrimiçi değişim noktası (BOCPD, Adams-MacKay 2007; sabit önsel, eğitimsiz).
# Seri: M1 bar dengesizlik oranı x = (alış−satış)/(alış+satış). Yeni rejim m bar onaylanınca rejim ortalaması işaretinde.
# Kaynak fikir: Tsaknaki-Lillo-Mazzarisi (QF 2024) akış rejimleri. Yalnız s.iloc[:i+1] kullanılır.
import numpy as np
from math import lgamma

MU0, KAPPA0, ALPHA0, BETA0 = 0.0, 1.0, 1.0, 0.16   # önsel: ortalama 0, varyans ölçeği ~0,16 (koşudan önce sabit)
RMAX = 300


def _t_logpdf(x, mu, kappa, alpha, beta):
    nu = 2 * alpha
    s2 = beta * (kappa + 1) / (alpha * kappa)
    z = (x - mu) ** 2 / (nu * s2)
    return (np.vectorize(lgamma)((nu + 1) / 2) - np.vectorize(lgamma)(nu / 2)
            - 0.5 * np.log(nu * np.pi * s2) - (nu + 1) / 2 * np.log1p(z))


def map_kosu(x, lam):
    """Her adımda en olası koşu uzunluğu (r*) dizisi. Yalnız geçmiş veriyle (çevrimiçi)."""
    H = 1.0 / lam
    n = len(x); rstar = np.zeros(n, dtype=int)
    logR = np.array([0.0])
    mu = np.array([MU0]); ka = np.array([KAPPA0]); al = np.array([ALPHA0]); be = np.array([BETA0])
    for t in range(n):
        lp = _t_logpdf(x[t], mu, ka, al, be)
        grow = logR + lp + np.log(1 - H)
        cp = np.logaddexp.reduce(logR + lp + np.log(H))
        logR = np.concatenate([[cp], grow])
        logR -= np.logaddexp.reduce(logR)
        mu_n = (ka * mu + x[t]) / (ka + 1)
        be_n = be + ka * (x[t] - mu) ** 2 / (2 * (ka + 1))
        mu = np.concatenate([[MU0], mu_n]); be = np.concatenate([[BETA0], be_n])
        ka = np.concatenate([[KAPPA0], ka + 1]); al = np.concatenate([[ALPHA0], al + 0.5])
        if len(logR) > RMAX:
            logR = logR[:RMAX]; mu = mu[:RMAX]; be = be[:RMAX]; ka = ka[:RMAX]; al = al[:RMAX]
            logR -= np.logaddexp.reduce(logR)
        rstar[t] = int(np.argmax(logR))
    return rstar


def sinyal(s, lam=60, m=5, tau=0.10, kontrol=False):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    bv = s.buy_volume.to_numpy(float); sv = s.sell_volume.to_numpy(float)
    tot = bv + sv
    x = np.where(tot > 0, (bv - sv) / np.where(tot > 0, tot, 1), 0.0)
    bas = np.flatnonzero(dk >= 570)
    if len(bas) == 0:
        return out
    b = bas[0]
    xs = x[b:]
    if kontrol:
        for k in range(len(xs)):
            i = b + k
            if dk[i] % 15 == 14 and k >= m - 1 and 600 <= dk[i] <= 1064:
                mu = xs[k - m + 1:k + 1].mean()
                if abs(mu) >= tau:
                    out[i] = np.sign(mu)
        return out
    r = map_kosu(xs, lam)
    for k in range(1, len(xs)):
        i = b + k
        if not (600 <= dk[i] <= 1064):
            continue
        # r*[k] = son r* gözlem mevcut rejimde. Yeni rejim tam m bardır sürüyor ve önceki adımda m−1 idi (kesintisiz onay)
        if r[k] == m and r[k - 1] == m - 1 and k - m >= 1:
            mu = xs[k - m + 1:k + 1].mean()
            if abs(mu) >= tau:
                out[i] = np.sign(mu)
    return out
