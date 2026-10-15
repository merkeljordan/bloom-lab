# Bloom — Instructor Guide

**Do not distribute this file or `solutions/` to students.**

This guide supports the student manual in `docs/student-lab-manual.md`. The original workshop notes (Women in ECE, Basys 3, Vivado) are expanded here with setup, solutions, and common failure modes.

---

## Pedagogy

The lab exists to teach **specification before syntax**.

Closing question for the room:

> "What was the first thing you did when you were given the flower problem?"

The answer should not be:

> "I opened Vivado and started coding."

It should be:

> **"I figured out what the system was supposed to do."**

Keep Level 1 tiny (one AND) so every student gets a bitstream on the board. Level 2 is the real conceptual jump (memory, FSMs). Customization is for groups that finish early—not a gate for “success.”

### Inclusive facilitation notes

- Assume mixed prior coding experience; never treat Python/C knowledge as a prerequisite for “being an engineer.”  
- Prefer “the circuit does X” over “you did it wrong.”  
- Stamp **simulation pass** before allowing FPGA time so boards don’t become a bottleneck.  
- Offer a printed LED overlay so the metaphor is visible from across the table.  
- If someone has motor or vision constraints, they can drive the keyboard while a partner handles switches, or use the visualizer.

---

## Learning goals (instructor version)

Students should leave able to:

- Separate combinational vs sequential.  
- Write a 3-always-style FSM (register / next-state / output).  
- Use simulation as a spec checker.  
- Explain why a 100 MHz clock plus level-sensitive `water & sun` would skip states (Appendix B in the student manual).

---

## Suggested workshop schedule (2:00)

```mermaid
flowchart LR
  A["0:00 Intro"] --> B["0:10 Level 1"]
  B --> C["0:35 Board check"]
  C --> D["0:45 Level 2"]
  D --> E["1:25 Visualizer"]
  E --> F["1:40 Customize"]
  F --> G["1:55 Showcase"]
```


### 0:00–0:10 — Introduction

- What is an FPGA?  
- What is RTL?  
- Design flow  
- Introduce Bloom  

### 0:10–0:35 — Level 1

- Specification, truth table, AND, SystemVerilog, simulation, program  

### 0:35–0:45 — Hardware checkpoint

Everyone gets Level 1 working on the board.

### 0:45–1:25 — Level 2

- State, registers, FSMs, diagram, RTL, simulation, program  

### 1:25–1:40 — Digital flower

Visualizer if serial is ready; otherwise LED showcase.

### 1:40–1:55 — Customization

### 1:55–2:00 — Showcase + closing question

### Course-lab variant (3 hours)

Add 20 min pre-lab recap, 20 min write-up, and a required challenge diagram (even if RTL is unfinished).

---

## Instructor setup checklist

Before the workshop:

☐ Install/test Vivado on every computer (or a known-good VM/image)  
☐ Install Digilent cable drivers  
☐ Verify FPGA board power, USB, and **DONE** LED on a known-good bitstream  
☐ Create the master Vivado project (`xc7a35tcpg236-1`)  
☐ Add `rtl/*.sv` and `constraints/basys3_bloom.xdc`  
☐ Set simulation and implementation tops as documented  
☐ Configure all `.xdc` constraints  
☐ Create Level 1 / Level 2 starter copies (TODOs intact)  
☐ Keep instructor solution project **offline**  
☐ Create known-good bitstreams (`solutions/` RTL)  
☐ Test synthesis, implementation, programming  
☐ Test every physical input/output (SW0/SW1/BTNC/BTNU/LD0–2)  
☐ Test `viz/bloom_viz.py` on at least one PC  
☐ Prepare backup USB drives / shared project folder  
☐ Print student manuals + stamp sheet  
☐ Prepare flower LED overlays  
☐ Label boards 1…N and cables  

### Vivado project recipe (if you must rebuild)

1. New project → RTL project → part `xc7a35tcpg236-1`.  
2. Add files: all of `rtl/` except you may omit UART if unused.  
3. Add `constraints/basys3_bloom.xdc`.  
4. Simulation top: `tb_flower_level1` then later `tb_flower_level2`.  
5. Implementation top: `top_level1` then `top_level2`.  
6. Save a zip **without** `solutions/`.

