---
title: "Rollup L2 Solution"
date: "2026-04-05"
tags:
  - "studynote-ict-convergence"
weight: 42
---
> **핵심 인사이트**
> 1. 롤업(Rollup)은 수천 개의 트랜잭션을 오프체인(Layer 2)에서 처리하고 압축·묶어서 Layer 1 메인넷에 하나의 배치로 제출하는 L2 스케일링 솔루션으로, 이더리움의 TPS 한계(15 TPS)를 100~10,000 TPS로 대폭 향상시킨다.
> 2. 롤업은 보안 증명 방식에 따라 Optimistic Rollup(사기 증명, 7일 인출 지연)과 ZK Rollup(유효성 증명, 즉시 완결성)으로 분류되며, Optimistic은 개발 용이성, ZK는 더 강한 보안성과 빠른 완결성이 트레이드오프다.
> 3. Vitalik Buterin이 제안한 이더리움 로드맵의 핵심은 "롤업 중심 세계(Rollup-Centric Roadmap)"로, 이더리움 L1은 데이터 가용성(DA Layer) 역할을 하고 실제 트랜잭션은 L2 롤업에서 처리하는 구조로 진화하고 있다.

---

## Ⅰ. 롤업 기본 원리

```
롤업 (Rollup) 작동 원리:

[사용자 트랜잭션] x 수천 개
      v L2 Sequencer에서 수집
[L2에서 실행 및 상태 업데이트]
      v 압축·묶음 처리
[압축된 배치 데이터]
      v L1 스마트 컨트랙트에 제출
[L1 이더리움 메인넷]
  - 데이터 가용성 보장
  - 스테이트 루트 기록
  - 최종 분쟁 해결 (Optimistic)
  - 유효성 증명 검증 (ZK)

롤업의 핵심 이점:
  가스비: L1 대비 10~100배 저렴
  TPS: 이더리움 15 TPS -> 롤업 1,000~10,000 TPS
  보안: L1 이더리움 보안 상속

L1 vs L2 vs 사이드체인:
  L1: 메인넷 (이더리움, 비트코인) — 최고 보안
  L2: L1 보안 활용 (롤업) — 빠름
  사이드체인: 독립 체인 — 빠르지만 L1 보안 미상속
```

> 📢 **섹션 요약 비유**: 롤업은 택배 묶음 배송 — 개별 배송(L1 직접) 대신 수천 개 상자를 하나의 컨테이너(롤업 배치)로 묶어 배송.

---

## Ⅱ. Optimistic Rollup vs ZK Rollup

```
롤업 두 가지 유형:

Optimistic Rollup:
  원리: "일단 믿고 처리, 문제 있으면 이의 제기"
  증명: 사기 증명 (Fraud Proof)
  인출 지연: 7일 (챌린지 기간 대기)
  EVM 호환성: 높음 (기존 코드 그대로)
  대표: Optimism, Arbitrum, Base

ZK Rollup:
  원리: "수학적으로 정확함 증명 후 L1 제출"
  증명: 유효성 증명 (ZK-SNARK/STARK)
  인출 지연: 수십 분 ~ 수 시간 (즉시 완결성)
  EVM 호환성: 낮음 (zkEVM 개발 중)
  대표: zkSync, StarkNet, Polygon zkEVM

비교:
  항목           | Optimistic    | ZK
  ---------------|---------------|-------------------
  보안 모델      | 사기 증명     | 수학적 유효성 증명
  인출 지연      | 7일           | 수 시간 이내
  개발 용이성    | 높음(EVM호환) | 낮음(zkEVM 필요)
  처리 비용      | 낮음          | 높음(증명 생성)
  장기 전망      | 단기 주도     | 장기 우위
```

> 📢 **섹션 요약 비유**: Optimistic은 신뢰 후 반박 — "일단 OK, 7일 내 이의 없으면 확정". ZK는 수학 시험 — "증명서 먼저 제출, 맞으면 즉시 확정".

---

## Ⅲ. 데이터 가용성

```
데이터 가용성 (Data Availability):

방식 1: On-chain DA (완전 롤업):
  모든 L2 트랜잭션 데이터 -> L1 calldata 게시
  안전: L1 보안 = 데이터 가용성 완전 보장
  단점: L1 calldata 비용 높음

방식 2: Off-chain DA (Validium):
  트랜잭션 데이터 L1 외부 저장
  증명만 L1 제출
  장점: 훨씬 저렴, 빠름
  단점: 데이터 가용성 위험

EIP-4844 (Proto-Danksharding):
  이더리움 칸쿤 업그레이드 (2024년 3월)
  "blob" 데이터 타입 추가
  롤업 calldata 비용 10~100배 감소
  -> L2 가스비 대폭 하락

궁극적 목표: Full Danksharding
  이더리움 L1 = DA Layer 최적화
  롤업 = 실행 레이어
```

