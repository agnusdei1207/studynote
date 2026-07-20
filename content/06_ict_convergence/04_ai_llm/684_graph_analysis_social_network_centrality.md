---
title: "Graph Analysis Social Network Centrality"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 684
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 소셜 네트워크 중심성(Social Network Centrality)은 그래프 G=(V,E) 위에서 노드·엣지·부분그래프의 구조적 중요도를 정량화하는 메트릭 체계로, 차수 중심성(Degree), 매개 중심성(Betweenness), 근접 중심성(Closeness), 아이겐벡터·페이지랭크·허브/authority·Katz·근조화(Harmonic) 등으로 분류되며, 각각 국부 연결성·경로 중개성·도달 효율성·영향 전파력을 측정한다.
> 2. **가치**: 직관적 차수 중심성 대비 매개·아이겐벡터 중심성은 O(V·E)∼O(V³)의 계산 복잡도를 가지지만, Brandes' algorithm 적용 시 매개 중심성을 O(V·E)까지 단축 가능하며, 이를 통해 1억 노드 규모의 그래프에서 영향력자(Influencer)·사기 허브(Fraud Ring Hub)·병목 라우터·단백질 상호작용 핵심 인자의 식별 정확도를 70~95% 수준으로 향상시킨다.
> 3. **판단 포인트**: 그래프 밀도·방향성·가중치 유무·시간 동적성·스케일에 따라 적합한 중심성이 달라지며, 대규모(>10⁸ 엣지) 환경에서는 Neo4j·TigerGraph 같은 네이티브 그래프 DB, Apache Spark GraphFrames/GraphX, Pregel/Giraph 기반 BSP 모델이 필수이고, 단일 메트릭 의존의 환원주의적 오류를 피하기 위해 다중 중심성 결합(Multi-centrality Ensemble)과 α-중심성 같은 연속 일반화 모형을 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

소셜 네트워크 분석(Social Network Analysis, SNA)의 핵심은 "어떤 노드가 다른 노드들 사이의 관계 구조에서 전략적으로 중요한 위치를 점유하고 있는가"를 측정하는 것이다. 1948년 Shaw이 제안하고 Bavelas(1950)가 실험으로 정형화한 중심성 개념은 이후 Freeman(1977, 1979)이 차수·매개·근접의 3대 메트릭을 수학적으로 완성하면서 현대 그래프 이론의 한 축으로 자리 잡았다. 이후 Bonacich(1972)의 아이겐벡터 중심성, Brin-Page(1998)의 PageRank, Kleinberg(1999)의 HITS, Katz(1953)의 감쇠합 산정 등 전파·순위·계층을 반영한 후속 메트릭이 등장했다.

기존 RDBMS 기반의 JOIN 연쇄 분석은 깊이(Depth) k=3만 넘어가도 결과 집합이 지수적으로 폭증하여(예: 평균 차수 d=10, 깊이 3 -> 1,000개 노드 스캔) 실시간 분석이 불가능했다. 그래프 네이티브 처리 방식은 인덱스 프리 어드미션(Index-Free Adjacency)을 통해 1-hop 이웃을 O(1)에 조회하고, multi-hop traversal을 인접 리스트 기반으로 처리하여 10⁻⁶~10⁻³ 초 단위로 응답한다. 마케팅·보안·바이오인포매틱스·전력 그리드·IoT 등 거의 모든 도메인에서 "가장 영향력 있는 누군가/가장 취약한 연결"을 찾는 것이 의사결정의 핵심 변수이므로, 소셜 네트워크 중심성은 단순 학문적 지표가 아니라 **데이터 기반 의사결정의 1차 필터**로 작동한다.

```text
[전통 RDBMS vs 그래프 네이티브 중심성 분석 비교]

   +------------------+                +------------------------------+
   |   RDBMS 환경     |                |   Graph-Native 분석 환경     |
   |  (관계형 조인)    |                |   (인접 리스트 + 인메모리)    |
   +--------+---------+                +--------------+---------------+
            |                                          |
   +--------v---------+                +---------------v---------------+
   | User --+         |                |  (A)--(B)--(C)--(D)           |
   |        |         |                |   |  ╲ |  ╱ |                 |
   | User --+ JOIN×N  |   ------►      |  (E)--(F)--(G)                |
   |        |         |   (Bavelas     |   |   ╲ |  ╱ |                 |
   | User --+         |    Freeman     |  (H)--(I)--(J)                |
   |  + Friend        |    Brandes)    |   ^ 인접 행렬 CSR/COO 인덱스  |
   |  + FriendOf      |                |   ^ n-hop 즉시 인출            |
   |  + Liked_Page    |                |   ^ α·β·γ 파라미터 즉시 산정  |
   +------------------+                +----------------------------------+
   * 3-hop 조회: ~10²~10⁴ ms                * 3-hop 조회: ~1~50 ms
   * 메모리:  관계형 O(n²) 정규화              * 메모리:  인접 리스트 O(n+E)
   * 정확도:  샘플링 손실 多                   * 정확도:  exact / approximate
```

