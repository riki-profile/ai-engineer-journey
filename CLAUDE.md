# CLAUDE.md

Panduan untuk Claude saat bekerja di repo ini.

## Konteks

Ini adalah repo belajar **AI engineering** pribadi, disusun per modul (`01-deep-learning` s.d. `13-mlops`).

Latar belakang pemilik repo:
- Sudah paham **Python, SQL, Git, dan machine learning dasar**.
- **Baru mulai deep learning** — jelaskan konsep DL (tensor, autograd, backprop, optimizer, dll.) secara bertahap dan jangan anggap sudah dikuasai.

## Aturan

1. **Komentar penjelasan dalam bahasa Indonesia.** Nama variabel/fungsi tetap boleh bahasa Inggris, tapi komentar dan penjelasan di notebook (markdown cell) ditulis dalam bahasa Indonesia.
2. **Jangan hardcode API key atau secret.** Simpan di file `.env` dan baca dengan `python-dotenv` / `os.getenv`. Pastikan `.env` tercantum di `.gitignore` sebelum membuat file tersebut. Di Colab, gunakan `google.colab.userdata` (Secrets) sebagai alternatif.
3. **Notebook harus bisa dijalankan di Google Colab.** Sertakan cell instalasi dependensi (`!pip install ...`) bila perlu, hindari path lokal absolut, dan unduh data lewat kode (bukan mengandalkan file yang hanya ada di mesin lokal).
4. **Cloud session ini hanya CPU.** Saat menguji kode di sini, pakai data kecil (subset dataset, sedikit epoch/batch, model kecil). Tulis kode yang otomatis memakai GPU bila tersedia, misalnya:
   ```python
   device = "cuda" if torch.cuda.is_available() else "cpu"
   ```
5. **Perbarui README setiap ada modul/materi baru.** Update `README.md` modul yang bersangkutan (topik & status) dan tabel status di `README.md` utama.
6. **Jalankan pengecekan CI secara lokal sebelum push**: `ruff check .`, `python scripts/run_notebooks.py --check-clean $(git ls-files '*.ipynb')`, dan notebook yang diubah lewat `python scripts/run_notebooks.py <notebook>`. Notebook di-commit **tanpa output**.

## Struktur

- `README.md` — daftar isi modul dan status.
- `NN-nama-modul/README.md` — tujuan, topik, dan status tiap modul.
- `requirements.txt` — dependensi (saat ini untuk modul 01–04).
- `projects/` — proyek portofolio. Setiap proyek punya `CLAUDE.md`, `README.md`, dan `requirements.txt` sendiri (lihat `projects/helmet-detection/`).
- `.github/workflows/ci.yml` — CI (GitHub Actions): ruff, notebook tanpa output, scan API key, pytest proyek helm, dan notebook dengan `QUICK_RUN=1`. Notebook baru yang ringan ditambahkan ke job `notebooks`; yang mengunduh dataset besar ke job `notebooks-berat`.
- `scripts/run_notebooks.py` — menjalankan notebook (`QUICK_RUN=1`) atau mengecek notebook bebas output (`--check-clean`).
- `LICENSE` — AGPL-3.0 (mengikuti `ultralytics`). Jangan menambahkan kode atau dependensi dengan lisensi yang tidak kompatibel.
