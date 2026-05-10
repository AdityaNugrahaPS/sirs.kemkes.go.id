# Dataset Rumah Sakit Indonesia — sirs.kemkes.go.id

Data profil lengkap rumah sakit seluruh Indonesia yang discrape dari portal resmi
**SIRS (Sistem Informasi Rumah Sakit) Kementerian Kesehatan RI** — sirs.kemkes.go.id.
Digunakan sebagai fitur untuk model Machine Learning.

---

## Struktur Folder

```
sirs.kemkes.go.id/
├── data/
│   ├── raw/              ← Data mentah per kategori
│   │   ├── daftar_kode_rs.csv      Daftar kode RS (sumber scraping awal)
│   │   ├── daftar_kode_rs_baru.csv Kode RS tambahan dari rekap_rs_all
│   │   ├── data_rekap_rs.csv       Data rekap dari endpoint rekap_rs_all
│   │   ├── data_profil_rs.csv      Info dasar tiap RS
│   │   ├── data_tempat_tidur.csv   Jumlah TT per tipe per RS
│   │   ├── data_layanan.csv        Daftar layanan per RS
│   │   └── data_sdm.csv            Tenaga kesehatan per RS
│   └── ml/
│       └── data_ml_features.csv    Wide format siap ML (1 baris per RS)
├── scripts/
│   ├── download_daftar_rs.py       Download daftar kode RS
│   ├── scraper_sirs.py             Scraper utama
│   ├── repair_profil.py            Re-scrape profil dengan kolom baku
│   ├── scrape_rs_baru.py           Scrape RS tambahan dari rekap_rs_all
│   └── test_scraper.py             Uji coba 5 RS sampel
└── logs/
    └── scraper.log                 Log proses scraping
```

---

## Ringkasan Data

### Cakupan

| Keterangan | Nilai |
|------------|-------|
| Total Rumah Sakit | **3.304 RS** |
| Cakupan Wilayah | 34 Provinsi seluruh Indonesia |
| Sumber | sirs.kemkes.go.id (publik, tanpa login) |
| Tanggal Scraping | 7 Mei 2026 |
| Kelengkapan | **100%** dari RS aktif di SIRS (3.302 rekap + 2 RS valid tambahan) |

---

### 1. Data Profil RS (`data_profil_rs.csv`)

Info dasar setiap rumah sakit.

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

#### Distribusi Jenis RS

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

#### Distribusi Kelas RS

| Kelas | Jumlah | Deskripsi |
|-------|--------|-----------|
| A | 85 | RS rujukan nasional, fasilitas lengkap |
| B | 454 | RS rujukan regional |
| C | 1.807 | RS kabupaten/kota |
| D | 870 | RS pratama |
| D PRATAMA | 82 | RS pratama tipe khusus |
| Belum Ditetapkan / Non Kelas | 6 | Dalam proses penetapan |

---

### 2. Data Tempat Tidur (`data_tempat_tidur.csv`)

Jumlah tempat tidur per tipe untuk setiap RS.

| Kolom | Deskripsi |
|-------|-----------|
| `kode_rs` | Kode RS |
| `kelas_tt` | Tipe tempat tidur |
| `jumlah_tt` | Jumlah tempat tidur |

| Statistik | Nilai |
|-----------|-------|
| RS dengan data TT | **3.285 RS** |
| Total baris | **57.880** |
| Tipe TT unik | **32 tipe** |

#### 15 Tipe Tempat Tidur Terbanyak

| Tipe | RS yang Memiliki |
|------|-----------------|
| Kelas III | 3.185 RS |
| Kelas I | 3.078 RS |
| Kelas II | 3.053 RS |
| Isolasi | 2.815 RS |
| ICU Dengan Ventilator | 2.688 RS |
| VIP | 2.680 RS |
| Isolasi Tanpa Tekanan Negatif | 2.561 RS |
| Isolasi Tekanan Negatif | 2.461 RS |
| IGD Khusus Covid | 2.433 RS |
| ICU Tekanan Negatif dengan Ventilator | 2.431 RS |
| ICU Tanpa Tekanan Negatif Dengan Ventilator | 2.413 RS |
| ICU Tekanan Negatif tanpa Ventilator | 2.377 RS |
| ICU Tanpa Tekanan Negatif Tanpa Ventilator | 2.365 RS |
| NICU Khusus Covid | 2.330 RS |
| VK (TT Observasi di R Bersalin) Khusus Covid | 2.302 RS |

---

### 3. Data Layanan (`data_layanan.csv`)

Daftar layanan medis yang tersedia di setiap RS.

| Kolom | Deskripsi |
|-------|-----------|
| `kode_rs` | Kode RS |
| `layanan` | Nama layanan |

| Statistik | Nilai |
|-----------|-------|
| RS dengan data layanan | **3.289 RS** |
| Total baris | **180.578** |
| Jenis layanan unik | **316 layanan** |

#### 15 Layanan Terbanyak

