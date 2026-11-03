# **Sistem Reservasi Lapangan Olahraga**

---

**ANGGOTA C2 FIKRICHANN PA DDP**
---
Muhammad Fikri	  2609116095

Soraya Ghina    	2609116081

Adhwa Maysura     2609116103

Diana Aurelia	    2609116105

---

Program Sistem Reservasi Lapangan Olahraga ini berbasis **python** untuk yang dibuat untuk mengelola reservasi lapangan olahraga. Program mempunyai **dua role**, yaitu **Admin** dan **User**. Pembayaran memakai **saldo yg sudah diisi melalui admin**, dan semua data disimpan otomatis di file **JSON**.

---

Sistem Reservasi Lapangan Olahraga merupakan aplikasi berbasis Python yang dirancang untuk mempermudah proses pengelolaan dan pemesanan lapangan olahraga. Aplikasi ini memiliki dua hak akses pengguna, yaitu **Admin** dan **User**. Admin dapat mengelola data lapangan, mengatur jam operasional, mengelola reservasi, serta melihat daftar pengguna. Sementara itu, User dapat melihat informasi lapangan, melakukan reservasi, melakukan pembayaran menggunakan saldo E-Money, melihat riwayat reservasi dan invoice, membatalkan reservasi, serta melakukan top up saldo.

Sistem ini juga dilengkapi dengan fitur validasi input, pengecekan ketersediaan jadwal, pencegahan bentrok reservasi, pengelolaan saldo dan refund, serta pembuatan invoice dalam format `.txt`. Seluruh data aplikasi disimpan menggunakan file JSON sehingga data pengguna, lapangan, reservasi, dan transaksi top up dapat dipertahankan meskipun program ditutup.

---

## Tujuan
Tujuan dari pembuatan program Sistem Reservasi Lapangan Olahraga adalah:
1. **Untuk mempermudah proses reservasi lapangan**, sehingga pengguna dapat melihat informasi dan melakukan pemesanan lapangan dengan lebih praktis.
2. **untuk membantu pengelolaan data lapangan**, seperti menambahkan, mengubah, melihat, dan menghapus informasi lapangan melalui hak akses admin.
3. **Menerapkan sistem login dan hak akses**, untuk membedakan fitur yang dapat digunakan oleh Admin dan User.
4. **Mengelola transaksi pembayaran digital**, melalui sistem saldo E-Money yang dilengkapi dengan fitur top up dan riwayat transaksi.
5. **Mencegah terjadinya bentrok jadwal reservasi**, dengan melakukan pemeriksaan ketersediaan waktu sebelum pemesanan dikonfirmasi.
6. **Menyediakan riwayat dan bukti transaksi**, melalui pencatatan reservasi serta pembuatan invoice secara otomatis.
7. **Menerapkan konsep pemrograman Python**, seperti penggunaan fungsi, percabangan, perulangan, dictionary, list, pengolahan file JSON, dan penanganan kesalahan (*error handling*).

File Program Python utama: `PADDP.py`  |  File Json Python: `DataDDP.json` (file ini dibuat otomatis)

---

## 📑 Daftar Isi

