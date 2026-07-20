---
title: "RAG Retrieval Augmented Generation Vector Search"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 646
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RAG(Retrieval-Augmented Generation)는 대규모 언어 모델(LLM)의 환각(hallucination) 문제와 지식 cutoff 한계를 해결하기 위해, 외부 지식베이스에서 **Dense Vector 검색**(Dense Passage Retrieval, DPR)을 통해 관련 문서를 검색하고 이를 LLM의 컨텍스트로 주입하는 검색-증강-생성 파이프라인이다. 핵심은 **임베딩 모델**(BGE, E5, OpenAI text-embedding-3, Cohere embed-v3)과 **ANN(Approximate Nearest Neighbor) 인덱스**(HNSW, IVF-PQ, ScaNN)를 통한 시맨틱 검색이다.
> 2. **가치**: 도메인 특화 QA 시스템에서 **환각률을 60~80% 감소**시키고, fine-tuning 대비 **구축 비용을 1/10 수준**으로 절감하며, 실시간 지식 갱신이 가능하다. 검색 latency 50~200ms 수준에서 recall@10 ≥ 0.95 달성이 가능하며, 엔터프라이즈 지식관리 응답 정확도를 40~70% 향상시킨다.
> 3. **판단 포인트**: 벡터 차원(dim 384/768/1024/1536/3072), 인덱스 알고리즘(HNSW M=16~64, efConstruction=200), 청크 크기(128~512 tokens, overlap 10~20%), 리랭킹 적용 여부, 하이브리드 검색(BM25 + Dense) 가중치(α=0.3~0.7) 등이 recall-정확도-latency 트레이드오프를 결정한다.

---

## Ⅰ. 개요 및 필요성

LLM(예: GPT-4, Claude 3.5, Llama 3.1)은 학습 시점 이후의 정보, 사내 confidential 데이터, 도메인 특화 지식에 대해 부정확한 답변을 생성하는 **환각(Hallucination)** 현상을 보인다. 또한 파라미터 학습 방식의 fine-tuning은 GPU 인프라 비용이 높고, 지식 갱신 시마다 재학습이 필요하다. **RAG(Retrieval-Augmented Generation)**는 2020년 Facebook AI의 Lewis et al. 논문 *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*에서 정식 제안되었으며, LLM의 **외부 메모리(External Memory)** 역할을 수행한다.

기존 keyword 기반 검색(BM25, TF-IDF)의 한계는 **어휘 불일치 문제(lexical mismatch)**이다. 예를 들어 "자동차"로 검색하면 "차량", "승용차"는 매칭되지 않는다. **Dense Vector 검색**은 텍스트를 고차원 임베딩 공간(예: 1536차원)에 매핑하여 의미적 유사성을 코사인 유사도(Cosine Similarity)로 측정하므로, **의미적 동치어(semantic synonyms)** 검색이 가능하다. 이를 통해 LLM은 검색된 문서 청크(Chunk)를 컨텍스트로 활용하여 **근거 기반(grounded) 답변**을 생성한다.

```text
   [기존 LLM 단독 파이프라인]            [RAG 기반 파이프라인]

   사용자 질문 ---> LLM ---> 답변            사용자 질문 ---> Query Encoder
                       |                                  |
                       |                                  v
                       |                         +--- Vector DB (ANN Search)
                       |                         |    +- Chunk 1: "RAG는 2020년..."
                       |                         |    +- Chunk 2: "임베딩 모델은..."
                       |                         |    +- Chunk 3: "벡터 인덱스는..."
                       |                         +----------+--------------+
                       |                                    v
                       |                         Top-K 청크 (K=3~10)
                       |                                    |
                       +------------------+                |
                                          v                v
                                       Prompt: "Context: {chunks} + Question: {query}"
                                          |
                                          v
                                       LLM ---> 근거 기반 답변 (with citation)
```

**📢 섹션 요약 비유**: RAG는 "시험공부를 혼자 하는 학생" vs "**오픈북 시험**을 보는 학생"의 차이이다. LLM이 "오픈북"을 통해 답을 찾을 때, **벡터 검색**은 책의 목차/색인이 아니라 **의미 기반으로 가장 관련 있는 페이지를 찾아주는 스마트 도서관 사서** 역할이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RAG 시스템은 크게 **Offline Indexing Pipeline**(문서 전처리 -> 청킹 -> 임베딩 -> 벡터 DB 저장)과 **Online Retrieval-Augmented Pipeline**(Query 임베딩 -> ANN 검색 -> 리랭킹 -> 프롬프트 합성 -> LLM 생성)으로 구분된다.

