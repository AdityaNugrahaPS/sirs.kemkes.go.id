"""
Scrape 576 RS baru dari rekap_rs_all yang belum ada di profil.
Append ke data_profil_rs.csv yang sudah ada.
Juga scrape TT, Layanan, SDM untuk RS baru ini.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv, time, logging
from datetime import datetime
from repair_profil import fetch, parse, COLS, DELAY, MAX_RETRIES
from scraper_sirs import parse_tempat_tidur, parse_layanan, parse_sdm

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_PROFIL  = os.path.join(BASE_DIR, "data", "raw", "data_profil_rs.csv")
OUTPUT_TT      = os.path.join(BASE_DIR, "data", "raw", "data_tempat_tidur.csv")
OUTPUT_LAYANAN = os.path.join(BASE_DIR, "data", "raw", "data_layanan.csv")
OUTPUT_SDM     = os.path.join(BASE_DIR, "data", "raw", "data_sdm.csv")
KODE_BARU      = os.path.join(BASE_DIR, "data", "raw", "daftar_kode_rs_baru.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "logs", "scrape_rs_baru.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger(__name__)

BATCH_SIZE = 50

def flush_profil(rows):
    with open(OUTPUT_PROFIL, "a", newline="", encoding="utf-8-sig") as f:
        csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore").writerows(rows)

def flush_rows(path, rows, fieldnames):
    if not rows: return
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore").writerows(rows)

def main():
    log.info("=" * 50)
    log.info(f"Scrape RS Baru - Mulai: {datetime.now()}")

    df_kode = pd.read_csv(KODE_BARU, dtype=str)
    kode_list = df_kode["kode_rs"].dropna().unique().tolist()

    # Resume: skip yang sudah ada di profil
    df_done = pd.read_csv(OUTPUT_PROFIL, dtype=str)
    done = set(df_done["kode_rs"].str.zfill(7).tolist())
    todo = [k for k in kode_list if k.zfill(7) not in done]
    log.info(f"Total baru: {len(kode_list)} | Perlu discrape: {len(todo)}")

    p_batch, tt_batch, lay_batch, sdm_batch = [], [], [], []
    sukses = gagal = 0
    total = len(todo)

    for i, kode in enumerate(todo, 1):
        log.info(f"[{i}/{total}] {kode}")
        soup = fetch(kode)
        if soup is None:
            gagal += 1
        else:
            p   = parse(soup, kode)
            tt  = parse_tempat_tidur(soup, kode)
            lay = parse_layanan(soup, kode)
            sdm = parse_sdm(soup, kode)

            p_batch.append(p)
            tt_batch.extend(tt)
            lay_batch.extend(lay)
            sdm_batch.extend(sdm)
            sukses += 1
            log.info(f"  -> {p['nama_rs']} | {p['jenis']} | Kelas {p['kelas']} | TT:{len(tt)} Lay:{len(lay)} SDM:{len(sdm)}")

        if len(p_batch) >= BATCH_SIZE:
            flush_profil(p_batch)
            flush_rows(OUTPUT_TT,      tt_batch,  ["kode_rs","kelas_tt","jumlah_tt"])
            flush_rows(OUTPUT_LAYANAN, lay_batch, ["kode_rs","layanan"])
            flush_rows(OUTPUT_SDM,     sdm_batch, ["kode_rs","grup_sdm","jenis_sdm","jumlah_sdm"])
            p_batch.clear(); tt_batch.clear(); lay_batch.clear(); sdm_batch.clear()
            log.info(f"  [Batch disimpan] {i}/{total}")

        time.sleep(DELAY)

    # Flush sisa
    flush_profil(p_batch)
    flush_rows(OUTPUT_TT,      tt_batch,  ["kode_rs","kelas_tt","jumlah_tt"])
    flush_rows(OUTPUT_LAYANAN, lay_batch, ["kode_rs","layanan"])
    flush_rows(OUTPUT_SDM,     sdm_batch, ["kode_rs","grup_sdm","jenis_sdm","jumlah_sdm"])

    log.info(f"Selesai! Sukses: {sukses} | Gagal: {gagal}")
    log.info("=" * 50)

if __name__ == "__main__":
    main()
