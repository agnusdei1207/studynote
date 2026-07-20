---
title: "Zk Rollup Validity Proof"
date: "2026-04-05"
tags:
  - "studynote-ict-convergence"
weight: 44
---
> **핵심 인사이트**
> 1. ZK-Rollup(Zero-Knowledge Rollup)은 수천 건의 트랜잭션을 오프체인에서 처리하고 수학적 유효성 증명(zk-SNARK/zk-STARK)만 메인체인에 제출하는 Layer 2 확장 기술로 — 낙관적 롤업(Optimistic Rollup)과 달리 도전 기간 없이 즉시 최종성(Finality)을 달성한다.
> 2. ZK-Rollup의 핵심인 영지식 증명(ZKP — Zero-Knowledge Proof)은 "비밀을 공개하지 않고 비밀을 알고 있음을 증명"하는 암호학 기법으로 — 증명자(Prover)는 계산 결과만 공개하고 메인체인(검증자)은 수학적으로 검증하므로, 프라이버시와 확장성을 동시에 달성한다.
> 3. zk-SNARK(Succinct Non-interactive ARgument of Knowledge)는 증명 크기가 작고 검증이 빠르지만 신뢰된 셋업(Trusted Setup)이 필요한 반면 — zk-STARK(Scalable Transparent ARgument of Knowledge)는 신뢰된 셋업이 없어 투명하고 양자 내성이 있지만 증명 크기가 크다는 트레이드오프가 있다.

---

## Ⅰ. ZK-Rollup 개념

```
ZK-Rollup (Zero-Knowledge Rollup):

배경 — Ethereum 확장 문제:
  이더리움 메인넷: 15~30 TPS
  비자 카드: 24,000 TPS
  -> 확장성 문제

Layer 2 해결책:
  트랜잭션을 오프체인에서 처리
  결과만 메인체인에 기록

ZK-Rollup 동작:
  1. 사용자가 L2 시퀀서에 트랜잭션 제출
  2. 시퀀서가 수천 건 트랜잭션 묶음(Batch) 처리
  3. ZK 증명(Validity Proof) 생성 (계산 집약적)
  4. 배치 상태 + ZK 증명만 이더리움 메인넷에 게시
  5. 메인넷 스마트 컨트랙트가 증명 검증 (빠름)
  6. 검증 성공 -> 상태 확정 (즉시 최종성)

효과:
  1,000건 트랜잭션 -> 1개 ZK 증명
  가스비: 1,000배 절약
  처리량: ~3,000 TPS (zkEVM 기준)

대표 프로젝트:
  Polygon zkEVM, zkSync Era, StarkNet, Scroll

ZK-Rollup vs Optimistic Rollup:
  ZK: 즉시 최종성, 증명 생성 비용 높음
  Optimistic: 7일 대기 기간, 사기 증명 필요
  -> ZK가 이론적으로 더 우수 (복잡성이 단점)
```

> 📢 **섹션 요약 비유**: ZK-Rollup은 회계 감사 요약 — 1만 건 거래 장부를 보내는 대신, 수학적 증명서 하나로 "모든 거래가 정확하다"를 증명. 장부 없이 도장(ZK 증명)만으로 신뢰.

---

## Ⅱ. 영지식 증명 (ZKP)

```
영지식 증명 (ZKP — Zero-Knowledge Proof):

개념:
  증명자(Prover): 비밀 정보 알고 있음
  검증자(Verifier): 비밀 모름

  ZKP: 비밀을 공개하지 않고 "알고 있음"을 수학적 증명

  3가지 속성:
  1. 완전성(Completeness): 진실이면 검증자 확신
  2. 건전성(Soundness): 거짓이면 속일 수 없음
  3. 영지식성(Zero-Knowledge): 비밀 정보 노출 없음

직관적 예시 — 색깔 맹인과 공:
  Alice: 빨간 공, 초록 공 보유 (빨간 = 비밀)
  Bob (색맹): 두 공 구별 불가

  ZKP: Bob이 등 뒤에서 공 교체 or 유지
  Alice: 교체 여부 맞춤 (색으로 판단)

  100번 반복 -> 모두 맞추면:
  Alice가 실제 색 구별한다는 것을 증명
  Bob은 Alice가 빨강/초록 어느 것인지 여전히 모름

블록체인 응용:
  계산: 1000건 트랜잭션 처리 정확성
  증명: "모든 트랜잭션이 유효하다" (수식으로)

  메인넷: 수식만 검증 -> 빠르고 저렴
  개별 트랜잭션 검증 불필요
```

