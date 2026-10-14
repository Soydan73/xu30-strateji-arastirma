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

## Yol B — link ver, Chrome'daki Claude kural dökümü çıkarsın (14.10.2026, güncellendi)
Chrome'daki Claude birebir tam transkripti telif nedeniyle vermiyor; ajanın da birebir metne ihtiyacı yok, **kurala** ihtiyacı var.
Soydan videoyu Chrome'da açar, Chrome'daki Claude'a aşağıdaki isteği yazar, çıkan dökümü Cowork sohbetine yapıştırır;
o sohbetteki Claude dökümü bu klasöre `.md` olarak yazıp push eder. Video ajanı dökümü transkript gibi işler
(`kanit` alanında "Claude döküm, birebir metin değil" notuyla).

İstek şablonu (Chrome'daki Claude'a):
> Bu videodaki işlem stratejisini kendi ifadelerinle, zaman damgalı bir kural dökümü olarak çıkar. Başa url, başlık, kanal,
> yükleme tarihi yaz. Sonra şu başlıkları doldur (videoda yoksa "belirtilmemiş" yaz, uydurma): piyasa ve periyot; kavram
> tanımları (sayısal eşik/pencere neyse aynen); giriş koşulu; yön; stop; hedef; zaman çıkışı / iz süren stop; günde kaç işlem;
> filtreler (saat, hacim, oynaklık); gerekli veri (tek seans mı, önceki gün mü, emir defteri mi); kanıt (backtest var mı,
> dönem, maliyet, isabet/kâr iddiası — aynen); videonun gösterdiği örnekler (dakika:saniye ile). Birebir uzun alıntı yapma.

Yalnız URL listesi koymak (transkriptsiz) işe yaramaz — ajan videoyu açamaz, metne ihtiyacı var.
