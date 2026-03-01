+++
title = "NoSQL 데이터베이스 (NoSQL Database)"
date = 2025-03-01

[extra]
categories = "database-nosql"
+++

# NoSQL 데이터베이스 (NoSQL Database)

## 핵심 인사이트 (3줄 요약)
> **비관계형 데이터베이스로 유연한 스키마와 수평 확장성** 제공. 문서형, 키-값, 컬럼형, 그래프형으로 분류. 빅데이터, 실시간 웹 애플리케이션에 적합.

## 1. 개념
NoSQL(Not Only SQL)은 **관계형 데이터베이스의 제약에서 벗어난 비관계형 데이터베이스**로, 유연한 스키마와 수평적 확장성을 제공한다.

> 비유: "자유로운 서랍장" - 정해진 칸 없이 자유롭게 물건을 넣을 수 있음

## 2. 등장 배경

```
관계형 DB의 한계:
1. 수직 확장만 가능 (비용 ↑)
2. 고정된 스키마 (변경 어려움)
3. 대용량 데이터 처리 한계
4. 비정형 데이터 처리 어려움
5. 분산 환경에서의 복잡성

NoSQL의 등장:
- 웹 2.0, 소셜 미디어
- 빅데이터 시대
- 실시간 처리 요구
- 클라우드 환경
```

## 3. NoSQL 유형

### 3.1 키-값 (Key-Value) 저장소
```
구조: Key → Value (단순)

┌─────────────────────────────────┐
│            Redis 예시            │
├─────────┬───────────────────────┤
│   Key   │        Value          │
├─────────┼───────────────────────┤
│user:1   │"{name:'홍길동',age:25}"│
│user:2   │"{name:'김철수',age:30}"│
│session:1│"abc123xyz"            │
└─────────┴───────────────────────┘

특징:
- 가장 단순
- O(1) 조회
- 캐시에 최적
- 예: Redis, Memcached

용도:
- 세션 저장소
- 캐시
- 실시간 데이터
```

### 3.2 문서형 (Document) 저장소
```
구조: Key → Document (JSON/BSON)

┌───────────────────────────────────────┐
│            MongoDB 예시                │
├─────────┬─────────────────────────────┤
│  _id    │         Document             │
├─────────┼─────────────────────────────┤
│"user:1" │ {                            │
│         │   "name": "홍길동",          │
│         │   "age": 25,                 │
│         │   "hobbies": ["독서","영화"] │
│         │ }                            │
├─────────┼─────────────────────────────┤
│"user:2" │ {                            │
│         │   "name": "김철수",          │
│         │   "email": "kim@test.com"    │
│         │   // age 없어도 됨!          │
│         │ }                            │
└─────────┴─────────────────────────────┘

특징:
- 유연한 스키마
- 중첩 구조 가능
- 쿼리 언어 지원
- 예: MongoDB, CouchDB

용도:
- 콘텐츠 관리
- 사용자 프로필
- 로그 분석
```

### 3.3 컬럼형 (Column-Family) 저장소
```
구조: Row Key → Column Family → Column

┌──────────────────────────────────────────────┐
│            Cassandra 예시                     │
├──────────┬───────────────────────────────────┤
│ Row Key  │           Column Families          │
├──────────┼───────────────────────────────────┤
│  "user1" │ info: {name:"홍길동", age:25}     │
│          │ activity: {login:100, post:50}    │
├──────────┼───────────────────────────────────┤
│  "user2" │ info: {name:"김철수"}             │
│          │ activity: {login:200}             │
└──────────┴───────────────────────────────────┘

특징:
- 대용량 분산 처리
- 높은 쓰기 성능
- 컬럼 동적 추가
- 예: Cassandra, HBase

용도:
- 시계열 데이터
- IoT 데이터
- 로그 수집
```

### 3.4 그래프형 (Graph) 저장소
```
구조: 노드(Node) + 엣지(Edge) + 속성(Property)

         ┌───────┐
         │ 철수  │
         │(사용자)│
         └───┬───┘
             │ 친구
         ┌───┴───┐
         │ 영희  │
         │(사용자)│
         └───┬───┘
             │ 구매
         ┌───┴───┐
         │ 노트북 │
         │(상품)  │
         └───────┘

특징:
- 관계 중심
- 복잡한 연결 표현
- 순회 쿼리 최적화
- 예: Neo4j, Amazon Neptune

용도:
- 소셜 네트워크
- 추천 시스템
- 사기 탐지
- 지식 그래프
```

