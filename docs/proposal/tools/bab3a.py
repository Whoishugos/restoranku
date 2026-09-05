"""BAB III bagian awal: objek penelitian, kerangka, pengumpulan data, kebutuhan fungsional."""

FR_WIDTHS = [1150, 2800, 5260]


def _block(D, anchor_text, intro, caption, template_tbl, widths, rows,
           tmpl_body, tmpl_caption):
    """Insert intro paragraph + table + caption after an anchor; returns new anchor text."""
    anchor = D.find_para(anchor_text)
    D.insert_paras_after(anchor, [(tmpl_body, intro), (tmpl_caption, caption)])
    intro_idx = D.find_para(intro[:60])
    D.insert_table_after_para(intro_idx, template_tbl, widths, rows,
                              label=f"table for {caption}")
    return caption


def apply(D, TBL):
    A = D.find_para

    # ------------------------------------------------------- 3.2 Objek Penelitian
    i = A("Sebagai solusi atas permasalahan tersebut, dilakukan pengembangan Sistem")
    D.sub(
        i,
        "mempercepat respons pelayanan di Restoran Kekupu Villa Jembrana.",
        "mempercepat respons pelayanan di Restoran Kekupu Villa Jembrana. Objek "
        "penelitian dibatasi pada proses pemesanan menu dan pelayanan pelanggan beserta "
        "koordinasinya dengan dapur dan kasir; penelitian ini tidak memperluas objek "
        "menjadi sistem inventori bahan baku dapur karena modul tersebut tidak dibangun.",
    )

    # ----------------------------------------------------- 3.3 Kerangka Penelitian
    i = A("Permasalahan Manajemen: Fragmentasi komunikasi antara bagian pelayanan")
    D.set_text(
        i,
        "Permasalahan Manajemen: Fragmentasi komunikasi antara bagian pelayanan (front "
        "of house) dengan pihak dapur (back of house), serta belum adanya pencatatan "
        "digital atas ketersediaan/stok menu sehingga menu yang telah habis masih "
        "ditawarkan kepada pelanggan dan rekapitulasi penjualan bulanan harus disusun "
        "secara manual dari tumpukan nota kertas.",
    )

    anchor = A("Kebutuhan Sistem: Perlunya otomatisasi dan digitalisasi sistem pemesanan")
    tmpl_body = A("Kerangka penelitian merupakan visualisasi logis dan konseptual")
    D.insert_paras_after(
        anchor,
        [
            (
                tmpl_body,
                "Data yang menjadi masukan sistem meliputi data menu (items), data "
                "kategori (categories), data meja beserta QR Code-nya (parameter "
                "table_number), data pengguna dan role (users dan roles), data add-on "
                "(addon_groups dan addons), data pesanan (orders dan order_items), serta "
                "data pembayaran (payment_method dan status pembayaran).",
            )
        ],
    )

    anchor = A("Pemeliharaan (Maintenance): Melakukan proses deployment (hosting)")
    D.insert_paras_after(
        anchor,
        [
            (
                tmpl_body,
                "Proses utama yang dijalankan sistem meliputi pemindaian QR Code meja, "
                "penampilan katalog menu digital, pemilihan menu, pemilihan add-on, "
                "pengelolaan keranjang, checkout, pembayaran tunai maupun non-tunai, "
                "penerimaan webhook Midtrans, penerusan pesanan yang telah lunas ke "
                "antrean dapur, serta pemutakhiran status dapur.",
            )
        ],
    )

    i = A("Dampak Operasional: Mereduksi turnaround time pelayanan")
    D.set_text(
        i,
        "Dampak Operasional: Mereduksi turnaround time pelayanan, meminimalisir potensi "
        "human error pada pencatatan pesanan, menghadirkan transparansi ketersediaan/stok "
        "menu dan add-on secara real-time, serta meningkatkan produktivitas dan kualitas "
        "pengalaman bersantap pelanggan (customer experience).",
    )

    anchor = A("Dampak Operasional: Mereduksi turnaround time pelayanan")
    D.insert_paras_after(
        anchor,
        [
            (
                tmpl_body,
                "Luaran data dan dokumen yang dihasilkan sistem meliputi pesanan yang "
                "tercatat secara digital, pembayaran yang terverifikasi, antrean dapur, "
                "status pesanan yang dapat dipantau pelanggan, nota transaksi, serta "
                "riwayat pesanan dan laporan rekapitulasi pesanan bulanan.",
            )
        ],
    )

    # -------------------------------------------------- 3.4 Metode Pengumpulan Data
    i = A("Data volume transaksi, waktu tunggu, frekuensi kesalahan")
    D.set_text(
        i,
        "Data volume transaksi, waktu tunggu, frekuensi kesalahan pencatatan, serta "
        "praktik pengelolaan ketersediaan menu tidak dicantumkan pada subbab observasi "
        "karena tidak diukur menggunakan stopwatch maupun sampling transaksi pada hari "
        "observasi.",
    )

    i = A("Staf Operasional Restoran: 5 orang (terdiri dari 2 orang Koki/Staf Dapur")
    D.set_text(
        i,
        "Staf Operasional Restoran: 5 orang (terdiri dari 2 orang Koki/Staf Dapur, 2 "
        "orang Pramusaji, dan 1 orang Kasir). Pramusaji dilibatkan sebagai informan "
        "proses pelayanan dan responden umum, bukan sebagai pengguna sistem, karena "
        "aktor sistem dibatasi pada Pelanggan, Koki, Kasir, dan Admin.",
    )

    i = A("Kriteria Pemilik (Owner): Pengelola utama yang memiliki wewenang manajerial")
    D.set_text(
        i,
        "Kriteria Pemilik (Owner): Pengelola utama yang memiliki wewenang manajerial "
        "penuh, memahami alur transaksi harian, rekapitulasi penjualan bulanan, serta "
        "kendala pengelolaan ketersediaan/stok menu yang ditawarkan kepada pelanggan.",
    )

    i = A("Estimasi kualitatif yang bersumber dari informan")
    D.set_text(
        i,
        "Estimasi kualitatif yang bersumber dari informan: rata-rata 10–20 transaksi per "
        "hari; waktu tunggu jam sibuk 25–45 menit; kesalahan pencatatan 3–5 kali per "
        "hari; serta rata-rata 2–4 item menu per hari yang telah habis namun masih "
        "ditawarkan kepada pelanggan karena ketersediaannya tidak tercatat secara "
        "digital. Keenam informan yang sama kelak menjadi bagian responden UAT, tetapi "
        "fungsi mereka pada tahap pengumpulan data adalah pemberi keterangan kebutuhan "
        "sistem, bukan pengisi kuesioner.",
    )

    i = A("Sesi 2: Manajemen Stok & Laporan Keuangan")
    D.set_text(i, "Sesi 2: Pengelolaan Ketersediaan Menu & Rekapitulasi Penjualan")

    i = A("Bagaimana penanganan selisih (discrepancy) antara data stok bahan baku riil")
    D.set_text(
        i,
        "Bagaimana proses pengelolaan ketersediaan/stok menu yang ditampilkan kepada "
        "pelanggan saat ini, termasuk penanganannya ketika suatu menu atau opsi tambahan "
        "(add-on) habis pada tengah jam operasional?",
    )

    i = A("Bagaimana pembagian hak akses (user role) yang diinginkan antara Admin")
    D.set_text(
        i,
        "Bagaimana pembagian hak akses (user role) yang diinginkan antara Admin, Koki, "
        "dan Kasir, serta sejauh mana pelanggan diperbolehkan mengakses sistem tanpa "
        "akun?",
    )

    i = A("Selisih Stok & Keuangan (Discrepancy): Ditemukan selisih antara ketersediaan")
    D.set_text(
        i,
        "Pengelolaan Ketersediaan Menu: Ketersediaan menu tidak tercatat secara digital. "
        "Menu yang habis hanya diketahui melalui komunikasi verbal antara dapur dan "
        "pramusaji, sehingga rata-rata 2 hingga 4 item per hari sempat ditawarkan kepada "
        "pelanggan meskipun sudah tidak tersedia dan pesanan harus dibatalkan atau "
        "diganti.",
    )

    # ------------------------------------------- 3.5.1 Requirement: acuan fitur BAB I
    i = A("Tahapan Requirement dimulai dengan pengumpulan data komprehensif")
    D.append_text(
        i,
        " Kebutuhan fungsional yang ditetapkan pada tahap ini merupakan penjabaran "
        "langsung dari delapan fungsi sistem yang telah disebutkan pada subbab 1.1 dan "
        "dibatasi pada subbab 1.3, yaitu pemesanan mandiri melalui QR Code, penyajian "
        "menu digital, pengelolaan ketersediaan/stok menu dan add-on, integrasi pesanan "
        "dengan dapur, pembayaran tunai dan non-tunai melalui Midtrans Snap, pemisahan "
        "status pembayaran dari status dapur, pelacakan progres pesanan oleh pelanggan, "
        "serta pembagian hak akses bagi empat aktor. Daftar kebutuhan fungsional pada "
        "subbab ini menjadi acuan utama bagi tahap Design (3.6–3.9), Implementation, "
        "serta Testing (3.10 dan 3.12).",
    )

    i = A("Kebutuhan fungsional sistem pemesanan menu mendefinisikan secara spesifik")
    D.set_text(
        i,
        "Kebutuhan fungsional sistem pemesanan menu mendefinisikan secara spesifik "
        "kapabilitas yang harus dimiliki perangkat lunak untuk memenuhi kebutuhan "
        "operasional di Restoran Kekupu Villa Jembrana. Tabel 3.1 memetakan kondisi "
        "berjalan terhadap target sistem baru pada setiap dimensi layanan, sedangkan "
        "Tabel 3.2 sampai dengan Tabel 3.6 merinci kebutuhan fungsional per aktor "
        "beserta kode acuannya. Kode kebutuhan inilah yang dirujuk kembali pada Use Case "
        "Diagram (3.7), ERD (3.8), rancangan antarmuka (3.9 dan 3.15), skenario "
        "Black-Box Testing (3.10), dan indikator UAT (3.12), sehingga setiap fungsi yang "
        "dinyatakan dibangun dapat dilacak sampai ke tahap pengujian.",
    )

    # Tabel 3.1: perbaiki target ketersediaan menu (dikelola Admin, bukan Koki)
    D.cell(
        TBL[1], 2, 4,
        "Admin memutakhirkan ketersediaan/stok menu dan add-on pada sistem, dan stok "
        "berkurang otomatis saat pesanan dibuat. Item atau opsi add-on dengan stok nol "
        "maupun berstatus nonaktif tidak lagi ditampilkan sebagai pilihan pada antarmuka "
        "pelanggan.",
    )
    D.cell(
        TBL[1], 2, 3,
        "Informasi ketersediaan menu tidak tercatat secara digital; pelanggan sering baru "
        "mengetahui menu habis setelah pramusaji konfirmasi ke dapur.",
    )
    D.cell(TBL[1], 2, 2, "Akurasi Ketersediaan/Stok Menu")

    i = A("Tabel 3.1 Analisis Kebutuhan Fungsional")
    D.set_text(
        i,
        "Tabel 3.1 Analisis Kebutuhan Fungsional (Kondisi Saat Ini terhadap Target "
        "Sistem Baru)",
    )

    tmpl_body = A("Kebutuhan fungsional sistem pemesanan menu mendefinisikan secara spesifik")
    tmpl_caption = i

    # ---------------------------------------------------- Tabel 3.2 s.d. Tabel 3.6
    hdr = ["Kode", "Kebutuhan Fungsional", "Keterangan Implementasi"]

    pelanggan = [
        hdr,
        ["KF-P01", "Memindai QR Code meja",
         "QR Code pada tiap meja memuat tautan rute /meja/{table_number}; nomor meja "
         "disimpan pada sesi pelanggan dan terisi otomatis pada pesanan."],
        ["KF-P02", "Melihat daftar menu berdasarkan kategori",
         "Katalog ditampilkan per kategori (Makanan dan Minuman) yang bersumber dari "
         "tabel categories."],
        ["KF-P03", "Melihat harga dan deskripsi menu",
         "Menampilkan items.price, items.description, dan items.img pada kartu menu."],
        ["KF-P04", "Melihat ketersediaan menu",
         "Hanya item dengan is_active bernilai benar dan stock lebih besar dari nol yang "
         "dapat dipesan; item lainnya ditandai tidak tersedia."],
        ["KF-P05", "Memilih add-on pada item menu",
         "Opsi diambil dari addon_groups dan addons, divalidasi terhadap min_select dan "
         "max_select serta ketersediaan stok add-on."],
        ["KF-P06", "Menambahkan menu ke keranjang",
         "Item beserta add-on terpilih disimpan pada keranjang berbasis sesi; subtotal "
         "dihitung dari harga item ditambah harga add-on dikalikan kuantitas."],
        ["KF-P07", "Mengubah atau menghapus isi keranjang",
         "Perubahan kuantitas, penggantian add-on, dan penghapusan baris memutakhirkan "
         "subtotal secara otomatis."],
        ["KF-P08", "Menambahkan catatan pesanan",
         "Catatan pelanggan disimpan pada kolom orders.note dan tampil pada layar dapur."],
        ["KF-P09", "Melakukan checkout",
         "Sistem membentuk data orders dan order_items, menghitung subtotal, pajak 10%, "
         "dan grand_total, membangkitkan order_code, serta mengurangi stok item dan "
         "add-on."],
        ["KF-P10", "Memilih metode pembayaran",
         "Pilihan tunai atau qris disimpan pada kolom orders.payment_method."],
        ["KF-P11", "Melakukan pembayaran non-tunai",
         "Sistem meminta snap_token ke Midtrans dan menampilkan jendela Snap berisi kanal "
         "QRIS, e-wallet, dan transfer bank."],
        ["KF-P12", "Melihat status dan progres pesanan",
         "Pelanggan menelusuri pesanannya melalui order_code dan melihat status "
         "pembayaran (orders.status) serta progres dapur (orders.kitchen_status)."],
    ]

    admin = [
        hdr,
        ["KF-A01", "Login sebagai Admin",
         "Autentikasi melalui akun staf; otorisasi ditentukan oleh role admin pada tabel "
         "roles."],
        ["KF-A02", "Mengelola data menu (tambah, ubah, hapus)",
         "Operasi CRUD pada tabel items beserta unggahan gambar menu."],
        ["KF-A03", "Mengelola kategori menu",
         "Operasi CRUD pada tabel categories yang dipakai sebagai filter katalog "
         "pelanggan."],
        ["KF-A04", "Mengelola ketersediaan/stok menu",
         "Memutakhirkan kolom items.stock dan items.is_active; nilai stok nol membuat "
         "item tersembunyi dari katalog pelanggan."],
        ["KF-A05", "Mengelola add-on",
         "Mengelola kelompok add-on (addon_groups) beserta opsinya (addons), keterkaitan "
         "dengan item melalui addon_group_item, batas min_select/max_select, harga, dan "
         "stok add-on."],
        ["KF-A06", "Mengelola data karyawan",
         "Operasi CRUD pada tabel users untuk akun Koki dan Kasir."],
        ["KF-A07", "Mengelola role/hak akses",
         "Operasi CRUD pada tabel roles yang menjadi dasar otorisasi setiap akun."],
        ["KF-A08", "Melihat riwayat pesanan",
         "Menampilkan seluruh pesanan beserta nomor meja, metode bayar, status "
         "pembayaran, status dapur, dan rincian item."],
        ["KF-A09", "Melihat dan mengunduh laporan pesanan bulanan",
         "Rekapitulasi pesanan per bulan yang dapat diunduh sebagai berkas lembar kerja."],
        ["KF-A10", "Membangkitkan QR Code meja",
         "Halaman QR meja menghasilkan QR Code untuk 12 meja yang masing-masing mengarah "
         "ke rute /meja/{table_number}."],
    ]

    koki = [
        hdr,
        ["KF-K01", "Login sebagai Koki",
         "Autentikasi akun staf dengan role chef; akses dibatasi pada halaman pesanan."],
        ["KF-K02", "Melihat antrean pesanan",
         "Menampilkan pesanan yang telah lunas (orders.status bernilai settlement) dan "
         "belum selesai diproses."],
        ["KF-K03", "Melihat nomor meja",
         "Menampilkan orders.table_number sebagai tujuan penyajian hidangan."],
        ["KF-K04", "Melihat item pesanan beserta add-on",
         "Menampilkan order_items beserta snapshot kustomisasi pada kolom JSON "
         "order_items.addons."],
        ["KF-K05", "Melihat catatan pesanan",
         "Menampilkan orders.note sebagai instruksi tambahan pengolahan."],
        ["KF-K06", "Memutakhirkan status dapur",
         "Mengubah orders.kitchen_status menjadi processing, cooking, atau ready; hanya "
         "diizinkan pada pesanan yang telah lunas."],
        ["KF-K07", "Menerima indikator pesanan baru",
         "Penanda visual pada kartu pesanan yang baru masuk ke antrean dapur."],
    ]

    kasir = [
        hdr,
        ["KF-S01", "Login sebagai Kasir",
         "Autentikasi akun staf dengan role cashier."],
        ["KF-S02", "Melihat pesanan yang menunggu pembayaran",
         "Menampilkan pesanan dengan orders.status bernilai pending beserta metode "
         "bayarnya."],
        ["KF-S03", "Mengonfirmasi pembayaran tunai",
         "Hanya untuk orders.payment_method bernilai tunai; sistem menuliskan status "
         "settlement dan meneruskan pesanan ke dapur (kitchen_status menjadi processing)."],
        ["KF-S04", "Memantau status pembayaran Midtrans",
         "Untuk orders.payment_method bernilai qris, Kasir hanya memantau status yang "
         "ditulis sistem melalui webhook; tombol konfirmasi manual tidak tersedia."],
        ["KF-S05", "Melihat pesanan yang telah lunas",
         "Menampilkan pesanan berstatus settlement beserta progres dapurnya."],
        ["KF-S06", "Mencetak nota transaksi",
         "Menampilkan dan mencetak rincian item, add-on, subtotal, pajak, dan "
         "grand_total pada format nota."],
        ["KF-S07", "Mengunduh laporan pesanan bulanan",
         "Rekapitulasi pesanan per bulan sebagai dasar penyusunan laporan penjualan."],
    ]

    sistem = [
        hdr,
        ["KF-M01", "Membuat transaksi Snap",
         "Sistem mengirim order_code, grand_total, dan rincian item ke Midtrans Snap API "
         "lalu menerima snap_token."],
        ["KF-M02", "Menerima webhook notifikasi pembayaran",
         "Midtrans mengirim notifikasi ke endpoint POST /midtrans/notification berisi "
         "transaction_status dan signature_key."],
        ["KF-M03", "Memverifikasi keaslian notifikasi",
         "Sistem mencocokkan signature_key (SHA-512 dari order_id, status_code, "
         "gross_amount, dan server_key) sebelum memproses notifikasi."],
        ["KF-M04", "Mengubah status pembayaran menjadi settlement",
         "Notifikasi berstatus settlement atau capture menuliskan orders.status menjadi "
         "settlement."],
        ["KF-M05", "Meneruskan pesanan lunas ke antrean dapur",
         "Setelah status settlement tercatat, orders.kitchen_status berubah dari waiting "
         "menjadi processing sehingga pesanan tampil pada layar dapur."],
        ["KF-M06", "Memvalidasi sesi/token meja pelanggan",
         "Sesi meja hasil pemindaian QR Code dijaga terpisah antar pelanggan sehingga "
         "keranjang dan pesanan tidak tertukar antar meja."],
    ]

    anchor_text = "Tabel 3.1 Analisis Kebutuhan Fungsional (Kondisi Saat Ini"
    for intro, caption, rows in [
        (
            "Kebutuhan fungsional Pelanggan mencakup keseluruhan alur pemesanan mandiri, "
            "mulai dari pemindaian QR Code meja sampai dengan pemantauan progres pesanan, "
            "sebagaimana dirinci pada tabel berikut.",
            "Tabel 3.2 Kebutuhan Fungsional Aktor Pelanggan",
            pelanggan,
        ),
        (
            "Kebutuhan fungsional Admin mencakup pengelolaan seluruh data master, "
            "ketersediaan menu dan add-on, akun karyawan beserta hak aksesnya, serta "
            "peninjauan riwayat pesanan dan laporan.",
            "Tabel 3.3 Kebutuhan Fungsional Aktor Admin",
            admin,
        ),
        (
            "Kebutuhan fungsional Koki dibatasi pada ranah produksi dapur, yaitu "
            "menerima antrean pesanan yang telah lunas dan memutakhirkan progres "
            "pengolahan hidangan.",
            "Tabel 3.4 Kebutuhan Fungsional Aktor Koki",
            koki,
        ),
        (
            "Kebutuhan fungsional Kasir dibatasi pada titik pembayaran, dengan pemisahan "
            "tegas antara pembayaran tunai yang dikonfirmasi manual dan pembayaran "
            "non-tunai yang hanya dipantau.",
            "Tabel 3.5 Kebutuhan Fungsional Aktor Kasir",
            kasir,
        ),
        (
            "Kebutuhan fungsional Sistem dan Midtrans mencakup pembuatan transaksi Snap, "
            "penerimaan serta verifikasi webhook, penulisan status pelunasan, dan "
            "penerusan pesanan ke antrean dapur.",
            "Tabel 3.6 Kebutuhan Fungsional Sistem dan Midtrans",
            sistem,
        ),
    ]:
        anchor_text = _block(D, anchor_text, intro, caption, TBL[4], FR_WIDTHS, rows,
                             tmpl_body, tmpl_caption)

    # Kebutuhan non-fungsional: Tabel 3.2 -> Tabel 3.7
    i = A("Tabel 3.2 Analisis Kebutuhan Non-Fungsional")
    D.set_text(i, "Tabel 3.7 Analisis Kebutuhan Non-Fungsional")

    D.cell(
        TBL[2], 2, 4,
        "Pembatasan hak akses yang ketat pada panel staf berdasarkan role (Admin, Koki, "
        "dan Kasir) menggunakan middleware otorisasi Laravel, sedangkan pelanggan "
        "diakses melalui sesi meja tanpa akun.",
    )
