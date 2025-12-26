from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime
from database import Kasir, User, Pembayaran, cr

# Buat root utama di awal
root = tk.Tk()
root.title("Program Sistem Kasir")
root.geometry("1200x800")
root.withdraw()  # Sembunyikan root sampai login berhasil

kasir_login = None

def buka_form_kasir():
    w = tk.Toplevel(root)  # Gunakan root sebagai master
    w.title("Form Kasir Baru")
    w.geometry("400x450")
    w.configure(bg="white")
    w.grab_set()

    tk.Label(w, text="MANAJEMEN KASIR", font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=20)

    def create_input(label_text, is_pass=False):
        tk.Label(w, text=label_text, font=("Arial", 10), bg="white", fg="#666").pack(anchor="w", padx=50)
        entry = tk.Entry(w, font=("Arial", 12), width=25, bd=1, relief="solid")
        if is_pass: entry.config(show="*")
        entry.pack(pady=(2, 15), padx=50)
        return entry

    e1 = create_input("Nama Lengkap")
    e2 = create_input("Password", True)
    e3 = create_input("ID Kasir")

    def simpan_data():
        if e1.get() and e2.get() and e3.get():
            try:
                # Periksa apakah ID Kasir sudah ada
                cr.execute("SELECT kode FROM Kasir WHERE kode=?", (e3.get(),))
                if cr.fetchone():
                    messagebox.showerror("Error", "ID Kasir sudah ada!")
                    return
                # Tambahkan kasir baru
                Kasir.tambah(e1.get(), e2.get(), e3.get())
                messagebox.showinfo("Sukses", f"Kasir {e1.get()} berhasil ditambahkan!")
                w.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambah kasir: {str(e)}")
        else:
            messagebox.showwarning("Peringatan", "Isi semua data!")

    tk.Button(w, text="SIMPAN KASIR", command=simpan_data, bg="#28a745", fg="white", 
              font=("Arial", 11, "bold"), width=20, pady=10, bd=0, cursor="hand2").pack(pady=20)

def login():
    global kasir_login
    nama = e_user.get()
    pw = e_pass.get()
    cr.execute("SELECT nama FROM Kasir WHERE nama=? AND password=?", (nama, pw))
    result = cr.fetchone()
    if result:
        kasir_login = nama
        login_win.destroy()  # Tutup window login
        root.deiconify()  # Tampilkan root utama
        tampilan()  # Panggil tampilan di root
    else:
        messagebox.showerror("Error", "Login Gagal!")

def tampilan():
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

    btn_riwayat = tk.Button(sidebar, text="Riwayat", width=20)
    btn_riwayat.pack(pady=5)

    # Pack sidebar secara default (visible)
    sidebar.pack(side="left", fill="y")

    # ================= CONTENT =================
    content = tk.Frame(main_container, bg="#ecf0f1")
    content.pack(side="right", fill="both", expand=True)

    # ================= TOGGLE FUNCTION =================
    sidebar_visible = True  # Ubah ke True karena sidebar sudah packed

    def toggle_sidebar():
        nonlocal sidebar_visible  # Gunakan nonlocal karena sidebar_visible di dalam fungsi
        if sidebar_visible:
            sidebar.pack_forget()
            sidebar_visible = False
        else:
            sidebar.pack(side="left", fill="y")
            sidebar_visible = True

    menu_btn.config(command=toggle_sidebar)

    pages = {}

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

    # ================= RIWAYAT PAGE =================
    page_riwayat = tk.Frame(content, bg="#ecf0f1")

    tk.Label(page_riwayat, text="Halaman Riwayat", font=("Arial", 20)).pack(pady=20)

    columns_riwayat = ("tanggal", "total", "kasir")

    table_riwayat = ttk.Treeview(page_riwayat, columns=columns_riwayat, show="headings")
    table_riwayat.heading("tanggal", text="Tanggal")
    table_riwayat.heading("total", text="Total")
    table_riwayat.heading("kasir", text="Kasir")

    table_riwayat.column("tanggal", width=150)
    table_riwayat.column("total", width=100, anchor="center")
    table_riwayat.column("kasir", width=150, anchor="center")

    table_riwayat.pack(fill="both", expand=True, padx=20, pady=20)

    pages["riwayat"] = page_riwayat

    # Fungsi untuk menampilkan halaman
    def show_barang():
        for page in pages.values():
            page.pack_forget()
        pages["barang"].pack(fill="both", expand=True)

    def show_pembayaran():
        for page in pages.values():
            page.pack_forget()
        pages["pembayaran"].pack(fill="both", expand=True)

    def show_karyawan():
        for page in pages.values():
            page.pack_forget()
        pages["karyawan"].pack(fill="both", expand=True)

    def show_member():
        for page in pages.values():
            page.pack_forget()
        pages["member"].pack(fill="both", expand=True)

    def show_riwayat():
        for page in pages.values():
            page.pack_forget()
        pages["riwayat"].pack(fill="both", expand=True)

    # Connect buttons to show pages
    btn_barang.config(command=show_barang)
    btn_pembayaran.config(command=show_pembayaran)
    btn_karyawan.config(command=show_karyawan)
    btn_member.config(command=show_member)
    btn_riwayat.config(command=show_riwayat)

    # Show default page
    show_barang()

# Login Window sebagai Toplevel
login_win = tk.Toplevel(root)
login_win.title("Login Kasir")
login_win.geometry("400x450")
login_win.configure(bg="#f0f2f5")

main_frame = tk.Frame(login_win, bg="white", padx=30, pady=30, highlightbackground="#d1d1d1", highlightthickness=1)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(main_frame, text="LOGIN KASIR", font=("Arial", 16, "bold"), bg="white", fg="#333").pack(pady=(0, 20))
tk.Label(main_frame, text="Nama Kasir", bg="white").pack(anchor="w")
e_user = tk.Entry(main_frame, font=("Arial", 12), width=25, bd=1, relief="solid")
e_user.pack(pady=5)
tk.Label(main_frame, text="Password", bg="white").pack(anchor="w")
e_pass = tk.Entry(main_frame, font=("Arial", 12), width=25, bd=1, relief="solid", show="*")
e_pass.pack(pady=5)

tk.Button(main_frame, text="MASUK", command=login, bg="#007bff", fg="white", font=("Arial", 11, "bold"), width=20, pady=8, bd=0).pack(pady=10)
tk.Button(main_frame, text="Daftar Kasir Baru", command=buka_form_kasir, bg="white", fg="#007bff", bd=0, cursor="hand2").pack()

root.mainloop()