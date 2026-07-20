---
title: "Multi Model Db"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
- **본질**: 다중 모델 DB는 문서·그래프·키-값을 단일 스토리지 엔진에서 통합 지원하여 Polyglot Persistence의 운영 복잡성 없이 여러 데이터 모델을 한 플랫폼에서 처리한다.
- **가치**: 쿼리 하나로 문서 조회->그래프 탐색->키-값 캐시를 오가는 크로스-모델 쿼리가 가능하여, 마이크로서비스 환경에서 DB 수를 줄이고 데이터 일관성을 높인다.
- **판단 포인트**: 단일 모델에서 극한 성능이 필요하면 전용 DB가 유리하지만, 다양한 데이터 모델을 중간 이상의 성능으로 활용하면서 운영 단순화가 목표라면 Multi-Model DB가 올바른 선택이다.

---

## Ⅰ. 개요 및 필요성

### Polyglot Persistence의 딜레마

```text
전통적 Polyglot Persistence 아키텍처:

  마이크로서비스
  +------------------------------------------------------+
  |  사용자 서비스 -> MongoDB  (문서형)                    |
  |  관계 서비스  -> Neo4j    (그래프)                    |
  |  세션 서비스  -> Redis    (키-값)                     |
  |  검색 서비스  -> Elasticsearch (검색)                 |
  +------------------------------------------------------+

  문제점:
  ① 4개 DB의 별도 운영·모니터링·백업
  ② DB 간 데이터 동기화·일관성 유지
  ③ 팀원이 4개 DB 모두 숙달해야 함
  ④ 네트워크 홉 증가 -> 지연 누적

Multi-Model DB 해결책:
  마이크로서비스 -> ArangoDB (모든 모델 통합)
```

### 대표 솔루션 비교

| 솔루션 | 지원 모델 | 쿼리 언어 | 특징 |
|:---:|:---:|:---:|:---|
| **ArangoDB** | 문서+그래프+KV | AQL (ArangoDB Query Language) | 성숙한 엔터프라이즈 솔루션 |
| **SurrealDB** | 문서+그래프+관계형 | SurrealQL | 신규, 서버리스+임베디드 지원 |
| **OrientDB** | 문서+그래프 | SQL 확장 | 멀티모델 선구자(유지보수 위험) |
| **CosmosDB** | KV+문서+그래프+컬럼 | SQL/Gremlin/Cassandra | Azure 완전 관리형 |

📢 **섹션 요약 비유**
> Multi-Model DB는 멀티탭 콘센트와 같다. 다른 콘센트 규격의 기기(데이터 모델)를 모두 꽂을 수 있는 어댑터 하나면 충분하다. 단, 고출력 기기(극한 성능)는 전용 콘센트(전문 DB)를 쓰는 게 더 안전하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ArangoDB 내부 아키텍처

```text
+----------------------------------------------------------+
|              ArangoDB 통합 아키텍처                        |
|                                                          |
|  +----------------------------------------------------+  |
|  |                  AQL 쿼리 엔진                       |  |
|  |  문서 쿼리 | 그래프 탐색 | KV 연산 통합 처리           |  |
|  +----------------------------------------------------+  |
|                           |                              |
|  +-----------------------------------------------------+ |
|  |           단일 VelocyPack 스토리지 엔진              | |
|  |  +--------------+  +-------------+  +-----------+  | |
|  |  |  Collections |  | Edge Colls  |  |  KV 컨테이너|  | |
|  |  |  (문서 저장)  |  | (그래프 관계)|  |  (키-값)   |  | |
|  |  +--------------+  +-------------+  +-----------+  | |
|  +-----------------------------------------------------+ |
|                                                          |
|  RocksDB (기본 스토리지) + MMFiles (선택)                  |
+----------------------------------------------------------+
```

### AQL (ArangoDB Query Language) 예시

```aql
// 문서 + 그래프 크로스 모델 쿼리:
// "추천 상품을 구매한 사용자들의 국가별 집계"

FOR product IN products
  FILTER product.category == "electronics"
  // 문서 조회 ^ + 그래프 탐색 v
  FOR user, purchase IN 1..1 INBOUND product._id purchased_by
    FILTER purchase.amount > 50000
    COLLECT country = user.country WITH COUNT INTO cnt
    SORT cnt DESC
    LIMIT 10
    RETURN { country, buyers: cnt }
```

### SurrealDB 핵심 특징

