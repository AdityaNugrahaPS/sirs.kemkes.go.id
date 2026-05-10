# ML Features

[← Kembali ke README](../README.md)

---

## data_ml_features.csv

Dataset wide-format hasil merge semua data mentah. Setiap baris = 1 RS.

| Keterangan | Nilai |
|------------|-------|
| Jumlah RS | **3.304** |
| Jumlah kolom | **802** |
| Ukuran file | ~10.6 MB |

### Komposisi Kolom

| Kelompok | Jumlah Kolom | Deskripsi |
|----------|-------------|-----------|
| Profil dasar | 17 | Nama, jenis, kelas, kepemilikan, luas, dll |
| Agregat (`total_*`) | 3 | `total_tt`, `total_layanan`, `total_sdm` |
| Tempat Tidur (`tt_*`) | 32 | Jumlah TT per tipe |
| Layanan (`layan_*`) | 316 | Binary 1/0 per jenis layanan |
| SDM per jenis (`sdm_*`) | 391 | Jumlah per jenis tenaga |
| SDM per grup (`grpsdm_*`) | 43 | Jumlah per grup tenaga |

---

## data_ml_clean.csv

Dataset bersih hasil EDA & cleaning, siap untuk clustering/segmentasi.

| Keterangan | Nilai |
|------------|-------|
| Jumlah RS | **3.292** |
| Jumlah kolom | **792** |
| Fitur untuk clustering | **785** |

### Proses Cleaning

| Tahap | Keterangan |
|-------|------------|
| Drop 10 kolom | `lon`, `lat`, `akreditasi`, `kecamatan` (100% kosong), `luas_tanah`, `luas_bangunan` (banyak missing), `nama_rs`, `direktur`, `alamat`, `telepon` (bukan fitur ML) |
| Drop 12 RS | RS dengan semua fitur bernilai 0 |
| Konversi tipe data | Semua fitur dikonversi ke `float64` |
| Scaling | Menggunakan `RobustScaler` (tahan terhadap outlier) |

### Komposisi Fitur Clustering

| Kelompok Fitur | Jumlah |
|----------------|--------|
| Agregat (`total_*`) | 3 |
| Tempat Tidur (`tt_*`) | 32 |
| Layanan (`layan_*`) | 316 |
| SDM per jenis (`sdm_*`) | 391 |
| SDM per grup (`grpsdm_*`) | 43 |
| **Total** | **785** |
