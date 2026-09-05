"""BAB I revisions: sinkronisasi masalah-fitur, aktor, batasan, rumusan, tujuan, manfaat."""


def apply(D):
    A = D.find_para

    # ---------------------------------------------------------------- Abstrak
    i = A("Fakultas Teknologi Informasi dan Sains, Universitas Hindu Indonesia, 2025")
    D.set_text(
        i,
        "Proposal, Program Studi Sistem Informasi, Fakultas Teknik, Perencanaan dan "
        "Informatika, Universitas Hindu Indonesia, 2026",
    )

    i = A("Penelitian ini bertujuan untuk mendigitalisasi sistem pemesanan menu")
    D.set_text(
        i,
        "Penelitian ini bertujuan mendigitalisasi sistem pemesanan menu di Restoran "
        "Kekupu Villa Jembrana guna mengatasi ketidakefisienan pelayanan, risiko "
        "kesalahan pencatatan pesanan, dan lambatnya verifikasi pembayaran pada proses "
        "manual. Sistem yang dibangun berbasis web dengan akses pelanggan melalui "
        "pemindaian QR Code meja, sehingga pelanggan dapat memesan secara mandiri tanpa "
        "diwajibkan membuat akun. Cakupan fungsi sistem meliputi penyajian menu digital, "
        "pengelolaan ketersediaan/stok menu dan add-on, penerusan pesanan yang telah "
        "lunas ke antrean dapur, pembayaran tunai yang dikonfirmasi Kasir serta "
        "pembayaran non-tunai melalui Payment Gateway Midtrans Snap yang diverifikasi "
        "melalui webhook, pemantauan progres pesanan oleh pelanggan, serta pembagian hak "
        "akses bagi empat aktor yaitu Pelanggan, Koki, Kasir, dan Admin. Pengembangan "
        "menggunakan metode Waterfall yang mencakup tahap requirement, design, "
        "implementation, testing, dan maintenance, dengan PHP 8.1, Framework Laravel 12, "
        "dan basis data MySQL. Pengumpulan data dilakukan melalui observasi, wawancara, "
        "dan studi pustaka, sedangkan pengujian kualitas perangkat lunak menggunakan "
        "Black-Box Testing dan User Acceptance Testing (UAT). Hasil akhir penelitian ini "
        "diharapkan meningkatkan akurasi pencatatan transaksi, kecepatan pelayanan, dan "
        "transparansi status pesanan maupun pembayaran.",
    )

    i = A("Kata Kunci : Sistem Informasi, Web, Menu, Laravel 12, Villa Jembrana")
    D.set_text(
        i,
        "Kata Kunci : Sistem Pemesanan Menu, QR Code, Laravel 12, Midtrans Snap, "
        "Ketersediaan Menu, Restoran Kekupu Villa Jembrana",
    )

    i = A("and Science, Universitas Hindu Indonesia, 2025.")
    D.set_text(
        i, "and Science, Universitas Hindu Indonesia, 2026."
    )

    i = A("This research aims to digitalize the menu ordering system")
    D.set_text(
        i,
        "This research aims to digitalize the menu ordering system at Kekupu Villa "
        "Jembrana Restaurant to address service inefficiency, order-recording errors, "
        "and slow payment verification inherent in manual processes. The system is "
        "web-based and is accessed by customers through scanning a table QR Code, "
        "enabling self-ordering without any account registration. Its functional scope "
        "covers digital menu presentation, management of menu and add-on availability "
        "(stock), forwarding of settled orders to the kitchen queue, cash payments "
        "confirmed by the Cashier as well as cashless payments through the Midtrans Snap "
        "payment gateway verified via webhook, customer order-progress tracking, and "
        "role-based access for four actors: Customer, Chef, Cashier, and Admin. The "
        "development adopts the Waterfall methodology covering requirement, design, "
        "implementation, testing, and maintenance, built with PHP 8.1, the Laravel 12 "
        "framework, and a MySQL database. Data were collected through observation, "
        "interviews, and literature study, while software quality was evaluated using "
        "Black-Box Testing and User Acceptance Testing (UAT). The expected outcome is "
        "improved transaction-recording accuracy, faster service, and greater "
        "transparency of order and payment status.",
    )

    i = A("Kata Kunci : Sistem Informasi, Web, Menu, Laravel 12, Villa Jembrana")
    D.set_text(
        i,
        "Keywords : Menu Ordering System, QR Code, Laravel 12, Midtrans Snap, Menu "
        "Availability, Kekupu Villa Jembrana Restaurant",
    )

    # ------------------------------------------------------- 1.1 Latar Belakang
    # Ringkasan fitur sistem baru: acuan tunggal BAB I -> BAB III.
    anchor = A("Dalam pengembangan sistem ini, Framework Laravel 12 dipilih")
    body_tmpl = A("Layanan hosting diperlukan agar tautan yang dituju")
    D.insert_paras_after(
        anchor,
        [
            (
                body_tmpl,
                "Agar permasalahan yang diuraikan di atas benar-benar terjawab oleh "
                "perangkat lunak yang dibangun, ruang lingkup fungsi sistem pada "
                "penelitian ini ditetapkan secara eksplisit sebagai berikut: (1) "
                "pemesanan dilakukan pelanggan secara mandiri melalui pemindaian QR Code "
                "pada meja; (2) menu ditampilkan secara digital beserta kategori, harga, "
                "deskripsi, dan gambar; (3) ketersediaan atau stok menu dan add-on dapat "
                "dikelola sehingga item yang telah habis tidak lagi ditawarkan kepada "
                "pelanggan; (4) pesanan yang telah lunas diteruskan ke dapur secara "
                "terintegrasi dalam satu basis data; (5) pembayaran mendukung metode "
                "tunai dan metode non-tunai melalui Midtrans Snap; (6) status pembayaran "
                "dibedakan secara eksplisit dari status proses dapur; (7) pelanggan dapat "
                "mengetahui progres pesanannya melalui kode pesanan; serta (8) Admin, "
                "Koki, Kasir, dan Pelanggan memiliki hak akses yang berbeda. Kedelapan "
                "fungsi inilah yang dipakai sebagai acuan tunggal pada rumusan masalah "
                "(1.4), tujuan penelitian (1.5), kebutuhan fungsional (3.5.1), "
                "perancangan (3.6–3.9), serta pengujian (3.10 dan 3.12), sehingga tidak "
                "terdapat fitur yang dibahas pada landasan teori maupun perancangan "
                "tetapi tidak dibangun pada implementasi.",
            ),
            (
                body_tmpl,
                "Perlu ditegaskan bahwa pengelolaan persediaan yang dimaksud dalam "
                "penelitian ini adalah pengelolaan ketersediaan atau stok menu dan add-on "
                "yang ditawarkan kepada pelanggan, bukan pengelolaan persediaan bahan "
                "baku dapur. Sistem tidak memiliki tabel maupun proses inventori bahan "
                "baku, sehingga istilah manajemen stok bahan baku tidak digunakan pada "
                "seluruh naskah proposal ini.",
            ),
        ],
    )

    i = A('Berdasarkan permasalahan tersebut, penelitian ini mengembangkan')
    D.sub(
        i,
        "serta menyediakan laporan transaksi operasional secara real-time bagi pemilik "
        "restoran.",
        "serta menyediakan rekapitulasi riwayat pesanan dan laporan pesanan bulanan yang "
        "dapat diunduh oleh pemilik restoran.",
    )

    # -------------------------------------------------- 1.2 Identifikasi Masalah
    anchor = A("Komunikasi Inter-Departemen Terhambat")
    D.insert_paras_after(
        anchor,
        [
            (
                anchor,
                "Ketersediaan Menu Tidak Transparan: Ketersediaan menu tidak tercatat "
                "secara digital, sehingga pelanggan baru mengetahui suatu menu telah "
                "habis setelah pramusaji menanyakannya ke dapur dan pesanan harus "
                "dibatalkan atau diganti.",
            )
        ],
    )

    i = A("Belum Adanya Pengujian Sistem yang Terukur")
    D.append_text(
        i,
        "",
    )

    # ---------------------------------------------------- 1.3 Pembatasan Masalah
    i = A("Sistem informasi ini dirancang khusus untuk mengotomatisasi proses pemesanan")
    D.set_text(
        i,
        "Sistem informasi ini dirancang khusus untuk mengotomatisasi proses pemesanan "
        "menu dan transaksi pembayaran pada Restoran Kekupu Villa Jembrana, dengan hak "
        "akses pengguna (user privilege) yang dibatasi pada empat aktor utama, yaitu "
        "Pelanggan, Koki, Kasir, dan Admin (Owner/Manager). Peran pramusaji tidak "
        "dimodelkan sebagai aktor sistem karena fungsi pencatatan pesanan telah "
        "digantikan oleh pemesanan mandiri pelanggan melalui QR Code, sehingga istilah "
        "Staf Pelayan tidak lagi digunakan pada perancangan maupun pengujian sistem.",
    )

    i = A("Pelanggan dapat mengakses menu digital secara langsung melalui pemindaian")
    D.set_text(
        i,
        "Pelanggan tidak diwajibkan membuat akun maupun melakukan login. Akses "
        "pelanggan diperoleh melalui sesi/token meja hasil pemindaian QR Code pada "
        "masing-masing meja, sehingga nomor meja terisi otomatis pada pesanan. "
        "Sebaliknya, Koki, Kasir, dan Admin wajib login menggunakan akun staf yang "
        "kewenangannya ditentukan berdasarkan role.",
    )

    i = A("Sistem ini difokuskan pada fitur pemesanan menu digital")
    D.set_text(
        i,
        "Sistem difokuskan pada pemesanan menu digital, pengelolaan ketersediaan/stok "
        "menu dan add-on, pengelolaan status proses dapur, serta pemrosesan pembayaran "
        "melalui dua kanal, yaitu: (a) tunai, yang dikonfirmasi secara manual oleh "
        "Kasir; dan (b) non-tunai, yang diproses melalui Midtrans Snap dan status "
        "pelunasannya diterima sistem melalui webhook. Kasir tidak mengonfirmasi "
        "pembayaran QRIS/Midtrans secara manual.",
    )

    stok_anchor = A("Sistem difokuskan pada pemesanan menu digital")
    D.insert_paras_after(
        stok_anchor,
        [
            (
                stok_anchor,
                "Sistem mengelola stok/ketersediaan menu dan add-on yang ditawarkan "
                "kepada pelanggan melalui kolom stock dan is_active pada tabel items "
                "serta addons. Menu maupun opsi add-on yang berstatus nonaktif atau "
                "berstok nol tidak ditampilkan sebagai pilihan pada antarmuka pelanggan.",
            ),
            (
                stok_anchor,
                "Status pembayaran (pending dan settlement pada kolom orders.status) "
                "dibedakan secara eksplisit dari status proses dapur (waiting, "
                "processing, cooking, dan ready pada kolom orders.kitchen_status), "
                "sehingga pelunasan pembayaran dan progres pengolahan hidangan tercatat "
                "sebagai dua informasi yang terpisah.",
            ),
        ],
    )

    i = A("Sistem ini tidak mencakup pengelolaan stok bahan baku/inventaris dapur")
    D.set_text(
        i,
        "Sistem tidak mencakup modul inventori bahan baku dapur, pembelian kepada "
        "pemasok (supplier), penggajian karyawan (payroll), reservasi meja, maupun "
        "manajemen logistik persediaan barang.",
    )

    # ------------------------------------------------------- 1.4 Rumusan Masalah
    r1 = A("Bagaimana merancang sistem informasi pemesanan menu berbasis web menggunakan")
    D.set_text(
        r1,
        "Bagaimana merancang dan membangun sistem pemesanan menu berbasis web dan QR "
        "Code menggunakan framework Laravel 12 yang memungkinkan pelanggan Restoran "
        "Kekupu Villa Jembrana memesan secara mandiri dari meja tanpa diwajibkan "
        "melakukan registrasi akun?",
    )

    r2 = A("Bagaimana mengimplementasikan sistem informasi pemesanan menu berbasis web dengan")
    D.set_text(
        r2,
        "Bagaimana mengimplementasikan pengelolaan menu, kategori, add-on, serta "
        "ketersediaan/stok menu sehingga katalog yang ditampilkan kepada pelanggan selalu "
        "mencerminkan item yang benar-benar tersedia?",
    )

    D.insert_paras_after(
        r2,
        [
            (
                r2,
                "Bagaimana mengintegrasikan pesanan pelanggan dengan antrean dapur "
                "sehingga Koki dapat menerima rincian pesanan dan memutakhirkan status "
                "pengolahan tanpa pencatatan ulang secara manual?",
            ),
            (
                r2,
                "Bagaimana mengelola pembayaran tunai yang dikonfirmasi oleh Kasir dan "
                "pembayaran non-tunai yang diproses melalui Midtrans Snap serta "
                "diverifikasi melalui webhook, dengan status pembayaran yang dibedakan "
                "dari status proses dapur?",
            ),
            (
                r2,
                "Bagaimana mengelola hak akses Admin, Koki, Kasir, dan Pelanggan agar "
                "setiap peran hanya dapat mengakses fungsi yang menjadi wewenangnya?",
            ),
        ],
    )

    # ------------------------------------------------------- 1.5 Tujuan Penelitian
    t1 = A("Menghasilkan rancangan sistem informasi pemesanan menu berbasis web menggunakan")
    D.set_text(
        t1,
        "Membangun sistem pemesanan menu berbasis web dan QR Code menggunakan framework "
        "Laravel 12 pada Restoran Kekupu Villa Jembrana.",
    )

    t2 = A("Membangun dan mengimplementasikan sistem informasi pemesanan menu berbasis web dengan")
    D.set_text(
        t2,
        "Menyediakan fasilitas pemesanan mandiri (self-ordering) bagi pelanggan melalui "
        "sesi/token meja hasil pemindaian QR Code, tanpa kewajiban registrasi akun.",
    )

    D.insert_paras_after(
        t2,
        [
            (
                t2,
                "Menyediakan pengelolaan menu, kategori, add-on, serta ketersediaan/stok "
                "menu bagi Admin sebagai pengelola data master.",
            ),
            (
                t2,
                "Mengintegrasikan pesanan pelanggan dengan antrean dapur sehingga Koki "
                "dapat memutakhirkan status pengolahan pesanan secara langsung pada "
                "sistem.",
            ),
            (
                t2,
                "Menyediakan dua kanal pembayaran, yaitu pembayaran tunai yang "
                "dikonfirmasi Kasir dan pembayaran non-tunai melalui Midtrans Snap yang "
                "status pelunasannya diverifikasi melalui webhook.",
            ),
            (
                t2,
                "Menyediakan informasi status pembayaran dan progres pesanan yang dapat "
                "dipantau oleh Pelanggan, Koki, Kasir, dan Admin sesuai wewenang "
                "masing-masing.",
            ),
        ],
    )

    i = A("Menguji fungsionalitas dan penerimaan sistem menggunakan metode Black Box Testing")
    D.set_text(
        i,
        "Menguji fungsionalitas dan penerimaan sistem menggunakan metode Black Box "
        "Testing dan User Acceptance Testing (UAT) untuk memastikan seluruh fitur "
        "berjalan sesuai luaran yang diharapkan serta mengetahui tingkat kelayakan sistem "
        "sebelum diterapkan secara penuh.",
    )

    # ------------------------------------------------------ 1.6 Manfaat Penelitian
    i = A("Sistem ini mempermudah pelanggan melalui mekanisme pemesanan dan pembayaran")
    D.set_text(
        i,
        "Manfaat sistem ini dijabarkan menurut peran masing-masing pengguna agar selaras "
        "dengan fungsi yang benar-benar dibangun.",
    )
    tmpl = i
    D.insert_paras_after(
        i,
        [
            (
                tmpl,
                "Bagi Pelanggan: dapat memesan secara lebih mandiri langsung dari meja, "
                "melihat daftar menu beserta harga dan ketersediaannya, memilih add-on "
                "sesuai selera, melakukan pembayaran secara tunai maupun non-tunai, serta "
                "mengetahui status pesanannya tanpa harus menanyakannya kepada staf.",
            ),
            (
                tmpl,
                "Bagi Koki: dapat menerima antrean pesanan yang telah lunas secara "
                "langsung pada perangkat dapur, mengetahui nomor meja, rincian item "
                "beserta add-on, dan catatan pelanggan, serta memperbarui status "
                "pengolahan pesanan tanpa bergantung pada nota kertas.",
            ),
            (
                tmpl,
                "Bagi Kasir: dapat memantau daftar pembayaran yang masih menunggu "
                "pelunasan, mengonfirmasi pembayaran tunai, memantau pelunasan "
                "(settlement) transaksi Midtrans tanpa konfirmasi manual, serta "
                "menampilkan dan mencetak nota transaksi.",
            ),
            (
                tmpl,
                "Bagi Admin/Owner: dapat mengelola data menu, kategori, add-on, "
                "ketersediaan/stok, data karyawan, serta role/hak akses, dan meninjau "
                "riwayat pesanan beserta laporan rekapitulasi pesanan bulanan sebagai "
                "dasar pengambilan keputusan operasional.",
            ),
            (
                tmpl,
                "Bagi Restoran Kekupu Villa Jembrana secara keseluruhan, sistem ini "
                "mengoptimalkan table turnover, meminimalisir kesalahan pencatatan "
                "pesanan, mempercepat verifikasi pembayaran, serta menyatukan koordinasi "
                "data operasional antara pelanggan, dapur, kasir, dan pemilik dalam satu "
                "basis data.",
            ),
        ],
    )
