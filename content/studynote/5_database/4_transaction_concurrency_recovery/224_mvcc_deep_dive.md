+++
title = "224. 다중 버전 동시성 제어 (MVCC, Multi-Version Concurrency Control)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 224
+++

# 224. 다중 버전 동시성 제어 (MVCC, Multi-Version Concurrency Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MVCC (Multi-Version Concurrency Control)는 데이터베이스의 동시성 제어 기법으로, **데이터 갱신 시 원본을 즉시 덮어쓰지 않고 과거 버전을 유지함으로써**, 읽기 작업(Read)과 쓰기 작업(Write)이 상호 배제(Exclusive Lock) 없이 동시에 수행되게 하는 메커니즘입니다.
> 2. **가치**: "Non-blocking Read(비차단 읽기)"를 구현하여 락(Lock) 경합에 따른 병목 현상을 해소하고, **DBMS (Database Management System)**의 처리량(Throughput)을 획기적으로 증대시키며, 시스템 응답 시간(Latency)을 최소화합니다.
> 3. **융합**: 격리 수준(Isolation Level) 중 **RC (Read Committed)**와 **RR (Repeatable Read)**의 충돌을 해결하기 위해 **Undo Log** 및 **Redo Log**와 결합하고, OS의 가상 메모리 관리 기법(Copy-on-Write)과 상동한 철학을 공유합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
**MVCC (Multi-Version Concurrency Control)**는 트랜잭션이 데이터를 수정할 때 현재 데이터를 즉시 오버라이트(Overwrite)하는 대신, 새로운 버전의 데이터를 생성하여 저장소에 기록하는 방식입니다. 이때 과거의 데이터 버전은 **Undo Segment**나 **MVCC Chain**이라는 별도의 영역에 보관됩니다. 이로 인해 읽기 트랜잭션은 자신이 시작된 시점(Snapshot)에 맞는 적절한 과거 버전을 접근하게 되며, 쓰기 트랜잭션은 최신 버전에 락을 겁니다. 결과적으로 "읽기는 쓰기를 기다리지 않고, 쓰기는 읽기를 방해하지 않는" 상태를 실현합니다.

**2. 등장 배경: 락 기반(Locking) 방식의 한계**
전통적인 락 기반 동시성 제어(예: **2PL, Two-Phase Locking**)는 높은 데이터 정합성을 보장하지만, 동시 접속자가 늘어날 경우 다음과 같은 치명적인 병목이 발생합니다.
*   **Read Lock 공유 문제**: 조회(SELECT)조차도 데이터에 Shared Lock을 걸어야 하므로, 쓰기 트랜잭션은 읽기가 끝날 때까지 무한정 대기해야 합니다.
*   **데드락(Deadlock) 발생**: 다중 트랜잭션이 서로가 가진 락을 기다리며 교착 상태에 빠질 확률이 급격히 증가합니다.
*   **동시성 저하**: 대부분의 OLTP(Online Transaction Processing) 환경은 읽기 비중이 80% 이상이나, 락 때문에 읽기조차 직렬화(Serial Execution)되어 성능이 급락합니다.

이를 해결하기 위해 **Lock-free Read** 개념을 도입하고, 대신 공간(Space)을 사용하여 시간(Time) 차이를 해소하는 MVCC 패러다임이 등장했습니다.

**3. 데이터베이스별 구현 표기**
*   **Oracle**: Undo Segment, SCN (System Change Number)
*   **MySQL (InnoDB)**: Undo Log, Read View, TRX_ID
*   **PostgreSQL**: Tuple Header, xmin/xmax, VACUUM

> **📢 섹션 요약 비유**
> MVCC는 마치 **'무한 리와인딩이 가능한 스트리밍 서비스'**와 같습니다. 새로운 에피소드(데이터 갱신)가 방영되더라도, 시청자(읽기 트랜잭션)는 자신이 보던 시점(스냅샷)의 영상을 계속 볼 수 있습니다. 새 에피소드를 만드는 제작진(쓰기 트랜잭션)이 작업 중이라도, 시청자들은 멈춤 없이 자신의 타임라인대로 콘텐츠를 소비할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 관련 프로토콜/속성 | 비유 |
|:---|:---|:---|:---|:---|
| **Transaction ID (TX_ID)** | 트랜잭션 식별자 | 전역적으로 단조 증가하는 숫자로 트랜잭션 순서 부여 | Global Counter, Monotonic | 티켓 번호표 |
| **Undo Log (Undo Segment)** | 과거 데이터 보관 | UPDATE/DELETE 실행 전 원본 데이터를 백업하는 저장소 | Rollback Segment, Linked List | 창고(질문지 보관함) |
| **Read View (Snapshot)** | 가시성 판단 기준 | 트랜잭션 시작 시점의 활성 트랜잭션 목록을 스냅샷화 | m_ids, low_limit_id, up_limit_id | 시점의 사진 |
| **Data Page Tuple** | 실제 데이터 저장 | 데이터 행마다 `DB_TRX_ID`(생성자)와 `ROLL_PTR`(이전 버전 포인터) 저장 | Header Fields, Record Structure | 문서와 수정 버전 |
| **Purge Thread** | 버전 정리 | 더 이상 참조되지 않는 오래된 Undo 로그를 삭제하여 공간 확보 | Garbage Collection (GC), VACUUM | 청소부 |

