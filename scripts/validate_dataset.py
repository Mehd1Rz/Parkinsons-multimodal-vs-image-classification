from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "metadata" / "parkinsons.csv"
IMAGE_ROOT = ROOT / "data" / "images"

if not CSV.exists():
    raise SystemExit(f"Metadata file not found: {CSV}")

df = pd.read_csv(CSV)
required = {"name", "status", "image_path"}
missing = required - set(df.columns)
if missing:
    raise SystemExit(f"Missing required columns: {sorted(missing)}")

print(f"Rows: {len(df)}")
print(f"Classes: {df['status'].value_counts().to_dict()}")
print(f"Unique image paths: {df['image_path'].nunique()}")
print(f"Repeated image-path rows: {df['image_path'].duplicated().sum()}")

def normalize_legacy_path(value: str) -> Path:
    p = str(value).replace("\\", "/")
    if p.startswith("test/"):
        p = p[len("test/"):]
    return IMAGE_ROOT / p

paths = [normalize_legacy_path(p) for p in df["image_path"]]
missing_paths = [p for p in paths if not p.exists()]
print(f"Missing referenced images: {len(missing_paths)}")
if missing_paths:
    print("First missing paths:")
    for p in missing_paths[:10]:
        print(f"  - {p.relative_to(ROOT)}")
else:
    print("All referenced images are present.")
