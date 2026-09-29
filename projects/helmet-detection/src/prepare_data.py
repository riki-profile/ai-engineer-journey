"""Menyiapkan dataset deteksi helm dalam format YOLO.

Langkah yang dilakukan skrip ini:
1. Mengambil dataset dari URL (unduh) atau path lokal (folder / .zip / .tar.gz).
2. Mengekstrak arsip dan menyusun ulang ke struktur standar:
       data/images/{train,val,test}/  dan  data/labels/{train,val,test}/
   Mendukung layout ekspor Roboflow (train/images, valid/images, ...) dan
   layout Ultralytics (images/train, labels/train, ...). Jika dataset belum
   punya split, gambar dibagi acak sesuai rasio --split.
3. Memvalidasi format YOLO: pasangan gambar-label, isi setiap baris label,
   jumlah objek per kelas, dan jumlah gambar per split.
4. Menyimpan laporan ke results/data_report.json.

Contoh pemakaian (jalankan dari folder projects/helmet-detection/):
    python src/prepare_data.py --source https://contoh.com/dataset.zip
    python src/prepare_data.py --source ~/Downloads/helmet.zip --sync-names
    python src/prepare_data.py --validate-only

URL dataset juga bisa diisi lewat variabel DATASET_URL di file .env, sehingga
URL yang memuat API key (misalnya ekspor Roboflow) tidak tertulis di kode.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import sys
import tarfile
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

import yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
# Nama folder split yang sering dipakai, dipetakan ke nama standar
SPLIT_ALIASES = {
    "train": "train",
    "training": "train",
    "val": "val",
    "valid": "val",
    "validation": "val",
    "test": "test",
    "testing": "test",
}
SPLITS = ("train", "val", "test")


# ---------------------------------------------------------------------------
# 1. Mengambil & mengekstrak dataset
# ---------------------------------------------------------------------------
def is_url(source: str) -> bool:
    return source.startswith(("http://", "https://"))


def download(url: str, dest_dir: Path) -> Path:
    """Unduh file ke dest_dir. Nama file tidak memuat query string (bisa berisi API key)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    nama = Path(url.split("?")[0]).name or "dataset"
    if not any(nama.endswith(ext) for ext in (".zip", ".tar", ".tar.gz", ".tgz")):
        nama += ".zip"  # ekspor Roboflow tidak punya ekstensi di URL, isinya zip
    tujuan = dest_dir / nama
    # Jangan cetak URL lengkap: query string-nya bisa berisi API key
    print(f"Mengunduh dataset → {tujuan}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(tujuan, "wb") as f:
        shutil.copyfileobj(resp, f)
    print(f"Selesai: {tujuan.stat().st_size / 1e6:.1f} MB")
    return tujuan


def _aman(base: Path, nama_anggota: str) -> bool:
    """Cegah 'zip slip': anggota arsip tidak boleh keluar dari folder tujuan."""
    target = (base / nama_anggota).resolve()
    return target == base.resolve() or base.resolve() in target.parents


def extract(archive: Path, dest_dir: Path) -> Path:
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True)
    print(f"Mengekstrak {archive.name} → {dest_dir}")
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as z:
            for anggota in z.namelist():
                if not _aman(dest_dir, anggota):
                    raise ValueError(f"Path berbahaya di dalam arsip: {anggota}")
            z.extractall(dest_dir)
    elif tarfile.is_tarfile(archive):
        with tarfile.open(archive) as t:
            for anggota in t.getmembers():
                if not _aman(dest_dir, anggota.name) or anggota.issym() or anggota.islnk():
                    raise ValueError(f"Anggota arsip tidak aman: {anggota.name}")
            t.extractall(dest_dir)
    else:
        raise ValueError(f"Format arsip tidak dikenali: {archive}")
    return dest_dir


def acquire(source: str, raw_dir: Path) -> Path:
    """Kembalikan folder berisi dataset mentah (sudah diekstrak)."""
    if is_url(source):
        return extract(download(source, raw_dir), raw_dir / "extracted")
    path = Path(source).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Source tidak ditemukan: {path}")
    if path.is_dir():
        return path
    return extract(path, raw_dir / "extracted")


# ---------------------------------------------------------------------------
# 2. Menyusun ulang ke struktur standar
# ---------------------------------------------------------------------------
def detect_split(img: Path, root: Path) -> str | None:
    """Tebak split dari nama folder di path gambar (mis. train/images atau images/valid)."""
    for bagian in img.relative_to(root).parts[:-1]:
        if bagian.lower() in SPLIT_ALIASES:
            return SPLIT_ALIASES[bagian.lower()]
    return None


