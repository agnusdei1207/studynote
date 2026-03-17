+++
title = "549. 스냅샷 (Snapshot) 및 복구 기술"
date = "2026-03-14"
weight = 549
+++

# # [스냅샷 (Snapshot) 및 복구 기술]

## #### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스냅샷(Snapshot)은 데이터 블록의 물리적 복제 없이 특정 시점(Point-in-Time)의 메타데이터(Metadata) 포인터를 고정함으로써, 논리적이고 즉각적인 데이터 보존을 가능하게 하는 가상화된 저장소 추상화 계층입니다.
> 2. **가치**: COW (Copy-on-Write) 또는 ROW (Redirect-on-Write) 알고리즘을 통해 저장 공간 효율성을 극대화하며, RPO (Recovery Point Objective)를 '0'에 수렴하게 하여 24/7 업무 연속성을 보장합니다.
> 3. **융합**: 가상화 플랫폼(Hypervisor), 스토리지 가상화(SAN/NAS), 클라우드 환경(AWS EBS Snapshot 등)의 근간이 되며, 랜섬웨어 대응 및 DevOps 환경의 CI/CD 파이프라인에서 무중단 배포 전략의 핵심 인프라로 작용합니다.

---

## ### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
스냅샷(Snapshot)이란 저장 장치(Storage) 내의 데이터 집합에 대해 특정 시점(Time Zero)의 상태를 캡처한 것으로, 파일 시스템(File System) 또는 논리 볼륨(Logical Volume) 전체에 대한 읽기 일관성 있는(Read-Consistent) 논리적 사본을 의미합니다. 물리적으로 데이터 전체를 복사하는 방식(Full Copy)이 아닌, 해당 시점의 데이터 블록 위치 정보를 포함하는 메타데이터(Map Table, Bitmap, Inode Tree)를 동결(Freeze)시키는 기술적 메커니즘을 말합니다.

**등장 배경 및 기술적 패러다임**
1.  **기존 한계 (Legacy Backup)**: 전통적 백업은 데이터 양이 방대해질수록 백업 윈도우(Backup Window)가 길어져, 24/7 비즈니스 환경에서 서비스 중단(Downtime)이 불가피하며, 증분 백업 관리의 복잡도가 증가했습니다.
2.  **혁신적 패러다임 (Virtualization)**: '스냅샷' 기술은 데이터 변경 블록만 추적하거나 포인터만 조작하는 방식을 도입하여, 수 TB(Terabyte) 급 데이터라도 수초 내에 백업 포인트를 생성하는 것을 가능하게 했습니다.
3.  **현재 비즈니스 요구 (Cyber Resilience)**: 랜섬웨어(Ransomware) 공격의 고도화와 더불어, '불변성(Immutability)'을 가진 스냅샷은 최후의 복구 수단으로서 재해 복구(Disaster Recovery) 계획의 필수 요소이자, 사이버 복원력(Cyber Resilience)의 핵심입니다.

```text
[ Evolution of Data Protection ]

Time Consuming (Hours)          Time Consuming (Seconds)
<-------------------------->    <-------------------->
|                            |    |                    |
[Full Backup] ---------> [Incremental] -----> [Snapshot]
(Tape / Disk Copy)         (File Level Diff)      (Metadata Pointer)
```

**💡 섹션 비유**
> **스냅샷은 '도서관의 도서 대출 카드(목록)'와 같습니다.** 책(원본 데이터)을 읽는 사람에게 그대로 두고, 사서(시스템)는 대장(메타데이터)에 "지금 이 시각의 도서 상태"를 기록합니다. 그 후 책이 새로운 버전으로 교체(수정)되더라도, 대장에 남은 기록(스냅샷)을 통해 과거 그 순간의 상태를 즉시 확인하고 복원할 수 있습니다.

---

## ### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스냅샷 구현의 핵심은 **CoW (Copy-on-Write)** 엔진과 **메타데이터 관리**, 그리고 **공간 재할당(Redirection)** 전략에 있습니다.

#### 1. 주요 구성 요소 (Component Table)

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Metadata Map (LBA Table)** | 데이터 위치 지도 | 논리적 블록 주소(LBA)와 물리적 디스크 주소(PBA) 간의 매핑 테이블 관리 | ZFS (DMU), LVM | 도서의 목차 |
| **Original Block (Active Data)** | 최초 데이터 | 현재 활성화된 데이터 블록 (읽기/쓰기 가능) | Block I/O | 현재 집필 중인 원고 |
| **Copy-on-Write Engine** | 데이터 수정 관제자 | 쓰기 요청 시 원본 블록의 '보호 상태'를 확인 후 보존(Save) 또는 재기록(Override) 수행 | IOCTL, FS Driver | 훈수 담당자 (심판) |
| **Snapshot Store (Reserved Pool)** | 보관 영역 | 변경되기 직전의 원본 블록(Old Block)들이 이동하여 저장되는 공간 (Sparse Volume) | COW Pool, Log | 보관창고 (폐기될 원고 보관) |
| **Space Reclaimer (GC)** | 공간 반환자 | 스냅샷 삭제 시, 더 이상 참조되지 않는 블록을 식별하여 여유 공간(Free List)으로 반환 | Garbage Collection | 폐지 수집대 |

