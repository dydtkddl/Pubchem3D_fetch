이 프로그램은 PubChem 데이터베이스에서 특정 화합물의 3D 구조 정보를 포함하는 MOL 파일을 다운로드하고 저장한다.

## 주요 기능
- PubChem의 3D Compound SDF 데이터는 25,000개 화합물 단위로 압축된 `.gz` 파일로 제공된다.  
- 입력받은 CID(Compound ID)에 해당하는 화합물 정보를 포함하는 SDF 파일을 다운로드 후 압축 해제한다.  
- 압축 해제된 SDF 파일에서 해당 CID 블록을 찾아서 MOL 포맷으로 분리 저장한다.  
- 임시 다운로드 및 압축 해제 파일은 기본적으로 삭제하며, 옵션에 따라 SDF 파일을 유지할 수 있다.

## 사용법

1. **파이썬 사용 시**  
   ```bash
   $ python fetch_pubchem.py <PubChem CID>
   ````

2. **윈도우 batch 파일 사용 시**

   * 전제 조건 : 환경변수에 이 프로그램이 있는 폴더가 등록되어 있어야 함.

   ```bash
   $ fetch_pubchem <PubChem CID> 
   ```

## 예시

```bash
$ python fetch_pubchem.py 2244
```

## 출력

* 현재 디렉토리에 `<CID>.mol` 파일 생성

## 필요 파이썬 라이브러리

* requests
* gzip
* shutil
* pathlib

---

작성자: 안용상
작성일: 2025/05/26

