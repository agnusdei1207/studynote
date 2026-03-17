+++
title = "558. F2FS (Flash-Friendly File System) - 삼성 주도 리눅스 FS"
date = "2026-03-14"
weight = 558
+++

# # [F2FS (Flash-Friendly File System)]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: F2FS (Flash-Friendly File System)는 삼성전자가 주도하여 개발한 오픈소스 리눅스 파일 시스템으로, NAND 플래시 메모리 기반 저장 장치의 '쓰기 전 삭제(Erase-before-Write)' 물리적 한계를 극복하기 위해 설계된 순수 로그 구조 파일 시스템(Log-Structured File System, LFS)이다.
> 2. **가치**: 저장 장치의 내부 동작 단위인 페이지(Page)와 블록(Block)을 인식하는 '멀티-헤드 로깅(Multi-head Logging)' 기법을 통해 쓰기 증폭(Write Amplification Factor, WAF)을 획기적으로 줄이고, 임의 쓰기(Random Write) 성능을 EXT4 대비 최대 200% 이상 향상시킨다.
> 3. **융합**: 모바일 컴퓨팅 환경의 표준이 되어 안드로이드 생태계에 깊이 침투했으며, 향후 NVMe (Non-Volatile Memory express)와 같은 고속 인터페이스와 ZNS (Zoned Namespace) SSD 등 차세대 스토리지 기술과의 결합을 통해 데이터 센터 영역으로 확장 중이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
F2FS (Flash-Friendly File System)는 기존 하드 디스크(HDD) 중심의 파일 시스템이 가진 '제자리 갱신(In-place Update)' 방식의 한계를 극복하기 위해 탄생했다. 플래시 메모리는 데이터를 덮어쓰기 위해 반드시 이전 데이터가 소속된 블록 전체를 지워야(Erase) 하는 '수정 불가능성(Immutability)'을 가진다. F2FS는 이를 '추가 전용(Append-only)' 로그 방식으로 전환하여, 데이터의 수정이 발생할 때마다 새로운 공간에 순차적으로 기록함으로써, 물리적인 '합치기(Operation Merge)' 오버헤드를 소프트웨어 차원에서 원천적으로 배제한다.

#### 2. 등장 배경: HDD에서 Flash로의 패러다임 시프트
① **기존 한계**: EXT4 (Fourth Extended File System) 등 기존 파일 시스템은 회전판 매체의 탐색 시간(Seek Time) 최소화에 최적화되어 있어, 4KB~16KB 작은 단위의 데이터가 여기저기 흩어지는 현상(Fragmentation)을 유발했다. 이는 SSD(Solid State Drive) 환경에서는 불필요한 연산이자 수명 단축의 원인이 되었다.
② **혁신적 패러다임**: SSD의 등장으로 탐색 시간은 사라졌지만, '쓰기 증폭(Write Amplification)' 문제가 대두되었다. F2FS는 논리적 블록 주소(LBA, Logical Block Address)를 물리적 위치와 1:1로 고정하지 않고 동적으로 매핑함으로써 이 문제를 해결했다.
③ **비즈니스 요구**: 모바일 기기의 저장 공간(eMMC, UFS)은 한정된 수명을 가지므로, 소프트웨어적 최적화를 통해 배터리 효율을 높이고 저장 장치의 수명을 연장해야 하는 시장적 요구가 존재했다.

#### 3. 핵심 메커니즘: 로그 구조 (Log Structure)
F2FS의 모든 쓰기 연산은 로그 형태로 디스크 끝단에 추가된다. 이때 단순히 순차적으로만 쓰는 것이 아니라, 데이터의 변경 빈도(Life time)에 따라 여러 개의 로그 버퍼(Hot/Warm/Cold)에 분류하여 기록함으로써, 나중에 불필요한 데이터를 지우는(Garbage Collection) 비용을 최소화한다. 이는 파일 시스템이 직접 FTL (Flash Translation Layer)의 역할을 일부 수행하는 '하이브리드 접근법'이라고 볼 수 있다.

> **📢 섹션 요약 비유**: F2FS는 "지우개질을 하려면 반드시 페이지 전체를 갈아야 하는 특수한 메모지(NAND Flash)를 위해, 겉으로는 깔끔하게 보이게 하되 내부적으로는 빈 곳에만 연필로 계속 덧붙여 쓰는 '스마트 노트 필기법'과 같다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
F2FS는 전체 볼륨을 다양한 목적을 가진 영역(Region)으로 나누어 관리한다. 이는 파일 시스템 메타데이터와 사용자 데이터의 수명 주기가 다르다는 점에 착안한 설계이다.

