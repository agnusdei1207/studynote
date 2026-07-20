---
title: "Wordpiece Sentencepiece"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 385
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WordPiece는 언어 모델 우도(Log-Likelihood) 증가량을 기준으로 서브워드를 병합하고, SentencePiece는 공백을 특수 문자로 처리해 언어에 독립적인 원시 텍스트 토크나이징을 구현한다.
> 2. **가치**: BERT의 WordPiece는 `##` 접두사로 서브워드 경계를 명시해 NLU (Natural Language Understanding) 태스크에 최적화되고, SentencePiece는 BPE/Unigram을 언어 독립적으로 구현해 다국어 모델의 표준이 됐다.
> 3. **판단 포인트**: 세 알고리즘(BPE·WordPiece·Unigram)의 병합/분할 기준 차이와 `##` vs `▁` 표기법, Sentencepiece의 역정규화 특성을 구분해서 설명할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

같은 서브워드 토크나이징 계열이지만, WordPiece와 SentencePiece는 알고리즘과 사용 맥락이 다르다. 실무에서 BERT 계열 모델을 다루면 WordPiece, T5·LLaMA 계열은 SentencePiece를 만나게 된다.

두 방법 모두 데이터 기반 서브워드 어휘 구축이라는 목표를 공유하지만, 병합 기준과 공백 처리 방식에서 차이가 있다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: WordPiece는 "확률적으로 가장 유리한 조합을 고르는 영리한 합병", SentencePiece는 "언어의 공백 규칙을 무시하고 바이트 스트림처럼 처리하는 언어 중립적 합병"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### WordPiece (BERT)

**병합 기준**: 두 서브워드 A, B를 병합했을 때 언어 모델 우도 증가량 최대
```
Score(A, B) = freq(AB) / (freq(A) × freq(B))
-> 단독으로 자주 나오는 쌍보다 함께 나올 때 더 의미 있는 쌍 우선
```

<strong><code>##</code> 표기</strong>: 단어 내부 서브워드에 `##` 접두사 부착
```
"playing" -> ["play", "##ing"]
"unbelievable" -> ["un", "##believe", "##able"]
```

### SentencePiece

언어에 독립적으로 작동하기 위한 핵심 아이디어:
```
공백을 특수 메타 심볼 ▁ (U+2581)로 대체
"Hello world" -> "▁Hello▁world" -> 토크나이징 -> ["▁Hello", "▁world"]
"Hello" -> ["▁Hello"]
```

공백이 토큰의 일부가 되어, 디토크나이징(역변환) 시 공백을 자동 복원:
```
["▁Hello", "▁world"] -> "Hello world"  (역방향 결정론적)
```

```
+-------------------------------------------------------+
|  WordPiece vs SentencePiece 비교                      |
|                                                       |
|  입력: "Hello world"                                  |
|                                                       |
|  WordPiece:  ["Hello", "world"]                       |
|              (단어 분리 후 서브워드)                   |
|                                                       |
|  SentencePiece: ["▁Hello", "▁world"]                  |
|              (원시 텍스트 직접 -> 공백 포함)            |
|                                                       |
|  "unhappy" 처리:                                      |
|  WordPiece: ["un", "##happy"]                         |
|  SentencePiece(BPE): ["▁un", "happy"]                 |
+-------------------------------------------------------+
```

| 특성 | BPE | WordPiece | SentencePiece |
|:---|:---|:---|:---|
| 병합 기준 | 빈도 최대 | 우도 증가 최대 | BPE 또는 Unigram |
| 공백 처리 | 외부 의존 | 외부 의존 | ▁ 내재화 |
| OOV 처리 | 서브워드 분해 | 서브워드 분해 | 완전 제거 가능 |
| 디토크나이징 | 복잡 | `##` 제거 | ▁ -> 공백 |
| 대표 모델 | GPT-2 | BERT | T5, LLaMA |

### Unigram Language Model 토크나이저 (SentencePiece 옵션)

