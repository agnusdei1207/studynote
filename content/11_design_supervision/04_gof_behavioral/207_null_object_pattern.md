---
title: "Null Object Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 207
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Null Object (널 객체) 패턴은 `null` 참조 대신 "아무 일도 하지 않는" 기본 객체(NoOp, No-Operation 객체)를 반환하여, 호출자가 `null` 체크를 하지 않아도 되게 만든다.
> 2. **가치**: NPE (NullPointerException)를 원천 차단하고, `if (obj != null)` 방어 코드를 제거하여 코드를 더 깔끔하고 안전하게 만든다.
> 3. **판단 포인트**: 객체가 없을 때 아무것도 하지 않거나 기본값을 반환해야 하는 상황에 적합하다. 오류 상황을 숨기면 안 될 때는 Optional이나 예외를 사용한다.

---

## Ⅰ. 개요 및 필요성
Tony Hoare가 1965년 null 참조를 도입하면서 "10억 달러짜리 실수"라고 직접 표현했다. null이 문제인 이유:

```java
// null 참조로 인한 NPE (NullPointerException) 위험
Logger logger = getLogger();
logger.log("message");  // logger가 null이면 NPE 발생!

// 전통적 방어적 프로그래밍 (Defensive Programming)
if (logger != null) {
    logger.log("message");
}

// 여러 단계 null 체크 = 코드 오염
if (user != null && user.getAddress() != null
    && user.getAddress().getCity() != null) {
    print(user.getAddress().getCity());
}
```

```java
// Null Object 도입 후
Logger logger = getLogger();  // null 대신 NullLogger 반환
logger.log("message");        // NullLogger.log() -> 아무것도 안 함, NPE 없음

// null 체크 코드 완전 제거!
```

| 사례 | Null Object 역할 | 실제 객체 |
|:---|:---|:---|
| 빈 배열 `[]` | 원소 없는 컬렉션 | 데이터 포함 배열 |
| `/dev/null` (Unix) | 쓰고 버리는 장치 | 실제 파일 |
| `Collections.emptyList()` | 빈 리스트 | 데이터 리스트 |
| NullLogger | 로그를 버리는 로거 | 실제 파일 로거 |
| Anonymous User | 미로그인 사용자 | 로그인 사용자 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 음소거 버튼(Null Object) — 음악이 없을 때 리모컨의 "다음 곡" 버튼을 눌러도 그냥 아무 일도 일어나지 않는다. 에러가 나지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  «interface» / «abstract class»
  AbstractLogger
  ------------------
  + log(message)
        ^
        |
  +-----+----------+
  v                v
FileLogger      NullLogger
----------      --------------------------
log(msg) {      log(msg) {
  file.write      // 아무것도 하지 않음
  (msg)           // NoOp (No-Operation)
}               }

// 사용처
Logger logger = config.isDebug()
    ? new FileLogger("app.log")
    : new NullLogger();   // null 아님!

logger.log("start");  // 항상 안전
```

```
  전략 패턴에서의 Null Object:

  interface DiscountStrategy {
      double apply(double price);
  }

  class NoDiscount implements DiscountStrategy {
      @Override
      public double apply(double price) {
          return price;  // 할인 없음, 원가 그대로 반환
      }
  }

  // 사용
  DiscountStrategy strategy = user.isPremium()
      ? new PremiumDiscount()
      : new NoDiscount();   // null이 아닌 Null Object

  double finalPrice = strategy.apply(100_000);
  // null 체크 없이 항상 안전
```

```
  계층: User -> Address -> City

  ❌ null 체크 방식:
  String city = "알 수 없음";
  if (user != null) {
      Address addr = user.getAddress();
      if (addr != null) {
          City c = addr.getCity();
          if (c != null) {
              city = c.getName();
          }
      }
  }

  ✅ Null Object 방식:
  String city = user.getAddress().getCity().getName();
  // 각 레이어에 Null Object -> 체인 전체가 안전
  // NullUser.getAddress() -> NullAddress 반환
  // NullAddress.getCity() -> NullCity 반환
  // NullCity.getName() -> "알 수 없음" 반환
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

- **📢 섹션 요약 비유**: 비어있는 통장(Null Object) — 잔액 조회를 해도 에러가 나지 않고 "0원"이라고 알려준다. null 참조라면 ATM기가 오작동할 것이다.

---

## Ⅲ. 비교 및 연결
| 항목 | Null Object | Java Optional | 예외 처리 |
|:---|:---|:---|:---|
| **목적** | 기본 동작 제공 | 값 존재 여부 표현 | 오류 상황 처리 |
| **null 체크** | 불필요 | Optional 체인 | try-catch |
| **기본 동작** | NoOp 메서드 실행 | `orElse()` | `catch` 블록 |
| **오류 숨김** | 있음 (주의 필요) | 없음 | 없음 |
| **사용 적합 상황** | 로거, 핸들러 없음 | 단순 값 반환 | 예외적 오류 상황 |
| **코드 간결성** | ✅ 최고 | 중간 | 낮음 |

