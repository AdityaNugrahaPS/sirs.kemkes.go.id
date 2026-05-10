"""
Re-scrape HANYA data profil RS dengan kolom yang benar.
TT, Layanan, SDM tidak disentuh (sudah benar).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv, time, os, re, logging
from datetime import datetime

BASE_URL = "https://sirs.kemkes.go.id/fo/home/profile_rs/{kode_rs}"
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "data_profil_rs.csv")
KODE_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "daftar_kode_rs.csv")
DELAY = 1.5
MAX_RETRIES = 3

# Urutan kolom kanonik — tidak berubah
COLS = ["kode_rs","nama_rs","jenis","kelas","status_blu","kepemilikan",
        "direktur","alamat","telepon","luas_tanah","luas_bangunan",
        "akreditasi","provinsi","kabkota","kecamatan","lat","lon"]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(os.path.join(os.path.dirname(__file__), "..", "logs", "repair_profil.log"), encoding="utf-8"),
                               logging.StreamHandler()])
log = logging.getLogger(__name__)


def fetch(kode_rs):
    url = BASE_URL.format(kode_rs=kode_rs)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return BeautifulSoup(r.text, "lxml")
            if r.status_code == 404:
                return None
        except Exception as e:
            log.warning(f"[{kode_rs}] attempt {attempt}: {e}")
        if attempt < MAX_RETRIES:
            time.sleep(DELAY * attempt)
    return None


def parse(soup, kode_rs):
    p = {c: "" for c in COLS}
    p["kode_rs"] = kode_rs

    # Nama RS: h3 ke-2 non-kosong
    h3s = [h.get_text(strip=True) for h in soup.find_all("h3") if h.get_text(strip=True)]
    p["nama_rs"] = h3s[1] if len(h3s) > 1 else (h3s[0] if h3s else "")

    for li in soup.find_all("li"):
        txt = li.get_text(separator="|", strip=True)
        if txt.startswith("Alamat|"):
            parts = txt.split("|")
            p["alamat"] = parts[1].strip() if len(parts) > 1 else ""
            if "Telepon" in parts:
                idx = parts.index("Telepon")
                p["telepon"] = parts[idx + 1].strip() if idx + 1 < len(parts) else ""
            continue
        if ":" in txt:
            parts = txt.split("|")
            if len(parts) >= 2:
                label = parts[0].rstrip(":").strip().lower()
                val = parts[1].strip()
                if "jenis rs" in label:       p["jenis"] = val
                elif "kelas rs" in label:     p["kelas"] = val
                elif "status blu" in label:   p["status_blu"] = val
                elif "kepemilikan" in label:  p["kepemilikan"] = val
                elif "direktur" in label:     p["direktur"] = val
                elif "luas tanah" in label:   p["luas_tanah"] = val
                elif "luas bangunan" in label:p["luas_bangunan"] = val
                elif "akreditasi" in label:   p["akreditasi"] = val
                elif "provinsi" in label:     p["provinsi"] = val
                elif "kab" in label:          p["kabkota"] = val
                elif "kecamatan" in label:    p["kecamatan"] = val

    for tag in soup.find_all(attrs={"data-lat": True}):
        p["lat"] = tag.get("data-lat", "")
        p["lon"] = tag.get("data-lon", tag.get("data-lng", ""))

    if not p["lat"]:
        for script in soup.find_all("script"):
            t = script.get_text()
            m = re.search(r"lat[itude]*['\"\s:=]+(-?\d+\.\d+)", t, re.IGNORECASE)
            if m: p["lat"] = m.group(1)
            m = re.search(r"lon[gitude]*['\"\s:=]+(\d+\.\d+)", t, re.IGNORECASE)
            if m: p["lon"] = m.group(1)

    return p


def main():
    output_path = os.path.abspath(OUTPUT)
    kode_path = os.path.abspath(KODE_CSV)

    df_kode = pd.read_csv(kode_path, dtype=str)
    kode_list = df_kode["kode_rs"].dropna().unique().tolist()
    log.info(f"Total RS: {len(kode_list)}")

    # Resume support
    done = set()
    if os.path.exists(output_path):
        df_done = pd.read_csv(output_path, dtype=str)
        if "kode_rs" in df_done.columns:
            done = set(df_done["kode_rs"].tolist())
        log.info(f"Resume: {len(done)} sudah selesai")

    # Init file baru jika belum ada
    if not os.path.exists(output_path):
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            csv.DictWriter(f, fieldnames=COLS).writeheader()

    total = len(kode_list)
    sukses = gagal = 0
    batch = []
    BATCH_SIZE = 50

    def flush(rows):
        with open(output_path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
            w.writerows(rows)

    for i, kode in enumerate(kode_list, 1):
        if kode in done:
            continue
        log.info(f"[{i}/{total}] {kode}")
        soup = fetch(kode)
        if soup is None:
            gagal += 1
        else:
            row = parse(soup, kode)
            batch.append(row)
            sukses += 1
            log.info(f"  -> {row['nama_rs']} | {row['jenis']} | Kelas {row['kelas']}")
        if len(batch) >= BATCH_SIZE:
            flush(batch)
            batch.clear()
        time.sleep(DELAY)

    if batch:
        flush(batch)

    log.info(f"Selesai! Sukses: {sukses} | Gagal: {gagal}")
    log.info(f"Output: {output_path}")


if __name__ == "__main__":
    log.info("=" * 50)
    log.info(f"Repair Profil - Mulai: {datetime.now()}")
    log.info("=" * 50)
    main()
