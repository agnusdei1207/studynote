+++
title = "511. 1단계 디렉터리 (Single-level Directory)"
date = "2026-03-14"
weight = 511
+++

# 511. 1단계 디렉터리 (Single-level Directory)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일 시스템 (File System)의 가장 원초적인 구조로, 모든 파일이 루트(Root) 아래 단 하나의 리스트로 존재하는 평면적 (Flat) 관리 체계이다.
> 2. **가치**: 구현 복잡도가 $O(1)$ 수준으로 낮고 메타데이터 오버헤드가 최소화되어, 메모리가 제한적인 초기 OS나 단일 태스크 임베디드 시스템에 최적화되어 있다.
> 3. **한계**: 전역적 이름 충돌(Global Naming Collision)이 필연적이며, 파일 수 증가에 따른 선형 검색(Linear Search) 지연과 사용자별 격리가 불가능하여 현대적 다중 사용자 환경에는 부적합하다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**1단계 디렉터리 (Single-level Directory)**는 컴퓨터 시스템의 전체 파일이 단 하나의 공용 디렉터리 내에 등록되는 구조를 의미한다. 이 구조는 계층(Hierarchy)이나 부모-자식(Parent-Child) 관계가 존재하지 않는 완전한 평면(Flat) 구조이다. 운영체제(OS)는 하나의 **마스터 파일 디렉터리 (Master File Directory, MFD)** 또는 단순히 '디렉터리'라 불리는 단일 테이블만을 유지하며, 이 테이블이 파일의 존재와 위치에 대한 모든 정보를 독점한다.

### 2. 역사적 배경 및 철학
1960년대 초기 시분할 시스템(Time-Sharing System, TSS)이나 일괄 처리(Batch Processing) 시스템 등 자원이 극도로 제한적이던 환경에서 탄생했다. 당시에는 파일을 논리적으로 분류하기보다, 단순히 '저장'하고 '불러오는' 물리적 매핑이 최우선이었다. 복잡한 트리(Tree) 알고리즘이나 경로(Path) 해석 로직은 귀중한 **CPU (Central Processing Unit)** 사이클과 메모리를 낭비하는 요소로 간주되었다.

### 3. 작동 메커니즘 개요
파일 생성 시, 시스템은 유일한 이름(Unique Name)을 생성할 책임을 사용자에게 전가한다. 파일 시스템은 해당 이름이 테이블에 존재하는지 확인하고, 존재하지 않으면 **FCB (File Control Block)** 정보를 할당하여 테이블에 등록한다. 이때 파일의 물리적 위치는 디스크의 블록 번호 혹는 i-node 번호와 직접 매핑된다.

```text
      [ User Request: "Open foo.txt" ]
                 │
                 ▼
    [ OS Kernel File System Manager ]
                 │
                 ▼
    +-----------------------------+
    |  Single Directory Table     | <--- Linear Search (O(N))
    +-----------------------------+
    | 1. boot.sys  -> Block 0100  |
    | 2. data.bin  -> Block 0550  |
    | 3. foo.txt   -> Block 2100  | <--- Match Found!
    | 4. ...       -> ...         |
    +-----------------------------+
```

> **📢 섹션 요약 비유**: 1단계 디렉터리는 **"천장이 높은 하나의 거대한 창고에 칸막이 없이 모든 물건을 바닥에 쌓아두는 관리 시스템"**과 같다. 물건을 넣을 때는 망설임 없이 던지면 되지만(빠른 생성), 나중에 특정 물건을 찾을 때는 입구부터 끝까지 발로 차며 찾아야 하며(느린 검색), 다른 사람이 같은 이름의 박스를 가져오면 충돌이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 데이터 구조 및 필드 분석
1단계 디렉터리의 핵심은 메타데이터를 저장하는 단일 테이블이다. 각 진입(Entry)은 보통 고정 크기(Fixed Size) 레코드 배열로 구성된다.

| 필드명 (Field) | 비트 크기 | 내부 동작 및 역할 | 설명 |
|:---|:---:|:---|:---|
| **File Name** | 8+3 chars | 사용자 입력 키 값. 시스템 내 **유일성(Unique)** 보장 필수. | 검색의 Primary Key 역할. |
| **File Type** | 1 Byte | Executable, Text, Binary 등을 구분. | 로더(Loader)가 실행 여부를 판단에 사용. |
| **Location** | 4 Bytes | 디스크 상의 시작 블록 번호나 **inode** 번호 저장. | 물리적 주소 매핑의 핵심. |
| **Size** | 4 Bytes | 파일의 바이트 크기 혹은 할당된 블록 수. | EOF(End of File) 판별 및 공간 관리용. |
| **Protection** | 1 Byte | **RWX** (Read/Write/Execute) 플래그. | 접근 제어 권한 정의. |
| **Status/Count** | 1 Byte | 파일 열림 횟수(Open Count). | 프로세스 간 공유 및 잠금(Lock) 관리. |

