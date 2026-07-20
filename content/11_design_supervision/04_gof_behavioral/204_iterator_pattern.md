---
title: "Iterator Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 204
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Iterator (이터레이터, 반복자) 패턴은 컬렉션(Collection)의 내부 구현(배열인지, 링크드리스트인지, 트리인지)을 완전히 숨긴 채 원소들을 순차적으로 접근하는 통일된 인터페이스를 제공한다.
> 2. **가치**: `hasNext()` + `next()` 인터페이스 하나로 모든 종류의 컬렉션을 동일하게 순회할 수 있어, 알고리즘과 자료구조를 완전히 분리한다.
> 3. **판단 포인트**: 컬렉션 구조를 바꾸더라도 순회 코드를 수정할 필요가 없어야 할 때, 또는 여러 순회 방식(깊이 우선, 너비 우선)을 동시에 지원해야 할 때 적용한다.

---

## Ⅰ. 개요 및 필요성
컬렉션 종류마다 다른 순회 방법이 필요하다:

```java
// 배열 순회
for (int i = 0; i < array.length; i++) { use(array[i]); }

// LinkedList 순회
Node curr = head;
while (curr != null) { use(curr.data); curr = curr.next; }

// 트리 순회 (DFS)
void traverse(TreeNode node) {
    if (node == null) return;
    use(node.data);
    traverse(node.left);
    traverse(node.right);
}
```

컬렉션이 배열에서 링크드리스트로 변경되면, 이 컬렉션을 사용하는 <strong>모든 순회 코드를 수정</strong>해야 한다.

```java
// Iterator 통일 인터페이스
Iterator<String> it = collection.iterator();
while (it.hasNext()) {
    String item = it.next();  // 내부 구현에 무관하게 동일한 코드
    use(item);
}
```

Collection이 배열이든, 링크드리스트든, 트리든 <strong>순회 코드는 동일</strong>하다.

| 언어 | Iterator 인터페이스 | for-each 지원 |
|:---|:---|:---|
| Java | `Iterator<T>`: `hasNext()`, `next()` | `Iterable<T>` 구현 시 |
| Python | `__iter__()`, `__next__()` | `for x in obj:` |
| JavaScript | `Symbol.iterator`, `{value, done}` | `for...of` |
| C# | `IEnumerator<T>`: `MoveNext()`, `Current` | `foreach` |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: TV 리모컨 채널 버튼(Iterator) — 아날로그인지 디지털인지, 케이블인지 IPTV인지 몰라도 "다음 채널" 버튼은 항상 같은 방식으로 동작한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  «interface»                   «interface»
  Iterable<T>                   Iterator<T>
  --------------                ------------------
  + iterator(): Iterator<T>     + hasNext(): boolean
        ^                       + next(): T
        |                       + remove()  [optional]
  ConcreteCollection                  ^
  ------------------                  |
  + iterator()                 ConcreteIterator
    -> new ConcreteIterator(this)  - collection
                                  - currentIndex
                                  + hasNext()
                                  + next()
```

```
  외부 이터레이터 (External Iterator)
  -------------------------------------
  Client가 Iterator를 직접 제어

  Iterator<T> it = list.iterator();
  while (it.hasNext()) {
      T item = it.next();  // Client가 next() 호출
      if (needStop(item)) break;  // 중간 탈출 가능
  }

  장점: 세밀한 제어 가능, 중간 탈출 가능
  단점: 클라이언트 코드가 복잡

  -------------------------------------
  내부 이터레이터 (Internal Iterator)
  -------------------------------------
  Collection이 순회를 제어하고 콜백 호출

  list.forEach(item -> process(item));
  list.stream().filter(x -> x > 0).map(x -> x * 2).collect(...);

  장점: 코드 간결, 함수형 스타일
  단점: 중간 탈출 어려움 (anyMatch, findFirst로 보완)
```

```
  파일 시스템 트리 (Composite)

  root/
  +-- docs/
  |   +-- readme.txt
  |   +-- design.pdf
  +-- src/
      +-- main.java
      +-- util/
          +-- helper.java

  DFSIterator (깊이 우선 탐색):
  root -> docs -> readme.txt -> design.pdf -> src -> main.java -> util -> helper.java

  BFSIterator (너비 우선 탐색):
  root -> docs -> src -> readme.txt -> design.pdf -> main.java -> util -> helper.java

  // 동일한 Collection에 다른 Iterator 적용
  Iterator<File> dfs = fileSystem.dfsIterator();
  Iterator<File> bfs = fileSystem.bfsIterator();
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

