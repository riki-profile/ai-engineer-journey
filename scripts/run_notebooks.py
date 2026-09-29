"""Menjalankan notebook dengan QUICK_RUN=1 dan melaporkan error (dipakai CI & lokal).

Contoh (dari root repo):
    python scripts/run_notebooks.py 01-deep-learning/*.ipynb
    python scripts/run_notebooks.py --check-clean $(git ls-files '*.ipynb')

--check-clean hanya memeriksa bahwa notebook di-commit TANPA output
(repo ini menyimpan notebook bersih; output dibuat saat dijalankan di Colab).
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import nbformat


def check_clean(paths: list[Path]) -> int:
    kotor = []
    for p in paths:
        nb = nbformat.read(p, as_version=4)
        n = sum(len(c.get("outputs", [])) for c in nb.cells if c.cell_type == "code")
        eksekusi = any(c.get("execution_count") for c in nb.cells if c.cell_type == "code")
        if n or eksekusi:
            kotor.append(f"{p}: {n} output tersimpan")
    for k in kotor:
        print(f"❌ {k}")
    print(f"{'❌' if kotor else '✅'} {len(paths) - len(kotor)}/{len(paths)} notebook bersih dari output")
    return 1 if kotor else 0


def run(paths: list[Path], timeout: int) -> int:
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    os.environ["QUICK_RUN"] = "1"
    gagal = []
    for p in paths:
        nb = nbformat.read(p, as_version=4)
        mulai = time.time()
        try:
            # Jalankan dengan folder notebook sebagai folder kerja, sama seperti di Jupyter/Colab
            NotebookClient(nb, timeout=timeout, kernel_name="python3",
                           resources={"metadata": {"path": str(p.parent)}}).execute()
            print(f"✅ {p} ({time.time() - mulai:.0f} detik)", flush=True)
        except CellExecutionError as e:
            print(f"❌ {p} ({time.time() - mulai:.0f} detik)\n{str(e)[-3000:]}", flush=True)
            gagal.append(p)
        except Exception as e:  # noqa: BLE001 - timeout, kernel mati, dll.
            print(f"❌ {p}: {type(e).__name__}: {e}", flush=True)
            gagal.append(p)
    print(f"\n{len(paths) - len(gagal)}/{len(paths)} notebook berhasil")
    return 1 if gagal else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("notebooks", nargs="+", type=Path)
    p.add_argument("--check-clean", action="store_true", help="hanya cek notebook tanpa output")
    p.add_argument("--timeout", type=int, default=1800, help="batas waktu per sel (detik)")
    args = p.parse_args()
    paths = sorted(set(args.notebooks))
    return check_clean(paths) if args.check_clean else run(paths, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
