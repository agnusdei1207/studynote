+++
title = "551. EXT4 파일 시스템 구조"
date = "2026-03-14"
weight = 551
+++

# 551. EXT4 파일 시스템 구조 (Architecture of EXT4 File System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EXT4 (Fourth Extended File System)는 리눅스 커널의 사실상의 표준 파일 시스템(De Facto Standard)으로, 기존 EXT3의 간접 블록 매핑(Indirect Block Mapping) 방식을 혁신적인 **Extent (연속 블록 매핑)** 기반의 B-Tree(Balanced Tree) 구조로 대체하여 메타데이터 오버헤드를 극적으로 감소시킨 저널링 파일 시스템(Journaling File System)이다.
> 2. **가치**: **지연 할당(Delayed Allocation)**과 **다중 블록 할당(Multi-Block Allocation)** 기술을 통해 대용량 파일 처리 시 디스크 단편화(Fragmentation)를 획기적으로 억제하며, 48비트 블록 주소 공간을 통해 최대 1EB(Exabyte)의 볼륨과 16TB의 단일 파일을 지원하여 대규모 엔터프라이즈 환경의 안정성을 보장한다.
> 3. **융합**: 하위 호환성을 완벽히 유지하면서도 **저널 체크섬(Journal Checksumming)**을 통해 데이터 무결성을 강화하였고, VFS(Virtual File System) 계층과의 긴밀한 결합을 통해 네트워크 스토리지(NAS/SAN) 및 클라우드 환경까지 아우르는 범용성을 확보하였다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**EXT4 (Fourth Extended File System)**는 리눅스 커널 2.6.19에서 개발되어 2.6.28부터 안정판으로 채택된 로그 구조 파일 시스템이다. 이는 단순한 확장을 넘어 EXT3 시리즈의 구조적 한계를 극복하기 위해 설계된 차세대 파일 시스템으로, 대용량 스토리지 환경과 고성능 I/O 처리를 위해 설계되었다.

### 2. 기술적 진화 배경
EXT3가 성공적이었으나, 테라바이트(TB)급 스토리지 시대가 도래함에 따라 다음과 같은 세 가지 치명적인 한계가 노출되었다.
1.  **블록 주소 공간 한계**: 32비트 블록 주소 방식으로 인해 최대 16TB 파일 시스템 제한 존재.
2.  **메타데이터 확장성 문제**: 전통적인 `inode`의 직접/간접 블록 포인터 방식은 대용량 파일(수 GB 이상)에서 메타데이터가 급증하여 성능 저하를 유발.
3.  **단편화 및 쓰기 성능**: 실시간 할당 방식으로 인해 디스크 단편화가 심화되는 문제.

이를 해결하기 위해 EXT4는 **Extent** 기반 매핑과 **48비트 블록 주소(블록 크기에 따라 16TB~1EB 지원)**를 도입하였다.

### 3. 아키텍처적 파급 효과
파일 시스템이 I/O 경로에서 병목 지점이 되는 것을 방지하기 위해, 메모리와 디스크 간 데이터 동기화 정책을 재설계하였으며, 이는 데이터베이스(DBMS)의 WAL(Write-Ahead Logging) 성능과 직결되는 중요한 개선이었다.

> **📢 섹션 요약 비유**: EXT4의 등장은 "기존의 '주소록 방식(EXT3)'으로는 관리가 불가능해진 거대 도시의 물류망을 위해, 모든 물건의 위치를 개별적으로 추적하는 대신 '구역 단위(Extent)'로 관리하는 초고속 물류 통제 시스템'을 도입한 것과 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Architecture & Core Principles)

EXT4의 성능 향상은 파일 데이터의 위치를 저장하는 방식의 근본적인 변화에 기인한다. 이 섹션에서는 디스크 레이아웃과 핵심 메커니즘인 Extent를 분석한다.

### 1. 디스크 레이아웃 시각화 (Disk Layout Visualization)
EXT4는 볼륨을 여러 개의 **블록 그룹(Block Group)**으로 나누며, 각 그룹은 독립적인 메타데이터 영역과 데이터 영역을 가진다. 유연성을 위해 **Flex Block Group** 기능을 사용하여 메타데이터를 묶어서 관리하기도 한다.

