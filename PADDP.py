from datetime import datetime
import json
import os
import random
import time
import pwinput
from prettytable import PrettyTable

FILE = "DataDDP.json"
FOLDER_INVOICE = "invoice"
MENU_UTAMA = ("Login", "Registrasi", "Keluar")
MENU_ADMIN = (
    "Lihat Lapangan", "Tambah Lapangan", "Ubah Lapangan", "Hapus Lapangan",
    "Kelola Reservasi", "Daftar User", "Lihat Ulasan Lapangan", "Logout",
)
MENU_UBAH = (
    "Ubah Nama", "Ubah Harga", "Ubah Luas", "Ubah Lokasi",
    "Ubah Jam Operasional", "Kembali",
)
MENU_USER = (
    "Lihat Lapangan", "Reservasi Lapangan", "Riwayat Reservasi & Invoice",
    "Batalkan Reservasi", "Top Up Saldo", "Riwayat Top Up",
    "Beri Rating Lapangan", "Lihat Ulasan Lapangan", "Logout",
)
MENU_KELOLA = ("Tandai Selesai", "Batalkan & Refund", "Hapus Riwayat", "Kembali")

MAKS_HARGA = 150000
MAKS_PASSWORD = 8
WAKTU_TUNGGU = 30

DEFAULT_BUKA = "08:00"
DEFAULT_TUTUP = "22:00"
MAKS_DURASI = 4
MIN_TOPUP = 10000
MAKS_TOPUP = 1000000
DENDA_BATAL = 10000
MAKS_PERCOBAAN_PASSWORD = 3
MAKS_ULASAN = 100

STATUS_DIPESAN = "Dipesan"
STATUS_SELESAI = "Selesai"
STATUS_BATAL = "Dibatalkan"

def bersihkan():
    os.system("cls" if os.name == "nt" else "clear")

def judul(teks):
    """Cetak judul dengan garis pembatas atas dan bawah."""
    print("=" * 40)
    print(teks.center(40))
    print("=" * 40)

def garis():
    print("-" * 40)

def tunggu():
    garis()
    input("Tekan Enter untuk kembali...")

def rupiah(angka):
    """Format angka jadi 100.000"""
    return f"{angka:,}".replace(",", ".")

def ke_menit(jam):
    """'08:30' -> 510 (menit sejak tengah malam)."""
    j, m = jam.split(":")
    return int(j) * 60 + int(m)

def dari_menit(menit):
    """510 -> '08:30'"""
    return f"{menit // 60:02d}:{menit % 60:02d}"

def format_jam(mulai, durasi):
    """Contoh: mulai='08:30', durasi=2 -> 08:30-10:30"""
    return f"{mulai}-{dari_menit(ke_menit(mulai) + durasi * 60)}"

def waktu_sekarang():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def input_angka(pesan):
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("[!] Harus angka!")

def input_rentang(pesan, kecil, besar):
    """Angka harus berada di antara kecil dan besar (inklusif)."""
    while True:
        angka = input_angka(pesan)
        if kecil <= angka <= besar:
            return angka
        print(f"[!] Harus antara {kecil} sampai {besar}!")

def input_harga(pesan):
    """Harga tidak boleh minus/nol dan tidak boleh melebihi MAKS_HARGA."""
    while True:
        harga = input_angka(pesan)
        if harga <= 0:
            print("[!] Harga tidak boleh minus atau nol!")
        elif harga > MAKS_HARGA:
            print(f"[!] Harga maksimal Rp {rupiah(MAKS_HARGA)}!")
        else:
            return harga

def input_luas(pesan):
    """Luas lapangan (m2) harus lebih dari 0."""
    while True:
        luas = input_angka(pesan)
        if luas <= 0:
            print("[!] Luas harus lebih dari 0!")
        else:
            return luas

def input_teks(pesan):
    """Teks tidak boleh kosong."""
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        print("[!] Tidak boleh kosong!")

def input_jam(pesan):
    """Jam format HH:MM (ada menitnya), contoh 08:30."""
    while True:
        teks = input(pesan).strip()
        try:
            return datetime.strptime(teks, "%H:%M").strftime("%H:%M")
        except ValueError:
            print("[!] Format jam salah! Contoh: 08:30")

def input_jam_operasional():
    """Minta jam buka & tutup. Return (buka, tutup), selisih minimal 1 jam."""
    while True:
        buka = input_jam("Jam buka  (HH:MM) : ")
        tutup = input_jam("Jam tutup (HH:MM) : ")
        if ke_menit(tutup) - ke_menit(buka) < 60:
            print("[!] Jam tutup minimal 1 jam setelah jam buka!")
        else:
            return buka, tutup

