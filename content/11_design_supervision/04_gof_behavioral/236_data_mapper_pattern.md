---
title: "Data Mapper Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 236
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 매퍼 (Data Mapper) 는 비즈니스 도메인 객체와 DB (Database) 영속성 레이어를 완전히 분리하여, 도메인 객체는 DB 존재를 모르고 별도 Mapper 클래스가 두 세계를 연결한다.
> 2. **가치**: 도메인 객체가 순수 POJO (Plain Old Java Object) 로 유지되어 단위 테스트가 용이하고, DDD (Domain-Driven Design) 에서 요구하는 도메인 모델 순수성을 보장한다.
> 3. **판단 포인트**: 비즈니스 로직이 복잡하고 도메인 모델이 테이블 구조와 다를 경우 데이터 매퍼가 필수이며, 단순 CRUD 앱은 Active Record (액티브 레코드) 가 생산성이 높다.

---

## Ⅰ. 개요 및 필요성
액티브 레코드 패턴은 빠른 개발을 가능하게 하지만, 도메인 객체와 DB (Database) 테이블 구조가 달라지거나 비즈니스 로직이 복잡해지면 한계가 드러난다. 특히:

- <strong>테이블 구조 ≠ 도메인 모델</strong>: `User`가 세 개의 테이블에 분산 저장되어야 할 경우
- <strong>상속 계층과 DB</strong>: 클래스 상속을 어떻게 테이블에 매핑할지 (STI, CTI 등)
- **비즈니스 로직의 순수성**: 도메인 객체가 `save()`를 알면 테스트 시 DB가 항상 필요

데이터 매퍼 패턴은 이러한 문제를 **분리(Separation)** 로 해결한다. Mapper 클래스 (또는 현대의 Repository) 가 도메인 ↔ DB 변환을 전담하며, 도메인 객체는 완전히 무지한 상태(Persistence Ignorant) 를 유지한다.

| 시대 | 구현 | 특징 |
|:---:|:---|:---|
| 2002 | PEAA Data Mapper (마틴 파울러) | 개념 정의 |
| 2000s | Hibernate (Java) | 첫 대규모 데이터 매퍼 ORM |
| 2010s | Spring Data JPA | Repository 인터페이스로 추상화 |
| 현재 | TypeORM, Prisma, SQLAlchemy | 현대 언어 구현체 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 외교관이 두 나라 사이에서 번역과 협상을 담당하듯, 데이터 매퍼는 객체 세계와 데이터베이스 세계 사이의 전문 통역사다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+----------------------------------------------------------------+
|                  Data Mapper 아키텍처                           |
|                                                                |
|  [도메인 레이어]         [매퍼 레이어]          [영속성 레이어]   |
|                                                                |
|  +--------------+       +-----------------+  +--------------+ |
|  |  User        |       |   UserMapper    |  |  DB Table    | |
|  |  (순수 객체) |<------->|  (변환 전담)     |<--->|  users       | |
|  |  - id        |       |  + toEntity()   |  |  id          | |
|  |  - name      |       |  + toRow()      |  |  name        | |
|  |  - email     |       |  + findById()   |  |  email       | |
|  |              |       |  + save()       |  |  created_at  | |
|  |  DB 모름!    |       +-----------------+  +--------------+ |
|  +--------------+                                              |
|                                                                |
|  +--------------+       +-----------------+                   |
|  |  Service     |------->|  UserRepository | <- 현대적 추상화    |
|  |  (비즈니스)   |       |  (인터페이스)    |                   |
|  +--------------+       +-----------------+                   |
+----------------------------------------------------------------+
```

```java
// 도메인 객체 - DB 완전 무지
public class User {
    private Long id;
    private String name;
    private Email email;  // Value Object, DB는 String

    public boolean isAdmin() {
        return email.getDomain().equals("company.com");
    }
    // save() 같은 DB 메서드 없음
}

// 매퍼/레포지토리 - 변환 전담
@Repository
public class UserJpaRepository implements UserRepository {
    @Override
    public User findById(Long id) {
        UserEntity entity = jpaRepo.findById(id).orElseThrow();
        return UserMapper.toDomain(entity);  // Entity -> Domain 변환
    }

