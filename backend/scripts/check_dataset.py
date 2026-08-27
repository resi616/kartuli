import os

VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def count_images(folder_path: str) -> int:
    if not os.path.exists(folder_path):
        return 0
    return len([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(VALID_EXTENSIONS)
    ])


if __name__ == "__main__":
    reference_count = count_images(os.path.join(DATA_DIR, 'reference'))
    real_count = count_images(os.path.join(DATA_DIR, 'dataset', 'real'))
    fake_count = count_images(os.path.join(DATA_DIR, 'dataset', 'fake'))

    print(f"Reference (acuan)  : {reference_count} gambar")
    print(f"Dataset real        : {real_count} gambar")
    print(f"Dataset fake        : {fake_count} gambar")

    if reference_count == 0:
        print("\n Belum ada foto reference")
    elif real_count < 5 or fake_count < 5:
        print("\n Dataset masih terlalu sedikit buat testing yang berarti.")