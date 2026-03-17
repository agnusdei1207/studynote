+++
title = "539. 루프 타일링 (Loop Tiling)"
date = "2026-03-14"
weight = 539
+++

# 539. 루프 타일링 (Loop Tiling)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 거대한 배열이나 행렬을 다루는 중첩 반복문(Nested Loop)을 실행할 때, 전체 데이터를 한 번에 순회하지 않고 **CPU (Central Processing Unit)의 고속 캐시(Cache) 크기에 최적화된 작은 조각(Tile 또는 Block)으로 분할하여 처리하는 컴파일러 및 알고리즘 최적화 기법**이다.
> 2. **가치**: 캐시 적중률(Cache Hit Rate)을 극대화하여 데이터 지역성(Data Locality)을 확보함으로써, 메모리 병목(Memory Wall) 현상을 완화하고 연산 성능을 수십 배 이상 향상시킨다.
> 3. **융합**: 딥러닝의 행렬 곱셈(GEMM)과 고성능 컴퓨팅(HPC) 필수 요소이며, 하드웨어 계층 구조와 소프트웨어 접근 패턴을 완벽하게 정렬시키는 '캐시 인지(Cache-aware) 프로그래밍'의 핵심이다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

루프 타일링(Loop Tiling) 또는 루프 블로킹(Loop Blocking)은 대용량 데이터를 처리하는 루프의 순회 공간(Iteration Space)을 재구성하여, 하드웨어의 메모리 계층 구조, 특히 캐시 메모리의 특성에 맞추는 최적화 기법이다. 복잡한 수치 연산에서 연산의 복잡도(Computational Complexity)는 $O(N^3)$이지만, 메모리 접근의 비효율로 인해 실제 성능은 훨씬 낮아지는 경우가 많은데, 이를 해결하기 위해 데이터를 캐시 라인(Cache Line) 단위가 아닌 논리적인 블록(Block) 단위로 재배치하는 전략이다.

**💡 비유**:
도서관(메인 메모리)에 있는 10,000권의 책(데이터)을 이용하여 연구(연산)를 해야 한다. 만약 책상(캐시)에 책 한 권을 올려놓고 읽고, 다시 반납하고를 10,000번 반복하면 이동 시간(메모리 지연 시간) 때문에 일을 진척할 수 없다. 하지만 책상 크기에 딱 맞게 책 100권(타일)을 한꺼번에 가져와서 책상 위에서 모든 작업을 마친 뒤 한 번에 반납한다면, 도서관과 책상 사이의 왕복 횟수는 1/100로 줄어든다. 루프 타일링은 바로 이 '한 번에 가져올 묶음'을 최적으로 정의하는 기술이다.

**등장 배경**:
1.  **폰 노이만 병목(Von Neumann Bottleneck)**: CPU의 연산 속도는 기하급수적으로 향상되었으나, 메모리 대역폭과 지연 시간(Latency)의 개선 속도는 이를 따라가지 못했다.
2.  **캐시의 한계**: CPU 내부의 작은 캐시(L1/L2)는 빠르지만 용량이 작다. 행렬 연산 등 순차적이지 않은 메모리 접근 패턴은 캐시의 데이터가 교체되기도 전에 다시 필요해지는 상황(Cache Thrashing)을 유발하여 성능을 저하시켰다.
3.  **소프트웨어적 해결책**: 하드웨어의 한계를 소프트웨어적으로 극복하고자, 데이터를 캐시 크기에 맞춰 잘라서 재사용성을 높이는 타일링 기법이 고안되었다.

> **📢 섹션 요약 비유**: **마치 식당 주방이 한정된 작업대(캐시) 공간을 효율적으로 쓰기 위해, 재료 냉장고(메모리)에서 한 번에 꺼내 올 수 있는 양을 정확히 계산하여 '재료 트레이(타일)'를 채워 놓고 요리하는 것과 같습니다.**

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

루프 타일링의 핵심은 **시간적 지역성(Temporal Locality)**과 **공간적 지역성(Spatial Locality)**을 동시에 만족시키는 데 있다. 이를 위해 루프의 인덱스 공간을 여러 개의 하위 공간(타일)으로 분할하고, 각 타일 내부에서 연산을 완료한다.

