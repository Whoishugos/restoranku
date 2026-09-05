"""BAB III lanjutan: use case, ERD, black-box 34 skenario, DFD, UAT, struktur tabel, UI."""


def apply(D, TBL):
    A = D.find_para

    # =============================================== 3.7 Use Case: hapus Staf Pelayan
    i = A("Use Case Diagram merupakan alat visualisasi penting dalam pengembangan sistem")
    D.set_text(
        i,
        "Use Case Diagram merupakan alat visualisasi yang menggambarkan interaksi antara "
        "aktor dengan fungsionalitas utama (use cases) sistem pemesanan menu di Restoran "
        "Kekupu Villa Jembrana. Sistem ini memiliki empat aktor, yaitu Pelanggan, Koki, "
        "Kasir, dan Admin. Istilah \"Staf Pelayan\" yang sebelumnya digunakan pada narasi "
        "tidak lagi dipakai karena fungsi pencatatan pesanan telah digantikan oleh "
        "pemesanan mandiri pelanggan melalui QR Code, sehingga aktor tersebut tidak "
        "memiliki use case maupun hak akses pada sistem. Diagram ini mendokumentasikan "
        "kebutuhan fungsional pada Tabel 3.2 sampai dengan Tabel 3.6 dari perspektif "
        "pengguna, mulai dari pemindaian QR Code meja oleh pelanggan sampai dengan "
        "pengelolaan data menu dan hak akses oleh Admin.",
    )
    tmpl_body = i

    D.insert_paras_after(
        i,
        [
            (
                tmpl_body,
                "Pelanggan memiliki use case memindai QR Code meja, melihat menu beserta "
                "ketersediaannya, memilih add-on, mengelola keranjang, melakukan "
                "checkout, melakukan pembayaran (tunai atau non-tunai melalui Midtrans "
                "Snap), dan melihat status pesanan.",
            ),
            (
                tmpl_body,
                "Koki memiliki use case login, melihat antrean pesanan yang telah lunas, "
                "dan memutakhirkan status dapur.",
            ),
            (
                tmpl_body,
                "Kasir memiliki use case login, melihat daftar pembayaran, mengonfirmasi "
                "pembayaran tunai, memantau status pembayaran Midtrans tanpa konfirmasi "
                "manual, dan mencetak nota transaksi.",
            ),
            (
                tmpl_body,
                "Admin memiliki use case login, mengelola menu, mengelola kategori, "
                "mengelola add-on beserta ketersediaan/stok, mengelola data karyawan, "
                "mengelola role/hak akses, serta melihat riwayat pesanan dan laporan "
                "pesanan bulanan. Keempat aktor tersebut digambarkan pada Gambar 3.3.",
            ),
        ],
    )

    # Gambar use case dipindahkan ke subbab 3.7 (sebelumnya hanya ada di BAB II)
    erd_head = A("3.8 Entity Relationship Diagram (ERD) Sistem Pemesanan Menu")
    cap_tmpl = A("Gambar 3.3 Entity-Relationship Diagram (ERD)")
    D.insert_paras_after(
        erd_head - 1,
        [(cap_tmpl, "Gambar 3.3 Use Case Diagram Sistem Pemesanan Menu")],
        label="caption Gambar 3.3 Use Case Diagram",
    )
    D.drop_blanks_after(
        A("Admin memiliki use case login, mengelola menu"),
        label="rapikan ruang kosong pada subbab 3.7",
    )
    uc_caption = A("Gambar 3.3 Use Case Diagram Sistem Pemesanan Menu")
    uc_image_src = A("Gambar 2.1 Use Case Diagram Sistem Pemesanan Menu") - 1
    D.clone_para_before(uc_image_src, uc_caption,
                        label="salin gambar use case ke subbab 3.7")

    # ============================================== renumber gambar (3.3 -> 3.4 dst.)
    for old, new in [
        ("Gambar 3.3 Entity-Relationship Diagram (ERD)",
         "Gambar 3.4 Entity-Relationship Diagram (ERD)"),
        ("Gambar 3.4 Menu Awal Web", "Gambar 3.5 Menu Awal Web"),
        ("Gambar 3.5 Menu Add-Ons Sebelum Masuk ke Keranjang",
         "Gambar 3.6 Menu Add-Ons Sebelum Masuk ke Keranjang"),
        ("Gambar 3.6 Halaman Pembayaran Cart", "Gambar 3.7 Halaman Keranjang (Cart)"),
        ("Gambar 3.7 Halaman Pembayaran", "Gambar 3.8 Halaman Pembayaran"),
        ("Tabel 3.8 Context Diagram (DFD Level 0)",
         "Gambar 3.9 Context Diagram (DFD Level 0)"),
        ("Tabel 3.9 Rincian Proses pada DFD Level 1", "Gambar 3.10 DFD Level 1"),
        ("Tabel 3.10 DFD Level 2 untuk Proses 2.0 dan Proses 4.0",
         "Gambar 3.11 DFD Level 2 untuk Proses 2.0 dan Proses 4.0"),
    ]:
        idx = A(old)
        D.sub(idx, old, new, label=f"figure {old} -> {new}")

    # ================================================================= 3.8 ERD
    i = A("Entity-Relationship Diagram (ERD) berfungsi sebagai cetak biru logis")
    D.set_text(
        i,
        "Entity-Relationship Diagram (ERD) berfungsi sebagai cetak biru logis dari "
        "struktur basis data sistem pemesanan menu di Restoran Kekupu Villa Jembrana. "
        "Sesuai kebutuhan fungsional pada Tabel 3.2 sampai dengan Tabel 3.6, ERD sistem "
        "ini memuat sembilan tabel, yaitu roles, users, categories, items, addon_groups, "
        "addons, addon_group_item, orders, dan order_items. Diagram ini menggambarkan "
        "kardinalitas antar entitas, misalnya satu kategori memayungi banyak item menu "
        "(one-to-many), satu pesanan terdiri atas banyak baris item pesanan "
        "(one-to-many), serta satu item menu dapat memiliki banyak kelompok add-on dan "
        "sebaliknya (many-to-many melalui tabel penghubung addon_group_item).",
    )
    tmpl_body = i

    D.insert_paras_after(
        i,
        [
            (
                tmpl_body,
                "Meja pelanggan tidak dimodelkan sebagai entitas tersendiri. Identitas "
                "meja disimpan pada atribut table_number di tabel orders yang nilainya "
                "berasal dari parameter QR Code, sedangkan daftar QR Code untuk 12 meja "
                "dibangkitkan oleh halaman QR meja pada panel Admin. Dengan demikian "
                "seluruh entitas yang digambarkan pada ERD benar-benar terpakai pada "
                "implementasi dan tidak terdapat tabel inventori bahan baku di dalam "
                "rancangan basis data.",
            ),
            (
                tmpl_body,
                "Fitur add-on dijaga konsistensinya di seluruh rantai perancangan. "
                "Kelompok add-on beserta opsinya disimpan pada tabel addon_groups dan "
                "addons; keterkaitannya dengan item menu disimpan pada tabel penghubung "
                "addon_group_item; pilihan pelanggan divalidasi terhadap min_select dan "
                "max_select; harga add-on ikut diperhitungkan pada subtotal setiap baris "
                "pesanan; dan pilihan yang telah dikonfirmasi disimpan sebagai snapshot "
                "pada kolom JSON order_items.addons sehingga tetap terbaca pada layar "
                "dapur, nota, dan riwayat pesanan meskipun opsi add-on kemudian diubah "
                "oleh Admin. Rantai yang sama diuji pada skenario Black-Box Testing "
                "(Tabel 3.10) dan diukur pada indikator UAT (Tabel 3.12).",
            ),
            (
                tmpl_body,
                "Status pembayaran dan status dapur disimpan pada dua kolom terpisah di "
                "tabel orders. Kolom orders.status memuat status pembayaran, yaitu "
                "pending untuk pesanan yang belum lunas dan settlement untuk pesanan "
                "yang telah lunas; sedangkan kolom orders.kitchen_status memuat status "
                "pengolahan hidangan, yaitu waiting, processing, cooking, dan ready. "
                "Pemisahan ini memastikan progres dapur tidak pernah dipakai untuk "
                "menyimpulkan pelunasan pembayaran, dan sebaliknya.",
            ),
        ],
    )

    # ========================================================= 3.9 Rancangan Design
    i = A("Pada tahapan design, diperlukan draf rancangan antarmuka (mockup/wireframe)")
    D.sub(
        i,
        "Berikut merupakan rancangan antarmuka sistem yang dikembangkan, yang dapat "
        "dilihat pada Gambar 3.5 sampai dengan Gambar 3.3.",
        "Rancangan antarmuka pelanggan dapat dilihat pada Gambar 3.5 sampai dengan "
        "Gambar 3.8, yang berturut-turut menampilkan halaman menu beserta kategori dan "
        "penanda ketersediaan, jendela pemilihan add-on, halaman keranjang, dan halaman "
        "pembayaran. Rancangan halaman status/progres pesanan pelanggan serta rancangan "
        "antarmuka Koki, Kasir, dan Admin dijabarkan pada subbab 3.15 (Tabel 3.22 sampai "
        "dengan Tabel 3.25).",
    )

    # ================================================= 3.10 Black-Box Testing (34)
    i = A("Pengujian Black-Box Testing bertujuan untuk memastikan bahwa setiap fungsi")
    D.set_text(
        i,
        "Pengujian Black-Box Testing bertujuan memastikan bahwa setiap fungsi sistem "
        "berjalan sesuai kebutuhan fungsional yang telah dirumuskan pada Tabel 3.2 sampai "
        "dengan Tabel 3.6, tanpa menguji struktur kode program secara internal. Cakupan "
        "pengujian meliputi pemindaian QR Code meja, penyajian menu per kategori, "
        "ketersediaan/stok menu, pemilihan add-on, pengelolaan keranjang dan catatan "
        "pesanan, checkout, pembayaran tunai maupun non-tunai melalui Midtrans Snap "
        "beserta webhook-nya, pelacakan status pesanan oleh pelanggan, pengelolaan data "
        "master oleh Admin, antrean serta pemutakhiran status dapur oleh Koki, dan "
        "pemantauan pembayaran serta pencetakan nota oleh Kasir.",
    )

    i = A("Tabel 3.3 Intrumen Pengujian")
    D.set_text(i, "Tabel 3.8 Instrumen Pengujian")

    i = A("Skenario uji disusun berdasarkan seluruh kebutuhan fungsional pada Tabel 3.1")
    D.set_text(
        i,
        "Skenario uji disusun berdasarkan seluruh kebutuhan fungsional pada Tabel 3.2 "
        "sampai dengan Tabel 3.6, dikelompokkan menurut hak akses (role) pengguna. Total "
        "skenario uji yang direncanakan berjumlah 34 skenario, dengan rincian sebagai "
        "berikut:",
    )

    D.cell(TBL[4], 1, 2, "11")
    D.cell(TBL[4], 2, 2, "8")
    D.cell(TBL[4], 3, 2, "4")
    D.cell(TBL[4], 4, 2, "5")
    D.cell(TBL[4], 5, 2, "6")
    D.cell(TBL[4], 6, 2, "34")

    i = A("Tabel 3.4 Jumlah Skenario Uji")
    D.set_text(i, "Tabel 3.9 Jumlah Skenario Uji")

    i = A("Pelanggan (6): memindai QR Code meja")
    D.set_text(
        i,
        "Pelanggan (11): memindai QR Code meja, melihat daftar menu per kategori, "
        "melihat harga dan deskripsi menu, melihat ketersediaan/stok menu, memilih "
        "add-on, menambahkan menu ke keranjang, mengubah/menghapus item keranjang, "
        "mengisi catatan pesanan, checkout dengan metode tunai, pembayaran non-tunai "
        "melalui Midtrans Snap, dan melihat status/progres pesanan.",
    )

    i = A("Admin (6): login administrator")
    D.set_text(
        i,
        "Admin (8): login administrator, CRUD menu, mengelola ketersediaan/stok menu, "
        "mengelola kategori menu, mengelola add-on, mengelola data karyawan, mengelola "
        "role/hak akses, serta melihat riwayat pesanan dan laporan pesanan bulanan.",
    )

    i = A("Koki (4): login akun koki")
    D.set_text(
        i,
        "Koki (4): login akun koki, melihat antrean pesanan yang telah lunas, "
        "memperbarui status dapur, dan menerima indikator pesanan baru.",
    )

    i = A("Kasir (5): login akun kasir")
    D.set_text(
        i,
        "Kasir (5): login akun kasir, melihat daftar pesanan menunggu pembayaran, "
        "mengonfirmasi pembayaran tunai, memantau status pembayaran Midtrans tanpa "
        "konfirmasi manual, dan melihat/mencetak nota transaksi.",
    )

    i = A("Sistem / Midtrans (3): validasi sesi/token meja")
    D.set_text(
        i,
        "Sistem / Midtrans (6): membuat transaksi Snap (snap_token), menerima dan "
        "memverifikasi webhook notifikasi Midtrans, menuliskan status settlement serta "
        "meneruskan pesanan ke antrean dapur, validasi sesi/token meja, responsivitas "
        "tampilan pada perangkat berbeda, dan penanganan input tidak valid.",
    )

    bb_widths = [560, 950, 2150, 2150, 1320, 2600, 800]
    bb = [[
        "No", "Aktor", "Skenario Uji", "Prosedur Pengujian", "Data Masukan",
        "Hasil yang Diharapkan", "Kesimpulan",
    ]]
    scenarios = [
        ("Pelanggan", "Memindai QR Code meja",
         "Arahkan kamera smartphone ke QR Code pada meja, buka tautan yang muncul",
         "URL berparameter table_number",
         "Halaman menu tampil dan nomor meja tersimpan otomatis pada sesi pelanggan"),
        ("Pelanggan", "Melihat daftar menu per kategori",
         "Pilih salah satu tab kategori pada halaman menu", "Kategori menu",
         "Daftar item menu sesuai kategori yang dipilih ditampilkan"),
        ("Pelanggan", "Melihat harga dan deskripsi menu",
         "Buka detail salah satu item pada katalog menu", "Item menu terpilih",
         "Harga, deskripsi, dan gambar item ditampilkan sesuai data tabel items"),
        ("Pelanggan", "Melihat ketersediaan/stok menu",
         "Amati katalog setelah Admin menetapkan stok bernilai nol atau menonaktifkan "
         "item", "items.stock = 0 atau is_active = false",
         "Item ditandai tidak tersedia dan tidak dapat ditambahkan ke keranjang"),
        ("Pelanggan", "Memilih add-on pada item menu",
         "Buka jendela kustomisasi item, pilih opsi add-on, lalu simpan",
         "Opsi add-on terpilih",
         "Opsi tersimpan pada baris keranjang, harga add-on menambah subtotal, dan "
         "pemilihan di luar batas min_select/max_select ditolak"),
        ("Pelanggan", "Menambahkan menu ke keranjang",
         "Pilih item menu, tentukan jumlah, tekan tombol Tambah", "Item menu, jumlah",
         "Item tersimpan pada keranjang dan subtotal ter-update"),
        ("Pelanggan", "Mengubah/menghapus item keranjang",
         "Ubah kuantitas atau tekan ikon hapus pada item keranjang",
         "Jumlah baru atau aksi hapus",
         "Subtotal dan grand total ter-update otomatis"),
        ("Pelanggan", "Mengisi catatan pesanan",
         "Isi kolom catatan pada halaman checkout", "Teks catatan",
         "Catatan tersimpan pada kolom orders.note dan tampil pada layar dapur"),
        ("Pelanggan", "Checkout metode tunai",
         "Isi data diri, pilih metode Tunai, tekan Konfirmasi Pembayaran",
         "Nama, nomor telepon, metode tunai",
         "Pesanan tersimpan dengan orders.status = pending dan menunggu konfirmasi Kasir"),
        ("Pelanggan", "Pembayaran non-tunai melalui Midtrans Snap",
         "Pilih metode QRIS, selesaikan pembayaran pada jendela Snap",
         "Order terpilih, kanal pembayaran",
         "Sistem memperoleh snap_token, jendela Snap tampil, dan pesanan berstatus "
         "pending hingga notifikasi pelunasan diterima"),
        ("Pelanggan", "Melihat status/progres pesanan",
         "Buka halaman Pesanan Saya atau telusuri melalui kode pesanan",
         "order_code",
         "Status pembayaran (pending/settlement) dan status dapur "
         "(waiting/processing/cooking/ready) ditampilkan terpisah"),
        ("Admin", "Login administrator",
         "Isi form login dengan akun admin terdaftar", "Username/email, password",
         "Admin diarahkan ke dashboard admin"),
        ("Admin", "Menambah/mengubah/menghapus menu (CRUD)",
         "Buka menu Kelola Menu, isi/ubah/hapus data item",
         "Nama, harga, kategori, gambar",
         "Data pada tabel items tersimpan/terupdate/terhapus sesuai aksi"),
        ("Admin", "Mengelola ketersediaan/stok menu",
         "Ubah nilai stok atau status aktif pada form item",
         "items.stock, items.is_active",
         "Perubahan tersimpan dan katalog pelanggan menyesuaikan ketersediaannya"),
        ("Admin", "Mengelola kategori menu",
         "Tambah/ubah/hapus data pada menu Kelola Kategori",
         "Nama kategori, deskripsi",
         "Data kategori tersimpan dan tampil pada filter menu pelanggan"),
        ("Admin", "Mengelola add-on",
         "Tambah/ubah/hapus kelompok add-on dan opsinya, tautkan ke item menu",
         "Nama kelompok, tipe, min/max select, nama opsi, harga, stok",
         "Data addon_groups, addons, dan addon_group_item tersimpan serta muncul pada "
         "jendela kustomisasi pelanggan"),
        ("Admin", "Mengelola data karyawan",
         "Tambah/ubah/hapus akun karyawan (Koki/Kasir)", "Nama, username, role",
         "Data user tersimpan dan dapat digunakan untuk login sesuai role"),
        ("Admin", "Mengelola role/hak akses",
         "Tambah/ubah data role pada menu Kelola Role", "Nama role, deskripsi",
         "Data role tersimpan dan tersedia pada form penambahan karyawan"),
        ("Admin", "Melihat riwayat pesanan dan laporan bulanan",
         "Buka menu Pesanan, lalu unduh laporan rekapitulasi bulanan",
         "Periode bulan/tahun",
         "Seluruh pesanan ditampilkan lengkap dan berkas laporan bulanan berhasil "
         "diunduh"),
        ("Koki", "Login akun Koki", "Isi form login dengan akun Koki",
         "Username/email, password",
         "Koki diarahkan ke halaman antrean dapur sesuai hak aksesnya"),
        ("Koki", "Melihat antrean pesanan yang telah lunas",
         "Buka halaman dapur setelah terdapat pesanan berstatus settlement", "-",
         "Pesanan lunas tampil pada antrean beserta nomor meja, item, add-on, catatan, "
         "dan waktu masuk"),
        ("Koki", "Memperbarui status dapur",
         "Tekan tombol status Diproses, Sedang Dimasak, atau Siap Disajikan",
         "Status dapur baru",
         "Kolom orders.kitchen_status berubah dan perubahan terlihat pada halaman Kasir "
         "serta halaman status pelanggan"),
        ("Koki", "Menerima indikator pesanan baru",
         "Amati tampilan saat pesanan baru masuk ke antrean", "-",
         "Penanda visual pesanan baru muncul pada layar dapur"),
        ("Kasir", "Login akun Kasir", "Isi form login dengan akun Kasir",
         "Username/email, password",
         "Kasir diarahkan ke halaman daftar pesanan sesuai hak aksesnya"),
        ("Kasir", "Melihat pesanan menunggu pembayaran",
         "Buka halaman daftar pesanan", "-",
         "Daftar pesanan berstatus pending ditampilkan beserta metode pembayarannya"),
        ("Kasir", "Mengonfirmasi pembayaran tunai",
         "Pilih pesanan dengan payment_method = tunai, tekan Konfirmasi Pembayaran",
         "Order terpilih",
         "orders.status menjadi settlement dan kitchen_status menjadi processing"),
        ("Kasir", "Memantau status pembayaran Midtrans",
         "Buka pesanan dengan payment_method = qris", "Order terpilih",
         "Status pembayaran hanya ditampilkan untuk dipantau dan tombol konfirmasi "
         "manual tidak tersedia"),
        ("Kasir", "Melihat/mencetak nota transaksi",
         "Tekan tombol cetak/lihat nota pada pesanan yang telah lunas", "Order terpilih",
         "Rincian item, add-on, subtotal, pajak, dan total ditampilkan/tercetak"),
        ("Sistem / Midtrans", "Membuat transaksi Snap",
         "Kirim permintaan pembayaran non-tunai dari halaman checkout",
         "order_code, grand_total, rincian item",
         "Midtrans menerbitkan snap_token dan jendela pembayaran dapat ditampilkan"),
        ("Sistem / Midtrans", "Menerima dan memverifikasi webhook",
         "Kirim notifikasi pembayaran ke POST /midtrans/notification",
         "transaction_status, signature_key",
         "Notifikasi dengan signature_key valid diproses, sedangkan notifikasi dengan "
         "signature tidak valid ditolak"),
        ("Sistem / Midtrans", "Menuliskan settlement dan meneruskan ke dapur",
         "Kirim notifikasi berstatus settlement pada pesanan qris", "Order terpilih",
         "orders.status = settlement dan kitchen_status = processing; pesanan tampil di "
         "dapur tanpa tombol konfirmasi Kasir"),
        ("Sistem / Midtrans", "Validasi sesi/token meja",
         "Buka dua tab berbeda menggunakan QR meja yang berbeda",
         "Token meja A, token meja B",
         "Setiap sesi tetap terpisah dan keranjang tidak tertukar antar meja"),
        ("Sistem / Midtrans", "Responsivitas tampilan pada perangkat berbeda",
         "Akses sistem melalui smartphone, tablet, dan desktop", "-",
         "Tata letak menyesuaikan (responsive) tanpa elemen terpotong"),
        ("Sistem / Midtrans", "Penanganan input tidak valid",
         "Kirim form dengan field wajib kosong atau format salah",
         "Data kosong/format salah",
         "Sistem menampilkan pesan validasi dan data tidak tersimpan"),
    ]
    for n, (aktor, skenario, prosedur, masukan, harapan) in enumerate(scenarios, 1):
        bb.append([str(n), aktor, skenario, prosedur, masukan, harapan, "Valid"])

    D.replace_table(TBL[5], bb_widths, bb, label="black-box 34 skenario")
    D.drop_table(TBL[6], label="drop tabel lanjutan black-box lama")

    i = A("Tabel 3.5 Instrumen Pengujian Black-Box Testing (24 Skenario)")
    D.set_text(i, "Tabel 3.10 Instrumen Pengujian Black-Box Testing (34 Skenario)")

    # ==================================================================== 3.11 DFD
    i = A("DFD dirancang secara hierarkis dalam notasi Gane & Sarson")
    D.set_text(
        i,
        "DFD dirancang secara hierarkis dalam notasi Gane & Sarson dan digambarkan pada "
        "Gambar 3.9 sampai dengan Gambar 3.11. Context Diagram menempatkan Midtrans "
        "sebagai entitas eksternal kelima agar aliran webhook tidak disamakan dengan "
        "masukan Kasir. DFD Level 1 memecah Proses 0 menjadi enam proses, sedangkan DFD "
        "Level 2 memecah Proses 2.0 dan Proses 4.0 untuk menunjukkan cabang non-tunai "
        "(Snap dan webhook) versus cabang tunai (konfirmasi Kasir). Entitas Midtrans "
        "tidak menggantikan Kasir; keduanya melayani kanal pembayaran yang berbeda.",
    )
    tmpl_body = i
    D.insert_paras_after(
        i,
        [
            (
                tmpl_body,
                "Alur pembayaran digambarkan dalam dua cabang yang terpisah. Cabang "
                "non-tunai mengalir dari Pelanggan menuju jendela Snap, diteruskan ke "
                "Midtrans, dikembalikan ke sistem melalui webhook, dituliskan sebagai "
                "status settlement, lalu diteruskan ke antrean dapur. Cabang tunai "
                "mengalir dari Pelanggan menuju sistem, diteruskan kepada Kasir untuk "
                "dikonfirmasi, dituliskan sebagai status settlement, kemudian diteruskan "
                "ke antrean dapur. Pada cabang non-tunai, Kasir tidak digambarkan sebagai "
                "pihak yang mengonfirmasi pembayaran; Kasir hanya menerima aliran data "
                "status pembayaran untuk keperluan pemantauan dan pencetakan nota.",
            )
        ],
    )

    i = A("satu proses tunggal (Proses 0) yang berinteraksi dengan empat entitas eksternal")
    D.set_text(
        i,
        "Context Diagram menggambarkan satu proses tunggal (Proses 0) yang berinteraksi "
        "dengan lima entitas eksternal, yaitu Pelanggan, Koki, Kasir, Admin/Owner, dan "
        "Midtrans. Rincian aliran data masuk dan keluar pada setiap entitas dijabarkan "
        "pada gambar berikut.",
    )

    i = A("Mengingat kompleksitasnya, Proses 2.0 (Kelola Pesanan) dapat didekomposisi")
    D.sub(
        i,
        "Diagram disusun menggunakan Draw.io/pemodelan terstruktur dan telah digambarkan "
        "dalam notasi Gane & Sarson pada Gambar 3.8 sampai dengan Gambar 3.10.",
        "Diagram disusun menggunakan Draw.io/pemodelan terstruktur dan digambarkan dalam "
        "notasi Gane & Sarson pada Gambar 3.9 sampai dengan Gambar 3.11.",
    )

    i = A("Proses 0 pada Context Diagram didekomposisi menjadi enam proses utama")
    D.sub(i, "data store (D1–D5) yang merepresentasikan tabel pada ERD (Gambar 2.2/3.3).",
          "data store (D1–D5) yang merepresentasikan tabel pada ERD (Gambar 3.4).")

    i = A("B. DFD Level 2")
    D.sub(i, "B. DFD Level 2", "C. DFD Level 2")

    # ==================================================================== 3.12 UAT
    i = A("Indikator kuesioner disusun mengacu pada aspek penerimaan sistem")
    D.set_text(
        i,
        "Instrumen UAT terdiri atas dua bagian. Bagian pertama adalah butir inti yang "
        "diisi oleh seluruh responden dan mengacu pada aspek penerimaan sistem yang "
        "relevan dengan kebutuhan non-fungsional pada Tabel 3.7, sebagaimana dirinci "
        "pada Tabel 3.11. Bagian kedua adalah butir spesifik per aktor yang hanya diisi "
        "oleh responden pemilik peran tersebut, sehingga setiap responden hanya menilai "
        "fitur yang benar-benar digunakannya, sebagaimana dirinci pada Tabel 3.12.",
    )

    i = A("Tabel 3.8 Indikator Penilaian UAT")
    D.set_text(i, "Tabel 3.11 Indikator Penilaian UAT (Butir Inti)")
    cap_tmpl = i
    tmpl_body = A("Instrumen UAT terdiri atas dua bagian")

    per_actor = [
        ["Aktor", "Indikator Spesifik yang Diukur", "Jumlah Butir"],
        ["Pelanggan",
         "Kemudahan memindai QR Code meja; kemudahan melihat daftar menu beserta "
         "ketersediaannya; kemudahan memilih menu dan add-on; kemudahan proses checkout; "
         "kemudahan melakukan pembayaran tunai maupun non-tunai; kemudahan melihat "
         "status pesanan", "6"],
        ["Koki",
         "Kemudahan melihat antrean pesanan; kejelasan informasi pesanan (nomor meja, "
         "item, add-on, catatan, dan waktu masuk); kemudahan memutakhirkan status dapur",
         "3"],
        ["Kasir",
         "Kemudahan melihat daftar pembayaran; kemudahan mengonfirmasi pembayaran tunai; "
         "kemudahan memantau status pembayaran Midtrans; kemudahan mencetak nota "
         "transaksi", "4"],
        ["Admin/Owner",
         "Kemudahan mengelola menu; kategori; ketersediaan/stok menu; add-on; data "
         "karyawan; role/hak akses; serta peninjauan riwayat pesanan dan laporan bulanan",
         "7"],
    ]
    D.insert_paras_after(
        A("Tabel 3.11 Indikator Penilaian UAT (Butir Inti)"),
        [
            (tmpl_body,
             "Butir spesifik per aktor disusun langsung dari kebutuhan fungsional pada "
             "Tabel 3.2 sampai dengan Tabel 3.6, sehingga indikator UAT hanya mengukur "
             "fitur yang tersedia bagi masing-masing peran."),
            (cap_tmpl, "Tabel 3.12 Indikator UAT Spesifik per Aktor"),
        ],
    )
    D.insert_table_after_para(
        A("Butir spesifik per aktor disusun langsung dari kebutuhan fungsional"),
        TBL[7], [1500, 5640, 1800], per_actor, label="Tabel 3.12 indikator per aktor",
    )

    i = A("Responden UAT berjumlah 18 orang dan hanya muncul pada subbab pengujian")
    D.set_text(
        i,
        "Responden UAT berjumlah 18 orang dan hanya muncul pada subbab pengujian "
        "penerimaan, bukan pada subbab observasi:",
    )

    i = A("Kelompok internal (6 orang): seluruh informan wawancara")
    D.set_text(
        i,
        "Kelompok internal (6 orang): seluruh informan wawancara, yaitu 1 owner (menguji "
        "peran Admin), 2 koki (menguji peran Koki), 1 kasir (menguji peran Kasir), dan 2 "
        "pramusaji. Pramusaji tidak memiliki akun sistem sehingga hanya mengisi butir "
        "inti sebagai pengguna pendukung penyajian, sedangkan owner, koki, dan kasir "
        "mengisi butir inti beserta butir spesifik perannya pada perangkat kerja "
        "restoran.",
    )

    i = A("Kelompok pelanggan (12 orang): satu tamu per meja")
    D.set_text(
        i,
        "Kelompok pelanggan (12 orang): satu tamu per meja, merepresentasikan 12 QR Code "
        "meja, dengan kriteria memiliki smartphone dan mampu mengoperasikan peramban "
        "web. Kelompok ini mengisi butir inti beserta butir spesifik Pelanggan.",
    )

    i = A("Tabel 3.9 Skala Penilaian")
    D.set_text(i, "Tabel 3.13 Skala Penilaian")

    i = A("Skor Ideal (Skor Maksimal) = Skor tertinggi × Jumlah responden × Jumlah butir")
    D.set_text(
        i,
        "Skor Ideal (Skor Maksimal) = Skor tertinggi × Jumlah butir yang diisi seluruh "
        "responden",
    )

    i = A("Sebagai ilustrasi, dengan 18 responden dan 12 butir pernyataan berskala 1–5")
    D.set_text(
        i,
        "Karena jumlah butir yang diisi berbeda antar kelompok responden, skor ideal "
        "dihitung per kelompok kemudian dijumlahkan, sebagaimana ditunjukkan pada Tabel "
        "3.14. Sebagai ilustrasi, apabila total skor yang terkumpul dari seluruh "
        "responden adalah 1.270 dari skor ideal 1.525, maka persentase kelayakan = "
        "(1.270 ÷ 1.525) × 100% = 83,3%, yang termasuk kategori Sangat Layak.",
    )
    tmpl_body = i

    skor = [
        ["Kelompok Responden", "Jumlah Responden", "Butir Inti", "Butir Spesifik",
         "Butir per Responden", "Total Butir", "Skor Ideal"],
        ["Pelanggan", "12", "12", "6", "18", "216", "1.080"],
        ["Koki", "2", "12", "3", "15", "30", "150"],
        ["Kasir", "1", "12", "4", "16", "16", "80"],
        ["Admin/Owner", "1", "12", "7", "19", "19", "95"],
        ["Pramusaji (pendukung, tanpa akun sistem)", "2", "12", "–", "12", "24", "120"],
        ["Total", "18", "–", "–", "–", "305", "1.525"],
    ]
    D.insert_paras_after(
        A("Karena jumlah butir yang diisi berbeda antar kelompok responden"),
        [(cap_tmpl, "Tabel 3.14 Perhitungan Skor Ideal per Kelompok Responden")],
    )
    D.insert_table_after_para(
        A("Karena jumlah butir yang diisi berbeda antar kelompok responden"),
        TBL[7], [2450, 1150, 900, 1050, 1240, 1050, 1100], skor,
        label="Tabel 3.14 skor ideal",
    )

    i = A("Tabel 3.10 Kategori Hasil")
    D.set_text(i, "Tabel 3.15 Kategori Hasil")

    i = A("Hasil UAT mencapai persentase kelayakan minimal 61%")
    D.sub(i, "berdasarkan Tabel kategori pada poin (g).", "berdasarkan Tabel 3.15.")

    i = A("Apabila persentase UAT berada di bawah 61%")
    D.sub(i, "sebagaimana dijelaskan pada subbab 2.15 dan 3.5.",
          "sebagaimana dijelaskan pada subbab 2.14 dan 3.5.")

    # ====================================================== 3.13 Deskripsi Use Case
    i = A("Berikut deskripsi naratif dari setiap use case yang digambarkan pada Gambar 2.1")
    D.set_text(
        i,
        "Berikut deskripsi naratif dari setiap use case yang digambarkan pada Gambar "
        "3.3, memuat aktor, deskripsi singkat, alur utama (main flow), dan kondisi akhir "
        "(post-condition). Deskripsi disusun mengikuti kode kebutuhan fungsional pada "
        "Tabel 3.2 sampai dengan Tabel 3.6.",
    )

    uc = [["Use Case", "Aktor", "Deskripsi", "Alur Utama (Main Flow)", "Kondisi Akhir"]]
    uc += [
        ["Memindai QR Code Meja", "Pelanggan",
         "Pelanggan memperoleh akses menu digital beserta identitas mejanya tanpa login.",
         "1) Pelanggan memindai QR Code pada meja.\n"
         "2) Peramban membuka rute /meja/{table_number}.\n"
         "3) Sistem menyimpan nomor meja pada sesi pelanggan.",
         "Halaman menu terbuka dengan nomor meja terisi otomatis."],
        ["Melihat Menu dan Ketersediaan", "Pelanggan",
         "Pelanggan menelusuri katalog menu per kategori beserta status ketersediaannya.",
         "1) Pelanggan memilih tab kategori.\n"
         "2) Sistem menampilkan item aktif dengan stok lebih dari nol.\n"
         "3) Item yang habis ditandai tidak tersedia.",
         "Pelanggan mengetahui menu yang benar-benar dapat dipesan."],
        ["Memilih Add-on", "Pelanggan",
         "Pelanggan menyesuaikan item menu melalui kelompok add-on yang tersedia.",
         "1) Pelanggan membuka jendela kustomisasi item.\n"
         "2) Sistem menampilkan kelompok add-on beserta batas min_select dan max_select.\n"
         "3) Pelanggan memilih opsi dan sistem memvalidasi jumlah pilihan.",
         "Pilihan add-on tersimpan dan harganya menambah subtotal baris."],
        ["Mengelola Keranjang", "Pelanggan",
         "Pelanggan menambah, mengubah, dan menghapus item pada keranjang berbasis sesi.",
         "1) Pelanggan menambahkan item ke keranjang.\n"
         "2) Pelanggan mengubah kuantitas atau menghapus baris.\n"
         "3) Sistem menghitung ulang subtotal.",
         "Keranjang mencerminkan pesanan terakhir pelanggan."],
        ["Melakukan Checkout", "Pelanggan",
         "Pelanggan mengirim pesanan beserta catatan dan memilih metode pembayaran.",
         "1) Pelanggan mengisi identitas dan catatan pesanan.\n"
         "2) Pelanggan memilih metode tunai atau QRIS.\n"
         "3) Sistem membentuk orders dan order_items, menghitung pajak 10% dan "
         "grand_total, serta mengurangi stok.",
         "Pesanan tersimpan dengan status pending dan kode pesanan terbit."],
        ["Membayar Pesanan Non-Tunai (Midtrans Snap)", "Pelanggan, Midtrans",
         "Pelanggan menyelesaikan pelunasan cashless pada jendela Snap. Sistem menerima "
         "settlement secara otomatis.",
         "1) Pelanggan memilih metode QRIS/e-wallet/transfer pada checkout.\n"
         "2) Sistem meminta snap_token ke Midtrans.\n"
         "3) Pelanggan membayar pada jendela Snap.\n"
         "4) Midtrans mengirim webhook dan sistem memverifikasi signature_key.\n"
         "5) Sistem menulis status settlement dan meneruskan pesanan ke dapur.",
         "Pesanan lunas tanpa tombol konfirmasi Kasir; dapur menerima antrean."],
        ["Melihat Status Pesanan", "Pelanggan",
         "Pelanggan memantau status pembayaran dan progres pengolahan pesanannya.",
         "1) Pelanggan membuka halaman pesanan atau memasukkan order_code.\n"
         "2) Sistem menampilkan orders.status dan orders.kitchen_status.",
         "Pelanggan mengetahui pesanannya lunas dan sedang diproses/siap disajikan."],
        ["Melihat Antrean Dapur", "Koki",
         "Koki menerima daftar pesanan lunas yang harus diolah.",
         "1) Koki login dengan akun berrole chef.\n"
         "2) Sistem menampilkan pesanan berstatus settlement beserta nomor meja, item, "
         "add-on, catatan, dan waktu masuk.\n"
         "3) Pesanan baru ditandai secara visual.",
         "Koki memperoleh instruksi pengolahan tanpa nota kertas."],
        ["Memutakhirkan Status Dapur", "Koki",
         "Koki memperbarui progres pengolahan hidangan.",
         "1) Koki memilih kartu pesanan.\n"
         "2) Koki menekan tombol Diproses, Sedang Dimasak, atau Siap Disajikan.\n"
         "3) Sistem menulis orders.kitchen_status.",
         "Progres dapur terlihat oleh Kasir dan pelanggan."],
        ["Mengonfirmasi Pembayaran Tunai", "Kasir",
         "Kasir menyatakan uang fisik telah diterima. Use case ini tidak dipakai untuk "
         "QRIS/Midtrans.",
         "1) Kasir membuka daftar pesanan payment_method = tunai dan status pending.\n"
         "2) Kasir mencocokkan grand_total dengan uang yang diterima.\n"
         "3) Kasir menekan Konfirmasi Pembayaran.\n"
         "4) Sistem menulis settlement dan kitchen_status processing.",
         "Pesanan tunai berstatus lunas dan masuk antrean dapur."],
        ["Memantau Status Pembayaran", "Kasir, Admin",
         "Kasir meninjau status yang sudah ditulis sistem (settlement dari webhook atau "
         "pending untuk tunai).",
         "1) Kasir membuka daftar pesanan.\n"
         "2) Sistem menampilkan metode bayar dan status pembayaran.\n"
         "3) Untuk QRIS, Kasir hanya memantau dan tidak menekan konfirmasi.",
         "Kasir memperoleh informasi pelunasan yang akurat."],
        ["Mencetak Nota Transaksi", "Kasir",
         "Kasir menampilkan/mencetak rincian pesanan yang telah lunas.",
         "1) Kasir memilih pesanan berstatus settlement.\n"
         "2) Sistem menampilkan item, add-on, pajak, dan total.\n"
         "3) Nota dicetak atau ditampilkan.",
         "Bukti transaksi tersedia bagi pelanggan."],
        ["Mengelola Menu dan Ketersediaan", "Admin",
         "Admin mengelola katalog menu beserta stok dan status aktifnya.",
         "1) Admin membuka Kelola Menu.\n"
         "2) Admin menambah, mengubah, atau menghapus item.\n"
         "3) Admin memutakhirkan items.stock dan items.is_active.",
         "Katalog pelanggan menampilkan menu yang tersedia saja."],
        ["Mengelola Kategori", "Admin",
         "Admin menyusun taksonomi menu yang dipakai sebagai filter katalog.",
         "1) Admin membuka Kelola Kategori.\n"
         "2) Admin menambah, mengubah, atau menghapus kategori.",
         "Filter kategori pada halaman pelanggan mengikuti data terbaru."],
        ["Mengelola Add-on", "Admin",
         "Admin merancang kelompok add-on beserta opsi, harga, batas pilihan, dan stok.",
         "1) Admin membuka Kelola Add-on.\n"
         "2) Admin menambah kelompok add-on dan menautkannya ke item menu.\n"
         "3) Admin menambah opsi beserta harga dan stoknya.",
         "Opsi kustomisasi tersedia pada jendela pemesanan pelanggan."],
        ["Mengelola Karyawan dan Role", "Admin",
         "Admin mengelola akun staf beserta hak aksesnya.",
         "1) Admin membuka Kelola Karyawan atau Kelola Role.\n"
         "2) Admin menambah/mengubah akun dan menetapkan role.\n"
         "3) Sistem menyimpan data pada tabel users dan roles.",
         "Setiap staf hanya dapat mengakses fungsi sesuai perannya."],
        ["Melihat Riwayat Pesanan dan Laporan", "Admin, Kasir",
         "Admin dan Kasir meninjau rekapitulasi transaksi.",
         "1) Pengguna membuka halaman Pesanan.\n"
         "2) Sistem menampilkan seluruh pesanan beserta status dan totalnya.\n"
         "3) Pengguna mengunduh laporan rekapitulasi pesanan bulanan.",
         "Rekapitulasi transaksi tersedia sebagai dasar keputusan operasional."],
    ]
    D.replace_table(TBL[10], [1900, 1150, 2100, 4300, 1320], uc,
                    label="Tabel 3.16 deskripsi use case (17 use case)")

    i = A("Tabel 3.11 Deskripsi Use Case")
    D.set_text(i, "Tabel 3.16 Deskripsi Use Case")

    # ================================================ 3.14 Struktur Tabel Basis Data
    i = A("Struktur tabel berikut merupakan penjabaran teknis dari ERD pada Gambar 2.2/3.3")
    D.set_text(
        i,
        "Struktur tabel berikut merupakan penjabaran teknis dari ERD pada Gambar 3.4, "
        "memuat nama field, tipe data, serta keterangan (constraint) masing-masing tabel "
        "menurut kewenangan setiap peran.",
    )

    D.add_rows(TBL[11], [
        ["32", "addon_groups.is_active", "TINYINT(1)",
         "Admin mengaktifkan atau menonaktifkan kelompok add-on pada antarmuka "
         "pelanggan."],
        ["33", "addons.is_active", "TINYINT(1)",
         "Admin mengatur ketersediaan setiap opsi add-on."],
        ["34", "addon_group_item.item_id", "BIGINT UNSIGNED",
         "Admin menautkan kelompok add-on tertentu kepada item menu yang relevan."],
        ["35", "orders.table_number", "INT",
         "Admin meninjau nomor meja asal pesanan yang berasal dari parameter QR Code."],
        ["36", "orders.note", "TEXT",
         "Admin meninjau catatan pelanggan pada riwayat pesanan."],
    ], label="tambah baris hak akses Admin")

    i = A("Tabel 3.12 Tabel Hak Akses Peran (Admin)")
    D.set_text(i, "Tabel 3.17 Tabel Hak Akses Peran (Admin)")

    i = A("Tabel 3.13 Tabel Hak Akses Peran (Kasir)")
    D.set_text(i, "Tabel 3.18 Tabel Hak Akses Peran (Kasir)")

    D.cell(
        TBL[12], 10, 3,
        "Kasir berwenang mengubah status pembayaran dari pending menjadi settlement "
        "hanya untuk pesanan bermetode tunai; status pesanan QRIS ditulis sistem melalui "
        "webhook Midtrans.",
    )
    D.cell(
        TBL[12], 13, 3,
        "Kasir membedakan transaksi tunai yang memerlukan konfirmasi manual dari "
        "transaksi QRIS yang hanya dipantau tanpa tombol konfirmasi.",
    )

    i = A("Tabel 3.14 Tabel Hak Akses Peran (Koki)")
    D.set_text(i, "Tabel 3.19 Tabel Hak Akses Peran (Koki)")

    i = A("C. Tabel Hak Akses Peran (Pelanggan)")
    D.set_text(i, "D. Tabel Hak Akses Peran (Pelanggan)")

    i = A("Tabel 3.15 Tabel Hak Akses Peran (Koki)")
    D.set_text(i, "Tabel 3.20 Tabel Hak Akses Peran (Pelanggan)")

    D.cell(TBL[14], 20, 2, "VARCHAR(32)")

    # Relasi antar tabel
    i = A("Relasi antar tabel pada basis data sistem ini diimplementasikan melalui foreign key")
    D.set_text(
        i,
        "Relasi antar tabel pada basis data sistem ini diimplementasikan melalui foreign "
        "key constraint sebagai berikut, sesuai kardinalitas pada ERD (Gambar 3.4). Meja "
        "pelanggan tidak berbentuk tabel tersendiri sehingga tidak memiliki relasi; "
        "identitas meja tersimpan sebagai atribut orders.table_number.",
    )

    D.cell(
        TBL[15], 3, 4,
        "Satu akun pengguna dapat memiliki banyak pesanan; akun pelanggan dibentuk "
        "otomatis pada saat checkout berdasarkan nomor telepon dan berrole customer.",
    )
    D.add_rows(TBL[15], [
        ["categories", "addon_groups", "One-to-Many",
         "addon_groups.category_id → categories.id",
         "Satu kategori dapat memayungi banyak kelompok add-on"],
        ["addon_groups", "addons", "One-to-Many",
         "addons.addon_group_id → addon_groups.id",
         "Satu kelompok add-on dapat memiliki banyak opsi add-on"],
        ["items ↔ addon_groups", "addon_group_item", "Many-to-Many",
         "addon_group_item.item_id → items.id dan addon_group_item.addon_group_id → "
         "addon_groups.id",
         "Satu item menu dapat memiliki banyak kelompok add-on dan sebaliknya"],
    ], label="tambah relasi add-on")

    i = A("Tabel 3.16 Relasi antar tabel")
    D.set_text(i, "Tabel 3.21 Relasi antar tabel")

    # =================================================== 3.15 Rancangan Antarmuka
    i = A("Rancangan antarmuka pelanggan (halaman menu, keranjang, dan pembayaran)")
    D.set_text(
        i,
        "Rancangan antarmuka pelanggan (halaman menu, add-on, keranjang, dan pembayaran) "
        "telah ditampilkan pada Gambar 3.5 sampai dengan Gambar 3.8. Berikut dilengkapi "
        "rancangan antarmuka untuk peran Admin, Koki, Kasir, dan Pelanggan termasuk "
        "halaman status pesanan, yang selanjutnya digambarkan sebagai wireframe "
        "(mockup) menggunakan Figma/Canva sebelum diimplementasikan.",
    )

    # UI Admin
    D.cell(TBL[16], 1, 1,
           "Menu Kelola Menu, Kelola Kategori, Kelola Add-on, Kelola Karyawan, Kelola "
           "Role, Lihat Pesanan, Laporan Bulanan, dan QR Meja")
    D.cell(TBL[16], 3, 1,
           "Daftar item menu dengan aksi Tambah/Ubah/Hapus, kolom stok, serta pengalih "
           "status aktif/nonaktif")
    D.cell(TBL[16], 5, 1,
           "Form input nama, harga, kategori, gambar, stok, dan status aktif item; "
           "termasuk form kelompok add-on beserta opsi, harga, batas pilihan, dan stok")
    D.add_rows(TBL[16], [
        ["Halaman Kelola Add-on",
         "Daftar kelompok add-on beserta tipe, batas min/max, item menu yang ditautkan, "
         "dan daftar opsi beserta harga dan stoknya"],
        ["Halaman Laporan Bulanan",
         "Pemilih periode bulan/tahun dan tombol unduh rekapitulasi pesanan"],
        ["Halaman QR Meja",
         "Kumpulan QR Code untuk 12 meja yang dapat dicetak, masing-masing mengarah ke "
         "rute /meja/{table_number}"],
    ], label="tambah komponen UI Admin")

    i = A("Tabel 3.17 Rancangan UI Admin (Dashboard)")
    D.set_text(i, "Tabel 3.22 Rancangan UI Admin (Dashboard)")

    # UI Koki
    D.cell(TBL[17], 2, 1,
           "Kartu pesanan berisi nomor meja, kode pesanan, daftar item beserta add-on "
           "terpilih, catatan pelanggan, dan waktu masuk pesanan")
    D.cell(TBL[17], 3, 1,
           "Tombol Diproses, Sedang Dimasak, dan Siap Disajikan pada setiap kartu "
           "pesanan sesuai nilai kolom orders.kitchen_status")
    D.add_rows(TBL[17], [
        ["Penyaring antrean",
         "Hanya menampilkan pesanan yang telah lunas (orders.status = settlement) dan "
         "belum berstatus siap disajikan"],
    ], label="tambah komponen UI Koki")

    i = A("Tabel 3.17 Rancangan UI Koki (Kitchen Display System sederhana)")
    D.set_text(i, "Tabel 3.23 Rancangan UI Koki (Kitchen Display System sederhana)")

    i = A("Tabel 3.18 Rancangan UI Kasir")
    D.set_text(i, "Tabel 3.24 Rancangan UI Kasir")

    D.add_rows(TBL[18], [
        ["Laporan bulanan",
         "Pemilih periode dan tombol unduh rekapitulasi pesanan bulanan"],
    ], label="tambah komponen UI Kasir")

    # UI Pelanggan
    D.cell(TBL[19], 3, 1,
           "Gambar, nama, deskripsi singkat, harga, serta tombol tambah/stepper jumlah; "
           "item dengan is_active = false atau stock = 0 ditandai \"Stok habis\" dan "
           "dinonaktifkan")
    D.add_rows(TBL[19], [
        ["Jendela pemilihan add-on",
         "Kelompok add-on beserta opsinya, penanda kelompok wajib, batas jumlah pilihan "
         "(min_select/max_select), dan penyesuaian harga yang langsung terlihat"],
        ["Halaman status/progres pesanan",
         "Kode pesanan, nomor meja, status pembayaran (pending/settlement), dan progres "
         "dapur (waiting/processing/cooking/ready) yang ditampilkan sebagai linimasa"],
    ], label="tambah komponen UI Pelanggan")

    i = A("Tabel 3.19 Rancangan UI Pelanggan")
    D.set_text(i, "Tabel 3.25 Rancangan UI Pelanggan")

    # ==================================================== 3.16 Tahapan Waktu Penelitian
    i = A("Tahapan waktu penelitian disusun secara sistematis mengikuti urutan Model Waterfall")
    D.sub(i, "sebagaimana dijelaskan pada subbab 3.5.3",
          "sebagaimana dijelaskan pada subbab 3.10 dan 3.12")
    D.sub(i, "Rincian jadwal pelaksanaan penelitian ditampilkan pada Tabel 3.8.",
          "Rincian jadwal pelaksanaan penelitian ditampilkan pada Tabel 3.26.")

    i = A("Tabel 3.20 Jadwal Pelaksanaan Penelitian")
    D.set_text(i, "Tabel 3.26 Jadwal Pelaksanaan Penelitian")

    i = A("Sistem (Use Case Diagram, ERD, dan rancangan antarmuka pada Gambar 3.4–3.6)")
    D.sub(i, "rancangan antarmuka pada Gambar 3.4–3.6", "rancangan antarmuka pada Gambar 3.5–3.8")
    D.sub(i, "hasil Black-Box Testing dan UAT (subbab 3.5.3)",
          "hasil Black-Box Testing dan UAT (subbab 3.10 dan 3.12)")
