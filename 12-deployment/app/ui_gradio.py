"""Demo UI dengan Gradio (modul 12).

Lokal:  python ui_gradio.py   → buka alamat yang dicetak.
Hugging Face Spaces: file ini dipakai sebagai app.py (lihat notebook 03).
"""

from __future__ import annotations

import os

import gradio as gr

from model import Prediktor

prediktor = Prediktor(os.getenv("FOLDER_MODEL", "artefak"))


def analisis(teks: str) -> dict[str, float]:
    if not teks.strip():
        return {}
    return prediktor.prediksi([teks[:2000]])[0]["skor"]      # gr.Label menampilkan skor per kelas


demo = gr.Interface(
    fn=analisis,
    inputs=gr.Textbox(label="Kalimat berbahasa Indonesia", lines=3),
    outputs=gr.Label(label="Sentimen"),
    title="Analisis Sentimen Bahasa Indonesia",
    description="Model kecil (embedding + MLP) yang dilatih pada NusaX-Senti. Contoh modul 12 ai-engineer-journey.",
    examples=[["Pengirimannya cepat dan barangnya bagus!"], ["Pelayanannya lambat, saya kecewa."],
              ["Barang sudah sampai hari ini."]],
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch()
