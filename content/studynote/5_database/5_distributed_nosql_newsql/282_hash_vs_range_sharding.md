+++
title = "282. 해시 샤딩 vs 레인지 샤딩 - 분산의 알고리즘"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 282
+++

# [해시 샤딩 vs 레인지 샤딩]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 해시 샤딩(Hash Sharding)은 해시 함수(Hash Function)를 통해 데이터를 무작위 분산시켜 **균등 분할(Even Distribution)**을 목표로 하며, 레인지 샤딩(Range Sharding)은 키의 순서(Ordering)를 유지하여 데이터를 **논리적 구간(Logical Partition)**으로 나누는 저장소 아키텍처이다.
> 2. **가치**: 해시 샤딩은 핫스팟(Hotspot) 방지와 쓰기 성능(Write Throughput)에 강점이 있어 OLTP(Online Transaction Processing) 환경에 적합하고, 레인지 샤딩은 범위 검색(Range Scan) 최적화로 OLAP(Online Analytical Processing) 및 리포팅 시스템의 성능을 극대화한다.
> 3. **융합**: 최신 분산 데이터베이스(Distributed DBMS)는 두 방식의 하이브리드 모델(Compound Key Strategy)을 지원하며, 이를 통해 균형 잡힌 데이터 분산과 빠른 집계 처리를 동시에 달성한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
샤딩(Sharding)은 대용량 데이터베이스를 수평 분할(Horizontal Partitioning)하여 관리하는 기술이다. 그 중심에는 데이터를 어느 노드에 배치할지 결정하는 **라우팅 알고리즘(Routing Algorithm)**이 존재한다. 해시 샤딩과 레인지 샤딩은 이 라우팅 로직을 양극단으로 정의하는 방식이다.

**💡 비유**
- **해시 샤딩**: 카드 게임에서 패를 섞어서 플레이어들에게 나눠주는 것과 같다. 카드의 숫자가 연속적이라도 누구에게 갈지 예측할 수 없다.
- **레인지 샤딩**: 도서관에서 책을 분류 번호(Dewey Decimal System)별로 서가에 꽂아두는 것과 같다. 100번대 서가에 가면 철학책이 있다는 것을 알 수 있다.

**등장 배경 및 발전**
단일 DBMS의 확장성 한계(Scale-up 비용 상승)를 극복하기 위해 Scale-out 아키텍처가 도입되었다. 초기에는 단순히 데이터를 순서대로 나누는 레인지 방식이 주류였으나, 특정 키값에 접근이 집중되는 **스큐(Skew)** 현상이 문제가 되었다. 이를 해결하기 위해 MongoDB 등 NoSQL이 등장하면서 데이터를 물리적으로 퍼뜨리는 해시 샤딩이 각광받았으나, 범위 검색 성능 저하 문제가 다시 대두되었다. 현재는 컴파운드 키 설계를 통해 두 장점을 취하려는 노력이 계속되고 있다.

**📢 섹션 요약 비유**
해시 샤딩은 **'로또 복권 추첨기'**처럼 번호 공(데이터)이 어느 통(노드)에 들어갈지 전혀 예측할 수 없이 무작위로 배정되어 개별 통의 부담을 줄이는 방식입니다. 반면, 레인지 샤딩은 **'학교 학년별 교실 배정'**처럼 1학년은 1반, 2학년은 2반에 몰아서 배치하는 방식이라, 특정 학년(키 범위)을 찾을 때는 매우 빠르지만 특정 반의 인원이 넘쳐날 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 비교**

| 요소 | 해시 샤딩 (Hash Sharding) | 레인지 샤딩 (Range Sharding) |
|:---|:---|:---|
| **샤드 키(Shard Key)** | 단일 필드 또는 복합 필드의 해시 값 | 순차적 범위가 있는 필드 (e.g., 날짜, ID) |
| **파티션 함수** `Partition Function` | `Modulus(Hash(Key), N)` | `Key >= Start AND Key < End` |
| **메타데이터** `Metadata` | Consistent Ring (VNode) | R-Tree 또는 Range Table |
| **데이터 분포** `Distribution` | 균등 분포 (Uniform) 편향 없음 | 편향 가능 (Skewed) 핫스팟 발생 가능 |
| **쿼리 라우팅** `Routing` | 단일 키 검색(Seek)에 최적화 | 범위 검색(Scan)에 최적화 |

**아키텍처 다이어그램**

아래는 두 방식의 데이터 배치 프로세스를 시각화한 것이다.

