"""Tes otomatis untuk src/prepare_data.py.

Jalankan dari folder projects/helmet-detection/:
    pytest -q
Semua tes memakai dataset sintetis kecil, jadi cepat dan tidak butuh internet.
"""

from __future__ import annotations

import functools
import http.server
import io
import json
import shutil
import sys
import tarfile
import threading
from pathlib import Path

import pytest
import yaml

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "src"))
sys.path.insert(0, str(PROJECT_DIR / "tests"))

import prepare_data  # noqa: E402
from make_synthetic_dataset import NAMES, make_roboflow_dir, zip_dir  # noqa: E402


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Folder kerja sementara berisi salinan configs/data.yaml, mirip folder proyek."""
    (tmp_path / "configs").mkdir()
    shutil.copy(PROJECT_DIR / "configs" / "data.yaml", tmp_path / "configs" / "data.yaml")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATASET_URL", raising=False)
    return tmp_path


def laporan(workdir):
    return json.loads((workdir / "results" / "data_report.json").read_text())


def test_roboflow_zip_valid_dan_sync_names(workdir):
    arsip = zip_dir(make_roboflow_dir(workdir / "sumber"), workdir / "helm.zip")

    assert prepare_data.main(["--source", str(arsip), "--sync-names"]) == 0

    lap = laporan(workdir)
    assert lap["errors"] == []
    assert {s: v["gambar"] for s, v in lap["split"].items()} == {"train": 24, "val": 6, "test": 6}
    # "valid" dari Roboflow harus dipetakan ke "val"
    assert (workdir / "data" / "images" / "val").is_dir()
    # Nama kelas disalin dari data.yaml bawaan dataset
    names = yaml.safe_load((workdir / "configs" / "data.yaml").read_text())["names"]
    assert names == {0: NAMES[0], 1: NAMES[1]}


def test_error_yang_ditanam_semuanya_tertangkap(workdir):
    src = make_roboflow_dir(workdir / "sumber")
    (src / "train/labels/train_1.txt").write_text("2 0.5 0.5 0.2 0.2\n")                    # class_id di luar rentang
    (src / "train/labels/train_2.txt").write_text("1 0.1 0.1 0.2 0.1 0.3 0.3 0.1 0.2\n")    # poligon segmentasi
    (src / "train/labels/train_3.txt").write_text("0 250 120 40 60\n")                      # koordinat piksel
    (src / "train/labels/yatim.txt").write_text("0 0.5 0.5 0.1 0.1\n")                      # label tanpa gambar
    (src / "valid/labels/valid_0.txt").unlink()                                              # gambar tanpa label
    (src / "test/images/test_0.jpg").write_bytes(b"bukan gambar")                           # gambar rusak

    assert prepare_data.main(["--source", str(src), "--sync-names"]) == 1

    errors = "\n".join(laporan(workdir)["errors"])
    assert "class_id 2 di luar rentang" in errors
    assert "poligon segmentasi" in errors
    assert "koordinat tidak valid" in errors
    assert "yatim.txt" in errors
    assert "gambar rusak test_0.jpg" in errors
    warnings = "\n".join(laporan(workdir)["warnings"])
    assert "gambar tanpa file label" in warnings


def test_dataset_tanpa_split_dibagi_otomatis(workdir):
    src = workdir / "flat"
    make_roboflow_dir(workdir / "tmp", sizes=(("train", 20),))
    shutil.move(workdir / "tmp" / "train", src)  # hasil: flat/images + flat/labels tanpa nama split

    assert prepare_data.main(["--source", str(src), "--skip-image-check"]) == 0

    jumlah = {s: v["gambar"] for s, v in laporan(workdir)["split"].items()}
    assert jumlah == {"train": 16, "val": 2, "test": 2}


def test_tidak_menimpa_tanpa_force_dan_validate_only(workdir):
    src = make_roboflow_dir(workdir / "sumber")
    assert prepare_data.main(["--source", str(src)]) == 0

    assert prepare_data.main(["--source", str(src)]) == 2           # data sudah ada, tanpa --force
    assert prepare_data.main(["--validate-only"]) == 0               # validasi saja tetap bisa
    assert prepare_data.main(["--source", str(src), "--force"]) == 0


def test_arsip_berbahaya_ditolak(workdir):
    arsip = workdir / "jahat.tar.gz"
    with tarfile.open(arsip, "w:gz") as t:
        info = tarfile.TarInfo("../../keluar.txt")
        info.size = 1
        t.addfile(info, io.BytesIO(b"x"))

    assert prepare_data.main(["--source", str(arsip)]) == 1
    assert not (workdir.parent / "keluar.txt").exists()
    assert not (workdir.parent.parent / "keluar.txt").exists()


def test_tanpa_source(workdir):
    assert prepare_data.main([]) == 2


def test_unduh_url_tidak_membocorkan_api_key(workdir, capsys):
    arsip = zip_dir(make_roboflow_dir(workdir / "sumber"), workdir / "helm.zip")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(workdir))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/{arsip.name}?api_key=RAHASIA123"
        assert prepare_data.main(["--source", url]) == 0
    finally:
        server.shutdown()

    assert "RAHASIA123" not in capsys.readouterr().out
    assert not any("RAHASIA123" in p.name for p in (workdir / "data").rglob("*"))
