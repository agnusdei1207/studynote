+++
title = "593. 존 스토리지 (Zoned Storage)"
date = "2026-03-14"
weight = 593
+++

# # 593. 존 스토리지 (Zoned Storage)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 호스트(Host)가 스토리지의 물리적 쓰기 특성(순차 기록)을 직접 제어하게 하여, 내부의 복잡한 변환 계층(FTL)을 삭제하고 효율을 극대화하는 **인터페이스 패러다임**.
> 2. **가치**: **WAF (Write Amplification Factor)**를 1.0에 근접시켜 미디어 수명을 2~4배 연장하고, 내부 **GC (Garbage Collection)** 부하를 제거하여 **Tail Latency**를 최소화함.
> 3. **융합**: NVMe **ZNS (Zoned Namespace)** SSD와 Host-Managed **SMR (Shingled Magnetic Recording)** HDD를 아우르며, Ceph/RocksDB 등 **Key-Value Store**와 결합하여 클라우드 비용 절감을 실현함.

---

### Ⅰ. 개요 (Context & Background)

존 스토리지(Zoned Storage)는 스토리지 매체의 물리적 한계(덮어쓰기 불가능)를 인터페이스 관점에서 해결하기 위해 제안된 차세대 아키텍처입니다. 기존의 블록(Block) 기반 스토리지(Linux Block Layer)는 호스트에게 "논리적 블록 주소(LBA)에 무작위(Random) 쓰기가 가능하다"는 환상을 제공했습니다. 이를 위해 스토리지 내부의 **FTL (Flash Translation Layer)**은 엄청난 오버헤드를 감수하며 랜덤 쓰기를 순차 쓰기로 변환했습니다.

