# Catatan Revisi Proposal — Catatan Pembimbing 5 September 2026

Berkas hasil revisi: **`Proposal-Revisi-5-September-2026.docx`**
Berkas sumber: `proposal fixed5.docx`

Seluruh revisi disinkronkan dengan implementasi nyata pada repositori **restoranku**
(Laravel 12). Setiap klaim fitur, nama tabel, nama kolom, dan nilai status pada proposal
sudah dicocokkan dengan migration, model, route, dan controller yang benar-benar ada.

---

## 1. Acuan implementasi yang dipakai

Fakta berikut diambil langsung dari kode dan dijadikan dasar penulisan ulang:

| Aspek | Kondisi di repositori |
|---|---|
| Tabel | `roles`, `users`, `categories`, `items`, `addon_groups`, `addons`, `addon_group_item`, `orders`, `order_items` |
| Role | `admin`, `chef` (Koki), `cashier` (Kasir), `customer` (`database/seeders/RoleSeeder.php`) |
| Status pembayaran | `orders.status` enum `pending`, `settlement`, `cooked` |
| Status dapur | `orders.kitchen_status` — `waiting`, `processing`, `cooking`, `ready` (`app/Models/Order.php`) |
| Metode bayar | `orders.payment_method` enum `tunai`, `qris` |
| Stok | `items.stock` + `items.is_active`, `addons.stock` + `addons.is_active` |
| Add-on tersimpan | Snapshot JSON pada `order_items.addons` |
| Pajak | 10% dihitung di `MenuController@storeOrder` |
| Meja | **Bukan tabel.** Disimpan sebagai `orders.table_number`; QR dibangkitkan `TableQrController` (default 12 meja) |
| Akses pelanggan | Tanpa login, via sesi meja dari rute `GET /meja/{tableNumber}` |
| Login staf | `AuthenticatedSessionController` menolak akun `customer` |
| Nota | `GET /orders/{order}/nota` |
| Laporan bulanan | `GET /orders/laporan-excel` (Admin + Kasir) |
| Tidak ada | Tabel/modul inventori bahan baku — **dikonfirmasi tidak ada sama sekali** |

---

## 2. Checklist final pembimbing

