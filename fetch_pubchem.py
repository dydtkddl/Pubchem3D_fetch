#!/usr/bin/env python3
import os
import requests
import gzip
import shutil
import sys
from pathlib import Path

def fetch_pubchem_mol(cid: int, output_dir=".", keep_sdf=False):
    range_start = (cid - 1) // 25000 * 25000 + 1
    range_end = range_start + 24999
    sdf_filename = f"{range_start:08d}_{range_end:08d}.sdf"
    gz_url = f"https://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/{sdf_filename}.gz"

    temp_gz_path = Path(output_dir) / f"{sdf_filename}.gz"
    temp_sdf_path = Path(output_dir) / sdf_filename
    mol_path = Path(output_dir) / f"{cid}.mol"

    print(f"[+] Downloading: {gz_url}")
    with requests.get(gz_url, stream=True) as r:
        r.raise_for_status()
        with open(temp_gz_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    print("[+] Extracting .gz...")
    with gzip.open(temp_gz_path, 'rb') as f_in:
        with open(temp_sdf_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"[+] Searching for CID: {cid}")
    block_lines = []
    found = False
    with open(temp_sdf_path, 'r') as f:
        buffer = []
        for line in f:
            if line.strip() == "$$$$":
                cid_str = ''.join(buffer)
                if f"> <PUBCHEM_COMPOUND_CID>\n{cid}\n" in cid_str:
                    block_lines = buffer
                    found = True
                    break
                buffer = []
            else:
                buffer.append(line)

    if not found:
        raise ValueError(f"CID {cid} not found in the file.")

    print(f"[+] Saving to: {mol_path}")
    with open(mol_path, 'w') as f:
        f.writelines(block_lines)

    temp_gz_path.unlink()
    if not keep_sdf:
        temp_sdf_path.unlink()

    print(f"[✓] Done. MOL file saved at: {mol_path.resolve()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_pubchem <PubChem CID>")
        sys.exit(1)
    cid = int(sys.argv[1])
    fetch_pubchem_mol(cid)
