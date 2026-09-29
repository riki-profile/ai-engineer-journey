"""Membuat dataset helm sintetis kecil untuk pengujian (pytest & CI).

Gambar berisi lingkaran (kelas 0, "With Helmet") dan persegi (kelas 1,
"Without Helmet") dengan label YOLO yang dijamin benar. Layout-nya meniru
ekspor Roboflow: train/images, valid/images, test/images + data.yaml.

Contoh:
    python tests/make_synthetic_dataset.py /tmp/helm.zip
"""

from __future__ import annotations

import random
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

NAMES = ["With Helmet", "Without Helmet"]


def make_roboflow_dir(root: Path, sizes=(("train", 24), ("valid", 6), ("test", 6)), img_size=96, seed=0) -> Path:
    rng = random.Random(seed)
    for split, n in sizes:
        (root / split / "images").mkdir(parents=True, exist_ok=True)
        (root / split / "labels").mkdir(parents=True, exist_ok=True)
        for i in range(n):
            img = Image.new("RGB", (img_size, img_size), tuple(rng.randint(150, 255) for _ in range(3)))
            draw = ImageDraw.Draw(img)
            baris = []
            for _ in range(rng.randint(1, 3)):
                k = rng.randint(0, 1)
                s = rng.randint(img_size // 6, img_size // 3)
                x, y = rng.randint(0, img_size - s), rng.randint(0, img_size - s)
                warna = tuple(rng.randint(0, 120) for _ in range(3))
                (draw.ellipse if k == 0 else draw.rectangle)([x, y, x + s, y + s], fill=warna)
                cx, cy, w = (x + s / 2) / img_size, (y + s / 2) / img_size, s / img_size
                baris.append(f"{k} {cx:.6f} {cy:.6f} {w:.6f} {w:.6f}")
            img.save(root / split / "images" / f"{split}_{i}.jpg")
            (root / split / "labels" / f"{split}_{i}.txt").write_text("\n".join(baris) + "\n")
    (root / "data.yaml").write_text(f"nc: {len(NAMES)}\nnames: {NAMES}\n")
    return root


def zip_dir(src: Path, zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w") as z:
        for f in sorted(src.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(src))
    return zip_path


if __name__ == "__main__":
    tujuan = Path(sys.argv[1] if len(sys.argv) > 1 else "helm_sintetis.zip").resolve()
    folder = tujuan.with_suffix("")
    make_roboflow_dir(folder)
    zip_dir(folder, tujuan)
    print(f"Dataset sintetis dibuat: {tujuan}")
