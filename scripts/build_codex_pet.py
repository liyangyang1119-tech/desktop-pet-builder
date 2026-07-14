#!/usr/bin/env python3
"""Build a Codex v2 custom pet package from action images."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageOps

CELL_W = 192
CELL_H = 208
COLS = 8
ROWS = 11


def open_fit(path: Path, scale: float, alpha_threshold: int) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha < alpha_threshold:
                pixels[x, y] = (0, 0, 0, 0)
    bbox = image.getchannel("A").getbbox()
    if bbox:
        image = image.crop(bbox)
    image.thumbnail((int(CELL_W * scale), int(CELL_H * scale)), Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    cell.alpha_composite(image, ((CELL_W - image.width) // 2, (CELL_H - image.height) // 2))
    return cell


def clean_hidden_rgb(image: Image.Image) -> None:
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y][3] == 0:
                pixels[x, y] = (0, 0, 0, 0)


def loop_frames(mode: str, run1: Image.Image, run2: Image.Image, run3: Image.Image | None) -> list[Image.Image]:
    if mode == "12":
        return [run1, run2, run1, run2, run1, run2, run1, run2]
    if mode == "23":
        if run3 is None:
            raise SystemExit("--drag-loop 23 requires --run3")
        return [run2, run3, run2, run3, run2, run3, run2, run3]
    if run3 is None:
        raise SystemExit(f"--drag-loop {mode} requires --run3")
    if mode == "bounce123":
        return [run1, run2, run3, run2, run1, run2, run3, run2]
    if mode == "123prefix":
        return [run1, run2, run3, run1, run2, run3, run1, run2]
    raise SystemExit(f"unknown drag loop: {mode}")


def write_manifest(output_dir: Path, pet_id: str, display_name: str, description: str) -> None:
    manifest = {
        "id": pet_id,
        "displayName": display_name,
        "description": description,
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    }
    (output_dir / "pet.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def default_output_dir(pet_id: str) -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    home = Path(codex_home) if codex_home else Path.home() / ".codex"
    return home / "pets" / pet_id


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--id", required=True)
    parser.add_argument("--display-name")
    parser.add_argument("--description", default="A custom desktop companion for Codex.")
    parser.add_argument("--idle", default="idle.png")
    parser.add_argument("--blink", default="blink.png")
    parser.add_argument("--sleep", default="sleep.png")
    parser.add_argument("--work", default="work.png")
    parser.add_argument("--run1", default="jump-1.png")
    parser.add_argument("--run2", default="jump-2.png")
    parser.add_argument("--run3", default="")
    parser.add_argument("--drag-loop", choices=["12", "23", "bounce123", "123prefix"], default="12")
    parser.add_argument(
        "--run-facing",
        choices=["right", "left"],
        default="right",
        help="Screen direction the source run frames face; the opposite Codex row is mirrored.",
    )
    parser.add_argument("--alpha-threshold", type=int, default=80)
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else default_output_dir(args.id)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source-frames").mkdir(exist_ok=True)

    idle = open_fit(source_dir / args.idle, 0.86, args.alpha_threshold)
    blink = open_fit(source_dir / args.blink, 0.86, args.alpha_threshold)
    sleep = open_fit(source_dir / args.sleep, 0.86, args.alpha_threshold)
    work = open_fit(source_dir / args.work, 0.86, args.alpha_threshold)
    run1 = open_fit(source_dir / args.run1, 0.90, args.alpha_threshold)
    run2 = open_fit(source_dir / args.run2, 0.90, args.alpha_threshold)
    run3_path = source_dir / args.run3 if args.run3 else None
    run3 = open_fit(run3_path, 0.90, args.alpha_threshold) if run3_path and run3_path.exists() else None

    drag = loop_frames(args.drag_loop, run1, run2, run3)
    atlas = Image.new("RGBA", (COLS * CELL_W, ROWS * CELL_H), (0, 0, 0, 0))

    def paste(row: int, col: int, cell: Image.Image) -> None:
        atlas.alpha_composite(cell, (col * CELL_W, row * CELL_H))

    running_right = drag if args.run_facing == "right" else [ImageOps.mirror(frame) for frame in drag]
    running_left = [ImageOps.mirror(frame) for frame in running_right]

    rows = {
        0: [idle, blink, idle, blink, idle, blink, idle],
        1: running_right,
        2: running_left,
        3: [sleep] * 4,
        4: [sleep] * 5,
        5: [sleep] * 8,
        6: [work] * 6,
        7: [work] * 6,
        8: [work] * 6,
        9: [sleep] * 8,
        10: [sleep] * 8,
    }
    for row, frames in rows.items():
        for col, frame in enumerate(frames):
            paste(row, col, frame)

    clean_hidden_rgb(atlas)
    atlas.save(output_dir / "spritesheet.png")
    atlas.save(output_dir / "spritesheet.webp", format="WEBP", lossless=True, exact=True, method=6)
    write_manifest(output_dir, args.id, args.display_name or args.id, args.description)
    print(output_dir)


if __name__ == "__main__":
    main()
