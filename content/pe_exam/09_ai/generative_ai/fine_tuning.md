+++
title = "파인튜닝 및 PEFT (Fine-tuning & LoRA)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 파인튜닝 및 PEFT (Fine-tuning & Parameter-Efficient Fine-Tuning)

## 핵심 인사이트 (3줄 요약)
> **파인튜닝**은 사전훈련 LLM을 특정 도메인/태스크에 맞게 추가 학습하는 기법으로, 전체 파라미터 업데이트(Full Fine-tuning)와 일부만 업데이트하는 **PEFT(LoRA, QLoRA, Adapter)** 방식으로 나뉜다. LoRA는 원본 파라미터 고정 후 저랭크 행렬(0.1~1% 파라미터)만 학습하여 비용 100분의 1로 성능 유사하게 달성한다. 2024년 **RLHF 없는 DPO**가 선호도 정렬의 주류로 자리잡았다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: 파인튜닝은 대규모 코퍼스로 사전훈련된 LLM을 특정 도메인 데이터나 태스크 지침으로 추가 학습하여 성능을 특화시키는 과정이다.

> 비유: "의대 졸업 후 내과 전문의 수련 — 일반 의학 지식을 갖춘 LLM을, 심장 전문 의사로 특화 훈련"

**등장 배경**:
- LLM은 범용이지만 도메인 전문성 부족 (의료·법률·코드)
- Few-shot만으론 성능 한계
- 전체 파인튜닝 비용: GPT-3 175B → GPU 수백~수천 장 × 수일
- **LoRA(2021, Hu et al.)**: 저랭크 분해로 0.1% 파라미터만 학습 → 비용 혁신

---

### Ⅱ. 구성 요소 및 핵심 원리

**파인튜닝 방식 비교**:
| 방식 | 파라미터 업데이트 | 비용 | 성능 | 대표 |
|------|------------|------|------|------|
| Full Fine-tuning | 전체 | 매우 높음 | 최고 | ChatGPT |
| Feature Extraction | Frozen + Head만 | 낮음 | 중간 | BERT 분류 |
| LoRA | 저랭크 행렬 (~0.1%) | 낮음 | 거의 동등 | LLaMA 특화 |
| QLoRA | 4bit 양자화 + LoRA | 매우 낮음 | 유사 | 메모리 제한 환경 |
| Adapter Tuning | 소형 Adapter 레이어 | 낮음 | 중-높음 | BERT 적응 |
| Prefix Tuning | 소프트 프롬프트 학습 | 매우 낮음 | 중간 | 생성 모델 |
| Instruction Tuning | 지침-응답 쌍 SFT | 중간 | 높음 | Alpaca, Vicuna |

**LoRA 핵심 원리**:
```
기존: W0 = 거대 가중치 행렬 (d×k)
LoRA: W0 + ΔW = W0 + B·A
  - A: r×k 행렬 (랜덤 초기화)
  - B: d×r 행렬 (0 초기화)
  - r: 랭크 (보통 4~64, 훨씬 작은 값)
  
파라미터 절감:
원본: d×k = 768×768 = 589,824
LoRA(r=8): r×k + d×r = 8×768 + 768×8 = 12,288 (98% 절감!)

추론 시: W = W0 + B·A로 병합 → 추론 오버헤드 없음!
```

**코드 예시** (QLoRA로 LLaMA 파인튜닝):
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from trl import SFTTrainer
import torch

# 1. 4bit 양자화로 모델 로딩 (QLoRA)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    load_in_4bit=True,              # QLoRA: 4bit 양자화
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    device_map="auto"
)

# 2. kbit 학습 준비
model = prepare_model_for_kbit_training(model)

# 3. LoRA 설정
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # 랭크
    lora_alpha=32,                 # 스케일링 하이퍼파라미터
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # 적용 레이어
    lora_dropout=0.05,
    bias="none"
)
model = get_peft_model(model, lora_config)

