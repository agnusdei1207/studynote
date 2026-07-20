---
title: "Nosql Database Types Overview"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 235
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL 데이터베이스는 "Not Only SQL"로, RDBMS의 강직한 스키마와 수직 확장 한계를 극복하기 위해 <strong>키-값·도큐먼트·와이드컬럼·그래프</strong> 4가지 데이터 모델로 특화된 분산 저장소다.
> 2. **가치**: 각 NoSQL 유형은 특정 액세스 패턴(밀리초 캐시·유연한 문서·시계열 쓰기·관계 탐색)에 <strong>10~100배 최적화</strong>되어 있으며, 수평 확장으로 빅데이터 규모를 처리한다.
> 3. **판단 포인트**: NoSQL은 RDBMS의 대체재가 아니라 <strong>"올바른 도구로 올바른 문제를 해결"</strong>하는 선택이므로, 액세스 패턴 분석이 DB 선택보다 선행되어야 한다.

---

## Ⅰ. 개요 및 필요성

RDBMS는 1970년대 이후 데이터 저장의 왕좌를 지켰다. 그러나 웹 2.0 시대가 열리면서 수억 명의 사용자, 수십억 건의 이벤트, 빠르게 변하는 스키마에 직면했다. RDBMS는 이 요구에 두 가지로 취약했다: <strong>수직 확장(장비 고비용) 한계</strong>와 <strong>엄격한 스키마로 인한 개발 민첩성 저하</strong>.

NoSQL은 이 문제를 해결하기 위해 <strong>CAP 정리에서 일관성을 일부 포기하고 가용성·파티션 허용성을 선택</strong>하거나, 특정 데이터 모델에 완전히 특화하는 전략을 채택했다.

```
[NoSQL 4가지 유형 분류]
+------------------------------------------------------------+
|              NoSQL 데이터베이스 분류                         |
|                                                            |
|  +--------------+    +--------------+                      |
|  | Key-Value    |    |  Document    |                      |
|  | Redis        |    |  MongoDB     |                      |
|  | DynamoDB     |    |  Elasticsearch|                     |
|  |             |    |              |                      |
|  | 밀리초 캐시  |    |  유연한 JSON  |                      |
|  | 세션 관리    |    |  스키마리스   |                      |
|  +--------------+    +--------------+                      |
|  +--------------+    +--------------+                      |
|  | Wide-Column  |    |    Graph     |                      |
|  | Cassandra    |    |  Neo4j       |                      |
|  | HBase        |    |  Amazon Neptune|                    |
|  |             |    |              |                      |
|  | 시계열 쓰기  |    | 관계 탐색    |                      |
|  | 페타바이트   |    | 추천 엔진    |                      |
|  +--------------+    +--------------+                      |
+------------------------------------------------------------+
```

📢 **섹션 요약 비유**: NoSQL 4가지 유형은 4가지 전문 음식점이다. 키-값(패스트푸드, 빠름), 도큐먼트(뷔페, 다양함), 와이드컬럼(대형 식당, 대용량), 그래프(코스요리, 관계 복잡도)다. 모든 음식을 파는 곳(RDBMS)보다 전문점이 특정 음식에선 훨씬 낫다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### NoSQL 4가지 유형 상세

#### 1. Key-Value Store
```
구조: {key: "user:1001", value: "{name:'김철수', age:28}"}

장점: O(1) 조회 속도, 단순 구조
단점: 범위 쿼리 어려움, 관계 없음
적합: 세션 저장, 캐시, 실시간 리더보드
대표: Redis (인메모리), DynamoDB (관리형)
```

#### 2. Document Store
```
구조: JSON/BSON 계층 문서
{
  "_id": "order_001",
  "customer": {"name": "김철수", "tier": "VIP"},
  "items": [
    {"product": "책", "qty": 2},
    {"product": "노트북", "qty": 1}
  ],
  "total": 1530000
}

장점: 유연한 스키마, 중첩 구조, 풍부한 쿼리
단점: JOIN 어려움, 대용량 쓰기 성능
적합: 콘텐츠 관리, 전자상거래, 검색
대표: MongoDB, Elasticsearch
```

