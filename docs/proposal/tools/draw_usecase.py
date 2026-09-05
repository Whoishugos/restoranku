"""Use Case Diagram: Koki hanya dapur, Kasir hanya pembayaran, tanpa garis silang."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Circle


OUT = Path("/tmp/rev/usecase_diagram.png")

fig, ax = plt.subplots(figsize=(16.4, 10.6), dpi=200)
ax.set_xlim(0, 16.4)
ax.set_ylim(0, 10.6)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

NAVY = "#1f4e79"
GREEN = "#0b6e4f"
ORANGE = "#9a3412"
BLUE = "#1d4ed8"
INK = "#16324f"


def stick(x, y, label, color):
    """y is the chest/line-anchor height."""
    ax.add_patch(Circle((x, y + 0.34), 0.155, fill=False, lw=1.7, color=color, zorder=6))
    ax.plot([x, x], [y + 0.185, y - 0.16], color=color, lw=1.7, zorder=6)
    ax.plot([x - 0.22, x + 0.22], [y + 0.08, y + 0.08], color=color, lw=1.7, zorder=6)
    ax.plot([x, x - 0.18], [y - 0.16, y - 0.48], color=color, lw=1.7, zorder=6)
    ax.plot([x, x + 0.18], [y - 0.16, y - 0.48], color=color, lw=1.7, zorder=6)
    ax.text(x, y - 0.74, label, ha="center", va="top", fontsize=11, fontweight="bold", color=color, zorder=6)
    return {"x": x, "y": y, "color": color}


def oval(x, y, w, h, text, fill, edge):
    ax.add_patch(Ellipse((x, y), w, h, facecolor=fill, edgecolor=edge, lw=1.5, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=7.8, color=INK, zorder=4, linespacing=1.12)
    return {"c": (x, y), "L": (x - w / 2.0, y), "R": (x + w / 2.0, y)}


def H(x0, x1, y, color, lw=1.35):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=2, solid_capstyle="round")


def V(x, y0, y1, color, lw=1.35):
    ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=2, solid_capstyle="round")


# Band backgrounds — make actor ownership unmistakable even before reading lines
ax.add_patch(
    FancyBboxPatch(
        (3.00, 4.92),
        7.55,
        0.96,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        facecolor="#dcfce7",
        edgecolor="#86efac",
        lw=0.7,
        zorder=1.2,
        alpha=0.55,
    )
)
ax.add_patch(
    FancyBboxPatch(
        (3.00, 1.72),
        7.55,
        0.96,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        facecolor="#ffedd5",
        edgecolor="#fdba74",
        lw=0.7,
        zorder=1.2,
        alpha=0.55,
    )
)
# System boundary
ax.add_patch(
    FancyBboxPatch(
        (2.78, 0.28),
        10.62,
        9.78,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#fbfcfe",
        edgecolor=NAVY,
        lw=1.7,
        zorder=1,
    )
)
ax.text(
    8.09,
    9.74,
    "Sistem Pemesanan Menu — Restoran Kekupu Villa Jembrana",
    ha="center",
    va="center",
    fontsize=10.4,
    fontweight="bold",
    color=NAVY,
    zorder=4,
)

# Actor chest heights = exclusive use-case row heights
Y_ADMIN = 8.55
Y_KOKI = 5.40
Y_KASIR = 2.20
Y_LOGIN = 3.80  # gap between Koki band and Kasir band

admin = stick(1.20, Y_ADMIN, "Admin", NAVY)
koki = stick(1.20, Y_KOKI, "Koki", GREEN)
kasir = stick(1.20, Y_KASIR, "Kasir", ORANGE)
pelanggan = stick(15.20, 5.40, "Pelanggan", BLUE)

# ---- Use cases ----
uc_menu = oval(5.55, 8.55, 3.20, 0.82, "Kelola menu, kategori,\nadd-on, dan stok", "#e8f1fa", NAVY)
uc_user = oval(8.95, 8.55, 2.80, 0.78, "Kelola karyawan\ndan role", "#e8f1fa", NAVY)
uc_qr = oval(5.55, 7.48, 2.60, 0.72, "Bangkitkan QR meja", "#e8f1fa", NAVY)
uc_dash = oval(8.95, 7.48, 2.60, 0.72, "Akses dashboard", "#e8f1fa", NAVY)
uc_lap = oval(8.95, 6.42, 2.80, 0.78, "Lihat riwayat pesanan\ndan export laporan", "#e8f1fa", NAVY)

# Login in the GAP between Koki (5.40) and Kasir (2.20)
uc_login = oval(5.55, Y_LOGIN, 2.50, 0.70, "Login staf", "#f4f4f5", "#52525b")

# Koki — both ovals on the SAME row as the Koki actor
uc_antrean = oval(5.55, Y_KOKI, 2.75, 0.80, "Lihat antrean\npesanan dapur", "#e6f6ee", GREEN)
uc_dapur = oval(8.95, Y_KOKI, 2.80, 0.80, "Update status dapur", "#e6f6ee", GREEN)

# Kasir — both primary ovals on the SAME row as the Kasir actor
uc_daftar = oval(5.55, Y_KASIR, 2.75, 0.78, "Lihat daftar\npembayaran", "#fff1e7", ORANGE)
uc_tunai = oval(8.95, Y_KASIR, 2.85, 0.80, "Konfirmasi bayar tunai", "#fff1e7", ORANGE)
uc_nota = oval(5.55, 1.12, 2.50, 0.70, "Cetak nota", "#fff1e7", ORANGE)
uc_midtrans = oval(8.95, 1.12, 2.85, 0.78, "Pantau pembayaran\nMidtrans", "#fff1e7", ORANGE)

# Pelanggan
uc_scan = oval(12.00, 8.20, 2.70, 0.78, "Scan QR / lihat menu", "#eaf0ff", BLUE)
uc_addon = oval(12.00, 7.12, 2.55, 0.72, "Pilih add-on", "#eaf0ff", BLUE)
uc_cart = oval(12.00, 6.08, 2.55, 0.72, "Kelola keranjang", "#eaf0ff", BLUE)
uc_check = oval(12.00, 5.04, 2.55, 0.72, "Checkout pesanan", "#eaf0ff", BLUE)
uc_bayar = oval(12.00, 3.92, 2.80, 0.84, "Bayar pesanan\n(tunai / Midtrans)", "#eaf0ff", BLUE)
uc_lacak = oval(12.00, 2.72, 2.70, 0.78, "Lacak status pesanan", "#eaf0ff", BLUE)

# ---- Admin: dedicated bus x=3.05, stays in the upper band ----
A_BUS = 3.05
H(admin["x"] + 0.28, A_BUS, Y_ADMIN, NAVY)
for uc in (uc_menu, uc_user):
    H(A_BUS, uc["L"][0], uc["L"][1], NAVY)
V(A_BUS, Y_ADMIN, uc_qr["L"][1], NAVY)
H(A_BUS, uc_qr["L"][0], uc_qr["L"][1], NAVY)
H(A_BUS, uc_dash["L"][0], uc_dash["L"][1], NAVY)
V(A_BUS, uc_qr["L"][1], uc_lap["L"][1], NAVY)
H(A_BUS, uc_lap["L"][0], uc_lap["L"][1], NAVY)
# Admin → login: continue down the admin bus only as far as login
V(A_BUS, uc_lap["L"][1], Y_LOGIN, NAVY)
H(A_BUS, uc_login["L"][0], Y_LOGIN, NAVY)

# ---- Koki: HORIZONTAL spine on Y_KOKI only. Never goes below 3.80. ----
K_BUS = 3.35
H(koki["x"] + 0.28, uc_antrean["L"][0], Y_KOKI, GREEN, lw=1.55)
# continue same horizontal through to Update status dapur
H(uc_antrean["R"][0] + 0.02, uc_dapur["L"][0], Y_KOKI, GREEN, lw=1.55)
# Koki → login: short drop from Y_KOKI to Y_LOGIN along K_BUS (stops at 3.80)
H(koki["x"] + 0.28, K_BUS, Y_KOKI, GREEN)
V(K_BUS, Y_KOKI, Y_LOGIN, GREEN)
H(K_BUS, uc_login["L"][0], Y_LOGIN, GREEN)

# ---- Kasir: HORIZONTAL spine on Y_KASIR only. Never goes above 3.80. ----
S_BUS = 2.88
H(kasir["x"] + 0.28, uc_daftar["L"][0], Y_KASIR, ORANGE, lw=1.55)
H(uc_daftar["R"][0] + 0.02, uc_tunai["L"][0], Y_KASIR, ORANGE, lw=1.55)
# down to nota / midtrans
V(S_BUS, Y_KASIR, uc_nota["L"][1], ORANGE)
H(kasir["x"] + 0.28, S_BUS, Y_KASIR, ORANGE)
H(S_BUS, uc_nota["L"][0], uc_nota["L"][1], ORANGE)
H(S_BUS, uc_midtrans["L"][0], uc_midtrans["L"][1], ORANGE)
# Kasir → login: short rise from Y_KASIR to Y_LOGIN along S_BUS (stops at 3.80)
V(S_BUS, Y_KASIR, Y_LOGIN, ORANGE)
H(S_BUS, uc_login["L"][0], Y_LOGIN, ORANGE)

# ---- Pelanggan: right bus ----
P_BUS = 13.72
V(P_BUS, uc_scan["R"][1], uc_lacak["R"][1], BLUE)
H(pelanggan["x"] - 0.28, P_BUS, pelanggan["y"], BLUE)
for uc in (uc_scan, uc_addon, uc_cart, uc_check, uc_bayar, uc_lacak):
    H(uc["R"][0], P_BUS, uc["R"][1], BLUE)

# Color key
ax.add_patch(
    FancyBboxPatch(
        (0.22, 0.16),
        2.36,
        1.28,
        boxstyle="round,pad=0.03,rounding_size=0.05",
        facecolor="#fafafa",
        edgecolor="#d4d4d8",
        lw=0.8,
        zorder=3,
    )
)
ax.text(1.40, 1.22, "Keterangan", ha="center", fontsize=7.1, fontweight="bold", color="#3f3f46")
ax.text(
    1.40,
    0.68,
    "Hijau  : Koki (dapur)\nOranye : Kasir (pembayaran)",
    ha="center",
    fontsize=6.6,
    color="#3f3f46",
    linespacing=1.4,
)

fig.tight_layout(pad=0.10)
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print("wrote", OUT)
