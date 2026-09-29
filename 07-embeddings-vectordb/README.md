# 07 — Embeddings & Vector Database

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Merepresentasikan teks/gambar sebagai vektor dan mencarinya secara efisien.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_embeddings_dan_similarity.ipynb](01_embeddings_dan_similarity.ipynb) | Cosine/dot/euclidean, sentence-transformers multibahasa, mean pooling manual (diverifikasi), semantic search vs TF-IDF, evaluasi recall@k & MRR lintas bahasa (Inggris → Indonesia), visualisasi PCA | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/07-embeddings-vectordb/01_embeddings_dan_similarity.ipynb) |
| 02 | [02_ann_faiss_hnsw.ipynb](02_ann_faiss_hnsw.ipynb) | Brute force vs ANN dengan FAISS: IVF, HNSW, PQ; kurva recall vs latensi vs memori; simpan/muat index. Tanpa GPU & tanpa unduhan. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/07-embeddings-vectordb/02_ann_faiss_hnsw.ipynb) |
| 03 | [03_vector_db.ipynb](03_vector_db.ipynb) | Chroma & Qdrant: metadata, filter, CRUD, persistensi; pgvector (contoh SQL); mini aplikasi pencarian ulasan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/07-embeddings-vectordb/03_vector_db.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (notebook 02: data lebih kecil).

## Data & Lisensi

- **NusaX-Senti** (paralel Indonesia–Inggris, [IndoNLP/nusax](https://github.com/IndoNLP/nusax)): lisensi data **CC-BY-SA**, diunduh langsung dari GitHub.
- Model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`: Apache-2.0.
- Library: `sentence-transformers` (Apache-2.0), `faiss-cpu` (MIT), `chromadb` (Apache-2.0), `qdrant-client` (Apache-2.0); pgvector berlisensi PostgreSQL License.

## Topik

- [ ] Konsep embedding dan similarity (cosine, dot product) — *notebook 01*
- [ ] Sentence embeddings (sentence-transformers) — *notebook 01*
- [ ] Approximate nearest neighbor (FAISS, HNSW) — *notebook 02*
- [ ] Vector database (Chroma, Qdrant, pgvector) — *notebook 03*
- [ ] Semantic search sederhana — *notebook 01, 03*