def jam_acak(data, id_abaikan=None):
    """Buat jam operasional acak (kelipatan 30 menit) yang belum dipakai lapangan lain.
    Buka: 06:00-10:00, tutup: 17:00-23:00 -> durasi buka selalu lebih dari 1 jam."""
    dipakai = {(l["buka"], l["tutup"]) for l in data["lapangan"]
               if l["id"] != id_abaikan and "buka" in l}
    for _ in range(200):
        buka = dari_menit(random.randrange(6 * 60, 10 * 60 + 1, 30))
        tutup = dari_menit(random.randrange(17 * 60, 23 * 60 + 1, 30))
        if (buka, tutup) not in dipakai:
            break
    return buka, tutup

def pilih_jam_operasional(data, id_abaikan=None):
    """Admin pilih: jam operasional diacak otomatis atau diisi manual."""
    if konfirmasi("Acak jam operasional otomatis?"):
        buka, tutup = jam_acak(data, id_abaikan)
        print(f"[+] Jam operasional acak : {buka}-{tutup}")
        return buka, tutup
    return input_jam_operasional()

def input_password(pesan):
    """Password tidak boleh kosong dan maksimal MAKS_PASSWORD karakter."""
    while True:
        password = pwinput.pwinput(pesan, mask="*")
        if password == "":
            print("[!] Password tidak boleh kosong!")
        elif len(password) > MAKS_PASSWORD:
            print(f"[!] Password maksimal {MAKS_PASSWORD} karakter!")
        else:
            return password

def input_tanggal(pesan):
    """Tanggal format YYYY-MM-DD dan tidak boleh sebelum hari ini."""
    while True:
        teks = input(pesan).strip()
        try:
            tgl = datetime.strptime(teks, "%Y-%m-%d")
        except ValueError:
            print("[!] Format tanggal salah! Contoh: 2026-11-05")
            continue
        if tgl.date() < datetime.now().date():
            print("[!] Tanggal tidak boleh sudah lewat!")
        else:
            return tgl.strftime("%Y-%m-%d")

def konfirmasi(pesan):
    """Return True jika user jawab y, False jika n."""
    while True:
        jawab = input(f"{pesan} (y/n): ").strip().lower()
        if jawab == "y":
            return True
        if jawab == "n":
            return False
        print("[!] Jawab dengan y atau n!")

def konfirmasi_password(akun, pesan):
    """Konfirmasi dengan mengisi password akun. Maksimal 3 kali percobaan."""
    print(pesan)
    for percobaan in range(1, MAKS_PERCOBAAN_PASSWORD + 1):
        password = pwinput.pwinput("Masukkan password untuk konfirmasi : ", mask="*")
        if password == akun["password"]:
            return True
        sisa = MAKS_PERCOBAAN_PASSWORD - percobaan
        print(f"[!] Password salah! Sisa percobaan: {sisa}")
    return False

def hitung_mundur(detik):
    """Hitung mundur sebelum user boleh login lagi."""
    print(f"\n[!] Login gagal 3 kali. Coba lagi dalam {detik} detik.")
    for sisa in range(detik, 0, -1):
        print(f"\r    Menunggu... {sisa:2d} detik ", end="", flush=True)
        time.sleep(1)
    print("\r    Silakan coba login kembali.      ")

def pilih_menu(teks_judul, menu, info=None):
    """Tampilkan menu dari tuple, return nomor pilihan."""
    judul(teks_judul)
    if info:
        print(info)
        garis()
    for i, item in enumerate(menu, start=1):
        print(f"  {i}. {item}")
    garis()
    return input_angka("Pilih menu: ")

def simpan(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def rapikan(data):
    """Lengkapi struktur data lama (versi sebelumnya) agar kompatibel."""
    data.setdefault("users", {})
    data.setdefault("lapangan", [])
    data.setdefault("reservasi", [])
    data.setdefault("topup", [])
    data.setdefault("rating", [])
    for akun in data["users"].values():
        akun.setdefault("role", "user")
        akun.setdefault("saldo", 0)
    for l in data["lapangan"]:
        l.setdefault("buka", DEFAULT_BUKA)
        l.setdefault("tutup", DEFAULT_TUTUP)
    for r in data["reservasi"]:
        if isinstance(r["mulai"], int):
            r["mulai"] = f"{r['mulai']:02d}:00"
        r.setdefault("denda", 0)
    return data

def muat():
    """Baca file JSON. Jika tidak ada/rusak, buat dari data awal."""
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "users": {"admin": {"password": "admin123", "role": "admin", "saldo": 0}},
            "lapangan": [
                {"id": 1, "nama": "Futsal A", "harga": 120000, "luas": 800,
                 "lokasi": "Jl. Pahlawan No. 10"},
                {"id": 2, "nama": "Badminton 1", "harga": 50000, "luas": 81,
                 "lokasi": "GOR Utama Lantai 1"},
                {"id": 3, "nama": "Basket Indoor", "harga": 100000, "luas": 420,
                 "lokasi": "Jl. Merdeka No. 5"},
                {"id": 4, "nama": "Voli Pasir", "harga": 70000, "luas": 162,
                 "lokasi": "Pantai Melawai"},
                {"id": 5, "nama": "Tenis Outdoor", "harga": 90000, "luas": 260,
                 "lokasi": "Jl. Sudirman No. 22"},
            ],
            "reservasi": [],
            "topup": [],
            "rating": [],
        }
        for l in data["lapangan"]:
            l["buka"], l["tutup"] = jam_acak(data, l["id"])
    data = rapikan(data)
    simpan(data)
    return data

