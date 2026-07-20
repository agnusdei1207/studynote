---
title: "Data Clumps Refactoring"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 244
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 클럼프 (Data Clumps) 는 항상 함께 등장하는 변수 묶음이 별도 클래스로 추상화되지 않아 중복·불일치·유효성 분산을 유발하는 코드 스멜이다.
> 2. **가치**: 클럼프를 클래스로 캡슐화하면 묶음의 <strong>의미</strong>가 코드에 드러나고, 유효성 검사와 행동이 한곳에 모인다.
> 3. **판단 포인트**: "이 변수들 중 하나를 지우면 나머지가 의미를 잃는가?" — Yes라면 데이터 클럼프다.

---

## Ⅰ. 개요 및 필요성
데이터 클럼프 (Data Clumps) 는 여러 클래스 필드나 메서드 매개변수에서 동일한 변수 그룹이 반복 등장하는 현상이다. 예: `firstName + lastName + email`, `x + y + z (좌표)`, `startDate + endDate`, `host + port + protocol`.

- 초기 설계 단계에서 개념을 **원시 타입 (Primitive Type)** 으로 분해한 후 추상화를 미룸
- 점진적 기능 추가 과정에서 관련 변수가 늘어남
- 복붙 (Copy-and-Paste) 개발로 동일 패턴이 여러 곳에 확산

```
+------------------------------------------------------+
|  데이터 클럼프 발생 위치                             |
+------------------------------------------------------+
|  1. 클래스 필드: 여러 필드가 항상 함께 변경됨       |
|     예) User { String firstName; String lastName;    |
|              String email; String phoneCountryCode;  |
|              String phoneNumber; }                   |
+------------------------------------------------------+
|  2. 메서드 매개변수: 항상 같이 전달되는 인수 묶음   |
|     예) send(String host, int port, boolean ssl)     |
+------------------------------------------------------+
|  3. 반환값: 여러 관련 값을 배열이나 맵으로 반환     |
|     예) return new Object[]{lat, lng, altitude}     |
+------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 항상 같이 다니는 친구들을 매번 이름 하나하나 불러 모으는 것보다 "농구팀"이라는 그룹 이름으로 부르는 게 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
[ 변환 전 — 클럼프 산재 ]
+--------------------------------------------------------+
|  class Server {                                        |
|    String host; int port; boolean ssl;                 |
|  }                                                     |
|  class HttpClient {                                    |
|    connect(String host, int port, boolean ssl) {}      |
|    ping   (String host, int port, boolean ssl) {}      |
|    retry  (String host, int port, boolean ssl, n) {}   |
|  }                                                     |
+--------------------------------------------------------+
         v  클래스 분리 (Extract Class) / 파라미터 객체화
+--------------------------------------------------------+
|  class ConnectionEndpoint {                            |
|    final String host;                                  |
|    final int    port;                                  |
|    final boolean ssl;                                  |
|    ConnectionEndpoint(host, port, ssl) { validate(); } |
|    String toUri() { return (ssl?"https":"http")        |
|                     + "://" + host + ":" + port; }     |
|  }                                                     |
|  class Server { ConnectionEndpoint endpoint; }         |
|  class HttpClient {                                    |
|    connect(ConnectionEndpoint ep) {}                   |
|    ping   (ConnectionEndpoint ep) {}                   |
|    retry  (ConnectionEndpoint ep, int n) {}            |
|  }                                                     |
+--------------------------------------------------------+
```

| 클럼프 위치 | 권장 처방 | 결과 |
|:---|:---|:---|
| 클래스 필드로 반복 | 클래스 분리 (Extract Class) | 독립 클래스로 캡슐화 |
| 메서드 매개변수로 반복 | 파라미터 객체화 (Introduce Parameter Object) | 값 객체 (VO) 생성 |
| 반환값 묶음 | 결과 객체 (Result Object) 도입 | 명시적 타입 반환 |

클럼프를 클래스로 변환한 후, 관련 로직을 새 클래스로 이동시키면 <strong>응집도 (Cohesion)</strong> 가 높아진다.

```
ConnectionEndpoint.isSecure()    <- ssl 판단 로직 이전
ConnectionEndpoint.toUri()       <- URI 조합 로직 이전
ConnectionEndpoint.validate()    <- 포트 범위 검사 이전
```

- **📢 섹션 요약 비유**: 흩어진 퍼즐 조각을 상자에 담고 나면, 상자 라벨을 붙이고 완성 그림 미리보기를 상자에 인쇄할 수 있다 — 그게 클럼프에 클래스를 만드는 일이다.

---

## Ⅲ. 비교 및 연결
| 스멜 | 공통점 | 차이점 | 처방 |
|:---|:---|:---|:---|
| 데이터 클럼프 (Data Clumps) | 관련 변수 묶음 | 항상 같이 다님 | 클래스 분리 |
| 프리미티브 강박 (Primitive Obsession) | 원시 타입 남용 | 의미 있는 타입 대체 필요 | 값 객체 도입 |
| 긴 매개변수 목록 (Long Parameter List) | 매개변수 많음 | 꼭 같이 다니지 않아도 됨 | 파라미터 객체화 |
| 임시 필드 (Temporary Field) | 필드 관련 문제 | 조건부 존재 필드 | 특수 케이스 객체 |

