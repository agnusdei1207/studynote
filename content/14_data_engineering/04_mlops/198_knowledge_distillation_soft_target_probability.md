---
title: "Knowledge Distillation Soft Target Probability"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 198
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지식 증류(Knowledge Distillation)는 대형 교사 모델(Teacher Model)의 확률 분포(소프트 타겟)를 소형 학생 모델(Student Model)이 모방하여, 크기를 줄이면서도 성능을 최대한 유지하는 경량화 기법이다.
> 2. **가치**: BERT -> DistilBERT처럼 파라미터 40% 감소 시 성능 97% 유지가 가능하며, 온도 매개변수(Temperature)로 클래스 간 관계 정보까지 전이하는 것이 일반 Hard Label 학습 대비 핵심 차별점이다.
> 3. **판단 포인트**: 응답 기반(Response-based), 피처 기반(Feature-based), 관계 기반(Relation-based) 3가지 증류 방식을 태스크와 모델 구조에 맞게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 모델 경량화의 필요성

대형 언어 모델(LLM)과 대형 비전 모델은 추론 비용이 막대하여 엣지 디바이스나 실시간 서비스에 배포하기 어렵다.

| 모델 | 파라미터 수 | 추론 메모리 | 추론 속도 |
|:---|:---|:---|:---|
| GPT-3 | 175B | 350GB | 수초/요청 |
| GPT-4 (추정) | 1T+ | 2TB+ | 수초/요청 |
| BERT-base | 110M | 440MB | 100ms |
| DistilBERT | 66M (-40%) | 264MB | 60ms (-40%) |
| MobileNet V3 | 5.4M | 22MB | 10ms |

### 1.2 지식 증류 vs 다른 경량화 기법

| 기법 | 방법 | 특징 |
|:---|:---|:---|
| 지식 증류 | 교사->학생 지식 전이 | 작은 모델로 높은 성능 |
| 양자화(Quantization) | 정밀도 감소 (FP32->INT8) | 구현 쉬움, 정확도 일부 손실 |
| 가지치기(Pruning) | 불필요 파라미터 제거 | 구조적/비구조적 선택 |
| NAS (Neural Architecture Search) | 최적 아키텍처 탐색 | 높은 계산 비용 |

### 1.3 지식 증류의 핵심 아이디어

```
Hard Label (전통 학습) vs Soft Target (지식 증류)

[분류 문제: 개, 고양이, 자동차]

Hard Label (원핫 인코딩):
  실제 정답: 개 -> [1, 0, 0]
  -> 클래스 간 관계 정보 없음
  -> "개와 고양이가 자동차보다 유사하다"는 정보 손실

Soft Target (교사 모델 출력):
  교사 모델 확률: 개 -> [0.7, 0.25, 0.05]
  -> "개랑 고양이가 비슷함" 정보 포함!
  -> 학생 모델이 더 풍부한 정보로 학습
```

📢 **섹션 요약 비유**: 지식 증류는 대학교수(교사 모델)가 학생(학생 모델)을 가르칠 때, 단순히 "정답은 A"가 아니라 "A가 가장 맞고 B도 일부 맞으며 C는 전혀 아니다"는 뉘앙스까지 전달하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 지식 증류 손실 함수

```
지식 증류 학습 구조

교사 모델 (Teacher, 고정)
  입력 x -> 소프트맥스(logits/T) -> 소프트 타겟 q_T
                                      |
학생 모델 (Student, 학습 중)           |
  입력 x -> 소프트맥스(logits/T) -> q_S v
                                  KL Divergence 손실
                                  L_distill = KL(q_T || q_S)
  입력 x -> 소프트맥스(logits/1) -> 하드 예측
                                  L_ce = CrossEntropy(y, q_S)

최종 손실 함수:
  L_total = α × T^ × L_distill + (1-α) × L_ce

  α: 증류 손실 가중치 (보통 0.5~0.9)
  T: 온도 매개변수 (보통 2~20)
  T^: 온도 스케일링 보정 (그래디언트 크기 정규화)
```

### 2.2 온도 매개변수 (Temperature) 효과

