+++
title = "트랜잭션 (Transaction)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 트랜잭션 (Transaction)

## 핵심 인사이트 (3줄 요약)
> **데이터베이스의 논리적 작업 단위**. ACID(원자성, 일관성, 격리성, 지속성) 특성을 보장. COMMIT으로 확정하거나 ROLLBACK으로 취소한다.

## 1. 개념
트랜잭션은 **데이터베이스에서 하나의 논리적 기능을 수행하기 위한 작업의 단위**로, 전체가 성공하거나 전체가 실패해야 한다.

> 비유: "은행 이체" - A계좌 출금 + B계좌 입금이 하나의 단위

## 2. ACID 특성

### 2.1 원자성 (Atomicity)
```
All or Nothing - 전부 성공하거나 전부 실패

예: 계좌 이체
1. A계좌: 100만원 출금
2. B계좌: 100만원 입금

→ 둘 다 성공하거나, 둘 다 실패해야 함
→ 중간에 장애가 나면 ROLLBACK
```

### 2.2 일관성 (Consistency)
```
트랜잭션 전후의 데이터베이스 상태가 일관되어야 함

예:
- 트랜잭션 전: A잔액 + B잔액 = 200만원
- 트랜잭션 후: A잔액 + B잔액 = 200만원

제약조건(무결성)이 항상 만족되어야 함
```

### 2.3 격리성 (Isolation)
```
동시에 실행되는 트랜잭션이 서로 영향을 주지 않아야 함

문제:
- Dirty Read: 커밋 안 된 데이터 읽음
- Non-repeatable Read: 같은 데이터가 다르게 읽힘
- Phantom Read: 새로운 행이 나타남/사라짐

해결: 격리 수준 설정
```

### 2.4 지속성 (Durability)
```
커밋된 트랜잭션은 영구적으로 저장됨

장애가 발생해도 커밋된 데이터는 복구 가능
→ 로그, 체크포인트 활용
```

## 3. 트랜잭션 상태

```
           ┌─────────────┐
           │    Active   │ ← 시작
           │   (활동)    │
           └──────┬──────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Partial │ │Committed│ │ Failed  │
│Commit   │ │ (완료)  │ │ (실패)  │
└────┬────┘ └─────────┘ └────┬────┘
     │                       │
     └───────────┬───────────┘
                 ▼
          ┌───────────┐
          │ Rollback  │
          │  (철회)   │
          └───────────┘
```

## 4. 트랜잭션 제어

### 4.1 TCL (Transaction Control Language)
```sql
-- 트랜잭션 시작 (명시적)
BEGIN TRANSACTION;

-- 데이터 조작
UPDATE 계좌 SET 잔액 = 잔액 - 100000 WHERE 계좌번호 = 'A';
UPDATE 계좌 SET 잔액 = 잔액 + 100000 WHERE 계좌번호 = 'B';

-- 커밋 (확정)
COMMIT;

-- 또는 롤백 (취소)
ROLLBACK;
```

### 4.2 세이브포인트
```sql
BEGIN TRANSACTION;

INSERT INTO 주문 VALUES (1, '2024-01-01');

SAVEPOINT sp1;

INSERT INTO 주문상세 VALUES (1, 'P001', 2);

-- sp1까지 롤백
ROLLBACK TO sp1;

COMMIT;
```

## 5. 격리 수준 (Isolation Level)

```
┌─────────────────────────────────────────────────┐
│             Isolation Level                      │
├─────────────────────────────────────────────────┤
│ READ UNCOMMITTED  │ Dirty Read 가능             │
├─────────────────────────────────────────────────┤
│ READ COMMITTED    │ Dirty Read 방지             │
│                   │ Non-repeatable Read 가능     │
├─────────────────────────────────────────────────┤
│ REPEATABLE READ   │ Non-repeatable Read 방지     │
│                   │ Phantom Read 가능            │
├─────────────────────────────────────────────────┤
│ SERIALIZABLE      │ 모든 문제 방지               │
│                   │ 성능 저하                    │
└─────────────────────────────────────────────────┘
```

