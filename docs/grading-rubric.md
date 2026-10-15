# Bloom Lab — Grading Rubric

Suggested total: **100 points**. Adjust weights for a workshop (credit/no-credit) vs. a graded course lab.

| Category | Points | Excellent | Adequate | Incomplete |
|---|---:|---|---|---|
| Pre-lab | 10 | Truth table, I/O list, and Bloom equation complete and correct | Mostly complete, minor errors | Missing or copied without understanding |
| Level 1 RTL | 15 | Synthesizable AND, ports match spec | Works but messy / extra sequential logic | Does not match spec |
| Level 1 simulation | 10 | Waveform / transcript matches all four rows | Most cases pass | Not simulated or wrong |
| Level 1 hardware | 10 | All four switch combinations match the table on the board | Works after coaching | Not demonstrated |
| Level 2 state diagram | 10 | Three states, labeled arcs, reset shown | Diagram present but incomplete | Missing |
| Level 2 RTL (FSM) | 20 | Register + next-state + outputs + async/sync reset as specified | FSM works but structure is tangled | Does not sequence correctly |
| Level 2 simulation | 10 | Tests 1–4 from the manual pass | Partial sequences | Not simulated |
| Level 2 hardware | 5 | Reset, stay, and grow behave on the board | Works with help | Not demonstrated |
| Lab conduct / checkpoints | 5 | Checkpoints filled, honest debugging notes | Partial | Blank |
| Reflection / challenge | 5 | Thoughtful answers; optional challenge attempted | Short answers | Missing |

## Workshop (ungraded) version

Use a **stamp sheet** instead of points:

1. Pre-lab complete  
2. Level 1 sim pass  
3. Level 1 FPGA demo  
4. Level 2 sim pass  
5. Level 2 FPGA demo  
6. Reflection started  

## Academic integrity

Students may discuss ideas, but each person (or assigned pair) submits **their own** RTL and written answers. Copying starter comments is expected; copying another group’s completed `assign` / `case` bodies is not.
