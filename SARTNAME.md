# XU30 Strateji Araştırma Ajanı — Şartname v1.02

**Tarih:** 13.10.2026 · **Durum:** YÜRÜRLÜKTE (v1.01: keşif verisi 00-Akis kararı, motor, K6–K7)
**Kullanıcı kararları (13.10.2026):** bulut zamanlanmış görev (A), döngü 4–6 saat,
kilitli bölüm 20 seans, keşif testleri ayrı sayaçta, keşif verisi 00-Akis (624 seans).
**Dayanak:** MÖT-AJAN-01 (Ek A), Std. 0.5.8 (brüt < 4,2 p kapanır), Ölçüm Arşivi 2.19 (maliyet 8,4 p).

---

## 1. Görev

Ajan internette (makale, akademik çalışma, forum, video transkripti) XU30 gündüz
seansına uyarlanabilir işlem fikirleri arar. Her fikri **mekanik bir kurala** çevirir,
keşif verisinde **gerçek maliyetle** eler ve sonuçları bir deftere yazar.

Ajan **işlem yapmaz, MT5'e dokunmaz, kilitli veriyi göremez, eşik değiştiremez.**
Çıktısı "aday" önerisidir; adayın kaderi Soydan'ın oturumunda verilir.

## 2. Değişmez kısıtlar

| Kısıt | Değer |
|---|---|
| Enstrüman | XU30_YAKINVADE, yalnız gündüz seansı (09:45–18:05 işlem penceresi) |
| Gece / akşam seansı | Pozisyon taşınmaz, akşam seansında işlem yok (risk kararı 29.09.2026) |
| Maliyet | **komisyon 6,0 × fiyat/16.500 + spread 2,4 p** gidiş-dönüş (16.500'de 8,4 p). Komisyon oranı sabit olduğu için fiyatla ölçeklenir (2023'te ~5,6 p). Kayma modellenmez, raporda not edilir |
| Hacim | Yalnız tik bayraklı gerçek hacim (buy_volume / sell_volume) |
| Ortalama | Yumuşatma gerektiren her yerde JMA tercih edilir (proje kuralı) |
| Vade geçişi | Devir günleri (tek ayların ilk işlem günü) ayrı raporlanır; kenar devir gününe dayanıyorsa aday olamaz |

## 3. Döngü (her koşu, 3 saatte bir — v1.02)

> **v1.02 (13.10.2026):** Okuma ile test ayrıldı. Her koşu **15–30 kaynak** okur ve fikirleri sınırsız
> olarak `havuz.csv`'ye yazar (ön eleme + öncelik puanı, KS'ye eklenmez). Test bütçesi değişmedi:
> koşu başına en fazla 2 kart / 12 varyant, havuzun en yüksek puanlı fikirlerinden seçilir.
> Ayrıntılı adımlar `AJAN.md`'dedir; aşağıdaki liste genel akıştır.

1. **Defteri oku.** Denenmiş fikirler, kapanmış aileler (Ölçüm Arşivi 2.19 dahil), sayaç.
2. **Tema seç.** Defterde en az kapsanan tema (Böl. 4). Aynı fikri ikinci kez deneme.
3. **Ara.** 5–15 kaynak. Öncelik: hakemli çalışma / ön baskı > yazarı belli blog > forum.
   Video yalnız transkript ve açıklama üzerinden okunur.
4. **Hipotez kartı yaz** (Böl. 5). Kural tam tanımlanamıyorsa kart "TANIMSIZ" kapanır.
5. **Uygunluk (K0).** Gece pozisyonu, akşam seansı, elimizde olmayan veri (opsiyon,
   emir defteri derinliği, haber akışı) gerektiriyorsa elenir.
6. **Kâğıt üstü maliyet kontrolü.** Kaynağın iddia ettiği tipik hareket × isabet
   8,4 p'yi aşmıyorsa test edilmeden elenir (gerekçe yazılır).