BPE와 반대 방향: 큰 어휘에서 시작해 제거
```
1. 큰 어휘 초기화 (모든 서브워드)
2. 각 서브워드 제거 시 우도 감소량 계산
3. 우도 감소가 가장 적은 서브워드 제거
4. 목표 크기까지 반복
```

- **📢 섹션 요약 비유**: BPE는 "작은 블록부터 쌓는" 방식, Unigram은 "큰 건물에서 덜 중요한 방을 뜯어내는" 방식이다.

---

## Ⅲ. 비교 및 연결

다국어 처리 측면:
- SentencePiece는 언어별 전처리(공백, 형태소 분석) 없이 원시 텍스트 직접 처리
- 한국어처럼 공백이 의미 단위와 다른 언어에서 특히 유리
- mT5, XLM-RoBERTa 등 다국어 모델에서 SentencePiece 표준 채택

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 설정 | 작은 규모, 개념 학습 |
| WordPiece / SentencePiece 토크나이징 비교 (Wordpiece Sentencepiece) | 성능과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | 서비스 고도화 단계 |

- **📢 섹션 요약 비유**: WordPiece는 영어 단어를 먼저 나눠 처리하는 "영어 중심" 방식이고, SentencePiece는 언어 상관없이 글자 흐름 그대로 처리하는 "언어 맹목적" 방식이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>BERT fine-tuning 시</strong>: `##` 표기 토큰의 오프셋 매핑 주의 (NER 등 span 예측 태스크)
<strong>T5/LLaMA fine-tuning</strong>: SentencePiece의 ▁ 처리로 공백 복원이 자동
**토크나이저 재사용**: 동일 토크나이저로 사전학습 -> 파인튜닝 일관성 필수

실무자 포인트: WordPiece의 스코어 함수(빈도 비율) vs BPE(빈도 합산)의 차이, SentencePiece의 언어 독립성 강점을 비교 설명.

- **📢 섹션 요약 비유**: 토크나이저 재사용은 "같은 사전으로 공부한 학생만 같은 시험을 볼 수 있다"는 원칙이다. 사전이 다르면 같은 단어도 다른 번호가 매겨진다.

---

## Ⅴ. 기대효과 및 결론

WordPiece와 SentencePiece는 BPE의 발전 형태로, 각각 BERT와 T5/LLaMA 생태계의 표준 토크나이저가 됐다. 서브워드 알고리즘의 선택은 모델 성능, 다국어 지원, 디토크나이징 편의성에 직접 영향을 미친다. 실무에서 올바른 토크나이저 이해는 파인튜닝과 프롬프트 엔지니어링의 토대다.

- **📢 섹션 요약 비유**: 토크나이저는 요리사의 칼이다. 재료(텍스트)를 어떻게 써느냐에 따라 요리(모델 학습)의 맛이 달라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| WordPiece | BERT, ## 표기, 우도 기반 / 영어 중심 서브워드 |
| SentencePiece | T5, LLaMA, ▁ 표기 / 언어 독립적 서브워드 |
| Unigram LM | 확률 기반 제거 / SentencePiece 옵션 |
| BPE | 빈도 병합 / 서브워드 기원 알고리즘 |
| OOV | 미등록 단어 / 서브워드로 해결 |
| 디토크나이징 | 역변환, 공백 복원 / SentencePiece 장점 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [WordPiece / SentencePiece 토크나이징 비교 (Wordpiece Sentencepiece)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. WordPiece는 단어를 먼저 나누고 그 안에서 조각을 찾는데, 조각 앞에 ## 표시를 달아서 "이건 단어 안에 있는 조각이야"라고 알려줘.
2. SentencePiece는 공백도 특별한 기호(▁)로 바꿔서 처리하니까 한국어처럼 공백 규칙이 다른 언어도 잘 다뤄.
3. 둘 다 모르는 단어가 나와도 당황하지 않아. 이미 알고 있는 조각들로 쪼개면 되니까!
