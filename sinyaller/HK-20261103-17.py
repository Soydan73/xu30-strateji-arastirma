# HK-20261103-17 — Onceki gun ozellik vektoru cekirdek analogu (egitimsiz). Kitaplik YALNIZ onceki seanslardan.
# Ozellikler seans ici buyukluklerden (fiyat duzeyi yok -> vade gecisi GAP'indan etkilenmez). Sinyal yalniz 09:44 barinda.
import numpy as np


def _gun(p):
    o = float(p.open.iloc[0]); c = float(p.close.iloc[-1])
    h = float(p.high.max()); l = float(p.low.min())
    return dict(r=c / o - 1.0, clv=(c - l) / (h - l) if h > l else 0.5, v=float(p.volume.sum()), a=(h - l) / o)


def _ozellik(gecmis, secim):
    # gecmis: en az 6 seans (eskiden yeniye); son eleman = "dun"
    g = [_gun(p) for p in gecmis[-6:]]
    dun = g[-1]; once5 = g[:-1]
    vm = np.mean([x["v"] for x in once5]); am = np.mean([x["a"] for x in once5])
    f = [dun["r"], sum(x["r"] for x in g[-5:]), dun["clv"],
         dun["v"] / vm if vm > 0 else 1.0, dun["a"] / am if am > 0 else 1.0]
    return np.array([f[k] for k in secim], float)


def _sonuc(p):
    dk = p.dk.to_numpy(); c = p.close.to_numpy(float); o = p.open.to_numpy(float)
    a = np.flatnonzero(dk >= 585); b = np.flatnonzero(dk <= 1084)
    if not len(a) or not len(b):
        return np.nan
    return c[b[-1]] / o[a[0]] - 1.0


def sinyal(s, onceki, bilgi, secim=(0, 1, 2, 3, 4), K=None, b=1.0, kontrol=False, min_kitap=30):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy()
    j = np.flatnonzero(dk == 584)  # yalniz 09:44 bari; kesik seansta yoksa sinyal yok
    if not len(j) or len(onceki) < 7:
        return out
    j = j[-1]
    X, Y = [], []
    for q in range(6, len(onceki)):
        y = _sonuc(onceki[q])
        if not np.isfinite(y):
            continue
        X.append(_ozellik(onceki[q - 6:q], secim)); Y.append(y)
    if len(Y) < min_kitap:
        return out
    X = np.array(X); Y = np.array(Y)
    if kontrol:
        m = Y.mean()
    else:
        x0 = _ozellik(onceki, secim)
        mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd == 0] = 1.0
        Z = (X - mu) / sd; z0 = (x0 - mu) / sd
        d = np.sqrt(((Z - z0) ** 2).sum(axis=1))
        if K is not None:
            idx = np.argsort(d, kind="stable")[:K]
            m = Y[idx].mean()
        else:
            med = np.median(d)
            w = np.exp(-d / (b * med)) if med > 0 else np.ones(len(d))
            m = (w * Y).sum() / w.sum()
    if np.isfinite(m) and m != 0:
        out[j] = np.sign(m)
    return out
