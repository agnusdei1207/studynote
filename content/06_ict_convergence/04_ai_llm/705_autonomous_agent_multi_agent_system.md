---
title: "Autonomous Agent Multi-Agent System"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 705
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 자율 에이전트(Autonomous Agent)는 LLM을 추론 엔진(Reasoning Engine)으로 사용하여 **계획(Planning) -> 행동(Action) -> 관찰(Observation)** 사이클을 자율 반복하는 개체이며, 멀티에이전트 시스템(MAS, Multi-Agent System)은 FIPA-ACL, MCP, A2A 같은 **에이전트 통신언어(ACL)** 와 계약망(Contract Net), Supervisor, Blackboard 같은 **조정 메커니즘(Orchestration)** 을 통해 개별 에이전트들의 BDI(Belief-Desire-Intention) 모델을 공유·협상하게 함으로써 단일 LLM의 컨텍스트 윈도우(예: 128K~1M token) 한계를 **역할 분할(Role Specialization)** 과 **상호 검증(Peer Verification)** 으로 돌파하는 분산 인지 아키텍처이다.
> 2. **가치**: Microsoft AutoGen·LangGraph·CrewAI·MetaGPT 등 프레임워크 도입 기업에서 SWE-bench Lite 13.86%->43.8% 향상, 복잡한 리서치/코딩 작업의 **라운드트립 시간 60~80% 단축**, 단일 모델 대비 **할루시네이션 검출률 35~50% 향상**(Self-Consistency + Multi-Agent Debate 기반), 그리고 n8n/Airflow 같은 정적 워크플로우로 불가능했던 비정형 의사결정 자동화가 가능하다.
> 3. **판단 포인트**: 에이전트 간 메시지 라우팅 오버헤드(Latency p50 2.3s -> p95 18.7s 급증), 토큰 비용의 기하급수적 증가(에이전트 4개 협업 시 단일 대비 5.7배), 에이전트 실패 전파(Failure Propagation)와 신뢰성, 그리고 인간 개입 지점(Human-in-the-Loop) 설계가 핵심 트레이드오프이며, **Supervisor 중앙집중형 vs P2P 분산형**, **동기 vs 비동기 메시지 패싱** 선택이 아키텍처의 확장성과 디버거빌리티를 결정한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의와 등장 배경

**자율 에이전트(Autonomous Agent)** 란 "주어진 목표(Goal)를 달성하기 위해 환경(Environment)을 지각(Perception)하고, 스스로 계획을 수립(Planning)·실행(Action)하며, 그 결과를 평가(Observation)하는 소프트웨어 개체"를 의미한다. Wooldridge & Jennings(1995)의 정형적 정의에 따르면, 에이전트는 다음 4가지 속성을 반드시 만족해야 한다.

- **자율성(Autonomy)**: 인간의 직접 개입 없이 스스로 의사결정
- **사회성(Social Ability)**: ACP(Agent Communication Protocol)로 다른 에이전트와 상호작용
- **반응성(Reactivity)**: 환경 변화에 실시간 대응
- **능동성(Pro-activeness)**: 단순 반응이 아닌 목표 지향적 행동 개시

**멀티에이전트 시스템(MAS, Multi-Agent System)** 은 이러한 에이전트 둘 이상이 공통의 또는 경쟁하는 목표를 가지고 **조정(Coordination)·협조(Cooperation)·협상(Negotiation)·경쟁(Competition)** 을 수행하는 시스템이다. 2022년 11월 ChatGPT 등장 이후, LLM(특히 GPT-4, Claude 3.5 Sonnet, Llama 3.1 405B)을 **추론 엔진**으로 사용하는 LLM-Agent가 각광받으면서, 단일 에이전트의 한계를 극복하기 위한 MAS 패턴이 Microsoft, Google, Anthropic 등 빅테크의 표준 아키텍처로 자리잡았다.

### 1.2 단일 에이전트의 한계

