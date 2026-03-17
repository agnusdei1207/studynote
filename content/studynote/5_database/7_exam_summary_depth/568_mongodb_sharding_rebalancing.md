+++
+++
title = "568. MongoDB 샤딩 리밸런싱 - 데이터의 공평한 이사"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 568
+++

# 568. MongoDB 샤딩 리밸런싱 - 데이터의 공평한 이사

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MongoDB 샤딩 리밸런싱은 분산 데이터베이스 환경에서 특정 샤드(Shard)로의 데이터 편중(Skew)을 해소하기 위해, **백그라운드 프로세스인 밸런서(Balancer)**가 청크(Chunk) 단위로 데이터를 재분배하는 자동화된 메커니즘입니다.
> 2. **가치**: 관리자 개입 없이 클러스터 전체의 **부하 균형(Load Balancing)**을 유지하여 쓰기 성능 저하를 방지하며, 서버 증설 시(Horizontal Scaling) 새로운 자원에 데이터를 즉시 분산시켜 투자 대비 성능을 최적화합니다.
> 3. **융합**: **CSRS (Config Server Replica Set)**의 메타데이터 관리와 분산 락(Distributed Lock) 프로토콜, 그리고 네트워크 대역폭 관리 기술이 융합되어, 데이터 이동 중에도 서비스 중단(Downtime) 없는 일관성을 보장합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
MongoDB 샤딩(Sharding) 환경에서 데이터는 **Chunk (청크)**라고 불리는 특정 범위의 데이터 덩어리로 나뉘어 각 샤드에 분산 저장됩니다. **리밸런싱(Rebalancing)**이란, 데이터의 추가/삭제 또는 샤드의 증설/제거로 인해 발생하는 샤드 간 데이터 분량 불균형을 해소하기 위해, 밸런서(Balancer)가 청크를 저장량이 많은 샤드(Donor)에서 적은 샤드(Recipient)로 이동시키는 동적 재분배 과정을 의미합니다.

**2. 💡 비유**
이는 거대한 창고에서 재고가 특정 구역(샤드)에만 쌓이는 것을 방지하기 위해, 포크레인(밸런서)이 짐을 나르는 상자(청크)들을 여유가 있는 다른 구역으로 실어 나르는 과정과 같습니다.

**3. 등장 배경 및 필요성**
① **기존 한계**: 단일 서버의 저장 용량 및 쓰기 처리량(TPS) 한계를 극복하기 위해 샤딩을 도입했으나, 데이터 편중이 발생하면 "병목 현상(Bottleneck)"으로 인해 성능이 저하됨.
② **혁신적 패러다임**: 수동으로 데이터를 이동하거나 애플리케이션 로직을 수정할 필요 없이, DBMS 내부의 자동화된 정책(Policy)에 의해 데이터가 스스로 최적의 위치를 찾아감.
③ **비즈니스 요구**: 급변하는 트래픽 패턴(이벤트, 시즌성)에 유연하게 대응하고, 무중단 서비스를 유지하면서도 시스템을 수평 확장(Scale-out)해야 하는 현대적 요구사항을 충족함.

> **📢 섹션 요약 비유**: 샤딩 리밸런싱은 **'태풍이 온 후 무너진 담벼락을 고르는 성벽 공사'**와 같습니다. 한쪽 성벽(샤드)에 충격(트래픽)이 몰려 무너질 위험이 있을 때, 건설 장비(밸런서)가 주변의 돌(청크)들을 가져와 성벽의 높이를 고르게 만들어 성(시스템)이 무너지지 않게 유지하는 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (Components)**

| 요소명 | 역할 (Role) | 내부 동작 (Internal Mechanism) | 주요 파라미터/프로토콜 |
|:---|:---|:---|:---|
| **Chunk (청크)** | 데이터 분산의 최소 단위 | Shard Key 값의 범위(Ex: 1~1000)를 가진 컬렉션의 일부 데이터. 기본 크기는 64MB (최대 1024MB). | `chunkSize` (config.settings) |
| **Balancer (밸런서)** | 리밸런싱 총괄 조율자 | Config Server의 메타데이터를 조회하여, 샤드 간 청크 수 차이가 임계치를 넘으면 마이그레이션을 명령함. | `_balancer` (Lock) |
| **Mongos (라우터)** | 요청 경로 지정 | 클라이언트 요청을 받아 Config Server에 청크 위치를 질의하고, Donor/Recipient 샤드로 라우팅함. | `moveChunk` Command |
| **Shard (샤드)** | 데이터 저장소 | Primary Shard에서 청크 복사(Clone) → 수신 → 소스 데이터 삭제(Drop) 과정 수행. | Internal Rollback |
| **Config Server (CSRS)** | 메타데이터 저장소 | 클러스터의 상태와 청크 분포도를 관리하며, 밸런서의 락(Lock)을 관리하는 권위자. | `config.chunks`, `config.locks` |

