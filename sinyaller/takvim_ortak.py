# Ortak takvim yardımcıları (HK-20261102-05/06). Yalnız tarih kuralları; fiyat verisi kullanılmaz.
import datetime as _dt


def abd_yaz_saati(g):
    """ABD yaz saati: Mart 2. Pazar – Kasım 1. Pazar (tarih bazında)."""
    y = g.year
    m1 = _dt.date(y, 3, 1); bas = m1 + _dt.timedelta(days=(6 - m1.weekday()) % 7 + 7)
    k1 = _dt.date(y, 11, 1); son = k1 + _dt.timedelta(days=(6 - k1.weekday()) % 7)
    return bas <= g < son


def nfp_gunu(g):
    """BLS kuralı: 12'sini içeren (Pazar–Cumartesi) referans haftasının bitişinden sonraki 3. Cuma.
    Önceki ayın referans haftasına göre bu ay yayımlanan tarih hesaplanır. Tatil/kapanma kaymaları modellenmez."""
    y, m = (g.year, g.month - 1) if g.month > 1 else (g.year - 1, 12)
    on2 = _dt.date(y, m, 12)
    cmt = on2 + _dt.timedelta(days=(5 - on2.weekday()) % 7)      # referans haftasının Cumartesisi
    yayin = cmt + _dt.timedelta(days=6 + 14)                     # ilk Cuma + 2 hafta = 3. Cuma
    return g == yayin


# Kural tarihleri + bilinen sapmalar (BLS tatil kaydırmaları, 2025 kapanması): kesin liste bundan türetilir.
_SAPMA_CIKAR = {_dt.date(2025, 1, 3), _dt.date(2025, 7, 4), _dt.date(2025, 10, 3), _dt.date(2026, 1, 2), _dt.date(2026, 7, 3)}
_SAPMA_EKLE = {_dt.date(2025, 1, 10), _dt.date(2025, 7, 3), _dt.date(2026, 1, 9), _dt.date(2026, 7, 2)}


def _nfp_liste(bas=_dt.date(2023, 8, 1), son=_dt.date(2026, 10, 1)):
    g, out = bas, set()
    while g < son:
        if nfp_gunu(g):
            out.add(g)
        g += _dt.timedelta(days=1)
    return (out - _SAPMA_CIKAR) | _SAPMA_EKLE


NFP = _nfp_liste()


# FOMC açıklama günleri (Fed'in önceden ilan ettiği takvim; keşif aralığı 2023-09 → 2026-09)
FOMC = {_dt.date(*t) for t in [
    (2023, 9, 20), (2023, 11, 1), (2023, 12, 13),
    (2024, 1, 31), (2024, 3, 20), (2024, 5, 1), (2024, 6, 12), (2024, 7, 31), (2024, 9, 18), (2024, 11, 7), (2024, 12, 18),
    (2025, 1, 29), (2025, 3, 19), (2025, 5, 7), (2025, 6, 18), (2025, 7, 30), (2025, 9, 17), (2025, 10, 29), (2025, 12, 10),
    (2026, 1, 28), (2026, 3, 18), (2026, 4, 29), (2026, 6, 17), (2026, 7, 29), (2026, 9, 16)]}
