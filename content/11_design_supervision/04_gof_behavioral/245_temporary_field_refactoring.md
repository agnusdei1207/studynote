---
title: "Temporary Field Anti-pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 245
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 임시 필드 (Temporary Field) 는 클래스 내 특정 메서드 실행 시에만 값을 가지고 평소에는 `null` 또는 쓰레기 값을 갖는 필드로, 클래스의 응집도를 해치는 설계 문제다.
> 2. **가치**: 임시 필드를 제거하면 객체 상태가 항상 유효 (Valid State) 하게 유지되고, 숨겨진 결합도와 컨텍스트 의존성이 제거된다.
> 3. **판단 포인트**: "이 필드가 null일 수 있는 시점이 있는가?" — Yes라면 임시 필드 의심이 필요하다.

---

## Ⅰ. 개요 및 필요성
임시 필드 (Temporary Field) 는 객체의 전체 수명 동안 필요한 것이 아니라, 복잡한 알고리즘 수행 시 임시로 필요한 데이터를 클래스 수준 필드로 선언하는 패턴이다. 매개변수 전달 대신 필드를 통해 '전역 변수처럼' 공유하는 구현 편의에서 발생한다.

```
+---------------------------------------------------------+
|  임시 필드 발생 시나리오                                |
+---------------------------------------------------------+
|  1. 알고리즘이 여러 메서드로 분리될 때                  |
|     -> 중간 결과를 필드로 저장해 메서드 간 공유          |
|                                                         |
|  2. 성능 최적화 목적 캐시 필드                          |
|     -> 계산 결과를 필드에 보관하나 무효화 조건 불명확    |
|                                                         |
|  3. 콜백이나 이벤트 핸들러를 위한 상태 저장             |
|     -> 처리 전/후만 유효한 컨텍스트 데이터              |
+---------------------------------------------------------+
```

- **NullPointerException 위험**: 필드가 설정되지 않은 상태에서 메서드 호출 시 NPE 발생
- **테스트 어려움**: 필드 설정 순서에 따라 동작이 달라지는 순서 의존성 (Order Dependency)
- <strong>스레드 안전성 (Thread Safety) 파괴</strong>: 여러 스레드가 동시에 임시 필드를 덮어씀

- **📢 섹션 요약 비유**: 회사 공유 냉장고에 "내 점심" 라벨을 붙여 하루만 쓰는 자리를 차지하는 것 — 오래 있으면 다른 사람이 실수로 먹거나 버린다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
[ 문제 있는 구조 — 임시 필드 사용 ]
+--------------------------------------------------------+
|  class RouteCalculator {                               |
|    private Graph   _graph;     <- 임시 (calculateRoute  |
|    private Node    _start;     <- 임시  호출 중에만     |
|    private Node    _end;       <- 임시  유효)           |
|    private List<Node> _path;   <- 임시                  |
|                                                        |
|    void calculateRoute(g, s, e) {                      |
|      _graph=g; _start=s; _end=e;  // 설정              |
|      _initializeNodes();          // _graph 사용        |
|      _findPath();                 // _start,_end 사용   |
|      _optimizePath();             // _path 사용         |
|    }                                                   |
|  }                                                     |
+--------------------------------------------------------+
          v 처방: 메서드 객체화 (Replace Method with Method Object)
+--------------------------------------------------------+
|  class RouteCalculation {   <- 계산 컨텍스트 클래스     |
|    private final Graph   graph;   <- 생성자에서 설정    |
|    private final Node    start;   <- (항상 유효)        |
|    private final Node    end;                          |
|    private List<Node>    path;    <- 계산 중 내부 상태  |
|                                                        |
|    RouteCalculation(g, s, e) { this.graph=g; ... }     |
|    List<Node> calculate() {                            |
|      initializeNodes(); findPath(); optimizePath();    |
|      return path;                                      |
|    }                                                   |
|  }                                                     |
|                                                        |
|  class RouteCalculator {                               |
|    List<Node> calculateRoute(g, s, e) {                |
|      return new RouteCalculation(g,s,e).calculate();   |
|    }                                                   |
|  }                                                     |
+--------------------------------------------------------+
```

| 임시 필드 유형 | 권장 처방 | 이유 |
|:---|:---|:---|
| 알고리즘 중간 상태 | 메서드 객체화 (Replace Method with Method Object) | 상태를 전용 객체로 격리 |
| 특수 케이스에서만 의미 있는 필드 | 특수 케이스 객체 (Introduce Special Case) | null 제거 |
| 캐시용 임시 필드 | 명시적 캐시 클래스 도입 | 무효화 로직 명확화 |
| 공통 컨텍스트 전달 | 파라미터 객체화 또는 ThreadLocal | 스레드 안전 보장 |

- **📢 섹션 요약 비유**: 조리대에 준비한 재료는 조리가 끝나면 치워야 한다 — 다음 요리를 위해 테이블을 비워두는 것처럼 임시 상태는 지역 변수나 전용 객체 안에 가둬야 한다.

---

## Ⅲ. 비교 및 연결
| 문제 | 임시 필드 | 글로벌 상태 | 공유 가변 상태 |
|:---|:---|:---|:---|
| 발생 범위 | 클래스 인스턴스 | 애플리케이션 전역 | 멀티스레드 |
| 주요 증상 | NPE, 순서 의존 | 테스트 격리 불가 | 경쟁 조건 (Race Condition) |
| 처방 방향 | 지역화 (Localize) | 의존성 주입 (DI) | 불변성 (Immutability) |
| 위험도 | 중 | 높음 | 매우 높음 |

임시 필드가 "이 객체가 유효하지 않은 상태"를 표현하는 경우, 널 객체 패턴 (Null Object Pattern) 또는 옵셔널 (Optional) 패턴으로 해결할 수 있다.

```
임시 필드 -> null -> NullPointerException
               v 처방
