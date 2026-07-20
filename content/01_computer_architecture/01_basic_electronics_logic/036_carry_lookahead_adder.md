---
title: "Carry Lookahead Adder"
date: "2026-03-03"
tags:
  - "studynote-computer-architecture"
weight: 36
---
> **핵심 인사이트**
> 1. CLA (Carry Lookahead Adder)는 각 비트의 Generate(G)·Propagate(P) 신호를 이용해 캐리를 병렬로 미리 계산함으로써 RCA의 O(n) 직렬 지연을 O(log n)으로 줄인 고속 가산기다.
> 2. G = A AND B (이 자리에서 캐리 생성), P = A XOR B (입력 캐리를 다음으로 전달)를 조합해 모든 자리의 캐리를 동시에 계산할 수 있다.
> 3. 계층적 CLA(Hierarchical CLA)는 4-bit 블록을 다시 CLA로 묶어 32·64-bit 가산을 O(log n) 유지하면서 게이트 수를 관리하며, Kogge-Stone·Brent-Kung은 이를 더 최적화한 병렬 접두사 구조다.

---

## I. G·P 신호와 캐리 공식

```
1-bit 수준 정의:
  Gi = Ai AND Bi        (Generate: 자체 캐리 생성)
  Pi = Ai XOR Bi        (Propagate: 입력 캐리 전달)

캐리 재귀 계산 (4-bit):
  C1 = G0 + P0·C0
  C2 = G1 + P1·G0 + P1·P0·C0
  C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0
  C4 = G3 + P3·G2 + P3·P2·G1 + P3·P2·P1·G0 + P3·P2·P1·P0·C0

모든 Ci를 병렬로 동시 계산 -> O(1) 캐리 지연
```

> 📢 **섹션 요약 비유**: 릴레이 경기 전에 각 구간 선수의 속도를 미리 계산해 바통 도착 시각을 예측 — 기다리지 않고 모든 구간을 동시에 준비.

---

## II. 4-bit CLA 구조

```
       A3 B3   A2 B2   A1 B1   A0 B0
         |       |       |       |
   G3,P3 |  G2,P2|  G1,P1|  G0,P0|
         |       |       |       |
    [CLA Logic: C4,C3,C2,C1 동시 계산]
         |       |       |       |
        [FA3]  [FA2]  [FA1]  [FA0]
         |       |       |       |
         S3      S2      S1      S0
```

| 구조 요소    | 역할                   |
|------------|----------------------|
| G/P 생성기  | 각 비트 G, P 계산      |
| CLA 로직    | 모든 캐리 병렬 계산    |
| Sum 생성기  | Si = Pi XOR Ci        |

> 📢 **섹션 요약 비유**: 모든 심판이 동시에 준비 완료 신호를 계산 — 선수들은 신호가 오자마자 일제히 출발.

---

## III. 계층적 CLA (Hierarchical CLA)

```
32-bit = 4 x 8-bit 블록

블록 0 (bit 0-7):
  G[0..7] = G7 + P7·G6 + P7·P6·G5 + ...
  P[0..7] = P7·P6·P5·P4·P3·P2·P1·P0

상위 CLA: C8, C16, C24, C32를 블록 G/P로 계산
        -> 전체 O(log n) 유지
```

| 방식              | 지연       | 게이트 수  |
|-----------------|-----------|-----------|
| RCA (32-bit)    | O(n)=32t  | 최소       |
| CLA (flat)      | O(log n)  | 많음       |
| 계층적 CLA       | O(log n)  | 중간       |
| Kogge-Stone     | O(log n)  | 최다       |
| Brent-Kung      | O(log n)  | 중간, 균형  |

> 📢 **섹션 요약 비유**: 4개 팀으로 나눠 각 팀이 동시에 달린 뒤, 팀 결과를 또 동시에 집계 — 분할 정복으로 전체가 빠르다.

---

## IV. Kogge-Stone 아키텍처

```
Kogge-Stone: 완전 병렬 접두사 구조
단계 수: log2(n) = 5 (32-bit)

단계 1: 거리 1 병합
단계 2: 거리 2 병합
단계 3: 거리 4 병합
단계 4: 거리 8 병합
단계 5: 거리 16 병합

장점: 최소 지연 (5단계)
단점: 와이어 수 많음 -> 칩 면적, 전력 소비
```

> 📢 **섹션 요약 비유**: 1, 2, 4, 8, 16칸씩 점프하며 이웃과 합산 — 도약 폭을 두 배씩 늘려 빠르게 전체를 합산.

---

## V. 실무 — Intel/AMD CPU ALU

| 제품                | 가산기 방식           | 목적                |
|--------------------|---------------------|---------------------|
| Intel Core 정수 ALU | Kogge-Stone 변형     | 1-cycle 64-bit 덧셈 |
| AMD Zen ALU         | Ling Adder (변형 CLA)| 빠른 비교 연산       |
| FPGA 구현           | 캐리 체인 LUT        | 면적·속도 균형       |

> 📢 **섹션 요약 비유**: 현대 CPU의 덧셈은 모두 CLA 계열 — 3GHz 클럭에서 1사이클에 덧셈을 끝내려면 캐리 예측이 필수.

---

## 📌 관련 개념 맵

```
CLA (Carry Lookahead Adder)
+-- G/P 신호: 각 비트의 캐리 생성/전달
+-- 병렬 캐리 계산: O(log n) 지연
+-- 계층 구조
|   +-- 계층적 CLA (블록 단위)
|   +-- Kogge-Stone (완전 병렬)
|   +-- Brent-Kung (면적 최적)
|   +-- Han-Carlson (균형)
+-- 비교
    +-- RCA: O(n), 단순
    +-- CLA: O(log n), 게이트 증가
    +-- CSA: 3->2 압축, 곱셈기 내부
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[반가산기 -> 전가산기 -> RCA]
O(n) 직렬 캐리 전파 문제
      |
      v
[CLA (Carry Lookahead Adder, 1960s)]
G/P로 캐리 병렬 계산 -> O(log n)
      |
      v
[계층적 CLA]
블록 단위 그룹화 -> 게이트 수 관리
      |
      v
[병렬 접두사 가산기]
Kogge-Stone (1973): 최소 지연
Brent-Kung (1982): 균형
      |
      v
[현대 CPU/GPU ALU]
GHz 주파수에서 1-cycle 64-bit 가산
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CLA는 덧셈의 받아올림을 미리 예측해서 기다리지 않고 동시에 계산해요.
2. 10자리 덧셈도 5단계만에 끝낼 수 있는 비법이에요.
3. 현대 컴퓨터 CPU가 엄청 빠른 덧셈을 할 수 있는 건 이 방법 덕분이에요!
