# **Sistem Reservasi Lapangan Olahraga**

---

**ANGGOTA C2 FIKRICHANN PA DDP**
---
Muhammad Fikri	  2609116095

Soraya Ghina    	2609116081

Adhwa Maysura     2609116103

Diana Aurelia	    2609116105

---

Program Sistem Reservasi Lapangan Olahraga ini berbasis **python** untuk yang dibuat untuk mengelola reservasi lapangan olahraga. Program punya **dua role**, yaitu **Admin** dan **User**. Pembayaran memakai **saldo yg sudah diisi melalui admin**, dan semua data disimpan otomatis di file **JSON**.

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


### Menu Admin
<img width="466" height="369" alt="image" src="https://github.com/user-attachments/assets/2f0132be-818f-426f-86ce-08e76217d2ea" />

saat login sebagai role admin akan menampilkan beberapa fungsi atau menu seperti berikut, dari menu berikut pengguna dipersilahkan untuk memilih (input pilihan)


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

Instal library tambahan melalui terminal:

bash
pip install prettytable pwinput

---

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

### 1. Konstanta & Tuple Menu (baris 9–42)

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