도메인 주도 설계 (DDD) 에서는 데이터 클럼프를 "아직 발견되지 않은 도메인 개념"으로 바라본다. `startDate + endDate`는 `DateRange`, `lat + lng`는 `GeoCoordinate`, `amount + currency`는 `Money` 라는 도메인 개념이 숨어 있는 것이다.

- **📢 섹션 요약 비유**: "생수 + 음료수 + 주스"가 항상 함께 주문되면 "음료 패키지"라는 이름을 붙여 메뉴판에 올리는 것이 비즈니스 의미 표현이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 클럼프 — 금액과 통화가 항상 붙어다님
double amount;
String currency;

// 클래스 분리 후
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    public Money add(Money other) {
        if (!this.currency.equals(other.currency))
            throw new CurrencyMismatchException();
        return new Money(this.amount.add(other.amount), currency);
    }

    public Money multiply(int factor) {
        return new Money(amount.multiply(BigDecimal.valueOf(factor)), currency);
    }
}
```

지도 서비스에서 `double latitude, double longitude, double altitude`가 100곳에 흩어진 경우, `GeoCoordinate` 객체로 통합하면 거리 계산 (`distanceTo`), 유효 범위 검사 (`isValid`), WKT (Well-Known Text) 직렬화 등을 한곳에서 관리한다.

- <strong>도메인 모델 (Domain Model) 풍부화</strong>: 클럼프 -> 클래스 전환은 빈약한 도메인 모델 (Anemic Domain Model) 을 탈출하는 첫걸음이다.
- **테스트 집중화**: 유효성 검사가 클래스 생성자에 모이므로 테스트 1개로 모든 사용처를 검증한다.
- <strong>불변 객체 (Immutable Object)</strong>: 스레드 안전성 (Thread Safety) 이 보장되어 멀티스레드 환경에서도 안전하다.

### 판단 체크리스트
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. 리팩토링 단위를 작게 나눠 롤백 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 병원에서 "혈압 + 맥박 + 체온"을 매번 따로 기록하다가 "활력징후 (Vital Signs) 표"로 통합하면 한눈에 추세를 파악하고 이상값 범위 검사를 자동화할 수 있다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | 클럼프 방치 | 클럼프 제거 |
|:---|:---:|:---:|
| 관련 유효성 검사 위치 수 | 23곳 | 1곳 (클래스 내부) |
| 관련 변수 추가 시 수정 파일 수 | 18개 | 1개 |
| 단위 테스트 케이스 수 (동일 커버리지) | 47개 | 12개 |
| 코드 중복률 | 19% | 3% |

데이터 클럼프 (Data Clumps) 제거는 <strong>숨겨진 도메인 개념을 발굴하는 탐사 작업</strong>이다. 단순히 변수를 묶는 것이 아니라, 그 묶음에 이름과 행동을 부여함으로써 코드가 비즈니스 언어와 일치하도록 만든다. 이는 유지보수성, 테스트 용이성, 팀 커뮤니케이션을 동시에 향상시킨다.

확장 방향은 ① 정적 분석 자동화, ② 아키텍처 적합성 검증, ③ 작은 단위의 상시 리팩토링 문화 정착이다.

- **📢 섹션 요약 비유**: 서랍 속 양말, 속옷, 티셔츠를 각자 제자리 수납함에 넣으면 "오늘 입을 옷 세트"를 꺼낼 때도 빠르고, 세탁 후 정리도 쉽다 — 이것이 데이터 클럼프 제거의 가치다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 코드 스멜 (Code Smell) | 데이터 클럼프는 주요 스멜 중 하나 |
| 상위 개념 | 리팩토링 (Refactoring) | 클럼프 제거의 공식 수단 |
| 연관 개념 | 프리미티브 강박 (Primitive Obsession) | 함께 발생하는 스멜 |
| 연관 개념 | 값 객체 (Value Object, VO) | 클럼프 클래스화의 이상적 형태 |
| 연관 개념 | DDD (Domain-Driven Design) | 클럼프에서 도메인 개념 발굴 |
| 처방 | 클래스 분리 (Extract Class) | 필드 클럼프 처방 |
| 처방 | 파라미터 객체화 (Introduce Parameter Object) | 매개변수 클럼프 처방 |

### 📈 관련 키워드 및 발전 흐름도
중복 매개변수 -> 데이터 클럼프 리팩토링 -> 개념 모델 정제

### 👶 어린이를 위한 3줄 비유 설명
1. 알림장에 매일 "국어책, 수학책, 연필, 지우개"를 따로따로 적는 대신 "1교시 준비물 세트"라고 묶어서 적으면 더 빠르다.
2. 세트 이름이 생기면 "오늘은 세트에 색연필도 추가"처럼 한번만 바꿔도 모든 알림장이 업데이트된다.
3. 데이터 클럼프 제거는 바로 이 "세트 이름 붙이기"다.
