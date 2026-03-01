+++
title = "분산 데이터베이스 (Distributed Database)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 분산 데이터베이스 (Distributed Database)

## 핵심 인사이트 (3줄 요약)
> **물리적으로 분산된 컴퓨터들에 데이터를 저장**하고 논리적으로는 하나처럼 관리. 위치 투명성, 중복 투명성 등을 제공. CAP 이론에 따른 일관성-가용성 트레이드오프가 핵심.

## 1. 개념
분산 데이터베이스는 **네트워크로 연결된 여러 사이트에 데이터가 분산 저장**되지만, 사용자에게는 하나의 통합된 데이터베이스처럼 보이는 시스템이다.

> 비유: "연쇄 빵집" - 여러 지점이 있지만 고객은 하나의 브랜드로 인식

## 2. 분산 데이터베이스 구조

```
┌──────────────────────────────────────────────────────┐
│                   사용자/응용 프로그램                │
└────────────────────────┬─────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────┐
│                분산 데이터베이스 관리 시스템          │
│              (Distributed DBMS)                       │
└───────┬───────────────┬───────────────┬──────────────┘
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   사이트 1     │ │   사이트 2     │ │   사이트 3     │
│   (서울)       │ │   (부산)       │ │   (대구)       │
│ ┌───────────┐ │ │ ┌───────────┐ │ │ ┌───────────┐ │
│ │   DBMS    │ │ │ │   DBMS    │ │ │ │   DBMS    │ │
│ └───────────┘ │ │ └───────────┘ │ │ └───────────┘ │
│ ┌───────────┐ │ │ ┌───────────┐ │ │ ┌───────────┐ │
│ │   데이터   │ │ │ │   데이터   │ │ │ │   데이터   │ │
│ └───────────┘ │ │ └───────────┘ │ │ └───────────┘ │
└───────────────┘ └───────────────┘ └───────────────┘
        ══════════════════════════════════
                    네트워크
```

## 3. 분산 데이터베이스 특성

### 3.1 투명성 (Transparency)
```
1. 위치 투명성 (Location Transparency)
   - 데이터가 어디 있는지 알 필요 없음
   - 사용자: SELECT * FROM 고객
   - 실제: 서울 DB에서 조회됨

2. 중복 투명성 (Replication Transparency)
   - 데이터가 복제되어 있는지 모름
   - 시스템이 자동으로 동기화

3. 분할 투명성 (Fragmentation Transparency)
   - 데이터가 분할되어 있는지 모름
   - 전체 데이터처럼 쿼리 가능

4. 병행 투명성 (Concurrency Transparency)
   - 분산 환경에서도 동시성 제어
   - 사용자는 단일 DB처럼 사용

5. 장애 투명성 (Failure Transparency)
   - 일부 사이트 장애 시에도 서비스 지속
   - 자동 장애 조치
```

### 3.2 분산 데이터베이스 목표
```
┌─────────────────────────────────────────┐
│          12개의 목표 (12 Objectives)     │
├─────────────────────────────────────────┤
│ 1. 지역 자율성                          │
│ 2. 중앙 사이트 없음                     │
│ 3. 연속 운영                            │
│ 4. 위치 독립성                          │
│ 5. 분할 독립성                          │
│ 6. 복제 독립성                          │
│ 7. 분산 쿼리 처리                       │
│ 8. 분산 트랜잭션 관리                   │
│ 9. 하드웨어 독립성                      │
│ 10. 운영체제 독립성                     │
│ 11. 네트워크 독립성                     │
│ 12. DBMS 독립성                         │
└─────────────────────────────────────────┘
```

## 4. 데이터 분산 방식

### 4.1 분할 (Fragmentation)
```
수평 분할 (Horizontal):
- 행 단위 분할
- 서울 고객 → 서울 DB
- 부산 고객 → 부산 DB

┌────────────┐     ┌────────────┐
│ 서울 고객   │     │ 부산 고객   │
│ 홍길동      │     │ 김철수      │
│ 이영희      │     │ 박민수      │
└────────────┘     └────────────┘

수직 분할 (Vertical):
- 컬럼 단위 분할
- 개인정보 → 보안 DB
│ 주문정보 → 주문 DB

┌────────────┐     ┌────────────┐
│ ID, 이름   │     │ ID, 주문    │
│ 홍길동      │     │ 주문1, 2    │
└────────────┘     └────────────┘
```

