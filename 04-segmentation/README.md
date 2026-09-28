# 04 — Image Segmentation

**Status:** 🟨 Sedang berjalan

## Tujuan Belajar

Memahami segmentasi gambar pada level piksel.

## Notebook

| No | Notebook | Isi | Colab |
|----|----------|-----|-------|
| 01 | [01_konsep_segmentasi.ipynb](01_konsep_segmentasi.ipynb) | Semantic vs instance vs panoptic, representasi mask (indeks, one-hot, poligon YOLO-seg, RLE COCO), pixel accuracy vs IoU/mIoU/Dice dari confusion matrix. Tanpa GPU. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/04-segmentation/01_konsep_segmentasi.ipynb) |
| 02 | [02_unet_dari_nol.ipynb](02_unet_dari_nol.ipynb) | U-Net dari nol di Oxford-IIIT Pet: transformasi tersinkron gambar–mask, pelacakan ukuran encoder/decoder/skip, loss CE + soft Dice, evaluasi mIoU | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/04-segmentation/02_unet_dari_nol.ipynb) |
| 03 | [03_yolo_seg_dan_sam.ipynb](03_yolo_seg_dan_sam.ipynb) | Instance segmentation YOLO11n-seg (mask, poligon, label YOLO-seg), SAM dengan prompt titik/kotak/titik negatif, pipeline YOLO → SAM | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riki-profile/ai-engineer-journey/blob/main/04-segmentation/03_yolo_seg_dan_sam.ipynb) |

Setiap notebook diakhiri bagian **Latihan** (3 soal).

> Uji cepat tanpa GPU: set environment variable `QUICK_RUN=1` (notebook 02: subset sangat kecil dan 1 epoch).

## Catatan Lisensi

Notebook 03 memakai `ultralytics` (**AGPL-3.0**, termasuk bobot YOLO). Bobot asli SAM, SAM 2, dan MobileSAM dirilis dengan Apache-2.0. Lihat juga catatan lisensi di [modul 03](../03-object-detection/README.md).

## Topik

- [ ] Semantic vs instance vs panoptic segmentation — *notebook 01*
- [ ] Arsitektur U-Net dan encoder-decoder — *notebook 02*
- [ ] Mask R-CNN dan YOLO-seg — *notebook 03 (YOLO-seg)*
- [ ] Segment Anything Model (SAM) — *notebook 03*
- [ ] Metrik: IoU/Dice — *notebook 01, 02*
