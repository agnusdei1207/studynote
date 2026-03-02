+++
title = "자연어 처리 (NLP)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 자연어 처리 (NLP, Natural Language Processing)

## 핵심 인사이트 (3줄 요약)
> **NLP**는 컴퓨터가 인간 언어를 이해·생성·분석하는 AI 분야로, 규칙 기반→통계 기반→딥러닝→LLM으로 패러다임이 전환되었다. BERT(이해)와 GPT(생성)가 현대 NLP의 두 축이며, 2024년 GPT-4o·Claude 3.5 등 멀티모달 LLM이 텍스트+이미지+음성을 통합한다. 기술사 관점에서 토크나이제이션·임베딩·파인튜닝·RAG 파이프라인이 핵심이다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: NLP는 컴퓨터가 인간의 자연어를 처리·이해·생성하는 기술 분야로, 텍스트 데이터에서 의미·감정·의도를 추출하고 원하는 언어로 출력한다.

> 비유: "AI 통역사 + 문서 분석가 + 작가 = NLP AI"

**등장 배경**:
- 규칙 기반 NLP 한계: 언어의 무한한 변형에 규칙 수동 대응 불가
- 통계 기반(2000년대): HMM, CRF, n-gram → 대규모 코퍼스 필요
- Word2Vec(2013): 단어를 벡터로 → 의미 산술 가능 ("왕-남=여왕")
- BERT(2018)·GPT-2(2019): 사전훈련+미세조정 패러다임 확립
- ChatGPT(2022): NLP로 세계를 바꿈

---

### Ⅱ. 구성 요소 및 핵심 원리

**NLP 핵심 태스크**:
| 태스크 | 설명 | 대표 모델 |
|-------|------|---------|
| 텍스트 분류 | 문서 → 카테고리 | BERT Fine-tuning |
| NER (개체명 인식) | 텍스트에서 사람/장소/조직 추출 | BERT, SpaCy |
| 감성 분석 | 긍정/부정/중립 분류 | BERT, LLM |
| 기계 번역 | 소스→타겟 언어 | mBART, NLLB |
| 질의응답 (QA) | 문맥+질문→답변 | BERT, GPT-4 |
| 텍스트 요약 | 긴 텍스트→핵심 요약 | BART, Pegasus, GPT-4 |
| 텍스트 생성 | 프롬프트→자연스러운 텍스트 | GPT-4o, Claude |
| 정보 추출 | 비정형→구조화 정보 | LLaMA, GPT + 스키마 |
| 대화 시스템 | 멀티턴 대화 | ChatGPT, Gemini |

**핵심 원리 - 임베딩 발전사**:
```
One-hot Encoding (초기):
  "고양이" → [0,0,1,0,0,...] (1만 차원)
  → 의미 없음, 메모리 낭비

Word2Vec (2013):
  "고양이" → [0.8, -0.3, 0.5, ...] (300 차원)
  → 의미 유사도: 코사인 유사도
  → "강아지"와 벡터가 비슷!

BERT Embedding (2018, Contextual):
  "은행에 갔다" vs "강둑(은행) 옆에 갔다"
  → 같은 "은행"이지만 다른 벡터!
  → 문맥 반영!

GPT 기반 Generation:
  트랜스포머 디코더로 다음 토큰 자동회귀 생성
```

**토크나이제이션**:
```
BPE (Byte Pair Encoding):
  "low" → 문자 단위 시작 → 자주 등장하는 쌍 합침
  "learn" → "le", "arn" → LLM 어휘
  → 미등록어 처리 + 효율적 어휘

SentencePiece:
  언어 무관한 서브워드 분리 → 다국어 모델
  
Tiktoken (OpenAI):
  GPT 계열 토크나이저
  한국어: 약 1-2토큰/자 (영어 1토큰/단어와 차이)
```