| # | Butir checklist | Status | Lokasi pada naskah revisi |
|---|---|---|---|
| 1 | BAB I memakai istilah fitur yang sama dengan BAB III | Selesai | Paragraf baru di akhir 1.1 memuat 8 fungsi sistem sebagai acuan tunggal, dirujuk ulang di 1.4, 1.5, 3.5.1, 3.10, 3.12 |
| 2 | Tidak ada lagi istilah "stok bahan baku" | Selesai | Semua diganti "ketersediaan/stok menu (dan add-on)". Istilah bahan baku hanya tersisa pada kalimat penyangkalan di 1.1, 1.3, 3.2, dan 3.8 |
| 3 | Aktor konsisten: Pelanggan, Koki, Kasir, Admin | Selesai | 1.3, 2.12, 3.6, 3.7, 3.11, 3.14 |
| 4 | Tidak ada lagi aktor "Staf Pelayan" | Selesai | 1.3 dan 3.7 menyatakan eksplisit aktor tersebut dihapus beserta alasannya |
| 5 | QR Code konsisten di BAB I, Requirement, Use Case, DFD, UI, Black Box | Selesai | 1.1, 1.3, 2.5, Tabel 3.2 (KF-P01), Gambar 3.3, Gambar 3.9–3.11, Tabel 3.25, Tabel 3.10 skenario 1 |
| 6 | Stok/ketersediaan menu konsisten | Selesai | 1.1, 1.3, Tabel 3.1, Tabel 3.2 (KF-P04), Tabel 3.3 (KF-A04), Tabel 3.17, Tabel 3.22, Tabel 3.25, Tabel 3.10 skenario 4 & 14 |
| 7 | Add-on konsisten: Requirement → ERD/database → UI → perhitungan harga → pengujian | Selesai | Paragraf rantai add-on di 3.8, Tabel 3.2 (KF-P05), Tabel 3.3 (KF-A05), relasi `addon_group_item` di Tabel 3.21, Tabel 3.22 & 3.25, Tabel 3.10 skenario 5 & 16, Tabel 3.12 |
| 8 | Payment method konsisten dengan implementasi Midtrans | Selesai | Subbab baru **2.10 Payment Gateway (Midtrans)**, Tabel 3.6, Tabel 3.16, Gambar 3.9–3.11 |
| 9 | Status pembayaran dibedakan dari status dapur | Selesai | Butir baru di 1.3, paragraf penutup 3.8, Tabel 3.2 (KF-P12), Tabel 3.10 skenario 11 |
| 10 | QRIS/Midtrans tanpa konfirmasi manual Kasir | Selesai | 1.3, 2.10, Tabel 3.5 (KF-S04), Tabel 3.18, Tabel 3.24, Tabel 3.10 skenario 27, narasi DFD 3.11 |
| 11 | Pembayaran tunai memakai konfirmasi Kasir | Selesai | 1.3, Tabel 3.5 (KF-S03), Tabel 3.16, Tabel 3.10 skenario 26 |
| 12 | Tracking status pesanan muncul di Requirement, UI, database, Black Box | Selesai | Tabel 3.2 (KF-P12), Tabel 3.25 baris "Halaman status/progres pesanan", Tabel 3.20, Tabel 3.10 skenario 11 |
| 13 | `order_code`, `table_number`, `payment_method`, `status`, `kitchen_status` konsisten | Selesai | Dipakai dengan nama dan nilai yang sama di 1.3, 2.6, 2.10, 3.8, 3.14, dan seluruh tabel pengujian |
| 14 | Use Case sesuai fitur terbaru | Sebagian — perlu gambar diperbarui | Narasi 3.7 sudah lengkap 4 aktor; Tabel 3.16 diperluas dari 4 menjadi 17 use case. **Lihat bagian 4 di bawah** |
| 15 | DFD sesuai alur terbaru | Selesai (isi gambar sudah benar) | Narasi 3.11 diperbaiki: 5 entitas eksternal (sebelumnya tertulis 4) dan dua cabang pembayaran dipisah tegas |
| 16 | ERD mendukung seluruh fitur | Selesai | Gambar ERD sudah memuat 9 tabel yang sama dengan migration; 3.8 menjelaskan tabel, alasan meja bukan entitas, dan pemisahan dua kolom status |
| 17 | UI menggambarkan seluruh fitur | Selesai | Tabel 3.22 (+3 komponen), Tabel 3.23 (+1), Tabel 3.24 (+1), Tabel 3.25 (+2) |
| 18 | Black Box menguji seluruh fitur utama | Selesai | Diperluas **24 → 34 skenario**, kini mencakup stok, add-on, tracking, Snap, webhook, dan settlement |
| 19 | UAT mengukur fitur yang benar-benar dipakai tiap aktor | Selesai | Tabel 3.12 baru (indikator spesifik per aktor) + Tabel 3.14 baru (skor ideal per kelompok responden) |

---

## 3. Rincian perubahan per bab

### BAB I

- **Abstrak (ID & EN)** ditulis ulang agar memuat fitur yang benar-benar dibangun. Nama
  fakultas dan tahun diselaraskan dengan halaman judul; label `Kata Kunci` pada abstrak
  Inggris diubah menjadi `Keywords`.
- **1.1 Latar Belakang** — dua paragraf baru: daftar 8 fungsi sistem sebagai acuan tunggal,
  dan penegasan bahwa yang dikelola adalah ketersediaan/stok menu, bukan bahan baku.
- **1.2 Identifikasi Masalah** — butir baru "Ketersediaan Menu Tidak Transparan" agar
  fitur pengelolaan stok menu punya dasar masalah.
- **1.3 Pembatasan Masalah** — ditulis ulang: empat aktor disebut eksplisit; pramusaji
  dinyatakan bukan aktor sistem; pelanggan tanpa login (sesi/token meja); dua kanal
  pembayaran dengan pemisahan wewenang Kasir; butir stok menu/add-on; butir pemisahan
  status pembayaran dan status dapur; daftar hal di luar cakupan (bahan baku, supplier,
  payroll, reservasi).
