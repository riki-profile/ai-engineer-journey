# 08 — Dasar Large Language Model

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami cara kerja LLM dan cara menggunakannya lewat API maupun model lokal.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_cara_kerja_llm.ipynb](01_cara_kerja_llm.ipynb) | Tokenisasi (Indonesia vs Inggris), logits & next-token prediction, loop generasi greedy manual vs `generate()`, temperature/top-k/top-p dari nol + visualisasi, context window & KV cache, chat template. Model lokal Qwen2.5-0.5B-Instruct, tanpa API key. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/08-llm-basics/01_cara_kerja_llm.ipynb) |
| 02 | [02_claude_api_dasar.ipynb](02_claude_api_dasar.ipynb) | Claude API dengan SDK `anthropic`: API key dari Colab Secrets/`.env`, anatomi respons, system prompt, prompt engineering yang diukur (instruksi jelas, tag XML, few-shot), multi-giliran, streaming, effort & thinking, token & biaya, penanganan error, refusal fallback | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/08-llm-basics/02_claude_api_dasar.ipynb) |
| 03 | [03_structured_output_dan_tool_use.ipynb](03_structured_output_dan_tool_use.ipynb) | Structured output (Pydantic + `messages.parse`, JSON schema), tool use langkah demi langkah, loop agen dengan `strict` tools & `is_error`, tool runner `@beta_tool`, keamanan tool use (prompt injection, human-in-the-loop) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/08-llm-basics/03_structured_output_dan_tool_use.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

## API Key (notebook 02 & 03)

Notebook 02 dan 03 memanggil **Claude API** (berbayar per token; menjalankan kedua notebook diperkirakan menghabiskan sekitar US$1–2). Buat API key di [Claude Console](https://platform.claude.com/), lalu simpan **tanpa menuliskannya di kode**:

- **Colab:** ikon 🔑 **Secrets** → tambah `ANTHROPIC_API_KEY` → aktifkan *Notebook access*.
- **Lokal:** `cp .env.example .env` di root repo, lalu isi `ANTHROPIC_API_KEY=...`. File `.env` diabaikan oleh `.gitignore`.

Model yang dipakai: `claude-opus-5-5`. Permintaan dikirim dengan **refusal fallback** (`fallbacks="default"`, fitur beta): jika model menolak permintaan, server otomatis mencoba ulang di model cadangan yang direkomendasikan Anthropic.

**Pengujian tanpa API key.** CI menjalankan notebook 02 dan 03 terhadap [server tiruan](../scripts/fake_anthropic_server.py) yang meniru bentuk respons Messages API (teks/JSON dummy). Ini memastikan kode notebook berjalan, tetapi tidak menilai kualitas jawaban. Menjalankannya secara lokal:

```bash
python scripts/fake_anthropic_server.py --port 8765 &
ANTHROPIC_BASE_URL=http://127.0.0.1:8765 ANTHROPIC_API_KEY=kunci-uji \
  python scripts/run_notebooks.py 08-llm-basics/02_claude_api_dasar.ipynb 08-llm-basics/03_structured_output_dan_tool_use.ipynb
```

> Uji cepat notebook 01 tanpa GPU: set environment variable `QUICK_RUN=1` (teks yang digenerate lebih pendek).

## Data & Lisensi

- Model [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct): **Apache-2.0**, diunduh dari Hugging Face (±1 GB).
- Ulasan produk dan katalog toko di notebook 02–03 ditulis sendiri untuk notebook ini (fiktif).
- Library: `transformers` (Apache-2.0), `anthropic` (MIT), `python-dotenv` (BSD-3-Clause), `pydantic` (MIT).
- Pemakaian Claude API tunduk pada ketentuan layanan Anthropic.

## Topik

- [ ] Cara kerja LLM: next-token prediction, context window — *notebook 01*
- [ ] Prompt engineering dasar — *notebook 02*
- [ ] Parameter sampling: temperature, top-p — *notebook 01*
- [ ] Menggunakan LLM via API (dengan API key di .env) — *notebook 02*
- [ ] Menjalankan model open-source kecil secara lokal — *notebook 01*
- [ ] Structured output dan tool/function calling — *notebook 03*
