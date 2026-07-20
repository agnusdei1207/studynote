---
title: "Prompt Engineering Chain of Thought"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 647
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Chain-of-Thought(CoT)는 LLM이 최종 답안을 도출하기 전 **명시적 중간 추론 단계(intermediate reasoning steps)** 를 토큰 단위로 생성하도록 유도하는 프롬프트 엔지니어링 기법으로, 2022년 Google Research의 Wei et al.이 NeurIPS에서 공개한 "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" 논문에서 체계화되었으며, Arithmetic(GSM8K), Commonsense(CSQA), Symbolic(Last Letter) 등 다중 벤치마크에서 SOTA를 달성한 핵심 기법임.
> 2. **가치**: PaLM 540B 모델 기준 GSM8K 정확도를 **17.9% -> 56.5%**(≈3.16배), MATH 데이터셋에서 **8.8% -> 33.2%**(≈3.77배) 향상시킨 실증 결과가 있으며, 별도 fine-tuning 없이 emergent ability scale-up만으로도 reasoning 성능이 비약적으로 개선되어 fine-tuning 대비 **학습 비용 0원, 배포 즉시 적용 가능**한 inference-time scaling의 대표 사례로 자리매김함.
> 3. **판단 포인트**: CoT는 **토큰 소비량 2~5배 증가, 추론 지연(latency) 1.5~3배 증가, 중간 hallucination 위험**이라는 트레이드오프를 수반하므로, (a) 모델 파라미터 ≥ 62B급의 emergent reasoning capability 가정, (b) 단계 분해가 가능한 문제 도메인, (c) self-consistency·verification 모듈 부착 여부, (d) Program-of-Thoughts(코드 실행 기반) 전환 가능성 검토가 설계 시 핵심 의사결정 포인트임.

---

## Ⅰ. 개요 및 필요성

대규모 언어 모델(LLM, 예: GPT-4, Claude 3.5 Sonnet, Gemini 1.5 Pro, PaLM 2, LLaMA 3.1 405B)은 자연어 이해·생성에서 인간 수준에 근접한 성능을 보이나, **다단계 추론(multi-step reasoning), 산술 연산, 기호 조작(symbolic manipulation), 인과 추론**이 필요한 문제에서는 여전히 취약점을 보인다. 이는 사전학습(pretraining) 시 next-token prediction objective가 **"정답 자체"가 아닌 "다음 토큰의 가능도"** 만을 최적화하기 때문이며, 결과적으로 모델은 "올바른 답으로 가는 경로"를 학습하지 못하고 **"그럴듯한 답(likely answer)"** 만 생성하는 경향이 있다.

예를 들어, GPT-3 175B에 "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?"라는 GSM8K 스타일 문제를 표준 프롬프트로 던지면 단순 패턴 매칭에 그쳐 11(정답: 5+2×3=11)이 아닌 다른 숫자를 산출한다. Wei et al.(2022)은 이 현상의 원인을 LLM이 **implicit reasoning**을 수행할 수 있는 표현력은 있으나 **explicit reasoning을 외부로 표출할 output format이 부재**한 점으로 진단했고, 이를 해결하기 위해 few-shot exemplars에 **"질문 -> 사고 과정(chain of thought) -> 정답"** 구조를 삽입하는 **Chain-of-Thought Prompting**을 제안했다.

```text
[기존 표준 프롬프트 vs Chain-of-Thought 프롬프트 비교]

   [Standard Prompting]                      [Chain-of-Thought Prompting]
   +---------------------+                    +-----------------------------+
   | Q: Roger has 5 ...  |                    | Q: Roger has 5 tennis balls |
   | A: The answer is 11 |  ❌ 단순 매칭        | He buys 2 more cans...      |
   |   (실제: 27% 오답)   |                    | A: Roger started with 5 ... |
   +---------------------+                    |   2 cans × 3 balls = 6 ...  |
                                              |   5 + 6 = 11.               |
                                              |   The answer is 11. ✅      |
                                              +-----------------------------+
                                                    |
                                                    v
                              [Emergent Reasoning Path]
                  "큰 모델일수록 단계 분해 능력이 emergent하게 발현"
                  (PaLM 8B < PaLM 62B < PaLM 540B 효과 검증)
```

기존 **standard prompting**은 question -> answer의 1-shot 매핑만 학습 가능한 반면, **CoT prompting**은 question -> {reasoning_1, reasoning_2, ..., reasoning_n} -> answer의 **k-shot decomposition**을 가능하게 한다. 이는 곧 (1) 계산 가능한 문제의 단계별 분해(Decomposability), (2) 모델이 자기 추론 과정을 self-explanation으로 검증할 기회 제공, (3) intermediate state를 외부 시스템(검증기, 코드 실행기, 검색 API)이 점검할 수 있는 **관측 가능성(observability)** 을 부여한다는 점에서 엔터프라이즈 LLM 시스템의 핵심 설계 패턴이 되었다.

