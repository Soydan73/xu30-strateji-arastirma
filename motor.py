# -*- coding: utf-8 -*-
"""
XU30 araştırma ajanı — ortak test motoru v1.00 (13.10.2026)

Ajan YALNIZ sinyal fonksiyonu yazar; giriş/çıkış, maliyet, istatistik, kapılar ve
sızıntı kanaryası burada sabittir. Bu dosyayı ajan DEĞİŞTİRMEZ.

Sinyal fonksiyonu sözleşmesi
----------------------------
    def sinyal(s: pd.DataFrame, **p) -> np.ndarray   # uzunluk len(s), değerler -1/0/+1
s : TEK seansın gündüz M1 barları (zaman sıralı). Sütunlar:
    time, open, high, low, close, volume, buy_volume, sell_volume, ticks, seans, dk (09:00'dan dakika)
Sinyal i. barın KAPANIŞINDA bilinen bilgiyle üretilir; motor i+1. barın AÇILIŞINDA girer.
Fonksiyon i. bar için yalnız s.iloc[:i+1]'i kullanmalıdır — kanarya bunu sınar.

Çıkış seçenekleri (cikis sözlüğü)
--------------------------------
    H      : en fazla H bar tut (zorunlu)
    stop   : giriş fiyatından puan (opsiyonel)
    hedef  : giriş fiyatından puan (opsiyonel)
    ters   : True ise ters sinyalde kapat (opsiyonel)
Aynı barda stop ve hedef değerse STOP sayılır (muhafazakâr). 18:05'te zorla kapanır.
Pozisyondayken yeni giriş yok; seans başına en fazla `max_islem` işlem.
"""
import numpy as np, pandas as pd

KOMISYON_P_16500 = 6.0      # gidiş-dönüş, 16.500 fiyatında; fiyatla orantılı (komisyon oranı sabit)
SPREAD_P = 2.4              # gidiş-dönüş, puan
GIRIS_BAS, GIRIS_SON, ZORLA_KAPAT = 9 * 60 + 45, 18 * 60, 18 * 60 + 5   # dakika
DONEM_SINIRI = pd.Timestamp("2025-01-01")   # K6: iki bağımsız dönem
T_ESIK = 3.0                                 # MÖT-AJAN-01


def maliyet(fiyat):
    return KOMISYON_P_16500 * fiyat / 16500.0 + SPREAD_P


def yukle(yol):
    m = pd.read_csv(yol, parse_dates=["time"])
    m["dk"] = m.time.dt.hour * 60 + m.time.dt.minute
    m["gun"] = m.time.dt.normalize()
    seanslar = [g.reset_index(drop=True) for _, g in m.groupby("gun", sort=True)]
    return seanslar


def devir_gunleri(seanslar):
    """Tek ayların (1,3,5,7,9,11) ilk işlem günü = yeni vadenin ilk günü."""
    gunler = pd.Series([s.gun.iloc[0] for s in seanslar])
    ay = gunler.dt.to_period("M")
    ilk = gunler.groupby(ay).transform("min")
    return set(gunler[(gunler == ilk) & (gunler.dt.month % 2 == 1)])


def _seans_islemleri(s, sig, cikis, max_islem):
    o, h, l, c, dk = (s[k].to_numpy(float) for k in ("open", "high", "low", "close", "dk"))
    n, islemler, i = len(s), [], 0
    H, stop, hedef, ters = cikis["H"], cikis.get("stop"), cikis.get("hedef"), cikis.get("ters", False)
    while i < n - 1 and len(islemler) < max_islem:
        y = sig[i]
        if y == 0 or not (GIRIS_BAS <= dk[i + 1] <= GIRIS_SON):
            i += 1; continue
        g = i + 1; px = o[g]; cik = None
        for j in range(g, min(g + H, n)):
            if dk[j] >= ZORLA_KAPAT:
                cik = (j, o[j], "seans"); break
            if stop is not None and ((y > 0 and l[j] <= px - stop) or (y < 0 and h[j] >= px + stop)):
                cik = (j, px - y * stop, "stop"); break
            if hedef is not None and ((y > 0 and h[j] >= px + hedef) or (y < 0 and l[j] <= px - hedef)):
                cik = (j, px + y * hedef, "hedef"); break
            if ters and j > g and sig[j - 1] == -y:
                cik = (j, o[j], "ters"); break
        if cik is None:
            j = min(g + H, n) - 1
            cik = (j, c[j], "zaman")
        j, cx, neden = cik
        brut = y * (cx - px)
        islemler.append((s.gun.iloc[0], s.time.iloc[g], y, px, cx, brut, brut - maliyet(px), neden))
        i = j if neden in ("seans", "ters") else j + 1
    return islemler


