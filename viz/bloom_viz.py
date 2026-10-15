"""Bloom visualizer — FPGA is the source of truth.

Reads one byte about 10 times per second at 115200 baud from the Basys 3
USB-UART: 0x30 + {sun, water, state_code}, i.e. ASCII '0'..'?'.
Draws the flower, the rain (SW0 water) and the sun (SW1 sun). Usage:

    python bloom_viz.py               # no board: demo with on-screen switches
    python -m pip install pyserial    # needed only with a board
    python bloom_viz.py COM5          # Windows
    python bloom_viz.py /dev/ttyUSB1  # Linux
    python bloom_viz.py /dev/tty.usbserial-XXXX  # macOS
"""

from __future__ import annotations

import math
import queue
import sys
import threading
import tkinter as tk
from tkinter import font as tkfont

PAPER = "#fff4f8"
CARD = "#ffffff"
INK = "#5a2438"
MUTED = "#8a4d62"
PINK = "#e86b96"
PINK_SOFT = "#f7a1c0"
PINK_DEEP = "#c73e72"
BLUSH = "#ffd6e6"
LINE = "#ffc2d6"
GREEN = "#5fae7c"
GREEN_LIGHT = "#86cfa0"
SOIL = "#7a4a3a"
POT = "#f6b1c7"
POT_RIM = "#ee96b4"
CHEEK = "#ff9fbf"
YELLOW = "#ffd36b"
SUN = "#ffcf4d"
SUN_RAY = "#ffb938"
CLOUD = "#e3f1fb"
RAIN = "#7fc4ec"
SEED = "#c98a5a"
LED_OFF = "#f3e3ea"

STAGES = [
    ("SEED", "Just planted"),
    ("SPROUT", "Growing..."),
    ("BLOOM", "In bloom!"),
]


def pick_font(root: tk.Tk, *names: str) -> str:
    available = set(tkfont.families(root))
    return next((n for n in names if n in available), "TkDefaultFont")


def decode(byte: int) -> tuple[int, bool, bool] | None:
    v = byte - 0x30
    if not 0 <= v <= 15 or (v & 3) == 3:
        return None
    return v & 3, bool(v & 4), bool(v & 8)