```
온도(T)에 따른 확률 분포 변화

원본 logits: [3.0, 0.5, -1.5]

T=1 (Hard, 기본):
  소프트맥스: [0.87, 0.12, 0.01]
  -> 개 압도적 우세, 고양이/자동차 구분 어려움

T=5 (Soft):
  소프트맥스: [0.55, 0.35, 0.10]
  -> 고양이와의 유사성 정보 드러남

T=10 (Very Soft):
  소프트맥스: [0.40, 0.38, 0.22]
  -> 모든 클래스 관계 정보 최대 활용

T->∞:
  소프트맥스: [0.33, 0.33, 0.33]
  -> 균등 분포 (정보 없음)

최적 T: 태스크와 교사 모델에 따라 실험적으로 결정
```

### 2.3 3가지 증류 방식

```
+-----------------------------------------------------------+
|              지식 증류 3가지 방식                           |
|                                                           |
|  ① 응답 기반 (Response-based Distillation)                |
|     교사 모델의 최종 출력 확률 분포만 모방                  |
|                                                           |
|     Teacher: [레이어1] -> [레이어N] -> 소프트맥스 출력       |
|                                              v 전이         |
|     Student: [레이어1] -> [레이어M] -> 소프트맥스 모방       |
|                                                           |
|  ② 피처 기반 (Feature-based Distillation)                 |
|     중간 피처 표현(Feature Map)도 함께 모방                 |
|                                                           |
|     Teacher: [레이어1] -> [레이어k] -> [레이어N]             |
|                              v 중간 피처 전이              |
|     Student: [레이어1] -> [레이어j] -> [레이어M]             |
|                                                           |
|  ③ 관계 기반 (Relation-based Distillation)                |
|     샘플 간 관계(거리, 각도)를 모방                        |
|                                                           |
|     데이터 포인트 A, B, C 간의 거리 관계:                  |
|     Teacher: dist(A,B) < dist(A,C)                       |
|     Student: 동일한 거리 관계 유지하도록 학습              |
+-----------------------------------------------------------+
```

| 방식 | 전이 정보 | 구현 난이도 | 효과 |
|:---|:---|:---|:---|
| 응답 기반 | 최종 확률 분포 | 쉬움 | 기본 경량화 |
| 피처 기반 | 중간 레이어 표현 | 중간 | 높은 성능 유지 |
| 관계 기반 | 샘플 간 관계 | 어려움 | 일반화 향상 |

### 2.4 BERT -> DistilBERT 증류 실제 구현

```
DistilBERT 증류 과정

교사: BERT-base (12 레이어, 110M 파라미터)
학생: DistilBERT (6 레이어, 66M 파라미터)

손실 함수 조합:
  L = 5.0 × L_ce           # 하드 레이블 손실
    + 2.0 × L_mlm           # 언어 모델 손실 (MLM)
    + 1.0 × L_cos           # 중간 레이어 코사인 유사도

결과:
  파라미터: 40% 감소 (110M -> 66M)
  추론 속도: 60% 향상
  성능 유지: GLUE 벤치마크 97% 유지
  메모리: 40% 감소
```

📢 **섹션 요약 비유**: 온도 매개변수는 사진 현상 온도와 같다. 너무 뜨거우면(높은 T) 모든 것이 흐릿하게 나오고(균등 분포), 너무 차가우면(낮은 T) 한 가지만 선명하게 나온다(한 클래스 독점). 최적 온도에서 전체 구도가 균형 있게 드러난다.

---

## Ⅲ. 비교 및 연결

### 3.1 지식 증류 적용 사례

| 사례 | 교사 | 학생 | 감소율 | 성능 유지 |
|:---|:---|:---|:---|:---|
| DistilBERT | BERT-base | DistilBERT | 40% 파라미터 | 97% GLUE |
| TinyBERT | BERT-base | TinyBERT | 87% 파라미터 | 96% GLUE |
| DistilGPT-2 | GPT-2 | DistilGPT-2 | 33% 파라미터 | 유사 생성 품질 |
| MobileNet -> ??? | EfficientNet | MobileNet | 96% 파라미터 | 90% Top-1 |
| ResNet -> 경량화 | ResNet-50 | ResNet-18 + KD | 75% 파라미터 | 98% 성능 |

### 3.2 Self-Distillation (자기 증류)