> 📢 **섹션 요약 비유**: 데이터 가용성은 회계 장부 공개 여부 — L1 calldata = 공개 장부, Validium = 내부 장부 (빠르지만 외부 감사 불가).

---

## Ⅳ. 주요 롤업 프로젝트

```
주요 L2 롤업 프로젝트 (2025년):

Arbitrum (Optimistic):
  TVL: 이더리움 L2 최대
  특징: Nitro 업그레이드, 빠른 EVM

Optimism / Base (Optimistic):
  OP Stack: 표준화된 L2 구축 도구
  Base: Coinbase 운영 L2 (OP Stack)
  Superchain 비전: 여러 L2 상호운용

zkSync Era (ZK):
  EVM 호환 zkEVM
  Account Abstraction 기본 지원

StarkNet (ZK):
  Cairo 언어 (ZK 최적화)
  STARK 증명 (양자 내성)

Polygon zkEVM (ZK):
  이더리움 EVM 동등성(equivalence) 목표

TVL 순위 (2025년 초):
  1위: Arbitrum
  2위: Base
  3위: Optimism
  4위: zkSync Era
  5위: StarkNet
```

> 📢 **섹션 요약 비유**: 롤업 경쟁은 스마트폰 OS 경쟁 — Optimistic(Android, 넓은 호환성) vs ZK(iOS, 더 강한 보안/성능).

---

## Ⅴ. 실무 시나리오 — DeFi L2 마이그레이션

```
DeFi DEX L2 마이그레이션 사례:

배경:
  이더리움 L1 기반 DEX
  가스비: 거래당 $20~$50
  사용자 이탈 (높은 가스비)

Arbitrum 선택 이유:
  EVM 호환성 (코드 수정 최소)
  L2 생태계 TVL 1위

마이그레이션 과정 (3주):
  스마트 컨트랙트 Arbitrum 배포
  유동성 브릿지 설정 (L1↔L2)
  프론트엔드 L2 RPC 연결 변경

결과 (3개월 후):
  가스비: $30 -> $0.10~$0.30 (99% 감소)
  TPS: 300~500 TPS 처리 가능
  일일 거래량: 3배 증가
  사용자 수: 2.5배 증가

교훈:
  EVM 호환 Optimistic Rollup = 빠른 마이그레이션
  브릿지 보안 리스크 별도 관리 필요
```

> 📢 **섹션 요약 비유**: DEX L2 마이그레이션은 고속도로 개통 — L1 국도(비싸고 느림) -> L2 고속도로(싸고 빠름)로 이전하니 교통량 급증.

---

## 📌 관련 개념 맵

```
롤업 (Rollup)
+-- 유형
|   +-- Optimistic Rollup (사기 증명, 7일)
|   +-- ZK Rollup (유효성 증명, 빠름)
+-- 핵심 개념
|   +-- 데이터 가용성 (On-chain/Off-chain)
|   +-- EIP-4844 (Blob, 가스비 절감)
+-- 주요 프로젝트
|   +-- Arbitrum, Base, Optimism
|   +-- zkSync, StarkNet, Polygon zkEVM
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[이더리움 확장성 문제 (2017~)]
CryptoKitties 가스비 폭등
L2 스케일링 연구 시작
      |
      v
[롤업 개념 정립 (2019~2020)]
Optimistic/ZK Rollup 이론화
      |
      v
[Arbitrum, Optimism 메인넷 (2021)]
L2 TVL 수십억 달러 성장
      |
      v
[EIP-4844 칸쿤 업그레이드 (2024)]
Blob 데이터로 L2 가스비 급감
      |
      v
[현재: Full Danksharding 로드맵]
이더리움 = DA Layer 전문화 진행
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 롤업은 편지 1만 장을 하나의 소포로 묶어 보내는 것 — 개별 배송(L1 직접)보다 훨씬 싸고 빠르게 블록체인 거래를 처리해요!
2. Optimistic 롤업은 "일단 믿고 7일 기다리기", ZK 롤업은 "수학으로 증명하고 즉시 확정" — 속도 vs 보안 트레이드오프예요.
3. 이더리움은 미래에 "L2 세계의 보안 기반"이 되기로 결정 — 빠른 거래는 L2에서, 최종 안전 보장은 이더리움이 담당해요!
