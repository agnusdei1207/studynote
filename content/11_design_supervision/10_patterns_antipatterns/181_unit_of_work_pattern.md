---
title: "Unit of Work Pattern"
date: "2026-05-06"
tags:
  - "studynote-design-supervision"
weight: 181
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 유닛 오브 워크 패턴 (Unit of Work Pattern)은 하나의 비즈니스 트랜잭션 안에서 생긴 객체의 추가·수정·삭제를 추적해 커밋 시점에 한꺼번에 반영하는 변경 관리 패턴이다.
> 2. **가치**: 중간마다 개별 SQL을 날리지 않아 데이터 일관성과 데이터베이스 왕복 효율을 함께 확보할 수 있으며, Repository와 ORM (Object-Relational Mapping) 계층의 핵심 기반이 된다.
> 3. **판단 포인트**: Unit of Work의 성패는 경계를 짧고 명확하게 잡는 데 있다. 짧은 트랜잭션에는 강하지만, 장시간 유지하거나 대량 데이터를 한 컨텍스트에 쌓아 두면 메모리 증가·예상치 못한 Flush·동시성 문제가 생긴다.

---

## Ⅰ. 개요 및 필요성

비즈니스 작업 하나가 보통 엔티티 하나만 바꾸는 경우는 드물다. 주문 생성은 주문 엔티티, 재고 수량, 결제 상태, 포인트 적립 여부를 함께 바꿀 수 있고, 회원 탈퇴는 회원 상태, 권한, 연관 데이터 정리를 동시에 요구한다. 이런 변경을 객체마다 즉시 저장하면 SQL 호출이 잘게 쪼개지고 중간 실패 시 부분 반영 위험이 커진다.

Unit of Work는 이 문제를 해결하기 위해 등장했다. 핵심 아이디어는 "지금 당장 DB에 쓰지 말고, 한 업무 단위에서 무슨 일이 바뀌었는지 먼저 기억하자"다. 그리고 트랜잭션 커밋 시점에 새 객체는 INSERT, 변경 객체는 UPDATE, 삭제 객체는 DELETE로 묶어 반영한다.

Martin Fowler의 PoEAA (Patterns of Enterprise Application Architecture)에서 정리된 이 패턴은 오늘날 JPA/Hibernate의 영속성 컨텍스트, Entity Framework의 DbContext, SQLAlchemy의 Session 같은 형태로 널리 구현되어 있다. 즉 Unit of Work는 특정 프레임워크 기능이 아니라, <strong>엔터프라이즈 애플리케이션이 변경을 안전하게 모아 처리하는 공통 원리</strong>다.

- **📢 섹션 요약 비유**: Unit of Work는 장을 보면서 물건마다 바로 계산하지 않고, 카트에 담아 둔 뒤 계산대에서 한 번에 결제하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Unit of Work는 보통 Identity Map, 변경 추적, Flush, 트랜잭션 커밋과 함께 작동한다. 먼저 조회된 객체를 같은 컨텍스트 안에 유지해 동일 객체를 재사용하고, 그 객체가 새로 생겼는지, 바뀌었는지, 삭제 예약되었는지 상태를 기록한다. 이후 Flush 단계에서 SQL을 생성해 DB 트랜잭션으로 내보낸다.

| 구성 요소 | 역할 | 대표 구현 예 |
| :--- | :--- | :--- |
| Identity Map | 같은 트랜잭션에서 동일 엔티티 중복 로딩 방지 | JPA 1차 캐시 |
| New / Dirty / Removed List | INSERT / UPDATE / DELETE 대상 추적 | Change Tracker, Dirty Checking |
| Flush | 메모리 변경 사항을 SQL로 변환 | `flush()` |
| Commit / Rollback | 전체 반영 또는 전체 취소 | `commit()`, `rollback()` |
| Repository | 도메인 로딩·저장을 추상화 | `find`, `save` 등 |

아래 그림은 Unit of Work가 "객체 변경 회계장부"처럼 동작한다는 점을 보여 준다.

```text
+----------------------------------------------------------------------+
| Unit of Work inside one business transaction                        |
+----------------------------------------------------------------------+
| Application Service                                                 |
|    | load / modify / remove via Repository                          |
|    v                                                                |
| Unit of Work                                                        |
|   +- Identity Map      : loaded entities                            |
|   +- New Objects       : INSERT queue                               |
|   +- Dirty Objects     : UPDATE queue                               |
|   +- Removed Objects   : DELETE queue                               |
|            |                                                        |
|            +- flush()    -> SQL generation / batching               |
|            +- rollback() -> discard tracked changes                 |
|                                                                      |
| Database transaction commits all or nothing                         |
+----------------------------------------------------------------------+
```

