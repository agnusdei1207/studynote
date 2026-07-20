---
title: "Immutable Object Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 218
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Immutable Object (불변 객체) 패턴은 한번 생성된 객체의 상태를 절대 변경하지 않도록 설계하여, 공유 가능한 안전한 값(Value)으로 사용하는 패턴이다.
> 2. **가치**: 불변 객체는 Thread-Safe (스레드 안전)를 보장하고, 부수효과(Side Effect)를 원천 차단하여 멀티스레드, 함수형 프로그래밍, 캐싱 시나리오에서 동기화 비용 없이 안전하게 공유 가능하다.
> 3. **판단 포인트**: 상태 변경이 필요할 때는 기존 객체를 수정하는 대신 "변경된 내용을 담은 새 객체를 반환"한다 — Java `String.toUpperCase()`가 원본 String을 바꾸지 않고 새 String을 반환하는 것이 대표적인 예다.

---

## Ⅰ. 개요 및 필요성
멀티스레드 환경에서 가변 객체를 공유하면:

```
Thread A: user.setName("Alice");   --+
Thread B: user.setName("Bob");     --+-- 동시 실행 -> Race Condition
                                     |
결과: user.getName() == ??? (예측 불가)
```

방어책으로 `synchronized`, `Lock`, `volatile` 등을 사용하지만:
- 성능 저하 (Lock Contention)
- 데드락(Deadlock) 위험
- 코드 복잡도 증가

```
불변 객체 설계 체크리스트:

  1. final class       -> 상속으로 인한 불변성 파괴 방지
  2. final fields      -> 재할당 방지
  3. 생성자에서만 초기화 -> 외부에서 값 세팅 불가 (setter 없음)
  4. 가변 객체 필드는   -> 방어적 복사(Defensive Copy) 적용
     getters에서        -> 방어적 복사본 반환
  5. 깊은 복사(Deep Copy) -> 컬렉션/배열 필드 초기화 시 복사
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 불변 객체는 박물관 전시품 — 유리 케이스(final 클래스) 안에 있어서 누구나 볼 수 있지만(공유 가능), 아무도 건드릴 수 없다(상태 변경 불가). 복사본이 필요하면 3D 프린터(새 객체 생성)로 만든다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```java
// 올바른 불변 객체 구현
public final class Money {                    // 1. final class
    private final long amount;                // 2. final fields
    private final Currency currency;          // 2. final fields
    private final List<String> history;       // 가변 컬렉션 필드

    public Money(long amount, Currency currency, List<String> history) {
        this.amount = amount;
        this.currency = currency;
        // 3. 방어적 복사 (Defensive Copy) — 외부 리스트 변경 차단
        this.history = Collections.unmodifiableList(new ArrayList<>(history));
    }

    // 4. Setter 없음 — getter만 존재
    public long getAmount() { return amount; }
    public Currency getCurrency() { return currency; }

    // 5. 방어적 복사본 반환
    public List<String> getHistory() {
        return new ArrayList<>(history); // 내부 리스트 노출 차단
    }

    // 6. 상태 변경 대신 새 객체 반환 (wither 패턴)
    public Money add(long delta) {
        return new Money(this.amount + delta, this.currency, this.history);
    }
}
```

```
+-----------------------------------------------------------------+
|                  불변 객체 공유 안전성                           |
|                                                                 |
|   Thread A --+                                                  |
|              +---- 읽기(Read) ---> Money { amount=1000, KRW }    |
|   Thread B --+                   (불변 객체 공유 — Lock 불필요)  |
|              +---- 읽기(Read) ---> (동일 참조 안전)               |
|   Thread C --+                                                  |
|                                                                 |
|   Thread A가 상태 변경이 필요할 때:                               |
|   Money original = Money(1000, KRW)                             |
|   Money updated  = original.add(500)  <- 새 객체 생성            |
|                                                                 |
|   original -> Money { amount=1000, KRW }  <- 그대로 유지           |
|   updated  -> Money { amount=1500, KRW }  <- 새 객체              |
+-----------------------------------------------------------------+
```

| 클래스 | 설명 | 가변 대응 클래스 |
|:---|:---|:---|
| `String` | 문자열 불변 | `StringBuilder` |
| `Integer`, `Long` 등 Wrapper | 기본형 래퍼 불변 | — |
| `LocalDate`, `LocalDateTime` | 날짜/시간 불변 | `Calendar` (가변) |
| `BigDecimal`, `BigInteger` | 고정밀 수 불변 | — |
| `List.of()`, `Map.of()` | 불변 컬렉션 (Java 9+) | `ArrayList`, `HashMap` |

- **📢 섹션 요약 비유**: Java String이 불변인 덕분에 "Hello"라는 문자열 리터럴을 프로그램 전체에서 공유해도 아무도 그 값을 바꿀 수 없다 — 각 메서드는 원본을 건드리지 않고 새 String을 만들어 반환한다.

---

## Ⅲ. 비교 및 연결
| 관점 | 가변 객체 (Mutable) | 불변 객체 (Immutable) |
|:---|:---|:---|
| 스레드 안전성 | 동기화 필요 | 동기화 불필요 |
| 캐싱 | 캐시 무효화 필요 | 자유롭게 캐시 가능 |
| Hash 키 안정성 | 해시 값 변동 위험 | 해시 값 안정 (HashMap 키로 안전) |
| 메모리 | 재사용 | 변경 시 새 객체 생성 |
| 방어적 복사 | 수시로 필요 | 불필요 |
| 적합한 사용처 | 복잡한 상태 변경 | DTO, Value Object, 설정값 |

| 구분 | Value Object | Reference Object |
|:---|:---|:---|
| 동등성 | 값(내용)으로 비교 (`equals`) | 참조(주소)로 비교 (`==`) |
| 불변성 | 일반적으로 불변 | 가변 가능 |
| 예시 | Money, Address, PhoneNumber | User, Order, Account |
| DDD 역할 | 컨텍스트 내 속성 표현 | 도메인 주요 엔티티 |

```
① 생성자에서 입력 복사:
   this.dates = new ArrayList<>(dates);  // 외부 변경 차단

