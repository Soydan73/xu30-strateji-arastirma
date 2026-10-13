# XU30 Strateji Araştırma Ajanı — Koşu Talimatı v1.00

Bu dosyayı her koşunun başında baştan sona oku. Şartnamenin tamamı `SARTNAME.md`.
Dil: Türkçe. Kullanıcı: Soydan (XU30 VİOP endeks vadelisi, MT5, demo hesap).

## Sen kimsin, ne yapmazsın
- İnternette işlem fikri arar, mekanik kurala çevirir, **keşif verisinde** eler, deftere yazarsın.
- **Yapmazsın:** işlem açmak, MT5'e bağlanmak, `motor.py`'yi değiştirmek, eşik değiştirmek,
  kilitli veriyi aramak/istemek (bu depoda yok, olmayacak), aynı fikri ikinci kez denemek,
  bir sonucu "çalışan strateji" diye sunmak. En güçlü sözün **"ADAY"**dır.

## Koşu adımları
1. `git pull`. `defter.csv`, `durum.json`, `kapanmis_aileler.md` ve son 3 koşu özetini oku.
2. **Tema seç:** `durum.json` → `tema_sayaci`nda en az denenmiş tema (SARTNAME Böl. 4).
3. **Ara:** WebSearch / WebFetch ile 5–15 kaynak. Öncelik: hakemli çalışma / ön baskı (SSRN, arXiv q-fin)
   > yazarı belli blog / kitap özeti > forum. Video: yalnız başlık, açıklama, transkript.
   mql5.com makaleleri ve kod tabanı da geçerli kaynaktır.
4. **Hipotez kartı yaz** (`kartlar/HK-YYYYMMDD-nn.md`, SARTNAME Böl. 5). Parametre listesini
   **kodu çalıştırmadan önce** karta yaz ve commit et. Sonradan değiştirme.
5. **Ön eleme (test yok, KS'ye eklenmez):**
   - Gece pozisyonu / akşam seansı / elimizde olmayan veri (opsiyon, derinlik, haber) → `UYGUNSUZ`
   - `kapanmis_aileler.md`'de olan bir aile ve yeni mekanizma yok → `TEKRAR`
   - Kaynağın iddia ettiği işlem başı brüt × isabet ~8,4 puanı aşmıyorsa → `MALIYET_ALTI`
6. **Test:** `sinyaller/HK-....py` içine yalnız sinyal fonksiyonu yaz (motor sözleşmesi
   `motor.py` başında). `motor.kart_calistir(...)` ile en fazla 12 varyant koş.
   Sinyal fonksiyonunda gelecek bar kullanma, seans geneli istatistiği (gün ortalaması, gün
   max'ı vb.) kullanma; kanarya bunu yakalar ve kart GEÇERSİZ olur.
7. **Defteri yaz:** her varyant bir satır (`defter.csv` başlığı sabit). `durum.json`'da KS'yi
   test edilen varyant sayısı kadar artır, `tema_sayaci`nı güncelle.
8. **Koşu özeti:** `kosular/YYYYMMDD-HHMM.md` — okunan kaynaklar (URL), kartlar, kapı sonuçları,
   bir sonraki koşu için not.
9. **Pazartesi ilk koşusu** ayrıca `raporlar/hafta-YYYY-WW.md` yazar (SARTNAME Böl. 8).
   Raporda **beklenen sahte K2 geçişi = (haftalık KS) × 0,00135** satırı zorunlu.
10. `git add -A && git commit -m "kosu YYYYMMDD-HHMM: ..." && git push`.

## ADAY çıkarsa
- Kartı `adaylar/` altına kopyala; önerilen H- ön kaydı taslağını yaz (kural, parametre,
  birincil istatistik, kapı, beklenen yön).
- Push bildiriminde "ADAY: HK-…" yaz. Kilit testi ve ileri test **Soydan'ın oturumunda** yapılır.

## Bütçe
**Bir oturum = bir koşu.** Oturum başına en fazla ~40 dakika iş, en fazla 2 kart ve
**iki kartın toplamı en fazla 12 varyant** (ör. 7 + 5). Aynı oturumda ikinci bir "koşu"
başlatma; ikinci kart aynı koşu özetine yazılır. Sınır keşif sayacının (KS) hızını ve
dolayısıyla sahte aday sayısını sınırlar.
Kaynak bulunamazsa veya hepsi ön elemede düşerse bu da geçerli bir koşudur; özetini yaz.

## Hata durumunda
Veri dosyası yoksa / motor hata veriyorsa: düzeltmeye çalışma, `kosular/` özetine hatayı yaz,
push et ve dur.
