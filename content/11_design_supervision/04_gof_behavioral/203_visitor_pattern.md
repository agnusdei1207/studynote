---
title: "Visitor Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 203
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Visitor (방문자) 패턴은 데이터 구조(Element)와 그 위에서 수행되는 연산(Visitor)을 분리하여, 데이터 구조를 변경하지 않고도 새로운 연산을 추가할 수 있게 한다.
> 2. **가치**: OCP (Open-Closed Principle, 개방-폐쇄 원칙)의 비용을 캡슐화가 지불하는 트레이드오프 패턴 — 연산 추가는 쉽지만, 새 Element 추가는 모든 Visitor를 수정해야 한다.
> 3. **판단 포인트**: 데이터 구조가 안정적이고 연산이 자주 추가되는 경우, 특히 컴파일러 AST (Abstract Syntax Tree) 처리처럼 다양한 분석·변환이 필요한 상황에 적합하다.

---

## Ⅰ. 개요 및 필요성
트리 구조(컴포지트 패턴)에서 모든 노드를 순회하며 직렬화, 출력, 코드 생성 등을 해야 한다고 가정하자. 이를 각 Element 클래스에 직접 추가하면:

```
  // 연산 하나가 추가될 때마다 모든 Element 클래스 수정
  class NumberNode {
      serialize() { ... }     // 연산 1
      prettyPrint() { ... }   // 연산 2  <- 추가됨
      generateCode() { ... }  // 연산 3  <- 추가됨
      typeCheck() { ... }     // 연산 4  <- 추가됨
  }
  // Element가 10개면, 연산 1개 추가 = 10개 클래스 수정
```

Visitor 패턴은 연산을 <strong>별도 Visitor 클래스</strong>로 분리하여 이 문제를 해결한다.

Visitor의 핵심 메커니즘. 일반적인 단일 디스패치(Single Dispatch)는 메서드를 호출하는 객체 타입만으로 메서드가 결정된다. Visitor는 <strong>두 객체의 타입</strong>으로 최종 메서드가 결정된다:

```
  element.accept(visitor)   -> 1st dispatch: element의 타입으로 accept() 결정
    +- visitor.visit(this)  -> 2nd dispatch: visitor의 타입으로 visit() 결정

  결과: Element 타입 × Visitor 타입 -> 구체적 연산 메서드
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 박물관 도슨트(Visitor)가 전시물(Element)을 방문할 때, 전시물마다 다른 설명을 한다. 새로운 전시 프로그램(연산)을 추가할 때 전시물(Element)을 바꾸지 않아도 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  «interface»              «interface»
  Element                  Visitor
  -------------            --------------------------
  + accept(Visitor)        + visit(ConcreteElementA)
        ^                  + visit(ConcreteElementB)
        |                        ^
   +----+----+          +--------+--------+
   v         v          v                 v
 ElemA     ElemB    ConcreteVisitor1  ConcreteVisitor2
 accept(v){        (코드 생성)        (타입 체크)
   v.visit(this)
 }
```

```
  AST 구조 (Expression Tree):

           AddNode (NonTerminal)
          /         \
   NumberNode(3)   MulNode (NonTerminal)
                  /        \
           NumberNode(4)  NumberNode(5)

  Visitor 1: PrettyPrintVisitor
    -> "3 + (4 * 5)"

  Visitor 2: EvaluateVisitor
    -> 3 + (4 × 5) = 23

  Visitor 3: TypeCheckVisitor
    -> 모든 노드가 Number 타입인지 검증
```

