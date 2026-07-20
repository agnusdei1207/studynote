---
title: "Knowledge Graph Ontology Semantic Web"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 683
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시맨틱 웹(Semantic Web)은 **RDF(Subject-Predicate-Object) 트리플**을 최소 의미 단위로 채택하고, **RDFS/OWL**로 클래스·속성·제약(카디널리티, 역관계, 동치관계)을 형식적으로 정의하며, **SPARQL**로 그래프 패턴 매칭 질의와 **RDFS/OWL 추론(Reasoning)**을 통해 암묵적 사실을 도출하는 메타데이터 아키텍처이다. 지식 그래프(Knowledge Graph)는 이를 엔터티·관계·속성 그래프 자료구조로 실체화하여 **Google Knowledge Vault, Wikidata, DBpedia, Schema.org** 같은 대규모 개방형 지식 베이스를 가능케 한 산업적 구현물이다.
> 2. **가치**: 구조화되지 않은 HTML 문서 기반 웹 대비 **기계 판독 가능성(Machine Readability)**, **엔터티 단위 정확도 90% 이상**(Google KG 기반 검색), **SPARQL Federation으로 이기종 데이터 통합**, **온톨로지 추론을 통한 0-shot 지식 확장**이라는 정성적 가치와, **스키마 진화(Schema Evolution) 시 애플리케이션 재컴파일 불필요**, **데이터 중복 제거로 30~60% 저장 효율** 등 정량적 이점을 제공한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ①**Owl:Thing까지 표현하는 최대 표현력 vs RDF 트리플 폭발(>10억)**로 인한 쿼리 성능 저하, ②**OWL2 DL의 결정가능성(Decidability) 보장 vs 표현력 한계**(OWL2 Full은 비결정가능), ③**Materialized Inference(추론 결과 사전 계산) vs Query-time Reasoning(질의 시 추론)**의 스토리지·응답시간 트레이드오프, ④**온톨로지 중앙 통제 vs 링크드 데이터의 분산 진화** 거버넌스 모델 선택이다.

---

## Ⅰ. 개요 및 필요성

1990년대 이후 폭증한 HTML 문서 웹(Document Web)은 인간이 읽기에는 직관적이지만 기계가 의미를 해석하기에는 한계가 명확했다. 검색 엔진은 키워드 매칭과 PageRank에 의존하여 "Apple"이 과일인지 IT 기업인지 구분하지 못했고(시맨틱 갭, Semantic Gap), 같은 개념을 표현하는 이기종 데이터베이스 간 통합은 ETL 파이프라인과 스키마 매핑 작업의 반복으로 이어졌다. 2001년 Tim Berners-Lee는 **"The Semantic Web"** Scientifc American 기고문을 통해 데이터를 문서가 아닌 **"데이터의 데이터(Metadata)"**로 기술하고, 기계가 의미적으로 추론·판단할 수 있는 웹 비전을 제시했다.

이 비전의 핵심 동기는 ①**데이터 상호운용성(Interoperability)** — 서로 다른 도메인의 데이터를 URI 기반 통합 식별자로 연결, ②**암묵적 지식의 명시화(Explicit Knowledge)** — ID/하나는 Person이고 hasParent로 Person을 가리키면 그 대상은 Father로 추론 가능, ③**진화하는 스키마(Schema Evolution Tolerance)** — 관계형 DB의 ALTER TABLE 없이 클래스/속성 추가만으로 확장이다. 2012년 Google이 **Knowledge Graph**(초기 5억 엔터티, 35억 사실)를 검색에 도입하면서 산업적 임계점이 형성되었고, 2010년대 후반 LLM의 환각(Hallucination) 문제가 대두되며 **Retrieval-Augmented Generation(RAG)** 의 사실 그라운딩(Grounding) 소스로 KG가 재조명되고 있다.

```text
[시맨틱 웹의 진화: 문서 웹에서 데이터 웹으로]

  +------------------+         +------------------+
  |  Document Web    |         |  Semantic Web    |
  |  (Web 1.0~2.0)   |         |   (Web 3.0)      |
  +--------+---------+         +--------+---------+
           |                            |
   HTML / XML 문서                RDF 트리플 그래프
   키워드 인덱싱                  URI 기반 식별
   인간 독해 위주                 기계 추론 가능
   PageRank                       SPARQL + Reasoner
           |                            |
   문제: 동음이의어(Apple),          해결: URI로 엔터티 구분
         스키마 종속,                 -> kg:Apple_Inc
         이기종 DB 통합 불가          -> kg:Apple_(fruit)
           v                            v
   +---------------------------------------------+
   |  지식 그래프(Knowledge Graph) 시대 (2012~)  |
   |  · Google KG, Wikidata, DBpedia, Freebase   |
   |  · LLM + KG (Neuro-Symbolic AI)            |
   +---------------------------------------------+
```