| 한계 유형 | 구체적 수치/현상 | 영향 |
| :--- | :--- | :--- |
| **컨텍스트 윈도우** | GPT-4 Turbo 128K, Claude 3.5 Sonnet 200K, Gemini 1.5 Pro 2M | 장기 프로젝트에서 컨텍스트 손실/축약 발생 |
| **단일 관점 편향** | 단일 시스템 프롬프트 -> 도메인 특화 지식 한계 | 복합 도메인(예: 의료+법률) 처리 불가 |
| **자기 검증 불가** | Self-Consistency는 동일 모델 반복샘플링에 의존 | 할루시네이션(Hallucination) 자체 검증 한계 |
| **도구 사용 폭주** | 단일 에이전트가 30+ Tool을 보유 시 선택 정확도 급감 | Tool Routing 오류율 증가 |
| **단일 장애점(SPOF)** | 에이전트 실패 시 전체 작업 중단 | 신뢰성 저하 |

### 1.3 시스템 아키텍처 컨셉

```text
+----------------------------------------------------------------------+
|           LLM-Based Multi-Agent System Conceptual Model              |
|                                                                      |
|   +----------+   Goal    +-------------------------------------+    |
|   |  Human / | --------► |        Orchestrator (Supervisor)    |    |
|   |  Trigger |           |  +-------+ +--------+ +--------+  |    |
|   +----------+           |  |Planner|->|Router  |->|Monitor |  |    |
|                          |  +-------+ +--------+ +--------+  |    |
|                          +-----+---------+---------+---------+    |
|                                | ACL     | ACL     | ACL           |
|                                v         v         v              |
|   +---------------------------------------------------------+     |
|   |              Agent Society (에이전트 사회)              |     |
|   |  +---------+  +---------+  +---------+  +---------+   |     |
|   |  |Research |  |Coder    |  |Reviewer |  |Critic   |   |     |
|   |  |Agent    |◄►|Agent    |◄►|Agent    |◄►|Agent    |   |     |
|   |  |(GPT-4o) |  |(Claude) |  |(Llama)  |  |(GPT-4o) |   |     |
|   |  +----+----+  +----+----+  +----+----+  +----+----+   |     |
|   |       | Tool Use   | Sandbox   | Static Anl | Debate   |     |
|   |       v            v           v             v          |     |
|   |  [Web Search]  [Python REPL]  [ESLint]   [Self-Check]  |     |
|   +---------------------------------------------------------+     |
|                                |                                    |
|                                v                                    |
|   +----------------------------------------------------------+    |
|   |   Shared Memory & Knowledge Layer (공유 인지 자원)       |    |
|   |  +--------------+  +--------------+  +--------------+   |    |
|   |  | Vector DB    |  | Blackboard   |  | Episodic     |   |    |
|   |  | (Pinecone)   |  | (Redis)      |  | Log (Postgres|   |    |
|   |  | Long-term    |  | Working Mem  |  | Audit Trail) |   |    |
|   |  +--------------+  +--------------+  +--------------+   |    |
|   +----------------------------------------------------------+    |
|                                                                      |
|   Communication Protocols: FIPA-ACL, MCP (Anthropic), A2A (Google) |
|   Coordination: Contract Net, Auction, Consensus, Supervisor, P2P   |
+----------------------------------------------------------------------+
```

### 1.4 패러다임 전환: From Pipeline to Agentic

| 구분 | 전통 RPA/Workflow | LLM 단일 에이전트 | LLM 멀티에이전트 |
| :--- | :--- | :--- | :--- |
| **결정 방식** | 정적 If-Then 룰 | LLM 단독 추론 | 다수 LLM 협업/경쟁 |
| **비정형 처리** | 불가 (OCR 후 매핑) | 가능하나 컨텍스트 한계 | 역할 분담으로 확장 |
| **실패 대응** | 사전 정의된 예외 분기 | 자체 Replan | Peer Review + Voter |
| **확장성** | 스크립트 추가 | 프롬프트 튜닝 | 에이전트 추가/교체 |
| **대표 도구** | UiPath, Airflow | Auto-GPT, BabyAGI | AutoGen, LangGraph, CrewAI |

