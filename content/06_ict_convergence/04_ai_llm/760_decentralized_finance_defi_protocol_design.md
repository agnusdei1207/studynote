---
title: "Decentralized Finance DeFi Protocol Design"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 760
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DeFi 프로토콜 설계는 이더리움 등 결정론적 상태머신 위에서 `Constant Function Market Maker(x·y=k)`, `Compound-style cToken 과잉담보 모델(Collateral Factor, LTV)`, `MakerDAO의 Vault CDP(Collateralized Debt Position)` 등 수학적 invariant와 오프체인 오라클(Chainlink Price Feed)을 결합하여 신뢰 최소화(trust-minimized)된 금융 primitives를 합성하는 것이다.
> 2. **가치**: 전통 금융 대비 운영 오버헤드 제거로 스프레드를 30~50bps에서 1~5bps로 축소(Uni v3), 24/7 무허가 composability, TVL 100B USD+ 규모의 글로벌 단일 유동성 풀 실현, atomic cross-protocol arbitrage로 자본 효율 극대화.
> 3. **판단 포인트**: 핵심 trade-off는 **탈중앙성-확장성-보안 트릴레마**와 **MEV(Maximal Extractable Value) 노출**, **오라콜 의존성(price feed manipulation risk)**, **스마트 컨트랙트 불변성(immutability) 하의 upgradeability 패턴 선택** (Transparent vs UUPS Proxy) 사이의 균형점 결정이다.

---

## Ⅰ. 개요 및 필요성

전통 금융(TradFi)은 약 7.7T USD 규모의 글로벌 결제·신용 인프라를 운영하지만, ① 은행의 신용 중개에 따른 KYC/AML 마찰비용, ② 영업시간·국경 제한, ③ 단일 기관의 부도위험(counterparty risk), ④ 장부 투명성 부재로 인한 사후적 감사 의존 등의 구조적 한계를 가진다. 2008년 서브프라임 모기지 사태, 2023년 SVB·Signature Bank 사태처럼 중앙화 신뢰기관의 실패는 시스템적 위험(systemic risk)으로 전이된다.

DeFi는 2018년 Compound의 `COMP` 거버넌스 토큰 배포를 기점으로 "**프로토콜은 법 없이 코드(Code is Law)로 운영되는 자율조직**"이라는 새로운 패러다임을 제시했다. 핵심 동기는 ① **신뢰 최소화** — 신뢰 대상을 인간/기관에서 수학적 합의 알고리즘으로 전환, ② **무허가 합성가능성(Composability)** — 레고 블록식 프로토콜 스택을 통한 atomic transaction, ③ **공개 검증가능성** — 모든 상태·거래가 온체인에서 검증 가능, ④ **글로벌 단일 유동성** — 인터넷이 단일 TCP/IP 스택을 가지듯 DeFi는 단일 금융 OS를 지향한다.

2024년 기준 DeFi TVL은 약 100B USD(Uniswap 5B, Aave 14B, MakerDAO 4B, Lido 32B ETH-staking)를 기록하며, 일일 온체인 거래량 10B USD+의 미시구조(microstructure)가 형성되어 있다.