### 5.1 문제 현상
```
Dirty Read:
T1: UPDATE 계좌 SET 잔액 = 0 WHERE id = 'A'  (미커밋)
T2: SELECT 잔액 FROM 계좌 WHERE id = 'A'  → 0 읽음
T1: ROLLBACK
→ T2는 잘못된 값을 읽음

Non-repeatable Read:
T1: SELECT 잔액 FROM 계좌 WHERE id = 'A'  → 100
T2: UPDATE 계좌 SET 잔액 = 200 WHERE id = 'A'; COMMIT;
T1: SELECT 잔액 FROM 계좌 WHERE id = 'A'  → 200
→ 같은 쿼리가 다른 결과

Phantom Read:
T1: SELECT * FROM 주문 WHERE 금액 > 10000  → 5행
T2: INSERT INTO 주문 VALUES (..., 20000); COMMIT;
T1: SELECT * FROM 주문 WHERE 금액 > 10000  → 6행
→ 행이 추가/삭제됨
```

## 6. 격리 수준별 문제

| 격리 수준 | Dirty Read | Non-repeatable | Phantom |
|-----------|------------|----------------|---------|
| READ UNCOMMITTED | O | O | O |
| READ COMMITTED | X | O | O |
| REPEATABLE READ | X | X | O |
| SERIALIZABLE | X | X | X |

## 7. 분산 트랜잭션

### 7.1 2PC (Two-Phase Commit)
```
참여자들이 모두 커밋하거나 모두 롤백

Phase 1: Prepare
Coordinator → 모든 참여자: "커밋 준비됐니?"
참여자 → Coordinator: "준비됨" 또는 "실패"

Phase 2: Commit/Rollback
모두 준비됨 → Coordinator: "커밋해!"
하나라도 실패 → Coordinator: "롤백해!"

특징:
- 강한 일관성
- 블로킹 문제
- 성능 오버헤드
```

### 7.2 SAGA 패턴
```
장기 실행 트랜잭션을 여러 로컬 트랜잭션으로 분리

순서:
1. 주문 생성 → 성공
2. 결제 처리 → 실패!
3. 보상 트랜잭션: 주문 취소

특징:
- 최종 일관성
- 비블로킹
- 보상 로직 필요
```

## 8. 코드 예시

