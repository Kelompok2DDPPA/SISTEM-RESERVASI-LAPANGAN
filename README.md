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

Instal library tambahan:

bash
pip install prettytable pwinput


---

## ▶️ Cara Menjalankan

1. Pastikan Python 3 sudah terpasang.
2. Instal library: pip install prettytable pwinput
3. Jalankan program:

bash
python PADDP.py


Saat pertama dijalankan, file DataDDP.json dibuat otomatis berisi 1 akun admin dan 5 lapangan awal.

---
