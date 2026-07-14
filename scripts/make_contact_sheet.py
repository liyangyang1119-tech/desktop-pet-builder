#!/usr/bin/env python3
"""Make a contact sheet preview for generated desktop pet action images."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


DEFAULT_NAMES = [
    ("idle", "idle.png"),
    ("blink", "blink.png"),
    ("sleep", "sleep.png"),
    ("work", "work.png"),
    ("run1", "jump-1.png"),
    ("run2", "jump-2.png"),
]


def trim(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--cell-size", type=int, default=240)
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    label_h = 28
    cell = args.cell_size
    sheet = Image.new("RGBA", (cell * 3, (cell + label_h) * 2), (210, 210, 210, 255))
    draw = ImageDraw.Draw(sheet)

    for index, (label, filename) in enumerate(DEFAULT_NAMES):
        row = index // 3
        col = index % 3
        x = col * cell
        y = row * (cell + label_h)
        path = source_dir / filename
        if path.exists():
            image = trim(Image.open(path))
            image.thumbnail((int(cell * 0.86), int(cell * 0.86)), Image.Resampling.LANCZOS)
            sheet.alpha_composite(image, (x + (cell - image.width) // 2, y + label_h + (cell - image.height) // 2))
        draw.text((x + 8, y + 6), label, fill=(0, 0, 0, 255))

    sheet.save(output)
    print(output)


if __name__ == "__main__":
    main()
