---
title: "Layer 2 Scaling Solution"
date: "2026-03-19"
tags:
  - "studynote-ict-convergence"
weight: 41
---
> **핵심 인사이트**
> 1. 레이어 2(L2) 솔루션은 블록체인 트릴레마를 우회하는 핵심 전략으로, 메인체인(L1) 밖에서 트랜잭션을 처리하고 최종 결과만 L1에 기록하여 L1의 보안성을 상속하면서 확장성을 수십~수천 배 향상시킨다.
> 2. Optimistic Rollup(낙관적 롤업)과 ZK-Rollup(영지식 롤업)이 L2의 양대 주류로, Optimistic은 구현이 간단하지만 7일 분쟁 기간이 있고, ZK-Rollup은 즉시 검증 가능하지만 영지식 증명 생성 비용이 높아 복잡한 연산에는 한계가 있다.
> 3. 2024년 기준 Arbitrum·Optimism(Optimistic Rollup)과 zkSync·StarkNet(ZK-Rollup)이 이더리움 L2 TVL(Total Value Locked)의 90% 이상을 차지하며, L2가 블록체인 생태계의 새로운 전장이 됐다.

---

## Ⅰ. L2 솔루션 분류

```
레이어 2 스케일링 전략:

1. Rollup (롤업):
   트랜잭션 묶음 처리 + L1에 압축 데이터 기록

   Optimistic Rollup:
     낙관적으로 처리 후 분쟁 제기 기간
     Arbitrum, Optimism

   ZK-Rollup (Zero-Knowledge):
     영지식 증명으로 유효성 즉시 검증
     zkSync, StarkNet, Polygon zkEVM

2. State Channel (상태 채널):
   두 당사자 간 Off-chain 채널 개설
   최종 상태만 L1 기록
   비트코인 Lightning Network

3. Plasma:
   사이드체인 + 주기적 L1 커밋
   폐기 가능성 검토됨 (데이터 가용성 문제)

4. Validium:
   ZK 증명 + Off-chain 데이터 저장
   높은 처리량, 낮은 비용, 데이터 가용성 절충
```

> 📢 **섹션 요약 비유**: L2 솔루션은 고속도로 하이패스 — 요금소(L1)를 통과하는 차량 수는 줄이고, 하이패스 차선(L2)으로 빠르게 처리.

---

## Ⅱ. Optimistic Rollup

```
Optimistic Rollup 동작:

원리: "낙관적으로 처리 (유효하다고 가정)"
  트랜잭션을 묶어서 처리
  처리 결과(State Root)를 L1에 게시
  7일 챌린지 기간: 누구든 사기 증명 제출 가능

처리 흐름:
  사용자 -> L2 Sequencer (트랜잭션 처리)
  Sequencer -> L1 (배치 커밋, 압축 calldata)
  검증자: 배치 검토 -> 사기 발견 시 챌린지
  7일 후 이의 없음 -> 최종 확정

장점:
  EVM 호환성 높음 (기존 Ethereum 앱 그대로 이식)
  구현 상대적으로 간단

단점:
  인출 대기: 7일 (L2 -> L1 자금 이동)
  사기 증명 비용 (챌린저 필요)

대표:
  Arbitrum One (TVL 1위, EVM 완전 호환)
  Optimism (OP Stack, Coinbase Base 기반)
```

> 📢 **섹션 요약 비유**: Optimistic Rollup은 온라인 경매 7일 환불 정책 — 판매자는 즉시 결제 수령, 구매자는 7일 내 사기 신고 가능.

---

## Ⅲ. ZK-Rollup

```
ZK-Rollup (Zero-Knowledge Rollup):

원리:
  모든 트랜잭션 처리 후 유효성 증명(Validity Proof) 생성
  L1에 증명 제출 -> 즉시 검증 완료

ZK 증명 유형:
  SNARK (Succinct Non-interactive ARgument of Knowledge):
    증명 크기 매우 작음, 검증 빠름
    Groth16, PLONK

  STARK (Scalable Transparent ARgument of Knowledge):
    신뢰 설정 불필요, 더 큰 증명 크기
    StarkNet 사용

장점:
  즉시 인출 (7일 기다림 없음)
  더 강한 보안 보장 (수학적 증명)

단점:
  EVM 호환 어려움 (zkEVM 개발로 개선 중)
  증명 생성 비용 높음 (GPU/ASIC 필요)
  개발 복잡성

대표:
  zkSync Era (EVM 호환 zkEVM)
  StarkNet (Cairo 언어, STARKs)
  Polygon zkEVM
  Linea (Consensys)
```

