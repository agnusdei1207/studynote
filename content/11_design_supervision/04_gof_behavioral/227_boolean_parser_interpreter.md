---
title: "Boolean Parser Interpreter"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 227
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Interpreter (인터프리터) 패턴은 언어의 문법을 객체 계층(Object Hierarchy)으로 표현하고, 각 객체가 자신의 해석(Interpret)을 담당하여 표현식을 평가하는 패턴이다 — Boolean Parser는 이 패턴의 가장 실용적인 구현 예다.
> 2. **가치**: 비개발자도 이해할 수 있는 도메인 특화 언어(DSL, Domain Specific Language)를 설계하여, 복잡한 비즈니스 규칙을 코드 변경 없이 외부에서 표현하고 변경할 수 있다.
> 3. **판단 포인트**: 렉서(Lexer) -> 파서(Parser, 재귀 하강) -> AST (Abstract Syntax Tree, 추상 구문 트리) -> 평가기(Evaluator)의 4단계 파이프라인이 인터프리터의 표준 구조다.

---

## Ⅰ. 개요 및 필요성
**문제**: 조건이 복잡하고 자주 바뀌는 비즈니스 규칙을 코드로 하드코딩하면 변경마다 배포가 필요하다.

```java
// 나쁜 예: 하드코딩된 규칙 (변경 시 배포 필요)
boolean eligible = user.getAge() >= 18
    && user.getCountry().equals("KR")
    && (user.getSubscription().equals("PREMIUM") || user.getPoints() > 1000);
```

**해결**: 규칙을 외부 DSL로 표현하고 런타임에 해석

```
// DSL 표현 (DB/설정 파일에서 읽음)
"age >= 18 AND country = 'KR' AND (subscription = 'PREMIUM' OR points > 1000)"

// 인터프리터가 위 문자열을 파싱하여 런타임에 평가
boolean eligible = interpreter.evaluate(rule, user);
```