# 학습 가능 파라미터 확인
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"학습 파라미터: {trainable:,} ({100*trainable/total:.2f}%)")
# → 학습 파라미터: 6,815,744 (0.08%)  ← 전체의 0.08%만!

# 4. SFT (Supervised Fine-Tuning)
trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    peft_config=lora_config,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        output_dir="./llama3-finetuned",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=False, bf16=True,
        logging_steps=10, save_steps=100,
        warmup_ratio=0.03,
    )
)
trainer.train()

# 5. LoRA 가중치 저장
model.save_pretrained("./llama3-lora-adapter")
```

**DPO (Direct Preference Optimization)**:
```
RLHF: 보상 모델 학습 → PPO 강화학습 → 복잡하고 불안정
DPO: 선호 데이터 (y_w > y_l) 직접 최적화
L = -E[log σ(β·log(π_θ(y_w)/π_ref(y_w)) - β·log(π_θ(y_l)/π_ref(y_l)))]
→ 보상 모델 불필요! 더 안정적, 더 효율적!
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + 기법 비교

**장단점**:
| 장점 | 단점 |
|-----|------|
| 도메인 특화 성능 향상 | 오버피팅 위험 (소량 데이터) |
| LoRA/QLoRA로 비용 혁신 | Catastrophic Forgetting (일반화 능력 손실) |
| PEFT로 여러 태스크 동시 적용 | 데이터 품질이 결과 좌우 |
| DPO로 RLHF 안정화 | 데이터 수집/가공 비용 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 시나리오 | 기법 | 기대 효과 |
|------------|------|--------|
| 사내 법률 AI | QLoRA + 계약서 데이터 | 법률 용어 정확도 90%+ |
| 의료 챗봇 | SFT + 의료 Q&A + DPO | 진단 보조 신뢰도 向上 |
| 코드 리뷰 AI | Instruction Tuning + 코드 데이터 | 코드 품질 제안 정확도↑ |
| 고객 서비스 | SFT + 회사 FAQ 데이터 | CS 자동화율 60~70% |
| 금융 분석 | Full Fine-tuning (충분한 GPU 있을 때) | 금융 전문 성능 최고 |

**관련 개념**: LLM, LoRA, QLoRA, RLHF, DPO, SFT, 전이학습, 지식 증류, PEFT

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 비용 효율 | LoRA로 일반 GPU에서 파인튜닝 | 학습 비용 95% 절감 |
| 도메인 성능 | 특화 데이터로 훈련 | F1 기준 10~30% 향상 |
| 배포 유연성 | 여러 LoRA Adapter 동적 교체 | 단일 기반 모델로 N개 도메인 |

> **결론**: LoRA/QLoRA는 "LLM 특화의 민주화" — 소규모 팀도 RTX 4090 한 장으로 전문 LLM 구축 가능하게 했다. 2024년 DPO가 RLHF를 대체하며 정렬 파인튜닝의 표준이 되었다. 기술사는 데이터 품질·LoRA 설정·Catastrophic Forgetting 방지·DPO 활용을 설계할 수 있어야 한다.

---

## 어린이를 위한 종합 설명

**파인튜닝은 "의대 졸업생을 전문의로 만들기"야!**

```
일반 LLM (의과대학 졸업생):
모든 걸 조금씩 알아 → 심장, 뼈, 피부, 안과...

의료 파인튜닝:
심장 교과서 1000권을 추가로 공부!
→ 심장 전문의 완성!
```

LoRA의 마법 (비용 혁신):
```
일반 파인튜닝: 뇌 전체를 다시 훈련 (비싸고 느림!)
LoRA: 뇌의 0.1%만 추가 훈련
→ 결과는 거의 같음!
비용은 100분의 1!
```

> 파인튜닝 = AI한테 "당신 전공이 뭐예요?"를 정해주는 것! 🎓💊⚕️

---
