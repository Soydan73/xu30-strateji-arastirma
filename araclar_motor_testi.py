import sys, time, numpy as np, pandas as pd
sys.path.insert(0, "."); import motor as M
S = M.yukle("./xu30_kesif_m1_gunduz.csv.gz"); print("seans", len(S), "devir", len(M.devir_gunleri(S)))

def delta_kural(s, t0=615, L=5):
    d = (s.buy_volume - s.sell_volume).to_numpy(float)
    out = np.zeros(len(s)); i = np.where(s.dk.to_numpy() == t0)[0]
    if len(i) and i[0] >= L: out[i[0]] = np.sign(d[i[0]-L+1:i[0]+1].sum())
    return out
def sizintili(s, t0=615, H=30):
    c = s.close.to_numpy(float); out = np.zeros(len(s)); i = np.where(s.dk.to_numpy() == t0)[0]
    if len(i) and i[0] + H < len(s): out[i[0]] = np.sign(c[i[0]+H] - c[i[0]])
    return out
t=time.time()
r = M.kart_calistir(S, delta_kural, [dict(t0=t0, L=L) for t0 in (615, 660) for L in (5, 15, 30)], lambda p: dict(H=30))
print(r.drop(columns="p").round(2).to_string()); print(f"{time.time()-t:.1f} sn")
r2 = M.kart_calistir(S, sizintili, [dict(t0=615, H=30)], lambda p: dict(H=30))
print(r2[["n_islem","brut","net","t","K2","K5","ADAY","kanarya"]].to_string())
# sentetik doğruluk: elle bir seans
s = S[100]; isl = M.calistir([s], delta_kural, dict(t0=615, L=5), dict(H=30))
print(isl.to_string()); i=np.where(s.dk==615)[0][0]; print("elle giris", s.open[i+1], "cikis", s.close[i+30], "maliyet", round(M.maliyet(s.open[i+1]),2))
