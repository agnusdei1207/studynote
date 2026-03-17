+++
title = "547. 로그 구조 파일 시스템 (Log-structured File System) / 저널링 (Journaling)"
date = "2026-03-14"
weight = 547
+++

# 547. 로그 구조 파일 시스템 (Log-structured File System) / 저널링 (Journaling)

## 핵심 인사이트 (3줄 요약)
> 1. **본질 (Essence)**: **저널링 (Journaling)**은 변경 사항을 로그에 선기록(Write-Ahead)하여 트랜잭션 원자성을 보장하고, **LFS (Log-structured File System)**는 모든 데이터를 갱신(Update)하지 않고 로그 끝에 추가(Append-only)하여 **Seek Time (탐색 시간)**을 제거하는 디스크 대역폭 최적화 아키텍처이다.
> 2. **가치 (Value)**: 기존 **FFS (Fast File System)**의 **Random Access (랜덤 액세스)** 병목을 해소하여 디스크 **Throughput (처리량)**을 극대화하며, 시스템 크래시(Crash) 시 복잡한 **fsck (File System Check)** 없이 로그 리플레이(Replay)로 초고속 복구(RTO 단축)를 달성한다.
> 3. **융합 (Synergy)**: LFS의 순차 쓰기 철학은 **SSD (Solid State Drive)**의 **Wear Leveling (마모 평준화)** 및 **FTL (Flash Translation Layer)** 설계의 기반이 되었으며, 데이터베이스의 **WAL (Write-Ahead Logging)** 및 최신 **CoW (Copy-on-Write)** 파일 시스템(ZFS, Btrfs)의 이론적 토대이다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
전통적인 파일 시스템(UNIX FS, FFS)은 데이터를 디스크의 고정된 블록에 위치시키고 수정 시 해당 블록을 덮어쓰는 **In-place Update (제자리 갱신)** 방식을 사용한다. 이는 데이터의 공간적 지역성(Spatial Locality)을 유지하지만, 쓰기 연구 발생 시 디스크 헤드가 Inode 영역과 Data 블록 영역을 오가야 하므로 막대한 **Seek Time (탐색 시간)**이 발생한다.

반면, **로그 구조 파일 시스템 (LFS)**과 **저널링 (Journaling)**은 시간의 흐름에 따라 발생하는 모든 변경 사항을 디스크의 순차적인 영역에 기록하는 **Temporal (시간 지향적)** 접근 방식을 취한다.
- **저널링**: 메타데이터의 일관성을 보장하기 위해 변경 사항을 실제 반영 전에 별도의 순차 영역(Journal Area)에 먼저 기록하는 기술이다.
- **LFS**: 저널링의 개념을 확장하여 파일 시스템의 *모든* 데이터와 메타데이터를 로그의 끝에 추가(Append)만 하여, 쓰기 연산을 완전한 순차 쓰기로 변환하는 설계 기법이다.

이는 CPU 속도와 디스크 속도의 격차(Memory Wall)가 벌어지면서, 디스크 쓰기가 병목 구간이 되자 이를 해소하기 위해 등장한 패러다임이다.

### 2. 등장 배경 및 진화
① **기존 한계 (The I/O Bottleneck)**: 1990년대 Ousterhout 등의 연구에 따르면, 당시 UNIX 파일 시스템은 디스크의 최대 순차 전송 속도의 단 5~10%만 활용할 뿐이었다. 대부분의 시간은 블록을 찾기 위한 **Seek (탐색)**과 **Rotational Latency (회전 지연)**에 낭비되었다.
② **혁신적 패러다임 (Log-Structure)**: "CPU와 메모리 속도는 빠르고, 디스크는 느리다. 그렇다면 메모리에 모아둔 데이터를 디스크에는 한 번에 쏟아내자(Write Buffering)"는 전략이 등장했다. 이를 위해 랜덤 쓰기를 제거하고 순차 쓰기만 수행하여 디스크 대역폭을 100% 활용하고자 했다.
③ **비즈니스 요구 (Availability)**: 대용량 디스크(터라바이트 급) 등장으로 기존 방식인 **fsck (File System Check)**는 시스템 부팅 시 수시간이 걸릴 수 있어 24/7 서비스 환경에서 치명적이었다. 저널링을 통해 복구 시간을 초단위로 줄일 필요가 있었다.

