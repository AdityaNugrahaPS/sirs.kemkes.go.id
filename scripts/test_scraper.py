"""
Test scraper pada sampel kecil (5 RS) sebelum full run.
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from scraper_sirs import fetch_page, parse_profil, parse_tempat_tidur, parse_layanan, parse_sdm

SAMPLE_KODE = [
    "7401038",   # RS Umum Daerah Kabupaten Buton
    "1275889",   # RS Umum Murni Teguh Memorial
    "3573264",   # RS Ibu dan Anak Melati
    "5171236",   # RS Bali International
    "1471067",   # RS Eka Hospital Pekanbaru
]

def test():
    print("=" * 60)
    print("TEST SCRAPER SIRS KEMKES")
    print("=" * 60)

    all_profil, all_tt, all_layanan, all_sdm = [], [], [], []

    for kode in SAMPLE_KODE:
        print(f"\n[TEST] Kode RS: {kode}")
        soup = fetch_page(kode)
        if not soup:
            print(f"  GAGAL fetch!")
            continue

        profil = parse_profil(soup, kode)
        tt = parse_tempat_tidur(soup, kode)
        layanan = parse_layanan(soup, kode)
        sdm = parse_sdm(soup, kode)

        print(f"  Nama    : {profil.get('nama_rs', '?')}")
        print(f"  Jenis   : {profil.get('jenis', '?')}")
        print(f"  Kelas   : {profil.get('kelas', '?')}")
        print(f"  Pemilik : {profil.get('kepemilikan', '?')}")
        print(f"  Alamat  : {profil.get('alamat', '?')[:60]}")
        print(f"  TT types: {len(tt)} | Layanan: {len(layanan)} | SDM types: {len(sdm)}")

        if tt:
            print(f"  Contoh TT: {tt[:3]}")
        if layanan:
            print(f"  Contoh Layanan: {[l['layanan'][:40] for l in layanan[:3]]}")
        if sdm:
            total_sdm = sum(s["jumlah_sdm"] for s in sdm)
            print(f"  Total SDM: {total_sdm}")

        all_profil.append(profil)
        all_tt.extend(tt)
        all_layanan.extend(layanan)
        all_sdm.extend(sdm)

        import time
        time.sleep(1.5)

    print("\n" + "=" * 60)
    print(f"HASIL: {len(all_profil)}/{len(SAMPLE_KODE)} RS berhasil di-scrape")
    print(f"  Total baris TT      : {len(all_tt)}")
    print(f"  Total baris Layanan : {len(all_layanan)}")
    print(f"  Total baris SDM     : {len(all_sdm)}")

    if all_profil:
        df = pd.DataFrame(all_profil)
        print("\nProfil preview:")
        print(df[["kode_rs", "nama_rs", "jenis", "kelas", "kepemilikan"]].to_string(index=False))
        df.to_csv("test_profil.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame(all_tt).to_csv("test_tt.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame(all_layanan).to_csv("test_layanan.csv", index=False, encoding="utf-8-sig")
        pd.DataFrame(all_sdm).to_csv("test_sdm.csv", index=False, encoding="utf-8-sig")
        print("\nFile test disimpan: test_profil.csv, test_tt.csv, test_layanan.csv, test_sdm.csv")

if __name__ == "__main__":
    test()
