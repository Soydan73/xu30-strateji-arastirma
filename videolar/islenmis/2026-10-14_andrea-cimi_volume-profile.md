url: https://www.youtube.com/watch?v=qihraSSdI_M
baslik: How to ACTUALLY use Volume Profiles
kanal: Andrea Cimi (deepcharts ile ortak)
tarih: 2026-01-19
sure: 24:15
kaynak: Chrome'daki Claude kural dökümü (youtube-transcriber ile transkript okunarak; birebir metin değil)
not: Soydan'ın seçtiği video (14.10.2026). Delta / order flow katmanı var; kısmen DeepCharts platform tanıtımı.
---

## Piyasa ve periyot
- Piyasa: CME vadelileri; örneklerin tamamı ES (S&P 500 vadelisi).
- Periyot: her periyotta kullanılabilir denir (1:31); şablon ES 5 dk (18:42); composite 90 gün (19:09). Tek doğru periyot kuralı yok.

## Kavram tanımları
| kavram | videodaki tanım |
|---|---|
| Volume profile | her fiyat seviyesinde gerçekleşen işlem dağılımı (1:12–1:25) |
| HVN | çok hacimli seviye; iki taraf aktif (2:08) |
| LVN | vadi; tek taraf sert baskın, "yönlü sprint" (3:03–3:25) |
| Değer alanı | normal dağılımın 1. standart sapması (%68) → %70'e yuvarlanır (6:41–7:24) |
| İçi / dışı | içi = adil değer; dışı = anomali, ortalamaya dönebilir (6:36–7:38) |
| VWAP | seansın hacim ağırlıklı ortalaması; gelişen VWAP da kullanılır (15:33) |
| Delta profili | her seviyede (alış − satış) net baskı (14:09–14:28) |
POC (22:25): tek seviye olarak bakılmamalı; komşu seviyelerin hacmi neredeyse eşit, POC'nin yeri algoritmik aktiviteyle rastgele olabilir — HVN bölgesi önemli.

## Giriş koşulu ve yön
**Setup A — aralık / dönüş (7:44):** fiyat değer alanı dışına çıkar → tepeleri sat, dipleri al. Özel biçim: başarısız açık artırma
(kırılım başarısız olup değer alanına geri döner, giriş orada, 8:32).
**Setup B — trend / kırılım (8:57):** yeni hacim dağılımının öncekinin ÜSTÜNDE (altında) oluşması = hacim kütlesinin taşınması trendi
niteler; yalnız tepe/dip kırılımına bakmak sahte sinyal üretir (9:17–9:40). Giriş kırılımda ya da dışarıda bir süre kaldıktan sonra
geri testte (9:45–9:57).
**Üç katman (17:07):** (1) bias: hacim yukarı kayıyorsa trend yukarı; (2) destek-direnç: önceki seansın değer alanı ve POC bölgesi —
trend yukarıysa dağılımın altında aşağı başarısız olup geri girişte trend yönünde, hedef değer alanının diğer tarafı (18:01);
(3) tetik: mum içi hacim profili / order flow ile emilim (absorption) ya da inisiyatif (19:34–22:24).

## Stop, hedef, çıkış
| setup | stop | hedef |
|---|---|---|
| aralık / başarısız açık artırma | kırılım dibinin altı (8:38) | dağılımın diğer tarafı; muhafazakâr: POC/HVN (8:43) |
| trend / kırılım | ana HVN'nin altı (9:57) | belirtilmemiş |
| tetik örneği (21:10) | tepenin üstü | ortalamaya dönüş seviyesi |
| açılış aralığı kırılımı (21:55) | kırılımın hemen altı | seans boyu, 1:3 R/R |
Sabit R kuralı yok; zaman çıkışı, iz süren stop, pozisyon büyüklüğü: belirtilmemiş.

## Günde kaç işlem
Belirtilmemiş.

## Filtreler
- Seans filtresi (16:11–17:04): profil RTH (normal seans) üzerinden kurulmalı; ETH ayrı profil. (XU30 karşılığı: yalnız gündüz seansı.)
- Saat / hacim / oynaklık eşiği: belirtilmemiş (bir örnekte açılış aralığı geçiyor, kural değil).

## Gerekli veri
- GERÇEK borsa hacmi vurgulanıyor (10:35–13:00): TradingView session profili tick hacmine dayanıyor; aynı seansta POC ~69,99 vs 69,87
  gibi birkaç puan fark, değer alanı sınırları da kayıyor (12:18).
- Katmanlar: 90 gün composite (uzun bias) + günlük seans profili + mum içi profil (tetik).
- Önceki gün profili: evet, destek-direnç olarak (13:04, 18:01) → COK_SEANS.
- Delta profili ve mum içi order flow aktif bileşen. Mum içi profil M1 altı çözünürlük ister (elimizde M1 + bar başı alış/satış hacmi).

## Kanıt
Backtest, dönem, maliyet, isabet oranı: yok ("very decent / really high win rate", rakamsız). Tek sayısal R/R bir örnekte 1:3.
Sunucu geriye dönük örnek seçmenin (cherry pick) mümkün olduğunu açıkça kabul ediyor (23:19). Kanıt düzeyi: ORNEK.

## Videodaki örnekler
| zaman | örnek |
|---|---|
| 2:08 | HVN / LVN işaretleme |
| 3:27 | hacim dağılımı → fiyat aksiyonu şeması |
| 7:11 | %68 / %95 / %99,7 ve %70'e yuvarlama |
| 8:32 | başarısız açık artırma: alım, stop altta, hedef karşı taraf ya da POC |
| 9:01 | trend niteleme: dağılımın tamamının yukarı kayması |
| 11:51 / 12:18 | tick hacmi profili vs gerçek hacim profili; POC farkı |
| 13:52 | delta profili: tepede büyük satış, aşağıda agresif alım kümesi |
| 15:33 | VWAP / gelişen VWAP |
| 16:11 | RTH / ETH profil ayrımı |
| 19:09 | 90 günlük composite |
| 19:51 | mum içi profil: emilim, değer alanı kayması, yutan mum + hacim teyidi |
| 21:16 | altta açılış → üst banda gidiş → başarısız açık artırma → ortalamaya dönüş → açılış aralığı kırılımı, 1:3 |
| 22:25 | POC ile komşu seviyelerin hacminin neredeyse eşit olduğu grafik |

## Döküm hazırlayanın uyarıları
- Tick hacmi vs gerçek hacim: profil hangi hacimle kuruluyorsa POC/VAH/VAL ona göre kayar.
- POC konusunda karşıt duruşlar: Data Trader POC'yi birincil giriş yapıyor; bu video (ve Drysdale) POC'nin tek seviye olarak rastgele
  olabileceğini söylüyor — XU30'da POC kararlılığı ölçülebilir bir soru.
- Row size çelişkisi (Data Trader 60, Drysdale 300); hiçbirinde dayanak yok.
- Üç videonun hiçbirinde backtest yok.
