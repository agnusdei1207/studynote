---
title: "GPT Large Language Model Pre-training"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 642
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPT 사전학습은 대규모 텍스트에서 다음 토큰 예측 목표를 학습하여 언어 패턴, 지식, 추론 단서를 하나의 decoder-only 트랜스포머에 압축하는 과정이다.
> 2. **가치**: 별도 과업별 모델을 매번 만들지 않아도 프롬프트, 파인튜닝, RAG를 통해 다양한 업무에 재사용할 수 있는 범용 기반 모델을 만든다.
> 3. **판단 포인트**: 모델 크기보다 데이터 품질, 중복 제거, 안전 필터링, 학습 안정성, 평가 체계가 더 중요하다.

---

## I. 개요 및 필요성

GPT 계열 모델은 decoder-only 트랜스포머를 사용하여 이전 토큰들을 조건으로 다음 토큰을 예측한다. 이 단순한 목표는 대규모 데이터와 모델 용량이 결합될 때 번역, 요약, 질의응답, 코드 생성 같은 다양한 능력으로 확장된다.

사전학습은 서비스 개발의 끝이 아니라 시작점이다. 실제 서비스에서는 지시 튜닝, 선호 최적화, 안전성 평가, RAG, 도메인 파인튜닝이 뒤따른다. 따라서 사전학습을 이해할 때는 학습 데이터 파이프라인과 평가 체계를 함께 봐야 한다.

```text
[GPT Pre-training Pipeline]

Raw Data -> Filter -> Deduplicate -> Tokenize -> Train
    |          |            |            |          |
    v          v            v            v          v
license    quality      near-dup      BPE/SPM    next-token
safety     language     removal       vocab      prediction
```

---

## II. 아키텍처 및 핵심 원리

| 단계 | 핵심 작업 | 주요 리스크 |
| :--- | :--- | :--- |
| 데이터 수집 | 웹, 코드, 문서, 대화 데이터 확보 | 저작권, 개인정보, 유해 콘텐츠 |
| 정제/필터링 | 품질 점수, 언어 판별, 중복 제거 | 편향, 과도한 필터링 |
| 토큰화 | BPE, SentencePiece 등 사용 | 희귀어/한국어 처리 품질 |
| 분산 학습 | 데이터/텐서/파이프라인 병렬 | 통신 병목, 학습 불안정 |
| 체크포인트 | 중간 저장과 재시작 | 저장소 비용, 복구 시간 |
| 평가 | perplexity, benchmark, safety eval | 벤치마크 과적합 |

학습 목표는 다음과 같다.

```text
maximize P(x_t | x_1, x_2, ..., x_{t-1})
loss = cross entropy(predicted token distribution, actual token)
```

Causal mask는 미래 토큰을 보지 못하게 막는다. 이 제약 덕분에 모델은 실제 생성 시점과 같은 조건에서 학습된다.

---

## III. 비교 및 연결

| 구분 | GPT | BERT | T5 |
| :--- | :--- | :--- | :--- |
| 구조 | Decoder-only | Encoder-only | Encoder-Decoder |
| 학습 목표 | 다음 토큰 예측 | 마스크 토큰 복원 | text-to-text 변환 |
| 강점 | 생성, 대화, 코드 | 이해, 분류, 검색 | 변환 과업 |
| 추론 방식 | autoregressive | 전체 입력 인코딩 | 입력 인코딩 후 생성 |

GPT는 생성형 서비스에 강하지만 환각, 프롬프트 인젝션, 개인정보 재현 가능성 같은 위험을 갖는다. RAG는 최신성/출처 문제를 보완하고, 파인튜닝은 도메인 스타일과 절차 준수를 보완한다.

---

## IV. 실무 적용 및 실무자 판단

### 판단 체크리스트

- 학습 데이터의 출처, 라이선스, 삭제 요청 대응 체계가 있는가?
- 한국어/도메인 데이터 비율이 목표 서비스와 맞는가?
- 중복 데이터와 벤치마크 오염을 제거했는가?
- 학습 중 loss spike, gradient overflow, checkpoint corruption 대응이 준비되어 있는가?
- 사전학습 후 instruction tuning, safety tuning, red teaming 계획이 있는가?

### 피해야 할 안티패턴

- 데이터 품질 검증 없이 양만 늘리는 경우
- 공개 벤치마크 점수만 보고 실제 업무 품질을 판단하는 경우
- 모델 학습과 배포 비용을 분리해 총소유비용을 보지 않는 경우

---

## V. 기대효과 및 결론

GPT 사전학습은 언어 모델의 범용 능력을 만드는 기반 단계다. 실무 관점에서는 모델 구조, 학습 목표, 데이터 거버넌스, 분산 학습, 안전성 평가까지 하나의 라이프사이클로 설명하는 것이 중요하다.

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Decoder-only Transformer | GPT의 기본 구조 |
| Causal Mask | 미래 토큰 차단 |
| Tokenization | 텍스트를 학습 단위로 변환 |
| RLHF/DPO | 선호와 지시 준수 개선 |
| RAG | 최신 지식과 출처 보강 |
