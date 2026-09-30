"""API sentimen dengan FastAPI (modul 12).

Menjalankan secara lokal (dari folder 12-deployment/app/, setelah `python latih.py`):
    uvicorn main:app --reload
lalu buka http://127.0.0.1:8000/docs untuk dokumentasi interaktif.

Konfigurasi lewat environment variable (bukan hardcode di kode):
    FOLDER_MODEL  folder artefak model (default: artefak)
    API_KEY       jika diisi, setiap permintaan prediksi wajib membawa header X-API-Key yang sama
    MAKS_BATCH    jumlah teks maksimum per permintaan batch (default: 32)
"""

from __future__ import annotations

import logging
import os
import secrets
import time
from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, StringConstraints

from model import Prediktor

FOLDER_MODEL = os.getenv("FOLDER_MODEL", "artefak")
API_KEY = os.getenv("API_KEY") or None
MAKS_BATCH = int(os.getenv("MAKS_BATCH", "32"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("api-sentimen")
state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Model dimuat SEKALI saat server mulai, bukan di setiap permintaan
    state["prediktor"] = Prediktor(FOLDER_MODEL)
    log.info("Model dimuat: backend=%s versi=%s", state["prediktor"].backend, state["prediktor"].config["versi"])
    yield
    state.clear()


app = FastAPI(title="API Sentimen Bahasa Indonesia", version="1.0.0", lifespan=lifespan,
              description="Contoh deployment model untuk modul 12 ai-engineer-journey.")


@app.middleware("http")
async def catat_waktu(request: Request, call_next):
    mulai = time.perf_counter()
    respons = await call_next(request)
    ms = (time.perf_counter() - mulai) * 1000
    respons.headers["X-Waktu-Proses-ms"] = f"{ms:.1f}"
    log.info("%s %s -> %d (%.1f ms)", request.method, request.url.path, respons.status_code, ms)
    return respons


header_api_key = APIKeyHeader(name="X-API-Key", auto_error=False)


def cek_api_key(key: str | None = Security(header_api_key)) -> None:
    """Autentikasi sederhana. Jika API_KEY tidak diatur, API terbuka (hanya untuk pengembangan lokal)."""
    if API_KEY and not secrets.compare_digest(key or "", API_KEY):     # compare_digest: tahan timing attack
        raise HTTPException(status_code=401, detail="API key tidak valid atau tidak ada (header X-API-Key)")


Teks = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]


class PermintaanPrediksi(BaseModel):
    teks: Teks = Field(examples=["Pengirimannya cepat dan barangnya bagus!"])


class PermintaanBatch(BaseModel):
    teks: list[Teks] = Field(min_length=1, max_length=MAKS_BATCH)


class HasilPrediksi(BaseModel):
    label: Literal["negatif", "netral", "positif"]
    skor: dict[str, float]


@app.get("/health")
def health() -> dict:
    prediktor = state.get("prediktor")
    return {"status": "ok" if prediktor else "memuat", "backend": getattr(prediktor, "backend", None),
            "versi_model": prediktor.config["versi"] if prediktor else None}


@app.post("/prediksi", response_model=HasilPrediksi, dependencies=[Depends(cek_api_key)])
def prediksi(permintaan: PermintaanPrediksi) -> dict:
    # Fungsi biasa (bukan async): FastAPI menjalankannya di thread pool, cocok untuk komputasi CPU
    return state["prediktor"].prediksi([permintaan.teks])[0]


@app.post("/prediksi/batch", response_model=list[HasilPrediksi], dependencies=[Depends(cek_api_key)])
def prediksi_batch(permintaan: PermintaanBatch) -> list[dict]:
    return state["prediktor"].prediksi(permintaan.teks)