```python
from contextlib import contextmanager
from enum import Enum
import logging

class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"

class Transaction:
    """트랜잭션 시뮬레이션"""

    def __init__(self, isolation_level=IsolationLevel.READ_COMMITTED):
        self.isolation_level = isolation_level
        self.operations = []
        self.savepoints = {}
        self.state = "active"

    def execute(self, operation, *args):
        """연산 실행"""
        if self.state != "active":
            raise Exception("트랜잭션이 활성 상태가 아님")

        try:
            result = operation(*args)
            self.operations.append({
                'operation': operation,
                'args': args,
                'result': result
            })
            return result
        except Exception as e:
            self.state = "failed"
            raise e

    def savepoint(self, name):
        """세이브포인트 생성"""
        self.savepoints[name] = len(self.operations)
        return name

    def rollback_to_savepoint(self, name):
        """세이브포인트까지 롤백"""
        if name not in self.savepoints:
            raise Exception(f"세이브포인트 {name} 없음")

        idx = self.savepoints[name]
        self.operations = self.operations[:idx]

    def commit(self):
        """커밋"""
        if self.state == "failed":
            raise Exception("실패한 트랜잭션은 커밋 불가")

        self.state = "committed"
        logging.info(f"트랜잭션 커밋: {len(self.operations)}개 연산")

    def rollback(self):
        """롤백"""
        self.state = "rolled_back"
        logging.info(f"트랜잭션 롤백: {len(self.operations)}개 연산 취소")

class AccountService:
    """계좌 서비스 (이체 예시)"""

    def __init__(self):
        self.accounts = {
            'A': {'balance': 1000000, 'lock': False},
            'B': {'balance': 500000, 'lock': False}
        }

    def get_balance(self, account_id):
        return self.accounts[account_id]['balance']

    def withdraw(self, account_id, amount):
        """출금"""
        account = self.accounts[account_id]
        if account['balance'] < amount:
            raise Exception(f"잔액 부족: {account['balance']}")
        account['balance'] -= amount
        return account['balance']

    def deposit(self, account_id, amount):
        """입금"""
        account = self.accounts[account_id]
        account['balance'] += amount
        return account['balance']

    @contextmanager
    def transaction(self):
        """트랜잭션 컨텍스트 매니저"""
        tx = Transaction()
        snapshot = {k: v.copy() for k, v in self.accounts.items()}

        try:
            yield tx
            tx.commit()
        except Exception as e:
            # 롤백: 원상 복구
            self.accounts = snapshot
            tx.rollback()
            raise e

    def transfer(self, from_id, to_id, amount):
        """이체"""
        with self.transaction() as tx:
            # 출금
            tx.execute(self.withdraw, from_id, amount)
            # 입금
            tx.execute(self.deposit, to_id, amount)

            return True

# 사용 예시
service = AccountService()

print("=== 초기 잔액 ===")
print(f"A계좌: {service.get_balance('A'):,}원")
print(f"B계좌: {service.get_balance('B'):,}원")

print("\n=== 이체 실행 (10만원) ===")
try:
    service.transfer('A', 'B', 100000)
    print("이체 성공!")
except Exception as e:
    print(f"이체 실패: {e}")

print("\n=== 이체 후 잔액 ===")
print(f"A계좌: {service.get_balance('A'):,}원")
print(f"B계좌: {service.get_balance('B'):,}원")

print("\n=== 초과 이체 시도 ===")
try:
    service.transfer('A', 'B', 50000000)  # 잔액 초과
except Exception as e:
    print(f"이체 실패: {e}")

print("\n=== 실패 후 잔액 (롤백됨) ===")
print(f"A계좌: {service.get_balance('A'):,}원")
print(f"B계좌: {service.get_balance('B'):,}원")
```

## 9. 장단점

### 트랜잭션의 장점
| 장점 | 설명 |
|-----|------|
| 데이터 무결성 | ACID 보장 |
| 오류 복구 | ROLLBACK 가능 |
| 동시성 제어 | 격리 수준 |

### 높은 격리 수준의 단점
| 단점 | 설명 |
|-----|------|
| 성능 저하 | 락 대기 증가 |
| 교착상태 | 데드락 가능성 |
| 처리량 감소 | 동시성 제한 |

## 10. 실무에선? (기술사적 판단)
- **OLTP**: READ COMMITTED 또는 REPEATABLE READ
- **일반 서비스**: READ COMMITTED (기본값)
- **금융**: SERIALIZABLE 또는 REPEATABLE READ
- **분산환경**: SAGA 패턴 고려

## 11. 관련 개념
- ACID
- 동시성 제어
- 로킹
- 회복

---

## 어린이를 위한 종합 설명

**트랜잭션은 "한 번에 다 하기"야!**

### ACID 💧
```
A (원자성): 전부 하거나 전부 안 하거나
   "이체는 출금+입금이 같이!"

C (일관성): 규칙을 지켜요
   "잔액은 마이너스가 안 돼!"

I (격리성): 다른 사람이 방해하지 마
   "내가 쓰는 동안 기다려!"

D (지속성): 저장하면 계속 남아요
   "커밋하면 사라지지 않아!"
```

### COMMIT vs ROLLBACK 📝
```
COMMIT: "확정!" ✅
   - 이체 완료
   - 되돌릴 수 없음

ROLLBACK: "취소!" ❌
   - 이체 취소
   - 처음으로 되돌림
```

### 계좌 이체 예시 💰
```
시작:
A: 100만원
B: 50만원

이체 (10만원):
1. A 출금: 100 → 90만원
2. B 입금: 50 → 60만원
3. COMMIT

완료:
A: 90만원
B: 60만원
```

**비밀**: 트랜잭션이 있어서 은행이체가 안전해요! 🏦✨
