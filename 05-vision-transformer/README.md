# 05 — Vision Transformer (ViT)

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami penerapan arsitektur transformer untuk computer vision.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_vit_dari_nol.ipynb](01_vit_dari_nol.ipynb) | Patch embedding (setara Conv2d), CLS token, positional embedding, self-attention & multi-head attention dari nol (diverifikasi terhadap PyTorch), mini-ViT di FashionMNIST, visualisasi attention & positional embedding | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/05-vision-transformer/01_vit_dari_nol.ipynb) |
| 02 | [02_finetune_vit_hf.ipynb](02_finetune_vit_hf.ipynb) | Fine-tune `google/vit-base-patch16-224-in21k` (Hugging Face) di Flowers102, mixed precision (AMP), attention rollout, `save_pretrained` & `push_to_hub` dengan token dari Colab Secrets | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/05-vision-transformer/02_finetune_vit_hf.ipynb) |
| 03 | [03_clip_zero_shot.ipynb](03_clip_zero_shot.ipynb) | CLIP (`open_clip`): embedding gambar–teks, zero-shot CIFAR-10, prompt engineering & ensembling, pencarian teks → gambar, linear probe dengan sedikit data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/05-vision-transformer/03_clip_zero_shot.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (subset kecil, 1 epoch).

## Catatan Lisensi

- `transformers` (Apache-2.0) dan bobot `google/vit-base-patch16-224-in21k` (Apache-2.0).
- `open_clip` (MIT) dan bobot CLIP OpenAI (MIT).

Semuanya kompatibel dengan lisensi AGPL-3.0 repo ini. Periksa lisensi di halaman model sebelum memakai model lain dari Hugging Face Hub.

## Topik

- [ ] Patch embedding dan positional encoding — *notebook 01*
- [ ] Self-attention pada gambar — *notebook 01, 02*
- [ ] ViT vs CNN: kelebihan dan kekurangan — *notebook 01, 02*
- [ ] Fine-tuning ViT pretrained (Hugging Face / timm) — *notebook 02*
- [ ] Model multimodal dasar (CLIP) — *notebook 03*