1. [Fitur Program](#-fitur-program)
2. [Library yang Digunakan](#-library-yang-digunakan)
3. [Cara Menjalankan](#-cara-menjalankan)
4. [Akun Admin Dan User](#-Role-Admin-Role-User)
5. [Struktur Data JSON](#-struktur-data-json)
6. [Penjelasan Kode Program](#-penjelasan-kode-program)
7. [Aturan & Validasi](#-aturan--validasi)
8. [Screenshot Output Program](#-screenshot-output-program)

---

## ✨ Fitur Program

### Menu Awal
<img width="477" height="285" alt="image" src="https://github.com/user-attachments/assets/57947167-9662-4c3d-87ef-9136f1cecb6a" />

di menu awal ini akan login sebagai admin atau user dan kita juga bisa membuat user baru dengan register.

--- 

### Menu Admin
<img width="466" height="369" alt="image" src="https://github.com/user-attachments/assets/2f0132be-818f-426f-86ce-08e76217d2ea" />

saat login sebagai role admin akan menampilkan beberapa fungsi atau menu seperti berikut, dari menu berikut pengguna dipersilahkan untuk memilih (input pilihan)

---

### Menu User
<img width="473" height="450" alt="image" src="https://github.com/user-attachments/assets/6d9bb7b1-fc6e-49ff-9180-f7b5cf171eb8" />

Begitu juga dengan role user dimana akan menampilkan fungsi atau menu sebagai berikut

### Fitur Tambahan
- 🔐 Password disembunyikan dengan tanda *
- ⏳ Login gagal 3 kali → hitung mundur 30 detik
- 🕒 Setiap lapangan punya *jam operasional sendiri* (bisa diacak otomatis)
- 🧾 Invoice otomatis, bisa disimpan sebagai file .txt
- ⭐ Rating dan ulasan lapangan
- 🛡️ Anti-crash: error input ditangani, Ctrl+C tidak menutup program

---

## 📦 Library yang Digunakan

| Library | Fungsi |
|---------|--------|
| json | Menyimpan & membaca data dari file JSON |
| os | Membersihkan layar (cls/clear) dan membuat folder invoice |
| time | Jeda dan hitung mundur saat login gagal |
| random | Mengacak jam operasional lapangan |
| datetime | Validasi tanggal/jam dan mengecek reservasi yang sudah lewat |
| pwinput | Input password dengan tanda * |
| prettytable | Menampilkan data dalam bentuk tabel rapi |

sebelum itu Instal terlebih dahulu library tambahan melalui terminal vscode:
pip install prettytable pwinput

---

## 🔀 Alur Flowchart
 
### 1. Flowchart Menu Utama
 
<img width="1098" height="1139" alt="RESERVASI LAPANGAN C2-Flowchart Menu Utama drawio (1)" src="https://github.com/user-attachments/assets/2aa734c7-594f-4ad9-9952-a7d0225c1afa" />

 Alur dimulai dari **Menu Utama**, yang menampilkan pilihan Menu User, Menu Admin, Registrasi, dan Log Out. Program meminta input pilihan (1/2/3/4), lalu memeriksa validitasnya:
 
- **Pilihan tidak valid** → program kembali menampilkan menu utama.
- **Pilihan 1 (Menu User)** → masuk ke alur *Menu User*.
- **Pilihan 2 (Menu Admin)** → masuk ke alur *Menu Admin*.
- **Pilihan 3 (Registrasi)** → user mengisi data registrasi (Nama, Username, Password). Jika data valid, data disimpan lalu muncul pesan "Registrasi Berhasil!" dan kembali ke menu utama. Jika tidak valid, muncul pesan "Data tidak valid, cek kembali!" dan form diisi ulang.
- **Pilihan 4 (Logout)** → muncul pesan "Anda akan keluar dari sistem", lalu program **selesai**.
  
### 2. Flowchart Registrasi
 
<img width="357" height="972" alt="RESERVASI LAPANGAN C2-Registrasi  drawio (1)" src="https://github.com/user-attachments/assets/c9995919-36f2-4c2b-a7e7-5fdb890d929f" />

 
1. **Mulai**, lalu tampil judul "REGISTRASI AKUN".
2. User memasukkan **username**, lalu **password** (dengan batas maksimal karakter).
3. Sistem memeriksa panjang password. Jika **lebih dari 8 karakter**, tampil pesan "Password tidak boleh lebih dari 8 karakter".
4. Jika valid, data **disimpan ke JSON** dan tampil pesan akun berhasil dibuat.
5. User menekan **Enter** untuk kembali ke **Menu Utama**.
   
### 3. Flowchart Menu User
 
<img width="1717" height="1777" alt="RESERVASI LAPANGAN C2-Menu User drawio (1)" src="https://github.com/user-attachments/assets/3cfa4274-594e-45c9-89d9-784cf1406433" />

 
Menu User menampilkan nama user dan saldo, lalu meminta input pilihan. Pilihan di luar daftar menampilkan "Pilihan tidak ada!". Setiap fitur selesai dengan "Tekan Enter untuk kembali ke Menu User".
 
| Pilihan | Alur singkat |
|---|---|
| **Lihat Lapangan** | Baca data dari JSON → tampilkan tabel lapangan (ID, Nama, Harga/Jam, Luas, Lokasi). |
| **Reservasi Lapangan** | Tampil saldo dan daftar lapangan → input ID lapangan → input tanggal (tidak boleh lewat) → tampil jam operasional dan jam terpesan → input jam mulai dan durasi → cek jam belum lewat dan tidak bentrok → hitung total (harga/jam × durasi) → cek saldo cukup → konfirmasi bayar (y/n) → saldo dikurangi, reservasi disimpan (status *Dipesan*) → tampil invoice (opsional simpan `.txt`). |
| **Riwayat Reservasi & Invoice** | Cek apakah punya reservasi → tampil tabel riwayat → input ID untuk cetak invoice (0 = kembali) → cek ID milik user → tampil invoice → opsi simpan ke folder `invoice/`. |
| **Batalkan Reservasi** | Cek ada reservasi aktif → tampil daftar → input ID → cek ID valid dan status *Dipesan* → cek belum dimulai → konfirmasi (y/n) → status *Dibatalkan*, saldo dikembalikan → tampil refund dan saldo sekarang. |
| **Top Up Saldo** | Tampil saldo dan batas top up → input nominal (Rp 10.000 sampai Rp 1.000.000) → konfirmasi → saldo bertambah dan riwayat dicatat. |
| **Riwayat Top Up** | Baca JSON → tampil tabel riwayat (ID, Waktu, Nominal), atau pesan jika belum ada. |
| **Logout** | Keluar dari Menu User dan kembali ke Menu Utama. |
 
### 4. Flowchart Menu Admin
 
<img width="2639" height="1502" alt="RESERVASI LAPANGAN C2-Menu Admin drawio (1)" src="https://github.com/user-attachments/assets/6dd4cca4-97be-4a31-b123-1b58330f6516" />

 
Menu Admin membersihkan layar, menampilkan daftar menu, dan meminta input angka (diulang jika bukan angka atau di luar rentang). Alur tiap menu:
 
| Pilihan | Alur singkat |
|---|---|
| **Lihat Lapangan** | Baca JSON → tampilkan tabel lapangan (atau "Belum ada data lapangan"). |
| **Tambah Lapangan** | Input nama (tidak boleh kosong) → pilih jenis/atribut → input harga dan stok/atribut lain → buat ID baru (ID terbesar + 1) → simpan ke JSON → tampil "Lapangan berhasil ditambahkan". |
| **Ubah Lapangan** | Tampil tabel → input ID → jika ditemukan, input data baru (kosong = tidak diubah) → validasi nilai → simpan ke JSON → tampil "Data lapangan diperbarui". |
| **Hapus Lapangan** | Tampil tabel → input ID → jika ditemukan, konfirmasi "Yakin hapus?" (y/n) → hapus dan simpan ke JSON. |
| **Kelola Reservasi** | Ambil semua reservasi → jika ada, input ID reservasi (0 = kembali) → jika ditemukan, lanjut ke sub-menu kelola reservasi. |
| **Lihat Daftar User** | Tampilkan tabel akun terdaftar (Username, Role, Saldo dalam format Rupiah). |
| **Lihat Ulasan Lapangan** | Baca JSON → input ID lapangan (0 = batal) → tampilkan ulasan. |
| **Logout** | Tampil "Logout berhasil." lalu kembali ke Menu Utama. |
 
Setelah fitur selesai, muncul jeda "Tekan Enter untuk melanjutkan..." lalu kembali ke Menu Admin.
## 🔑 Akun Default

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

User biasa dibuat lewat menu *Registrasi*.

---

## 🗂️ Struktur Data JSON

File DataDDP.json menyimpan data user dan admin, menyimpan data lapangan, data reservasi, data topup pengguna:

<img width="516" height="517" alt="WhatsApp Image 2026-11-03 at 21 49 50" src="https://github.com/user-attachments/assets/a1b99fa1-201e-4b98-9c30-2bb373a1b306" />
<img width="579" height="481" alt="WhatsApp Image 2026-11-03 at 21 49 50 (1)" src="https://github.com/user-attachments/assets/490540ff-5a82-4e3d-a70d-720f83075c82" />
<img width="523" height="435" alt="WhatsApp Image 2026-11-03 at 21 49 51" src="https://github.com/user-attachments/assets/480ee60f-10b4-4681-9b46-f073c7d21b10" />
<img width="631" height="402" alt="image" src="https://github.com/user-attachments/assets/9ed20afd-d501-471f-84b4-b2f2a48a0104" />



---

## 📖 Penjelasan Kode Program

### 1. Tuple Menu

Semua pengaturan program dikumpulkan di bagian atas supaya mudah diubah.

| Konstanta | Nilai | Fungsi |
|-----------|-------|--------|
| FILE | DataDDP.json | Nama file penyimpanan data |
| FOLDER_INVOICE | invoice | Folder hasil simpan invoice |
| MENU_UTAMA, MENU_ADMIN, MENU_USER, MENU_UBAH, MENU_KELOLA | tuple | Daftar menu (tuple karena isinya tidak berubah) |
| MAKS_HARGA | 150.000 | Harga maksimal per jam |
| MAKS_PASSWORD | 8 | Panjang password maksimal |
| WAKTU_TUNGGU | 30 | Detik hitung mundur setelah login gagal |
| MAKS_DURASI | 4 | Durasi sewa maksimal (jam) |
| MIN_TOPUP / MAKS_TOPUP | 10.000 / 1.000.000 | Batas nominal top up |
| DENDA_BATAL | 10.000 | Denda pembatalan oleh user |
| MAKS_PERCOBAAN_PASSWORD | 3 | Batas salah password saat konfirmasi |
| MAKS_ULASAN | 100 | Panjang ulasan maksimal |
| STATUS_DIPESAN, STATUS_SELESAI, STATUS_BATAL | teks | Tiga status reservasi |


## 👥 Daftar Fitur per Role
 
### 🔐 (belum login)

 
| No | Fitur | Deskripsi |
|---|---|---|
| 1 | Login | Masuk dengan username dan password. Gagal 3 kali memicu hitung mundur 30 detik. Role (admin/user) menentukan menu yang tampil. |
| 2 | Registrasi | Membuat akun user baru (username unik, password maks 8 karakter, saldo awal Rp 0). |
| 3 | Keluar | Menutup program. |
 
### 🛠️ Admin
 
| No | Fitur | Deskripsi |
|---|---|---|
| 1 | Lihat Lapangan | Menampilkan semua lapangan beserta harga, luas, jam operasional, lokasi, dan rating. |
| 2 | Tambah Lapangan | Menambah lapangan baru, jam operasional bisa diacak otomatis atau manual. |
| 3 | Ubah Lapangan | Mengubah nama, harga, luas, lokasi, atau jam operasional. Perubahan jam ditolak jika ada reservasi aktif di luar jam baru. |
| 4 | Hapus Lapangan | Menghapus lapangan (dengan konfirmasi), ditolak jika masih ada reservasi aktif. |
| 5 | Kelola Reservasi | Melihat semua reservasi plus total pendapatan, lalu **Tandai Selesai**, **Batalkan & Refund** (refund penuh), atau **Hapus Riwayat**. |
| 6 | Daftar User | Melihat semua akun beserta role, saldo, dan jumlah reservasi. |
| 7 | Lihat Ulasan Lapangan | Melihat rating dan ulasan dari user per lapangan. |
| 8 | Logout | Kembali ke menu utama. |
 
### 👤 User
 
| No | Fitur | Deskripsi |
|---|---|---|
| 1 | Lihat Lapangan | Melihat daftar lapangan, harga, jam operasional, dan rating. |
| 2 | Reservasi Lapangan | Memesan lapangan dengan validasi jadwal dan pembayaran memakai saldo. |
| 3 | Riwayat Reservasi & Invoice | Melihat riwayat pesanan dan mencetak atau menyimpan invoice `.txt`. |
| 4 | Batalkan Reservasi | Membatalkan pesanan aktif dengan denda Rp 10.000, sisanya di-refund ke saldo. |
| 5 | Top Up Saldo | Menambah saldo (Rp 10.000 sampai Rp 1.000.000), dikonfirmasi password. |
| 6 | Riwayat Top Up | Melihat semua transaksi top up. |
| 7 | Beri Rating Lapangan | Memberi 1 sampai 5 bintang dan ulasan untuk reservasi berstatus *Selesai*. |
| 8 | Lihat Ulasan Lapangan | Membaca rating dan ulasan lapangan. |
| 9 | Logout | Kembali ke menu utama. |
 
---

### 📷 Screenshoot Output setiap program

<img width="466" height="254" alt="image" src="https://github.com/user-attachments/assets/bc08e0b8-c2ff-48c3-9aa2-21d96ef7740d" />

Berikut halaman awal program untuk login

---

<img width="466" height="361" alt="image" src="https://github.com/user-attachments/assets/c8851400-9c82-4aa2-9985-34df91489dfc" />

menu awal admin

---

<img width="916" height="363" alt="image" src="https://github.com/user-attachments/assets/99ccd51a-c5da-4c1d-aa77-0bba1b62307a" />

berikut menu daftar lapangan

---

<img width="523" height="370" alt="image" src="https://github.com/user-attachments/assets/0610a8ce-c8bf-4b79-a929-67f9d5d95be7" />

menu menambahkan lapangan 

---

<img width="1018" height="673" alt="image" src="https://github.com/user-attachments/assets/c0fc5ef6-f360-4648-9427-ef3238ff97e0" />

mengubah data lapangan 

---

<img width="898" height="490" alt="image" src="https://github.com/user-attachments/assets/7ec160c2-69e5-4b25-b5b7-2e6173784d05" />

menghapus data lapangan yg hanya bisa di lakukan oleh admin

---

<img width="826" height="643" alt="image" src="https://github.com/user-attachments/assets/a78290bc-5746-4cd0-83a1-2fbdbe774a65" />

berikut mengelola reservasi lapngan termasuk total pendapatan denda

---

<img width="626" height="518" alt="image" src="https://github.com/user-attachments/assets/20365d99-47b9-4c91-873e-fe5f5ea5009e" />

berikut daftar user yg pernah registrasi serta login

---

<img width="1037" height="485" alt="image" src="https://github.com/user-attachments/assets/08c92777-b822-4c6b-9d69-b11adbd11c2e" />

ulasan lapangan olahraga 

---

<img width="620" height="443" alt="image" src="https://github.com/user-attachments/assets/be9b1644-02ba-427e-afc7-25d75eb893d2" />

dan berikut ini menu user 

---

<img width="1052" height="725" alt="image" src="https://github.com/user-attachments/assets/d98428cb-bb4d-4c8a-a2c1-fd9f352ea71a" />

berikut ini menu user saat reservasi lapangan dan pembayaran menggunakan saldo yg diisi melalui admin

---

<img width="584" height="485" alt="image" src="https://github.com/user-attachments/assets/6e5dd8a6-de21-41b2-93db-43c93388c7ec" />

setelah reservasi lapangan berhasil akan mencetak invoice berformat txt

---

<img width="812" height="758" alt="image" src="https://github.com/user-attachments/assets/ab2ae6e3-b4a0-451d-ae57-11311328e009" />

riwayat reservasi dan bisa juga mencetak invoice disini

---

<img width="831" height="522" alt="image" src="https://github.com/user-attachments/assets/4d34c7d3-f65d-49a5-ac2c-1e8b0162c053" />

berikut menu pembatalan reservasi dan saat pembatalan akan terkena denda 10rb

---

<img width="643" height="391" alt="image" src="https://github.com/user-attachments/assets/d4167885-b251-41f5-8b8c-d1a38e7ea1dd" />

berikut ialah menu topup saldo dan untuk mengkonfirmasinya menggunakan password

---

<img width="930" height="377" alt="image" src="https://github.com/user-attachments/assets/6c2f49db-5d42-4395-a677-aabc770050f5" />

ulasan tiap lapangan

---

<img width="693" height="263" alt="image" src="https://github.com/user-attachments/assets/3de0add0-c45a-4635-8a4d-3412dc89e548" />

menu untuk memberi rating lapangan

---

sekian dari kami Kelompok 2 TERIMAKASIH