```text
+------------------------------------------------------------------+
|          DeFi 프로토콜 설계 패러다임 비교 (TradFi vs DeFi)         |
+------------------------------------------------------------------+
|                                                                  |
|  TradFi (Centralized)              DeFi (Decentralized)          |
|  +---------------+                 +----------------------+     |
|  | Central Bank  |                 |  Governance Token    |     |
|  |  + Clearing   |                 |  + DAO Voting        |     |
|  |  + Custodian  |                 |  + On-chain Treasury |     |
|  +-------+-------+                 +----------+-----------+     |
|          |                                    |                  |
|  +-------v-------+                 +----------v-----------+     |
|  |  Intermediary |                 |  Smart Contract      |     |
|  |  (은행/증권사) |                 |  (EVM/Solidity/Vyper)|     |
|  |  - KYC/AML    |                 |  - Permissionless    |     |
|  |  - 영업시간   |                 |  - 24/7/365          |     |
|  |  - 2~7일结算   |                 |  - 12~15s block      |     |
|  +-------+-------+                 +----------+-----------+     |
|          |                                    |                  |
|  +-------v-------+                 +----------v-----------+     |
|  | Ledger (DB)   |                 |  Blockchain State    |     |
|  | - 불투명       |                 |  - 완전 투명          |     |
|  | - 감사 사후    |                 |  - 실시간 검증        |     |
|  | - 수기 오류    |                 | - 결정론적 머신       |     |
|  +-------+-------+                 +----------+-----------+     |
|          |                                    |                  |
|  +-------v-------+                 +----------v-----------+     |
|  | 실물 자산     |                 |  Crypto-native 자산  |     |
|  | (은행 예금)   |                 |  (ETH, wBTC, stETH) |     |
|  +---------------+                 +----------------------+     |
|                                                                  |
|  문제점:                       해결:                              |
|  ✗ 단일 실패점(SPOF)           ✓ 분산 합의(1/N 신뢰)             |
|  ✗ 검열 가능성                  ✓ Censorship-resistance          |
|  ✗ 결제 지연 T+2               ✓ Atomic Settlement (12s)        |
|  ✗ 진입 장벽 (고액 최소투자)     ✓ EOA 생성만으로 참여             |
+------------------------------------------------------------------+
```

기존 CeFi(Centralized Finance)의 Layered Architecture(Matching Engine -> Clearing -> Settlement -> Custody)가 DeFi에서는 **단일 EVM 컨트랙트**로 압축되어, 한 트랜잭션 내에서 Matching-Clearing-Settlement가 atomic하게 완료된다. 예를 들어 Uniswap V3의 swap은 `pool.swap()` 한 호출로 가격 결정(matching), 토큰 전송(settlement), LP 토큰 발행(clearing)이 동시 처리된다.

- **📢 섹션 요약 비유**: TradFi가 "은행 창구 직원에게 수표 주고 3일 기다려 현금 받는" 방식이라면, DeFi는 "수학 공식이 적힌 자판기"에 동전을 넣으면 즉시 음료(자산 교환)가 나오는 구조다. 자판기 프로그램(Smart Contract)이 오작동하면 누구도 중재할 수 없다는 점만 주의하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DeFi 프로토콜은 일반적으로 **5계층 레이어 아키텍처**로 설계된다. 각 계층은 보안 경계(security boundary)를 가지며, 신뢰 가정(trust assumption)을 최소화하도록 분리된다.

```text
+--------------------------------------------------------------------+
|                DeFi 프로토콜 5계층 참조 아키텍처                    |
+--------------------------------------------------------------------+
|                                                                    |
|  L5  Governance & Tokenomics                                       |
|  +------------------------------------------------------------+  |
|  |  Governor Bravo / OpenZeppelin Governor + Timelock         |  |
|  |  - Proposal -> Vote (quorum > 4%) -> Timelock(48h) -> Execute |  |
|  |  - Token: ERC20Votes (snapshot 기반 위임형 투표)             |  |
|  +------------------------------------------------------------+  |
|                          ^                                         |
|  L4  Application Logic (비즈니스 룰)                                |
|  +------------------------------------------------------------+  |
|  |  Router / Vault / Pool / Position Manager                  |  |
|  |  - UniswapV3Router, AavePool, CompoundComptroller           |  |
|  |  - 핵심: ReentrancyGuard, AccessControl, Pausable            |  |
|  +------------------------------------------------------------+  |
|                          ^                                         |
|  L3  Primitive Libraries (수학적 핵심)                              |
|  +------------------------------------------------------------+  |
|  |  TickMath, SqrtPriceMath, OracleLib, WadRayMath,          |  |
|  |  FixedPoint96, LiquidityAmounts                            |  |
|  |  - 0.7->1.0 6-decimal, 1e27 WAD, 1e27 RAY 풀스케일          |  |
|  +------------------------------------------------------------+  |
|                          ^                                         |
|  L2  Asset Layer (토큰 표준)                                        |
|  +------------------------------------------------------------+  |
|  |  ERC-20 (fungible), ERC-721 (NFT), ERC-1155, ERC-4626     |  |
|  |  (Tokenized Vault), ERC-3156 (Flash Loan), ERC-2612 (Permit)|  |
|  |  - WETH9, wBTC, stETH (Lido), cDAI (Compound)             |  |
|  +------------------------------------------------------------+  |
|                          ^                                         |
|  L1  Infrastructure (블록체인 + 오라클 + 브릿지)                      |
|  +------------------------------------------------------------+  |
|  |  EVM (Ethereum/Arbitrum/Optimism/Base)                     |  |
|  |  Oracle: Chainlink PriceFeed (8 aggregator), Pyth, UMA     |  |
|  |  Bridge: LayerZero, Wormhole, CCIP, native canonical      |  |
|  +------------------------------------------------------------+  |
+--------------------------------------------------------------------+
```

