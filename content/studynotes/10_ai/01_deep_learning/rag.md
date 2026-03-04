+++
title = "RAG (Retrieval-Augmented Generation)"
description = "거대 언어 모델의 환각 현상을 극복하고 최신 지식 기반의 정확한 답변을 생성하는 검색 증강 생성 기술의 심층 아키텍처와 실무 적용 방안"
date = 2024-05-24
[taxonomies]
tags = ["AI", "Deep Learning", "LLM", "RAG", "Vector DB"]
+++

# RAG (Retrieval-Augmented Generation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RAG는 거대 언어 모델(LLM)의 내재적 지식 한계를 외부 데이터베이스의 실시간 검색 결과로 보완하여, 맥락을 이해한 고도로 정확한 답변을 생성하는 하이브리드(검색+생성) 아키텍처입니다.
> 2. **가치**: 모델의 재학습(Fine-tuning) 없이도 최신 도메인 특화 지식을 반영할 수 있어, 환각(Hallucination)을 최대 80% 이상 감소시키고, 시스템 유지보수 비용을 획기적으로 절감합니다.
> 3. **융합**: 벡터 데이터베이스(Vector DB), 시맨틱 검색(Semantic Search), 임베딩(Embedding) 모델, 그리고 랭체인(LangChain)과 같은 오케스트레이션 프레임워크와 결합하여 엔터프라이즈 AI의 핵심 표준으로 자리잡고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

RAG(Retrieval-Augmented Generation, 검색 증강 생성)는 사전에 학습된 거대 언어 모델(LLM)이 답변을 생성하기 전에, 신뢰할 수 있는 외부 지식 베이스(Knowledge Base)에서 사용자의 질의와 의미적으로 가장 연관성이 높은 정보(문서, 단락 등)를 검색(Retrieval)하여 가져온 뒤, 이를 프롬프트에 맥락(Context)으로 주입하여 모델이 보다 정확하고 풍부한 근거를 바탕으로 답변을 생성(Generation)하도록 유도하는 최첨단 인공지능 파이프라인 기술입니다. 단순한 키워드 매칭을 넘어서서 벡터 공간에서의 의미적 유사도를 바탕으로 문맥을 파악하며, 기업의 폐쇄적인 데이터나 최신 트렌드를 실시간으로 반영할 수 있는 가장 현실적이고 효율적인 방법론입니다.

**💡 비유: 오픈북 시험을 치르는 천재 학자**
LLM을 '모든 분야의 기본 지식을 갖추고 글을 매우 잘 쓰는 천재 학자'라고 가정해 봅시다. 하지만 이 학자는 최근 1년간의 새로운 뉴스나 특정 회사의 내부 기밀문서에 대해서는 전혀 알지 못합니다(Knowledge Cutoff). 만약 이 학자에게 폐쇄형 시험(Closed-book Exam)을 보게 한다면, 모르는 문제에 대해 그럴싸한 거짓말(환각 현상)을 지어낼 확률이 높습니다. RAG는 이 천재 학자에게 '관련된 최신 서적과 문서가 가득한 도서관'과 '뛰어난 사서(Retriever)'를 제공하여 **오픈북 시험(Open-book Exam)**을 치르게 하는 것과 같습니다. 사서가 질문과 관련된 가장 정확한 페이지들을 찾아다 주면, 학자는 그 자료들을 읽고 자신의 뛰어난 문장력을 발휘해 완벽한 답안을 작성하는 원리입니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: LLM은 학습 시점의 데이터로 지식이 동결(Knowledge Cutoff)되어 최신 정보를 알 수 없고, 모르는 정보를 질문받았을 때 사실인 것처럼 허위 정보를 생성하는 **환각(Hallucination)** 현상이 발생합니다. 또한 기업의 민감한 내부 데이터를 모델에 학습시키는 것은 보안상 위험하며, 도메인 특화 지식을 주입하기 위한 미세 조정(Fine-tuning)은 엄청난 GPU 컴퓨팅 자원과 데이터 전처리 비용을 요구합니다.
2. **혁신적 패러다임의 변화**: 2020년 메타(Meta, 구 Facebook) AI 연구진이 발표한 논문 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"에서 처음 제안된 RAG는 모델 내부의 매개변수(Parametric Memory)에만 의존하던 기존의 패러다임을 깨고, 외부 지식(Non-parametric Memory)을 동적으로 결합하는 혁신을 이루었습니다. 이는 모델의 크기를 키우지 않고도 지식의 확장성을 무한대로 늘릴 수 있는 돌파구가 되었습니다.
3. **비즈니스적 요구사항**: 현재 수많은 엔터프라이즈 환경에서는 LLM을 고객 지원 챗봇, 사내 문서 검색, 법률/의료 자문 등에 활용하고자 합니다. 이때 "절대적으로 정확하고 근거가 명확한 답변"이 요구되며, 정보의 출처(Citation)를 투명하게 제공해야만 비즈니스 리스크를 피할 수 있으므로 RAG 도입이 필수 불가결한 표준 아키텍처로 자리매김하였습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