```
  ✅ Null Object 적합:
  - Logger: 로그 없어도 앱 동작에 지장 없음
  - Event Handler: 핸들러 없어도 이벤트 발생은 계속
  - 기본 정책: 할인 없음, 필터 없음

  ❌ Null Object 부적합:
  - 결제 처리: null 결제는 위험 -> 예외 발생 필수
  - 인증: null 사용자는 명확히 거부해야 함
  - 데이터 저장: null 저장소는 데이터 유실로 이어짐
```

- **📢 섹션 요약 비유**: Null Object는 "묵묵히 일하는 임시 직원" — 주요 직원이 없을 때 회사가 멈추지 않도록 기본 업무는 처리하지만, 중요한 결정은 하지 않는다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// Spring Security의 AnonymousAuthenticationToken
// -> 미로그인 사용자 = null이 아닌 AnonymousUser
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
// auth가 AnonymousAuthenticationToken이면 Null Object

// 항상 auth.getName()을 안전하게 호출 가능
String username = auth.getName();  // "anonymousUser" 반환

// Spring의 NullBeanFactory, NullDataSource 등도 동일 패턴
```

```java
// 완전한 NoOp Null Object 예시
public final class NullEventPublisher implements ApplicationEventPublisher {
    public static final NullEventPublisher INSTANCE = new NullEventPublisher();
    private NullEventPublisher() {}

    @Override
    public void publishEvent(ApplicationEvent event) {
        // 아무것도 하지 않음
    }

    @Override
    public void publishEvent(Object event) {
        // 아무것도 하지 않음
    }
}

// 테스트 환경에서 실제 이벤트 버스 대신 사용
ApplicationEventPublisher publisher = isTest
    ? NullEventPublisher.INSTANCE
    : realEventPublisher;
```

- <strong>NPE (NullPointerException) 회피</strong>를 Null Object의 핵심 가치로 제시
- Java `Optional`과의 차이점: Optional은 값의 존재를 표현, Null Object는 행동을 제공
- <strong>방어적 프로그래밍(Defensive Programming)의 코드 제거</strong> 효과 강조

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 식당에서 아직 손님이 안 왔어도 빈 테이블 세팅(Null Object)이 되어 있다 — 손님이 올 때까지 기다리지 않고 이미 준비가 되어 있는 상태.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| NPE 완전 제거 | null 참조 자체를 없앰 |
| 코드 간결성 | `if (x != null)` 방어 코드 제거 |
| 일관된 인터페이스 | null 여부 관계없이 동일하게 호출 |
| 테스트 용이 | NullObject로 의존성 제거 (테스트 더블) |

- 오류 상황을 <strong>조용히 무시</strong>할 수 있음 -> 중요한 에러가 숨겨질 위험
- 디버깅 시 "왜 아무 일도 일어나지 않는지" 파악 어려울 수 있음
- Null Object도 명확한 <strong>로깅</strong>을 포함하는 것을 권장

Null Object (널 객체) 패턴은 방어적 프로그래밍의 대안으로, 코드를 더 단순하고 NPE로부터 안전하게 만든다. 로거, 이벤트 핸들러, 기본 정책 객체처럼 "없어도 동작이 계속되어야 하는" 컴포넌트에 특히 효과적이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Null Object는 "전원이 꺼진 전자기기의 안전 차단기" — 전기가 없어도 전자기기가 폭발하지 않고 그냥 동작 안 하는 것처럼, NPE 없이 조용히 아무것도 하지 않는다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 연관 개념 | Strategy Pattern | Null Object를 기본 전략으로 사용 |
| 연관 개념 | State Pattern | Null Object를 기본 상태로 사용 |
| 연관 개념 | Java Optional | 값 유무 표현의 대안적 접근 |
| 연관 개념 | NPE (NullPointerException) | 패턴이 해결하는 핵심 문제 |
| 연관 개념 | NoOp (No-Operation) | Null Object의 다른 이름 |

### 📈 관련 키워드 및 발전 흐름도
기본값 처리 -> 널 객체 패턴 -> Fail-safe 객체

### 👶 어린이를 위한 3줄 비유 설명
1. 음악을 끄면 소리가 나지 않아요. 에러가 나는 게 아니라 그냥 조용해지는 거죠.
2. 널 객체 패턴은 "없는 것"을 "아무것도 안 하는 것"으로 표현하는 방법이에요.
3. 리모컨에 음소거 버튼이 있듯이, 코드에도 "아무것도 안 하는 객체"가 있을 수 있어요!