7. **Keşif testi.** Kart başına **en fazla 12 varyant**. Her varyant keşif sayacına eklenir.
8. **Kapılar** (Böl. 6) ve **sızıntı kanaryası.**
9. **Defteri güncelle**, koşu özetini yaz.
10. Haftanın ilk koşusu (Pazartesi sabahı) **haftalık raporu** yazar (Böl. 8).

## 4. Tema havuzu (başlangıç)

Açılış aralığı ve ilk saat yapısı · gün içi mevsimsellik (saat dilimi etkisi) ·
sipariş akışı dengesizliği / delta · hacim profili (VWAP, POC sapması) ·
oynaklık rejimi koşullu kurallar · ortalamaya dönüş (kısa ufuk, 2–5 dk) ·
seans sonu akışı · vade sonu / devir etkisi · endeks–hisse ilişkisi (yalnız elimizdeki veriyle) ·
akademik "intraday momentum" (ilk yarım saat → son yarım saat) literatürü.

Kapanmış aileler (yeniden denenmez, yalnız **yeni bir mekanizma** getirirse):
SAR ailesi, OSC/OFC uç bölge-sıfır kesişimi-eğim, Nyao scalper, öngörüsüz giriş + yönetim
("sürüş"), σ ölçekli hedef, H-K1 açılış kırılımı, H-B1 büyük emir, H-D1 dönüş kapısı.

## 5. Hipotez kartı

```
kart_id      : HK-YYYYMMDD-nn
kaynak       : başlık, yazar, URL, tarih, tür (akademik/blog/forum/video)
iddia        : kaynağın kendi iddiası (kendi cümlelerimizle)
mekanizma    : neden çalışması gerektiği (yoksa "YOK" — bu bir uyarıdır)
kural        : giriş zamanı/koşulu, yön, çıkış (zaman/hedef/stop), seans başına işlem sayısı
parametreler : en fazla 12 kombinasyon, KOŞUDAN ÖNCE yazılır
beklenen     : kaynağa göre işlem başı brüt (puan), yoksa "bilinmiyor"
```

## 6. Kapılar