#### 2. ASCII 구조 다이어그램: Copy-on-Write (CoW) 매커니즘

```text
[ Copy-on-Write (CoW) Execution Flow ]

  State 1: Snapshot Creation (T0)           State 2: Write Request on Block A (T1)
  ┌───────────────────────┐                ┌───────────────────────┐
  │  Metadata Map (Table)  │                │  Metadata Map (Table)  │
  ├───────────┬───────────┤                ├───────────┬───────────┤
  │ LBA A      │ PBA [100] │◄───┐           │ LBA A      │ PBA [105] │◄─── New Ptr
  │ LBA B      │ PBA [200] │     │           │ LBA B      │ PBA [200] │
  └───────────┴───────────┘     │           └───────────┴───────────┘
       ▲    │                   │                ▲    │
       │    └─ Refers to        │                │    └─ Refers to
       ▼                        │                ▼
  [Physical Disk Layout]         │           [Physical Disk Layout]
  ┌─────────────────────┐       │           ┌─────────────────────┐
  │ 100: [Data A]       │       │           │ 100: [Data A]       │ (Kept for Snap)
  │ 200: [Data B]       │       │           │ 200: [Data B]       │
  └─────────────────────┘       │           │ 105: [Data A' ]     │ (New Data)
                                │           └─────────────────────┘
          [Step 2-1: Copy Old Block to Snap Pool]
```

**해설 (Deep Dive)**
1.  **스냅샷 생성 (State 1)**: T0 시점에서 시스템은 데이터 블록(A, B)을 복사하지 않고, 단순히 해당 시점의 메타데이터 포인터 테이블(Map Table)을 복제해 둡니다. 이때 물리적 디스크(PBA 100, 200)는 변화가 없으므로 공간을 소비하지 않습니다.
2.  **데이터 쓰기 요청 (State 2)**: 사용자가 블록 A의 내용을 수정하려고 하면, CoW 엔진은 I/O 요청을 가로챕니다.
    *   **원본 보존**: 기존 물리적 블록 `[PBA 100]`에 있는 데이터 `[Data A]`를 스냅샷 풀(Snapshot Pool)로 보존합니다. (실제로는 이동시키지 않고 포인터만 끊어버리는 방식도 존재)
    *   **신규 기록**: 새로운 데이터 `[Data A']`를 쓸 새로운 물리적 블록 `[PBA 105]`를 할당(Allocation)받아 기록합니다.
    *   **포인터 업데이트**: 메타데이터 테이블의 `LBA A` 포인터를 `[PBA 105]`로 변경합니다.
3.  **결과**: 현재 파일 시스템은 최신 데이터(`A'`)를 보게 되고, 스냅샷은 여전히 과거 데이터(`A`)를 참조하게 됩니다.

#### 3. 핵심 알고리즘 (CoW Write Logic)

```python
# Pseudo-code: Copy-on-Write Write Operation
def cow_write(logical_block_addr, new_data):
    # 1. Look up current physical address
    current_pba = lookup_translation_table(logical_block_addr)
    
    # 2. Check if block is shared (referenced by snapshot)
    if is_block_shared(current_pba):
        # [Performance Critical Path]
        # Allocate new physical block
        new_pba = allocate_free_block()
        
        # Copy old data to new block (Background or Foreground)
        # NOTE: This read operation adds latency
        copy_data(src=current_pba, dst=new_pba)
        
        # 3. Update Snapshot Map (Source block becomes immutable)
        update_snapshot_map(logical_block_addr, current_pba)
        
        # 4. Update Active Map (Target block becomes active)
        update_translation_table(logical_block_addr, new_pba)
        
        target_pba = new_pba
    else:
        # Block is not shared, overwrite directly
        target_pba = current_pba

    # Finally, write new data
    write_disk(target_pba, new_data)
```

**📢 섹션 요약 비유**
> 스냅샷 기술의 동작 원리는 **"건물의 리모델링 시, 도면만 바꾸는 공법"**과 같습니다. 건물(데이터)을 통째로 다시 짓는 대신, 구조 변경이 필요할 때 기존 부실(원본 블록)은 그대로 둔 채, 새로운 부실(신규 블록)을 증축하고 입구 명판(메타데이터)만 새로운 곳으로 바꿉니다. 과거의 도면(스냅샷)을 가지고 있다면, 언제든지 리모델링되기 전의 건물 상태로 되돌릴 수 있습니다.

