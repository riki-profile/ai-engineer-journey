"""Tes otomatis API sentimen (modul 12).

Jalankan dari folder 12-deployment/app/:
    pytest -q
Jika artefak model belum ada, tes melatih model lebih dulu (lihat conftest.py; butuh torch & internet untuk data NusaX).
"""

from __future__ import annotations

import numpy as np
import pytest
from conftest import ARTEFAK

from model import LABELS, Prediktor


@pytest.fixture
def client(monkeypatch):
    from fastapi.testclient import TestClient

    import main
    monkeypatch.setattr(main, "FOLDER_MODEL", str(ARTEFAK))
    monkeypatch.setattr(main, "API_KEY", None)
    with TestClient(main.app) as c:          # `with` menjalankan lifespan (memuat model)
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["backend"] == "onnx"


def test_prediksi_satu_teks(client):
    r = client.post("/prediksi", json={"teks": "Barangnya bagus sekali, pengiriman cepat!"})
    assert r.status_code == 200
    hasil = r.json()
    assert hasil["label"] in LABELS
    assert set(hasil["skor"]) == set(LABELS)
    assert abs(sum(hasil["skor"].values()) - 1) < 1e-3
    assert "X-Waktu-Proses-ms" in r.headers


def test_prediksi_batch(client):
    r = client.post("/prediksi/batch", json={"teks": ["enak sekali", "pelayanan buruk", "biasa saja"]})
    assert r.status_code == 200
    assert len(r.json()) == 3


@pytest.mark.parametrize("payload", [{"teks": ""}, {"teks": "   "}, {"teks": "a" * 2001}, {}, {"teks": 123}])
def test_input_tidak_valid_ditolak(client, payload):
    assert client.post("/prediksi", json=payload).status_code == 422


def test_batch_terlalu_besar_ditolak(client):
    import main
    assert client.post("/prediksi/batch", json={"teks": ["x"] * (main.MAKS_BATCH + 1)}).status_code == 422


def test_api_key(client, monkeypatch):
    import main
    monkeypatch.setattr(main, "API_KEY", "rahasia-uji")
    data = {"teks": "mantap"}
    assert client.post("/prediksi", json=data).status_code == 401
    assert client.post("/prediksi", json=data, headers={"X-API-Key": "salah"}).status_code == 401
    assert client.post("/prediksi", json=data, headers={"X-API-Key": "rahasia-uji"}).status_code == 200
    assert client.get("/health").status_code == 200          # health check tetap terbuka


def test_onnx_sama_dengan_pytorch():
    pytest.importorskip("torch")
    teks = ["mantap sekali", "kecewa berat dengan pelayanannya", "biasa", "kata yang tidak dikenal xyzabc"]
    onnx, torch_ = Prediktor(ARTEFAK, backend="onnx"), Prediktor(ARTEFAK, backend="torch")
    np.testing.assert_allclose(onnx.logits(teks), torch_.logits(teks), atol=1e-4)
