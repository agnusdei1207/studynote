+++
title = "275. NoSQL의 4대 데이터 모델 - 목적에 따른 저장의 기술"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 275
+++

# 275. NoSQL의 4대 데이터 모델 - 목적에 따른 저장의 기술

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL 데이터 모델은 정형화된 표(Table) 형식을 넘어, 데이터의 성격에 따라 **Key-Value, Document, Column-Family, Graph**의 4가지 최적화된 저장 구조를 제공한다.
> 2. **가치**: 캐시(KV), 웹 콘텐츠(Doc), 대용량 통계(Column), 관계 탐색(Graph) 등 각 도메인에 특화된 물리적 구조를 가짐으로써 RDBMS가 해결하지 못한 성능 한계를 돌파한다.
> 3. **융합**: 현대 아키텍처에서는 하나의 서비스 내에서도 데이터 모델별 장점을 취사선택하는 폴리글랏 퍼시스턴스(Polyglot Persistence) 전략으로 융합되어 사용된다.

+++

### Ⅰ. NoSQL 4대 모델 비교 요약

| 모델명 | 데이터 구조 | 주요 특징 | 대표 제품 |
|:---|:---|:---|:---|
| **Key-Value** | 단순 배열 (Map) | 속도 최우선, 가장 단순 | Redis, Memcached |
| **Document** | JSON, BSON (Tree) | 객체 지향적, 유연한 검색 | MongoDB, CouchDB |
| **Column-Family** | 희소 행렬 (Grid) | 대량 쓰기, 압축, 분석 유리 | Cassandra, HBase |
| **Graph** | Node & Edge (Network) | 관계 및 경로 탐색 특화 | Neo4j, Neptune |

+++

### Ⅱ. 모델별 시각화 (ASCII Map)

```text
[ 1. Key-Value ]       [ 2. Document ]
 { "ID": "Val" }        { "ID": 1, "Profile": { "Age": 20, "City": "Seoul" } }

[ 3. Column-Family ]   [ 4. Graph ]
 (RowKey) ┬─ (Col1)      (Node: User) ───[Edge: Follows]──▶ (Node: User)
          └─ (Col2)           │                                 ▲
                              └─────────[Edge: Likes]───────────┘
```

+++

### Ⅲ. 모델별 최적의 유즈케이스

1. **Key-Value**: 세션 관리, 실시간 순위표, 고성능 캐싱.
2. **Document**: 블로그 포스트, 상품 카탈로그, 사용자 프로필.
3. **Column-Family**: 로그 데이터 분석, IoT 센서 데이터 수집, 시계열 통계.
4. **Graph**: 소셜 네트워크 친구 추천, 사기 탐지(Fraud Detection), 경로 최적화.

- **📢 섹션 요약 비유**: NoSQL 모델은 **'서류 가방의 종류'**와 같습니다. KV는 '단순한 파우치', Doc은 '칸막이 있는 백팩', Column은 '대형 캐리어', Graph는 '그물망 가방'인 셈입니다. 립밤 하나 넣을 땐 파우치가 최고지만, 이사할 땐 캐리어가 필요하듯 데이터의 양과 용도에 맞는 가방을 잘 골라야 합니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Aggregate Oriented]**: KV, Doc, Column 모델을 묶어 부르는 통칭.
- **[No Join]**: Graph 모델을 제외한 나머지가 성능을 위해 포기한 것.
- **[Impedance Mismatch]**: 객체 지향 언어와 데이터 모델 간의 괴리를 해결하려는 노력.

📢 **마무리 요약**: **4대 데이터 모델**은 현대 개발자의 필수 도구 상자입니다. 저장할 데이터의 형태를 먼저 보고, 그에 가장 잘 맞는 그릇을 골라 담는 것이 시스템 설계의 핵심입니다.