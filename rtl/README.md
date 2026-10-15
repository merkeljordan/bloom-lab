# RTL file map

| File | Edit? | Role |
|---|---|---|
| `flower_level1.sv` | Tested copy | Combinational bloom (`water & sun`) |
| `flower_level2.sv` | Tested copy | 3-state FSM |
| `starters/flower_level1.sv` | **Yes (students)** | Level 1 with `TODO`s |
| `starters/flower_level2.sv` | **Yes (students)** | Level 2 with `TODO`s |
| `tb_flower_level1.sv` | No | Self-checking sim |
| `tb_flower_level2.sv` | No | Self-checking sim |
| `top_level1.sv` | No | Board wrapper |
| `top_level2.sv` | No | Board wrapper + grow pulse + UART |
| `sync_debounce.sv` | No | Switch/button filter |
| `rise_pulse.sv` | No | Edge → 1-cycle `grow` |
| `uart_tx.sv` | No | 115200 8N1 TX |

Simulation tops: `tb_flower_level1`, `tb_flower_level2`  
FPGA tops: `top_level1`, `top_level2`
