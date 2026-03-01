+++
title = "블록체인 (Blockchain)"
date = 2025-03-01

[extra]
categories = "ict-ai_blockchain"
+++

# 블록체인 (Blockchain)

## 핵심 인사이트 (3줄 요약)
> **분산 원장 기술로 거래를 투명하게 기록**하는 시스템. 블록들이 체인처럼 연결되어 위변조가 불가능. 비트코인, 이더리움 등 암호화폐와 스마트 계약의 기반.

## 1. 개념
블록체인은 **데이터를 블록 단위로 저장하고, 각 블록을 암호학적으로 연결**하여 분산 네트워크에 저장하는 기술이다.

> 비유: "공개 장부" - 모두가 볼 수 있고, 한 번 적으면 지울 수 없는 장부

## 2. 블록체인 구조

```
┌─────────────────────────────────────────────────────────┐
│                    블록체인 구조                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ Block 1 │───→│ Block 2 │───→│ Block 3 │───→ ...    │
│  └────┬────┘    └────┬────┘    └────┬────┘            │
│       │              │              │                  │
│       ▼              ▼              ▼                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │Header   │    │Header   │    │Header   │            │
│  │- Prev   │    │- Prev   │    │- Prev   │            │
│  │  Hash   │    │  Hash   │    │  Hash   │            │
│  │- Nonce  │    │- Nonce  │    │- Nonce  │            │
│  │- Time   │    │- Time   │    │- Time   │            │
│  ├─────────┤    ├─────────┤    ├─────────┤            │
│  │Transactions│ │Transactions│ │Transactions│          │
│  │- Tx1    │    │- Tx1    │    │- Tx1    │            │
│  │- Tx2    │    │- Tx2    │    │- Tx2    │            │
│  │- ...    │    │- ...    │    │- ...    │            │
│  └─────────┘    └─────────┘    └─────────┘            │
│                                                         │
│  각 블록은 이전 블록의 해시를 포함 → 체인 형성        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3. 블록체인 특성

```
1. 분산성 (Decentralization)
   - 중앙 서버 없음
   - 모든 노드가 동일한 데이터 보유
   - 단일 실패 지점 없음

2. 투명성 (Transparency)
   - 모든 거래 공개
   - 누구나 조회 가능
   - 추적 가능

3. 불변성 (Immutability)
   - 한 번 기록되면 변경 불가
   - 해시 체인으로 보호
   - 위변조 방지

4. 보안성 (Security)
   - 암호화 기반
   - 합의 메커니즘
   - 51% 공격 방어
```

## 4. 합의 메커니즘

```
┌────────────────────────────────────────────────────────┐
│                   합의 메커니즘                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 작업 증명 (Proof of Work, PoW)                     │
│     - 복잡한 연산 문제 해결                            │
│     - 채굴(Mining)                                     │
│     - 비트코인 사용                                    │
│     - 단점: 에너지 소모 큼                             │
│                                                        │
│  2. 지분 증명 (Proof of Stake, PoS)                    │
│     - 보유 코인 양에 비례하여 검증 권한                │
│     - 이더리움 2.0                                     │
│     - 에너지 효율적                                    │
│                                                        │
│  3. 위임 지분 증명 (Delegated PoS)                     │
│     - 대표 노드 선출                                   │
│     - 빠른 처리 속도                                   │
│     - EOS, TRON                                        │
│                                                        │
│  4. 실용 비잔틴 장애 허용 (PBFT)                       │
│     - 투표 기반                                        │
│     - 하이퍼레저 패브릭                                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 블록체인 종류

```
1. 퍼블릭 블록체인 (Public)
   - 누구나 참여 가능
   - 비트코인, 이더리움
   - 완전 탈중앙화

2. 프라이빗 블록체인 (Private)
   - 허가된 참여자만
   - 기업 내부용
   - 높은 처리 속도

3. 컨소시엄 블록체인 (Consortium)
   - 여러 기관이 운영
   - 하이퍼레저, R3 Corda
   - 부분 탈중앙화

┌─────────────┬─────────────┬─────────────┬─────────────┐
│    구분      │   퍼블릭    │  프라이빗   │  컨소시엄   │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ 참여        │ 누구나      │ 허가된 자   │ 선정된 기관 │
│ 속도        │ 느림        │ 빠름        │ 중간        │
│ 보안        │ 높음        │ 중간        │ 높음        │
│ 탈중앙화    │ 완전        │ 낮음        │ 부분        │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

## 6. 스마트 계약

```
스마트 계약 (Smart Contract):
- 블록체인상에서 자동 실행되는 계약
- 조건 충족 시 자동 처리
- 신뢰 없는 거래 가능

예시 (송금):
┌─────────────────────────────────────┐
│ if (buyer_confirmed == true &&      │
│     payment_received == true) {     │
│     transfer(item, buyer);          │
│     transfer(payment, seller);      │
│ }                                   │
└─────────────────────────────────────┘

이더리움:
- 스마트 계약 플랫폼
- 솔리디티(Solidity) 언어
- DApp 개발 가능
```

## 7. 코드 예시

```python
from dataclasses import dataclass
from typing import List, Dict, Any
import hashlib
import time

