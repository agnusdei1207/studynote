---
title: "Cypher Query"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
- **본질**: Cypher는 그래프 패턴을 ASCII 아트처럼 시각적으로 표현하는 선언적 쿼리 언어로, `(노드)-[:관계]->(노드)` 문법이 관계를 직관적으로 기술하게 해준다.
- **가치**: SQL의 복잡한 다중 JOIN을 `(a)-[:KNOWS*1..3]->(b)` 단 한 줄의 가변 길이 패턴으로 표현할 수 있어, 관계 탐색 쿼리 개발 생산성이 극적으로 향상된다.
- **판단 포인트**: `MATCH`로 읽고 `MERGE`로 멱등 생성하며 `WITH`로 중간 결과를 파이프라이닝하는 세 가지 패턴이 Cypher 쿼리의 80%를 구성한다.

---

## Ⅰ. 개요 및 필요성

### 그래프 쿼리 언어의 필요성
SPARQL은 RDF 트리플스토어에 특화되었고, Gremlin은 명령형(절차적)이라 복잡한 탐색 로직을 기술하기 어렵다. Cypher는 2011년 Neo4j가 개발한 선언적 그래프 쿼리 언어로, SQL처럼 "무엇을 원하는가"를 기술하면 엔진이 최적 실행 계획을 수립한다. 2019년 ISO/GQL(Graph Query Language) 표준화 과정에서 Cypher가 핵심 영향을 미쳤다.

### Cypher 문법 기초

```text
+-------------------------------------------------------+
|              Cypher 핵심 문법 요소                      |
|                                                       |
|  (n)          <- 모든 노드                              |
|  (n:Person)   <- 라벨이 Person인 노드                   |
|  (n:Person {name:"홍길동"})  <- 속성 필터링             |
|                                                       |
|  -[:KNOWS]->  <- 방향 있는 관계                         |
|  -[:KNOWS]-   <- 방향 없는 관계                         |
|  -[r]->       <- 관계 변수 r로 참조                     |
|  -[:KNOWS*2..5]-> <- 2~5홉 가변 길이 탐색               |
|                                                       |
|  패턴 예시:                                            |
|  (alice:Person)-[:FOLLOWS]->(bob:Person)              |
|  (p)-[:BOUGHT]->(product:Product {category:"전자"})   |
+-------------------------------------------------------+
```

📢 **섹션 요약 비유**
> Cypher 문법은 지하철 노선도를 말로 표현하는 것과 같다. `(강남역)-[:2호선]->(역삼역)`이라고 쓰면 지도를 그리듯이 관계를 표현할 수 있다. SQL의 `JOIN users ON follows.following_id = users.id`보다 훨씬 직관적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Cypher 주요 절(Clause) 정리

```text
+----------------------------------------------------------+
|             Cypher 절(Clause) 역할 요약                    |
+--------------+-------------------------------------------+
|  MATCH       | 패턴과 일치하는 노드/관계 찾기 (SELECT)     |
|  OPTIONAL MATCH | LEFT JOIN 과 동일, 없으면 null          |
|  WHERE       | 필터 조건 (AND/OR/NOT/IN/STARTS WITH)     |
|  RETURN      | 결과 반환 (SELECT 절의 컬럼 선택)           |
|  CREATE      | 노드/관계 생성                             |
|  MERGE       | 없으면 CREATE, 있으면 MATCH (UPSERT)       |
|  SET         | 속성 추가/수정                             |
|  DELETE      | 노드/관계 삭제                             |
|  DETACH DELETE| 노드 + 연결 관계 모두 삭제                 |
|  WITH        | 파이프라인: 중간 결과를 다음 절에 전달       |
|  UNWIND      | 리스트를 행으로 분해 (explode)              |
|  ORDER BY    | 정렬                                      |
|  SKIP/LIMIT  | 페이지네이션                               |
|  CALL        | 프로시저/함수 호출 (GDS 알고리즘 등)        |
+--------------+-------------------------------------------+
```

### 핵심 쿼리 예시 모음

