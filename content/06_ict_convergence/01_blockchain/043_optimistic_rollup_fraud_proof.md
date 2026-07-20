---
title: "Optimistic Rollup & Fraud Proof"
date: "2026-04-05"
tags:
  - "studynote-ict-convergence"
weight: 43
---
> **핵심 인사이트**
> 1. 옵티미스틱 롤업(Optimistic Rollup)은 "일단 믿고, 문제 있으면 증명"하는 낙관적 가정으로 설계된 이더리움 Layer 2 확장 솔루션으로 — ZK 롤업과 달리 트랜잭션 유효성 증명을 즉시 생성하지 않아 가스 비용이 낮지만, 출금 시 7일 이의제기 기간(Challenge Period)이 발생한다.
> 2. 사기 증명(Fraud Proof)은 "시퀀서가 잘못된 상태 전이를 제출했다"고 누군가 증명하면 해당 배치가 롤백되는 메커니즘으로 — 이의제기자에게 보상을 주어 감시 인센티브를 만들고 시퀀서에게 슬래시(Slash) 패널티를 부과한다.
> 3. Optimism(OP Stack)과 Arbitrum이 양대 옵티미스틱 롤업 구현체이며 — OP Stack의 오픈소스화로 Base(Coinbase), Zora, Mantle 등 수십 개의 Layer 2 체인이 동일한 스택으로 구축되는 "Superchain" 생태계가 형성되고 있다.

---

## Ⅰ. 옵티미스틱 롤업 개념

```
롤업 (Rollup) 원리:
  대량 트랜잭션을 L2(Layer 2)에서 실행
  -> 실행 결과(상태 루트)만 L1(이더리움 메인넷)에 제출
  -> L1 데이터 가용성 활용 + L1 실행 비용 절감

옵티미스틱 (Optimistic) 의미:
  "트랜잭션이 유효하다고 낙관적으로 가정"
  즉시 유효성 검증 없이 상태 전이 수용

  vs ZK 롤업:
    ZK: 매 배치마다 유효성 증명(zk-proof) 생성 및 검증
    Optimistic: 7일 이의제기 기간 동안 누가 문제 제기하지 않으면 확정

구조:
  시퀀서 (Sequencer):
    L2 트랜잭션 수집 및 순서 결정
    배치 상태 루트를 L1에 제출

  L1 계약 (Rollup Contract):
    배치 데이터 저장 (calldata or blob)
    상태 루트 기록
    이의제기 처리

  이의제기자 (Challenger):
    배치 데이터를 재실행하여 검증
    오류 발견 시 사기 증명 제출

흐름:
  L2 트랜잭션 -> 시퀀서 -> 배치 압축 -> L1 제출
                                              v
                                    7일 이의제기 기간
                                              v
                                    이의 없음 -> 최종 확정
```

> 📢 **섹션 요약 비유**: 옵티미스틱 롤업은 선불 여행 정산 — 회사 출장비를 먼저 쓰고(L2 실행), 나중에 영수증 제출(L1 제출). 7일 내 문제 제기 없으면 확정.

---

## Ⅱ. 사기 증명 메커니즘

```
사기 증명 (Fraud Proof) 단계:

1. 시퀀서의 잘못된 상태 전이 제출:
   배치 번호 100: 상태루트 WRONG_ROOT 제출
   (실제 올바른 상태루트: CORRECT_ROOT)

2. 이의제기자가 오류 발견:
   배치 데이터 다운로드 (L1 calldata/blob)
   자체 실행 결과: CORRECT_ROOT
   시퀀서 제출: WRONG_ROOT
   -> 불일치 탐지!

3. 이의제기 (Challenge) 제출:
   L1 Rollup 계약에 이의제기 트랜잭션 발송
   경쟁적 게임 시작

4. 인터랙티브 이분 게임 (Arbitrum 방식):
   "배치 내 어느 트랜잭션이 잘못됐나?"를 절반씩 좁힘
   최종적으로 단일 트랜잭션 오류 특정
   L1에서 해당 트랜잭션만 재실행 (저비용)

5. 판정:
   시퀀서 잘못 -> 상태 롤백, 시퀀서 슬래시(Slash)
   이의제기 잘못 -> 이의제기자 보증금 몰수

인센티브 설계:
  이의제기자: 성공 시 보상 (시퀀서 슬래시 일부)
  시퀀서: 허위 제출 시 본딩(Bonding) 자산 몰수
  -> 게임이론적 균형: 시퀀서가 정직하게 행동하도록 유도

이의제기 기간:
  Optimism: 7일
  Arbitrum: 7일
  이유: 이더리움 이클립스 공격 방어 시간 필요
```

