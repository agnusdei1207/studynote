---
title: "Layer1 Mainnet"
date: "2026-03-04"
tags:
  - "studynote-ict-convergence"
weight: 39
---
> **핵심 인사이트**
> 1. 레이어1(Layer 1)은 블록체인 스택의 기반 계층으로, 자체 합의 메커니즘과 네이티브 토큰을 통해 분산 원장의 보안·탈중앙화·처리량(Scalability) 세 가지를 모두 달성하려는 블록체인 트릴레마(Trilemma)의 최전선이다.
> 2. 비트코인(PoW, 7TPS), 이더리움(PoS, ~30TPS), 솔라나(PoH+PoS, ~65,000TPS)는 각각 다른 트릴레마 트레이드오프 — 비트코인은 보안 최우선, 이더리움은 탈중앙화+보안, 솔라나는 처리량+속도 — 를 선택한 결과다.
> 3. 레이어1 확장 전략은 두 갈래 — 레이어1 자체 개선(샤딩, 합의 알고리즘 교체)과 레이어2에게 처리 위임(채널, 롤업) — 이며, 현재 주류는 레이어1 보안을 유지하며 레이어2로 처리량을 위임하는 방향이다.

---

## I. 블록체인 트릴레마

```
블록체인 트릴레마 (Vitalik Buterin):

          보안 (Security)
           /         \\
          /           \\
  탈중앙화    ——    처리량
  (Decentralization)  (Scalability)

세 가지를 동시에 완벽하게 달성 불가
-> 어느 두 가지를 우선할지 선택

Bitcoin: 보안 + 탈중앙화 (처리량 희생)
  PoW + 10분 블록 타임 = 7 TPS

Ethereum: 보안 + 탈중앙화 (처리량 제한)
  PoS + 12초 블록 = ~30 TPS

Solana: 처리량 + 보안 (탈중앙화 일부 희생)
  PoH + PoS + 고성능 하드웨어 요구
  ~65,000 TPS (이론), 실제 ~4,000 TPS

Binance Smart Chain: 처리량 + 탈중앙화 일부 희생
  21개 검증자 (더 중앙화)
  ~300 TPS
```

> 📢 **섹션 요약 비유**: 삼각형 꼭짓점 세 개 중 동시에 두 곳만 닿을 수 있는 고무줄 — 셋 다 닿으려면 끊어짐.

---

## II. 주요 L1 비교

```
L1 블록체인 비교표:

              Bitcoin   Ethereum  Solana   Cardano
합의 알고리즘:   PoW       PoS       PoH+PoS  PoS(Ouroboros)
블록 타임:      10분       12초      0.4초    20초
TPS:            7         ~30       ~4,000   ~250
검증자:         수십만     수십만     ~2,000   ~3,000
스마트 컨트랙트: X         O(EVM)    O        O(Plutus)
네이티브 토큰:  BTC        ETH       SOL      ADA
주요 용도:      가치저장   DeFi/NFT  DeFi/NFT 금융

레이어1 핵심 요소:
  - 자체 합의 (자생적 보안)
  - 네이티브 토큰 (경제적 인센티브)
  - 스마트 컨트랙트 가상머신 (EVM, SVM)
  - 상태 관리 (Account 또는 UTXO 모델)
```

> 📢 **섹션 요약 비유**: L1은 국가 통화 발행권을 가진 중앙은행 — 규칙(합의)을 스스로 정하고, 화폐(토큰)를 발행하는 주권 시스템.

---

## III. 레이어1 확장 전략

```
레이어1 자체 확장:

1. 샤딩 (Sharding):
   블록체인을 여러 샤드(조각)로 분할
   각 샤드가 독립적으로 트랜잭션 처리
   이더리움 로드맵: Danksharding

   문제: 샤드 간 통신, 보안 복잡성

2. 합의 알고리즘 개선:
   PoW -> PoS (이더리움 머지 2022)
   에너지 99.95% 절약
   TPS 직접 향상 효과는 제한적

3. 블록 크기/타임 조정:
   단기 처리량 향상 but 중앙화 위험
   (큰 블록 -> 일반 노드 운영 어려움)

레이어2 위임:
  L1: 보안/합의만 담당
  L2 (롤업): 실제 트랜잭션 처리
  L2가 주기적으로 L1에 증명 제출

  Optimistic Rollup: ETH 위에 10x TPS
  ZK Rollup: ETH 위에 100x TPS (zkSync)
```