| Layanan | Jumlah RS |
|---------|-----------|
| Pelayanan Gawat Darurat Umum 24 jam & 7 hari | 3.248 |
| Pelayanan medik dasar / umum | 3.191 |
| Rekam medis dan informasi kesehatan | 3.190 |
| Pelayanan farmasi | 3.169 |
| Pengelolaan limbah / kesehatan lingkungan | 3.091 |
| Pemeliharaan Sarana, Prasarana dan fasilitas | 3.080 |
| Kesehatan anak | 3.063 |
| Sistem informasi dan komunikasi / SIRS / IT | 3.051 |
| Penyakit dalam | 3.029 |
| Anestesi | 3.024 |
| Obstetri dan ginekologi | 3.002 |
| Sterilisasi / CSSD | 2.951 |
| Bedah | 2.919 |
| Radiologi | 2.886 |
| Pelayanan KIA/KB | 2.854 |

---

### 4. Data SDM / Tenaga (`data_sdm.csv`)

Jumlah tenaga kesehatan per jenis dan grup untuk setiap RS.

| Kolom | Deskripsi |
|-------|-----------|
| `kode_rs` | Kode RS |
| `grup_sdm` | Grup/kategori tenaga |
| `jenis_sdm` | Jenis tenaga (spesifik) |
| `jumlah_sdm` | Jumlah tenaga |

| Statistik | Nilai |
|-----------|-------|
| RS dengan data SDM | **3.262 RS** |
| Total baris | **168.468** |
| Jenis SDM unik | **391 jenis** |

#### Grup SDM (Top 10 berdasarkan total tenaga)

| Grup | Total Tenaga |
|------|-------------|
| Tenaga Keperawatan dan Kebidanan | 471.207 |
| Tenaga Penunjang - Dukungan Manajemen | 111.762 |
| Pelayanan Medik Umum | 76.547 |
| Tenaga Teknik Biomedika | 58.262 |
| Pelayanan Medik Spesialis Lain | 55.539 |
| Tenaga Kefarmasian - TTK | 39.011 |
| Tenaga Keteknisian Medis | 35.306 |
| Pelayanan Medik Spesialis Dasar | 34.343 |
| Tenaga Kefarmasian - Apoteker | 21.546 |
| Asisten Tenaga Kesehatan | 17.600 |

---

### 5. ML Features (`data_ml_features.csv`)

Dataset wide-format siap pakai untuk Machine Learning. Setiap baris = 1 RS.

| Statistik | Nilai |
|-----------|-------|
| Jumlah baris (RS) | **3.304** |
| Jumlah fitur (kolom) | **802** |
| Ukuran file | ~10.6 MB |

#### Komposisi Fitur

| Kelompok Fitur | Jumlah Kolom | Deskripsi |
|----------------|-------------|-----------|
| Profil dasar | 17 | Nama, jenis, kelas, kepemilikan, luas, dll |
| Agregat | 3 | `total_tt`, `total_layanan`, `total_sdm` |
| Tempat Tidur (`tt_*`) | 32 | Jumlah TT per tipe |
| Layanan (`layan_*`) | 316 | Binary 1/0 per jenis layanan |
| SDM per jenis (`sdm_*`) | 391 | Jumlah per jenis tenaga |
| SDM per grup (`grpsdm_*`) | 43 | Jumlah per grup tenaga |

---

## Cara Penggunaan

```python
import pandas as pd

# Load dataset siap ML
df = pd.read_csv("data/ml/data_ml_features.csv")
print(df.shape)  # (3304, 802)

# Load data mentah
profil = pd.read_csv("data/raw/data_profil_rs.csv")
tt     = pd.read_csv("data/raw/data_tempat_tidur.csv")
layanan= pd.read_csv("data/raw/data_layanan.csv")
sdm    = pd.read_csv("data/raw/data_sdm.csv")
```

## Update Data

```bash
# Download ulang daftar RS
python scripts/download_daftar_rs.py

# Scrape ulang semua (mendukung resume)
python scripts/scraper_sirs.py

# Scrape ulang profil saja
python scripts/repair_profil.py
```

---

## Catatan Kelengkapan

Dataset ini mencakup **semua RS aktif** yang dapat diakses secara publik dari sirs.kemkes.go.id:
- Endpoint `rekap_rs_all` (sumber utama): 3.302 RS aktif
- 2 RS valid tambahan dari sumber GitHub
- 178 entri stub/kosong (profil tanpa data) telah **dihapus** dari dataset

Data yang **tidak dapat diakses** tanpa login institusi:
- Akreditasi detail dan sertifikasi
- Data Kebutuhan Tempat Tidur (BOR, ALOS)
- Data Rujukan RS (SISRUTE)
- Data ASPAK (Alat, Sarana, Prasarana)

---

*Sumber: [sirs.kemkes.go.id](https://sirs.kemkes.go.id) — Kementerian Kesehatan Republik Indonesia*
