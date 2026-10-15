# HK-20261015-02 — geniş IB günlerinde IB kenarı reddinin sönümlenmesi (yalnız sinyal)
import numpy as np

IB_BAS, IB_SON = 585, 644          # 09:45–10:44
GIR_BAS = 645


def sinyal(s, P=1, w=0.91, son=960):
    n = len(s); out = np.zeros(n)
    dk = s.dk.to_numpy(); o = s.open.to_numpy(float)
    h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    ibh = -np.inf; ibl = np.inf; ib_o = None; ib_n = 0
    hazir = False; genis = False
    kabul_ust = kabul_alt = False
    kh = -np.inf; kl = np.inf; kova = None
    for i in range(n):
        d = dk[i]
        if IB_BAS <= d <= IB_SON:
            if ib_o is None: ib_o = o[i]
            ibh = max(ibh, h[i]); ibl = min(ibl, l[i]); ib_n += 1
            continue
        if d < GIR_BAS:
            continue
        if not hazir:
            hazir = True
            genis = ib_n >= 50 and ib_o is not None and (ibh - ibl) / ib_o * 100.0 >= w
        if not genis:
            continue
        # M15 kovası (09:45 hizalı) biriktir
        k = (d - IB_BAS) // 15
        if k != kova:
            kova = k; kh = -np.inf; kl = np.inf
        kh = max(kh, h[i]); kl = min(kl, l[i])
        tamam = (d - IB_BAS) % 15 == 14
        sig = 0
        if P == 1:
            ust = h[i] >= ibh and c[i] < ibh and not kabul_ust
            alt = l[i] <= ibl and c[i] > ibl and not kabul_alt
            if ust != alt:
                sig = -1 if ust else 1
        elif tamam:
            ust = kh >= ibh and c[i] < ibh and not kabul_ust
            alt = kl <= ibl and c[i] > ibl and not kabul_alt
            if ust != alt:
                sig = -1 if ust else 1
        if d <= son:
            out[i] = sig
        # kabul: tamamlanmış M15 kovası kenarın ötesinde kapandı (bu bar sonrası geçerli)
        if tamam:
            if c[i] > ibh: kabul_ust = True
            if c[i] < ibl: kabul_alt = True
    return out