- **1.4 Rumusan Masalah** — dari 3 menjadi **6 butir**, masing-masing menunjuk fitur nyata.
- **1.5 Tujuan Penelitian** — dari 3 menjadi **7 butir**, sejalan dengan rumusan masalah.
- **1.6 Manfaat Penelitian** — manfaat pengguna dipecah per aktor (Pelanggan, Koki, Kasir,
  Admin/Owner) sesuai permintaan pembimbing.

### BAB II

- **Subbab baru 2.10 Payment Gateway (Midtrans)** — menjelaskan fungsi payment gateway,
  alur Snap API (`snap_token`), alur webhook (`POST /midtrans/notification`), verifikasi
  `signature_key` (SHA-512), dan konsekuensinya terhadap wewenang Kasir. Fitur Midtrans
  yang tidak dipakai (recurring, payout, refund) dinyatakan tidak dibahas.
- Penomoran subbab setelahnya digeser: 2.11 VS Code, 2.12 Use Case, 2.13 ERD,
  2.14 Waterfall, 2.15 DFD, 2.16 Black-box, 2.17 UAT. Semua rujukan silang disesuaikan.
- **2.12 Use Case** — kalimat "pelanggan, pelayan, dan bagian dapur" diganti menjadi empat
  aktor sistem. Typo "Villa Jembrana. ini" diperbaiki.
- **2.13 ERD** — paragraf baru mendaftar 9 tabel yang benar-benar dipakai dan menegaskan
  meja bukan entitas tersendiri.
- **2.14 Waterfall** — output tahap Requirement dinyatakan sebagai *single source of
  requirement* yang wajib muncul kembali di Use Case, ERD, DFD, UI, Black Box, dan UAT.
- **2.6 PHP 8.1** — contoh Enums diselaraskan dengan nilai enum yang sebenarnya ada.
- **2.7 Laravel 12** — daftar tabel migration dan relasi dilengkapi add-on; role
  diselaraskan dengan tabel `roles`.
- Istilah "stok bahan baku" pada ulasan penelitian terdahulu (4 tempat) diganti
  "ketersediaan/stok menu".
- **Tabel 2.1** baris penelitian ini: kolom Teknologi, Stok, Laporan, dan Pengujian
  diperbarui (sebelumnya kolom Stok hanya berisi tanda "-").
- Caption **Gambar 2.1** dan **Gambar 2.2** diperbaiki: gambar tersebut sebenarnya Use Case
  Diagram dan ERD sistem, bukan "simbol". Keduanya kini dirujuk silang ke subbab 3.7/3.8.

### BAB III

- **3.2 Objek Penelitian** — ditegaskan objek tidak diperluas ke inventori bahan baku.
- **3.3 Kerangka Penelitian** — "selisih kronis stok bahan baku" dihapus; tiga paragraf
  baru merinci Input, Process, dan Output persis seperti daftar pembimbing (scan QR,
  add-on, keranjang, checkout, webhook Midtrans, antrean dapur, nota, riwayat, dst.).
- **3.4 Pengumpulan Data**
  - Pertanyaan wawancara Sesi 2 diganti sesuai instruksi menjadi *"Bagaimana proses
    pengelolaan ketersediaan/stok menu yang ditampilkan kepada pelanggan…"*.
  - Judul Sesi 2 diubah menjadi "Pengelolaan Ketersediaan Menu & Rekapitulasi Penjualan".
  - Temuan observasi "Selisih Stok & Keuangan 5–8%" diganti temuan pengelolaan
    ketersediaan menu (2–4 item/hari).
  - Kriteria Owner dan estimasi kualitatif informan disesuaikan.
  - Ditegaskan pramusaji ikut sebagai informan/responden umum, bukan pengguna sistem.
- **3.5.1 Requirement** — menjadi acuan utama. **Lima tabel baru**:
  Tabel 3.2 Pelanggan (12 kebutuhan, KF-P01–KF-P12), Tabel 3.3 Admin (10, KF-A01–KF-A10),
  Tabel 3.4 Koki (7, KF-K01–KF-K07), Tabel 3.5 Kasir (7, KF-S01–KF-S07),
  Tabel 3.6 Sistem/Midtrans (6, KF-M01–KF-M06). Setiap baris memuat keterangan
  implementasi (nama tabel/kolom/rute yang dipakai).