RAG 아키텍처는 크게 **데이터 준비 및 색인(Indexing) 파이프라인**과 **실시간 검색 및 생성(Query & Generation) 파이프라인**으로 나뉩니다.

#### 주요 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|---|---|---|---|---|
| **Document Loader / Splitter** | 다양한 포맷의 문서를 읽고 의미 단위를 보존하며 청크(Chunk)로 분할 | PDF, HTML, DB 데이터를 텍스트로 추출 후, Token 단위나 문장 단위(Recursive Character Text Splitting)로 분리하고 Overlap을 주어 맥락 손실 방지 | LangChain, LlamaIndex, Unstructured.io | 두꺼운 전공 서적을 요약 카드 사이즈로 자르기 |
| **Embedding Model** | 텍스트 청크를 고차원 밀집 벡터(Dense Vector)로 변환 | 텍스트의 의미적 특성을 포착하여 실수 배열(예: 768차원, 1536차원)로 사상. 거리가 가까울수록 의미가 유사함 | OpenAI `text-embedding-ada-002`, BERT, HuggingFace BGE | 문장의 의미를 좌표 평면상의 정확한 위치(위도/경도)로 번역하기 |
| **Vector Database** | 생성된 임베딩 벡터와 원본 텍스트 메타데이터를 저장하고 초고속 유사도 검색 수행 | HNSW(Hierarchical Navigable Small World) 알고리즘이나 IVF, PQ 등의 인덱싱을 통해 역색인이 아닌 벡터 간의 공간적 근접성을 계산하여 ANN(Approximate Nearest Neighbor) 검색 수행 | Pinecone, Milvus, Chroma, FAISS, pgvector | 수백만 개의 카드 중 특정 카드와 가장 색깔/패턴이 비슷한 카드를 0.1초 만에 찾는 특수 서랍장 |
| **Retriever** | 사용자 질의에 대해 가장 적합한 문서를 Vector DB에서 추출 | 사용자의 쿼리 역시 임베딩 모델을 거쳐 벡터로 변환된 후, Cosine Similarity나 L2 거리 계산을 통해 가장 유사도가 높은 Top-K 개의 청크를 반환 | Dense Search, Keyword Search(BM25), Hybrid Search, Re-ranking(Cohere) | 도서관의 유능한 검색 사서 |
| **Generator (LLM)** | 검색된 컨텍스트를 바탕으로 최종 답변을 합성 및 생성 | `[System Prompt] + [Retrieved Context 1..K] + [User Query]` 형태로 결합된 프롬프트를 토큰 단위로 처리하여, Next Token Prediction 방식으로 맥락에 맞는 일관된 자연어 답변 생성 | GPT-4, Claude 3, Llama 3 | 자료를 읽고 최종 보고서를 작성하는 분석가 |

#### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                                 [ RAG SYSTEM ARCHITECTURE ]
========================================================================================================

  [ PHASE 1: Data Ingestion & Indexing Pipeline (Offline/Asynchronous) ]

  +-------------+    +---------------+    +-------------------+    +----------------+    +-------------+
  | Raw Data    |    | Text Splitter |    | Embedding Model   |    | Vector Index   |    | Vector DB   |
  | (PDF, DB,   |===>| (Chunking w/  |===>| (e.g., text-emb-  |===>| (HNSW / IVF)   |===>| (Milvus,    |
  |  Intranet)  |    |  overlap)     |    |  ada-002)         |    | + Metadata     |    |  Chroma)    |
  +-------------+    +---------------+    +-------------------+    +----------------+    +-------------+
                                                 |                         ^
                                                 v                         |
                                          [Dense Vector: [0.12, -0.05, 0.88, ... 1536 dim]]

