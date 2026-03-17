+++
title = "219. 2단계 락킹(2PL)의 한계 - 데드락과 연쇄 복귀"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 219
+++

# 219. 2단계 락킹(2PL)의 한계 - 데드락과 연쇄 복귀
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2단계 락킹(2PL, Two-Phase Locking)은 직렬 가능성(Serializability)을 보장하는 가장 대표적인 동시성 제어 프로토콜이지만, **교착 상태(Deadlock) 발생 가능성**과 **연쇄 복귀(Cascading Rollback)**라는 구조적 한계를 내재하고 있다.
> 2. **가치**: 이러한 한계를 분석하는 것은 단순한 이론을 넘어, 대규모 트랜잭션 환경에서 DBMS(Database Management System)의 처리량(Throughput)과 안정성(Availability) 사이의 트레이드오프를 설계하는 핵심적인 의사결정 근거가 된다.
> 3. **융합**: OS(Operating System)의 자원 할급 교착 상태 이론과 응용 프로그램의 재시도(Retry) 로직이 연결되는 지점이며, 분산 시스템에서의 고립성 수준(Isolation Level)을 결정하는 기반이 된다.
+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**2PL (Two-Phase Locking)**은 트랜잭션이 데이터에 접근하기 전에 반드시 락(Lock)을 획득하고, 해제한 뒤에는 다시 획득할 수 없는 **'성장 단계(Growing Phase)'**와 **'축소 단계(Shrinking Phase)'**로 트랜잭션의 생명주기를 분리하는 프로토콜이다. 이론적으로는 직렬 가능성(Serializability)을 완벽하게 보장하지만, 실무 환경에서는 **'자원 점유와 대기(Wait-for)'**라는 비용 문제로 인해 심각한 부작용이 발생한다.

#### 2. 등장 배경과 한계의 시발점
초기 데이터베이스 시스템은 데이터 무결성(Integrity)을 최우선으로 여겨 강력한 락킹을 사용했다. 그러나 트랜잭션 수가 증가하고, 트랜잭션 간의 데이터 의존성(Dependency)이 복잡해지면서 다음과 같은 문제가 대두되었다.
1.  **순환 의존 (Cycle)**: 서로가 가진 리소스를 기다리는 무한 루프(Deadlock)
2.  **더티 읽기 전파 (Propagation)**: 롤백된 데이터를 참고하여 연쇄적으로 취소되어야 하는 상황(Cascading Rollback)

#### 3. 시각적 개요
```text
      [ 트랜잭션 생명주기와 한계점 ]
      
  시간의 흐름 ─────────────────────────────────────────▶
  
  ① 성장 단계 (Growing)     ② 축소 단계 (Shrinking)
  (Lock 만 획득 가능)         (Lock만 해제 가능)
  ┌────────────────┐        ┌────────────────┐
  │ 🔒 Lock(A)     │        │ 🔓 Unlock(A)   │
  │ 🔒 Lock(B)     │  ----> │ 🔓 Unlock(B)   │
  └────────────────┘        └────────────────┘
          │                         │
          ▼                         ▼
   [독점 점유 구간]             [의존성 발생 구간]
          │                         │
          ▼                         ▼
  ⚠️ 타 트랜잭션 대기 유발    ⚠️ 롤백 시 데이터 정합성 위험
          │                         │
          └───────────┬─────────────┘
                      ▼
          [⛔ 데드락 & 연쇄 복귀 발생 영역]
```

#### 4. 💡 비유
여행객(트랜잭션)이 안전을 위해 화장실과 열쇠를 모두 휴대하고 다니는 것과 같다. 내가 열쇠를 쥐고 있는 동안 아무도 들어오지 못하니 안전하지만, 내가 열쇠를 놓지 않은 채 다른 열쇠를 기다느라 문 앞에서 서로 마주 보고 서 있으면(Deadlock), 화장실은 영원히 막힌다.

