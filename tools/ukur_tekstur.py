import sys, numpy as np
from PIL import Image, ImageFilter
def stats(p, box):
    im=Image.open(p).convert('RGB').crop(box)
    a=np.asarray(im).astype(float); R,G,B=a[...,0],a[...,1],a[...,2]
    L=0.299*R+0.587*G+0.114*B
    hair=(R>B+8)&(L<170)&(L>8)
    Lb=np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(2))).astype(float)
    hp=np.abs(L-Lb)                                   # detail halus (helai)
    Lb8=np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(8))).astype(float)
    mid=np.abs(Lb-Lb8)                                 # pita/gumpalan lebar (smooth band)
    sat=(a.max(2)-a.min(2))/np.maximum(a.max(2),1)
    hl=(L>np.percentile(L[hair],95))
    r=R[hair]/np.maximum(G[hair],1)
    return dict(detail_halus=hp[hair].mean(), pita_lebar=mid[hair].mean(), rasio_detail=hp[hair].mean()/max(mid[hair].mean(),1e-3),
                kecerahan=L[hair].mean(), sebaran_terang=L[hair].std(), saturasi=sat[hair].mean(), merah_vs_hijau=r.mean())
rows=[('ACUAN FINAL (kemeja)','ComfyUI/acuan_wajah_final.png',(700,560,1071,1260)),
      ('JANGKAR depan','ComfyUI/jangkar_depan_turtleneck_s2001.png',(560,420,880,1000)),
      ('PROFIL KIRI lock','ComfyUI/turn_profil_kiri_LOCK.png',(480,420,800,1000)),
      ('BELAKANG G2 s3221','bible_v2_ukur/G2_belakang_s3221.png',(250,420,630,1000))]
print(f"{'gambar':22s} detail  pita  rasio  terang sebaran satur  R/G")
for n,p,b in rows:
    s=stats(p,b); print(f"{n:22s} {s['detail_halus']:5.2f} {s['pita_lebar']:5.2f} {s['rasio_detail']:5.2f} {s['kecerahan']:6.1f} {s['sebaran_terang']:6.1f} {s['saturasi']:5.2f} {s['merah_vs_hijau']:5.2f}")