> 📢 **섹션 요약 비유**: 사기 증명은 법원 항소 시스템 — 판결(상태 제출) 후 7일 안에 이의신청(Fraud Proof) 가능. 이의가 타당하면 판결 취소, 아니면 확정.

---

## Ⅲ. Optimism vs Arbitrum

```
비교:

항목              | Optimism (OP Stack)     | Arbitrum One
------------------+-------------------------+--------------------
사기 증명         | 단일 라운드 (Non-interactive) | 인터랙티브 이분 게임
가스 비용         | 유사                    | 약간 저렴
EVM 호환성        | 100% EVM 동일           | EVM 동일 (Arbitrum Stylus)
스택 오픈소스     | OP Stack (MIT 라이선스) | BOLD (사기 증명 개선)
체인 생태계       | Superchain (Base, Zora) | Arbitrum Orbit
TVL (2025)       | ~$8B                    | ~$15B
출금 시간         | 7일                     | 7일

Optimism OP Stack:
  OP Mainnet: 최초 배포
  Base (Coinbase): OP Stack 기반
  Zora: NFT 특화 OP Stack 체인
  Mantle: OP Stack 변형

Arbitrum:
  Arbitrum One: 범용 L2
  Arbitrum Nova: 게임/소셜 (AnyTrust, 낮은 비용)
  Arbitrum Orbit: OP Stack처럼 자체 체인 구축 프레임워크

공통점:
  EVM 호환
  이더리움 데이터 가용성 활용
  7일 이의제기 기간
  Bridging 인터페이스 제공
```

> 📢 **섹션 요약 비유**: Optimism vs Arbitrum은 두 제조사의 동일 규격 TV — 화면은 똑같이 잘 나오지만 내부 작동 방식(사기 증명 구현)이 달라요. Optimism은 삼성, Arbitrum은 LG.

---

## Ⅳ. ZK 롤업과의 비교

```
Optimistic vs ZK Rollup:

항목            | Optimistic Rollup     | ZK Rollup
----------------+-----------------------+---------------------
유효성 검증     | 이의제기 기간 (사후)  | 즉시 (zk-proof)
출금 지연       | 7일                   | 수십 분~수 시간
EVM 호환성      | 100% (간단)           | zkEVM 필요 (복잡)
계산 비용       | 시퀀서 낮음           | 증명 생성 비용 높음
보안 모델       | 최소 1명의 정직한 검증자 | 암호학적 보안 (수학적)
현재 TVL        | 더 높음               | 성장 중

Optimistic 롤업 주요 위험:
  1. 시퀀서 검열: 시퀀서가 특정 트랜잭션 제외 가능
     대응: L1 Force Include (이더리움으로 강제 포함)

  2. 이의제기 활성화 가정: 아무도 감시 안 하면?
     대응: Watchers (자동 감시 봇)

  3. 7일 유동성 잠금:
     대응: 브리지 유동성 공급자 (즉시 출금 + 수수료)

ZK 롤업 확산:
  zkSync Era, Polygon zkEVM, Scroll, StarkNet
  "ZK > Optimistic" 장기 전망 (Vitalik)
  하지만 단기: Optimistic 더 높은 TVL/활동성
```