| Kapı | Koşul | Kaynak |
|---|---|---|
| K0 | Uygunluk (Böl. 3.5) | Kısıtlar |
| K1 | Keşif **brüt ≥ 0,5 × maliyet** (16.500'de 4,2 p) | Std. 0.5.8 |
| K2 | Keşif **net > 0** ve seans-kümeli **t ≥ 3,0** | MÖT-AJAN-01: kural başı sahte geçiş ≈ %0,004 |
| K3 | En iyi 5 gün çıkarıldığında **net > 0** | Aykırı gün kapısı (17.09.2026 dersi) |
| K4 | Komşu parametrelerin çoğunluğunda brüt aynı işaret | Tek noktalı uyum elenir |
| K5 | **Sızıntı kanaryası** geçer | MÖT-AJAN-01 bulgusu (Ek A.3) |
| K6 | İki bağımsız dönemde (2023-09→2024-12 / 2025-01→2026-09) **net > 0** | Rejim/tick değişimine dayanıklılık |
| K7 | Vade devir günleri çıkarılınca **net > 0** | Proje talimatı (devir boşlukları) |

Kapılar `motor.py` içinde sabittir; ajan yalnız sinyal fonksiyonu yazar (giriş: sinyal barından
sonraki barın açılışı; stop/hedef aynı barda değerse STOP; 18:05'te zorla kapanış).

**Sızıntı kanaryası:** sinyal, rastgele kesim noktalarında ve her sinyal barında geleceği
silinmiş veriyle yeniden hesaplanır; tek bir sinyal bile değişirse kural GEÇERSİZ sayılır ve kod düzeltilene kadar
sonuç yazılmaz. Ayrıca geriye bakış penceresi seans başını aşan kombinasyonlar test edilmez.

Hepsini geçen kural **ADAY** olur. Aday işlem kuralı değildir.

**Beklenen sahte geçiş:** K2 tek başına kural başına ~%0,135 sahte geçiş verir (tek yönlü t ≥ 3).
Günde 8 koşu × 12 varyant ile haftada en fazla ~670 varyantta ~0,9 sahte K2 geçişi beklenir; K3/K6/K7 bunu azaltır ama sıfırlamaz.
Haftalık rapor bu sayıyı yazmak zorundadır.

## 7. Sayaçlar ve kilitli veri

- **Keşif sayacı (KS):** ajanın test ettiği her varyant +1. Genel H- sayacına **girmez**.
- **Genel H- sayacı:** yalnız Soydan'ın onayıyla terfi eden aday için açılan ön kayıt +1.
- **Kilitli bölüm:** **14.09.2026 → 09.10.2026 (20 seans)** ajanın deposunda **yoktur**
  (fiziksel kilit). Keşif verisi 08.09.2026'da biter; 09–11.09 tampon, kullanılmaz.
  10.10.2026 ve sonrası ileri test verisidir. Kilit testi Soydan'ın oturumunda, aday başına **bir kez** yapılır.
- **Kilit testinin gücü düşüktür** (Ek A.4): 20 seans, seans başı tek işlemde ancak
  ~28 p/işlem net kenarı ayırt eder. Bu yüzden kilit testi **yalnız eleme** yapar
  (net ≤ 0 ise aday düşer); onay **ileri testle** gelir: ön kayıttan sonra gelen yeni seanslar.

## 8. Çıktılar

**Defter (`defter.csv`)** — her varyant bir satır:
`tarih, kart_id, tema, kaynak_url, varyant, n_seans, n_islem, brut, net, t, net_eksi5gun, K0..K5, sonuc, gerekce, KS`

**Koşu özeti (`kosular/YYYYMMDD-HHMM.md`)** — okunan kaynaklar, yazılan kartlar, sonuçlar.

**Haftalık rapor (`raporlar/hafta-YYYY-WW.md`)**:
1. Hafta özeti: kaynak / kart / varyant sayısı, KS değeri
2. Adaylar (varsa): kart, sonuçlar, kuyruk duyarlılığı, **önerilen H- ön kaydı taslağı**
3. Elenenler: tek satır gerekçe, kapı bazında dağılım
4. Kaynak kalitesi notları (tekrar eden, ölçülemeyen, ücretli)
5. Gelecek haftanın temaları

Ajan hiçbir sonucu "çalışan strateji" diye sunmaz; en güçlü ifade "aday" dır.

## 9. Kurulum (v1.01)

| | |
|---|---|
| Çalışma yeri | Bulut zamanlanmış görev, 3 saatte bir, günde 8 koşu (bilgisayar kapalıyken de çalışır) |
| Depo | Özel GitHub deposu: `motor.py`, `AJAN.md`, keşif verisi, defter, raporlar |
| Keşif verisi | `xu30_kesif_m1_gunduz.csv.gz` — `00-Akis.csv` (SHA-256 `a3e7c018…`) gündüz barları, **624 seans, 01.09.2023 → 08.09.2026**; hariç: 02.12.2024 (10 bar), 09.09.2026 (kesik). Boşluk: 31.10.2025 → 05.05.2026 veri yok. Dosya SHA-256 `1242a76d…` |
| Motor testi | Gerçek kural (10:15 · 5 dk delta · 30 dk): 82 seansta net +35 p, 624 seansta **net −6,1 p** (t −2,7). Bilerek sızıntılı kural: t 20,6 ile K2'yi geçti, **kanarya yakaladı** |

## Ek A — MÖT-AJAN-01 (13.10.2026)

**Betik:** `mot_ajan_kapisi.py` · **Veri:** proje kopyası `XU30_M1_birlesik.csv`
(102 seans, 05.05 → 30.09.2026, SHA-256 `7049b509bdcf1e16…`) — güncel 109 seanslık sürüm değil,
yöntem sınaması için yeterli. Keşif 82 seans (05.05 → 02.09), kilit 20 seans (03.09 → 30.09).

**Kural ailesi:** 1.792 "makul görünen" kural — giriş 10:00–17:00 (15 dk ızgara) ×
geriye bakış 5/15/30/60 dk × özellik (getiri / delta) × takip/ters × tutma 15/30/60/120 dk;
seans başına tek işlem, maliyet 8,4 p.

### A.1 Ailenin genel görünümü
Keşif brüt ortalaması **+0,00 p** (std 9,3). K1'i (brüt ≥ 4,2) tek başına **%26** geçiyor —
yani K1 tek başına bir filtre değildir, gürültünün dörtte biri onu aşar.

### A.2 Kapı eşiği
| Kapı (net > 0 ve t ≥) | Gerçek aileden geçen | Null'da kural başı sahte geçiş | Kilitte net > 0 kalan |
|---|---|---|---|
| 2,00 | 10 (%0,56) | %0,131 | 3 / 10 |
| 2,58 | 1 | %0,017 | 0 / 1 |
| **3,00** | **1** | **%0,004** | **0 / 1** |
| 3,50 | 0 | %0,001 | — |

Null: işaret karıştırma (seans bazında rastgele yön, 200 tekrar). t ≥ 3,0'da geçen tek kural
(10:15, 5 dk delta takip, 30 dk tut: keşif net +35,2 p, t 3,30) kilitte **−25,5 p**. Aile,
gerçek kenar olmadığı yönündeki proje bulgusuyla tutarlı. **Karar: K2 eşiği t ≥ 3,0.**

### A.3 Sızıntı bulgusu (kapıyı tasarlatan asıl ders)
İlk koşuda betikte bir indeks hatası vardı: geriye bakış penceresi seans başını aştığında
dizinin sonundan (aynı günün 17:50'si) okunuyordu — **gelecekten bilgi**. Sonuç: 12 kural
t = 3–6,4 ile keşif kapısını geçti ve **11'i kilitli bölümde de pozitif kaldı**
(ör. 10:00 · 30 dk ters · 120 dk tut: keşif +93,6 p, kilit +124,0 p).

> **Kilitli bölüm kod hatasına karşı koruma sağlamaz.** Hata her iki bölümde de aynı
> sızıntıyı üretir. Bu yüzden K5 (sızıntı kanaryası) zorunlu kapı yapıldı.

Hata düzeltildi (geçersiz kombinasyonlar aileden çıkarıldı, 1.856 → 1.792); yukarıdaki tablo
düzeltilmiş sonuçtur.

### A.4 Güç
Seans başı P&L std medyanı **63 p**.

| Net kenar (p/işlem) | 82 seans, t ≥ 3 yakalama | 646 seans (tahmini) |
|---|---|---|
| 5 | %1 | ~%16 |
| 10 | %6 | ~%85 |
| 20 | %45 | ~%100 |

t ≥ 3 için gereken net kenar: **82 seansta ~21 p, 646 seansta ~7,4 p.**
Kilitli 20 seansta net > 0'ın t ≥ 2 ile görülmesi için ~28 p gerekir → kilit yalnız eleme yapar.
(646 seans sütunu std'nin aynı kaldığı varsayımıyla hesaplandı; tick boyu değişimi ve rejim
farkı bunu bozabilir.)

### A.5 Neye kör
- Tek işlem/seans ailesi ölçüldü. Günde çok işlem yapan kurallarda n büyür ama seans-içi
  bağımlılık nedeniyle t yine seans kümesiyle hesaplanmalı.
- Giriş, sinyal barının kapanışından; spread 2,4 p sabit. Açılış saatlerinde spread daha geniş.
- Null, kuralların gerçek korelasyon yapısını tam taşımaz; aile içi korelasyon yüksek olduğu için
  "kaç kural geçti" sayısı bağımsız denemelerden daha oynaktır.