## 4. NoSQL 유형 비교

| 유형 | 데이터 모델 | 성능 | 확장성 | 쿼리 | 대표 제품 |
|------|------------|------|--------|------|----------|
| 키-값 | Key-Value | 최고 | 수평 | 단순 | Redis |
| 문서형 | JSON/BSON | 높음 | 수평 | 풍부 | MongoDB |
| 컬럼형 | Column Family | 높음 | 수평 | 중간 | Cassandra |
| 그래프 | Graph | 중간 | 수직 | 복잡 | Neo4j |

## 5. RDBMS vs NoSQL

```
┌────────────────┬─────────────────┬─────────────────┐
│      항목       │      RDBMS      │      NoSQL      │
├────────────────┼─────────────────┼─────────────────┤
│ 스키마         │ 고정 (사전 정의) │ 유연 (동적)     │
│ 확장성         │ 수직 (Scale-up) │ 수평 (Scale-out)│
│ 일관성         │ 강한 일관성     │ 결과적 일관성   │
│ 트랜잭션       │ ACID            │ BASE            │
│ 조인           │ 지원            │ 제한적          │
│ 쿼리           │ SQL             │ 제품별 다름     │
│ 정규화         │ 필수            │ 선택적          │
│ 적합한 데이터  │ 정형            │ 비정형          │
│ 적합한 용도    │ OLTP            │ 빅데이터, 실시간│
└────────────────┴─────────────────┴─────────────────┘
```

## 6. CAP 이론과 NoSQL

```
CAP Theorem:

      Consistency
          ▲
         /│\
        / │ \
       /  │  \
      /   │   \
     /    │    \
    ●─────┼─────●
Availability  Partition
             Tolerance

CP 시스템 (일관성 우선):
- MongoDB, HBase, Redis
- 분할 시 일부 사용 불가

AP 시스템 (가용성 우선):
- Cassandra, CouchDB, DynamoDB
- 분할 시에도 서비스, 일관성은 나중에

CA 시스템:
- 전통적 RDBMS
- 네트워크 분할 없는 환경만
```

## 7. BASE 속성

```
BASE (ACID의 대안):

B - Basically Available
    기본적 가용성
    → 항상 응답은 함

S - Soft State
    소프트 상태
    → 상태가 시간에 따라 변할 수 있음

E - Eventually Consistent
    결과적 일관성
    → 시간이 지나면 일관성 달성

vs ACID:
┌─────────┬─────────────┬─────────────┐
│         │    ACID     │    BASE     │
├─────────┼─────────────┼─────────────┤
│ 일관성  │ 강한 일관성 │ 결과적 일관성│
│ 트랜잭션│ 엄격함      │ 유연함      │
│ 복잡성  │ 높음        │ 낮음        │
│ 성능    │ 제한적      │ 높음        │
└─────────┴─────────────┴─────────────┘
```

## 8. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import json
import time

