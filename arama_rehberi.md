# Arama rehberi (başlangıç listesi, 14.10.2026)

Bu liste bir **başlangıç noktasıdır**, sınır değildir. Ajan her koşuda en az **2 yeni sorgu** (listede ve
`arama_gunlugu.csv`'de olmayan) üretmek zorundadır. İşe yarayan yeni anahtar kelimeleri bu dosyanın
"Ajanın eklediği" bölümüne ekler.

## Kaynaklar (öncelik sırasıyla)

| Tür | Site / arama kalıbı | Not |
|---|---|---|
| Akademik ML | `site:arxiv.org q-fin.TR`, `site:arxiv.org cs.LG trading`, `site:paperswithcode.com`, `site:openreview.net`, Journal of Financial Data Science, Quantitative Finance (dergi) | Yöntem bölümünü oku: hangi veri, hangi bölme, maliyet var mı |
| Quant derleme | `site:hudsonthames.org`, `site:quantstart.com`, `site:quantinsti.com/blog`, `site:paperswithbacktest.com`, López de Prado çalışmaları | ML + finans yöntem tuzakları (sızıntı, meta-etiketleme) |
| Akademik | `site:ssrn.com`, `site:arxiv.org q-fin`, `site:ideas.repec.org`, `site:sciencedirect.com` | Özet çoğu zaman açık, tam metin bazen ücretli |
| Akademik (TR) | `site:dergipark.org.tr`, `site:tez.yok.gov.tr`, üniversite açık arşivleri (`openaccess`, `polen.itu.edu.tr`) | BIST / VİOP üzerine yerel çalışmalar |
| Strateji derlemeleri | `site:quantpedia.com`, `site:alphaarchitect.com`, `site:quantocracy.com`, `site:robotwealth.com`, `site:qoppac.blogspot.com` | Kaynağa atıf verirler; asıl makaleyi izle |
| MQL5 | `site:mql5.com/en/articles`, `site:mql5.com/en/code`, `site:mql5.com/tr/articles` | Uygulama ayrıntısı; iddiaları şüpheyle oku |
| Forum | `site:elitetrader.com`, `site:reddit.com/r/algotrading`, `site:reddit.com/r/quant`, `site:forexfactory.com`, `site:nuclearphynance.com` | Fikir kaynağı; sonuç iddiası kanıt sayılmaz |
| Forum (TR) | `site:borsagundem.com`, `site:eksisozluk.com viop`, `"VİOP" "endeks vadeli" strateji` | Yerel pratik, seans alışkanlıkları |
| Uygulayıcı — script | `site:tradingview.com/script` (açık kaynak, "strategy" etiketli), `site:mql5.com/en/code`, `site:github.com` + "backtest" + enstrüman | Kod = kesin kural; açıklamadaki performans iddiası kanıt değildir |
| Uygulayıcı — derleme / blog | `site:quantpedia.com` (ücretsiz strateji sayfaları), `site:substack.com` quant blogları, `site:priceactionlab.com`, `site:quantifiedstrategies.com`, `site:marketcalls.in`, `site:systemtradersuccess.com`, `site:tradingmarkets.com` | Çoğu backtest'i maliyetsiz / ABD hissesi; kuralı al, sonucu alma |
| Uygulayıcı — forum (genişletilmiş) | `site:nexusfi.com` (futures.io), `site:tradingqna.com`, `site:quant.stackexchange.com`, `site:reddit.com/r/Daytrading`, `site:reddit.com/r/FuturesTrading` | Endeks vadeli gün içi pratiği yoğun |
| Video | Video ajanı (`VIDEO_AJANI.md`): `videolar/gelen/` transkriptleri; web'de yalnız WebFetch ile açılan yazılı sayfalar | youtube.com bu ortamda açılmıyor (14.10.2026); dolanma yolu kullanılmaz |
| Kitap özeti | yazarı belli kitap özetleri (ör. Crabel, Fisher ACD, Dalton Market Profile, Chan, Carver) | Mekanizma kaynağı; tam metin gerekmez |
| Borsa / düzenleyici | `site:borsaistanbul.com`, `site:spk.gov.tr` | Seans saatleri, kontrat özellikleri, piyasa yapıcı kuralları |

## Tema → sorgu tohumları

| Tema | İngilizce | Türkçe |
|---|---|---|
| acilis_ilk_saat | opening range breakout futures intraday, opening auction imbalance index futures, first hour return predictability | açılış aralığı kırılımı vadeli, VİOP açılış seansı, gap kapanma endeks |
| gun_ici_mevsimsellik | intraday seasonality index futures half-hour returns, time-of-day effect emerging market futures | gün içi saat etkisi borsa istanbul, seans içi getiri deseni |
| akis_dengesizligi_delta | order flow imbalance predict returns futures, signed volume trade imbalance intraday, VPIN futures | alış satış dengesizliği, gerçek hacim delta vadeli |
| hacim_profili_vwap | VWAP deviation mean reversion intraday futures, volume profile POC value area strategy, anchored VWAP | VWAP sapması strateji, hacim profili POC |
| oynaklik_rejimi | volatility regime conditional intraday momentum, realized volatility filter trading rule, range compression breakout | oynaklık rejimi filtre, dar bant kırılım |
| kisa_ufuk_ortalamaya_donus | short-term reversal intraday futures, overreaction minutes mean reversion, liquidity provision returns | kısa vadeli dönüş, aşırı tepki geri dönüş |
| seans_sonu_akisi | end of day price pressure futures, closing auction imbalance, last half hour momentum, market on close flow | seans sonu fiyat baskısı, kapanış seansı |
| vade_sonu_devir | futures roll period returns, expiration day effect index futures, calendar spread roll pressure | vade sonu etkisi VİOP, vade geçişi fiyat hareketi |
| intraday_momentum_literaturu | market intraday momentum, gamma hedging intraday momentum, time-series momentum intraday | gün içi momentum borsa istanbul |
| **yapay_zeka_ml** (ÖNCELİKLİ) | machine learning intraday futures prediction, gradient boosting order flow features, LSTM transformer limit order book mid-price, deep learning index futures intraday, reinforcement learning trading agent futures, meta-labeling triple barrier, LLM agents trading strategy generation, feature importance intraday returns | yapay zeka borsa tahmini, makine öğrenmesi BIST 30, derin öğrenme VİOP |
| *Video ve uygulayıcı tohumları* (tema değil; bulunan fikir kendi temasına yazılır) | "futures day trading strategy rules" + VWAP / opening drive / initial balance / liquidity sweep / fair value gap / order block / market profile / delta divergence; "NQ ES scalping strategy backtest" | VİOP strateji, BIST 30 vadeli gün içi strateji, viop scalping, endeks vadeli al sat stratejisi |
| **quant_istatistik_modeller** | Hurst exponent regime intraday, entropy predictability returns, Kalman filter trend futures, fractional differentiation, change-point detection volatility, Ornstein-Uhlenbeck intraday, realized variance jump detection | Hurst üssü borsa, entropi öngörülebilirlik, Kalman filtresi trend |
| diger | emerging market index futures anomaly, BIST 30 futures strategy, Turkish derivatives market microstructure | BIST 30 vadeli anomali, VİOP mikro yapı |

## Öncelikler (kullanıcı kararı, 14.10.2026)
1. **Yapay zekâ / ML tabanlı fikirler:** her koşunun temalarından biri `yapay_zeka_ml` olur.
2. **Akademik yayınlar:** okunan kaynakların **en az %30'u** akademik (hakemli dergi, SSRN, arXiv, tez).
   *(14.10.2026 güncellemesi: önceki oran %50 idi; Soydan kararıyla kaynak tabanı genişletildi.)*
2b. **Uygulayıcı kaynaklar:** okunan kaynakların **en az %30'u** uygulayıcı (TradingView / mql5 kodu, Quantpedia,
   blog, forum, video transkripti). Her koşuda en az 3 sorgu bu kaynaklara. Video ajanı her koşuda çalışır.
