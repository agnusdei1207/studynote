---
title: "Double Dispatch / Visitor Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 229
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Double Dispatch (더블 디스패치)는 메서드 호출이 **두 객체의 런타임 타입** 모두를 기반으로 결정되는 메커니즘이며, Visitor (방문자) 패턴은 Java의 단일 디스패치(Single Dispatch) 한계를 `accept(visitor) -> visitor.visit(this)` 두 번의 가상 호출(Virtual Call)로 더블 디스패치를 구현하는 GoF 패턴이다.
> 2. **가치**: 요소(Element) 클래스 계층을 변경하지 않고 새로운 연산(Visitor)을 추가할 수 있어, <strong>Open/Closed Principle(개방-폐쇄 원칙)</strong> 을 지키면서 타입별 동작을 확장한다.
> 3. **판단 포인트**: 요소 타입은 고정적이지만 연산이 자주 추가되는 경우 Visitor — 반대로 연산은 고정적이지만 타입이 자주 추가되는 경우 Visitor는 부적합 (모든 Visitor 클래스 수정 필요).

---

## Ⅰ. 개요 및 필요성
Java는 **Single Dispatch** — 메서드 호출 대상 객체의 런타임 타입만으로 다형성이 결정된다:

```java
class Shape { void draw(Renderer r) { r.render(this); } }
class Circle extends Shape { }
class Square extends Shape { }

class Renderer {
    void render(Shape s)  { ... } // 어떤 Shape든 이 메서드 호출됨!
    void render(Circle c) { ... } // 오버로딩은 컴파일 타임 결정
    void render(Square s) { ... } // -> 런타임에 Circle/Square 구분 불가
}

Shape shape = new Circle(); // 런타임 타입: Circle
renderer.render(shape);     // 컴파일 타임 타입: Shape -> render(Shape) 호출
                            // render(Circle)이 호출되길 원하지만 불가
```

**문제**: 인수 타입에 대한 런타임 다형성이 필요한데, Java 오버로딩은 컴파일 타임에 결정된다.

```
1번 디스패치: shape.accept(visitor)
  -> shape의 런타임 타입(Circle)이 Circle::accept를 호출

2번 디스패치: visitor.visit(this)
  -> this의 컴파일 타입이 Circle -> visitor.visit(Circle)을 호출
  -> 이 시점의 this는 확실히 Circle 타입 -> 오버로딩 정확히 해결!
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 더블 디스패치는 두 번의 악수로 신원을 확인하는 것 — "나는 Circle이에요(1번 디스패치: accept)" -> "그럼 Circle용 처리를 할게요(2번 디스패치: visit(Circle))"

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+----------------------------------------------------------------+
|                    Visitor Pattern 구조                        |
|                                                                |
|  <<interface>>          <<interface>>                         |
|  Element                Visitor                               |
|  +--------------+       +------------------------+            |
|  | +accept(v:V) |       | +visit(c:Circle): void  |           |
|  +------+-------+       | +visit(s:Square): void  |           |
|         |               | +visit(t:Triangle): void|           |
|    +----+----+          +----------+--------------+           |
|    |         |                +----+----+                     |
|  Circle   Square          DrawVisitor  AreaVisitor            |
|  +------+ +------+        +---------+ +---------+            |
|  |accept| |accept|        |visit(c) | |visit(c) |            |
|  |(v){  | |(v){  |        |visit(s) | |visit(s) |            |
|  | v.visit| | v.visit|     |visit(t) | |visit(t) |            |
|  | (this)| | (this)|      +---------+ +---------+            |
|  |}     | |}     |                                            |
|  +------+ +------+                                            |
|                                                                |
|  호출 흐름:                                                     |
|  shape.accept(drawVisitor)                                     |
|    -> Circle::accept(drawVisitor)  [1번 디스패치: shape 타입]   |
|    -> drawVisitor.visit(this)      [2번 디스패치: this=Circle]  |
|    -> DrawVisitor::visit(Circle)   [Circle 특화 처리]           |
+----------------------------------------------------------------+
```