- **📢 섹션 요약 비유**: 단일 에이전트는 "한 명의 천재가 모든 문제를 혼자 푸" 것이고, 멀티에이전트는 "각 분야 전문가 5명이 화상회의로 협업"하는 것이니, 연구원은 리서치하고 개발자는 코딩하며 비서는 회의록을 정리하듯 **역할 분리(Role Specialization)** 가 MAS의 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 에이전트 내부 아키텍처 (ReAct / ReWOO / Reflexion)

LLM 에이전트의 핵심은 **인지 루프(Cognitive Loop)** 다. 2022년 Yao et al.이 제안한 ReAct(Reasoning + Acting) 패턴이 사실상 표준이며, 이를 확장한 변형들이 존재한다.

```text
+----------------------------------------------------------------------+
|         LLM Agent Internal Loop (ReAct + Reflexion)                 |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  |  Step 1: Thought (추론)                                      |   |
|  |  Thought: "사용자가 2023 매출액을 묻는다. CSV 파일 확인 필요"|   |
|  +--------------------------------------------------------------+   |
|                              |                                       |
|                              v                                       |
|  +--------------------------------------------------------------+   |
|  |  Step 2: Action (행동)                                       |   |
|  |  Action: tool_call(read_csv, {"path": "sales_2023.csv"})     |   |
|  +--------------------------------------------------------------+   |
|                              |                                       |
|                              v                                       |
|  +--------------------------------------------------------------+   |
|  |  Step 3: Observation (관찰)                                   |   |
|  |  Observation: "2023 Q1: 1.2억, Q2: 1.5억, Q3: 1.8억, Q4..." |   |
|  +--------------------------------------------------------------+   |
|                              |                                       |
|                              v                                       |
|  +--------------------------------------------------------------+   |
|  |  Step 4: Reflection (반성, Reflexion - Shinn 2023)           |   |
|  |  Reflection: "Q4 누락 가능성 체크 필요, 재조회 여부 결정"    |   |
|  +--------------------------------------------------------------+   |
|                              |                                       |
|              +---------------+---------------+                      |
|              v                               v                      |
|       +--------------+              +--------------+                |
|       | Final Answer |              |  Re-Loop     |                |
|       | Return       |              | (max 10 iter)|                |
|       +--------------+              +--------------+                |
|                                                                      |
|   Memory Stack: Working(8K ctx) + Episodic(Redis) + Semantic(Vector)|
|   Tool Belt: [search, calculator, code_exec, file_io, sql_query]    |
+----------------------------------------------------------------------+
```

### 2.2 멀티에이전트 토폴로지 (Topology)

**가. Supervisor (중앙집중형)**
- 한 개의 Supervisor 에이전트가 작업 분해, 라우팅, 결과 통합
- 장점: 제어 용이, 디버깅 단순
- 단점: Supervisor 자체가 SPOF, 병목

**나. Hierarchical (계층형)**
- CEO Agent -> Manager Agent -> Worker Agent
- MetaGPT의 Software Company 시뮬레이션이 대표 사례

**다. Peer-to-Peer (P2P, 동등형)**
- 모든 에이전트가 동등, AutoGen GroupChat이 대표
- 장점: 단일 장애점 없음
- 단점: 무한 루프 위험, 합의 도출 어려움

**라. Blackboard (공유 게시판형)**
- 에이전트들이 공유 Blackboard(메모리)를 읽고/쓰며 협업
- 고전 MAS(Hearsay-II, OpenCCS)에서 사용, 현대에는 Redis Pub/Sub로 구현

**마. Contract Net Protocol (CNP)**
- Manager가 작업 공고(CFP, Call For Proposal) -> Worker가 입찰(Bid) -> Manager가 낙찰(Award)
- 작업량이 동적인 분산 시스템에 적합

```text
+----------------------------------------------------------------------+
|        Multi-Agent Coordination Pattern: Contract Net               |
|                                                                      |
|  Manager Agent              Worker Pool                              |
|      |                                                             |
|      |  (1) CFP: "PDF 1000건 번역 필요"                             |
|      +------------------► +----------+                              |
|      |                    |Worker A  | Bid: 5s/doc, capacity