**기존 패러다임 대비 신규 패러다임의 진화 포인트**

| 항목 | 관계형 SQL 다중 JOIN | 그래프 트래버설 + 중심성 분석 |
| :--- | :--- | :--- |
| **시간 복잡도** | 깊이 k에 대해 O(dᵏ) (폭발) | BFS/DFS 기반 O(V+E) |
| **메모리 모델** | 행 단위 정규화, FK 인덱스 | 인접 리스트(CSR/COO) + 라벨 |
| **쿼리 패러다임** | 선언적 관계 질의 (SQL) | 절차적·경로 의존 질의 (Cypher/GQL/SPARQL) |
| **중심성 갱신 비용** | 전체 재계산 필요 | 증분 업데이트 (Δ-degree, Δ-edge) 가능 |
| **시각화** | ER 다이어그램 (정적) | Force-directed, Arc Diagram, Multi-layer |

- **📢 섹션 요약 비유**: 왕국에서 "누가 진짜 권력자인가"를 가려내려면, 신하 수를 세는 것(차수)만으로는 부족하고, 왕과 왕 사이의 다리 역할을 하는 사람(매개), 명령이 가장 빠르게 퍼지는 사람(근접), 그리고 권력자들과 직접 연결된 사람(아이겐벡터)을 함께 봐야 진짜 영향력자가 보인다. RDBMS는 신하 명부를 노려보는 것이고, 그래프 분석은 왕국의 전체 지도를 입체적으로 펼치는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

소셜 네트워크 중심성 분석 시스템은 일반적으로 **① 데이터 수집 -> ② 그래프 모델링 -> ③ 메트릭 산출 -> ④ 시각화·응용**의 4계층 파이프라인으로 구성된다. 입력 그래프는 방향성·가중치·시간차원의 유무에 따라 (a) 단순 무향 비가중치, (b) 방향 그래프(Digraph), (c) 다중 가중치 그래프(Multi-weight), (d) 시계열 다층 그래프(Temporal/Multiplex)로 분류되며, 메트릭 정의 자체가 그래프 유형에 의존한다.

### 중심성 메트릭별 수학적 정의

```text
1) 차수 중심성 (Degree Centrality)            C_D(v) = deg(v) / (|V|-1)
   - 정규화:   C'_D(v) = deg(v)/(n-1)
   - 방향:     in-degree C_D⁻(v), out-degree C_D⁺(v)

2) 매개 중심성 (Betweenness Centrality)
   C_B(v) = Σ_{s≠v≠t}  [σ_st(v) / σ_st]
   σ_st   : s->t 최단경로 수
   σ_st(v): 그 중 v를 지나는 경로 수
   - Brandes(2001) 알고리즘: 단일 BFS로 모든 최단경로 수 누적
     δ_s(v) = Σ_w  δ_s(w) / σ_sw  · [v∈P_s(w)]
   - 정규화: C'_B(v) = C_B(v) / [(n-1)(n-2)/2]   (무향, ordered pair)

3) 근접 중심성 (Closeness Centrality)
   C_C(v) = (|V|-1) / Σ_{u≠v} d(v,u)
   - Wasserman-Faust 보정(연결 그래프 외): Σ_{u∈R(v)} 2⁻ᵈ⁽ᵛ·ᵘ⁾
   - 근조화 중심성(Harmonic, decaying): C_H(v) = Σ_{u≠v} 1/d(v,u)

4) 아이겐벡터 / Bonacich 중심성
   C_E(v) = (1/λ) · Σ_{u∈N(v)} C_E(u)
   -> 고유방정식 A·x = λ·x 의 최대 고유값 λ_max에 대한 고유벡터
   - Power iteration: x^{(k+1)} = (A·x^{(k)}) / ||A·x^{(k)}||₂

5) PageRank (방향 + 감쇠)
   PR(v) = (1-d)/N + d · Σ_{u->v}  PR(u) / L(u)
   d: 감쇠계수(0.85), L(u): out-degree of u, dangling node 처리
   - Power method, Gauss-Seidel, Monte Carlo 병렬화

6) Katz 중심성 (감쇠합)
   C_K(v) = Σ_{k=1}^∞  Σ_{u∈Nᵏ(v)}  αᵏ  = α·A·(I - αA)⁻¹·𝟏
   0 < α < 1/λ(A) 이어야 수렴

7) HITS (Hyperlink-Induced Topic Search)
   hub(v)    = Σ_{v->u}  auth(u)
   auth(v)   = Σ_{u->v}  hub(u)
   -> 서로 상호 강화되는 두 벡터로 수렴

8) α-중심성 / DECA / Cross-Clique
   C_α(v) = Σ_{u∈V\{v}}  e^(-α·d(v,u))        (α: 감쇠율)
```

