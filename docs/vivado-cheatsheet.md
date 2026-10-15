# Vivado Cheat Sheet (Bloom Lab)

Use this as a click-path. Exact menu names vary slightly by Vivado version.

## Open the project

1. Launch **Vivado**.
2. **Open Project** → select the provided `.xpr`.
3. In the **Sources** pane, find `flower_level1.sv` or `flower_level2.sv`.

## Edit RTL

1. Double-click the file.
2. Make your change.
3. **File → Save** (`Ctrl+S`).

## Run behavioral simulation

1. Set the correct testbench as the simulation top (right-click `tb_flower_level1.sv` → **Set as Top** under Simulation, if needed).
2. **Flow Navigator → Simulation → Run Simulation → Run Behavioral Simulation**.
3. In the waveform window, add `water`, `sun`, `bloom` (Level 1) or `clk`, `reset`, `water`, `sun`, `state` (Level 2).
4. Click **Run All** or run for a few microseconds.
5. Compare the waveform to the truth table / state tests.

If the waveform is empty: **Restart**, then **Run All**. If signals are missing: right-click in **Scope**, add to wave.

## Synthesize, implement, bitstream

For this lab the project is already constrained. After RTL is saved:

1. **Run Synthesis** → wait for green check.  
2. **Run Implementation** → wait.  
3. **Generate Bitstream** → wait.

If synthesis fails, open the **Messages** tab and jump to the **first red error**, not the last one.

## Program the Basys 3

1. Connect the board with the **micro-USB** cable. Turn the board **ON** (power switch).
2. Confirm the **USB** jumper is set for USB power (Digilent default).
3. **Open Hardware Manager** → **Open target** → **Auto Connect**.
4. **Program Device** → select the `.bit` file if prompted → **Program**.
5. The **DONE** LED on the Basys 3 should light.

If Auto Connect fails: install Digilent Adept/cable drivers, try a different USB port, and confirm the board is powered.

## Which sources to use

| Lab part | Student file | Simulation top | FPGA top |
|---|---|---|---|
| Level 1 | `flower_level1.sv` | `tb_flower_level1` | `top_level1` |
| Level 2 | `flower_level2.sv` | `tb_flower_level2` | `top_level2` |

Do not edit `*_top*.sv`, debounce, or the `.xdc` unless an instructor asks you to.