@dataclass
class Transaction:
    """트랜잭션"""
    sender: str
    receiver: str
    amount: float
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    def to_dict(self) -> Dict:
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def hash(self) -> str:
        """트랜잭션 해시"""
        tx_string = str(self.to_dict())
        return hashlib.sha256(tx_string.encode()).hexdigest()

@dataclass
class Block:
    """블록"""
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def calculate_hash(self) -> str:
        """블록 해시 계산"""
        block_string = f"{self.index}{self.timestamp}{len(self.transactions)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int):
        """채굴 (작업 증명)"""
        target = "0" * difficulty
        while not self.calculate_hash().startswith(target):
            self.nonce += 1
        self.hash = self.calculate_hash()

class Blockchain:
    """블록체인 구현"""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = 10.0

        # 제네시스 블록 생성
        self.create_genesis_block()

    def create_genesis_block(self):
        """제네시스 블록 생성"""
        genesis = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0"
        )
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def get_latest_block(self) -> Block:
        """최신 블록 조회"""
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """트랜잭션 추가"""
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        """대기 중인 트랜잭션 채굴"""
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        block.mine(self.difficulty)
        self.chain.append(block)

        # 채굴 보상
        self.pending_transactions = [
            Transaction(sender="network", receiver=miner_address, amount=self.mining_reward)
        ]

    def get_balance(self, address: str) -> float:
        """잔액 조회"""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance

    def is_chain_valid(self) -> bool:
        """체인 유효성 검증"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# 사용 예시
print("=== 블록체인 시뮬레이션 ===\n")

# 블록체인 생성
blockchain = Blockchain(difficulty=2)

# 트랜잭션 생성
blockchain.add_transaction(Transaction("Alice", "Bob", 50))
blockchain.add_transaction(Transaction("Bob", "Charlie", 25))

# 채굴
print("채굴 중...")
blockchain.mine_pending_transactions("Miner1")
print(f"블록 1 채굴 완료!")

# 추가 트랜잭션
blockchain.add_transaction(Transaction("Charlie", "Alice", 10))
blockchain.mine_pending_transactions("Miner1")
print(f"블록 2 채굴 완료!")

# 잔액 확인
print("\n=== 잔액 확인 ===")
print(f"Alice: {blockchain.get_balance('Alice')}")
print(f"Bob: {blockchain.get_balance('Bob')}")
print(f"Charlie: {blockchain.get_balance('Charlie')}")
print(f"Miner1: {blockchain.get_balance('Miner1')} (채굴 보상)")

# 체인 검증
print(f"\n체인 유효성: {'유효함' if blockchain.is_chain_valid() else '유효하지 않음'}")
```

## 8. 블록체인 진화

```
블록체인 1.0: 암호화폐
- 비트코인
- P2P 전자 화폐

블록체인 2.0: 스마트 계약
- 이더리움
- 프로그래밍 가능한 블록체인

블록체인 3.0: DApp & 엔터프라이즈
- 하이퍼레저
- 기업용 솔루션

블록체인 4.0: 산업 적용
- Web3
- 메타버스 연동
```

## 9. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 투명성 | 모든 거래 공개 |
| 보안 | 위변조 불가 |
| 탈중앙화 | 중개 없는 거래 |
| 자동화 | 스마트 계약 |

### 단점
| 단점 | 설명 |
|-----|------|
| 속도 | 처리 속도 느림 |
| 확장성 | 대규모 처리 한계 |
| 에너지 | 채굴 에너지 소모 |
| 규제 | 법적 규제 불확실 |

## 10. 실무에선? (기술사적 판단)
- **금융**: 송금, 결제, 증권 거래
- **공공**: 전자투표, 신원증명
- **물류**: 이력 추적, 원산지 증명
- **의료**: 전자처방, 임상데이터
- **저작권**: NFT, 디지털 자산

## 11. 관련 개념
- 암호화폐
- 스마트 계약
- 분산원장
- 합의 알고리즘

---

## 어린이를 위한 종합 설명

**블록체인은 "모두가 같은 장부"예요!**

### 어떻게 작동할까요? 📒
```
기존 방식:
은행이 장부를 가지고 있어요
→ 은행이 기록을 바꿀 수도?

블록체인:
모두가 장부를 가지고 있어요
→ 아무도 몰래 바꿀 수 없어요!
```

### 블록과 체인 🔗
```
블록: 거래 내역 상자
┌─────────────────┐
│ A→B: 100원      │
│ B→C: 50원       │
└─────────────────┘

체인: 상자들이 연결됨
[블록1]─[블록2]─[블록3]...
```

### 채굴이란? ⛏️
```
어려운 문제를 풀면:
- 새 블록을 만들 수 있어요
- 보상을 받아요 (비트코인)

수학 문제를 컴퓨터로 풀어요!
```

### 스마트 계약 📜
```
자동으로 실행되는 계약:
"돈을 보내면 상품을 보내요"
→ 사람이 확인 안 해도 돼요!
```

**비밀**: 비트코인이 블록체인으로 만들어졌어요! ₿✨
