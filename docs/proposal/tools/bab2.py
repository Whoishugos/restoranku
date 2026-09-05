"""BAB II revisions: hapus istilah bahan baku, tambah teori Midtrans, renumber subbab."""


def apply(D, TBL):
    A = D.find_para

    # -------------------------------------- 2.1 tabel penelitian relevan (Tabel 2.1)
    t = TBL[0]
    D.cell(t, 11, 4, "Web + QR Code + Laravel 12 + MySQL + Payment Gateway Midtrans "
                     "(Snap + webhook)")
    D.cell(t, 11, 8, "Ya, stok/ketersediaan menu dan add-on (bukan inventori bahan baku)")
    D.cell(t, 11, 9, "Ya, riwayat pesanan dan laporan rekapitulasi pesanan bulanan "
                     "(dapat diunduh)")
    D.cell(t, 11, 10, "Black-box (34 skenario) + UAT (skala Likert)")

    # ------------------------------ istilah "stok bahan baku" pada ulasan penelitian
    i = A("Kekurangan: Sistem belum dilengkapi fitur pengelolaan stok bahan baku maupun "
          "peran khusus untuk aktor dapur")
    D.set_text(
        i,
        "Kekurangan: Sistem belum dilengkapi fitur pengelolaan ketersediaan/stok menu "
        "maupun peran khusus untuk aktor dapur, sehingga informasi pesanan yang perlu "
        "dimasak masih bergantung pada komunikasi manual antara kasir dan karyawan "
        "dapur.",
    )

    i = A("Penelitian ini menggunakan framework CodeIgniter 4 dan belum memiliki modul "
          "dapur maupun manajemen stok")
    D.set_text(
        i,
        "Perbedaan dengan penelitian yang dilakukan: Penelitian ini menggunakan "
        "framework CodeIgniter 4 dan belum memiliki modul dapur maupun pengelolaan "
        "ketersediaan menu, sedangkan penelitian yang dilakukan memadukan Framework "
        "Laravel 12 dengan teknologi QR Code yang dilengkapi modul dapur dan pengelolaan "
        "ketersediaan/stok menu beserta add-on pada studi kasus Restoran Kekupu Villa "
        "Jembrana.",
    )

    i = A("Kekurangan: Sistem belum dilengkapi fitur pengelolaan stok bahan baku, serta "
          "pengujian kepuasan pengguna")
    D.set_text(
        i,
        "Kekurangan: Sistem belum dilengkapi fitur pengelolaan ketersediaan/stok menu, "
        "serta pengujian kepuasan pengguna pada bagian dapur (65%) masih menunjukkan "
        "tingkat kepuasan yang relatif rendah dibanding aktor lain, mengindikasikan "
        "adanya kendala pada sisi kemudahan penggunaan modul dapur.",
    )

    i = A("Penelitian ini menggunakan framework CodeIgniter dan belum memiliki fitur "
          "manajemen stok bahan baku")
    D.set_text(
        i,
        "Perbedaan dengan penelitian yang dilakukan: Penelitian ini menggunakan "
        "framework CodeIgniter dan belum memiliki fitur pengelolaan ketersediaan menu, "
        "sedangkan penelitian yang dilakukan memadukan Framework Laravel 12 dengan "
        "teknologi QR Code yang dilengkapi pengelolaan ketersediaan/stok menu dan add-on "
        "pada studi kasus Restoran Kekupu Villa Jembrana.",
    )

    # ------------------------------------------------- 2.2 Sistem Informasi (istilah)
    i = A("Kondisi pencatatan pesanan di Restoran Kekupu Villa Jembrana saat ini bersifat")
    D.sub(
        i,
        "(2) data transaksi (pesanan, menu, stok) sebagai objek yang diolah",
        "(2) data transaksi (pesanan, menu, add-on, dan ketersediaan/stok menu) sebagai "
        "objek yang diolah",
    )

    # ---------------------------------------------------------- 2.5 QR Code (detail)
    i = A("QR Code dipilih dibanding alternatif lain")
    D.sub(
        i,
        "Parameter inilah yang kemudian tersimpan pada kolom table_number di tabel "
        "orders sebagaimana digambarkan pada ERD (Gambar 2.2).",
        "Tautan tersebut mengarah ke rute pemindaian meja (/meja/{table_number}) yang "
        "menyimpan nomor meja pada sesi pelanggan, dan parameter inilah yang kemudian "
        "tersimpan pada kolom table_number di tabel orders sebagaimana digambarkan pada "
        "ERD (Gambar 3.4).",
    )

    # ------------------------------------------------------------- 2.6 PHP 8.1 (enum)
    i = A("Enums  digunakan untuk mendefinisikan nilai tetap")
    D.set_text(
        i,
        "● Enums digunakan untuk mendefinisikan nilai tetap yang tidak boleh berubah "
        "secara bebas, yaitu status pembayaran pesanan (pending dan settlement pada "
        "kolom orders.status), status proses dapur (waiting, processing, cooking, dan "
        "ready pada kolom orders.kitchen_status), serta metode pembayaran "
        "(orders.payment_method bernilai tunai atau qris) yang pada ERD (Gambar 3.4) "
        "memang dirancang bertipe enum. Penggunaan Enums mencegah kesalahan penulisan "
        "string status secara manual yang berpotensi menimbulkan bug pada logika alur "
        "pesanan (misalnya \"Diproses\" versus \"processing\").",
    )

    # --------------------------------------------------------- 2.7 Laravel 12 (ERD ref)
    i = A("Eloquent ORM merepresentasikan relasi antar tabel pada ERD")
    D.sub(i, "ERD (Gambar 2.2)", "ERD (Gambar 3.4)")
    D.sub(
        i,
        "seperti relasi one-to-many antara categories dan items, antara orders dan "
        "order_items, serta antara roles dan users.",
        "seperti relasi one-to-many antara categories dan items, antara orders dan "
        "order_items, antara addon_groups dan addons, serta antara roles dan users, "
        "termasuk relasi many-to-many antara items dan addon_groups melalui tabel "
        "penghubung addon_group_item.",
    )

    i = A("Migration dipakai untuk mendefinisikan dan mendeploy skema basis data")
    D.sub(
        i,
        "(tabel roles, users, categories, items, orders, order_items beserta kolom dan "
        "foreign key-nya)",
        "(tabel roles, users, categories, items, addon_groups, addons, "
        "addon_group_item, orders, dan order_items beserta kolom dan foreign key-nya)",
    )

    i = A("Autentikasi dan Otorisasi Berbasis Role Laravel menyediakan mekanisme")
    D.sub(
        i,
        "berdasarkan kolom role_id pada tabel users (Admin, Koki, Kasir)",
        "berdasarkan kolom role_id pada tabel users yang merujuk tabel roles (admin, "
        "chef/koki, cashier/kasir, dan customer)",
    )
    D.sub(i, "(sesuai pembatasan masalah 1.3 poin 2)", "(sesuai pembatasan masalah 1.3)")

    # ------------------------------------------------------------- 2.9 Hosting (ref)
    i = A("Layanan hosting diperlukan agar tautan yang dituju oleh QR Code")
    D.sub(i, "Model Waterfall (2.13)", "Model Waterfall (2.14)")

    # -------------------------------- SISIP 2.10 Payment Gateway (Midtrans) + renumber
    head_tmpl = A("2.9 Hosting")
    body_tmpl = A("Layanan hosting diperlukan agar tautan yang dituju oleh QR Code")
    anchor = body_tmpl
    D.insert_paras_after(
        anchor,
        [
            (head_tmpl, "2.10 Payment Gateway (Midtrans)"),
            (
                body_tmpl,
                "Payment gateway adalah layanan perantara yang menghubungkan aplikasi "
                "penjual dengan kanal pembayaran milik bank maupun penyelenggara uang "
                "elektronik, sehingga proses otorisasi, penagihan, dan konfirmasi "
                "pelunasan dapat dilakukan secara otomatis tanpa pencocokan bukti "
                "transfer secara manual. Midtrans merupakan salah satu penyedia payment "
                "gateway di Indonesia yang menyediakan Snap, yaitu antarmuka pembayaran "
                "siap pakai yang dipanggil dari sisi klien menggunakan token transaksi "
                "(snap_token) yang sebelumnya diterbitkan oleh server melalui Snap API.",
            ),
            (
                body_tmpl,
                "Pada sistem ini Midtrans dipakai melalui dua mekanisme yang saling "
                "melengkapi. Pertama, Snap API: server mengirimkan identitas transaksi "
                "(order_code), nilai tagihan (grand_total), dan rincian item kepada "
                "Midtrans, lalu menerima snap_token yang digunakan untuk memunculkan "
                "jendela pembayaran berisi kanal QRIS, e-wallet (GoPay dan ShopeePay), "
                "serta transfer bank/virtual account. Kedua, HTTP notification atau "
                "webhook: setelah pelanggan menyelesaikan pembayaran, Midtrans "
                "mengirimkan notifikasi ke endpoint sistem (POST /midtrans/notification) "
                "yang memuat transaction_status dan signature_key. Sistem memverifikasi "
                "keaslian notifikasi tersebut dengan mencocokkan signature_key (hash "
                "SHA-512 dari gabungan order_id, status_code, gross_amount, dan "
                "server_key) sebelum menuliskan status pelunasan pada basis data.",
            ),
            (
                body_tmpl,
                "Konsekuensi arsitektural dari mekanisme tersebut menjadi dasar "
                "pembagian wewenang pada sistem: pelunasan non-tunai diverifikasi oleh "
                "penyedia pembayaran melalui webhook, bukan oleh Kasir, sehingga Kasir "
                "hanya berwenang mengonfirmasi pembayaran tunai dan memantau status "
                "transaksi non-tunai. Status pembayaran yang ditulis melalui jalur ini "
                "(pending menjadi settlement pada kolom orders.status) tetap dibedakan "
                "dari status proses dapur (orders.kitchen_status). Pembahasan teori "
                "Midtrans pada penelitian ini dibatasi pada fungsi Snap dan webhook yang "
                "benar-benar diimplementasikan; fitur lain seperti pembayaran berulang "
                "(recurring), payout, dan pengembalian dana otomatis (refund) tidak "
                "dibahas karena tidak menjadi bagian sistem.",
            ),
        ],
        label="insert 2.10 Payment Gateway (Midtrans)",
    )

    # ------------------------------------------------------------ renumber 2.10 -> 2.17
    renames = [
        ("2.10 Visual Studio Code", "2.11 Visual Studio Code"),
        ("2.11 Use Case Diagram", "2.12 Use Case Diagram"),
        ("2.12 Entity Relationship Diagram (ERD)", "2.13 Entity Relationship Diagram (ERD)"),
        ("2.13 Waterfall Model", "2.14 Waterfall Model"),
        ("2.14 Data Flow Diagram (DFD)", "2.15 Data Flow Diagram (DFD)"),
        ("2.15 Black-box Testing", "2.16 Black-box Testing"),
        ("2.16 User Acceptance Testing (UAT)", "2.17 User Acceptance Testing (UAT)"),
    ]
    for old, new in renames:
        idx = A(old)
        D.sub(idx, old, new, label=f"renumber {old} -> {new}")

    # ------------------------- caption gambar BAB II: bukan "simbol", tetapi diagram sistem
    i = A("Gambar 2.1 Simbol Use Case Diagram")
    D.set_text(i, "Gambar 2.1 Use Case Diagram Sistem Pemesanan Menu")

    i = A("Gambar 2.2 Simbol Entity Relationship Diagram (ERD)")
    D.set_text(i, "Gambar 2.2 Entity Relationship Diagram Sistem Pemesanan Menu")

    # ---------------------------------------- 2.12 Use Case: hapus aktor Staf Pelayan
    i = A("Use Case Diagram adalah salah satu jenis diagram dalam pemodelan sistem")
    D.sub(
        i,
        "yang berfungsi untuk menggambarkan interaksi antara aktor, seperti pelanggan, "
        "pelayan, dan bagian dapur, dengan sistem pemesanan menu berbasis QR Code yang "
        "dikembangkan.",
        "yang berfungsi untuk menggambarkan interaksi antara aktor dan sistem. Pada "
        "sistem pemesanan menu berbasis QR Code yang dikembangkan, aktor tersebut terdiri "
        "atas empat peran, yaitu Pelanggan, Koki, Kasir, dan Admin.",
    )
    D.sub(
        i,
        "seperti memindai menu, melakukan pemesanan, hingga konfirmasi pembayaran tunai.",
        "seperti memindai QR Code meja, melakukan pemesanan mandiri, memutakhirkan status "
        "dapur, hingga konfirmasi pembayaran tunai oleh Kasir.",
    )

    i = A("Lebih lanjut, Use Case Diagram dalam pengembangan sistem")
    D.sub(
        i,
        "Lebih lanjut, Use Case Diagram dalam pengembangan sistem di Restoran Kekupu "
        "Villa Jembrana. ini juga berfungsi",
        "Lebih lanjut, Use Case Diagram dalam pengembangan sistem di Restoran Kekupu "
        "Villa Jembrana ini juga berfungsi",
    )
    D.append_text(
        i,
        " Penerapan notasi tersebut pada sistem yang dikembangkan ditampilkan pada "
        "Gambar 2.1 dan dibahas secara rinci pada BAB III subbab 3.7 (Gambar 3.3) "
        "beserta deskripsi setiap use case pada Tabel 3.16.",
    )

    # ------------------------------------------------- 2.13 ERD: tabel yang benar dipakai
    anchor = A("Lebih lanjut, dijelaskan bahwa ERD digunakan untuk memodelkan struktur data")
    D.insert_paras_after(
        anchor,
        [
            (
                anchor,
                "Pada penelitian ini ERD dipakai untuk memodelkan sembilan tabel yang "
                "benar-benar digunakan sistem, yaitu roles, users, categories, items, "
                "addon_groups, addons, addon_group_item, orders, dan order_items. "
                "Identitas meja tidak dimodelkan sebagai entitas tersendiri, melainkan "
                "disimpan sebagai atribut table_number pada tabel orders yang nilainya "
                "diperoleh dari parameter QR Code. Dengan pembatasan ini tidak terdapat "
                "entitas yang digambarkan pada ERD tetapi tidak dipakai pada "
                "implementasi, dan sebaliknya tidak terdapat tabel yang dipakai "
                "implementasi tetapi tidak tergambar pada ERD. Penerapannya ditampilkan "
                "pada Gambar 2.2 dan dibahas secara rinci pada BAB III subbab 3.8 "
                "(Gambar 3.4), sedangkan penjabaran field setiap tabel disajikan pada "
                "subbab 3.14.",
            )
        ],
    )

    # --------------------------------- 2.14 Waterfall: requirement sebagai acuan tunggal
    i = A("Output: Dokumen spesifikasi kebutuhan sistem (kebutuhan fungsional dan non-fungsional)")
    D.set_text(
        i,
        "Output: Dokumen spesifikasi kebutuhan sistem (kebutuhan fungsional dan "
        "non-fungsional), meliputi daftar fitur pemesanan berbasis QR Code, pengelolaan "
        "menu dan ketersediaan/stok, pengelolaan add-on, integrasi pesanan dengan dapur, "
        "pembayaran tunai dan non-tunai, pelacakan status pesanan, serta hak akses "
        "pengguna (Admin, Koki, Kasir, dan Pelanggan). Daftar kebutuhan fungsional pada "
        "tahap ini berfungsi sebagai acuan tunggal (single source of requirement) yang "
        "wajib muncul kembali pada Use Case Diagram, ERD, DFD, rancangan antarmuka, "
        "skenario Black-Box Testing, dan indikator UAT.",
    )

    # --------------------------------------------------- 2.17 UAT: perbaiki referensi
    i = A("Ketentuan teknis instrumen, indikator, skala, rumus, kategori")
    D.sub(i, "BAB III subbab 3.5.3", "BAB III subbab 3.12")