# ===== 키-값 저장소 =====
class KeyValueStore:
    """간단한 키-값 저장소"""

    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> bool:
        """값 저장"""
        self.data[key] = value
        return True

    def get(self, key: str) -> Optional[Any]:
        """값 조회"""
        return self.data.get(key)

    def delete(self, key: str) -> bool:
        """값 삭제"""
        if key in self.data:
            del self.data[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        """키 존재 확인"""
        return key in self.data

    def expire(self, key: str, seconds: int):
        """만료 시간 설정 (간소화)"""
        time.sleep(seconds)
        self.delete(key)


# ===== 문서형 저장소 =====
@dataclass
class Document:
    """문서 구조"""
    _id: str
    data: Dict[str, Any]
    version: int = 1

class DocumentStore:
    """간단한 문서형 저장소"""

    def __init__(self):
        self.collections: Dict[str, Dict[str, Document]] = {}

    def insert(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Document:
        """문서 삽입"""
        if collection not in self.collections:
            self.collections[collection] = {}

        doc = Document(_id=doc_id, data=data)
        self.collections[collection][doc_id] = doc
        return doc

    def find(self, collection: str, query: Dict[str, Any] = None) -> List[Document]:
        """문서 검색"""
        if collection not in self.collections:
            return []

        if query is None:
            return list(self.collections[collection].values())

        results = []
        for doc in self.collections[collection].values():
            match = True
            for key, value in query.items():
                if key not in doc.data or doc.data[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)

        return results

    def find_one(self, collection: str, doc_id: str) -> Optional[Document]:
        """단일 문서 조회"""
        if collection not in self.collections:
            return None
        return self.collections[collection].get(doc_id)

    def update(self, collection: str, doc_id: str, updates: Dict[str, Any]) -> bool:
        """문서 수정"""
        doc = self.find_one(collection, doc_id)
        if doc:
            doc.data.update(updates)
            doc.version += 1
            return True
        return False

    def delete(self, collection: str, doc_id: str) -> bool:
        """문서 삭제"""
        if collection in self.collections and doc_id in self.collections[collection]:
            del self.collections[collection][doc_id]
            return True
        return False


# ===== 컬럼형 저장소 =====
class ColumnFamilyStore:
    """간단한 컬럼 패밀리 저장소"""

    def __init__(self):
        self.data: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def put(self, row_key: str, column_family: str, column: str, value: Any):
        """데이터 저장"""
        if row_key not in self.data:
            self.data[row_key] = {}
        if column_family not in self.data[row_key]:
            self.data[row_key][column_family] = {}

        self.data[row_key][column_family][column] = value

    def get(self, row_key: str, column_family: str = None, column: str = None) -> Any:
        """데이터 조회"""
        if row_key not in self.data:
            return None

        if column_family is None:
            return self.data[row_key]

        if column_family not in self.data[row_key]:
            return None

        if column is None:
            return self.data[row_key][column_family]

        return self.data[row_key][column_family].get(column)

    def scan(self, start_key: str = None, limit: int = 100) -> List[tuple]:
        """범위 스캔"""
        results = []
        for key in sorted(self.data.keys()):
            if start_key and key < start_key:
                continue
            results.append((key, self.data[key]))
            if len(results) >= limit:
                break
        return results


# ===== 그래프 저장소 =====
@dataclass
class Node:
    """그래프 노드"""
    id: str
    labels: List[str]
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Edge:
    """그래프 엣지"""
    id: str
    from_node: str
    to_node: str
    relationship: str
    properties: Dict[str, Any] = field(default_factory=dict)

class GraphStore:
    """간단한 그래프 저장소"""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self.adjacency: Dict[str, List[str]] = {}  # node_id -> edge_ids

    def create_node(self, node_id: str, labels: List[str], properties: Dict = None) -> Node:
        """노드 생성"""
        node = Node(node_id, labels, properties or {})
        self.nodes[node_id] = node
        self.adjacency[node_id] = []
        return node

    def create_edge(self, edge_id: str, from_id: str, to_id: str,
                    relationship: str, properties: Dict = None) -> Optional[Edge]:
        """엣지 생성"""
        if from_id not in self.nodes or to_id not in self.nodes:
            return None

        edge = Edge(edge_id, from_id, to_id, relationship, properties or {})
        self.edges[edge_id] = edge
        self.adjacency[from_id].append(edge_id)
        return edge

    def find_neighbors(self, node_id: str, relationship: str = None) -> List[Node]:
        """이웃 노드 찾기"""
        if node_id not in self.adjacency:
            return []

        neighbors = []
        for edge_id in self.adjacency[node_id]:
            edge = self.edges[edge_id]
            if relationship is None or edge.relationship == relationship:
                neighbors.append(self.nodes[edge.to_node])

        return neighbors

    def shortest_path(self, start_id: str, end_id: str) -> List[str]:
        """최단 경로 (BFS)"""
        if start_id not in self.nodes or end_id not in self.nodes:
            return []

        from collections import deque

        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current, path = queue.popleft()

            if current == end_id:
                return path

            for neighbor in self.find_neighbors(current):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append((neighbor.id, path + [neighbor.id]))

        return []


# ===== 사용 예시 =====
print("=== 키-값 저장소 테스트 ===")
kv = KeyValueStore()
kv.set("user:1", {"name": "홍길동", "age": 25})
kv.set("session:abc", "token123")
print(f"user:1 조회: {kv.get('user:1')}")
print(f"session:abc 조회: {kv.get('session:abc')}")

print("\n=== 문서형 저장소 테스트 ===")
doc_store = DocumentStore()
doc_store.insert("users", "user1", {"name": "홍길동", "age": 25, "hobbies": ["독서", "영화"]})
doc_store.insert("users", "user2", {"name": "김철수", "age": 30})
doc_store.insert("users", "user3", {"name": "이영희", "age": 25})

print(f"전체 사용자: {len(doc_store.find('users'))}명")
print(f"25세 사용자: {[d.data['name'] for d in doc_store.find('users', {'age': 25})]}")

print("\n=== 컬럼형 저장소 테스트 ===")
cf = ColumnFamilyStore()
cf.put("user1", "info", "name", "홍길동")
cf.put("user1", "info", "age", 25)
cf.put("user1", "activity", "login_count", 100)
cf.put("user2", "info", "name", "김철수")

print(f"user1 info: {cf.get('user1', 'info')}")
print(f"user1 name: {cf.get('user1', 'info', 'name')}")

print("\n=== 그래프 저장소 테스트 ===")
graph = GraphStore()

# 노드 생성
graph.create_node("user1", ["User"], {"name": "홍길동"})
graph.create_node("user2", ["User"], {"name": "김철수"})
graph.create_node("user3", ["User"], {"name": "이영희"})
graph.create_node("product1", ["Product"], {"name": "노트북"})

# 엣지 생성
graph.create_edge("e1", "user1", "user2", "FRIEND")
graph.create_edge("e2", "user2", "user3", "FRIEND")
graph.create_edge("e3", "user1", "product1", "PURCHASED")

print(f"홍길동의 친구: {[n.properties['name'] for n in graph.find_neighbors('user1', 'FRIEND')]}")
print(f"user1 → user3 최단 경로: {graph.shortest_path('user1', 'user3')}")
```

## 9. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 확장성 | 수평 확장 용이 |
| 유연성 | 스키마 변경 자유 |
| 성능 | 대용량 처리 |
| 비용 | 오픈소스, 일반 하드웨어 |

### 단점
| 단점 | 설명 |
|-----|------|
| 일관성 | 결과적 일관성만 보장 |
| 트랜잭션 | 제한적 |
| 쿼리 | SQL보다 제한적 |
| 표준화 | 제품별 상이 |

## 10. 실무에선? (기술사적 판단)
- **캐싱**: Redis (세션, 캐시)
- **콘텐츠**: MongoDB (블로그, CMS)
- **시계열**: Cassandra (IoT, 로그)
- **관계 분석**: Neo4j (추천, 소셜)
- **하이브리드**: RDBMS + NoSQL 조합
- **클라우드**: DynamoDB, Cosmos DB, Firestore

## 11. 관련 개념
- CAP 이론
- BASE
- 샤딩
- 복제
- 결과적 일관성

---

## 어린이를 위한 종합 설명

**NoSQL은 "자유로운 정리함"이에요!**

### RDBMS vs NoSQL 📦
```
RDBMS (엄격한 서랍장):
- 정해진 칸에 맞는 것만 넣어요
- "이 칸은 사과만!"

NoSQL (자유로운 서랍장):
- 아무거나 넣을 수 있어요
- "사과도, 배도, 포도도!"
```

### 4가지 종류 🗂️
```
1. 키-값 (Redis):
   "이름표만 붙이면 끝!"
   사과 → "맛있는 사과"

2. 문서형 (MongoDB):
   "문서로 저장해요"
   {이름: 철수, 나이: 10, 취미: 축구}

3. 컬럼형 (Cassandra):
   "엑셀처럼 세로로"
   | 이름 | 나이 | 취미 |
   | 철수 |  10  | 축구 |

4. 그래프형 (Neo4j):
   "관계를 그래프로"
   철수 ─친구─ 영희 ─구매─ 노트북
```

### CAP 트레이드오프 ⚖️
```
세 가지를 다 가질 순 없어요:

C: 모두가 같은 데이터
A: 항상 응답해요
P: 통신이 끊겨도 작동

→ 두 가지만 선택!
```

**비밀**: 페이스북, 구글도 NoSQL을 써요! 🌍✨