========================================================================================================

  [ PHASE 2: Query & Generation Pipeline (Online/Real-time) ]

  +-------------+    +-------------------+    +----------------------------------+
  | User Query  |===>| Embedding Model   |===>| Vector Database (ANN Search)     |
  | "사내 휴가  |    | (Same as Indexing)|    | (Cosine Similarity Calculation)  |
  |  규정이 뭐지?"|    +-------------------+    +----------------------------------+
  +-------------+                                              |
        |                                                      | Returns Top-K (e.g., K=3)
        |                                                      v
        |                                     +----------------------------------+
        |                                     | Retrieved Contexts               |
        |                                     | 1. "정규직 연차는 15일..."       |
        |                                     | 2. "경조사 휴가는 5일..."        |
        +------------------------------------>| 3. "반차 사용 시 주의사항..."      |
                 (Original Query)             +----------------------------------+
                                                               |
                                                               v
  +----------------------------------------------------------------------------------------------------+
  | Prompt Construction (Orchestrator e.g., LangChain)                                                 |
  | Prompt: "You are a helpful assistant. Answer the question ONLY based on the provided context.      |
  |          Context: {Retrieved Contexts}                                                             |
  |          Question: {User Query}"                                                                   |
  +----------------------------------------------------------------------------------------------------+
                                                               |
                                                               v
                                                      +-----------------+
                                                      | Generator (LLM) | (GPT-4 / Claude)
                                                      | (Inference)     |
                                                      +-----------------+
                                                               |
                                                               v
                                                    +---------------------+
                                                    | Final Response      |
                                                    | "사내 규정에 따르면,|
                                                    | 정규직의 기본 연차는|
                                                    | 15일이며..."        |
                                                    +---------------------+
```

#### 심층 동작 원리 및 알고리즘
RAG의 성능은 **"문서를 어떻게 벡터 공간에 잘 배치하고, 질의 벡터와 얼마나 빠르고 정확하게 매칭시키는가"**에 달려있습니다.

**1. 임베딩과 코사인 유사도 (Cosine Similarity)**
문서 청크 $D_i$와 질의 $Q$는 임베딩 모델 $f(x)$를 통해 고차원 벡터 $\vec{d}_i$와 $\vec{q}$로 변환됩니다. 검색기(Retriever)는 두 벡터 사이의 각도를 기반으로 유사도를 계산합니다.
$$ \text{Similarity}(\vec{q}, \vec{d}_i) = \cos(\theta) = \frac{\vec{q} \cdot \vec{d}_i}{\|\vec{q}\| \|\vec{d}_i\|} = \frac{\sum_{j=1}^{n} q_j d_{ij}}{\sqrt{\sum_{j=1}^{n} q_j^2} \sqrt{\sum_{j=1}^{n} d_{ij}^2}} $$
코사인 유사도는 1에 가까울수록 두 텍스트의 의미가 동일함을 나타냅니다. 

**2. HNSW (Hierarchical Navigable Small World) 알고리즘**
수천만 개의 청크 벡터와 질의 벡터를 일일이 비교(Exhaustive Search, O(N))하는 것은 실시간 응답에 부적합합니다. 최신 Vector DB는 HNSW 알고리즘을 사용하여 $O(\log N)$ 수준의 Approximate Nearest Neighbor(ANN) 검색을 수행합니다. 
HNSW는 여러 개의 층(Layer)으로 구성된 그래프 구조를 만듭니다. 최상위 층에는 소수의 노드(벡터)만 존재하고, 아래 층으로 갈수록 노드가 촘촘해집니다. 검색 시 최상위 층의 진입점(Entry Point)에서 시작해 질의 벡터와 가장 가까운 노드를 탐욕적으로(Greedy) 찾으며 점차 아래 층으로 파고들어 최종적으로 가장 인접한 노드를 고속으로 도출합니다.

**실무 수준의 구현 코드 (Python, LangChain & ChromaDB 기반)**
다음 코드는 PDF 문서를 로드하여 청킹하고, Vector DB에 인덱싱한 뒤, 질의를 통해 답변을 생성하는 완성된 파이프라인입니다.

```python
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 문서 로드 및 청킹 (Data Ingestion)
loader = PyPDFLoader("enterprise_policy.pdf")
docs = loader.load()

