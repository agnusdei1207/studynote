---
title: "Document Store Mongodb Elasticsearch"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 237
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 도큐먼트 저장소(Document Store)는 JSON/BSON 형태의 <strong>계층적 중첩 구조</strong>를 단일 문서(Document)로 저장하며, 각 문서가 서로 다른 필드를 가질 수 있는 <strong>스키마리스(Schema-less)</strong> 유연성을 제공한다.
> 2. **가치**: MongoDB는 복잡한 중첩 객체를 JOIN 없이 단일 문서로 저장해 <strong>읽기 성능을 극대화</strong>하고, Elasticsearch는 역인덱스(Inverted Index) 기반의 <strong>전문 검색(Full-Text Search)</strong>에 특화되어 있다.
> 3. **판단 포인트**: MongoDB는 애플리케이션 데이터 저장소, Elasticsearch는 검색·분석·로그 가시성 플랫폼으로 역할이 다르며, 많은 기업이 <strong>주 저장소(MongoDB) + 검색 인덱스(Elasticsearch)</strong> 패턴을 병행한다.

---

## Ⅰ. 개요 및 필요성

전자상거래 주문 데이터를 RDBMS로 저장하려면 orders, order_items, shipping_addresses 등 여러 테이블로 정규화하고 JOIN해야 한다. 도큐먼트 저장소는 이 데이터를 <strong>하나의 JSON 문서</strong>로 저장하여 JOIN 없이 단일 조회로 완성된 데이터를 반환한다.

```
[RDBMS vs Document Store 비교]
RDBMS:
  orders 테이블 + order_items 테이블 + addresses 테이블
  -> SELECT orders JOIN order_items JOIN addresses WHERE order_id=1

Document Store (MongoDB):
  {
    "_id": "order_001",
    "customer": {"name": "김철수", "email": "kim@email.com"},
    "shipping": {"city": "서울", "street": "강남대로 100"},
    "items": [
      {"product": "책", "qty": 2, "price": 15000},
      {"product": "노트북", "qty": 1, "price": 1500000}
    ],
    "total": 1530000,
    "status": "delivered"
  }
  -> db.orders.findOne({_id: "order_001"})  (단일 조회)
```

📢 **섹션 요약 비유**: 도큐먼트 저장소는 파일 봉투 시스템이다. 한 건의 주문 관련 서류(고객 정보, 배송지, 상품 목록)를 봉투 하나에 다 넣어두면, 해당 주문 봉투만 꺼내면 모든 정보가 있다. RDBMS는 각 서류를 별도 서랍에 보관하고 매번 꺼내 맞춰야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MongoDB 아키텍처

```
+------------------------------------------------------------+
|                   MongoDB 클러스터 구조                      |
|                                                            |
|  +------------------------------------------------------+  |
|  |  Replica Set (복제 셋)                               |  |
|  |  Primary ---> Secondary ---> Secondary (자동 장애복구) |  |
|  +------------------------------------------------------+  |
|                                                            |
|  +------------------------------------------------------+  |
|  |  Sharded Cluster (샤드 클러스터)                     |  |
|  |  mongos (라우터)                                     |  |
|  |   +-- Shard 1 (Replica Set): user_id 0~999           |  |
|  |   +-- Shard 2 (Replica Set): user_id 1000~1999       |  |
|  |   +-- Shard 3 (Replica Set): user_id 2000+           |  |
|  +------------------------------------------------------+  |
+------------------------------------------------------------+
```

### MongoDB 집계 파이프라인

```javascript
// 집계 파이프라인 예시: 월별 카테고리별 매출
db.orders.aggregate([
  { $match: { status: "completed", createdAt: { $gte: ISODate("2024-01-01") } } },
  { $unwind: "$items" },  // 배열 펼치기
  { $group: {
      _id: { month: { $month: "$createdAt" }, category: "$items.category" },
      total_revenue: { $sum: { $multiply: ["$items.price", "$items.qty"] } },
      order_count: { $sum: 1 }
  }},
  { $sort: { "_id.month": 1, total_revenue: -1 } }
])
```

### Elasticsearch 역인덱스 원리