- **3.7 Use Case** — narasi ditulis ulang tanpa "Staf Pelayan", ditambah daftar use case
  per aktor, dan **gambar use case dipindahkan ke subbab ini sebagai Gambar 3.3**
  (sebelumnya subbab 3.7 hanya berisi ruang kosong).
- **3.8 ERD** — tiga paragraf baru: daftar tabel, alasan meja bukan entitas, rantai
  konsistensi add-on (ERD → database → UI → perhitungan harga → order item → Black Box),
  dan pemisahan `orders.status` vs `orders.kitchen_status`.
- **3.10 Black-Box Testing** — **24 → 34 skenario** (Pelanggan 11, Admin 8, Koki 4,
  Kasir 5, Sistem/Midtrans 6). Tabel lama yang terpecah dua digabung menjadi satu tabel
  dengan baris judul berulang dan baris yang tidak terpotong antarhalaman.
- **3.11 DFD** — jumlah entitas eksternal diperbaiki dari 4 menjadi **5** (termasuk
  Midtrans), ditambah paragraf yang memisahkan cabang non-tunai dan cabang tunai serta
  menegaskan Kasir bukan pihak yang mengonfirmasi QRIS. Penomoran ganda "B." diperbaiki.
- **3.12 UAT** — instrumen dipecah menjadi butir inti (12) + butir spesifik per aktor;
  **Tabel 3.12** (indikator per aktor: Pelanggan 6, Koki 3, Kasir 4, Admin 7) dan
  **Tabel 3.14** (skor ideal per kelompok responden, total 305 butir / skor ideal 1.525)
  ditambahkan; rumus dan contoh perhitungan disesuaikan.
- **3.13 Deskripsi Use Case** — Tabel 3.16 diperluas dari 4 menjadi **17 use case**
  mencakup keempat aktor.
- **3.14 Struktur Tabel** — Tabel 3.17 (Admin) ditambah 5 field (`addon_groups.is_active`,
  `addons.is_active`, `addon_group_item.item_id`, `orders.table_number`, `orders.note`);
  keterangan Kasir untuk `orders.status` dan `orders.payment_method` dipertegas; caption
  tabel hak akses Pelanggan diperbaiki (sebelumnya tertulis "(Koki)" dan diberi label "C."
  ganda); Tabel 3.21 ditambah 3 relasi add-on dan keterangan `users → orders` diperbaiki
  (pemilik pesanan adalah akun pelanggan yang dibuat otomatis, bukan kasir/admin).
- **3.15 Rancangan UI** — komponen add-on, stok, laporan bulanan, QR meja, penyaring
  antrean dapur, tombol status sesuai `kitchen_status`, dan halaman status/progres pesanan
  pelanggan ditambahkan.

### Penomoran gambar dan tabel

Penomoran sebelumnya bertabrakan (dua "Tabel 3.17", tiga pasang "Tabel 3.8/3.9/3.10",
gambar DFD diberi label "Tabel", dan rujukan "Gambar 3.5 sampai dengan Gambar 3.3").
Kini berurutan tanpa duplikasi:

- Gambar: 2.1, 2.2, 2.3 · 3.1 Kerangka · 3.2 Prosedur Waterfall · **3.3 Use Case** ·
  3.4 ERD · 3.5–3.8 UI Pelanggan · 3.9 Context Diagram · 3.10 DFD Level 1 ·
  3.11 DFD Level 2
- Tabel: 2.1 · 3.1 · **3.2–3.6 kebutuhan fungsional** · 3.7 non-fungsional ·
  3.8–3.10 Black Box · 3.11–3.15 UAT · 3.16 deskripsi use case · 3.17–3.20 hak akses ·
  3.21 relasi · 3.22–3.25 UI · 3.26 jadwal

Rujukan menggantung ke "subbab 3.5.3" (yang tidak pernah ada) diarahkan ke subbab 3.10
dan 3.12.

---

## 4. Yang masih perlu dikerjakan manual