# 맥락 유지 최적화를 위한 Recursive Split (Overlap 설정 중요)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " "]
)
splits = text_splitter.split_documents(docs)

# 2. 임베딩 생성 및 Vector DB(Chroma)에 적재
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")

# 3. Retriever 설정 (Top-K=4 설정 및 유사도 점수 임계값 반영 가능)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# 4. 프롬프트 템플릿 정의 (환각 억제를 위한 System Prompt 최적화)
template = """
당신은 사내 규정 안내 AI 어시스턴트입니다.
반드시 아래 제공된 Context만을 기반으로 질문에 답변하세요.
Context에 없는 내용은 "알 수 없습니다"라고 답변해야 합니다.

Context:
{context}

Question: {question}

Answer:
"""
custom_prompt = PromptTemplate.from_template(template)

# 5. LLM 초기화 및 LCEL(LangChain Expression Language) 체인 구성
llm = ChatOpenAI(model_name="gpt-4o", temperature=0) # temperature 0으로 설정하여 결정론적이고 사실적인 답변 유도

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | custom_prompt
    | llm
    | StrOutputParser()
)

# 6. 사용자 질의 실행
query = "육아휴직은 최대 몇 개월까지 사용 가능한가요?"
response = rag_chain.invoke(query)
print(response)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: RAG vs Fine-tuning vs Prompt Engineering
지식 업데이트와 도메인 적응을 위한 3대 전략을 정량적/구조적 관점에서 비교합니다.

| 평가 지표 | Prompt Engineering (Few-shot) | Fine-tuning (미세 조정) | RAG (검색 증강 생성) |
|---|---|---|---|
| **지식 주입 방식** | 프롬프트에 정적 예시 주입 | 모델의 파라미터(가중치) 자체를 업데이트 | 외부 DB에서 동적으로 문맥 검색 후 프롬프트 주입 |
| **최신 정보 반영** | 불가능 (수동 프롬프트 수정 필요) | 극히 어려움 (주기적 재학습 필요, 비용 폭발) | **매우 용이 (Vector DB에 문서 추가/수정/삭제만 하면 즉시 반영)** |
| **환각(Hallucination)** | 높음 (본질적 해결 불가) | 중간 (여전히 파라미터 의존으로 허위 사실 생성 가능) | **매우 낮음 (검색된 Ground Truth에 기반하여 답변 강제)** |
| **비용 모델 (컴퓨팅)** | 매우 낮음 | 초기 학습 비용 매우 높음 (GPU 클러스터 필요) | 초기 인덱싱 비용 중간 + 건당 임베딩 및 검색 인프라 유지비 |
| **데이터 보안/통제력** | 낮음 (컨텍스트 윈도우 한계) | 낮음 (모델에 지식이 녹아들어 부분 삭제/권한 제어 불가) | **매우 높음 (DB 단에서 RBAC 적용, 사용자 권한별 검색 제한 가능)** |
| **구현 난이도/RTO** | 매우 쉬움 | 어려움 (하이퍼파라미터 튜닝, 데이터 정제, 평가 지표 설정) | 중간 (검색 품질 최적화(Retriever 튜닝)가 관건) |

#### 과목 융합 관점 분석
- **[RAG + DB (데이터베이스)]**: RAG의 성능은 벡터 데이터베이스의 인덱싱 구조에 크게 의존합니다. B-Tree 인덱스가 정확한 값 매칭(Exact Match)에 유리하다면, RAG는 고차원 벡터의 ANN 검색을 위해 HNSW, PQ(Product Quantization), LSH(Locality Sensitive Hashing) 등과 융합됩니다. 최근에는 RDBMS(PostgreSQL의 pgvector)가 벡터 타입과 거리 연산자를 네이티브로 지원하여, 메타데이터 필터링(SQL)과 벡터 유사도 검색을 동시에 수행하는 **하이브리드 검색 아키텍처**로 진화하고 있습니다.
- **[RAG + AI/보안]**: RAG 파이프라인은 프롬프트 인젝션(Prompt Injection) 및 데이터 오염(Data Poisoning) 공격에 취약할 수 있습니다. 악의적인 문서가 Vector DB에 적재될 경우, Retriever가 이를 추출하여 LLM에 전달하면 시스템이 해커의 의도대로 동작할 수 있습니다. 따라서 제로 트러스트(Zero Trust) 관점에서 데이터 수집 단계의 무결성 검증, 쿼리 및 결과물에 대한 실시간 유해성 필터링(NVIDIA NeMo Guardrails 등) 메커니즘이 강제되어야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