```
교사와 학생이 동일 아키텍처인 경우

Self-KD (Self-Knowledge Distillation):
  에포크 초기 모델 -> 교사 역할
  현재 학습 중 모델 -> 학생 역할

Born Again Networks (BAN):
  학습 완료 모델 -> 교사
  동일 크기 새 모델 -> 학생
  -> 앙상블 없이 앙상블 효과
```

### 3.3 지식 증류 vs 전이 학습 비교

| 항목 | 지식 증류 | 전이 학습 (Fine-tuning) |
|:---|:---|:---|
| 목표 | 모델 경량화 | 새 태스크 적응 |
| 교사 역할 | 소프트 레이블 제공 | 초기 가중치 제공 |
| 학생 크기 | 교사보다 작음 | 교사와 동일 또는 더 작음 |
| 학습 데이터 | 동일 태스크 데이터 | 새 태스크 데이터 |
| 출력 | 경량 추론 모델 | 새 태스크 특화 모델 |

📢 **섹션 요약 비유**: 지식 증류는 전문의(교사)가 의대생(학생)을 가르칠 때, 교과서(하드 레이블) 외에 실제 임상 경험과 직관(소프트 타겟)까지 전달하는 것이다. 의대생은 더 빠르게, 더 폭넓은 지식으로 성장한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 엣지 배포를 위한 모델 경량화 전략 비교

| 전략 | 파라미터 감소 | 정확도 손실 | 구현 난이도 | 적합 시나리오 |
|:---|:---|:---|:---|:---|
| 지식 증류 | 40~90% | 낮음 (1~5%) | 중간 | 구조 변경 가능 시 |
| PTQ 양자화 | 0% (메모리만) | 낮음 (1~3%) | 쉬움 | 빠른 배포 필요 |
| QAT 양자화 | 0% (메모리만) | 최소 | 어려움 | 최고 품질 필요 |
| 구조적 가지치기 | 10~50% | 중간 | 어려움 | FLOP 감소 필요 |
| NAS | 60~95% | 최소 | 매우 어려움 | 장기 프로젝트 |

### 4.2 지식 증류 구현 코드 (PyTorch)

```python
import torch
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits,
                      labels, T=4.0, alpha=0.7):
    """
    지식 증류 손실 함수
    Args:
        student_logits: 학생 모델 출력 (배치, 클래스)
        teacher_logits: 교사 모델 출력 (배치, 클래스)
        labels: 실제 정답 레이블
        T: 온도 매개변수
        alpha: 증류 손실 가중치
    """
    # 소프트 타겟 생성 (온도 T 적용)
    soft_teacher = F.softmax(teacher_logits / T, dim=-1)
    soft_student = F.log_softmax(student_logits / T, dim=-1)

    # 증류 손실 (KL Divergence) - T^2로 스케일링
    distill_loss = F.kl_div(soft_student, soft_teacher,
                            reduction='batchmean') * (T ** 2)

    # 하드 레이블 손실 (Cross Entropy)
    hard_loss = F.cross_entropy(student_logits, labels)

    # 최종 손실 조합
    return alpha * distill_loss + (1 - alpha) * hard_loss


# 학습 루프
teacher_model.eval()  # 교사는 고정 (그래디언트 없음)
for inputs, labels in dataloader:
    with torch.no_grad():
        teacher_logits = teacher_model(inputs)

    student_logits = student_model(inputs)
    loss = distillation_loss(student_logits, teacher_logits,
                             labels, T=4.0, alpha=0.7)
    loss.backward()
    optimizer.step()
```

### 4.3 실무자 논술 핵심 판단 기준

| 판단 항목 | 지식 증류 선택 기준 |
|:---|:---|
| 엣지 디바이스 배포 | 구조 변경 가능하고 재학습 리소스 있을 때 |
| 빠른 경량화 필요 | PTQ 양자화 먼저 고려 (구현 쉬움) |
| 최고 성능 유지 | 피처 기반 증류 + QAT 양자화 조합 |
| 언어 모델 경량화 | DistilBERT/TinyBERT 사전학습 모델 활용 |

📢 **섹션 요약 비유**: 모델 경량화 전략 선택은 이삿짐 싸기와 같다. 빠리 이사(빠른 배포)에는 핵심만 챙기는 PTQ 양자화, 장거리 이사(장기 프로젝트)에는 꼼꼼히 분류하는 지식 증류가 적합하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 지식 증류 기대효과

