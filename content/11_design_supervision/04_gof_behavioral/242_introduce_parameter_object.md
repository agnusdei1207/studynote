---
title: "Introduce Parameter Object"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 242
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파라미터 객체화 (Introduce Parameter Object) 는 항상 함께 전달되는 매개변수 그룹을 하나의 객체로 묶어, 메서드 시그니처를 단순화하는 리팩토링 기법이다.
> 2. **가치**: 긴 매개변수 목록 (Long Parameter List) 코드 스멜을 제거하고, 관련 데이터와 그에 속한 행동을 함께 캡슐화할 발판을 마련한다.
> 3. **판단 포인트**: 동일한 매개변수 3개 이상이 여러 메서드에 반복 등장하면 파라미터 객체화 신호다.

---

## Ⅰ. 개요 및 필요성
파라미터 객체화 (Introduce Parameter Object) 는 여러 메서드에 함께 전달되는 매개변수 묶음을 새로운 클래스(또는 레코드)로 추출하고, 해당 클래스의 인스턴스를 대신 전달하는 기법이다. 단순 데이터 홀더 (Data Holder) 에서 시작하지만, 이후 관련 비즈니스 로직을 해당 클래스로 이관할 수 있는 <strong>성장 가능한 객체</strong>가 된다.

```
// 변환 전 — 긴 매개변수 목록
public Report generate(
    Date startDate, Date endDate,
    String region, String category,
    int minAmount, int maxAmount) { ... }

// 변환 후 — 파라미터 객체 사용
public Report generate(ReportCriteria criteria) { ... }
```

- <strong>인지 부하 감소</strong>: 매개변수 6개 이상은 호출 시 순서 실수를 유발한다 (특히 동일 타입 연속).
- <strong>일관성 보장</strong>: 날짜 범위(시작·종료)처럼 항상 쌍으로 다녀야 하는 데이터를 하나의 객체로 묶으면 "시작일 없이 종료일만 전달"하는 실수를 방지한다.
- **진화 용이성**: 새 조건 추가 시 메서드 시그니처 변경 없이 객체 필드만 추가하면 된다.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 편의점 도시락을 낱개로 들고 다니는 대신, 쇼핑백 하나에 담아 한 번에 전달하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
[ 변환 전 구조 ]
+--------------------------------------------------------+
| searchOrders(Date from, Date to, String region,        |
|              String status, int page, int size)        |
| exportOrders(Date from, Date to, String region,        |
|              String status, String format)             |
| countOrders (Date from, Date to, String region,        |
|              String status)                            |
+--------------------------------------------------------+
           v  파라미터 객체화 (Introduce Parameter Object)
+------------------------------------------------------+
|                   OrderQuery (Value Object)          |
|  +------------------------------------------------+  |
|  |  dateRange  : DateRange  (from, to)            |  |
|  |  region     : String                           |  |
|  |  status     : OrderStatus                      |  |
|  |  + isValid(): boolean                          |  |
|  |  + overlaps(DateRange other): boolean          |  |
|  +------------------------------------------------+  |
+------------------------------------------------------+
           v
