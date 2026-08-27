import csv
import shutil
from pathlib import Path

KAGGLE_TRAIN_DIR = Path(r"C:\Users\Galang\Downloads\Real and Fake Pokemon Cards\train")
KAGGLE_CSV = Path(r"C:\Users\Galang\Downloads\Real and Fake Pokemon Cards\train_labels.csv")
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "dataset"

LABEL_MAP = {
    "0": "fake",
    "1": "real",
}

def find_image_file(image_id: str) -> Path | None:
    candidates = [
        f"{int(image_id)}.JPG",
        f"{int(image_id)}.jpg",
        f"{image_id}.JPG",
        f"{image_id}.jpg",
    ]
    for name in candidates:
        path = KAGGLE_TRAIN_DIR / name
        if path.exists():
            return path
    return None


def main():
    counts = {"real": 0, "fake": 0}
    missing = []

    with open(KAGGLE_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_id = row["id"]
            label = row["label"]

            category = LABEL_MAP.get(label)
            if category is None:
                continue

            source_path = find_image_file(image_id)
            if source_path is None:
                missing.append(image_id)
                continue

            dest_dir = OUTPUT_DIR / category
            dest_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source_path, dest_dir / source_path.name)
            counts[category] += 1

    print(f"Real: {counts['real']} gambar")
    print(f"Fake: {counts['fake']} gambar")
    if missing:
        print(f"\n {len(missing)} file nggak ketemu, contoh id: {missing[:5]}")


if __name__ == "__main__":
    main()