def registrasi(data):
    judul("REGISTRASI AKUN")
    username = input("Username : ").strip()
    if username == "":
        print("[!] Username tidak boleh kosong!")
    elif username in data["users"]:
        print("[!] Username sudah dipakai!")
    else:
        password = input_password(f"Password (maks {MAKS_PASSWORD} karakter) : ")
        data["users"][username] = {"password": password, "role": "user", "saldo": 0}
        simpan(data)
        print("[+] Registrasi berhasil, silakan login.")

def login(data):
    """Return username jika berhasil, None jika gagal 3 kali (lalu hitung mundur)."""
    judul("LOGIN")
    for _ in range(3):
        username = input("Username : ").strip()
        password = pwinput.pwinput("Password : ", mask="*")
        if username in data["users"] and data["users"][username]["password"] == password:
            return username
        print("[!] Username/password salah!")
    hitung_mundur(WAKTU_TUNGGU)
    return None

def tampil(data):
    tabel = PrettyTable(["ID", "Nama", "Harga/Jam", "Luas (m2)", "Jam Operasional", "Lokasi", "Rating"])
    for l in data["lapangan"]:
        tabel.add_row([
            l["id"],
            l["nama"],
            "Rp " + rupiah(l["harga"]),
            l.get("luas", "-"),
            f"{l['buka']}-{l['tutup']}",
            l.get("lokasi", "-"),
            teks_rating(data, l["id"]),
        ])
    print(tabel)

def cari(data, id_cari):
    """Return data lapangan sesuai ID, atau None."""
    for l in data["lapangan"]:
        if l["id"] == id_cari:
            return l
    return None

def punya_reservasi_aktif(data, id_lapangan):
    """True jika masih ada reservasi berstatus Dipesan pada lapangan ini."""
    for r in data["reservasi"]:
        if r["id_lapangan"] == id_lapangan and r["status"] == STATUS_DIPESAN:
            return True
    return False

def jam_muat_reservasi_aktif(data, id_lapangan, buka, tutup):
    """True jika semua reservasi aktif lapangan ini masih masuk jam operasional baru."""
    for r in data["reservasi"]:
        if r["id_lapangan"] == id_lapangan and r["status"] == STATUS_DIPESAN:
            awal = ke_menit(r["mulai"])
            akhir = awal + r["durasi"] * 60
            if awal < ke_menit(buka) or akhir > ke_menit(tutup):
                return False
    return True

def tambah(data):
    judul("TAMBAH LAPANGAN")
    nama = input_teks("Nama lapangan     : ")
    harga = input_harga("Harga per jam     : ")
    luas = input_luas("Luas lapangan (m2): ")
    lokasi = input_teks("Lokasi            : ")
    buka, tutup = pilih_jam_operasional(data)
    id_baru = max([l["id"] for l in data["lapangan"]], default=0) + 1
    data["lapangan"].append({
        "id": id_baru, "nama": nama, "harga": harga, "luas": luas,
        "lokasi": lokasi, "buka": buka, "tutup": tutup,
    })
    simpan(data)
    print("[+] Data berhasil ditambah.")