```cypher
-- ① 기본 패턴 매칭: 홍길동이 팔로우하는 사람들
MATCH (p:Person {name:"홍길동"})-[:FOLLOWS]->(following:Person)
RETURN following.name, following.city
ORDER BY following.name;

-- ② 가변 길이 탐색: 홍길동과 3단계 이내 연결된 모든 사람
MATCH (p:Person {name:"홍길동"})-[:KNOWS*1..3]-(connected:Person)
WHERE p <> connected
RETURN DISTINCT connected.name, length(shortestPath(
       (p)-[:KNOWS*]-(connected))) AS distance
ORDER BY distance;

-- ③ WITH 파이프라이닝: 팔로워 10명 이상인 인플루언서
MATCH (influencer:Person)<-[:FOLLOWS]-(follower:Person)
WITH influencer, count(follower) AS followerCount
WHERE followerCount >= 10
RETURN influencer.name, followerCount
ORDER BY followerCount DESC LIMIT 20;

-- ④ MERGE (Upsert): 없으면 생성, 있으면 속성만 갱신
MERGE (p:Person {email:"hong@example.com"})
ON CREATE SET p.name = "홍길동", p.created = timestamp()
ON MATCH  SET p.lastLogin = timestamp()
RETURN p;

-- ⑤ 관계 생성: 구매 관계 추가
MATCH (buyer:Person {id: $userId}),
      (product:Product {sku: $sku})
MERGE (buyer)-[r:BOUGHT]->(product)
ON CREATE SET r.boughtAt = timestamp(), r.price = $price
RETURN r;
```

### Cypher vs SQL 표현 비교

| 목적 | SQL | Cypher |
|:---:|:---|:---|
| 전체 조회 | `SELECT * FROM users` | `MATCH (u:User) RETURN u` |
| 필터 | `WHERE name='홍'` | `WHERE u.name STARTS WITH '홍'` |
| 관계 탐색 | `JOIN follows ON...` | `-[:FOLLOWS]->` |
| 3홉 탐색 | 3중 Self-JOIN | `-[:FOLLOWS*3]->` |
| 집계 | `COUNT(*), GROUP BY` | `count(), WITH` |
| 최단 경로 | 복잡한 재귀 CTE | `shortestPath(...)` |

📢 **섹션 요약 비유**
> Cypher의 `WITH`는 공장 컨베이어 벨트의 중간 검사대와 같다. 1단계에서 만들어진 중간 제품을 검사하고 가공한 뒤 2단계로 넘긴다. SQL의 서브쿼리처럼 괄호 속에 숨기지 않고, 파이프라인처럼 명시적으로 흘러가는 것이 Cypher의 강점이다.

---

## Ⅲ. 비교 및 연결

### Cypher vs SPARQL vs Gremlin

| 항목 | Cypher | SPARQL | Gremlin |
|:---:|:---:|:---:|:---:|
| 패러다임 | 선언형 | 선언형 | 명령형(절차) |
| 대상 모델 | Property Graph | RDF 트리플 | Property Graph |
| 문법 직관성 | 높음 (ASCII 아트) | 중간 | 낮음 (체이닝) |
| 표준 여부 | openCypher / ISO GQL | W3C 표준 | Apache TinkerPop |
| 주요 DB | Neo4j, Memgraph | Amazon Neptune, GraphDB | JanusGraph, CosmosDB |

### GDS (Graph Data Science) 라이브러리 연계

```cypher
-- Neo4j GDS: PageRank 알고리즘 실행
CALL gds.pageRank.stream('myGraph', {
  maxIterations: 20,
  dampingFactor: 0.85
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC LIMIT 10;

-- 커뮤니티 탐지 (Louvain 알고리즘)
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN communityId, collect(gds.util.asNode(nodeId).name) AS members
ORDER BY size(members) DESC;
```

📢 **섹션 요약 비유**
> Cypher와 Gremlin의 차이는 목적지 안내의 차이다. Cypher는 "강남에서 홍대까지 가는 경로를 보여줘"(선언형)이고, Gremlin은 "이 버스 타고, 지하철 2호선으로 갈아타고, 몇 정거장 가서 내려"(명령형)이다. 목적지가 같아도 사람이 직접 지시하는 방식이 훨씬 복잡하다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 추천 엔진 구현 패턴

```cypher
-- "이 상품을 산 사람들이 함께 산 상품" 추천
MATCH (target:Product {sku: $targetSku})<-[:BOUGHT]-(buyer:Person)
      -[:BOUGHT]->(recommended:Product)
WHERE recommended <> target
  AND NOT (buyer)-[:BOUGHT]->(recommended)  -- 이미 산 것 제외
WITH recommended, count(DISTINCT buyer) AS cobuyers
ORDER BY cobuyers DESC
LIMIT 10
RETURN recommended.name, cobuyers;
```

### 성능 최적화 포인트

