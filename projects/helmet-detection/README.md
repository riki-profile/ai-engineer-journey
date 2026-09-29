# Deteksi Helm Pengendara Motor dengan YOLO

**Status:** 🟨 Persiapan data & training

## Tujuan Proyek

Membangun model object detection yang mendeteksi pengendara motor dan membedakan apakah mereka **memakai helm** atau **tidak memakai helm**, menggunakan YOLO dari library [`ultralytics`](https://github.com/ultralytics/ultralytics).

Contoh pemakaian nyata: analisis rekaman CCTV lalu lintas untuk memantau tingkat kepatuhan memakai helm.

Target proyek:
- [ ] Menyiapkan dan memvalidasi dataset dalam format YOLO.
- [ ] Melatih model (fine-tune YOLO pretrained) di Google Colab.
- [ ] Mengevaluasi dengan mAP50, mAP50-95, precision/recall per kelas, dan confusion matrix.
- [ ] Menganalisis kasus gagal (objek kecil, oklusi, malam hari, dan sebagainya).
- [ ] Demo inference pada gambar/video.

## Dataset

| | |
|---|---|
| **Sumber** | _TODO: tempel link dataset_ |
| **Lisensi** | _TODO: tulis lisensi dataset_ |
| **Kelas** | _TODO: sesuaikan dengan dataset_ (sementara `helmet`, `no_helmet`) |

> ⚠️ Periksa lisensi dataset sebelum dipakai. Beberapa dataset (misalnya CC BY-NC) melarang penggunaan komersial, dan larangan itu juga bisa berlaku untuk model yang dilatih darinya. Dataset **tidak** disimpan di repo ini.

## Cara Menyiapkan Data

Semua perintah dijalankan dari folder `projects/helmet-detection/`.

```bash
pip install -r requirements.txt

# Opsi 1: URL di file .env (disarankan jika URL memuat API key, misalnya ekspor Roboflow)
cp .env.example .env        # lalu isi DATASET_URL
python src/prepare_data.py --sync-names

# Opsi 2: URL atau file/folder lokal langsung
python src/prepare_data.py --source path/ke/dataset.zip --sync-names

# Validasi ulang tanpa mengunduh
python src/prepare_data.py --validate-only
```

Yang dilakukan `src/prepare_data.py`:
1. Mengunduh (URL) atau membaca (folder / `.zip` / `.tar.gz`) dataset, lalu mengekstraknya dengan aman.
2. Menyusun ulang ke `data/images/{train,val,test}` dan `data/labels/{train,val,test}`. Skrip mengenali layout ekspor Roboflow (`train/images`, `valid/images`, …) dan layout Ultralytics (`images/train`, …). Jika dataset belum punya split, data dibagi acak 80/10/10 (bisa diubah dengan `--split`).
3. `--sync-names` menyalin nama kelas dari `data.yaml` bawaan dataset ke `configs/data.yaml`.
4. Memvalidasi format YOLO:
   - pasangan gambar ↔ label,
   - label tanpa gambar,
   - baris label (5 nilai, `class_id` valid, koordinat ternormalisasi 0–1, poligon segmentasi terdeteksi),
   - gambar rusak,
   - jumlah objek per kelas per split, dan ketidakseimbangan kelas.
5. Menyimpan laporan ke `results/data_report.json`. Skrip keluar dengan kode `1` jika ada error, sehingga bisa dipakai di pipeline.

Opsi lengkap: `python src/prepare_data.py --help`.

Tes otomatis (juga dijalankan oleh CI): `pytest -q`. Tes memakai dataset sintetis dari `tests/make_synthetic_dataset.py` dan mencakup error yang sengaja ditanam, dataset tanpa split, arsip berbahaya, serta kebocoran API key di URL.

## Training di Google Colab

| Notebook | Isi | Colab |
|---|---|---|
| [01_train_yolo_colab.ipynb](notebooks/01_train_yolo_colab.ipynb) | Cek GPU → clone repo → siapkan & validasi dataset → training YOLO → kurva training → evaluasi per kelas di split test → contoh prediksi → simpan hasil ke `results/` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/projects/helmet-detection/notebooks/01_train_yolo_colab.ipynb) |

Langkah pemakaian:
1. Di Colab, simpan URL dataset di **Secrets** (ikon 🔑) dengan nama `DATASET_URL` dan aktifkan *Notebook access*. Jika repo private, tambahkan juga `GITHUB_TOKEN`.
2. Aktifkan GPU (**Runtime → Change runtime type → T4 GPU**), atur sel **Konfigurasi** (model, epoch, ukuran gambar), lalu **Run all**.
3. Hasil training disimpan di Google Drive (`MyDrive/helmet-detection/runs/`). Jika Colab terputus, jalankan ulang notebook dengan `RUN_NAME` yang sama, dan training akan dilanjutkan dari checkpoint terakhir.
4. Metrik dan grafik (`metrics.json`, `per_class.csv`, confusion matrix, kurva PR) disalin ke `results/<RUN_NAME>/` dan diunduh sebagai zip, siap di-commit. Bobot model (`*.pt`) tidak di-commit.

## Hasil

_Belum ada. Isi setelah training pertama: model, epoch, mAP50 / mAP50-95 per kelas, dan temuan dari analisis kasus gagal._

## Struktur

```
projects/helmet-detection/
├── configs/data.yaml    # konfigurasi dataset YOLO
├── src/prepare_data.py  # siapkan & validasi dataset
├── notebooks/           # training & evaluasi di Colab
├── results/             # laporan data, metrik, grafik
└── data/                # dataset (tidak di-commit)
```

## Lisensi: Mengapa AGPL-3.0?

Seluruh repo ini berlisensi **[GNU AGPL-3.0](../../LICENSE)**. Alasannya:

1. **`ultralytics` berlisensi AGPL-3.0**, begitu pula bobot pretrained YOLO yang disediakan Ultralytics. Kode proyek ini memakai library tersebut secara langsung, dan model hasil fine-tune adalah turunan dari bobot pretrained itu.
2. **AGPL mewajibkan keterbukaan kode, termasuk untuk layanan jaringan.** Jika proyek ini dibagikan, atau dijalankan sebagai layanan yang bisa diakses orang lain (misalnya demo web atau API deteksi helm), kode sumber lengkapnya harus tersedia dengan lisensi AGPL-3.0. Memakai AGPL-3.0 sejak awal membuat repo ini otomatis patuh dan tidak menimbulkan kebingungan lisensi.
3. **Konsisten untuk portofolio.** Siapa pun yang melihat repo ini langsung tahu syarat penggunaannya. Karena proyek ini berada di repo yang sama dengan materi belajar, lisensi AGPL-3.0 berlaku untuk seluruh repo.

Catatan:
- Lisensi **dataset** terpisah dari lisensi kode, dan dataset tidak disertakan di repo ini. Lihat bagian Dataset.
- Untuk penggunaan komersial tertutup, dibutuhkan [Ultralytics Enterprise License](https://www.ultralytics.com/license), atau detektor dengan lisensi permisif.
- Ini ringkasan untuk keperluan belajar, bukan nasihat hukum.