2c. **Önceki seans isteyen fikirler** `COK_SEANS` olarak puanlanıp saklanır (UYGUNSUZ değil) — motor genişletilirse ilk bunlar taranır.
3. **Quant analiz:** `quant_istatistik_modeller` teması her 2 koşudan birinde seçilir.

**ML kaynaklarını okurken zorunlu kontrol:** (a) bölme zamansal mı, yoksa rastgele mi (rastgele bölme =
sızıntı şüphesi); (b) işlem maliyeti dahil mi; (c) örneklem dışı süre ne kadar; (d) kaç model / hiperparametre
denendi. Bu dördünü havuz satırının `gerekce` alanına yaz. Doğruluk (accuracy) iddiası kâr kanıtı değildir.

## Sorgu kuralları
- Her koşuda en az bir sorgu **Türkçe**, en az bir sorgu **yeni** olsun.
- Sorgu sıfır işe yarar sonuç verirse günlüğe `0` yaz; aynı sorgu 30 gün içinde tekrar denenmez.
- İyi bir makalede: "references" bölümündeki 2–3 çalışmayı ve "cited by" ile sonraki çalışmaları ara.
- Ücretli sayfada özet + yöntem bölümü yeterliyse kart yazılabilir; değilse `TANIMSIZ` (gerekçe: tam metin yok).

