---
title: "Interpreter Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 206
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Interpreter (해석자) 패턴은 언어나 문법의 각 규칙을 클래스로 표현하고, 해당 언어로 작성된 문장을 AST (Abstract Syntax Tree, 추상 구문 트리)로 파싱한 뒤 평가(Evaluate)하는 구조를 제공한다.
> 2. **가치**: 도메인 특화 언어(DSL, Domain-Specific Language)나 규칙 엔진을 구현할 때, 문법 규칙을 코드와 1:1 매핑하여 이해·확장이 쉬운 인터프리터를 만든다.
> 3. **판단 포인트**: 정규 표현식, SQL WHERE절, 수식 파서처럼 반복적으로 사용되는 간단한 문법이 있을 때 적용하되, 복잡한 문법에는 전용 파서 생성기(ANTLR 등)를 사용한다.

---

## Ⅰ. 개요 및 필요성
GoF는 다음 조건에서 Interpreter 패턴을 권장한다:

1. 해석할 언어의 <strong>문법이 단순</strong>하고 규칙의 수가 적다
2. 동일한 문장을 <strong>반복적으로 해석</strong>해야 한다
3. 효율보다 <strong>이해·확장 용이성</strong>이 중요한 경우

BNF (Backus-Naur Form, 배커스-나우르 표기법)는 문법을 정의하는 형식 언어다. Interpreter 패턴은 BNF의 각 규칙을 클래스로 구현한다:

```
BNF 문법 예시 (산술 표현식):
  expression ::= number | expression '+' expression | expression '*' expression
  number     ::= [0-9]+

  v 각 규칙이 클래스가 됨

  AbstractExpression    -> expression 인터페이스
  NumberExpression      -> TerminalExpression (더 이상 분해 안 됨)
  AddExpression         -> NonTerminalExpression (2개의 expression 포함)
  MultiplyExpression    -> NonTerminalExpression
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 영어 문법책의 "주어 + 동사 + 목적어" 규칙 하나하나를 클래스로 만들고, 그 규칙 클래스들로 문장을 파싱하고 이해하는 것이 Interpreter 패턴이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  +--------------------------------------------------+
  |  Context                                         |
  |  (전역 해석 상태: 변수 바인딩, 환경 정보 등)      |
  +--------------------------------------------------+
          |
          | interpret(context)
          v
  «interface» AbstractExpression
  ------------------------------
  + interpret(Context): Object
          ^
          |
  +-------+----------+
  v                  v
TerminalExpression  NonTerminalExpression
(리프 노드)          (내부 노드 - 하위 Expression 포함)
  예: NumberExpr     예: AddExpr(left, right)
      VariableExpr        left.interpret() + right.interpret()
```

```
  파싱 결과 AST:

            AddExpression
           /             \
    NumberExpr(3)    MultiplyExpression
                    /                 \
             NumberExpr(4)       NumberExpr(5)

  평가 (interpret):
  1. MultiplyExpression.interpret() = 4 × 5 = 20
  2. AddExpression.interpret() = 3 + 20 = 23
```

```
  SQL: WHERE age > 25 AND city = 'Seoul'

  AST:
              AndExpression
             /             \
    GreaterThanExpr         EqualExpr
    (age, 25)               (city, 'Seoul')

  해석:
  AndExpression.interpret(row)
    = GreaterThanExpr.interpret(row) && EqualExpr.interpret(row)
    = (row.age > 25) && (row.city.equals("Seoul"))
```