---

## ### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: CoW vs. RoW (Redirect-on-Write) vs. Full Clone

| 구분 (Criteria) | **Copy-on-Write (CoW)** | **Redirect-on-Write (RoW)** | **Full Clone (Full Copy)** |
|:---|:---|:---|:---|
| **작동 방식 (Mechanism)** | 쓰기 시, 원본 블록을 보관 영역으로 복사 후 신규 블록에 기록 | 쓰기 시, 원본 블록은 건드리지 않고 새로운 위치에만 기록 (In-place Update 지양) | 스냅샷 생성 시 데이터 전체를 물리적으로 복제 |
| **쓰기 성능 (Write Penalty)** | 낮음~중간 (Read + Write + Map Update 2회 발생) | 높음 (Sequential Write 유리, Random Write 시 Fragmentation 심화) | 가장 높음 (Direct Access, Overhead 없음) |
| **읽기 성능 (Read Perf.)** | 높음 (데이터가 연속적 위치에 존재 가능) | 낮음 (데이터가 디스크 곳곳에 흩어짐/Fragmentation) | 높음 (독립적 데이터) |
| **스냅샷 생성 속도** | 매우 빠름 (메타데이터만 복사) | 매우 빠름 (메타데이터만 복사) | 매우 느림 (전체 데이터 Read/Write 소요) |
| **저장 공간 효율** | 높음 (변경된 블록만 차지) | 매우 높음 (기존 블록을 절대 변경하지 않음) | 낮음 (원본과 동일한 공간 즉시 소요) |
| **대표 기술 (Tech)** | **ZFS**, NetApp ONTAP (WAFL), LVM Snaps | **Log-Structured File System (LFS)**, Ceph RBD (Fast Clone) | VM Template, Legacy Disk Copy |

#### 2. 과목 융합 관점 분석 (OS & DB & Cloud)

*   **[운영체제 (OS) & 파일 시스템]**: **VFS (Virtual File System)** 커널 레벨에서 스냅샷 시스템 콜(System Call)이 처리됩니다. 특히 **Atomicity(원자성)**을 보장하기 위해 일관된 시점의 스냅샷을 위해 OS의 `Flush` 명령(`sync`) 또는 `Freeze` 기능이 사용되며, 이는 메인 메모리의 페이지 캐치(Buffer Cache)와 스토리지 간의 데이터 불일치를 방지하는 핵심 메커니즘입니다.
*   **[데이터베이스 (DB) & 트랜잭션]**: DB의 **ACID** 특성 중 Atomicity와 Durability 보장을 위해 스냅샷이 활�용됩니다. Oracle RMAN 등에서의 "Hot Backup" 모드는 OS 레벨의 스냅샷 기능을 기반으로, 데이터 파일의 일관성을 보장하는 체크포인트(Checkpoint)와 연동하여 Crash Recovery(CR) 시간을 단축합니다.

```text
[ Data Consistency Layers ]

┌──────────────────────────────────────────────────────┐
│ Application Layer (DB: Oracle, MySQL)                │
│  └─> Transaction Log (Redo Log) Management           │
├──────────────────────────────────────────────────────┤
│ File System Layer (ZFS, NTFS, EXT4)                  │
│  └─> Snapshot Freeze (Flush Buffers) ──────┐        │
├──────────────────────────────────────────────┼───────┤
│ Volume Manager / Storage Array (LVM, SAN)    │       │
│  └─> Point-in-Time Copy Metadata Lock <──────┘       │
└──────────────────────────────────────────────────────┘
         ▲                                    │
         │ Consistency Guarantee              │
         └────────────────────────────────────┘
```

**📢 섹션 요약 비유**
> **CoW 방식은 '편집증적인 화가'**가 붓을 대는 방식입니다. 그림을 조금만 수정해도 원본을 보관창고에 넣어두고 새 캔버스에 다시 그리느라 시간이 오래 걸리지만(쓰기 지연), 원본이 완벽하게 보존됩니다. 반면 **RoW 방식은 '효율적인 필름 카메라'**와 같습니다. 새로운 사진(데이터)은 빈 공간에 계속 찍기만 하므로 촬영(쓰기)이 매우 빠르지만, 나중에 영화를 보려고 필름을 뒤질 때(읽기) 여기저기 흩어져 있어 오래 걸릴 수 있습니다(Fragmentation).

---

## ### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 과정

1.  **시나리오 A: 랜섬웨어 감염 대응 (Ransomware Recovery)**
    *   **