그러나 **QLC (Quad Level Cell)**/**PLC (Penta Level Cell)** NAND와 같은 고밀도 낸드 플래시나, 기록 트랙을 겹쳐 쓰는 **SMR (Shingled Magnetic Recording)** HDD가 등장하면서, 내부 연산(맵핑, GC)에 드는 비용과 지연이 너무 커졌습니다. 이에 물리적 배치 단위인 **존(Zone)**을 하나의 관리 단위로 노출하고, **"존 내부에서는 반드시 순차적으로만 쓰고(Sequential Write), 덮어쓰기 위해서는 존 전체를 리셋(Reset)해야 한다"**는 규칙을 호스트에게 강제합니다. 이는 스토리지 장치를 수동적인 '저장소'에서 능동적인 '협력자'로 탈바꿈시킵니다.

💡 **비유**
책상 정리를 생각해 봅시다. 기존 방식은 책상 위 아무 곳에나 서류를 올려두면(랜덤 쓰기), 뒤에서 누군가(FTL)가 자꾸 그 서류들을 정리 돌리느라(가비지 컬렉션) 책상을 못 쓰게 만듭니다. 존 스토리지는 책상에 칸막이(Zone)를 쭉 만들어두고, "왼쪽 칸부터 빈 곳 없이 채워야 하고, 수정하려면 그 칸을 통째로 비워야 한다"고 정해주는 것입니다. 대신 정리하는 사람은 사라지고 오로지 일만 집중하게 됩니다.

📢 **섹션 요약 비유**: 운영체제가 아무 곳에나 쓰기만 하면 내부적으로 복잡한 '청소부(GC)'가 움직여야 했던 것을, 구역을 나누어 "반드시 앞에서부터 차곡차곡 채워라"는 규칙을 줌으로써 청소부가 필요 없는 **엄격한 관리 주차장** 도입 방식입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

존 스토리지의 핵심은 **LBA (Logical Block Address)**의 무작위 할당을 포기하고 **ZNS (Zoned Namespace)** 또는 **Host-Aware Zoned Block Device** 모델을 채택하는 것입니다.

#### 1. 구성 요소 및 상태 기계 (State Machine)

존 스토리지의 각 Zone은 독립적인 상태 머신(State Machine)을 가집니다. 애플리케이션은 이 상태를 엄격히 준수해야 합니다.

| 요소 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **Zone (존)** | 연속된 LBA 그룹 (보통 256MB~수GB) | 독립적인 Write Pointer 관리 | 공책의 한 페이지 |
| **WP (Write Pointer)** | 현재 쓰기가 가능한 위치의 오프셋 | 존 내에서 순차적으로만 증가 (Reset 시 0으로 복귀) | 펜의 위치 |
| **Zone States** | 현재 존의 상태를 정의 (Empty, Open, Full, Read-only) | 상태 전이를 통해 데이터 무결성 보장 | 페이지의 사용 상태 |
| **ZAS (Zoned Storage Software)** | Linux Kernel의 ZBD 스택 | 앱의 비순차 요청을 차단하고 스케줄링 | 작성 감독관 |
| **Active/Idle Zones** | 동시에 열릴 수 있는 존의 개수 리소스 | 매체 내부 버퍼/워킹 셋 제한으로 성능 보장 | 한 번에 펼쳐볼 수 있는 페이지 수 |

#### 2. 존 상태 전이 다이어그램 (ASCII)

아래는 NVMe ZNS의 Zone State Transition입니다. 호스트는 이 상태 기계를 따라 명령을 내려야 합니다.

```text
+-----------------------------------------------------------+
|                  ZNS Zone State Machine                   |
+-----------------------------------------------------------+

      (Reset Write Pointer)
  +----------+                                       +----------+
  |          |                                       |          |
  |  Empty   | ----------------------------------->  |   Full   |
  |          | (Write until Zone Capacity)           |          |
  +----------+                                       +----------+
       ^  ^                                              |  ^
       |  | (Finish)                                      |  | (Reset)
(First) |  |                                              |  |
 Write  |  v                                              v  |
       | +-------------+      (Finish)      +---------------------------+
       | |             | ----------------> |            |              |
       +-+    Open     |                   |        Closed             |
         |             | <---------------- |            |              |
         +-------------+      (Close)       +---------------------------+
               |
               | (Explicit Close Command or Implicit)
               v
         +-------------+
         |    Read     |  (Explicitly Read Only)
         |    Only     |
         +-------------+
```
**(해설)**: 호스트는 비어 있는 `Empty` 상태의 존에 쓰기를 시작하면 `Open` 상태가 되며, 내부 **WP (Write Pointer)**가 자동 증가합니다. 용량이 차면 `Full` 상태가 되어 더 이상 쓰기가 불가능하며, 데이터를 수정하려면 `Finish` 후 `Reset` 명령을 통해 `Empty`로 되돌려야 합니다.

#### 3. 핵심 기술 메커니즘: Write Pointer & Append Only

존 스토리지는 일반적인 `Write` 명령(LBA 지정) 대신 `Zone Append` 명령을 사용할 때가 많습니다.
*   **Traditional Write**: `Write(LBA=X, Data)` → FTL이 물리 위치 찾음 (랜덤 접근 유발)
*   **Zoned Append**: `Append(Zone_ID=Z, Data)` → 장치가 현재 WP 위치에 기록하고 그 오프셋을 반환

이로 인해 호스트는 맵핑 테이블(LBA → PBA) 관리 주체가 됩니다.

```python
# Pseudo-Code: Zone Append Workflow
# Host-side mapping table maintenance example

zone = device.open_zone(zone_id=10)
lba_map = {} # Host managed mapping table

# Sequential Write Logic
def write_data(key, data):
    # 1. Record the current Write Pointer (LBA offset) returned by device
    current_lba = zone.get_write_pointer()
    
    # 2. Issue Append Command (Host only provides Zone ID)
    zone.append(data) 
    
    # 3. Host updates its own Map: Key -> LBA
    lba_map[key] = current_lba
    
    # 4. No random overwrite allowed within the zone
```

이 구조는 **Open-Channel SSD**의 장점(Host Control)을 계승하되, 칩별 파편화(Partial Page Write) 등의 복잡성은 추상화하여 **NVMe TPM (ZNS)** 표준으로 정착시켰습니다.

📢 **섹션 요약 비유**: 기존 방식이 "비어있는 주차 구역을 찾아서 여기저기 주차(Row parking)하는 것"이라면, 존 스토리지는 **"들어온 순서대로 번호표를 뽑아 지정된 주차 라인에 끝까지 채워서 주차(Line parking)하는 것"**입니다. 중간에 빠져나갈 수 없고 반드시 구역 끝까지 채워야 하므로 주차 관리 비용이 0에 수렴합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Block vs Zoned

| 구분 (Criteria) | Traditional Block Device | Zoned Storage (ZNS/SMR) |
|:---|:---|:---|
| **인터페이스 모델** | **LBA 모델**: 임의의 LBA에 쓰기 가능 | **Zone 모델**: 순차적 쓰기 강제 (Sequential Write Mandatory) |
| **맵핑 테이블 주체** | 장치 내부 FTL (Device-side FTL) | 호스트/파일 시스템 (Host-side) |
| **쓰기 증폭 (WAF)** | 1.5 ~ 3.0 (랜덤 쓰기 시 10+ 초과) | **~1.0** (이론적 최소화) |
| **오버 프로비저닝 (OP)** | 7% ~ 28% (GC 여유 공간 확보 필수) | **~0%** (OP 없이도 최대 용량 사용 가능) |
| **지연 시간 (Latency)** | 예측 어려움 (GC 발생 시 Spike 발생) | **예측 가능(Deterministic)** (GC 없음) |
| **주요 매체** | MLC/TLC NAND, CMR HDD | QLC/PLC NAND, **SMR HDD** |

#### 2. NVMe ZNS vs SMR HDD ASCII

같은 존 스토리지라도 매체 특성에 따라 최적화 포인트가 다릅니다.

```text
+-----------------------------+       +-----------------------------+
|      NVMe ZNS (SSD)         |       |      Host-Managed SMR       |
|      (Flash Based)          |       |      (Magnetic Disk)        |
+-----------------------------+       +-----------------------------+
| [Zone 0] [Zone 1] [Zone 2] |       | [Zone 0] [Zone 1] [Zone 2] |
|  |Chip0| |Chip1| |Chip2|   |       |  |Band0| |Band1| |Band2|   |
+-----------------------------+       +-----------------------------+
| 1. Parallel Write           |       | 1. Seeks minimized (Head)   |
|    (존 단위 병렬 쓰기 가능)   |       |    (헤드 이동 최소화)         |
| 2. Granularity: Block       |       | 2. Granularity: Sector      |
| 3. Reset = Block Erase      |       | 3. Reset = Track Overwrite  |
+-----------------------------+       +-----------------------------+
```

**(해설)**: **ZNS SSD**는 여러 Zone에 대해 동시에 쓰기 요청을 보내어 내부 여러 NAND 칩을 병렬로 활용할 수 있습니다(Parallelism). 반면 **SMR HDD**는 존을 물리적 밴드(Band) 단위로 매핑하여 헤드의 이동(Seek)을 최소화하는 데 주력합니다.

#### 3. 타 과목 융합 (OS & Database)

*   **운영체제(OS)**: Linux **ZBD (Zoned Block Device)** 드라이버는 존 스토리지를 `/dev/sdX`로 인식시키며, `blk-zoned` 모듈을 통해 `report zones`, `reset zone` 등의 **ioctl** 명령을 제공합니다. 이는 기존 블록 레이어와 호환되면서도 존 속성을 노출하는 하이브리드 계층입니다.
*   **데이터베이스(DB)**: **RocksDB**와 같은 **LSM-tree (Log-Structured Merge-tree)** 기반 저장소는 본질적으로 순차 쓰기를 수행합니다. 존 스토리지와의 궁합이 가장 좋습니다. 데이터 컴팩션(Compaction) 작업을 존 단위로 수행하여 파일 시스템 오버헤드를 완전히 제거하고, **Zone Append** 명령을 통해 WAL(Write-Ahead Log) 성능을 극대화합니다.

📢 **섹션 요약 비유**: 일반 스토리지는 "교통체증이 심한 시내 골목길"과 같아서(랜덤 접근/잦은 정리) 언제 막힐지 모르지만, 존 스토리지는 데이터베이스가 **"고속도로(순차 쓰기)"를 달리는 버스**처럼 설계되어 있어, **진입로(존)**만 확보하면 쉴 새 없이 고속으로 주행이 가능한 구조입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스

하이퍼스케일 데이터센터 설계 시 다음과 같은 기준으로 채택 여부를 결정합니다.

*   **시나리오 A: 로그/이벤트 데이터 수집 (Log Ingestion)**
    *   **특징**: 기록 후 거의 수정 안 함 (WORM: Write Once Read Many).
    *   **판단**: **ZNS 채택 (적합)**. 순차 쓰기만 수행하므로 WAF 1.0 달성으로 QLC NAND 수명 문제 해결.
*   **시나리오 B: 범용 OLTP 데이터베이스**
    *   **특징**: 잦은 랜덤 갱신(In-place Update).
    *   **판단**: **기존 TLC SSD 채택 (보류)**. 랜덤 갱신을 위한 존 리셋 오버헤드가 크고 애플리케이션 수정 비용이 높음. 다만 LSM-tree 기반 DB라면 ZNS 검토.
*   **시나리오 C: 비디오 감시(CCTV) 백업**
    *   **특징**: 순차적 기록, 오래된 데이터 삭제.
    *   **판단**: **SMR HDD 채택 (적합)**. 순차 기록에 최적화되어 있으며 비용(Capacity/$) 우수.

#### 2. 도입 체크리스트 (Checklist)

| 구분 | 항목 | 검토 포인트 |
|:---|:---|:---|
| **HW Spec** | **Zone Size** | 애플리케이션의 쓰기 단위(Chunk size)와 Zone Size가 배수 관계인가? (예: 256MB Zone) |
| **HW Spec** | **Active Zones** | 동시에 열 수 있는 존(Max Active Zones) 수가 앱의 병렬성(Pipeline depth)을 충족하는가? |
| **SW Stack** | **File System** | F2FS/Btrfs 지원 여부 또는 Raw Device 접근(No FS) 가능 여부