```text
SurrealDB (2022년 출시, 차세대 Multi-Model):

  1. 서버리스 + 임베디드 모두 지원
     (Node.js 내장, WebAssembly 빌드 가능)

  2. 실시간 쿼리 (LIVE SELECT)
     LIVE SELECT * FROM orders WHERE status = 'pending'
     -> 새 주문 발생 시 자동 알림

  3. 그래프 관계 표현 (SQL 내장)
     RELATE user:john->purchased->product:phone
     SELECT ->purchased->product.* FROM user:john

  4. 레코드 링크 (JOIN 없는 참조)
     SELECT *, ->friends->user.name AS friendNames
     FROM user:alice
```

### 다중 모델 통합 쿼리 아키텍처

```text
단일 AQL 쿼리 처리 흐름:

쿼리: "특정 사용자의 친구(그래프)가 구매한 상품(문서)의 카테고리 집계"

1. 사용자 문서 조회    (Document Model)
2. 친구 관계 탐색      (Graph Model: 1홉)
3. 친구별 구매 목록    (Document Model)
4. 카테고리 집계       (Analytics)

-> 네트워크 홉 0 (단일 DB 내부 처리)
-> 일관된 트랜잭션 (ACID 보장)
```

📢 **섹션 요약 비유**
> AQL의 크로스모델 쿼리는 한 번의 쇼핑으로 백화점(문서), 주차장(그래프), 편의점(KV)을 모두 들르는 것과 같다. 각 층을 따로 다니는 것(별도 DB 호출)보다 훨씬 빠르고, 계산도 한 번에 끝난다.

---

## Ⅲ. 비교 및 연결

### Multi-Model DB vs 전용 DB 트레이드오프

| 관점 | Multi-Model DB | 전용 DB 조합 |
|:---:|:---:|:---:|
| <strong>성능</strong> | 각 모델의 70~90% | 각 모델 100% |
| **운영 복잡도** | 낮음 (1개 DB) | 높음 (N개 DB) |
| <strong>일관성</strong> | 단일 트랜잭션 가능 | 분산 트랜잭션 필요 |
| **팀 러닝 커브** | 1개 쿼리 언어 | N개 쿼리 언어 |
| **비용** | 라이선스 단순화 | DB별 라이선스 |
| **적합 규모** | 중소~중대형 | 대형 (모델별 극한 성능) |

### Azure Cosmos DB의 Multi-Model 접근

```text
Azure Cosmos DB 다중 API:
  - Core (SQL) API  -> 문서형
  - MongoDB API     -> MongoDB 호환
  - Cassandra API   -> CQL 호환
  - Gremlin API     -> 그래프 탐색
  - Table API       -> 키-값

공통: 글로벌 분산, 5가지 일관성 수준, 99.999% SLA
-> 기존 MongoDB/Cassandra 앱을 마이그레이션 용이
```

📢 **섹션 요약 비유**
> Cosmos DB의 멀티 API는 같은 원어민 선생님이 한국어, 영어, 일본어로 동시에 강의하는 것과 같다. 학생(기존 앱)은 자신이 익숙한 언어(API)로 소통하면 되고, 선생님(Cosmos DB)은 내부에서 하나의 스토리지를 공유한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Multi-Model DB 도입 시나리오

```text
적합한 도입 시나리오:
  ✅ 소~중규모 스타트업: 빠른 기능 개발, 인프라 단순화
  ✅ IoT + 소셜 기능: 센서 데이터(문서) + 기기 관계(그래프)
  ✅ 지식 관리 플랫폼: 콘텐츠(문서) + 연관 개념(그래프)
  ✅ 기존 Polyglot를 단순화하고 싶은 팀

신중해야 할 시나리오:
  ⚠️ 초당 수백만 그래프 홉 탐색 (Neo4j가 우월)
  ⚠️ 100만+ QPS 단순 KV 캐시 (Redis가 우월)
  ⚠️ 페타바이트급 컬럼 저장 (Cassandra가 우월)
```

### ArangoDB Foxx 마이크로서비스

```text
ArangoDB Foxx: DB 내부에 REST API 직접 배포

// DB 서버에서 직접 실행되는 JavaScript 마이크로서비스
router.get('/recommendations/:userId', function(req, res) {
  const userId = req.pathParams.userId;
  const result = db._query(`
    FOR user IN users FILTER user._key == @id
    FOR product IN 1..2 OUTBOUND user purchased_by
    RETURN DISTINCT product
  `, {id: userId});
  res.json(result.toArray());
});
```