### 2. 핵심 알고리즘과 시간 복잡도
구현의 핵심은 **선형 탐색(Linear Search)**이다. 최적화가 없는 순수 1단계 디렉터리에서 파일 $k$를 찾는 시간 복잡도는 $O(N)$이다.

```text
[ALGORITHM] Search_File(directory, target_name)
-------------------------------------------------------------------
01: FOR each entry IN directory DO             // N개의 엔트리 순회
02:    IF entry.file_name == target_name THEN  // 문자열 비교 연산
03:       RETURN entry.physical_address        // 매핑 성공, 주소 반환
04:    END IF
05: END FOR
06: RETURN ERROR_FILE_NOT_FOUND                // 실패 시 에러 반환
-------------------------------------------------------------------
```

### 3. 디스크 레이아웃 시각화 (Architecture)

```text
   [ Logical File System (VFS Layer) ]
                │
                ▼
┌─────────────────────────────────────────────────────┐
│          SINGLE-LEVEL DIRECTORY TABLE               │
│  (Located at Fixed Block, e.g., Block 0 or 2)       │
├──────────┬───────────┬───────────────┬──────────────┤
│Name      │Permissions│Length (Bytes) │Start Address │
├──────────┼───────────┼───────────────┼──────────────┤
│kernel.bin│r-xr-xr-x  │ 40,960        │  [Block 5]   │
│usr.txt   │rw-r--r--  │ 1,024         │  [Block 12]  │
│data.log  │rw-rw-rw-  │ 500           │  [Block 15]  │
│[Empty]   │N/A        │ N/A           │  NULL        │
└──────────┴───────────┴───────────────┴──────────────┘
          │               │               │
          ▼               ▼               ▼
┌─────────────────────────────────────────────────────┐
│               PHYSICAL DISK SPACE                   │
│  [5] [6] [7] [8] [9] [10] [11] [12] [13] [14] [15] │
│   <-- kernel.bin (Contiguous) -->   ^   ^   ^       │
│                                     │   │   └── data.log
│                                     │   └──── usr.txt
```

**해설**:
위 다이어그램은 논리적 파일명이 물리적 디스크 블록으로 연결되는 과정을 보여준다. 파일 시스템의 부팅 블록(Boot Block) 바로 뒤에 이 단일 테이블이 위치하는 것이 전형적이다. 모든 파일은 이 테이블을 통해서만 접근 가능하며, 파일 간의 상대적 위치 개념(상위/하위 폴더)이 존재하지 않음을 알 수 있다.

> **📢 섹션 요약 비유**: 마치 **"전교생의 이름을 가나다순으로 적은 한 장의 출석부"**와 같다. 누군가를 찾으려면 첫 페이지부터 쭉 훑어야 하며(선형 검색), 만약 '김철수'가 두 명 있다면(이름 중복), 선생님은 출석부만으로는 누구인지 전혀 구분할 수 없는 구조적 한계를 지닌다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 디렉터리 구조 비교 분석
파일 시스템의 진화 과정에서 1단계 구조가 가지는 위치를 정량적으로 분석한다.

| 비교 기준 | 1단계 디렉터리 (Single-Level) | 2단계 디렉터리 (Two-Level) | 계층형 디렉터리 (Tree-Structured) |
|:---|:---|:---|:---|
| **구조 복잡도** | 최하 (Low) | 중간 (Medium) | 높음 (High - Path Resolution req.) |
| **검색 속도** | $O(N)$ (느림) | $O(N/M)$ (M=사용자 수, 중간) | $O(\log N)$ ~ $O(1)$ (빠름) |
| **네이밍 규칙** | 전역 유일 필수 (Global Unique) | 사용자 내 유일 (User Unique) | 전체 경로 유일 (Path Unique) |
| **다중 사용자 지원** | 불가능 (격리 없음) | 가능 (UFD로 격리) | 완벽 지원 (홈 디렉터리) |
| **그룹핑灵活性** | None | User Level Only | File/Directory Level Free |
| **대표 OS** | CP/M, MS-DOS (Root) | IBM MFT, early Unix | Windows NTFS, Linux ext4 |

