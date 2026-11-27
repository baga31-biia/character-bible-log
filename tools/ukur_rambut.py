# Ukur panjang rambut: puncak kepala -> ujung rambut terbawah (piksel rambut = coklat: R > B+12, gelap)
import sys, numpy as np
from PIL import Image
for p in sys.argv[1:]:
    a=np.asarray(Image.open(p).convert('RGB')).astype(int); R,G,B=a[...,0],a[...,1],a[...,2]
    hair=(R>B+12)&(R<200)&((R+G+B)<450)
    skin=(R>150)&(R>B+25)
    hair&=~skin
    rows=hair.sum(1); idx=np.where(rows>25)[0]
    top,bot=idx.min(),idx.max()
    # ujung berlapis: lebar profil 30 baris terbawah (makin bervariasi = makin berlapis)
    print(f"{p.split('/')[-1]:38s} puncak={top:4d} ujung={bot:4d} panjang={bot-top:4d}px")
