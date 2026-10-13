# -*- coding: utf-8 -*-
"""
MÖT-AJAN-01 — Araştırma ajanının eleme kapısının mantık ön testi
Soru 1: "Makul görünen" kural ailesinde (gerçek kenar yoksayılır) keşif kapısını
        şans eseri kaç kural geçer? (sahte geçiş oranı)
Soru 2: Gerçek bir kenar varsa keşif bölümü onu yakalayabilir mi? (güç)
Soru 3: Keşifte geçenler 20 günlük kilitli bölümde ne yapıyor?
Veri : XU30_M1_birlesik.csv (proje kopyası, 102 seans), yalnız GUNDUZ.
Maliyet: 8,4 p/işlem (Ölçüm Arşivi 2.19 ortak ölçütü).
"""
import itertools, numpy as np, pandas as pd

MALIYET = 8.4
KILIT = 20
rng = np.random.default_rng(20261013)

m = pd.read_csv("m1.csv", parse_dates=["time"])
m = m[m.seans == "GUNDUZ"].copy()
m["gun"] = m.time.dt.date
m["dk"] = m.time.dt.hour * 60 + m.time.dt.minute
m["delta"] = m.buy_volume - m.sell_volume
gunler = sorted(m.gun.unique())
kesif_g, kilit_g = gunler[:-KILIT], gunler[-KILIT:]

# her gün için dakika ızgarasında kapanış ve delta (09:45..18:05)
izgara = np.arange(9 * 60 + 45, 18 * 60 + 6)
C = np.full((len(gunler), len(izgara)), np.nan)
D = np.zeros((len(gunler), len(izgara)))
for i, g in enumerate(gunler):
    x = m[m.gun == g].set_index("dk")
    C[i] = x.close.reindex(izgara).ffill().bfill().values
    D[i] = x.delta.reindex(izgara).fillna(0).values

def kural_pnl(t0, L, ozellik, mod, H):
    """Seans başına tek işlem: t0'da L dk geriye bak, işaret yönünde (veya tersine) H dk tut."""
    a = izgara.searchsorted(t0); b = min(a + H, len(izgara) - 1)
    if a - L < 0:
        return None                            # geriye bakış seans başını aşıyor: geçersiz
    if ozellik == "getiri":
        s = np.sign(C[:, a] - C[:, a - L])
    else:
        s = np.sign(D[:, a - L:a].sum(1))
    if mod == "ters":
        s = -s
    return s * (C[:, b] - C[:, a])            # brüt, puan

t0s = list(range(10 * 60, 17 * 60 + 1, 15))
Ls, Hs = [5, 15, 30, 60], [15, 30, 60, 120]
aile = [k for k in itertools.product(t0s, Ls, ["getiri", "delta"], ["takip", "ters"], Hs)
        if izgara.searchsorted(k[0]) - k[1] >= 0]
ik = np.array([i for i, g in enumerate(gunler) if g in set(kesif_g)])
il = np.array([i for i, g in enumerate(gunler) if g in set(kilit_g)])

def ist(p):
    n = len(p); mu = p.mean(); se = p.std(ddof=1) / np.sqrt(n)
    return mu, mu / se if se > 0 else 0.0

sat = []
for k in aile:
    g = kural_pnl(*k)
    net = g - MALIYET
    mk, tk = ist(net[ik]); ml, tl = ist(net[il])
    bk, _ = ist(g[ik])
    sat.append((k, bk, mk, tk, ml, tl))
df = pd.DataFrame(sat, columns=["kural", "brut_k", "net_k", "t_k", "net_l", "t_l"])