**2. MVCC 데이터 구조 및 버전 체이닝 (ASCII Diagram)**

```text
[InnoDB MVCC Update Chain 구조]

┌──────────────────────────────────────────────────────────────┐
│                       Buffer Pool (Data Page)                │
├──────────────────────────────────────────────────────────────┤
│  Record [A]                                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Header:  TRX_ID: 100 (Creator)                       │    │
│  │          ROLL_PTR: ---> 0x7F0002 (Points to Undo)    │    │
│  │          ... DB_TRX_ID ...                           │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │ Body:   Name='Alibaba',  Age=19                      │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼ (ROLL_PTR Follows)
┌──────────────────────────────────────────────────────────────┐
│                       Undo Log Space                         │
├──────────────────────────────────────────────────────────────┤
│  Undo Log Entry 1 (0x7F0002)                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Type: UPDATE                                          │    │
│  │ TRX_ID: 50                                            │    │
│  │ ROLL_PTR: ---> 0x7F0001 (Previous Version)            │    │
│  │ Data:   Name='Ali',     Age=10  (Before Image)        │    │
│  └──────────────────────────────────────────────────────┘    │
│                            │                                  │
│                            ▼                                  │
│  Undo Log Entry 2 (0x7F0001)                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Type: INSERT                                          │    │
│  │ TRX_ID: 10                                            │    │
│  │ Data:   Name='Init',    Age=0                         │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```
*(해설: 데이터 페이지의 `ROLL_PTR` 포인터가 Undo 영역의 이전 버전을 가리키며 연결 리스트(Linked List)를 형성함)*

**3. 핵심 알고리즘: 가시성 판단 (Visibility Check)**
읽기 트랜잭션(T1)이 데이터(A)를 읽을 때, DBMS는 내부적으로 다음 로직을 수행합니다.

```python
# Pseudo-code for MVCC Visibility Check
def is_visible(txn_read_view, data_trx_id):
    # 1. 데이터를 만든 트랜잭션이 나보다 이전의 것인가?
    if data_trx_id < txn_read_view.up_limit_id:
        return True  # 당연히 보임 (내 스냅샷 이전에 확정된 데이터)
    
    # 2. 데이터를 만든 트랜잭션이 나보다 이후의 것인가?
    if data_trx_id >= txn_read_view.low_limit_id:
        return False # 당연히 안 보임 (내 시작 후에 생성된 데이터)

    # 3. 내 스냅샷 생성 당시 활성화 되어 있던(Active) 트랜잭션인가?
    if data_trx_id in txn_read_view.m_ids:
        # 나보다 늦게 커밋된 것이므로 안 보임 (Undo Log 타고 감)
        return False 
    
    return True # 내 스냅샷 찍고 나서 커밋된 건데, m_ids에 없으면 보임
```
*   **Deep Dive**: 만약 `is_visible`이 False라면, DBMS는 `ROLL_PTR`을 따라 Undo Log 영역으로 이동하여, `is_visible`이 True가 될 때까지(또는 루트에 도달할 때까지) 체이닝을 타고 거슬러 올라갑니다.

**4. 수식적 모델링 (오버헤드 분석)**
MVCC의 공간 오버헤드는 다음과 같이 정의할 수 있습니다.
$$ S_{total} = S_{data} + \sum_{i=1}^{n} (S_{undo\_i} \times T_{active\_period\_i}) $$
여기서 $S_{undo\_i}$는 트랜잭션 $i$가 생성하는 Undo 로그의 크기이며, $T_{active\_period\_i}$는 해당 로그가 유지되는 시간입니다. 긴 트랜잭션(Long-running Transaction)이 존재할 경우 $T$가 급증하여 저장소 공간을 압박하므로 **Vacuum/Purge** 주기가 핵심적입니다.