**2. 청크 분할 및 이동 원리 (Split & Move)**
데이터가 쓰이며 청크의 크기가 임계값을 초과하면 MongoDB는 이를 둘로 쪼개는 **Split (분할)** 작업을 수행합니다. 그 후 밸런서가 이 쪼개진 청크를 다른 샤드로 이동시키는 **Move (이동)** 작업을 수행합니다.

```text
   [Splitting Phase]                [Balancing Phase]
      (Before)                          (After)

   [Shard Key Range: Min~Max]      [Shard A]        [Shard B]
   ┌─────────────────────┐        ┌─────────┐      ┌─────────┐
   │   Chunk 1 (68MB)    │        │ Chunk 1 │      │ Chunk 2 │
   │   (Needs Split!)    │   ───▶ │ (1~500) │      │ (501~1k)│
   └─────────────────────┘        └─────────┘      └─────────┘
           │
           ▼ Split Point
   ┌───────────┬───────────┐
   │ Chunk 1   │ Chunk 2   │
   │ (Min~500) │ (500~Max) │
   └───────────┴───────────┘
```

**3. 청크 마이그레이션(Chunk Migration) 상세 프로세스**
밸런서에 의해 마이그레이션이 결정되면, 다음과 같은 단계를 거쳐 안전하게 데이터가 이동합니다. 이 과정에서 네트워크 및 디스크 I/O가 발생합니다.

```text
   [ Chunk Migration Flow ]

   1. [Balancer]                : "Shard A의 청크 수가 Shard B보다 2개 많군. MoveChunk 시작!"
       └─> [Config Server]      : Metadata Lock 획득 (다른 마이그레이션과 충돌 방지)

   2. [Mongos] ──(MoveChunk Cmd)──> [Donor: Shard A] : "Chunk_01을 Shard B로 보내라"
       │
       ├─> [Recipient: Shard B]   : (1) Clone Phase (Donor의 데이터를 복사 시작)
       │                          : 데이터 복사 중 Donor의 증분 업데이트(Incremental)를 수신하여 동기화
       │
       ├─> [Recipient: Shard B]   : (2) Catch-up Phase (Donor의 쓰기 연결 및 복사 완료 대기)
       │
       ├─> [Config Server]        : (3) Metadata Update (Chunk_01의 소유권을 Shard B로 변경)
       │                          : 이 시점부터 들어오는 쿼리는 Shard B로 라우팅됨
       │
       └─> [Donor: Shard A]       : (4) Cleanup Phase (데이터 삭제 및 디스크 공간 반환)

   ⚠️ Key Point:
   - (1)~(2) 단계에서 Donor에 쓰기가 발생하면,Recipient로도 전송되어 최신화.
   - (3) Metadata Update 순간 짧게 쓰기가 차단될 수 있음(보통 ms 단위).
```

**4. 핵심 알고리즘 및 가중치 계산**
밸런서는 샤드 간 불균형을 판단하기 위해 다음 로직을 사용합니다.
```python
# Pseudo-code for Balancer Logic
threshold = 0.025 # 2.5% difference triggers balancing
max_chunk_size = 64

for shard in cluster:
    chunk_count = get_chunk_count(shard)

avg_chunks = total_chunks / num_shards

if abs(shard_A.chunks - shard_B.chunks) > (avg_chunks * threshold):
    # Check if migration window is active
    if is_active_window():
        initiate_migration(shard_A, shard_B)
```

> **📢 섹션 요약 비유**: 청크 마이그레이션은 **'고속도로에서 톨게이트 차선 이동'**과 같습니다. 운전자(밸런서)가 A 차로(샤드)가 막힌 것을 보고 B 차로(샤드)로 차를 옮기라고 지시합니다. 차(청크)를 옮기는 동안에는 다른 차들이 방해하지 않도록 잠시 통제(Lock)하고, 옮기는 동안 계속해서 새로운 승객(데이터)이 탑승하면 그들도 B 차로로 함께 보내는 것(증분 동기화)과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Static vs Dynamic Hashing**

