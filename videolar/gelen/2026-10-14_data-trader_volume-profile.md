url: https://www.youtube.com/watch?v=Xa2fB097ajs
baslik: The BEST Volume Profile Trading Guide You'll EVER FIND
kanal: Data Trader
tarih: 2026-09-15
sure: 23:49
kaynak: Chrome'daki Claude kural dökümü (youtube-transcriber ile transkript okunarak; birebir metin değil)
not: Soydan'ın seçtiği video (14.10.2026). Otomatik altyazıda POC "PC", VAH "VH" geçiyor; dökümde doğru terimler kullanıldı.
---

## Piyasa ve periyot
- Piyasa: belirtilmemiş (23:27 altın geçiyor ama Telegram tanıtımı, strateji örneği değil).
- Periyot: günlük altı herhangi bir intraday (5 dk, 10 dk, 1 saat sayılıyor, 8:57); anlatım örneği 45 dk (7:32), gerçek grafik örneği 15 dk (9:08).
- Araç: TradingView Fixed Range Volume Profile (4:21). Grafik saati borsa saati olmalı (9:12).

## Kavram tanımları
| kavram | videodaki tanım |
|---|---|
| Volume profile | her fiyat seviyesinde işlem gören hacim (1:17) |
| Uzun bar | yüksek hacim bölgesi; fiyat yavaşlar, sıkışır (2:27) |
| Kısa bar | düşük hacim bölgesi; fiyat hızlı geçer (2:56) |
| POC | aralıktaki en yüksek hacimli fiyat seviyesi; destek/direnç gibi (5:34) |
| Değer alanı | toplam hacmin %70'ini içeren bölge (6:10) |
| VAH / VAL | değer alanının üst / alt sınırı; VAH üstü premium, VAL altı iskonto, dışı "overextended" (6:29) |
| Profil penceresi | önceki günün tam seansı, ilk mumdan son muma (7:44) |

Sayısal ayarlar (5:11): row size 60, value area %70.
Yerleştirme (7:24–8:53): profil her zaman tamamlanmış ÖNCEKİ seansa konur, seviyeler mevcut seansa uzatılır
(mevcut seansın profili kayar, yanıltıcı). Seans bitince bir sonraki güne kaydırılır.

## Giriş koşulu ve yön
**Strateji 1 — POC sekmesi (10:26):** önceki seans değer alanının DIŞINDA kapanmış olmalı (içeride kapandıysa geçersiz, 11:05).
Fiyatın POC'ye gelmesi beklenir; price action onayı: aşağı için seviyeyi delip geri dönen uzun fitil + ardışık kırmızı mumlar (12:01),
yukarı için POC dokunuşu sonrası büyük yeşil mum / yutan boğa (13:29). Yön: POC'den sekme yönünde.

**Strateji 2 — Değer alanı dönüşü (14:29):** önceki seans değer alanının İÇİNDE kapanmış olmalı (15:03). Mevcut seansta fiyat VAH
üstüne ya da VAL altına çıkar; sonra bir mumun değer alanı İÇİNDE kapanması gerekir — yalnız fitil yetmez (15:49).
Yön: VAL altına taştıysa uzun, VAH üstüne taştıysa kısa.

**Strateji 3 — Kırılım (17:28):** önceki seansın kapanış yeri fark etmez (17:54). Mevcut seansta değer alanı dışına "belirgin" kırılım
(sayısal eşik yok); değer alanına doğru geri çekilme seviye civarında tutunmalı, "çok derine" girmemeli (sayısal tanım yok, 18:28);
kırılım yönünde yapı kırılımı: boğada daha yüksek tepe, ayıda daha düşük dip (18:50). Yön: kırılım yönünde.

**Birleşik sistem (20:47):** önceki seansın nerede kapandığına ve fiyatın davranışına göre üç kurulumdan geçerli olan seçilir.

## Stop, hedef, çıkış
| | stop | hedef |
|---|---|---|
| Strateji 1 | POC'nin hemen üstü (kısa) / altı (uzun) | 2R |
| Strateji 2 | swing dibi yakını (uzun) / tepeler yakını (kısa) | 2R |
| Strateji 3 | yapı kırılımının hemen altı (uzun) / üstü (kısa) | 2R |
Zaman çıkışı, iz süren stop, kısmi kapatma, başabaş: belirtilmemiş.

## Günde kaç işlem
Üst sınır belirtilmemiş; "seans bitmediği sürece kurulum aramaya devam" (16:24); birleşik örnekte tek seansta 2 işlem (21:06).

## Filtreler
Saat / hacim / oynaklık / haber filtresi: belirtilmemiş.

## Gerekli veri
- ÖNCEKİ günün tek, tam seans profili zorunlu (mevcut günün profili bilinçli olarak kullanılmıyor) → tek seanslık motorla test edilemez.
- Emir defteri / delta gerekmiyor; yalnız OHLC + hacim.
- Seans sınırı tanımı (gece yarısı mı, borsa seansı mı) ve boşlukla açılan günde ne yapılacağı: belirtilmemiş.

## Kanıt
- Backtest yok; dönem, maliyet, isabet oranı: belirtilmemiş. "High win rate" iddiası rakamsız.
- Tek sayısal iddia (23:27): altının destekten "3.000 pip'ten fazla" yükselişi — Telegram tanıtımı, stratejinin kanıtı değil.
- Kanıt = elle seçilmiş tekil grafik örnekleri: 7 örneğin 6'sı kazanan. Kanıt düzeyi: ORNEK.

## Videodaki örnekler
| zaman | örnek |
|---|---|
| 1:28 | 1 saatlik grafikte zaman hacmi vs fiyat hacmi |
| 3:16 | düşük hacimde hızlı geçiş, yüksek hacimde yavaşlama şeması |
| 4:21 / 5:11 | TradingView uygulaması ve ayarlar |
| 7:29 | yerleştirme anlatımı (45 dk) |
| 8:55 | 15 dk grafik, profil önceki seansa |
| 11:16 | POC sekmesi #1: dışarıda kapanmış seans, POC'de uzun fitil → kısa → 2R (12:54) |
| 13:01 | POC sekmesi #2: yutan boğa → uzun → 2R (14:03) |
| 15:10 | değer alanı dönüşü #1: VAL altı taşma, içeri kapanış → uzun → 2R (16:22) |
| 16:32 | aynı seansta #2: VAH üstü taşma → kısa → 2R (17:02) |
| 18:00 | kırılım #1: boğa kırılımı, tutunan geri çekilme, yüksek tepe → uzun → 2R (19:36) |
| 19:40 | kırılım #2: önce geçersiz kurulum; 20:05 VAL altı kırılım → kısa → 2R (20:38) |
| 21:06 | birleşik: dönüş uzun −1R, ardından kırılım kısa +2R, seans net +1R (22:04) |

## Döküm hazırlayanın uyarıları
- Sabit 2R hedefle beklenen değer > 0 için isabet > %33 gerekir; veri sunulmuyor.
- İki kural sayısallaştırılmamış: kırılımın "belirgin"liği ve geri çekilmenin "çok derin" olmaması.
- Maliyet hiç yok; VİOP komisyon + spread 2R hedefli gün içi sistemde beklenen değeri ciddi düşürür.
- XU30'da gece boşluğu, önceki gün profilini mevcut seansa taşırken kayma yaratır; seans tanımı netleştirilmeli.