임시 필드 -> Optional<T> -> 명시적 부재 처리
또는
        -> NullObject (기본 행동 제공)
```

- **📢 섹션 요약 비유**: 식당 예약 테이블에 "비어있음" 팻말을 정확히 세워두는 것 — null 팻말이 없으면 손님이 임의로 앉아버린다.

---

## Ⅳ. 실무 적용 및 실무자 판단
웹 서버에서 요청 컨텍스트 (Request Context) 를 임시 필드 대신 `ThreadLocal`로 관리하는 패턴이 표준이다.

```java
// 안티패턴 — 임시 필드로 요청 컨텍스트 공유
class Service {
    private User currentUser;  // 임시 필드 — 멀티스레드 위험!
    void process() { /* currentUser 사용 */ }
}

// 올바른 패턴 — ThreadLocal 사용
class RequestContext {
    private static final ThreadLocal<User> CURRENT_USER
        = new ThreadLocal<>();

    public static void set(User user) { CURRENT_USER.set(user); }
    public static User get()          { return CURRENT_USER.get(); }
    public static void clear()        { CURRENT_USER.remove(); }
}
```

배치 처리 시 진행 상태를 임시 필드로 관리하면 재시작 (Restart) 시 상태가 초기화되지 않아 오류가 발생한다. `JobContext` 같은 전용 객체나 영속 스토어 (Persistent Store) 에 상태를 저장해야 한다.

- <strong>상태 불변성 (State Invariant)</strong>: 클래스의 모든 메서드 호출 전후로 객체 상태가 유효해야 한다는 설계 원칙 강조
- **명령-조회 분리 (CQS: Command-Query Separation)**: 임시 필드는 명령 실행 중에만 유효하므로 조회 메서드에서 접근하면 불일치 발생
- **불변 객체 선호**: 임시 필드 문제의 근본 해결책은 불변 설계

### 판단 체크리스트
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. 리팩토링 단위를 작게 나눠 롤백 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 계약서에 "이 조항은 특정 날짜에만 유효하다"고 적지 않으면 언제 적용되는지 아무도 모른다 — 임시 필드의 유효 기간도 코드에 명시해야 한다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | 임시 필드 사용 | 임시 필드 제거 |
|:---|:---:|:---:|
| NullPointerException 발생률 | 높음 | 없음 (생성자 강제) |
| 멀티스레드 안전성 | 불안전 | 안전 (ThreadLocal/불변) |
| 단위 테스트 독립성 | 실패 (순서 의존) | 보장 |
| 클래스 상태 불변식 | 빈번 위반 | 항상 유효 |

임시 필드 (Temporary Field) 는 "지금 당장 편하려고 만든 지름길"이 장기적으로 어떤 위험을 초래하는지 보여주는 전형적인 안티패턴이다. 알고리즘 중간 상태는 전용 객체로 캡슐화하고, 컨텍스트 데이터는 파라미터로 명시적으로 전달하며, null 가능 상태는 `Optional`이나 특수 케이스 객체로 처리하는 것이 올바른 방향이다.

확장 방향은 ① 정적 분석 자동화, ② 아키텍처 적합성 검증, ③ 작은 단위의 상시 리팩토링 문화 정착이다.

- **📢 섹션 요약 비유**: 탈의실을 개인 사물함으로 오해하고 옷을 놔두면 다음 손님이 치워버린다 — 임시 데이터는 임시 장소(지역 변수)에 두어야 한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 코드 스멜 (Code Smell) | 임시 필드는 주요 스멜 중 하나 |
| 처방 | 메서드 객체화 (Replace Method with Method Object) | 임시 필드를 전용 클래스로 격리 |
| 처방 | 특수 케이스 객체 (Special Case Pattern) | null 필드 대체 |
| 연관 개념 | 상태 불변식 (State Invariant) | 항상 유효한 객체 상태 |
| 연관 개념 | ThreadLocal | 요청 컨텍스트 임시 상태 관리 |
| 연관 개념 | 불변 객체 (Immutable Object) | 임시 필드 문제의 근본 해결 |
| 연관 개념 | Optional | null 필드의 명시적 표현 |

### 📈 관련 키워드 및 발전 흐름도
희소 상태 -> 임시 필드 안티패턴 -> context/specification 분리

### 👶 어린이를 위한 3줄 비유 설명
1. 숙제할 때만 꺼내는 색연필을 책상 서랍이 아닌 거실 테이블 위에 두면 가족이 치워버릴 수 있다.
2. "잠깐 쓰는 것"은 잠깐 쓰는 장소(지역 변수)에 두어야 하고, 항상 필요한 것만 책상 서랍(클래스 필드)에 둬야 한다.
3. 임시 필드 제거는 바로 "잠깐 쓰는 것을 제자리에 치우는 정리 정돈"이다.