기존 RDBMS 패러다임은 "데이터를 어떻게 저장·조회할 것인가"에 집중했다면, 시맨틱 웹은 "데이터가 무엇을 의미하는가"를 형식적으로 표현한다. 이는 단순한 기술 변화가 아니라 **인식론적(Epistemological) 전환** — 데이터를 사실의 집합이 아니라 **명제(Proposition)의 집합**으로 다루는 패러다임 전환이다. 온톨로지(Ontology)는 특정 도메인의 개념·관계·제약을 명시적으로 형식화한 명세서이며, W3C 표준인 **RDF, RDFS, OWL, SKOS**가 이를 표현하는 언어 스택을 구성한다.

- **📢 섹션 요약 비유**: 기존 웹이 **"도서관의 책"**이라면 시맨틱 웹은 **"책 한 권 한 권에 국제 표준 도서번호(URI)를 부여하고, 책 간 참조·인용·번역을 컴퓨터가 자동으로 이해하도록 메타데이터 카드를 꽂아둔 도서관**이다. 사서가 "이 책의 저자가 쓴 다른 책"을 즉시 찾아주듯, 기계가 연관 사실을 추론한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시맨틱 웹 아키텍처는 **계층적(Layered)** 이며, 하위 계층이 상위 계층의 기반이 된다. W3C Semantic Web Stack이라 불리는 이 구조는 Unicode/URI 기반 식별에서 시작해 RDF 트리플, RDFS 클래스 모델, OWL 표현 논리, SPARQL 질의, 추론, 그리고 상위 응용(Trust, Proof)까지 7~8개 계층으로 구성된다. 각 계층은 단독으로도 사용 가능하지만, 통합使用时 추론과 검증을 통해 진정한 시맨틱 가치를 발휘한다.

```text
[W3C 시맨틱 웹 스택 (Layer Cake) — 데이터 흐름 포함]

  +--------------------------------------------------+
  |  Trust / Proof          <- 전자서명, 신뢰 평가    |
  +--------------------------------------------------+
  |  Inference / Reasoning  <- RDFS/OWL Reasoner      |
  |       ↕ SPARQL ASK/CONSTRUCT                       |
  |  Query: SPARQL          <- 그래프 패턴 매칭 질의 |
  +--------------------------------------------------+
  |  Ontology: OWL / RDFS   <- 클래스·제약·동치 정의|
  +--------------------------------------------------+
  |  Data: RDF / RDFS       <- Subject-Predicate-Obj |
  |       ↕ Turtle/N-Triple/JSON-LD/RDF-XML 직렬화  |
  +--------------------------------------------------+
  |  Identification: URI/IRI <- 모든 자원의 고유 ID   |
  +--------------------------------------------------+
  |  Syntax: XML / Unicode   <- 인코딩·구문 표현     |
  +--------------------------------------------------+
         ^                 ^
   RDFa/Microdata    SPARQL Endpoint
   (HTML 임베딩)     (질의 인터페이스)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **URI/IRI (Uniform Resource Identifier)** | 모든 자원(엔터티, 속성, 개념)의 **전역 고유 식별자**. DNS의 <urn:isbn:...> 또는 HTTP의 <http://dbpedia.org/resource/Seoul> 형태. IRI는 Unicode 확장으로 한글·일본어 도메인 지원. | 충돌 방지 위해 **namespace** 사용(`xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"`). HTTP URI 채택 시 **303 See Other** 또는 **Content Negotiation**으로 사람용 HTML·기계용 RDF 동시 제공(Tim Berners-Lee의 Linked Data 원칙 1번) |
