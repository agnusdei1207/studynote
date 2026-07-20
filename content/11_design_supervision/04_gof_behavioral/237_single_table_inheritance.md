---
title: "Single Table Inheritance, STI"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 237
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: STI (Single Table Inheritance, 싱글 테이블 상속) 는 클래스 상속 계층 전체를 단일 DB (Database) 테이블로 평탄화(Flatten) 하고, `DTYPE` 구분자 컬럼으로 각 행이 어떤 하위 클래스인지 식별한다.
> 2. **가치**: 조인이 없어 조회 성능이 빠르고, JPA (Java Persistence API) 구현이 간단하지만, 모든 하위 클래스의 컬럼이 한 테이블에 모여 NULL이 많아지고 스키마가 지저분해진다.
> 3. **판단 포인트**: 하위 클래스 간 공유 컬럼이 많고 차이가 적을 때 적합하며, 하위 클래스별 고유 속성이 많아지면 CTI (Class Table Inheritance, 클래스 테이블 상속) 로 전환을 고려해야 한다.

---

## Ⅰ. 개요 및 필요성
객체지향 설계에서 상속(Inheritance)은 자연스러운 추상화 수단이다. `Employee -> FullTimeEmployee`, `Employee -> PartTimeEmployee`, `Employee -> Contractor` 같은 계층이 코드에 존재할 때, 이를 관계형 DB (Relational Database) 에 어떻게 매핑할지가 ORM (Object-Relational Mapping) 의 핵심 문제 중 하나다.

STI (Single Table Inheritance) 는 가장 단순한 전략이다—**계층 전체를 하나의 테이블로 합친다**. `employee_type` 컬럼(JPA에서는 `DTYPE`이 기본)이 어떤 서브타입인지 구분한다.

```
Employee (추상 클래스)
 +-- FullTimeEmployee   (salary 컬럼 추가)
 +-- PartTimeEmployee   (hourlyRate 컬럼 추가)
 +-- Contractor         (contractEndDate 컬럼 추가)
```

이를 STI로 매핑하면 `employees` 테이블 하나에 모든 컬럼이 모인다.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 다양한 직원 유형(정규직, 시간제, 계약직)의 서류를 하나의 서랍에 모두 넣되, 서류 오른쪽 위에 "정규직/시간제/계약직" 도장을 찍어 구분하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+--------------------------------------------------------------------+
|                  employees 테이블 (STI)                             |
|                                                                    |
|  id  | DTYPE           | name  | salary | hourly_rate | end_date   |
|  ----+-----------------+-------+--------+-------------+----------- |
|   1  | FullTimeEmployee| Alice | 5000   |   NULL      |   NULL     |
|   2  | PartTimeEmployee| Bob   | NULL   |   25.50     |   NULL     |
|   3  | Contractor      | Carol | NULL   |   NULL      | 2026-12-31 |
|   4  | FullTimeEmployee| Dave  | 6000   |   NULL      |   NULL     |
|                                                                    |
|  ※ DTYPE: JPA 기본 구분자 컬럼 (DiscriminatorColumn)              |
|  ※ NULL이 많아지는 것이 STI의 단점                                 |
+--------------------------------------------------------------------+
```

```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "DTYPE")
public abstract class Employee {
    @Id @GeneratedValue
    private Long id;
    private String name;
}

@Entity
@DiscriminatorValue("FULL")
public class FullTimeEmployee extends Employee {
    private Integer salary;
}

@Entity
@DiscriminatorValue("PART")
public class PartTimeEmployee extends Employee {
    private Double hourlyRate;
}
```

| 특성 | 내용 |
|:---|:---|
| 테이블 수 | 1개 (전체 계층 공유) |
| 조인 필요 | ❌ (단일 테이블) |
| NULL 컬럼 | 많음 (서브타입별 전용 컬럼) |
| INSERT 속도 | 빠름 |
| 조회 속도 | 빠름 (조인 없음) |
| 스키마 직관성 | 낮음 (NULL 범람) |
| NOT NULL 제약 | 사용 어려움 (서브타입 컬럼) |

- **📢 섹션 요약 비유**: 빨간칸·파란칸·초록칸이 있는 표에서, 어떤 행은 빨간칸만 채워지고 나머지는 비어있다. 공간 낭비처럼 보이지만 표 하나로 모든 걸 관리한다.

---

## Ⅲ. 비교 및 연결
| 전략 | JPA 설정 | 테이블 수 | 조인 | NULL | 추천 상황 |
|:---|:---|:---:|:---:|:---:|:---|
| STI (Single Table) | `SINGLE_TABLE` | 1 | ❌ | 많음 | 서브타입 수 적고 공통 컬럼 많을 때 |
| CTI (Class Table) | `JOINED` | 부모+자식 수 | ✅ | 없음 | 서브타입별 고유 속성 많을 때 |
| Concrete Table | `TABLE_PER_CLASS` | 자식 수 | 다형 쿼리 느림 | 없음 | 다형 쿼리 거의 없을 때 |

```
하위 클래스 수가 많은가?
      |
      +-- 아니오 (2~4개) -> STI 가능성 높음
      |
      +-- 예           -> 아래 확인
            |
            +-- 하위 클래스별 고유 컬럼이 많은가?
                    |
                    +-- 아니오 -> STI 여전히 적합
                    +-- 예    -> CTI (JOINED) 고려
