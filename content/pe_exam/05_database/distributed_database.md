+++
title = "분산 데이터베이스 (Distributed Database)"
date = 2025-03-01

[extra]
categories = "pe_exam-database"
+++

# 분산 데이터베이스 (Distributed Database)

## 핵심 인사이트 (3줄 요약)
> **물리적 분산 + 논리적 통합**: 네트워크로 연결된 여러 노드에 데이터를 분산 저장하면서 사용자에게는 하나의 DB처럼 보이게 하는 시스템**. CAP 이론에 따라 일관성(C), 가용성(A), 분할 내성(P) 중 2가지만 선택 가능. 2PC/3PC, SAGA 패턴으로 분산 트랜잭션 관리.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 분산 데이터베이스(Distributed Database, DDB)는 **네트워크로 연결된 여러 컴퓨터 노드에 데이터가 물리적으로 분산 저장되지만, 사용자에게는 논리적으로 하나의 통합된 데이터베이스처럼 보이는 시스템**이다. 위치 투명성, 중복 투명성, 분할 투명성을 제공한다.

> 💡 **비유**: 분산 DB는 **"전국 체인 빵집"** 같아요. 서울, 부산, 대구에 각각 지점이 있지만, 고객은 어디서든 "BB빵 하나 주세요"라고 주문하면 같은 메뉴를 받을 수 있죠. 각 지점은 재료를 나눠 갖지만(분산), 전체 메뉴는 같아요(논리적 통합).

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 단일 노드 한계**: 대용량 데이터 처리, 지리적 분산 서비스, SPOF(Single Point of Failure) 문제
2. **기술적 필요성 - 확장성과 가용성**: 수평 확장(Scale-out)으로 처리량 증대, 지역별 빠른 응답
3. **시장/산업 요구 - 글로벌 서비스**: 전 세계 사용자 대상 저지연 서비스, 재해 복구(DR)

**핵심 목적**: **확장성(Scalability)**, **가용성(Availability)**, **지역성(Locality)** 확보

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **분산 DBMS** | 전체 시스템 관리 | 글로벌 스키마, 분산 제어 | 본사 관리팀 |
| **로컬 DBMS** | 각 노드 DB 관리 | 지역 자율성 | 지점장 |
| **분산 딕셔너리** | 메타데이터 관리 | 위치, 분할, 복제 정보 | 전화번호부 |
| **네트워크** | 노드 간 통신 | 지연, 신뢰성 문제 | 도로망 |
| **코디네이터** | 분산 트랜잭션 관리 | 2PC/3PC 수행 | 총괄 매니저 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    분산 데이터베이스 아키텍처                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [사용자/응용 프로그램]                                            │
│            │                                                        │
│            ▼                                                        │
│   ┌───────────────────────────────────────┐                        │
│   │        분산 DBMS (Global View)         │                        │
│   │   ┌─────────────────────────────┐     │                        │
│   │   │   글로벌 스키마 / 메타데이터  │     │                        │
│   │   └─────────────────────────────┘     │                        │
│   │   ┌─────────────────────────────┐     │                        │
│   │   │   분산 쿼리 처리기           │     │                        │
│   │   └─────────────────────────────┘     │                        │
│   │   ┌─────────────────────────────┐     │                        │
│   │   │   분산 트랜잭션 관리자       │     │                        │
│   │   └─────────────────────────────┘     │                        │
│   └───────────────┬───────────────────────┘                        │
│                   │                                                 │
│     ┌─────────────┼─────────────┐                                  │
│     │             │             │                                  │
│     ▼             ▼             ▼                                  │
│   ┌─────┐      ┌─────┐      ┌─────┐                              │
│   │노드1│      │노드2│      │노드3│                              │
│     │             │             │                                  │
│   ┌─────┐      ┌─────┐      ┌─────┐                              │
│     │        네트워크         │                                  │
│   ═══════════════════════════════════                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    CAP 이론 시각화                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                 Consistency (일관성)                                │
│                     ▲                                               │
│                    /│\                                              │
│                   / │ \                                             │
│                  /  │  \                                            │
│                 /   │   \                                           │
│                /    │    \                                          │
│               /     │     \                                         │
│              ●──────┼──────●                                        │
│    Availability     │    Partition                                  │
│       (가용성)       │    Tolerance                                 │
│                      │    (분할 내성)                                │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  CP 시스템: 일관성 + 분할 내성 (가용성 희생)                  │  │
│   │  → MongoDB, HBase, Redis Cluster                             │  │
│   │  → 네트워크 분할 시 응답 안 함 (일관성 우선)                  │  │
│   ├─────────────────────────────────────────────────────────────┤  │
│   │  AP 시스템: 가용성 + 분할 내성 (일관성 희생)                  │  │
│   │  → Cassandra, DynamoDB, CouchDB                              │  │
│   │  → 네트워크 분할 시 최신이 아닐 수 있음 (가용성 우선)         │  │
│   ├─────────────────────────────────────────────────────────────┤  │
│   │  CA 시스템: 일관성 + 가용성 (분할 없는 환경)                  │  │
│   │  → 단일 노드 RDBMS, 분산 없는 환경                           │  │
│   │  → 네트워크 분할이 발생하지 않는 환경에서만 가능              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 쿼리 접수 → ② 쿼리 분해 → ③ 분산 실행 → ④ 결과 취합 → ⑤ 반환
```

- **1단계 - 쿼리 접수**: 글로벌 쿼리를 분산 DBMS가 수신
- **2단계 - 쿼리 분해**: 글로벌 스키마를 로컬 쿼리로 변환, 실행 위치 결정
- **3단계 - 분산 실행**: 각 노드에서 로컬 쿼리 병렬 실행
- **4단계 - 결과 취합**: 부분 결과를 모아 최종 결과 생성
- **5단계 - 반환**: 사용자에게 결과 반환

**핵심 알고리즘/공식** (해당 시 필수):

```
[2PC (Two-Phase Commit) 프로토콜]