| 구성 요소 | 설명 | 예시 |
|:---|:---|:---|
| 터미널 표현식 | 최소 단위 (변수, 리터럴) | `age >= 18`, `true`, `"KR"` |
| 논리 AND | 두 표현식 모두 참 | `A AND B` |
| 논리 OR | 하나 이상 참 | `A OR B` |
| 논리 NOT | 부정 | `NOT A` |
| 괄호 그룹 | 우선순위 조정 | `(A OR B) AND C` |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 인터프리터 패턴은 번역가 팀 — 원문(표현식)을 받아 어휘 분석가(Lexer)가 단어로 쪼개고, 문법 분석가(Parser)가 문장 구조(AST)를 파악하고, 번역가(Evaluator)가 최종 의미(true/false)를 판단한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-----------------------------------------------------------------+
|           Boolean Parser Interpreter Pipeline                   |
|                                                                 |
|  입력: "age >= 18 AND (role = 'ADMIN' OR score > 100)"          |
|                                                                 |
|  Step 1: Lexer (렉서 / 토크나이저)                               |
|    +---------------------------------------------------------+  |
|    | [age] [>=] [18] [AND] [(] [role] [=] ['ADMIN'] [OR]... |  |
|    +----------------------------+----------------------------+  |
|                                 | 토큰 스트림                    |
|  Step 2: Parser (파서, 재귀 하강)                                |
|    +---------------------------------------------------------+  |
|    |           AST (추상 구문 트리)                            |  |
|    |                  AND                                    |  |
|    |                 /   \                                   |  |
|    |           age>=18    OR                                 |  |
|    |                     /  \                                |  |
|    |              role=ADMIN  score>100                      |  |
|    +----------------------------+----------------------------+  |
|                                 | AST                           |
|  Step 3: Evaluator (평가기)                                      |
|    +---------------------------------------------------------+  |
|    | context = { age: 25, role: "USER", score: 150 }         |  |
|    | AND(age>=18:true, OR(role=ADMIN:false, score>100:true))  |  |
|    | = AND(true, OR(false, true)) = AND(true, true) = true   |  |
|    +---------------------------------------------------------+  |
|                                                                 |
|  출력: true (조건 충족)                                           |
+-----------------------------------------------------------------+
```

```bnf
expression  ::= or_expr
or_expr     ::= and_expr ("OR" and_expr)*
and_expr    ::= not_expr ("AND" not_expr)*
not_expr    ::= "NOT" not_expr | primary
primary     ::= "(" expression ")" | comparison
comparison  ::= identifier operator value
operator    ::= "=" | "!=" | ">=" | "<=" | ">" | "<"
value       ::= STRING | NUMBER | BOOLEAN
identifier  ::= [a-zA-Z_][a-zA-Z0-9_]*
```

```java
class BooleanParser {
    private List<Token> tokens;
    private int pos = 0;

    public Expression parse(String input) {
        this.tokens = new Lexer().tokenize(input);
        return parseOrExpr();
    }

    private Expression parseOrExpr() {
        Expression left = parseAndExpr();
        while (match(TokenType.OR)) {
            Expression right = parseAndExpr();
            left = new OrExpression(left, right);  // AST 노드 생성
        }
        return left;
    }

    private Expression parseAndExpr() {
        Expression left = parseNotExpr();
        while (match(TokenType.AND)) {
            Expression right = parseNotExpr();
            left = new AndExpression(left, right);
        }
        return left;
    }
}

// AST 노드 (Composite Pattern과 결합)
interface Expression {
    boolean evaluate(Context context);
}

class AndExpression implements Expression {
    private final Expression left, right;
    public boolean evaluate(Context ctx) {
        return left.evaluate(ctx) && right.evaluate(ctx);  // 단락 평가
    }
}
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 재귀 하강 파서는 수학 문제를 푸는 학생 — "괄호 먼저, 곱셈/나눗셈 그다음, 덧셈/뺄셈 마지막"처럼 문법 우선순위 규칙을 재귀 함수의 호출 순서로 구현한다.

---

## Ⅲ. 비교 및 연결
| GoF 참여자 | Boolean Parser에서의 역할 |
|:---|:---|
| AbstractExpression | `Expression` 인터페이스 (evaluate 메서드) |
| TerminalExpression | `ComparisonExpression` (단말 비교 노드) |
| NonterminalExpression | `AndExpression`, `OrExpression`, `NotExpression` |
| Context | 변수 값을 담은 평가 컨텍스트 |
| Client | 파서로 AST를 구성하고 evaluate 호출 |

| 시스템 | 인터프리터 활용 |
|:---|:---|
| ElasticSearch Query DSL | JSON 기반 Boolean 쿼리 파서 |
| Spring Security SpEL | `hasRole('ADMIN') and isAuthenticated()` |
| Drools Business Rules | 비즈니스 규칙 DSL 평가 엔진 |
| AWS IAM Policy | JSON으로 표현된 권한 표현식 평가 |
| SQL WHERE 절 | `age > 18 AND status = 'ACTIVE'` |

- **📢 섹션 요약 비유**: Spring Security의 `@PreAuthorize("hasRole('ADMIN') and #userId == principal.id")` 는 인터프리터 패턴의 실사용 — 문자열로 쓴 보안 규칙을 런타임에 파싱하고 평가한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 권한 평가 컨텍스트
class PermissionContext {
    private final User user;
    private final Resource resource;
    // role, department, score 등 속성 맵
    Map<String, Object> attributes;
}

// 규칙 엔진 사용
RuleEngine engine = new RuleEngine();
String rule = "role = 'ADMIN' OR (role = 'MANAGER' AND department = resource.department)";

boolean allowed = engine.evaluate(rule, new PermissionContext(currentUser, targetResource));
```

```
성능 문제:
  같은 규칙 문자열을 매 요청마다 파싱 -> 파싱 비용 반복 발생

최적화:
  규칙 문자열 -> AST 변환 결과를 캐시
  (규칙 변경 시 캐시 무효화)

  Map<String, Expression> astCache = new ConcurrentHashMap<>();
  Expression ast = astCache.computeIfAbsent(ruleText, parser::parse);
  boolean result = ast.evaluate(context);  // 파싱 없이 평가만
```

| 적합 | 부적합 |
|:---|:---|
| 간단한 문법의 DSL | 복잡한 프로그래밍 언어 구현 |
| 빈번한 규칙 변경 | 규칙이 고정된 경우 |
| 규칙을 DB/설정에 저장 | 성능 최우선 (파싱 오버헤드) |
| 비개발자가 규칙 정의 | 개발자만 규칙 관리 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 인터프리터 패턴은 교통 신호 제어 시스템 — 교통 담당자(비개발자)가 "출퇴근 시간 버스전용차로 활성화" 규칙을 텍스트로 입력하면, 시스템이 런타임에 해석해서 신호를 바꾼다. 개발자가 코드를 바꿀 필요 없다.

---

## Ⅴ. 기대효과 및 결론
Boolean Parser Interpreter 패턴은 비즈니스 규칙의 외부화(Externalize)를 통해 시스템 유연성을 극대화한다:

**기대효과**:
- **배포 없는 규칙 변경**: DB의 규칙 문자열만 수정하면 즉시 반영
- <strong>도메인 전문가 참여</strong>: 코드를 모르는 전문가도 규칙 정의 가능
- **테스트 용이성**: 규칙을 독립적으로 단위 테스트 가능
- **재사용성**: 동일 인터프리터로 다양한 도메인 규칙 처리

**한계**:
- 복잡한 언어일수록 파서 구현이 복잡해짐 (ANTLR 등 파서 생성기 권장)
- 파싱 오버헤드 (AST 캐싱으로 완화)
- 문법 에러 처리 및 디버깅 도구 필요

심화 학습에서는 <strong>Lexer -> Parser -> AST -> Evaluator 4단계</strong>와 <strong>TerminalExpression/NonterminalExpression 역할</strong>을 명확히 서술하고, <strong>실무 적용 사례(Spring Security SpEL, Drools)</strong>를 언급하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Boolean Parser는 법원의 판사 — 법 조문(문법 정의)에 따라 사건(표현식)을 분석하고, 증거(컨텍스트 값)를 검토하여 무죄/유죄(true/false)를 판결(evaluate)한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Interpreter Pattern | Boolean Parser의 상위 패턴 |
| 구성 패턴 | Composite Pattern | AST 노드 계층 구조에 활용 |
| 연관 개념 | DSL (Domain Specific Language) | 인터프리터가 해석하는 도메인 언어 |
| 연관 개념 | AST (Abstract Syntax Tree) | 파싱 결과물, 평가의 입력 |
| 구현 도구 | ANTLR | 문법 정의 -> 파서 자동 생성 도구 |
| 실무 사례 | Spring Security SpEL | 권한 표현식 DSL 인터프리터 |
| 연관 개념 | BNF 문법 정의 | 언어 구조를 형식적으로 기술하는 표기법 |

### 📈 관련 키워드 및 발전 흐름도
토큰화 -> 불리언 파서 인터프리터 -> 규칙 DSL

### 👶 어린이를 위한 3줄 비유 설명
1. 인터프리터는 번역기 — "나이 >= 18 그리고 회원등급 = VIP" 같은 조건문(DSL)을 컴퓨터가 이해하는 true/false로 번역해줘.
2. 번역하는 순서는 먼저 단어로 쪼개고(Lexer), 그다음 문장 구조를 파악하고(Parser -> AST), 마지막으로 실제로 계산해서(Evaluator) 답을 내.
3. 이 방법 덕분에 "접속 허용 규칙"을 개발자가 코드를 바꾸지 않아도 비개발자가 텍스트로 수정할 수 있어 — 마치 법률 조항을 바꾸는 것처럼.