```text
+--------------+    +--------------+    +--------------+
| Input/State  |--->| Control Point |--->| Output/Action |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 도서관 책 목록(Collection)을 검색할 때, 사서가 책장 어떻게 정리했는지 몰라도 "다음 책 주세요"라고 하면 된다 — 그것이 Iterator.

---

## Ⅲ. 비교 및 연결
| 항목 | 외부 이터레이터 | 내부 이터레이터 |
|:---|:---|:---|
| **제어권** | 클라이언트 | 컬렉션/람다 |
| **중간 탈출** | `break` 가능 | `anyMatch()` 등으로 제한적 |
| <strong>병렬 처리</strong> | 어려움 | `parallelStream()` 용이 |
| **코드 간결성** | 낮음 | 높음 |
| **상태 저장** | Iterator 객체에 | 없음 (Stateless) |
| **대표 사례** | Java `Iterator`, Python `for` | Java `Stream`, Python 컴프리헨션 |

| 패턴 | Iterator와의 관계 |
|:---|:---|
| Composite (컴포지트) | Iterator가 순회하는 트리 구조 |
| Visitor (방문자) | Iterator로 순회하며 각 요소에 Visitor 적용 |
| Factory Method (팩토리 메서드) | `iterator()` 메서드가 ConcreteIterator를 생성 |
| Memento (메멘토) | Iterator 상태 저장 후 복원 가능 |

- **📢 섹션 요약 비유**: Iterator는 "컨베이어 벨트 위의 상품 스캐너" — 상품이 박스에 담겼든 낱개든, 스캐너는 동일하게 바코드를 읽는다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 고전적 Iterator
Iterator<Order> it = orders.iterator();
while (it.hasNext()) {
    Order o = it.next();
    if (o.getStatus() == COMPLETED && o.getAmount() > 1_000_000) {
        result.add(o);
    }
}

// Stream API (내부 이터레이터 + 함수형)
List<Order> result = orders.stream()
    .filter(o -> o.getStatus() == COMPLETED)
    .filter(o -> o.getAmount() > 1_000_000)
    .collect(Collectors.toList());

// 병렬 처리 (내부 구현 무관)
List<Order> result = orders.parallelStream()
    .filter(o -> o.getStatus() == COMPLETED)
    .collect(Collectors.toList());
```

```python
# Python Generator = 지연 평가(Lazy Evaluation) Iterator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a           # Iterator의 next()를 yield로 표현
        a, b = b, a + b

gen = fibonacci()
for _ in range(10):
    print(next(gen))     # 필요할 때만 계산 (메모리 효율)
```

Generator는 무한 수열을 메모리 효율적으로 구현하는 Iterator의 변형이다.

- Iterator 패턴이 <strong>컬렉션 추상화</strong>의 핵심 메커니즘임을 명시
- Java `for-each` 루프가 내부적으로 `Iterable.iterator()`를 호출함 언급
- 외부/내부 이터레이터의 **트레이드오프** 비교 제시

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Iterator는 "만능 자동 계산기" — 어떤 나라 화폐든 넣으면 원화로 환산해 준다. 화폐 종류(컬렉션 구현)에 상관없이 같은 버튼(hasNext/next)으로 작동한다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 컬렉션-알고리즘 분리 | 데이터 구조 변경 시 순회 코드 무수정 |
| 다중 순회 지원 | 동일 컬렉션에 DFS, BFS 등 여러 Iterator |
| SRP 달성 | 컬렉션은 저장, Iterator는 순회 책임 분리 |
| 지연 평가 가능 | Generator로 메모리 효율적 처리 |

- Iterator 상태를 외부에서 관리하므로 <strong>멀티스레드 환경 동기화</strong> 주의 필요
- 컬렉션 수정 중 순회 시 `ConcurrentModificationException` 위험

Iterator (이터레이터) 패턴은 현대 프로그래밍 언어의 `for-each`, Stream, Generator 등 모든 순회 추상화의 이론적 기반이다. 알고리즘과 자료구조를 분리하는 가장 근본적인 수단으로, 언어 내장 지원으로 자연스럽게 일상화된 패턴이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Iterator는 "지하철 개찰구" — 타는 사람이 학생인지 어른인지, 서울인지 부산인지 관계없이 하나씩 통과시키는 통일된 메커니즘이다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | ConcreteIterator | 구체적 순회 구현 |
| 연관 개념 | Composite Pattern | Iterator가 순회하는 트리 구조 |
| 연관 개념 | Java Stream API | Iterator의 현대적 진화 |
| 연관 개념 | Python Generator | 지연 평가 Iterator |
| 연관 개념 | Visitor Pattern | Iterator로 순회하며 Visitor 적용 |

### 📈 관련 키워드 및 발전 흐름도
Collection 추상화 -> 이터레이터 패턴 -> Stream/파이프라인

### 👶 어린이를 위한 3줄 비유 설명
1. 사탕 상자(컬렉션)에서 사탕을 꺼내는 방법이 상자마다 달라도, "다음 사탕 주세요"라는 말은 항상 같아요.
2. Iterator는 상자 안을 들여다보지 않고도 하나씩 꺼낼 수 있게 해주는 마법이에요.
3. Java의 `for-each`, Python의 `for` 루프가 바로 이 마법을 쓰고 있어요!
