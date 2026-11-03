# motor_cok v1.00 — çok seanslı test motoru (ön kayıt + kabul)

**Tarih:** 03.11.2026 · **Karar:** Soydan (seçenek 3: mevcut motoru bozmadan ayrı motor; kontrol ajanda, akış otomatik,
bildirim yalnız ADAY) · **Durum:** YÜRÜRLÜKTE (kabul testi geçti)

## 1. Neden
`motor.py` sinyal fonksiyonuna tek seans verir. Havuzdaki `COK_SEANS` fikirleri (03.11.2026'da 64; puanı ≥ 2 olan 34)
dünün yükseği/düşüğü/kapanışı, gece boşluğu, önceki değer alanı, N günlük ortalama hacim/oynaklık, önceki günlerin
aynı saat hareketi gibi bilgiler ister ve bu yüzden test edilemiyordu.

## 2. Mimari (değişmezler)
- `motor.py` **değişmedi**. `motor_cok.py` onu `import motor as M` ile kullanır: maliyet, işlem simülasyonu
  (sonraki bar açılışında giriş, stop/hedef aynı barda → STOP, 18:05 zorla kapanış), seans-kümeli `ozet`,
  K1–K7 `kapilar` hepsi `motor.py`'den gelir. Kopya kod yok → iki motor ayrışamaz.
- **KS ortaktır.** `motor_cok` varyantları aynı sayaca eklenir; defterde `gerekce` sonuna `; motor_cok` yazılır.
- Ajan `motor_cok.py`'yi değiştirmez (`motor.py` ile aynı statü).

## 3. Sözleşme
```
sinyal(s, onceki, bilgi, **p) -> np.ndarray (len(s), -1/0/+1)
s      : bugünün gündüz M1 barları; i. bar için yalnız s.iloc[:i+1]
onceki : bugünden önceki seanslar (eskiden yeniye), en fazla `geri` (≤ 60), SALT OKUNUR
bilgi  : gun, devir_bugun, ayni_vade (onceki ile aynı uzunlukta bool), vade_no
```
`motor_cok.kart_calistir_cok(seanslar, sinyal, varyantlar, cikis_fn, max_islem=1, geri=20)` —
çıktı `motor.kart_calistir` ile aynı sütunlar + `motor`. Varyant sözlüğünde `geri` varsa o varyant onu kullanır.

## 4. XU30'a özgü sabit kurallar (motorda, ajana bırakılmaz)
| Konu | Kural |
|---|---|
| Vade geçişi | `XU30_YAKINVADE` sürekli seri, devirde GAP'lı. `ayni_vade[j]` = j. önceki seans bugünkü kontratla aynı vadede mi (vade = tek ayların ilk işlem gününden başlayan iki aylık dönem; `motor.devir_gunleri`). Devir gününde hepsi False. **Fiyat düzeyi** karşılaştırmaları yalnız True olanlardan yapılır (AJAN.md adım 7). |
| Veri boşluğu | Ardışık iki seans arasında > 5 iş günü varsa bağlam o noktada kesilir. 31.10.2025 → 05.05.2026 boşluğunda 05.05.2026'nın `onceki`'si boştur; sonraki günler yalnız boşluk sonrası seansları görür. |
| Akşam seansı | Veride yok. "Dünkü kapanış" = önceki gündüz seansının son barının kapanışı; gece boşluğu akşam seansındaki hareketi de içerir. |
| Gece pozisyonu | Yok. İşlem yalnız gündüz, 18:05'te kapanır (`motor.py`). Önceki seans yalnız BİLGİDİR. |
| Bağlam derinliği | `geri` ≤ 60 seans. Bağlam yetmezse (boş ya da < gereken) sinyal 0 olmalıdır. |
| K7 | Devir günleri `motor.ozet` ile ayrı raporlanmaya devam eder. |

## 5. Genişletilmiş kanarya (K5)
1. **Statik denetim:** sinyal modülünün TAM kaynağında dosya/ağ/küresel erişim kalıbı yok (`read_csv`, `open(`,
   `os.`, `glob`, `pathlib`, `pickle`, `np.load`, `import motor`, `global`, `eval/exec`, `__import__` …).
2. **Gün içi kesim:** `motor.kanarya` aynen (bağlam sabitken bugünün gelecek barları silinir; sinyal değişmemeli).
3. **Bağlam bütünlüğü:** rastgele 40 seansta (a) seans listesi bugünde kesilince (gelecek seanslar yok) sinyal aynı
   olmalı, (b) sinyal çağrısından sonra `onceki` seansların kapanış/hacim toplamları değişmemeli.

**Bilinen sınır:** statik denetim sözcük tabanlıdır; dolambaçlı bir yolu (ör. modül düzeyinde gizlenmiş veri) kaçırabilir.
Bu yüzden AJAN.md sinyal dosyasında modül düzeyinde veri tutmayı yasaklar ve sinyal dosyaları depoda denetlenebilir kalır.
`onceki` değişmezlik testi yalnız `close` ve `volume` toplamlarına bakar.

## 6. Kabul testi (`araclar_motor_cok_testi.py`, 03.11.2026) — TÜMÜ GEÇTİ
| # | Sınama | Sonuç |
|---|---|---|
| 1a | 624 seansın hepsinde `onceki` yalnız geçmiş, ≤ geri, `ayni_vade` uzunluğu doğru | GEÇTİ |
| 1b | 05.05.2026 (boşluk sonrası ilk seans) `onceki` boş | GEÇTİ |
| 1c | ilk seans `onceki` boş | GEÇTİ |
| 1d | devir günü (01.11.2023) tüm `ayni_vade` False | GEÇTİ |
| 1e | devirden sonraki gün yalnız devir günü True | GEÇTİ |
| 1f | `geri` > 60 kırpılır | GEÇTİ |
| 2 | tek seanslı kural (HK-20261103-10, 2 varyant) iki motorda **birebir** aynı n/brüt/net/t/net−5/A/B/devirsiz/K1–K7 | GEÇTİ |
| 3 | sızıntılı kural yakalandı: gelecek bar (gün içi kesim), dosya okuma (statik), `onceki` bozma (bütünlük) | GEÇTİ (3/3) |
| 3 | temiz çok seanslı kural kanaryadan geçer | GEÇTİ |
| 4 | `kart_calistir_cok` uçtan uca, 2 varyant ~8 sn (P&L değerlendirilmedi, KS'ye eklenmedi) | GEÇTİ |

Kabul testi yalnız mekaniği sınar; hiçbir çok seanslı hipotezin sonucuna bakılmadı (veri gözetleme yok, KS 351 değişmedi).

## 7. Ajan akışına etkisi (AJAN.md v1.03)
- `COK_SEANS` artık "test edilemez" değil, "motor_cok ile test edilir" demektir.
- Kuyrukta puanı ≥ 2 fikir kaldıkça her koşunun kartlarından biri kuyruğun en yüksek puanlısıdır. Test bütçesi
  değişmedi (2 kart / 12 varyant).
- Bildirim yalnız ADAY'da.
