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

tk.Button(sidebar, text="Barang", width=20).pack(pady=5)
tk.Button(sidebar, text="Pembayaran", width=20).pack(pady=5)
tk.Button(sidebar, text="Karyawan", width=20).pack(pady=5)
tk.Button(sidebar, text="Member", width=20).pack(pady=5)

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

# Barang

# Tabel
columns = ("nama", "jumlah", "harga", "aksi")

table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("nama", text="Nama Barang")
table.heading("jumlah", text="Jumlah")
table.heading("harga", text="Harga")
table.heading("aksi", text="Aksi")

table.column("nama", width=100)
table.column("jumlah", width=100, anchor="center")
table.column("harga", width=150, anchor="center")
table.column("aksi", width=120, anchor="center")

table.pack(side="bottom", anchor="n", pady=50, padx=50, fill="x")

def tambah():
    window = tk.Toplevel(root)
    window.title("Tambah Barang")
    window.geometry("800x600")

    def submit():
        nama = e1.get()
        jumlah = e2.get()
        harga = e3.get()

        if not nama or not jumlah or not harga:
            messagebox.showerror("Error", "Semua field wajib diisi")
            return
        
        if jumlah.isdigit() and harga.isdigit():
            jumlah = int(jumlah)
            harga = int(harga)
        else:
            messagebox.showerror("Error", "Jumlah/Harga tidak valid")
            return
        
        table.insert("", "end", values=(nama, jumlah, harga, "✏️ Edit | 🗑 Hapus"))
        window.destroy()
    
    def on_table_click(event):
        item = table.identify_row(event.y)
        column = table.identify_column(event.x)

        if not item:
            return
        
        if column == "#4":
            x, y, width, height = table.bbox(item, column)
        click_x = event.x - x

        if click_x < width / 2:
            edit_data(item)
        else:
            delete_data(item)

    table.bind("<Button-1>", on_table_click)

    def delete_data(item):
        confirm = messagebox.askyesno(
            "Hapus",
            "Yakin ingin menghapus data ini?"
        )
        if confirm:
            table.delete(item)

    def edit_data(item):
        data = table.item(item, "values")

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
            table.item(
                item,
                values=(e1.get(), e2.get(), e3.get(), "✏️ Edit | 🗑 Hapus")
            )
            window.destroy()

        tk.Button(window, text="Update", command=update).grid(row=3, column=1, pady=15)


    tk.Label(window, text="Nama Barang").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(window, text="Jumlah").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(window, text="Harga").grid(row=2, column=0, padx=10, pady=5)

    e1 = tk.Entry(window)
    e2 = tk.Entry(window)
    e3 = tk.Entry(window)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    tk.Button(window, text="Submit", command=submit).grid(row=3, column=1, pady=15)

buttonTambah = tk.Button(root, text="Tambah Barang", command=tambah)
buttonTambah.pack(side="right", anchor="n", pady=30, padx=30)
root.mainloop()