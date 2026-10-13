# Keşif verisi: 00-Akis.csv -> yalnız gündüz seansı, tarih <= 2026-09-09 (sonrası ajana KAPALI)
import pandas as pd, hashlib, sys
SRC = sys.argv[1]; SON = pd.Timestamp("2026-09-08")   # 09.09 bu dosyada 16:44'te kesik (bilinen kusur)
HARIC = {pd.Timestamp("2024-12-02").date()}   # 10 bar: bozuk gün
a = pd.read_csv(SRC)
a["time"] = pd.to_datetime(a.DATE + " " + a.TIME, format="%Y.%m.%d %H:%M")
a = a.drop(columns=["DATE","TIME"]); a = a[a.time.dt.normalize() <= SON]
hm = a.time.dt.hour * 100 + a.time.dt.minute
a = a[(hm >= 925) & (hm <= 1815)].copy()
a = a[~a.time.dt.date.isin(HARIC)].copy()
hm = a.time.dt.hour * 100 + a.time.dt.minute
a["seans"] = (hm[a.index] < 945).map({True: "ACILIS", False: "GUNDUZ"})
out = a.rename(columns=str.lower)[["time","open","high","low","close","vol","ticks","buyvol","sellvol","seans"]]
out = out.rename(columns={"vol":"volume","buyvol":"buy_volume","sellvol":"sell_volume"})
n = out.groupby(out.time.dt.date).size()
kisa = n[n < 400]
out.to_csv("xu30_kesif_m1_gunduz.csv.gz", index=False, date_format="%Y-%m-%d %H:%M", compression="gzip")
h = hashlib.sha256(open(SRC,"rb").read()).hexdigest()
print(f"kaynak SHA256 {h[:16]}  satir {len(out)}  gun {n.size}  {n.index.min()} -> {n.index.max()}")
print(f"bar<400 gun: {len(kisa)}"); print(kisa.to_string())