> 📢 **섹션 요약 비유**: ZKP는 정답만 아는 증명 — 수학 문제 정답지 없이 "내가 풀었다"를 증명하는 것. 풀이 과정(비밀)은 안 보여줘도 되고, 결과(증명)만으로 신뢰를 줘요.

---

## Ⅲ. zk-SNARK vs zk-STARK

```
zk-SNARK (Succinct Non-interactive ARgument of Knowledge):

특징:
  Succinct: 증명 크기 매우 작음 (수백 바이트)
  Non-interactive: 단방향 (증명자 -> 검증자)
  ARgument: 계산 가정 하에 건전성
  Knowledge: 비밀 지식 증명

장점:
  증명 크기 작음 -> 온체인 가스비 저렴
  검증 빠름

단점:
  Trusted Setup (신뢰된 셋업) 필요
  특수 파라미터 생성 행사 필요
  파라미터 생성 참여자가 결탁하면 보안 취약
  -> "독성 폐기물 (Toxic Waste)" 문제

  양자 컴퓨터 취약 (Elliptic Curve 기반)

대표: Groth16 (Zcash), PLONK (zkSync)

zk-STARK (Scalable Transparent ARgument of Knowledge):

특징:
  Scalable: 증명 크기 O(log^n) 스케일
  Transparent: Trusted Setup 불필요
  ARgument of Knowledge: 같음

장점:
  Trusted Setup 없음 -> 완전 투명
  양자 내성 (해시 함수 기반)

단점:
  증명 크기 큼 (수십~수백 KB)
  -> 온체인 비용 높음

비교:

항목       | zk-SNARK        | zk-STARK
-----------|-----------------|------------------
증명 크기  | ~200 바이트     | ~수십 KB
검증 속도  | 빠름            | 느림
셋업       | Trusted Setup   | 투명, 불필요
양자 내성  | 없음            | 있음
가스비     | 저렴            | 높음

대표: StarkNet (이더리움 L2), StarkEx (dYdX)
```

> 📢 **섹션 요약 비유**: SNARK vs STARK는 작고 비밀스러운 vs 크고 투명한 — SNARK는 수납 쪽지(작지만 신뢰 세팅 필요), STARK는 공개 회의록(크지만 누구나 신뢰 가능).

---

## Ⅳ. ZK-Rollup 생태계

```
ZK-Rollup 프로젝트 현황:

1. zkSync Era (Matter Labs):
   zkEVM 타입 3 (EVM 호환)
   zk-SNARK + PLONK 증명 시스템
   TVL: 수억 달러 규모

2. Polygon zkEVM:
   타입 2 zkEVM (완전 EVM 등가)
   기존 이더리움 도구 100% 호환

3. StarkNet (StarkWare):
   zk-STARK 기반
   Cairo 언어 (전용 회로 언어)
   dYdX DEX에서 StarkEx 사용

4. Scroll:
   오픈소스 zkEVM
   바이트코드 호환 (타입 2)

zkEVM 타입:
  타입 1: 이더리움 완전 동일 (증명 매우 느림)
  타입 2: EVM 등가, 약간 수정
  타입 3: EVM 호환, 일부 차이
  타입 4: 고급 언어 호환 (Solidity 등)

ZK 증명 생성 비용:
  GPU 집중적 (ZK 증명 생성 = 행렬 연산 집약)
  NVIDIA A100 GPU 클러스터 필요

  최적화 방향:
  - FPGA/ASIC 가속기 (ZK 증명 전용 하드웨어)
  - 재귀 증명 (Proof Aggregation)
  - 병렬화

응용 확장:
  ZK 신원 증명: 나이 증명 (숫자 공개 없이)
  ZK ML: 모델 추론 결과 증명 (가중치 비공개)
  ZK 투표: 무기명 투표 정확성 증명
```

