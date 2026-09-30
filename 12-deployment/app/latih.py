"""Melatih model sentimen kecil pada NusaX-Senti dan menyimpan artefak untuk serving.

Pemakaian (dari folder 12-deployment/app/):
    python latih.py                 # simpan ke artefak/ (model.pt, model.onnx, vocab.json, config.json)
    python latih.py --tanpa-onnx    # tanpa ekspor ONNX

Butuh: torch, pandas, onnx, onnxscript (untuk ekspor). Training hanya beberapa detik di CPU.
Data: NusaX-Senti (IndoNLP/nusax, lisensi CC-BY-SA), diunduh dari GitHub.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from model import LABELS, Vocab, buat_model

NUSAX_URL = "https://raw.githubusercontent.com/IndoNLP/nusax/main/datasets/sentiment/indonesian"
LABEL_ID = {"negative": 0, "neutral": 1, "positive": 2}


def muat_data(split: str) -> tuple[list[str], np.ndarray]:
    df = pd.read_csv(f"{NUSAX_URL}/{split}.csv")
    return df["text"].tolist(), df["label"].map(LABEL_ID).to_numpy().copy()   # salinan yang bisa ditulis


def akurasi(model, vocab, teks, label) -> float:
    import torch
    model.eval()
    with torch.no_grad():
        pred = model(torch.from_numpy(vocab.batch(teks))).argmax(1).numpy()
    return float((pred == label).mean())


def ekspor_onnx(model, vocab, path: Path) -> None:
    import onnx
    import torch
    contoh = torch.from_numpy(vocab.batch(["contoh kalimat", "contoh kalimat yang lebih panjang"]))
    # dynamic_shapes: ukuran batch dan panjang kalimat boleh berbeda-beda saat inference
    batch, panjang = torch.export.Dim("batch"), torch.export.Dim("panjang")
    torch.onnx.export(model.eval(), (contoh,), str(path), input_names=["ids"], output_names=["logits"],
                      dynamic_shapes=({0: batch, 1: panjang},), dynamo=True,
                      external_data=False)      # satu file .onnx (bobot tidak dipisah ke .onnx.data)
    # Buang info shape tensor perantara (value_info). Tidak dibutuhkan untuk inference, dan versi saat ini
    # membuat alat kuantisasi ONNX Runtime gagal ("Inferred shape and existing shape differ").
    graf = onnx.load(str(path))
    del graf.graph.value_info[:]
    onnx.save(graf, str(path))


def latih(folder: str | Path = "artefak", epoch: int = 40, dim: int = 64, seed: int = 0, onnx: bool = True) -> dict:
    import torch
    import torch.nn.functional as F

    torch.manual_seed(seed)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = (muat_data(s) for s in ["train", "valid", "test"])

    vocab = Vocab.bangun(x_train)
    model = buat_model(len(vocab), dim)
    opt = torch.optim.AdamW(model.parameters(), lr=5e-3, weight_decay=1e-4)
    ids_train, label_train = torch.from_numpy(vocab.batch(x_train)), torch.from_numpy(y_train)

    terbaik, state_terbaik = -1.0, None
    for _ in range(epoch):
        model.train()
        for idx in torch.randperm(len(x_train)).split(32):
            loss = F.cross_entropy(model(ids_train[idx]), label_train[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
        acc_val = akurasi(model, vocab, x_val, y_val)
        if acc_val > terbaik:                            # simpan bobot terbaik di data validasi
            terbaik, state_terbaik = acc_val, {k: v.clone() for k, v in model.state_dict().items()}
    model.load_state_dict(state_terbaik)

    metrik = {"akurasi_val": round(terbaik, 4), "akurasi_test": round(akurasi(model, vocab, x_test, y_test), 4)}
    config = {"versi": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"), "dim": dim, "n_vocab": len(vocab),
              "labels": LABELS, "data": "NusaX-Senti (CC-BY-SA)", **metrik}
    torch.save(model.state_dict(), folder / "model.pt")
    (folder / "vocab.json").write_text(json.dumps(vocab.token_ke_id, ensure_ascii=False))
    (folder / "config.json").write_text(json.dumps(config, indent=2))
    if onnx:
        ekspor_onnx(model, vocab, folder / "model.onnx")
    return config


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--folder", default="artefak")
    p.add_argument("--epoch", type=int, default=40)
    p.add_argument("--tanpa-onnx", action="store_true")
    args = p.parse_args()
    print(json.dumps(latih(args.folder, epoch=args.epoch, onnx=not args.tanpa_onnx), indent=2))
