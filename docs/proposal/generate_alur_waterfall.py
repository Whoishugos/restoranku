#!/usr/bin/env python3
"""Generate Gambar 3.1 — Alur Penelitian metode Waterfall (detailed cascade)."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

OUT_DIRS = [
    Path("/workspace/docs/proposal"),
    Path("/opt/cursor/artifacts"),
]
FILENAME = "gambar-3-1-alur-waterfall.png"

NAVY = "#1B3A5F"
NAVY_DARK = "#0D2137"
HEADER = "#163552"
PANEL = "#F4F7FA"
PANEL_EDGE = "#C5D2E0"
SUB_TEXT = "#1A2A3A"
ARROW = "#111111"
BG = "#FFFFFF"
TITLE_SUB = "#555555"

# Main stage title + detailed sub-steps (Indonesian, skripsi Bab 3)
STAGES = [
    {
        "title": "Analisis Kebutuhan",
        "en": "Requirement Analysis",
        "steps": [
            "Observasi proses bisnis & alur kerja",
            "Wawancara pemangku kepentingan",
            "Studi pustaka & referensi sistem sejenis",
            "Identifikasi kebutuhan fungsional",
            "Identifikasi kebutuhan non-fungsional",
        ],
    },
    {
        "title": "Perancangan Sistem",
        "en": "System Design",
        "steps": [
            "Pemodelan Use Case Diagram",
            "Perancangan ERD (basis data)",
            "Pemodelan DFD (aliran data)",
            "Rancangan UI / antarmuka pengguna",
        ],
    },
    {
        "title": "Implementasi",
        "en": "Implementation — Penulisan Kode",
        "steps": [
            "Penulisan kode (coding) PHP / Laravel 12",
            "Implementasi basis data MySQL",
            "Integrasi QR Code",
            "Integrasi pembayaran Midtrans",
        ],
    },
    {
        "title": "Pengujian",
        "en": "Testing",
        "steps": [
            "Black-Box Testing (uji fungsionalitas)",
            "User Acceptance Testing (UAT)",
        ],
    },
    {
        "title": "Pemeliharaan",
        "en": "Maintenance",
        "steps": [
            "Deployment / hosting sistem",
            "Perbaikan & pemeliharaan berkala",
        ],
    },
]


def draw_flowchart(out_path: Path, dpi: int = 300) -> None:
    # Portrait, print-friendly; taller to fit sub-steps
    fig, ax = plt.subplots(figsize=(8.0, 13.2), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("auto")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Title block
    ax.text(
        50,
        97.4,
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
        95.2,
        "Model Waterfall — Siklus Hidup Pengembangan Sistem "
        "(dengan rincian tahap desain hingga penulisan kode)",
        ha="center",
        va="center",
        fontsize=7.8,
        color=TITLE_SUB,
        fontfamily="DejaVu Sans",
        style="italic",
    )

    n = len(STAGES)
    top_width = 78
    bottom_width = 52
    # Height budget: title ~4, caption ~6, gaps between stages, stages fill rest
    top_y = 92.5
    bottom_margin = 8.5
    gap = 2.6
    available = top_y - bottom_margin - (n - 1) * gap
    # Proportional heights by number of sub-steps (min readable)
    weights = [len(s["steps"]) + 1.6 for s in STAGES]
    total_w = sum(weights)
    heights = [available * (w / total_w) for w in weights]

    center_x = 50.0
    stage_centers = []
    y_cursor = top_y

    for i, stage in enumerate(STAGES):
        t0 = i / n
        t1 = (i + 1) / n
        w_top = top_width - (top_width - bottom_width) * t0
        w_bot = top_width - (top_width - bottom_width) * t1
        stage_h = heights[i]

        y_top = y_cursor
        y_bot = y_top - stage_h

        # Slight rightward cascade (waterfall step)
        shift = i * 1.6
        cx = center_x + shift - (n - 1) * 0.8

        # Outer cascade shell (navy)
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
            edgecolor=NAVY_DARK,
            linewidth=1.5,
            zorder=2,
        )
        ax.add_patch(poly)

        # Header band height (title area)
        header_h = min(2.55, stage_h * 0.28)
        # Inner light panel for sub-steps
        inset = 1.15
        panel_top = y_top - header_h - 0.25
        panel_bot = y_bot + 0.55
        # Approximate width at mid of panel
        mid_frac = (y_top - (panel_top + panel_bot) / 2) / stage_h if stage_h else 0.5
        w_mid = w_top - (w_top - w_bot) * mid_frac
        panel_w = max(w_mid - 2 * inset, 28)

        panel = FancyBboxPatch(
            (cx - panel_w / 2, panel_bot),
            panel_w,
            panel_top - panel_bot,
            boxstyle="round,pad=0.15,rounding_size=0.35",
            facecolor=PANEL,
            edgecolor=PANEL_EDGE,
            linewidth=0.9,
            zorder=3,
        )
        ax.add_patch(panel)

        # Stage title (in navy header)
        title_y = y_top - header_h / 2 - 0.05
        ax.text(
            cx,
            title_y + 0.35,
            stage["title"],
            ha="center",
            va="center",
            fontsize=11.2,
            fontweight="bold",
            color="white",
            fontfamily="DejaVu Sans",
            zorder=4,
        )
        ax.text(
            cx,
            title_y - 0.75,
            f"({stage['en']})",
            ha="center",
            va="center",
            fontsize=6.8,
            color="#C8D6E6",
            fontfamily="DejaVu Sans",
            zorder=4,
        )

        # Sub-steps inside panel
        steps = stage["steps"]
        panel_h = panel_top - panel_bot
        # Vertical layout of bullets
        line_gap = panel_h / (len(steps) + 0.85)
        start_y = panel_top - line_gap * 0.75
        left = cx - panel_w / 2 + 1.6

        for j, step in enumerate(steps):
            sy = start_y - j * line_gap
            # Bullet
            ax.plot(
                left,
                sy,
                "o",
                markersize=3.2,
                color=NAVY,
                zorder=5,
                markeredgewidth=0,
            )
            ax.text(
                left + 1.1,
                sy,
                step,
                ha="left",
                va="center",
                fontsize=7.6,
                color=SUB_TEXT,
                fontfamily="DejaVu Sans",
                zorder=5,
            )

        # Stage number badge on left
        badge_x = cx - max(w_top, w_bot) / 2 - 4.2
        circle = plt.Circle(
            (badge_x, (y_top + y_bot) / 2),
            1.45,
            facecolor="white",
            edgecolor=NAVY_DARK,
            linewidth=1.3,
            zorder=6,
        )
        ax.add_patch(circle)
        ax.text(
            badge_x,
            (y_top + y_bot) / 2,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=NAVY,
            fontfamily="DejaVu Sans",
            zorder=7,
        )

        stage_centers.append((cx, y_top, y_bot, w_bot))
        y_cursor = y_bot - gap

    # Downward arrows between stages
    for i in range(n - 1):
        cx, _, y_bot, _ = stage_centers[i]
        cx2, y_top2, _, _ = stage_centers[i + 1]
        arrow = FancyArrowPatch(
            (cx, y_bot - 0.15),
            (cx2, y_top2 + 0.2),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.55,
            color=ARROW,
            zorder=1,
        )
        ax.add_patch(arrow)

    # Caption
    ax.text(
        50,
        5.5,
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
        3.4,
        "Sumber: Diadaptasi dari model Waterfall (Pressman, 2015)",
        ha="center",
        va="center",
        fontsize=7.5,
        color=TITLE_SUB,
        fontfamily="DejaVu Sans",
        style="italic",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.28,
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
