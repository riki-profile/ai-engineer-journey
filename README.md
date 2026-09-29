# AI Engineer Journey

[![CI](https://github.com/riki-profile/ai-engineer-journey/actions/workflows/ci.yml/badge.svg)](https://github.com/riki-profile/ai-engineer-journey/actions/workflows/ci.yml)

Repo catatan dan latihan belajar **AI engineering**, dari deep learning dasar hingga deployment dan MLOps.

## Daftar Isi Modul

| No | Modul | Status |
|----|-------|--------|
| 01 | [Deep Learning Dasar](01-deep-learning/) | 🟨 Sedang berjalan (2 notebook) |
| 02 | [Convolutional Neural Network (CNN)](02-cnn/) | 🟨 Sedang berjalan (2 notebook) |
| 03 | [Object Detection](03-object-detection/) | 🟨 Sedang berjalan (3 notebook) |
| 04 | [Image Segmentation](04-segmentation/) | 🟨 Sedang berjalan (3 notebook) |
| 05 | [Vision Transformer (ViT)](05-vision-transformer/) | ⬜ Belum dimulai |
| 06 | [Transformers untuk NLP](06-transformers-nlp/) | ⬜ Belum dimulai |
| 07 | [Embeddings & Vector Database](07-embeddings-vectordb/) | ⬜ Belum dimulai |
| 08 | [Dasar Large Language Model](08-llm-basics/) | ⬜ Belum dimulai |
| 09 | [Retrieval-Augmented Generation (RAG)](09-rag/) | ⬜ Belum dimulai |
| 10 | [Fine-tuning LLM](10-llm-finetuning/) | ⬜ Belum dimulai |
| 11 | [AI Agent](11-ai-agent/) | ⬜ Belum dimulai |
| 12 | [Deployment Model AI](12-deployment/) | ⬜ Belum dimulai |
| 13 | [MLOps](13-mlops/) | ⬜ Belum dimulai |

**Keterangan status:** ⬜ Belum dimulai · 🟨 Sedang berjalan · ✅ Selesai

## Proyek

| Proyek | Deskripsi | Status |
|--------|-----------|--------|
| [Deteksi Helm](projects/helmet-detection/) | Deteksi pengendara motor memakai / tidak memakai helm dengan YOLO (ultralytics) | 🟨 Persiapan data & training |

## Setup

Notebook dirancang agar bisa dijalankan di **Google Colab**. Untuk menjalankan secara lokal:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` saat ini mencakup dependensi modul 01–04.

## Pengecekan Otomatis (CI)

Setiap pull request dan push ke `main` diperiksa otomatis oleh GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

| Job | Isi |
|---|---|
| Lint & kebersihan repo | `ruff check .`, notebook di-commit tanpa output, scan pola API key/token |
| Tes `prepare_data.py` | `pytest` untuk proyek deteksi helm (dataset sintetis) |
| Notebook (QUICK_RUN) | Menjalankan notebook modul 01, 03, 04 (kecuali U-Net), dan notebook training helm dengan data kecil di CPU |
| Notebook dataset besar | Modul 02 dan U-Net (unduhan dataset besar); hanya terjadwal tiap Senin atau manual lewat tab **Actions → CI → Run workflow** |

Menjalankan pengecekan yang sama secara lokal:

```bash
pip install ruff nbformat nbclient ipykernel pytest
ruff check .
python scripts/run_notebooks.py --check-clean $(git ls-files '*.ipynb')
(cd projects/helmet-detection && pytest -q)
python scripts/run_notebooks.py 01-deep-learning/*.ipynb   # menjalankan notebook dengan QUICK_RUN=1
```

## Catatan Keamanan

Simpan API key di file `.env` (sudah diabaikan oleh `.gitignore`) — jangan pernah menulisnya langsung di kode atau notebook.

## Lisensi

Repo ini berlisensi **[GNU AGPL-3.0](LICENSE)**, mengikuti lisensi library `ultralytics` yang dipakai di modul 03 dan proyek deteksi helm. Alasannya dijelaskan di [README proyek](projects/helmet-detection/README.md#lisensi-mengapa-agpl-30).
