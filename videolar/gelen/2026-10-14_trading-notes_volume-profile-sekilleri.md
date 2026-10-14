url: https://www.youtube.com/watch?v=XMNUAJvReg0
baslik: NEVER Read Price Again – Volume Profile is 10x Better!
kanal: Trading Notes
tarih: 2026-05-01
sure: 13:31
kaynak: Chrome'daki Claude kural dökümü (youtube-transcriber ile transkript okunarak; birebir metin değil)
not: Soydan'ın seçtiği video (14.10.2026). Sponsorlar: Flux Charts, Phemex, TradingView.
---

## Piyasa ve periyot
- Piyasa / periyot: belirtilmemiş ("her piyasa, her zaman dilimi", 1:10). Yalnız bonus kuralda günlük RTH seansı.
- Araç: TradingView Anchored Volume Profile; ayar: VAH/VAL/POC açık, satır sayısı 400 (varsayılan 24 "işe yaramaz", 4:42–5:06).

## Kavram tanımları
| kavram | videodaki tanım |
|---|---|
| Senaryo 1 — sağlıklı hareket | büyük mum + yüksek hacim; devam beklenir (1:50) |
| Senaryo 2 — emilim | küçük mum + devasa hacim; büyük taraf karşı akışı emiyor, sonra sert ters hareket (2:02) |
| Senaryo 3 — arz yokluğu | düşük hacimde hareket; karşı taraf yok (2:33) |
| Renk uyarısı | hacim çubuğu rengi mum rengini izler; alış/satış ayrımı değildir (2:46–3:11) |
| Hacim uyumsuzluğu | fiyat yeni tepe + hacim küçülüyor = uyarı; düşen fiyat + azalan hacim = satıcı tükeniyor (3:11) |
| POC | en çok hacimli seviye; fiyat ona dönme eğiliminde (5:17) |
| Değer alanı | aktivitenin ~%70'i (5:30) |
| LVN | neredeyse işlem olmayan seviyeler, "hızlı şerit" (5:44) |
| Çekirdek ilke | yüksek hacim = yapışkan fiyat, düşük hacim = fiyat yırtılır (5:58) |

## Dört profil şekli (7:37–9:39)
| şekil | görünüm | yorum | işlem |
|---|---|---|---|
| D | ortada yoğun, kenarlarda ince | denge | uçları fade et; hedef ortadaki POC |
| P | üstte yoğun, altta ince kuyruk | boğa | POC'ye ya da kuyruktaki düşük hacim tümseğine geri çekilmede uzun. **Gün, aralığının %50'sinin ÜSTÜNDE kapanmalı** — yoksa gerçek P değil |
| B | altta yoğun, üstte ince kuyruk | ayı | POC'ye ya da üstteki düşük hacim tümseğine sıçramada kısa. **Gün, aralığının %50'sinin ALTINDA kapanmalı** |
| İnce | merkezi yoğunluk yok, geniş ince sütun | patlayıcı, genelde haber kaynaklı trend | karşı koyma; profil içindeki küçük hacim kümeleri geri çekilmede destek |
(D/P/B şekilleri Steidlmayer Market Profile literatüründen; videoda kaynak verilmemiş.)

## Ana örnek (10:56–12:20)
Büyük HVN → makro olayla sert satış → fiyat alttaki düşük hacim alanını süpürüp HVN kümesinin kenarına değer (tetik bölgesi).
Sinyal mumu: kenarda, bir önceki muma göre daha yüksek hacimli doji / çekiç / kayan yıldız; mum tam kapanmalı (önden girme yok).
Kapanış + hacim artışı teyidi → uzun. Stop: node'un hemen altı (12:06). Hedef: profilin karşı kenarı (12:12).
Profil penceresi / çapa noktası: TANIMSIZ (anchored araçta çapa sonucu belirler).

## Bonus kural (12:20–13:22)
Fiyat önceki seansın (dünün RTH) değer alanı DIŞINDA açılır ve sonra İÇİNE geri girerse, büyük olasılıkla değer alanının karşı ucuna gider.
Kabul şartı: yalnız fitil yetmez, değer alanı içinde gerçek mum kapanışları gerekir; dokunup hemen reddediyorsa geçersiz.
Hedef: dünkü değer alanının karşı ucu. Stop: belirtilmemiş. ("Her seferinde isabet eder" → hemen "ezici çoğunlukla" diye geri alınıyor; rakam yok.)

## Stop, hedef, çıkış
| | stop | hedef |
|---|---|---|
| ana örnek | node'un hemen altı | profilin karşı kenarı |
| D şekli | belirtilmemiş | POC |
| P / B / ince | belirtilmemiş | belirtilmemiş |
| bonus kural | belirtilmemiş | değer alanının karşı ucu |
R/R, iz süren stop, zaman çıkışı, pozisyon büyüklüğü, günde işlem sayısı: belirtilmemiş.

## Filtreler
- P/B için %50 kapanış kuralı (en net sayısal filtre) — gün kapanışını gerektirdiği için yalnız ertesi gün için bilgi verir.
- Bonus kural kabul filtresi: değer alanı içinde mum kapanışı.
- Sinyal mumu: bir önceki muma göre daha yüksek hacim.
- Saat / oynaklık: belirtilmemiş.

## Gerekli veri
- Bonus kural: önceki günün RTH profili (çok seans). Ana model: profil penceresi tanımsız. Emir defteri gerekmiyor.
- Gerçek hacim / tick hacmi ayrımı konuşulmamış.

## Kanıt
Backtest, dönem, maliyet, isabet, kâr iddiası: yok. Tek işlem örneği (kazançlı). Sabitlenmiş yorumda "her şeyi backtest edin" deniyor,
videoda test yok. Kanıt düzeyi: ORNEK.

## Döküm hazırlayanın uyarıları
- Hacim "kaç kişi" değil, kontrat sayısıdır; tek büyük oyuncu devasa hacim yaratabilir (ayırmak için işlem adedi gerekir).
- Satır sayısı dördüncü farklı değer: 60 (Data Trader), 300 (Drysdale), 400 (bu video); hiçbirinin dayanağı yok.
- Ana modelde profil penceresi tanımsız → kodlanamaz; bonus kural test edilmeye değer ama isabet iddiası rakamsız.
