# 10 — Fine-tuning LLM

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Menyesuaikan LLM untuk tugas tertentu secara efisien.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_kapan_finetuning_dan_lora_dari_nol.ipynb](01_kapan_finetuning_dan_lora_dari_nol.ipynb) | Prompting vs RAG vs fine-tuning, hitungan memori (full FT vs LoRA vs QLoRA), intuisi low-rank dengan SVD, `LoRALinear` dari nol (diverifikasi terhadap `peft`, merge), eksperimen FashionMNIST → MNIST: hanya layer terakhir vs LoRA r=1/4/16 vs full FT dan catastrophic forgetting, kuantisasi absmax 8/4/3/2-bit. Cukup CPU. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/10-llm-finetuning/01_kapan_finetuning_dan_lora_dari_nol.ipynb) |
| 02 | [02_sft_lora_qwen_sentimen.ipynb](02_sft_lora_qwen_sentimen.ipynb) | SFT `Qwen2.5-0.5B-Instruct` dengan LoRA (`peft` + `SFTTrainer` dari TRL) untuk sentimen NusaX: format prompt–completion (loss hanya di jawaban), baseline sebelum vs sesudah (akurasi, macro-F1, validitas format), kurva loss, cek efek samping dengan `disable_adapter()`, simpan/muat/merge adapter, konfigurasi QLoRA | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/10-llm-finetuning/02_sft_lora_qwen_sentimen.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Notebook 02 butuh GPU (Colab T4, training ±5 menit). Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (subset sangat kecil dan beberapa langkah training; hasilnya tidak bermakna). Di CI, notebook 01 berjalan di job `notebooks` dan notebook 02 di job `notebooks-berat`.

## Data & Lisensi

- **FashionMNIST** (MIT) dan **MNIST** (CC BY-SA 3.0), diunduh lewat `torchvision`.
- **NusaX-Senti** bahasa Indonesia ([IndoNLP/nusax](https://github.com/IndoNLP/nusax)): **CC-BY-SA**, diunduh dari GitHub. Adapter yang dilatih dari data ini sebaiknya dibagikan dengan mencantumkan sumber dan lisensi data.
- Model [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct): Apache-2.0.
- Library: `peft` dan `trl` (Apache-2.0), `transformers` (Apache-2.0). QLoRA memakai `bitsandbytes` (MIT), tidak dijalankan di notebook.
- Folder hasil training (`hasil_sft/`, `adapter_sentimen/`) diabaikan oleh `.gitignore`.

## Topik

- [ ] Kapan perlu fine-tuning vs prompting vs RAG — *notebook 01*
- [ ] Supervised fine-tuning (SFT) dan format dataset — *notebook 02*
- [ ] Parameter-efficient fine-tuning: LoRA, QLoRA — *notebook 01, 02*
- [ ] Library: PEFT, TRL — *notebook 01, 02*
- [ ] Evaluasi hasil fine-tuning — *notebook 02*
