---
title: "Concept"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 144
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RAG는 <strong>LLM이 답변 생성 전에 외부 지식 저장소(벡터 DB)에서 관련 문서를 검색(Retrieve)하여 프롬프트에 포함</strong>시킨 후 생성(Generate)하는 기법이며, 환각(Hallucination)을 줄이고 최신 정보를 반영한다.
> 2. **가치**: LLM의 파라메트릭 지식은 <strong>학습 시점에 고정</strong>되지만, RAG는 <strong>외부 DB를 실시간 참조</strong>하여 학습 이후의 최신 정보·사내 문서·도메인 지식을 반영한다.
> 3. **판단 포인트**: Naive RAG(단순 검색)->Advanced RAG(쿼리 변환·리랭킹·청킹 최적화)->Modular RAG(파이프라인 모듈화)로 진화하며, 임베딩 모델·벡터 DB(Pinecone·Chroma)가 핵심 인프라이다.

---

## Ⅰ. 개요 및 필요성

```text
RAG 파이프라인:
  1. 문서 -> 청킹 -> 임베딩 -> 벡터 DB 저장 (오프라인)
  2. 사용자 질문 -> 임베딩 -> 벡터 DB 유사도 검색 (온라인)
  3. Top-K 문서 + 질문 -> LLM 프롬프트 -> 답변 생성
```

- **📢 섹션 요약 비유**: RAG는 <strong>오픈북 시험</strong>이다. 시험(질문) 중 교과서(문서)를 참고하여 더 정확한 답을 쓴다.

---

## Ⅱ~Ⅴ. 결론

RAG는 <strong>LLM 환각 해결·최신 지식 반영의 핵심 기법</strong>이며, 임베딩+벡터DB+리랭킹이 파이프라인의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>RAG</strong> | 검색+생성 |
| **벡터 DB** | 임베딩 저장·검색 |
| **청킹** | 문서 분할 |
| **리랭킹** | 검색 정밀도 향상 |
| <strong>환각</strong> | RAG의 핵심 해결 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
[LLM 환각 문제] -> [RAG (Lewis et al., 2020)]
    -> [LangChain/LlamaIndex (2023)]
    -> [Advanced RAG (리랭킹·HyDE, 2023)]
    -> [현재: Agentic RAG — 자율 검색·도구 호출]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RAG는 <strong>오픈북 시험</strong>이에요. 교과서(문서)를 보면서 답을 써요.
2. 교과서 없이 기억만으로 쓰면 <strong>틀릴 수 있지만(환각)</strong>, 책을 보면 정확해요.
3. AI도 <strong>검색해서 확인</strong>하고 답하면 더 정확해요!