class BloomApp:
    def __init__(self, root: tk.Tk, port: str | None) -> None:
        self.root = root
        self.stage = 0
        self.water = False
        self.sun = False
        self.t = 1.0
        self.phase = 0
        self.anim_id: str | None = None
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()

        head = pick_font(root, "Baloo 2", "Nunito", "Segoe UI Semibold", "Segoe UI")
        body = pick_font(root, "Nunito", "Segoe UI")
        self.body_font = body

        root.title("Bloom")
        root.configure(bg=PAPER, padx=24, pady=18)
        root.resizable(False, False)

        tk.Label(root, text="Bloom", font=(head, 30, "bold"), fg=PINK_DEEP, bg=PAPER).pack()
        tk.Label(root, text="your flower, live from the FPGA", font=(body, 11), fg=MUTED, bg=PAPER).pack()

        frame = tk.Frame(root, bg=BLUSH)
        frame.pack(pady=(14, 10))
        self.canvas = tk.Canvas(
            frame, width=340, height=300, bg=CARD,
            highlightthickness=2, highlightbackground=LINE,
        )
        self.canvas.pack(padx=(0, 6), pady=(0, 6))

        self.stage_label = tk.Label(root, font=(head, 22, "bold"), fg=INK, bg=PAPER)
        self.stage_label.pack()
        self.caption = tk.Label(root, font=(body, 11), fg=MUTED, bg=PAPER)
        self.caption.pack()

        self.leds = tk.Canvas(root, width=340, height=64, bg=PAPER, highlightthickness=0)
        self.leds.pack(pady=(8, 4))

        if not port:
            self.build_controls()

        self.status = tk.Label(root, font=(body, 9), fg=MUTED, bg=PAPER, wraplength=340)
        self.status.pack(pady=(6, 0))

        self.draw()
        self.tick()

        if port:
            self.status.config(text=f"Listening on {port}. Press BTNC to reset, then flip the switches.")
            threading.Thread(target=self.read_serial, args=(port,), daemon=True).start()
            self.poll()
        else:
            self.status.config(text="Demo mode, no board connected. These buttons stand in for the switches.")

    def pill(self, parent: tk.Widget, text: str, command) -> tk.Label:
        b = tk.Label(parent, text=text, font=(self.body_font, 10, "bold"), fg=PINK_DEEP, bg=CARD,
                     padx=12, pady=5, cursor="hand2", highlightthickness=2, highlightbackground=LINE)
        b.bind("<Button-1>", lambda _e: command())
        return b

    def build_controls(self) -> None:
        row = tk.Frame(self.root, bg=PAPER)
        row.pack(pady=(4, 0))
        self.water_btn = self.pill(row, "Water  SW0", lambda: self.demo_switch(water=not self.water))
        self.sun_btn = self.pill(row, "Sun  SW1", lambda: self.demo_switch(sun=not self.sun))
        for b in (self.water_btn, self.sun_btn):
            b.pack(side="left", padx=4)
        self.pill(row, "Grow  BTNU", self.demo_grow).pack(side="left", padx=4)
        self.pill(row, "Reset  BTNC", self.demo_reset).pack(side="left", padx=4)

    def demo_switch(self, water: bool | None = None, sun: bool | None = None) -> None:
        was_both = self.water and self.sun
        self.water = self.water if water is None else water
        self.sun = self.sun if sun is None else sun
        for b, on in ((self.water_btn, self.water), (self.sun_btn, self.sun)):
            b.config(bg=PINK if on else CARD, fg=CARD if on else PINK_DEEP)
        if self.water and self.sun and not was_both:
            self.set_stage(min(self.stage + 1, 2))
        self.draw()

    def demo_grow(self) -> None:
        if self.water and self.sun:
            self.set_stage(min(self.stage + 1, 2))

    def demo_reset(self) -> None:
        self.set_stage(0)

    def read_serial(self, port: str) -> None:
        try:
            import serial  # type: ignore
        except ImportError:
            self.events.put(("error", "Install pyserial first:  python -m pip install pyserial"))
            return
        try:
            ser = serial.Serial(port, 115200, timeout=1)
        except Exception as exc:
            self.events.put(("error", f"Couldn't open {port}: {exc}"))
            return
        with ser:
            while True:
                raw = ser.read(1)
                if raw and (msg := decode(raw[0])):
                    self.events.put(("state", msg))

    def poll(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "state":
                    stage, self.water, self.sun = value  # type: ignore[misc]
                    self.set_stage(stage)
                    self.draw()
                else:
                    self.status.config(text=str(value), fg=PINK_DEEP)
        except queue.Empty:
            pass
        self.root.after(30, self.poll)

    def set_stage(self, stage: int) -> None:
        if stage == self.stage:
            return
        self.stage = stage
        self.t = 0.0
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
        self.animate()

    def animate(self) -> None:
        self.t = min(1.0, self.t + 0.07)
        self.draw()
        self.anim_id = self.root.after(16, self.animate) if self.t < 1.0 else None

    def tick(self) -> None:
        self.phase += 1
        if (self.water or self.sun) and self.anim_id is None:
            self.draw()
        self.root.after(50, self.tick)

    def leaf(self, x: float, y: float, d: int, s: float) -> None:
        pts = [x, y, x + d * 18 * s, y - 20 * s, x + d * 44 * s, y - 14 * s, x + d * 26 * s, y + 2 * s]
        self.canvas.create_polygon(pts, fill=GREEN_LIGHT, outline=GREEN, width=2, smooth=True)

    def draw_sun(self) -> None:
        c = self.canvas
        x, y, r = 56, 54, 22
        spin = self.phase * 2
        for i in range(8):
            a = math.radians(i * 45 + spin)
            c.create_line(x + math.cos(a) * (r + 6), y + math.sin(a) * (r + 6),
                          x + math.cos(a) * (r + 14), y + math.sin(a) * (r + 14),
                          fill=SUN_RAY, width=4, capstyle="round")
        c.create_oval(x - r, y - r, x + r, y + r, fill=SUN, outline="")
        c.create_oval(x - 9, y - 5, x - 5, y - 1, fill=INK, outline="")
        c.create_oval(x + 5, y - 5, x + 9, y - 1, fill=INK, outline="")
        c.create_arc(x - 6, y - 2, x + 6, y + 8, start=200, extent=140, style="arc", outline=INK, width=2)
        c.create_oval(x - 16, y + 2, x - 9, y + 7, fill=CHEEK, outline="")
        c.create_oval(x + 9, y + 2, x + 16, y + 7, fill=CHEEK, outline="")

    def draw_rain(self) -> None:
        c = self.canvas
        cx, cy = 262, 46
        for dx, dy, r in [(-26, 6, 16), (-6, -4, 22), (18, 4, 18), (34, 10, 12)]:
            c.create_oval(cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r, fill=CLOUD, outline="")
        c.create_rectangle(cx - 40, cy + 6, cx + 44, cy + 22, fill=CLOUD, outline="")
        for i in range(10):
            col = i % 5
            x = cx - 30 + col * 16
            fall = ((i // 5) * 75 + col * 29 + self.phase * 7) % 150
            drift = fall * 0.15
            y = cy + 26 + fall
            c.create_line(x - drift, y, x - drift - 2, y + 10, fill=RAIN, width=3, capstyle="round")

    def draw(self) -> None:
        c, s = self.canvas, self.stage
        t = 1 - (1 - self.t) ** 3
        c.delete("all")
        cx, ground = 170, 222

        for x, y in [(40, 120), (300, 110), (60, 170), (290, 190), (30, 250), (310, 270)]:
            c.create_oval(x - 2, y - 2, x + 2, y + 2, fill=BLUSH, outline="")

        if self.sun:
            self.draw_sun()
        if self.water:
            self.draw_rain()

        c.create_polygon(112, 228, 228, 228, 214, 290, 126, 290, fill=POT, outline="")
        c.create_rectangle(102, 214, 238, 232, fill=POT_RIM, outline="")
        c.create_oval(112, 216, 228, 230, fill=SOIL, outline="")

        if s == 0:
            r = 9 * t
            c.create_oval(cx - r, ground - 8 - r * 0.7, cx + r, ground - 8 + r * 0.7, fill=SEED, outline="")
        else:
            h = 70 * t if s == 1 else 70 + 65 * t
            top = ground - h
            c.create_line(cx, ground, cx + 5, ground - h / 2, cx, top,
                          fill=GREEN, width=6, capstyle="round", smooth=True)
            if s == 1:
                self.leaf(cx, top + 6, -1, 0.8 * t)
                self.leaf(cx, top + 6, 1, 0.8 * t)
            else:
                self.leaf(cx + 2, ground - 45, -1, 1)
                self.leaf(cx + 3, ground - 70, 1, 1)
                for i in range(6):
                    a = math.radians(i * 60 - 90)
                    px, py = cx + math.cos(a) * 22 * t, top + math.sin(a) * 22 * t
                    r = 17 * t
                    c.create_oval(px - r, py - r, px + r, py + r,
                                  fill=PINK if i % 2 else PINK_SOFT, outline="")
                r = 12 * t
                c.create_oval(cx - r, top - r, cx + r, top + r, fill=YELLOW, outline="")
                if self.t >= 1:
                    for x, y, size in [(cx - 62, top + 20, 14), (cx + 58, top + 30, 11), (cx - 44, top - 34, 10)]:
                        c.create_text(x, y, text="✦", fill=PINK, font=(self.body_font, size))

        c.create_oval(cx - 25, 249, cx - 19, 255, fill=INK, outline="")
        c.create_oval(cx + 19, 249, cx + 25, 255, fill=INK, outline="")
        c.create_arc(cx - 8, 248, cx + 8, 262, start=200, extent=140, style="arc", outline=INK, width=2)
        c.create_oval(cx - 42, 257, cx - 28, 265, fill=CHEEK, outline="")
        c.create_oval(cx + 28, 257, cx + 42, 265, fill=CHEEK, outline="")

        name, caption = STAGES[s]
        self.stage_label.config(text=name)
        self.caption.config(text=caption)
        self.draw_leds()

    def draw_leds(self) -> None:
        l = self.leds
        l.delete("all")
        for i, name in enumerate(["seed", "sprout", "bloom"]):
            x = 70 + i * 100
            on = i == self.stage
            if on:
                l.create_oval(x - 18, 4, x + 18, 40, fill=BLUSH, outline="")
            l.create_oval(x - 11, 11, x + 11, 33, fill=PINK if on else LED_OFF,
                          outline=PINK_DEEP if on else LINE, width=2)
            l.create_text(x, 54, text=name, fill=INK if on else MUTED,
                          font=(self.body_font, 9, "bold" if on else "normal"))


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--demo"]
    root = tk.Tk()
    BloomApp(root, args[0] if args else None)
    root.mainloop()


if __name__ == "__main__":
    main()
