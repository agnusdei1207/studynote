+++
title = "동시성 제어 (Concurrency Control)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 동시성 제어 (Concurrency Control)

## 핵심 인사이트 (3줄 요약)
> **다수 트랜잭션이 동시 실행될 때 데이터 일관성을 보장**하는 기법. 로킹, MVCC, 타임스탬프 등의 방식 사용. 성능과 일관성의 트레이드오프가 핵심이다.

## 1. 개념
동시성 제어는 **여러 트랜잭션이 동시에 실행될 때 데이터베이스의 일관성을 유지**하기 위한 기법으로, 상호 간섭을 방지한다.

> 비유: "화장실 열쇠" - 한 사람이 쓸 때 다른 사람은 대기

## 2. 동시성 문제

```
1. Lost Update (갱신 손실)
   T1: x = x + 100
   T2: x = x + 200
   → T1의 갱신이 T2에 의해 덮어씌워짐

2. Dirty Read (오손 읽기)
   T1: x = 10 → x = 20 (미커밋)
   T2: READ x → 20
   T1: ROLLBACK
   → T2는 없는 값을 읽음

3. Non-repeatable Read (반복 불가능 읽기)
   T1: READ x → 10
   T2: UPDATE x = 20, COMMIT
   T1: READ x → 20
   → 같은 쿼리가 다른 결과

4. Phantom Read (유령 읽기)
   T1: SELECT WHERE age > 20 → 5행
   T2: INSERT age=25, COMMIT
   T1: SELECT WHERE age > 20 → 6행
```

## 3. 로킹 (Locking)

### 3.1 락 종류
```
공유 락 (Shared Lock, S-Lock):
- 읽기 전용
- 여러 트랜잭션이 동시 획득 가능
- S-Lock끼리 호환

베타 락 (Exclusive Lock, X-Lock):
- 읽기+쓰기
- 하나의 트랜잭션만 획득 가능
- S-Lock, X-Lock과 모두 비호환
```

### 3.2 락 호환성 매트릭스
```
         요청
          S    X
보유  S  O    X
      X  X    X

O: 호환 (대기 없음)
X: 비호환 (대기)
```

### 3.3 락킹 프로토콜
```
1단계 로킹 (1PL):
- 트랜잭션 내내 락 보유
- 문제: 동시성 낮음

2단계 로킹 (2PL):
- 확장 단계: 락 획득만 가능
- 축소 단계: 락 해제만 가능
- 직렬 가능성 보장

엄격 2단계 로킹 (Strict 2PL):
- 모든 X-Lock을 커밋/롤백까지 보유
- 연쇄 복귀 방지
```

### 3.4 2PL 단계
```
     락 개수
        ↑
        │    ──────┐
        │   /       │ 축소 단계
        │  /  확장  │ (unlock만)
        │ /   단계  │
        │/          │
        └───────────┴───→ 시간
           ↑
        Lock Point
```

## 4. 교착상태 (Deadlock)

### 4.1 발생 조건
```
1. 상호 배제: 자원은 한 번에 하나만 사용
2. 점유 대기: 자원을 가진 채 다른 자원 대기
3. 비선점: 강제로 자원 뺏기 불가
4. 순환 대기: 대기 사이클 형성
```

### 4.2 교착상태 예시
```
T1: lock(A) → lock(B) 대기
T2: lock(B) → lock(A) 대기

┌────┐          ┌────┐
│ T1 │──A대기──→│ T2 │
└────┘←──B대기──└────┘

서로가 서로의 자원을 기다림 → 무한 대기
```

### 4.3 해결 방법
```
예방 (Prevention):
- 모든 자원을 미리 획득
- 자원 순서 부여 (A → B 순서)

회피 (Avoidance):
- Wait-Die: 오래된 것이 대기
- Wound-Wait: 오래된 것이 선점

발견 (Detection):
- 대기 그래프 주기적 검사
- 교착상태 탐지 시 희생자 선정

복구 (Recovery):
- 희생자 선택하여 ROLLBACK
- Starvation 방지 필요
```

## 5. MVCC (다중 버전 동시성 제어)

```
개념: 데이터의 여러 버전을 유지하여 락 없이 읽기

구조:
┌─────────────────────────────────┐
│           현재 버전              │
│   id=1, name='홍길동', v=3      │
├─────────────────────────────────┤
│           이전 버전들            │
│   v=2: name='홍길동'            │
│   v=1: name='홍'                │
└─────────────────────────────────┘

읽기 작업:
- 특정 시점의 스냅샷 읽기
- 쓰기를 블로킹하지 않음

쓰기 작업:
- 새 버전 생성
- 읽기를 블로킹하지 않음

장점:
- 읽기와 쓰기가 서로 블로킹 안 함
- 높은 동시성

단점:
- 버전 관리 오버헤드
- 주기적 정리(GC) 필요
```

## 6. 타임스탬프 순서

```
각 트랜잭션에 고유한 타임스탬프 부여

규칙:
- W-TS(x): x의 마지막 쓰기 타임스탬프
- R-TS(x): x의 마지막 읽기 타임스탬프

읽기 규칙:
TS(T) < W-TS(x) → 거부 (이미 덮어씌워짐)
그 외 → 허용, R-TS(x) 갱신

쓰기 규칙:
TS(T) < R-TS(x) → 거부 (이미 읽힘)
TS(T) < W-TS(x) → 거부 (Thomas Write)
그 외 → 허용, W-TS(x) 갱신

장점: 락 없음, 교착상태 없음
단점: 기아 현상 가능
```

## 7. 낙관적 동시성 제어

