# 12 — Deployment Model AI

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Menyajikan model AI sebagai layanan yang bisa dipakai pengguna.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_model_ke_api_fastapi.ipynb](01_model_ke_api_fastapi.ipynb) | Artefak model (bobot, vocab, versi, metrik) dan *training–serving skew*, API FastAPI (lifespan, validasi Pydantic, `/health`, batch, API key dari env, middleware latensi), `TestClient`, server uvicorn sungguhan + p50/p95 & throughput (satu per satu vs batch vs paralel), demo Gradio | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/12-deployment/01_model_ke_api_fastapi.ipynb) |
| 02 | [02_optimasi_inferensi.ipynb](02_optimasi_inferensi.ipynb) | Mengukur dengan benar (warm-up, p50/p95), ONNX & ONNX Runtime (verifikasi output), kuantisasi int8 dinamis (ukuran, latensi, akurasi), model seukuran MiniLM untuk benchmark, batching (latensi vs throughput) & pemborosan padding | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/12-deployment/02_optimasi_inferensi.ipynb) |
| 03 | [03_docker_dan_deploy.ipynb](03_docker_dan_deploy.ipynb) | Docker (image, container, layer), Dockerfile serving yang ramping (tanpa PyTorch, non-root, health check), konfigurasi & rahasia lewat environment, checklist produksi, deploy demo Gradio ke Hugging Face Spaces (opt-in), pilihan platform lain | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/12-deployment/03_docker_dan_deploy.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal). Tidak butuh GPU maupun API key.

> Uji cepat: set environment variable `QUICK_RUN=1` (training 5 epoch, model benchmark 2 layer, pengulangan lebih sedikit).

## Aplikasi (`app/`)

Kode aplikasi berupa file biasa, bukan di dalam notebook:

| File | Fungsi |
|---|---|
| [`model.py`](app/model.py) | Tokenizer (kata + bigram), model PyTorch, dan `Prediktor` dengan backend ONNX Runtime atau PyTorch |
| [`latih.py`](app/latih.py) | Melatih model pada NusaX-Senti (±20 detik di CPU) dan menyimpan `artefak/` (`model.pt`, `model.onnx`, `vocab.json`, `config.json`) |
| [`main.py`](app/main.py) | API FastAPI: `GET /health`, `POST /prediksi`, `POST /prediksi/batch` |
| [`ui_gradio.py`](app/ui_gradio.py) | Demo UI Gradio (juga dipakai sebagai `app.py` di Hugging Face Spaces) |
| [`Dockerfile`](app/Dockerfile), [`requirements.txt`](app/requirements.txt) | Image serving: FastAPI + ONNX Runtime, tanpa PyTorch (±400 MB) |
| [`tests/test_api.py`](app/tests/test_api.py) | 11 tes: health, prediksi, validasi input, API key, ONNX = PyTorch |

Menjalankan secara lokal (dari `12-deployment/app/`):

```bash
pip install torch pandas onnx onnxscript -r requirements.txt httpx pytest
python latih.py                   # buat artefak/
pytest -q                         # tes API
uvicorn main:app --reload         # buka http://127.0.0.1:8000/docs
docker build -t api-sentimen . && docker run -p 8000:8000 -e API_KEY=rahasiamu api-sentimen
```

CI menjalankan hal yang sama di job **API & Docker (modul 12)**: melatih model, `pytest`, membangun image, lalu menguji container (health check, 401 tanpa API key, prediksi dengan API key, user non-root).

## Data & Lisensi

- **NusaX-Senti** bahasa Indonesia ([IndoNLP/nusax](https://github.com/IndoNLP/nusax)): **CC-BY-SA**, diunduh dari GitHub saat training. Artefak model tidak di-commit.
- Model benchmark di notebook 02 memakai arsitektur BERT dari `transformers` dengan **bobot acak** (tidak mengunduh model).
- Library: `fastapi` (MIT), `uvicorn` (BSD-3-Clause), `gradio` (Apache-2.0), `onnx` (Apache-2.0), `onnxruntime` (MIT), `onnxscript` (MIT), `httpx` (BSD-3-Clause).
- Space Hugging Face yang dibuat notebook 03 memakai lisensi `agpl-3.0` (mengikuti repo ini).

## Topik

- [ ] Membuat API dengan FastAPI — *notebook 01*
- [ ] Demo UI dengan Gradio / Streamlit — *notebook 01 (Gradio), 03 (Spaces)*
- [ ] Containerization dengan Docker — *notebook 03*
- [ ] Optimasi inferensi: ONNX, kuantisasi, batching — *notebook 02*
- [ ] Deploy ke cloud / Hugging Face Spaces — *notebook 03*
