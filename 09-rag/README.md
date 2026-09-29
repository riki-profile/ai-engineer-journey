# 09 — Retrieval-Augmented Generation (RAG)

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Membangun sistem tanya-jawab yang menggabungkan retrieval dan LLM.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_chunking_dan_retrieval.ipynb](01_chunking_dan_retrieval.ipynb) | Pipeline RAG, 3 strategi chunking (tetap, kalimat, per bagian), dense retrieval dengan e5, recall@k & MRR, BM25, hybrid search (RRF), reranking cross-encoder, analisis kegagalan. Tanpa API key. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/09-rag/01_chunking_dan_retrieval.ipynb) |
| 02 | [02_rag_dengan_claude.ipynb](02_rag_dengan_claude.ipynb) | Tanpa vs dengan RAG, prompt RAG (konteks XML, grounding, sitasi), pertanyaan yang tidak bisa dijawab, output terstruktur (`jawaban`/`sumber`/`ditemukan`), pengaruh `k`, query rewriting untuk percakapan, biaya, prompt injection lewat dokumen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/09-rag/02_rag_dengan_claude.ipynb) |
| 03 | [03_evaluasi_rag.ipynb](03_evaluasi_rag.ipynb) | Evaluasi per komponen: recall@k, LLM-as-judge (kebenaran & faithfulness), akurasi abstain, biaya & latensi; membandingkan 2 konfigurasi; memilah gagal retrieval vs gagal generation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/09-rag/03_evaluasi_rag.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

Notebook 02 dan 03 memanggil **Claude API** (`claude-opus-5-5`, dengan refusal fallback seperti di modul 08). Simpan `ANTHROPIC_API_KEY` di Colab Secrets atau `.env` (lihat [README modul 08](../08-llm-basics/README.md#api-key-notebook-02--03)). Perkiraan biaya: notebook 02 < US$1, notebook 03 sekitar US$1–2 untuk seluruh pertanyaan uji.

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (notebook 01: kandidat rerank lebih sedikit; notebook 03: 5 pertanyaan). CI menjalankan ketiga notebook di job **notebook berat** (mengunduh model dari Hugging Face), dengan server tiruan pengganti Claude API.

## Korpus: Toko Elektronik Nusantara (fiktif)

Folder [`korpus/`](korpus/) berisi:
- `dokumen/`: 10 dokumen panduan layanan toko **fiktif** "Toko Elektronik Nusantara (TEN)" dalam Markdown (pengembalian, garansi, pengiriman, pembayaran, member, tukar tambah, servis, akun, promo, privasi), ±1.900 kata.
- `pertanyaan_uji.jsonl`: 27 pertanyaan uji dengan `jawaban_acuan`, kutipan `bukti` yang persis ada di dokumen, dan `jenis` (`fakta`, `parafrase`, `multi_dokumen`, `tidak_ada`).

Toko sengaja fiktif agar LLM tidak mungkin tahu jawabannya dari data pretraining, sehingga manfaat RAG dan kemampuan menolak menjawab bisa diukur dengan jelas. Korpus ditulis khusus untuk repo ini dan mengikuti lisensi repo. Di Colab, file korpus diunduh otomatis dari GitHub.

## Model & Lisensi

- Embedding [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small): MIT.
- Reranker [`BAAI/bge-reranker-v2-m3`](https://huggingface.co/BAAI/bge-reranker-v2-m3): Apache-2.0 (±2 GB, hanya notebook 01).
- Library: `sentence-transformers` (Apache-2.0), `rank_bm25` (Apache-2.0), `anthropic` (MIT), `pydantic` (MIT).

## Topik

- [ ] Pipeline RAG: ingest, chunking, embedding, retrieval, generation — *notebook 01, 02*
- [ ] Strategi chunking — *notebook 01*
- [ ] Reranking dan hybrid search — *notebook 01*
- [ ] Evaluasi RAG (faithfulness, relevance) — *notebook 03*
- [ ] Membangun aplikasi RAG end-to-end — *notebook 02 (dan Latihan)*
