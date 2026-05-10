# Dataset Rumah Sakit Indonesia — sirs.kemkes.go.id

Data profil lengkap rumah sakit seluruh Indonesia yang discrape dari portal resmi
**SIRS (Sistem Informasi Rumah Sakit) Kementerian Kesehatan RI** — sirs.kemkes.go.id.
Digunakan sebagai fitur untuk model Machine Learning segmentasi/clustering RS.

---

## 📂 Struktur Folder

```
sirs.kemkes.go.id/
├── data/
│   ├── raw/              ← Data mentah per kategori
│   │   ├── data_profil_rs.csv
│   │   ├── data_tempat_tidur.csv
│   │   ├── data_layanan.csv
│   │   └── data_sdm.csv
│   └── ml/
│       ├── data_ml_features.csv    ← Wide format siap ML
│       └── data_ml_clean.csv       ← Data bersih siap clustering
├── docs/                ← Dokumentasi detail per dataset
├── notebooks/
│   └── EDA_sirs.kemkes.ipynb
├── scripts/
│   ├── scraper_sirs.py
│   ├── repair_profil.py
│   └── scrape_rs_baru.py
└── logs/
```

---

## 📊 Ringkasan Data

| Keterangan | Nilai |
|------------|-------|
| Total Rumah Sakit | **3.304 RS** |
| Cakupan Wilayah | 34 Provinsi seluruh Indonesia |
| Sumber | sirs.kemkes.go.id (publik, tanpa login) |
| Tanggal Scraping | 7 Mei 2026 |
| Kelengkapan | **100%** dari RS aktif di SIRS |

---

## 📚 Dokumentasi Dataset

| Dataset | Deskripsi | Link |
|---------|-----------|------|
| `data_profil_rs.csv` | Info dasar tiap RS (nama, jenis, kelas, dll) | [![Lihat Detail](https://img.shields.io/badge/Lihat%20Detail-blue?style=for-the-badge)](docs/profil_rs.md) |
| `data_tempat_tidur.csv` | Jumlah TT per tipe per RS | [![Lihat Detail](https://img.shields.io/badge/Lihat%20Detail-blue?style=for-the-badge)](docs/tempat_tidur.md) |
| `data_layanan.csv` | Daftar layanan medis per RS | [![Lihat Detail](https://img.shields.io/badge/Lihat%20Detail-blue?style=for-the-badge)](docs/layanan.md) |
| `data_sdm.csv` | Jumlah tenaga kesehatan per RS | [![Lihat Detail](https://img.shields.io/badge/Lihat%20Detail-blue?style=for-the-badge)](docs/sdm.md) |
| `data_ml_features.csv` & `data_ml_clean.csv` | Dataset siap ML & clustering | [![Lihat Detail](https://img.shields.io/badge/Lihat%20Detail-blue?style=for-the-badge)](docs/ml_features.md) |

---

## 💻 Cara Penggunaan

```python
import pandas as pd

# Dataset bersih siap clustering
df_clean = pd.read_csv("data/ml/data_ml_clean.csv")
print(df_clean.shape)  # (3292, 792)

# Dataset lengkap sebelum cleaning
df = pd.read_csv("data/ml/data_ml_features.csv")
print(df.shape)  # (3304, 802)
```

---

## ⚠️ Catatan Kelengkapan

Data yang **tidak dapat diakses** tanpa login institusi:
- Akreditasi detail dan sertifikasi
- Data BOR / ALOS (tingkat hunian)
- Data Rujukan RS (SISRUTE)
- Data ASPAK (Alat, Sarana, Prasarana)

---

*Sumber: [sirs.kemkes.go.id](https://sirs.kemkes.go.id) — Kementerian Kesehatan Republik Indonesia*