> 📢 **섹션 요약 비유**: Optimistic vs ZK는 신용 대출 vs 담보 대출 — Optimistic은 일단 믿어줌(낙관적, 빠름), ZK는 담보 증명 필요(느리지만 확실). 장기 추세는 ZK로 이동 중.

---

## Ⅴ. 실무 시나리오 — Base 체인 DApp 배포

```
OP Stack 기반 Base 체인 DApp 배포:

Base 개요:
  Coinbase 운영, OP Stack 기반
  이더리움 L2, TVL ~$5B (2025)
  수수료: 이더리움의 1/50~1/100 수준

DApp 배포 단계:
  1. 계약 배포:
     이더리움 mainnet 계약 -> Base에 그대로 배포
     (EVM 100% 호환)

     forge deploy --rpc-url https://mainnet.base.org

  2. 브리징:
     ETH -> Base ETH (7일 출금 지연)
     또는 CEX(Coinbase) 직접 출금으로 즉시 획득

  3. 사용자 경험:
     가스비: ~$0.01~$0.10 (이더리움 $3~$50 대비)
     처리량: ~2,000 TPS (이더리움 ~15 TPS)

EIP-4844 (Proto-Danksharding) 영향:
  2024년 이더리움 업그레이드
  Blob 데이터: calldata 대비 10~100배 저렴
  -> Optimistic 롤업 수수료 추가 80~90% 감소

  Base, Optimism, Arbitrum 모두 즉시 적용
  결과: 평균 L2 거래 수수료 $0.001~$0.01 수준

미래: EIP-4844 -> Full Danksharding
  수백 개 Blob/블록 -> 롤업 비용 거의 0
  "롤업 중심의 이더리움 로드맵" 실현
```

> 📢 **섹션 요약 비유**: Base/OP Stack은 이더리움의 고속도로 톨게이트 절감 — 원래 1만 원 톨비(이더리움 가스)를 100원(L2)으로 줄여주는 빠른 우회 도로.

---

## 📌 관련 개념 맵

```
옵티미스틱 롤업
+-- 핵심 메커니즘
|   +-- 낙관적 가정 (사전 증명 없음)
|   +-- 7일 이의제기 기간
|   +-- 사기 증명 (Fraud Proof)
+-- 구현체
|   +-- Optimism / OP Stack
|   +-- Arbitrum (인터랙티브 이분 게임)
+-- 비교
|   +-- vs ZK 롤업 (암호학적 즉시 증명)
+-- 인프라
|   +-- EIP-4844 Blob 데이터
|   +-- Superchain (OP 생태계)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[이더리움 확장성 문제 (2017~)]
CryptoKitties로 네트워크 마비
가스비 급등, TPS 한계
      |
      v
[롤업 제안 (2018~)]
Plasma -> 데이터 가용성 문제
Rollup 개념 등장 (Vitalik)
      |
      v
[Optimism 베타 출시 (2021)]
Synthetix, Uniswap 이주
사기 증명 메커니즘 실전 검증
      |
      v
[Arbitrum One 출시 (2021)]
인터랙티브 이분 게임 방식
더 낮은 가스비로 빠른 성장
      |
      v
[OP Stack 오픈소스 + Base 출시 (2023)]
Superchain 생태계 형성
EIP-4844로 수수료 대폭 감소
      |
      v
[현재: ZK vs Optimistic 경쟁]
ZK 기술 성숙 -> 점진적 대체 가능성
단기: Optimistic이 높은 TVL/생태계 유지
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 옵티미스틱 롤업은 "일단 믿어주는 빠른 계산기" — 수천 개 거래를 묶어서 이더리움에 제출하고, 7일 동안 아무도 문제 제기 안 하면 확정이에요!
2. 사기 증명은 법원 항소 — 계산이 틀렸다고 생각하면 증거를 들고 법원(스마트 계약)에 가면 돼요. 맞으면 보상, 틀리면 내 돈 몰수.
3. Base(Coinbase)가 이 방식으로 만들어져 이더리움보다 100배 저렴하게 거래할 수 있어요!
