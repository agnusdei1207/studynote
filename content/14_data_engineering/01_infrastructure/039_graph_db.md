---
title: "Graph Database"
date: "2026-03-04"
tags:
  - "studynote-data-engineering"
weight: 39
---
> **핵심 인사이트**
> 1. 그래프 DB는 데이터를 노드(Node)·엣지(Edge)·속성(Property)으로 표현하여 관계(Relationship)가 일급 시민(First-Class Citizen)인 데이터 모델로, SNS·추천 시스템·사기 탐지처럼 연결성이 핵심인 문제에서 관계형 DB의 다단계 JOIN을 그래프 탐색으로 대체하여 수십~수백 배 빠른 성능을 제공한다.
> 2. 프로퍼티 그래프(Property Graph, Neo4j)와 RDF 그래프(Triple Store, Ontology) 두 가지 모델이 주류 — 프로퍼티 그래프는 애플리케이션 개발에, RDF/SPARQL은 시맨틱 웹과 지식 그래프에 적합하다.
> 3. Cypher 쿼리 언어의 핵심 패턴: `(a)-[r]->(b)` — 노드와 관계를 ASCII 아트처럼 직관적으로 표현하여 "6단계 친분 찾기" 같은 복잡한 그래프 탐색을 간단한 쿼리로 작성할 수 있다.

---

## I. 그래프 모델 기본

```
프로퍼티 그래프 (Property Graph):

노드 (Node / Vertex):
  엔티티 표현
  라벨: (Person), (Movie), (Product)
  속성: {name: "Alice", age: 30}

엣지 (Edge / Relationship):
  관계 표현 (방향 있음)
  유형: -[:KNOWS]->  -[:BOUGHT]->
  속성: {since: "2020", weight: 0.8}

예시:
  (Alice:Person {age:30})
    -[:KNOWS {since:2020}]->
  (Bob:Person {age:25})
    -[:WORKS_AT]->
  (Acme:Company {employees:500})

관계형 DB 비교:
  관계형: 친구의 친구의 친구 = 3번 JOIN
  그래프: MATCH (a)-[:KNOWS*3]->(c) RETURN c

  JOIN 깊이 ^ -> 관계형 성능 급감
  그래프 탐색 -> 깊이에 관계없이 일정
```

> 📢 **섹션 요약 비유**: 관계형 DB는 여러 층 계단 오르기(JOIN), 그래프 DB는 줄 따라가기(엣지 탐색) — 관계가 많을수록 줄 따라가기가 훨씬 빠름.

---

## II. Cypher 쿼리 언어

```
Cypher (Neo4j):
  그래프 패턴을 ASCII 아트로 표현

기본 문법:
  (노드) -[관계]-> (노드)

MATCH: 패턴 검색
  MATCH (p:Person {name: "Alice"})
        -[:KNOWS]->
        (friend:Person)
  RETURN friend.name

친구의 친구 찾기:
  MATCH (alice {name:"Alice"})
        -[:KNOWS*2]->(fof)
  WHERE NOT (alice)-[:KNOWS]->(fof)
  RETURN fof.name

최단 경로:
  MATCH path = shortestPath(
    (alice:Person {name:"Alice"})
    -[:KNOWS*]->
    (bob:Person {name:"Bob"})
  )
  RETURN length(path)

Page Rank:
  CALL algo.pageRank('Person', 'KNOWS')
  YIELD nodeId, score
  RETURN algo.getNodeById(nodeId).name, score
  ORDER BY score DESC LIMIT 10
```

> 📢 **섹션 요약 비유**: Cypher는 그래프를 그림처럼 쓰는 쿼리 언어 — `(나)-[친구]->(친구)` 이렇게 쓰면 "내 친구의 친구를 찾아라"는 뜻.

---

## III. 그래프 DB 유스케이스

```
1. SNS 소셜 그래프:
   (User)-[:FOLLOWS]->(User)
   팔로워 추천, 영향력 분석
   예: Twitter 팔로우 그래프

2. 추천 시스템:
   (User)-[:BOUGHT]->(Product)
   (User)-[:LIKES]->(Product)
   협업 필터링 -> "당신과 비슷한 사람이 산 것"

3. 사기 탐지 (Fraud Detection):
   (Account)-[:TRANSFER_TO]->(Account)
   공통 기기/주소/패턴으로 사기 링 탐지
   링크 분석(Link Analysis): 공통 연결 노드 발견

4. 지식 그래프 (Knowledge Graph):
   Google 지식 패널, Wikidata
   (Entity)-[:IS_A]->(Category)

5. IT 인프라 의존성:
   (Service)-[:DEPENDS_ON]->(Database)
   장애 전파 경로 분석
   "어떤 서비스가 영향받는가?"
```