### 핵심 메커니즘별 수학적 모델

**(1) AMM (Automated Market Maker) — Uniswap V3 집중 유동성**
- 기존 V2의 `x·y = k` 불변량을 유지하되, 유동성 공급자가 `[Pa, Pb]` 가격 범위를 지정하여 자본 효율을 ~4000배 향상.
- **집중 유동성 공식**:
  - `L = Δx · √Pb / (√Pb - √Pa) = Δy / (√Pb - √Pa)` (가상储备量)
  - `sqrtPriceX96 = √price · 2^96` (Q64.96 fixed-point)
  - 스왑 출력량: `amountOut = reserveIn · (1 - fee) - k / (reserveOut + amountIn·(1-fee))` (V2 단순형)
- **Tick 구조**: `price(i) = 1.0001^i`, 각 tick에서 `L`이 piecewise constant -> 사실상 **이산적限价委托簿(Discretized Limit Order Book)**.

**(2) Lending — Aave V3 과잉담보 모델**
- `Health Factor (HF) = Σ(Collateral_i · LiquidationThreshold_i) / Σ(Debt_j)`, HF < 1 시 청산 대상.
- `LTV (Loan-to-Value) = Debt / Collateral`, Aave USDC 기준 LTV=80%, Liquidation Threshold=85%.
- **Interest Rate Model**: `Utilization U = TotalBorrows / TotalLiquidity`
  - `Rborrow = Rslope1·U/Roptimal   (U ≤ Roptimal)`
  - `Rborrow = Rslope1 + (Rslope2·(U - Roptimal))/(1 - Roptimal)   (U > Roptimal)`
  - 급격한 금리 상승으로 borrow를 억제 -> utilization ≈ 100% 회피.
- **aToken**: 사용자가 예치 즉시 `aToken` 1:1 발행, `aToken.balance = principal · index / index₀`로 복리 자동 반영 (index는 1e27 RAY 단위, 매 블록 갱신).

**(3) Stablecoin CDP — MakerDAO DSR/Debt Ceiling**
- ETH를 Vault에 예치 -> `DAI` 발행, **Liquidation Ratio (LR)** 미만 시 청산.
- 예: ETH-A LR=145%, 1 ETH = 2000 USD, max 발행 = 2000/1.45 ≈ 1379 DAI.
- **Global Debt Ceiling**: 거버넌스 투표로 설정, 현재 ~2.4B DAI 한도.
- **PSM (Peg Stability Module)**: USDC ↔ DAI 1:1 즉시 교환, 0.1% 수수료, 가격페그 유지 메커니즘.

**(4) 오라클 (Chainlink)**
- `AggregatorV3Interface.latestRoundData()` -> `(roundId, answer, startedAt, updatedAt, answeredInRound)`
- **Heartbeat**: ETH/USD 1시간, BTC/USD 1시간, 빠른 페어는 1분
- **Deviation Threshold**: 가격 변동 ≥ 0.5% 시 새 라운드 트리거
- 가격 조작 방어를 위해 **TWAP (Time-Weighted Average Price)** 활용 권장, Uniswap V3의 `observe()`로 자체 오라클 구현 가능.