#### 📢 섹션 요약 비유
2PL의 한계는 마치 **'융통성 없는 톨게이트 바리케이드'**와 같습니다. 차량(트랜잭션)이 통과할 때까지 바리케이드(락)를 내려놓아 안전을 보장하지만, 운이 나쁘게 서로 다른 차선의 바리케이드를 서로 기다리면 교통 체증(데드락)이 발생하고, 앞차가 통행료를 못 내고 되돌아가면 뒤에 있던 모든 차량도 강제로 되돌아가야(연쇄 복귀) 하는 상황이 발생합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 한계 상황의 구성 요소 분석
2PL의 한계를 구성하는 핵심 요소들은 다음과 같이 세분화할 수 있다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 프로토콜 | 비고 |
|:---|:---|:---|:---|:---|
| **Wait-for Graph** | 대기 그래프 | 트랜잭션 간의 자원 대기 방향성을 유향 그래프로 표현 | Cycle Detection | 사이클(Cycle) 존재 시 데드락 확정 |
| **X-Lock (Exclusive Lock)** | 쓰기 잠금 | 다른 트랜잭션의 읽기/쓰기를 모두 차단 (Update/Delete) | `Lock-X()` | 데드락의 주범 |
| **S-Lock (Shared Lock)** | 읽기 잠금 | 다른 트랜잭션의 읽기는 허용하나 쓰기는 차단 | `Lock-S()` | 연쇄 복귀의 촉매 |
| **Rollback Segment** | 복구 영역 | 변경 전 데이터 이미지를 보관 (Undo Log) | Undo | 연쇄 복귀 시 연쇄 접근 지점 |
| **Lock Manager** | 락 관리자 | 큐(Queue)를 통해 락 요청을 순서대로 관리 | Grant/Wait | 병목 지점 |

#### 2. 데드락(Deadlock) 시나리오 아키텍처
아래는 전형적인 **교착 상태(Deadlock)** 발생 구조를 도식화한 것이다. T1과 T2가 서로 상대방이 점유한 리소스(X-Lock)를 해제하기를 기다리며 영원히 대기하는 상태에 빠진다.

```text
      [ 데드락(Deadlock) 발생 구조 다이어그램 ]

      자원 A                  자원 B
   (Item: x)               (Item: y)
      │                      │
      │ X-Lock               │ X-Lock
      ▼                      ▼
  ┌─────────┐           ┌─────────┐
  │   T1    │           │   T2    │
  │(Trx Id) │           │(Trx Id) │
  └─────────┘           └─────────┘
      │                      ▲
      │ 1. Lock(A) 획득       │ 2. Lock(B) 획득
      │                      │
      │ 3. Lock(B) 요청 ────►│ 4. Lock(A) 요청
      │ (BLOCKED!)            │ (BLOCKED!)

      ◀──────────────────────▶
         Wait-for Graph (Cycle)
      
  결과: 두 트랜잭션 모두 영원히 진행 불가 (DBMS 주입 필요)
```

**[해설]**:
위 다이어그램에서 T1은 A를 확보한 상태에서 B를 요청하고, T2는 B를 확보한 상태에서 A를 요청한다. `Lock Manager`는 서로가 서로를 기다리는 순환(Cycle)을 감지한다. 이를 해결하기 위해 DBMS는 **Victim Selection(피해자 선택)** 알고리즘(주로 가장 작은 트랜잭션 또는 수행 시간이 짧은 트랜잭션)을 통해 하나를 강제로 롤백(Rollback)시켜 자원을 반환하게 한다.

#### 3. 연쇄 복귀(Cascading Rollback) 메커니즘
기본형 2PL(Basic 2PL)은 축소 단계(Shrinking Phase)에 진입하면 즉시 Unlock을 수행한다. 이때 발생하는 데이터 정합성 파괴 과정은 다음과 같다.

```text
      [ 연쇄 복귀(Cascading Rollback) 프로세스 ]

  시간 ──────────────────────────────────────────────▶
  
  T1 (쓰기):  ──▶ Lock(A) ──▶ Write(A=100) ──▶ 🔓 Unlock(A) ──▶ [Commit 실패!]
                                                          │
  T2 (읽기):  ──────────────────────────────▶ Read(A=100) ◀───┘
  (Dirty Read)                                         │
                                                       │
  T3 (쓰기):  ────────────────────────────────▶ Lock(A) ───▶ Write(A=200)
                                                        │
                                                        ▼
                                      [ T1 Rollback 발생 시 T2, T3도 모두 Rollback ]
                                              
  원인: T1이 Unlock한 뒤 Commit 전에 실패하여, T2가 읽은 A=100이 '쓰레기 데이터'가 됨.
```

**[해설]**:
1. **Dirty Read 유발**: T1이 데이터를 수정하고 락을 해제(Unlock)했으나 아직 커밋하지 않은 상태에서, T2가 해당 데이터를 읽는다.
2. **실패 전파**: T1이 오류로 인해 Rollback하면 원본 데이터로 복구된다. 하지만 T2는 이미 쓰레기 데이터(Dirty Data)를 읽었고, T2가 이를 바탕으로 연산을 수행했다면 결과 역시 신뢰할 수 없다.
3. **연쇄 작용**: T2뿐만 아니라 T2의 데이터를 참조한 T3까지 모두 Rollback되어야 한다. 이는 **실행 폭발(Work Explosion)**을 유발하여 시스템 자원을 심각하게 낭비한다.

