#!/usr/bin/env python3
"""Build dist/bloom-student-kit.zip: everything a station needs, no answers.

    python scripts/make_student_kit.py           # also builds BloomViz.exe (needs PyInstaller)
    python scripts/make_student_kit.py --no-exe  # skip the visualizer
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD = ROOT / "build" / "kit"
KIT = "bloom-student-kit"

FILES = {
    "rtl/flower_level1.sv": "rtl/starters/flower_level1.sv",
    "rtl/flower_level2.sv": "rtl/starters/flower_level2.sv",
    "rtl/tb_flower_level1.sv": "rtl/tb_flower_level1.sv",
    "rtl/tb_flower_level2.sv": "rtl/tb_flower_level2.sv",
    "rtl/top_level1.sv": "rtl/top_level1.sv",
    "rtl/top_level2.sv": "rtl/top_level2.sv",
    "rtl/sync_debounce.sv": "rtl/sync_debounce.sv",
    "rtl/rise_pulse.sv": "rtl/rise_pulse.sv",
    "rtl/uart_tx.sv": "rtl/uart_tx.sv",
    "constraints/basys3_bloom.xdc": "constraints/basys3_bloom.xdc",
    "handout.html": "handout/index.html",
}

START_HERE = """\
Bloom: your first RTL design

  rtl/flower_level1.sv   Level 1. The only file you edit first.
  rtl/flower_level2.sv   Level 2. The only file you edit second.
  handout.html           The printout: Vivado clicks, board map, fixes.
  BloomViz.exe           Optional flower window. Double-click, pick your
                         board's port, press Connect.

Everything else (tb_, top_level, the .xdc) is already done. Leave it alone.
"""


def build_exe() -> Path:
    work = BUILD / "pyinstaller"
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller", "--onefile", "--windowed", "--noconfirm",
        "--name", "BloomViz",
        "--distpath", str(work / "dist"),
        "--workpath", str(work / "work"),
        "--specpath", str(work),
        str(ROOT / "viz" / "bloom_viz.py"),
    ])
    return work / "dist" / "BloomViz.exe"


def main() -> int:
    for src in ("rtl/starters/flower_level1.sv", "rtl/starters/flower_level2.sv"):
        if "TODO" not in (ROOT / src).read_text(encoding="utf-8"):
            print(f"[stop] {src} has no TODO. It may be a finished answer; not packaging it.")
            return 1

    exe = None
    if "--no-exe" not in sys.argv:
        exe = build_exe()

    DIST.mkdir(exist_ok=True)
    out = DIST / f"{KIT}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dest, src in FILES.items():
            z.write(ROOT / src, f"{KIT}/{dest}")
        z.writestr(f"{KIT}/START HERE.txt", START_HERE)
        if exe:
            z.write(exe, f"{KIT}/BloomViz.exe")

    if exe:
        shutil.copy2(exe, DIST / "BloomViz.exe")
    print(f"[ok] {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
