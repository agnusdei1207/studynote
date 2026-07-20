---
title: "Comparator"
date: "2026-04-05"
tags:
  - "studynote-computer-architecture"
weight: 43
---
> **핵심 인사이트**
> 1. 비교기(Comparator)는 두 이진수 A와 B를 비교하여 A>B, A=B, A<B 세 가지 출력을 만드는 조합 논리 회로로, ALU(산술논리연산장치)의 조건 분기 판단과 정렬 네트워크의 기본 구성 요소이다.
> 2. 1비트 비교기는 XNOR(동치), AND/NOT 조합으로 구현하지만, 다비트 비교기는 MSB(Most Significant Bit)부터 우선 비교하는 직렬 비교(Iterative) 방식과 병렬 비교(Parallel) 방식의 속도-비용 트레이드오프가 존재한다.
> 3. 현대 CPU의 비교 연산은 플래그 레지스터(ZF, CF, SF, OF)를 통해 구현되며, CMP 명령어가 두 값을 빼고 결과를 버리되 플래그만 설정하는 방식 — 이것이 조건 점프(JE, JNE, JG, JL)와 연동되는 원리이다.

---

## Ⅰ. 1비트 비교기 설계

```
1비트 비교기 진리표:

A  B | A>B  A=B  A<B
-----|------------------
0  0 |  0    1    0
0  1 |  0    0    1
1  0 |  1    0    0
1  1 |  0    1    0

논리식:
  A=B: XNOR(A,B) = A⊙B = +(A⊕B)
  A>B: A AND +B
  A<B: +A AND B

게이트 구현:
  +-----+
A-+     +--- A>B (A AND +B)
B-+ NOT +-+
  +-----+ +- ...

  A--+-------------- AND --- A>B
     |      NOT-B -+
     |
     +-- XNOR ---- A=B
     |
  B--+
     +-- NOT-A -+
                +- AND --- A<B
```

> 📢 **섹션 요약 비유**: 1비트 비교기는 "둘 중 누가 큰가?" 심판 — 두 선수의 점수를 보고 이겼다/졌다/비겼다 세 가지 판정.

---

## Ⅱ. 4비트 직렬 비교기

```
4비트 직렬 비교기 (Iterative Comparator):

아이디어:
  MSB부터 순서대로 비교
  같으면 다음 비트로, 다르면 즉시 결론

알고리즘:
  result = EQ (초기: 동등 가정)
  FOR i = 3 DOWN TO 0:
    IF A[i] > B[i] AND result == EQ:
      result = GT; BREAK
    ELIF A[i] < B[i] AND result == EQ:
      result = LT; BREAK

  최종 result = GT/EQ/LT

회로 구조:
  각 비트에 1비트 비교기 4개 직렬 연결
  이전 단계의 결과를 다음 단계로 전달

비교 우선순위 (캐스케이드):
  Bit3 (MSB) -> Bit2 -> Bit1 -> Bit0 (LSB)

  [Bit3 비교기]--(GT3,EQ3,LT3)-->[Bit2 비교기]-->...-->[최종 출력]

시간 복잡도: O(n) 직렬 처리
단점: n비트 비교에 n개 단계 = 지연 누적
```

> 📢 **섹션 요약 비유**: 직렬 비교기는 릴레이 경주 — MSB 선수가 먼저 뛰고, 비겼으면 다음 주자에게 배턴 전달. 한 주자가 이기면 경주 종료.

---

## Ⅲ. 병렬 비교기와 74HC85

```
병렬 비교기 (Parallel Comparator):

아이디어:
  모든 비트를 동시에 비교 (병렬 처리)
  결과를 논리 게이트로 조합

4비트 병렬 비교기 논리식:
  A3 > B3: A3 AND +B3
  A3 = B3: A3 XNOR B3
  ...

전체 A > B 조건:
  (A3>B3) OR
  (A3=B3 AND A2>B2) OR
  (A3=B3 AND A2=B2 AND A1>B1) OR
  (A3=B3 AND A2=B2 AND A1=B1 AND A0>B0)

시간 복잡도: O(1) 병렬 처리 (지연: 2~3게이트)
단점: 게이트 수 = O(n^) 기하급수 증가

74HC85 (4비트 비교기 IC):
  입력: A3-A0, B3-B0, IAGB, IAEB, IALB (캐스케이드 입력)
  출력: OAGB (A>B), OAEB (A=B), OALB (A<B)

  캐스케이드 연결:
  낮은 비트 비교기의 출력 -> 높은 비트 비교기의 캐스케이드 입력
  -> 8비트, 16비트 비교기 확장 가능

성능 비교:
  직렬: 지연 O(n), 게이트 O(n)
  병렬: 지연 O(1), 게이트 O(n^)
  실제: 계층적 비교기로 균형
```

> 📢 **섹션 요약 비유**: 병렬 비교기는 여러 심판이 동시 판정 — 1번 심판은 100점 자리, 2번은 10점 자리 동시 채점, 한 번에 결론. 빠르지만 심판이 많이 필요.

