# HK-20261015-04 — ay dönümü (TOTM) gün içi uzun, kontrol varyantlı (yalnız sinyal)
# Takvim resmî borsa iş günü takviminden hesaplanır (fiyat verisi kullanılmaz; önceden bilinen bilgi).
import numpy as np
import pandas as pd

TATIL = {pd.Timestamp(x) for x in [
    "2023-10-29",
    "2024-01-01", "2024-04-10", "2024-04-11", "2024-04-12", "2024-04-23", "2024-05-01",
    "2024-06-17", "2024-06-18", "2024-06-19", "2024-07-15", "2024-08-30", "2024-10-29",
    "2025-01-01", "2025-03-31", "2025-04-01", "2025-04-23", "2025-05-01", "2025-05-19",
    "2025-06-06", "2025-06-09", "2025-07-15", "2025-10-29",
    "2026-01-01", "2026-03-20", "2026-04-23", "2026-05-01", "2026-05-19",
    "2026-05-27", "2026-05-28", "2026-05-29", "2026-07-15",
]}


def is_gunu(d):
    return d.weekday() < 5 and d not in TATIL


def takvim(d):
    """(ayın kaçıncı iş günü, ayın son iş günü mü)"""
    d = pd.Timestamp(d).normalize()
    ilk = d.replace(day=1)
    pos = sum(1 for x in pd.date_range(ilk, d) if is_gunu(x))
    sonraki = d + pd.Timedelta(days=1)
    while not is_gunu(sonraki):
        sonraki += pd.Timedelta(days=1)
    return pos, sonraki.month != d.month


def pencerede(pos, son, pencere):
    totm4 = son or pos <= 3
    return {"TOTM4": totm4, "TOTM2": son or pos == 1, "SON": son, "ILK": pos == 1,
            "HER_GUN": True, "TOTM_DISI": not totm4}[pencere]


def sinyal(s, pencere="TOTM4", g=585):
    n = len(s); out = np.zeros(n)
    if n == 0:
        return out
    pos, son = takvim(s.time.iloc[0])
    if not pencerede(pos, son, pencere):
        return out
    dk = s.dk.to_numpy()
    for i in range(n):
        if dk[i] >= g - 1:
            out[i] = 1.0          # ilk kez g−1 veya sonrası: motor sonraki barın açılışında girer
            break
    return out