**코드 예시** (BERT 텍스트 분류 Fine-tuning):
```python
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import torch

# 모델 및 토크나이저 로딩
MODEL_NAME = "klue/bert-base"  # 한국어 BERT
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)  # 긍정/부정/중립

# 데이터 전처리
def tokenize_function(examples):
    return tokenizer(
        examples["text"], 
        padding="max_length", 
        truncation=True, 
        max_length=128,
        return_tensors="pt"
    )

train_dataset = Dataset.from_dict({
    "text": ["서비스가 정말 좋아요!", "최악입니다", "보통이네요"],
    "label": [2, 0, 1]  # 2=긍정, 0=부정, 1=중립
})
tokenized_train = train_dataset.map(tokenize_function, batched=True)

# 학습 설정
training_args = TrainingArguments(
    output_dir="./sentiment_model",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
)
trainer.train()

# 추론
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    pred = outputs.logits.argmax(-1).item()
    return ["부정", "중립", "긍정"][pred]

print(predict_sentiment("오늘 서비스가 놀라울 정도로 좋았어요!"))  # → 긍정
```

---

### Ⅲ. 기술 비교 분석  ↔  NLP 패러다임 변화

**NLP 패러다임 비교**:
| 시대 | 방식 | 대표 기술 | 한계 |
|------|------|---------|------|
| 규칙 기반 | 사람이 문법 규칙 직접 작성 | ELIZA(1966) | 확장성 없음 |
| 통계 기반 | 확률 통계 모델 | n-gram, HMM, CRF | 희소성 문제 |
| 딥러닝 초기 | 단어 임베딩 + RNN | Word2Vec + LSTM | 장거리 의존성 |
| Transformer | 사전훈련 + 미세조정 | BERT, GPT-2 | 도메인 일반화 |
| LLM 시대 | 초거대 사전훈련 | ChatGPT, GPT-4 | 비용, 환각 |

> **선택 기준**: 분류/추출 → BERT 계열 Fine-tuning; 생성/대화 → GPT/Claude API; 비용 제한 → 오픈소스 LLM + LoRA

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 시나리오 | NLP 기법 | 기대 효과 |
|------------|--------|--------|
| 고객 리뷰 분석 | 감성 분석 + 키워드 추출 | 제품 개선 인사이트 자동화 |
| 계약서 검토 자동화 | 정보 추출 + QA | 법무팀 처리 시간 70% 단축 |
| 다국어 고객 지원 | NMT + LLM | 24/7 다국어 자동 응답 |
| 뉴스 요약 서비스 | Abstractive Summarization | 뉴스 처리 시간 80% 절감 |
| 코드 이해·생성 | Code LLM (CodeLlama, StarCoder) | 개발 생산성 30~50% 향상 |

**관련 개념**: 토크나이제이션, Word2Vec, BERT, GPT, 감성 분석, NER, 기계 번역, RAG, 임베딩

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 고객 서비스 | NLP 기반 자동 응답 | CS 처리량 3~5배 향상 |
| 문서 처리 | 계약서·보고서 자동 분석 | 처리 시간 70~90% 단축 |
| 언어 장벽 제거 | 실시간 번역 | 글로벌 진출 비용 절감 |

> **결론**: NLP는 LLM의 근간이자 인간-AI 인터페이스의 핵심. 2024년 GPT-4o·Gemini로 텍스트+음성+이미지가 통합된 멀티모달 NLP 시대가 도래했다. 기술사는 토크나이제이션·임베딩·BERT/GPT 미세조정·RAG 파이프라인 설계를 핵심 역량으로 갖춰야 한다.

---

## 어린이를 위한 종합 설명

**NLP는 "AI가 우리 말을 이해하고 대화하는 것"이야!**

```
예전: "날씨 알려줘" → 컴퓨터: "날씨"를 키워드로 검색
지금 NLP AI: "내일 소풍 가려는데 어때?" → 소풍 = 날씨 필요
             → "내일 맑음! 소풑 가기 딱 좋아요 ☀️"

감성 분석:
"이 음식 진짜 맛있다!" → 긍정 (AI가 알아서 파악!)
"조금 아쉽네요..."    → 부정
```

실생활:
```
번역기 (파파고, 구글): 한국어 → 영어 (NLP!)
맞춤법 검사기: 문법 오류 탐지 (NLP!)
유튜브 자막: 음성→텍스트 (Speech NLP!)
ChatGPT와 대화: 가장 강력한 NLP!
```

> NLP = AI에게 우리말을 이해하는 귀와 말하는 입을 달아주는 것! 🗣️👂🤖

---
