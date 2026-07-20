---
title: "Parallel Adder-Subtractor"
date: "2026-03-03"
tags:
  - "studynote-computer-architecture"
weight: 38
---
> **핵심 인사이트**
> 1. 병렬 가감산기(Parallel Adder-Subtractor)는 단일 회로에서 ADD(덧셈)와 SUB(뺄셈)를 모두 처리하는 복합 산술 회로로, SUB 제어 신호 하나로 XOR 게이트를 통한 B 반전과 Carry-In=1(2의 보수 +1)을 동시에 제어한다.
> 2. n비트 병렬 가감산기의 핵심은 Ripple Carry vs Carry Lookahead 트레이드오프 — Ripple Carry는 단순하지만 n단 지연, CLA(Carry Lookahead Adder)는 복잡하지만 O(log n) 지연으로 고속 CPU에 필수다.
> 3. 오버플로(Overflow) 감지는 부호 있는 연산의 필수 기능으로, 두 양수를 더해 음수가 되거나 두 음수를 더해 양수가 될 때 발생하며, MSB Carry-In과 Carry-Out의 XOR로 검출한다.

---

## I. 병렬 가감산기 구조

```
4비트 병렬 가감산기:

  B3  B2  B1  B0
   |   |   |   |
  XOR XOR XOR XOR  <-- SUB=1이면 B 반전
   |   |   |   |
  FA3 FA2 FA1 FA0  <-- Full Adder 4개 병렬 연결
   |   |   |   |  +-- SUB (Carry-In에 연결)
  S3  S2  S1  S0  (합/차 출력)
  |
 Cout (올림/넘침)

SUB=0: S = A + B       (덧셈)
SUB=1: S = A + ~B + 1  (뺄셈, 2의 보수)
```

| 제어 신호 | 동작              | Carry-In | B 처리    |
|---------|-----------------|---------|---------|
| SUB=0  | 덧셈 (A + B)     | 0       | 그대로   |
| SUB=1  | 뺄셈 (A - B)     | 1       | XOR로 반전|

> 📢 **섹션 요약 비유**: 스위치 하나로 믹서기(더하기 모드)와 분리기(빼기 모드)를 바꾸는 것 — 회로 두 배 없이 기능 두 배.

---

## II. Ripple Carry vs Carry Lookahead

```
Ripple Carry Adder (RCA):
  각 FA의 Carry-Out이 다음 FA의 Carry-In으로
  전달 지연: n × t_FA  (n=비트 수, t_FA=FA 지연)

  4비트: 4 × t_FA
  32비트: 32 × t_FA  (느림!)

Carry Lookahead Adder (CLA):
  Generate: G_i = A_i AND B_i  (항상 올림 생성)
  Propagate: P_i = A_i XOR B_i  (올림 전파)

  C_i+1 = G_i OR (P_i AND C_i)

  모든 Carry를 병렬로 미리 계산
  지연: O(log n) (2단계 로직 게이트)

  32비트 CLA vs RCA:
  RCA: ~32 t_FA
  CLA: ~4-5 게이트 지연 (블록 CLA)
```

> 📢 **섹션 요약 비유**: RCA는 편지를 한 명씩 전달, CLA는 모든 수신자에게 동시에 복사본 발송 — 수신자가 많을수록 CLA가 압도적으로 빠르다.

---

## III. 오버플로(Overflow) 검출

```
부호 있는 n비트 표현 범위:
  -2^(n-1) ~ 2^(n-1) - 1
  4비트: -8 ~ +7

오버플로 발생 조건:
  양수 + 양수 = 음수 (결과가 +7 초과)
  음수 + 음수 = 양수 (결과가 -8 미만)

오버플로 검출 회로:
  V = C_n XOR C_(n-1)
  (MSB Carry-Out XOR MSB Carry-In)

  V = 1이면 오버플로 발생

예시 (4비트 부호 있는):
  0111 (+7) + 0001 (+1) = 1000 = -8 (오버플로!)
  C_4=0, C_3=1 -> V = 0 XOR 1 = 1 (오버플로 감지)
```

> 📢 **섹션 요약 비유**: 온도계가 최대 눈금을 초과하면 바늘이 반대쪽으로 튀는 것처럼 — 오버플로는 결과가 표현 범위를 벗어나는 것.

---

## IV. ALU 내 가감산기 통합

```
현대 ALU (Arithmetic Logic Unit) 구조:

   A[n]       B[n]
    |           |
    |       [XOR] <-- SUB/ADD 제어
    |           |
        [CLA]      <-- 병렬 가감산기 핵심
          |
         S[n]  <-- 결과
          |
    [Overflow] <-- V = C_out XOR C_(n-1)
    [Zero]     <-- NOR(S[n])
    [Carry]    <-- C_out
    [Sign]     <-- S[n-1] (MSB)

상태 플래그 (NZVC):
  N (Negative): S의 MSB
  Z (Zero):     결과가 0이면 1
  V (oVerflow): 오버플로
  C (Carry):    올림수
```

> 📢 **섹션 요약 비유**: ALU는 스위스 군용 칼 — 가감산기 날, 오버플로 경고, 영 감지, 올림 표시가 한 손잡이에 모두.

---

## V. 실무 시나리오 — RISC-V ALU 실현

```
RISC-V 32비트 ALU:
  32비트 CLA 기반 가감산기
  SUB 신호: rs2를 반전 + Carry-In=1

  NZVC 플래그 -> 조건 분기 명령어에 활용:
    BEQ (Branch if Equal):  Z=1
    BNE (Branch if Not Equal): Z=0
    BLT (Branch if Less Than): N XOR V = 1
    BGE (Branch if Greater or Equal): N XOR V = 0

클락 속도에 미치는 영향:
  가감산기 지연 = 임계 경로(Critical Path)
  3GHz CPU에서 한 클락 = 0.33ns
  32비트 CLA 지연 목표: < 0.15ns (절반 이내)
```

> 📢 **섹션 요약 비유**: CPU 3GHz는 초당 30억 번 계산 — 가감산기가 0.15나노초 이내에 끝나야 다음 명령을 받을 수 있다.

---

## �� 관련 개념 맵

```
병렬 가감산기
+-- 구조
|   +-- XOR 게이트 (B 반전)
|   +-- SUB 제어 신호 (Carry-In)
+-- Carry 처리
|   +-- Ripple Carry: 직렬 전파, 느림
|   +-- CLA: 병렬 미리 계산, 빠름
+-- 오버플로
|   +-- V = C_out XOR C_(n-1)
|   +-- NZVC 상태 플래그
+-- ALU 통합
    +-- ADD/SUB 공용 회로
    +-- 조건 분기 플래그 생성
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전감산기 + 전가산기 분리]
각각 독립 회로, 비효율
      |
      v
[병렬 가감산기 통합]
XOR + Carry-In으로 ADD/SUB 공용
      |
      v
[CLA로 고속화]
O(log n) Carry 계산
Intel/AMD CPU ALU 적용
      |
      v
[현재: SIMD + 벡터 ALU]
256/512비트 병렬 연산 (AVX-512)
AI 가속기: 행렬 곱 전용 ALU
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 병렬 가감산기는 스위치 하나로 덧셈과 뺄셈을 모두 할 수 있는 계산기 회로예요.
2. 자리 올림수(Carry)를 미리 계산하는 CLA 방식 덕분에 32자리 수도 빠르게 계산할 수 있어요.
3. 오버플로는 계산기 표시 범위를 벗어나는 것 — CPU가 이를 감지해서 프로그램이 이상한 결과를 쓰지 않도록 막아요!
