---
title: "Boyer Moore Algorithm"
date: "2024-03-21"
tags:
  - "studynote-algorithm-stats"
weight: 95
---
## 핵심 인사이트 (3줄 요약)
1. **역방향 비교의 승리**: 패턴의 뒤쪽(오른쪽)부터 거꾸로 비교하여 매칭되지 않는 텍스트를 대량으로 건너뛰는(Skip) 고성능 문자열 탐색 알고리즘임.
2. **두 가지 이동 규칙**: 나쁜 문자 규칙(Bad Character Rule)과 착한 접미사 규칙(Good Suffix Rule)을 사용하여 매칭 실패 시 최대 이동 거리를 결정함.
3. **실무형 최강자**: 긴 패턴과 큰 문자 집합(ASCII, Unicode) 환경에서 KMP보다 실질적으로 훨씬 빠른 속도를 보이며 $O(N/M)$ 수준의 평균 성능을 달성함.

### Ⅰ. 개요 (Context & Background)
- **개념**: 1977년 Robert S. Boyer와 J Strother Moore가 발표한 알고리즘으로, 현대 텍스트 에디터의 '찾기' 기능과 UNIX의 `grep` 등에서 표준으로 사용됨.
- **철학**: "텍스트의 문자가 패턴에 없다면, 그 패턴은 절대 해당 위치를 포함할 수 없다"는 원리를 활용하여 대담한 점프를 수행함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
#### 1. 핵심 메커니즘 (Backward Match & Skip)
- **오른쪽에서 왼쪽으로 비교**: 패턴의 마지막 문자가 텍스트와 다르면 바로 스킵함.

```text
[ Boyer-Moore Skip Logic ]
Text:    X X X X X A B C D X X X
Pattern: T E S T
                 ^ (Start comparing from here)
                 Mismatch: 'A' is not in "TEST"
                 Action: Jump pattern past 'A'

Result:  X X X X X A B C D X X X
                   T E S T
```

#### 2. 두 가지 점프 테이블
- **Bad Character Rule**: 텍스트의 불일치 문자가 패턴 내에 존재하는지 확인하여, 있다면 가장 오른쪽 위치에 맞춰 이동하고 없으면 통째로 건너뜀.
- **Good Suffix Rule**: 이미 매칭된 접미사 부분이 패턴 내의 다른 위치에 존재하는지 확인하여 최적의 이동 거리를 계산함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 보이어-무어 (Boyer-Moore) | KMP 알고리즘 | 호스풀 (Horspool) 변형 |
| :--- | :--- | :--- | :--- |
| **비교 순서** | 뒤 -> 앞 (Backwards) | 앞 -> 뒤 (Forwards) | 뒤 -> 앞 |
| <strong>평균 시간 복잡도</strong> | $O(N/M)$ (매우 우수) | $O(N+M)$ | $O(N/M)$ |
| <strong>최악 시간 복잡도</strong> | $O(N \cdot M)$ (이론적) | $O(N+M)$ | $O(N \cdot M)$ |
| **주요 장점** | 패턴이 길수록 빨라짐 | 최악의 경우 성능 보장 | 구현이 단순 (Bad Char만 사용) |
| <strong>공간 복잡도</strong> | $O(\Sigma + M)$ | $O(M)$ | $O(\Sigma)$ |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- **실무 적용**: GNU `grep` 도구, 텍스트 에디터의 검색 엔진, 대용량 로그 파일 분석 시스템.
- **실무적 판단**: 이론적 최악 시간 복잡도는 KMP가 낫지만, 실제 데이터 환경(Sparse match)에서는 보이어-무어가 압도적인 성능 우위를 점함. 현대 시스템 아키텍처에서는 메모리 대역폭을 절약하는 스킵 기능이 매우 중요하므로, 보이어-무어 또는 그 변형인 Boyer-Moore-Horspool이 실질적인 표준임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 수 기가바이트(GB) 규모의 빅데이터 내에서 특정 패턴을 검색할 때 인덱스 없이도 초고속 탐색이 가능함.
- **결론**: 보이어-무어는 "최적화는 무엇을 할 것인가뿐만 아니라, 무엇을 하지 않을 것인가에 대한 고민"임을 보여주는 알고리즘의 정수임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 문자열 탐색 (String Searching)
- **하위/변형**: Horspool Algorithm, Sunday Algorithm (스킵 성능 극대화)
- **관련 자료구조**: 전처리 테이블 (Pre-processing Tables)

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 문자열 탐색 (String Searching)]
    |
    v
[하위/변형: Horspool Algorithm, Sunday Algorithm (스킵 성능 극대화)]
    |
    v
[관련 자료구조: 전처리 테이블 (Pre-processing Tables)]
```

이 흐름도는 상위 개념: 문자열 탐색 (String Searching)에서 출발해 관련 자료구조: 전처리 테이블 (Pre-processing Tables)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 책에서 특정 단어를 찾을 때, 첫 글자부터 안 보고 끝 글자를 먼저 본 다음 아니면 확 넘겨버리는 아주 똑똑한 방법이에요.
2. 줄을 서 있는 친구들 중 "철수"를 찾을 때, 뒤통수만 보고 아니면 다음 줄로 바로 가는 것과 같아요.
3. 매번 한 걸음씩 걷는 게 아니라, 장애물을 미리 보고 "여긴 없네!" 하며 멀리뛰기를 하는 거예요.
