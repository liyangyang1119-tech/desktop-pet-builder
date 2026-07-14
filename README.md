
# Desktop Pet Builder

涓€涓敤浜庡垱寤哄拰鎵撳寘妗屽疇鐨?Codex Skill锛氭敮鎸佷粠涓€寮犺鑹插弬鑰冨浘鐢熸垚鍔ㄤ綔绱犳潗锛屼篃鏀寔鐩存帴鏁寸悊宸叉湁鍔ㄤ綔鍥俱€?
## 鏁堟灉灞曠ず

### 鍏姩浣滈瑙?
![Desktop pet action sheet](assets/demo/desktop-pet-action-sheet.png)

### 鍔ㄤ綔鍙傝€冩澘

![Action reference board](assets/demo/action-reference-board.png)

## 鏀寔鍐呭

- Codex 鑷畾涔夋瀹狅細鐢熸垚 `pet.json` 鍜?Codex v2 `spritesheet.webp`
- Windows 妗屽疇锛氱敓鎴愰€忔槑銆佺疆椤躲€佸彲鎷栨嫿鐨?PowerShell/WPF 妗屽疇
- 榛樿鍔ㄤ綔锛氬緟鏈恒€佺湪鐪笺€佺潯瑙夈€佸伐浣溿€佸弻甯ц窇鍔?- 璺戝姩鏂瑰悜鏄犲皠锛氫娇鐢?`--run-facing left/right`锛岄伩鍏嶅乏鍙虫嫋鎷芥柟鍚戝弽杞?- 閫忔槑杈圭紭銆佺敾甯冦€佸熀绾裤€佸姩浣滃惊鐜拰鍥鹃泦鏍￠獙

## 浣跨敤

灏嗘湰鐩綍鏀惧叆 Codex skills 鐩綍鍚庯紝浣跨敤 `$desktop-pet-builder` 瑙﹀彂銆?
Codex 妗屽疇鎵撳寘绀轰緥锛?
```powershell
python scripts/build_codex_pet.py `
  --source-dir "path/to/pet-images" `
  --id "my-pet" `
  --display-name "My Pet" `
  --run-facing left `
  --drag-loop 12
```

Windows 妗屽疇鎵撳寘绀轰緥锛?
```powershell
python scripts/create_windows_desktop_pet.py `
  --source-dir "path/to/pet-images" `
  --output-dir "output/my-pet"
```

## 鐩綍

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/demo/
```

鏈粨搴撲笉鍖呭惈涓汉瑙掕壊鍘熷浘銆佺櫥褰曞嚟鎹€佷护鐗屻€佹湰鏈鸿矾寰勩€佺敓鎴愮紦瀛樻垨涓存椂鍙戝竷鑴氭湰銆?
## License

MIT License锛岃瑙?[LICENSE](LICENSE)銆?