print(f"Seans: toplam {len(gunler)} | keşif {len(kesif_g)} ({kesif_g[0]}→{kesif_g[-1]}) | kilit {len(kilit_g)} ({kilit_g[0]}→{kilit_g[-1]})")
print(f"Kural ailesi: {len(df)} kural (t0 × L × özellik × mod × H)")
print(f"Keşif brüt ortalaması (aile): {df.brut_k.mean():+.2f} p, std {df.brut_k.std():.2f}")
print(f"Keşifte brüt >= 4,2 p (Std 0.5.8 eşiği): {(df.brut_k >= 4.2).sum()} kural ({(df.brut_k >= 4.2).mean():.1%})")
for esik in [2.0, 2.58, 3.0, 3.5]:
    gec = df[(df.net_k > 0) & (df.t_k >= esik)]
    tut = gec[(gec.net_l > 0)]
    print(f"Kapı net>0 ve t>={esik:<4}: geçen {len(gec):4d} ({len(gec)/len(df):.2%}) | kilitte net>0 kalan {len(tut)}")

# Null kalibrasyonu: işaret karıştırma (seans bazında rastgele yön) -> gerçek sahte geçiş oranı
print("\nİşaret-karıştırma null'ı (200 tekrar × aile, keşif bölümü):")
gecis = {2.0: [], 2.58: [], 3.0: [], 3.5: []}
kaba = np.array([np.abs(kural_pnl(*k)) for k in aile])     # |hareket|
for _ in range(200):
    s = rng.choice([-1.0, 1.0], size=kaba.shape)
    net = (s * kaba)[:, ik] - MALIYET
    mu = net.mean(1); t = mu / (net.std(1, ddof=1) / np.sqrt(len(ik)))
    for e in gecis: gecis[e].append(((mu > 0) & (t >= e)).mean())
for e, v in gecis.items():
    print(f"  t>={e:<4}: kural başına sahte geçiş {np.mean(v):.4%}")

# Güç: tek işlem/seans, keşif bölümü; gerçek net kenar delta p/işlem olsaydı
sd = np.median([kural_pnl(*k)[ik].std(ddof=1) for k in aile])
n = len(ik)
print(f"\nGüç (seans başı P&L std medyanı {sd:.1f} p, n={n} seans):")
from math import erf, sqrt
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
for d in [2, 5, 10, 15, 20]:
    for e in [2.58, 3.0]:
        print(f"  net kenar {d:>2} p → t>={e} yakalama olasılığı {1 - Phi(e - d / (sd / sqrt(n))):.1%}")
print(f"  t>=3 için gereken net kenar ≈ {3 * sd / sqrt(n):.1f} p/işlem")
print(f"  Kilitli 20 seansta net>0 t>=2 için gereken ≈ {2 * sd / sqrt(KILIT):.1f} p/işlem")

# --- Ek teşhis: geçenler kim, kuyruk günlerine mi bağlı? ---
print("\nKeşifte net>0 ve t>=2,58 geçen kurallar (aykırı gün duyarlılığı):")
gec = df[(df.net_k > 0) & (df.t_k >= 2.58)].sort_values("t_k", ascending=False)
for _, r in gec.iterrows():
    g = kural_pnl(*r.kural)[ik] - MALIYET
    srt = np.sort(g)[::-1]
    out = []
    for k in [3, 5]:
        x = np.sort(g)[:-k]; mu, t = ist(x); out.append(f"en iyi {k} gün çıkınca net {mu:+.1f} (t {t:+.2f})")
    print(f"  {r.kural}: net {r.net_k:+.1f} t {r.t_k:.2f} | kilit net {r.net_l:+.1f} t {r.t_l:.2f} | " + " | ".join(out))
# Bağımsızlık: geçenlerin keşif P&L'leri ne kadar ilişkili?
P = np.array([kural_pnl(*k)[ik] for k in gec.kural])
if len(P) < 2:
    raise SystemExit("  (tek kural geçti; korelasyon teşhisi atlandı)")
cc = np.corrcoef(P); print(f"  Geçenler arası ortalama korelasyon: {cc[np.triu_indices(len(P),1)].mean():.2f}")
# Piyasa yönü ile ilişki: günlük gündüz getirisi
gun_get = (C[:, -1] - C[:, 0])[ik]
print(f"  Geçenlerin P&L'inin gün getirisi |r| ile korelasyonu (ort.): {np.mean([np.corrcoef(p, np.abs(gun_get))[0,1] for p in P]):.2f}")