def label_for(img: Path) -> Path:
    """Path label pasangan: ganti folder 'images' terakhir menjadi 'labels', ekstensi .txt."""
    parts = list(img.parts)
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == "images":
            parts[i] = "labels"
            break
    return Path(*parts).with_suffix(".txt")


def find_images(root: Path) -> dict[str | None, list[Path]]:
    per_split: dict[str | None, list[Path]] = {}
    for img in sorted(root.rglob("*")):
        if img.suffix.lower() in IMAGE_EXTS and "images" in img.parts:
            per_split.setdefault(detect_split(img, root), []).append(img)
    return per_split


def find_orphan_labels(root: Path) -> list[Path]:
    """Label di dataset sumber yang tidak punya gambar pasangan (tidak akan ikut disalin)."""
    stem_gambar = {
        label_for(img) for img in root.rglob("*")
        if img.suffix.lower() in IMAGE_EXTS and "images" in img.parts
    }
    return sorted(
        lbl for lbl in root.rglob("*.txt")
        if "labels" in lbl.parts and lbl not in stem_gambar
    )


def assign_splits(per_split, ratios, seed):
    """Lengkapi split yang belum ada dengan membagi data secara acak."""
    rng = random.Random(seed)
    train_r, val_r, test_r = ratios
    hasil = {s: list(per_split.get(s, [])) for s in SPLITS}

    tanpa_split = per_split.get(None, [])
    if tanpa_split:
        if any(hasil.values()):
            print(f"⚠️  {len(tanpa_split)} gambar tanpa split dimasukkan ke train")
            hasil["train"] += tanpa_split
        else:
            print(f"Dataset belum punya split → dibagi acak {train_r}/{val_r}/{test_r} (seed {seed})")
            rng.shuffle(tanpa_split)
            n = len(tanpa_split)
            n_train, n_val = round(n * train_r), round(n * val_r)
            hasil["train"] = tanpa_split[:n_train]
            hasil["val"] = tanpa_split[n_train:n_train + n_val]
            hasil["test"] = tanpa_split[n_train + n_val:]

    if hasil["train"] and not hasil["val"]:
        # Sisihkan sebagian train untuk validasi, proporsional terhadap rasio
        rng.shuffle(hasil["train"])
        n_val = max(1, round(len(hasil["train"]) * val_r / (train_r + val_r)))
        hasil["val"], hasil["train"] = hasil["train"][:n_val], hasil["train"][n_val:]
        print(f"Split val tidak ada → {n_val} gambar diambil dari train")
    if not hasil["test"]:
        print("⚠️  Split test tidak ada. Evaluasi akhir hanya bisa memakai val.")
    return hasil


def organize(splits, data_dir: Path) -> None:
    for split, images in splits.items():
        img_dir, lbl_dir = data_dir / "images" / split, data_dir / "labels" / split
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)
        dipakai: set[str] = set()
        for img in images:
            # Hindari tabrakan nama jika gambar berasal dari beberapa subfolder
            stem, k = img.stem, 1
            while stem in dipakai:
                stem, k = f"{img.stem}_{k}", k + 1
            dipakai.add(stem)
            shutil.copy2(img, img_dir / f"{stem}{img.suffix.lower()}")
            lbl = label_for(img)
            if lbl.exists():
                shutil.copy2(lbl, lbl_dir / f"{stem}.txt")
        print(f"  {split:<5}: {len(images)} gambar disalin")


# ---------------------------------------------------------------------------
# 3. Nama kelas
# ---------------------------------------------------------------------------
def normalize_names(names) -> dict[int, str]:
    # data.yaml bisa memakai list (Roboflow) atau dict {id: nama} (Ultralytics)
    if isinstance(names, list):
        return dict(enumerate(names))
    return {int(k): str(v) for k, v in names.items()}


