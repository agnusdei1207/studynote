+++
title = "모델 압축 (Model Compression)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 모델 압축 (Model Compression)

## 핵심 인사이트 (3줄 요약)
> **모델 압축**은 대형 AI 모델을 정확도 손실을 최소화하면서 크기·속도·전력 소비를 줄이는 기술로, **지식 증류(Knowledge Distillation)·가지치기(Pruning)·양자화(Quantization)**가 3대 기법이다. LLM Time: INT8→INT4→FP8 양자화와 LoRA 결합의 QLoRA가 2024년 표준이 되었으며, 엣지 AI·온디바이스 AI 배포의 핵심 요소다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: 모델 압축은 딥러닝 모델의 연산량·메모리·파라미터를 줄여 추론 속도를 높이고 배포 비용을 낮추면서 성능 저하를 최소화하는 기술 집합이다.

> 비유: "백과사전 → 핵심 요약집 — 내용은 거의 같지만 크기는 1/10, 찾기는 10배 빠름"

**등장 배경**:
- LLM 크기 폭발: GPT-3 175B → 스마트폰·엣지에서 실행 불가
- 추론 비용: GPT-4 API 100K 토큰 = $10 → 비용 최적화 필수
- On-device AI 수요: 클라우드 없이 프라이버시 보장 AI 처리
- 에너지 효율: AI의 탄소발자국 규제 강화

---

### Ⅱ. 구성 요소 및 핵심 원리

**3대 압축 기법 비교**:
| 기법 | 원리 | 크기 절감 | 정확도 손실 | 복잡도 |
|------|------|--------|---------|------|
| 양자화 | FP32→INT8/INT4 | 4~8배↓ | 작음 | 낮음 |
| 가지치기 | 중요도 낮은 가중치 제거 | 2~10배↓ | 중간 | 중간 |
| 지식 증류 | 큰 모델→작은 모델 학습 | 10~100배↓ | 낮음 | 높음 |
| 저랭크 분해 | 행렬 SVD 분해 | 2~5배↓ | 작음 | 낮음 |
| 아키텍처 탐색 (NAS) | 효율적 구조 자동 탐색 | 가변 | 작음 | 매우 높음 |

**핵심 원리**:
```
[1. 양자화 (Quantization)]
FP32 가중치 → INT8 (8비트 정수) 변환

Scale = (max - min) / (2^8 - 1)
quantized = round(weight / scale)

FP32(4bytes) → INT8(1byte): 4배 메모리 절감, 4배 빠름!
INT4(0.5byte): 8배 절감 (QLoRA, llama.cpp 사용)
FP8 (H100 네이티브): 학습 효율 2배↑

[2. 가지치기 (Pruning)]
크기 작은 가중치 → 0으로 설정 (밀도 감소)
비구조적 가지치기: 임의 위치 가중치 제거
구조적 가지치기: Attention Head·레이어 전체 제거 → 하드웨어 친화

[3. 지식 증류 (Knowledge Distillation)]
Teacher Model (GPT-4) → Student Model (작은 모델)
손실 함수:
L = α·L_CE(labels, student) + (1-α)·T²·KL(softmax(teacher/T), softmax(student/T))
T: 온도 (Teacher 확률분포를 부드럽게)
"정답만 아니라 Teacher가 어떻게 생각하는지도 학습"

Phi-3-mini (3B): GPT-4 수준 데이터로 증류 → 소형 모델의 놀라운 성능
```

**코드 예시** (지식 증류):
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, labels, 
                       alpha=0.5, temperature=4.0):
    """지식 증류 손실 함수"""
    # 소프트 레이블 손실 (Teacher 분포 모방)
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=-1),
        F.softmax(teacher_logits / temperature, dim=-1),
        reduction="batchmean"
    ) * (temperature ** 2)
    
    # 하드 레이블 손실 (정답 분류)
    hard_loss = F.cross_entropy(student_logits, labels)
    
    return alpha * hard_loss + (1 - alpha) * soft_loss