| **RDF (Resource Description Framework)** | **트리플(S-P-O)** 최소 단위로 사실(Fact)을 기술. `ex:Seoul rdf:type dbo:City .` `ex:Seoul dbo:country ex:South_Korea .` 모든 RDF 그래프는 트리플 집합의 합집합으로 표현 가능. | 직렬화 포맷: **Turtle**(가독성 ^), **N-Triple**(라인당 1 트리플), **RDF/XML**(레거시), **JSON-LD**(웹 친화), **N-Quads/RDF-star**(메타 트리플·주석). RDF-star는 트리플 자체에 확신도·출처·시각 부여 |
| **RDFS (RDF Schema)** | RDF에 **클래스·속성·서브클래스(subClassOf)/서브속성(subPropertyOf)** 계층 도입. `rdfs:domain`(속성의 주체 범위), `rdfs:range`(속성의 대상 범위) 제약 가능. | 추론 예: `A rdfs:subClassOf B .` ∧ `x rdf:type A .` -> `x rdf:type B` (Type Propagation). 단순하지만 실용적 추론 다수 가능 |
| **OWL (Web Ontology Language)** | **SROIQ Description Logic** 기반. OWL2에서 `owl:ObjectProperty`, `owl:DatatypeProperty`, `owl:TransitiveProperty`, `owl:SymmetricProperty`, `owl:FunctionalProperty`, `owl:InverseFunctionalProperty`(고유 식별자), `owl:cardinality N`, `owl:disjointWith`, `owl:equivalentClass`, **Property Chain**(`A∘B ⊑ C`) 지원. | **OWL2 Profile**: EL(경량, 대용량, eClass), QL(SPARQL-기반 추론, 대규모 ABox), RL(Rule 기반). **OWL2 DL = SHOIN(D)** 결정가능, **OWL2 Full**은 비결정가능. SROIQ의 결정가능성 한계 -> 별도 Reasoner 필요 |
| **SPARQL (Protocol and RDF Query Language)** | **그래프 패턴 매칭** 질의 언어. SQL과 유사하지만 FROM에 매핑된 **기본 그래프(Graph)** 단위로 작업. **OPTIONAL**(LEFT JOIN), **UNION**, **FILTER**(정규식, 산술, 바운드), **GROUP BY/HAVING/ORDER BY**, **SUB-SELECT**, **VALUES**(바인딩 주입), **PROPERTY PATH**(`ex:parent/ex:brother` 축약) 지원. | 결과 형태: SELECT(튜플), CONSTRUCT(새 RDF 그래프 생성), ASK(불리언), DESCRIBE(RDF 덤프). **SPARQL 1.1 Federated Query**는 SERVICE 키워드로 여러 엔드포인트 통합. 엔드포인트는 HTTP GET/POST, Content-Type: `application/sparql-query` |
| **Triple Store / Quad Store** | RDF 그래프 전용 스토어. 내부 저장: **단일 테이블(3 컬럼)**(Jena SDB), **속성 테이블**(속성별 수직 분할, Jena TDB), **Triples Index(SPO/POS/OSP 6개 조합)**(RDF4J, Stardog, Virtuoso), **Graph DB(Neo4j, AllegroGraph)**. | 트리플 수 10억 이상 시 **Vertical Partitioning + Bitmap Index**(MonetDB/RDF), **Hexastore(6-index)**, **RDF-3X(클러스터 B+Tree)** 사용. SPARQL 1.1 Update(INSERT/DELETE/WHERE) 지원 |
| **Reasoner (추론 엔진)** | RDFS/OWL TBox 스키마로부터 **암묵적 사실(Entailment)** 도출. Forward Chaining(자료 입력 시 즉시 추론, Materialization) vs Backward Chaining(질의 시 경로 따라 추론). | 주요 구현: **HermiT**(OWL DL, Tableau 알고리즘), **Pellet**(SROIQ 완전 지원, ABox 일관성 검사), **FaCT++**(고성능), **ELK**(OWL2 EL, 실시간), **Jena InfModel**(RDFS/OWL Rules). OWL2 RL Profile은 Datalog 룰 변환 가능(Drools) |
| **R2RML / RML (Mapping Language)** | RDB->RDF 변환 매핑. R2RML은 RDB 한정, RML은 CSV/JSON/XML까지 확장. `rr:triplesMap`에 SQL 쿼리·주어 템플릿·예측-객체 매핑 정의. | KARMA, RML Mapper, Ontop(Virtual SPARQL — RDB를 SPARQL로 가상 노출, 온톨로지 매핑 기반) |

**핵심 메커니즘 — 트리플과 그래프 패턴 매칭**:
RDF는 모든 사실을 `Subject Predicate Object` 3-튜플로 표현한다. 예:
```
<http://dbpedia.org/resource/Seoul>  rdf:type  schema:City .
<http://dbpedia.org/resource/Seoul>  schema:country  <http://dbpedia.org/resource/South_Korea> .
<http://dbpedia.org/resource/Seoul>  schema:Population  9776000 .
```
SPARQL은 이 트리플을 변수가 포함된 **Triple Pattern**(`?city rdf:type schema:City .`)으로 매칭한다. 다중 패턴 결합이 **Basic Graph Pattern(BGP)** 이며, 이 BGP가 RDF 그래프의 부분 그래프 동형(Subgraph Homomorphism)으로 매칭된다.

```text
[SPARQL 그래프 패턴 매칭 메커니즘]

  RDF 그래프 (데이터)              SPARQL BGP (질의)

  Seoul --type--> City            ?city --type--> City
  Seoul --country--> S.Korea      ?city --country--> ?country
  Busan --type--> City            ?city --pop--> ?pop
  Busan --country--> S.Korea      FILTER(?pop > 1000000)
  Tokyo  --type--> City
  Tokyo  --country--> Japan       +-------------------------+
                                  | 매칭 결과 (Solution):    |
                                  | ?city=Seoul, ?country=  |
                                  |   S.Korea, ?pop=9776000 |
                                  | ?city=Busan, ?country=  |
                                  |   S.Korea, ?pop=3413000 |
                                  +-------------------------+
```

- **📢 섹션 요약 비유**: 시맨틱 웹 스택은 **"통역이 가능한 다층 우체국"**이다. 가장 아래 URI는 **우편번호**(전 세계 유일), RDF는 **"누가 무엇을 누구에게" 형식의 짧은 우편 엽서**, RDFS는 **엽서에 쓰인 단어의 뜻풀이 사전**, OWL은 **"아버지의 아버지는 할아버지다" 같은 우편 규칙집**, SPARQL은 **"이런 엽서만 골라줘"라는 검색 담당자**, Reasoner는 **