| 구성 요소 (Module) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 프로토콜/특징 | 비유 |
|:---:|:---|:---|:---|:---|
| **SB** | Superblock | 파일 시스템의 전체 설정 값(Magic No, Version) 저장 | 손상 대비 2개 세트(A/B) 유지 | 건물의 등기부등본 |
| **CP** | Checkpoint | 일관된 상태의 시작점(커서)을 기록 | 마운트 시 이 지점부터 복구 (Recovery) | 게임 세이브 포인트 |
| **SIT** | Segment Information Table | 각 세그먼트별 '유효 블록 개수' 비트맵 관리 | GC 효율성 판단의 핵심 자료구조 | 재활용 품질 식별표 |
| **NAT** | Node Address Table | 파일의 메타데이터(Node)의 물리적 위치 매핑 테이블 | 메모리 상에 캐싱(Caching)하여 탐색 가속화 | 주소록 |
| **SSA** | Segment Summary Area | 상위 노드 정보(Parent Info) 포함 (복구 로그용) | 롤링 마이그레이션(Rolling Migration) 지원 | 이사 짐 가방 내역서 |
| **MAIN** | Main Area | 실제 사용자 파일 데이터와 노드가 저장되는 공간 | 6개의 로그 타입(Hot/Warm/Cold)으로 분리 저장 | 실제 거주 공간 |

#### 2. F2FS 논리적 레이아웃 구조도
F2FS는 기존 파일 시스템의 블록 그룹(Block Group) 개념을 버리고, 플래시의 _erase_ 단위인 '세그먼트(Segment)'를 기본 단위로 사용한다.

```text
[ F2FS On-Disk Layout ]
┌───────────────────────────────────────────────────────────────┐
│  Superblock (SB) [A/B] ── 시스템 부팅 및 마운트 시 최초 참조    │
├───────────────────────────────────────────────────────────────┤
│  Checkpoint (CP)    ── 파일 시스템 일관성 복구 기준점          │
├───────────────────────────────────────────────────────────────┤
│  SIT (Segment Info) ── 블록 유효성 비트맵 (GC 대상 선정)       │
├───────────────────────────────────────────────────────────────┤
│  NAT (Node Addr)    ── 메타데이터 위치 인덱스 (L2P 테이블)     │
├───────────────────────────────────────────────────────────────┤
│  SSA (Seg Summary)  ── 블록 간 연결 정보 (복구용)              │
├───────────────────────────────────────────────────────────────┤
│                    MAIN AREA (사용자 영역)                     │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Type    │ Hot (자주 변경)  │ Warm (중간)  │ Cold (드묾)  │  │
│  ├─────────┼─────────────────┼─────────────┼──────────────┤  │
│  │ Node    │ Hot Node        │ Warm Node   │ Cold Node    │  │
│  │ (Meta)  │ (Dir entries)   │ (Inodes)    │ (xattrs)     │  │
│  ├─────────┼─────────────────┼─────────────┼──────────────┤  │
│  │ Data    │ Hot Data        │ Warm Data   │ Cold Data    │  │
│  │ (File)  │ (Journaling)    │ (DB files)  │ (Media)      │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```
**(해설)**:
위 구조에서 가장 중요한 점은 **MAIN AREA**가 6개의 타입으로 분리되어 있다는 것이다. 이를 '멀티-헤드 로깅(Multi-head Logging)'이라고 한다. 예를 들어, 동영상 파일(Cold Data)처럼 생성 후 수정이 거의 없는 데이터는 딱 한 번만 쓰이고 영원히 보존될 가능성이 높으므로, 자주 수정되는 데이터(Hot Data)와 섞이지 않도록 별도 영역에 저장한다. 이렇게 하면 나중에 쓰레기 수집(Garbage Collection)을 돌 때, "수정이 안 된 파일이 모여있는 구역"은 건드리지 않고 "수정이 잦은 구역"만 수집하면 되므로 연산량이 획기적으로 줄어든다.

#### 3. 핵심 동작 알고리즘: 멀티-헤드 로깅 (Multi-head Logging)
파일 시스템은 데이터의 **'수명(Lifetime)'**을 안다고 가정할 때 최적의 성능을 낸다.