#### 4. 핵심 알고리즘 (의사코드)
락 매니저가 데드락을 감지하는 **Wait-for Graph 탐색 알고리즘**은 다음과 같다.

```python
# Deadlock Detection Logic (Pseudo-code)
def detect_deadlock(wait_for_graph):
    """
    wait_for_graph: { Txn_Id: [Waiting_Txn_List] }
    """
    visited = set()
    rec_stack = set()

    def visit(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in wait_for_graph.get(node, []):
            if neighbor not in visited:
                if visit(neighbor):
                    return True
            elif neighbor in rec_stack:
                # Cycle Detected -> Deadlock!
                return True
        
        rec_stack.remove(node)
        return False

    # 모든 노드(트랜잭션)에 대해 사이클 탐색
    for txn in wait_for_graph:
        if txn not in visited:
            if visit(txn):
                return True # DEADLOCK OCCURRED
    return False
```

#### 📢 섹션 요약 비유
이러한 2PL의 동작 방식은 **'독으로 짓는 무너지기 쉬운 타워'**와 같습니다. 아래 블록(락)을 먼저 놓고 위를 쌓는 구조라, 만약 중간에 있는 블록(T1)이 빠져나가면 그 위에 있던 모든 블록(T2, T3)이 한꺼번에 무너져 내립니다(연쇄 복귀). 또한, 두 사람이 서로 상대방의 벽돌을 기다리며 멈춰 서 있으면 공사는 영원히 끝나지 않습니다(데드락).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 2PL 변형 기법 비교 (Strict vs Rigorous)
연쇄 복귀를 막기 위해 2PL을 실무에서 어떻게 변형하여 사용하는지 비교 분석한다.

| 구분 | Basic 2PL (기본형) | Strict 2PL (엄격형) | Rigorous 2PL (강건형) |
|:---|:---|:---|:---|
| **락 해제 시점** | 축소 단계 진입 시 즉시 해제 가능 | **Commit/Abort 시점까지 유지 (쓰기 락)** | **Commit/Abort 시점까지 유지 (모든 락)** |
| **연쇄 복귀** | 발생 가능 (위험) | **방지 (안전)** | **방지 (안전)** |
| **병행성** | 높음 (일찍 해제하므로) | 낮음 (락을 오래 잡고 있음) | 매우 낮음 |
| **실무 사용 여부** | 거의 사용되지 않음 | **대부분의 RDBMS 표준 (Default)** | 특수한 목적 제외 |
| **교착 상태** | 가능 | 가능 | 가능 |
| **성능 지표** | TPS 높음, but Retry 비용 높음 | TPS 낮음, but 일관성 보장 | TPS 가장 낮음 |

#### 2. 기술 스택 융합 분석 (2PL과 MVCC)
대부분의 현대적 DBMS(MySQL, PostgreSQL)는 2PL과 **MVCC(Multi-Version Concurrency Control)**를 결합하여 사용한다.

**A. MVCC와의 시너지**
- **문제 해결**: 2PL의 성능 저하(병행성 저하)를 MVCC가 **'Non-locking Read'**로 보완한다.
- **메커니즘**: 읽기 트랜잭션(Select)은 Undo Log를 통해 이전 버전의 데이터를 읽으므로, 쓰기 트랜잭션의 X-Lock과 충돌하지 않아 기다릴 필요가 없다.
- **한계**: 하지만 갱신(Update/Delete) 연산 간의 충돌은 여전히 2PL(또는 Next-Key Lock) 방식으로 관리되므로 데드락 위험은 완전히 사라지지 않는다.

**B. 네트워크와의 연관성**
- 분산 DB 환경(Distributed Database)에서는 **2PC (Two-Phase Commit)** 프로토콜과 2PL이 결합된다. 로컬 데드락이 전역 교착 상태(Global Deadlock)으로 확장될 수 있어 탐지 지연(Latency)이 급증한다.

#### 3. 정량적 성능 영향 분석

| 시나리오 | 추정 TPS (Transactions/Sec) | 평균 대기 시간 (Avg Latency) | 교착 상태 빈도 | 데이터 정합성 |
|:---|:---:|:---:|:---:|:---:|
| **No Locking** | 10,000 | 5ms | 0 | ❌ 매우 낮음 |
| **Basic 2PL** | 4,000 | 150ms | 보통 | ⚠