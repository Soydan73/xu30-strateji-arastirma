url: https://www.youtube.com/watch?v=FTAfj2g4bHM
baslik: The Only 4 Volume Profile Settings I Use (TradingView Walkthrough)
kanal: Trader Drysdale (Chris Drysdale)
tarih: 2026-08-22
sure: 11:55
kaynak: Chrome'daki Claude kural dökümü (youtube-transcriber ile transkript okunarak; birebir metin değil)
not: Soydan'ın seçtiği video (14.10.2026). Ağırlıklı AYAR videosu; giriş/çıkış kuralları yüzeysel.
---

## Piyasa ve periyot
- Piyasa: CME endeks vadelileri (NQ, MNQ, ES, YM, 6:45); altın/petrol/döviz yalnız saat sorunu bağlamında (7:41).
- Periyot: ana çalışma periyodu belirtilmemiş; composite anlatımında 30 dk grafik (8:18). Platform: TradingView.

## Kavram tanımları
| kavram | videodaki tanım |
|---|---|
| Volume profile | her fiyat seviyesinde ne kadar iş yapıldığı (0:56) |
| HVN | çok kontrat el değiştirmiş bölge; fiyat sıkışır, rotasyon yapar (1:46, 2:50) |
| LVN | az iş yapılmış seviye; fiyat reddetmiş ya da tek taraf baskın geçmiş; kırılırsa hızlı hareket (2:19–3:08) |
| POC | seansta en çok hacmin işlem gördüğü seviye (3:28) |
| VAH / VAL | seans hacminin %70'ini içeren aralığın sınırları (3:37) |
| Değer alanı içi / dışı | içi = adil değer, dengeli; dışı = istatistiksel anomali, "the stretch" (3:49) |
Uyarı (4:04–4:32): POC'nin tam fiyatına bağlanma; platform/veriye göre birkaç tik kayabilir — "bölge, kesinlikten önemli".

## Ayarlar (videonun ana konusu)
| # | ayar | değer | gerekçe |
|---|---|---|---|
| 1 | Value area | %70 | %68 denendi, seviyeler neredeyse oynamıyor (4:41, 11:10) |
| 2 | Volume type | Total | up/down/delta gereksiz bulunuyor (5:02) |
| 3 | Row size | 300 (maksimuma yakın) | az satır = kaba blok; 20 ile gösteriliyor (6:01) |
| 4 | Seans başlangıcı | 08:30 (CME endeks vadelileri) | TradingView'de 9:30 girilince profil 10:30'a kayıyor (6:33–7:40) |

## Session vs composite (7:56)
- Session profili: her gün sıfırlanır, yalnız bugünün işi; gün içi seviyeler için.
- Composite: fixed range ile 2–3 gün ya da 20 gün; sabit sayı yok, "o an önemli fiyat aralığı" (8:51).

## Giriş koşulu ve yön (9:19) — genel yaklaşım düzeyinde
- Fiyat HVN içindeyse: rotasyon beklenir; bölge kenarları fade edilir (tepeden kısa, dipten uzun, 9:37).
- Fiyat LVN'yi kırarsa: hız beklenir; fade edilmez, hareket yönünde gidilir — "kırar, geri test eder, tutunur" (9:58).
- Tetik, mum onayı, kesin giriş kuralı: belirtilmemiş.

## Stop, hedef, çıkış
Hiçbiri belirtilmemiş (yalnız "riskinizi yönetin", 11:49).

## Günde kaç işlem / filtreler
Belirtilmemiş. 08:30 bir işlem filtresi değil, profil kurulum ayarı.

## Gerekli veri
- Gün içi: o günün session profili (tek seans) — bağlam için değişken uzunlukta composite (çok seans).
- Önceki gün profili kural olarak geçmiyor. Delta seçeneği bilinçli olarak kullanılmıyor; emir defteri gerekmiyor.
- Ekranda: değer alanı + POC bölgesi + fiyata yakın 2–3 LVN; 12–15 çizgi en sık hata (10:11).

## Kanıt
Backtest, dönem, maliyet, isabet, kâr iddiası: yok. Tek işlem örneği bile gösterilmiyor. Kanıt düzeyi: YOK.

## Videodaki örnekler
| zaman | örnek |
|---|---|
| 4:46 | value area %70 → %68, seviyeler neredeyse sabit |
| 6:21 | row size 20 → 300 |
| 7:00 | 9:30 girişinde profilin 10:30'a kayması |
| 8:18 | 30 dk grafikte composite (2–3 gün, 20 gün) |
| 9:21 | HVN rotasyon / kenar fade şeması |
| 9:40 | LVN kırılımı ve hızlı hareket şeması |

## Döküm hazırlayanın uyarıları
- "CME tuhaflığı" büyük olasılıkla saat dilimi uyuşmazlığı (08:30 CT = 09:30 ET); doğru çözüm seans saat dilimini grafikle eşitlemek.
  XU30'da da seans–saat dilimi eşleşmesi kontrol edilmeli.
- Row size çelişkisi: bu video 300, Data Trader 60; ikisi de test sunmuyor. Row size POC yerini oynatır — XU30'da POC kararlılığı ölçülerek seçilmeli.
- Bu videodan tam işlem sistemi çıkmaz (stop/hedef yok); ayar reçetesi olarak faydalı.