Perubahan teks, tabel, dan penomoran sudah selesai. Tiga hal berikut menyangkut isi
gambar sehingga tidak dapat diselesaikan dari naskah:

1. **Gambar 3.3 Use Case Diagram — perlu dilengkapi.**
   Gambar yang tersedia sudah benar dari sisi aktor (Admin, Koki, Kasir, Pelanggan; tidak
   ada Staf Pelayan), tetapi belum memuat seluruh use case pada Tabel 3.16. Yang perlu
   ditambahkan:
   - Admin: kelola kategori, kelola karyawan, kelola role/hak akses, kelola
     ketersediaan/stok menu, lihat riwayat pesanan, bangkitkan QR meja
   - Koki: lihat antrean pesanan
   - Kasir: lihat daftar pesanan menunggu pembayaran, pantau status pembayaran Midtrans
   - Pelanggan: pilih add-on, bayar pesanan (tunai dan non-tunai via Midtrans Snap)

   Selain itu, garis relasi Admin/Koki/Kasir saat ini menyatu dalam satu berkas garis
   sehingga sulit dibaca aktor mana memiliki use case mana — sebaiknya dipisah per aktor.

2. **Judul di dalam gambar DFD perlu disesuaikan.**
   Ketiga gambar DFD memuat judul yang tercetak di dalam gambar berbunyi
   "Gambar 3.8", "Gambar 3.9", dan "Gambar 3.10", sedangkan caption di dokumen kini
   "Gambar 3.9", "Gambar 3.10", dan "Gambar 3.11" (karena Use Case Diagram masuk sebagai
   Gambar 3.3). Pilih salah satu: perbarui teks judul di dalam gambar, atau hapus judul di
   dalam gambar karena caption dokumen sudah memuat nomor dan nama gambar. Isi diagramnya
   sendiri sudah sesuai catatan pembimbing dan tidak perlu diubah.

3. **Gambar 2.1 dan 2.2 adalah salinan dari Gambar 3.3 dan 3.4.**
   Caption sudah diperbaiki dan dirujuk silang. Bila pembimbing tidak menghendaki gambar
   yang sama muncul dua kali, kedua gambar di BAB II dapat dihapus dan cukup mengacu ke
   BAB III (nomor Gambar 2.3 Model Waterfall perlu digeser menjadi 2.1 bila ini dilakukan).

---

## 5. Celah implementasi yang perlu ditutup agar klaim proposal terpenuhi

Beberapa kebutuhan fungsional pada naskah revisi belum ada di kode. Karena naskah ini
proposal (rancangan), hal tersebut sah dituliskan, tetapi harus dikerjakan sebelum BAB IV:

| Kebutuhan pada proposal | Kondisi di repositori |
|---|---|
| KF-M02 / KF-M03 webhook + verifikasi `signature_key` | Rute `POST /midtrans/notification` masih dikomentari di `routes/app.php`; `MidtransController` belum ada. Saat ini pelunasan QRIS hanya dicek saat pelanggan kembali ke halaman sukses (`MenuController@checkoutSuccess`) |
| Skenario Black Box no. 30 (webhook) | Belum dapat diuji sebelum webhook diimplementasikan |
| KF-A10 halaman QR meja | Rute `GET /qr-meja` sudah ada, tetapi view `admin.table.index` belum dibuat |
| Penanganan status `expire`, `deny`, `cancel` dari Midtrans | Belum ditangani |
| Enum `orders.status` | Masih memuat nilai warisan `cooked`; sebaiknya dibersihkan agar hanya `pending` dan `settlement` sesuai naskah |

---

## 6. Cara menghasilkan ulang berkas revisi

Skrip yang dipakai disimpan di `tools/` agar perubahan dapat diaudit dan dijalankan ulang
bila naskah sumber diperbarui.

```bash
pip install python-docx
cd docs/proposal/tools
python3 revise.py "/path/ke/proposal fixed5.docx" ../Proposal-Revisi-5-September-2026.docx
```

Skrip mengedit paragraf dan sel tabel secara terarah (berbasis pencarian teks) sehingga
gaya huruf, penomoran otomatis, gambar, dan tata letak dokumen asli tetap dipertahankan.
