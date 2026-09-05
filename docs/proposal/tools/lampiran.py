"""Lampiran A: catatan revisi digabungkan ke dalam berkas proposal."""


def apply(D, TBL):
    A = D.find_para

    title = A("METODE PENELITIAN")          # judul bab, rata tengah
    head = A("2.9 Hosting")                 # subjudul, tebal
    body = A("Layanan hosting diperlukan agar tautan yang dituju oleh QR Code")
    flat = A("Secara akademik, penelitian ini bermanfaat")   # paragraf tanpa indentasi
    cap = A("Tabel 3.1 Analisis Kebutuhan Fungsional (Kondisi Saat Ini")

    P = lambda t: D.append_para(body, t)
    F = lambda t: D.append_para(flat, t)
    H = lambda t: D.append_para(head, t)
    C = lambda t: D.append_para(cap, t)
    T = lambda w, r: D.append_table(TBL[4], w, r)

    D.append_para(title, "LAMPIRAN A", page_break=True,
                  label="mulai Lampiran A")
    D.append_para(title, "CATATAN REVISI PROPOSAL — 5 SEPTEMBER 2026")
    P("Lampiran ini merekam tindak lanjut atas catatan revisi pembimbing tanggal 5 "
      "September 2026 beserta lokasi perubahannya pada naskah. Seluruh revisi "
      "diselaraskan dengan implementasi nyata sistem pada repositori pengembangan "
      "(restoranku, Laravel 12), sehingga setiap klaim fitur, nama tabel, nama kolom, "
      "dan nilai status yang tertulis pada proposal telah dicocokkan dengan migration, "
      "model, rute, dan controller yang benar-benar tersedia.")

    # ------------------------------------------------------------------ A.1
    H("A.1 Acuan Implementasi yang Dipakai")
    P("Fakta berikut diambil langsung dari kode program dan dijadikan dasar penulisan "
      "ulang naskah:")
    T([2600, 6610], [
        ["Aspek", "Kondisi pada Implementasi"],
        ["Tabel basis data",
         "roles, users, categories, items, addon_groups, addons, addon_group_item, "
         "orders, order_items"],
        ["Role pengguna", "admin, chef (Koki), cashier (Kasir), customer"],
        ["Status pembayaran", "orders.status bernilai pending dan settlement"],
        ["Status dapur",
         "orders.kitchen_status bernilai waiting, processing, cooking, dan ready"],
        ["Metode pembayaran", "orders.payment_method bernilai tunai dan qris"],
        ["Ketersediaan/stok",
         "items.stock dan items.is_active, addons.stock dan addons.is_active"],
        ["Penyimpanan add-on", "Snapshot JSON pada kolom order_items.addons"],
        ["Pajak", "10% dihitung pada saat pembentukan pesanan"],
        ["Meja",
         "Bukan tabel tersendiri; disimpan sebagai orders.table_number dan QR Code "
         "dibangkitkan untuk 12 meja"],
        ["Akses pelanggan",
         "Tanpa login, melalui sesi meja dari rute GET /meja/{table_number}"],
        ["Login staf",
         "Hanya akun berrole admin, chef, dan cashier yang dapat masuk panel staf"],
        ["Nota transaksi", "Rute GET /orders/{order}/nota"],
        ["Laporan bulanan", "Rute GET /orders/laporan-excel (Admin dan Kasir)"],
        ["Inventori bahan baku",
         "Tidak tersedia; tidak terdapat tabel maupun proses inventori bahan baku"],
    ])
    C("Tabel A.1 Acuan Implementasi Sistem")

    # ------------------------------------------------------------------ A.2
    H("A.2 Pemenuhan Checklist Final Pembimbing")
    P("Seluruh butir checklist final pada catatan revisi telah ditindaklanjuti dengan "
      "lokasi perubahan sebagai berikut:")
    T([440, 2870, 1150, 4750], [
        ["No", "Butir Checklist", "Status", "Lokasi pada Naskah Revisi"],
        ["1", "BAB I memakai istilah fitur yang sama dengan BAB III", "Selesai",
         "Paragraf akhir subbab 1.1 memuat delapan fungsi sistem sebagai acuan tunggal, "
         "dirujuk ulang pada 1.4, 1.5, 3.5.1, 3.10, dan 3.12"],
        ["2", "Tidak ada lagi istilah stok bahan baku", "Selesai",
         "Seluruh istilah diganti menjadi ketersediaan/stok menu dan add-on; istilah "
         "bahan baku hanya tersisa pada kalimat penyangkalan di 1.1, 1.3, 3.2, dan 3.8"],
        ["3", "Aktor konsisten: Pelanggan, Koki, Kasir, Admin", "Selesai",
         "Subbab 1.3, 2.12, 3.6, 3.7, 3.11, dan 3.14"],
        ["4", "Tidak ada lagi aktor Staf Pelayan", "Selesai",
         "Subbab 1.3 dan 3.7 menyatakan secara eksplisit aktor tersebut dihapus beserta "
         "alasannya"],
        ["5", "QR Code konsisten di BAB I, Requirement, Use Case, DFD, UI, dan Black Box",
         "Selesai",
         "Subbab 1.1, 1.3, 2.5; Tabel 3.2 (KF-P01); Gambar 3.3; Gambar 3.9–3.11; "
         "Tabel 3.25; Tabel 3.10 skenario 1"],
        ["6", "Ketersediaan/stok menu konsisten", "Selesai",
         "Subbab 1.1, 1.3; Tabel 3.1; Tabel 3.2 (KF-P04); Tabel 3.3 (KF-A04); "
         "Tabel 3.17; Tabel 3.22; Tabel 3.25; Tabel 3.10 skenario 4 dan 14"],
        ["7", "Add-on konsisten dari Requirement, ERD/database, UI, perhitungan harga, "
              "hingga pengujian", "Selesai",
         "Paragraf rantai add-on pada 3.8; Tabel 3.2 (KF-P05); Tabel 3.3 (KF-A05); "
         "relasi addon_group_item pada Tabel 3.21; Tabel 3.22 dan 3.25; Tabel 3.10 "
         "skenario 5 dan 16; Tabel 3.12"],
        ["8", "Payment method konsisten dengan implementasi Midtrans", "Selesai",
         "Subbab baru 2.10 Payment Gateway (Midtrans); Tabel 3.6; Tabel 3.16; "
         "Gambar 3.9–3.11"],
        ["9", "Status pembayaran dibedakan dari status dapur", "Selesai",
         "Butir baru pada 1.3; paragraf penutup 3.8; Tabel 3.2 (KF-P12); Tabel 3.10 "
         "skenario 11"],
        ["10", "QRIS/Midtrans tanpa konfirmasi manual Kasir", "Selesai",
         "Subbab 1.3 dan 2.10; Tabel 3.5 (KF-S04); Tabel 3.18; Tabel 3.24; Tabel 3.10 "
         "skenario 27; narasi DFD pada 3.11"],
        ["11", "Pembayaran tunai memakai konfirmasi Kasir", "Selesai",
         "Subbab 1.3; Tabel 3.5 (KF-S03); Tabel 3.16; Tabel 3.10 skenario 26"],
        ["12", "Tracking status pesanan muncul pada Requirement, UI, database, dan "
               "Black Box", "Selesai",
         "Tabel 3.2 (KF-P12); Tabel 3.25 baris halaman status/progres pesanan; "
         "Tabel 3.20; Tabel 3.10 skenario 11"],
        ["13", "order_code, table_number, payment_method, status, dan kitchen_status "
               "konsisten", "Selesai",
         "Dipakai dengan nama dan nilai yang sama pada 1.3, 2.6, 2.10, 3.8, 3.14, serta "
         "seluruh tabel pengujian"],
        ["14", "Use Case sesuai fitur terbaru", "Sebagian; gambar perlu dilengkapi",
         "Narasi 3.7 sudah memuat empat aktor dan Tabel 3.16 diperluas dari 4 menjadi 17 "
         "use case; kekurangan pada gambar dijelaskan pada subbab A.4"],
        ["15", "DFD sesuai alur terbaru", "Selesai",
         "Narasi 3.11 diperbaiki menjadi lima entitas eksternal (sebelumnya tertulis "
         "empat) dan dua cabang pembayaran dipisah secara tegas"],
        ["16", "ERD mendukung seluruh fitur", "Selesai",
         "Gambar ERD memuat sembilan tabel yang sama dengan migration; subbab 3.8 "
         "menjelaskan daftar tabel, alasan meja bukan entitas, dan pemisahan dua kolom "
         "status"],
        ["17", "UI menggambarkan seluruh fitur", "Selesai",
         "Tabel 3.22 (tiga komponen baru), Tabel 3.23 (satu), Tabel 3.24 (satu), dan "
         "Tabel 3.25 (dua)"],
        ["18", "Black Box menguji seluruh fitur utama", "Selesai",
         "Diperluas dari 24 menjadi 34 skenario, kini mencakup stok, add-on, tracking, "
         "Snap, webhook, dan settlement"],
        ["19", "UAT mengukur fitur yang benar-benar dipakai tiap aktor", "Selesai",
         "Tabel 3.12 (indikator spesifik per aktor) dan Tabel 3.14 (skor ideal per "
         "kelompok responden)"],
    ])
    C("Tabel A.2 Pemenuhan Checklist Final Pembimbing")

    # ------------------------------------------------------------------ A.3
    H("A.3 Rincian Perubahan per Bab")
    H("A.3.1 BAB I Pendahuluan")
    F("● Abstrak berbahasa Indonesia dan Inggris ditulis ulang agar memuat fitur yang "
      "benar-benar dibangun. Nama fakultas dan tahun diselaraskan dengan halaman judul, "
      "serta label Kata Kunci pada abstrak Inggris diubah menjadi Keywords.")
    F("● Subbab 1.1 memperoleh dua paragraf baru, yaitu daftar delapan fungsi sistem "
      "sebagai acuan tunggal dan penegasan bahwa yang dikelola adalah ketersediaan/stok "
      "menu, bukan persediaan bahan baku.")
    F("● Subbab 1.2 memperoleh butir baru mengenai ketersediaan menu yang tidak "
      "transparan, agar fitur pengelolaan stok menu memiliki dasar permasalahan.")
    F("● Subbab 1.3 ditulis ulang: empat aktor disebut eksplisit, pramusaji dinyatakan "
      "bukan aktor sistem, pelanggan tidak diwajibkan login, dua kanal pembayaran "
      "dipisah beserta wewenang Kasir, ditambah butir stok menu/add-on, butir pemisahan "
      "status pembayaran dari status dapur, serta daftar hal di luar cakupan sistem.")
    F("● Rumusan masalah bertambah dari 3 menjadi 6 butir dan tujuan penelitian dari 3 "
      "menjadi 7 butir, masing-masing menunjuk fitur nyata.")
    F("● Manfaat bagi pengguna dipecah per aktor, yaitu Pelanggan, Koki, Kasir, dan "
      "Admin/Owner.")

    H("A.3.2 BAB II Landasan Teori")
    F("● Subbab baru 2.10 Payment Gateway (Midtrans) menjelaskan fungsi payment gateway, "
      "alur Snap API beserta snap_token, alur webhook pada rute POST "
      "/midtrans/notification, verifikasi signature_key dengan SHA-512, serta "
      "konsekuensinya terhadap wewenang Kasir. Fitur Midtrans yang tidak dipakai "
      "dinyatakan tidak dibahas.")
    F("● Penomoran subbab setelahnya digeser menjadi 2.11 Visual Studio Code, 2.12 Use "
      "Case Diagram, 2.13 ERD, 2.14 Waterfall Model, 2.15 DFD, 2.16 Black-box Testing, "
      "dan 2.17 UAT, beserta seluruh rujukan silangnya.")
    F("● Subbab 2.12 tidak lagi menyebut pelayan dan bagian dapur sebagai aktor, "
      "melainkan empat aktor sistem.")
    F("● Subbab 2.13 memperoleh paragraf yang mendaftar sembilan tabel yang benar-benar "
      "dipakai dan menegaskan meja bukan entitas tersendiri.")
    F("● Subbab 2.14 menegaskan output tahap Requirement sebagai acuan tunggal yang wajib "
      "muncul kembali pada Use Case, ERD, DFD, UI, Black Box, dan UAT.")
    F("● Contoh Enums pada 2.6 serta daftar tabel dan relasi pada 2.7 diselaraskan dengan "
      "skema basis data yang sebenarnya.")
    F("● Istilah stok bahan baku pada ulasan penelitian terdahulu diganti menjadi "
      "ketersediaan/stok menu, dan baris penelitian ini pada Tabel 2.1 diperbarui pada "
      "kolom Teknologi, Stok, Laporan, serta Pengujian.")
    F("● Caption Gambar 2.1 dan Gambar 2.2 dibetulkan karena kedua gambar tersebut "
      "sebenarnya Use Case Diagram dan ERD sistem, bukan simbol notasi.")

    H("A.3.3 BAB III Metode Penelitian")
    F("● Subbab 3.2 menegaskan objek penelitian tidak diperluas ke inventori bahan baku.")
    F("● Subbab 3.3 tidak lagi menyebut selisih stok bahan baku; ditambahkan tiga "
      "paragraf yang merinci komponen Input, Process, dan Output sesuai daftar "
      "pembimbing.")
    F("● Subbab 3.4 memperbaiki pertanyaan wawancara Sesi 2 menjadi pertanyaan mengenai "
      "proses pengelolaan ketersediaan/stok menu, mengubah judul sesi, mengganti temuan "
      "observasi selisih stok menjadi temuan pengelolaan ketersediaan menu, serta "
      "menegaskan pramusaji berperan sebagai informan dan bukan pengguna sistem.")
    F("● Subbab 3.5.1 memperoleh lima tabel kebutuhan fungsional per aktor, yaitu "
      "Tabel 3.2 Pelanggan (KF-P01–KF-P12), Tabel 3.3 Admin (KF-A01–KF-A10), Tabel 3.4 "
      "Koki (KF-K01–KF-K07), Tabel 3.5 Kasir (KF-S01–KF-S07), dan Tabel 3.6 "
      "Sistem/Midtrans (KF-M01–KF-M06). Setiap baris memuat keterangan implementasi.")
    F("● Subbab 3.7 ditulis ulang tanpa aktor Staf Pelayan, dilengkapi daftar use case "
      "per aktor, dan gambar use case dipindahkan ke subbab ini sebagai Gambar 3.3 "
      "karena sebelumnya subbab tersebut hanya berisi ruang kosong.")
    F("● Subbab 3.8 memperoleh tiga paragraf baru mengenai daftar tabel, rantai "
      "konsistensi add-on, dan pemisahan orders.status dengan orders.kitchen_status.")
    F("● Subbab 3.10 memperluas Black-Box Testing dari 24 menjadi 34 skenario dengan "
      "rincian Pelanggan 11, Admin 8, Koki 4, Kasir 5, dan Sistem/Midtrans 6. Tabel yang "
      "sebelumnya terpecah dua digabung menjadi satu tabel dengan baris judul berulang.")
    F("● Subbab 3.11 memperbaiki jumlah entitas eksternal dari empat menjadi lima "
      "termasuk Midtrans, ditambah paragraf yang memisahkan cabang non-tunai dan cabang "
      "tunai serta menegaskan Kasir bukan pihak yang mengonfirmasi pembayaran QRIS.")
    F("● Subbab 3.12 memecah instrumen UAT menjadi butir inti dan butir spesifik per "
      "aktor, dilengkapi Tabel 3.12 dan Tabel 3.14 beserta penyesuaian rumus dan contoh "
      "perhitungan.")
    F("● Subbab 3.13 memperluas deskripsi use case dari 4 menjadi 17 use case yang "
      "mencakup keempat aktor.")
    F("● Subbab 3.14 melengkapi tabel hak akses Admin dengan lima field, mempertegas "
      "keterangan Kasir, membetulkan caption tabel hak akses Pelanggan, serta menambah "
      "tiga relasi add-on dan memperbaiki keterangan relasi users dengan orders.")
    F("● Subbab 3.15 menambahkan komponen antarmuka untuk add-on, stok, laporan bulanan, "
      "QR meja, penyaring antrean dapur, tombol status dapur, dan halaman status pesanan "
      "pelanggan.")

    # ------------------------------------------------------------------ A.4
    H("A.4 Penomoran Gambar dan Tabel")
    P("Penomoran sebelumnya bertabrakan, antara lain terdapat dua Tabel 3.17, tiga "
      "pasang Tabel 3.8 sampai 3.10, gambar DFD yang diberi label Tabel, serta rujukan "
      "Gambar 3.5 sampai dengan Gambar 3.3. Penomoran kini berurutan tanpa duplikasi.")
    F("● Gambar: 2.1, 2.2, dan 2.3; 3.1 Kerangka Penelitian; 3.2 Prosedur Waterfall; "
      "3.3 Use Case Diagram; 3.4 ERD; 3.5 sampai 3.8 antarmuka Pelanggan; 3.9 Context "
      "Diagram; 3.10 DFD Level 1; dan 3.11 DFD Level 2.")
    F("● Tabel: 2.1; 3.1; 3.2 sampai 3.6 kebutuhan fungsional; 3.7 kebutuhan "
      "non-fungsional; 3.8 sampai 3.10 Black Box; 3.11 sampai 3.15 UAT; 3.16 deskripsi "
      "use case; 3.17 sampai 3.20 hak akses; 3.21 relasi antar tabel; 3.22 sampai 3.25 "
      "rancangan antarmuka; dan 3.26 jadwal penelitian.")
    P("Rujukan menggantung ke subbab 3.5.3 yang tidak pernah ada diarahkan ke subbab 3.10 "
      "dan 3.12.")

    # ------------------------------------------------------------------ A.5
    H("A.5 Hal yang Masih Perlu Dikerjakan pada Gambar")
    P("Perubahan teks, tabel, dan penomoran telah selesai. Tiga hal berikut menyangkut "
      "isi gambar sehingga tidak dapat diselesaikan dari naskah:")
    F("1. Gambar 3.3 Use Case Diagram perlu dilengkapi. Gambar yang tersedia sudah benar "
      "dari sisi aktor, yaitu Admin, Koki, Kasir, dan Pelanggan tanpa Staf Pelayan, "
      "tetapi belum memuat seluruh use case pada Tabel 3.16. Use case yang perlu "
      "ditambahkan adalah: kelola kategori, kelola karyawan, kelola role/hak akses, "
      "kelola ketersediaan/stok menu, lihat riwayat pesanan, dan bangkitkan QR meja "
      "untuk Admin; lihat antrean pesanan untuk Koki; lihat daftar pesanan menunggu "
      "pembayaran dan pantau status pembayaran Midtrans untuk Kasir; serta pilih add-on "
      "dan bayar pesanan secara tunai maupun non-tunai melalui Midtrans Snap untuk "
      "Pelanggan. Garis relasi Admin, Koki, dan Kasir sebaiknya juga dipisah per aktor "
      "agar mudah dibaca.")
    F("2. Judul yang tercetak di dalam ketiga gambar DFD masih berbunyi Gambar 3.8, "
      "Gambar 3.9, dan Gambar 3.10, sedangkan caption pada dokumen kini Gambar 3.9, "
      "Gambar 3.10, dan Gambar 3.11 karena Use Case Diagram masuk sebagai Gambar 3.3. "
      "Judul di dalam gambar dapat diperbarui atau dihapus, karena caption dokumen sudah "
      "memuat nomor dan nama gambar. Isi diagramnya sendiri sudah sesuai catatan "
      "pembimbing dan tidak perlu diubah.")
    F("3. Gambar 2.1 dan Gambar 2.2 merupakan salinan dari Gambar 3.3 dan Gambar 3.4. "
      "Caption keduanya telah dibetulkan dan dirujuk silang. Apabila pembimbing tidak "
      "menghendaki gambar yang sama muncul dua kali, kedua gambar pada BAB II dapat "
      "dihapus dengan menggeser nomor Gambar 2.3 Model Waterfall menjadi Gambar 2.1.")

    # ------------------------------------------------------------------ A.6
    H("A.6 Celah Implementasi yang Perlu Ditutup")
    P("Beberapa kebutuhan fungsional pada naskah revisi belum tersedia pada kode program. "
      "Karena naskah ini berupa proposal atau rancangan, hal tersebut sah dituliskan, "
      "namun perlu diselesaikan sebelum penyusunan BAB IV:")
    T([3400, 5810], [
        ["Kebutuhan pada Proposal", "Kondisi pada Implementasi"],
        ["KF-M02 dan KF-M03: webhook beserta verifikasi signature_key",
         "Rute POST /midtrans/notification masih dinonaktifkan dan controller webhook "
         "belum dibuat. Saat ini pelunasan QRIS hanya diperiksa ketika pelanggan kembali "
         "ke halaman sukses pembayaran"],
        ["Skenario Black Box nomor 30 mengenai webhook",
         "Belum dapat diuji sebelum webhook diimplementasikan"],
        ["KF-A10: halaman QR meja",
         "Rute GET /qr-meja sudah tersedia, tetapi tampilan halamannya belum dibuat"],
        ["Penanganan status expire, deny, dan cancel dari Midtrans",
         "Belum ditangani"],
        ["Nilai enum orders.status",
         "Masih memuat nilai warisan cooked; sebaiknya dibersihkan agar hanya pending "
         "dan settlement sesuai naskah"],
    ])
    C("Tabel A.3 Celah Implementasi terhadap Kebutuhan Fungsional")
