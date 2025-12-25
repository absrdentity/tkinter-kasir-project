from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk

root = tk.Tk()
root.geometry("1200x800")
root.title("Program Sistem Kasir")

# Hamburger Menu
topbar = tk.Frame(root, bg="#2c3e50", height=50)
topbar.pack(side="top", fill="x")

menu_btn = tk.Button(
    topbar,
    text="☰",
    font=("Arial", 18),
    bg="#2c3e50",
    fg="white",
    bd=0
)
menu_btn.pack(side="left", padx=15)

# ================= MAIN CONTAINER =================
main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True)

# ================= SIDEBAR =================
sidebar = tk.Frame(main_container, bg="#34495e", width=250)

tk.Label(
    sidebar,
    bg="#34495e",
    fg="white",
    font=("Arial", 14, "bold")
).pack(pady=20)

btn_barang = tk.Button(sidebar, text="Barang", width=20)
btn_barang.pack(pady=5)

btn_pembayaran = tk.Button(sidebar, text="Pembayaran", width=20)
btn_pembayaran.pack(pady=5)

btn_karyawan = tk.Button(sidebar, text="Karyawan", width=20)
btn_karyawan.pack(pady=5)

btn_member = tk.Button(sidebar, text="Member", width=20)
btn_member.pack(pady=5)

# ================= CONTENT =================
content = tk.Frame(main_container, bg="#ecf0f1")
content.pack(side="right", fill="both", expand=True)

# ================= TOGGLE FUNCTION =================
sidebar_visible = False

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar.pack_forget()
        sidebar_visible = False
    else:
        sidebar.pack(side="left", fill="y")
        sidebar_visible = True

menu_btn.config(command=toggle_sidebar)

pages = {}

# Function to show pages
def show_page(name):
    for page in pages.values():
        page.pack_forget()
    pages[name].pack(fill="both", expand=True)

# ================= BARANG PAGE =================
page_barang = tk.Frame(content, bg="#ecf0f1")

columns = ("nama", "jumlah", "harga", "aksi")

table_barang = ttk.Treeview(
    page_barang, 
    columns=columns, 
    show="headings",
    height=10
)
table_barang.heading("nama", text="Nama Barang")
table_barang.heading("jumlah", text="Jumlah")
table_barang.heading("harga", text="Harga")
table_barang.heading("aksi", text="Aksi")

table_barang.column("nama", width=100)
table_barang.column("jumlah", width=100, anchor="center")
table_barang.column("harga", width=150, anchor="center")
table_barang.column("aksi", width=120, anchor="center")

def on_table_click(event):
    item = table_barang.identify_row(event.y)
    column = table_barang.identify_column(event.x)

    if not item or column != "#4":
        return

    x, y, width, height = table_barang.bbox(item, column)
    click_x = event.x - x

    if click_x < width / 2:
        edit_data(item)
    else:
        delete_data(item)

table_barang.bind("<Button-1>", on_table_click)

def delete_data(item):
    confirm = messagebox.askyesno(
        "Hapus",
        "Yakin ingin menghapus data ini?"
    )
    if confirm:
        table_barang.delete(item)

def tambah():
    win = tk.Toplevel(root)
    win.title("Tambah Barang")
    win.geometry("400x250")

    tk.Label(win, text="Nama").grid(row=0, column=0)
    tk.Label(win, text="Jumlah").grid(row=1, column=0)
    tk.Label(win, text="Harga").grid(row=2, column=0)

    e1, e2, e3 = tk.Entry(win), tk.Entry(win), tk.Entry(win)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    def submit():
        nama = e1.get().strip()
        jumlah = e2.get().strip()
        harga = e3.get().strip()

        if not nama:
            messagebox.showerror("Error", "Nama tidak boleh kosong")
            return
        if not jumlah.isdigit() or not harga.isdigit():
            messagebox.showerror("Error", "Jumlah dan Harga harus angka")
            return

        table_barang.insert(
            "",
            "end",
            values=(nama, jumlah, harga, "✏️ Edit | 🗑 Hapus")
        )
        win.destroy()

    tk.Button(win, text="Simpan", command=submit).grid(row=3, column=1, pady=10)