```java
// Element 인터페이스
interface Shape {
    void accept(ShapeVisitor visitor);
}

// ConcreteElement
class Circle implements Shape {
    private final double radius;
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this);  // 2번 디스패치: this=Circle -> visit(Circle)
    }
}

class Square implements Shape {
    private final double side;
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this);  // 2번 디스패치: this=Square -> visit(Square)
    }
}

// Visitor 인터페이스
interface ShapeVisitor {
    void visit(Circle circle);
    void visit(Square square);
}

// ConcreteVisitor - 연산 추가 시 Element 클래스 수정 없음!
class AreaCalculator implements ShapeVisitor {
    private double totalArea = 0;
    @Override public void visit(Circle c) { totalArea += Math.PI * c.getRadius() * c.getRadius(); }
    @Override public void visit(Square s) { totalArea += s.getSide() * s.getSide(); }
}

class DrawVisitor implements ShapeVisitor {
    @Override public void visit(Circle c) { canvas.drawCircle(c.getRadius()); }
    @Override public void visit(Square s) { canvas.drawSquare(s.getSide()); }
}
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: Visitor는 세금 조사관 — 각 건물(Shape)이 "내가 어떤 건물인지(accept -> this)" 을 신고하면, 조사관(Visitor)은 건물 유형에 맞는 세금 계산법(visit(Circle), visit(Square))을 적용한다.

---

## Ⅲ. 비교 및 연결
| 관점 | Visitor 적합 | Visitor 부적합 |
|:---|:---|:---|
| 요소 타입 변화 | 고정 (드물게 추가) | 자주 추가 |
| 연산 변화 | 자주 추가 | 고정 |
| OCP 측면 | 연산 추가에 닫힘 | 타입 추가에 열림 필요 |
| 적용 예시 | AST 연산 (컴파일러) | Plugin 아키텍처 |

| 패턴 | 관계 | 차이점 |
|:---|:---|:---|
| Strategy | 유사 | Strategy는 런타임 교체, Visitor는 Element 계층에 외부 연산 추가 |
| Iterator + Visitor | 조합 | Iterator로 컬렉션 순회, 각 요소에 Visitor 적용 |
| Composite | 조합 | 트리 구조(Composite)에 Visitor로 연산 추가 (AST 처리) |
| Command | 대비 | Command는 요청을 캡슐화, Visitor는 요소 타입별 연산 캡슐화 |

| 사례 | Visitor 역할 |
|:---|:---|
| 컴파일러 AST 처리 | TypeCheckVisitor, CodeGenVisitor, OptimizeVisitor |
| XML/JSON DOM 처리 | ElementVisitor (노드 타입별 처리) |
| 파일 시스템 탐색 | SizeCalculatorVisitor, FileSearchVisitor |
| 세금 계산기 | TaxVisitor (상품 유형별 세율 적용) |

- **📢 섹션 요약 비유**: 컴파일러에서 AST(Abstract Syntax Tree) 노드들은 고정(IntNode, AddNode, FunctionCallNode)되어 있지만, 연산(타입 체크, 코드 생성, 최적화)은 계속 추가됨 -> Visitor 패턴이 이상적인 이유.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// Java 21 pattern matching (switch expression) — Visitor 대안
sealed interface Shape permits Circle, Square, Triangle {}
record Circle(double radius) implements Shape {}
record Square(double side)  implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle c  -> Math.PI * c.radius() * c.radius();
        case Square s  -> s.side() * s.side();
        // 컴파일러가 모든 케이스 처리 여부 검사 -> 타입 안전
    };
}
// 단, 새 Shape 타입 추가 시 모든 switch 수정 필요 (Visitor와 동일 문제)
```

```java
// 컴파일러의 AST Visitor 예시
interface AstVisitor {
    void visit(NumberLiteral node);
    void visit(BinaryExpression node);
    void visit(FunctionCall node);
    void visit(IfStatement node);
}

class TypeChecker implements AstVisitor {
    @Override
    public void visit(BinaryExpression node) {
        node.getLeft().accept(this);   // 재귀 순회
        node.getRight().accept(this);
        // 타입 호환성 검사 로직
    }
}
```

