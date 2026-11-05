# HK-20261105-09 — Gurultu bolgesi (noise area) momentumu, Zarattini-Aziz-Barbon "Beat the Market" uyarlamasi.
# motor_cok 1.00. sigma(tau) = onceki N seansta ayni saat-dakikasinda |C_tau / O_gun - 1| ortalamasi (getiri orani, vade-bagimsiz).
# Fiyat duzeyi (dunku kapanis, RSI) yalniz ayni vadeden. i. bar icin yalniz s.iloc[:i+1].
# Kontrol barlari: kapanisi HH:00 / HH:30 olan barlar (dk % 30 == 29), 10:00 -> 17:30.
# Sanal pozisyon: sinyal, motorun pozisyonunu taklit eder; cikis = karsi isaretli tek bar (motor 'ters' ile kapatir).
import numpy as np


def _acilis(x):
    o = x.open.to_numpy(float)
    return float(o[1]) if len(o) > 1 else np.nan      # ilk bar acilis muzayedesi; surekli islem 2. bardan


def sinyal(s, onceki, bilgi, N=14, m=1.0, mod="iz", suzgec="yok", rsi_q=40.0, sabit=None, H=600):  # H yalniz cikis
    n = len(s); out = np.zeros(n)
    if n < 1 or len(onceki) < N or len(bilgi["ayni_vade"]) == 0 or not bool(bilgi["ayni_vade"][-1]):
        return out
    gec = onceki[-N:]
    dun = onceki[-1]
    C_dun = float(dun.close.iloc[-1])
    # --- gunluk suzgec (yalniz onceki seanslar) ---
    if suzgec == "nr4":
        if len(onceki) < 4:
            return out
        r = [float((x.high.max() - x.low.min()) / x.close.iloc[-1]) for x in onceki[-4:]]
        if not r[-1] <= min(r):
            return out
    elif suzgec == "rsi":
        av = bilgi["ayni_vade"]
        if len(onceki) < 6 or not bool(np.all(av[-6:])):
            return out
        c = np.array([float(x.close.iloc[-1]) for x in onceki[-6:]])
        d = np.diff(c); up = d[d > 0].sum() / 5.0; dn = -d[d < 0].sum() / 5.0
        rsi = 100.0 if dn == 0 else 100.0 - 100.0 / (1.0 + up / dn)
        if not rsi <= rsi_q:
            return out
    # --- sigma(tau) tablosu (onceki seanslardan) ---
    if sabit is None:
        tab = {}
        for x in gec:
            O_x = _acilis(x)
            if not O_x > 0:
                continue
            for d_, c_ in zip(x.dk.to_numpy(), x.close.to_numpy(float)):
                if int(d_) % 30 == 29:
                    tab.setdefault(int(d_), []).append(abs(c_ / O_x - 1.0))
    if n < 2:
        return out
    O = float(s.open.iloc[1])
    dk = s.dk.to_numpy(); c = s.close.to_numpy(float)
    tp = (s.high.to_numpy(float) + s.low.to_numpy(float) + c) / 3.0
    v = s.volume.to_numpy(float)
    cv = np.cumsum(tp * v); cvol = np.cumsum(v)
    poz = 0
    for i in range(1, n):
        d_ = int(dk[i])
        if d_ % 30 != 29 or d_ < 599 or d_ > 1049:
            continue
        if sabit is None:
            l = tab.get(d_, [])
            if len(l) < max(10, N - 4):
                continue
            sg = m * float(np.mean(l))
            U = max(O, C_dun) * (1 + sg); L = min(O, C_dun) * (1 - sg)
        else:
            U = O * (1 + sabit); L = O * (1 - sabit)
        vw = cv[i] / cvol[i] if cvol[i] > 0 else c[i]
        if poz == 0:
            if c[i] > U:
                out[i] = 1.0; poz = 1
            elif c[i] < L:
                out[i] = -1.0; poz = -1
        elif poz == 1:
            cik = (c[i] < L) if mod == "ters" else (c[i] < max(U, vw))
            if cik:
                out[i] = -1.0; poz = 0
        else:
            cik = (c[i] > U) if mod == "ters" else (c[i] > min(L, vw))
            if cik:
                out[i] = 1.0; poz = 0
    return out
