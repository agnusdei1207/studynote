---
title: "Zero Redundancy Optimizer"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 334
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VRAM (Video RAM) 부족은 대형 모델 학습의 핵심 병목이며, ZeRO (Zero Redundancy Optimizer) 는 옵티마이저 상태·그래디언트·파라미터를 GPU 간에 분할해 중복 저장을 제거함으로써 단일 GPU 한계를 돌파한다.
> 2. **가치**: ZeRO Stage 3 적용 시 N개 GPU 사용 시 메모리 소비를 이론적으로 1/N 수준으로 줄여, 수백억 파라미터 모델을 소규모 GPU 클러스터로 학습 가능하게 한다.
> 3. **판단 포인트**: 학습 정리에서는 "Stage 1->2->3 순으로 분산 범위가 확대되고 통신 오버헤드도 증가한다"는 트레이드오프를 반드시 언급해야 한다.

---

## Ⅰ. 개요 및 필요성

### VRAM 부족 문제의 구조

GPT-3 (175B 파라미터) 를 FP32 (Float 32-bit Precision) 로 학습하면 파라미터만 700 GB 이상이 필요하다. 단일 A100 GPU 의 VRAM 은 80 GB 에 불과하므로, 파라미터 외에도 다음 요소가 메모리를 압박한다.

| 구성 요소 | 메모리 비중 | 설명 |
|:---|:---:|:---|
| 파라미터 (Parameters) | ~16% | 모델 가중치 자체 |
| 그래디언트 (Gradients) | ~16% | 역전파 결과값 |
| 옵티마이저 상태 (Optimizer States) | ~48% | Adam: 모멘텀+분산 각 1copy |
| 활성화 (Activations) | ~20% | 순전파 중간 결과 |

Adam Optimizer 를 사용할 경우 파라미터 1개당 옵티마이저 상태 2개 (m, v) 가 추가되어 실질 메모리 소비는 파라미터 단독 대비 **3배 이상** 증가한다.

### 기존 해법의 한계

- <strong>DDP (Distributed Data Parallel)</strong>: 각 GPU 가 전체 모델 사본을 보유 -> VRAM 절감 없음
- <strong>모델 병렬화 (Tensor/Pipeline Parallelism)</strong>: 구현 복잡도 높고 파이프라인 버블 발생

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: VRAM 부족 문제는 "10명이 같은 두꺼운 교재를 각자 다 사서 들고 다니는" DDP 방식의 낭비와 같다. ZeRO 는 "교재를 10등분해서 한 명이 한 챕터씩만 들고 다니되, 필요할 때 빌려 쓰는" 도서관 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ZeRO Stage 1 / 2 / 3 분할 범위

```
+-----------------------------------------------------------------+
|           ZeRO (Zero Redundancy Optimizer) Stage 비교           |
+------------+--------------+--------------+----------------------+
|  구성 요소  |   Stage 1    |   Stage 2    |       Stage 3        |
+------------+--------------+--------------+----------------------+
| 옵티마이저  |  분할(Shard) |  분할(Shard) |    분할(Shard)       |
|   상태     |              |              |                      |
+------------+--------------+--------------+----------------------+
| 그래디언트  |    각 GPU    |  분할(Shard) |    분할(Shard)       |
|            |   전체 보유  |              |                      |
+------------+--------------+--------------+----------------------+
|  파라미터  |    각 GPU    |   각 GPU     |    분할(Shard)       |
|            |   전체 보유  |  전체 보유   |                      |
+------------+--------------+--------------+----------------------+
| 메모리 절감 |    ~4x       |    ~8x       |    ~Nx (N=GPU수)     |
+------------+--------------+--------------+----------------------+
| 통신 비용  |   적음        |   보통        |    높음              |
+------------+--------------+--------------+----------------------+
```

### DeepSpeed ZeRO 동작 흐름

```
  Forward Pass (순전파)
  +----------------------------------------------+
  |  GPU-0      GPU-1      GPU-2      GPU-3      |
  |  P[0..k]   P[k..2k]  P[2k..3k]  P[3k..N]  |  <- Stage 3: 파라미터 분할
  |     |           |          |           |     |
  |     +-----------+----------+-----------+     |
  |          All-Gather (파라미터 수집)            |
  +----------------------------------------------+
  Backward Pass (역전파)
  +----------------------------------------------+
  |  각 GPU 에서 로컬 그래디언트 계산              |
  |  Reduce-Scatter (그래디언트 집계 + 분산)       |
  |  각 GPU 는 자신의 파라미터 샤드만 업데이트     |
  +----------------------------------------------+
```

### ZeRO-Offload 와 ZeRO-Infinity

- <strong>ZeRO-Offload</strong>: 옵티마이저 상태·그래디언트를 CPU RAM 으로 오프로드 -> 단일 GPU 대형 모델 학습 가능
- <strong>ZeRO-Infinity</strong>: NVMe SSD 까지 오프로드 확장, 수조 파라미터 모델 지원

| 요소 | 역할 |
|:---|:---|
| 손실 함수 | 모델이 줄여야 할 오차를 정의하며 학습 방향을 만든다. |
| 학습률 | 업데이트 폭을 결정해 수렴 속도와 발산 위험을 좌우한다. |
| 일반화 | 훈련 성능이 아니라 실제 데이터 성능으로 품질을 판단하게 만든다. |
| 분산 학습 | 대규모 모델에서 학습 속도와 자원 배치를 현실화한다. |

