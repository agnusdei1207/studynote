---
title: "Fenwick Tree"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
weight: 86
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 펜윅 트리(Fenwick Tree) 또는 BIT(Binary Indexed Tree)는 배열의 접두사 합(Prefix Sum)을 O(log N)에 쿼리하고 O(log N)에 업데이트하는 자료 구조다. 단순 배열의 O(1) 업데이트/O(N) 쿼리와 누적 합 배열의 O(N) 업데이트/O(1) 쿼리 사이의 최적 균형이다.
> 2. **가치**: 비트 연산(lowbit = n & (-n))으로 트리 구조를 1D 배열에 압축하여 구현한다. 세그먼트 트리보다 코드가 간결하고 캐시 효율이 좋다. 구현 단순성과 성능 모두 뛰어나다.
> 3. **판단 포인트**: 펜윅 트리는 점 업데이트 + 범위 합 쿼리에 최적이다. 범위 업데이트 + 범위 합 쿼리가 필요하다면 2개의 BIT를 조합하거나 세그먼트 트리를 사용한다.

---

## Ⅰ. 개요 및 필요성

```text
문제: 배열 A[1..N]에서
  - 점 업데이트: A[i] += delta
  - 범위 합 쿼리: A[l] + A[l+1] + ... + A[r]
  를 반복적으로 수행

접근 비교:
  단순 배열:    업데이트 O(1) / 쿼리 O(N)
  누적 합:      업데이트 O(N) / 쿼리 O(1)
  펜윅 트리:    업데이트 O(logN) / 쿼리 O(logN) <- 최적 균형
  세그먼트:     업데이트 O(logN) / 쿼리 O(logN) (더 범용)
```

- **📢 섹션 요약 비유**: 펜윅 트리는 분산 회계 시스템이다. 각 지점이 일부 지역 합계를 담당하여, 업데이트 시 관련 지점만 갱신하고 전체 합산 시 필요한 지점만 합산해서 O(log N)의 균형 성능을 낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### lowbit과 BIT 인덱스

```text
핵심: lowbit(i) = i & (-i) = i의 최하위 비트

i = 6 = 0b0110
-i = 0b1010 (2의 보수)
i & (-i) = 0b0010 = 2

BIT[i]는 A[i-lowbit(i)+1 .. i]의 합 담당

예: BIT[6] = A[5] + A[6]  (lowbit(6)=2이므로)
    BIT[4] = A[1]+A[2]+A[3]+A[4]  (lowbit(4)=4)

업데이트 A[i]:
  i = i, i + lowbit(i), i + 2*lowbit(i), ...
  (루트 방향으로 올라가며 갱신)

쿼리 합(1..i):
  i = i, i - lowbit(i), i - 2*lowbit(i), ...
  (왼쪽으로 이동하며 합산)
```

### Python 구현

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i, delta):    # O(log N)
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)          # lowbit 추가

    def query(self, i):            # prefix sum [1..i], O(log N)
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)          # lowbit 제거
        return s

    def range_query(self, l, r):   # [l..r] 범위 합
        return self.query(r) - self.query(l - 1)
```

- **📢 섹션 요약 비유**: lowbit 비트 연산은 이진수 계단 탐색이다. 숫자의 마지막 1비트 위치가 담당 범위를 결정하고, 올라가거나 내려가며 필요한 블록만 정확하게 합산한다.

---

## Ⅲ. 비교 및 연결

| 비교 | BIT | 세그먼트 트리 | 누적 합 |
|:---|:---|:---|:---|
| 업데이트 | O(log N) | O(log N) | O(N) |
| 쿼리 | O(log N) | O(log N) | O(1) |
| 범위 업데이트 | 2BIT 조합 | ✅ 기본 지원 | O(N) |
| 코드 복잡도 | 매우 낮음 | 중간 | 매우 낮음 |
| 메모리 | O(N) | O(4N) | O(N) |

- **📢 섹션 요약 비유**: BIT·세그먼트 트리·누적 합은 세 가지 계산기다. 누적 합(암산 후 기록), BIT(영리한 중간 결과 기록), 세그먼트 트리(완전한 메모장) 순으로 기능은 강해지지만 복잡해진다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 역전 수 (Inversion Count) — BIT 응용

```text
배열에서 i < j이지만 A[i] > A[j]인 쌍의 수 계산:

1. 좌표 압축 후 BIT 초기화
2. 오른쪽에서 왼쪽으로 순회:
   - query(A[i] - 1): 현재 원소보다 작은 값이
     이미 처리된 개수 (= A[i]가 앞에 있으면 역전)
   - update(A[i], 1): 현재 원소 추가

시간: O(N log N), 공간: O(N)
병합 정렬 O(N log N)과 동일하지만 구현이 더 직관적
```

### 2D BIT

```text
2D 범위 합 쿼리:
  update(x, y, delta)  -> O(log M × log N)
  query(x1, y1, x2, y2) -> O(log M × log N)

응용: 2D 히트맵 누적, 행렬 부분 합
```

- **📢 섹션 요약 비유**: 역전 수 계산은 줄 서기 질서 측정이다. 키 순서대로 서야 하는데, 큰 사람이 작은 사람 앞에 있는 쌍의 수가 역전 수다. BIT로 O(N log N)에 계산한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **범위 합 O(log N)** | 업데이트·쿼리 균형 성능 |
| **코드 단순성** | 세그먼트 트리 대비 4~5줄 구현 |
| **캐시 효율** | 1D 배열 기반 좋은 캐시 지역성 |

BIT 개념은 GPU 병렬 계산에서 Prefix Sum(병렬 스캔 알고리즘)으로 확장된다. CUDA Thrust·cuDNN 내부에서 N개 스레드가 동시에 부분 합을 계산하는 Parallel Prefix Sum은 딥러닝 배치 정규화·소프트맥스 계산의 기반이 된다.

- **📢 섹션 요약 비유**: GPU Parallel Prefix Sum은 BIT의 병렬 버전이다. BIT가 직렬로 O(log N) 단계로 합산하는 것을 GPU가 N개 스레드로 동시에 수행하여 O(log N) 병렬 시간으로 처리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>세그먼트 트리</strong> | BIT보다 범용적인 범위 자료 구조 |
| **누적 합** | 정적 배열 범위 합 쿼리 기초 |
| **역전 수** | BIT 대표 응용 문제 |
| **Parallel Prefix Sum** | GPU 병렬 BIT |
| **2D BIT** | 행렬 범위 합 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[누적 합 배열 — O(N) 업데이트 / O(1) 쿼리]
    |
    v
[펜윅 트리 (BIT) — O(logN) 업데이트 / O(logN) 쿼리]
    |
    v
[세그먼트 트리 — 범위 업데이트까지 지원]
    |
    v
[2D BIT / 2D 세그먼트 — 다차원 범위 쿼리]
    |
    v
[GPU Parallel Prefix Sum — 병렬 BIT 딥러닝 응용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 펜윅 트리는 분산 회계 시스템이에요 — 각 담당자가 일부 합계를 미리 기록해서 빠르게 합산해요!
2. 비트 마법(lowbit)으로 어떤 담당자를 찾아가야 할지 O(log N) 만에 알 수 있어요!
3. 구간 합 쿼리가 많은 코딩 테스트와 대규모 데이터 집계에서 가장 많이 쓰이는 도구예요!
