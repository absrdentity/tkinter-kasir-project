import sqlite3
from datetime import datetime

# Inisialisasi koneksi database (biarkan terbuka selama aplikasi berjalan)
conn = sqlite3.connect("DataMaster.db")
cr = conn.cursor()

# Buat tabel jika belum ada
cr.execute("""CREATE TABLE IF NOT EXISTS Kasir(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT UNIQUE,
    password TEXT,
    kode TEXT
)""")

cr.execute("""CREATE TABLE IF NOT EXISTS Barang(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT UNIQUE,
    harga INTEGER,
    stok INTEGER
)""")

cr.execute("""CREATE TABLE IF NOT EXISTS Member(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    kode TEXT UNIQUE,
    masa_aktif TEXT
)""")

cr.execute("""CREATE TABLE IF NOT EXISTS Riwayat(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT,
    total INTEGER,
    jumlah_barang INTEGER,
    kasir TEXT
)""")

conn.commit()  # Commit pembuatan tabel

# --- CLASSES ---
class User:
    def __init__(self, nama, kode):
        self._nama = nama
        self._kode = kode

class Kasir(User):
    @staticmethod
    def tambah(nama, password, kode):
        cr.execute("INSERT INTO Kasir VALUES(NULL,?,?,?)", (nama, password, kode))
        conn.commit()

    @staticmethod
    def edit(nama, password):
        cr.execute("UPDATE Kasir SET password=? WHERE nama=?", (password, nama))
        conn.commit()

    @staticmethod
    def hapus(nama):
        cr.execute("DELETE FROM Kasir WHERE nama=?", (nama,))
        conn.commit()

    @staticmethod
    def semua():
        cr.execute("SELECT nama, kode FROM Kasir")
        return cr.fetchall()

class Pembayaran:
    def __init__(self):
        self.keranjang = []
        self.total_awal = 0
        self.diskon = 0
        self.total_akhir = 0

    def tambah_barang(self, nama, harga, jumlah):
        subtotal = harga * jumlah
        self.keranjang.append((nama, harga, jumlah, subtotal))
        self.total_awal += subtotal
        self.total_akhir = self.total_awal

    def hitung_diskon(self, kode_member):
        if not kode_member:
            self.diskon = 0
            self.total_akhir = self.total_awal
            return
        cr.execute("SELECT masa_aktif FROM Member WHERE kode=?", (kode_member,))
        m = cr.fetchone()
        if m and datetime.strptime(m[0], "%Y-%m-%d") > datetime.now():
            # Jika masa aktif masih berlaku, berikan diskon 10% sebagai contoh (sesuaikan jika perlu)
            self.diskon = self.total_awal * 10 // 100
            self.total_akhir = self.total_awal - self.diskon
        else:
            self.diskon = 0
            self.total_akhir = self.total_awal

    def simpan_transaksi(self, kasir_aktif):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        jumlah_item = sum(b[2] for b in self.keranjang)
        cr.execute("INSERT INTO Riwayat (tanggal, total, jumlah_barang, kasir) VALUES (?,?,?,?)",
                   (waktu, self.total_akhir, jumlah_item, kasir_aktif))
        conn.commit()