```text
Cypher 성능 최적화 지침:

1. 시작점을 가장 선택적인 노드로 지정
   MATCH (:Person {name:"홍길동"})  <- 인덱스 활용
   NOT: MATCH (p:Person) WHERE p.name = "홍길동"

2. 인덱스 생성
   CREATE INDEX person_name FOR (p:Person) ON (p.name);

3. PROFILE로 실행 계획 분석
   PROFILE MATCH (p:Person)-[:KNOWS*1..3]->(target)
   WHERE p.name = "홍길동" RETURN target

4. 가변 길이 탐색 상한 제한
   [:KNOWS*..5]  <- 상한 없으면 전체 그래프 탐색 위험
```

📢 **섹션 요약 비유**
> 추천 쿼리는 "같은 식당을 자주 찾는 단골들이 다른 어떤 식당을 좋아하는가"를 묻는 것과 같다. 그래프 DB는 이 관계망을 이미 그려두었기 때문에, 단골 목록을 하나하나 비교하지 않고 관계 선을 따라가기만 하면 된다.

---

## Ⅴ. 기대효과 및 결론

### 실무자 필수 Cypher 패턴 요약

| 패턴 | 문법 | 용도 |
|:---:|:---:|:---:|
| 단순 탐색 | `MATCH (a)-[:R]->(b)` | 직접 연결 조회 |
| 가변 탐색 | `MATCH (a)-[:R*1..5]->(b)` | N홉 관계 탐색 |
| 최단 경로 | `shortestPath((a)-[*]-(b))` | 최단 연결 경로 |
| 모든 경로 | `allShortestPaths(...)` | 동일 거리 모든 경로 |
| 멱등 생성 | `MERGE (n {id:$id})` | Upsert 패턴 |
| 파이프라이닝 | `WITH var, count(*) AS cnt` | 다단계 집계 |

### 결론
Cypher는 그래프 패턴 매칭에 특화된 선언적 쿼리 언어로, 복잡한 관계 탐색을 직관적이고 간결하게 표현한다. 심화 학습에서는 **패턴 매칭 문법 구조**, **MATCH/MERGE/WITH 절의 역할**, **가변 길이 탐색 문법**, <strong>추천·사기탐지 적용 쿼리 예시</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> Cypher를 익히는 것은 악보 읽기를 배우는 것과 같다. 처음엔 기호가 낯설지만, 패턴이 보이기 시작하면 복잡한 관계 쿼리도 악보 한 장처럼 한눈에 읽힌다. SQL 경험자라면 `MATCH` = `SELECT`, `WHERE` = `WHERE`, `WITH` = 서브쿼리로 대응시키면 금방 익숙해진다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---:|:---:|:---|
| openCypher | 표준화 | Neo4j Cypher의 오픈소스 명세 |
| ISO GQL | 국제 표준 | 2024 그래프 쿼리 언어 표준 |
| Gremlin | 대안 언어 | Apache TinkerPop 명령형 언어 |
| SPARQL | 대안 언어 | W3C RDF 표준 쿼리 언어 |
| GDS Library | 확장 기능 | 그래프 알고리즘(PageRank, 커뮤니티 탐지) |

### 📈 관련 키워드 및 발전 흐름도

```text
[그래프 데이터베이스 (Graph Database) — 노드/관계 모델]
    |
    v
[Cypher 쿼리 언어 (Cypher Query Language) — 패턴 매칭]
    |
    v
[기본 구문 (MATCH/WHERE/RETURN) — 쿼리 핵심 키워드]
    |
    v
[경로 탐색 (Path Traversal) — 최단 경로]
    |
    v
[그래프 쿼리 언어 GQL (Graph Query Language) — ISO 표준화]
```

이 흐름은 그래프 데이터베이스의 관계 모델을 Cypher로 표현하고, 기본 구문과 경로 탐색을 거쳐 GQL 표준으로 수렴하는 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Cypher는 관계를 화살표로 그림처럼 표현하는 언어 — `(홍길동)-[알아요]->(이몽룡)`처럼 쓰면 두 사람의 관계를 딱 표현할 수 있어요.
2. `*1..3`은 "최대 3번 연결된 친구까지 찾아줘"라는 뜻 — 친구, 친구의 친구, 친구의 친구의 친구를 한 번에 검색해요.
3. `MERGE`는 "있으면 그걸 써, 없으면 만들어줘"라는 스마트한 명령 — 중복 없이 안전하게 데이터를 넣을 수 있어요.
