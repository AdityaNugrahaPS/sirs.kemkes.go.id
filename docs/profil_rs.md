# Data Profil RS

[← Kembali ke README](../README.md)

Dataset info dasar setiap rumah sakit di Indonesia.

---

## Struktur Kolom

| Kolom | Deskripsi |
|-------|-----------|
| `kode_rs` | Kode unik RS (7 digit) |
| `nama_rs` | Nama rumah sakit |
| `jenis` | Jenis RS (Umum / Khusus) |
| `kelas` | Kelas RS (A / B / C / D) |
| `status_blu` | Status BLU / BLUD / Non BLU |
| `kepemilikan` | Pemkab / Pemprov / TNI / Swasta / dll |
| `direktur` | Nama direktur |
| `alamat` | Alamat lengkap |
| `telepon` | Nomor telepon |
| `luas_tanah` | Luas tanah (m²) |
| `luas_bangunan` | Luas bangunan (m²) |
| `akreditasi` | Status akreditasi |
| `provinsi` | Provinsi |
| `kabkota` | Kabupaten / Kota |
| `kecamatan` | Kecamatan |
| `lat` | Koordinat latitude |
| `lon` | Koordinat longitude |

---

## Statistik

| Keterangan | Nilai |
|------------|-------|
| Total RS | **3.304** |
| Kolom | 17 |

---

## Distribusi Jenis RS

| Jenis | Jumlah |
|-------|--------|
| Rumah Sakit Umum | 2.792 |
| Rumah Sakit Khusus Ibu dan Anak | 314 |
| Rumah Sakit Khusus Jiwa | 42 |
| Rumah Sakit Khusus Mata | 40 |
| Rumah Sakit Khusus Gigi dan Mulut | 36 |
| Rumah Sakit Khusus Bedah | 32 |
| Rumah Sakit Khusus Jantung | 13 |
| Rumah Sakit Khusus Paru | 9 |
| Rumah Sakit Khusus Orthopedi | 7 |
| Lainnya (Kanker, THT-KL, Otak, dll) | 19 |

---

## Distribusi Kelas RS

| Kelas | Jumlah | Deskripsi |
|-------|--------|-----------|
| A | 85 | RS rujukan nasional, fasilitas lengkap |
| B | 454 | RS rujukan regional |
| C | 1.807 | RS kabupaten/kota |
| D | 870 | RS pratama |
| D PRATAMA | 82 | RS pratama tipe khusus |
| Belum Ditetapkan / Non Kelas | 6 | Dalam proses penetapan |