    @Override
    public void save(User user) {
        UserEntity entity = UserMapper.toEntity(user);  // Domain -> Entity 변환
        jpaRepo.save(entity);
    }
}
```

| 레이어 | 책임 | DB 의존 |
|:---|:---|:---:|
| Domain Object (도메인 객체) | 비즈니스 로직만 | ❌ |
| Mapper / Repository | 변환 + 영속성 조작 | ✅ |
| Entity (JPA) | DB 테이블 매핑 구조체 | ✅ |
| Service | 유즈케이스 오케스트레이션 | ❌ |

- **📢 섹션 요약 비유**: 셰프(도메인 객체)는 요리만 하고, 웨이터(매퍼)가 주방과 손님 사이를 오가며 음식을 날라준다. 셰프는 홀 구조를 몰라도 된다.

---

## Ⅲ. 비교 및 연결
| 항목 | Data Mapper | Active Record |
|:---|:---|:---|
| 도메인 순수성 | ✅ 완전 분리 | ❌ DB 메서드 포함 |
| 구현 코드량 | 많음 | 적음 |
| 테스트 용이성 | ✅ Mock Repository | ❌ DB 필요 |
| DDD 적합성 | ✅ | ❌ |
| 복잡 매핑 지원 | ✅ (Aggregate 등) | 제한적 |
| 학습 곡선 | 높음 | 낮음 |
| 대표 프레임워크 | Hibernate, JPA, TypeORM | Rails, Laravel Eloquent |

```
+----------------------------------------------------+
|            Clean Architecture 레이어                |
|                                                    |
|  +------------------+  <- 데이터 매퍼가 보호하는 영역|
|  |   Entities (도메인) |                           |
|  +------------------+                             |
|  +------------------+                             |
|  |   Use Cases      |                             |
|  +------------------+                             |
|  +------------------+  <- 데이터 매퍼/리포지토리     |
|  |   Interface Adapters |  (Infrastructure)       |
|  +------------------+                             |
|  +------------------+                             |
|  |   Frameworks/DB  |                             |
|  +------------------+                             |
+----------------------------------------------------+
```

데이터 매퍼 패턴은 Clean Architecture의 **Infrastructure Layer** 에 위치하며, Domain Layer를 DB 변화로부터 보호한다.

- **📢 섹션 요약 비유**: 성의 해자(매퍼)가 외부(DB 변경)로부터 성 내부(도메인 로직)를 보호한다. 해자를 건너지 않으면 성 안으로 들어올 수 없다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
// 1. 도메인 인터페이스 (Infrastructure 모름)
public interface UserRepository {
    Optional<User> findById(UserId id);
    void save(User user);
}

// 2. JPA 구현체 (Infrastructure 레이어)
@Repository
class JpaUserRepository implements UserRepository {
    // JPA Entity ↔ Domain User 변환
}

// 3. 서비스에서 사용 (DB 코드 없음)
@Service
class UserService {
    UserService(UserRepository repo) { ... }
    User getUser(UserId id) {
        return repo.findById(id)
                   .orElseThrow(UserNotFoundException::new);
    }
}
```

| 복잡도 | 상황 | 전략 |
|:---:|:---|:---|
| 단순 | 1:1 클래스-테이블 | Spring Data JPA 기본 사용 |
| 중간 | Value Object, 연관관계 | MapStruct 자동 매핑 |
| 복잡 | Aggregate Root, 상속 | 수동 Mapper 구현 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 데이터 매퍼는 두 언어를 구사하는 통역사다. 한국어(도메인)와 SQL(DB)을 모두 알고, 두 세계가 서로를 몰라도 소통하게 해준다.

---

## Ⅴ. 기대효과 및 결론
데이터 매퍼 패턴 도입의 효과:

- **테스트 가능성**: Repository를 Mock으로 교체하면 DB 없이 서비스 레이어 완전 테스트
- **DB 변경 격리**: PostgreSQL -> MongoDB 이전 시 매퍼만 교체, 도메인 코드 변경 없음
- <strong>도메인 풍부화</strong>: DB 제약 없이 도메인 객체에 비즈니스 메서드 자유롭게 추가
- **팀 분업**: 백엔드 도메인 개발자와 DBA (Database Administrator) 가 독립적으로 작업

실무 관점에서, 데이터 매퍼는 **"좋은 설계는 변화에 강하다"** 는 원칙의 구체적 구현이다. DB가 바뀌어도 비즈니스 로직은 흔들리지 않아야 한다는 Clean Architecture의 핵심 철학과 일치한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 집의 전기 배선(DB 구조)이 바뀌어도 가전제품(도메인 로직)은 그대로 쓸 수 있도록, 콘센트(매퍼)가 두 세계를 연결한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | ORM (Object-Relational Mapping) | 데이터 매퍼가 속하는 기술 범주 |
| 상위 개념 | Clean Architecture | 데이터 매퍼로 Infrastructure 분리 |
| 하위 개념 | Repository Pattern | 데이터 매퍼의 현대적 추상화 |
| 연관 개념 | Active Record | 대조 패턴 (결합 vs 분리) |
| 연관 개념 | DDD (Domain-Driven Design) | 데이터 매퍼와 친화적 설계 방법론 |
| 연관 개념 | Unit of Work | 트랜잭션 범위 내 변경 추적 패턴 |

### 📈 관련 키워드 및 발전 흐름도
persistence separation -> 데이터 매퍼 패턴 -> repository/unit of work

### 👶 어린이를 위한 3줄 비유 설명
1. 요리사(도메인)는 요리만 하고, 배달원(매퍼)은 음식을 냉장고(DB)에서 꺼내고 넣는 일만 해.
2. 요리사는 냉장고가 어디 있는지, 어떻게 생겼는지 전혀 몰라도 돼.
3. 냉장고가 바뀌어도(DB 교체) 요리사는 계속 같은 방식으로 요리할 수 있어!