> 📢 **섹션 요약 비유**: ZK-Rollup 생태계는 고속도로 요금소 — 이더리움 메인넷이 막힌 도로라면, ZK-Rollup은 옆에 새로 낸 고속 우회로. 요금은 증명 비용(GPU), 속도는 훨씬 빠름.

---

## Ⅴ. 실무 시나리오 — ZK-Rollup DEX

```
ZK-Rollup 기반 탈중앙화 거래소 (DEX):

사례: dYdX v4 (StarkEx 기반)

기존 이더리움 DEX 문제:
  Uniswap v3 (메인넷 직접):
  - 스왑 1건 = 가스비 약 $10~50
  - 블록 확인 시간: ~15초
  - 초당 처리: 15 TPS

StarkEx ZK-Rollup 해결:
  처리 방식:
  1. 사용자 -> dYdX API: 주문 제출
  2. StarkEx 시퀀서: 수천 건 주문 배치 처리
  3. zk-STARK 증명 생성 (오프체인, GPU)
  4. 증명 + 상태 루트만 이더리움 게시
  5. 검증 스마트 컨트랙트: 증명 확인
  6. 즉시 최종성

성능:
  처리량: ~10,000 TPS
  가스비: $0.001 이하/거래 (1000배 절약)
  최종성: 수분 (이더리움 레이어 증명 확인 후)

자금 인출:
  ZK 증명 기반: 즉시 인출 가능
  (Optimistic Rollup은 7일 대기)

보안 모델:
  이더리움 메인넷이 최종 검증자
  StarkEx 운영자가 도망가도 데이터 가용성 보장
  사용자는 메인넷으로 직접 자산 복구 가능

ZK-Rollup의 미래:
  이더리움 로드맵: "The Surge" = ZK-Rollup 100,000 TPS
  ZK 증명 생성 비용 감소 추세
  -> 2025~2027년 주류 L2 기술로 자리잡을 전망
```

> 📢 **섹션 요약 비유**: dYdX ZK-DEX는 초고속 거래 창구 — 수천 건 주문을 모아서 수학 증명 도장 하나로 이더리움에 제출. 개별 확인 없이 도장 하나로 모두 인정받아요!

---

## 📌 관련 개념 맵

```
ZK-Rollup
+-- 핵심 기술
|   +-- 영지식 증명 (ZKP)
|   +-- zk-SNARK (작은 증명, Trusted Setup)
|   +-- zk-STARK (투명, 양자 내성)
+-- 비교
|   +-- Optimistic Rollup (사기 증명, 7일 대기)
|   +-- ZK-Rollup (유효성 증명, 즉시 확정)
+-- 프로젝트
|   +-- zkSync, Polygon zkEVM, StarkNet, Scroll
+-- 응용
|   +-- DEX, ZK 신원 증명, ZK ML
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[영지식 증명 개념 (1985)]
Goldwasser, Micali, Rackoff 논문
이론적 기반 확립
      |
      v
[zk-SNARK 실용화 (2012~)]
Groth16 알고리즘
Zcash 프라이버시 코인 적용
      |
      v
[이더리움 L2 탄생 (2018~)]
Plasma -> Optimistic Rollup -> ZK-Rollup
StarkEx dYdX 런칭 (2020)
      |
      v
[zkEVM 경쟁 (2022~)]
zkSync Era, Polygon zkEVM
zk-STARK 성능 개선
      |
      v
[현재: 주류 L2]
이더리움 로드맵 ZK 중심
ZK 증명 하드웨어 가속기 등장
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ZK-Rollup은 수학 도장 — 수천 건 거래를 모아서 "다 맞아요!"라는 수학 증명 도장 하나만 이더리움에 찍어요. 훨씬 저렴하고 빨라요!
2. 영지식 증명은 비밀 없는 증명 — "나 이 문제 풀었어" 라고 풀이 없이 증명하는 것. 비밀은 지키면서 신뢰는 얻을 수 있어요!
3. SNARK는 작고 STARK는 투명 — SNARK는 납작한 증명서(작지만 사전 준비 필요), STARK는 큰 공개 증명서(크지만 누구나 믿을 수 있음).
