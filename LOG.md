# Log Character Bible v2 — Prompt, Perubahan & Hasil Ukur

Semua prompt untuk generator ditulis dalam bahasa Inggris. Catatan dalam bahasa Indonesia.
Skor identitas = kemiripan wajah ArcFace (insightface buffalo_l, 0–1). Pembanding utama: `jangkar_depan_turtleneck_s2001.png` (foto depan) dan `acuan_wajah_final.png`.

## Lingkungan
- Kaggle, 2× Tesla T4 16 GB, RAM 30 GB, ComfyUI 0.46.0
- Model: `flux1-dev-kontext_fp8_scaled`, CLIP `clip_l` + `t5xxl_fp8_e4m3fn`, VAE `flux-vae-bf16`
- Sampler: euler / simple, 20 steps, CFG 1, FluxGuidance 2.5, denoise 1

## Perubahan optimasi (urut waktu)

| # | Perubahan | Alasan | Hasil |
|---|---|---|---|
| O1 | Acuan wajah = `acuan_wajah_final.png` resolusi penuh (FluxKontextImageScale ~1 MP), bukan acuan gabungan 0,6 MP | Wajah di acuan gabungan hanya ~80 px, identitas melenceng | Jangkar depan skor 0.868 |
| O2 | Hapus "fine lines" dari prompt kulit | Dibaca sebagai kerutan → wajah tampak tua | Kulit natural, tidak menua |
| O3 | Text encoder di CPU (`DualCLIPLoader device=cpu`) | Percobaan menghindari macet | Membantu sebagian, bukan akar masalah |
| O4 | Dua acuan: jangkar + acuan wajah final (ReferenceLatent berantai) | Penguat identitas saat wajah menoleh | ¾ kiri menoleh 33° dengan skor tetap ~0.66; waktu naik ~4 → ~6,5 menit/gambar |
| O5 | Acuan wajah final dipotong sampai leher (`ImageCrop 1071×900`) | Kemeja putih acuan ikut terbawa ke baju | Turtleneck konsisten |
| O6 | Teknik mirror-sandwich untuk sisi kanan (balik input → putar ke kiri → balik hasil) | Kontext cenderung selalu memutar ke kiri; mirror hasil akhir memindah belahan rambut | Sisi kanan arah benar, belahan rambut tetap |
| O7 | **`--disable-dynamic-vram`** saat menjalankan ComfyUI | Akar masalah macet: fitur dynamic VRAM (comfy-aimdo) membuat proses diam (CPU 3%) saat memuat model | Tidak macet lagi |
| O8 | Tunnel cloudflared di background + link dicetak | Kernel bebas → Console bisa dipakai saat ComfyUI berjalan | Diagnosa & perbaikan tanpa restart sesi |
| O9 | Dataset Kaggle "Alat Ukur Wajah" (wheel insightface + ukur.py), dipasang SEBELUM ComfyUI menyala | Ukur langsung di Kaggle; pip saat ComfyUI berjalan berisiko | Notebook versi #6 |
| O10 | **Panaskan model**: baca T5, CLIP, VAE berurutan (`cat ... > /dev/null`) sebelum ComfyUI | Akar masalah macet yang sebenarnya: di sesi baru Kaggle mengunduh isi dataset secara malas (lazy); ComfyUI membaca acak per potongan → sangat lambat/diam. Terbukti: saat file dibaca berurutan dari Console, ComfyUI langsung lanjut | Notebook versi #7 |
| O11 | Dataset Wan 2.1 (23,5 GB) dilepas dari notebook Character Bible | Tidak dipakai; memperlambat mulai sesi | Mulai sesi lebih cepat |
| O12 | Sel alat ukur pakai path pasti (bukan `$(find ...)`) | `$(...)` tidak terproses di sel Jupyter | Notebook versi #7 |
| O13 | Workflow dimuat ke kanvas ComfyUI + disimpan format kanvas (`workflows_kanvas/`), workflow tertanam di PNG hasil | User perlu melihat workflow | Menu Workflows ComfyUI berisi CB-v2-01..05 |

## Prompt yang dipakai

### Akhiran wajib (KEEP) untuk semua sudut
```
Keep the exact same woman with an identical face: same facial features and proportions, same eyes, eyelids, eyebrows, nose, lips, jawline and face shape, same youthful age, same skin tone, same hairstyle and hair color, same small stud earrings, same dark navy knit turtleneck sweater, neutral relaxed expression. Close-up head and shoulders portrait, same plain light grey background, same soft even studio lighting. Natural realistic skin with subtle visible pores, matte finish, no glow, no shine, no added wrinkles.
```

