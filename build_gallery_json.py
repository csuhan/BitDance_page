import argparse
import json
import random
import re
from typing import Optional, Tuple
from pathlib import Path


def get_image_size(image_path: Path) -> Tuple[Optional[int], Optional[int]]:
    match = re.search(r"_(\d+)x(\d+)\.png$", image_path.name, flags=re.IGNORECASE)
    if not match:
        return None, None
    width = int(match.group(1))
    height = int(match.group(2))
    return width, height


def collect_records(gallery_dir: Path, root_dir: Path) -> list[dict]:
    txt_files = sorted(gallery_dir.glob("*.txt"))
    records = []
    for txt_file in txt_files:
        if 'p4' in txt_file.name and random.random() < 0.8:
            continue
        prompt = txt_file.read_text(encoding="utf-8").strip()
        images = sorted(gallery_dir.glob(f"{txt_file.stem}_*.png"))
        if not images:
            continue
        image = random.choice(images)
        width, height = get_image_size(image)
        image_path = f"https://hf.co/datasets/csuhan/bitdance_demo/resolve/main/{image.name}"
        record = {"prompt": prompt, "image_path": image_path}
        if width and height:
            record["width"] = width
            record["height"] = height
        records.append(record)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gallery", default="gallery_images")
    parser.add_argument("--output", default="gallery.json")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    gallery_dir = Path(args.gallery)
    root_dir = Path.cwd()
    records = collect_records(gallery_dir, root_dir)
    random.shuffle(records)
    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