### 4.2 복제 (Replication)
```
완전 복제 (Full Replication):
- 모든 사이트에 전체 데이터
- 높은 가용성
- 많은 저장 공간
- 동기화 복잡

부분 복제 (Partial Replication):
- 일부 사이트에만 복제
- 중요 데이터만 복제
- 균형 잡힌 접근

마스터-슬레이브:
┌────────┐
│ Master │ ← 쓰기
└────┬───┘
     │ 복제
  ┌──┴──┬──────┐
  ▼     ▼      ▼
┌────┐┌────┐┌────┐
│ S1 ││ S2 ││ S3 │ ← 읽기
└────┘└────┘└────┘
```

## 5. CAP 이론

```
CAP Theorem: 세 가지를 모두 만족할 수 없다

      Consistency
      (일관성)
          ▲
         /│\
        / │ \
       /  │  \
      /   │   \
     /    │    \
    ●─────┼─────●
Availability  Partition
 (가용성)     Tolerance
             (분할 내성)

C: 모든 노드가 같은 시점에 같은 데이터 반환
A: 항상 응답 보장 (실패하지 않음)
P: 네트워크 분할이 발생해도 동작

트레이드오프:
- CP: 일관성 우선 (분산 락)
- AP: 가용성 우선 (결과적 일관성)
- CA: 분할 없는 환경에서만 가능 (단일 노드)
```

## 6. 분산 트랜잭션

### 6.1 2PC (Two-Phase Commit)
```
Phase 1: Prepare (준비)
┌──────────┐                    ┌──────────┐
│Coordinator│───"준비됐니?"───→│Participant│
└──────────┘                    └──────────┘
     ↑                               │
     └────────"준비됨"───────────────┘

Phase 2: Commit (커밋)
┌──────────┐                    ┌──────────┐
│Coordinator│───"커밋해!"────→│Participant│
└──────────┘                    └──────────┘
     ↑                               │
     └────────"완료"─────────────────┘

문제점:
- 블로킹: Coordinator 장애 시 대기
- 단일 실패 지점
```

### 6.2 3PC (Three-Phase Commit)
```
Phase 1: CanCommit?
Phase 2: PreCommit
Phase 3: DoCommit

추가 단계로 블로킹 문제 완화
하지만 여전히 복잡
```

### 6.3 SAGA 패턴
```
장기 실행 트랜잭션을 로컬 트랜잭션으로 분리

순차 실행:
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│주문  │───→│결제  │───→│배송  │───→│완료  │
└─────┘    └─────┘    └─────┘    └─────┘
   │          │
   │         실패!
   │          ↓
   │    ┌─────────┐
   └───→│결제취소  │ (보상 트랜잭션)
        └─────────┘

특징:
- 비블로킹
- 결과적 일관성
- 보상 로직 필요
```

## 7. 분산 쿼리 처리

```
쿼리 최적화 고려사항:

1. 데이터 전송 비용
   - 네트워크 비용 > 로컬 처리 비용

2. 조인 전략
   - 어떤 사이트에서 조인할 것인가?

예: 서울 고객 ⟕ 부산 주문
   - 서울→부산 전송 vs 부산→서울 전송
   - 작은 테이블을 이동하는 것이 유리

3. 세미 조인 (Semi-Join)
   - 필요한 컬럼만 전송
   - 통신량 감소

   서울: 고객ID만 전송
   부산: 해당 주문만 반환
   서울: 최종 조인
```

## 8. 일관성 모델

