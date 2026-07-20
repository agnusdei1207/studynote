---
title: "vLLM PagedAttention KV Cache Optimization"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 528
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vLLM(Variable-length Large Language Model inference)의 PagedAttention은 OS 가상 메모리 페이징 개념을 KV 캐시에 적용해 GPU 메모리 단편화를 제거하고 처리량을 최대 24배 향상시킨다.
> 2. **가치**: 연속 배치(Continuous Batching)와 PagedAttention의 결합으로, 다양한 시퀀스 길이의 요청을 동적으로 스케줄링해 GPU 활용률을 획기적으로 높인다.
> 3. **판단 포인트**: vLLM의 Tensor Parallelism으로 모델을 여러 GPU에 분산하고, Pipeline Parallelism으로 레이어를 분산할 때 통신 오버헤드와 처리량 간 트레이드오프를 설계 단계에서 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

LLM 서빙의 전통적 문제: 각 요청의 KV 캐시 크기는 생성 완료 전까지 알 수 없어 과다 할당(Over-provisioning) 또는 미리 최대 시퀀스 길이만큼 연속 메모리를 예약해야 했다. 이로 인해 GPU 메모리의 <strong>20~40%가 내부 단편화(Internal Fragmentation)</strong>로 낭비됐다.

vLLM은 UC Berkeley 연구팀이 2023년 발표한 오픈소스 추론 엔진으로, PagedAttention으로 이 문제를 근본적으로 해결했다.