def find_source_names(root: Path) -> dict[int, str] | None:
    for f in sorted(root.rglob("*.yaml")):
        try:
            isi = yaml.safe_load(f.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(isi, dict) and isi.get("names"):
            return normalize_names(isi["names"])
    return None


def write_config_names(config: Path, names: dict[int, str]) -> None:
    """Ganti blok `names:` (bagian terakhir file) dan pertahankan komentar di atasnya."""
    baris = config.read_text().splitlines()
    idx = next(i for i, b in enumerate(baris) if b.startswith("names:"))
    blok = yaml.safe_dump({"names": names}, sort_keys=False, allow_unicode=True)
    config.write_text("\n".join(baris[:idx]) + "\n" + blok)


# ---------------------------------------------------------------------------
# 4. Validasi format YOLO
# ---------------------------------------------------------------------------
def check_label_file(lbl: Path, n_kelas: int):
    """Kembalikan (daftar class_id, daftar pesan error) untuk satu file label."""
    kelas, errors = [], []
    for no, baris in enumerate(lbl.read_text().splitlines(), 1):
        nilai = baris.split()
        if not nilai:
            continue
        if len(nilai) != 5:
            jenis = " (sepertinya poligon segmentasi)" if len(nilai) > 5 and len(nilai) % 2 == 1 else ""
            errors.append(f"{lbl.name}:{no} harus 5 nilai, ada {len(nilai)}{jenis}")
            continue
        try:
            cls = int(nilai[0])
            cx, cy, w, h = map(float, nilai[1:])
        except ValueError:
            errors.append(f"{lbl.name}:{no} bukan angka: {baris.strip()}")
            continue
        if not 0 <= cls < n_kelas:
            errors.append(f"{lbl.name}:{no} class_id {cls} di luar rentang 0..{n_kelas - 1}")
        if not all(0 <= v <= 1 for v in (cx, cy, w, h)) or w <= 0 or h <= 0:
            errors.append(f"{lbl.name}:{no} koordinat tidak valid (harus ternormalisasi 0–1): {cx} {cy} {w} {h}")
        kelas.append(cls)
    return kelas, errors


def validate(data_dir: Path, names: dict[int, str], check_images: bool = True) -> dict:
    n_kelas = len(names)
    laporan = {"kelas": names, "split": {}, "errors": [], "warnings": []}

    for split in SPLITS:
        img_dir, lbl_dir = data_dir / "images" / split, data_dir / "labels" / split
        images = sorted(p for p in img_dir.glob("*") if p.suffix.lower() in IMAGE_EXTS) if img_dir.exists() else []
        labels = sorted(lbl_dir.glob("*.txt")) if lbl_dir.exists() else []
        stem_img = {p.stem for p in images}
        stem_lbl = {p.stem for p in labels}

        tanpa_label = sorted(stem_img - stem_lbl)
        label_yatim = sorted(stem_lbl - stem_img)
        instances, gambar_per_kelas, kosong = Counter(), Counter(), 0

        for lbl in labels:
            if lbl.stem not in stem_img:
                continue
            kelas, errs = check_label_file(lbl, n_kelas)
            laporan["errors"] += [f"[{split}] {e}" for e in errs]
            instances.update(kelas)
            gambar_per_kelas.update(set(kelas))
            kosong += not kelas

        if check_images:
            from PIL import Image  # terpasang bersama ultralytics
            for img in images:
                try:
                    with Image.open(img) as im:
                        im.verify()
                except Exception as e:  # noqa: BLE001 - laporkan semua jenis kerusakan file
                    laporan["errors"].append(f"[{split}] gambar rusak {img.name}: {e}")

        if label_yatim:
            laporan["errors"].append(f"[{split}] {len(label_yatim)} label tanpa gambar, mis. {label_yatim[:3]}")
        if tanpa_label:
            laporan["warnings"].append(
                f"[{split}] {len(tanpa_label)} gambar tanpa file label (dianggap background), mis. {tanpa_label[:3]}")
        if images and not instances:
            laporan["warnings"].append(f"[{split}] tidak ada satu pun objek berlabel")
        for k in range(n_kelas):
            if images and instances[k] == 0:
                laporan["warnings"].append(f"[{split}] kelas '{names[k]}' tidak punya objek")

        laporan["split"][split] = {
            "gambar": len(images),
            "label": len(labels),
            "gambar_tanpa_label": len(tanpa_label),
            "label_kosong": kosong,
            "objek_per_kelas": {names.get(k, str(k)): instances[k] for k in sorted(set(names) | set(instances))},
            "gambar_per_kelas": {names.get(k, str(k)): gambar_per_kelas[k] for k in sorted(set(names) | set(gambar_per_kelas))},
        }

    if not any(s["gambar"] for s in laporan["split"].values()):
        laporan["errors"].append(f"Tidak ada gambar di {data_dir}/images/{{train,val,test}}")
    return laporan


def print_report(laporan: dict) -> None:
    names = list(laporan["kelas"].values())
    total = sum(s["gambar"] for s in laporan["split"].values()) or 1
    print("\n=== Ringkasan dataset ===")
    header = f"{'split':<6} {'gambar':>7} {'%':>5} {'tanpa label':>12} " + " ".join(f"{n[:16]:>16}" for n in names)
    print(header)
    print("-" * len(header))
    for split, s in laporan["split"].items():
        objek = " ".join(f"{s['objek_per_kelas'].get(n, 0):>16}" for n in names)
        print(f"{split:<6} {s['gambar']:>7} {s['gambar'] / total:>5.0%} {s['gambar_tanpa_label']:>12} {objek}")
    print("(kolom kelas = jumlah objek/bounding box)")

    semua = Counter()
    for s in laporan["split"].values():
        semua.update({n: s["objek_per_kelas"].get(n, 0) for n in names})  # abaikan class_id tidak valid
    if len(semua) > 1 and min(semua.values()) > 0:
        rasio = max(semua.values()) / min(semua.values())
        if rasio > 3:
            laporan["warnings"].append(f"Kelas tidak seimbang: rasio terbanyak/tersedikit = {rasio:.1f}×")

    for judul, key, ikon in [("Peringatan", "warnings", "⚠️ "), ("Error", "errors", "❌")]:
        if laporan[key]:
            print(f"\n{judul} ({len(laporan[key])}):")
            for m in laporan[key][:20]:
                print(f"  {ikon} {m}")
            if len(laporan[key]) > 20:
                print(f"  ... dan {len(laporan[key]) - 20} lainnya (lihat file laporan)")
    if not laporan["errors"]:
        print("\n✅ Format YOLO valid.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Unduh, susun, dan validasi dataset YOLO deteksi helm.")
    p.add_argument("--source", help="URL atau path lokal (folder/.zip/.tar.gz). Default: DATASET_URL dari .env")
    p.add_argument("--data-dir", default="data", type=Path, help="folder tujuan dataset (default: data)")
    p.add_argument("--config", default="configs/data.yaml", type=Path, help="file data.yaml proyek")
    p.add_argument("--report", default="results/data_report.json", type=Path, help="file laporan JSON")
    p.add_argument("--split", nargs=3, type=float, default=(0.8, 0.1, 0.1), metavar=("TRAIN", "VAL", "TEST"),
                   help="rasio split jika dataset belum terbagi (default: 0.8 0.1 0.1)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--sync-names", action="store_true",
                   help="salin nama kelas dari data.yaml bawaan dataset ke --config")
    p.add_argument("--force", action="store_true", help="hapus isi --data-dir yang sudah ada lalu susun ulang")
    p.add_argument("--validate-only", action="store_true", help="hanya validasi --data-dir tanpa mengunduh")
    p.add_argument("--skip-image-check", action="store_true", help="lewati pengecekan file gambar rusak")
    args = p.parse_args(argv)
    if abs(sum(args.split) - 1.0) > 1e-6:
        p.error("jumlah rasio --split harus 1.0")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv opsional; variabel environment biasa tetap terbaca

    config = yaml.safe_load(args.config.read_text())
    names = normalize_names(config["names"])

    if not args.validate_only:
        source = args.source or os.getenv("DATASET_URL")
        if not source:
            print("❌ Tidak ada source. Pakai --source atau isi DATASET_URL di file .env")
            return 2
        sudah_ada = (args.data_dir / "images").exists()
        if sudah_ada and not args.force:
            print(f"❌ {args.data_dir}/images sudah ada. Pakai --force untuk menyusun ulang, "
                  "atau --validate-only untuk validasi saja.")
            return 2
        for sub in ("images", "labels"):
            shutil.rmtree(args.data_dir / sub, ignore_errors=True)

        try:
            raw_root = acquire(source, args.data_dir / "_raw")
        except (OSError, ValueError) as e:  # gagal unduh, file tidak ada, atau arsip tidak aman
            print(f"❌ Gagal mengambil dataset: {e}")
            return 1
        src_names = find_source_names(raw_root)
        if src_names and src_names != names:
            if args.sync_names:
                write_config_names(args.config, src_names)
                names = src_names
                print(f"Nama kelas di {args.config} diperbarui: {names}")
            else:
                print(f"⚠️  Nama kelas dataset {src_names} berbeda dengan {args.config} {names}. "
                      "Periksa urutannya, atau jalankan ulang dengan --sync-names.")

        per_split = find_images(raw_root)
        if not per_split:
            print(f"❌ Tidak menemukan gambar di dalam folder 'images' pada {raw_root}")
            return 1
        print("Split ditemukan:", {k or "(tanpa split)": len(v) for k, v in per_split.items()})
        yatim_sumber = find_orphan_labels(raw_root)
        organize(assign_splits(per_split, args.split, args.seed), args.data_dir)

    laporan = validate(args.data_dir, names, check_images=not args.skip_image_check)
    if not args.validate_only and yatim_sumber:
        contoh = [str(p.relative_to(raw_root)) for p in yatim_sumber[:3]]
        laporan["errors"].append(
            f"[sumber] {len(yatim_sumber)} label tanpa gambar tidak ikut disalin, mis. {contoh}")
    print_report(laporan)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(laporan, indent=2, ensure_ascii=False, default=str))
    print(f"\nLaporan disimpan di {args.report}")
    return 1 if laporan["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
