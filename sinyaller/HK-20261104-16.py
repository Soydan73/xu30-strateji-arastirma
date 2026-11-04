# HK-20261104-16 — Vade son 2 seansi 14:00: en yakin G kati K'ya cekilme (ya da itilme). Takvim sabit liste (fiyat verisi degil).
import numpy as np, datetime as _dt

_SON2 = ['2023-10-30', '2023-10-31', '2023-12-28', '2023-12-29', '2024-02-28', '2024-02-29', '2024-04-29', '2024-04-30',
         '2024-06-27', '2024-06-28', '2024-08-28', '2024-08-29', '2024-10-30', '2024-10-31', '2024-12-30', '2024-12-31',
         '2025-02-27', '2025-02-28', '2025-04-29', '2025-04-30', '2025-06-27', '2025-06-30', '2025-08-28', '2025-08-29',
         '2025-10-30', '2025-10-31', '2026-06-29', '2026-06-30', '2026-08-28', '2026-08-31']
SON2 = {_dt.date.fromisoformat(x) for x in _SON2}
SON1 = {_dt.date.fromisoformat(x) for x in _SON2[1::2]}


def sinyal(s, G=250, yon="cekme", gunler="son2", H=209, hedef=None):
    n = len(s); out = np.zeros(n)
    if n < 1:
        return out
    g = s.time.iloc[0].date()
    if gunler == "son2" and g not in SON2:
        return out
    if gunler == "son1" and g not in SON1:
        return out
    if gunler == "diger" and g in SON2:
        return out
    dk = s.dk.to_numpy()
    idx = np.flatnonzero(dk >= 840)
    if not len(idx):
        return out
    i = int(idx[0])
    P = float(s.close.iloc[i])
    K = round(P / G) * G
    d = K - P
    if abs(d) <= 0.3 * G:
        return out
    out[i] = np.sign(d) if yon == "cekme" else -np.sign(d)
    return out