def ubah(data):
    judul("UBAH LAPANGAN")
    tampil(data)
    garis()
    l = cari(data, input_angka("ID yang diubah : "))
    if l is None:
        print("[!] ID tidak ditemukan!")
        return

    pilih = pilih_menu(f"UBAH: {l['nama']}", MENU_UBAH)
    if pilih == 1:
        l["nama"] = input_teks("Nama baru        : ")
    elif pilih == 2:
        l["harga"] = input_harga("Harga baru       : ")
        print("    (Reservasi lama tetap memakai harga saat transaksi.)")
    elif pilih == 3:
        l["luas"] = input_luas("Luas baru (m2)   : ")
    elif pilih == 4:
        l["lokasi"] = input_teks("Lokasi baru      : ")
    elif pilih == 5:
        buka, tutup = pilih_jam_operasional(data, l["id"])
        if not jam_muat_reservasi_aktif(data, l["id"], buka, tutup):
            print("[!] Ada reservasi aktif di luar jam operasional baru!")
            print("    Selesaikan/batalkan dulu lewat menu Kelola Reservasi.")
            return
        l["buka"], l["tutup"] = buka, tutup
    elif pilih == 6:
        return
    else:
        print("[!] Pilihan tidak ada!")
        return
    simpan(data)
    print("[+] Data berhasil diubah.")

def urutkan_ulang_id(data):
    """Setelah ada lapangan dihapus, ID dirapatkan lagi: 1, 2, 3, ...
    ID lapangan di data reservasi ikut disesuaikan agar tetap cocok."""
    peta = {}
    for nomor, l in enumerate(data["lapangan"], start=1):
        peta[l["id"]] = nomor
        l["id"] = nomor
    for r in data["reservasi"]:
        r["id_lapangan"] = peta.get(r["id_lapangan"])
    # rating lapangan yang dihapus ikut dibuang, sisanya disesuaikan ID-nya
    data["rating"] = [x for x in data["rating"] if x["id_lapangan"] in peta]
    for x in data["rating"]:
        x["id_lapangan"] = peta[x["id_lapangan"]]

def hapus(data):
    judul("HAPUS LAPANGAN")
    tampil(data)
    garis()
    l = cari(data, input_angka("ID yang dihapus: "))
    if l is None:
        print("[!] ID tidak ditemukan!")
    elif punya_reservasi_aktif(data, l["id"]):
        print("[!] Tidak bisa dihapus, masih ada reservasi aktif di lapangan ini!")
        print("    Selesaikan/batalkan dulu lewat menu Kelola Reservasi.")
    elif konfirmasi(f"Yakin hapus '{l['nama']}'?"):
        data["lapangan"].remove(l)
        urutkan_ulang_id(data)
        simpan(data)
        print("[+] Data berhasil dihapus. ID lapangan diurutkan ulang.")
    else:
        print("[!] Penghapusan dibatalkan.")

def cari_reservasi(data, id_cari):
    for r in data["reservasi"]:
        if r["id"] == id_cari:
            return r
    return None

def waktu_mulai(r):
    """Return objek datetime saat reservasi dimulai."""
    return datetime.strptime(f"{r['tanggal']} {r['mulai']}", "%Y-%m-%d %H:%M")

def sudah_lewat(tanggal, mulai):
    """True jika jam mulai sudah lewat dari waktu sekarang."""
    awal = datetime.strptime(f"{tanggal} {mulai}", "%Y-%m-%d %H:%M")
    return awal <= datetime.now()

def ada_bentrok(data, id_lapangan, tanggal, mulai, durasi):
    """Cek apakah jadwal baru bertabrakan dengan reservasi yang masih aktif."""
    awal = ke_menit(mulai)
    akhir = awal + durasi * 60
    for r in data["reservasi"]:
        if (r["id_lapangan"] == id_lapangan and r["tanggal"] == tanggal
                and r["status"] != STATUS_BATAL):
            r_awal = ke_menit(r["mulai"])
            r_akhir = r_awal + r["durasi"] * 60
            if awal < r_akhir and akhir > r_awal:
                return True
    return False

def jadwal_terisi(data, id_lapangan, tanggal):
    """Return list jam yang sudah dipesan pada lapangan & tanggal tertentu."""
    hasil = []
    for r in data["reservasi"]:
        if (r["id_lapangan"] == id_lapangan and r["tanggal"] == tanggal
                and r["status"] != STATUS_BATAL):
            hasil.append(format_jam(r["mulai"], r["durasi"]))
    return sorted(hasil)

def tampil_reservasi(daftar, dengan_pelanggan=False):
    kolom = ["ID", "Lapangan", "Tanggal", "Jam", "Total", "Status"]
    if dengan_pelanggan:
        kolom.insert(1, "Pelanggan")
    tabel = PrettyTable(kolom)
    for r in daftar:
        baris = [
            r["id"], r["lapangan"], r["tanggal"],
            format_jam(r["mulai"], r["durasi"]),
            "Rp " + rupiah(r["total"]), r["status"],
        ]
        if dengan_pelanggan:
            baris.insert(1, r["username"])
        tabel.add_row(baris)
    print(tabel)

