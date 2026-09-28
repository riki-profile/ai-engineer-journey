# AI Engineer Journey

Repo catatan dan latihan belajar **AI engineering**, dari deep learning dasar hingga deployment dan MLOps.

## Daftar Isi Modul

| No | Modul | Status |
|----|-------|--------|
| 01 | [Deep Learning Dasar](01-deep-learning/) | 🟨 Sedang berjalan (2 notebook) |
| 02 | [Convolutional Neural Network (CNN)](02-cnn/) | 🟨 Sedang berjalan (2 notebook) |
| 03 | [Object Detection](03-object-detection/) | 🟨 Sedang berjalan (3 notebook) |
| 04 | [Image Segmentation](04-segmentation/) | ⬜ Belum dimulai |
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

`requirements.txt` saat ini mencakup dependensi modul 01–03.

## Catatan Keamanan

Simpan API key di file `.env` (sudah diabaikan oleh `.gitignore`) — jangan pernah menulisnya langsung di kode atau notebook.

## Lisensi

Repo ini berlisensi **[GNU AGPL-3.0](LICENSE)**, mengikuti lisensi library `ultralytics` yang dipakai di modul 03 dan proyek deteksi helm. Alasannya dijelaskan di [README proyek](projects/helmet-detection/README.md#lisensi-mengapa-agpl-30).