---

## Pin and UI decisions (do not change casually)

| Function | Board |
|---|---|
| `clk` | W5, 100 MHz |
| `water` | SW0 |
| `sun` | SW1 |
| `reset` | BTNC (debounced, active-high after wrapper) |
| extra grow | BTNU |
| Level 1 bloom | LD0 |
| Level 2 SEED/SPROUT/BLOOM | LD0/LD1/LD2 |
| UART TX | A18, 115200 8N1, ASCII `'0'`/`'1'`/`'2'` |

**Grow pulse:** rising edge of `(water & sun)` OR (BTNU pressed while both switches on). This is implemented in `top_level2.sv`, not in the student FSM.

If you remove the wrapper and let students clock on raw AND, almost every board will jump to BLOOM. Do not “simplify” that away.

---

## Level 1 expected behavior

```text
bloom = water & sun
```

Purely combinational. Reference:

```systemverilog
assign bloom = water & sun;
```

Also acceptable:

```systemverilog
always_comb bloom = water & sun;
```

### Common student mistakes (L1)

| Symptom | Cause |
|---|---|
| `bloom` stuck 0 | Used `&&` in a way that still works—usually fine; or never saved file |
| `bloom` is 1 whenever water is 1 | Used OR `\|` |
| Simulation X | `bloom` never assigned |
| FPGA disagrees with sim | Wrong top (`top_level2` still selected); old bitstream |
| Used `always_ff` | Works coincidentally if they sample switches; still mark down vs spec |

---

## Level 2 expected FSM

```text
SEED + grow   → SPROUT
SEED otherwise → SEED

SPROUT + grow → BLOOM
SPROUT otherwise → SPROUT

BLOOM         → BLOOM

RESET         → SEED
```

`grow` is a 1-cycle pulse from the wrapper. In diagrams for students, labeling the arc `water AND sun` is fine.

Reference next-state:

```systemverilog
always_comb begin
    next_state = state;
    case (state)
        SEED:   if (grow) next_state = SPROUT;
        SPROUT: if (grow) next_state = BLOOM;
        BLOOM:  next_state = BLOOM;
        default: next_state = SEED;
    endcase
end
```

Outputs:

```text
SEED   → state_code = 0, led_seed
SPROUT → state_code = 1, led_sprout
BLOOM  → state_code = 2, led_bloom
```

### Common student mistakes (L2)

| Symptom | Cause |
|---|---|
| Instant BLOOM | Used `water & sun` levels inside the FSM instead of `grow` |
| Never leaves SEED | Forgot `if (grow)`; inverted reset; didn’t program L2 top |
| Oscillates / extra advances | No debounce (if they bypassed wrapper); BTNU held |
| Latch inferred | Missing default `next_state = state` or incomplete case |
| Sim OK, board not | Async reset polarity; didn’t hit BTNC; switches not both on |
| `state` X in sim | Forgot to reset at time 0 in their own tb |

---

## Oral check questions

Level 1: “If I turn sun off, does the bloom LED remember? Why not?”

Level 2: “Point to the flip-flops in your code.” (the `always_ff` block)

Level 2: “Why didn’t we clock the FSM with the raw AND of two switches?”

---

## Solutions location

Canonical RTL:

- `solutions/flower_level1.sv`  
- `solutions/flower_level2.sv`  

Wrappers, UART, debounce, and testbenches in `rtl/` are instructor-complete on purpose so students only edit the flower modules.

---

## Visualizer troubleshooting

- Wrong COM port; another program (Vivado hw_server) usually does **not** take UART, but serial terminals do.  
- TX/RX swapped in XDC (must be FPGA **TX** = A18).  
- Baud mismatch.  
- Students still running `top_level1` (no UART).  

---

## Accessibility / remote backup

If boards fail, students can still be assessed on:

- Pre-lab + diagrams  
- Passing xsim / Vivado sim  
- Walk-through of the FSM on a projector  

A recorded “golden board” video is useful as a demo, not as a substitute for the one group that never got USB drivers.

---

## Optional closing discussion prompts

- Where else do you see FSMs? (elevators, protocols, games, traffic lights)  
- What would a processor be, in this language? (a very large FSM plus datapath)  
- Why companies simulate for weeks before tapeout  
