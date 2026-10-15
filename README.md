# 🌸 Bloom: Your First RTL Design

A beginner **FPGA + RTL** lab for introductory digital design (originally framed for Women in ECE workshops). Students specify a tiny “virtual flower,” describe it in SystemVerilog, simulate it, and program a **Digilent Basys 3**.

```mermaid
flowchart LR
  SPEC[Specification] --> RTL[SystemVerilog]
  RTL --> SIM[Simulation]
  SIM --> FPGA[Basys 3]
  FPGA --> VIZ[🌱 🌿 🌸]
```


## What’s in this package

| Path | Audience | Purpose |
|---|---|---|
| [`slides/index.html`](slides/index.html) | Facilitators | Workshop slides (open in a browser) |
| [`docs/student-lab-manual.md`](docs/student-lab-manual.md) | Students | Full lab: pre-lab through reflection |
| [`docs/instructor-guide.md`](docs/instructor-guide.md) | Instructors | Setup, solutions, pedagogy, schedule |
| [`docs/vivado-cheatsheet.md`](docs/vivado-cheatsheet.md) | Students | Click-path for Vivado |
| [`rtl/`](rtl/) | Students | Starter RTL, testbenches, top wrappers |
| [`constraints/basys3_bloom.xdc`](constraints/basys3_bloom.xdc) | Students | Basys 3 pin map |
| [`viz/bloom_viz.py`](viz/bloom_viz.py) | Students | Optional serial flower visualizer |
| [`sim/index.html`](sim/index.html) | Anyone | Browser bench: same spec, no board |
| [`solutions/`](solutions/) | Instructors only | Reference RTL |

## Suggested duration

**2 hours** as a facilitated workshop, or **one 3-hour lab period** if students also write a short report.

## Hardware / software

- Digilent **Basys 3** (Artix-7 `xc7a35tcpg236-1`)
- USB cable (micro-USB)
- **Vivado** (ML Standard / Webpack is enough; 2020.2+ recommended)
- Optional: Python 3 + `pyserial` for the visualizer
- Optional: printed flower LED overlay

## How students should work

1. Complete the **pre-lab** in the student manual (no FPGA required).
2. Open the provided Vivado project (or add the files in `rtl/` and `constraints/`).
3. Fill in **Level 1** (`flower_level1.sv`), simulate, then program.
4. Fill in **Level 2** (`flower_level2.sv`), simulate, then program.
5. Optionally connect the visualizer (`viz/bloom_viz.py`).
6. Attempt at least one customization challenge.

Do **not** start from solutions. Blank student copies with `TODO` markers are in `rtl/starters/`. The copies in `rtl/flower_level1.sv` and `rtl/flower_level2.sv` are the tested implementation (same behavior as `solutions/`).

## Try it without a board

```text
python scripts/run_tests.py
```

That runs the Python golden model. If Icarus Verilog (`iverilog` / `vvp`) is on `PATH`, it also simulates `rtl/tb_flower_level1.sv` and `rtl/tb_flower_level2.sv`.

Open [`sim/index.html`](sim/index.html) in a browser to flip water, sun, grow, and reset. The page runs the same checks as `tests/test_bloom_model.py` and shows the result at the top.

## Instructor note

Keep `solutions/` off the student share. Print or distribute only `docs/student-lab-manual.md` plus the starter `rtl/` and `constraints/` files.