📢 **섹션 요약 비유**
> Multi-Model DB 도입 판단은 팔방미인(Multi-Model) 사원을 뽑을지, 각 분야 전문가(전용 DB)를 뽑을지 결정하는 것과 같다. 회사 규모가 작을 때는 팔방미인 한 명이 훨씬 효율적이지만, 규모가 커지면 전문가 팀이 필요하다.

---

## Ⅴ. 기대효과 및 결론

### Multi-Model DB 도입 효과 정량화

| 항목 | Polyglot 4 DB | ArangoDB 단일 | 개선 |
|:---:|:---:|:---:|:---:|
| 운영 서버 수 | 12개 (3DB × 4노드) | 3개 | 75% 절감 |
| 크로스-모델 쿼리 지연 | 200ms (4번 네트워크) | 20ms (단일 DB) | 90% 감소 |
| 개발자 학습 DB 수 | 4개 언어 | 1개 (AQL) | — |
| 일관성 보장 | 분산 트랜잭션 복잡 | 단일 ACID | — |

### 결론
Multi-Model DB는 Polyglot Persistence의 운영 복잡성을 근본적으로 줄이는 실용적 대안이다. ArangoDB의 성숙도와 SurrealDB의 혁신적 서버리스 지원으로 선택 폭이 넓어지고 있다. 심화 학습에서는 <strong>Polyglot Persistence 문제점</strong>, <strong>Multi-Model DB의 크로스-모델 쿼리 이점</strong>, <strong>AQL 문법의 문서+그래프 통합 원리</strong>, <strong>성능 트레이드오프 판단 기준</strong>이 핵심 논점이다.

📢 **섹션 요약 비유**
> Multi-Model DB를 도입하는 팀은 여러 언어를 구사하는 통역사 없이 직접 소통하는 글로벌 팀과 같다. 처음에는 "한 DB가 모든 걸 잘 할 수 있을까?" 의심하지만, 중간 규모의 비즈니스에서는 통역사 비용(운영 복잡도)을 줄이는 것이 전문성의 일부를 포기하는 것보다 훨씬 가치 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---:|:---:|:---|
| Polyglot Persistence | 문제 맥락 | 용도별 다양한 DB 사용 아키텍처 |
| AQL | 쿼리 언어 | ArangoDB 통합 쿼리 언어 |
| VelocyPack | 스토리지 형식 | ArangoDB 바이너리 직렬화 포맷 |
| SurrealQL | 쿼리 언어 | SurrealDB 차세대 쿼리 언어 |
| Foxx | 확장 기능 | ArangoDB 내장 마이크로서비스 |


### 📈 관련 키워드 및 발전 흐름도

```text
[폴리글롯 퍼시스턴스 (Polyglot Persistence) — 용도별 최적 DB를 따로 운영, 운영 복잡도^]
    |
    v
[다중 모델 DB (Multi-Model DB) — 단일 엔진에서 도큐먼트·그래프·키-값 통합 처리]
    |
    v
[ArangoDB — AQL 통합 쿼리 언어로 3가지 모델 일관성 있게 접근]
    |
    v
[SurrealDB — SurrealQL로 레코드·그래프·스키마리스를 단일 플랫폼에서 처리]
    |
    v
[엣지 AI + 다중 모델 DB — IoT 엣지에서 그래프+시계열+도큐먼트를 경량 DB 하나로 통합]
```

이 흐름은 폴리글롯 퍼시스턴스의 운영 복잡도를 해소하기 위해 다중 모델 DB가 등장하고, ArangoDB·SurrealDB가 통합 쿼리 언어로 구현 복잡도를 낮추며, 엣지 AI 환경에서 경량 통합 DB로 진화하는 데이터베이스 통합 아키텍처의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Multi-Model DB는 스위스 아미 나이프처럼 하나의 도구에 여러 기능이 있어요 — 칼(문서)·가위(그래프)·드라이버(KV)를 따로 챙길 필요가 없어요.
2. 여러 DB를 쓰면 마치 학교·병원·은행 모두 따로 다녀야 하는 것처럼 번거롭지만, Multi-Model DB는 이 모두를 한 건물에서 처리할 수 있어요.
3. 단, 아주 전문적인 수술(극한 성능)이 필요하면 종합병원보다 전문 병원(전용 DB)에 가는 게 나을 수 있어요.
