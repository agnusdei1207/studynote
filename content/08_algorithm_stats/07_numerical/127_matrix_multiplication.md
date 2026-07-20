---
title: "Matrix Multiplication Optimization"
date: "2025-01-01"
tags:
  - "GEMM"
  - "O(N^2.81)"
  - "Strassen"
  - "block matrix"
  - "cache optimization"
  - "cuBLAS"
  - "deep learning"
  - "matrix multiplication"
  - "studynote-algorithm-stats"
weight: 127
---
> **핵심 인사이트 3줄**
> 1. 나이브 행렬 곱셈 O(N³)은 Strassen(1969)의 분할정복으로 O(N^2.807)으로 개선됐으나, 실무에서는 캐시 효율을 극대화한 블록 행렬 곱셈(GEMM)이 더 중요하다.
> 2. 딥러닝의 핵심 연산인 행렬 곱셈(matmul)은 GPU의 SIMD 병렬 처리와 Tensor Core(FP16/INT8)를 통해 수천 배 가속된다.
> 3. 현대 BLAS 라이브러리(OpenBLAS, cuBLAS, oneMKL)는 하드웨어 특성에 맞춘 극도로 최적화된 GEMM 커널을 제공하여 직접 구현보다 수십~수백 배 빠르다.

---

## Ⅰ. 나이브 행렬 곱셈

### 1.1 기본 정의

C[i][j] = Σ_{k=0}^{N-1} A[i][k] × B[k][j]

3중 루프 -> O(N³)

```python
def matmul_naive(A, B):
    N = len(A)
    C = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    return C
```

### 1.2 캐시 미스 문제

```
메모리 접근 패턴:
A[i][k]: 행 방향 접근 -> 캐시 친화적 ✓
B[k][j]: 열 방향 접근 -> 캐시 미스 빈번 ✗
```

B 행렬을 전치(transpose)하면 j 방향 접근이 행 방향으로 바뀌어 캐시 효율 개선.

📢 **섹션 요약 비유**: 행렬 곱셈에서 B를 열방향으로 읽는 건 책을 한 쪽 건너뛰며 읽는 것 — 캐시가 미리 준비를 못 해 느리다.

---

## Ⅱ. Strassen 알고리즘

### 2.1 분할 정복

2N×2N 행렬을 N×N 블록으로 분할:

```
[C11 C12]   [A11 A12]   [B11 B12]
[C21 C22] = [A21 A22] × [B21 B22]

나이브: 8번 재귀 곱셈 -> T(N) = 8T(N/2) + O(N^) -> O(N³)

Strassen:
M1 = (A11+A22)(B11+B22)
M2 = (A21+A22)B11
M3 = A11(B12-B22)
M4 = A22(B21-B11)
M5 = (A11+A12)B22
M6 = (A21-A11)(B11+B12)
M7 = (A12-A22)(B21+B22)

C11 = M1+M4-M5+M7
C12 = M3+M5
C21 = M2+M4
C22 = M1-M2+M3+M6
-> 7번 재귀 곱셈 -> O(N^log₂7) ≈ O(N^2.807)
```

### 2.2 실용성 한계

- 수치 불안정성 (부동소수점 오류 누적)
- 작은 N에서는 오버헤드로 나이브보다 느림
- 현재 이론적 최선: Williams et al. (2024) O(N^2.371552)

📢 **섹션 요약 비유**: Strassen은 8번 곱할 것을 7번으로 줄인 영리한 요령 — 하지만 중간 계산(덧셈)이 늘어 실제로는 항상 빠르지 않다.

---

## Ⅲ. 블록 행렬 곱셈 (Cache Blocking)

### 3.1 캐시 계층 활용

```
L1 캐시: ~32KB, ~4 사이클
L2 캐시: ~256KB, ~12 사이클
L3 캐시: ~8MB, ~40 사이클
메모리:  수 GB, ~100+ 사이클
```

블록 크기 B를 L1/L2 캐시에 맞게 설정:

```python
def matmul_blocked(A, B, block_size=64):
    N = len(A)
    C = [[0]*N for _ in range(N)]
    for ii in range(0, N, block_size):
        for jj in range(0, N, block_size):
            for kk in range(0, N, block_size):
                # 블록 단위 계산 (L1 캐시 내에서)
                for i in range(ii, min(ii+block_size, N)):
                    for j in range(jj, min(jj+block_size, N)):
                        for k in range(kk, min(kk+block_size, N)):
                            C[i][j] += A[i][k] * B[k][j]
    return C
```