```java
// 규칙 엔진 구현
interface RuleExpression {
    boolean interpret(Context ctx);
}

class GreaterThanRule implements RuleExpression {
    private String field; private int threshold;
    @Override
    public boolean interpret(Context ctx) {
        return ctx.getValue(field) > threshold;
    }
}

class AndRule implements RuleExpression {
    private RuleExpression left, right;
    @Override
    public boolean interpret(Context ctx) {
        return left.interpret(ctx) && right.interpret(ctx);
    }
}
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 악보(언어)를 보고 연주하는 것 — 음표(TerminalExpression), 화음 기호(NonTerminalExpression), 지휘자 지시(Context)가 합쳐져서 음악(실행 결과)이 탄생한다.

---

## Ⅲ. 비교 및 연결
| 적용 대상 | 적합성 | 이유 |
|:---|:---|:---|
| 정규 표현식 (Regex) | ✅ 적합 | 규칙 수 제한, 반복 사용 |
| SQL 파서 | ✅ 적합 | 명확한 BNF 문법 |
| 간단한 DSL | ✅ 적합 | 도메인 규칙을 코드로 표현 |
| 프로그래밍 언어 파서 | ❌ 부적합 | 문법 복잡 -> ANTLR 사용 |
| 자연어 처리 | ❌ 부적합 | 불규칙성 너무 높음 |

| 패턴 | Interpreter와의 관계 |
|:---|:---|
| Composite (컴포지트) | AST 자체가 Composite 구조 |
| Visitor (방문자) | AST 노드를 순회하며 여러 연산 적용 |
| Flyweight (플라이웨이트) | TerminalExpression 인스턴스 공유 |
| Iterator (이터레이터) | AST 순회에 사용 |

- **📢 섹션 요약 비유**: 계산기 앱 — 버튼(TerminalExpression: 숫자), 연산자(NonTerminalExpression: +, ×), 메모리(Context: 이전 결과). 이 세 가지가 Interpreter 패턴의 3요소이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```
  보험 할인 규칙 DSL:
  "나이 >= 65 AND 무사고 >= 5년 -> 20% 할인"

  RuleExpression rule = new AndRule(
      new GreaterOrEqualRule("age", 65),
      new GreaterOrEqualRule("accidentFreeYears", 5)
  );

  if (rule.interpret(customer)) {
      applyDiscount(0.20);
  }
```

Spring의 SpEL (Spring Expression Language)은 Interpreter 패턴의 실제 구현:

```
  // SpEL = Interpreter 패턴으로 구현된 표현식 언어
  @Value("#{systemProperties['user.region'] == 'KR' ? '한국' : '해외'}")
  private String region;

  // 동적 권한 체크
  @PreAuthorize("hasRole('ADMIN') or #userId == authentication.name")
  public void deleteUser(String userId) { ... }
```

- BNF (Backus-Naur Form)와의 관계: 각 BNF 규칙 = 하나의 클래스
- AST (Abstract Syntax Tree) 구조가 <strong>Composite 패턴</strong>임을 명시
- **복잡한 문법에는 부적합** -> ANTLR, JavaCC 같은 파서 생성기 권장

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 요리 레시피(언어) 해석 — "재료를 볶다"(Terminal), "볶은 것에 소스를 더하다"(NonTerminal), 요리사의 경험치(Context)가 합쳐져서 최종 요리(실행 결과)가 완성된다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 문법-코드 1:1 매핑 | 문법 규칙을 클래스로 직접 표현 -> 가독성 |
| 규칙 재사용 | 각 Expression 독립 재사용 가능 |
| 확장 용이 | 새 문법 규칙 = 새 Expression 클래스 추가 |
| 비즈니스 로직 외재화 | 규칙을 코드가 아닌 DSL로 관리 가능 |

- **복잡한 문법**: 규칙 수가 많아지면 클래스 폭발 (Class Explosion)
- <strong>성능</strong>: 재귀적 AST 평가 오버헤드 -> 캐싱(Caching)으로 보완
- **유지보수**: 문법 변경 시 여러 클래스 수정 필요

Interpreter (해석자) 패턴은 <strong>도메인 규칙을 언어로 표현</strong>해야 하는 상황에서 빛을 발한다. 정규 표현식, SQL, SpEL 등 현실 세계의 많은 인터프리터가 이 패턴을 기반으로 한다. 단순한 문법에는 강력하지만, 복잡한 문법은 전문 파서 도구로 처리하는 것이 현명하다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Interpreter는 "번역기" — 외국어(DSL)를 컴퓨터가 이해하는 언어(실행 코드)로 변환한다. 문법이 단순할수록 번역기도 단순해진다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | TerminalExpression | 더 이상 분해 안 되는 리프 노드 |
| 하위 개념 | NonTerminalExpression | 하위 표현식을 포함하는 내부 노드 |
| 연관 개념 | AST (Abstract Syntax Tree) | 파싱 결과 트리 구조 |
| 연관 개념 | BNF (Backus-Naur Form) | 문법 정의 형식 |
| 연관 개념 | Spring SpEL | 실제 산업 적용 사례 |

### 📈 관련 키워드 및 발전 흐름도
문법 정의 -> 해석자 패턴 -> DSL 엔진·규칙 처리

### 👶 어린이를 위한 3줄 비유 설명
1. "빨강 3개 더하기 파랑 2개" 같은 말을 컴퓨터가 이해하게 만드는 게 해석자 패턴이에요.
2. 각 단어(숫자, 더하기)가 하나의 클래스(Expression)가 돼서 함께 계산해요.
3. 이렇게 만들면 "나누기"나 "빼기"도 새 클래스만 추가하면 바로 쓸 수 있어요!
