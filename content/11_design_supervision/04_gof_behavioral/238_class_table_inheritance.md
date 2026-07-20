---
title: "Class Table Inheritance"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 238
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CTI (Class Table Inheritance, 클래스 테이블 상속) 는 부모 클래스와 각 자식 클래스가 별도 테이블을 갖고, 자식 테이블의 PK (Primary Key) 가 부모 테이블의 FK (Foreign Key) 를 겸해 조인으로 연결된다.
> 2. **가치**: NULL 컬럼이 없어 데이터 정합성이 높고, NOT NULL 등 DB 제약을 제대로 활용할 수 있으며, 각 클래스의 관계가 테이블 구조에 명확히 반영된다.
> 3. **판단 포인트**: 하위 클래스별 고유 속성이 많고 DB 정합성이 중요한 경우 CTI가 적합하지만, 다형 쿼리(전체 부모 조회) 시 조인 비용이 STI (Single Table Inheritance) 보다 크다.

---

## Ⅰ. 개요 및 필요성
ORM (Object-Relational Mapping) 의 상속 매핑 전략 중 CTI (Class Table Inheritance) 는 가장 <strong>관계형 데이터베이스 친화적인</strong> 방식이다. 객체 세계의 클래스 계층을 그대로 테이블 계층으로 반영한다.

STI (Single Table Inheritance) 가 "하나의 서랍에 모두 넣기"라면, CTI는 "각 서랍에 해당 서류만 넣고 서랍끼리 공통 번호로 연결하기"다.

JPA (Java Persistence API) 에서는 `@Inheritance(strategy = InheritanceType.JOINED)` 로 설정하며, 마틴 파울러의 PEAA (Patterns of Enterprise Application Architecture) 에서 Class Table Inheritance라는 이름으로 정의되었다.

```
Vehicle (추상 부모)
 +-- Car       (doors, fuelType 컬럼)
 +-- Truck     (payload, trailerHitch 컬럼)
 +-- Motorcycle (hasSidecar 컬럼)
```

각 클래스가 별도 테이블을 갖고, 자식 테이블의 `id`는 부모 `vehicles.id`를 참조한다.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 병원에서 기본 진료 기록(부모 테이블)은 모든 환자가 공유하고, 외과·내과·소아과는 각자의 전문 차트(자식 테이블)를 추가로 가지는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-------------------------------------------------------------------+
|              Class Table Inheritance 테이블 구조                   |
|                                                                   |
|  vehicles (부모 테이블)                                            |
|  +-----+------------+--------------+--------------------------+   |
|  | id  | type       | make         | model                    |   |
|  +-----+------------+--------------+--------------------------+   |
|  |  1  | Car        | Toyota       | Camry                    |   |
|  |  2  | Truck      | Ford         | F-150                    |   |
|  |  3  | Motorcycle | Honda        | CBR500                   |   |
|  +-----+------------+--------------+--------------------------+   |
|          |                  |                     |               |
|          v                  v                     v               |
|  cars                 trucks              motorcycles             |
|  +---------------+  +------------------+  +------------------+   |
|  | id(FK) | doors|  | id(FK) | payload |  | id(FK)| sidecar  |   |
|  +--------+------+  +--------+---------+  +-------+----------+   |
|  |   1    |   4  |  |   2    |  1500kg |  |   3   |  false   |   |
|  +--------+------+  +--------+---------+  +-------+----------+   |
|                                                                   |
|  ※ 자식 id = 부모 id (FK이자 PK)                                  |
+-------------------------------------------------------------------+
```

```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "type")
public abstract class Vehicle {
    @Id @GeneratedValue
    private Long id;
    private String make;
    private String model;
}

@Entity
@DiscriminatorValue("Car")
@PrimaryKeyJoinColumn(name = "id")
public class Car extends Vehicle {
    @Column(nullable = false)   // NOT NULL 제약 가능!
    private Integer doors;
    private String fuelType;
}

