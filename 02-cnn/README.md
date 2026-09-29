# 02 — Convolutional Neural Network (CNN)

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami CNN untuk klasifikasi gambar dan memanfaatkan transfer learning.

## Notebook

Kedua notebook dirancang untuk **Google Colab dengan GPU** (Runtime → Change runtime type → T4 GPU). Sel pertama tiap notebook mengecek ketersediaan GPU.

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_cnn_dari_nol.ipynb](01_cnn_dari_nol.ipynb) | CIFAR-10: konvolusi, pooling, rumus & pelacakan ukuran output tiap layer, data augmentation, CNN dengan BatchNorm, akurasi per kelas | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/02-cnn/01_cnn_dari_nol.ipynb) |
| 02 | [02_transfer_learning.ipynb](02_transfer_learning.ipynb) | Flowers102: fine-tune ResNet18 pretrained, perbandingan *freeze backbone* vs *fine-tune semua layer* | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/02-cnn/02_transfer_learning.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` untuk memakai subset sangat kecil dan 1 epoch.

## Topik

- [ ] Konvolusi, padding, stride, pooling — *notebook 01*
- [ ] Arsitektur klasik: LeNet, VGG, ResNet — *notebook 02 (ResNet)*
- [ ] Data augmentation dengan torchvision.transforms — *notebook 01, 02*
- [ ] Transfer learning dan fine-tuning model pretrained — *notebook 02*
- [ ] Evaluasi: confusion matrix, precision/recall — *notebook 01 (akurasi per kelas), latihan modul 01*
