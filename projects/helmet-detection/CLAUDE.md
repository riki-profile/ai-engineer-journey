# CLAUDE.md — Proyek Deteksi Helm

Panduan untuk Claude saat bekerja di folder `projects/helmet-detection/`. Aturan umum repo di `/CLAUDE.md` (root) tetap berlaku.

## Konteks

Proyek **portofolio** object detection: mendeteksi pengendara motor yang **memakai helm** dan **tidak memakai helm** dengan YOLO (library `ultralytics`).

Pemilik proyek sudah paham Python, SQL, Git, dan ML dasar, serta sudah menyelesaikan materi object detection di `03-object-detection/` (IoU, NMS, mAP, format YOLO). Karena ini proyek portofolio, kode harus rapi, dapat direproduksi, dan terdokumentasi, bukan sekadar eksperimen.

## Aturan

1. **Komentar penjelasan dalam bahasa Indonesia.** Nama variabel/fungsi boleh bahasa Inggris.
2. **Tanpa API key atau secret di kode.** URL dataset (misalnya ekspor Roboflow yang memuat API key) disimpan di `.env` sebagai `DATASET_URL` (lihat `.env.example`). `.env` sudah diabaikan oleh `.gitignore`. Jangan mencetak URL lengkap yang berisi key ke log.
3. **Training dilakukan di Google Colab (GPU).** Notebook di `notebooks/` harus bisa dijalankan di Colab dari awal (clone repo, install dependensi, siapkan data).
4. **Cloud session ini hanya CPU.** Uji skrip dengan data kecil/sintetis dan 1 epoch saja. Kode harus otomatis memakai GPU bila tersedia.
5. **Perbarui README proyek** setiap ada perubahan penting (hasil training, metrik, sumber data, cara pakai).

## Aturan khusus proyek

- Jalankan semua perintah dari folder `projects/helmet-detection/`; path di `configs/data.yaml` relatif terhadap folder ini.
- `data/` **tidak pernah di-commit** (sudah diabaikan oleh `.gitignore` root). Dataset selalu diperoleh ulang lewat `src/prepare_data.py`.
- `results/` hanya untuk artefak kecil yang layak di-commit: laporan data, metrik, grafik, dan contoh prediksi. Bobot model (`*.pt`) dan folder `runs/` tidak di-commit.
- Repo ini berlisensi **AGPL-3.0** (mengikuti `ultralytics`). Jangan menambahkan dependensi atau kode dengan lisensi yang tidak kompatibel, dan catat lisensi setiap sumber data/model baru di README.

## Struktur

```
projects/helmet-detection/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env.example         # template DATASET_URL
├── configs/data.yaml    # konfigurasi dataset YOLO (nama kelas & path split)
├── src/prepare_data.py  # unduh/ekstrak + susun + validasi dataset
├── notebooks/           # notebook training/evaluasi (Colab)
├── results/             # laporan & metrik (kecil, di-commit)
└── data/                # dataset (diabaikan git)
```