def edit_data(item):
    data = table_barang.item(item, "values")

    window = tk.Toplevel(root)
    window.title("Edit Barang")
    window.geometry("400x250")

    tk.Label(window, text="Nama Barang").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(window, text="Jumlah").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(window, text="Harga").grid(row=2, column=0, padx=10, pady=5)

    e1 = tk.Entry(window)
    e2 = tk.Entry(window)
    e3 = tk.Entry(window)

    e1.insert(0, data[0])
    e2.insert(0, data[1])
    e3.insert(0, data[2])

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    def update():
        nama = e1.get().strip()
        jumlah = e2.get().strip()
        harga = e3.get().strip()

        if not nama:
            messagebox.showerror("Error", "Nama tidak boleh kosong")
            return
        if not jumlah.isdigit() or not harga.isdigit():
            messagebox.showerror("Error", "Jumlah dan Harga harus angka")
            return

        table_barang.item(
            item,
            values=(nama, jumlah, harga, "✏️ Edit | 🗑 Hapus")
        )
        window.destroy()

    tk.Button(window, text="Update", command=update).grid(row=3, column=1, pady=15)

tk.Button(
    page_barang,
    text="Tambah Barang",
    command=tambah
).pack(anchor="e", padx=20, pady=10)

table_barang.pack(fill="both", expand=True, padx=20, pady=10)

pages["barang"] = page_barang

# ================= PEMBAYARAN PAGE =================
page_pembayaran = tk.Frame(content, bg="#ecf0f1")

tk.Label(page_pembayaran, text="Halaman Pembayaran", font=("Arial", 20)).pack(pady=20)

# Tambahkan elemen untuk input pembayaran, misalnya:
tk.Label(page_pembayaran, text="Total Belanja:").pack()
entry_total = tk.Entry(page_pembayaran)
entry_total.pack()

tk.Label(page_pembayaran, text="Bayar:").pack()
entry_bayar = tk.Entry(page_pembayaran)
entry_bayar.pack()

def proses_pembayaran():
    try:
        total = float(entry_total.get())
        bayar = float(entry_bayar.get())
        kembalian = bayar - total
        if kembalian < 0:
            messagebox.showerror("Error", "Uang tidak cukup")
        else:
            messagebox.showinfo("Pembayaran", f"Kembalian: {kembalian}")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid")

tk.Button(page_pembayaran, text="Proses Pembayaran", command=proses_pembayaran).pack(pady=10)

pages["pembayaran"] = page_pembayaran

# ================= KARYAWAN PAGE =================
page_karyawan = tk.Frame(content, bg="#ecf0f1")

tk.Label(page_karyawan, text="Halaman Karyawan", font=("Arial", 20)).pack(pady=20)

# Tambahkan tabel atau form untuk karyawan
columns_karyawan = ("id", "nama", "jabatan")

table_karyawan = ttk.Treeview(page_karyawan, columns=columns_karyawan, show="headings")
table_karyawan.heading("id", text="ID")
table_karyawan.heading("nama", text="Nama")
table_karyawan.heading("jabatan", text="Jabatan")

table_karyawan.column("id", width=100)
table_karyawan.column("nama", width=150)
table_karyawan.column("jabatan", width=150)

table_karyawan.pack(fill="both", expand=True, padx=20, pady=20)

pages["karyawan"] = page_karyawan

# ================= MEMBER PAGE =================
page_member = tk.Frame(content, bg="#ecf0f1")

tk.Label(page_member, text="Halaman Member", font=("Arial", 20)).pack(pady=20)

columns_member = ("id", "nama", "kode", "masa_aktif")

table_member = ttk.Treeview(page_member, columns=columns_member, show="headings")
table_member.heading("id", text="ID")
table_member.heading("nama", text="Nama")
table_member.heading("kode", text="Kode")
table_member.heading("masa_aktif", text="Masa Aktif")

table_member.column("id", width=100)
table_member.column("nama", width=100, anchor="center")
table_member.column("kode", width=150, anchor="center")
table_member.column("masa_aktif", width=120, anchor="center")

table_member.pack(fill="both", expand=True, padx=20, pady=20)

pages["member"] = page_member

# Connect buttons to show pages
btn_barang.config(command=lambda: show_page("barang"))
btn_pembayaran.config(command=lambda: show_page("pembayaran"))
btn_karyawan.config(command=lambda: show_page("karyawan"))
btn_member.config(command=lambda: show_page("member"))

# Show default page
show_page("barang")

root.mainloop()