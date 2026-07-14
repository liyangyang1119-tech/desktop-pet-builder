---
name: desktop-pet-builder
description: Build reusable Codex custom pets and Windows desktop pets from character reference images or action sprites. Use for pet generation, state mapping, spritesheet packaging, transparent floating windows, and action consistency checks.
---

# Desktop Pet Builder

## Goal

Create a reusable pet from a full action set or one character reference image. Output either a Codex custom pet, a Windows desktop pet, or both.

## Inputs

Ask for one of the following when no source is supplied:

1. A full action image set.
2. One character reference image.
3. A request to design the character from scratch.

Preserve the chosen illustration style. Do not force pixel art onto an illustrated reference unless requested.

## Required actions

Create these transparent sprites with the same canvas size, character scale, baseline, and camera angle:

- `idle.png`: neutral resting pose.
- `blink.png`: same proportions and framing as idle; only a small expression or hand change is allowed.
- `sleep.png`: clearly sleeping, with a compact pose.
- `work.png`: working or focused pose.
- `run_left.png` and `run_right.png`: a two-frame run cycle.

For run sprites, use one consistent slight side-facing direction in both frames. Do not make one frame face left and the other face right. Keep the head and torso stable. Make arm and leg alternation clear but natural, with only a small expression change between frames.

## Direction mapping

Before packaging, verify direction against actual dragging behavior. A left drag must use the intended left-facing run sprite and a right drag must use the intended right-facing run sprite. Never silently reverse these mappings.

## Image quality

- Use native transparency when available.
- If chroma key is required, use a flat `#00ff00` background only, remove it locally, and inspect alpha edges.
- Do not leave white halos, matte fringes, backgrounds, floor shadows, text, or watermarks.
- Build a contact sheet before final packaging to check consistency.

## Packaging

For a Codex pet, create `pet.json` and a Codex v2 `spritesheet.webp` using `scripts/build_codex_pet.py`.

For a Windows pet, use `scripts/create_windows_desktop_pet.py` to produce a transparent, always-on-top, draggable PowerShell/WPF pet.

## Validation checklist

1. All expected files exist and are readable.
2. Every sprite has alpha transparency and matching dimensions.
3. Idle and blink have matching scale and baseline.
4. Run frames have one stable side-facing direction and obvious alternating limbs.
5. Left and right drag direction mapping is correct.
6. Generated package launches successfully.