def reservasi_lapangan(data, username):
    judul("RESERVASI LAPANGAN")
    akun = data["users"][username]
    print(f"Saldo Anda : Rp {rupiah(akun['saldo'])}")
    tampil(data)
    garis()
    lap = cari(data, input_angka("ID lapangan : "))
    if lap is None:
        print("[!] ID lapangan tidak ditemukan!")
        return

    buka, tutup = lap["buka"], lap["tutup"]
    tanggal = input_tanggal("Tanggal main (YYYY-MM-DD) : ")
    terisi = jadwal_terisi(data, lap["id"], tanggal)
    print(f"\nJam operasional : {buka}-{tutup}")
    if terisi:
        print("Jam yang sudah dipesan:")
        for jam in terisi:
            print(f"  - {jam}")
    else:
        print("Semua jam masih kosong pada tanggal ini.")
    garis()
    paling_akhir = dari_menit(ke_menit(tutup) - 60)
    while True:
        mulai = input_jam(f"Jam mulai ({buka}-{paling_akhir}) : ")
        if ke_menit(buka) <= ke_menit(mulai) <= ke_menit(paling_akhir):
            break
        print(f"[!] Jam mulai harus antara {buka} sampai {paling_akhir}!")
    maks = min(MAKS_DURASI, (ke_menit(tutup) - ke_menit(mulai)) // 60)
    durasi = input_rentang(f"Durasi (1-{maks} jam) : ", 1, maks)

    if sudah_lewat(tanggal, mulai):
        print("[!] Jam tersebut sudah lewat, pilih jadwal yang akan datang!")
        return
    if ada_bentrok(data, lap["id"], tanggal, mulai, durasi):
        print("[!] Jadwal bentrok dengan reservasi lain, pilih jam berbeda!")
        return

    total = lap["harga"] * durasi
    garis()
    print(f"Lapangan : {lap['nama']}")
    print(f"Jadwal   : {tanggal}, {format_jam(mulai, durasi)}")
    print(f"Total    : Rp {rupiah(total)}")
    print(f"(Jika dibatalkan setelah bayar, dikenakan denda Rp {rupiah(DENDA_BATAL)})")
    garis()
    if akun["saldo"] < total:
        kurang = total - akun["saldo"]
        print(f"[!] Saldo tidak cukup, kurang Rp {rupiah(kurang)}. Silakan Top Up dulu.")
        return
    if not konfirmasi("Bayar dengan saldo?"):
        print("[!] Reservasi dibatalkan.")
        return

    akun["saldo"] -= total
    id_baru = max([r["id"] for r in data["reservasi"]], default=0) + 1
    reservasi = {
        "id": id_baru,
        "username": username,
        "id_lapangan": lap["id"],
        "lapangan": lap["nama"],
        "lokasi": lap.get("lokasi", "-"),
        "harga_jam": lap["harga"],
        "tanggal": tanggal,
        "mulai": mulai,
        "durasi": durasi,
        "total": total,
        "denda": 0,
        "status": STATUS_DIPESAN,
        "waktu_transaksi": waktu_sekarang(),
    }
    data["reservasi"].append(reservasi)
    simpan(data)
    print("[+] Pembayaran berhasil! Reservasi tercatat.")
    print(f"    Sisa saldo : Rp {rupiah(akun['saldo'])}\n")
    tampil_invoice(reservasi)

def batalkan_reservasi(data, r, denda=0):
    """Ubah status jadi Dibatalkan dan kembalikan saldo (total dikurangi denda)."""
    denda = min(denda, r["total"])
    pemilik = data["users"].get(r["username"])
    if pemilik is not None:
        pemilik["saldo"] += r["total"] - denda
    r["denda"] = denda
    r["status"] = STATUS_BATAL
    simpan(data)

def batalkan_user(data, username):
    judul("BATALKAN RESERVASI")
    aktif = [r for r in data["reservasi"]
             if r["username"] == username and r["status"] == STATUS_DIPESAN]
    if not aktif:
        print("[!] Tidak ada reservasi aktif yang bisa dibatalkan.")
        return
    tampil_reservasi(aktif)
    garis()
    r = cari_reservasi(data, input_angka("ID reservasi yang dibatalkan : "))
    if r is None or r["username"] != username or r["status"] != STATUS_DIPESAN:
        print("[!] ID tidak valid atau reservasi tidak bisa dibatalkan!")
    elif waktu_mulai(r) <= datetime.now():
        print("[!] Reservasi sudah dimulai/lewat, tidak bisa dibatalkan!")
    else:
        denda = min(DENDA_BATAL, r["total"])
        print(f"Total dibayar : Rp {rupiah(r['total'])}")
        print(f"Denda batal   : Rp {rupiah(denda)}")
        print(f"Refund        : Rp {rupiah(r['total'] - denda)}")
        garis()
        if konfirmasi(f"Batalkan reservasi #{r['id']}?"):
            batalkan_reservasi(data, r, denda)
            print(f"[+] Reservasi dibatalkan. Refund Rp {rupiah(r['total'] - denda)} masuk ke saldo.")
            print(f"    Saldo sekarang : Rp {rupiah(data['users'][username]['saldo'])}")
        else:
            print("[!] Pembatalan dibatalkan.")

def no_invoice(r):
    tanggal = r["waktu_transaksi"][:10].replace("-", "")
    return f"INV-{tanggal}-{r['id']:03d}"

def teks_invoice(r):
    """Susun isi invoice sebagai string."""
    denda = r.get("denda", 0)
    isi = (
        ("No. Invoice", no_invoice(r)),
        ("Waktu Transaksi", r["waktu_transaksi"]),
        ("Pelanggan", r["username"]),
        ("Lapangan", r["lapangan"]),
        ("Lokasi", r["lokasi"]),
        ("Tanggal Main", r["tanggal"]),
        ("Jam", format_jam(r["mulai"], r["durasi"])),
        ("Durasi", f"{r['durasi']} jam"),
        ("Harga/Jam", "Rp " + rupiah(r["harga_jam"])),
        ("Metode Bayar", "Saldo E-Money"),
        ("Status", r["status"]),
    )
    baris = ["=" * 44, "INVOICE RESERVASI LAPANGAN".center(44), "=" * 44]
    for label, nilai in isi:
        baris.append(f"{label:<17}: {nilai}")
    baris.append("-" * 44)
    baris.append(f"{'TOTAL BAYAR':<17}: Rp {rupiah(r['total'])}")
    if r["status"] == STATUS_BATAL:
        baris.append(f"{'Denda Batal':<17}: Rp {rupiah(denda)}")
        baris.append(f"{'REFUND':<17}: Rp {rupiah(r['total'] - denda)}")
    baris.append("=" * 44)
    if r["status"] == STATUS_BATAL:
        if denda > 0:
            baris.append("Reservasi dibatalkan, saldo di-refund setelah denda.")
        else:
            baris.append("Reservasi dibatalkan, saldo sudah di-refund penuh.")
    else:
        baris.append("Terima kasih telah memesan!")
    return "\n".join(baris)

def simpan_invoice(r):
    """Simpan invoice ke file .txt di folder invoice/."""
    try:
        os.makedirs(FOLDER_INVOICE, exist_ok=True)
        path = os.path.join(FOLDER_INVOICE, no_invoice(r) + ".txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(teks_invoice(r))
        print(f"[+] Invoice disimpan di: {path}")
    except OSError:
        print("[!] Gagal menyimpan file invoice.")

def tampil_invoice(r):
    print(teks_invoice(r))
    if konfirmasi("Simpan invoice ke file .txt?"):
        simpan_invoice(r)

def riwayat_user(data, username):
    judul("RIWAYAT RESERVASI")
    milik = [r for r in data["reservasi"] if r["username"] == username]
    if not milik:
        print("[!] Anda belum pernah melakukan reservasi.")
        return
    tampil_reservasi(milik)
    garis()
    id_pilih = input_angka("ID untuk cetak invoice (0 = kembali) : ")
    if id_pilih == 0:
        return
    r = cari_reservasi(data, id_pilih)
    if r is None or r["username"] != username:
        print("[!] ID tidak ditemukan di riwayat Anda!")
    else:
        print()
        tampil_invoice(r)

def rata_rating(data, id_lapangan):
    """Return (rata-rata, jumlah) rating lapangan, atau None jika belum ada."""
    nilai = [x["bintang"] for x in data["rating"] if x["id_lapangan"] == id_lapangan]
    if not nilai:
        return None
    return sum(nilai) / len(nilai), len(nilai)

def teks_rating(data, id_lapangan):
    """Contoh: '4.5/5 (2 ulasan)' atau 'Belum ada'."""
    hasil = rata_rating(data, id_lapangan)
    if hasil is None:
        return "Belum ada"
    return f"{hasil[0]:.1f}/5 ({hasil[1]} ulasan)"

def input_ulasan(pesan):
    """Ulasan boleh kosong, maksimal MAKS_ULASAN karakter."""
    while True:
        teks = input(pesan).strip()
        if len(teks) <= MAKS_ULASAN:
            return teks if teks != "" else "-"
        print(f"[!] Ulasan maksimal {MAKS_ULASAN} karakter!")

def beri_rating(data, username):
    judul("BERI RATING LAPANGAN")
    sudah_dinilai = {x["id_reservasi"] for x in data["rating"]}
    layak = [r for r in data["reservasi"]
             if r["username"] == username and r["status"] == STATUS_SELESAI
             and r["id"] not in sudah_dinilai and cari(data, r["id_lapangan"]) is not None]
    if not layak:
        print("[!] Tidak ada reservasi selesai yang bisa dinilai.")
        print("    Rating hanya untuk reservasi berstatus Selesai dan belum dinilai.")
        return
    tampil_reservasi(layak)
    garis()
    r = cari_reservasi(data, input_angka("ID reservasi yang dinilai (0 = kembali) : "))
    if r is None:
        print("[!] Dibatalkan / ID tidak ditemukan.")
        return
    if r not in layak:
        print("[!] Reservasi ini tidak bisa dinilai!")
        return
    print(f"Lapangan : {r['lapangan']} ({r['tanggal']})")
    bintang = input_rentang("Rating (1-5 bintang) : ", 1, 5)
    ulasan = input_ulasan(f"Ulasan (maks {MAKS_ULASAN} karakter, boleh kosong) : ")
    id_baru = max([x["id"] for x in data["rating"]], default=0) + 1
    data["rating"].append({
        "id": id_baru, "username": username, "id_lapangan": r["id_lapangan"],
        "id_reservasi": r["id"], "bintang": bintang, "ulasan": ulasan,
        "waktu": waktu_sekarang(),
    })
    simpan(data)
    print(f"[+] Terima kasih! Rating {'*' * bintang} ({bintang}/5) tersimpan.")

def lihat_ulasan(data):
    judul("ULASAN LAPANGAN")
    tampil(data)
    garis()
    lap = cari(data, input_angka("ID lapangan (0 = kembali) : "))
    if lap is None:
        print("[!] Dibatalkan / ID tidak ditemukan.")
        return
    daftar = [x for x in data["rating"] if x["id_lapangan"] == lap["id"]]
    print(f"\n{lap['nama']} - Rating: {teks_rating(data, lap['id'])}")
    if not daftar:
        print("[!] Belum ada ulasan untuk lapangan ini.")
        return
    tabel = PrettyTable(["User", "Bintang", "Ulasan", "Waktu"])
    tabel.align["Ulasan"] = "l"
    for x in reversed(daftar):
        tabel.add_row([x["username"], "*" * x["bintang"], x["ulasan"], x["waktu"]])
    print(tabel)

def top_up(data, username):
    judul("TOP UP SALDO")
    akun = data["users"][username]
    print(f"Saldo saat ini : Rp {rupiah(akun['saldo'])}")
    print(f"Minimal Rp {rupiah(MIN_TOPUP)}, maksimal Rp {rupiah(MAKS_TOPUP)} per transaksi")
    garis()
    nominal = input_rentang("Nominal top up : ", MIN_TOPUP, MAKS_TOPUP)
    if not konfirmasi_password(akun, f"Top up Rp {rupiah(nominal)} - konfirmasi dengan password."):
        print("[!] Top up dibatalkan.")
        return
    akun["saldo"] += nominal
    id_baru = max([t["id"] for t in data["topup"]], default=0) + 1
    data["topup"].append({
        "id": id_baru, "username": username,
        "nominal": nominal, "waktu": waktu_sekarang(),
    })
    simpan(data)
    print(f"[+] Top up berhasil! Saldo sekarang : Rp {rupiah(akun['saldo'])}")

def riwayat_topup(data, username):
    judul("RIWAYAT TOP UP")
    milik = [t for t in data["topup"] if t["username"] == username]
    if not milik:
        print("[!] Belum ada riwayat top up.")
        return
    tabel = PrettyTable(["ID", "Waktu", "Nominal"])
    for t in milik:
        tabel.add_row([t["id"], t["waktu"], "Rp " + rupiah(t["nominal"])])
    print(tabel)

def kelola_reservasi(data):
    judul("KELOLA RESERVASI")
    if not data["reservasi"]:
        print("[!] Belum ada reservasi.")
        return
    tampil_reservasi(data["reservasi"], dengan_pelanggan=True)
    pendapatan = sum(
        r["total"] if r["status"] != STATUS_BATAL else r.get("denda", 0)
        for r in data["reservasi"]
    )
    print(f"Total pendapatan (termasuk denda) : Rp {rupiah(pendapatan)}")
    garis()
    id_pilih = input_angka("ID reservasi (0 = kembali) : ")
    if id_pilih == 0:
        return
    r = cari_reservasi(data, id_pilih)
    if r is None:
        print("[!] ID tidak ditemukan!")
        return

    pilih = pilih_menu(f"RESERVASI #{r['id']} - {r['status']}", MENU_KELOLA)
    if pilih == 1:
        if r["status"] != STATUS_DIPESAN:
            print("[!] Hanya reservasi berstatus Dipesan yang bisa diselesaikan!")
        else:
            r["status"] = STATUS_SELESAI
            simpan(data)
            print("[+] Status diubah menjadi Selesai.")
    elif pilih == 2:
        if r["status"] != STATUS_DIPESAN:
            print("[!] Hanya reservasi berstatus Dipesan yang bisa dibatalkan!")
        elif konfirmasi(f"Batalkan & refund penuh Rp {rupiah(r['total'])} ke {r['username']}?"):
            batalkan_reservasi(data, r)
            print("[+] Reservasi dibatalkan, saldo user sudah dikembalikan.")
        else:
            print("[!] Dibatalkan.")
    elif pilih == 3:
        if r["status"] == STATUS_DIPESAN:
            print("[!] Reservasi aktif tidak boleh dihapus. Selesaikan/batalkan dulu!")
        elif konfirmasi(f"Hapus riwayat reservasi #{r['id']}?"):
            data["reservasi"].remove(r)
            simpan(data)
            print("[+] Riwayat reservasi dihapus.")
        else:
            print("[!] Dibatalkan.")
    elif pilih == 4:
        return
    else:
        print("[!] Pilihan tidak ada!")

def daftar_user(data):
    judul("DAFTAR USER")
    tabel = PrettyTable(["Username", "Role", "Saldo", "Jml Reservasi"])
    for nama, akun in data["users"].items():
        jumlah = len([r for r in data["reservasi"] if r["username"] == nama])
        tabel.add_row([nama, akun["role"], "Rp " + rupiah(akun["saldo"]), jumlah])
    print(tabel)

def menu_admin(data):
    while True:
        try:
            bersihkan()
            pilih = pilih_menu("MENU ADMIN", MENU_ADMIN)
            bersihkan()
            if pilih == 1:
                judul("DAFTAR LAPANGAN")
                tampil(data)
            elif pilih == 2:
                tambah(data)
            elif pilih == 3:
                ubah(data)
            elif pilih == 4:
                hapus(data)
            elif pilih == 5:
                kelola_reservasi(data)
            elif pilih == 6:
                daftar_user(data)
            elif pilih == 7:
                lihat_ulasan(data)
            elif pilih == 8:
                return
            else:
                print("[!] Pilihan tidak ada!")
            tunggu()
        except KeyboardInterrupt:
            print("\n\n[!] Ctrl+C terdeteksi. Kembali ke menu admin...")
            jeda_singkat(1.5)

def menu_user(data, username):
    while True:
        try:
            bersihkan()
            info = f"User: {username} | Saldo: Rp {rupiah(data['users'][username]['saldo'])}"
            pilih = pilih_menu("MENU USER", MENU_USER, info)
            bersihkan()
            if pilih == 1:
                judul("DAFTAR LAPANGAN")
                tampil(data)
            elif pilih == 2:
                reservasi_lapangan(data, username)
            elif pilih == 3:
                riwayat_user(data, username)
            elif pilih == 4:
                batalkan_user(data, username)
            elif pilih == 5:
                top_up(data, username)
            elif pilih == 6:
                riwayat_topup(data, username)
            elif pilih == 7:
                beri_rating(data, username)
            elif pilih == 8:
                lihat_ulasan(data)
            elif pilih == 9:
                return
            else:
                print("[!] Pilihan tidak ada!")
            tunggu()
        except KeyboardInterrupt:
            print("\n\n[!] Ctrl+C terdeteksi. Kembali ke menu user...")
            jeda_singkat(1.5)

def jeda_singkat(detik):
    """Jeda singkat; Ctrl+C saat jeda diabaikan agar tidak keluar dari program."""
    try:
        time.sleep(detik)
    except KeyboardInterrupt:
        pass

def main():
    data = muat()
    while True:
        try:
            bersihkan()
            pilih = pilih_menu("RESERVASI LAPANGAN OLAHRAGA", MENU_UTAMA)
            bersihkan()
            if pilih == 1:
                username = login(data)
                if username is None:
                    pass
                elif data["users"][username]["role"] == "admin":
                    menu_admin(data)
                    continue
                else:
                    menu_user(data, username)
                    continue
            elif pilih == 2:
                registrasi(data)
            elif pilih == 3:
                print("Terima kasih!")
                break
            else:
                print("[!] Pilihan tidak ada!")
            tunggu()
        except KeyboardInterrupt:
            print("\n\n[!] Ctrl+C terdeteksi. Kembali ke menu awal...")
            jeda_singkat(1.5)

if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\n\n[!] Input ditutup. Program dihentikan.")