```text
[ EXT4 Volume Structure Overview ]
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Boot Block & Reserved Space                          │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Block Group 0 (Primary)                            │
├─────────┬─────────┬─────────┬─────────┬─────────┬───────────────────────────┤
│ Super   │ GDT     │Reserved │ Block   │ Inode   │      Data Blocks          │
│ Block   │(Group   │(GDT     │ Bitmap  │ Bitmap  │ (Actual File Contents)    │
│         │ Desc    │ Backup) │         │         │                           │
├─────────┴─────────┴─────────┴─────────┴─────────┴───────────────────────────┤
│                          Block Group 1...N                                  │
│  ┌───────────┬─────────────┬─────────────┬─────────────┬─────────────────┐   │
│  │ Inode     │ Inode       │ Block       │      Data Blocks (Data Blocks  │   │
│  │ Table     │ Bitmap      │ Bitmap      │             │  may span groups)│   │
│  └───────────┴─────────────┴─────────────┴─────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

*   **Super Block**: 전체 파일 시스템의 파라미터(총 블록 수, 마운트 횟수 등) 저장.
*   **GDT (Group Descriptor Table)**: 각 블록 그룹의 위치 정보를 가진 테이블. 백업본이 존재하여 복구에 활용됨.
*   **Inode Table**: 파일의 메타데이터(권한, 크기, 타임스탬프, **Extents Tree 포인터**)를 저장.

### 2. 핵심 메커니즘: Extent Tree 구조 (Deep Dive)
EXT4의 가장 큰 특징은 `inode` 내부에서 파일의 데이터 블록을 가리키는 방식이 **Extents**로 변경된 것이다.

#### A. 기존 방식 (EXT3 Indirect Block) vs EXT4 (Extents)
| 구분 | EXT3 (Indirect Mapping) | EXT4 (Extent Mapping) |
|:---|:---|:---|
| **기본 단위** | 블록 번호 1개씩 | 논리적 블록의 연속된 묶음 |
| **메타데이터** | 4KB 데이터 기준 12개(직접) + 3단계(간접) 필요 | 1개의 Extent(초기 4개 트리 노드)로 최대 128MB 표현 |
| **대용량 파일** | 트리 깊이가 깊어져 탐색 비용 증가 | B+Tree 구조로 탐색 복잡도 $O(\log N)$ 유지 |
| **구조** | 고정된 4중 간접 포인터 | 동적 트리 구조 (Depth 0~5) |

#### B. Extent 구조 세부 필드 분석
하나의 Extent는 12바이트 크기의 구조체로 다음 정보를 포함한다.
1.  **Logical Block**: 파일 내에서의 논리적 시작 위치 (예: 파일의 0번째 블록)
2.  **Physical Block**: 디스크 상의 실제 물리적 시작 블록 번호
3.  **Length**: 연속된 블록의 개수 (최대 2^15개, 즉 128MB)

```text
[ EXT4 Extent Tree in Inode ]
      ┌───────────────┐
      │     Inode     │
      │  (Metadata)   │
      └───────┬───────┘
              │
      ┌───────▼───────┐      (Root Node of Extent Index)
      │ Extent Header │      ┌───┬───┬───┬───┐
      │ (Depth, etc)  │      │idx│idx│...│idx│  <- Logical Block Offsets
      └───────┬───────┘      └─┬─┴─┬─┴───┴─┬─┘
              │                │   │      │
      ┌───────▼────────────────▼───▼──────▼────┐
      │    Extent Index (Intermediate Node)     │  ─┐
      │ "Points to next level"                  │   │
      └──────────────────────────────────────────┘  ├─ B+Tree (Height Dynamic)
      ┌──────────────────────────────────────────┐  │
      │    Extent Leaf (Data Node)               │  ─┘
      │ [Log: 0] -> [Phys: 100] -> [Len: 1024]   │
      │ [Log: 1024] -> [Phys: 5000] -> [Len: 2048]│
      └──────────────────────────────────────────┘
