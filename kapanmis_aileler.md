# Kapanmış aileler (proje ölçümleri, 13.10.2026)

Yeniden denenmez; ancak YENİ bir mekanizma getirirse (kartta açıkça yazılarak) denenebilir.

| Aile | Sonuç | Kaynak belge |
|---|---|---|
| Parabolic SAR (klasik / JMA / JCFB-adaptif; M1, M15, H1; giriş ve çıkış) | brüt < 0, H-J1 bağımsız veride RED | Ölçüm Arşivi 2.19 |
| Osilatör 20/80 uç bölge dönüşü | brüt +0,2…+0,3 p | claude_OSC-on-tarama-sonuc |
| Order Flow Conviction 0 kesişimi / eğim dönüşü | brüt +0,7 / −0,4 p, günde ~20 işlem | claude_OFC-on-tarama-sonuc |
| Nyao scalper sinyal ailesi (M1) | brüt −3,1 p | claude_H-N1-* |
| Öngörüsüz giriş + pozisyon yönetimi ("sürüş") | hareket devamı +0,4…+2,6 p, maliyetin altında | claude_SURUS-sonuc |
| σ ölçekli kâr hedefi | yapısal katkı ≈ 0 | MÖT-02, H-Ç1 |
| Çıkış parametresi taramasıyla zayıf girişi kurtarma | girişlerin yön bilgisi ~1 p | claude_MFE-MAE-teshis-sonuc |
| Açılış kırılımı (H-K1) | RED | claude/H-K1-acilis-kirilimi-sonuc |
| Büyük emir takibi (H-B1) | RED | claude/H-B1-buyuk-emir-sonuc |
| Dönüş kapısı (H-D1, 44 test) | RED | claude/H-D1-donus-kapisi-sonuc |
| HMM rejim EA'sı | yön hipotezi yok, zararlı | Ölçüm Arşivi |
| Yüksek frekans (günde 10+ işlem) genel | maliyet brüt kenarı yer (EK99: brüt +4,3 p, maliyet 6,7 p) | claude/EK99-backtest-sonuc |
| 10:15 · 5 dk delta takip · 30 dk tut | 82 seansta net +35 (t 3,3), 624 seansta net −6,1 | MÖT-AJAN-01 / motor testi |
