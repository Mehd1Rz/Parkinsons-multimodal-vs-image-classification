## Image Dataset

The project includes the complete spiral + wave image dataset in the following structure:

```text
data/images/
├── training/
│   ├── healthy/      (36 images)
│   └── parkinson/    (36 images)
└── testing/
    ├── healthy/      (15 images)
    └── parkinson/    (15 images)
```

The dataset contains:

* **72 training images**

  * 36 Healthy
  * 36 Parkinson
* **30 testing images**

  * 15 Healthy
  * 15 Parkinson
* **102 images in total**

The image files are included directly in the repository under `data/images/`.

### Metadata

The file:

```text
data/metadata/parkinsons.csv
```

contains the metadata associated with the dataset. Some entries use legacy Windows-style paths such as:

```text
test\training\parkinson\008_sw.png
```

The notebooks and `scripts/validate_dataset.py` normalize these paths to match the repository's current directory structure.

### Dataset Validation

To verify that the dataset is correctly organized and that all expected images are available, run:

```bash
python scripts/validate_dataset.py
```

The validation script checks the expected directory structure and image files before running the notebooks.
