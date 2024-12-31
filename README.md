# struktur database

#table produk
CREATE TABLE produk (
    id_produk INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(255) NOT NULL,
    harga_produk DECIMAL(10, 2) NOT NULL
);

#table transaksi
CREATE TABLE transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_produk INT NOT NULL,
    jumlah_produk INT NOT NULL,
    total_harga DECIMAL(10, 2) NOT NULL,
    tanggal_transaksi DATE NOT NULL,
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
);