> 📢 **섹션 요약 비유**: ZK-Rollup은 수학 시험 답안지 + 채점 기준표 동시 제출 — 선생님이 즉시 맞는지 확인 가능, 7일 기다림 없음.

---

## Ⅳ. State Channel

```
State Channel (상태 채널):

동작:
  1. L1에 채널 개설 (보증금 예치)
  2. 두 당사자 간 Off-chain 무제한 거래
  3. 최종 상태만 L1에 기록 (채널 닫기)

Lightning Network (비트코인):
  수백만 채널 연결된 네트워크
  경로 라우팅으로 직접 채널 없어도 전송
  수수료 매우 낮음 (0.001% 이하)
  즉시 결제 (0.1초 이내)

한계:
  두 당사자만 가능 (스마트 컨트랙트 복잡)
  채널 개설/닫기 비용
  온라인 유지 필요 (감시자 필요)

사용 케이스:
  마이크로페이먼트 (커피값 결제)
  게임 내 즉시 거래
  IoT 기기 간 마이크로 결제
```

> 📢 **섹션 요약 비유**: State Channel은 친구와 술집 외상 — 매번 카드 긁지 않고 나갈 때 총 한 번 계산.

---

## Ⅴ. 실무 시나리오 — DeFi L2 선택

```
DeFi 프로토콜 L2 선택 기준 (2024):

프로토콜 A (DEX, 소규모 거래 많음):
  요구: 낮은 가스비, 빠른 처리
  선택: Arbitrum One
    이유: EVM 호환 100%, TVL 1위, 생태계 풍부
          가스비 이더리움의 1/20~1/50

프로토콜 B (고빈도 거래 플랫폼):
  요구: 초고속, 매우 낮은 지연
  선택: StarkNet
    이유: STARKs 고성능, 배치 처리 우수

프로토콜 C (NFT 마켓플레이스):
  요구: 빠른 인출, 높은 보안
  선택: zkSync Era
    이유: ZK-Rollup 즉시 인출
          이더리움 보안 완전 상속

L2 상호운용성 문제:
  L2 간 직접 이동 불편 (L1 거쳐야 함)
  해결 시도: 크로스체인 브리지
             LayerZero, Axelar

미래: L3 (L2 위의 L3)
  게임/앱 특화 체인
  더 높은 처리량, 더 낮은 비용
```

> 📢 **섹션 요약 비유**: DeFi L2 선택은 물류 창고 위치 결정 — 비용(가스비), 속도(처리량), 안전(보안) 중 무엇이 가장 중요한지에 따라 결정.

---

## 📌 관련 개념 맵

```
레이어 2 스케일링 솔루션
+-- 유형
|   +-- Optimistic Rollup (Arbitrum, Optimism)
|   +-- ZK-Rollup (zkSync, StarkNet)
|   +-- State Channel (Lightning)
|   +-- Validium
+-- 비교
|   +-- 인출 대기: Optimistic(7일) vs ZK(즉시)
|   +-- EVM 호환: Optimistic(높음) vs ZK(개선 중)
+-- 이론
|   +-- 블록체인 트릴레마 우회
|   +-- ZK 증명 (SNARK, STARK)
+-- 현황
    +-- L2 TVL 이더리움 생태계 핵심
    +-- L3 (앱 특화 체인) 부상
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[블록체인 트릴레마 인식 (2017~)]
이더리움 확장성 문제 본격화
      |
      v
[Plasma (2017)]
초기 L2 시도, 데이터 가용성 문제
      |
      v
[State Channel / Lightning (2018)]
비트코인 L2 실용화
      |
      v
[Optimistic Rollup (2019~)]
Arbitrum, Optimism 출시
      |
      v
[ZK-Rollup 성숙 (2021~)]
zkSync, StarkNet 메인넷
      |
      v
[현재: L2 생태계 경쟁]
Arbitrum, Base, zkSync Era
L3 (앱 체인) 등장
이더리움 L1 -> L2 트래픽 이동
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. L2는 바쁜 고속도로(이더리움) 옆에 하이패스 전용 차선을 만드는 것 — 빠르고 저렴하게 통과하고, 최종 결과만 고속도로에 기록해요.
2. Optimistic Rollup은 "일단 OK, 7일 내 이의 제기 가능"이고, ZK-Rollup은 "수학 증명으로 즉시 OK 확인"이에요.
3. 덕분에 이더리움에서 1달러 거래 수수료가 0.01달러로 줄어들어서 소액 결제도 가능해졌어요!
