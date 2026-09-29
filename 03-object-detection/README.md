# 03 — Object Detection

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Mendeteksi dan melokalisasi objek dalam gambar menggunakan model modern.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_konsep_deteksi.ipynb](01_konsep_deteksi.ipynb) | Format bounding box, IoU (implementasi sendiri), NMS, precision/recall, kurva PR, AP, mAP50 & mAP50-95 dengan contoh angka. Tanpa GPU. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/03-object-detection/01_konsep_deteksi.ipynb) |
| 02 | [02_yolo_inference.ipynb](02_yolo_inference.ipynb) | Inference YOLO11n pretrained COCO, membedah `Results`, menggambar bounding box sendiri, efek `conf`/`iou`/`classes`, perbandingan dengan YOLO26n | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/03-object-detection/02_yolo_inference.ipynb) |
| 03 | [03_format_dataset_yolo.ipynb](03_format_dataset_yolo.ipynb) | Format anotasi YOLO (`.txt` & `data.yaml`), dataset sintetis kecil, konversi COCO/VOC → YOLO, validasi label, training singkat | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/03-object-detection/03_format_dataset_yolo.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (notebook 03: dataset lebih kecil dan 1 epoch training).

## ⚖️ Catatan Lisensi: Ultralytics (AGPL-3.0)

Notebook 02 dan 03 memakai library [`ultralytics`](https://github.com/ultralytics/ultralytics), yang berlisensi **[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)**. Hal ini juga berlaku untuk bobot model YOLO yang disediakan Ultralytics.

- ✅ Bebas dipakai untuk belajar, riset, dan proyek open-source.
- ⚠️ Jika kode atau model yang memakai `ultralytics` dipakai dalam produk atau layanan (termasuk layanan web/API), AGPL-3.0 mewajibkan seluruh kode sumber proyek tersebut dibuka dengan lisensi yang kompatibel.
- 💼 Untuk penggunaan komersial tertutup, diperlukan [Ultralytics Enterprise License](https://www.ultralytics.com/license), atau pakai detektor berlisensi permisif (misalnya model deteksi di `torchvision`, BSD-3-Clause).

## Topik

- [ ] Bounding box, IoU, dan Non-Maximum Suppression — *notebook 01*
- [ ] Metrik mAP — *notebook 01*
- [ ] Keluarga detektor: two-stage (Faster R-CNN) vs one-stage (YOLO) — *notebook 02 (YOLO)*
- [ ] Inferensi dan training YOLO dengan Ultralytics — *notebook 02, 03*
- [ ] Format anotasi dataset (YOLO, COCO) — *notebook 03*
