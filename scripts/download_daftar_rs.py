"""
Download daftar kode RS dari sumber publik Kemkes.
Mengambil ~2900+ kode RS dari dataset GitHub + scraping halaman dashboard.
"""

import requests
import pandas as pd
import io
import time
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

OUTPUT = "daftar_kode_rs.csv"


def dari_github() -> pd.DataFrame:
    """Dataset publik dari pusdatin kemenkes (2900+ RS)."""
    url = "https://raw.githubusercontent.com/zakiego/data-pusdatin-kemenkes/main/rumah_sakit.csv"
    log.info(f"Download dari GitHub: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text), dtype=str)
    log.info(f"  → {len(df)} RS dari GitHub dataset")
    return df


def dari_sirs_dashboard() -> pd.DataFrame:
    """Coba ambil ID dari endpoint peta SIRS (fallback)."""
    # Endpoint yang diketahui memuat marker peta
    kandidat = [
        "https://sirs.kemkes.go.id/fo/home/get_peta_rs",
        "https://sirs.kemkes.go.id/fo/home/getPetaRS",
        "https://sirs.kemkes.go.id/fo/home/data_peta",
    ]
    for url in kandidat:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            if resp.status_code == 200 and resp.text.strip().startswith("["):
                import json
                data = json.loads(resp.text)
                kodes = []
                for item in data:
                    for key in ["kode_rs", "kode", "id_rs", "id"]:
                        if key in item:
                            kodes.append(str(item[key]))
                            break
                if kodes:
                    log.info(f"  → {len(kodes)} RS dari endpoint: {url}")
                    return pd.DataFrame({"kode_rs": kodes})
        except Exception:
            pass
    return pd.DataFrame()


def main():
    frames = []

    # Sumber 1: GitHub dataset
    try:
        df_gh = dari_github()
        # Kolom kode bisa 'kode_rs' atau 'kode'
        kode_col = next((c for c in df_gh.columns if "kode" in c.lower()), None)
        if kode_col:
            frames.append(pd.DataFrame({
                "kode_rs": df_gh[kode_col].dropna().astype(str),
                "nama_rs": df_gh.get("nama", pd.Series(dtype=str)),
                "provinsi": df_gh.get("wilayah", pd.Series(dtype=str)),
            }))
    except Exception as e:
        log.warning(f"Gagal dari GitHub: {e}")

    # Sumber 2: SIRS dashboard API
    try:
        df_sirs = dari_sirs_dashboard()
        if not df_sirs.empty:
            frames.append(df_sirs)
    except Exception as e:
        log.warning(f"Gagal dari SIRS dashboard: {e}")

    if not frames:
        log.error("Tidak ada data berhasil diunduh!")
        return

    df_all = pd.concat(frames, ignore_index=True)
    df_all["kode_rs"] = df_all["kode_rs"].str.strip().str.zfill(7)
    df_all = df_all.drop_duplicates(subset="kode_rs")
    df_all = df_all[df_all["kode_rs"].str.match(r"^\d{7}$")]

    df_all.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    log.info(f"\nTotal unik: {len(df_all)} RS → disimpan ke '{OUTPUT}'")
    log.info("Kolom tersedia: " + ", ".join(df_all.columns.tolist()))


if __name__ == "__main__":
    main()
