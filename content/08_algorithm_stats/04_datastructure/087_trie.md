---
title: "Trie"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
weight: 87
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트라이(Trie, Prefix Tree)는 문자열 집합을 저장하고 검색하는 트리 자료 구조다. 루트에서 리프까지의 경로가 하나의 문자열을 나타내며, 공통 접두사(Prefix)를 공유하는 문자열들이 같은 노드를 공유한다.
> 2. **가치**: 트라이에서 문자열 검색 시간은 O(L) (L = 문자열 길이)로, 비교 기반 검색(O(N log N))이나 해시맵(충돌 시 O(N))보다 최악 성능이 보장된다. 자동 완성·사전 검색·IP 라우팅에서 핵심 자료 구조다.
> 3. **판단 포인트**: 트라이의 단점은 메모리다. 각 노드가 26개(알파벳) 또는 N개의 자식 포인터를 가져야 해서 희소(Sparse) 데이터에선 메모리 낭비가 크다. 압축 트라이(Patricia Trie, Radix Tree)가 이를 해결한다.

---

## Ⅰ. 개요 및 필요성

```text
트라이 구조 ("CAT", "CAR", "CAN", "DOG" 삽입):

      루트
      /       C    D
     |    |
     A    O
   / | \  |
  T  R  N  G
(CAT)(CAR)(CAN)(DOG)

공통 접두사 "CA"를 두 노드가 공유!
검색 "CAR": C->A->R 이동, O(3) = O(L)
```

- **📢 섹션 요약 비유**: 트라이는 도서관 분류 시스템이다. "컴퓨터과학" 서가 안에 "컴퓨터과학-알고리즘", "컴퓨터과학-네트워크"가 함께 있어서 "컴퓨터과학"이라는 공통 접두사를 공유한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 트라이 노드 구조

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # 자식 노드 딕셔너리
        self.is_end = False    # 단어 끝 여부

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):       # O(L)
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):       # O(L)
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix): # O(L) - 자동완성!
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True  # 접두사 존재 확인
```

- **📢 섹션 요약 비유**: 트라이 삽입은 주소록에 연락처 추가와 같다. 성(C)->이름 첫 글자(A)->두 번째 글자(T) 순으로 트리를 따라 이동하며 새 분기가 필요한 곳에서만 새 노드를 만든다.

---

## Ⅲ. 비교 및 연결

| 비교 | 트라이 | 해시맵 | BST |
|:---|:---|:---|:---|
| 검색 시간 | O(L) | O(L) 평균 | O(L log N) |
| 접두사 검색 | ✅ O(L) | ❌ O(N) | ❌ O(N) |
| 메모리 | 많음 (포인터) | 적음 | 중간 |
| 자동 완성 | ✅ 최적 | ❌ | ❌ |

- **📢 섹션 요약 비유**: 트라이·해시맵·BST는 책 찾는 방법이다. 제목 전체 암기(해시맵), 알파벳 순 사전(BST), 접두사로 관련 책 모아보기(트라이). 접두사 검색에는 트라이가 압도적이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 자동 완성 구현

```python
def autocomplete(trie, prefix, max_results=5):
    """접두사로 시작하는 단어 모두 반환"""
    results = []

    # 접두사까지 이동
    node = trie.root
    for ch in prefix:
        if ch not in node.children:
            return []
        node = node.children[ch]

    # DFS로 모든 완성 단어 수집
    def dfs(node, current):
        if len(results) >= max_results:
            return
        if node.is_end:
            results.append(current)
        for ch, child in node.children.items():
            dfs(child, current + ch)

    dfs(node, prefix)
    return results
```

### 압축 트라이 (Radix Tree)

```text
일반 트라이:
  C -> A -> T (3 노드)

압축 트라이:
  CAT (1 노드에 "CAT" 저장)
  CAR -> R (공통 접두사 "CA" 이후 분기)

  "CA" --- "T" (CAT)
            +-- "R" (CAR)
            +-- "N" (CAN)
```

- **📢 섹션 요약 비유**: 압축 트라이는 주소 약어 시스템이다. "서울특별시 강남구"를 매번 쓰는 대신 공통 부분을 하나로 압축하여 "서울강남-역삼", "서울강남-삼성"으로 저장하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **자동 완성** | 접두사 기반 O(L) 검색 |
| **사전 구현** | 효율적 단어 저장·검색 |
| <strong>IP 라우팅</strong> | CIDR 접두사 매칭 (Longest Prefix Match) |

LLM(대형 언어 모델)에서 트라이는 토큰화(Tokenization) 단계에서 활용된다. BPE(Byte Pair Encoding)·WordPiece 같은 서브워드 토큰화에서 어휘 사전 탐색에 트라이 기반 빠른 매칭이 사용된다. 수백만 토큰의 어휘에서 O(L) 검색이 LLM 추론 속도를 지킨다.

- **📢 섹션 요약 비유**: LLM 토큰화의 트라이는 사전 빠른 검색이다. 문장 "Hello World"를 단어로 분리할 때, 수백만 단어 사전에서 "Hell", "Hello", "HelloW"... 를 빠르게 매칭하는 것이 트라이의 역할이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>압축 트라이</strong> | 메모리 효율화 (Radix Tree) |
| **자동 완성** | 트라이의 핵심 응용 |
| **Longest Prefix Match** | IP 라우팅 트라이 활용 |
| <strong>BPE 토큰화</strong> | LLM 어휘 트라이 매칭 |
| <strong>Aho-Corasick</strong> | 다중 패턴 매칭 트라이 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[해시맵·BST — 일반 문자열 저장·검색]
    |
    v
[트라이 (Trie) — 접두사 공유 O(L) 검색]
    |
    v
[압축 트라이 (Radix Tree) — 메모리 최적화]
    |
    v
[Aho-Corasick — 다중 패턴 매칭 (실패 링크 추가)]
    |
    v
[LLM 토큰화 — BPE 어휘 사전 트라이 매칭]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 트라이는 도서관 분류 시스템이에요 — 공통 시작 글자끼리 모여서 찾기 쉬워요!
2. "CA"로 시작하는 단어 모두 찾기(자동 완성)가 O(L)로 매우 빠르게 동작해요!
3. 구글 검색창 자동 완성, 사전 앱, 네트워크 라우터가 모두 트라이를 사용해요!