---

## Ⅳ. CPU 플래그와 CMP 명령어

```
CPU 비교 연산 구현 (x86):

CMP 명령어:
  CMP A, B -> A - B 수행 (결과 버림), 플래그 설정

플래그 레지스터:
  ZF (Zero Flag): 결과 = 0 (A = B)
  CF (Carry Flag): 언사인드 빌림 발생 (A < B, 부호 없음)
  SF (Sign Flag): 결과 음수 (사인드)
  OF (Overflow Flag): 오버플로우

조건 점프 명령어:
  JE / JZ:  ZF=1       -> Jump if Equal
  JNE/JNZ:  ZF=0       -> Jump if Not Equal
  JG:       ZF=0, SF=OF -> Jump if Greater (부호 있음)
  JL:       SF≠OF      -> Jump if Less (부호 있음)
  JA:       CF=0, ZF=0 -> Jump if Above (부호 없음)
  JB:       CF=1       -> Jump if Below (부호 없음)

예시 (어셈블리):
  CMP EAX, EBX    ; EAX - EBX, 플래그 설정
  JE  equal_label ; ZF=1이면 점프
  JG  greater     ; EAX > EBX이면 점프
  JL  less        ; EAX < EBX이면 점프

ARM Cond:
  SUBS R0, R1, R2  ; R1 - R2, CPSR 플래그 설정
  BEQ  label        ; CPSR Z=1이면 분기
```

> 📢 **섹션 요약 비유**: CMP 명령어는 저울 0점 보정 — 두 무게를 비교할 때 실제로 빼보고 결과만 버리되 "어느 쪽이 무거웠는지" 기록만 남기는 것.

---

## Ⅴ. 실무 시나리오 — 정렬 네트워크

```
정렬 네트워크 (Sorting Network):

정의:
  비교기를 네트워크로 연결해 n개 값을 정렬하는 회로
  비교기가 직렬/병렬로 배치되어 고정된 순서로 비교

버블 정렬 하드웨어 구현:
  n=4 정렬 네트워크:

  [A0,A1] 비교기 -> 교환
  [A1,A2] 비교기 -> 교환
  [A0,A1] 비교기 -> 교환
  [A2,A3] 비교기 -> 교환
  [A1,A2] 비교기 -> 교환

Bitonic Sort Network:
  n=8: O(log^n) 단계 = 6단계
  병렬 처리: O(log^n) 지연

  장점: 완전 병렬 (GPU 정렬에 활용)
  단점: 2^k 개 원소만 처리 가능

FPGA/GPU 활용:
  비교기 네트워크 -> FPGA 로직 블록 구현
  GPU Thrust 라이브러리의 정렬 기반
  병렬 처리로 O(n) vs O(n log n) 속도 차이

데이터베이스 정렬:
  ORDER BY 실행: CPU 비교 + 병렬 정렬 네트워크
  SIMD 명령어: AVX2의 _mm256_cmp_ps 비교 명령
```

> 📢 **섹션 요약 비유**: 정렬 네트워크는 여러 체중계로 동시 측정 — 모든 사람이 동시에 서로 비교해서 한 번에 키 순서로 줄 세우기.

---

## 📌 관련 개념 맵

```
비교기 (Comparator)
+-- 1비트 비교기
|   +-- XNOR (동치), AND/NOT
+-- 다비트 비교기
|   +-- 직렬 (Iterative): O(n) 지연
|   +-- 병렬 (Parallel): O(1) 지연, O(n^) 게이트
|   +-- 74HC85 (캐스케이드)
+-- CPU 구현
|   +-- CMP 명령어, 플래그 레지스터
|   +-- 조건 점프 (JE, JG, JL)
+-- 응용
|   +-- 정렬 네트워크 (Bitonic Sort)
|   +-- ALU 조건 연산
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[기초 논리 게이트 (1940s~)]
XNOR = 동치 검사 기본
      |
      v
[조합 회로 비교기 (1960s)]
74HC85 4비트 비교기 IC
      |
      v
[CPU ALU 통합 (1970s~)]
플래그 레지스터 + CMP 명령어
x86 JE/JG/JL 조건 분기
      |
      v
[SIMD 병렬 비교 (1999~)]
SSE/AVX: 8개/16개 동시 비교
      |
      v
[현재: AI 가속기 비교기]
TPU/GPU: 행렬 원소 비교 병렬화
신경망 ReLU = 0과 비교기
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 비교기는 "둘 중 누가 더 크나?" 판단하는 심판 회로 — 두 숫자를 보고 "크다/같다/작다" 세 가지 신호를 보내줘요!
2. 1비트 비교기는 간단한 메모 — 1과 0만 비교, 4비트는 4단계 릴레이 경주로 결정해요.
3. CPU의 CMP 명령어는 저울 역할 — 두 값을 빼보고 결과는 버리되 "어느 쪽이 컸는지" 기록(플래그)만 남겨요!
