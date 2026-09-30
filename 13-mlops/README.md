# 13 — MLOps

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Mengelola siklus hidup model secara terstruktur dan dapat direproduksi.

## Notebook

Semua notebook memakai model sentimen kecil dari [modul 12](../12-deployment/app/) (dilatih pada NusaX-Senti dalam hitungan detik di CPU), jadi fokusnya pada proses MLOps, bukan modelnya.

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_experiment_tracking_mlflow.ipynb](01_experiment_tracking_mlflow.ipynb) | Konsep MLflow (experiment, run, parameter, metrik, artefak), mencatat kurva training per epoch lewat callback, *hyperparameter sweep* dengan *nested run*, memilih model dari data validasi (bukan test), model **pyfunc** (*models from code*), **Model Registry** dengan alias `champion` dan memuat model lewat `models:/nama@alias` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/13-mlops/01_experiment_tracking_mlflow.ipynb) |
| 02 | [02_versioning_reproducibility_cicd.ipynb](02_versioning_reproducibility_cicd.ipynb) | Seed dan variasi antar-seed, versioning data dengan hash SHA-256 (manifest), validasi data, **lineage** (commit git, hash data, environment, `pip freeze`) di MLflow, manajemen environment, uji perilaku (*behavioral testing*), CI/CD/CT untuk ML dan **gerbang kualitas** model di CI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/13-mlops/02_versioning_reproducibility_cicd.ipynb) |
| 03 | [03_monitoring_dan_drift.ipynb](03_monitoring_dan_drift.ipynb) | Simulasi 6 minggu trafik produksi (normal, *label drift*, bahasa Jawa/Sunda/Inggris), metrik monitoring (KS test panjang teks, rasio token tak dikenal, PSI distribusi prediksi, keyakinan, akurasi dengan label terlambat), aturan peringatan dan dashboard, model **challenger** vs **champion** dan promosi berbasis aturan di registry | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/13-mlops/03_monitoring_dan_drift.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal). Tidak butuh GPU maupun API key.

> Uji cepat: set environment variable `QUICK_RUN=1` (training 3 epoch, sweep lebih kecil).

File pendukung:

| File | Fungsi |
|---|---|
| [`pyfunc_sentimen.py`](pyfunc_sentimen.py) | Pembungkus model modul 12 sebagai model MLflow `pyfunc` (*models from code*) |
| [`../12-deployment/app/tests/test_kualitas_model.py`](../12-deployment/app/tests/test_kualitas_model.py) | Gerbang kualitas di CI: akurasi test ≥ ambang dan uji regresi perilaku |

Notebook membuat `mlflow.db` (SQLite), `mlruns/`, dan folder `artefak_*` di folder ini. Semuanya diabaikan oleh `.gitignore`. Untuk melihat hasil di UI MLflow (lokal):

```bash
cd 13-mlops
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Data & Lisensi

- **NusaX-Senti** ([IndoNLP/nusax](https://github.com/IndoNLP/nusax)), bahasa Indonesia, Jawa, Sunda, dan Inggris: **CC-BY-SA**, diunduh dari GitHub saat notebook dijalankan.
- Library: `mlflow` (Apache-2.0), `scipy` (BSD-3-Clause), ditambah library modul 12.

## Topik

- [ ] Experiment tracking (MLflow) — *notebook 01*
- [ ] Versioning data dan model — *notebook 01 (registry), 02 (data)*
- [ ] CI/CD untuk proyek ML — *notebook 02*
- [ ] Monitoring model di produksi dan data drift — *notebook 03*
- [ ] Reproducibility dan manajemen environment — *notebook 02*