### Jangkar depan (seed 2001) — edit langsung acuan_wajah_final
```
Change only the clothing: replace the white collared shirt with a dark navy fitted knit turtleneck sweater with a high rolled neck. Keep everything else exactly the same: identical face, identical facial features and proportions, same eyes, eyelids, eyebrows, nose, lips, jawline and face shape, same youthful age, same skin tone, same hairstyle and hair color, same small stud earrings, same neutral expression, same head position, same framing, same plain light grey background. Natural realistic skin with subtle visible pores, matte finish, no glow, no shine, no added wrinkles.
```

### Tiga-perempat kiri (seed 3001, 2 acuan)
```
Rotate the camera so her head and shoulders are seen in a three-quarter view, her face turned about 45 degrees toward the left side of the image. + KEEP
```

### Profil (seed 3003 kiri langsung / 3004 kanan sandwich)
```
Rotate the camera to a full side profile: her head and shoulders turned 90 degrees so she faces the left side of the image, only one side of her face visible. + KEEP
```

### Tiga-perempat kanan (seed 3012, sandwich) — versi putaran tegas
```
Rotate the camera clearly to a three-quarter view: her head and shoulders turned a full 45 degrees toward the left side of the image, the far cheek partly hidden and the nose pointing toward the left edge, eyes looking in the same direction as the face. + KEEP
```

## Hasil ukur & keputusan

| Gambar | vs jangkar depan | vs acuan final | Sudut (yaw) | Status |
|---|---|---|---|---|
| Jangkar depan s2001 | – | 0.868 | 0° | KUNCI |
| ¾ kiri (Uji C, s3001) | 0.717 | 0.660 | −33° | KUNCI |
| ¾ kanan (sandwich, s3012) | 0.645 | 0.628 | +34° | KUNCI |
| Profil kanan (sandwich, s3004) | 0.571 | 0.540 | +49° | KUNCI |
| Profil kiri (C2, s3003) | 0.477 | 0.389 | −61° | **DICABUT** — bentuk wajah/rahang bergeser (dikoreksi user); kesalahan: dulu diukur vs ¾ kiri, bukan vs depan |
| **Profil kiri (F, s3103)** — acuan 1 = ¾ kiri terkunci (langkah kecil) + acuan wajah final | **0.576** | – | −57° | **KUNCI** (pengganti). s3113 ditolak: menghadap kanan |
| Belakang kepala (G, s3211/s3201) | n/a | – | 180° | **DICABUT** (koreksi user): panjang rambut 743px vs jangkar 899px = 83%, ujung rata seperti bob |
| Belakang kepala v2 (G2, s3221) — prompt panjang + ujung berlapis | panjang 885px = **98.4%** | – | 180° | KANDIDAT — ujung sedikit meruncing tapi belum mengembang keluar seperti depan |
| Belakang kepala v2 (G2, s3231) | panjang 834px = 92.8% | – | 180° | ditolak: terlalu pendek (ujung mengembang sudah bagus) |

### Prompt profil kiri versi F
```
Rotate the camera further to a full side profile: her head and shoulders turned another 45 degrees toward the left side of the image, so she faces the left edge in a clean 90 degree profile, only one side of her face visible. + KEEP
```

### Ditolak (ringkas)
- Uji awal 1 acuan: ¾ kanan & profil kanan salah arah (Kontext memutar ke kiri)
- Profil kiri Uji C: kemeja putih terbawa dari acuan
- ¾ kanan s3002: hanya menoleh 19° (skor 0.693 tapi putaran kurang)
- ¾ kanan s3022: 0.538

### Prompt belakang kepala versi G (workflow CB-v2-06-BelakangKepala)
```
Rotate the camera to a view from directly behind her: we see the back of her head and shoulders, her hair falling from behind, the back of the turtleneck collar, her face is not visible at all. Keep the exact same woman: same hairstyle, same shoulder-length dark brown hair with the same length, color, volume and side part, same dark navy knit turtleneck sweater, same body proportions. Head and shoulders framing, same plain light grey background, same soft even studio lighting. Photorealistic, natural hair texture, no glow.
```
Ukur sudut belakang: ArcFace tidak bisa (tanpa wajah) → dipakai warna rambut (hue/saturasi piksel gelap) vs jangkar + cek visual panjang/belahan. Catatan: ujung rambut belakang lebih rata (bob) dibanding ujung berlapis di depan.

