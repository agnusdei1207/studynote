---
title: "Rb Tree"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
weight: 89
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Red-Black Tree는 각 노드에 색(Red/Black)을 부여하는 5가지 규칙으로 균형을 유지하는 자가 균형 BST다. AVL보다 균형 조건이 덜 엄격하지만, 삽입·삭제가 더 빠르다.
> 2. **가치**: Red-Black Tree의 높이는 2 log₂(N+1) 이하로 보장된다. 따라서 검색·삽입·삭제 모두 O(log N)이다. C++ STL의 map/set/multimap, Java의 TreeMap/TreeSet, Linux 커널의 CFS 스케줄러가 Red-Black Tree를 사용한다.
> 3. **판단 포인트**: Red-Black Tree의 규칙 중 핵심은 "빨간 노드의 자녀는 반드시 검정"이다. 이를 위반하면 삽입 후 회전(Rotation) + 재색칠(Recoloring)로 규칙을 복구한다.

---

## Ⅰ. 개요 및 필요성

```text
Red-Black Tree 5가지 규칙:
  1. 모든 노드는 Red 또는 Black
  2. 루트는 반드시 Black
  3. 모든 NIL(Null) 리프는 Black
  4. Red 노드의 두 자녀는 반드시 Black
     (Red-Red 연속 금지)
  5. 어떤 노드에서 리프까지의 경로에
     포함된 Black 노드 수는 동일 (Black Height)

-> 5 규칙으로 트리 높이 ≤ 2 log₂(N+1) 보장
```

- **📢 섹션 요약 비유**: Red-Black 규칙은 교통 신호 규칙이다. "빨간불(Red) 뒤에는 반드시 초록불(Black)"처럼, Red 노드 뒤에는 반드시 Black 노드가 와야 한다는 규칙이 트리 균형을 유지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 삽입 후 규칙 복구

```text
새 노드 삽입 -> 항상 Red로 삽입
    |
    v
규칙 4 위반? (Red-Red 연속)
    +- 삼촌이 Red -> 재색칠(Recoloring)
    |   부모·삼촌 -> Black
    |   조부모 -> Red
    |   (조부모로 이동하여 재확인)
    |
    +- 삼촌이 Black -> 회전+재색칠
        LL/LR/RL/RR 케이스별 처리
```

### C++ STL map 내부 구조

```text
std::map<key, value> 내부:
  - Red-Black Tree 기반
  - 삽입: O(log N)
  - 검색: O(log N)
  - 범위 조회: 중위 순회 O(K + log N)
  - K개 반환 조회

예: std::map.lower_bound(key)
    -> O(log N)으로 key 이상의 첫 값 검색
    -> 정렬된 데이터 범위 검색에 최적
```

- **📢 섹션 요약 비유**: RB Tree 재색칠은 빨간불 연속 신호등 수리다. 빨간불 두 개가 연속(Red-Red 위반)이면, 앞 신호등을 초록(Black)으로 바꾸고 필요하면 교차로 구조(회전)도 변경한다.

---

## Ⅲ. 비교 및 연결

| 비교 | AVL | Red-Black | Skip List |
|:---|:---|:---|:---|
| 균형 | 엄격 (±1) | 유연 (2×) | 확률적 |
| 검색 | 약간 빠름 | 약간 느림 | O(log N) 평균 |
| 삽입/삭제 | 약간 느림 | 약간 빠름 | O(log N) 평균 |
| 병렬화 | 어려움 | 어려움 | 쉬움 |
| 사용처 | 읽기 집중 | 표준 라이브러리 | Redis, LevelDB |

- **📢 섹션 요약 비유**: AVL·RB·Skip List는 세 정렬 방식이다. AVL(완벽한 ABC 정리), RB(빠른 정리, 약간 느슨), Skip List(확률적 정리, 병렬 가능)로 상황에 맞게 선택한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Linux CFS 스케줄러의 RB Tree

```text
Linux Completely Fair Scheduler (CFS):
  - 프로세스를 가상 런타임(vruntime) 키로 RB Tree 관리
  - vruntime 가장 작은 프로세스 = 가장 적게 실행된 프로세스
  - leftmost 노드 선택 O(1) (캐싱 최적화)
  - 삽입(생성/wakeup): O(log N)
  - 삭제(스케줄 아웃): O(log N)
```

### Java TreeMap 활용

```java
// TreeMap: RB Tree 기반 정렬 Map
TreeMap<Integer, String> ranking = new TreeMap<>();
ranking.put(1000, "Alice");
ranking.put(850, "Bob");
ranking.put(1200, "Carol");

// 상위 2개: O(log N)
System.out.println(ranking.headMap(1100));  // {1000: Alice, 850: Bob}

// 범위 검색: O(log N + K)
System.out.println(ranking.subMap(800, 1100)); // 800-1100 범위
```

- **📢 섹션 요약 비유**: CFS의 RB Tree는 공정한 순번 대기 시스템이다. 가장 적게 CPU를 사용한 프로세스(vruntime 최소)를 RB Tree 맨 왼쪽 노드로 즉시 찾아서 CPU를 배정한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **O(log N) 보장** | 삽입·삭제 집중 환경에서 빠른 균형 |
| **범용성** | STL·JVM·Linux 커널 표준 채택 |
| **정렬 유지** | 범위 검색·순위 관리에 최적 |

Persistent Red-Black Tree는 함수형 프로그래밍에서 불변(Immutable) 자료 구조로 활용된다. 버전별 트리 스냅샷을 O(log N) 공간만 추가하여 유지하는 구조적 공유(Structural Sharing)로 함수형 언어(Clojure·Haskell)의 불변 Map/Set을 효율적으로 구현한다.

- **📢 섹션 요약 비유**: Persistent RB Tree는 Git과 비슷하다. 매 변경마다 전체를 복사하지 않고, 변경된 경로만 새로 만들어서 이전 버전을 O(log N) 추가 공간으로 유지한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **AVL 트리** | RB의 더 엄격한 균형 대안 |
| **B+Tree** | 디스크 기반 DB 인덱스 확장 |
| **Linux CFS** | RB Tree 기반 공정 스케줄러 |
| **STL map/TreeMap** | RB Tree 표준 라이브러리 적용 |
| **Persistent RB Tree** | 함수형 불변 자료 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
[BST — 이진 탐색, 최악 O(N)]
    |
    v
[AVL — 엄격 균형, 읽기 최적화]
    |
    v
[Red-Black — 유연 균형, 삽입/삭제 최적화]
    |
    v
[Linux CFS / STL / JVM — 표준 라이브러리 채택]
    |
    v
[Persistent RB — 함수형 불변 자료 구조]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Red-Black 트리는 빨간불 연속 금지 규칙으로 균형을 유지하는 트리예요!
2. C++의 map과 Java의 TreeMap이 모두 Red-Black 트리를 사용해서 정렬과 검색을 O(log N)으로 해요!
3. Linux 커널도 이 트리로 프로세스 스케줄링을 공정하게 관리한답니다!