```text
[ Write Request Flow ]
         │
         ▼
[ F2FS Kernel Layer ] ── 분류 로직 (Classification)
         │
         ├── Hot (DIR, I_NODE) ──→ [HEAD 1: Hot Node] ──→ (주로 덮어쓰임)
         │
         ├── Warm (Meta Data) ───→ [HEAD 2: Warm Node]
         │
         ├── Cold (File Attr) ───→ [HEAD 3: Cold Node] ──→ (거의 안 변함)
         │
         ├── Hot (DB Data) ──────→ [HEAD 4: Hot Data]
         │
         ├── Warm (User Docs) ───→ [HEAD 5: Warm Data]
         │
         └── Cold (Media) ───────→ [HEAD 6: Cold Data] ──→ (Write-once)
```
**코드 수준의 이해**:
리눅스 커널의 `f2fs_inode_info` 구조체에는 파일의 데이터 타입을 식별하는 필드가 있어, `f2fs_write_data_pages()` 함수 호출 시 해당 데이터의 쓰기 빈도(Heat)를 판단하여 적절한 로그 헤드(Current Log Header)에 할당한다. 이 과정은 FS(Free Segment) 개수를 지속적으로 모니터링하며 LBA(LBA) 할당 정책을 동적으로 변경한다.

> **📢 섹션 요약 비유**: F2FS의 아키텍처는 "유통기한이 짧은 생활용품과 유통기한이 긴 통조림을 입고 시점부터 다른 창고(Hot/Cold Zone)에 완벽히 분리해서 보관하는 지능형 물류 센터와 같다. 이렇게 하면 폐기(GC) 처리가 필요할 때 생활용품 창고만 뒤지면 되므로 업무 효율이 극대화된다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: F2FS vs EXT4
두 파일 시스템은 근본적인 철학에서 차이를 보인다.

| 비교 항목 | EXT4 (Fourth Extended Filesystem) | F2FS (Flash-Friendly File System) |
|:---|:---|:---|
| **설계 타겟** | HDD (Rotating Media) 최적화 | NAND Flash Memory (SSD/eMMC/UFS) 최적화 |
| **갱신 방식** | In-place Update (제자리 덮어쓰기) | Out-of-place Update (로그 구조 Append) |
| **Location** | LBA (Logical Block Address) 근접 배치 | LBA 무관, 수명 주기(Lifetime) 기반 배치 |
| **Metadata** | Block Group / Bitmap / Extent Tree | Node Address Table (NAT) / Segment Information Table (SIT) |
| **Random Write** | 느림 (Block 할당 및 Metadata 갱신 Overhead) | 빠름 (Sequential Append 방식이므로) |
| **Fragmentation** | 발생 가능성 높음 (Free space fragmentation) | 낮음 (Sequential log에 기록하므로) |
| **Write Amp.** | 높음 (F2FS 대비 1.5~2배 높은 경향) | 낮음 (Cold/Hot 분리로 GC 비용 절감) |

#### 2. 성능 메트릭스 분석 (정량적 지표)
일반적인 안드로이드 스마트폰 환경(UFS 3.0)에서의 상대적 성능 지표이다. (단위: %, EXT4를 100으로 기준)

| 작업 유형 | EXT4 | F2FS | 비고 |
|:---:|:---:|:---:|:---|
| **Sequential Write** | 100 | 100 | 순차 쓰기는 물리적 대역폭에 의해 제약됨 |
| **Random Write** | 100 | **210** | 로그 구조의 강점, EXT4의 단점 극복 |
| **SQLite (DB)** | 100 | **250** | 안드로이드 앱 설치 및 DB 작업 성능 향상 |
| **Read Speed** | 100 | 105 | Read는 큰 차이 없으나 Fragmentation 감소로 소폭 상승 |

#### 3. 타 과목 융합 관점
- **운영체제(OS)**: F2FS는 Linux Kernel VFS (Virtual File System) 계층 아래에서 동작하며, Page Cache와 밀접하게 연동된다. Dirty Page를 플러시(Flush)할 때 F2FS의 로그 버퍼를 거치게 된다. 이때 `f2fs_balance_fs()` 함수를 통해 메모리 매핑된 NAT/SIT 정보를 주기적으로 동기화한다.
- **컴퓨터 구조**: FTL (Flash Translation Layer)과의 상호작용이 중요하다. F2FS가 Hot/Cold 데이터를 분리해서 보내주면, FTL 입장에서도 더 효율적인 Wear Leveling(마모 평준화)을 수행할 수 있어 시너지가 발생한다.

> **📢 섹션 요약 비유**: EXT4가 "기존의 시내버스 노선(정류장 순서대로 이동하는 HDD 방식)"이라면, F2FS는 "고속도로의 하이패스 차선(목적지별로 분리되어 혼잡을 피하는 Flash 방식)"과 같다. 손님(데이터)의 성격에 따라 차선을 미리 나누어 놓아 전체 도로의 처리량(Throughput)을 극대화한다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스
시스템 엔지니어가 파일 시스템을 선택할 때 고려해야 할 의사결정 트리이다.

```text