# Desktop Pet Builder
+&#19968;&#20010;&#21487;&#22797;&#29992;&#30340; Codex &#26700;&#23456; Skill锛?#20174;&#35282;&#33394;&#21442;&#32771;&#22270;&#25110;&#21160;&#20316;&#32032;&#26448;&#29983;&#25104;&#36879;&#26126;&#26700;&#23456;锛?#24182;&#21487;&#25171;&#21253;&#20026; Codex &#33258;&#23450;&#20041;&#26700;&#23456;&#25110; Windows &#26700;&#23456;銆?
## &#25928;&#26524;&#23637;&#31034;

&#19979;&#26041;&#23637;&#31034;&#21516;&#19968;&#35282;&#33394;&#30340;&#24453;&#26426;銆?#30504;&#30524;銆?#30561;&#35273;銆?#24037;&#20316;&#19982;&#20004;&#24103;&#36305;&#21160;&#21160;&#20316;銆?#36305;&#21160;&#20004;&#24103;&#22987;&#32456;&#20445;&#25345;&#21516;&#19968;&#36731;&#24494;&#20391;&#38754;&#26397;&#21521;锛?#20165;&#33258;&#28982;&#20132;&#26367;&#25670;&#21160;&#25163;&#33050;銆?
![Desktop pet action sheet](assets/demo/desktop-pet-action-sheet.svg)

## &#20351;&#29992;&#35828;&#26126;

&#23558;&#26412;&#30446;&#24405;&#25918;&#20837; Codex skills &#30446;&#24405;&#21518;锛?#20351;&#29992; `$desktop-pet-builder` &#35843;&#29992;銆?#20844;&#24320;&#29256;&#24050;&#21435;&#38500;&#20010;&#20154;&#35282;&#33394;&#21407;&#22270;銆?#36134;&#21495;&#20449;&#24687;銆?#20973;&#25454;銆?#20196;&#29260;銆?#26412;&#26426;&#36335;&#24452;&#21644;&#20020;&#26102;&#21457;&#24067;&#25991;&#20214;銆?

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