Phase 1 - Prepare (준비):
1. Coordinator가 모든 Participant에게 PREPARE 전송
2. Participant가 로컬 트랜잭션 준비 (undo/redo 로그 기록)
3. Participant가 READY 또는 ABORT 응답

Phase 2 - Commit/Abort (결정):
- 모든 Participant가 READY면:
  Coordinator가 COMMIT 전송 → Participant 커밋
- 하나라도 ABORT면:
  Coordinator가 ABORT 전송 → Participant 롤백

문제점:
- 블로킹: Coordinator 장애 시 Participant가 대기 상태로 무한 대기
- 단일 실패 지점: Coordinator가 SPOF

[3PC (Three-Phase Commit) 프로토콜]
Phase 1: CanCommit? - 커밋 가능 여부 확인
Phase 2: PreCommit - 실제 커밋 준비 (논블로킹)
Phase 3: DoCommit - 최종 커밋

타임아웃으로 블로킹 해결하지만, 네트워크 분할 시 문제 발생

[SAGA 패턴]
장기 실행 분산 트랜잭션을 로컬 트랜잭션 시퀀스로 분해

주문 → 결제 → 배송 → 완료
  │       │
  │      실패!
  │       ↓
  │    결제취소 (보상 트랜잭션)
  │       ↓
  └── 주문취소 (보상 트랜잭션)

특징:
- 비블로킹
- 결과적 일관성 (Eventual Consistency)
- 각 단계별 보상 로직(Compensation) 필요

[데이터 분할 전략]
1. 수평 분할 (Horizontal Sharding):
   - 행 단위 분할: hash(key) % N
   - 예: 홀수 ID → 노드1, 짝수 ID → 노드2

2. 수직 분할 (Vertical Partitioning):
   - 컬럼 단위 분할
   - 예: 개인정보 → 보안 DB, 주문정보 → 주문 DB

3. 해시 샤딩 (Hash Sharding):
   key → hash(key) % N → 노드 결정
   장점: 균등 분산
   단점: 노드 추가 시 재분배 필요

4. 범위 샤딩 (Range Sharding):
   ID 1-1000 → 노드1, 1001-2000 → 노드2
   장점: 범위 쿼리 효율
   단점: 핫스팟 발생 가능

5. 일관성 해시 (Consistent Hashing):
   - 가상 노드로 균등 분산
   - 노드 추가/삭제 시 최소 이동
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Any
from enum import Enum
import hashlib
import random

class TransactionState(Enum):
    INITIAL = "initial"
    PREPARED = "prepared"
    COMMITTED = "committed"
    ABORTED = "aborted"

