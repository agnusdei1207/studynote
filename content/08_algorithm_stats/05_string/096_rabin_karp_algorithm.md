---
title: "Rabin Karp Algorithm"
date: "2024-03-21"
tags:
  - "studynote-algorithm-stats"
weight: 96
---
## 핵심 인사이트 (3줄 요약)
1. **해시 기반 탐색**: 문자열을 수치화된 해시(Hash) 값으로 변환하여 매칭 여부를 빠르게 판단하는 알고리즘임.
2. **롤링 해시 (Rolling Hash)**: 이전 윈도우의 해시값을 활용하여 다음 윈도우의 해시를 $O(1)$에 계산하는 슬라이딩 윈도우 기법을 사용함.
3. **다중 패턴 탐색**: 하나의 텍스트에서 여러 개의 패턴을 동시에 찾을 때 특히 유리하며, 평균적으로 선형 시간 복잡도를 가짐.

### Ⅰ. 개요 (Context & Background)
- **개념**: 1987년 Michael O. Rabin과 Richard M. Karp가 발표한 알고리즘으로, 단순 문자 비교 대신 지수 함수 기반의 다항식 해시(Polynomial Rolling Hash)를 활용함.
- **필요성**: 해시 충돌(Hash Collision)의 위험이 있으나, 적절한 소수(Prime)와 진법(Base) 선택으로 실무적 활용도를 높임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
#### 1. 롤링 해시의 매커니즘
- **윈도우 이동**: 다음 해시 = (진법 $\times$ (현재 해시 - 첫 글자 가중치) + 새로운 글자) mod 소수.

```text
[ Rabin-Karp Rolling Hash Logic ]
Text:    H E L L O _ W O R L D
Pattern: L L O (Hash Value = P_Hash)

Step 1: Hash("HEL") != P_Hash (Skip)
Step 2: Hash("ELL") != P_Hash (Skip)
Step 3: Hash("LLO") == P_Hash (Potential Match!)

[ Hash Calculation Formula ]
H = (c1 * d^(m-1) + c2 * d^(m-2) + ... + cm * d^0) mod q
- d: Base (e.g., 256 for ASCII)
- q: Large Prime Number
- m: Pattern Length
```

#### 2. 해시 충돌 방지
- 해시값이 일치하더라도 실제로 문자열이 같은지 한 번 더 확인(Verification)하여 정확성을 보장함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 라빈-카프 (Rabin-Karp) | KMP 알고리즘 | 보이어-무어 (Boyer-Moore) |
| :--- | :--- | :--- | :--- |
| **핵심 원리** | 해시 값 비교 | 실패 함수 (LPS) | 스킵 테이블 (Bad Char/Good Suffix) |
| <strong>시간 복잡도</strong> | 평균 $O(N+M)$, 최악 $O(N \cdot M)$ | $O(N+M)$ | $O(N/M)$ |
| **주요 장점** | 다중 패턴 탐색 시 효율적 | 이론적 최악 성능 보장 | 대부분의 실무 데이터에서 최적 |
| <strong>해시 충돌</strong> | 발생 가능 (검증 단계 필요) | 없음 | 없음 |
| **적용 분야** | 표절 검사, 침입 탐지 | 바이너리 탐색, DNA 분석 | 텍스트 검색 (Grep, 에디터) |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- **실무 적용**: 문서 표절 검출(두 문서의 해시 집합 비교), 고정된 시그니처가 많은 네트워크 침입 탐지 시스템.
- **실무적 판단**: 라빈-카프는 단일 패턴 검색에서는 보이어-무어에 밀리지만, <strong>다중 패턴 동시 검색</strong>이 필요한 보안 장비나 <strong>문서 유사도 비교</strong>에서 압도적인 가치를 지님. 해시 함수 설계 시 오버플로우와 모듈러 연산 최적화가 필수적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 복잡한 문자열 비교 문제를 수치 계산 문제로 전환하여 대규모 데이터 집합의 유사성을 빠르게 정량화함.
- **결론**: 알고리즘과 대수학의 융합을 보여주는 사례로, 현대 데이터 마이닝과 보안 기술의 근간이 되는 알고리즘임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 문자열 탐색, 해시 함수
- **하위 개념**: Rolling Hash, Fingerprinting
- **융합 응용**: Bloom Filter (공간 효율적 필터링)

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 문자열 탐색, 해시 함수]
    |
    v
[하위 개념: Rolling Hash, Fingerprinting]
    |
    v
[융합 응용: Bloom Filter (공간 효율적 필터링)]
```

이 흐름도는 상위 개념: 문자열 탐색, 해시 함수에서 출발해 융합 응용: Bloom Filter (공간 효율적 필터링)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 가방 속에 숨긴 장난감 이름을 하나하나 확인하는 대신, 가방의 "무게"를 먼저 재보는 것과 같아요.
2. 무게가 같으면 그제야 가방을 열어 진짜 장난감이 들어있는지 확인하는 영리한 방법이죠.
3. 기차 칸을 하나씩 이동하며 무게를 잴 때, 내리는 사람 몸무게는 빼고 타는 사람 몸무게는 더하면 금방 계산되겠죠?