### Prompt belakang kepala versi G2 (workflow CB-v2-06b-BelakangKepala-Panjang)
```
Rotate the camera to a view from directly behind her: we see the back of her head and shoulders, her face is not visible at all. Her hair is exactly as long as in the reference image: it falls well past her shoulders down onto her upper back, the hair ends reaching the middle of the shoulder blades, far below the top of the shoulders. The hair ends are softly layered and feathered with uneven tapered tips that flick slightly outward, exactly like the reference, not a blunt straight-cut bob. Keep the exact same woman: same hairstyle, same dark brown hair color, same volume and side part, same dark navy knit turtleneck sweater, same body proportions. Head and shoulders framing, same plain light grey background, same soft even studio lighting. Photorealistic, natural hair texture, no glow.
```
Alat ukur baru `tools/ukur_rambut.py`: panjang rambut = baris piksel rambut (coklat, R>B+12) teratas s/d terbawah. Jangkar 899px; semua sudut terkunci 898–901px. Target ≥ 99%.

O14: Kaggle mematikan sesi saat idle ("Are you still there?") di tengah sampling → dipasang skrip keepalive di tab Kaggle yang otomatis klik "Continue editing".

### Percobaan memperbaiki ujung rambut s3221 (belum berhasil)
| Versi | Teknik | Hasil |
|---|---|---|
| G3 (s3241/3251, CB-v2-06c) | Kontext edit seluruh gambar, acuan = s3221 | Ujung hampir tak berubah; framing membesar → panjang turun ke 857px (95%). Ditolak |
| G4 (s3261/3271, CB-v2-06d) | Inpaint mask area ujung, denoise 0.75, tempel balik | Perubahan rata-rata 0.6/255 di area ujung → praktis identik. Ditolak |
| G5 (s3281/3291, CB-v2-06e) | Mask diperluas ke bawah, denoise 0.95, prompt "outward flip" | Perubahan 0.9/255 → identik. Ditolak |

Diagnosis: ReferenceLatent memakai gambar yang sama dengan yang di-inpaint, sehingga Kontext menyalin ulang ujung lama apa pun promptnya. Perbaikan berikutnya: acuan diganti (mis. jangkar depan yang ujungnya mengembang) atau inpaint tanpa ReferenceLatent.

O15: Simulasi aktivitas berkala di tab Kaggle (tombol "Continue editing" ternyata muncul setelah sesi berhenti, jadi auto-klik saja tidak mencegah).

### Evaluasi tekstur rambut (koreksi user, 27 Nov)
Rambut harus seperti acuan final: tipis-ringan, sedikit messy, ada flyaway, ujung runcing lentik ke luar (lihat profil kiri), tidak tebal/smooth/kilap iklan. Alat baru `tools/ukur_tekstur.py`.

| Gambar | detail helai | variasi terang | saturasi | R/G | panjang (ujung di bawah bahu) |
|---|---|---|---|---|---|
| Acuan final | 6.87 | 38.0 | 0.44 | 1.61 | – |
| Profil kiri | 7.47 | 28.8 | 0.62 | 2.03 | 0.053 |
| G2 s3221 | 4.78 | 11.7 | 0.74 | 2.32 | 0.028 |
| H s3301/3311/3321 (CB-v2-06f: acuan 2 = acuan final asli + prompt tekstur eksplisit) | 4.9–5.2 | 11–13 | 0.73–0.75 | 2.36–2.47 | 0.015–0.023 |

Kesimpulan H: prompt tekstur & acuan final hampir tidak berpengaruh — Kontext untuk tampak belakang selalu jatuh ke gaya "rambut iklan" (tebal, licin, kemerahan). Drift juga terlihat bertahap di rantai acuan→jangkar→profil.

O16: Sel penjaga (heartbeat loop) ditambahkan di akhir notebook: sesi Kaggle mati tiap kali ComfyUI selesai & kernel idle.

## Aturan ukur (mulai sekarang)
- Selalu dibandingkan dengan **foto depan (jangkar)**, bukan hanya sudut tetangga.
- Panjang rambut (ukur_rambut.py) harus ≥ 99% jangkar (≈ 890px), ujung berlapis & mengembang keluar.
- Ambang awal per sudut (vs jangkar): 15–30° ≥ 0.70, 45° ≥ 0.60, 60–90° ≥ 0.50, plus cek rasio rahang.

## Rencana berikutnya
1. Menoleh ke belakang lewat bahu kanan, lalu bahu kiri (satu per satu, tunggu instruksi user).
2. Ekspresi: senyum, sedih ingin menangis, marah tegas, terkejut.
3. Kumpulkan 15–25 gambar terkunci → latih LoRA karakter.
