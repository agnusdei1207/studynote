---
title: "Vector Database"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 260
---
> **핵심 인사이트**
> 1. 벡터 데이터베이스(Vector Database)는 고차원 벡터 임베딩을 저장하고 근사 최근접 이웃(ANN) 검색을 수행하도록 특화된 데이터베이스 — LLM·이미지 인식·추천 시스템에서 "의미적으로 유사한 항목을 빠르게 찾는" 핵심 인프라가 되었다.
> 2. ANN(Approximate Nearest Neighbor) 알고리즘이 벡터 DB의 심장 — 정확한 최근접 이웃 탐색(Exact NN)은 고차원에서 O(N) 이상이지만, HNSW(계층적 탐색 그래프)·IVF·PQ 같은 ANN 알고리즘은 99%+ 리콜로 O(log N) 수준 성능을 달성한다.
> 3. RAG(Retrieval-Augmented Generation) 아키텍처에서 벡터 DB가 필수 구성 요소 — LLM의 지식 한계를 극복하기 위해 문서를 임베딩하여 벡터 DB에 저장하고, 질의(Query) 벡터와 유사한 문서를 검색하여 LLM 컨텍스트로 제공하는 패턴이 표준화됐다.

---

## Ⅰ. 벡터 임베딩과 유사도

```
벡터 임베딩 (Vector Embedding):
  텍스트, 이미지, 오디오를 고차원 벡터로 표현

  예:
  "고양이" -> [0.2, -0.5, 0.8, 0.1, ..., 0.3] (1536차원)
  "강아지" -> [0.3, -0.4, 0.7, 0.2, ..., 0.4]

  유사한 의미 = 가까운 벡터 위치

임베딩 생성 모델:
  텍스트: OpenAI text-embedding-3-large (3072차원)
          Sentence-BERT, E5, BGE
  이미지: CLIP, ResNet (512~2048차원)
  멀티모달: CLIP, DALL-E 내부

유사도 측정:

코사인 유사도 (Cosine Similarity):
  cos(θ) = (A · B) / (|A| × |B|)

  범위: -1 ~ 1 (1: 완전 동일, 0: 직교, -1: 반대)
  텍스트 검색에서 가장 많이 사용

유클리드 거리 (L2 Distance):
  d = √Σ(ai - bi)^

  낮을수록 유사 (0: 동일)

내적 (Inner Product/Dot Product):
  A · B = Σ ai × bi

  정규화된 벡터에서 코사인 유사도와 동일

차원의 저주 (Curse of Dimensionality):
  차원 증가 -> 모든 점이 "비슷한 거리"로 수렴
  고차원 벡터 검색이 어려운 이유
  -> ANN 알고리즘으로 극복
```

> 📢 **섹션 요약 비유**: 벡터 임베딩 = 의미 지도 좌표 — "고양이"와 "강아지"는 지도에서 가까운 좌표. "자동차"는 멀리. 코사인 유사도는 두 좌표가 같은 방향을 가리키는 정도!

---

## Ⅱ. ANN 알고리즘

```
ANN (Approximate Nearest Neighbor):
  정확한 최근접 이웃 대신 근사치 (99%+ 리콜)
  정확도와 속도의 트레이드오프

1. HNSW (Hierarchical Navigable Small World):
  계층적 그래프 탐색 알고리즘

  구조:
  레이어 0 (가장 조밀): 모든 노드
  레이어 1: 일부 노드 (점프 포인트)
  레이어 2+: 더 적은 노드 (고속 탐색)

  검색:
  최상위 레이어에서 시작 -> 대략적 근처
  레이어 내려가며 정밀화 -> O(log N)

  장점:
  최고 성능/리콜 균형
  동적 삽입 지원

  단점:
  메모리 사용 높음 (그래프 저장)

  사용: Pinecone, Weaviate, ChromaDB 기본

2. IVF (Inverted File Index):
  k-means 클러스터링으로 인덱스

  구조:
  n개 클러스터 -> 각 클러스터 센트로이드
  벡터를 가장 가까운 클러스터에 할당

  검색:
  쿼리 -> 가장 가까운 k개 클러스터 찾기
  해당 클러스터 내에서만 탐색

  장점: 메모리 효율적
  단점: 경계 클러스터 누락 가능

3. PQ (Product Quantization):
  벡터를 부분 공간으로 분할 후 각각 압축

  목적: 메모리 절감 (50~100배)

  768차원 float32 (3072바이트)
  -> PQ 후 96바이트 (32배 압축)

  일반적으로 HNSW 또는 IVF와 결합

4. FAISS (Facebook AI Similarity Search):
  오픈소스, C++ (Python 바인딩)
  GPU 가속 지원
  알고리즘 선택 유연: IVF, HNSW, PQ 등
```

