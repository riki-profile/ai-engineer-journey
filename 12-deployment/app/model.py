"""Tokenizer, model sentimen kecil, dan `Prediktor` untuk serving (modul 12).

Dipakai bersama oleh notebook, API FastAPI (`main.py`), UI Gradio (`ui_gradio.py`),
dan skrip training (`latih.py`).

Serving bisa memakai dua backend:
- ONNX Runtime (`model.onnx`): ringan, tanpa PyTorch. Dipakai di image Docker.
- PyTorch (`model.pt`): dipakai saat belajar/eksperimen.
PyTorch hanya diimpor jika backend PyTorch dipakai, sehingga image produksi tidak perlu torch.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

LABELS = ["negatif", "netral", "positif"]
PAD, UNK = 0, 1
MAKS_TOKEN = 64


def tokenisasi(teks: str) -> list[str]:
    """Kata (huruf kecil) + bigram kata, seperti ide fastText: "tidak enak" jadi fitur tersendiri."""
    kata = re.findall(r"\w+", teks.lower())
    return kata + [f"{a}_{b}" for a, b in zip(kata, kata[1:])]


class Vocab:
    def __init__(self, token_ke_id: dict[str, int]):
        self.token_ke_id = token_ke_id

    @classmethod
    def bangun(cls, kumpulan_teks: list[str], min_frek: int = 2) -> "Vocab":
        hitung = Counter(t for teks in kumpulan_teks for t in tokenisasi(teks))
        token = sorted(t for t, n in hitung.items() if n >= min_frek)
        return cls({"<pad>": PAD, "<unk>": UNK, **{t: i + 2 for i, t in enumerate(token)}})

    def __len__(self) -> int:
        return len(self.token_ke_id)

    def encode(self, teks: str) -> list[int]:
        ids = [self.token_ke_id.get(t, UNK) for t in tokenisasi(teks)][:MAKS_TOKEN]
        return ids or [UNK]

    def batch(self, kumpulan_teks: list[str]) -> np.ndarray:
        """Ubah beberapa teks menjadi matriks ID [batch, panjang] dengan padding 0."""
        semua = [self.encode(t) for t in kumpulan_teks]
        panjang = max(len(ids) for ids in semua)
        return np.array([ids + [PAD] * (panjang - len(ids)) for ids in semua], dtype=np.int64)


def buat_model(n_vocab: int, dim: int = 64, n_kelas: int = len(LABELS)):
    """Model PyTorch: embedding → rata-rata (mengabaikan padding) → MLP kecil."""
    import torch
    import torch.nn as nn

    class ModelSentimen(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(n_vocab, dim, padding_idx=PAD)
            self.mlp = nn.Sequential(nn.Linear(dim, dim), nn.ReLU(), nn.Dropout(0.3), nn.Linear(dim, n_kelas))

        def forward(self, ids: torch.Tensor) -> torch.Tensor:
            mask = (ids != PAD).unsqueeze(-1).float()
            rata = (self.emb(ids) * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
            return self.mlp(rata)

    return ModelSentimen()


def softmax(logits: np.ndarray) -> np.ndarray:
    e = np.exp(logits - logits.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


class Prediktor:
    """Memuat artefak dari satu folder dan memprediksi sentimen sekumpulan teks."""

    def __init__(self, folder: str | Path = "artefak", backend: str = "auto"):
        folder = Path(folder)
        self.config = json.loads((folder / "config.json").read_text())
        self.vocab = Vocab(json.loads((folder / "vocab.json").read_text()))
        if backend == "auto":
            backend = "onnx" if (folder / "model.onnx").exists() else "torch"
        self.backend = backend
        if backend == "onnx":
            import onnxruntime as ort
            self.sesi = ort.InferenceSession(str(folder / "model.onnx"), providers=["CPUExecutionProvider"])
        else:
            import torch
            self.model = buat_model(len(self.vocab), self.config["dim"])
            self.model.load_state_dict(torch.load(folder / "model.pt", map_location="cpu"))
            self.model.eval()

    def logits(self, kumpulan_teks: list[str]) -> np.ndarray:
        ids = self.vocab.batch(kumpulan_teks)
        if self.backend == "onnx":
            return self.sesi.run(None, {"ids": ids})[0]
        import torch
        with torch.no_grad():
            return self.model(torch.from_numpy(ids)).numpy()

    def prediksi(self, kumpulan_teks: list[str]) -> list[dict]:
        prob = softmax(self.logits(kumpulan_teks))
        return [{"label": LABELS[int(p.argmax())], "skor": {lab: round(float(s), 4) for lab, s in zip(LABELS, p)}}
                for p in prob]