```text
[소셜 네트워크 중심성 분석 시스템 4계층 아키텍처]

   +--------------------------------------------------------------------+
   |  L1. Data Ingestion                                              |
   |   +----------+ +----------+ +----------+ +----------+              |
   |   | Twitter  | | Facebook | |   Call   | |  Mobile  |              |
   |   |   API    | |   Graph  | |   CDR    | |  Cell-ID |              |
   |   +----+-----+ +----+-----+ +----+-----+ +----+-----+              |
   |        +------------+-----+------+------------+                    |
   |                          v                                         |
   |            Kafka / Pulsar / Kinesis                                |
   |            (event-time, idempotent ingestion)                      |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  L2. Graph Storage & Modeling                                      |
   |   +-------------+  +-------------+  +-------------+                |
   |   |  Neo4j 5.x  |  | TigerGraph  |  | JanusGraph  |                |
   |   | (Labeled    |  | (Native MPP |  | (Cassandra  |                |
   |   |  Property)  |  |  C++)       |  |  +ES)       |                |
   |   +------+------+  +------+------+  +------+------+                |
   |          |                |                |                       |
   |   +------v------+  +------v------+  +------v------+                |
   |   |  Apache     |  |  NetworkX   |  |  iGraph     |                |
   |   |  TinkerPop  |  |  (in-mem)   |  |  (C core)   |                |
   |   |  Gremlin    |  |             |  |             |                |
   |   +-------------+  +-------------+  +-------------+                |
   |   Schema: (Person)-[:FOLLOWS {ts, weight}]->(Person)               |
   |           (Person)-[:POSTED]->(Tweet)<-[:MENTIONS]-(Person)        |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  L3. Centrality Computation Engine                                 |
   |   +---------------------------------------------------------+      |
   |   |  Exact Algorithms                                       |      |
   |   |   • Brandes Betweenness  O(VE)  (single-source BFS)     |      |
   |   |   • Dijkstra for weighted betweenness                    |      |
   |   |   • Power Iteration for Eigenvector / PageRank          |      |
   |   |   • Floyd-Warshall for all-pairs (small world only)     |      |
   |   +---------------------------------------------------------+      |
   |   |  Approximation / Sampling                               |      |
   |   |   • Riondato-Kornaropoulos  VC-dim sampling for k-medo. |      |
   |   |   • Bader et al. adaptive sampling for betweenness      |      |
   |   |   • Local clustering coefficient (transitivity)         |      |
   |   +---------------------------------------------------------+      |
   |   |  Distributed BSP / Pregel-like                          |      |
   |   |   • Spark GraphX (Pregel API)                            |      |
   |   |   • Apache Giraph                                        |      |
   |   |   • Google Pregel / cuGraph (GPU)                        |      |
   |   +---------------------------------------------------------+      |
   +----------------------------+---------------------------------------+
                                v
   +--------------------------------------------------------------------+
   |  L4. Application & Visualization                                   |
   |   • Gephi / Cytoscape / d3-force                                   |
   |   • Influence ranking dashboard                                    |
   |   • Fraud ring detection alert                                     |
   |   • Recommendation: candidate injection for cold-start             |
   |   • Diffusion simulator (SIR / IC / LT)                            |
   +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **그래프 스토어 (Graph Store)** | 노드·엣지의 영속 저장과 1-hop O(1) 인출 | Neo4j 5.x (Cypher, Labeled Property Graph), TigerGraph 3.x (GSQL, C++ MPP), Memgraph, Amazon Neptune (SPARQL/Gremlin), ArangoDB (multi-model) |
| **연산 엔진 (Computation Engine)** | 중심성 메트릭 산출의 분산·병렬 처리 | Apache Spark GraphX/GraphFrames (lineage, Pregel API), Giraph (BSP), NetworkX (in-mem·연구용), iGraph/C (R/Python), cuGraph (GPU), igraph-python |
| **메트릭 알고리즘 (Metric Algorithms)** | 차수·매개·근접·아이겐벡터·PageRank 등의 정량화 | Brandes' BFS for Betweenness (O(VE)), Power Iteration for Eigenvector (O(k·E)), Jacobi-Davidson (대형 sparse), Riondato–Kornaropoulos VC-dim sampling (ε-approximation) |
| **확산 시뮬레이터 (Diffusion Simulator)** | 영향력 전파의 시간·확률 모델링 | Independent Cascade (IC), Linear Threshold (LT), SIR/SEIR (감염병), Continuous-Time Markov, Agent-Based Monte Carlo (10⁴~10⁶ trial) |
| **시