JPA/Hibernate에서는 이 메커니즘이 영속성 컨텍스트로 구현된다. 엔티티를 조회하면 1차 캐시에 올라가고, 트랜잭션 안에서 필드를 바꾸면 스냅샷과 현재 상태를 비교하는 Dirty Checking으로 UPDATE가 준비된다. 즉 `save()`를 반복 호출하지 않아도 Unit of Work가 "무엇이 달라졌는지"를 알아낸다.

여기서 중요한 구분은 Flush와 Commit이다. Flush는 SQL을 DB에 보내는 동작이고, Commit은 DB 트랜잭션을 확정하는 동작이다. 그래서 Flush가 먼저 일어나도 Commit 전이면 Rollback으로 되돌릴 수 있다. 이 차이를 모르면 ORM의 동작을 오해하기 쉽다.

- **📢 섹션 요약 비유**: Unit of Work는 회계 장부에 입출금을 먼저 적어 두고, 마감 시점에 최종 합계를 확정하는 회계팀과 같다.

---

## Ⅲ. 비교 및 연결

Unit of Work는 즉시 저장 방식과 비교할 때 차이가 분명하다. 즉시 저장은 이해하기 쉽지만 변경이 많을수록 SQL 왕복과 부분 실패 위험이 커진다. 반면 Unit of Work는 한 비즈니스 경계를 기준으로 변경을 묶기 때문에 일관성과 성능을 동시에 챙기기 쉽다.

| 비교 축 | 즉시 저장 방식 | Unit of Work |
| :--- | :--- | :--- |
| 저장 시점 | 객체 변경 직후 곧바로 DB 반영 | 커밋 또는 Flush 시점에 일괄 반영 |
| DB 왕복 | 많아지기 쉬움 | 상대적으로 적음 |
| 부분 실패 위험 | 높음 | 트랜잭션 경계 안에서 낮음 |
| 코드 표현 | `save()` 호출이 자주 등장 | 변경 추적이 자동화되는 경우가 많음 |
| 주의점 | 중복 저장, 일관성 깨짐 | 컨텍스트가 길어지면 메모리와 동시성 이슈 |

이 패턴은 Transaction Script와 Domain Model 양쪽 모두와 연결된다. Transaction Script를 쓰더라도 내부 저장 계층이 Unit of Work를 제공할 수 있고, Domain Model에서는 Aggregate의 불변식을 유지한 뒤 Repository를 통해 한 번에 반영하기 때문에 더 자연스럽게 결합된다. 즉 Unit of Work는 상위 설계 스타일과 독립적으로, <strong>저장 일관성을 지키는 하부 메커니즘</strong>이다.

또한 Lazy Loading, Repository, Optimistic Locking과도 밀접하다. 조회된 객체를 같은 컨텍스트가 관리하므로 지연 로딩이 가능하고, 버전 필드 비교로 동시 수정 충돌도 커밋 시점에 감지할 수 있다. 반대로 이 메커니즘을 모르고 쓰면 "왜 SQL이 지금 나가지?", "왜 수정이 자동 저장됐지?" 같은 혼란이 생긴다.

- **📢 섹션 요약 비유**: 즉시 저장이 물건 하나 집을 때마다 카드 결제하는 방식이라면, Unit of Work는 카트에 담아 최종 합계만 한 번 결제하는 방식과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 Unit of Work 경계를 "유스케이스 하나" 수준으로 짧게 잡는 것이 기본이다. 웹 요청 하나, 서비스 메서드 하나, 메시지 처리 한 건처럼 명확한 비즈니스 경계 안에서만 유지해야 한다. 경계가 길어지면 오래된 스냅샷을 쥔 채 메모리를 많이 먹고, 예상하지 못한 자동 Flush나 동시성 충돌을 일으키기 쉽다.

| 실무 상황 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 주문 생성, 결제 승인, 정산 확정 | 적극 활용 | 여러 엔티티 변경을 원자적으로 묶기 좋음 |
| 대량 배치 업데이트 | 구간별 Flush / Clear | 한 컨텍스트에 너무 많이 쌓이면 메모리 부담 |
| 화면 세션 전체를 하나의 UoW로 유지 | 지양 | 장수명 컨텍스트로 인한 stale data와 충돌 위험 |
| Repository 메서드마다 개별 Commit | 지양 | 상위 유스케이스 일관성 경계가 깨짐 |

### 실무 체크리스트