#### 구성 요소 및 파라미터

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 결정 파라미터 |
|:---|:---|:---|:---|
| **Iteration Space (순회 공간)** | 중첩 루프가 탐색하는 전체 다차원 좌표계 | 2중 루프는 2D 평면, 3중 루프는 3D 입체 공간으로 모델링됨 | $N \times N$ (행렬 크기) |
| **Tile Size (Block Factor)** | 한 번에 캐시에 적재할 데이터 뭉치의 크기 | L1 Cache Size를 초과하지 않아야 하며, 보통 $32 \times 32$ ~ $128 \times 128$ 사이로 결정 | CPU의 L1/L2 Cache Line Size, Associativity |
| **Padding & Alignment** | 캐시 충돌(Conflict Miss) 방지 | 타일의 시작 주소가 캐시 라인 경계와 일치하도록 메모리를 정렬 | Memory Alignment (예: 64-byte aligned) |
| **Loop Transformation** | 루프 순서 재배치 및 분할 | 기존 루프 위에 외부 블록 루프(Outer Block Loop)를 추가하고 내부에 내부 루프(Inner Loop)를 생성 | Blocking Factor ($B$), Stride |

---

#### 기본 아키텍처 다이어그램

다음은 타일링이 적용되지 않은 일반 루프와 타일링이 적용된 루프의 메모리 접근 패턴을 비교한 것이다.

```text
  [일반 루프 (Standard) vs 타일링 루프 (Tiled) 아키텍처]

  (A) 일반 중첩 루프 (Naive Loop)
  ------------------------------------------------------------
  for (i = 0; i < N; i++)
      for (k = 0; k < N; k++)
          for (j = 0; j < N; j++)
              C[i][j] += A[i][k] * B[k][j];
  
  [메모리 접근 흐름]
  CPU Cache (L1)  : [ A[i][k] ] (입구만 킁킁) --> 빈번한 Miss
  Memory (DRAM)   : <------- 데이터 전송 (느림) ------->

  (B) 루프 타일링 (Blocked Loop with Tile Size B)
  ------------------------------------------------------------
  // Outer Loops: Tile 단위 이동
  for (ii = 0; ii < N; ii += B)
      for (kk = 0; kk < N; kk += B)
          for (jj = 0; jj < N; jj += B)
              
              // Inner Loops: Tile 내부 미세 연산
              for (i = ii; i < ii + B; i++)
                  for (k = kk; k < kk + B; k++)
                      for (j = jj; j < jj + B; j++)
                          C[i][j] += A[i][k] * B[k][j];

  [메모리 접근 흐름]
  CPU Cache (L1)  : [ A[ii...ii+B][kk...kk+B] Tile ]
                   [ B[kk...kk+B][jj...jj+B] Tile ]  (재사용 극대화)
  Memory (DRAM)   : <----- Tile 단위로 한 번만 로드 ------>
```

**[다이어그램 해설]**
(A)의 일반 루프 방식에서는 행렬 $B$의 열(Column) 방향 접근이 발생할 때마다 캐시 라인을 새로 교체해야 하므로, 한 번 로드된 데이터가 제때 재사용되지 못하고 메모리에서 쫓겨난다. 반면 (B)의 타일링 방식은 외부 루프(Outer Loops)가 $ii, kk, jj$라는 블록 단위 인덱스를 이동시킨다. 내부 루프는 $B \times B$ 크기의 작은 행렬만을 집중적으로 계산한다. 이 작은 타일이 L1 캐시에 완전히 적재되면, 내부 연산이 끝날 때까지 메모리(DRAM)와의 통신이 전혀 발생하지 않는다. 즉, 느린 메모리 접근을 $O(N^3)$ 번에서 $O(N^3/B^2)$ 수준으로 획기적으로 줄여주는 구조다.

---

#### 심층 알고리즘 및 코드 (C 언어)

타일링의 효과를 극대화하기 위해서는 데이터의 배열 순서(Array Layout)를 고려해야 한다. 아래는 C 언어로 구현된 행렬 곱셈의 타일링 예시이며, `restrict` 키워드를 사용하여 포인터 별칭 문제를 최소화한다.