+------------------------------------------------------+
| searchOrders(OrderQuery q, Pageable p)               |
| exportOrders(OrderQuery q, String format)            |
| countOrders (OrderQuery q)                           |
+------------------------------------------------------+
```

파라미터 객체는 자연스럽게 **값 객체 (Value Object, VO)** 패턴으로 발전한다.

| 특성 | 일반 파라미터 묶음 | 값 객체 (VO) |
|:---|:---:|:---:|
| 불변성 (Immutability) | ✗ | ✅ |
| 동등성 (Equality) | 참조 기반 | 값 기반 |
| 자가 유효성 검사 | ✗ | ✅ |
| 도메인 로직 포함 | ✗ | ✅ |

1. 매개변수 그룹을 담을 새 클래스 생성 (불변 권고)
2. 기존 메서드에 새 클래스를 추가 매개변수로 병행 선언
3. 호출부를 새 클래스를 사용하도록 점진적 전환
4. 기존 개별 매개변수 제거
5. 관련 동작을 새 클래스로 이관

- **📢 섹션 요약 비유**: 주소록에 이름, 전화번호, 이메일을 따로 적는 대신 "연락처 카드" 한 장으로 관리하는 것 — 카드에는 나중에 주소, SNS도 추가할 수 있다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 목적 | 적합 상황 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| 파라미터 객체화 (Introduce Parameter Object) | 묶음 단순화 | 3개+ 관련 매개변수 | 확장 용이, 유효성 통합 | 클래스 수 증가 |
| 빌더 패턴 (Builder Pattern) | 복잡 객체 생성 | 선택적 매개변수 다 | 순서 무관 명시적 설정 | 보일러플레이트 코드 |
| 메서드 체이닝 (Method Chaining) | 플루언트 API | 설정 계열 호출 | 가독성 높음 | 디버깅 어려움 |
| 가변 인수 (Varargs) | 동종 복수 전달 | 동일 타입 N개 | 유연한 개수 | 타입 안전성 저하 |

데이터 클럼프 (Data Clumps) 코드 스멜은 "항상 함께 다니는 변수 묶음"이고, 파라미터 객체화는 그 해결책 중 하나다. 데이터 클럼프가 <strong>필드</strong>로 나타나면 클래스 분리 (Extract Class) 를, <strong>매개변수</strong>로 나타나면 파라미터 객체화를 적용한다.

- **📢 섹션 요약 비유**: 학교 소풍 준비물 목록이 공책, 연필, 가방에 따로따로 있으면 혼란스럽다 — "소풍 키트" 하나로 묶는 게 파라미터 객체화다.

---

## Ⅳ. 실무 적용 및 실무자 판단
자바 16+ Record 문법은 파라미터 객체 구현을 극도로 단순화한다.

```java
// Java Record — 불변 파라미터 객체
public record DateRange(LocalDate from, LocalDate to) {
    public DateRange {
        if (from.isAfter(to))
            throw new IllegalArgumentException("from > to");
    }
    public boolean contains(LocalDate date) {
        return !date.isBefore(from) && !date.isAfter(to);
    }
}
```

외부 REST API (Representational State Transfer Application Programming Interface) 설계 시, 쿼리 파라미터 묶음을 <strong>요청 DTO (Data Transfer Object)</strong> 로 캡슐화하면 버전 변경 없이 필드를 추가할 수 있어 하위 호환성 (Backward Compatibility) 을 유지한다.

- <strong>DDD (Domain-Driven Design)</strong>: 파라미터 객체 -> 값 객체 -> 도메인 엔티티 (Domain Entity) 로 발전하는 경로를 설명하면 높은 점수를 받는다.
- **유지보수 비용**: 시그니처 변경 없이 기능 확장 가능 -> 변경 비용 (Change Cost) 절감 논거로 활용한다.

### 판단 체크리스트
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. 리팩토링 단위를 작게 나눠 롤백 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 배달 앱에서 주문할 때 "집 주소", "층수", "도어락 번호"를 매번 입력하는 대신 "배달지 프로필"을 저장해두는 것과 같은 원리다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | 객체화 전 | 객체화 후 |
|:---|:---:|:---:|
| 메서드 시그니처 매개변수 수 | 평균 6.2개 | 평균 1.8개 |
| 매개변수 순서 실수 버그 | 월 3건 | 0건 |
| 신규 조건 추가 변경 파일 수 | 8개 | 1개 |
| 유효성 검사 중복 코드 | 4곳 | 1곳 (VO 내부) |

파라미터 객체화 (Introduce Parameter Object) 는 단순한 코드 정리를 넘어, <strong>도메인 언어 (Domain Language) 를 코드에 끌어들이는 출발점</strong>이다. 날짜 범위, 금액 범위, 좌표 쌍 같은 개념은 원시 타입 대신 의미 있는 객체로 표현되어야 시스템 전체의 가독성과 신뢰성이 높아진다.

확장 방향은 ① 정적 분석 자동화, ② 아키텍처 적합성 검증, ③ 작은 단위의 상시 리팩토링 문화 정착이다.

- **📢 섹션 요약 비유**: 음악 앨범은 개별 트랙 파일 수십 개보다 하나의 앨범 패키지로 묶여야 제목, 발매일, 아티스트 정보를 일관되게 관리할 수 있다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 리팩토링 (Refactoring) | 외부 동작 불변 하에 내부 구조 개선 |
| 상위 개념 | 코드 스멜 (Code Smell) | 긴 매개변수 목록 스멜 해결 |
| 연관 개념 | 값 객체 (Value Object, VO) | 파라미터 객체의 불변 심화 형태 |
| 연관 개념 | 데이터 클럼프 (Data Clumps) | 파라미터 객체화의 주요 대상 스멜 |
| 연관 개념 | 빌더 패턴 (Builder Pattern) | 선택적 매개변수 처리 대안 |
| 연관 개념 | DTO (Data Transfer Object) | API 계층에서의 파라미터 객체 응용 |
| 하위 개념 | Java Record | 파라미터 객체 구현 현대적 수단 |

### 📈 관련 키워드 및 발전 흐름도
long parameter list -> 파라미터 객체화 -> value object

### 👶 어린이를 위한 3줄 비유 설명
1. 친구한테 심부름을 부탁할 때 "우유, 빵, 계란, 버터, 치즈 가져다줘" 하는 것보다 "냉장고 목록 카드"를 주는 게 훨씬 쉽다.
2. 카드에는 나중에 "요거트"도 추가할 수 있지만, 말로 전달하면 매번 새로 외워야 한다.
3. 파라미터 객체화는 바로 그 "심부름 카드"를 만드는 작업이다.