### 3. 구조적 시각화: 공간 vs 시간
```text
      [ Traditional Spatial Layout ]           [ Log-structured Temporal Layout ]

  Block Group 1        Block Group 2          Segment 1 (Time T1)
+------------------+  +------------------+  +-----------------------------+
| Inode Table      |  | Inode Table      |  | Tx 1: Inode Update (File A)|
| Data Blocks      |  | Data Blocks      |  | Tx 2: Data Write (File B)  |
| (Fixed Location) |  | (Fixed Location) |  +-----------------------------+
+------------------+  +------------------+           |
      ^    ^   ^        ^    ^   ^               | Data grows sequentially
      |    |   |        |    |   |               v
    Seek  Seek Seek    Seek Seek Seek      +-----------------------------+
  (Random Access overhead)               | Segment 2 (Time T2)         |
                                         | Tx 3: Data Append (File A)  |
                                         +-----------------------------+
```
*그림 1-1. 공간 기반(Spatial) 배치와 로그 기반(Temporal) 배치의 데이터 흐름 비교*

**해설**: 전통적인 시스템은 파일 A를 수정하기 위해 Inode 영역과 Data 영역을 왔다 갔다 해야 하지만(Seek), LFS는 버퍼에 모아서 디스크 끝에 한꺼번에 쓰기만 하면 된다. 이는 비행기가 착륙하여 여러 곳을 방문하는 것보다, 공중에서 물자를 투하하는 것과 같은 효율을 가진다.

📢 **섹션 요약 비유**: 저널링과 LFS는 "도서관 사서가 책장에 꽂힌 원본을 찾아다니며 직접 수정하는 것(전통 방식) 대신, 연필로 수정할 내용을 **일지(Journal)**에 미리 적어두고, 장소에 상관없이 **창고 끝(Log)**에 새로운 책장을 계속 추가하는 방식"과 같습니다. 이렇게 하면 중간에 정전이 와도 일지를 보고 복구할 수 있고, 책장 사이를 오가는 시간을 획기적으로 줄일 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (Components)
LFS 및 저널링 시스템의 작동을 위해 다음과 같은 5가지 핵심 모듈이 필요하다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/특징 |
|:---|:---|:---|:---|
| **Transaction** | 원자적 작업 단위 | 여러 개의 블록 쓰기(메타데이터+데이터)를 묶어 All-or-Nothing 보장 | Atomicity, Consistency |
| **Journal Area** | 순차 쓰기 버퍼 영역 | 실제 파일 시스템 영역과 분리된 고속 순차 기록 영역. Circular Queue 관리 | **WAL (Write-Ahead Logging)** |
| **Checkpoint** | 영구화 지점 | 메모리 상의 변경 사항을 메인 파일 시스템 영역(Home)에 반영하고 커밋하는 시점 | Periodic Sync, Consistent State |
| **Segment** | 쓰기 최적화 단위 (LFS) | 여러 개의 파일 블록과 Inode를 모아서 한 번에 디스크에 기록하는 큰 단위 | Large Block I/O, Efficiency |
| **Cleaner (GC)** | 공간 회수기 (LFS) | 유효 블록(Live)과 무효 블록(Dead)을 분류하고, 유효 블록만 모아서 Compaction 수행 | Garbage Collection, Read/Modify/Write |

### 2. 저널링의 데이터 무결성 메커니즘 (WAL Protocol)
저널링 파일 시스템(예: ext4, NTFS)의 쓰기 작업은 다음과 같은 **WAL (Write-Ahead Logging)** 프로토콜을 엄격히 준수하여 시스템 크래시 시 데이터를 보호한다.

```text
[Step 1: Begin]  [Step 2: Journal Write]  [Step 3: Commit]    [Step 4: Checkpoint]
   (TX Start) --> (Log to Disk)       --> (Mark Complete) --> (Write to Main FS)
+-------------+  +-------------------+  +----------------+  +---------------------+
| TxB = 1001  |  | J-Blk: Meta Data |  | TxB=Commit     |  | FS Blk <= J-Blk     |
| LSN = 50    |  | J-Blk: File Data |  | Checksum=OK    |  | (Background Flush)  |
+-------------+  +-------------------+  +----------------+  +---------------------+
      |                  |                       |                      |
      v                  v                       v                      v
 [Memory Cache]    [Disk Journal]          [Disk Journal]         [Disk Main Area]
                   (Sequential Write)       (Metadata Update)      (Random Write)

*Crash Recovery Scenarios*:
1. Crash at Step 2: Transaction Incomplete -> Ignored (Rollback).
2. Crash at Step 3: Transaction Commited -> Re-apply to Main Area (Rollforward).
3. Crash at Step 4: Safe (Already in Journal, will be Checkpointed later).
```
*그림 2-1. 저널링 파일 시스템의 쓰기 단계 및 상태 전이 다이어그램*

