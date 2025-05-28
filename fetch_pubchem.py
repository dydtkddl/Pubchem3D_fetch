"""
이 프로그램은 PubChem 데이터베이스에서 특정 화합물의 3D 구조 정보를 포함하는 MOL 파일을 다운로드하고 저장한다.

주요 기능:
> PubChem의 3D Compound SDF 데이터는 25,000개 화합물 단위로 압축된 .gz 파일로 제공된다.
> 입력받은 CID(Compound ID)에 해당하는 화합물 정보를 포함하는 SDF 파일을 다운로드 후 압축 해제한다.
> 압축 해제된 SDF 파일에서 해당 CID 블록을 찾아서 MOL 포맷으로 분리 저장한다.
> 임시 다운로드 및 압축 해제 파일은 기본적으로 삭제하며, 옵션에 따라 SDF 파일을 유지할 수 있디/

사용법:
    1. 파이썬 사용 시.
    $ python fetch_pubchem.py <PubChem CID>
    
    2. 윈도우 batch 파일 사용시 
    전제 조건 : 환경변수에 이 프로그램이 있는 폴더가 등록되어있어야 함.
    $ fetch_pubchem <PubChem CID> 
    
example :
$ python fetch_pubchem.py 2244

출력:
- 현재 디렉토리에 <CID>.mol 파일 생성

필요 파이썬 라이브러리:
- requests
- gzip
- shutil
- pathlib

작성자: [안용상]
작성일: [2025/05/26]
"""


import os
import requests
import gzip
import shutil
import sys
from pathlib import Path

def fetch_pubchem(cid: int, output_dir=".", keep_sdf=False):
    ### sdf 파일이 25000개 mol파일씩 끊겨져서 존재하므로, 파일 인덱스 플래그 전처리를 해준다
    range_start = (cid - 1) // 25000 * 25000 + 1
    range_end = range_start + 24999
    ### sdf file 이름 및 url 정의
    sdf_filename = f"{range_start:08d}_{range_end:08d}.sdf"
    gz_url = f"https://ftp.ncbi.nlm.nih.gov/pubchem/Compound_3D/01_conf_per_cmpd/SDF/{sdf_filename}.gz"
    temp_gz_path = Path(output_dir) / f"{sdf_filename}.gz"
    temp_sdf_path = Path(output_dir) / sdf_filename
    mol_path = Path(output_dir) / f"{cid}.mol"

    print(f">>>>>>>> Downloading: {gz_url}")
    with requests.get(gz_url, stream=True) as r:
        r.raise_for_status()
        with open(temp_gz_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    print(">>>>>>>> Extracting .gz...")
    with gzip.open(temp_gz_path, 'rb') as f_in:
        with open(temp_sdf_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f">>>>>>>> Searching for CID: {cid}")
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

    print(f">>>>>>>> Saving to: {mol_path}")
    with open(mol_path, 'w') as f:
        f.writelines(block_lines)

    temp_gz_path.unlink()
    if not keep_sdf:
        temp_sdf_path.unlink()

    print(f">>>>>>>> Done. MOL file saved at: {mol_path.resolve()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(">>>>>>>> Usage: fetch_pubchem <PubChem CID>")
        sys.exit(1)
    cid = int(sys.argv[1])
    fetch_pubchem(cid)