```
가정: 충돌이 드물 것이다

3단계:
1. 읽기 단계: 데이터 읽기 (검증 없이)
2. 검증 단계: 충돌 여부 확인
3. 쓰기 단계: 검증 통과 시 쓰기

검증 방법:
- 뒤쪽 검증: 커밋 시점에만 검증
- 앞쪽 검증: 읽기 시작 시점에 검증

충돌 시:
- 트랜잭션 재시작

장점: 높은 동시성
단점: 충돌 많으면 성능 저하
```

## 8. 코드 예시

```python
from enum import Enum
from threading import Lock, Condition
from typing import Dict, Set, Optional
import time

class LockType(Enum):
    SHARED = "S"
    EXCLUSIVE = "X"

class LockManager:
    """락 관리자 시뮬레이션"""

    def __init__(self):
        self.locks: Dict[str, Dict] = {}  # resource -> lock info
        self.global_lock = Lock()

    def acquire(self, resource: str, lock_type: LockType,
                transaction_id: str, timeout: float = 5.0) -> bool:
        """락 획득"""
        start_time = time.time()

        while True:
            with self.global_lock:
                if resource not in self.locks:
                    self.locks[resource] = {
                        'type': lock_type,
                        'holders': {transaction_id}
                    }
                    return True

                lock_info = self.locks[resource]

                # 이미 보유 중
                if transaction_id in lock_info['holders']:
                    # S → X 승격
                    if lock_info['type'] == LockType.SHARED and \
                       lock_type == LockType.EXCLUSIVE:
                        if len(lock_info['holders']) == 1:
                            lock_info['type'] = LockType.EXCLUSIVE
                            return True
                    return True

                # 호환성 검사
                if self._is_compatible(lock_info, lock_type):
                    lock_info['holders'].add(transaction_id)
                    if lock_type == LockType.EXCLUSIVE:
                        lock_info['type'] = LockType.EXCLUSIVE
                    return True

            # 타임아웃 확인
            if time.time() - start_time > timeout:
                return False

            time.sleep(0.01)

    def release(self, resource: str, transaction_id: str):
        """락 해제"""
        with self.global_lock:
            if resource in self.locks:
                lock_info = self.locks[resource]
                lock_info['holders'].discard(transaction_id)
                if not lock_info['holders']:
                    del self.locks[resource]

    def _is_compatible(self, lock_info: Dict, request_type: LockType) -> bool:
        """호환성 검사"""
        if lock_info['type'] == LockType.SHARED and \
           request_type == LockType.SHARED:
            return True
        return False


class DeadlockDetector:
    """교착상태 탐지기"""

    def __init__(self):
        self.wait_for_graph: Dict[str, Set[str]] = {}

    def add_wait(self, waiter: str, holder: str):
        """대기 관계 추가"""
        if waiter not in self.wait_for_graph:
            self.wait_for_graph[waiter] = set()
        self.wait_for_graph[waiter].add(holder)

    def remove_wait(self, waiter: str):
        """대기 관계 제거"""
        if waiter in self.wait_for_graph:
            del self.wait_for_graph[waiter]

    def detect_deadlock(self) -> Optional[str]:
        """교착상태 탐지 (사이클 검사)"""
        visited = set()
        rec_stack = set()

        def dfs(node: str) -> Optional[str]:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.wait_for_graph.get(node, []):
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result
                elif neighbor in rec_stack:
                    return neighbor  # 사이클 발견

            rec_stack.remove(node)
            return None

        for node in self.wait_for_graph:
            if node not in visited:
                victim = dfs(node)
                if victim:
                    return victim

        return None


class MVCCManager:
    """MVCC 시뮬레이션"""

    def __init__(self):
        self.data: Dict[str, list] = {}  # key -> [(value, tx_id, deleted)]
        self.tx_counter = 0

    def begin_transaction(self) -> int:
        self.tx_counter += 1
        return self.tx_counter

    def read(self, key: str, tx_id: int) -> Optional[str]:
        """읽기 - 해당 tx_id 이전의 최신 버전"""
        if key not in self.data:
            return None

        for value, version_tx, deleted in reversed(self.data[key]):
            if version_tx <= tx_id and not deleted:
                return value

        return None

    def write(self, key: str, value: str, tx_id: int):
        """쓰기 - 새 버전 추가"""
        if key not in self.data:
            self.data[key] = []
        self.data[key].append((value, tx_id, False))

    def delete(self, key: str, tx_id: int):
        """삭제 - 삭제 마커 추가"""
        if key in self.data:
            self.data[key].append((None, tx_id, True))


# 사용 예시
print("=== 락 매니저 테스트 ===")
lm = LockManager()

# 공유 락 테스트
print("T1이 리소스A에 S락 획득:", lm.acquire("A", LockType.SHARED, "T1"))
print("T2가 리소스A에 S락 획득:", lm.acquire("A", LockType.SHARED, "T2"))
print("T3이 리소스A에 X락 획득 (실패 예상):",
      lm.acquire("A", LockType.EXCLUSIVE, "T3", timeout=0.1))

lm.release("A", "T1")
lm.release("A", "T2")
print("T3이 리소스A에 X락 획득 (재시도):",
      lm.acquire("A", LockType.EXCLUSIVE, "T3", timeout=1.0))

print("\n=== MVCC 테스트 ===")
mvcc = MVCCManager()

tx1 = mvcc.begin_transaction()
mvcc.write("name", "홍길동", tx1)

tx2 = mvcc.begin_transaction()
print(f"TX2 읽기: {mvcc.read('name', tx2)}")  # 홍길동

mvcc.write("name", "김철수", tx2)

tx3 = mvcc.begin_transaction()
print(f"TX3 읽기: {mvcc.read('name', tx3)}")  # 김철수
print(f"TX1 읽기: {mvcc.read('name', tx1)}")  # 홍길동 (자신보다 이전 버전)