@Entity
@DiscriminatorValue("Truck")
public class Truck extends Vehicle {
    @Column(nullable = false)
    private Integer payloadKg;
}
```

| 특성 | CTI | STI |
|:---|:---|:---|
| 테이블 수 | 부모 + 자식 수 | 1개 |
| NULL 컬럼 | 없음 | 많음 |
| NOT NULL 제약 | 가능 | 불가 (서브타입 컬럼) |
| 단일 객체 조회 | JOIN 필요 | 단순 SELECT |
| 다형 쿼리 전체 | 여러 JOIN | 단순 SELECT |
| 스키마 정규화 | 높음 | 낮음 |

- **📢 섹션 요약 비유**: 레고로 기본 자동차 몸체(부모 테이블)를 만들고, 종류별 전용 파츠(자식 테이블)를 조립 번호(FK)로 연결하는 구조다.

---

## Ⅲ. 비교 및 연결
| 항목 | STI (SINGLE_TABLE) | CTI (JOINED) | Concrete (TABLE_PER_CLASS) |
|:---|:---:|:---:|:---:|
| 테이블 수 | 1 | N+1 | N |
| 조인 | 없음 | 있음 | 없음 (단형 쿼리) |
| NULL 컬럼 | 많음 | 없음 | 없음 |
| DB 정규화 | 낮음 | 높음 | 중간 |
| 다형 쿼리 성능 | ✅ 최고 | 중간 | ❌ 느림 (UNION) |
| NOT NULL 사용 | ❌ | ✅ | ✅ |
| 권장 사용 | 서브타입 단순 | 정합성 중요 | 다형 쿼리 없을 때 |

```
선택 기준:
1. 서브타입별 고유 속성이 많다 (3개 이상)
2. DB 수준의 NOT NULL, UNIQUE 제약이 중요하다
3. DBA (Database Administrator) 와 협업이 필요한 프로젝트
4. 서브타입이 독립적으로 쿼리되는 경우 많음
```

- **📢 섹션 요약 비유**: STI가 다목적 홀이라면 CTI는 세분화된 전용 회의실이다. 전용 회의실은 각자 특화 장비(제약)를 갖추지만, 이동(조인)이 필요하다.

---

## Ⅳ. 실무 적용 및 실무자 판단
CTI의 가장 큰 단점은 조인 비용이다. 대응 전략:

1. <strong>인덱스 설정</strong>: 자식 테이블 FK 컬럼에 인덱스 필수
2. **Fetch Type 주의**: JPA `@ManyToOne(fetch = LAZY)` 로 N+1 쿼리 방지
3. <strong>쿼리 최적화</strong>: 특정 서브타입만 조회할 경우 자식 테이블 직접 쿼리

- <strong>스키마 변경 비용</strong>: 부모 테이블 컬럼 추가는 모든 자식에 영향
- **ORM 복잡성**: Hibernate의 JOINED 전략은 SQL 생성이 복잡해 디버깅 어려움
- **마이그레이션**: 서브타입 추가 시 새 테이블 생성 + FK 제약 추가 필요

```java
// 다형 쿼리: 모든 Vehicle 조회 (자식 테이블 JOIN)
List<Vehicle> vehicles = vehicleRepository.findAll();

// 특정 서브타입만 조회 (JOIN 없음, 자식 테이블 직접)
List<Car> cars = carRepository.findByDoorsGreaterThan(2);
```

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: CTI는 전문의(자식 테이블)가 기본 병원 기록(부모 테이블)을 공유하는 병원 시스템이다. 전문의 기록은 풍부하지만, 전체 환자 현황을 보려면 모든 과의 기록을 합쳐봐야 한다.

---

## Ⅴ. 기대효과 및 결론
CTI 패턴의 실무 적용 판단:

**장점 요약**:
- 정규화된 스키마 -> 데이터 무결성 최고
- 서브타입별 NOT NULL, CHECK 제약 적용 가능
- 새 서브타입 추가가 기존 테이블에 영향 없음

**단점 요약**:
- 다형 조회 시 조인 비용 발생
- ORM 설정과 디버깅 복잡도 증가

실무자 논점: <strong>"정규화와 성능 사이의 균형"</strong> 이다. CTI는 데이터 모델링 원칙에 충실하지만, 고트래픽 환경에서는 STI의 단순함이 더 실용적일 수 있다. 시스템의 조회 패턴과 데이터 정합성 요구사항을 분석해 선택 근거를 명확히 서술해야 한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: CTI는 정리정돈이 잘 된 서재다. 책마다 제자리가 있어 찾기 쉽지만, 여러 책을 한 번에 꺼내려면 여러 선반을 돌아다녀야 한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | ORM 상속 전략 | SINGLE_TABLE / JOINED / TABLE_PER_CLASS |
| 대조 개념 | STI (Single Table Inheritance) | 단일 테이블, NULL 다수 |
| 대조 개념 | Concrete Table Inheritance | 자식별 완전 독립 테이블 |
| 하위 개념 | PrimaryKeyJoinColumn | 자식 PK = 부모 FK 설정 |
| 연관 개념 | 데이터 정규화 (Database Normalization) | CTI가 지향하는 설계 원칙 |
| 연관 개념 | JPA @Inheritance(JOINED) | Java 구현 어노테이션 |

### 📈 관련 키워드 및 발전 흐름도
상속 매핑 -> 클래스 테이블 상속 -> joined inheritance tuning

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 기록부(부모 테이블)에는 이름·학번만 쓰고, 각 동아리(자식 테이블)마다 자기 활동 기록을 따로 써.
2. 학번(FK)으로 연결되니까, "축구부 이창민"의 전체 정보를 보려면 기록부 + 축구부 기록을 같이 봐야 해.
3. 빈칸(NULL) 없이 깔끔하지만, 정보를 합칠 때는 두 표를 함께 봐야 하는 게 단점이야!
