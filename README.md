# Parkinson's Disease Classification: Multimodal vs. Image-Only

Transfer-learning experiments that compare eight pretrained image backbones for classifying Parkinson's disease (PD) from hand-drawn **spiral + wave** images, with and without a second input: **22 numerical voice-measurement features**.

> **Research / educational project. Not a medical device and not for diagnosis.**

## What's inside

| Notebook | What it does |
| --- | --- |
| `notebooks/1_MultimodalModels.ipynb` | Image backbone + voice-feature MLP, fused and trained end to end. Grouped train/val/test split. |
| `notebooks/2_ImageOnlyModels.ipynb` | Same eight backbones on the drawings only, using the `training/` and `testing/` folders. |
| `notebooks/3_MultimodalModels_Vs_ImageOnlyModels.ipynb` | Loads the saved results from notebooks 1 and 2 and compares them. |

Backbones (all ImageNet-pretrained, frozen): MobileNetV2, VGG16, VGG19, ResNet50V2, EfficientNetV2B0, Xception, InceptionResNetV2, ConvNeXtTiny.

## Repository structure

```text
.
├── data/
│   ├── metadata/parkinsons.csv      # 195 rows: voice features, label, image path
│   └── images/                      # training/ and testing/ x healthy/ and parkinson/
├── notebooks/
│   ├── 1_MultimodalModels.ipynb
│   ├── 2_ImageOnlyModels.ipynb
│   ├── 3_MultimodalModels_Vs_ImageOnlyModels.ipynb
│   └── model_comparison/            # saved results (.pkl) used by notebook 3
├── scripts/
│   └── validate_dataset.py          # checks the CSV and that every image exists
├── requirements.txt
└── README.md
```

## Data

- **Voice features** (`data/metadata/parkinsons.csv`): 195 recordings, 22 acoustic measures (MDVP jitter/shimmer, NHR, HNR, RPDE, DFA, spread1/2, D2, PPE, ...), label `status` (1 = Parkinson's: 147 rows, 0 = healthy: 48 rows). The columns match the UCI *Parkinson's Disease* voice dataset (Little et al., 2007).
- **Images** (`data/images/`): 102 spiral + wave drawings, 72 in `training/` and 30 in `testing/`, 36 + 36 and 15 + 15 per class.
- The CSV column `image_path` uses legacy Windows paths (e.g. `test\training\parkinson\008_sw.png`). The notebooks and `validate_dataset.py` normalize these automatically.


## Setup

Requires Python 3.10-3.12.

```bash
git clone https://github.com/Mehd1Rz/Parkinsons-multimodal-vs-image-classification.git
cd Parkinsons-multimodal-vs-image-classification

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Put the images in `data/images/` and check everything resolves:

   ```bash
   python scripts/validate_dataset.py
   ```

2. Launch Jupyter **from the repository root** and run the notebooks from the `notebooks/` folder, in order:

   ```bash
   jupyter lab
   ```

   Run `1_...` and `2_...` first (each saves a `.pkl` into `notebooks/model_comparison/`), then `3_...`. The `.pkl` files from the original run are included, so notebook 3 works without retraining.

All notebooks use `SEED = 42`. Each backbone trains for 20 epochs; the larger ones are slow without a GPU.

## Results (from the original run)

Test metrics, one run each. Multimodal test set: n = 38. Image-only test set: n = 30.

| Backbone | Multimodal acc | Image-only acc | Multimodal F1 | Image-only F1 | Multimodal AUC | Image-only AUC |
| --- | --- | --- | --- | --- | --- | --- |
| MobileNetV2 | 0.9211 | 0.7000 | 0.9455 | 0.7273 | 0.9607 | 0.7778 |
| VGG16 | 0.8158 | 0.6000 | 0.8571 | 0.3333 | 0.9214 | 0.7644 |
| VGG19 | 0.8947 | 0.6333 | 0.9231 | 0.6667 | 0.9786 | 0.7511 |
| ResNet50V2 | 0.8947 | 0.8333 | 0.9259 | 0.8387 | 0.9786 | 0.9467 |
| EfficientNetV2B0 | 0.9737 | 0.7667 | 0.9825 | 0.7586 | 0.9929 | 0.8400 |
| Xception | 0.9737 | 0.6667 | 0.9825 | 0.6875 | 0.9893 | 0.8711 |
| InceptionResNetV2 | 0.9474 | 0.8000 | 0.9643 | 0.8000 | 0.9893 | 0.9111 |
| ConvNeXtTiny | 0.9737 | 0.8667 | 0.9818 | 0.8571 | 0.9893 | 0.8978 |

## Limitations (please read before citing these numbers)

- **Tiny test sets.** One test sample is worth about 2.6 points of accuracy (n = 38) or 3.3 points (n = 30). Results come from a single run and a single split.
- **The two test sets differ**, so the multimodal and image-only columns are not a controlled comparison.
- **Image-only notebook has no separate validation set.** The test set is used as validation during training, so its curves and "best validation" numbers are optimistic.
- **Voice and image pairing is not per person.** In the CSV, the recordings of one subject point to several different drawings (all 32 subjects have more than one distinct image), and only 85 distinct images are shared by 195 rows (one image is reused up to 8 times). The labels agree with the image folders, but this pairing should not be read as drawings and voice from the same patient.
- **No subject-level split.** The multimodal split is grouped by image path, which stops the same image appearing in two partitions, but recordings from the same subject can still land in both train and test.
- **No voice-only baseline** is included, so the multimodal gain cannot be attributed to the drawings versus the voice features.

## Citation

Voice features: M. A. Little, P. E. McSharry, S. J. Roberts, D. A. E. Costello, I. M. Moroz, *Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection*, BioMedical Engineering OnLine, 2007.