```text
+-----------------------------------------------------------------------+
|                        [ Shard Key Decision Logic ]                   |
+-----------------------------------------------------------------------+

  [A. Hash Sharding Path]                    [B. Range Sharding Path]

  1. Input Data (ID: 101)                    1. Input Data (Date: 2023-10-05)
       |                                           |
       v                                           v
  2. Hash Function (MD5/SHA)                 2. Compare Bounds
  Hash(101) -> 0x3F2A...                          |
       |                                           |
       v                                           v
  3. Modulo Operation                          3. Range Table Lookup
  0x3F2A % 4 = Slot 2                         Oct(10) is in Q4 Range
       |                                           |
       +--[Router]--[Router]--[Router]-------------+
             |           |           |
             v           v           v
+------------+    +------+------+    +------------+
|  Node 1    |    |  Node 2     |    |  Node 3    |
| [Slot 0]   |    | [Slot 1]    |    | [Slot 2]   |
|            |    |             |    | (Target)   |
| Random IDs |    | Random IDs  |    | Q4 Data    |
+------------+    +-------------+    | (Oct~Dec)  |
                                  +------------+
```

**해설 (Deep Dive)**
1.  **해시 샤딩 경로 (A)**: 클라이언트는 `ID: 101`을 요청한다. 라우터는 이 ID를 해시화하여 고유한 주소를 만든 뒤, 노드의 개수로 나눈 나머지(Modulo) 값을 구한다. 이 결과에 따라 데이터가 Node 2로 전달된다. 이 과정은 데이터의 **순서(Sequence)**를 완전히 무시하고 오직 **위치(Location)**만을 중시한다.
2.  **레인지 샤딩 경로 (B)**: 클라이언트는 날짜 데이터를 요청한다. 라우터는 이 값이 미리 정의된 범위 테이블(Range Table)의 어디에 속하는지 확인한다. 10월은 4분기(Q4) 범위에 속하므로 Node 3으로 전달된다. 이 과정은 데이터의 **의미(Semantics)**와 **순서**를 유지한다.

**핵심 알고리즘 및 코드 (Pseudo-code)**

*해시 파티셔닝 로직 (Python Style)*
```python
def get_hash_shard(key, total_nodes):
    """
    해시 함수를 사용하여 타겟 노드 ID를 반환합니다.
    실무에서는 MurmurHash와 같은 빠르고 충돌이 적은 해시를 사용합니다.
    """
    # 1. 키를 해싱 (정수 공간으로 매핑)
    hash_value = hash_function(key) 
    
    # 2. 노드 개수로 나머지 연산 (Modulo Operation)
    # 주의: 노드가 증설되면 모든 데이터의 재배치(Resharding)가 발생할 수 있음
    target_node = hash_value % total_nodes
    
    return target_node
```

*레인지 파티셔닝 로직 (Python Style)*
```python
def get_range_shard(key, range_map):
    """
    키가 속하는 범위를 검색하여 타겟 샤드를 반환합니다.
    Binary Search(이진 탐색)를 사용하여 O(log N)에 검색합니다.
    """
    # range_map 예시: [('2020-01-01', 'Shard_A'), ('2021-01-01', 'Shard_B')]
    
    for start_date, shard_id in range_map:
        if key >= start_date:
            current_shard = shard_id
        else:
            break
            
    return current_shard
```

**📢 섹션 요약 비유**
해시 샤딩의 내부 로직은 **'탁구 공 추첨기'**와 같습니다. 공 안의 번호가 무엇이든 상관없이 기계가 돌아가고 나온 구멍 위치만이 데이터의 집을 결정합니다. 레인지 샤딩은 **'우편물 분류기'**와 같아서, 우편 번호가 100번대는 서울 가방, 600번대는 부산 가방으로 규칙에 맞춰 떨어지게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교 분석표**

| 분석 지표 | 해시 샤딩 (Hash Sharding) | 레인지 샤딩 (Range Sharding) | 비고 |
|:---|:---|:---|:---|
| **쓰기 성능** `Write TPS` | ⭐⭐⭐⭐⭐ | ⭐⭐~⭐⭐⭐⭐ | 해시는 노드 분산이 균일하여 Lock Contention이 적음 |
| **읽기 성능** `Read Latency` | **Point Seek**: 빠름 <br> **Range Scan**: 매우 느림 | **Point Seek**: 보통 <br> **Range Scan**: 매우 빠름 | 레인지는 인접 데이터가 같은 디스크에 있어 Sequential I/O 유리 |
| **데이터 재균형** `Rebalancing` | 어려움 (Consistent Hashing 필요) | 상대적으로 쉬움 (Split만 수행) | |
| **스키마 유연성** `Schema Flex` | 키 변경 시 재배치 필요 | 범위 추가 용이 | |
| **주요 사용 사례** `Use Case` | 유저 프로필, 세션 데이터 | 로그 데이터, 시계열(Time-Series) 데이터 | |

