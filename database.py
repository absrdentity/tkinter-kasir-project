import sqlite3
from datetime import datetime

conn = sqlite3.connect("DataMaster.db")
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Kasir(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Kasir TEXT UNIQUE,
                    Password TEXT NOT NULL,
                    Kode_Kasir TEXT NOT NULL,
                    Telepon INTEGER UNIQUE
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Barang(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Barang TEXT UNIQUE,
                    Harga INTEGER NOT NULL,
                    Stok INTEGER NOT NULL
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Member(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Member TEXT NOT NULL,
                    Kode_Member TEXT UNIQUE,
                    Masa_Aktif INTEGER NOT NULL
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Riwayat(
                    id_Transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
                    Pembeli TEXT NOT NULL,
                    Status TEXT NOT NULL,
                    Harga_Total INTEGER NOT NULL,
                    Waktu_Transaksi TEXT NOT NULL
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Detail_Transaksi(
                    id_Detail INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_Transaksi INTEGER NOT NULL,
                    Nama_Barang TEXT NOT NULL,
                    Harga_Barang INTEGER NOT NULL,
                    Jumlah INTEGER NOT NULL,
                    Subtotal INTEGER NOT NULL,
                    FOREIGN KEY (id_Transaksi)
                         REFERENCES Riwayat(id_Transaksi)
                         ON UPDATE CASCADE
                         ON DELETE CASCADE
               )
               """)

conn.commit()
conn.close()