> 📢 **섹션 요약 비유**: L1 직접 확장은 고속도로 확장 공사, L2는 고속도로 위에 2층 도로 만들기 — 2층이 더 빠르지만 기초(L1)가 안전해야 함.

---

## IV. EVM 호환성

```
EVM (Ethereum Virtual Machine) 생태계:

EVM 호환 L1들:
  Ethereum (원조)
  Binance Smart Chain (EVM 포크)
  Avalanche C-Chain (EVM 호환)
  Polygon PoS (EVM 호환)
  Fantom (EVM 호환)

장점:
  Solidity 코드 재사용 가능
  MetaMask, DApp 그대로 사용
  개발자 풀 공유

EVM 비호환 (독자 VM):
  Solana: SVM (Rust, C)
  Cardano: Plutus VM (Haskell)
  Near Protocol: WASM 기반

EVM 트레이드오프:
  EVM 호환: 쉬운 마이그레이션
  독자 VM: 성능/기능 최적화 가능
```

> 📢 **섹션 요약 비유**: EVM 호환은 안드로이드 호환 스마트폰처럼 — 기존 앱(DApp)을 그대로 실행 가능, 독자 생태계보다 유리.

---

## V. 실무 시나리오 — DeFi 프로토콜 L1 선택

```
DeFi 프로토콜 개발팀 L1 선택 기준:

기능 요구사항:
  스마트 컨트랙트 필수 -> Bitcoin 제외

성능 요구사항:
  DEX (탈중앙 거래소): 초당 수천 트랜잭션
  -> 이더리움 직접: ~30TPS 부족
  -> 이더리움 + L2 (Arbitrum): ~2,000TPS
  -> Solana: 고성능 but 다운타임 이력 있음

보안/탈중앙화:
  $1B+ TVL(총 예치금) -> 보안 최우선
  이더리움: 가장 검증된 L1

비용:
  이더리움 가스비: 피크 시 $50/트랜잭션
  Solana: $0.0001/트랜잭션

결정:
  소규모 DeFi: Solana 또는 L2
  대규모 DeFi (TVL > $1B): Ethereum + L2

2024년 현재:
  DeFi TVL 상위: Ethereum L1+L2 (>60%)
  성장세: Solana, Base(Coinbase L2)
```

> 📢 **섹션 요약 비유**: 큰 돈이 오가는 DeFi는 보안 검증된 이더리움을, 빠른 실험은 저렴한 Solana를 선택 — 안전과 속도의 트레이드오프.

---

## 📌 관련 개념 맵

```
레이어1 메인넷
+-- 트릴레마
|   +-- 보안, 탈중앙화, 처리량
+-- 주요 L1
|   +-- Bitcoin (PoW, 보안 최우선)
|   +-- Ethereum (PoS, DeFi 기반)
|   +-- Solana (PoH, 고처리량)
+-- 확장 전략
|   +-- L1 자체: 샤딩, 합의 개선
|   +-- L2 위임: 롤업 (Optimistic, ZK)
+-- EVM 생태계
    +-- EVM 호환 vs 독자 VM
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Bitcoin (2009)]
최초 L1, PoW, 가치 저장
      |
      v
[Ethereum (2015)]
스마트 컨트랙트 L1
DeFi/NFT 폭발 성장
      |
      v
[L1 경쟁 (2019~2021)]
Solana, Avalanche, BSC 등
      |
      v
[이더리움 머지 (2022)]
PoW -> PoS 전환
      |
      v
[현재: L2 중심 (2023~)]
Arbitrum, Optimism, zkSync
L1 보안 + L2 처리량 분리 트렌드
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 레이어1은 나라의 법과 화폐처럼 블록체인의 가장 기본 규칙을 정하는 층이에요 — 비트코인, 이더리움, 솔라나가 각자 다른 나라처럼 독립적으로 운영돼요.
2. 안전성·탈중앙화·속도 세 가지를 동시에 완벽하게 달성할 수 없어서, 각 블록체인은 어떤 것을 우선할지 선택해야 해요.
3. 이더리움은 느리지만 안전해서 큰 돈이 오가는 금융에 쓰이고, 솔라나는 빠르지만 가끔 멈추기도 해서 빠른 거래에 쓰여요!