```
*(해설: EXT4는 파일이 커질수록 Extent Leaf 노드를 생성하고, 이를 관리하기 위해 인덱스 노드를 추가하여 B+Tree 형태로 확장한다. 이로 인해 수 GB 파일이라도 디스크 헤드의 최소한의 이동(Seeks)으로 위치를 찾을 수 있다.)*

### 3. 핵심 알고리즘 및 코드
대용량 파일 생성 시 `fallocate` 시스템 콜을 사용하면 파일 시스템은 실제 데이터를 쓰지 않고도 메타데이터(Extent)만 미리 할당하여 성능을 확보한다.

```c
/* fallocate 시스템 콜 개념적 흐름 (Linux Kernel) */
SYSCALL_DEFINE(fallocate, int, fd, int, mode, loff_t, offset, loff_t, len) {
    /* 1. 파일 시스템이 extent 기반 지원 여부 확인 (EXT4는 지원) */
    if (!inode->i_op->fallocate)
        return -EOPNOTSUPP;

    /* 2. 파일 락 획득 및 Inode 동기화 */
    mutex_lock(&inode->i_mutex);

    /* 3. EXT4_ES_MAGIC: Extent Status Tree 영역에 공간 예약 할당 */
    /* 실제 블록을 디스크에 쓰는 것이 아니라, 비트맵만 설정 */
    ret = inode->i_op->fallocate(inode, mode, offset, len);
    
    /* 4. 초기화되지 않은 데이터 영역(NOSPACE) 표시 */
    mutex_unlock(&inode->i_mutex);
    return ret;
}
```

> **📢 섹션 요약 비유**: EXT4의 Extent 구조는 "수백 페이지짜리 책의 목차에서 '1장: 1쪽~10쪽', '2장: 11쪽~50쪽' 처럼 연속된 페이지를 '구간'으로 관리하는 것"과 같습니다. 예전 방식(Indirect)은 '1쪽은 주소 A, 2쪽은 주소 B...'처럼 쪽마다 주소를 일일이 적어야 했기에 목차만으로도 책 한 권을 만들었던 셈입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교 분석표 (Quantitative Comparison)
EXT4는 다른 파일 시스템(XFS, Btrfs)과 비교할 때 범용성과 안정성에 초점을 맞추고 있다.

| 비교 항목 | EXT4 | XFS (High Performance) | Btrfs (Next Gen) | ZFS (Zettabyte) |
|:---|:---|:---|:---|:---|
| **최대 파일 크기** | 16 TB (4KB Block) | 8 EB (즉시 16TB 지원) | 16 TB | 16 EB |
| **최대 볼륨 크기** | 1 EB (48-bit Block) | 8 EB | 16 EB | 256 QB (Quadrillion) |
| **메타데이터 방식** | Extent Tree | B+ Tree (Alloc BTree) | B+ Tree (Copy-on-Write) | DMU (Copy-on-Write) |
| **동적 I-node** | 지원 (ea_inode) | 지원 | 고정 개념 없음 | 동적 할당 (ZPL) |
| **저널링 (Journaling)** | Ordered/Writback/Recovery | **Journaling (가변 크기)** | **Copy-on-Write (COW)** | **Copy-on-Write (COW)** |
| **스냅샷 (Snapshot)** | 지원 안 함 (LVM에 의존) | 지원 (Calc와 독립) | **네이티브 지원 (빠름)** | **네이티브 지원** |
| **주요 용도** | 범용 서버/안드로이드 | 대용량 멀티미디어/DB | 복잡한 스토리지/백업 | 엔터프라이즈 스토리지 |

### 2. OS 및 네트워크와의 융합 (Convergence)

#### A. 가상 메모리 시스템과의 연계 (Page Cache)
리눅스 커널의 **MM (Memory Management)** 계층에서 `read()` 시스템 콜이 호출되면, 디스크 I/O 없이 페이지 캐시(Page Cache)를 반환한다. EXT4는 `readahead`(선행 읽기) 알고리즘과 결합하여, Extent 정보를 참조하여 **연속된 128MB**의 데이터를 순차적으로 메모리로 로드하여 미리 읽기 효율을 극대화한다.

#### B. 데이터베이스(DBMS)와의 관계
대부분의 RDBMS(MySQL, PostgreSQL)는 OS의 파일 시스템 위에 데이터 파일을 생성한다. EXT4의 ** barriers (디스크 쓰기 순서 보장)** 옵션은 WAL(Write-Ahead Logging)의 ACID 속성을 보장하는 데 필수적이다. 만약 EXT4에서 `barrier=0`으로 설정 시 정전 발생 시 데이터베이스 복구가 불가능해질 수 있다.

#### C. 네트워크 스토리지(NFS)와의 동기화
NFSv4 서버 구현 시 EXT4의 **i_version** 필드(inode 변경 버전)를 활용하여 클라이언트에게 캐시 유효성을 신속하게 알릴 수 있다.

> **📢 섹션 요약 비유**: EXT4와 다른 파일 시스템의 관계는 "범용 세단(EXT4), 스포츠카(XFS), 지프형 캠핑카(Btrfs), 그리고 이동식 집(ZFS)"의 관계와 같습니다. 범용 세단은 거의 모든 도로(Linux 환경)에서 부드럽게 달리고 연비도 좋지만(안정적), 극한의 속도나 특수한 기능(스냅샷 등)이 필요하면 전문차량(Btrfs, ZFS)을 사용하는 것이 유리합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 매트릭스

#### 시나리오 A: 대규모 로그