현업에서 RAG 시스템을 도입할 때 아키텍트와 기술사는 시스템의 신뢰성과 응답 지연 시간(Latency) 간의 트레이드오프를 철저히 관리해야 합니다.

#### 기술사적 판단 (실무 시나리오)
- **시나리오 1: 문서의 길이가 매우 길고 맥락이 분산되어 있는 경우 (예: 법률 판례 분석)**
  - **문제**: 단순 Chunking(예: 500 토큰 단위)을 하면 법률 문서의 조항과 단서 조항이 분리되어, Retrieval 시 핵심 문맥이 유실(Context Loss)되는 현상이 발생합니다.
  - **전략적 의사결정**: **Parent Document Retriever (또는 Auto-merging Retriever)** 전략을 도입합니다. 문서를 작은 청크(Child)로 잘라 Vector DB에 저장하여 검색의 정밀도는 높이되, 실제 LLM에 전달할 때는 해당 청크가 속한 큰 덩어리의 원본 문서(Parent)를 통째로 제공하여 모델이 전체 맥락을 잃지 않도록 구성합니다.
- **시나리오 2: "2023년 매출액과 2024년 매출액을 비교해줘"와 같은 분석적 질의**
  - **문제**: 일반적인 Dense Vector 검색은 의미적 유사성만 찾으므로, 특정 숫자나 연도, 고유명사에 대한 정확도(Exact Match)가 떨어집니다.
  - **전략적 의사결정**: **Hybrid Search (Dense + Sparse Search) 및 앙상블 검색**을 도입합니다. 의미 검색은 Embedding(Dense)으로 처리하고, 키워드 검색은 TF-IDF 기반의 BM25(Sparse) 알고리즘으로 병행 수행한 뒤, RRF(Reciprocal Rank Fusion) 알고리즘을 통해 두 결과를 결합하고, Re-ranker(Cross-Encoder) 모델을 통해 최종 순위를 재조정하여 숫자와 고유명사의 정확도를 극대화합니다.
- **시나리오 3: 응답 지연 시간(Latency) 요구사항이 엄격한 대국민 서비스**
  - **문제**: Embedding -> Vector DB 검색 -> LLM Generation의 3단계 파이프라인을 거치면서 TTFT(Time To First Token)가 3~5초 이상 지연될 수 있습니다.
  - **전략적 의사결정**: **Semantic Cache (시맨틱 캐싱)** 레이어를 도입합니다. 사용자의 쿼리를 캐싱하여, 완전히 동일하지 않더라도 의미적으로 매우 유사한 쿼리(예: "비밀번호 어떻게 바꿔요?" vs "비번 변경 방법")가 인입되면 LLM을 거치지 않고 캐시된 답변을 즉시 반환(Redis Vector 등 활용)하여 Latency를 100ms 이하로 단축하고 API 호출 비용을 절감합니다.

#### 주의사항 및 안티패턴 (Anti-patterns)
- **Lost in the Middle 현상**: LLM은 프롬프트의 맨 앞과 맨 끝에 있는 정보는 잘 기억하지만, 중간에 위치한 정보는 간과하는 경향이 있습니다. 너무 많은 문서를 Retrieved Context로 주입하면 오히려 답변 품질이 하락합니다. 반드시 Re-ranker를 통해 가장 중요한 문서를 프롬프트의 양 끝(처음과 마지막)에 배치하거나, 주입하는 Context의 개수를 모델의 역량에 맞게 제한해야 합니다.
- **Blind Retrieval (눈먼 검색)**: 사용자의 질문 의도를 파악하지 않고 그대로 Vector DB에 던지는 안티패턴입니다. "그것에 대해 더 자세히 알려줘" 같은 후속 질문은 이전 문맥 없이는 검색이 불가능합니다. 반드시 질의를 재작성(Query Rewriting / Standalone Question Generation)하는 사전 처리 단계를 거쳐야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 정량적/정성적 기대효과
| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 블랙박스인 LLM 답변에 대한 투명성 및 출처(Citation) 검증 가능 확보<br>- 데이터 보안 유지 및 내부 기밀 유출 방지 (프라이빗 인프라 내 DB 유지) |
| **정량적 효과** | - 환각(Hallucination) 발생률 기존 대비 **80% 이상 감소** (업계 평균)<br>- Fine-tuning 대비 시스템 유지보수(재학습) 비용 **90% 이상 절감**<br>- 지식 업데이트 주기 단축 (수일/수주 -> 실시간(0초)) |

