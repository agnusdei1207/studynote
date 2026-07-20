---
title: "Non-Interactive Zero-Knowledge Proof"
date: "2026-03-03"
tags:
  - "studynote-ict-convergence"
weight: 38
---
> **핵심 인사이트**
> 1. zk-SNARK(Succinct Non-interactive ARguments of Knowledge)는 영지식 증명을 단 한 번의 메시지 전송으로 검증 가능하게 만든 비대화형 프로토콜로, 블록체인에서 여러 라운드 상호작용 없이 스마트 컨트랙트가 즉시 검증할 수 있다.
> 2. 핵심 구성 요소는 신뢰 설정(Trusted Setup, CRS: Common Reference String)으로 생성된 증명 키(pk)와 검증 키(vk)로, 이 CRS가 안전하게 폐기되지 않으면 위조 증명이 가능한 독성 폐기물(Toxic Waste) 문제가 있다.
> 3. Groth16이 현재 가장 효율적인 zk-SNARK 구현(증명 크기 192바이트, 검증 3ms)이며, Ethereum zkEVM(zkSync, Polygon zkEVM)의 핵심 암호 기반으로 Layer 2 스케일링의 보안을 보장한다.

---

## I. 대화형 vs 비대화형 ZKP

```
대화형 ZKP (Interactive):
  증명자와 검증자가 여러 라운드 메시지 교환

  증명자: 커밋(commit)
  검증자: 챌린지(challenge)
  증명자: 응답(response)
  -> 반복 (보안 요구 수준만큼)

  문제: 블록체인 스마트 컨트랙트는
        실시간 상호작용 불가!

비대화형 ZKP (Non-Interactive, NIZK):
  단 하나의 증명 메시지만 전송
  누구든 언제든 검증 가능

  핵심 기술: Fiat-Shamir 휴리스틱
    챌린지를 랜덤 오라클(해시 함수)로 대체
    -> 챌린지를 증명자가 스스로 생성
```

> 📢 **섹션 요약 비유**: 대화형은 퀴즈쇼처럼 MC가 질문하고 참가자가 답하는 것, 비대화형은 참가자가 미리 답변서를 작성해 제출하는 것 — 블록체인에서는 제출형만 가능.

---

## II. zk-SNARK 구성 요소

```
zk-SNARK 시스템 구성:

1. 신뢰 설정 (Trusted Setup):
   비밀 파라미터 τ (독성 폐기물)로 CRS 생성
   CRS = (pk, vk)
   -> τ는 반드시 안전하게 폐기되어야 함!

   의식 (Ceremony): 수천 명이 참여해
   각자 랜덤성 기여 -> 일부만 정직해도 안전

2. 증명 (Prove):
   input(공개값) + witness(비밀값) + pk
   -> 증명 π 생성 (수백 바이트)

3. 검증 (Verify):
   input(공개값) + π + vk
   -> True/False (밀리초 단위)
```

| 단계     | 입력                    | 출력       | 수행자    |
|--------|------------------------|---------|--------|
| 설정    | 비밀 파라미터 τ          | (pk, vk)| 신뢰 제3자|
| 증명    | witness + input + pk   | π       | 증명자   |
| 검증    | π + input + vk         | True/False| 검증자  |

> �� **섹션 요약 비유**: CRS 생성은 열쇠 공장 설립(독성 폐기물=마스터키 파괴), 증명은 자물쇠 만들기, 검증은 열쇠로 열어보기.

---

## III. Groth16 — 현재 표준

```
Groth16 (Jens Groth, 2016):

증명 크기: 192바이트 (가장 작음)
검증 시간: ~3ms (이더리움 가스: ~300,000)
증명 시간: 회로 크기에 비례 (수 ms ~ 수 분)

구조:
  QAP (Quadratic Arithmetic Program)로
  계산 문제를 다항식 제약으로 변환

  예: "나는 x를 알고 있고 f(x) = y이다"
  -> 다항식 P(z)가 특정 조건 만족하는지 증명

한계:
  회로별 신뢰 설정 필요 (회로 변경 시 재설정)
  -> PLONK/Halo2는 Universal Setup으로 개선
```

