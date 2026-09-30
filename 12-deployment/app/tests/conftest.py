"""Fixture bersama untuk tes API dan tes kualitas model (modul 12–13)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
ARTEFAK = APP_DIR / "artefak"


@pytest.fixture(scope="session", autouse=True)
def artefak():
    """Pastikan artefak model ada. CI membuatnya lebih dulu dengan `python latih.py --epoch 10`."""
    if not (ARTEFAK / "model.onnx").exists():
        from latih import latih
        latih(ARTEFAK, epoch=10)
    return ARTEFAK