#### 미래 전망 및 진화 방향
- **GraphRAG (지식 그래프 결합)**: 현재의 Vector 기반 RAG는 단일 문서 파편을 찾는 데는 유리하지만, 여러 문서에 걸친 복잡한 관계망을 추론하는 데는 약합니다. 향후에는 노드와 엣지로 이루어진 Knowledge Graph와 LLM을 결합한 **GraphRAG**가 대세가 되어, "A와 B의 관계를 설명하고 C에 미치는 영향을 분석하라"는 복합 추론 질의를 완벽히 소화할 것입니다.
- **Multi-modal RAG**: 텍스트를 넘어 이미지, 도표, 비디오, 오디오 데이터까지 임베딩하여, "첨부한 차트 이미지의 하락 추세와 유사한 과거 보고서를 찾아 원인을 분석해달라"는 수준의 다중 양식 검색 증강 생성이 상용화될 것입니다.
- **Agentic RAG**: 정적인 파이프라인을 넘어, AI 에이전트가 스스로 "현재 검색된 정보가 부족하므로, 외부 웹 검색 API를 추가로 호출하고, 사내 SQL DB를 쿼리하여 결과를 조합하겠다"고 판단하는 자율형 RAG 루프 체계로 진화 중입니다.

**※ 참고 표준/가이드**: 
- RAG 시스템 구축 시 AI 시스템의 신뢰성과 투명성을 규정한 **ISO/IEC 42001 (인공지능 경영시스템)** 인증 요건을 준수해야 하며, 개인정보가 포함된 문서를 색인할 경우 국내 **ISMS-P** 및 유럽 **GDPR**의 데이터 파기/가명처리 기준을 벡터 데이터베이스 스키마 설계 단계부터 엄격히 반영해야 합니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- `[Vector Database](@/studynotes/10_ai/01_deep_learning/_index.md)`: RAG의 기억 저장소 역할을 하며 고차원 벡터의 근사 최근접 이웃(ANN) 검색을 수행하는 핵심 인프라.
- `[Embedding](@/studynotes/10_ai/01_deep_learning/_index.md)`: 자연어를 컴퓨터가 유사도를 계산할 수 있는 실수 벡터 좌표계로 변환하는 선형 대수적 매핑 기술.
- `[LLM Hallucination](@/studynotes/10_ai/01_deep_learning/_index.md)`: LLM이 그럴싸한 거짓말을 지어내는 현상으로, RAG가 극복하고자 하는 가장 핵심적인 Pain Point.
- `[Fine-Tuning](@/studynotes/10_ai/01_deep_learning/_index.md)`: 모델의 가중치를 직접 수정하는 기법으로, RAG와 상호 보완적으로(RAG는 지식 주입, Fine-Tuning은 어조/도메인 지시어 학습) 사용됨.
- `[LangChain / LlamaIndex](@/studynotes/10_ai/01_deep_learning/_index.md)`: RAG의 복잡한 파이프라인(Loader, Splitter, Retriever, Prompting)을 쉽게 구성하도록 돕는 오케스트레이션 프레임워크.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **RAG가 뭔가요?**: 모든 걸 외우고 있지 않은 똑똑한 AI에게, 시험을 볼 때 **최신 백과사전과 관련된 책들을 마음껏 찾아볼 수 있게 해주는 '오픈북 시험' 규칙**이에요.
2. **어떻게 작동하나요?**: 내가 질문을 하면, 아주 빠른 사서(Retriever)가 도서관(Vector DB)으로 달려가서 정답이 있을 만한 페이지를 3장 정도 뽑아와요. 그럼 AI가 그 페이지를 꼼꼼히 읽고 나에게 아주 정확한 답을 말해준답니다.
3. **왜 좋은가요?**: AI가 모르는 걸 아는 척하며 거짓말(환각)을 하는 나쁜 버릇을 싹 고쳐주고, 세상이 바뀌어서 새로운 소식이 생겨도 책만 새것으로 갈아 끼워주면 바로바로 똑똑한 대답을 할 수 있어서 엄청 돈과 시간이 절약돼요!