@dataclass
class Node:
    """분산 노드"""
    id: str
    data: Dict[str, Any] = field(default_factory=dict)
    prepared_txs: Set[str] = field(default_factory=set)
    logs: List[Tuple] = field(default_factory=list)

    def prepare(self, tx_id: str, operations: List[Tuple]) -> bool:
        """트랜잭션 준비 (로그 기록)"""
        # 로컬 로그에 undo/redo 정보 기록
        for op in operations:
            self.logs.append((tx_id, "PREPARE", op))
        self.prepared_txs.add(tx_id)
        return True

    def commit(self, tx_id: str, operations: List[Tuple]) -> None:
        """트랜잭션 커밋"""
        for op in operations:
            key, value = op
            self.data[key] = value
        self.logs.append((tx_id, "COMMIT", None))
        self.prepared_txs.discard(tx_id)

    def abort(self, tx_id: str) -> None:
        """트랜잭션 중단"""
        self.logs.append((tx_id, "ABORT", None))
        self.prepared_txs.discard(tx_id)

@dataclass
class Transaction:
    """분산 트랜잭션"""
    id: str
    operations: Dict[str, List[Tuple]]  # node_id -> operations
    state: TransactionState = TransactionState.INITIAL

class TwoPhaseCommitCoordinator:
    """2PC 코디네이터"""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.timeout = 5.0  # 초

    def add_node(self, node: Node) -> None:
        """노드 추가"""
        self.nodes[node.id] = node

    def begin_transaction(self, tx_id: str,
                         operations: Dict[str, List[Tuple]]) -> Transaction:
        """트랜잭션 시작"""
        tx = Transaction(id=tx_id, operations=operations)
        self.transactions[tx_id] = tx
        return tx

    def execute_2pc(self, tx_id: str) -> bool:
        """2PC 실행"""
        tx = self.transactions.get(tx_id)
        if not tx:
            return False

        # Phase 1: Prepare
        all_prepared = True
        for node_id, ops in tx.operations.items():
            node = self.nodes.get(node_id)
            if node:
                try:
                    if not node.prepare(tx_id, ops):
                        all_prepared = False
                        break
                except Exception as e:
                    all_prepared = False
                    break

        # Phase 2: Commit or Abort
        if all_prepared:
            for node_id, ops in tx.operations.items():
                node = self.nodes.get(node_id)
                if node:
                    node.commit(tx_id, ops)
            tx.state = TransactionState.COMMITTED
            return True
        else:
            for node_id in tx.operations:
                node = self.nodes.get(node_id)
                if node and tx_id in node.prepared_txs:
                    node.abort(tx_id)
            tx.state = TransactionState.ABORTED
            return False