```

- **📢 섹션 요약 비유**: 소규모 가족 회사에서 정규직·알바·인턴을 같은 엑셀 시트에 관리하는 건 합리적이지만, 직원이 수백 명이면 시트를 나눠야 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```
조회 성능:   STI > CTI > Concrete Table (다형 조회)
스키마 깔끔: CTI > Concrete > STI
NULL 컬럼:  CTI = 없음 / STI = 많음
```

Rails는 기본적으로 `type` 컬럼을 구분자로 사용한다:

```ruby
class Animal < ApplicationRecord; end
class Dog < Animal; end
class Cat < Animal; end

# animals 테이블: id, type, name, breed(Dog만), indoor(Cat만)
Dog.create(name: "Rex", breed: "Lab")
# -> type='Dog', name='Rex', breed='Lab', indoor=NULL
```

1. <strong>데이터 무결성</strong>: 서브타입 전용 컬럼에 NOT NULL 제약을 걸 수 없어 애플리케이션 수준에서 검증 필요
2. **테이블 비대화**: 서브타입이 늘어날수록 컬럼 수가 폭발적으로 증가
3. <strong>인덱스 전략</strong>: `DTYPE` 컬럼 인덱스 설정으로 특정 서브타입 필터링 최적화

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 공공 화장실처럼 모두가 같은 공간을 쓰면 빠르게 들어갈 수 있지만, 사용하지 않는 공간(NULL 컬럼)이 생긴다.

---

## Ⅴ. 기대효과 및 결론
STI 패턴의 선택 근거 요약:

**장점**:
- 단일 테이블이므로 쿼리가 단순하고 빠름
- ORM 설정이 간단 (JPA `SINGLE_TABLE` 한 줄)
- 다형 쿼리 (`findAll Employee`) 가 조인 없이 가능

**단점**:
- NULL 컬럼 증가 -> 스키마 가독성 저하
- NOT NULL 같은 DB 제약 적용 불가
- 서브타입 컬럼 추가 시 전체 테이블 ALTER -> 대형 테이블에서 위험

실무 관점에서 STI는 <strong>단순성과 성능을 위해 데이터 모델 순수성을 일부 희생하는 트레이드오프</strong> 다. 시스템 초기, 서브타입이 단순할 때 빠르게 개발하고, 복잡해지면 CTI로 리팩토링하는 진화적 접근이 현실적이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 처음엔 작은 집(STI) 하나로 가족 모두가 살지만, 가족이 늘면 방을 나누거나(CTI) 별채를 짓는 게 낫다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | ORM 상속 전략 | JPA SINGLE_TABLE / JOINED / TABLE_PER_CLASS |
| 대조 개념 | CTI (Class Table Inheritance) | 부모·자식 테이블 분리 전략 |
| 대조 개념 | Concrete Table Inheritance | 자식별 독립 테이블 전략 |
| 연관 개념 | DiscriminatorColumn (구분자 컬럼) | DTYPE, type 등 서브타입 식별 컬럼 |
| 연관 개념 | JPA @Inheritance | Java 상속 매핑 어노테이션 |
| 연관 개념 | Polymorphic Query (다형 쿼리) | 부모 타입으로 자식 모두 조회 |

### 📈 관련 키워드 및 발전 흐름도
상속 매핑 -> 싱글 테이블 상속 -> polymorphic query

### 👶 어린이를 위한 3줄 비유 설명
1. 강아지, 고양이, 토끼를 모두 같은 표(테이블)에 넣고, '종류' 칸에 각각 이름을 써두는 거야.
2. 강아지칸(breed)은 고양이에겐 필요 없어서 비워둬(NULL)—낭비처럼 보이지만 표 하나로 다 관리해!
3. 나중에 동물 종류가 너무 많아지면, 종류별로 표를 나누는 게(CTI) 더 깔끔해.