| 효과 | 수치 |
|:---|:---|
| 모델 크기 감소 | 40~90% |
| 추론 속도 향상 | 2~5배 |
| 메모리 사용 감소 | 40~90% |
| 성능 유지율 | 95~99% (태스크에 따라) |
| 배포 비용 감소 | 클라우드 추론 비용 50~80% 감소 |

### 5.2 최신 증류 기법 동향

```
지식 증류 발전 방향

1. LLM 증류 (Large Language Model Distillation)
   +- GPT-4 -> GPT-3.5급 성능으로 증류
   +- Alpaca: GPT-4 52K 샘플로 LLaMA 7B 파인튜닝

2. 멀티모달 증류 (Multimodal Distillation)
   +- 텍스트+이미지 교사 -> 경량 단일 모달 학생

3. Online Distillation
   +- 교사 학습과 학생 학습 동시 진행 (코-학습)

4. Task-Agnostic Distillation
   +- 태스크 무관하게 일반 표현 증류
      (DistilBERT, TinyBERT 방식)
```

### 5.3 결론 요약

지식 증류는 AI 모델의 엣지 배포와 실시간 서빙을 가능하게 하는 핵심 경량화 기법이다. 소프트 타겟이 하드 레이블 대비 더 풍부한 학습 신호를 제공하는 원리를 이해하고, 실무 관점에서는 <strong>3가지 증류 방식의 차이, 온도 매개변수의 역할, BERT -> DistilBERT 같은 실제 적용 사례</strong>를 명확히 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: 지식 증류는 거대한 백과사전(교사 모델)의 핵심 내용을 작은 포켓북(학생 모델)으로 압축하는 작업이다. 단순히 내용을 잘라내는 것이 아니라, 전문가(교사)가 "이것이 왜 중요한지"(소프트 타겟)를 함께 기록해서 포켓북만 봐도 본질을 이해할 수 있게 한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기법 | Knowledge Distillation (지식 증류) | 교사->학생 모델 지식 전이 |
| 입력 신호 | Soft Target (소프트 타겟) | 교사 모델 확률 분포 출력 |
| 하이퍼파라미터 | Temperature (온도) | 확률 분포 부드러움 조절 |
| 증류 방식 | Response-based | 최종 출력 모방 |
| 증류 방식 | Feature-based | 중간 레이어 표현 모방 |
| 증류 방식 | Relation-based | 샘플 간 관계 모방 |
| 실사례 | DistilBERT | BERT 40% 경량화 |
| 비교 기법 | Quantization (양자화) | FP32->INT8 정밀도 감소 |
| 비교 기법 | Pruning (가지치기) | 불필요 파라미터 제거 |

### 👶 어린이를 위한 3줄 비유 설명

1. 지식 증류는 선생님(큰 AI)이 "정답은 A야, 근데 B도 조금 맞고 C는 완전히 틀렸어"라고 자세히 설명해주면, 학생(작은 AI)이 더 빠르게 배우는 거예요.

### 📈 관련 키워드 및 발전 흐름도

```text
대형 Teacher 모델 (높은 정확도 · 느린 추론)
    |
    v
지식 증류 (Knowledge Distillation)
    +-► 소프트 타겟: Teacher의 확률 분포 전달
    +-► Temperature Scaling: 분포 평탄화 (T>1)
    +-► KL Divergence 손실: Student ↔ Teacher 분포 매칭
    |
    v
경량 Student 모델 (엣지 배포 가능)
    |
    v
결합 기법
    +-► 양자화 + 증류: INT8 Student
    +-► 프루닝 + 증류: 희소 Student
    +-► Self-Distillation: 같은 모델 내 증류
```
2. 온도 매개변수는 아이스크림 온도예요. 너무 딱딱하면(낮은 온도) 한 맛만 강하게 느껴지고, 살짝 녹으면(높은 온도) 여러 맛이 고루 느껴지죠.
3. DistilBERT는 두꺼운 사전을 얇은 포켓 사전으로 만든 거예요. 40%는 줄었지만 97%의 내용은 그대로 담겨 있어요.
