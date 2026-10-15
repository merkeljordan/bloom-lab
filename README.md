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
| [`slides/index.html`](slides/index.html) | Everyone | Workshop slides; they teach the whole lab (open in a browser) |
| [`handout/index.html`](handout/index.html) | Students | One-page printout for each board: Vivado clicks, board map, fixes |
| [`docs/instructor-guide.md`](docs/instructor-guide.md) | Instructors | Solutions, pedagogy, schedule |
| [`docs/station-checklist.md`](docs/station-checklist.md) | Instructors | Setting up each computer and board, and fixes on the day |
| [`scripts/make_student_kit.py`](scripts/make_student_kit.py) | Instructors | Builds the student zip (no answers) and `BloomViz.exe` |
| [`rtl/`](rtl/) | Students | Starter RTL, testbenches, top wrappers |
| [`constraints/basys3_bloom.xdc`](constraints/basys3_bloom.xdc) | Students | Basys 3 pin map |
| [`viz/bloom_viz.py`](viz/bloom_viz.py) | Students | Optional serial flower visualizer |
| [`sim/index.html`](sim/index.html) | Anyone | Browser bench: same spec, no board |
| [`solutions/`](solutions/) | Instructors only | Reference RTL |

## Suggested duration

About **2 hours** as a facilitated workshop.

## Hardware / software

- Digilent **Basys 3** (Artix-7 `xc7a35tcpg236-1`)
- USB cable (micro-USB)
- **Vivado** (ML Standard / Webpack is enough; 2020.2+ recommended)
- Optional: Python 3 + `pyserial` for the visualizer
- Optional: printed flower LED overlay

## How students should work

1. Follow the slides on the projector, with the printout at the board.
2. Open the station's Vivado project.
3. Fill in **Level 1** (`flower_level1.sv`), simulate, then program.
4. Fill in **Level 2** (`flower_level2.sv`), simulate, then program.
5. Optionally connect the visualizer (`viz/bloom_viz.py`).
6. If there's time, try a change from the "Going further" slide.

Do **not** start from solutions. Blank student copies with `TODO` markers are in `rtl/starters/`. The copies in `rtl/flower_level1.sv` and `rtl/flower_level2.sv` are the tested implementation (same behavior as `solutions/`).

## Try it without a board

```text
python scripts/run_tests.py
```

That runs the Python golden model. If Icarus Verilog (`iverilog` / `vvp`) is on `PATH`, it also simulates `rtl/tb_flower_level1.sv` and `rtl/tb_flower_level2.sv`.

Open [`sim/index.html`](sim/index.html) in a browser to flip water, sun, grow, and reset. The page runs the same checks as `tests/test_bloom_model.py` and shows the result at the top.

## Instructor note

Students never need git, Python, or pip. Run `python scripts/make_student_kit.py` (needs `python -m pip install pyinstaller` once) to get `dist/bloom-student-kit.zip`: the starter files, tests, wrappers, pin file, printout, and `BloomViz.exe`, with no answers. Set up each station from that zip using [`docs/station-checklist.md`](docs/station-checklist.md).

`rtl/flower_level1.sv`, `rtl/flower_level2.sv`, and `solutions/` are finished answers. Keep them off student machines.
