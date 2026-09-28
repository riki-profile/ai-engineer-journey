# 01 — Deep Learning Dasar

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami dasar neural network dan cara melatihnya dengan PyTorch.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_tensor_autograd.ipynb](01_tensor_autograd.ipynb) | Tensor, operasi dasar, GPU/device, autograd, gradient descent manual untuk regresi linear | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/01-deep-learning/01_tensor_autograd.ipynb) |
| 02 | [02_training_loop_manual.ipynb](02_training_loop_manual.ipynb) | Klasifikasi FashionMNIST: `nn.Module` sendiri, training & validasi loop manual, grafik loss/akurasi, contoh prediksi | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/01-deep-learning/02_training_loop_manual.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (atau tulis `QUICK_RUN = True` di notebook 02) untuk memakai subset kecil data dan 1 epoch.

## Topik

- [ ] Tensor dan operasi dasar di PyTorch — *notebook 01*
- [ ] Autograd dan backpropagation — *notebook 01*
- [ ] Fungsi aktivasi dan loss function — *notebook 02*
- [ ] Optimizer (SGD, Adam) dan learning rate — *notebook 01, 02*
- [ ] Training loop, validasi, overfitting, regularisasi (dropout, weight decay) — *notebook 02*
- [ ] MLP untuk klasifikasi sederhana (FashionMNIST) — *notebook 02*
