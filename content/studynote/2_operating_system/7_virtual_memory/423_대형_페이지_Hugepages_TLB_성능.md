+++
title = "423. 대형 페이지 (Large Page / Transparent Hugepage)의 가상 메모리 성능 이점"
date = "2026-03-14"
weight = 423
+++

## 💡 Insight
- 현대 시스템은 메모리 용량이 비약적으로 증가함에 따라 기본 4KB 페이지 단위가 가져오는 관리 오버헤드(TLB Miss)를 줄이기 위해 대형 페이지(Hugepages)를 활용한다.
- 대형 페이지는 TLB 엔트리 하나가 커버하는 메모리 영역을 수백 배 이상 확장시켜 주소 변환 속도를 획기적으로 향상시킨다.
- 단, 메모리 파편화와 내부 단편화(Internal Fragmentation)가 발생할 수 있어, OS가 자동으로 관리하는 THP(Transparent Hugepage) 기술이 도입되었다.

---

## Ⅰ. 대형 페이지 (Large Page / Hugepage) 개요
### 1. 정의
- 일반적인 4KB 크기의 페이지 대신 2MB(x86_64 기준), 1GB 등 훨씬 큰 단위로 메모리를 관리하는 기법.
### 2. 배경
- 64비트 시스템에서 수백 GB의 RAM을 4KB 단위로 쪼개면 페이지 테이블 자체가 거대해지고, TLB 적중률이 낮아지는 문제가 발생함.

📢 섹션 요약 비유: 도서관 책장을 낱장(4KB)으로 관리하다가, 수백 장의 페이지를 하나로 묶은 두꺼운 전집(Hugepage) 단위로 관리하여 목록 검색 시간을 줄이는 것입니다.

---

## Ⅱ. 작동 원리 및 TLB 성능 이점
### 1. TLB(Translation Lookaside Buffer) 효율성 극대화
- TLB는 CPU 캐시처럼 주소 변환 정보를 저장하는 고가의 하드웨어 자원임.
- 4KB 페이지일 때 TLB 엔트리 512개는 2MB를 커버하지만, 2MB 대형 페이지를 쓰면 엔트리 1개로 동일한 범위를 커버할 수 있음.

### 2. 다단계 페이지 테이블 깊이 축소
- 4단계(L4) 페이지 테이블을 거칠 필요 없이 중간 단계에서 즉시 물리 주소를 찾음.

### 3. ASCII 다이어그램: 4KB vs 2MB Page Comparison
```text
[ 4KB Pages ]                     [ 2MB Hugepage ]
TLB Entry 1 -> Page A (4KB)       TLB Entry 1 -> Page Alpha (2MB)
TLB Entry 2 -> Page B (4KB)                      | (2048x larger!)
TLB Entry 3 -> Page C (4KB)                      |
...                                              |
TLB Entry 512 -> Page X (4KB)     (Matches same memory range as 512 entries)
```

📢 섹션 요약 비유: 작은 포스트잇(4KB) 512개를 붙여 주소를 적는 대신, 큰 전지(2MB) 한 장에 주소를 크게 써서 시력을 낭비하지 않는 것과 같습니다.

---

## Ⅲ. THP (Transparent Hugepage) vs Standard Hugepages
### 1. Standard Hugepages (Hugetlbfs)
- 부팅 시 미리 메모리를 예약하며 관리자가 수동으로 할당함. 고정된 성능이 필요한 DB(Oracle, MySQL) 등에서 사용.
### 2. THP (Transparent Hugepage)
- 커널이 런타임에 동적으로 작은 페이지들을 합쳐 대형 페이지로 승격(Promotion)시키거나, 필요 시 다시 쪼갬(Demotion).
- 사용자 프로세스는 수정 없이 성능 이점을 누릴 수 있음.

📢 섹션 요약 비유: THP는 직원이 상황을 봐서 알아서 작은 박스들을 큰 박스로 옮겨 담아주는 "자동 포장 서비스"입니다.

---

## Ⅳ. 성능상의 트레이드오프 (Trade-offs)
### 1. 내부 단편화 (Internal Fragmentation)
- 2MB 페이지를 할당했는데 실제 10KB만 쓰면 나머지는 낭비됨.
### 2. 지연 시간 (Latency)
- THP의 경우, 백그라운드 스캔 스레드(khugepaged)가 페이지를 합치는 과정에서 CPU 점유 및 메모리 복사 지연이 발생할 수 있음.

📢 섹션 요약 비유: 큰 화물차(2MB)는 짐을 한 번에 많이 실을 수 있지만, 골목길(작은 데이터)을 갈 때는 비효율적이고 차를 돌릴 때 시간이 더 걸립니다.

---

## Ⅴ. 주요 활용 사례
### 1. 대용량 데이터베이스 (RDBMS / In-memory DB)
- 수십 GB의 인덱스를 빠르게 조회해야 하는 환경에서 TLB 미스로 인한 성능 저하를 방지함.
### 2. 가상화 (KVM / VMware)
- 게스트 OS의 주소 변환을 이중으로 거쳐야 하는 환경(EPT/NPT)에서 대형 페이지는 필수적임.

📢 섹션 요약 비유: 고속도로(대규모 데이터 처리)를 달릴 때는 소형차(4KB) 여러 대보다 대형 버스(2MB) 한 대가 더 효율적인 수송 수단이 됩니다.

---

## 🌳 지식 그래프 (Knowledge Graph)
- **부모**: 381. 가상 메모리 개념
- **자식**: [하드웨어 페이지 테이블 워커 (추후 예정)]
- **유사 개념**:
  - TLB (Translation Lookaside Buffer)
  - Memory Fragmentation

## 👶 아이의 시각 (Child Analogy)
> "레고 블록(4KB)이 수백만 개 있으면 정리하기 너무 힘들겠지? 그래서 어떤 블록들은 아주 큰 왕레고 블록(2MB)으로 만들었어. 왕레고 블록 하나만 옮기면 작은 블록 500개를 한꺼번에 옮기는 거랑 똑같아서, 정리 정돈(주소 변환) 속도가 엄청 빨라진단다!"