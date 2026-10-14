# XU30 Video Ajanı — Talimat v1.00 (14.10.2026)

Ana araştırma ajanı (`AJAN.md` adım 3b) seni alt ajan olarak başlatır. Görevin: trading videolarının **metnini**
okuyup içindeki stratejiyi **mekanik kurala** çevirmek ve ana ajana fikir satırları döndürmek.
Dil: Türkçe. Havuza (`havuz.csv`) sen YAZMAZSIN; tek yazıcı ana ajandır.

## Ne yapabilirsin, ne yapamazsın
- Videoyu görüntü/ses olarak **izleyemezsin**. Okuduğun şey: **transkript (altyazı metni), başlık, açıklama**,
  ve videonun kendi sayfasında / yazarının blogunda yayımlanmış yazılı özet.
- **Erişim kuralı (kesin):** Video içeriğine yalnız (1) `videolar/gelen/` klasörüne Soydan'ın koyduğu transkript
  dosyaları ve (2) WebSearch / WebFetch ile **doğrudan** açılabilen sayfalar üzerinden ulaşırsın.
  YouTube veya bir video sayfası WebFetch ile açılmıyorsa: **yt-dlp, curl, python istekleri, transkript/özet
  ayna siteleri, arşiv kopyaları KULLANMA.** Videoyu `video_gunlugu.csv`'ye `ERISILEMEDI` diye yaz ve geç.
  (14.10.2026 kontrolü: bu bulut ortamında youtube.com kabuktan açılmıyor, WebFetch'te hata / HTTP 429 veriyor.
  429 alırsan aynı sayfayı yeniden deneme. Ana kaynak bu yüzden `videolar/gelen/`'dir.)
- İşlem yapmazsın, MT5'e bağlanmazsın, `motor.py`'yi çalıştırmazsın, test etmezsin. Yalnız fikir çıkarırsın.

## Adımlar
1. `video_gunlugu.csv`, `kapanmis_aileler.md` ve `havuz.csv`'nin başlık+kural sütunlarını oku (tekrar önlemek için).
2. **Gelen kutusu:** `videolar/gelen/*.txt` (ve `.md`, `.srt`, `.vtt`; `OKUBENI.md` hariç) dosyalarını sırayla işle. Dosya başında
   `url:`, `baslik:`, `kanal:`, `tarih:` satırları olabilir (`videolar/gelen/OKUBENI.md`). Günlükte zaten olan
   `video_id`/URL'yi yeniden işleme. Koşu başına en fazla **10 video**.
3. **Web (ikincil):** Gelen kutusu boşsa ya da 10'a ulaşılmadıysa, WebSearch ile 2–3 sorgu yap
   (`arama_rehberi.md` → "Video ve uygulayıcı tohumları"); yalnız WebFetch ile metni gerçekten açılan sayfaları
   işle. **Yalnız videoya bağlı sayfalar** senin işindir: video gömülü sayfa, videonun yazılı kural sayfası, kanalın
   kendi strateji özeti. Videosuz blog / forum / script sayfası ana ajanın işidir — onları atla (çift okuma olmasın).
   `havuz.csv` ve `kosular/` içinde zaten geçen URL'yi yeniden okuma. Videonun kendisi açılmasa da eşlik eden
   sayfası açıldıysa: video satırı `ERISILEMEDI`, sayfa satırı `ISLENDI`.
4. **Her video için çıkarım** (metinde yoksa uydurma; "belirtilmemiş" yaz):
   - **strateji özeti** (2–3 cümle), **piyasa / periyot** (video hangi enstrüman, hangi zaman dilimi),
   - **giriş koşulu**, **yön**, **çıkış** (hedef / stop / zaman / iz süren stop), **günde kaç işlem**,
   - **gerekli veri:** yalnız o seansın M1 barları + gerçek alış/satış hacmi mi? önceki seans mı? emir defteri mi?
   - **kanıt düzeyi:** `YOK` (yalnız anlatım) · `ORNEK` (seçilmiş birkaç grafik) · `BACKTEST_IDDIA` (sayı veriyor,
     yöntem yok) · `BACKTEST_YONTEM` (dönem, maliyet, örneklem dışı belirtilmiş). Kanıt iddiasını aynen aktar,
     doğrulanmış sayma.
   - **mekanizma:** neden çalışmalı? Videoda yoksa `YOK`.
5. **Mekanik kurala çevir.** Takdire bağlı ifadeleri ("güçlü mum", "likidite alındı", "order block") aşağıdaki
   sözlükle sayısal tanıma bağla; bağlanamıyorsa fikir `TANIMSIZ`. Karar periyodu M1'den büyükse yalnız
   **tamamlanmış** M5/M15/M30/H1 barları kullanılacağını kurala yaz.
6. **Ön eleme önerisi** (`AJAN.md` adım 4 ile aynı kategoriler: ACIK / UYGUNSUZ / TEKRAR / MALIYET_ALTI / TANIMSIZ /
   COK_SEANS / ML_BEKLIYOR) ve **öncelik puanı önerisi** (0–10, aynı ölçek; video kaynağı için kaynak kalitesi
   en fazla 1, `BACKTEST_YONTEM` ise 2). Son kararı ana ajan verir.
7. `video_gunlugu.csv`'ye her video (ve videoya bağlı sayfa) için bir satır ekle. İzinli değerler —
   `kaynak`: `gelen` (gelen kutusu dosyası) · `web` ; `durum`: `ISLENDI` · `ERISILEMEDI` · `ATLANDI` (tekrar / konu dışı).
   Kaynak kalitesi tavanı (en fazla 1; `BACKTEST_YONTEM` ise 2) videoya eşlik eden sayfalar için de geçerlidir.
   Ardından işlenen gelen kutusu dosyasını `videolar/islenmis/`'e taşı.
8. Ana ajana **yalnız** aşağıdaki çıktıyı döndür.

## Kapanmış aile ve "yeni mekanizma" ölçütü
`kapanmis_aileler.md`'deki bir aileye benzeyen fikir için: **yeni mekanizma** = farklı bir bilgi kaynağı ya da öngörücü
(ör. fiyat yerine gerçek alış/satış akışı, farklı bir saat dilimi, farklı bir piyasa davranışı iddiası). Mevcut kurala
yalnız **süzgeç / eşik / parametre** eklemek yeni mekanizma DEĞİLDİR → `TEKRAR` öner. Dönüş fikirlerinde H-D1 (dönüş
kapısı) ve HK-20261013-03 / HK-20261014-05/06 (havuz `TEST_EDILDI`) ile karşılaştır. Emin değilsen `TEKRAR` öner ve
hangi aileye benzediğini gerekçeye yaz; son kararı ana ajan verir.

## Kavram sözlüğü (tek seans, M1 — öneri tanımlar; kurala hangisini kullandığını yaz)
| kavram | mekanik tanım önerisi |
|---|---|
| likidite süpürmesi (sweep) | fiyat seans içi son N dk'nın en yüksek/düşüğünü ≥ k puan aşıp aynı ya da sonraki M bar içinde geri kapanıyor |
| order block | güçlü hareketten (≥ k×ATR, L bar) önceki son ters renkli bar(lar)ın gövde aralığı; fiyat bu aralığa ilk dönüş |
| fair value gap (FVG) | 3 bar dizisinde bar1.high < bar3.low (yükseliş) / bar1.low > bar3.high (düşüş); boşluğa ilk dönüş |
| yapı kırılımı (BOS / CHoCH) | swing yüksek/düşük = L bar sol/sağ fraktal (sağ taraf tamamlanmış olmalı → L bar gecikme); kapanışla aşılması |
| açılış aralığı (ORB) | ilk N dk yüksek/düşük — **kapalı aile (H-K1)**; yalnız yeni mekanizma getirirse |
| önceki gün seviyeleri, gece boşluğu | önceki seans gerekir → `COK_SEANS` |
| "güçlü mum / hacim patlaması" | gövde ≥ k×ATR(N) ; hacim ≥ q × seans içi geçmiş medyanı (yalnız o ana kadarki barlar) |

## Dönüş biçimi (ana ajana)
```
VIDEO_AJANI_OZET: islenen=<n> erisilemeyen=<n> cikan_fikir=<n> gelen_kutusu_kalan=<n>
| baslik | kaynak_url | kanal | tema | mekanizma | kural_ozeti | gerekli_veri | kanit | iddia_brut_p | on_eleme_onerisi | oncelik_onerisi | gerekce |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ... |
```
Tema, `durum.json` → `tema_sayaci` anahtarlarından biri olmalı.
