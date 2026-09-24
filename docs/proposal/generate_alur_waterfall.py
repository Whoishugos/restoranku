#!/usr/bin/env python3
"""Generate Gambar 3.1 — Alur Penelitian metode Waterfall (academic cascade)."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

OUT_DIRS = [
    Path("/workspace/docs/proposal"),
    Path("/opt/cursor/artifacts"),
]
FILENAME = "gambar-3-1-alur-waterfall.png"

NAVY = "#1B3A5F"
BOX_EDGE = "#0D2137"
ARROW = "#111111"
BG = "#FFFFFF"
SUB = "#DCE6F0"

STAGES = [
    ("Analisis Kebutuhan", "(Requirement Analysis)"),
    ("Perancangan Sistem", "(System Design)"),
    ("Implementasi", "(Implementation)"),
    ("Pengujian", "Black-Box Testing & UAT"),
    ("Pemeliharaan", "(Maintenance)"),
]


def draw_flowchart(out_path: Path, dpi: int = 300) -> None:
    # Portrait, print-friendly (approx A4 content area)
    fig, ax = plt.subplots(figsize=(7.2, 10.2), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("auto")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Title block
    ax.text(
        50,
        96.2,
        "Alur Penelitian menggunakan metode Waterfall",
        ha="center",
        va="center",
        fontsize=12.5,
        fontweight="bold",
        color="#111111",
        fontfamily="DejaVu Sans",
    )
    ax.text(
        50,
        93.0,
        "Model Waterfall — Siklus Hidup Pengembangan Sistem",
        ha="center",
        va="center",
        fontsize=8.5,
        color="#555555",
        fontfamily="DejaVu Sans",
        style="italic",
    )

    n = len(STAGES)
    # Classic cascading trapezoids: top widest, bottom narrowest
    top_width = 72
    bottom_width = 42
    stage_h = 10.2
    top_y = 88.5
    gap = 4.0
    center_x = 50.0

    stage_centers = []

    for i, (title, subtitle) in enumerate(STAGES):
        # Linear taper for cascade look
        t0 = i / n
        t1 = (i + 1) / n
        w_top = top_width - (top_width - bottom_width) * t0
        w_bot = top_width - (top_width - bottom_width) * t1

        y_top = top_y - i * (stage_h + gap)
        y_bot = y_top - stage_h

        # Slight rightward cascade (waterfall step)
        shift = i * 1.8
        cx = center_x + shift - (n - 1) * 0.9

        pts = [
            (cx - w_top / 2, y_top),
            (cx + w_top / 2, y_top),
            (cx + w_bot / 2, y_bot),
            (cx - w_bot / 2, y_bot),
        ]
        poly = Polygon(
            pts,
            closed=True,
            facecolor=NAVY,
            edgecolor=BOX_EDGE,
            linewidth=1.7,
            zorder=2,
        )
        ax.add_patch(poly)

        mid_y = (y_top + y_bot) / 2
        ax.text(
            cx,
            mid_y + 1.35,
            title,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="white",
            fontfamily="DejaVu Sans",
            zorder=3,
        )
        ax.text(
            cx,
            mid_y - 1.55,
            subtitle,
            ha="center",
            va="center",
            fontsize=8.5,
            color=SUB,
            fontfamily="DejaVu Sans",
            zorder=3,
        )

        # Stage number on left
        badge_x = cx - max(w_top, w_bot) / 2 - 4.5
        circle = plt.Circle(
            (badge_x, mid_y),
            1.55,
            facecolor="white",
            edgecolor=BOX_EDGE,
            linewidth=1.35,
            zorder=4,
        )
        ax.add_patch(circle)
        ax.text(
            badge_x,
            mid_y,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=NAVY,
            fontfamily="DejaVu Sans",
            zorder=5,
        )

        stage_centers.append((cx, y_top, y_bot, w_bot))

    # Downward arrows between stages
    for i in range(n - 1):
        cx, _, y_bot, _ = stage_centers[i]
        cx2, y_top2, _, _ = stage_centers[i + 1]
        arrow = FancyArrowPatch(
            (cx, y_bot - 0.25),
            (cx2, y_top2 + 0.35),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.7,
            color=ARROW,
            zorder=1,
        )
        ax.add_patch(arrow)

    # Caption
    ax.text(
        50,
        5.8,
        "Gambar 3.1 Alur Penelitian menggunakan metode waterfall",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="#222222",
        fontfamily="DejaVu Sans",
    )
    ax.text(
        50,
        3.5,
        "Sumber: Diadaptasi dari model Waterfall (Pressman, 2015)",
        ha="center",
        va="center",
        fontsize=7.5,
        color="#555555",
        fontfamily="DejaVu Sans",
        style="italic",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.3,
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