**해설**:
1. **Journal Write**: 데이터를 실제 위치에 쓰기 전에 먼저 저널 영역에 순차적으로 기록한다. 이 단계가 완료되면 트랜잭션은 논리적으로 성공한 것으로 간주된다.
2. **Commit**: 트랜잭션의 끝을 표시하고 체크섬(Checksum)을 업데이트하여 무결성을 검증한다.
3. **Checkpoint**: 백그라운드 프로세스가 저널의 데이터를 실제 파일 시스템의 고정 위치(Home Location)로 옮긴다. 이때는 랜덤 액세스가 발생하지만, 이미 데이터는 안전하게 보호되어 있으므로 성능보다는 정확성에 집중한다.

### 3. LFS의 핵심: 세그먼트(Segment) 구조와 청소(Cleaning)
LFS는 단순 저널링을 넘어 파일 시스템 전체를 하나의 순환 로그(Circular Log)로 관리한다. 이에 따라 독특한 **Inode Map**과 **Cleaning** 메커니즘이 필요하다.

```text
[ LFS Segment Layout on Disk ]

+-------------------+  +-------------------+  +-------------------+
| Segment 1 (Fixed) |  | Segment 2 (Fixed) |  | Segment 3 (Fixed) |
| [Summary][Data]   |  | [Summary][Data]   |  | [Summary][Data]   |
+-------------------+  +-------------------+  +-------------------+
     ^                      ^                      ^
     |                      |                      |
     +----------+-----------+-----------+----------+
                |
                v
        (Log grows to the right)

[ Cleaning Process (Garbage Collection) ]

Current State:           After Cleaning:
+-------------------+    +-------------------+
| Live (20%)         |    | Live (20%)         | --> Moved to new segment
| Dead (80%)         |    | Dead (100%)         | --> Freed for reuse
+-------------------+    +-------------------+
  (Victim Segment)        (Free Segment)

Steps:
1. Select a segment with low utilization (High dead ratio).
2. Read live blocks from the victim segment.
3. Write live blocks compactly into a new segment (in memory buffer).
4. Update the Inode Map (Old Segment -> New Segment).
5. Write the new segment to the head of the log.
6. Mark the old segment as FREE.
```
*그림 2-2. LFS의 세그먼트 구조 및 가비지 컬렉션(Cleaning) 동작 과정*

**해설**:
LFS의 가장 큰 문제는 **공간 낭비(Space Waste)**와 **청소 비용(Cleaning Overhead)**이다. 파일을 수정할 때마다 새 위치에 쓰기 때문에(Old version becomes dead), 디스크 전체가 유효 데이터(Live)와 오래된 데이터(Dead)의 뒤죽박죽이 된다.
이를 해결하기 위해 **Cleaner**는 마치 메모리의 Compaction처럼, 오래된 세그먼트 중 **이용률(Utilization)**이 낮은 것을 골라 유효한 데이터만 취하여 모은 뒤, 로그의 끝에 다시 기록한다. 이 과정에서 **Inode Map**이 갱신되어 파일의 논리적 위치가 바뀌게 된다.

📢 **섹션 요약 비유**: LFS의 작동 원리는 "무한히 확장 가능한 **롤링 페이퍼(Rolling Paper)**"와 같습니다. 일기(데이터)를 쓸 때마다 지운 다음 쓰는 것이 아니라, 종이의 끝에 계속해서 내용을 추가(Append)로 적어나갑니다. 종이가 다 쓰면, 안 쓰는 페이지는 찢어내고(Garbage Collection), 다시 새 롤을 연결하여 계속 사용합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교 (Traditional vs Journaling vs LFS)

| 구분 | 전통적 FS (e.g., BSD FFS) | 저널링 FS (e.g., ext4, NTFS) | 로그 구조 FS (e.g., LFS, NILFS) |
|:---|:---|:---|:---|
| **쓰기 방식** | **In-place Update** (Random Write) | **WAL**: Low overhead<br>Ordered Mode: 1-pass | **Append-only** (Sequential Write) |
| **순차 읽기 성능** | **높음** (데이터가 인접해 있음) | 높음 (Ordered 모드 유지) | 낮음 (파일의 블록들이 시간순으로 흩어짐) |
| **순차 쓰기 성능** | 낮음 (Seek 오버헤드 큼) | 중간 (저널 쓰기는 빠름, 체크포인트 지연) | **매우 높음** (디스크 대역폭 극대화) |
| **복구 속도 (RTO)** | 느림 (전체 블록 스캔: `fsck`) | **매우 빠름** (저널 리플레이만 수행) | 빠름 (체크포인트 + 로그 리플레이) |
| **공간 효율성** | 높음 (조각화만 관리하면 됨) | 중간 (저널 영역 낭비) | 낮음 (Cleaning Overhead, Dead Block 발생) |
| **주요 적용 분야** | 일반 범용 OS (Read optimized) | 범용 서버, 표준 리눅스/윈도우 | **SSD**, WORM 미디어, 로그 서버, 임베디드 |

### 2. 타 과목 융합 관점 분석

**1)