📢 **섹션 요약 비유**: 블록 분할은 큰 교재를 챕터(블록)로 나눠 공부하는 것 — 챕터 내용을 한 번에 머릿속(캐시)에 넣어 효율을 높인다.

---

## Ⅳ. GPU 가속 행렬 곱셈

### 4.1 GPU 병렬화

```
CPU (단일 코어 순차):
  C[0][0], C[0][1], ... (순서대로)

GPU (수천 코어 병렬):
  C[i][j] 각각을 독립 스레드로 계산
  -> 이론상 N^ 병렬 처리
```

### 4.2 Tensor Core (NVIDIA)

- FP32 연산 대비 FP16/BF16 -> ~2배, INT8 -> ~4배 처리량
- A100 GPU: FP16 Tensor Core 312 TFLOPS
- 딥러닝 matmul에서 Automatic Mixed Precision(AMP)으로 활용

### 4.3 BLAS GEMM 호출

```python
import numpy as np  # BLAS (OpenBLAS/MKL) 자동 활용
C = np.dot(A, B)  # 또는 A @ B

import torch
C = torch.mm(A_gpu, B_gpu)  # cuBLAS 자동 활용
```

📢 **섹션 요약 비유**: GPU는 수천 명의 계산원 — 큰 행렬의 모든 원소를 동시에 계산해 CPU 한 명이 순서대로 하는 것보다 압도적으로 빠르다.

---

## Ⅴ. 현대 행렬 곱셈 표준 — GEMM

### 5.1 BLAS GEMM API

```
C = α·op(A)·op(B) + β·C
```

- op(): 전치(T), 켤레전치(H), 또는 그대로(N)
- SGEMM: 단정밀도, DGEMM: 배정밀도, HGEMM: 반정밀도

### 5.2 행렬 곱셈 복잡도 최선

| 알고리즘          | 복잡도            | 비고                      |
|----------------|-----------------|--------------------------|
| 나이브           | O(N³)           | 기본                     |
| Strassen        | O(N^2.807)      | 실용성 제한              |
| Williams(2024)  | O(N^2.371552)   | 이론적 최선              |
| GPU BLAS        | O(N³/P)         | P개 코어 병렬             |

📢 **섹션 요약 비유**: BLAS GEMM은 수학 계산기 중 최고 성능 — 직접 3중 루프 짜는 것보다 항상 라이브러리를 써라.

---

## 📌 관련 개념 맵

```
행렬 곱셈 최적화
+-- 알고리즘
|   +-- 나이브 O(N³)
|   +-- Strassen O(N^2.807)
|   +-- 이론 한계 (O(N^2.37))
+-- 캐시 최적화
|   +-- 전치 최적화
|   +-- 블록 행렬 곱셈
+-- 하드웨어 가속
|   +-- SIMD (AVX-512)
|   +-- GPU (Tensor Core)
|   +-- TPU (Google)
+-- 라이브러리
    +-- BLAS (OpenBLAS, MKL)
    +-- cuBLAS (NVIDIA GPU)
    +-- NumPy/PyTorch 자동 활용
```

---

## 📈 관련 키워드 및 발전 흐름도

```
나이브 행렬 곱셈 O(N³)
     |  이론적 개선
     v
Strassen O(N^2.807) (1969)
     |  캐시 효율 최적화
     v
블록 GEMM + BLAS (1970s~80s)
     |  GPU 병렬화
     v
cuBLAS / cuDNN (2007~)
     |  딥러닝 전용 하드웨어
     v
Tensor Core FP16/INT8 (2017~)
     |  이론 한계 접근
     v
Williams et al. O(N^2.37) (2024)
```

**핵심 키워드**: Strassen, GEMM, BLAS, 블록 행렬, Tensor Core, cuBLAS, AMP, 캐시 최적화

---

## 👶 어린이를 위한 3줄 비유 설명

1. 나이브 행렬 곱셈은 곱셈표를 직접 채우는 것 — 칸이 많을수록(N³) 엄청 오래 걸려.
2. Strassen은 8번 곱할 걸 7번으로 줄이는 꼼수 — 조금이라도 덜 계산해서 빠르게 만드는 거야.
3. GPU는 수천 명이 동시에 한 줄씩 채우는 것 — 혼자 다 하는 CPU보다 훨씬 빠르고 딥러닝에서 필수야.
