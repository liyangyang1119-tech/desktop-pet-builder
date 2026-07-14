# Desktop Pet Builder

A reusable Codex skill for building transparent desktop pets from a character reference or a set of action images.

## What it does

- Generates and validates the six standard states: idle, blink, sleep, work, run-left, and run-right.
- Packages a Codex custom pet with `pet.json` and `spritesheet.webp`.
- Creates a transparent, always-on-top, draggable Windows desktop pet.
- Keeps run frames in one consistent, slight side-facing direction. The two frames only alternate natural arm and leg motion.
- Maps the run-facing direction correctly so left and right dragging are not reversed.

## Use

Put this folder in your Codex skills directory and invoke `$desktop-pet-builder`.

Build a Codex pet:

```powershell
python scripts/build_codex_pet.py `
  --source-dir "path/to/pet-images" `
  --id "my-pet" `
  --display-name "My Pet" `
  --run-facing left `
  --drag-loop 12
```

Build a Windows desktop pet:

```powershell
python scripts/create_windows_desktop_pet.py `
  --source-dir "path/to/pet-images" `
  --output-dir "output/my-pet"
```

## Repository contents

```text
SKILL.md
agents/openai.yaml
references/
scripts/
```

This public version excludes personal character source images, credentials, tokens, local paths, generated caches, and temporary publishing files.

## License

MIT. See [LICENSE](LICENSE).