```

**양자화 유형**:
```
PTQ (Post-Training Quantization):
  학습 완료 후 양자화 → 빠르고 간단
  GPTQ, AWQ, SmoothQuant (LLM 특화)

QAT (Quantization-Aware Training):
  학습 중에 양자화 시뮬레이션 → 더 정확
  훈련 시간 2~3배 증가

QLoRA (Fine-tuning 특화):
  4bit 양자화 기반 모델 + LoRA 파인튜닝
  = 단일 RTX 4090으로 LLaMA-70B 파인튜닝 가능!
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + 기법별 사용 사례

**장단점**:
| 장점 | 단점 |
|-----|------|
| 추론 속도 대폭 향상 | 정확도 손실 (특히 양자화) |
| 메모리 사용량 감소 | 압축 과정 복잡 (특히 증류) |
| 엣지/모바일 배포 가능 | 태스크별 최적화 필요 |
| 비용·전력 절감 | 구조적 가지치기 시 재설계 필요 |

**LLM 양자화 도구 비교**:
| 도구 | 방법 | 지원 모델 | 특징 |
|------|------|---------|------|
| GPTQ | PTQ, INT4 | LLaMA, GPT | 고속 추론 최적화 |
| AWQ | PTQ, INT4 | LLaMA, Mistral | Activation-aware |
| llama.cpp | GGUF (INT4/5/8) | 범용 | CPU+GPU 추론 |
| TensorRT-LLM | INT8/FP8 | NVIDIA GPU | 최고 성능 (NVIDIA) |
| vLLM | Continuous Batching | 범용 서빙 | 처리량 최대화 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 목표 | 기법 | 기대 효과 |
|-----|------|--------|
| 모바일 AI | 지식 증류 (Teacher→Student) | GPT-4급 Teacher → Phi-3 수준 Student |
| 엣지 서버 | GPTQ INT4 양자화 | 메모리 8배↓, 속도 3~4배↑ |
| LLM 서비스 비용 절감 | FP8 + vLLM | 처리량 2~3배↑, 비용 50%↓ |
| 스마트폰 배포 | TFLite + INT8 | 클라우드 없이 On-device 추론 |
| LLM 파인튜닝 | QLoRA (4bit) | GPU 1장으로 70B 모델 파인튜닝 |

**관련 개념**: 양자화, 가지치기, 지식 증류, LoRA, QLoRA, TensorRT, ONNX, llama.cpp, vLLM

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 모델 크기 | INT4 양자화 | 원본 대비 8배 크기 절감 |
| 추론 속도 | TensorRT 최적화 | latency 3~5배 단축 |
| 배포 비용 | 엣지 배포 최적화 | 클라우드 비용 80% 절감 |

> **결론**: 모델 압축은 "AI 민주화의 핵심 기술" — 수천억 파라미터 모델을 일반 GPU·스마트폰에서 실행 가능하게 한다. INT4 양자화+지식증류+LoRA의 3중 조합이 2024~2025년 실무 표준이며, vLLM+TensorRT가 서빙 최적화의 표준이다.

---

## 어린이를 위한 종합 설명

**모델 압축은 "백과사전을 핵심 요약집으로 만들기"야!**

```
원본 LLM: 140GB (학교 도서관 전체)
→ 폰에 넣기 불가능!

양자화 (INT4):
  소수점 전부 → 정수로 바꾸기
  "3.14159..." → "3" (약간 틀리지만 훨씬 작음!)
  → 140GB → 17.5GB (8배 작아짐!)

지식 증류:
  GPT-4 (선생님) → 작은 AI (학생)
  "선생님처럼 생각하는 법을 가르침"
  → 선생님 실력의 80%를 가진 학생 완성!
```

> 모델 압축 = AI에게 "다이어트"시켜서 스마트폰에도 들어가게 만들기! 📱✂️🤖

---
