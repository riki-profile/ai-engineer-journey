"""Gerbang kualitas model (modul 13, CI/CD untuk ML).

Tes ini gagal jika model yang baru dilatih lebih buruk dari standar minimum, sehingga
model yang jelek tidak ikut di-build dan di-deploy. Ambang bisa diatur lewat
environment variable AMBANG_AKURASI (default 0.60).
"""

from __future__ import annotations

import json
import os

import pytest
from conftest import ARTEFAK

from model import Prediktor

AMBANG_AKURASI = float(os.getenv("AMBANG_AKURASI", "0.60"))


def test_akurasi_test_di_atas_ambang():
    config = json.loads((ARTEFAK / "config.json").read_text())
    assert config["akurasi_test"] >= AMBANG_AKURASI, (
        f"Akurasi test {config['akurasi_test']:.3f} di bawah ambang {AMBANG_AKURASI}")


# Uji regresi perilaku: kasus jelas yang SUDAH benar di model saat ini tidak boleh rusak di versi berikutnya.
# Catatan jujur: model kecil ini masih salah di beberapa kasus jelas lain, misalnya
# "Barangnya jelek dan rusak." diprediksi positif (lihat notebook 02 modul 13, bagian uji perilaku).
# Kasus yang sudah diperbaiki sebaiknya ditambahkan ke daftar ini agar tidak kambuh.
@pytest.mark.parametrize("teks, label", [
    ("Barangnya bagus sekali, saya sangat puas!", "positif"),
    ("Pelayanannya buruk sekali, saya kecewa.", "negatif"),
    ("Kecewa berat, barangnya rusak.", "negatif"),
])
def test_regresi_perilaku(teks, label):
    assert Prediktor(ARTEFAK).prediksi([teks])[0]["label"] == label