#### 3. Wide-Column Store
```
구조: {행키: {열패밀리: {열: 값}}}
Row Key: "sensor:IoT-001:2024-01-15:00:00"
 +-- cf_data: {temp: 23.5, humidity: 60.2}
 +-- cf_meta: {firmware: "v2.1", location: "서울"}

장점: 시계열 대용량 쓰기, 열 동적 추가
단점: 설계 복잡, 집계 쿼리 어려움
적합: IoT 시계열, 이벤트 로그, 클릭스트림
대표: Cassandra (분산), HBase (Hadoop 기반)
```

#### 4. Graph Database
```
구조: 노드(Node) + 엣지(Edge) + 속성(Property)
노드: {id:1, label:"사람", name:"김철수"}
엣지: {from:1, to:2, type:"친구", since:2020}

장점: 관계 탐색 쿼리 탁월, 다중 홉 경로
단점: 대규모 수평 확장 어려움
적합: 추천 엔진, SNS 관계, FDS, 지식 그래프
대표: Neo4j, Amazon Neptune
```

📢 **섹션 요약 비유**: Wide-Column은 스프레드시트를 세로로 무한 확장한 것이다. 각 행(IoT 기기)의 열(측정값)이 기기마다 달라도 되고, 수십억 행도 여러 서버에 분산해 저장할 수 있다.

---

## Ⅲ. 비교 및 연결

### NoSQL 4가지 유형 종합 비교

| 비교 항목 | Key-Value | Document | Wide-Column | Graph |
|:---|:---:|:---:|:---:|:---:|
| **읽기 속도** | ★★★★★ | ★★★★ | ★★★ | ★★ |
| <strong>쓰기 처리량</strong> | ★★★★★ | ★★★ | ★★★★★ | ★★ |
| <strong>쿼리 유연성</strong> | ★ | ★★★★ | ★★ | ★★★★★ |
| **수평 확장** | ★★★★★ | ★★★★ | ★★★★★ | ★★ |
| <strong>ACID 트랜잭션</strong> | 제한 | 제한 | 제한 | 지원 |
| <strong>스키마 유연성</strong> | 높음 | 매우 높음 | 높음 | 높음 |

### RDBMS vs NoSQL 선택 기준

| 선택 요소 | RDBMS | NoSQL |
|:---|:---|:---|
| <strong>ACID 트랜잭션 필수</strong> | ✅ | 제한적 |
| <strong>복잡한 JOIN</strong> | ✅ | ❌ (데이터 모델로 회피) |
| <strong>스키마 유연성</strong> | ❌ | ✅ |
| **수평 확장 필요** | 제한 | ✅ |
| **단순 액세스 패턴** | 오버스펙 | ✅ (단순할수록 빠름) |
| <strong>대규모 쓰기</strong> | 느림 | ✅ |

📢 **섹션 요약 비유**: RDBMS vs NoSQL 선택은 만능 스위스아미 나이프 vs 전문 주방 칼의 차이다. 스위스아미 나이프(RDBMS)는 무엇이든 할 수 있지만, 요리사(고처리량 전문)는 전문 칼(NoSQL) 하나가 훨씬 효과적이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 액세스 패턴 기반 선택 가이드

```
[NoSQL 선택 결정 트리]
Q1: 밀리초 단위 조회 + 단순 key 기반 액세스?
  -> YES: Key-Value (Redis/DynamoDB)

Q2: 유연한 JSON 구조, 복잡한 문서 쿼리?
  -> YES: Document (MongoDB/Elasticsearch)

Q3: 초당 수십만 건 시계열 쓰기 + 행 키 기반?
  -> YES: Wide-Column (Cassandra/HBase)

Q4: 다중 홉 관계 탐색 (친구의 친구, 추천)?
  -> YES: Graph (Neo4j/Neptune)

Q5: 강력한 JOIN + ACID 필수?
  -> RDBMS (PostgreSQL/MySQL)
```

### 폴리글랏 퍼시스턴스(Polyglot Persistence)