def calistir(seanslar, sinyal, p, cikis, max_islem=1):
    rows = []
    for s in seanslar:
        sig = np.asarray(sinyal(s, **p), dtype=float)
        assert len(sig) == len(s), "sinyal uzunluğu seansla aynı olmalı"
        rows += _seans_islemleri(s, np.sign(np.nan_to_num(sig)), cikis, max_islem)
    return pd.DataFrame(rows, columns=["gun", "giris", "yon", "px", "cx", "brut", "net", "neden"])


def kanarya(seanslar, sinyal, p, k_seans=40, k_kesim=6, tohum=1):
    """Gelecek barlar silinince geçmiş sinyaller değişiyorsa SIZINTI var."""
    rng = np.random.default_rng(tohum)
    secim = rng.choice(len(seanslar), size=min(k_seans, len(seanslar)), replace=False)
    for si in secim:
        s = seanslar[si]
        tam = np.sign(np.nan_to_num(np.asarray(sinyal(s, **p), float)))
        kesimler = set(rng.integers(5, len(s) - 1, size=k_kesim).tolist())
        kesimler |= {int(i) for i in np.flatnonzero(tam) if i < len(s) - 1}   # her sinyal barında da kes
        for kes in sorted(kesimler):
            kisa = np.sign(np.nan_to_num(np.asarray(sinyal(s.iloc[:kes + 1].copy(), **p), float)))
            if not np.array_equal(kisa, tam[:kes + 1]):
                return False, f"seans {s.gun.iloc[0].date()} kesim {kes}: geçmiş sinyal değişti"
    return True, "temiz"


def _t(x):
    x = np.asarray(x, float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return 0.0
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


def ozet(islem, devir=frozenset()):
    """Seans-kümeli istatistik: t, seans başına net toplamı üzerinden."""
    if islem.empty:
        return dict(n_islem=0, n_seans=0, brut=0, net=0, t=0, net_eksi5=0, t_eksi5=0,
                    net_A=0, net_B=0, net_devirsiz=0, maliyet_ort=0)
    ss = islem.groupby("gun").net.sum()
    eksi5 = ss.sort_values().iloc[:-5] if len(ss) > 5 else ss.iloc[:0]
    A = islem[islem.gun < DONEM_SINIRI]; B = islem[islem.gun >= DONEM_SINIRI]
    dv = islem[~islem.gun.isin(devir)]
    return dict(
        n_islem=len(islem), n_seans=ss.size,
        brut=islem.brut.mean(), net=islem.net.mean(), t=_t(ss),
        net_eksi5=eksi5.sum() / max(1, islem.gun.isin(eksi5.index).sum()), t_eksi5=_t(eksi5),
        net_A=A.net.mean() if len(A) else np.nan, net_B=B.net.mean() if len(B) else np.nan,
        net_devirsiz=dv.net.mean() if len(dv) else np.nan,
        maliyet_ort=(islem.brut - islem.net).mean(),
    )


def kapilar(oz, kanarya_ok, komsu_ayni_isaret_orani):
    k = {}
    k["K1"] = oz["brut"] >= 0.5 * oz["maliyet_ort"] if oz["n_islem"] else False
    k["K2"] = oz["net"] > 0 and oz["t"] >= T_ESIK
    k["K3"] = oz["net_eksi5"] > 0
    k["K4"] = komsu_ayni_isaret_orani >= 0.5
    k["K5"] = bool(kanarya_ok)
    k["K6"] = (oz["net_A"] > 0) and (oz["net_B"] > 0)
    k["K7"] = oz["net_devirsiz"] > 0 if not np.isnan(oz["net_devirsiz"]) else False
    k["ADAY"] = all(k.values())
    return k


def kart_calistir(seanslar, sinyal, varyantlar, cikis_fn, max_islem=1):
    """varyantlar: parametre sözlükleri listesi (<= 12). cikis_fn(p) -> cikis sözlüğü.
    Döner: her varyant için özet + kapılar (DataFrame)."""
    assert 1 <= len(varyantlar) <= 12, "kart başına 1–12 varyant"
    devir = devir_gunleri(seanslar)
    sonuc = []
    for p in varyantlar:
        isl = calistir(seanslar, sinyal, p, cikis_fn(p), max_islem)
        sonuc.append(dict(p=p, **ozet(isl, devir)))
    df = pd.DataFrame(sonuc)
    isaret = np.sign(df.brut.to_numpy())
    for i, r in df.iterrows():
        oran = (isaret == np.sign(r.brut)).mean() if len(df) > 1 else 0.0
        ok, msg = kanarya(seanslar, sinyal, r.p)
        k = kapilar(r, ok, oran)
        for a, v in k.items():
            df.loc[i, a] = v
        df.loc[i, "kanarya"] = msg
    return df
