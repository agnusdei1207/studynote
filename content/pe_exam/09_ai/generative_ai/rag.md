+++
title = "RAG (검색 증강 생성)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# RAG (Retrieval-Augmented Generation, 검색 증강 생성)

## 핵심 인사이트 (3줄 요약)
> **RAG**는 LLM의 지식 부족·환각 문제를 외부 지식 검색으로 보완하는 아키텍처. 사용자 쿼리와 관련된 문서를 벡터DB에서 유사도 검색 후 LLM의 컨텍스트에 주입하여 근거 기반 답변을 생성한다. 2024~2025년 기업 AI 도입의 핵심 패턴으로, **GraphRAG·Agentic RAG** 등으로 진화 중이다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: RAG는 정보 검색(Retrieval)과 언어 생성(Generation)을 결합한 하이브리드 AI 아키텍처로, LLM이 훈련 데이터 외의 최신·도메인 지식을 활용할 수 있게 한다.

> 비유: "오픈북 시험 — 교과서(벡터DB)에서 관련 내용을 먼저 찾아보고 답안을 작성한다"

**등장 배경**:
- LLM 한계: 학습 시점 이후 정보 반영 불가 (Knowledge Cutoff)
- 환각(Hallucination): 모르면 그럴듯하게 거짓 생성
- 도메인 특화 비용: 전체 Fine-tuning은 수억 달러 비용
- Meta FAIR 논문(2020, RAG): 검색+생성 결합으로 지식 기반 QA 획기적 향상

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소**:
| 구성 요소 | 역할 | 예시 |
|----------|------|------|
| Document Loader | 문서 수집·파싱 | PDF, HTML, DB, API |
| Text Splitter | 문서를 청크로 분할 | Recursive/Semantic Split |
| Embedding Model | 텍스트 → 벡터 변환 | BGE, OpenAI-ada-002, E5 |
| Vector Database | 벡터 저장·유사도 검색 | Chroma, Weaviate, Pinecone |
| Retriever | 쿼리와 관련 문서 검색 | Dense/Sparse/Hybrid |
| LLM Generator | 검색 결과 + 쿼리 → 답변 | GPT-4o, Claude, LLaMA |
| Reranker | 검색 결과 재순위화 | Cohere Rerank, BGE-reranker |

**핵심 원리** (RAG 파이프라인):
```
[인덱싱 단계] (오프라인)
문서 → Chunking → Embedding → Vector DB 저장

[추론 단계] (실시간)
쿼리 → Embedding → Vector DB 유사도 검색 → Top-K 청크 추출
     → Prompt = [시스템 지시] + [검색 문서] + [사용자 쿼리]
     → LLM → 근거 기반 답변

유사도 계산 (코사인 유사도):
similarity = cos(q, d) = (q·d) / (|q|·|d|)
```

**코드 예시** (LangChain 기반 RAG):
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader

