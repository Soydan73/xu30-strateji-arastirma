# Video gelen kutusu

Video ajanı YouTube'u bu ortamdan doğrudan açamıyor. İncelenmesini istediğin videoların **transkriptini** buraya koy;
her koşuda en fazla 10 video işlenir ve işlenen dosya `videolar/islenmis/`'e taşınır.

## Transkript nasıl alınır (YouTube, tarayıcıdan, ~30 sn)
1. Videonun altında "...daha fazla" → **"Transkripti göster"**.
2. Açılan paneldeki metni seç, kopyala.
3. Bu klasöre `.txt` dosyası olarak kaydet (dosya adı serbest, ör. `2026-10-15_vwap-pullback.txt`).

Altyazı dosyası (`.srt` / `.vtt`) da olur.

## Dosya başı (isteğe bağlı ama önerilir)
```
url: https://www.youtube.com/watch?v=XXXXXXXXXXX
baslik: Videonun başlığı
kanal: Kanal adı
tarih: 2026-10-15
not: neden ilgini çekti (isteğe bağlı)
---
(transkript metni)
```
Yalnız URL listesi koymak işe yaramaz — ajan videoyu açamaz, metne ihtiyacı var.
