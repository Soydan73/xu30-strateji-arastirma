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

## Yol B — link ver, Claude çeksin (14.10.2026, Soydan kararı)
Soydan, **Claude in Chrome bağlı** bir Cowork oturumunda YouTube linklerini verir. O oturumdaki Claude `youtube-transcriber`
eklentisiyle (Soydan'ın kendi Chrome'u, videonun "Transkripti göster" paneli) transkripti çıkarır, yukarıdaki dosya başıyla
(`url / baslik / kanal / tarih / not` + `kaynak: youtube-transcriber (otomatik altyazı)`) bu klasöre `.txt` olarak yazar ve push eder.
Zamanlanmış video ajanı dosyayı her zamanki gibi işler. Not: bulut zamanlanmış koşularında Chrome yoktur; transkript çekme
yalnız bu elle başlatılan oturumlarda yapılır. Otomatik altyazıda sayı/terim hatası olabilir; altyazısı olmayan video atlanır.

Yalnız URL listesi koymak (transkriptsiz) işe yaramaz — ajan videoyu açamaz, metne ihtiyacı var.
