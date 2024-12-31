import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Koneksi ke database MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Ganti dengan password MySQL Anda jika ada
            database="retail_db"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Koneksi database gagal: {e}")
        return None

# Kelas utama aplikasi
class RetailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Management App")
        self.root.geometry("900x600")

        # Tab Control untuk Produk dan Transaksi
        tab_control = ttk.Notebook(root)
        self.tab_produk = ttk.Frame(tab_control)
        self.tab_transaksi = ttk.Frame(tab_control)

        tab_control.add(self.tab_produk, text="Manajemen Produk")
        tab_control.add(self.tab_transaksi, text="Proses Transaksi")
        tab_control.pack(expand=1, fill="both")

        # Inisialisasi komponen
        self.init_produk_tab()
        self.init_transaksi_tab()

    def init_produk_tab(self):
        frame_form = tk.Frame(self.tab_produk)
        frame_form.pack(pady=10, padx=10, fill="x")

        # Form untuk input data produk
        tk.Label(frame_form, text="Nama Produk:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nama_produk = tk.Entry(frame_form)
        self.entry_nama_produk.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Harga Produk:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_harga_produk = tk.Entry(frame_form)
        self.entry_harga_produk.grid(row=1, column=1, padx=10, pady=5)

        btn_tambah = tk.Button(frame_form, text="Tambah Produk", command=self.tambah_produk, bg="green", fg="white")
        btn_tambah.grid(row=2, column=1, pady=10, sticky="w")

        btn_update = tk.Button(frame_form, text="Update Produk", command=self.update_produk, bg="orange", fg="white")
        btn_update.grid(row=3, column=1, pady=10, sticky="w")

        # Tabel untuk daftar produk
        frame_table = tk.Frame(self.tab_produk)
        frame_table.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree_produk = ttk.Treeview(frame_table, columns=("ID", "Nama", "Harga"), show="headings")
        self.tree_produk.heading("ID", text="ID")
        self.tree_produk.heading("Nama", text="Nama Produk")
        self.tree_produk.heading("Harga", text="Harga Produk")
        self.tree_produk.column("ID", width=50, anchor="center")
        self.tree_produk.column("Nama", width=200, anchor="w")
        self.tree_produk.column("Harga", width=100, anchor="center")
        self.tree_produk.pack(fill="both", expand=True)

        # Tombol Hapus Produk
        btn_hapus_produk = tk.Button(self.tab_produk, text="Hapus Produk", command=self.hapus_produk, bg="red", fg="white")
        btn_hapus_produk.pack(pady=5)

        self.load_produk()

    def tambah_produk(self):
        nama = self.entry_nama_produk.get()
        harga = self.entry_harga_produk.get()

        if not nama or not harga:
            messagebox.showwarning("Input Error", "Nama dan harga produk harus diisi!")
            return

        try:
            harga = float(harga)
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produk (nama_produk, harga_produk) VALUES (%s, %s)", (nama, harga))
                conn.commit()
                conn.close()
                self.entry_nama_produk.delete(0, tk.END)
                self.entry_harga_produk.delete(0, tk.END)
                self.load_produk()
                messagebox.showinfo("Success", "Produk berhasil ditambahkan!")
        except ValueError:
            messagebox.showerror("Input Error", "Harga harus berupa angka!")

    def update_produk(self):
        selected_item = self.tree_produk.selection()
        if not selected_item:
            messagebox.showwarning("Update Error", "Pilih produk yang akan diupdate!")
            return

        item = self.tree_produk.item(selected_item)
        produk_id = item["values"][0]
        nama = self.entry_nama_produk.get()
        harga = self.entry_harga_produk.get()

        if not nama or not harga:
            messagebox.showwarning("Input Error", "Nama dan harga produk harus diisi!")
            return

        try:
            harga = float(harga)
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE produk SET nama_produk = %s, harga_produk = %s WHERE id_produk = %s",
                    (nama, harga, produk_id)
                )
                conn.commit()
                conn.close()
                self.entry_nama_produk.delete(0, tk.END)
                self.entry_harga_produk.delete(0, tk.END)
                self.load_produk()
                messagebox.showinfo("Success", "Produk berhasil diupdate!")
        except ValueError:
            messagebox.showerror("Input Error", "Harga harus berupa angka!")

    def hapus_produk(self):
        selected_item = self.tree_produk.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Pilih produk yang akan dihapus!")
            return

        item = self.tree_produk.item(selected_item)
        produk_id = item["values"][0]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produk WHERE id_produk = %s", (produk_id,))
            conn.commit()
            conn.close()
            self.load_produk()
            messagebox.showinfo("Success", "Produk berhasil dihapus!")

    def load_produk(self):
        for item in self.tree_produk.get_children():
            self.tree_produk.delete(item)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_produk, nama_produk, harga_produk FROM produk")
            for row in cursor.fetchall():
                self.tree_produk.insert("", "end", values=row)
            conn.close()

    def init_transaksi_tab(self):
        frame_form = tk.Frame(self.tab_transaksi)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Nama Produk:").grid(row=0, column=0, padx=10, pady=5)
        self.combo_produk = ttk.Combobox(frame_form, state="readonly")
        self.combo_produk.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Jumlah:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_jumlah = tk.Entry(frame_form)
        self.entry_jumlah.grid(row=1, column=1, padx=10, pady=5)

        btn_tambah_transaksi = tk.Button(frame_form, text="Tambah Transaksi", command=self.tambah_transaksi, bg="green", fg="white")
        btn_tambah_transaksi.grid(row=2, column=1, pady=10, sticky="w")

        frame_table = tk.Frame(self.tab_transaksi)
        frame_table.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree_transaksi = ttk.Treeview(frame_table, columns=("ID", "Nama Produk", "Jumlah", "Total Harga", "Tanggal"), show="headings")
        self.tree_transaksi.heading("ID", text="ID")
        self.tree_transaksi.heading("Nama Produk", text="Nama Produk")
        self.tree_transaksi.heading("Jumlah", text="Jumlah")
        self.tree_transaksi.heading("Total Harga", text="Total Harga")
        self.tree_transaksi.heading("Tanggal", text="Tanggal")

        self.tree_transaksi.column("ID", width=50, anchor="center")
        self.tree_transaksi.column("Nama Produk", width=200, anchor="w")
        self.tree_transaksi.column("Jumlah", width=100, anchor="center")
        self.tree_transaksi.column("Total Harga", width=150, anchor="center")
        self.tree_transaksi.column("Tanggal", width=150, anchor="center")
        self.tree_transaksi.pack(fill="both", expand=True)

        self.load_transaksi()
        self.load_combo_produk()

    def tambah_transaksi(self):
        produk_nama = self.combo_produk.get()
        jumlah = self.entry_jumlah.get()

        if not produk_nama or not jumlah:
            messagebox.showwarning("Input Error", "Nama produk dan jumlah harus diisi!")
            return

        try:
            jumlah = int(jumlah)
            if jumlah <= 0:
                raise ValueError("Jumlah harus lebih dari 0")

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_produk, harga_produk FROM produk WHERE nama_produk = %s", (produk_nama,))
                produk = cursor.fetchone()

                if not produk:
                    messagebox.showerror("Error", "Produk tidak ditemukan di database!")
                    return

                produk_id, harga = produk
                total_harga = jumlah * harga
                tanggal = datetime.now().strftime("%Y-%m-%d")

                cursor.execute(
                    "INSERT INTO transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi) VALUES (%s, %s, %s, %s)",
                    (produk_id, jumlah, total_harga, tanggal)
                )
                conn.commit()
                conn.close()

                self.entry_jumlah.delete(0, tk.END)
                self.load_transaksi()
                messagebox.showinfo("Success", "Transaksi berhasil ditambahkan!")
        except ValueError:
            messagebox.showerror("Input Error", "Jumlah harus berupa angka positif!")

    def load_transaksi(self):
        for item in self.tree_transaksi.get_children():
            self.tree_transaksi.delete(item)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id_transaksi, p.nama_produk, t.jumlah_produk, t.total_harga, t.tanggal_transaksi
                FROM transaksi t
                JOIN produk p ON t.id_produk = p.id_produk
            """)
            for row in cursor.fetchall():
                self.tree_transaksi.insert("", "end", values=row)
            conn.close()

    def load_combo_produk(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nama_produk FROM produk")
            produk_list = [row[0] for row in cursor.fetchall()]
            self.combo_produk["values"] = produk_list
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RetailApp(root)
    root.mainloop()
