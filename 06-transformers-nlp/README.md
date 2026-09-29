# 06 — Transformers untuk NLP

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami arsitektur transformer dan penggunaannya untuk tugas NLP.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_tokenisasi.ipynb](01_tokenisasi.ipynb) | Karakter vs kata vs subword (masalah OOV), BPE dari nol, melatih tokenizer BPE & WordPiece dengan `tokenizers`, fertility tokenizer GPT-2/BERT/IndoBERT/XLM-R pada teks Indonesia, `input_ids`/`attention_mask`/padding. Tanpa GPU. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/06-transformers-nlp/01_tokenisasi.ipynb) |
| 02 | [02_transformer_decoder_dari_nol.ipynb](02_transformer_decoder_dari_nol.ipynb) | Encoder vs decoder vs encoder–decoder (BERT/GPT/T5), causal mask, positional encoding sinusoidal, mini-GPT tingkat karakter di tiny Shakespeare, generasi dengan temperature & top-k | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/06-transformers-nlp/02_transformer_decoder_dari_nol.ipynb) |
| 03 | [03_finetune_indobert_sentimen.ipynb](03_finetune_indobert_sentimen.ipynb) | Baseline TF-IDF + Logistic Regression vs fine-tune IndoBERT dengan `Trainer` untuk sentimen bahasa Indonesia (NusaX), macro-F1, confusion matrix, analisis kesalahan, `pipeline` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/06-transformers-nlp/03_finetune_indobert_sentimen.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1`.

## Data & Lisensi

- **NusaX-Senti** (bahasa Indonesia, [IndoNLP/nusax](https://github.com/IndoNLP/nusax)): lisensi data **CC-BY-SA**. Diunduh langsung dari GitHub dan tidak disimpan di repo ini.
- **Tiny Shakespeare**: teks domain publik (diunduh dari repo `karpathy/char-rnn`).
- Library: `transformers`, `tokenizers`, `datasets`, `accelerate` (Apache-2.0).
- Model `indobenchmark/indobert-base-p1`: periksa lisensi di halaman model sebelum dipakai di luar keperluan belajar.

## Topik

- [ ] Tokenisasi (BPE, WordPiece) — *notebook 01*
- [ ] Attention, multi-head attention, arsitektur encoder-decoder — *notebook 02 (dan modul 05)*
- [ ] BERT, GPT, T5: perbedaan dan kegunaan — *notebook 02*
- [ ] Library Hugging Face Transformers — *notebook 01, 03*
- [ ] Fine-tuning untuk klasifikasi teks — *notebook 03*