```c
// MAC (Multiply-Accumulate) 연산 매크로
#define MIN(a, b) ((a) < (b) ? (a) : (b))

void matrix_multiply_tiling(int N, double *restrict A, double *restrict B, double *restrict C) {
    // 타일 크기 B는 시스템의 L1 캐시 크기에 따라 실험적으로 결정해야 함.
    // 예: L1 캐시 32KB 일 때, double(8byte) * 3개(A,B,C) = 24byte 사용.
    // B*B*24 < 32768 -> B^2 < 1300 -> B = 32 (안전한 값)
    const int B = 32; 

    for (int ii = 0; ii < N; ii += B) {
        for (int kk = 0; kk < N; kk += B) {
            for (int jj = 0; jj < N; jj += B) {
                
                // 현재 타일 영역 계산
                int i_max = MIN(ii + B, N);
                int k_max = MIN(kk + B, N);
                int j_max = MIN(jj + B, N);

                // 타일 내부 연산 (L1 Cache 내에서 실행됨)
                for (int i = ii; i < i_max; i++) {
                    for (int k = kk; k < k_max; k++) {
                        // 루프 언롤링 및 레지스터 할당을 유도하기 위한 로컬 변수
                        double temp = A[i * N + k]; 
                        
                        // k 루프를 jj 루프 안으로 배치하여 B[k][j] 재사용 극대화
                        for (int j = jj; j < j_max; j++) {
                            C[i * N + j] += temp * B[k * N + j];
                        }
                    }
                }
            }
        }
    }
}
```
*주요 포인트: `k` 루프를 `j` 루프 내부에 배치하여 행렬 $B$의 데이터가 캐시에서 쫓겨나기 전에 `j`축 방향으로 최대한 재사용되도록 유도했다.*

> **📢 섹션 요약 비유**: **마치 거대한 퍼즐(행렬 연산)을 맞출 때, 전체 퍼즐 조각을 한꺼번에 테이블에 깔지 않고, '한 눈금 분량의 조각(타일)'만 테이블(캐시) 위에 올려놓고 그 부분만 완성해 낸 뒤 다음 조각을 가져오는 방식과 같습니다. 테이블이 작아도 거대한 작업을 완성할 수 있는 지혜입니다.**

---

### Ⅲ. 융합 비교 및 다각도 분석 - [비교표 2개+]

루프 타일링은 단순히 루프를 바꾸는 것이 아니라, 시스템 아키텍처의 병목 지점을 공략하는 전술이다.

#### 루프 최적화 기법 심층 비교

| 비교 항목 | Loop Tiling (Loop Blocking) | Loop Interchange | Loop Unrolling (Loop Unwinding) |
|:---|:---|:---|:---|
| **주 타겟 아키텍처** | Memory Hierarchy (Cache/RAM) | Memory Hierarchy (Spatial Locality) | CPU Pipeline (ILP: Instruction Level Parallelism) |
| **동작 원리** | 데이터를 일정 크기 블록으로 나누어 캐시 유지 시간 증대 | 루프의 순서를 바꾸어 메모리 연속 접근 유도 | 루프 인덱스 증가 분기를 제거하여 파이프라인 스톨 방지 |
| **주요 지표** | Cache Hit Rate ↑, Memory Bandwidth ↓ | Stride 접근 최소화 | CPI (Cycles Per Instruction) ↓, Branch Prediction 부하 ↓ |
| **부작용** | 코드 복잡도 증가, 타일 크기 결정의 어려움 | 데이터 의존성(Dependency) 위반 시 오류 발생 가능 | 코드 사이즈(Code Size) 폭발 (Instruction Cache Pressure) |
| **융합 시너지** | **데이터를 캐시에 올려두는 (Load 단계)** 역할 | **데이터를 효율적으로 펼쳐놓는 (Layout 단계)** 역할 | **올려진 데이터를 빠르게 연산하는 (Execute 단계)** 역할 |

#### 타 과목 융합 관점 (OS & 컴퓨터 구조)

1.  **OS와의 융합 (페이지 폴트 감소)**:
    가상 메모리(Virtual Memory)를 사용하는 시스템에서 운영체제(OS)는 페이지(Page) 단위로 데이터를 스왑(Swap)한다. 만약 루프 타일링을 하지 않아 대형 배열이 흩어서 접근된다면, OS는 페이지 부재(Page Fault)가 발생할 때마다 디스크 I/O를 발생시켜 성능이 현저히 저하된다(Thrashing). 타일링은 메모리 접근을 국지화(Localize)하여 운영체제가 관리해야 할 워킹 세트(Working Set)의 크기를 줄여주어 시스템 전체의 안정성에 기여한다.

2.  **컴퓨터 구조와의 융합 (프리패칭 효율)**:
    현대 CPU는 **Hardware Prefetcher**를 탑재하여 메모리 접근 패턴을 학습하고 데이터를 미리 가져온다. 타일링된 루프는 매우 규칙적이고 국소적인 메모리 접근 패턴(stride access)을 보여준다. 이는 프리패처가 예측 성공률을 높이고, 메모리 대역폭을 효율적으로 사용하게 하여, 결과적으로 CPU의 슈퍼스칼라(Superscalar) 파이프라인이 데이터 기다림 없이 가득 차게 만든다.

> **