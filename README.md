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
| 05 | [Vision Transformer (ViT)](05-vision-transformer/) | 🟨 Sedang berjalan (3 notebook) |
| 06 | [Transformers untuk NLP](06-transformers-nlp/) | 🟨 Sedang berjalan (3 notebook) |
| 07 | [Embeddings & Vector Database](07-embeddings-vectordb/) | 🟨 Sedang berjalan (3 notebook) |
| 08 | [Dasar Large Language Model](08-llm-basics/) | 🟨 Sedang berjalan (3 notebook) |
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

`requirements.txt` saat ini mencakup dependensi modul 01–08.

## Pengecekan Otomatis (CI)

Setiap pull request dan push ke `main` diperiksa otomatis oleh GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

| Job | Isi |
|---|---|
| Lint & kebersihan repo | `ruff check .`, notebook di-commit tanpa output, scan pola API key/token |
| Tes `prepare_data.py` | `pytest` untuk proyek deteksi helm (dataset sintetis) |
| Notebook (QUICK_RUN) | Menjalankan notebook modul 01, 03, 04 (kecuali U-Net), 05 (ViT dari nol), 06 (tokenisasi & mini-GPT), 07 (FAISS), 08 (Claude API & tool use, terhadap [server tiruan](scripts/fake_anthropic_server.py) tanpa API key), dan notebook training helm dengan data kecil di CPU |
| Notebook berat (1 job paralel per notebook) | Modul 02, U-Net, fine-tune ViT, CLIP, fine-tune IndoBERT, embedding kalimat/vector DB, dan LLM lokal modul 08 (unduhan dataset/model besar). Tidak jalan di setiap PR; jalan terjadwal tiap Senin, manual lewat **Actions → CI → Run workflow**, atau di PR yang diberi label `notebook-berat` |

**Menguji notebook berat sebelum merge:** beri label `notebook-berat` pada PR. Job berat langsung berjalan, dan akan berjalan lagi di setiap push selama label masih terpasang (hapus label untuk menghentikannya). Tombol **Run workflow** hanya tersedia untuk workflow yang sudah ada di `main`.

Menjalankan pengecekan yang sama secara lokal:

```bash
pip install ruff nbformat nbclient ipykernel pytest
ruff check .
python scripts/run_notebooks.py --check-clean $(git ls-files '*.ipynb')
(cd projects/helmet-detection && pytest -q)
python scripts/run_notebooks.py 01-deep-learning/*.ipynb   # menjalankan notebook dengan QUICK_RUN=1
```

## Catatan Keamanan

Simpan API key di file `.env` (sudah diabaikan oleh `.gitignore`; salin dari [`.env.example`](.env.example)) atau di **Colab Secrets** — jangan pernah menulisnya langsung di kode atau notebook. CI memeriksa pola API key/token di setiap PR.

## Lisensi

Repo ini berlisensi **[GNU AGPL-3.0](LICENSE)**, mengikuti lisensi library `ultralytics` yang dipakai di modul 03 dan proyek deteksi helm. Alasannya dijelaskan di [README proyek](projects/helmet-detection/README.md#lisensi-mengapa-agpl-30).