| 구분 | MongoDB Balancing (Range-based) | Consistent Hashing (Dynamo/Cassandra 스타일) |
|:---|:---|:---|
| **분배 방식** | Shard Key의 **범위(Range)** 기반 데이터 분할 | 해시 공간상의 **가상 노드(Virtual Node)** 배치 |
| **데이터 이동** | 불균형 시 **거대한 Chunk** 단위 이동 | 노드 탈퇴/참여 시 **일부 파티션**만 이동 |
| **Hotspot 민감도** | **취약함** (특정 Shard Key 트래픽 몰림) | **강함** (해시 분산으로 자동 분배) |
| **쿼리 성능** | **Range Scan에 유리** (인접 데이터가 같은 샤드에 존재) | Multi-Key 요청 시 네트워크 Hop 증가 |

**2. 과목 융합 관점**
*   **네트워크 (Network)**: 리밸런싱은 대량의 내부 트래픽을 발생시킵니다. 만약 샤드 간 대역폭이 낮다면, 사용자 요청 트래픽과 밸런싱 트래픽이 경합하여 **Latency가 급증**합니다. 따라서 `activeWindow` 설정을 통해 업무 시간(피크 타임)을 피해 밸런싱을 수행하는 네트워크 운영 정책이 필수적입니다.
*   **운영체제 (OS) / 저장장치**: 청크 복사는 결국 디스크에서 디스크로의 데이터 이동입니다. `Journaling` 과 `WAL (Write-Ahead Logging)` 활동이 리밸런싱 중 급증할 수 있으므로, I/O Scheduler의 성능 모니터링이 필요합니다.

**3. 정량적 성능 지표 및 의사결정 매트릭스**
리밸런싱이 필요한 상황을 판단하기 위한 지표입니다.

| 지표 (Metric) | 정상 상태 | 리밸런싱 필요 상태 (Action Required) |
|:---|:---|:---|
| **Chunk Skew (편차)** | 모든 샤드의 청크 수 ≈ 평균 | 특정 샤드가 평균 ±2~3개 이상 초과 |
| **Disk Usage** | 전체 용량의 80% 이하 공유 | 특정 샤드만 90% 이상 사용 (Full 경계) |
| **Opcounter (Write Latency)** | 10ms 이하 | 특정 샤드에서만 100ms 이상 급증 |

> **📢 섹션 요약 비유**: MongoDB의 리밸런싱은 **'급행열차의 객차 배치 조정'**과 같습니다. 승객(데이터)이 특정 객차(샤드)에만 몰리면 무게 중심이不稳해져 안전 운행이 어렵습니다. 반면, 일반적인 해시 방식은 승객이 역마다 무작위로 열차에 나누어 타는 것과 같아, 특정 칸에 몰리는 일은 없지만 가족끼리(관련 데이터) 떨어질 확률이 높습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 프로세스**

*   **시나리오 A: 급격한 트래픽 급증 (이벤트 시즌)**
    *   *상황*: 이벤트 참여 데이터가 최근 생성된 날짜 순으로 몰림.
    *   *판단*: Ranged Shard Key 특성상 최신 Chunk에 쓰기가 집중됨.
    *   *대응*: 일시적으로 밸런서를 중지(`sh.stopBalancer()`)하고, 이벤트 종료 후 재개하여 리밸런싱에 의한 쓰기 경합을 방지함.

*   **시나리오 B: 컬렉션 단일 Shard 유지 (Jumbo Chunk)**
    *   *상황*: 단일 청크가 1024MB(Chunk Size 상한)를 초과하여 더 이상 쪼개지지 않는 상태. 리밸런싱 불가.
    *   *판단*: Shard Key의 카디널리티(Cardinality)가 부족하거나 특정 값이 과도하게 많음.
    *   *대응*: `refineCollectionShardKey` 등을 통해 Shard Key를 수정하거나, 데이터를 재설계해야 함.

**2. 도입 체크리스트 (Checklist)**

*   **기술적 사항**
    *   [ ] NTP (Network Time Protocol) 동기화: 샤드 간 시간 차이는 Replication Lag를 유발함.
    *   [ ] 태그 인식(Tags) 샤딩: 특정 데이터를 지역별(Data Center)로 고정해야 할 경우, 밸런서가 이를 무시하고 이동시키지 않도록 Zone 설정 확인.
    *   [ ] CSRS (Config Server Replica Set) 안정성: 메타데이터가 깨지면 클러스터 전체가 마비됨.

*   **운영 및 보안적 사항**
    *   [ ] 밸런싱 윈도우(Active Window) 설정: 업무 시간(09:00~18:00) 외 시간대에만 리밸런싱이 작동하도록 스케줄링.
    *   [ ] 네트워크 비용 절감: 샤드가 물리적으로 다른 리전(AWS Region, GCP Zone)에 있을 경우, 데이터 이전에 따른 전송 비용(Egress Cost)을 고려해야 함.

**3. 안티패턴 (Anti-Pattern)**
*   **Low Cardinality Key