> 📢 **섹션 요약 비유**: Groth16은 최소 포장재로 최대 정보를 담은 소포 — 192바이트로 수백만 연산 결과의 정확성을 증명.

---

## IV. PLONK와 범용 설정

```
PLONK (Permutations over Lagrange-bases
        for Oecumenical Noninteractive
        arguments of Knowledge, 2019):

개선점:
  Universal Setup (범용 설정):
    한 번 설정으로 모든 회로 사용 가능
    Groth16: 회로마다 별도 설정 필요

  Updateable Setup (업데이트 가능):
    기존 CRS에 랜덤성 추가 가능
    신뢰 의식 반복 가능

  증명 크기: ~500 바이트 (Groth16 192보다 큼)
  검증 시간: 비슷한 수준

Halo2 (Zcash 개발):
  신뢰 설정 불필요 (Inner Product Argument 기반)
  재귀 증명(Recursive Proof) 지원
  Ethereum zkEVM 일부 채택
```

> 📢 **섹션 요약 비유**: Groth16은 맞춤 정장(회로마다 재단), PLONK는 기성복(범용 설정으로 어느 회로든) — 편의성과 크기의 트레이드오프.

---

## V. 실무 시나리오 — zkSync Era 동작

```
zkSync Era (Ethereum Layer 2):

사용자 트랜잭션 흐름:
  1. 사용자 트랜잭션 수천 건 수집
  2. Sequencer: 상태 전환 계산
     (Before State Root -> After State Root)
  3. Prover: zk-SNARK 증명 생성
     회로: EVM 실행 + 상태 전환 검증
     증명 시간: 초 ~ 수 분 (회로 크기)
  4. Verifier Contract (Ethereum L1):
     π + 공개 입출력 + vk
     -> 가스 300,000 소비 (~$1~3)
     -> 수천 건 트랜잭션 검증 완료!

보안:
  L2 운영자가 악의적이어도
  유효한 증명 없이는 L1 통과 불가
  수학적으로 안전 (암호학적 가정 하에)
```

> 📢 **섹션 요약 비유**: zkSync는 수천 명의 정산을 공인 회계사(zk-SNARK)가 검증한 한 장의 확인서로 제출하는 것 — $1로 수천 건 검증.

---

## 📌 관련 개념 맵

```
zk-SNARK (비대화형 ZKP)
+-- 핵심 특성
|   +-- Succinct (간결: 작은 증명)
|   +-- Non-interactive (비대화형)
|   +-- ARguments (계산적 건전성)
|   +-- Knowledge (증인 지식)
+-- 구성
|   +-- 신뢰 설정 (CRS, 독성 폐기물 문제)
|   +-- 증명 키(pk), 검증 키(vk)
+-- 구현
|   +-- Groth16 (가장 효율적)
|   +-- PLONK (범용 설정)
|   +-- Halo2 (신뢰 설정 불필요)
+-- 응용
    +-- zkEVM (zkSync, Polygon)
    +-- Zcash (프라이버시 코인)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[ZKP 이론 (1985)]
대화형 영지식 증명
      |
      v
[Fiat-Shamir 휴리스틱 (1986)]
비대화형 변환
      |
      v
[Groth16 (2016)]
실용적 zk-SNARK
Zcash 채택
      |
      v
[PLONK (2019) / Halo2]
범용 설정, 신뢰 설정 개선
      |
      v
[현재: zkEVM 경쟁 (2022~)]
zkSync Era, Polygon zkEVM, Scroll
EVM 전체를 zk-SNARK 회로로
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. zk-SNARK는 "나는 이 비밀을 알고 있다"를 단 한 장의 종이(증명서)로 증명하는 방법이에요.
2. 이더리움 같은 블록체인에서는 여러 번 대화할 수 없어서, 한 번에 제출하는 비대화형 방식이 꼭 필요해요.
3. 이 덕분에 수천 건의 거래를 단 1달러짜리 검증 하나로 처리해서 블록체인을 100배 이상 빠르게 만들 수 있어요!