class ConsistentHashing:
    """일관성 해시 구현"""

    def __init__(self, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}  # hash -> node_id
        self.sorted_keys: List[int] = []

    def _hash(self, key: str) -> int:
        """키 해싱"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node_id: str) -> None:
        """노드 추가 (가상 노드 포함)"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node_id}:{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node_id
        self.sorted_keys = sorted(self.ring.keys())

    def remove_node(self, node_id: str) -> None:
        """노드 제거"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node_id}:{i}"
            hash_val = self._hash(virtual_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key: str) -> Optional[str]:
        """키에 해당하는 노드 찾기"""
        if not self.ring:
            return None

        hash_val = self._hash(key)

        # 이진 탐색으로 시계 방향 첫 번째 노드 찾기
        for ring_key in self.sorted_keys:
            if hash_val <= ring_key:
                return self.ring[ring_key]

        # 끝에 도달하면 처음으로 래핑
        return self.ring[self.sorted_keys[0]]

class SagaOrchestrator:
    """SAGA 패턴 오케스트레이터"""

    @dataclass
    class SagaStep:
        """SAGA 단계"""
        name: str
        action: callable
        compensation: callable
        completed: bool = False

    def __init__(self):
        self.steps: List[SagaOrchestrator.SagaStep] = []
        self.completed_steps: List[SagaOrchestrator.SagaStep] = []

    def add_step(self, name: str, action: callable, compensation: callable) -> None:
        """단계 추가"""
        self.steps.append(self.SagaStep(name, action, compensation))

    def execute(self) -> Tuple[bool, str]:
        """SAGA 실행"""
        for step in self.steps:
            try:
                result = step.action()
                step.completed = True
                self.completed_steps.append(step)
            except Exception as e:
                # 보상 트랜잭션 실행 (역순)
                self._compensate()
                return False, f"Step '{step.name}' failed: {str(e)}"

        return True, "Saga completed successfully"

    def _compensate(self) -> None:
        """보상 트랜잭션 실행"""
        for step in reversed(self.completed_steps):
            try:
                step.compensation()
            except Exception as e:
                print(f"Compensation failed for {step.name}: {e}")

# 사용 예시
if __name__ == "__main__":
    print("=== 2PC Demo ===")
    coordinator = TwoPhaseCommitCoordinator()

    # 노드 추가
    coordinator.add_node(Node("node1"))
    coordinator.add_node(Node("node2"))
    coordinator.add_node(Node("node3"))

    # 분산 트랜잭션 생성
    tx = coordinator.begin_transaction("tx1", {
        "node1": [("key1", "value1")],
        "node2": [("key2", "value2")],
        "node3": [("key3", "value3")]
    })

    # 2PC 실행
    success = coordinator.execute_2pc("tx1")
    print(f"Transaction result: {'COMMITTED' if success else 'ABORTED'}")

    print("\n=== Consistent Hashing Demo ===")
    ch = ConsistentHashing(virtual_nodes=100)

    ch.add_node("node1")
    ch.add_node("node2")
    ch.add_node("node3")

    keys = ["user:1", "user:2", "user:3", "order:1", "order:2"]
    for key in keys:
        node = ch.get_node(key)
        print(f"{key} → {node}")

    print("\n=== SAGA Pattern Demo ===")
    saga = SagaOrchestrator()

    # 주문 처리 SAGA
    saga.add_step(
        "create_order",
        lambda: print("1. 주문 생성") or True,
        lambda: print("1-보상. 주문 취소")
    )
    saga.add_step(
        "process_payment",
        lambda: (_ for _ in ()).throw(Exception("결제 실패!")),  # 실패 시뮬레이션
        lambda: print("2-보상. 결제 취소")
    )
    saga.add_step(
        "ship_order",
        lambda: print("3. 배송 시작") or True,
        lambda: print("3-보상. 배송 취소")
    )

    success, message = saga.execute()
    print(f"\nResult: {message}")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **수평 확장**: 노드 추가로 처리량 증대 | **복잡성**: 설계, 운영, 디버깅 어려움 |
| **고가용성**: 일부 노드 장애 시에도 서비스 지속 | **네트워크 지연**: 노드 간 통신 오버헤드 |
| **지역성**: 지역별 데이터 배치로 응답 시간 단축 | **일관성 관리**: 분산 환경의 데이터 정합성 확보 어려움 |
| **유연성**: 이기종 DBMS 혼용 가능 | **트랜잭션 복잡**: 2PC 오버헤드, 분산 락 |

**CAP 기반 시스템 비교** (필수: 최소 2개 대안):
| 비교 항목 | CP (MongoDB) | AP (Cassandra) | CA (PostgreSQL) |
|---------|-------------|----------------|-----------------|
| **일관성** | ★ 강한 일관성 | 결과적 일관성 | ★ 강한 일관성 |
| **가용성** | 분할 시 응답 안 함 | ★ 항상 응답 | 단일 노드만 |
| **분할 내성** | ★ O | ★ O | X |
| **지연 시간** | 높음 (동기화) | 낮음 | 낮음 |
| **적합 환경** | 금융, 주문 | IoT, 소셜 | 단일 데이터센터 |

> **★ 선택 기준**:
> - **CP (강한 일관성)**: 금융, 주문, 재고 관리
> - **AP (고가용성)**: SNS, IoT 센서, 캐시
> - **CA (단일 노드)**: 소규모, 내부 시스템

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **글로벌 전자상거래** | 지역별 샤딩 + 결과적 일관성 | 지역 응답시간 50ms 이내, 가용성 99.99% |
| **금융 핀테크** | CP 시스템 + 동기식 복제 | 데이터 정합성 100%, RPO 0 |
| **IoT 데이터 수집** | AP 시스템 + 시계열 DB | 초당 100만 건 수집, 무중단 운영 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - Netflix**: Cassandra (AP)로 전 세계 스트리밍 데이터 관리, 99.99% 가용성 달성
- **사례 2 - Uber**: Schemaless (CP/AP 하이브리드)로 실시간 위치 추적, 초당 수백만 업데이트
- **사례 3 - 카카오**: Cassandra + Kafka로 메시지 저장, 일일 200억 건 메시지 처리

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - CAP 트레이드오프 명확화
   - 분할 전략 (해시 vs 범위)
   - 복제 팩터 (Replication Factor)
   - 일관성 수준 (Consistency Level)
2. **운영적**:
   - 노드 모니터링
   - 자동 장애 조치
   - 밸런싱 (Rebalancing)
   - 분산 추적 (Distributed Tracing)
3. **보안적**:
   - 노드 간 암호화
   - 접근 제어
   - 감사 로그
4. **경제적**:
   - 노드 수 vs 비용
   - 네트워크 비용
   - 운영 인력

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **CAP 오해**: "CA 시스템 선택" → 네트워크 분할은 항상 발생 가능
- ❌ **잘못된 샤딩 키**: 핫스팟 발생 → 특정 노드 과부하
- ❌ **2PC 과신**: 성능 병목 → SAGA로 대체 검토
- ❌ **복제 지연 무시**: 결과적 일관성의 stale read

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 분산 DB와 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  분산 DB 핵심 연관 개념 맵                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [CAP이론] ←──→ [분산DB] ←──→ [NewSQL]                        │
│       ↓            ↓              ↓                             │
│   [BASE]      [분산트랜잭션]  [NoSQL]                           │
│       ↓            ↓              ↓                             │
│   [일관성모델]  [2PC/3PC]    [샤딩]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **CAP 이론** | 이론적 기반 | 분산 시스템 트레이드오프 | `[CAP이론](../distributed_database.md)` |
| **NoSQL** | 구현 예 | 분산 DB의 대표적 구현 | `[NoSQL](./nosql/nosql_database.md)` |
| **동시성 제어** | 하위 개념 | 분산 환경의 동시성 | `[동시성제어](./concurrency_control.md)` |
| **트랜잭션** | 확장 개념 | 분산 트랜잭션 | `[트랜잭션](../transaction.md)` |
| **클라우드** | 인프라 | 분산 DB 실행 환경 | `[클라우드](../06_ict_convergence/cloud/_index.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **확장성** | 노드 추가로 선형 증가 | 처리량 선형 확장 |
| **가용성** | 부분 장애 시에도 서비스 | 99.99% 이상 Uptime |
| **지역성** | 지역별 데이터 배치 | 응답시간 50ms 이내 |
| **비용 효율** | 상용 하드웨어 활용 | TCO 40% 절감 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: NewSQL로 RDBMS + 분산 특성 결합, Serverless DB, Edge Computing과 결합
2. **시장 트렌드**: 멀티 클라우드 분산 DB, Global Database (AWS Aurora Global), AI 기반 자동 샤딩
3. **후속 기술**: 분산 SQL (CockroachDB, TiDB), 분산 벡터 DB (Milvus, Pinecone)

> **결론**: 분산 데이터베이스는 대용량, 고가용성, 지역성이 필요한 현대 서비스의 필수 요소다. CAP 이론을 이해하고 서비스 특성에 맞는 CP/AP 선택이 중요하며, 2PC의 한계를 극복하기 위한 SAGA 패턴 활용이 증가하고 있다.

> **※ 참고 표준**: CAP Theorem (Brewer, 2000), PACELC, Google Spanner Paper

---

## 어린이를 위한 종합 설명 (필수)

**분산 데이터베이스**은(는) 마치 **"전국 체인 빵집"** 같아요.

여러분이 사는 도시에 BB빵집이 있다고 해요. 서울, 부산, 대구, 광주... 전국에 100개의 지점이 있어요. 각 지점은 자신의 재료를 갖고 빵을 만들지만, **모든 지점의 메뉴는 똑같아요**. 어느 지점을 가든 "BB빵 주세요"라고 하면 같은 빵을 받을 수 있죠!

분산 데이터베이스도 이와 비슷해요:
- **분산**: 데이터가 여러 컴퓨터(노드)에 나눠서 저장돼요
- **통합**: 사용자는 하나의 데이터베이스처럼 사용할 수 있어요

**CAP 이론**이라는 중요한 규칙이 있어요:
- **일관성(C)**: 모든 지점의 메뉴가 항상 똑같아야 해요
- **가용성(A)**: 문이 열려 있으면 항상 주문을 받아야 해요
- **분할 내성(P)**: 일부 지점이 연락이 안 돼도 영업해야 해요

하지만 **세 가지를 다 가질 수는 없어요**! 두 가지만 선택해야 해요:
- **CP**: 메뉴가 확실해야 하니까, 연락이 안 되면 문을 닫아요
- **AP**: 항상 영업하니까, 메뉴가 조금 다를 수 있어요

이 규칙을 알면 어떤 시스템이 우리 서비스에 맞는지 선택할 수 있어요! 🏪🌐