- **📢 섹션 요약 비유**: ZeRO Stage 3 는 "각 팀원이 프로젝트 파일을 쪼개서 보관하고, 필요할 때 네트워크 드라이브에서 불러오는 협업 문서함" 같다. 파일이 중복 저장되지 않아 저장 공간이 절약되지만 불러오는 데 시간이 걸린다.

---

## Ⅲ. 비교 및 연결

### ZeRO vs 기존 병렬화 전략

| 전략 | VRAM 절감 | 구현 난이도 | 통신 패턴 | 적합 규모 |
|:---|:---:|:---:|:---|:---:|
| DDP (Distributed Data Parallel) | ❌ | 낮음 | AllReduce | 소형~중형 |
| 텐서 병렬 (Tensor Parallelism) | ✅ | 높음 | AllReduce (행/열) | 대형 |
| 파이프라인 병렬 (Pipeline Parallelism) | ✅ | 높음 | P2P 마이크로배치 | 대형 |
| ZeRO Stage 1 | ✅ | 낮음 | AllGather+Scatter | 중형~대형 |
| ZeRO Stage 3 | ✅✅✅ | 중간 | AllGather+Scatter | 초대형 |

### DeepSpeed 설정 포인트 (ds_config.json)

```json
{
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": { "device": "cpu" },
    "offload_param":     { "device": "cpu" },
    "overlap_comm": true,
    "contiguous_gradients": true
  },
  "fp16": { "enabled": true }
}
```

- **📢 섹션 요약 비유**: ZeRO 와 Tensor Parallelism 은 "짐을 수평으로 쪼개느냐(ZeRO), 수직으로 쪼개느냐(TP)" 의 차이다. ZeRO 는 레이어 단위가 아닌 텐서 값 자체를 나누므로 구현이 상대적으로 단순하다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 설정 체크리스트

1. **Stage 선택**: 모델 크기와 GPU 수에 따라 Stage 1->2->3 순차 시도
2. <strong>Gradient Checkpointing 병행</strong>: 활성화 메모리를 추가 절감 (시간 ~30% 증가)
3. <strong>Mixed Precision (FP16/BF16)</strong>: VRAM 절반 수준으로 감소, Tensor Core 가속
4. **overlap_comm**: 통신과 연산을 파이프라인화해 레이턴시 숨기기
5. **contiguous_gradients**: 그래디언트를 연속 메모리에 할당해 AllReduce 효율 향상

### 학습 주제 포인트

- ZeRO 3단계 각각이 절약하는 메모리 구성 요소를 정확히 서술
- "중복 제거(Redundancy Elimination) vs 통신 오버헤드" 트레이드오프 명시
- DeepSpeed, Megatron-LM, FSDP (Fully Sharded Data Parallel) 비교 언급

- **📢 섹션 요약 비유**: ZeRO Stage 를 올릴수록 메모리 방은 넓어지지만, 팀원끼리 파일을 주고받는 채팅 트래픽이 늘어나는 것과 같다. 적절한 Stage 선택은 "방 크기 vs 소통 비용" 의 균형점 찾기다.

---

## Ⅴ. 기대효과 및 결론

- **비용 절감**: 소규모 GPU 클러스터로 GPT-3 급 모델 학습 가능
- **확장성**: GPU 수 증가에 비례한 메모리 분산 -> 선형 확장
- **생태계**: HuggingFace Accelerate, PyTorch FSDP 에 ZeRO 아이디어 통합
- **한계**: All-Gather 통신이 빈번해 네트워크 대역폭이 병목 가능성 존재

ZeRO 는 "메모리 중복을 제거한다" 는 단순한 아이디어로 대형 언어 모델 시대의 핵심 인프라 기술이 되었다. 심화 학습에서는 Stage 별 분할 대상과 통신 패턴을 정확히 서술하고, DeepSpeed 와의 연동 방식을 언급하면 고득점이 가능하다.

- **📢 섹션 요약 비유**: ZeRO 는 "모든 팀원이 똑같은 보고서를 각자 출력해 들고 다니던" 낭비를 없애고, "한 장씩 나눠 가지되 언제든 복사 가능한" 공유 문서 시스템으로 전환한 혁신이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| ZeRO Stage 1 | 옵티마이저 상태 분할 / 최소 통신 오버헤드 분산 |
| ZeRO Stage 3 | 파라미터 분할, AllGather / 최대 메모리 절감 |
| DeepSpeed | ZeRO-Offload, ZeRO-Infinity / Microsoft 오픈소스 구현체 |
| FSDP | PyTorch 내장 ZeRO-3 유사 / Meta/PyTorch 2.0 네이티브 |
| Mixed Precision | FP16, BF16, Tensor Core / ZeRO 와 시너지 조합 |
| Gradient Checkpointing | 활성화 재계산 / 추가 메모리 절감 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [GPU VRAM 부족과 ZeRO 옵티마이저 (Zero Redundancy Optimizer)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🎒 GPU 가 들고 다닐 수 있는 가방(VRAM)에 책(모델)이 너무 많아서 넘쳐요.
2. ✂️ ZeRO 는 책을 친구들끼리 한 챕터씩 나눠 들고, 필요할 때 빌려 보는 방법이에요.
3. 📈 친구가 많을수록(GPU 수) 더 두꺼운 책도 함께 들 수 있어요!