- **📢 섹션 요약 비유**: CoT는 **"환자 진료 과정"** 과 같다. 응급실에서 "배가 아파요"라는 한마디만 듣고 바로 처방하는 일반의(standard prompting)와 달리, 좋은 내과 의사는 **"언제부터, 어디가, 어떤 통증, 동반 증상, 식이·생활 패턴, 가족력..."** 을 순차적으로 묻고 문진표를 작성한 뒤(중간 추론 단계) 진단을 내린다. 그 문진표 자체가 chain of thought이며, 진단의 정당성과 검증 가능성을 동시에 확보한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CoT 기반 추론 시스템은 단순 프롬프트 기법을 넘어 **검증·분해·통합 모듈이 결합된 다층 아키텍처**로 진화했다. Kojima et al.(2022)의 **Zero-shot CoT**는 "Let's think step by step"이라는 마법의 문장(magic phrase)만으로 few-shot 예시 없이도 CoT를 트리거할 수 있음을 보였고, 이를 기점으로 CoT는 **few-shot CoT, Zero-shot CoT, Self-Consistency, Tree of Thoughts, ReAct, Program-of-Thoughts, Least-to-Most, Auto-CoT, Reflexion, IRCoT** 등으로 분화되었다.

```text
[CoT 기반 엔터프라이즈 추론 아키텍처]

  +--------------------------------------------------------------------+
  |  ① Problem Input Layer                                            |
  |  +--------------+   +--------------+   +----------------------+    |
  |  | User Query   | -> | Pre-processor| -> | Tokenizer + Context   |    |
  |  | (자연어/JSON)|   | (PII 마스킹, |   | Window Manager        |    |
  |  |              |   |  정규화)     |   | (e.g., 200K tokens)   |    |
  |  +--------------+   +--------------+   +----------------------+    |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  |  ② Prompt Template Composer (Few-shot + Zero-shot 하이브리드)     |
  |  +------------------------------------------------------------+    |
  |  | [System]  You are an expert reasoner. Think step by step.  |    |
  |  | [Demo 1]  Q->CoT1->A1  (8-shot exemplars)                   |    |
  |  | [Demo 2]  Q->CoT2->A2                                       |    |
  |  | [Query]   User question                                    |    |
  |  +------------------------------------------------------------+    |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  |  ③ LLM Inference Engine (Transformer-based)                       |
  |  +--------------------+    +------------------------------+       |
  |  |  Self-Attention    | ->  |  Intermediate Token Stream    |       |
  |  |  (KV-cache 활성)   |    |  ("Step 1: ... Step 2: ...")  |       |
  |  +--------------------+    +------------------------------+       |
  |                                       |                            |
  |       temperature=0.0 (deterministic)| temperature=0.7 (CoT-SC)   |
  |       1 path only                    | N=40 sampled paths         |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  |  ④ Verification & Aggregation Layer                               |
  |  +--------------+  +--------------+  +---------------------+       |
  |  | Process      |  | Outcome      |  | Majority Vote       |       |
  |  | Reward Model |  | Reward Model |  | (Self-Consistency)  |       |
  |  | (PRM)        |  | (ORM)        |  |                     |       |
  |  +--------------+  +--------------+  +---------------------+       |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  |  ⑤ Tool-Augmented Reasoning (ReAct, Program-of-Thoughts)          |
  |  +----------+   +----------+   +----------+   +--------------+     |
  |  | Python   |   | Search   |   | Database |   | Function     |     |
  |  | Sandbox  |   | (RAG)    |   | (SQL)    |   | Call (API)   |     |
  |  +----------+   +----------+   +----------+   +--------------+     |
  +--------------------------------------------------------------------+
                                  |
                                  v
  +--------------------------------------------------------------------+
  |  ⑥ Output Formatter (JSON Schema / Function Call / Streaming)     |
  |  { "reasoning": "...", "answer": "...", "confidence": 0.93 }      |
  +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Problem Input Layer** | 사용자 질의 정규화, 컨텍스트 윈도우 관리 | PII 마스킹(NER 모델), 토큰 절약형 summarization, Long-context 모델(Gemini 1.5 Pro 2M, Claude 3.5 200K) 활용 |
| **② Prompt Template Composer** | Few-shot exemplars + zero-shot 트리거 결합 | "Let's think step by step"(Kojima 2022), 8-shot CoT demonstrations(Wei 2022), Auto-CoT로 클러스터별 대표 exemplars 자동 생성(Zhang 2022) |
| **③ LLM Inference Engine** | 다중 추론 경로 생성 | Temperature=0.0(단일 결정론), Temperature=0.7 + N=40 sampling(Self-Consistency), Top-p=0.95 nucleus sampling, KV-cache로 prefix 재사용 |
| **④ Verification Layer** | 추론 경로의 충실성(faithfulness)·정합성 검증 | Process Reward Model(PRM, 단계별 채점), Outcome Reward Model(ORM, 최종 답만 채점), Critic Model(Reflexion, 자기 반성), majority voting |
| **⑤ Tool-Augmented Layer** | 외부 도구 호출로 LLM 한계 보완 | ReAct(Yao 2022): Thought-Action-Observation 루프, Program-of-Thoughts(Chen 2022): Python 코드 생성·실행, IRCoT: Retrieval interleaved with CoT |
| **⑥ Output Formatter** | 구조화된 응답으로 후속 시스템 연동 | JSON mode(OpenAI), function calling, Pydantic schema 검증, streaming(SSE) with reasoning token 분리 출력 |

핵심 알고리즘적 세부사항을 짚자면, **Self-Consistency**(Wang et al., 2022)는 동일 prompt에 대해 temperature ≥ 0.7로 N개(보통 40개)의 추론 경로를 sampling한 뒤 **marginalize out the reasoning**하여 최종 답의 **majority vote**를 취한다. GSM8K 기준 PaLM 540B가 single-path CoT 대비 +17.9% p, 다수결만으로 +12.2% p 추가 향상을 보였다. **Tree of Thoughts(ToT)**(Yao et al., 2023)는 BFS/DFS로 **thought space를 명시적 트리 탐색**하며, Game of 24에서 GPT-4 + To