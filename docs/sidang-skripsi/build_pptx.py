#!/usr/bin/env python3
"""Bangun presentasi sidang skripsi dari proposal Kekupu Villa Jembrana."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "Presentasi-Sidang-Skripsi-Kekupu-Villa.pptx"

W, H = 13.333, 7.5

MAROON = RGBColor(0x7A, 0x1F, 0x1A)
ORANGE = RGBColor(0xE0, 0x7A, 0x28)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
CREAM = RGBColor(0xFF, 0xF8, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x2A, 0x1B, 0x14)
MUTED = RGBColor(0x6E, 0x56, 0x48)
SOFT = RGBColor(0xF4, 0xE6, 0xD4)
TEAL = RGBColor(0x1F, 0x6B, 0x4E)
NAVY = RGBColor(0x1E, 0x2C, 0x4A)
RED = RGBColor(0xB4, 0x23, 0x18)
LINE = RGBColor(0xE8, 0xD5, 0xC0)

FONT = "Calibri"


def set_run(run, size=16, bold=False, color=INK, font=FONT, italic=False):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = OxmlElement("a:ea")
        rPr.append(ea)
    ea.set("typeface", font)


def set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def set_line(shape, color, pt=1):
    shape.line.color.rgb = color
    shape.line.width = Pt(pt)


def add_rect(slide, l, t, w, h, color, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    set_fill(s, color)
    if line:
        set_line(s, line, 1)
    else:
        s.line.fill.background()
    return s


def add_round(slide, l, t, w, h, color, line=None, radius=0.08):
    s = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h)
    )
    set_fill(s, color)
    if line:
        set_line(s, line, 1)
    else:
        s.line.fill.background()
    try:
        s.adjustments[0] = radius
    except Exception:
        pass
    return s


def add_text(slide, l, t, w, h, text, size=16, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color, italic=italic)
    return box


def add_paras(slide, l, t, w, h, items, size=14, color=INK, bold=False, spacing=8):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(spacing)
        run = p.add_run()
        run.text = item
        set_run(run, size=size, bold=bold, color=color)
    return box


def add_bullets(slide, l, t, w, h, items, size=15, color=INK, spacing=7):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(spacing)
        p.level = 0
        run = p.add_run()
        run.text = "•  " + item
        set_run(run, size=size, color=color)
    return box


def footer(slide, n, total, label="Sidang Proposal Skripsi  •  UNHI 2026"):
    add_rect(slide, 0, 7.28, W, 0.22, MAROON)
    add_text(slide, 0.4, 7.28, 10, 0.22, label, size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_text(
        slide,
        11.2,
        7.28,
        1.8,
        0.22,
        f"{n} / {total}",
        size=10,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.RIGHT,
        anchor=MSO_ANCHOR.MIDDLE,
    )


def header(slide, section, title, n, total):
    add_rect(slide, 0, 0, W, 0.08, ORANGE)
    add_rect(slide, 0, 0.08, W, 0.92, MAROON)
    logo = ASSETS / "logo-unhi.png"
    if logo.exists():
        slide.shapes.add_picture(str(logo), Inches(0.28), Inches(0.18), Inches(0.68), Inches(0.68))
    add_text(slide, 1.1, 0.14, 10.4, 0.28, section.upper(), size=11, bold=True, color=GOLD)
    add_text(slide, 1.1, 0.38, 10.8, 0.52, title, size=24, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(slide, 0, 1.0, W, 6.28, CREAM)
    footer(slide, n, total)


def card(slide, l, t, w, h, title, body, accent=ORANGE, title_size=14, body_size=12):
    add_round(slide, l, t, w, h, WHITE, LINE, 0.06)
    add_rect(slide, l, t, 0.08, h, accent)
    add_text(slide, l + 0.22, t + 0.1, w - 0.34, 0.36, title, size=title_size, bold=True, color=MAROON)
    if isinstance(body, list):
        add_bullets(slide, l + 0.18, t + 0.46, w - 0.32, h - 0.58, body, size=body_size, color=INK, spacing=5)
    else:
        add_text(slide, l + 0.22, t + 0.46, w - 0.34, h - 0.58, body, size=body_size, color=INK)


def kpi(slide, l, t, w, h, value, caption, accent=ORANGE):
    add_round(slide, l, t, w, h, WHITE, LINE, 0.08)
    add_rect(slide, l, t, w, 0.08, accent)
    add_text(slide, l + 0.1, t + 0.22, w - 0.2, 0.5, value, size=22, bold=True, color=MAROON, align=PP_ALIGN.CENTER)
    add_text(slide, l + 0.1, t + 0.72, w - 0.2, 0.55, caption, size=11, color=MUTED, align=PP_ALIGN.CENTER)


def style_table(table, header_fill=MAROON, alt=SOFT):
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            solid = OxmlElement("a:solidFill")
            srgb = OxmlElement("a:srgbClr")
            if i == 0:
                srgb.set("val", "7A1F1A")
            elif i % 2 == 0:
                srgb.set("val", "F4E6D4")
            else:
                srgb.set("val", "FFFFFF")
            solid.append(srgb)
            existing = tcPr.find(qn("a:solidFill"))
            if existing is not None:
                tcPr.remove(existing)
            tcPr.append(solid)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT
                for run in p.runs:
                    set_run(run, size=11 if i else 11, bold=i == 0, color=WHITE if i == 0 else INK)
            cell.text_frame.word_wrap = True
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def add_table(slide, l, t, w, h, headers, rows):
    shape = slide.shapes.add_table(1 + len(rows), len(headers), Inches(l), Inches(t), Inches(w), Inches(h))
    table = shape.table
    for i, head in enumerate(headers):
        table.cell(0, i).text = head
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            table.cell(r, c).text = val
    style_table(table)
    return table


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def build():
    prs = new_prs()
    TOTAL = 27

    # 1 Cover
    s = blank(prs)
    add_rect(s, 0, 0, W, H, MAROON)
    add_rect(s, 0, 0, 0.22, H, GOLD)
    add_rect(s, 0, 6.95, W, 0.55, RGBColor(0x5C, 0x16, 0x12))
    if (ASSETS / "logo-unhi.png").exists():
        s.shapes.add_picture(str(ASSETS / "logo-unhi.png"), Inches(6.16), Inches(0.28), Inches(1.02), Inches(1.02))
    add_text(s, 0.7, 1.38, 12, 0.28, "SIDANG PROPOSAL SKRIPSI", size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_text(
        s,
        0.8,
        1.72,
        11.7,
        1.7,
        "Pengembangan Sistem Pemesanan Menu\nBerbasis Web dan QR Code\nMenggunakan Framework Laravel 12",
        size=28,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        0.8,
        3.5,
        11.7,
        0.4,
        "Studi Kasus: Restoran Kekupu Villa Jembrana",
        size=18,
        color=RGBColor(0xF5, 0xD7, 0xB0),
        align=PP_ALIGN.CENTER,
    )
    add_rect(s, 5.55, 4.02, 2.2, 0.05, GOLD)
    add_text(s, 0.8, 4.28, 11.7, 0.36, "Ida Bagus Gede Rama Tommy Saputera", size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, 0.8, 4.64, 11.7, 0.3, "NIM  22.03.02.0065", size=14, color=GOLD, align=PP_ALIGN.CENTER)
    add_text(
        s,
        0.8,
        5.1,
        11.7,
        0.7,
        "Program Studi Sistem Informasi\nFakultas Teknik, Perencanaan dan Informatika  •  Universitas Hindu Indonesia",
        size=13,
        color=RGBColor(0xF5, 0xD7, 0xB0),
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        0.7,
        7.05,
        12,
        0.32,
        "Pembimbing I: I Putu Mahendra Adi Wardana, S.Pd., M.Kom.     •     Pembimbing II: Ida Ayu Utari Dewi, S.T., M.Si.     •     2026",
        size=11,
        color=RGBColor(0xF5, 0xD7, 0xB0),
        align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    # 2 Agenda
    s = blank(prs)
    header(s, "Pendahuluan", "Alur Presentasi", 2, TOTAL)
    items = [
        ("01", "Latar Belakang & Masalah", "Kondisi lapangan, identifikasi, dan research gap"),
        ("02", "Rumusan, Tujuan & Manfaat", "Enam pertanyaan penelitian dan luaran yang dituju"),
        ("03", "Landasan Teori", "Teknologi, penelitian terdahulu, dan model Waterfall"),
        ("04", "Metode & Perancangan", "Aktor, kebutuhan, Use Case, ERD, dan DFD"),
        ("05", "Pengujian & Jadwal", "Black-Box, UAT, dan tahapan waktu penelitian"),
    ]
    for i, (num, title, desc) in enumerate(items):
        y = 1.28 + i * 1.12
        add_round(s, 0.45, y, 12.4, 1.0, WHITE, LINE, 0.08)
        add_round(s, 0.62, y + 0.2, 0.62, 0.6, ORANGE, radius=0.2)
        add_text(s, 0.62, y + 0.2, 0.62, 0.6, num, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, 1.5, y + 0.16, 10.8, 0.38, title, size=18, bold=True, color=MAROON)
        add_text(s, 1.5, y + 0.52, 10.8, 0.34, desc, size=14, color=MUTED)

    # 3 Latar Belakang
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Latar Belakang", 3, TOTAL)
    add_text(
        s,
        0.45,
        1.2,
        12.4,
        0.7,
        "Industri jasa boga menuntut kecepatan dan akurasi pelayanan. Restoran Kekupu Villa Jembrana masih mencatat pesanan secara manual dengan nota kertas, tanpa integrasi digital antara meja, dapur, dan kasir.",
        size=15,
        color=INK,
    )
    points = [
        ("Manual & verbal", "Pemesanan dicatat pramusaji, diantar fisik ke dapur, lalu dibayar di kasir."),
        ("Tanpa data terukur", "Pemilik sulit mengambil keputusan karena tidak ada pencatatan transaksi real-time."),
        ("POS komersial kurang pas", "Biaya langganan tinggi, fitur generik, dan antarmuka rumit bagi staf."),
        ("Solusi terpadu", "QR Code meja + Laravel 12 + Midtrans Snap + antrean dapur dalam satu sistem."),
    ]
    for i, (t, d) in enumerate(points):
        x = 0.45 + (i % 2) * 6.4
        y = 2.05 + (i // 2) * 2.35
        card(s, x, y, 6.15, 2.15, t, d, accent=ORANGE if i < 3 else TEAL, title_size=16, body_size=14)

    # 4 Temuan lapangan
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Temuan Observasi & Wawancara  •  4 Januari 2026", 4, TOTAL)
    kpis = [
        ("12 meja", "Kapasitas fisik\n(dihitung langsung)", ORANGE),
        ("10–20 trx/hari", "Volume transaksi\n(estimasi pemilik)", GOLD),
        ("25–45 menit", "Waktu tunggu\njam sibuk", RED),
        ("3–5 kali/hari", "Kesalahan catat\nmenu", RED),
        ("2–4 item/hari", "Menu habis tetap\nditawarkan", NAVY),
    ]
    for i, (v, c, a) in enumerate(kpis):
        kpi(s, 0.4 + i * 2.56, 1.25, 2.42, 1.45, v, c, a)
    add_text(
        s,
        0.45,
        2.88,
        12.4,
        0.4,
        "Angka volume, waktu tunggu, dan kesalahan bersumber dari wawancara Bapak Bagus Suteja (pemilik) — indikasi awal, bukan pengukuran stopwatch.",
        size=13,
        italic=True,
        color=MUTED,
    )
    card(
        s,
        0.4,
        3.38,
        12.5,
        3.55,
        "Akar permasalahan yang menjadi urgensi penelitian",
        [
            "12 meja dine-in masih dilayani dengan nota kertas; tidak ada sistem digital terintegrasi.",
            "Komunikasi verbal memperlambat siklus meja–dapur–kasir dan memicu human error.",
            "Ketersediaan menu tidak tercatat digital, sehingga item habis baru diketahui setelah dipesan.",
            "Pembayaran tunai/manual memicu antrean kasir dan rekap bulanan dari tumpukan nota.",
            "Ketiadaan basis data andal membuat pemilik sulit memantau kinerja operasional secara real-time.",
        ],
        accent=MAROON,
        title_size=16,
        body_size=14,
    )

    # 5 Identifikasi masalah
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Identifikasi Masalah", 5, TOTAL)
    card(
        s,
        0.4,
        1.25,
        6.2,
        5.7,
        "Aspek Operasional & Pelayanan",
        [
            "Efisiensi rendah: waktu tunggu jam padat 25–45 menit.",
            "Human error: salah catat menu 3–5 kali per hari.",
            "Koordinasi FOH–BOH terhambat nota kertas dan jarak area.",
            "Ketersediaan menu tidak transparan bagi pelanggan.",
            "Pembayaran kasir lambat dan rekapitulasi rentan selisih.",
        ],
        accent=RED,
        title_size=16,
        body_size=15,
    )
    card(
        s,
        6.8,
        1.25,
        6.1,
        5.7,
        "Aspek Teknis & Pengembangan",
        [
            "POS komersial mahal, generik, dan UI-nya rumit.",
            "Sistem sejenis belum mengintegrasikan pembayaran otomatis.",
            "Diperlukan arsitektur web Laravel 12 yang aman dan maintainable.",
            "Belum ada pengujian terukur (Black-Box + UAT) sebelum implementasi.",
        ],
        accent=NAVY,
        title_size=16,
        body_size=15,
    )

    # 6 Research gap
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Research Gap", 6, TOTAL)
    add_text(
        s,
        0.45,
        1.2,
        12.4,
        0.55,
        "Penelitian terdahulu sudah membahas QR Code, POS, atau payment gateway secara terpisah. Belum ada sistem terpadu yang memadukan keempatnya pada studi kasus UMKM restoran.",
        size=15,
        color=INK,
    )
    gaps = [
        ("QR + KDS", "Irzan & Yuliadi (2026)", "Belum merinci framework dan belum ada payment gateway."),
        ("QR + CodeIgniter", "Milenia dkk. (2024)", "Framework lama; pembayaran masih konvensional di kasir."),
        ("Mobile + Midtrans", "Benny dkk. (2022)", "Wajib unduh aplikasi Android; tanpa QR meja."),
        ("QR + CI4", "Makarim dkk. (2025)", "Tanpa modul dapur dan tanpa pengelolaan stok menu."),
    ]
    for i, (tag, src, gap) in enumerate(gaps):
        x = 0.4 + (i % 2) * 6.45
        y = 1.9 + (i // 2) * 2.4
        add_round(s, x, y, 6.25, 2.2, WHITE, LINE, 0.07)
        add_round(s, x + 0.2, y + 0.2, 2.3, 0.38, SOFT, radius=0.15)
        add_text(s, x + 0.2, y + 0.2, 2.3, 0.38, tag, size=12, bold=True, color=MAROON, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, x + 0.22, y + 0.7, 5.85, 0.35, src, size=14, bold=True, color=INK)
        add_text(s, x + 0.22, y + 1.1, 5.85, 0.85, gap, size=14, color=MUTED)

    # 7 Batasan
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Pembatasan Masalah", 7, TOTAL)
    ins = [
        "4 aktor: Pelanggan, Koki, Kasir, Admin/Owner.",
        "Pelanggan tanpa akun; akses lewat sesi/token QR meja.",
        "Stok yang dikelola = ketersediaan menu & add-on.",
        "Bayar tunai (kasir) dan non-tunai (Midtrans Snap + webhook).",
        "Status bayar terpisah dari status dapur.",
        "Web responsif: PHP 8.1, Laravel 12, MySQL.",
        "Metode Waterfall; uji Black-Box + UAT.",
    ]
    outs = [
        "Inventori bahan baku dapur.",
        "Pembelian ke pemasok (supplier).",
        "Penggajian karyawan (payroll).",
        "Reservasi meja.",
        "Manajemen logistik barang.",
        "Aktor pramusaji (diganti self-ordering).",
        "Refund/recurring Midtrans.",
    ]
    card(s, 0.4, 1.25, 6.3, 5.7, "Termasuk dalam sistem", ins, accent=TEAL, title_size=17, body_size=14)
    card(s, 6.9, 1.25, 6.0, 5.7, "Di luar lingkup", outs, accent=RED, title_size=17, body_size=14)

    # 8 Rumusan
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Rumusan Masalah", 8, TOTAL)
    rumus = [
        "Bagaimana merancang sistem pemesanan web + QR Code (Laravel 12) agar pelanggan memesan mandiri tanpa registrasi?",
        "Bagaimana mengelola menu, kategori, add-on, dan stok agar katalog hanya menampilkan item yang tersedia?",
        "Bagaimana mengintegrasikan pesanan lunas ke antrean dapur tanpa pencatatan ulang?",
        "Bagaimana mengelola bayar tunai (kasir) dan non-tunai (Midtrans webhook) terpisah dari status dapur?",
        "Bagaimana membagi hak akses Admin, Koki, Kasir, dan Pelanggan sesuai wewenang?",
        "Bagaimana hasil pengujian Black-Box Testing dan User Acceptance Testing (UAT)?",
    ]
    for i, t in enumerate(rumus):
        y = 1.2 + i * 0.95
        add_round(s, 0.4, y, 12.5, 0.86, WHITE, LINE, 0.08)
        add_round(s, 0.55, y + 0.18, 0.52, 0.5, ORANGE, radius=0.18)
        add_text(s, 0.55, y + 0.18, 0.52, 0.5, str(i + 1), size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, 1.3, y + 0.16, 11.35, 0.56, t, size=15, color=INK, anchor=MSO_ANCHOR.MIDDLE)

    # 9 Tujuan
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Tujuan Penelitian", 9, TOTAL)
    goals = [
        ("01", "Membangun sistem", "Sistem pemesanan menu web + QR Code dengan Laravel 12 di Kekupu Villa."),
        ("02", "Self-ordering", "Pelanggan memesan dari meja lewat sesi QR, tanpa wajib buat akun."),
        ("03", "Data master", "Admin kelola menu, kategori, add-on, dan ketersediaan/stok."),
        ("04", "Antrean dapur", "Koki menerima pesanan lunas dan memutakhirkan kitchen_status."),
        ("05", "Dua kanal bayar", "Tunai dikonfirmasi Kasir; non-tunai diverifikasi webhook Midtrans."),
        ("06", "Transparansi status", "Pembayaran dan progres dapur dipantau sesuai wewenang masing-masing."),
        ("07", "Pengujian terukur", "Black-Box Testing dan UAT untuk kelayakan sebelum implementasi penuh."),
    ]
    for i, (n, t, d) in enumerate(goals):
        x = 0.4 + (i % 2) * 6.45
        y = 1.22 + (i // 2) * 1.45
        if i == 6:
            x = 0.4
            w = 12.5
        else:
            w = 6.25
        add_round(s, x, y, w, 1.32, WHITE, LINE, 0.07)
        add_text(s, x + 0.2, y + 0.12, 1.0, 0.3, n, size=13, bold=True, color=ORANGE)
        add_text(s, x + 1.1, y + 0.12, w - 1.35, 0.3, t, size=15, bold=True, color=MAROON)
        add_text(s, x + 0.2, y + 0.5, w - 0.4, 0.7, d, size=13, color=INK)

    # 10 Manfaat
    s = blank(prs)
    header(s, "BAB I  •  Pendahuluan", "Manfaat Penelitian", 10, TOTAL)
    benefits = [
        ("Pelanggan", "Pesan mandiri dari meja, lihat ketersediaan, pilih add-on, bayar tunai/QRIS, lacak status.", TEAL),
        ("Koki", "Antrean pesanan lunas masuk ke layar dapur: meja, item, add-on, catatan — tanpa nota kertas.", ORANGE),
        ("Kasir", "Konfirmasi tunai, pantau settlement Midtrans, cetak nota, unduh rekap bulanan.", GOLD),
        ("Admin/Owner", "Kelola master data, QR 12 meja, riwayat pesanan, dan laporan sebagai dasar keputusan.", NAVY),
        ("Akademik", "Studi kasus Waterfall + Laravel 12 + Midtrans; dokumentasi Use Case, ERD, dan DFD.", MAROON),
        ("UNHI", "Hilirisasi teknologi untuk industri kuliner lokal, wujud Tri Dharma Perguruan Tinggi.", RGBColor(0x6B, 0x3F, 0x2A)),
    ]
    for i, (t, d, a) in enumerate(benefits):
        x = 0.4 + (i % 3) * 4.25
        y = 1.25 + (i // 3) * 2.85
        card(s, x, y, 4.1, 2.65, t, d, accent=a, title_size=16, body_size=13)

    # 11 Teori
    s = blank(prs)
    header(s, "BAB II  •  Landasan Teori", "Landasan Teori & Stack Teknologi", 11, TOTAL)
    techs = [
        ("Laravel 12", "Framework PHP MVC: keamanan, Artisan, dan integrasi API Midtrans."),
        ("PHP 8.1", "Bahasa server untuk logika bisnis, sesi meja, dan webhook."),
        ("MySQL", "9 tabel: roles, users, categories, items, add-on, orders, order_items."),
        ("QR Code", "Akses frictionless ke /meja/{n}; nomor meja otomatis tanpa unduh aplikasi."),
        ("Midtrans Snap", "QRIS, e-wallet, transfer; settlement ditulis lewat webhook + signature SHA-512."),
        ("UML & DFD", "Use Case, ERD, DFD Gane & Sarson, plus Black-Box dan UAT."),
    ]
    for i, (t, d) in enumerate(techs):
        x = 0.4 + (i % 3) * 4.25
        y = 1.25 + (i // 3) * 2.85
        card(s, x, y, 4.1, 2.65, t, d, accent=ORANGE if i % 2 == 0 else GOLD, title_size=16, body_size=14)

    # 12 Penelitian terdahulu
    s = blank(prs)
    header(s, "BAB II  •  Landasan Teori", "Penelitian Terdahulu — Posisi Penelitian Ini", 12, TOTAL)
    add_table(
        s,
        0.35,
        1.22,
        12.6,
        4.55,
        ["Penelitian", "Pendekatan", "Kekurangan", "Pembedaan penelitian ini"],
        [
            ["Irzan & Yuliadi (2026)", "QR + KDS, Waterfall", "Framework tidak rinci; tanpa PG", "Laravel 12 + Midtrans Snap"],
            ["Milenia dkk. (2024)", "QR + CodeIgniter", "Bayar masih di kasir", "Dua kanal: tunai & webhook"],
            ["Benny dkk. (2022)", "Android + Midtrans", "Wajib instal aplikasi", "Web + QR meja, tanpa unduh app"],
            ["Makarim dkk. (2025)", "QR + CI4", "Tanpa dapur & stok menu", "KDS + stok menu/add-on"],
            ["Hikmah dkk. (2023)", "QR + Waterfall", "Tanpa payment gateway", "Snap + pemisahan status bayar/dapur"],
        ],
    )
    add_round(s, 0.35, 5.95, 12.6, 1.05, WHITE, ORANGE, 0.06)
    add_text(
        s,
        0.55,
        6.1,
        12.2,
        0.75,
        "Kontribusi: satu sistem terpadu — QR meja, stok menu/add-on, antrean dapur real-time, Midtrans webhook, dan dashboard laporan — untuk UMKM restoran.",
        size=14,
        bold=True,
        color=MAROON,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    # 13 Waterfall
    s = blank(prs)
    header(s, "BAB III  •  Metode Penelitian", "Metode Pengembangan: Waterfall", 13, TOTAL)
    if (ASSETS / "waterfall.png").exists():
        s.shapes.add_picture(str(ASSETS / "waterfall.png"), Inches(0.4), Inches(1.25), Inches(5.6), Inches(3.55))
    steps = [
        ("1  Requirement", "Observasi, wawancara, studi pustaka → spesifikasi KF & KNF."),
        ("2  Design", "Use Case, ERD, DFD, dan rancangan UI per peran."),
        ("3  Implementation", "PHP 8.1, Laravel 12, Bootstrap, MySQL."),
        ("4  Testing", "34 skenario Black-Box + UAT 18 responden."),
        ("5  Maintenance", "Deployment (Niagahoster) dan perbaikan pasca-rilis."),
    ]
    for i, (t, d) in enumerate(steps):
        y = 1.22 + i * 1.1
        add_round(s, 6.25, y, 6.65, 1.0, WHITE, LINE, 0.07)
        add_text(s, 6.45, y + 0.1, 6.25, 0.32, t, size=15, bold=True, color=MAROON)
        add_text(s, 6.45, y + 0.46, 6.25, 0.42, d, size=13, color=INK)

    # 14 Kerangka
    s = blank(prs)
    header(s, "BAB III  •  Metode Penelitian", "Kerangka Penelitian (Input → Process → Output)", 14, TOTAL)
    if (ASSETS / "kerangka.png").exists():
        s.shapes.add_picture(str(ASSETS / "kerangka.png"), Inches(0.55), Inches(1.18), Inches(12.2), Inches(5.9))

    # 15 Pengumpulan data
    s = blank(prs)
    header(s, "BAB III  •  Metode Penelitian", "Pengumpulan Data & Responden", 15, TOTAL)
    card(
        s,
        0.4,
        1.22,
        4.1,
        5.75,
        "Observasi  •  4 Jan 2026",
        [
            "12 meja pelanggan.",
            "Nota kertas, tanpa sistem digital.",
            "Alur fisik meja–dapur–kasir.",
            "Media bayar di titik kasir.",
            "Volume & waktu tunggu tidak diukur stopwatch pada hari observasi.",
        ],
        accent=ORANGE,
        title_size=15,
        body_size=13,
    )
    card(
        s,
        4.65,
        1.22,
        4.1,
        5.75,
        "Wawancara  •  6 informan",
        [
            "1 pemilik (Bagus Suteja).",
            "2 koki, 2 pramusaji, 1 kasir.",
            "Alur kerja & kendala rush hour.",
            "Pengelolaan ketersediaan menu.",
            "Kebutuhan fitur & pembagian role.",
        ],
        accent=GOLD,
        title_size=15,
        body_size=13,
    )
    card(
        s,
        8.9,
        1.22,
        4.0,
        5.75,
        "UAT kelak  •  18 orang",
        [
            "1 owner (peran Admin).",
            "2 koki + 1 kasir.",
            "2 pramusaji: butir inti saja.",
            "12 pelanggan (satu per meja).",
            "Skala Likert 1–5; skor ideal 1.525.",
        ],
        accent=TEAL,
        title_size=15,
        body_size=13,
    )

    # 16 Aktor
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Empat Aktor Sistem", 16, TOTAL)
    actors = [
        ("Pelanggan", "Tanpa login", "Scan QR meja, lihat menu & stok, pilih add-on, keranjang, checkout, bayar, lacak status.", TEAL),
        ("Koki", "Login role chef", "Lihat antrean pesanan lunas, rincian item/add-on/catatan, update kitchen_status.", ORANGE),
        ("Kasir", "Login role cashier", "Pantau pending, konfirmasi tunai saja, pantau Midtrans, cetak nota, laporan.", GOLD),
        ("Admin", "Login role admin", "CRUD menu/kategori/add-on/stok, karyawan & role, QR 12 meja, riwayat & laporan.", NAVY),
    ]
    for i, (name, tag, desc, a) in enumerate(actors):
        x = 0.4 + i * 3.2
        add_round(s, x, 1.3, 3.05, 5.6, WHITE, LINE, 0.07)
        add_rect(s, x, 1.3, 3.05, 1.15, a)
        add_text(s, x + 0.12, 1.4, 2.8, 0.5, name, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, x + 0.12, 1.9, 2.8, 0.4, tag, size=12, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, x + 0.18, 2.65, 2.7, 3.9, desc, size=14, color=INK)

    # 17 KF
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Kebutuhan Fungsional per Aktor", 17, TOTAL)
    add_table(
        s,
        0.35,
        1.22,
        12.6,
        5.7,
        ["Aktor", "Kode", "Contoh kemampuan inti"],
        [
            ["Pelanggan", "KF-P01–P12", "Scan QR, katalog, stok, add-on, keranjang, checkout, tunai/QRIS, lacak status"],
            ["Admin", "KF-A01–A10", "Login, CRUD menu/kategori/add-on/stok, karyawan, role, laporan, QR meja"],
            ["Koki", "KF-K01–K07", "Login, antrean lunas, meja/item/add-on/catatan, update status, indikator baru"],
            ["Kasir", "KF-S01–S07", "Login, daftar pending, konfirmasi tunai, pantau Midtrans, nota, laporan"],
            ["Sistem/Midtrans", "KF-M01–M06", "Snap token, webhook, verifikasi SHA-512, settlement, terus ke dapur, sesi meja"],
        ],
    )

    # 18 Use case
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Use Case Diagram", 18, TOTAL)
    if (ASSETS / "usecase.png").exists():
        s.shapes.add_picture(str(ASSETS / "usecase.png"), Inches(0.28), Inches(1.15), Inches(12.75), Inches(5.95))

    # 19 ERD
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Entity Relationship Diagram — 9 Tabel", 19, TOTAL)
    if (ASSETS / "erd.png").exists():
        s.shapes.add_picture(str(ASSETS / "erd.png"), Inches(0.3), Inches(1.15), Inches(6.3), Inches(5.95))
    notes = [
        ("Tanpa tabel meja", "Identitas meja = orders.table_number dari parameter QR Code."),
        ("Add-on konsisten", "addon_groups + addons + addon_group_item; pilihan tersimpan JSON di order_items.addons."),
        ("Dua status terpisah", "orders.status: pending / settlement.  orders.kitchen_status: waiting / processing / cooking / ready."),
        ("Tidak ada inventori bahan", "Stok hanya item & add-on yang ditawarkan ke pelanggan."),
    ]
    for i, (t, d) in enumerate(notes):
        y = 1.22 + i * 1.4
        card(s, 6.8, y, 6.1, 1.28, t, d, accent=ORANGE if i % 2 == 0 else GOLD, title_size=14, body_size=12)

    # 20 DFD
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Context Diagram (DFD Level 0)", 20, TOTAL)
    if (ASSETS / "dfd-l0.png").exists():
        s.shapes.add_picture(str(ASSETS / "dfd-l0.png"), Inches(2.55), Inches(1.12), Inches(8.2), Inches(5.95))

    # 21 DFD L1
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "DFD Level 1 — Enam Proses Utama", 21, TOTAL)
    if (ASSETS / "dfd-l1.png").exists():
        s.shapes.add_picture(str(ASSETS / "dfd-l1.png"), Inches(2.35), Inches(1.1), Inches(8.6), Inches(5.95))

    # 22 Pembayaran
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Dua Kanal Pembayaran yang Dipisahkan Tegas", 22, TOTAL)
    card(
        s,
        0.4,
        1.22,
        6.2,
        4.55,
        "Non-tunai  •  Midtrans Snap",
        [
            "Pelanggan pilih QRIS / e-wallet / transfer.",
            "Sistem minta snap_token ke Midtrans.",
            "Pelanggan bayar di jendela Snap.",
            "Webhook ke POST /midtrans/notification.",
            "Signature SHA-512 diverifikasi dulu.",
            "settlement/capture → orders.status = settlement.",
            "kitchen_status: waiting → processing.",
            "Kasir hanya memantau; tanpa tombol konfirmasi.",
        ],
        accent=NAVY,
        title_size=16,
        body_size=13,
    )
    card(
        s,
        6.8,
        1.22,
        6.1,
        4.55,
        "Tunai  •  Konfirmasi Kasir",
        [
            "Pelanggan pilih metode tunai saat checkout.",
            "Pesanan tersimpan status pending.",
            "Muncul di daftar Kasir menunggu pelunasan.",
            "Kasir cocokkan grand_total dengan uang fisik.",
            "Tombol Konfirmasi hanya untuk payment_method = tunai.",
            "Sistem menulis settlement + kitchen_status processing.",
            "Pesanan baru tampil di antrean dapur.",
            "Pajak 10% dihitung saat checkout.",
        ],
        accent=ORANGE,
        title_size=16,
        body_size=13,
    )
    add_round(s, 0.4, 5.95, 12.5, 1.05, WHITE, GOLD, 0.06)
    add_text(
        s,
        0.6,
        6.1,
        12.1,
        0.75,
        "Prinsip desain: pelunasan pembayaran tidak pernah disimpulkan dari progres dapur, dan sebaliknya.",
        size=15,
        bold=True,
        color=MAROON,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    # 23 UI
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Rancangan Antarmuka Pelanggan", 23, TOTAL)
    uis = [
        (ASSETS / "ui-menu.png", "Katalog menu digital"),
        (ASSETS / "ui-addon.png", "Kustomisasi add-on"),
        (ASSETS / "ui-cart.png", "Keranjang"),
        (ASSETS / "ui-bayar.png", "Pembayaran"),
    ]
    for i, (path, cap) in enumerate(uis):
        x = 0.35 + i * 3.25
        add_round(s, x, 1.2, 3.1, 5.0, WHITE, LINE, 0.05)
        if path.exists():
            s.shapes.add_picture(str(path), Inches(x + 0.1), Inches(1.32), Inches(2.9), Inches(4.35))
        add_text(s, x, 6.25, 3.1, 0.35, cap, size=13, bold=True, color=MAROON, align=PP_ALIGN.CENTER)

    # 24 UI staf
    s = blank(prs)
    header(s, "BAB III  •  Perancangan", "Rancangan Antarmuka Staf", 24, TOTAL)
    staff_ui = [
        (
            "Admin",
            [
                "Sidebar: menu, kategori, add-on, karyawan, role, pesanan, laporan, QR meja.",
                "Kartu ringkasan: pesanan hari ini, pendapatan, item aktif.",
                "CRUD stok & is_active; unduh rekap bulanan.",
                "Generate QR 12 meja → /meja/{n}.",
            ],
            NAVY,
        ),
        (
            "Koki  •  KDS",
            [
                "Papan antrean kartu: meja, kode, item + add-on, catatan, waktu.",
                "Tombol: Diproses → Dimasak → Siap disajikan.",
                "Hanya pesanan settlement yang tampil.",
                "Indikator visual pesanan baru.",
            ],
            ORANGE,
        ),
        (
            "Kasir",
            [
                "Pisahkan antrean tunai pending vs QRIS Midtrans.",
                "Tombol konfirmasi hanya untuk tunai.",
                "Cetak nota: item, add-on, pajak, total.",
                "Unduh laporan pesanan bulanan.",
            ],
            GOLD,
        ),
    ]
    for i, (t, body, a) in enumerate(staff_ui):
        card(s, 0.4 + i * 4.25, 1.25, 4.1, 5.7, t, body, accent=a, title_size=17, body_size=14)

    # 25 Pengujian
    s = blank(prs)
    header(s, "BAB III  •  Pengujian", "Black-Box Testing  •  34 Skenario", 25, TOTAL)
    add_table(
        s,
        0.35,
        1.2,
        7.4,
        3.4,
        ["Aktor", "Jumlah", "Contoh skenario"],
        [
            ["Pelanggan", "11", "Scan QR, stok, add-on, checkout, Snap, lacak status"],
            ["Admin", "8", "CRUD menu/stok/add-on, karyawan, role, laporan"],
            ["Koki", "4", "Login, antrean lunas, update status, indikator baru"],
            ["Kasir", "5", "Pending, konfirmasi tunai, pantau Midtrans, nota"],
            ["Sistem / Midtrans", "6", "Snap, webhook, SHA-512, sesi meja, validasi"],
        ],
    )
    card(
        s,
        7.95,
        1.2,
        4.95,
        3.4,
        "Kriteria lulus",
        [
            "Valid = hasil aktual = expected.",
            "Invalid = fungsi/data/tampilan menyimpang.",
            "Sistem lulus jika 100% skenario Valid.",
            "Invalid → bugfix lalu regression testing.",
        ],
        accent=TEAL,
        title_size=16,
        body_size=13,
    )
    add_round(s, 0.35, 4.8, 12.6, 2.15, WHITE, LINE, 0.06)
    add_text(s, 0.55, 4.95, 12.2, 0.35, "User Acceptance Testing (UAT)", size=16, bold=True, color=MAROON)
    add_text(
        s,
        0.55,
        5.35,
        12.2,
        1.4,
        "18 responden  •  12 butir inti (usability, fungsi, UI, kinerja, kepuasan) + butir spesifik per peran.\nSkala Likert 1–5  •  skor ideal 1.525  •  layak jika ≥ 61% dan Black-Box 100% Valid.\nContoh: 1.270 / 1.525 = 83,3% → kategori Sangat Layak (81–100%).",
        size=14,
        color=INK,
    )

    # 26 Jadwal + penutup
    s = blank(prs)
    header(s, "BAB III  •  Jadwal", "Tahapan Waktu Penelitian  •  Des 2025 – Jun 2026", 26, TOTAL)
    add_table(
        s,
        0.35,
        1.18,
        12.6,
        3.55,
        ["Kegiatan", "Des", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
        [
            ["Observasi lapangan", "✓", "✓", "", "", "", "", ""],
            ["Wawancara manajemen & staf", "✓", "✓", "", "", "", "", ""],
            ["Analisis kebutuhan", "", "✓", "", "", "", "", ""],
            ["Perancangan (Use Case, ERD, DFD, UI)", "", "", "✓", "✓", "", "", ""],
            ["Implementasi Laravel 12 & PHP 8.1", "", "", "", "✓", "✓", "✓", ""],
            ["Black-Box Testing & UAT", "", "", "", "", "", "✓", "✓"],
            ["Penyusunan laporan akhir", "", "", "", "", "", "✓", "✓"],
        ],
    )
    add_round(s, 0.35, 4.95, 12.6, 2.0, WHITE, ORANGE, 0.06)
    add_text(s, 0.55, 5.1, 12.2, 0.35, "Luaran yang diharapkan", size=15, bold=True, color=MAROON)
    add_text(
        s,
        0.55,
        5.5,
        12.2,
        1.25,
        "Sistem pemesanan mandiri berbasis QR yang akurat mencatat transaksi, mempercepat pelayanan,\nmemisahkan status bayar dan dapur, serta menyediakan laporan bulanan bagi pemilik restoran.",
        size=14,
        color=INK,
    )

    # Closing (extra, beyond numbered 26? Wait I set TOTAL=26 but this would be 27)
    # I'll make this slide 26 was jadwal and add closing as last - need to fix TOTAL.
    # Recalculate: I have slides 1-26 plus I was going to add closing. Let me add closing as slide 27 and update TOTAL.
    # Actually looking at my plan I said TOTAL=26 but I'm adding a thank you. I'll add it and fix TOTAL to 27 by regenerating headers... 
    # Easier: make thank you unnumbered visually as 27 and update TOTAL constant at top after counting.
    # I'll add thank you and set TOTAL to 27. But all previous footers already used TOTAL=26.
    # I need to set TOTAL correctly from the start. Let me count:
    # 1 cover, 2 agenda, 3 latar, 4 temuan, 5 identifikasi, 6 gap, 7 batasan, 8 rumusan, 9 tujuan, 10 manfaat,
    # 11 teori, 12 terdahulu, 13 waterfall, 14 kerangka, 15 data, 16 aktor, 17 KF, 18 usecase, 19 erd,
    # 20 dfd0, 21 dfd1, 22 bayar, 23 ui, 24 staf, 25 uji, 26 jadwal, 27 thanks
    # That's 27. I used TOTAL=26. I should fix this by setting TOTAL=27 at the top.
    
    s = blank(prs)
    add_rect(s, 0, 0, W, H, MAROON)
    add_rect(s, 0, 0, 0.22, H, GOLD)
    if (ASSETS / "logo-unhi.png").exists():
        s.shapes.add_picture(str(ASSETS / "logo-unhi.png"), Inches(6.16), Inches(1.15), Inches(1.02), Inches(1.02))
    add_text(s, 0.7, 2.4, 12, 0.7, "Terima Kasih", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, 5.7, 3.2, 1.9, 0.06, GOLD)
    add_text(
        s,
        1.2,
        3.5,
        10.9,
        0.9,
        "Kritik dan saran dari Bapak/Ibu penguji sangat diharapkan\nuntuk penyempurnaan penelitian ini.",
        size=16,
        color=RGBColor(0xF5, 0xD7, 0xB0),
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        1.2,
        4.6,
        10.9,
        1.1,
        "Ida Bagus Gede Rama Tommy Saputera  •  22.03.02.0065\nSistem Informasi  •  Universitas Hindu Indonesia",
        size=15,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        1.2,
        6.3,
        10.9,
        0.5,
        "Om Śāntiḥ Śāntiḥ Śāntiḥ",
        size=16,
        italic=True,
        color=GOLD,
        align=PP_ALIGN.CENTER,
    )

    prs.save(OUT)
    print(f"Saved {OUT} with {len(prs.slides)} slides")


if __name__ == "__main__":
    build()