**융합 관점 분석**

1.  **OS & 컴퓨터 구조 관점 (Memory & Disk I/O)**
    *   해시 샤딩은 메모리 상의 **해시 테이블(Hash Table)** 구조와 유사하며, O(1)의 접근 시간을 제공하지만 캐시 **지역성(Locality)**이 낮아 디스크 I/O가 Random 발생한다.
    *   레인지 샤딩은 **B-Tree 인덱스** 구조와 유사하며, Sequential Access가 가능하여 디스크의 **Seek Time**을 최소화하고 Read-Ahead 효과를 극대화한다.

2.  **네트워크 관점 (Traffic Pattern)**
    *   해시 샤딩은 특정 키를 조회할 때 요청이 특정 노드로 확정되므로 **Unicast** 패턴이 명확하다.
    *   레인지 샤딩은 대용량 데이터를 조회(Sort, Group By)할 때 네트워크 대역폭을 특정 노드가 독점할 수 있어 **Traffic Hotspot**이 발생할 수 있다.

**📢 섹션 요약 비유**
해시 샤딩은 **'무질서한 난수표'**처럼 통계적으로는 고르지만 연속성이 없어 이웃을 찾기 어렵습니다. 반면 레인지 샤딩은 **'연필 색깔별로 정리된 필통'**처럼 같은 색(범위)을 찾을 때는 매우 효율적이지만, 빨간색 연필이 너무 많으면 그 칸만 넘치는 불균형이 발생할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **SaaS 사용자 프로필 저장 (User Profile)**
    *   **상황**: 수천만 명의 회원을 가진 서비스. 특정 ID 조회가 90%, 회원가입(쓰기)이 10%.
    *   **결정**: **해시 샤딩 채택**.
    *   **이유**: 특정 ID 집중(예: ID가 1~100번인 사용자)으로 인한 특정 노드 과부하(핫스팟)를 방지해야 함. 레인지로 할 경우 신규 가입자가 ID 1대부터 채워지는 역사적 데이터 이슈로 첫 번째 노드가 폭발할 수 있음.

2.  **금융 거래 내역 조회 (Transaction Log)**
    *   **상황**: 하루 수천만 건 거래 발생. 주요 쿼리는 "3월 1일~3월 31일 거래 내역 조회".
    *   **결정**: **레인지 샤딩 채택**.
    *   **이유**: 날짜별로 파티셔닝하면 특정 기간 조회 시 해당 기간 노드만 스캔하면 됨. 해시로 할 경우 모든 노드를 뒤져서 Scatter-Gather를 해야 하므로 대기시간(Latency)이 너무 김.

3.  **실시간 게임 랭킹보드 (Real-time Ranking)**
    *   **상황**: 점수별 순위(Rank)가 중요하며, 업데이트와 조회가 빈번함.
    *   **결정**: **하이브리드 (Hash + Range)** 또는 **Sorted Set (In-Memory)**.
    *   **이유**: 단순 레인지는 상위권(100~1000점) 사용자가 몰려 핫스팟 발생. 단순 해시는 순위 계산이 불가능함. 따라서 점수대(100대, 200대)별로 레인지를 나누고, 내부에서 해시를 돌리거나 별도의 정렬 노드를 둠.

**도입 체크리스트 (Checklist)**

| 구분 | 항목 | 내용 |
|:---|:---|:---|
| **Technical** | **Key Selection** | 샤드 키(Cardinality)가 충분히 높은가? (중복 최소화) |
| | **Query Pattern** | Point Query가 80% 이상인가? (해시 추천) |
| | **Growth Rate** | 데이터 증가율이 예측 가능한가? (레인지 추천) |
| **Operational** | **Resharding Cost** | 노드 추가 시 전체 데이터를 이동해도 되는가? (해시 비용 높음) |
| **Security** | **Data Isolation** | 특정 범위의 고객 데이터를 물리적으로 격리해야 하는가? (레인지 유리) |

**안티패턴 (Anti-Patterns)**
- **Sequential Key를 Hashing하지 않기**: 자동 증가 컬럼(Auto Increment)을 해시 키로 사용하면, 데이터 분포는 고르지만 **순서 보장이 안 되어 Batch Insert 시 슬롯 간 이동(Jumping)이 잦아 성능이 저하될 수 있음** (MongoDB ObjectId와 같은 Random Key 생성 전략과 병행 필요).
- **Low-Cardinality K