```text
-----------------------------------------------------------------------
  [Offline Indexing] - 문서 수집 시 1회 수행
-----------------------------------------------------------------------

  +--------------+    +--------------+    +--------------+    +--------------+
  |  Data Source |    |   Chunking   |    |  Embedding   |    |  Vector DB   |
  |  (Docs, PDF, |--->|  (Split +    |--->|  (BGE-M3,    |--->|  (Milvus,    |
  |   Confluence,|    |  Overlap)    |    |   E5, ada)   |    |   Pinecone)  |
  |   Notion 등) |    |  256~512 tok |    |  dim=768~3072|    |   HNSW/IVF   |
  +--------------+    +--------------+    +--------------+    +--------------+
        |                     |                   |                    |
        |            Semantic Chunking,         |              Metadata:
        |            Sentence-aware split        |              - doc_id
        |                     |                  |              - chunk_id
        |                     v                  |              - source
        |           +-----------------+          |              - timestamp
        |           | 청크 예시:      |          |
        |           | "RAG는 검색과   |          |
        |           |  생성을 결합..."|          |
        |           +-----------------+          |
        |                     |                  |
        |                     +---------+--------+
        |                               v
        |                     vec = [0.023, -0.114, ..., 0.872]
        |                     (1536-dim float32 vector)
        |                               |
        |                               v
        |                  [0.023, -0.114, ...]  --> row_id: 12345
        |                  [0.451, 0.223, ...]   --> row_id: 12346
        |                  [ ... ]               --> row_id: 12347


-----------------------------------------------------------------------
  [Online Retrieval] - 사용자 질의 시 실시간 수행
-----------------------------------------------------------------------

  사용자 Query ---> Query Encoder ---> q_vec [1×d]
                                              |
                                              v
                              +------------------------------+
                              | ANN Search (HNSW/IVF-PQ)    |
                              | similarity = cos(q, c)       |
                              | = (q·c) / (||q||·||c||)      |
                              +--------------+---------------+
                                             |
                                             v
                              Top-K chunks (K=5~20) by score
                                             |
                                             v
                              [Optional] Re-ranker (BGE-reranker, Cohere Rerank)
                                             |
                                             v
                              Top-N relevant chunks (N=3~5)
                                             |
                                             v
                              +---------------------------------+
                              | Prompt Assembly:                |
                              | System: "주어진 컨텍스트로 답변"  |
                              | Context: [chunk1][chunk2]...    |
                              | Question: {user_query}          |
                              +--------------+------------------+
                                             v
                                        LLM (GPT-4, Claude)
                                             |
                                             v
                                  Answer + Source Citation
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **임베딩 모델 (Embedding Model)** | 텍스트 -> 고차원 실수 벡터 변환 | BGE-M3 (BAAI, 다국어 1024d), E5-Large (Microsoft, 1024d), OpenAI text-embedding-3-small/large (1536/3072d), Cohere embed-multilingual-v3 (1024d), KoSimCSE (한국어 특화 768d), KR-FinBert (금융 도메인) |
| **청킹 전략 (Chunking)** | 문서를 검색 단위로 분할 | Fixed-size chunking (256~512 tokens, overlap 10~20%), Semantic chunking (임계값 기반 경계 탐지), Sentence-aware split, Recursive character splitting, Document-aware (Markdown header, HTML section) |
| **벡터 데이터베이스 (Vector DB)** | 임베딩 벡터 저장 및 ANN 검색 | **Pinecone** (관리형 SaaS, pod-based), **Weaviate** (GraphQL + HNSW + BM25 하이브리드), **Milvus** (분산, IVF/HNSW/DiskANN, Go/C++ 구현), **Qdrant** (Rust, payload filtering 강점), **Chroma** (로컬 경량, LangChain 통합), **FAISS** (Meta, 라이브러리형), **pgvector** (PostgreSQL 확장) |
| **ANN 인덱스 알고리즘** | 고차원 벡터 유사도 검색 가속 | **HNSW** (Hierarchical Navigable Small World, M=16~64, efConstruction=100~200, efSearch=50~500, recall@10 ≥ 0.95), **IVF-PQ** (Inverted File + Product Quantization, nlist=√N, m=8~64, 메모리 1/32 압축), **ScaNN** (Google, Anisotropic Vector Quantization), **DiskANN** (Microsoft, SSD 기반 10억 스케일) |
| **유사도 측정 (Similarity Metric)** | 두 벡터 간 관련성 계산 | **Cosine Similarity** (정규화 후 내적, [-1, 1], 가장 일반적), **Euclidean L2 Distance** (벡터 크기 영향 받음), **Dot Product** (정규화 시 Cosine과 동일, Asymmetric retrieval에 사용) |
| **리랭커 (Re-ranker)** | 1차 검색 결과 정밀 재정렬 | Cross-Encoder 모델 (BGE-reranker-v2-m3, MS-MARCO MiniLM, Cohere Rerank 3.5), Bi-Encoder의 100배 정확도, 5~50배 느린 latency, Top-100 -> Top-3~5 |
| **LLM (Generator)** | 컨텍스트 기반 답변 생성 | GPT-4o (128K ctx, $5/$15 per 1M tokens), Claude 3.5 Sonnet (200K ctx), Llama 3.1 70B (로컬), Mistral Large, HyperCLOVA X (한국어) |

**임베딩 수학적 원리**: 텍스트 $t$는 임베딩 함수 $f: \mathcal{T} \rightarrow \mathbb{R}^d$를 통해 $d$차원 벡터 $\mathbf{v}_t \in \mathbb{R}^d$로 매핑된다. 검색 시 코사인 유사도는 다음과 같이 정의된다:
$$\text{cos}(\mathbf{q}, \mathbf{c}) = \frac{\mathbf{q} \cdot \mathbf{c}}{\|\mathbf{q}\|_2 \|\mathbf{c}\|_2} = \frac{\sum_{i=1}^{d} q_i c_i}{\sqrt{\sum_{i=1}^{d} q_i^2} \sqrt{\sum_{i=1}^{d} c_i^2}}$$

**HNSW 파라미터 영향**: HNSW는 다층 그래프 구조로 $O(\log N)$ 시간 복잡도를 가지며, `M`(노드당 연결 수, 16~64), `efConstruction`(빌드 시 탐색 후보, 100~500), `efSearch`(쿼리 시 탐색 후보, 50~500) 파라미터로 recall-latency를 조절한다. `M=32, efConstruction=200, efSearch=100`이 일반적 기본값이며, recall@10 ≥ 0.95를 위해 `efSearch ≥ 100` 권장된다.

**📢 섹션 요약 비유**: 벡터 검색은 "**수만 권의 책을 좌표 평면 위에 펼쳐놓는 것**"과 같다. 비슷한 주제의 책끼리는 가까운 위치에 놓이게 되고, 사용자의 질문을 하나의 점으로 찍으면 가장 가까운 책들을 자동으로 찾아준다. HNSW는 이 평면 위에 "지름길 도로망"을 깔아 빠른 검색이 가능하게 하는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Sparse Retrieval (BM25/TF-IDF)** | **Dense Vector Retrieval (RAG 핵심)** | **Hybrid Search (BM25 + Dense)** |
| :--- | :--- | :--- | :--- |
| **표현 방식** | 단어 빈도 기반 sparse vector (vocab 크기, 0이 대부분) | 의미 기반 dense vector (모든 차원 nonzero, dim=768~3072) | 두 방식의 score를 가중합 (RRF 또는 linear combination) |
| **어휘 일치 강점** | 매우 강함 (정확한 keyword 매칭, 코드/ID/제품번호) | 약함 (의미는 맞지만 단어가 다르면 recall 저하) | 양쪽 장점 결합 |
| **의미 이해** | 없음 (synonym, paraphrase 처리 불가) | 강함 (paraphrase, multilingual, conceptual) | 강함 |
| **인덱스 구조** | Inverted Index (Posting List) | HNSW / IVF-PQ / DiskANN | BM25 Inverted + HNSW 동시 운영 |
| **검색 속도** | 매우 빠름 (Elasticsearch, 10K QPS) | 빠름 (Pinecone/Milvus, 1K~10K QPS) | 두 시스템 동시 조회로 1.5~2배 latency |
| **저장 비용** | 낮음 (수 MB/문서) | 높음 (4 byte × 1536 dim = 6KB/doc, 10M docs -> 60GB) | 가장 높음 (양쪽 저장) |
| **주 사용 사례** | 법률/의료/코드 검색 (정확한 용어 매칭 중요) | 일반 QA, semantic search, RAG | 엔터프라이즈 검색 표준 (Azure AI Search, Elastic 8.0+) |
| **대표 시스템** | Elasticsearch BM25, OpenSearch, Solr, Lucene | Pinecone, Milvus, Weaviate, Qdrant, Chroma, FAISS, Vespa | Azure Cognitive Search, Elasticsearch 8 ELSER, Weaviate Hybrid, Vespa |

**다른 RAG 변형 아키텍처**:
- **Naive RAG**: 단순 Query -> Retrieve -> Prompt -> LLM 구조
- **Advanced RAG**: Pre-retrieval (Query rewriting, HyDE, Multi-Query) + Post-retrieval (Re-ranking, Contextual compression)
- **Modular RAG**: 검색 모듈, 메모리 모듈, 라우팅 모듈을 분리/조립 (Self-RAG, FLARE, CRAG)
- **GraphRAG**: Neo4j/Memgraph + Vector 결합 (Microsoft GraphRAG, 2024)
- **Agentic RAG**: LangGraph/AutoGen 기반 multi-agent RAG (Self-Reflective RAG, 2024)

**연계 시스템**:
- **LangChain / LlamaIndex**: RAG 오케스트레이션 프레임워크 (Loader, Splitter, Retriever, VectorStore 인터페이스)
- **LangSmith / Langfuse**: RAG 트레이싱 및 평가 (retrieval recall, generation faithfulness)
- **RAGAS / TruLens**: RAG 전용 평가 프레임워크 (Context Precision, Context Recall, Faithfulness, Answer Relevancy)
- **Haystack (deepset)**: Production-grade RAG 파이프라인

**📢 섹션 요약 비유**: Sparse 검색은 "찾고 싶은 단어가 정확히 적힌 색인"이고, Dense 검색은 "**주제가 비슷한 책장**을 찾아주는 것"이다. Hybrid 검색은 "색인을 먼저 뒤지고, 책장 추천까지 받는" 가장 똑똑한 도서관