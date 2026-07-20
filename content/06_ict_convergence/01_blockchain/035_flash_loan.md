---
title: "Flash Loan"
date: "2026-03-03"
tags:
  - "studynote-ict-convergence"
weight: 35
---
> **핵심 인사이트**
> 1. Flash Loan은 블록체인의 원자성(Atomicity)을 이용해 담보 없이 대규모 자금을 빌리고, 하나의 트랜잭션 내에서 사용 후 즉시 상환하는 DeFi 혁신 금융 도구다.
> 2. 상환 실패 시 전체 트랜잭션이 롤백(revert)되므로 대출자는 손실 위험이 없지만, 공격자는 이를 악용해 가격 조작, 재진입 공격(Reentrancy)에 활용한다.
> 3. 아비트라지(Arbitrage), 청산(Liquidation), 담보 전환(Collateral Swap) 등 합법적 활용도 크지만, Flash Loan Attack은 DeFi 보안의 핵심 위협이다.

---

## I. Flash Loan 동작 원리

```
하나의 이더리움 트랜잭션 내에서:

1. 프로토콜에서 자금 대출 (예: 100만 DAI)
   |
   v
2. 대출금으로 DeFi 작업 수행
   (아비트라지, 청산, 담보 교환 등)
   |
   v
3. 원금 + 수수료 상환 (0.09% Aave 기준)
   |
   v
4a. 상환 성공 -> 트랜잭션 완료(Commit)
4b. 상환 실패 -> 전체 롤백(Revert)
```

- <strong>원자성(Atomicity)</strong>: 1~4가 모두 성공하거나 모두 실패
- **담보 불필요**: 상환이 보장되므로 신용 평가 불필요
- **수수료**: Aave 0.09%, dYdX 2 wei 고정

> 📢 **섹션 요약 비유**: 은행이 "지금 당장 갚으면 OK"라는 조건으로 무담보 대출 — 갚지 못하면 거래 자체가 없었던 일이 된다.

---

## II. 합법적 활용 사례

### 2-1. 아비트라지 (Arbitrage)

```
DEX A: ETH = 2,000 DAI
DEX B: ETH = 2,100 DAI

Flash Loan 1,000,000 DAI
  -> DEX A에서 500 ETH 매수 (200만 DAI)
  -> DEX B에서 500 ETH 매도 (210만 DAI)
  -> 차익 10만 DAI - 수수료 = 순이익
  -> 원금 상환
```

### 2-2. 청산 (Liquidation)

```
담보 부족 포지션 발생
  -> Flash Loan으로 부채 즉시 상환
  -> 담보 자산 인수 (할인 가격)
  -> 담보 매각으로 Flash Loan 상환
  -> 청산 보너스 획득
```

### 2-3. 담보 전환 (Collateral Swap)

```
기존: ETH 담보 -> DAI 대출
목표: WBTC 담보로 전환

Flash Loan DAI
  -> DAI 대출 상환 (ETH 담보 회수)
  -> ETH -> WBTC 교환
  -> WBTC 담보로 재대출
  -> Flash Loan 상환
```

> 📢 **섹션 요약 비유**: 순식간에 여러 가게를 돌며 싸게 사서 비싸게 파는 번개 쇼핑 — 손에서 돈이 나갔다 들어오는 시간이 0.

---

## III. Flash Loan Attack 패턴

```
대표 공격 사례: bZx Attack (2020)

1. Flash Loan 10,000 ETH
2. 일부로 WBTC 공매도 포지션 설정 (bZx)
3. 나머지로 Uniswap에서 WBTC 대량 매수
   -> WBTC 가격 급등
4. bZx의 오라클이 부풀려진 가격 참조
   -> 공매도 포지션 청산 이익 획득
5. 이익으로 원금 상환
```

| 공격 유형          | 설명                          |
|-------------------|-------------------------------|
| 가격 조작          | 오라클 조작, 슬리피지 악용     |
| 재진입 공격        | 콜백 함수 내 재호출            |
| 거버넌스 공격      | 순간 의결권 확보으로 제안 통과 |
| 청산 봇 앞지르기   | MEV(최대 추출 가능 가치) 악용  |

> 📢 **섹션 요약 비유**: 선거 당일 아침 돈을 빌려 표를 사고, 결과 발표 직후 갚는 것 — 규칙이 없으면 민주주의가 뚫린다.

---

## IV. Flash Loan 방어 전략

| 방어 방법             | 설명                                    |
|----------------------|-----------------------------------------|
| TWAP 오라클           | 순간 가격 대신 시간 가중 평균 가격 사용  |
| 재진입 방지 (Mutex)   | OpenZeppelin ReentrancyGuard            |
| 거버넌스 시간 지연    | 제안-실행 간 타임락(Timelock) 설정       |
| 플래시 론 탐지        | tx.origin vs msg.sender 검사            |
| 회로 차단기           | 단일 블록 내 대규모 가격 변동 시 거래 중단|

> 📢 **섹션 요약 비유**: 번개 쇼핑꾼이 오자마자 가게 가격을 바꾸는 것 — 실시간 가격 대신 평균 가격표를 사용해 조작을 막는다.

---

## V. 실무 시나리오 — Aave Flash Loan 구현

```solidity
// SPDX-License-Identifier: MIT
contract FlashLoanExample is IFlashLoanReceiver {
    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        // 아비트라지 로직 실행
        // ...

        // 원금 + 수수료 승인
        uint256 amountOwed = amounts[0] + premiums[0];
        IERC20(assets[0]).approve(address(POOL), amountOwed);
        return true;
    }
}
```

> 📢 **섹션 요약 비유**: 코드 한 줄로 백만 달러 대출·사용·상환 — 스마트 컨트랙트가 전통 금융의 담보 심사를 대체.

---

## 📌 관련 개념 맵

```
Flash Loan
+-- 기반 기술
|   +-- 블록체인 원자성 (Atomicity)
|   +-- 스마트 컨트랙트 콜백
|   +-- ERC-3156 표준
+-- 합법적 활용
|   +-- 아비트라지 (가격 차익)
|   +-- 청산 (Liquidation)
|   +-- 담보 전환
+-- 공격 벡터
|   +-- 가격 오라클 조작
|   +-- 재진입 공격 (Reentrancy)
|   +-- 거버넌스 공격
+-- 방어
    +-- TWAP 오라클
    +-- ReentrancyGuard
    +-- Timelock 거버넌스
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 금융]
담보 대출 + 신용 평가 + 며칠 처리
      |
      v
[DeFi 등장 (2017~)]
무허가 대출, 스마트 컨트랙트
      |
      v
[Flash Loan 등장 (Aave 2020)]
원자성 활용, 담보 없는 순간 대출
      |
      v
[Flash Loan 공격 (bZx 2020)]
오라클 조작 + 가격 조작 공격
      |
      v
[방어 기술 발전]
TWAP, ReentrancyGuard, Timelock
      |
      v
[현재: MEV & 고도화 공격]
Flashbots, 샌드위치 공격, 거버넌스 공격
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 플래시 론은 "지금 당장 갚겠다"는 약속만 있으면 담보 없이도 큰돈을 빌릴 수 있는 마법이에요.
2. 갚지 못하면 거래 자체가 없었던 일이 되니까 은행도 손해가 없어요.
3. 착한 사람은 이걸로 싸게 사고 비싸게 팔아 돈을 벌지만, 나쁜 사람은 가격을 조작하는 데 쓰기도 해요!
