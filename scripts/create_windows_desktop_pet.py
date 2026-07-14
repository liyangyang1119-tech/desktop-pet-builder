#!/usr/bin/env python3
"""Create a standalone Windows PowerShell/WPF desktop pet folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_asset(source_dir: Path, output_assets: Path, source_name: str, target_name: str) -> None:
    source = source_dir / source_name
    if not source.exists():
        raise SystemExit(f"missing required image: {source}")
    shutil.copy2(source, output_assets / target_name)


def ps_single(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_pet_script(output_dir: Path, width: int, height: int, image_size: int, work_seconds: int) -> None:
    assets = str((output_dir / "assets").resolve())
    script = f"""
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase

$assets = {ps_single(assets)}
$window = New-Object Windows.Window
$window.Width = {width}
$window.Height = {height}
$window.WindowStyle = 'None'
$window.AllowsTransparency = $true
$window.Background = [Windows.Media.Brushes]::Transparent
$window.Topmost = $true
$window.ShowInTaskbar = $false
$window.Left = 120
$window.Top = 120

$image = New-Object Windows.Controls.Image
$image.Width = {image_size}
$image.Height = {image_size}
$image.Stretch = 'Uniform'
$image.RenderTransformOrigin = '0.5,0.5'

$grid = New-Object Windows.Controls.Grid
$grid.Background = [Windows.Media.Brushes]::Transparent
$grid.Children.Add($image) | Out-Null
$window.Content = $grid

$state = 'idle'
$dragging = $false
$dragIndex = 0
$dragFrames = @('run1.png','run2.png')

function Set-Image([string]$name) {{
  $path = Join-Path $assets $name
  $bitmap = New-Object Windows.Media.Imaging.BitmapImage
  $bitmap.BeginInit()
  $bitmap.CacheOption = [Windows.Media.Imaging.BitmapCacheOption]::OnLoad
  $bitmap.UriSource = [Uri]$path
  $bitmap.EndInit()
  $image.Source = $bitmap
}}

function Set-State([string]$next) {{
  $script:state = $next
  if ($next -eq 'idle') {{ Set-Image 'idle.png' }}
  elseif ($next -eq 'blink') {{ Set-Image 'blink.png' }}
  elseif ($next -eq 'sleep') {{ Set-Image 'sleep.png' }}
  elseif ($next -eq 'work') {{ Set-Image 'work.png' }}
  elseif ($next -eq 'drag') {{ Set-Image $dragFrames[$script:dragIndex % $dragFrames.Count] }}
}}

$blinkTimer = New-Object Windows.Threading.DispatcherTimer
$blinkTimer.Interval = [TimeSpan]::FromMilliseconds(4800)
$blinkTimer.Add_Tick({{
  if ($script:state -eq 'idle' -and -not $script:dragging) {{
    Set-State 'blink'
    $returnTimer = New-Object Windows.Threading.DispatcherTimer
    $returnTimer.Interval = [TimeSpan]::FromMilliseconds(500)
    $returnTimer.Add_Tick({{
      $this.Stop()
      if ($script:state -eq 'blink') {{ Set-State 'idle' }}
    }})
    $returnTimer.Start()
  }}
}})
$blinkTimer.Start()

$dragTimer = New-Object Windows.Threading.DispatcherTimer
$dragTimer.Interval = [TimeSpan]::FromMilliseconds(180)
$dragTimer.Add_Tick({{
  if ($script:dragging) {{
    $script:dragIndex++
    Set-State 'drag'
  }}
}})
$dragTimer.Start()

$grid.Add_MouseEnter({{
  if (-not $script:dragging -and $script:state -ne 'work') {{ Set-State 'sleep' }}
}})
$grid.Add_MouseLeave({{
  if (-not $script:dragging -and $script:state -ne 'work') {{ Set-State 'idle' }}
}})
$grid.Add_MouseLeftButtonDown({{
  $script:dragging = $true
  $script:dragIndex = 0
  Set-State 'drag'
  $window.DragMove()
}})
$grid.Add_MouseLeftButtonUp({{
  $script:dragging = $false
  if ($script:state -ne 'work') {{ Set-State 'idle' }}
}})
$grid.Add_MouseRightButtonDown({{
  $script:dragging = $false
  Set-State 'work'
  $workTimer = New-Object Windows.Threading.DispatcherTimer
  $workTimer.Interval = [TimeSpan]::FromSeconds({work_seconds})
  $workTimer.Add_Tick({{
    $this.Stop()
    if ($script:state -eq 'work') {{ Set-State 'idle' }}
  }})
  $workTimer.Start()
}})

Set-State 'idle'
$window.ShowDialog() | Out-Null
""".lstrip()
    (output_dir / "open-desktop-pet.ps1").write_text(script, encoding="utf-8")


def write_launcher(output_dir: Path) -> None:
    script_path = str((output_dir / "open-desktop-pet.ps1").resolve())
    launcher = (
        "@echo off\r\n"
        f"start \"\" powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File \"{script_path}\"\r\n"
    )
    (output_dir / "open-desktop-pet.cmd").write_text(launcher, encoding="ascii")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--idle", default="idle.png")
    parser.add_argument("--blink", default="blink.png")
    parser.add_argument("--sleep", default="sleep.png")
    parser.add_argument("--work", default="work.png")
    parser.add_argument("--run1", default="jump-1.png")
    parser.add_argument("--run2", default="jump-2.png")
    parser.add_argument("--width", type=int, default=300)
    parser.add_argument("--height", type=int, default=335)
    parser.add_argument("--image-size", type=int, default=210)
    parser.add_argument("--work-seconds", type=int, default=8)
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    assets = output_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    copy_asset(source_dir, assets, args.idle, "idle.png")
    copy_asset(source_dir, assets, args.blink, "blink.png")
    copy_asset(source_dir, assets, args.sleep, "sleep.png")
    copy_asset(source_dir, assets, args.work, "work.png")
    copy_asset(source_dir, assets, args.run1, "run1.png")
    copy_asset(source_dir, assets, args.run2, "run2.png")
    write_pet_script(output_dir, args.width, args.height, args.image_size, args.work_seconds)
    write_launcher(output_dir)
    print(output_dir)


if __name__ == "__main__":
    main()