**(5) Flash Loan (Aave V3, Uniswap V3, dYdX)**
- 한 트랜잭션 내에서 `borrow -> use -> repay`를 atomic하게 실행, 실패 시 전체 revert.
- **활용 사례**: Collateral swap(부채 상환 없이 담보 교체), Self-liquidation(청산 페널티 회피), Arbitrage(CEX-DEX 차익).
- **Fee**: Aave 0.09%, Uniswap 0.3% (swap에 통합).

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Smart Contract (Solidity/Vyper ^0.8.20)** | 비즈니스 로직 실행, 상태 전이 | EVM opcode 실행, gas 최적화(bit-packing, custom errors), `unchecked` 블록 활용, Yul/Assembly로 hot-path 최적화 |
| **Token Standard (ERC-20/4626/3156)** | 자산·지분·대여 인터페이스 표준화 | ERC-4626 `convertToShares/convertToAssets/deposit/redeem` 표준화로 vault 통합성^, ERC-2612 `permit`으로 가스리스 승인 |
| **Oracle (Chainlink/Pyth/UMA)** | 오프체인 -> 온체인 가격 브릿지 | Chainlink OCR(Off-Chain Reporting) 2.0으로 다중 노드 p2p 합의, medianizer + outlier 필터, 8 decimals |
| **Governance (Governor + Timelock)** | 파라미터 변경, 업그레이드 통제 | OpenZeppelin Governor Bravo 변형, `quorum = 4%`, `voting delay=1 block`, `voting period=45818 blocks(7일)`, Timelock 48h |
| **Proxy / Upgradeability** | 버그 패치·기능 추가 | UUPS Proxy(EIP-1967, EIP-1822): logic 주소를 storage slot `0x360894…`에 저장, Transparent Proxy보다 gas v |
| **Liquidity Pool / Vault** | 자본 풀, 자산 custody | ERC-4626 Vault(Shares-Owner), Unbonded LP(UniV3 NFT-based), Bound(Convex), Rehypothecation 제한 |
| **Bridge / Cross-chain Messaging** | L1↔L2, L1↔L1 자산 이동 | Canonical Bridge(Arbitrum/Optimism 7일 챌린지), CCIP(Chainlink), LayerZero UltraLight Node, Wormhole Guardian |

### 핵심 보안 고려사항

1. **Reentrancy Attack**: `Checks-Effects-Interactions` 패턴 + `ReentrancyGuard` (mutex), `nonReentrant` modifier. The DAO(2016), Cream Finance(2021) 사례.
2. **Oracle Manipulation**: 단일 DEX spot price 사용 금지, 반드시 **TWAP(min 30분) + Chainlink 이중 검증**. Inverse Finance(2022) $1.6M 해킹 사례.
3. **Integer Overflow/Underflow**: Solidity 0.8+는 built-in revert이지만 `unchecked` 사용 시 주의.
4. **Front-running / MEV**: `block.builder`, `flashbots` private mempool, commit-reveal 스킴.
5. **Flash Loan Attack**: Price-dependent 로직에 단일 블록 의존 금지, 24h MA 활용.
6. **Storage Collision in Proxy**: EIP-7201 namespaced storage로 충돌 방지.

- **📢 섹션 요약 비유**: DeFi 프로토콜은 "투명한 유리 상자 안에서 돌아가는 시계"와 같다. 모든 톱니바퀴(컨트랙트)와 태엽(블록) 움직임이 모두에게 공개되지만, 한 번 조립되면 분해가 어려워 처음 설계 시 100% 검증이 필수다. 이 "유리 상자"가 바로 EVM의 결정론적 실행환경이다.

---

## Ⅲ. 비교 및 연결

|