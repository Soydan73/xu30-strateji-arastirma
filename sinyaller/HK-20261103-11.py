# HK-20261103-11 — Standartlaştırılmış sabah VR(q) >= theta ise sabah yönünde öğleden sonra tut (motor_cok).
# Kaynak: EJF 2024 bellek-güçlendirilmiş momentum + proje VR teşhisi (tanım C). Eğitim YOK.
# i. bar için yalnız s.iloc[:i+1]; oynaklık profili yalnız onceki seanslardan (getiri tabanlı, vade geçişinden bağımsız).
import numpy as np

BAS = 585  # 09:45


def _profil(onceki):
    """Önceki seanslarda dakika başına ortalama |log getiri| (dk -> sigma), ±2 dk komşu yumuşatma."""
    top = np.zeros(1440); say = np.zeros(1440)
    for o in onceki:
        dk = o.dk.to_numpy(); c = o.close.to_numpy(float)
        r = np.abs(np.diff(np.log(c)))
        d = dk[1:]
        m = d >= BAS
        np.add.at(top, d[m], r[m]); np.add.at(say, d[m], 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        ham = top / say
    sig = np.full(1440, np.nan)
    for k in range(BAS, 1440):
        w = ham[max(BAS, k - 2):k + 3]
        w = w[np.isfinite(w) & (w > 0)]
        if len(w):
            sig[k] = w.mean()
    return sig


def vr(z, q):
    z = np.asarray(z, float)
    n = len(z)
    if n < 2 * q:
        return np.nan
    z = z - z.mean()
    v1 = (z ** 2).mean()
    if v1 <= 0:
        return np.nan
    cs = np.concatenate([[0.0], np.cumsum(z)])
    sq = cs[q:] - cs[:-q]
    return (sq ** 2).mean() / (q * v1)


def sinyal(s, onceki, bilgi, T=780, q=60, theta=1.0, tanim="C", kontrol=False, en_az=20, H=None):
    # H: yalnız çıkış parametresi (motor cikis_fn okur), sinyali etkilemez
    n = len(s); out = np.zeros(n)
    if len(onceki) < en_az:
        return out
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float); c = s.close.to_numpy(float)
    ib = np.flatnonzero(dk == BAS); it = np.flatnonzero(dk == T - 1)   # T barı: T−1 dakikasında kapanan bar
    if not len(ib) or not len(it):
        return out
    ib, it = ib[0], it[0]
    y = np.sign(c[it] - o[ib])
    if y == 0:
        return out
    if kontrol:
        out[it] = y; return out
    r = np.diff(np.log(c[ib - 1:it + 1])) if ib >= 1 else np.diff(np.log(c[ib:it + 1]))
    d = dk[ib:it + 1] if ib >= 1 else dk[ib + 1:it + 1]
    if tanim == "C":
        sig = _profil(onceki)[d]
        if not np.all(np.isfinite(sig)) or np.any(sig <= 0):
            return out
        z = r / sig
    else:
        z = r
    v = vr(z, q)
    if np.isfinite(v) and v >= theta:
        out[it] = y
    return out
