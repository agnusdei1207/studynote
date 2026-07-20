---
title: "Brain Science AI Cognitive Computing Neuro"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 788
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인간 뇌의 86B 뉴런·100T 시냅스 구조를 **뉴런 모델(LIF, Izhikevich)·시냅스 가소성(STDP, Hebbian)·인지 아키텍처(SOAR, ACT-R, LIDA)·뉴로모픽 하드웨어(Intel Loihi 2, IBM TrueNorth, SpiNNaker)** 4계층으로 모방하여, 폰노이만 병목을 제거한 **In-Memory Computing**과 **Event-Driven Spiking**으로 구현하는 통합 패러다임.
> 2. **가치**: GPU 대비 **에너지 효율 1,000배 이상**(Loihi 2: 15mW/코어, GPU: 300W), **지연 시간 100ms -> 1ms** 실시간 추론, Neuro-Symbolic 결합으로 **학습 데이터 1/1000**로 동등 추론 정확도 달성, IBM Watson 기준 의료 진단 30% 정확도 향상.
> 3. **판단 포인트**: ①**생물학적 충실도 vs 실용성**(Hodgkin-Huxley 4차 미분방정식 vs 단순 LIF), ②**Rate Coding vs Temporal Coding**(정밀도 vs 지연), ③**Symbolic vs Connectionist vs Neuro-Symbolic**, ④**온디바이스 vs 클라우드 엣지**, ⑤**Spike 호환성**(기존 DNN 모델의 SNN 변환 시 정확도 손실 5~30%) 트레이드오프.

---

## Ⅰ. 개요 및 필요성

딥러닝의 폭발적 성장에도 불구하고, GPU/TPU 기반 시스템은 **폰노이만 아키텍처의 메모리-연산 분리 병목**으로 인해 막대한 에너지를 소비합니다. GPT-4 학습에 약 50GWh(원자력 1기 6시간 발전량), ResNet-50 추론 1회 0.5J(뇌 시각처리 0.0001J 대비 5,000배)이라는 비효율이 발생합니다. 반면 인간 뇌는 **20W** 전력으로 **86B 뉴런, 100T 시냅스**가 병렬 동작하며, Edge에서 실시간 학습·추론·판단을 수행합니다.

기존 AI 패러다임의 한계는 다음과 같습니다:
- **데이터 의존성**: GPT-3 175B 파라미터 학습에 45TB 텍스트 코퍼스 필요 -> 인간은 5살까지 약 5M 단어만으로 언어 습득
- **에너지 비효율**: AlphaGo 1,920 CPU + 280 GPU, 1MW 소비 vs 인간 바둑기사 20W
- **일반화 실패**: Distribution shift 시 성능 급락, 인과 추론·상식 판단 불가
- **설명가능성 부재**: Black-box 추론으로 의료·법률·금융 적용 한계

**뇌모방 AI 인지컴퓨팅**은 신경과학(Neuroscience)·인지심리학(Cognitive Psychology)·컴퓨터공학의 융합으로, 뇌의 **예측 코딩(Predictive Coding)**, **자유에너지 원리(Free Energy Principle)**, **글로벌 워크스페이스 이론(Global Workspace Theory)**을 하드웨어·소프트웨어·아키텍처 3축으로 구현합니다.

```text
+------------------------------------------------------------------+
|          Brain-Inspired AI 4-Layer Reference Stack                |
+------------------------------------------------------------------+
|                                                                   |
|  +-----------------------------------------------------------+   |
|  | L4. Cognitive Architecture (인지 아키텍처, 상위)            |   |
|  | +------+ +------+ +------+ +------+ +------+ +--------+  |   |
|  | |SOAR  | |ACT-R | | LIDA | |CLARION| |Sigma | | ICARUS |  |   |
|  | +------+ +------+ +------+ +------+ +------+ +--------+  |   |
|  |   Production Rules, Declarative Memory, Attention,         |   |
|  |   Episodic Buffer, Consciousness Cycle (40Hz)              |   |
|  +-----------------------╤-----------------------------------+   |
|                          |  Neuro-Symbolic Bridge                |
|  +-----------------------╧-----------------------------------+   |
|  | L3. Neuro-Symbolic & Cognitive Algorithm Layer             |   |
|  | +----------+ +--------------+ +----------+ +------------+ |   |
|  | | Logic    | | DeepProbLog  | |  NARS    | |  Nengo     | |   |
|  | | Tensor   | | (ProbLog+NN) | |(Non-Axiom| | (SNN+Symbol)| |   |
|  | | Network  | |              | | Reasoning)| |            | |   |
|  | +----------+ +--------------+ +----------+ +------------+ |   |
|  |   First-Order Logic + Gradient Learning + Causal Inference |   |
|  +-----------------------╤-----------------------------------+   |
|                          |  Spike Encoding / AER Protocol        |
|  +-----------------------╧-----------------------------------+   |
|  | L2. Spiking Neural Network (SNN) Layer                     |   |
|  |  Encoding: Rate / Temporal / Population / Burst Coding     |   |
|  |  Neuron:  LIF / Izhikevich / Adaptive Exponential (AdEx)   |   |
|  |  Plasticity: STDP / Hebbian / BCM / Reward-modulated STDP  |   |
|  |  Topology: FFN / Recurrent (LSTM-like) / Reservoir / STDP  |   |
|  +----------------------