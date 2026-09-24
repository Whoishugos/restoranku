#!/usr/bin/env python3
"""Generate Gambar 3.1 — Alur Penelitian metode Waterfall.

Matches the classic skripsi flowchart style: white background, black-bordered
rectangles, black arrows, with a three-way parallel branch after Analisis
Kebutuhan that merges before Desain Sistem.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT_DIRS = [
    Path("/workspace/docs/proposal"),
    Path("/opt/cursor/artifacts"),
]
FILENAME = "gambar-3-1-alur-waterfall.png"

BG = "#FFFFFF"
EDGE = "#000000"
TEXT = "#000000"
ARROW = "#000000"
CAPTION = "#222222"
CAPTION_SUB = "#555555"

# Box geometry (axes coordinates 0–100)
BOX_H = 4.2
BOX_W_MAIN = 38.0
BOX_W_START = 18.0
BOX_W_SIDE = 23.0
BOX_W_CENTER = 30.0

LINE_W = 1.35
ARROW_MUT = 12
FONT = "DejaVu Sans"


def _box(ax, cx, cy, w, h, label, *, rounded=False, fontsize=10.5, multiline=False):
    """Draw a black-bordered white rectangle centered at (cx, cy)."""
    style = "round,pad=0.12,rounding_size=0.85" if rounded else "square,pad=0.05"
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2),
        w,
        h,
        boxstyle=style,
        facecolor=BG,
        edgecolor=EDGE,
        linewidth=LINE_W,
        zorder=3,
    )
    ax.add_patch(patch)
    ax.text(
        cx,
        cy,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold" if rounded else "normal",
        color=TEXT,
        fontfamily=FONT,
        zorder=4,
        linespacing=1.25 if multiline else 1.0,
    )
    return cy - h / 2, cy + h / 2  # bottom, top


def _vline_arrow(ax, x, y_from, y_to):
    """Vertical arrow from y_from (higher) down to y_to (lower)."""
    arrow = FancyArrowPatch(
        (x, y_from),
        (x, y_to),
        arrowstyle="-|>",
        mutation_scale=ARROW_MUT,
        linewidth=LINE_W,
        color=ARROW,
        zorder=2,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(arrow)


def _hline(ax, x0, x1, y):
    ax.plot([x0, x1], [y, y], color=ARROW, linewidth=LINE_W, zorder=2, solid_capstyle="butt")


def draw_flowchart(out_path: Path, dpi: int = 300) -> None:
    fig, ax = plt.subplots(figsize=(9.0, 14.0), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("auto")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    cx = 50.0
    gap = 2.35  # vertical gap between box edge and next arrow tip / bar

    # --- 1. Mulai ---
    y = 94.0
    bot, _ = _box(ax, cx, y, BOX_W_START, BOX_H, "Mulai", rounded=True, fontsize=11)

    # --- 2. Analisis Kebutuhan ---
    y_arrow_end = bot - gap
    y_next = y_arrow_end - BOX_H / 2
    _vline_arrow(ax, cx, bot - 0.05, y_arrow_end + 0.05)
    bot, top = _box(ax, cx, y_next, BOX_W_MAIN, BOX_H, "Analisis Kebutuhan", fontsize=10.5)

    # --- 3. Fork into three parallel boxes ---
    fork_y = bot - gap * 0.85
    ax.plot([cx, cx], [bot - 0.05, fork_y], color=ARROW, linewidth=LINE_W, zorder=2)

    # Column centers for the three parallel boxes (gap between boxes)
    left_x = 18.0
    mid_x = 50.0
    right_x = 82.0
    _hline(ax, left_x, right_x, fork_y)

    # Parallel boxes (center label wraps to two lines like the example)
    par_h = 5.4
    y_par = fork_y - gap - par_h / 2 - 0.15
    for x in (left_x, mid_x, right_x):
        _vline_arrow(ax, x, fork_y, y_par + par_h / 2 + 0.05)

    bot_l, _ = _box(
        ax, left_x, y_par, BOX_W_SIDE, par_h, "Identifikasi Masalah",
        fontsize=9.5,
    )
    bot_m, _ = _box(
        ax, mid_x, y_par, BOX_W_CENTER, par_h,
        "Menentukan Tujuan dan\nRuang Lingkup Penelitian",
        fontsize=9.0, multiline=True,
    )
    bot_r, _ = _box(
        ax, right_x, y_par, BOX_W_SIDE, par_h, "Pengumpulan Data",
        fontsize=9.5,
    )
    # Use lowest bottom among the three (they share the same cy/h)
    par_bot = min(bot_l, bot_m, bot_r)

    # --- 4. Join / merge ---
    join_y = par_bot - gap * 0.85
    for x in (left_x, mid_x, right_x):
        # Plain drop lines into the join bar (classic fork-join look)
        ax.plot([x, x], [par_bot - 0.05, join_y], color=ARROW, linewidth=LINE_W, zorder=2)
    _hline(ax, left_x, right_x, join_y)

    # Arrow from join center down to Desain Sistem
    y_arrow_end = join_y - gap
    y_desain = y_arrow_end - BOX_H / 2
    _vline_arrow(ax, cx, join_y, y_arrow_end + 0.05)
    bot, _ = _box(ax, cx, y_desain, BOX_W_MAIN, BOX_H, "Desain Sistem", fontsize=10.5)

    # --- Linear cascade ---
    linear = [
        "Penulisan Kode (Coding)",
        "Pengujian Sistem (Blackbox Testing)",
        "Penerapan dan Pemeliharaan",
    ]
    for label in linear:
        y_arrow_end = bot - gap
        y_next = y_arrow_end - BOX_H / 2
        _vline_arrow(ax, cx, bot - 0.05, y_arrow_end + 0.05)
        # Slightly wider for longer labels
        w = 46.0 if "Blackbox" in label or "Pemeliharaan" in label else BOX_W_MAIN
        if "Penulisan" in label:
            w = 40.0
        bot, _ = _box(ax, cx, y_next, w, BOX_H, label, fontsize=10.2)

    # --- Selesai ---
    y_arrow_end = bot - gap
    y_end = y_arrow_end - BOX_H / 2
    _vline_arrow(ax, cx, bot - 0.05, y_arrow_end + 0.05)
    _box(ax, cx, y_end, BOX_W_START, BOX_H, "Selesai", rounded=True, fontsize=11)

    # Caption (skripsi)
    ax.text(
        50,
        4.8,
        "Gambar 3.1 Alur Penelitian menggunakan metode waterfall",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color=CAPTION,
        fontfamily=FONT,
    )
    ax.text(
        50,
        2.7,
        "Sumber: Diadaptasi dari model Waterfall (Pressman, 2015)",
        ha="center",
        va="center",
        fontsize=7.5,
        color=CAPTION_SUB,
        fontfamily=FONT,
        style="italic",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.35,
        facecolor=BG,
        edgecolor="none",
    )
    plt.close(fig)
    print(f"Wrote: {out_path} ({out_path.stat().st_size} bytes)")


def main() -> None:
    primary = OUT_DIRS[0] / FILENAME
    draw_flowchart(primary, dpi=300)
    for d in OUT_DIRS[1:]:
        dest = d / FILENAME
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(primary.read_bytes())
        print(f"Copied: {dest}")

    caption = OUT_DIRS[0] / "gambar-3-1-caption.txt"
    caption.write_text(
        "Gambar 3.1 Alur Penelitian menggunakan metode waterfall\n",
        encoding="utf-8",
    )
    print(f"Caption: {caption}")


if __name__ == "__main__":
    main()