1. Unit of Work 경계가 한 유스케이스 또는 한 트랜잭션 안으로 명확히 제한되어 있는가?
2. Dirty Checking에 의존하는 엔티티 수정이 실제로 트랜잭션 범위 안에서 일어나는가?
3. 대량 처리에서는 `flush()`와 `clear()` 주기를 설계해 메모리 폭증을 막고 있는가?
4. 낙관적 잠금 (Optimistic Locking)이나 비관적 잠금 전략을 함께 검토했는가?
5. SQL 로그와 Flush 시점을 파악할 수 있도록 관측성을 확보했는가?

### 자주 발생하는 안티패턴

- Repository가 메서드마다 자체 Commit을 수행해 상위 서비스의 원자성을 깨뜨리는 구조
- 웹 화면 전환 전체를 하나의 장수명 영속성 컨텍스트로 잡아 메모리와 충돌 문제를 키우는 구조
- Detached 엔티티를 수정해 놓고 자동 저장될 것이라 오해하는 구현
- 대량 배치에서 수만 건을 한 컨텍스트에 쌓아 놓고 Flush / Clear를 하지 않는 운영

학습 정리에서는 <strong>"Unit of Work는 객체 변경을 트랜잭션 단위로 추적해 커밋 시 일괄 반영하는 패턴이며, JPA 영속성 컨텍스트의 1차 캐시·Dirty Checking·Flush 메커니즘이 대표 구현"</strong>이라고 정리하면 핵심이 살아난다.

- **📢 섹션 요약 비유**: Unit of Work를 잘 쓰는 팀은 한 장의 업무 전표로 입금·출금·수정 내역을 묶어 처리하고, 못 쓰는 팀은 칸마다 따로 결재를 올려 중간에 서류가 어긋나는 셈이다.

---

## Ⅴ. 기대효과 및 결론

Unit of Work의 장점은 명확하다. 변경을 한 번에 반영하므로 데이터베이스 왕복이 줄고, 한 유스케이스 안의 변경을 원자적으로 묶어 일관성을 지키기 쉽다. 또한 도메인 로직은 "무엇을 바꿀지"에 집중하고, 저장 계층은 "언제 어떻게 반영할지"를 책임지게 되어 코드 구조도 정리된다.

하지만 이 패턴은 보이지 않게 SQL을 만들어 주기 때문에 내부 동작을 모른 채 쓰면 오히려 위험하다. Flush 시점, Lazy Loading, 잠금 충돌, 대량 배치 메모리 사용량을 이해하지 못하면 성능과 정합성 문제를 뒤늦게 만난다. 즉 Unit of Work는 편의 기능이 아니라, <strong>트랜잭션 경계와 변경 추적을 disciplined 하게 다루게 만드는 패턴</strong>이다.

결론적으로 기억할 문장은 이렇다. "Unit of Work는 ORM의 마법이 아니라, 비즈니스 트랜잭션의 변경 내역을 회계 장부처럼 관리하는 원리다." 설계감리 관점에서는 이 경계가 짧고 명확한지, 그리고 대량 처리·동시성 상황까지 고려했는지를 보는 것이 핵심이다.

- **📢 섹션 요약 비유**: Unit of Work는 하루 종일 생긴 거래를 장부에 모아 두었다가 마감할 때 한 번에 정산하는 금고 관리 방식과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Transaction | Unit of Work가 보장하려는 원자성 경계다. |
| Repository Pattern | 도메인 로딩과 저장을 추상화해 Unit of Work와 자주 결합된다. |
| Identity Map | 같은 트랜잭션에서 동일 엔티티를 하나의 객체로 관리한다. |
| Dirty Checking | 어떤 엔티티가 수정되었는지 자동 탐지하는 핵심 메커니즘이다. |
| Lazy Loading | Unit of Work가 관리하는 컨텍스트 안에서 연관 객체를 지연 조회한다. |
| Optimistic Locking | 커밋 시점 충돌 감지를 통해 동시 수정 문제를 제어한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
비즈니스 유스케이스 시작
    |
    v
Repository로 엔티티 로드
    |
    v
Identity Map + New / Dirty / Removed 추적
    |
    +- dirty checking
    +- flush
    +- rollback / commit
    |
    v
일관된 트랜잭션 반영과 ORM 최적화
```

이 흐름은 Unit of Work가 단순 캐시가 아니라, 변경 추적에서 커밋 제어까지 이어지는 트랜잭션 관리 패턴임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감을 고치고 바꾸는 일을 할 때마다 엄마에게 바로바로 말하지 않고 메모장에 먼저 적어 두는 거예요.
2. 다 끝나면 메모장을 보고 한 번에 "이건 새로 넣고, 이건 고치고, 이건 버릴게요" 하고 정리해요.
3. 유닛 오브 워크는 이렇게 바뀐 것을 한꺼번에 정리해 주는 똑똑한 메모장이에요.
