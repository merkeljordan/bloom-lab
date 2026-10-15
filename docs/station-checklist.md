# Bloom — Station setup checklist

One station = one computer + one Basys 3 + one micro-USB cable. Students should sit down to a project that is already open and only touch Vivado.

## 1. Weeks before

☐ Confirm every computer has Vivado installed (Standard edition is free and enough). It is a very large install; never leave it for the day.  
☐ Confirm the board's USB drivers work: plug in a Basys 3, **Open Hardware Manager → Open Target → Auto Connect** finds `xc7a35t`.  
☐ Ask whether students can run `.exe` files on these machines (needed only for the optional flower window).  
☐ Count stations, boards, and cables, plus one spare of each.

## 2. Build the kit (once, on your laptop)

☐ `python scripts/make_student_kit.py` → `dist/bloom-student-kit.zip` (and `dist/BloomViz.exe`).  
☐ Open the zip and check `rtl/flower_level1.sv` still says `TODO`. The script refuses to run if it doesn't.  
☐ Build a known-good bitstream for each level from `solutions/`. Name them `bloom_level1_good.bit` and `bloom_level2_good.bit`; keep them on a USB drive, **not** in the kit.  
☐ Print one `handout/index.html` per station (browser → Print, letter, one page).

## 3. Each station (day before)

☐ Unzip the kit to the same place on every machine, e.g. `C:\bloom-student-kit`. Avoid paths with spaces or apostrophes.  
☐ In Vivado: **Create Project** → RTL Project → part `xc7a35tcpg236-1`.  
☐ **Add Sources:** every `.sv` in `rtl/`. **Add Constraints:** `constraints/basys3_bloom.xdc`.  
☐ **Set as Top:** `top_level1` under Design Sources, `tb_flower_level1` under Simulation Sources.  
☐ Run Behavioral Simulation once. It should print `LEVEL1 TESTBENCH FAILED`, because the starter is blank. That proves the test runs.  
☐ Program `bloom_level1_good.bit` from the USB drive. Flip SW0 and SW1: LD0 lights only when both are up.  
☐ Program `bloom_level2_good.bit`. BTNC → LD0, both switches on → LD1, BTNU → LD2.  
☐ If using the flower window: double-click `BloomViz.exe`, pick the board's port, Connect, flip switches. Rain and sun should appear.  
☐ Close the simulation, leave the project open with `flower_level1.sv` showing, and label the board and cable with the station number.

## 4. Morning of

☐ Power on each board and check the DONE light after programming a good bitstream.  
☐ Printout at every station.  
☐ USB drive with the good bitstreams and a fresh copy of the kit at the front.  
☐ Your laptop: slides open, a board at the front, `BloomViz.exe` ready to show on the projector.  
☐ One helper per four or five stations; each helper has walked through section 3 once.

## 5. When a station breaks

| Problem | Fast fix |
|---|---|
| Hardware Manager can't find the board | Power switch, then another USB port, then the spare cable, then the spare board |
| Vivado won't open the project | Re-unzip the kit to a new folder and repeat section 3 (about 3 minutes) |
| Student file is a mess | Copy a fresh `flower_level*.sv` from the kit zip over it |
| Board works for nobody at that station | Program a good bitstream to check the board, then pair them with a neighbour |
| Flower window won't connect | Skip it. The LEDs are the real result |
