# HK-20261020-03 — meta-etiketleme kural karşılığı: M15 JMA hızlı/yavaş kesişimi, yalnız oynaklık ve
# momentum uyumu süzgecinden geçerse (yalnız sinyal fonksiyonu; model eğitimi YOK)
import numpy as np


def _jma_adim(x, durum, L, faz=0.0, guc=2.0):
    """Jurik JMA (kamuya açık yaklaşık biçim), tek adım. durum = [e0, e1, e2, jma] ya da None."""
    fo = 0.5 if faz < -100 else (2.5 if faz > 100 else faz / 100 + 1.5)
    beta = 0.45 * (L - 1) / (0.45 * (L - 1) + 2)
    alfa = beta ** guc
    if durum is None:
        return [x, 0.0, 0.0, x]
    e0, e1, e2, j = durum
    e0 = (1 - alfa) * x + alfa * e0
    e1 = (x - e0) * (1 - beta) + beta * e1
    e2 = (e0 + fo * e1 - j) * (1 - alfa) ** 2 + alfa ** 2 * e2
    j = e2 + j
    return [e0, e1, e2, j]


def m15_kovalar(s):
    """Tamamlanmış M15 kovaları: (sinyal_bar_indeksi, kapanış, yüksek, düşük). Kova dk//15, dk>=570,
    dk%15==14 olan M1 barı kapanınca tamamlanır; >= 12 bar içermeli. Yalnız o bara kadarki veri kullanılır."""
    dk = s.dk.to_numpy(); h = s.high.to_numpy(float); l = s.low.to_numpy(float); c = s.close.to_numpy(float)
    out = []
    for i in range(len(s)):
        if dk[i] < 570 or dk[i] % 15 != 14:
            continue
        k = dk[i] // 15
        m = (dk[: i + 1] >= 570) & (dk[: i + 1] // 15 == k)
        if m.sum() < 12:
            continue
        out.append((i, c[i], h[: i + 1][m].max(), l[: i + 1][m].min()))
    return out


def ozellikler(s, hizli=3, yavas=8, nv=4):
    """Her tamamlanmış M15 kovası için: (bar, kesisim_yonu, oynaklik_bps, r1, r4). Kesişim yönü 0 ise kesişim yok."""
    kov = m15_kovalar(s)
    dh = dy = None
    onceki_fark = None
    sat = []
    for j, (i, c, h, l) in enumerate(kov):
        dh = _jma_adim(c, dh, hizli); dy = _jma_adim(c, dy, yavas)
        fark = dh[3] - dy[3]
        yon = 0
        if onceki_fark is not None and j >= 5 and np.sign(fark) != 0 and np.sign(fark) != np.sign(onceki_fark):
            yon = int(np.sign(fark))
        onceki_fark = fark
        if j >= nv:
            v = np.mean([(kov[q][2] - kov[q][3]) / kov[q][1] * 1e4 for q in range(j - nv + 1, j + 1)])
        else:
            v = np.nan
        r1 = c - kov[j - 1][1] if j >= 1 else np.nan
        r4 = c - kov[j - 4][1] if j >= 4 else np.nan
        sat.append((i, yon, v, r1, r4))
    return sat


def sinyal(s, mod="ana", hizli=3, yavas=8, nv=4, v_esik=0.0, H=60):
    """mod: 'kesisim' (KONTROL, süzgeçsiz), 'oyn' (yalnız oynaklık), 'mom' (yalnız momentum uyumu),
    'ana' (oynaklık + momentum). Sinyal yalnız 10:44–16:59 arasında tamamlanan kovalarda."""
    n = len(s)
    out = np.zeros(n)
    dk = s.dk.to_numpy()
    for i, yon, v, r1, r4 in ozellikler(s, hizli, yavas, nv):
        if yon == 0 or not (644 <= dk[i] <= 1019):
            continue
        oyn_ok = (not np.isnan(v)) and v >= v_esik
        mom_ok = (not np.isnan(r4)) and np.sign(r1) == yon and np.sign(r4) == yon
        if mod == "kesisim" or (mod == "oyn" and oyn_ok) or (mod == "mom" and mom_ok) or \
           (mod == "ana" and oyn_ok and mom_ok):
            out[i] = yon
    return out