### 2. 운영체제(OS) 및 메모리 관리 융합
- **메모리 관리 (MMU)와의 관계**: 1단계 디렉터리는 페이지 테이블(Page Table)의 '순차 매핑' 방식과 유사하다. 테이블이 커지면 **TLB (Translation Lookaside Buffer)** 미스가 빈번해져 성능이 급격히 저하되는 것과 동일한 이치다.
- **보안 (Security) 취약점**: 모든 파일이 하나의 테이블에 노출되므로, **ACL (Access Control List)** 적용 시 사용자별로 필터링해야 하는 오버헤드가 발생한다. 만약 A 사용자가 `system_config`라는 파일을 생성하면, B 사용자는 더 이상 시스템 설정을 위한 `system_config`를 생성할 수 없는 '자원 독점' 문제가 발생한다.

```text
   [ Naming Conflict Visualization ]

    User A Request: Create "report.doc"
           │
           ▼
    [ Directory Table Check ] -> "report.doc" NOT FOUND -> SUCCESS (Create)
           │
    (Time passes...)
           │
    User B Request: Create "report.doc"
           │
           ▼
    [ Directory Table Check ] -> "report.doc" FOUND (by User A!) -> ERROR
           │
           ▼
    Result: User B cannot create file even though it's for a different purpose.
```

> **📢 섹션 요약 비유**: 1단계 디렉터리는 **"번호표 하나만 있는 대형 예약 시스템"**과 같아서, 이미 누군가 '1번'을 쓰고 있으면 다른 목적의 용도로도 1번을 절대 쓸 수 없는 반면, 트리 구조는 **"지역번호 + 국번 + 번호"로 구성된 전화 시스템**이라서 서로 다른 지역(폴더)에서는 같은 번호(파일명)를 사용해도 혼란이 없다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 적용 가능성 분석 및 의사결정 매트릭스
현대 IT 시스템에서 순수 1단계 디렉터리를 메인으로 사용하는 경우는 드물지만, 특수한 경우 유효성을 검증해야 한다.

| 상황 (Scenario) | 적합성 (Verdict) | 기술적 판단 (Rationale) |
|:---|:---:|:---|
| **초소형 IoT 센서 노드** | ⭕ **적합** | 파일 개수가 10개 미만이고, 전력/메모리 제약으로 복잡한 경로 연산이 불가능한 경우 유리함. |
| **단일 사용자 플래시 저장소** | ⭕ **적합** | SD카드 라이브러리(FAT16 루트 등) 초기화 영역처럼, 관리 목적의 간단함이 최우선인 경우. |
| **다중 사용자 서버** | ❌ **부적합** | 보안 격리 불가능, 파일명 충돌로 인한 운영 장애 발생 확률 100%. |
| **대용량 데이터 저장소** | ❌ **부적합** | 검색 속도가 데이터 양에 비례하여 저하되어 **SLA (Service Level Agreement)** 준수 불가. |

### 2. 도입 체크리스트 (Checklist)
시스템 설계 시 1단계 구조를 고려한다면 다음을 확인한다.
- [ ] 1. **파일 수명 주기**: 생성 후 자주 삭제되지 않는 정적 파일(Static Files)인가?
- [ ] 2. **사용자 수**: 시스템에 동시 접속하는 사용자가 오직 1명인가?
- [ ] 3. **네이밍 정책**: 중앙 집중식 네이밍 관리(예: 사용자ID_타임스탬프)를 통해 충돌을 방지할 수 있는가?

### 3. 안티패턴 (Anti-Pattern)
- **DOS Attack 유발**: 악의적인 사용자가 시스템의 최대 파일 개수(예: 디렉터리 엔트리 테이블의 한계)까지 쓰레기 파일을 생성하면, 더 이상 파일을 생성할 수 없는 **자원 고갈(Exhaustion)** 상태가 된다.

> **📢 섹션 요약 비유**: 1단계 디렉터리를 선택하는 것은 **"가족 구성원만 쓰는 별장의 열쇠꾸러미"**를 만드는 것과 같다. 관리가 단순해서 좋지만, 이걸 **"수천 명의 직원이 출입하는 본사 사옥"**에 적용하면 누가 열쇠를 가졌는지 모르거나, 열쇠 이름이 같아서 열리지 않는 대형 사고가 발생한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 효과
1단계 디렉터리 도입 시 얻을 수 있는 효과는 다음과 같다.
- **구현 단순성 (Simplicity)**: 디렉터리 관리를 위한 코드 라인 수가 트리 구조 대비 1/10 수준으로 감소한다.
- **접근 속도 (Speed)**: 파일이