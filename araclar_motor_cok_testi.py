# motor_cok.py kabul testi (03.11.2026). Çalıştır: python3 araclar_motor_cok_testi.py
# Yalnız MEKANİK sınar; çok seanslı bir hipotezin P&L'ine BAKMAZ (KS'ye eklenmez).
import sys, time, types, importlib.util, tempfile, os, textwrap, numpy as np, pandas as pd
sys.path.insert(0, "."); import motor as M, motor_cok as C
S = M.yukle("./xu30_kesif_m1_gunduz.csv.gz"); tablo = C._baglam_tablosu(S)
gun = tablo[0]; devir = tablo[1]; hata = 0
def kontrol(ad, kosul, ek=""):
    global hata
    print(("GECTI " if kosul else "KALDI ") + ad + (f"  ({ek})" if ek else "")); hata += (not kosul)

# 1) bağlam mekaniği
ok = True
for k in range(len(S)):
    o, b = C.baglam(S, k, 20, tablo)
    if len(o) > 20 or any(x.gun.iloc[0] >= gun[k] for x in o) or len(b["ayni_vade"]) != len(o): ok = False; break
kontrol("1a onceki hep geçmiş, ≤ geri, ayni_vade uzunluğu", ok)
k0 = [k for k, g in enumerate(gun) if g >= pd.Timestamp("2026-05-05")][0]
kontrol("1b veri boşluğundan sonraki ilk seansta onceki boş", len(C.baglam(S, k0, 60, tablo)[0]) == 0, str(gun[k0].date()))
kontrol("1c ilk seansta onceki boş", len(C.baglam(S, 0, 60, tablo)[0]) == 0)
kd = [k for k, g in enumerate(gun) if g in devir and k > 25 and k != k0][0]
o, b = C.baglam(S, kd, 20, tablo)
kontrol("1d devir gününde tüm onceki ayni_vade=False", b["devir_bugun"] and not b["ayni_vade"].any(), str(gun[kd].date()))
o, b = C.baglam(S, kd + 1, 20, tablo)
kontrol("1e devirden sonraki gün yalnız devir günü ayni_vade=True", b["ayni_vade"].sum() == 1 and b["ayni_vade"][-1])
kontrol("1f geri > 60 kırpılır", len(C.baglam(S, 300, 500, tablo)[0]) <= 60)

# 2) eşdeğerlik: tek seanslı kural iki motorda birebir aynı
spec = importlib.util.spec_from_file_location("hk10", "sinyaller/HK-20261103-10.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def sar(s, onceki, bilgi, **p): return m.sinyal(s, **p)
V = [dict(), dict(bas=1050)]
a = M.kart_calistir(S, m.sinyal, V, lambda p: dict(H=10)); c = C.kart_calistir_cok(S, sar, V, lambda p: dict(H=10))
sut = ["n_islem", "n_seans", "brut", "net", "t", "net_eksi5", "net_A", "net_B", "net_devirsiz", "K1", "K2", "K3", "K4", "K6", "K7"]
kontrol("2 tek seanslı kural motor.py ile birebir aynı sonuç", np.allclose(a[sut].astype(float).values, c[sut].astype(float).values, equal_nan=True))

# 3) sızıntılı kurallar yakalanmalı (dosyadan yüklenen gerçek modüller; statik denetim kaynak okur)
tmp = tempfile.mkdtemp()
def modul(ad, kod):
    yol = os.path.join(tmp, ad + ".py"); open(yol, "w").write(textwrap.dedent(kod))
    sp = importlib.util.spec_from_file_location(ad, yol); mm = importlib.util.module_from_spec(sp); sp.loader.exec_module(mm); return mm.sinyal
gelecek = modul("gelecek", """
    import numpy as np
    def sinyal(s, onceki, bilgi):
        c = s.close.to_numpy(float); out = np.zeros(len(s)); i = np.flatnonzero(s.dk.to_numpy() == 615)
        if len(i) and i[0] + 30 < len(s): out[i[0]] = np.sign(c[i[0] + 30] - c[i[0]])
        return out
""")
dosya = modul("dosya", """
    import numpy as np, pandas as pd
    def sinyal(s, onceki, bilgi):
        d = pd.read_csv("xu30_kesif_m1_gunduz.csv.gz")
        return np.zeros(len(s))
""")
bozan = modul("bozan", """
    import numpy as np
    def sinyal(s, onceki, bilgi):
        for o in onceki: o.loc[o.index[-1], "close"] += 1.0
        return np.zeros(len(s))
""")
temiz = modul("temiz", """
    import numpy as np
    def sinyal(s, onceki, bilgi, esik=0):
        # mekanik deneme: yön tarihten türetilen sözde rastgele işaret (hipotez değil)
        out = np.zeros(len(s)); i = np.flatnonzero(s.dk.to_numpy() == 600)
        dun = [o for o, a in zip(onceki, bilgi["ayni_vade"]) if a]
        if len(i) and len(onceki) >= 5:
            h = (bilgi["gun"].toordinal() * 2654435761) % 2
            out[i[0]] = 1 if h else -1
        return out
""")
for ad, f, bek in [("gelecek bar", gelecek, "gün içi"), ("dosya okuma", dosya, "statik"), ("onceki bozma", bozan, "değiştirdi")]:
    ok, msg = C.kanarya_cok(S, f, {}, 20)
    kontrol(f"3 sızıntılı kural yakalandı: {ad}", (not ok) and bek in msg, msg)
t = time.time(); ok, msg = C.kanarya_cok(S, temiz, {}, 20)
kontrol("3 temiz çok seanslı kural kanaryadan geçer", ok, msg)
r = C.kart_calistir_cok(S, temiz, [dict(), dict(geri=60)], lambda p: dict(H=30))
kontrol("4 kart_calistir_cok uçtan uca çalışır (P&L değerlendirilmez)", len(r) == 2 and (r.n_islem > 0).all() and r.K5.all(), f"{time.time()-t:.1f} sn")
print("SONUC:", "TUM TESTLER GECTI" if hata == 0 else f"{hata} TEST KALDI")