```java
// Element 인터페이스
interface Expression {
    void accept(ExpressionVisitor visitor);
}

// ConcreteElement
class NumberNode implements Expression {
    int value;
    @Override
    public void accept(ExpressionVisitor visitor) {
        visitor.visit(this);  // Double Dispatch 2nd hop
    }
}

// Visitor 인터페이스
interface ExpressionVisitor {
    void visit(NumberNode node);
    void visit(AddNode node);
    void visit(MulNode node);
}

// ConcreteVisitor
class EvaluateVisitor implements ExpressionVisitor {
    private int result;
    @Override
    public void visit(NumberNode node) {
        result = node.value;
    }
    // ...
}
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

- **📢 섹션 요약 비유**: 세금 조사관(Visitor)이 각 기업(Element)을 방문한다. 기업은 문을 열어주기만 하면 되고(accept), 세금 계산 방식은 조사관(Visitor)이 결정한다.

---

## Ⅲ. 비교 및 연결
| 변경 유형 | Visitor 패턴 | 일반 Element 내부 구현 |
|:---|:---|:---|
| <strong>새 연산(Visitor) 추가</strong> | ✅ 쉬움 (새 Visitor 클래스 추가) | ❌ 어려움 (모든 Element 수정) |
| **새 Element 추가** | ❌ 어려움 (모든 Visitor에 visit() 추가) | ✅ 쉬움 (새 Element 클래스만 추가) |
| **캡슐화** | ❌ Element 내부를 Visitor에 노출 | ✅ 보존 |
| <strong>코드 응집도</strong> | 연산별 응집 (한 Visitor = 한 기능) | Element별 응집 |

| 패턴 | Visitor와의 관계 |
|:---|:---|
| Composite (컴포지트) | Visitor가 순회하는 구조 제공 |
| Iterator (이터레이터) | Element 구조 순회를 Iterator로 위임 가능 |
| Strategy (전략) | Visitor의 알고리즘이 전략처럼 교체 가능 |
| Command (커맨드) | Visitor를 Command로 구현하면 실행 취소 가능 |

- **📢 섹션 요약 비유**: Visitor 패턴은 "수술 없이 새 장기를 추가"하는 게 아니라, "기존 몸(Element)에 새 의사(Visitor)를 붙이는 것". 몸은 그대로지만 의사가 다르면 다른 처치가 가능하다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```
  DOM Tree:
  <html>
    <body>
      <p>Hello</p>
      <div>World</div>
    </body>
  </html>

  Visitor 1: HTMLValidatorVisitor
    -> <p>, <div> 태그 유효성 검사

  Visitor 2: TextExtractorVisitor
    -> "Hello", "World" 텍스트 추출

  Visitor 3: SecurityScanVisitor
    -> XSS (Cross-Site Scripting) 스크립트 탐지
```

```
  Visitor 적합 판단:
  +------------------------------------------------+
  |  데이터 구조(Element)의 변화가 적고,            |
  |  그 위에서 수행하는 연산(Operation)이           |
  |  자주 추가·변경되는가?                          |
  |                                                |
  |  YES -> Visitor Pattern 적용                    |
  |  NO  -> 일반 메서드 또는 Strategy 적용          |
  +------------------------------------------------+
```

- **Double Dispatch** 메커니즘 명확히 설명 (두 번의 동적 바인딩)
- OCP 달성의 **비용**: 캡슐화 약화 (Element 내부를 Visitor에 노출)
- **트레이드오프 명시**: 연산 추가 쉬움 ↔ Element 추가 어려움

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 도서관 책(Element)들은 그 자리에 있고, 방문하는 사서(Visitor)가 재고 확인, 연체료 계산, 대출 기록 등 다른 일을 한다. 책은 항상 문을 열어줄(accept) 뿐이다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 연산의 응집성 향상 | 관련 연산이 한 Visitor 클래스에 집중 |
| SRP 달성 | Element는 구조, Visitor는 연산 담당 분리 |
| 기능 추가 용이 | 새 연산 = 새 Visitor 클래스만 추가 |
| 복합 구조 순회 | Composite 패턴과 자연스럽게 결합 |

- <strong>Element 추가 시 모든 Visitor 수정</strong> -> 추상 기본 구현(Default 메서드)으로 완화 가능
- **캡슐화 약화** -> 내부를 노출하는 범위를 Package-Private 등으로 제한

Visitor (방문자) 패턴은 안정된 데이터 구조 위에 <strong>다양한 연산을 플러그인처럼 추가</strong>해야 하는 상황에서 가장 빛을 발한다. 컴파일러 설계, AST (Abstract Syntax Tree) 분석, DOM 조작 등이 대표적이다. OCP와 캡슐화의 트레이드오프를 명확히 이해하고 적용해야 한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Visitor는 "기존 공장(Element)의 라인을 멈추지 않고 새 품질 검사원(Visitor)을 투입"하는 것. 공장은 문만 열어주면 된다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | ConcreteVisitor | 실제 연산 구현체 |
| 연관 개념 | Composite Pattern | Visitor가 순회하는 트리 구조 |
| 연관 개념 | Double Dispatch | Visitor의 핵심 메커니즘 |
| 연관 개념 | AST (Abstract Syntax Tree) | 컴파일러 적용 사례 |
| 연관 개념 | OCP (Open-Closed Principle) | 연산 확장에서 달성, Element 확장에서 비용 |

### 📈 관련 키워드 및 발전 흐름도
Composite 구조 -> 방문자 패턴 -> AST 분석/코드 생성

### 👶 어린이를 위한 3줄 비유 설명
1. 동물원의 동물들(Element)은 우리 안에 있고, 수의사(Visitor)가 차례로 방문해요.
2. 수의사마다 하는 일이 달라요: 예방접종 수의사, 치과 수의사, 건강검진 수의사!
3. 동물들은 그냥 "들어오세요"(accept)만 하면 되고, 어떤 검사를 받는지는 수의사가 결정해요.
