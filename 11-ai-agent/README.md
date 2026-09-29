# 11 — AI Agent

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Membangun agent berbasis LLM yang dapat memakai tools dan menyelesaikan tugas multi-langkah.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_agent_loop_dari_nol.ipynb](01_agent_loop_dari_nol.ipynb) | Agen analis data untuk database SQLite toko fiktif: loop reason → act → observe dari nol dengan jejak per langkah, tool SQL read-only & kalkulator tanpa `eval`, verifikasi jawaban dengan SQL sendiri, pemulihan dari error, workflow (text-to-SQL) vs agent, biaya per langkah | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/11-ai-agent/01_agent_loop_dari_nol.ipynb) |
| 02 | [02_memori_state_dan_mcp.ipynb](02_memori_state_dan_mcp.ipynb) | Memori jangka pendek (pertumbuhan konteks, ringkasan riwayat), memori jangka panjang antarsesi (tool baca/simpan ingatan), state tugas (rencana yang diperbarui agen), Model Context Protocol: server MCP sendiri + client + `async_mcp_tool` dengan tool runner, perbandingan framework agent | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/11-ai-agent/02_memori_state_dan_mcp.ipynb) |
| 03 | [03_guardrails_dan_evaluasi.ipynb](03_guardrails_dan_evaluasi.ipynb) | Guardrail di level sistem: authorizer SQLite (tolak tulis/DROP/ATTACH/PRAGMA, kolom data pribadi terbaca `NULL`), aksi tulis dengan persetujuan manusia + log audit, uji prompt injection & red-team otomatis, batas langkah & anggaran, evaluasi agen dengan jawaban acuan dari SQL (kebenaran, langkah, error tool, biaya) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/11-ai-agent/03_guardrails_dan_evaluasi.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

Semua notebook memanggil **Claude API** (`claude-opus-5-5`, dengan refusal fallback seperti modul 08) dan tidak butuh GPU. Simpan `ANTHROPIC_API_KEY` di Colab Secrets atau `.env` (lihat [README modul 08](../08-llm-basics/README.md#api-key-notebook-02--03)). Perkiraan biaya: < US$1 per notebook untuk 01–02, US$1–2 untuk 03. CI menjalankan ketiganya terhadap [server tiruan](../scripts/fake_anthropic_server.py) (job `notebooks`), sehingga jalur kodenya teruji tanpa API key, tetapi kualitas jawaban agen tidak.

## File Pendukung

- [`toko_db.py`](toko_db.py): membuat database SQLite `toko.db` untuk toko **fiktif** "Toko Elektronik Nusantara" (produk, pelanggan, pesanan, item pesanan, ulasan; Januari 2025 – Juni 2026) dengan seed tetap. Semua nama, email, dan nomor telepon dibuat acak. Satu ulasan sengaja berisi *prompt injection* untuk latihan guardrail.
- [`server_toko.py`](server_toko.py): server MCP baca-saja (`lihat_skema`, `jalankan_sql`), bisa dipasang juga di Claude Desktop atau Claude Code.
- Di Colab, kedua file diunduh otomatis dari GitHub. `toko.db` dan `ingatan.json` yang dibuat notebook diabaikan oleh `.gitignore`.

## Lisensi

Library: `anthropic` (MIT), `mcp` (MIT), `pandas` (BSD-3-Clause). Data sepenuhnya sintetis dan mengikuti lisensi repo.

## Topik

- [ ] Konsep agent loop (reason → act → observe) — *notebook 01*
- [ ] Tool use / function calling — *notebook 01 (lanjutan modul 08)*
- [ ] Memory dan state — *notebook 02*
- [ ] Framework agent dan Model Context Protocol (MCP) — *notebook 02*
- [ ] Evaluasi dan keamanan agent (guardrails) — *notebook 03*
