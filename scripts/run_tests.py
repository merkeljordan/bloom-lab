#!/usr/bin/env python3
"""Run Bloom golden-model tests, and Icarus Verilog if it is installed."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_python_tests() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def run_iverilog(tb: str, sources: list[str], plusarg_name: str) -> int:
    iverilog = shutil.which("iverilog")
    vvp = shutil.which("vvp")
    if not iverilog or not vvp:
        print(f"[skip] Icarus Verilog not on PATH — {plusarg_name} RTL sim skipped")
        return 0

    out = ROOT / "build" / f"{plusarg_name}.vvp"
    out.parent.mkdir(exist_ok=True)
    cmd = [iverilog, "-g2012", "-o", str(out), str(ROOT / "rtl" / tb), *sources]
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)
    log = subprocess.check_output([vvp, str(out)], text=True)
    print(log)
    if "PASSED" not in log or "FAILED" in log:
        print(f"[fail] {plusarg_name}")
        return 1
    print(f"[ok] {plusarg_name}")
    return 0


def main() -> int:
    rc = run_python_tests()
    rtl = ROOT / "rtl"
    rc |= run_iverilog(
        "tb_flower_level1.sv",
        [str(rtl / "flower_level1.sv")],
        "level1",
    )
    rc |= run_iverilog(
        "tb_flower_level2.sv",
        [str(rtl / "flower_level2.sv")],
        "level2",
    )
    return rc


if __name__ == "__main__":
    sys.exit(main())