## Ajanın eklediği
- 13.10.2026 (`quant_istatistik_modeller`): "variance ratio intraday autocorrelation regime switch" → Bianco-Corsi-Renò gün içi LeBaron, Mehlitz-Auer bellek momentumu (3 işe yarar)
- 13.10.2026 (`akis_dengesizligi_delta`): "order flow entropy" / "hidden order in trades" → bilgi kuramsal akış ölçüleri (arXiv 2512.15720)
- 13.10.2026 (`oynaklik_rejimi`): "filter trading rule realized volatility index futures" → Hang Seng filtre kuralı literatürü
- Verimsiz (tekrarlama): "NR7 range contraction", "Kaufman efficiency ratio" (yalnız gösterge sayfaları); TR "oynaklık rejimi VİOP" (yalnız aracı kurum bültenleri)
- 14.10.2026 (`kisa_ufuk_ortalamaya_donus`): "drift burst" / "locally explosive trends" / "flash crash reversal futures" → Christensen-Oomen-Renò (vadeli tik verisi, dönüş ~2/3)
- 14.10.2026 (`kisa_ufuk_ortalamaya_donus`): "century of market reversals" / "asymmetric reversal expected volatility" → Bogousslavsky-LeBaron-Pontiff
- Verimsiz (tekrarlama): TR "derin öğrenme VİOP endeks vadeli gün içi" (yalnız bültenler); gün içi mevsimsellik sorguları çoğunlukla kesitsel hisse ya da yalnız oynaklık deseni döndürüyor
- 14.10.2026 (`vade_sonu_devir`): "expiration day effect index futures intraday" + "settlement pinning last hour" → Varşova (endeks vadelisinde etki YOK), HKIMR Asya tipi uzlaşma (dönüş YOK), CSI 300 (hafif). Vade teması literatürde zayıf; XU30'da yılda 6 vade günü → güç sorunu.
- 14.10.2026 (`akis_dengesizligi_delta`): "VPIN order flow toxicity" → Andersen-Bondarenko (BVC eleştirisi; bizde gerçek bayrak var), Bjursell vd.
- Verimsiz (tekrarlama): TR "VİOP vade sonu etkisi ..." ve "site:dergipark.org.tr BIST 30 endeks vadeli vade sonu" (bültenler); "futures roll period price pressure" (emtia endeksi roll'u)
- 14.10.2026 (`seans_sonu_akisi`/`acilis_ilk_saat`): "order imbalance predicts closing return" + "first half an hour order imbalance" → Chu-Qiu FOIB (IJFE), Kang vd. JFM (opsiyon OIB → endeks vadeli); "intraday momentum Taiwan OR KOSPI" → Onishchenko vd. (2.-3. yarım saat), NTU TAIEX tezleri
- 14.10.2026 (`diger`): "market time-series reversal last three hours" → Xiang-Luo-Yu (TEDE 2025) — önceki seans gerekir, motor tek seans
- 14.10.2026 (`yapay_zeka_ml`): "falsification study MNQ" → Mesfin (arXiv 2605.04004 / 2605.11423): tek bar OHLCV sinyallerinin sürtünme sınırı
- Verimsiz (tekrarlama): "opening gap index futures gap fill", "relative volume first hour", TR "Borsa İstanbul açılış gap kapanma", "purged CV LightGBM intraday futures" (bloglar)