> 📢 **섹션 요약 비유**: ANN = 도서관 검색 전략 — 모든 책(벡터) 다 보기(Exact NN: 느림) vs 주제별 분류(IVF), 가까운 서가 먼저(HNSW). 완벽하진 않지만 99% 정확도로 100배 빠름!

---

## Ⅲ. 주요 벡터 DB

```
벡터 DB 비교:

Pinecone (상용 서비스):
  Fully Managed SaaS
  API만으로 사용, 인프라 관리 불필요

  특징:
  서버리스 + Pod 기반 2가지 옵션
  메타데이터 필터링 + 벡터 검색
  멀티 테넌시, 엔터프라이즈 기능

  적합: 빠른 프로토타이핑, 관리 부담 없이

Weaviate (오픈소스 + 클라우드):
  GraphQL API + REST API
  자체 임베딩 생성 가능 (모듈 시스템)

  특징:
  멀티 벡터 (텍스트+이미지 혼합)
  자동 ML 파이프라인 통합
  K8s 배포 지원

  적합: 엔터프라이즈 자체 배포

Milvus (오픈소스, Zilliz):
  규모에 최적화 (10억+ 벡터)
  HNSW, IVF, DiskANN 지원

  특징:
  클라우드 네이티브 (K8s)
  스트리밍 데이터 지원 (Pulsar 통합)
  GPU 가속

  적합: 대규모 프로덕션

ChromaDB (오픈소스):
  경량, Python 네이티브
  인메모리 또는 영구 저장

  특징:
  LangChain, LlamaIndex 기본 통합
  로컬 개발에 최적

  적합: 개발/프로토타이핑, RAG 실험

Qdrant (오픈소스, Rust):
  Rust 구현 -> 높은 성능, 낮은 메모리
  필터링 성능 우수

  적합: 고성능 프로덕션

pgvector (PostgreSQL 확장):
  기존 PostgreSQL에 벡터 검색 추가
  SQL + 벡터 검색 통합

  적합: 기존 Postgres 환경
```

> 📢 **섹션 요약 비유**: 벡터 DB 선택 = 용도별 도구 — Pinecone(배달 음식: 빠르게 시작), Weaviate(레스토랑: 맞춤 서비스), Milvus(대형 식당: 대규모), ChromaDB(집에서 요리: 로컬 개발)!

---

## Ⅳ. RAG 아키텍처

```
RAG (Retrieval-Augmented Generation):
  LLM의 지식 한계 극복 아키텍처

  LLM 한계:
  학습 데이터 이후 지식 없음 (Knowledge Cutoff)
  특정 도메인 문서(사내 문서) 모름
  환각(Hallucination) 발생

RAG 동작 흐름:

인덱싱 단계 (Indexing):
  문서 -> 청크(Chunk) 분할 (500~2000 토큰)
  청크 -> 임베딩 모델 -> 벡터
  벡터 -> 벡터 DB 저장 + 원본 텍스트 메타데이터

검색 단계 (Retrieval):
  사용자 질의 -> 임베딩 -> 쿼리 벡터
  쿼리 벡터 -> 벡터 DB 유사도 검색 -> 상위 K개 청크

생성 단계 (Generation):
  시스템 프롬프트 + 검색된 K개 청크 + 사용자 질의
  -> LLM -> 답변

구현 예 (LangChain + ChromaDB):
  from langchain.vectorstores import Chroma
  from langchain.embeddings import OpenAIEmbeddings
  from langchain.chains import RetrievalQA
  from langchain.llms import OpenAI

  # 인덱싱
  db = Chroma.from_documents(docs, OpenAIEmbeddings())

  # RAG 체인
  qa = RetrievalQA.from_chain_type(
      llm=OpenAI(),
      retriever=db.as_retriever(search_kwargs={"k": 5})
  )

  answer = qa.run("2024년 신규 기능은?")

고급 RAG 기법:

Hybrid Search:
  BM25 (키워드) + 벡터 (의미) 결합
  -> 더 정확한 검색

Re-ranking:
  검색 결과 -> Cross-Encoder로 재순위화
  -> 정밀도 향상

HyDE (Hypothetical Document Embeddings):
  질의로 가상 답변 생성 -> 답변으로 검색
  -> 검색 정확도 향상
```