```
[현대 전자상거래 플랫폼 예시]
사용자 세션·장바구니  --->  Redis (Key-Value, 밀리초 응답)
상품 카탈로그·리뷰    --->  MongoDB (Document, 유연한 구조)
주문·결제 내역        --->  PostgreSQL (RDBMS, ACID 필수)
검색 인덱스           --->  Elasticsearch (Document, 전문 검색)
추천 엔진            --->  Neo4j (Graph, 관계 탐색)
클릭스트림 로그       --->  Cassandra (Wide-Column, 대용량 쓰기)
```

**실무자 핵심 판단**: 단일 DB 만능주의를 탈피하고, "데이터의 액세스 패턴을 먼저 분석한 뒤, 각 패턴에 최적화된 DB를 선택"하는 폴리글랏 퍼시스턴스 전략을 제안한다.

📢 **섹션 요약 비유**: 폴리글랏 퍼시스턴스는 도구 상자에 다양한 공구를 갖추는 것이다. 나사엔 드라이버, 못엔 망치, 파이프엔 렌치를 쓰듯이, 각 데이터 요건에 맞는 DB를 선택하는 것이 최선이다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| <strong>성능 최적화</strong> | 액세스 패턴에 맞는 DB 선택으로 수십 배 성능 향상 |
| **비용 최적화** | 고비용 RDBMS 라이선스 대신 특화 오픈소스 활용 |
| **수평 확장** | 데이터 증가에 따른 서버 추가로 선형 확장 |
| **개발 민첩성** | 스키마리스로 빠른 프로토타이핑 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **ACID 약화** | 대부분의 NoSQL은 BASE(Basically Available, Soft state, Eventually consistent) |
| <strong>JOIN 미지원</strong> | 데이터 모델링 단계에서 관계를 사전 처리 필요 |
| **운영 복잡성** | 여러 DB 운영 시 관리 비용 증가 |
| **표준 SQL 없음** | DB마다 고유 쿼리 언어(Cypher, CQL 등) |

📢 **섹션 요약 비유**: NoSQL은 전문 레스토랑 체인과 같다. 각 레스토랑(DB)은 해당 음식(액세스 패턴)에서 최고지만, 여러 레스토랑을 동시에 운영하는 관리(폴리글랏 운영)는 복잡하다. 처음엔 RDBMS 하나로 시작하고, 병목 지점이 생기면 전문 NoSQL을 도입하는 단계적 전략이 현명하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| CAP 정리 | NoSQL이 RDBMS와 다른 일관성·가용성 트레이드오프 |
| Key-Value Store (Redis) | NoSQL 4가지 유형 중 가장 단순·고속 |
| Document Store (MongoDB) | 유연한 JSON 구조, 스키마리스 |
| Wide-Column (Cassandra) | 시계열·대용량 쓰기 특화 |
| Graph DB (Neo4j) | 관계 탐색 쿼리 특화 |
| 폴리글랏 퍼시스턴스 | 여러 DB를 목적에 맞게 혼용하는 아키텍처 전략 |
| ACID vs BASE | RDBMS와 NoSQL의 일관성 모델 차이 |

### 👶 어린이를 위한 3줄 비유 설명
1. NoSQL의 4가지 종류는 4가지 장난감 수납 방법이다. 키-값은 라벨 달린 상자(빠른 찾기), 도큐먼트는 파일 폴더(자세한 내용), 와이드컬럼은 대형 선반(엄청 많은 양), 그래프는 거미줄(연결 관계)이다.

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS: SQL · ACID · 정규화 (수직 확장 한계)
    |
    v
NoSQL: 수평 확장 · 유연한 스키마 · 최종 일관성
    +-► Key-Value: Redis · DynamoDB
    +-► Document: MongoDB · Elasticsearch
    +-► Wide-Column: Cassandra · HBase
    +-► Graph: Neo4j · Neptune
```
2. RDBMS가 만능 도구라면, NoSQL은 각자 한 가지를 잘하는 전문 도구다. 볼트를 조이는 데는 스패너(Key-Value)가, 나무를 자르는 데는 톱(Wide-Column)이 더 낫다.
3. 현대 앱들은 여러 종류의 NoSQL을 함께 쓴다. 로그인(Redis), 상품 정보(MongoDB), 친구 추천(Neo4j)처럼 각 기능에 맞는 DB를 고르는 것이 스마트한 방법이다.