```
[역인덱스 (Inverted Index) 구조]
문서:
  Doc 1: "Redis는 인메모리 캐시 데이터베이스이다"
  Doc 2: "Redis Cluster로 분산 캐시를 구성한다"
  Doc 3: "MongoDB는 도큐먼트 데이터베이스이다"

역인덱스:
  "Redis"      -> [Doc1, Doc2]
  "캐시"        -> [Doc1, Doc2]
  "데이터베이스" -> [Doc1, Doc3]
  "인메모리"    -> [Doc1]
  "MongoDB"    -> [Doc3]

검색: "Redis 캐시"
  -> "Redis" 히트: [Doc1, Doc2]
  -> "캐시" 히트: [Doc1, Doc2]
  -> 교집합 + TF-IDF 스코어링 -> Doc1(연관성 높음), Doc2
```

### Elasticsearch 아키텍처

```
[Elasticsearch 클러스터]
+-----------------------------------------------------+
|  Index: "products" (5 Primary Shards, Replica 1)    |
|                                                     |
|  Node 1: Shard 0 (P) + Shard 3 (R)                 |
|  Node 2: Shard 1 (P) + Shard 4 (R)                 |
|  Node 3: Shard 2 (P) + Shard 0 (R)                 |
|  Node 4: Shard 3 (P) + Shard 1 (R)                 |
|  Node 5: Shard 4 (P) + Shard 2 (R)                 |
+-----------------------------------------------------+
P = Primary, R = Replica
```

📢 **섹션 요약 비유**: 역인덱스는 책 뒷면 색인(Index)과 같다. "Redis"를 색인에서 찾으면 관련 페이지 번호가 나오듯이, ES는 단어->문서 목록 매핑으로 수억 개 문서에서도 밀리초 만에 검색 결과를 반환한다.

---

## Ⅲ. 비교 및 연결

### MongoDB vs Elasticsearch 비교

| 비교 항목 | MongoDB | Elasticsearch |
|:---|:---|:---|
| **주요 목적** | 애플리케이션 데이터 저장소 | 전문 검색·로그 분석 |
| <strong>쿼리 강점</strong> | 복잡한 CRUD, 집계 | 전문 검색, 점수 기반 랭킹 |
| <strong>스키마</strong> | 완전 스키마리스 | 매핑(동적 추론 가능) |
| <strong>트랜잭션</strong> | ACID (v4.0+, 다중 문서) | 없음 |
| <strong>쓰기 성능</strong> | 우수 | 보통 (인덱싱 오버헤드) |
| **텍스트 검색** | 기본 지원 | 탁월 (형태소 분석기) |
| **집계** | 집계 파이프라인 | Aggregation API |
| **스케일** | 수평 샤딩 | 수평 샤딩 |
| **적합 사례** | 콘텐츠 관리, 주문, 이커머스 | 검색 엔진, 로그 분석, APM |

### ELK 스택 (Elasticsearch + Logstash + Kibana)

```
[ELK 로그 분석 파이프라인]
앱 서버 로그 -> Filebeat -> Logstash (파싱/변환) -> Elasticsearch -> Kibana
             -> Kafka (버퍼) -> Logstash -> Elasticsearch

Kibana: ES 데이터 시각화 대시보드
  - 로그 검색 (Discover)
  - 대시보드 (Dashboard)
  - APM (Application Performance Monitoring)
  - SIEM (보안 이벤트 모니터링)
```

📢 **섹션 요약 비유**: MongoDB는 회사 내부 파일 서버(주문·고객 데이터 저장), Elasticsearch는 구글 검색(빠른 텍스트 검색·분석)이다. 많은 회사가 파일 서버에 저장하고, 중요 파일은 검색 시스템에도 인덱싱하는 방식으로 두 시스템을 병행한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### MongoDB 인덱싱 전략