> **📢 섹션 요약 비유**
> MVCC의 데이터 버전 관리는 **'토론의 기록(Revision History)'**과 같습니다. 누군가 현재 문서를 집중적으로 수정하고 있더라도(쓰기), 다른 사람들은 편집 날짜가 어제인 안정적인 문서(읽기)를 읽을 수 있습니다. 수정 툴(트랜잭션 ID)은 "이 버전은 언제 만들어졌는가"를 스탬프처럼 찍어두고, 구독자(Read View)는 자신의 구독 시작 시점보다 이전에 발행된 기록만을 골라서 읽습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Locking vs. MVCC**

| 비교 항목 (Criteria) | Locking Based (2PL) | MVCC (Multi-Version) |
|:---|:---|:---|
| **Read 작업 동작** | Shared Lock (S-Lock) 획득 필요 <br>→ 다른 트랜잭션의 Write 차단 | Lock 획득 불필요 (Snapshot Read) <br>→ Undo Log 영역의 복사본 읽기 |
| **Write 작업 동작** | Exclusive Lock (X-Lock) 획득 <br>→ Read/Write 모두 차단 | 데이터 페이지에 X-Lock 획득 <br>→ 읽기 트랜잭션에 영향 없음 |
| **Concurrency Level** | Low (읽기와 쓰기가 상호 방해) | High (읽기와 쓰기가 병렬 처리) |
| **Deadlock Risk** | 높음 (Lock 대기 그래프 순환 발생) | 낮음 (읽기는 락을 안 잡으므로) |
| **Storage Overhead** | 낮음 (최신 데이터만 유지) | 높음 (Undo Log, 버전 관리 영역 필요) |
| **Isolation Support** | Serializability 구현 용이 | Snapshot Isolation (SI) 기반 <br> Serializability 구현 시 추가 비용 발생 (SSI 등) |

**2. 과목 융합 관점**
*   **운영체제 (OS)와의 연계**: MVCC는 OS의 **Copy-On-Write (COW)** 기법과 맥락을 같이합니다. 리눅스 커널의 `fork()` 시스템 콜이 메모리 페이지를 복사하여 프로세스 간 간섭을 막는 것처럼, MVCC는 데이터 페이지를 논리적으로 복사하여 트랜잭션 간 간섭을 막습니다.
*   **네트워크 프로토콜과의 연계**: 분산 DB 환경에서 MVCC는 **Global Transaction ID (GTID)**와 결합하여 여러 노드 간의 버전 동기화 문제를 해결해야 합니다. 네트워크 지연(Latency)으로 인해 과거 버전의 데이터가 필요할 경우, 로컬 Undo Log뿐만 아니라 원격 노드의 데이터 상태도 고려해야 하므로 복잡도가 급증합니다(Clock Skew 문제).

> **📢 섹션 요약 비유**
> MVCC 대 락(Locking)의 차이는 **'비행기 탑승 수속(게이트 변경)'**과 **'온라인 체크인'**의 차이와 같습니다. 락 방식은 탑승 수속 직원(CPU)이 한 명일 때, 앞사람의 처리가 끝날 때까지 줄 서서 기다려야 하는 방식입니다. 반면 MVCC는 키오스크(Snapshot)가 있어서, 내가 앞에서 서류를 검사하는 동안 뒷사람(쓰기)은 이미 다른 카운터에서 업무를 보고 있는 것과 같습니다. 대신 키오스크(저장소)를 유지하는 비용이 듭니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

*   **시나리오 A: 대규모 읽기 집중 웹 서비스 (뉴스/피드)**
    *   **상황**: 조회 쿼리가 초당 10,000건 발생하며, 갱신은 드물게 발생함.
    *   **판단**: **MVCC 기반 DB(MySQL InnoDB)**가 필수적입니다. Read Committed 수준에서도 대부분의 요청을 Disk I/O 없이 Memory(Buffer Pool) + Undo Log 영역에서 즉시 처리하여 Latency를 10ms 이내로 유지할 수 있습니다. 락 방식을 사용했다면 락 대기로 인한 타임아웃이 빈번할 것입니다.

*   **시나리오 B: 금융 거래 시스템 (계좌 이체)**
    *   **상황**: 데이터 갱신이 잦고, 잔액 조회 시 반드시 최신 정보를 보장해야 함(Phantom Read 방지).
    *   **판단**: MVCC를 사용하되, **Serializable** 격리 수준을 설정하거나 SELECT 시 `SELECT ... FOR UPDATE` (Locking Read)를 명시적으로 사용해야 합니다. 순수 MVCC만 사용할 경우 Non-repeatable Read가 발생하여 잔액 불일치가