- **📢 섹션 요약 비유**: 호텔에서 투숙 기간을 모르는 손님에게 무조건 최대 일수분 방을 통째로 예약하던 방식에서, 필요한 만큼만 날마다 배정하는 방식으로 전환한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------+
|                 PagedAttention 구조                   |
|                                                      |
|  논리적 KV 캐시           물리적 GPU 메모리 블록       |
|  +---------------+       +-------+-------+-------+  |
|  | 요청 A        |       |Block 0|Block 3|Block 7|  |
|  | [Token 1~16]  |------►|(A:1-4)|(A:5-8)|(A:9-12)|  |
|  +---------------+       +-------+-------+-------+  |
|  +---------------+       +-------+-------+           |
|  | 요청 B        |       |Block 1|Block 4|           |
|  | [Token 1~8]   |------►|(B:1-4)|(B:5-8)|           |
|  +---------------+       +-------+-------+           |
|                          블록 테이블(Block Table) 매핑 |
+------------------------------------------------------+
```

**PagedAttention 핵심 아이디어**
1. KV 캐시를 고정 크기 블록(예: 16토큰)으로 분할
2. 요청별 논리 KV 블록 -> 물리 GPU 메모리 블록을 블록 테이블로 간접 매핑
3. 비연속 물리 메모리 사용 가능 -> 단편화 거의 제로
4. 프리픽스 캐시(Prefix Cache) 공유: 동일 시스템 프롬프트 -> 블록 공유로 메모리 재사용

<strong>연속 배치(Continuous Batching)</strong>

| 방식 | 동작 | 문제 |
|:---:|:---:|:---:|
| 정적 배치(Static Batching) | 배치 내 모든 요청 완료 후 새 요청 수용 | GPU 유휴(Idle) 시간 발생 |
| 연속 배치(Continuous Batching) | 완료된 요청 즉시 제거, 새 요청 즉시 삽입 | 높은 GPU 활용률 |

### vLLM 성능 비교

| 프레임워크 | 처리량(Throughput) | 특이사항 |
|:---:|:---:|:---|
| Naive 서빙 | 1× (기준) | 정적 배치, KV 낭비 |
| vLLM | 최대 24× | PagedAttention + 연속 배치 |
| TGI(HuggingFace) | 5~10× | Flash Attention 활용 |
| TensorRT-LLM | 10~20× | NVIDIA 최적화, 높은 복잡도 |

- **📢 섹션 요약 비유**: 연속 배치는 버스가 종점까지 기다리지 않고 내리는 승객 즉시 새 승객을 태우는 방식 — GPU가 한순간도 쉬지 않는다.

---

## Ⅲ. 비교 및 연결

### 모델 병렬화 전략

<strong>Tensor Parallelism(텐서 병렬)</strong>: 단일 레이어의 행렬을 여러 GPU에 열(Column)/행(Row) 분할
- GPU 간 All-Reduce 통신 필요 -> 동일 서버(NVLink) 내 권장
- 메모리 절감: GPU 수에 비례

<strong>Pipeline Parallelism(파이프라인 병렬)</strong>: 레이어 그룹을 GPU에 순차 배분
- 마이크로배치(Microbatch)로 버블(Bubble, 대기 시간) 최소화
- 데이터센터 간 다중 노드에 적합

| 병렬 방식 | 장점 | 단점 |
|:---:|:---:|:---:|
| Tensor Parallelism | 레이턴시 낮음 | 고속 NVLink 필수 |
| Pipeline Parallelism | 다중 노드 확장 | 파이프라인 버블 |
| 혼합(Megatron-LM) | 대규모 모델 최적 | 설계 복잡도 높음 |

- **📢 섹션 요약 비유**: 텐서 병렬은 주방 조리대를 여러 명이 나눠 쓰는 것, 파이프라인 병렬은 냉채->메인->디저트 순서대로 다른 요리사가 담당하는 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**vLLM 배포 구성 예시**

```
vllm serve meta-llama/Llama-3-70B-Instruct \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90
```

**실무자 판단 포인트**

1. **KV 캐시 용량 계획**: `--max-model-len × 배치 크기 × KV 바이트 수`로 HBM 요구량 사전 계산
2. <strong>프리픽스 캐싱 활용</strong>: RAG/챗봇에서 동일 시스템 프롬프트 -> 자동 캐시 히트 -> TTFT(Time to First Token) 단축
3. **Speculative Decoding**: 소형 Draft 모델로 토큰 후보 생성 -> 대형 모델 검증 -> Decode 처리량 2~3배 향상
4. <strong>LoRA 서빙</strong>: vLLM의 Punica 확장으로 다중 LoRA 어댑터 동시 서빙 가능

- **📢 섹션 요약 비유**: vLLM은 GPU라는 주방을 낭비 없이 24시간 풀가동하는 최고 효율 주방 관리 시스템이다.

---

## Ⅴ. 기대효과 및 결론

vLLM의 PagedAttention과 연속 배치는 LLM 서빙 인프라의 패러다임을 바꿨다. 동일한 GPU로 최대 24배 많은 요청을 처리할 수 있어 클라우드 서빙 비용이 획기적으로 절감됐다. OpenAI·Anthropic·Google 등 주요 서빙 인프라도 유사 최적화 기법을 채택했다. 향후 Speculative Decoding과 프리픽스 캐싱의 결합이 TTFT를 더욱 단축할 전망이다.

- **📢 섹션 요약 비유**: vLLM 이전 GPU 서빙은 방 하나에 손님 하나만 받던 호텔, 이후는 빈 방 없이 효율적으로 운영하는 비즈니스 호텔이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| PagedAttention | vLLM 핵심 · OS 페이징 기반 KV 캐시 |
| 연속 배치 | 처리량 최적화 · 동적 요청 스케줄링 |
| Tensor Parallelism | 모델 병렬화 · 행렬 분할 GPU 분산 |
| Pipeline Parallelism | 모델 병렬화 · 레이어 분할 GPU 분산 |
| KV 캐시 | LLM 추론 · 어텐션 Key-Value 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[vLLM 핵심 · OS 페이징 기반 KV 캐시] -> [vLLM과 PagedAttention KV 캐시 최적화] -> [LLM 추론 · 어텐션 Key-Value 저장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. AI가 대화할 때 이전 내용을 기억하는 메모장(KV 캐시)을 낭비 없이 관리하는 것이 PagedAttention이에요.
2. 메모장을 미리 왕창 예약하지 않고, 필요한 만큼만 조각조각 빌려 쓰는 방식이에요.
3. 이 덕분에 같은 GPU로 훨씬 많은 사람과 동시에 대화할 수 있어요.
