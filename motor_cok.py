# -*- coding: utf-8 -*-
"""
XU30 araştırma ajanı — çok seanslı test motoru v1.00 (03.11.2026, Soydan kararı: seçenek 3)

`motor.py` DEĞİŞMEDEN kalır; bu dosya onu İÇE AKTARIR. Maliyet, işlem simülasyonu (giriş/çıkış, 18:05),
seans-kümeli istatistik ve K1–K7 kapıları tek yerde, `motor.py`'dedir. Burada yalnız şunlar eklenir:
  (1) sinyal fonksiyonuna o günden ÖNCEKİ seansları veren bağlam (onceki, bilgi),
  (2) XU30'a özgü sabit kurallar (vade, veri boşluğu, akşam seansı tanımı),
  (3) genişletilmiş kanarya (gün içi kesim + bağlam bütünlüğü + statik kaynak denetimi).
Bu dosyayı ajan DEĞİŞTİRMEZ (motor.py ile aynı statü). Ayrıntı: MOTOR_COK.md.

Sinyal fonksiyonu sözleşmesi
----------------------------
    def sinyal(s, onceki, bilgi, **p) -> np.ndarray    # uzunluk len(s), değerler -1/0/+1
s       : bugünün gündüz M1 barları (motor.py ile aynı sütunlar). i. bar için yalnız s.iloc[:i+1] kullanılır.
onceki  : bugünden ÖNCEKİ seansların listesi (eskiden yeniye), en fazla `geri` seans. SALT OKUNUR.
          Veri boşluğu kuralı: iki ardışık seans arasında > 5 iş günü varsa liste o boşlukta kesilir
          (05.05.2026'nın öncesi görünmez). Liste boş olabilir.
bilgi   : dict —
          gun          : bugünün tarihi (Timestamp)
          devir_bugun  : bugün yeni vadenin ilk işlem günü mü
          ayni_vade    : onceki ile aynı uzunlukta bool dizi; True = o seans bugünkü kontratla aynı vadede.
                         FİYAT DÜZEYİ karşılaştıran kurallar (dünün kapanışı/yükseği/düşüğü, gece boşluğu, önceki
                         değer alanı) YALNIZ ayni_vade=True seansları kullanmalıdır; vade geçişinde seri GAP'lıdır.
                         Hacim / oynaklık / getiri ortalamaları tüm onceki'yi kullanabilir.
          vade_no      : bugünün vade sıra numarası
"Dünkü kapanış" = önceki gündüz seansının son barının (≤ 18:15) kapanışıdır; akşam seansı veride YOKTUR,
bu yüzden gece boşluğu akşam seansındaki hareketi de içerir.
"""
import inspect, re
import numpy as np, pandas as pd
import motor as M

SURUM = "1.00"
GERI_MAX = 60          # seans
BOSLUK_IS_GUNU = 5     # bundan uzun ara = veri boşluğu, bağlam kesilir
YASAK = [r"read_csv", r"read_parquet", r"read_pickle", r"\bopen\s*\(", r"\byukle\b", r"\bglob\b", r"\bos\.",
         r"pathlib", r"requests", r"urllib", r"gzip", r"pickle", r"np\.load", r"\bimport\s+motor", r"\bglobal\b",
         r"__import__", r"\beval\s*\(", r"\bexec\s*\("]


def _baglam_tablosu(seanslar):
    gunler = [s.gun.iloc[0] for s in seanslar]
    assert all(a < b for a, b in zip(gunler, gunler[1:])), "seanslar tarih sırasında ve tekil olmalı"
    devir = M.devir_gunleri(seanslar)
    vade_no = np.cumsum([g in devir for g in gunler])
    blok = np.zeros(len(gunler), dtype=int)
    for k in range(1, len(gunler)):
        ara = np.busday_count(gunler[k - 1].date(), gunler[k].date())
        blok[k] = blok[k - 1] + (1 if ara > BOSLUK_IS_GUNU else 0)
    blok_bas = {}
    for k, b in enumerate(blok):
        blok_bas.setdefault(b, k)
    return gunler, devir, vade_no, blok, blok_bas


def baglam(seanslar, k, geri, _tablo=None):
    """k. seans için (onceki, bilgi). Yalnız seanslar[:k] kullanılır."""
    gunler, devir, vade_no, blok, blok_bas = _tablo or _baglam_tablosu(seanslar)
    geri = int(min(max(geri, 0), GERI_MAX))
    bas = max(blok_bas[blok[k]], k - geri)
    idx = list(range(bas, k))
    onceki = [seanslar[j] for j in idx]
    assert all(gunler[j] < gunler[k] for j in idx)
    bilgi = dict(gun=gunler[k], devir_bugun=gunler[k] in devir,
                 ayni_vade=np.array([vade_no[j] == vade_no[k] for j in idx], dtype=bool),
                 vade_no=int(vade_no[k]))
    return onceki, bilgi