> 📢 **섹션 요약 비유**: 사기 탐지에서 "동일 기기를 쓰는 계좌들" 연결 — 그래프가 이상한 연결 패턴을 시각적으로 드러냄.

---

## IV. 관계형 DB vs 그래프 DB

```
관계형 DB 한계 (연결 데이터):

친구의 친구의 친구 조회 (6 degrees):
  관계형 SQL (6단계 JOIN):
    SELECT u6.name FROM users u1
    JOIN friends f1 ON u1.id = f1.user_id
    JOIN users u2 ON f1.friend_id = u2.id
    ... (6번 반복)

  1억 사용자 기준: ~분 소요

그래프 Cypher (6단계):
  MATCH (p:Person {name:"Alice"})
        -[:KNOWS*1..6]->(target)
  RETURN target.name

  같은 데이터: ~밀리초
  이유: "인덱스 없는 인접성 (Index-Free Adjacency)"
       각 노드가 자신의 이웃 직접 참조

언제 관계형을 쓸 것인가:
  - 집계(SUM, GROUP BY) 중심 분석
  - 관계가 단순 (1~2단계 JOIN)
  - ACID 트랜잭션 필수
  - 팀의 SQL 역량 높음
```

> 📢 **섹션 요약 비유**: 전화번호부(관계형)는 이름으로 번호 찾기엔 완벽, 연락망 탐색(그래프)에는 연결고리 따라가기가 훨씬 빠름.

---

## V. 실무 시나리오 — 사기 탐지 시스템

```
금융 사기 탐지:

데이터 모델:
  (Account)-[:TRANSFER {amount,time}]->(Account)
  (Account)-[:USES]->(Device)
  (Account)-[:LIVES_AT]->(Address)

사기 링 탐지 쿼리:
  // 동일 기기를 공유하는 계좌 클러스터
  MATCH (a1:Account)-[:USES]->(d:Device)
        <-[:USES]-(a2:Account)
  WHERE a1 <> a2
  WITH d, collect(a1) + collect(a2) AS accounts
  WHERE size(accounts) > 3
  RETURN d.deviceId, accounts

의심 패턴:
  기기 1개를 10개 계좌가 공유
  -> 10개 계좌가 서로 소액 이체 반복
  -> 자금 세탁 링(Money Laundering Ring) 의심

결과:
  관계형 DB: 이 패턴 찾는 쿼리 = 5분 이상
  Neo4j: 동일 데이터 = 200ms

실시간 처리:
  거래 발생 시 즉시 그래프 분석
  의심 패턴 발견 시 거래 보류
```

> 📢 **섹션 요약 비유**: 사기범들은 연결망으로 감추지만, 그래프 DB는 그 연결망 전체를 한 번에 보는 눈 — "공통 기기" 하나가 10개 계좌를 연결하는 패턴 즉시 발견.

---

## 📌 관련 개념 맵

```
그래프 데이터베이스
+-- 모델
|   +-- 프로퍼티 그래프 (Neo4j)
|   +-- RDF 트리플 스토어 (지식 그래프)
+-- 쿼리 언어
|   +-- Cypher (Neo4j)
|   +-- SPARQL (RDF)
|   +-- Gremlin (범용)
+-- 강점
|   +-- 다단계 관계 탐색 (인덱스 없는 인접성)
+-- 유스케이스
    +-- 소셜 그래프, 추천 시스템
    +-- 사기 탐지, 지식 그래프
    +-- IT 인프라 의존성
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[그래프 이론 (Euler, 1736)]
쾨니히스베르크 다리 문제
      |
      v
[초기 그래프 DB (AllegroGraph, 2004)]
      |
      v
[Neo4j (2007)]
프로퍼티 그래프 표준화
Cypher 쿼리 언어
      |
      v
[Google 지식 그래프 (2012)]
RDF 기반 대규모 지식 그래프
      |
      v
[현재: GNN + 지식 그래프]
그래프 신경망 (GNN)
AI + 지식 그래프 통합 (LLM + KG)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 그래프 DB는 사람들의 관계를 점(사람)과 선(관계)으로 저장하는 데이터베이스로, SNS에서 "친구의 친구의 친구" 찾기에 완벽해요.
2. 관계형 DB로 여러 단계 연결을 찾으려면 여러 번 테이블을 합쳐야 해서 느리지만, 그래프 DB는 선을 따라가면 되니까 훨씬 빠르고 간단해요.
3. 사기꾼들이 여러 계좌를 하나의 기기로 나누어 쓰는 패턴을 그래프 DB가 즉시 발견해서 금융 사기 탐지에 핵심적으로 쓰여요!