| 방법 | 언어 지원 | 성능 | 안전성 |
|:---|:---|:---|:---|
| Visitor Pattern | 모든 OO 언어 | 가상 호출 2번 | 컴파일 타임 검사 |
| `instanceof` + 캐스팅 | 모든 OO 언어 | 낮음 (런타임 체크) | 위험 (캐스팅) |
| Pattern Matching (Java 21) | Java 21+ | 최적화됨 | 타입 안전 |
| Multimethods (Groovy, Clojure) | 언어 네이티브 | 높음 | 동적 타이핑 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: `instanceof` 체인은 손님 얼굴을 보고 직접 "이 분은 VIP인가요?" 하고 하나씩 물어보는 것, Visitor는 손님이 직접 "저는 VIP예요(accept -> visit(VIP))"라고 신원을 알리는 구조 — 더 안전하고 확장적이다.

---

## Ⅴ. 기대효과 및 결론
Visitor 패턴과 더블 디스패치는 타입 계층이 안정적이고 연산이 다양한 시스템에서 강력한 확장성을 제공한다:

**기대효과**:
- **새 연산 추가 용이**: 새 Visitor 클래스만 추가, Element 클래스 불변
- **관심사 분리**: 데이터(Element)와 연산(Visitor) 완전 분리
- **컴파일 타임 안전성**: 모든 타입에 대한 처리 구현 여부 컴파일러 검사

**한계**:
- 새 Element 타입 추가 시 모든 Visitor 구현 수정 필요
- 캡슐화 약화: Element의 내부 상태를 Visitor에 노출해야 함
- 보일러플레이트 코드 증가

심화 학습에서는 **더블 디스패치의 메커니즘(두 번의 가상 호출)**, <strong>Visitor 패턴의 구조(Element + Visitor 인터페이스)</strong>, <strong>적합/부적합 시나리오(연산 추가 ↔ 타입 추가)</strong>를 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Visitor 패턴은 백화점 VIP 서비스 — 각 층(Element)은 "저는 3층이에요(accept)"라고 안내하고, 전담 컨시어지(Visitor)가 층에 맞는 특화 서비스(visit(3층))를 제공한다. 새 서비스를 추가할 때 각 층을 건드리지 않고 컨시어지(Visitor)만 새로 만들면 된다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF 행동 패턴 (Behavioral Pattern) | Visitor가 속하는 패턴 범주 |
| 핵심 메커니즘 | Double Dispatch | Visitor 패턴이 구현하는 두 번의 가상 호출 |
| 연관 패턴 | Composite Pattern | 트리 구조 + Visitor로 AST 처리 |
| 연관 패턴 | Iterator Pattern | 컬렉션 순회 후 각 요소에 Visitor 적용 |
| 언어 대안 | Java Pattern Matching (sealed class) | Java 21의 native 더블 디스패치 대안 |
| 실무 사례 | 컴파일러 AST Visitor | 타입 검사, 코드 생성, 최적화 각각 별도 Visitor |
| 대비 개념 | Single Dispatch | Java의 기본 다형성 — 호출 대상 타입만 고려 |

### 📈 관련 키워드 및 발전 흐름도
single dispatch -> 더블 디스패치와 방문자 패턴 -> 다형성 연산 분리

### 👶 어린이를 위한 3줄 비유 설명
1. 더블 디스패치는 두 번 확인하는 것 — "너는 어떤 도형이야?(1번: accept)" -> "그럼 내가 너에게 맞는 방법으로 처리할게(2번: visit(Circle))"처럼 두 번 확인 후 행동해.
2. Visitor 패턴 덕분에 새로운 행동(연산)을 추가할 때 기존 도형 클래스를 건드리지 않고 새 방문자(Visitor)만 만들면 되니까 기존 코드가 안전해.
3. 단, 새 도형 종류를 추가하면 모든 방문자에 그 도형 처리를 추가해야 하니 — 도형 종류는 거의 안 바뀌고 처리 방법이 자주 늘어나는 경우에 Visitor가 최선이야.
