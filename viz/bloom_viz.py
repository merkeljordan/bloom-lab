"""Bloom visualizer — FPGA is the source of truth.

Reads ASCII '0' / '1' / '2' at 115200 baud from the Basys 3 USB-UART
and draws the flower in a window. Usage:

    python bloom_viz.py               # no board: demo, click to grow
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


class BloomApp:
    def __init__(self, root: tk.Tk, port: str | None) -> None:
        self.root = root
        self.stage = 0
        self.t = 1.0
        self.anim_id: str | None = None
        self.events: queue.Queue[tuple[str, str]] = queue.Queue()

        head = pick_font(root, "Baloo 2", "Nunito", "Segoe UI Semibold", "Segoe UI")
        body = pick_font(root, "Nunito", "Segoe UI")

        root.title("Bloom")
        root.configure(bg=PAPER, padx=24, pady=18)
        root.resizable(False, False)

        tk.Label(root, text="Bloom", font=(head, 30, "bold"), fg=PINK_DEEP, bg=PAPER).pack()
        tk.Label(root, text="your flower, live from the FPGA", font=(body, 11), fg=MUTED, bg=PAPER).pack()

        frame = tk.Frame(root, bg=BLUSH, padx=0, pady=0)
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

        self.status = tk.Label(root, font=(body, 9), fg=MUTED, bg=PAPER, wraplength=340)
        self.status.pack(pady=(4, 0))

        self.body_font = body
        self.draw()

        if port:
            self.status.config(text=f"Listening on {port}. Press BTNC to reset, then grow the flower.")
            threading.Thread(target=self.read_serial, args=(port,), daemon=True).start()
            self.poll()
        else:
            self.status.config(text="Demo mode, no board connected. Click the flower to grow it.")
            self.canvas.bind("<Button-1>", lambda _e: self.set_stage((self.stage + 1) % 3))
            root.bind("<space>", lambda _e: self.set_stage((self.stage + 1) % 3))

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
                ch = ser.read(1).decode("ascii", errors="ignore")
                if ch and ch in "012":
                    self.events.put(("stage", ch))

    def poll(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "stage":
                    self.set_stage(int(value))
                else:
                    self.status.config(text=value, fg=PINK_DEEP)
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

    def leaf(self, x: float, y: float, d: int, s: float) -> None:
        pts = [x, y, x + d * 18 * s, y - 20 * s, x + d * 44 * s, y - 14 * s, x + d * 26 * s, y + 2 * s]
        self.canvas.create_polygon(pts, fill=GREEN_LIGHT, outline=GREEN, width=2, smooth=True)

    def draw(self) -> None:
        c, s = self.canvas, self.stage
        t = 1 - (1 - self.t) ** 3
        c.delete("all")
        cx, ground = 170, 222

        for x, y in [(40, 40), (300, 60), (60, 150), (290, 170), (30, 250), (310, 270)]:
            c.create_oval(x - 2, y - 2, x + 2, y + 2, fill=BLUSH, outline="")

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
                    for x, y, size in [(cx - 72, top - 10, 16), (cx + 70, top + 18, 12), (cx + 52, top - 40, 10)]:
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
            l.create_text(x, 54, text=f"LD{i}  {name}", fill=INK if on else MUTED,
                          font=(self.body_font, 9, "bold" if on else "normal"))


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--demo"]
    root = tk.Tk()
    BloomApp(root, args[0] if args else None)
    root.mainloop()


if __name__ == "__main__":
    main()