② getter에서 복사본 반환:
   return new ArrayList<>(this.dates);   // 내부 노출 차단

③ 컬렉션은 불변 뷰 제공:
   return Collections.unmodifiableList(dates);
```

- **📢 섹션 요약 비유**: 방어적 복사는 비밀 서류를 줄 때 원본이 아닌 복사본을 주는 것 — 상대방이 복사본을 찢어도 원본(내부 필드)은 안전하게 보존된다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// record는 자동으로 불변 필드, 생성자, equals/hashCode/toString 생성
public record Money(long amount, Currency currency) {
    // compact constructor로 유효성 검증
    public Money {
        if (amount < 0) throw new IllegalArgumentException("음수 불가");
    }
    // wither 메서드
    public Money add(long delta) {
        return new Money(this.amount + delta, this.currency);
    }
}
```

불변 객체는 함수형 프로그래밍의 핵심 전제다:
- 순수 함수(Pure Function)는 인수를 변경하지 않음 -> 불변 객체가 이를 보장
- 참조 투명성(Referential Transparency): 같은 인수 -> 항상 같은 결과 -> 불변 상태에서만 가능
- 메모이제이션(Memoization): 불변 객체의 결과는 캐시 가능

| 설계 원칙 | 불변 객체와의 관계 |
|:---|:---|
| 단일 책임 원칙 (SRP) | 상태 변경 책임이 없어 역할이 명확 |
| 개방-폐쇄 원칙 (OCP) | 새 값은 새 객체로 — 기존 코드 불변 |
| 의존성 역전 (DIP) | 값 객체는 구현이 아닌 값에 의존 |
| 테스트 용이성 | 상태 변화 없어 단위 테스트가 단순 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 불변 객체로 설계된 시스템은 레고 블록 — 각 블록(객체)은 자신의 모양을 바꾸지 않고, 새 구조가 필요하면 새 블록을 만들어 조립한다. 멀티스레드에서 여러 아이가 같은 블록을 동시에 봐도 아무도 모양이 바뀌지 않는다.

---

## Ⅴ. 기대효과 및 결론
불변 객체 패턴은 멀티코어 CPU 시대에 필수적인 설계 기법이다:

**핵심 기대효과**:
- <strong>스레드 안전성 보장</strong>: 락(Lock) 없이 자유로운 공유
- **버그 감소**: 예측 불가능한 상태 변경(공유 가변 상태) 제거
- <strong>캐싱 용이</strong>: HashMap 키, 캐시 값으로 안전하게 사용
- **코드 이해도 향상**: 한번 만들면 절대 바뀌지 않는 예측 가능성

**트레이드오프**:
- 상태 변경 시마다 새 객체 생성 -> GC(가비지 컬렉터) 부하 증가
- 매우 큰 객체를 자주 변경해야 하는 경우 성능 저하
- 해결책: Builder 패턴, 내부 가변 구조 + 불변 외부 API (예: CopyOnWriteArrayList)

심화 학습에서는 **불변 객체의 5가지 설계 원칙**(final 클래스, final 필드, setter 없음, 방어적 복사, 새 객체 반환)과 <strong>Thread-Safe 보장 원리</strong>를 정확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 불변 객체는 신분증 — 한번 발급되면 내용을 바꿀 수 없고, 필요하면 새 신분증을 발급(새 객체 생성)받는다. 여러 사람이 동시에 신분증을 봐도 내용이 바뀔 걱정이 없다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 함수형 프로그래밍 (Functional Programming) | 불변성은 함수형의 핵심 원칙 |
| 연관 개념 | Value Object (값 객체) | DDD에서 불변 객체의 대표 활용 |
| 연관 개념 | Thread Safety (스레드 안전성) | 불변 객체가 제공하는 핵심 이점 |
| 구현 도구 | Java Record (Java 16+) | 불변 객체의 간결한 선언 방법 |
| 연관 패턴 | Builder Pattern | 복잡한 불변 객체 생성 지원 |
| 연관 개념 | 방어적 복사 (Defensive Copy) | 가변 필드 포함 시 불변성 유지 기법 |
| 연관 개념 | 모나드 (Monad) | 불변성 위에서 동작하는 함수형 패턴 |

### 📈 관련 키워드 및 발전 흐름도
값 객체 -> 불변 객체 패턴 -> 함수형 동시성

### 👶 어린이를 위한 3줄 비유 설명
1. 불변 객체는 박제된 나비 표본처럼 — 아무리 많은 친구가 구경해도 나비는 변하지 않고, 나비가 필요하면 새 표본을 만든다.
2. Java의 String "Hello"는 한번 만들어지면 절대 바뀌지 않아 — `.toUpperCase()`를 해도 원래 "Hello"는 그대로고 새 "HELLO"가 생겨나.
3. 여러 사람이 동시에 같은 책(불변 객체)을 읽어도 내용이 바뀌지 않으니까 싸울 필요가 없어 — 이것이 스레드 안전성이야.