```
강한 일관성 (Strong Consistency):
- 모든 읽기가 최신 쓰기를 반환
- 동기식 복제
- 성능 저하

결과적 일관성 (Eventual Consistency):
- 시간이 지나면 일관성 달성
- 비동기식 복제
- 높은 성능

인과적 일관성 (Causal Consistency):
- 인과관계가 있는 작업은 순서 보장
- A→B 관계면 모든 노드에서 A 후 B

세션 일관성 (Session Consistency):
- 같은 세션에서는 일관성 보장
- "내가 쓴 것은 내가 바로 읽을 수 있음"
```

## 9. 코드 예시

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import threading
import time
import random

class NodeStatus(Enum):
    ACTIVE = "active"
    FAILED = "failed"

@dataclass
class DataItem:
    key: str
    value: str
    version: int
    node_id: str

class DistributedNode:
    """분산 데이터베이스 노드"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.data: Dict[str, DataItem] = {}
        self.status = NodeStatus.ACTIVE
        self.lock = threading.Lock()
        self.log: List[str] = []

    def read(self, key: str) -> Optional[DataItem]:
        """로컬 읽기"""
        with self.lock:
            return self.data.get(key)

    def write(self, key: str, value: str) -> DataItem:
        """로컬 쓰기"""
        with self.lock:
            version = 1
            if key in self.data:
                version = self.data[key].version + 1

            item = DataItem(key, value, version, self.node_id)
            self.data[key] = item
            self.log.append(f"WRITE {key}={value} v{version}")
            return item

class TwoPhaseCommit:
    """2PC 구현"""

    def __init__(self, coordinator: DistributedNode, participants: List[DistributedNode]):
        self.coordinator = coordinator
        self.participants = participants

    def execute(self, key: str, value: str) -> bool:
        """2PC 실행"""
        print(f"\n=== 2PC 시작: {key}={value} ===")

        # Phase 1: Prepare
        print("Phase 1: Prepare")
        prepared = []
        for p in self.participants:
            if p.status == NodeStatus.ACTIVE:
                # 실제로는 네트워크 통신
                prepared.append(p)
                print(f"  {p.node_id}: 준비됨")
            else:
                print(f"  {p.node_id}: 실패")

        if len(prepared) != len(self.participants):
            # Abort
            print("Phase 2: Abort")
            return False

        # Phase 2: Commit
        print("Phase 2: Commit")
        for p in prepared:
            p.write(key, value)
            print(f"  {p.node_id}: 커밋 완료")

        return True

class EventuallyConsistentDB:
    """결과적 일관성 DB"""

    def __init__(self, nodes: List[DistributedNode], replication_factor: int = 3):
        self.nodes = nodes
        self.replication_factor = replication_factor

    def write(self, key: str, value: str):
        """비동기 복제 쓰기"""
        # 즉시 로컬에 쓰기
        primary = self._get_primary_node(key)
        primary.write(key, value)
        print(f"쓰기 완료: {primary.node_id}")

        # 비동기로 복제
        threading.Thread(target=self._replicate, args=(key, value)).start()

    def read(self, key: str) -> Optional[DataItem]:
        """읽기 (결과적 일관성)"""
        node = self._get_primary_node(key)
        return node.read(key)

    def _get_primary_node(self, key: str) -> DistributedNode:
        """키에 대한 기본 노드 결정 (일관성 해싱)"""
        idx = hash(key) % len(self.nodes)
        return self.nodes[idx]

    def _replicate(self, key: str, value: str):
        """비동기 복제"""
        time.sleep(0.5)  # 네트워크 지연 시뮬레이션

        for node in self.nodes:
            if node.status == NodeStatus.ACTIVE:
                existing = node.read(key)
                if existing is None or existing.version < 1:
                    node.write(key, value)
                    print(f"복제 완료: {node.node_id}")

class QuorumConsistency:
    """정족수 일관성"""

    def __init__(self, nodes: List[DistributedNode], r: int, w: int):
        """
        r: 읽기 정족수
        w: 쓰기 정족수
        r + w > n (n: 전체 노드 수)
        """
        self.nodes = nodes
        self.r = r
        self.w = w
        self.n = len(nodes)

        if self.r + self.w <= self.n:
            raise ValueError("r + w must be > n")

    def write(self, key: str, value: str) -> bool:
        """쓰기 정족수"""
        success_count = 0
        version = int(time.time())

        for node in self.nodes:
            if node.status == NodeStatus.ACTIVE:
                node.write(key, value)
                success_count += 1
                if success_count >= self.w:
                    return True

        return False

    def read(self, key: str) -> Optional[DataItem]:
        """읽기 정족수"""
        responses = []

        for node in self.nodes:
            if node.status == NodeStatus.ACTIVE:
                item = node.read(key)
                if item:
                    responses.append(item)
                if len(responses) >= self.r:
                    break

        if not responses:
            return None

        # 최신 버전 반환
        return max(responses, key=lambda x: x.version)


# 사용 예시
print("=== 분산 데이터베이스 시뮬레이션 ===\n")

# 노드 생성
nodes = [
    DistributedNode("서울"),
    DistributedNode("부산"),
    DistributedNode("대구")
]

# 2PC 테스트
print("\n--- 2PC 테스트 ---")
twopc = TwoPhaseCommit(nodes[0], nodes)
twopc.execute("고객1", "홍길동")

# 결과적 일관성 테스트
print("\n--- 결과적 일관성 테스트 ---")
ec_db = EventuallyConsistentDB(nodes)
ec_db.write("상품1", "노트북")
time.sleep(1)  # 복제 대기

print("\n모든 노드에서 읽기:")
for node in nodes:
    item = node.read("상품1")
    print(f"  {node.node_id}: {item}")

# 정족수 일관성 테스트
print("\n--- 정족수 일관성 테스트 ---")
quorum = QuorumConsistency(nodes, r=2, w=2)
quorum.write("주문1", "주문데이터")
item = quorum.read("주문1")
print(f"정족수 읽기 결과: {item}")
```

## 10. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 확장성 | 수평 확장 가능 |
| 가용성 | 일부 장애 시에도 서비스 |
| 성능 | 지역별 데이터 접근 |
| 유연성 | 다양한 DBMS 사용 가능 |

### 단점
| 단점 | 설명 |
|-----|------|
| 복잡성 | 설계, 관리 어려움 |
| 네트워크 | 통신 비용, 지연 |
| 일관성 | 분산 환경 일관성 유지 어려움 |
| 보안 | 분산 환경 보안 관리 |

## 11. 실무에선? (기술사적 판단)
- **데이터 지역성**: 자주 접근하는 데이터를 가까운 곳에
- **CAP 선택**: 서비스 특성에 따라 CP vs AP 선택
- **복제 전략**: 읽기 많으면 복제, 쓰기 많으면 분할
- **일관성 수준**: 금융은 강한 일관성, SNS는 결과적 일관성
- **모니터링**: 분산 추적(Tracing) 필수

## 12. 관련 개념
- CAP 이론
- 일관성 모델
- 분산 트랜잭션
- 복제
- 샤딩

---

## 어린이를 위한 종합 설명

**분산 데이터베이스는 "연쇄 빵집"이에요!**

### 하나처럼 보이지만... 🏪
```
빵집이 여러 곳에 있어요:
- 서울점, 부산점, 대구점

하지만 고객은:
"어느 점포든 같은 빵을 살 수 있어!"
→ 하나의 빵집처럼 느껴져요
```

### 데이터는 어디에? 📍
```
분할:
- 서울 고객 → 서울점
- 부산 고객 → 부산점

복제:
- 인기 빵 → 모든 점포에
```

### CAP 트레이드오프 ⚖️
```
세 가지를 다 가질 순 없어요:

C (일관성): 모든 점포가 같은 정보
A (가용성): 항상 문을 열어요
P (분할 내성): 통신이 끊겨도 작동

→ 두 가지만 선택 가능!
```

### 2PC (Two-Phase Commit) 🤝
```
모든 점포가 함께 결정해요:

1단계: "준비됐어?"
   서울: 준비됨 ✓
   부산: 준비됨 ✓

2단계: "커밋해!"
   모든 점포가 동시에 반영
```

**비밀**: 카카오톡, 넷플릭스도 분산 DB를 써요! 🌍✨