def _sarmala(seanslar, sinyal, geri):
    tablo = _baglam_tablosu(seanslar)
    harita = {g: k for k, g in enumerate(tablo[0])}

    def tek(s, **p):
        k = harita[s.gun.iloc[0]]
        onceki, bilgi = baglam(seanslar, k, geri, tablo)
        return sinyal(s, onceki, bilgi, **p)
    return tek, tablo


def statik_denetim(sinyal):
    """Sinyal modülünün kaynağında dosya/ağ/küresel erişim yok mu? (gelecek seansa dolanma yolu)"""
    try:
        with open(inspect.getfile(sinyal), encoding="utf-8") as f:   # modülün TAMAMI (modül düzeyi kod dahil)
            kaynak = f.read()
    except (OSError, TypeError):
        return False, "kaynak okunamadı"
    kod = "\n".join(l.split("#", 1)[0] for l in kaynak.splitlines())
    for y in YASAK:
        if re.search(y, kod):
            return False, f"yasak kalıp: {y}"
    return True, "temiz"


def _ozet_dizi(onceki):
    return [(float(o.close.sum()), float(o.volume.sum()), len(o)) for o in onceki]


def kanarya_cok(seanslar, sinyal, p, geri, k_seans=40, k_kesim=6, tohum=1):
    """(a) statik denetim, (b) gün içi kesim (motor.kanarya, bağlam sabit), (c) bağlam bütünlüğü:
    seans listesi bugünde kesilince sinyal aynı mı, sinyal onceki'yi değiştiriyor mu."""
    ok, msg = statik_denetim(sinyal)
    if not ok:
        return False, "statik: " + msg
    tek, tablo = _sarmala(seanslar, sinyal, geri)
    ok, msg = M.kanarya(seanslar, tek, p, k_seans=k_seans, k_kesim=k_kesim, tohum=tohum)
    if not ok:
        return False, "gün içi: " + msg
    rng = np.random.default_rng(tohum + 7)
    for k in rng.choice(len(seanslar), size=min(k_seans, len(seanslar)), replace=False):
        k = int(k)
        s = seanslar[k]
        onceki, bilgi = baglam(seanslar, k, geri, tablo)
        once = _ozet_dizi(onceki)
        tam = np.sign(np.nan_to_num(np.asarray(sinyal(s, onceki, bilgi, **p), float)))
        if _ozet_dizi(onceki) != once:
            return False, f"seans {s.gun.iloc[0].date()}: sinyal onceki seansları değiştirdi"
        kisa_liste = seanslar[:k + 1]
        o2, b2 = baglam(kisa_liste, k, geri)
        kisa = np.sign(np.nan_to_num(np.asarray(sinyal(s, o2, b2, **p), float)))
        if not np.array_equal(kisa, tam):
            return False, f"seans {s.gun.iloc[0].date()}: gelecek seanslar silinince sinyal değişti"
    return True, "temiz"


def calistir(seanslar, sinyal, p, cikis, max_islem=1, geri=20):
    tek, _ = _sarmala(seanslar, sinyal, geri)
    return M.calistir(seanslar, tek, p, cikis, max_islem)


def kart_calistir_cok(seanslar, sinyal, varyantlar, cikis_fn, max_islem=1, geri=20):
    """motor.kart_calistir ile aynı çıktı; K5 = kanarya_cok. geri: bağlam derinliği (≤ 60 seans).
    Varyant sözlüğünde 'geri' anahtarı varsa o varyant için onu kullanır (sinyale geçirilmez)."""
    assert 1 <= len(varyantlar) <= 12, "kart başına 1–12 varyant"
    devir = M.devir_gunleri(seanslar)
    sonuc = []
    for p in varyantlar:
        g = p.get("geri", geri); q = {a: b for a, b in p.items() if a != "geri"}
        isl = calistir(seanslar, sinyal, q, cikis_fn(p), max_islem, g)
        sonuc.append(dict(p=p, **M.ozet(isl, devir)))
    df = pd.DataFrame(sonuc)
    isaret = np.sign(df.brut.to_numpy())
    for i, r in df.iterrows():
        oran = (isaret == np.sign(r.brut)).mean() if len(df) > 1 else 0.0
        g = r.p.get("geri", geri); q = {a: b for a, b in r.p.items() if a != "geri"}
        ok, msg = kanarya_cok(seanslar, sinyal, q, g)
        k = M.kapilar(r, ok, oran)
        for a, v in k.items():
            df.loc[i, a] = v
        df.loc[i, "kanarya"] = msg
    df["motor"] = "motor_cok " + SURUM
    return df