> 📢 **섹션 요약 비유**: RAG = 오픈북 시험 — LLM이 암기(학습)만으로 답하면 오류. RAG는 관련 책 페이지(검색)를 펼쳐보고 답변. 사내 문서, 최신 정보도 LLM이 활용!

---

## Ⅴ. 실무 시나리오 — 기업 지식 검색 RAG

```
대기업 사내 지식 관리 RAG 구축:

배경:
  사내 문서 50만 건 (정책, 기술 문서, FAQ)
  직원이 정보 찾는 시간: 하루 평균 2.5시간

  목표: 자연어 질의로 즉시 답변

아키텍처:

인덱싱 파이프라인:
  SharePoint + Confluence 문서 -> LangChain Loader
  청킹: RecursiveCharacterTextSplitter (512 tokens, overlap 50)
  임베딩: text-embedding-3-large (3072차원)
  저장: Weaviate (자체 배포, 50만 × 3072차원)

  총 저장량: 50만 × 3072 × 4바이트 = 6GB
  인덱스(HNSW): 추가 ~3GB

검색 API:
  쿼리 -> 임베딩 -> Weaviate ANN 검색 (top-5)
  Hybrid Search (BM25 + 벡터, α=0.5)
  Re-ranking (cross-encoder)

생성:
  GPT-4o -> 검색된 5개 청크 + 질의
  응답 + 출처 문서 링크 제공

보안:
  Weaviate에 문서 권한(ACL) 메타데이터 저장
  검색 시 사용자 권한 필터링
  (접근 불가 문서 검색 결과 제외)

결과:
  질의 응답 시간: P99 2.3초 (LLM 포함)
  정확도 (관련성): 89% (HR팀 평가)
  직원 정보 탐색 시간: 2.5시간 -> 15분 (83% 감소)

  도입 6개월:
  일 평균 질의: 3,000건
  긍정 피드백: 92%
```

> 📢 **섹션 요약 비유**: 기업 RAG = AI 사내 도서관 사서 — 50만 문서를 의미 지도(임베딩)에 배치. 질문하면 관련 문서 5개 즉시 찾아 LLM이 요약 답변. 정보 탐색 시간 83% 감소!

---

## 📌 관련 개념 맵

```
벡터 데이터베이스
+-- 핵심 기술
|   +-- 벡터 임베딩
|   +-- ANN 알고리즘 (HNSW, IVF, PQ)
|   +-- 유사도 측정 (코사인, L2)
+-- 주요 DB
|   +-- Pinecone, Weaviate, Milvus
|   +-- ChromaDB, Qdrant, pgvector
+-- 응용
|   +-- RAG (LLM 지식 보강)
|   +-- 추천 시스템
|   +-- 이미지 검색
+-- 도구
    +-- FAISS (오픈소스 ANN)
    +-- LangChain, LlamaIndex
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Word2Vec (2013)]
단어 벡터 임베딩
의미적 유사도 계산
      |
      v
[BERT / Transformer (2018)]
문맥 인식 임베딩
문장 수준 벡터
      |
      v
[Pinecone 출시 (2021)]
벡터 DB SaaS
대중화
      |
      v
[ChatGPT + RAG (2022~)]
LLM 지식 한계 극복
벡터 DB 수요 폭발
      |
      v
[현재: 멀티모달 벡터 DB]
텍스트+이미지+오디오 통합
실시간 스트리밍 인덱싱
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 벡터 임베딩 = 의미 지도 좌표 — "고양이"와 "강아지"는 지도에서 가까운 좌표. "자동차"는 멀리. 비슷한 의미 = 가까운 위치!
2. HNSW = 계층적 지름길 — 먼 곳 먼저 빠르게 이동(상위 레이어), 가까이서 정밀 탐색(하위 레이어). 99% 정확도로 100배 빠름!
3. RAG = AI 오픈북 시험 — LLM이 암기만으로 답하면 오류. 관련 문서(벡터 DB 검색)를 펼쳐보고 답변. 최신 정보도 OK!
