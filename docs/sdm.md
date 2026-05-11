# Data SDM / Tenaga

[← Kembali ke README](../README.md)

Dataset jumlah tenaga kesehatan per jenis dan grup untuk setiap RS.

---

## Struktur Kolom

| Kolom | Deskripsi |
|-------|-----------|
| `kode_rs` | Kode RS |
| `grup_sdm` | Grup/kategori tenaga |
| `jenis_sdm` | Jenis tenaga (spesifik) |
| `jumlah_sdm` | Jumlah tenaga |

---

## Statistik

| Keterangan | Nilai |
|------------|-------|
| RS dengan data SDM | **3.262 RS** |
| Total baris | **168.468** |
| Jenis SDM unik | **391 jenis** |
| Grup SDM | **43 grup** |

---

## Catatan `total_sdm`

`total_sdm` = **semua tenaga** (klinis + non-klinis) yang tercatat di RS.

| Kategori | Jumlah Grup |
|----------|-------------|
| ✅ Tenaga Klinis (bidang kesehatan) | 39 grup |
| ❌ Tenaga Non-Klinis (manajemen, IT, dll) | 4 grup |

---

## ✅ Tenaga Klinis — Dokter & Subspesialis

| Nama Kolom | Profesi |
|------------|---------|
| `grpsdm_pelayanan_medik_umum` | Dokter umum |
| `grpsdm_pelayanan_medik_spesialis_dasar` | Dokter spesialis dasar |
| `grpsdm_pelayanan_medik_spesialis_lain` | Dokter spesialis lain |
| `grpsdm_pelayanan_medik_spesialis_gigi` | Dokter gigi spesialis |
| `grpsdm_subspesialis_anestesi_dan_terapi_intensi` | Subspesialis anestesi |
| `grpsdm_subspesialis_bedah_anak_dan_atau_dokter_` | Subspesialis bedah anak |
| `grpsdm_subspesialis_bedah_plastik` | Subspesialis bedah plastik |
| `grpsdm_subspesialis_bedah_saraf_dan_atau_dokter` | Subspesialis bedah saraf |
| `grpsdm_subspesialis_jantung_dan_pembuluh_darah_` | Subspesialis jantung |
| `grpsdm_subspesialis_kedokteran_fisik_dan_rehabi` | Subspesialis fisik & rehabilitasi |
| `grpsdm_subspesialis_kedokteran_nuklir` | Subspesialis nuklir |
| `grpsdm_subspesialis_kedokteran_jiwa_dan_atau_do` | Subspesialis jiwa |
| `grpsdm_subspesialis_kulit_dan_kelamin_dan_atau_` | Subspesialis kulit & kelamin |
| `grpsdm_subspesialis_mata_dan_atau_dokter_spesia` | Subspesialis mata |
| `grpsdm_subspesialis_orthopaedi_dan_traumatologi` | Subspesialis orthopaedi |
| `grpsdm_subspesialis_paru_dan_atau_dokter_spesia` | Subspesialis paru |
| `grpsdm_subspesialis_patologi_klinik_dan_atau_do` | Subspesialis patologi klinik |
| `grpsdm_subspesialis_radiologi_dan_atau_dokter_s` | Subspesialis radiologi |
| `grpsdm_subspesialis_saraf_dan_atau_dokter_spesi` | Subspesialis saraf |
| `grpsdm_subspesialis_telinga_hidung_tenggorok_da` | Subspesialis THT-KL |
| `grpsdm_subspesialis_urologi` | Subspesialis urologi |
| `grpsdm_subspesialis_anak_dan_atau_dokter_spesia` | Subspesialis anak |
| `grpsdm_subspesialis_bedah_dan_atau_dokter_spesi` | Subspesialis bedah |
| `grpsdm_subspesialis_obstetri_dan_ginekologi_dan` | Subspesialis obsgin |
| `grpsdm_subspesialis_penyakit_dalam_dan_atau_dok` | Subspesialis penyakit dalam |
| `grpsdm_subspesialis_gizi_klinik` | Subspesialis gizi klinik |
| `grpsdm_subspesialis_dan_atau_dokter_spesialis_d` | Subspesialis lainnya |

---

## ✅ Tenaga Klinis — Non-Dokter

| Nama Kolom | Profesi |
|------------|---------|
| `grpsdm_tenaga_keperawatan_dan_kebidanan` | Perawat & bidan |
| `grpsdm_tenaga_kefarmasian___apoteker` | Apoteker |
| `grpsdm_tenaga_kefarmasian___ttk` | Asisten apoteker |
| `grpsdm_tenaga_gizi` | Ahli gizi |
| `grpsdm_tenaga_keteknisian_medis` | Lab, radiografer, dll |
| `grpsdm_tenaga_keterapian_fisik` | Fisioterapis, dll |
| `grpsdm_tenaga_psikologi_klinis` | Psikolog klinis |
| `grpsdm_tenaga_kesehatan_lingkungan` | Kesehatan lingkungan |
| `grpsdm_tenaga_kesehatan_masyarakat` | Kesehatan masyarakat |
| `grpsdm_tenaga_kesehatan_tradisional` | Kesehatan tradisional |
| `grpsdm_tenaga_teknik_biomedika` | Elektromedis, dll |
| `grpsdm_asisten_tenaga_kesehatan` | Asisten nakes |

---

## ❌ Tenaga Non-Klinis

| Nama Kolom | Profesi |
|------------|---------|
| `grpsdm_tenaga_penunjang___dukungan_manajemen` | Manajemen |
| `grpsdm_tenaga_penunjang___dukungan_ti` | IT |
| `grpsdm_tenaga_penunjang___struktural` | Struktural |
| `grpsdm_tenaga_penunjang___lainnya` | Lainnya |

---

## Grup SDM (Top 10 berdasarkan total tenaga)

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