```javascript
// 단일 필드 인덱스
db.orders.createIndex({ customer_id: 1 })  // 오름차순

// 복합 인덱스 (ESR 규칙: Equality->Sort->Range)
db.orders.createIndex({ customer_id: 1, status: 1, created_at: -1 })

// 텍스트 인덱스 (전문 검색)
db.products.createIndex({ name: "text", description: "text" })

// TTL 인덱스 (자동 만료)
db.sessions.createIndex({ expiredAt: 1 }, { expireAfterSeconds: 0 })

// 인덱스 현황 분석
db.orders.explain("executionStats").find({ customer_id: "U001" })
```

### Elasticsearch 한국어 검색 설정

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "korean_analyzer": {
          "type": "custom",
          "tokenizer": "nori_tokenizer",
          "filter": ["nori_part_of_speech", "lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": { "type": "text", "analyzer": "korean_analyzer" },
      "price": { "type": "integer" },
      "created_at": { "type": "date" }
    }
  }
}
```

📢 **섹션 요약 비유**: MongoDB 인덱스는 책의 목차다. "c고객_id + status"로 인덱스를 만들면, 특정 고객의 특정 상태 주문을 목차에서 바로 찾을 수 있다. 인덱스가 없으면 모든 주문을 하나씩 확인해야 한다(Full Collection Scan).

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **개발 속도** | 스키마리스로 스키마 변경 없이 새 필드 즉시 추가 |
| <strong>쿼리 단순화</strong> | JOIN 없는 단일 문서 조회로 애플리케이션 코드 단순화 |
| **검색 품질** | ES 형태소 분석·TF-IDF로 의미 기반 검색 |
| **수평 확장** | 샤딩으로 데이터 증가에 선형 대응 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **문서 크기 제한** | MongoDB 단일 문서 16MB 제한 |
| <strong>트랜잭션 성능</strong> | 다중 문서 ACID는 MongoDB 4.0+에서 가능하나 성능 저하 |
| <strong>ES 쓰기 지연</strong> | 역인덱스 구축으로 실시간 쓰기 후 검색 반영 1초 지연 |
| <strong>데이터 중복</strong> | 비정규화 문서 구조로 동일 데이터 중복 저장 가능 |

📢 **섹션 요약 비유**: 도큐먼트 저장소의 비정규화는 중복 복사를 감수하는 것이다. 각 주문 문서에 고객 이름을 복사해 넣으면(중복), 고객 이름 변경 시 모든 주문 문서를 업데이트해야 한다. 빠른 읽기를 위해 쓰기 복잡성을 감수하는 트레이드오프다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| NoSQL 4가지 유형 | 도큐먼트 저장소는 4가지 유형 중 가장 범용 |
| MongoDB Atlas | MongoDB의 완전 관리형 클라우드 서비스 |
| Elasticsearch (ELK) | 로그 분석·APM의 표준 스택 |
| 역인덱스 (Inverted Index) | ES 전문 검색의 핵심 자료구조 |
| 샤딩 | MongoDB/ES 수평 확장 메커니즘 |
| CDC / Debezium | MongoDB 변경 이벤트 -> Kafka 스트리밍 |
| 집계 파이프라인 | MongoDB OLAP 유사 집계 기능 |

### 👶 어린이를 위한 3줄 비유 설명
1. 도큐먼트 저장소는 스크랩북이다. 한 사람의 정보(사진, 연락처, 취미)를 하나의 스크랩 페이지에 다 붙여두면, 그 페이지만 펼쳐도 모든 정보가 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS: 정규화 -> JOIN 필요 (비용 ^)
    |
    v
Document DB: JSON/BSON 문서 단위 저장 (JOIN 불필요)
    +-► MongoDB: 범용 도큐먼트 DB
    +-► Elasticsearch: 전문 검색 + 분석
    |
    v
활용: CMS · 카탈로그 · 사용자 프로필 · 로그
```
2. MongoDB는 자유 노트 앱이다. 줄이 없는 노트처럼 각 메모(문서)가 원하는 형태로 저장되고, 메모마다 다른 내용을 적어도 된다.
3. Elasticsearch는 강력한 책 검색 시스템이다. "레시피 책"을 찾을 때 "레시피"나 "조리법"을 검색해도 찾아주고, 어떤 책이 더 관련 있는지 점수(TF-IDF)로 정렬해서 보여준다.
