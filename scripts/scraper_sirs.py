"""
Scraper data Rumah Sakit dari sirs.kemkes.go.id
Data: Profil RS, Tempat Tidur, Layanan, Tenaga (SDM)
Output: CSV siap pakai untuk fitur Machine Learning
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import os
import json
import logging
from datetime import datetime

# ── Konfigurasi ─────────────────────────────────────────────────────────────
BASE_URL = "https://sirs.kemkes.go.id/fo/home/profile_rs/{kode_rs}"
CSV_KODE_RS = "daftar_kode_rs.csv"       # input: daftar kode RS
OUTPUT_PROFIL = "data_profil_rs.csv"     # output: info dasar
OUTPUT_TT = "data_tempat_tidur.csv"      # output: tempat tidur
OUTPUT_LAYANAN = "data_layanan.csv"      # output: layanan
OUTPUT_SDM = "data_sdm.csv"             # output: SDM/tenaga
OUTPUT_FLAT = "data_ml_features.csv"    # output: flat/wide untuk ML
LOG_FILE = "scraper.log"
DELAY_SECONDS = 1.5                     # jeda antar request (sopan ke server)
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
}

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── Fetch dengan retry ────────────────────────────────────────────────────────
def fetch_page(kode_rs: str) -> BeautifulSoup | None:
    url = BASE_URL.format(kode_rs=kode_rs)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, "lxml")
            elif resp.status_code == 404:
                log.warning(f"[{kode_rs}] Tidak ditemukan (404)")
                return None
            else:
                log.warning(f"[{kode_rs}] Status {resp.status_code}, attempt {attempt}")
        except requests.RequestException as e:
            log.warning(f"[{kode_rs}] Error attempt {attempt}: {e}")
        if attempt < MAX_RETRIES:
            time.sleep(DELAY_SECONDS * attempt)
    return None


# ── Parser: info dasar ────────────────────────────────────────────────────────
def parse_profil(soup: BeautifulSoup, kode_rs: str) -> dict:
    profil = {"kode_rs": kode_rs}

    # Nama RS: h3 ke-2 yang non-kosong (urutan: "Profile Fasyankes", "Nama RS", "")
    h3_list = [h.get_text(strip=True) for h in soup.find_all("h3") if h.get_text(strip=True)]
    profil["nama_rs"] = h3_list[1] if len(h3_list) > 1 else (h3_list[0] if h3_list else "")

    # Scan semua <li> items - struktur utama profil RS di halaman ini
    for li in soup.find_all("li"):
        txt = li.get_text(separator="|", strip=True)

        # Alamat dan Telepon dalam satu <li>: "Alamat|...|Telepon|..."
        if txt.startswith("Alamat|"):
            parts = txt.split("|")
            if len(parts) >= 2:
                profil["alamat"] = parts[1].strip()
            # Cari telepon setelah "Telepon"
            if "Telepon" in parts:
                idx = parts.index("Telepon")
                if idx + 1 < len(parts):
                    profil["telepon"] = parts[idx + 1].strip()
            continue

        # Field dengan format "Label RS:|Value" atau "Label:|Value"
        if ":" in txt:
            parts = txt.split("|")
            if len(parts) >= 2:
                label = parts[0].rstrip(":").strip().lower()
                value = parts[1].strip()
                if "jenis rs" in label or label == "jenis":
                    profil["jenis"] = value
                elif "kelas rs" in label or label == "kelas":
                    profil["kelas"] = value
                elif "status blu" in label:
                    profil["status_blu"] = value
                elif "kepemilikan" in label:
                    profil["kepemilikan"] = value
                elif "direktur" in label:
                    profil["direktur"] = value
                elif "luas tanah" in label:
                    profil["luas_tanah"] = value
                elif "luas bangunan" in label:
                    profil["luas_bangunan"] = value
                elif "akreditasi" in label:
                    profil["akreditasi"] = value
                elif "provinsi" in label:
                    profil["provinsi"] = value
                elif "kab" in label or "kota" in label:
                    profil["kabkota"] = value
                elif "kecamatan" in label:
                    profil["kecamatan"] = value

    # Cari lat/lon dari atribut data atau script
    for tag in soup.find_all(attrs={"data-lat": True}):
        profil["lat"] = tag.get("data-lat", "")
        profil["lon"] = tag.get("data-lon", tag.get("data-lng", ""))

    # Fallback: cari di script untuk koordinat
    if "lat" not in profil:
        import re
        for script in soup.find_all("script"):
            txt = script.get_text()
            m_lat = re.search(r"lat[itude]*['\"\s:=]+(-?\d+\.\d+)", txt, re.IGNORECASE)
            m_lon = re.search(r"lon[gitude]*['\"\s:=]+(\d+\.\d+)", txt, re.IGNORECASE)
            if m_lat:
                profil["lat"] = m_lat.group(1)
            if m_lon:
                profil["lon"] = m_lon.group(1)

    # Pastikan semua field ada dengan default kosong
    for field in ["jenis", "kelas", "status_blu", "kepemilikan", "direktur",
                  "alamat", "telepon", "luas_tanah", "luas_bangunan",
                  "akreditasi", "provinsi", "kabkota", "kecamatan", "lat", "lon"]:
        profil.setdefault(field, "")

    return profil


# ── Parser: tempat tidur ──────────────────────────────────────────────────────
def parse_tempat_tidur(soup: BeautifulSoup, kode_rs: str) -> list[dict]:
    results = []

    # Cari section dengan keyword tempat tidur
    headers = soup.find_all(["h3", "h4", "h5", "strong", "b"])
    tt_section = None
    for h in headers:
        if "tempat tidur" in h.get_text(strip=True).lower():
            # Cari tabel terdekat setelah header ini
            for sib in h.find_all_next(["table", "h3", "h4"], limit=5):
                if sib.name == "table":
                    tt_section = sib
                    break
            if tt_section:
                break

    # Fallback: ambil tabel yang punya kolom "kelas" dan "jumlah"
    if not tt_section:
        for table in soup.find_all("table"):
            text = table.get_text(strip=True).lower()
            if "kelas" in text and "jumlah" in text:
                tt_section = table
                break

    if tt_section:
        for row in tt_section.find_all("tr")[1:]:  # skip header
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                kelas = ""
                jumlah = 0
                # cari kolom kelas dan jumlah
                for i, cell in enumerate(cells):
                    txt = cell.get_text(strip=True)
                    if i == 0 and txt.isdigit():
                        continue  # nomor urut
                    if i == 1 or (i == 0 and not txt.isdigit()):
                        kelas = txt
                    elif txt.replace(".", "").replace(",", "").isdigit():
                        jumlah = int(txt.replace(".", "").replace(",", ""))

                if kelas:
                    results.append({
                        "kode_rs": kode_rs,
                        "kelas_tt": kelas,
                        "jumlah_tt": jumlah,
                    })

    return results


# ── Parser: layanan ───────────────────────────────────────────────────────────
def parse_layanan(soup: BeautifulSoup, kode_rs: str) -> list[dict]:
    results = []

    headers = soup.find_all(["h3", "h4", "h5", "strong", "b"])
    layanan_table = None
    for h in headers:
        if "pelayanan" in h.get_text(strip=True).lower():
            for sib in h.find_all_next(["table", "h3", "h4"], limit=5):
                if sib.name == "table":
                    layanan_table = sib
                    break
            if layanan_table:
                break

    if not layanan_table:
        for table in soup.find_all("table"):
            text = table.get_text(strip=True).lower()
            if "pelayanan" in text:
                layanan_table = table
                break

    if layanan_table:
        for row in layanan_table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                pelayanan = ""
                for i, cell in enumerate(cells):
                    txt = cell.get_text(strip=True)
                    if not txt.isdigit() and txt:
                        pelayanan = txt
                        break
                if pelayanan:
                    results.append({
                        "kode_rs": kode_rs,
                        "layanan": pelayanan,
                    })

    return results


# ── Parser: SDM / tenaga ──────────────────────────────────────────────────────
def parse_sdm(soup: BeautifulSoup, kode_rs: str) -> list[dict]:
    results = []

    headers = soup.find_all(["h3", "h4", "h5", "strong", "b"])
    sdm_table = None
    for h in headers:
        text = h.get_text(strip=True).lower()
        if "sdm" in text or "sumber daya" in text or "tenaga" in text:
            for sib in h.find_all_next(["table", "h3", "h4"], limit=5):
                if sib.name == "table":
                    sdm_table = sib
                    break
            if sdm_table:
                break

    if not sdm_table:
        for table in soup.find_all("table"):
            text = table.get_text(strip=True).lower()
            if ("grup" in text or "sdm" in text) and "jumlah" in text:
                sdm_table = table
                break

    if sdm_table:
        rows = sdm_table.find_all("tr")
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 3:
                grup = ""
                jenis_sdm = ""
                jumlah = 0
                non_num = [c.get_text(strip=True) for c in cells
                           if not c.get_text(strip=True).replace(".", "").replace(",", "").isdigit()
                           and c.get_text(strip=True)]
                num_vals = [c.get_text(strip=True) for c in cells
                            if c.get_text(strip=True).replace(".", "").replace(",", "").isdigit()]

                if len(non_num) >= 2:
                    grup = non_num[0]
                    jenis_sdm = non_num[1]
                elif len(non_num) == 1:
                    jenis_sdm = non_num[0]

                if num_vals:
                    try:
                        jumlah = int(num_vals[-1].replace(".", "").replace(",", ""))
                    except ValueError:
                        jumlah = 0

                if jenis_sdm:
                    results.append({
                        "kode_rs": kode_rs,
                        "grup_sdm": grup,
                        "jenis_sdm": jenis_sdm,
                        "jumlah_sdm": jumlah,
                    })

    return results


# ── Buat fitur flat/wide untuk ML ─────────────────────────────────────────────
def build_ml_features(
    profil_list: list[dict],
    tt_list: list[dict],
    layanan_list: list[dict],
    sdm_list: list[dict],
) -> pd.DataFrame:
    """
    Gabungkan semua data menjadi satu baris per RS (wide format).
    Setiap tipe tempat tidur, layanan, dan grup SDM jadi kolom tersendiri.
    """
    df_profil = pd.DataFrame(profil_list)
    df_tt = pd.DataFrame(tt_list) if tt_list else pd.DataFrame(columns=["kode_rs", "kelas_tt", "jumlah_tt"])
    df_layanan = pd.DataFrame(layanan_list) if layanan_list else pd.DataFrame(columns=["kode_rs", "layanan"])
    df_sdm = pd.DataFrame(sdm_list) if sdm_list else pd.DataFrame(columns=["kode_rs", "grup_sdm", "jenis_sdm", "jumlah_sdm"])

    # Pivot tempat tidur → kolom tt_<kelas>
    if not df_tt.empty:
        df_tt["kelas_tt"] = df_tt["kelas_tt"].str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
        tt_pivot = df_tt.pivot_table(index="kode_rs", columns="kelas_tt", values="jumlah_tt", aggfunc="sum", fill_value=0)
        tt_pivot.columns = [f"tt_{c}" for c in tt_pivot.columns]
        tt_pivot = tt_pivot.reset_index()
    else:
        tt_pivot = pd.DataFrame(columns=["kode_rs"])

    # Pivot layanan → kolom layanan_<nama> (binary: ada=1)
    if not df_layanan.empty:
        df_layanan["layanan_key"] = (
            df_layanan["layanan"].str.strip().str.lower()
            .str.replace(r"[^a-z0-9\s]", "", regex=True)
            .str.replace(r"\s+", "_", regex=True)
            .str[:50]
        )
        df_layanan["value"] = 1
        layanan_pivot = df_layanan.pivot_table(
            index="kode_rs", columns="layanan_key", values="value", aggfunc="max", fill_value=0
        )
        layanan_pivot.columns = [f"layan_{c}" for c in layanan_pivot.columns]
        layanan_pivot = layanan_pivot.reset_index()
    else:
        layanan_pivot = pd.DataFrame(columns=["kode_rs"])

    # Pivot SDM → jumlah per jenis
    if not df_sdm.empty:
        df_sdm["jenis_key"] = (
            df_sdm["jenis_sdm"].str.strip().str.lower()
            .str.replace(r"[^a-z0-9\s]", "", regex=True)
            .str.replace(r"\s+", "_", regex=True)
            .str[:50]
        )
        sdm_pivot = df_sdm.pivot_table(
            index="kode_rs", columns="jenis_key", values="jumlah_sdm", aggfunc="sum", fill_value=0
        )
        sdm_pivot.columns = [f"sdm_{c}" for c in sdm_pivot.columns]
        sdm_pivot = sdm_pivot.reset_index()

        # Tambah agregat SDM per grup
        grp_pivot = df_sdm.pivot_table(
            index="kode_rs", columns="grup_sdm", values="jumlah_sdm", aggfunc="sum", fill_value=0
        )
        grp_pivot.columns = [f"grpsdm_{c.strip().lower().replace(' ', '_')}" for c in grp_pivot.columns]
        grp_pivot = grp_pivot.reset_index()
        sdm_pivot = sdm_pivot.merge(grp_pivot, on="kode_rs", how="left")
    else:
        sdm_pivot = pd.DataFrame(columns=["kode_rs"])

    # Tambah agregat total per RS
    tt_total = df_tt.groupby("kode_rs")["jumlah_tt"].sum().reset_index().rename(columns={"jumlah_tt": "total_tt"})
    layanan_total = df_layanan.groupby("kode_rs").size().reset_index(name="total_layanan") if not df_layanan.empty else pd.DataFrame(columns=["kode_rs", "total_layanan"])
    sdm_total = df_sdm.groupby("kode_rs")["jumlah_sdm"].sum().reset_index().rename(columns={"jumlah_sdm": "total_sdm"}) if not df_sdm.empty else pd.DataFrame(columns=["kode_rs", "total_sdm"])

    # Merge semua
    df = df_profil.copy()
    for df_merge in [tt_total, layanan_total, sdm_total, tt_pivot, layanan_pivot, sdm_pivot]:
        if not df_merge.empty and "kode_rs" in df_merge.columns:
            df = df.merge(df_merge, on="kode_rs", how="left")

    df = df.fillna(0)
    return df


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    log.info("=" * 60)
    log.info(f"Scraper SIRS Kemkes - Mulai: {datetime.now()}")
    log.info("=" * 60)

    # Load daftar kode RS
    if not os.path.exists(CSV_KODE_RS):
        log.error(f"File '{CSV_KODE_RS}' tidak ditemukan!")
        log.info("Buat file daftar_kode_rs.csv dengan kolom 'kode_rs'")
        log.info("Atau jalankan: python download_daftar_rs.py")
        return

    df_kode = pd.read_csv(CSV_KODE_RS, dtype=str)
    if "kode_rs" not in df_kode.columns:
        log.error("Kolom 'kode_rs' tidak ada di file CSV!")
        return

    kode_list = df_kode["kode_rs"].dropna().unique().tolist()
    log.info(f"Total RS akan di-scrape: {len(kode_list)}")

    # Cek progress sebelumnya (resume support)
    scraped = set()
    if os.path.exists(OUTPUT_PROFIL):
        df_done = pd.read_csv(OUTPUT_PROFIL, dtype=str)
        scraped = set(df_done["kode_rs"].tolist())
        log.info(f"Resume: {len(scraped)} RS sudah di-scrape sebelumnya")

    # Inisialisasi file output
    def init_csv(path, fieldnames):
        if not os.path.exists(path):
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()

    init_csv(OUTPUT_PROFIL, [
        "kode_rs", "nama_rs", "jenis", "kelas", "status_blu", "kepemilikan",
        "direktur", "alamat", "telepon", "luas_tanah", "luas_bangunan",
        "akreditasi", "provinsi", "kabkota", "kecamatan", "lat", "lon",
    ])
    init_csv(OUTPUT_TT, ["kode_rs", "kelas_tt", "jumlah_tt"])
    init_csv(OUTPUT_LAYANAN, ["kode_rs", "layanan"])
    init_csv(OUTPUT_SDM, ["kode_rs", "grup_sdm", "jenis_sdm", "jumlah_sdm"])

    profil_batch, tt_batch, layanan_batch, sdm_batch = [], [], [], []
    BATCH_SIZE = 50

    def flush_batch():
        # Append ke CSV
        def append_rows(path, rows, fieldnames):
            if not rows:
                return
            with open(path, "a", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                w.writerows(rows)

        append_rows(OUTPUT_PROFIL, profil_batch, list(profil_batch[0].keys()) if profil_batch else [])
        append_rows(OUTPUT_TT, tt_batch, ["kode_rs", "kelas_tt", "jumlah_tt"])
        append_rows(OUTPUT_LAYANAN, layanan_batch, ["kode_rs", "layanan"])
        append_rows(OUTPUT_SDM, sdm_batch, ["kode_rs", "grup_sdm", "jenis_sdm", "jumlah_sdm"])

        profil_batch.clear()
        tt_batch.clear()
        layanan_batch.clear()
        sdm_batch.clear()

    total = len(kode_list)
    sukses = 0
    gagal = 0

    for i, kode_rs in enumerate(kode_list, 1):
        if kode_rs in scraped:
            continue

        log.info(f"[{i}/{total}] Scraping RS: {kode_rs}")

        soup = fetch_page(kode_rs)
        if soup is None:
            gagal += 1
            log.warning(f"[{kode_rs}] Gagal - dilewati")
        else:
            profil = parse_profil(soup, kode_rs)
            tt = parse_tempat_tidur(soup, kode_rs)
            layanan = parse_layanan(soup, kode_rs)
            sdm = parse_sdm(soup, kode_rs)

            profil_batch.append(profil)
            tt_batch.extend(tt)
            layanan_batch.extend(layanan)
            sdm_batch.extend(sdm)

            sukses += 1
            log.info(
                f"  → {profil.get('nama_rs', '?')} | "
                f"TT: {len(tt)} tipe | Layanan: {len(layanan)} | SDM: {len(sdm)} jenis"
            )

        if len(profil_batch) >= BATCH_SIZE:
            flush_batch()
            log.info(f"  [Batch disimpan] Progress: {i}/{total}")

        time.sleep(DELAY_SECONDS)

    # Flush sisa
    if profil_batch:
        flush_batch()

    log.info(f"\nSelesai! Sukses: {sukses} | Gagal: {gagal}")
    log.info(f"Output: {OUTPUT_PROFIL}, {OUTPUT_TT}, {OUTPUT_LAYANAN}, {OUTPUT_SDM}")

    # Buat ML features flat
    log.info("Membangun ML features (wide format)...")
    try:
        df_p = pd.read_csv(OUTPUT_PROFIL, dtype=str)
        df_t = pd.read_csv(OUTPUT_TT, dtype=str) if os.path.getsize(OUTPUT_TT) > 50 else pd.DataFrame()
        df_l = pd.read_csv(OUTPUT_LAYANAN, dtype=str) if os.path.getsize(OUTPUT_LAYANAN) > 50 else pd.DataFrame()
        df_s = pd.read_csv(OUTPUT_SDM, dtype=str) if os.path.getsize(OUTPUT_SDM) > 50 else pd.DataFrame()

        if not df_t.empty:
            df_t["jumlah_tt"] = pd.to_numeric(df_t["jumlah_tt"], errors="coerce").fillna(0)
        if not df_s.empty:
            df_s["jumlah_sdm"] = pd.to_numeric(df_s["jumlah_sdm"], errors="coerce").fillna(0)

        df_ml = build_ml_features(
            df_p.to_dict("records"),
            df_t.to_dict("records") if not df_t.empty else [],
            df_l.to_dict("records") if not df_l.empty else [],
            df_s.to_dict("records") if not df_s.empty else [],
        )
        df_ml.to_csv(OUTPUT_FLAT, index=False, encoding="utf-8-sig")
        log.info(f"ML features: {df_ml.shape[0]} RS × {df_ml.shape[1]} fitur → {OUTPUT_FLAT}")
    except Exception as e:
        log.error(f"Error build ML features: {e}")

    log.info("=" * 60)
    log.info(f"Scraper selesai: {datetime.now()}")


if __name__ == "__main__":
    main()