# 1. 문서 로딩 및 분할
loader = PyPDFLoader("기술사_교재.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 2. 임베딩 + 벡터 DB 저장
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. RAG 체인 구성
llm = ChatOpenAI(model="gpt-4o", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# 4. 질의응답
result = qa_chain.invoke("LLM의 Hallucination 해결 방법은?")
print(result["result"])
print("\n출처:", [doc.metadata for doc in result["source_documents"]])
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + RAG 종류 비교

**장단점**:
| 장점 | 단점 |
|-----|------|
| 최신 정보 반영 가능 | 파이프라인 구성 복잡 |
| 환각 감소 (출처 명시) | 검색 품질에 성능 의존 |
| Fine-tuning 없이 도메인 특화 | 레이턴시 증가 (검색 시간 추가) |
| 지식 업데이트 용이 | Chunking 전략에 민감 |
| 비용 효율적 (전체 재학습 불필요) | 검색 실패 시 오히려 오답 가중 |

**RAG 유형 비교**:
| 유형 | 특징 | 적합한 상황 |
|------|------|----------|
| Naive RAG | 단순 유사도 검색 → 생성 | 빠른 프로토타입 |
| Advanced RAG | 쿼리 재작성 + Reranking | 정확도 중시 |
| Modular RAG | 선택적 검색, 파이프라인 조합 | 복잡한 워크플로우 |
| GraphRAG (Microsoft) | 지식 그래프 + RAG | 복잡한 관계 추론 |
| Agentic RAG | Agent가 자율 검색 결정 | 다단계 추론 |
| Corrective RAG (CRAG) | 검색 결과 자동 검증·수정 | 고신뢰 환경 |
| HyDE | 가상 문서로 쿼리 확장 | 짧은 쿼리 검색 향상 |

> **선택 기준**: 빠른 구축 → Naive RAG; 정확도 → Advanced+Reranker; 복잡한 지식 → GraphRAG

---

### Ⅳ. 실무 적용 방안  ↔  기술사적 판단 + 활용 + 주의사항

**기술사적 판단** (기업별 적용):
| 적용 시나리오 | 아키텍처 | 기대 효과 |
|------------|--------|--------|
| 사내 Q&A 시스템 | RAG + Confluence/Notion 연동 | 정보 검색 시간 70% 절감 |
| 법률/규정 검색 | Hybrid Search + Reranker | 정확도 90%+ |
| 고객 지원 | RAG + 제품 매뉴얼 | CS 처리 시간 50% 단축 |
| 의료 정보 검색 | RAG + 의료 DB | 진단 보조 정확도 향상 |
| 코드 문서화 Q&A | RAG + GitHub/코드베이스 | 온보딩 시간 40% 단축 |

**RAG 최적화 전략**:
```
1. Chunking 전략
   - Recursive: 단락 → 문장 순으로 계층 분할
   - Semantic: 의미 단위로 분할 (더 정확)
   - Parent-Child: 검색은 작은 청크, 컨텍스트는 큰 청크

2. Embedding 선택
   - 한국어: KLUE-RoBERTa, BGE-M3
   - 영어: OpenAI ada-002, E5-large
   - 멀티링구얼: mE5, BGE-M3

3. Retrieval 전략
   - Dense: 의미 기반 (ANN 검색)
   - Sparse: 키워드 기반 (BM25)
   - Hybrid: Dense + Sparse 결합 (최고 성능)
```

**주의사항 / 흔한 실수**:
- **청크 크기 부적절**: 너무 작으면 문맥 손실 / 너무 크면 노이즈 증가 → 512~1024 토큰 권장
- **검색 개수 남용**: k=20 이상이면 LLM 컨텍스트 낭비 → 적절한 Reranking 필수
- **임베딩 모델-생성 모델 불일치**: 인덱싱/검색 시 동일 임베딩 모델 사용 필수

**관련 개념**: 벡터 DB, 임베딩, Pinecone/Chroma/Weaviate, Semantic Search, LangChain, LlamaIndex

---

### Ⅴ. 기대 효과 및 결론  ↔  미래 전망

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 환각 감소 | 검색 기반 근거 생성 | 오류율 40~60% 감소 |
| 최신성 | 실시간 문서 업데이트 | 지식 갱신 비용 90% 절감 |
| 도메인 특화 | Fine-tuning 없이 가능 | 구축 비용 80% 절감 |

> **결론**: RAG는 "LLM의 기억력 한계를 외부 저장소로 극복"하는 실용적 아키텍처. GraphRAG·Agentic RAG로 진화하며, 기업 AI의 표준 패턴으로 자리 잡았다. 기술사는 벡터DB 선택·청킹 전략·하이브리드 검색·Reranker 설계를 핵심 역량으로 갖춰야 한다.  
> **※ 참고**: RAG 원논문(Lewis et al., 2020 Meta), Microsoft GraphRAG(2024), LangChain/LlamaIndex 공식 문서

---

## 어린이를 위한 종합 설명

**RAG는 "오픈북 시험을 허락한 AI"야!**

일반 LLM (닫힌 책 시험):
```
AI가 배운 지식으로만 답해야 해
→ 모르면 지어내거나 틀린 답을 해 (환각!)
```

RAG (오픈북 시험):
```
1. 시험 보기 전에 먼저 교과서에서 관련 내용 찾기 (검색!)
2. 찾은 내용을 보면서 답 작성 (근거 기반!)
3. "여기 교과서 125쪽 참고했어요!" (출처 명시!)
```

실제 작동 방식:
```
질문: "2024년 노벨 물리학상 수상자는?"

RAG 없이: AI가 모름 → 지어냄 (틀릴 수 있음!)

RAG 있이:
1. 벡터DB에서 "노벨 물리학상 2024" 검색
2. 관련 기사 발견: "힌튼·홉필드 수상"
3. AI: "2024년 노벨 물리학상은 제프리 힌튼과 존 홉필드입니다" (정확!)
```

> RAG = AI에게 "자료실 이용 허락"을 주는 것! 그러면 훨씬 정확해진다 📚🔍

---
