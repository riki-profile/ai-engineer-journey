# Image API sentimen (modul 12). Artefak model harus dibuat dulu: python latih.py
# Build & jalankan (dari folder 12-deployment/app/):
#   docker build -t api-sentimen .
#   docker run -p 8000:8000 -e API_KEY=ganti-dengan-rahasia api-sentimen
FROM python:3.11-slim

# Log Python langsung tampil (tanpa buffer) dan tanpa file .pyc
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instal dependensi lebih dulu: layer ini di-cache selama requirements.txt tidak berubah
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kode dan artefak model (hanya file yang dibutuhkan saat serving)
COPY model.py main.py ./
COPY artefak/config.json artefak/vocab.json artefak/model.onnx ./artefak/

# Jalankan sebagai pengguna biasa, bukan root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
