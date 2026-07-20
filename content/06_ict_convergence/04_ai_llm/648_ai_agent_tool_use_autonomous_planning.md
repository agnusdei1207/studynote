---
title: "AI Agent Tool Use Autonomous Planning"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 648
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM(대규모언어모델)을 추론 엔진으로 사용하되, **Reasoning(생각) ↔ Acting(도구호출) ↔ Observation(결과관찰)** 루프를 반복 수행하여 다단계 작업을 자율적으로 분해·계획·실행하는 **에이전트 오케스트레이션 패턴**(ReAct, Plan-and-Execute, ReWOO, Reflexion 등)이며, 핵심 메커니즘은 **Function Calling(Structured I/O)**과 **MCP(Model Context Protocol)** 기반의 표준화된 도구 인터페이스이다.
> 2. **가치**: 단일 LLM 추론으로는 불가능한 **실시간 데이터 조회, 트랜잭션 실행, 코드 인터프리터, 외부 시스템 제어**가 가능해져, 복잡한 업무 자동화에서 **작업 성공률 30~70% 향상**(Yao et al. 2023 ReAct 기준) 및 **운영비용 40~60% 절감**(고객지원·SRE 도메인 측정값)을 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **①도구 호출 신뢰성 vs 도구 개수(할루시네이션 지수함수적 증가)**, **②계획 정밀도(Plan-and-Execute) vs 적응성(ReAct)**, **③토큰 비용·지연시간 vs 작업 성공률**, **④보안 샌드박스 vs 기능 확장성**이며, 실무적 판단 기준은 **도메인 결정성(Determinism)**, **에러 전파 한계 설계**, **관측가능성(Tracing) 인프라** 확보 여부이다.

---

## Ⅰ. 개요 및 필요성

기존 LLM(ChatGPT 초기)은 **학습 데이터 cutoff** 이후의 정보를 알지 못하며, **사칙연산·DB 조회·API 호출·파일 조작** 등 시스템-외부 액션이 불가능하다는 근본적 한계가 있다. 사용자가 "내일 서울 날씨에 맞춰 우산 추천해줘"라고 요청하면, LLM은 그럴듯한 텍스트를 생성(환각, Hallucination)할 뿐 실제 API를 호출하지 못한다.

**AI 에이전트 도구 사용 자율 계획(Agentic Tool Use & Autonomous Planning)** 은 LLM을 **두뇌(CPU)**로, 외부 도구들을 **손발(I/O Device)**로 비유할 수 있는 아키텍처이다. LLM이 스스로 **"무엇을(계획) -> 어떤 도구로(선택) -> 어떻게(파라미터) -> 결과가 옳은가(검증)"** 를 동적으로 결정하는 메타-인지 루프를 구현한다. 이는 2022년 ReAct 논문(Yao et al., ICLR 2023) 이후 급속 발전하여, 2024년 OpenAI Function Calling, 2024년 Anthropic Model Context Protocol(MCP), 2025년 OpenAI Agents SDK로 산업 표준이 정착되었다.

**기존 vs 신규 패러다임 비교**

| 항목 | 정적 LLM (Pre-2022) | 에이전틱 LLM (2022~) |
| :--- | :--- | :--- |
| 데이터 소스 | 학습 시점 스냅샷만 | 실시간 API·DB·웹 |
| 액션 수행 | 불가 (텍스트만 생성) | 도구 호출로 시스템 변경 |
| 계획 방식 | 단일 forward pass | 다단계 추론-행동 루프 |
| 에러 처리 | N/A | Self-Reflection, Re-planning |
| 인터페이스 | 자연어 입력 | 자연어 + 구조화 함수 호출 |

```text
        +-------------------------------------------------------------+
        |   기존 LLM 패러다임          신규 Agentic 패러다임          |
        |   +----------+               +----------+                  |
        |   | 사용자 ---> LLM ---> 텍스트 |  사용자 ---> Planner(LLM)   |
        |   +----------+               |            |                |
        |                              |   +--------v--------+       |
        |                              |   | Tool Registry   |       |
        |                              |   | • Search API    |       |
        |                              |   | • Code Interp.  |       |
        |                              |   | • DB Query      |       |
        |                              |   | • File System   |       |
        |                              |   +--------+--------+       |
        |                              |            |                |
        |                              |   +--------v--------+       |
        |                              |   | Executor->Result |       |
        |                              |   |  -> Reflection   |       |
        |                              |   +-----------------+       |
        |                              +-----------------------------+
```

- **📢 섹션 요약 비유**: LLM이 시험에 답만 적는 **수험생**이었다면, 에이전트는 **교과서도 들고보고 계산기도 두드리고 답안도 제출하는 시험관**이 된 것이다. 어떤 도구를 언제 쓸지 스스로 판단한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

에이전트의 핵심 아키텍처는 **인지 루프(Cognitive Loop)** 라고 불리는 4단계 사이클이다: **①Perceive(지각) -> ②Plan(계획) -> ③Act(실행) -> ④Reflect(관찰)**. 이 사이클은 LLM의 Chain-of-Thought(CoT) 프롬프팅을 구조화한 **ReAct(Reason+Act)** 패턴이 기반이며, 여기에 메모리·플래너·툴 레지스트리가 결합된다.

**상세 아키텍처 다이어그램**

```text
   +--------------------------------------------------------------------+
   |                    AI Agent Autonomous Planning System              |
   +--------------------------------------------------------------------+
   |                                                                    |
   |  +----------+    +--------------+    +--------------+             |
   |  |  USER    |---->|  PLANNER     |---->| TOOL REGISTRY|             |
   |  |  GOAL    |    |  (LLM Core)  |    | (MCP Server) |             |
   |  +----------+    +------+-------+    +------+-------+             |
   |       ^                 | ReAct Loop         |                     |
   |       |            +----v-----+              |                     |
   |       |            |  MEMORY  |              |                     |
   |       |            | • Short  |              |                     |
   |       |            | • Long   |              |                     |
   |       |            | • Episodic|             |                     |
   |       |            +----+-----+              |                     |
   |       |                 |                    |                     |
   |       |            +----v------+   function_call  +----------+   |
   |       |            | EXECUTOR  |------------------>|  TOOLS   |   |
   |       |            | (Sandbox) |<------result------| • API    |   |
   |       |            +----+------+                  | • DB     |   |
   |       |                 |                         | • Code   |   |
   |       |            +----v------+                  | • Browser|   |
   |       +------------|REFLECTOR  |                  +----------+   |
   |                    | (Critic)  |                                  |
   |                    +-----------+                                  |
   +--------------------------------------------------------------------+
```

**ReAct 프롬프트 패턴 상세**

```
Thought 1: 사용자가 "오늘 환율 기준 USD->KRW 환산"을 요청했다. 환율은 실시간 데이터이므로 학습 데이터에 없으므로 도구 호출이 필요하다.
Action 1: exchange_rate_api(base="USD", target="KRW")
Observation 1: {"rate": 1342.5, "timestamp": "2025-01-15T10:00:00Z"}
Thought 2: 환율을 얻었다. 이제 사용자가 입력한 금액을 곱해야 한다. 산술 연산이므로 코드 인터프리터 호출.
Action 2: python_calc(expression="100 * 1342.5")
Observation 2: 134250
Thought 3: 결과를 사용자에게 자연어로 반환하면 작업 완료.
Final Answer: 오늘(2025-01-15) USD->KRW 환율 1,342.5원 기준으로 $100은 134,250원입니다.
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Planner (계획자)** | 작업을 DAG(Directed Acyclic Graph) 형태의 서브태스크로 분해 | **Plan-and-Execute**, **ReWOO**(추론-가중치 분리), **Tree of Thoughts(ToT)**, LLM-as-a-Planner |
| **Tool Registry (도구 카탈로그)** | 사용 가능한 도구의 메타데이터·스키마·권한 관리 | **OpenAPI 3.1 Schema**, **JSON Schema**, **Anthropic MCP Server**, **OpenAI Function Calling JSON** |
| **Executor (실행기)** | LLM 출력의 함수 호출 부분을 파싱·검증·실행 | **Function Call Parser**(JSON mode), **Sandbox**(gVisor/Firecracker), **Rate Limiter**, **Retry/Backoff** |
| **Memory (기억)** | 단기 작업 컨텍스트·장기 사용자 선호도·에피소드 학습 | **Scratchpad**(in-context), **Vector DB**(Pinecone/Weaviate), **Episodic Store**, **LangGraph State** |
| **Reflector (평가자)** | 실행 결과의 정합성·완전성 평가 및 재계획 트리거 | **ReAct Self-Critique**, **Reflexion**(verbal reinforcement), **Self-Refine**, **Constitutional AI** |

**핵심 알고리즘 의사코드**

```python
def agent_loop(user_goal, max_iter=10):
    state = {"goal": user_goal, "history": [], "memory": load_memory()}
    plan = planner.decompose(user_goal)              # Plan 단계

    for step in plan:
        for i in range(max_iter):
            thought = llm.reason(state)                # Reasoning
            tool_call = llm.select_tool(thought,      # Action 선택
                                       tools=registry.list())
            if tool_call is None:
                return llm.generate_answer(state)

            try:
                result = executor.run(tool_call)       # 실행
            except ToolError as e:
                result = f"ERROR: {e}"

            state["history"].append({                  # Observation
                "thought": thought,
                "action": tool_call,
                "result": result
            })

            if reflector.is_satisfactory(result, goal):
                break                                  # 조기 종료
            else:
                plan = replanner.adjust(plan, state)    # Re-plan

    return llm.synthesize_final_answer(state)
```

**핵심 파라미터 및 튜닝 포인트**
- **Temperature**: 도구 선택 시 `0.0`(결정적), 응답 생성 시 `0.7`(창의성) 분리
- **Max Iterations**: 5~15 (무한루프 방지, 토큰 폭증 차단)
- **Context Window**: 평균 ReAct 트리거 시 4K~32K 토큰 (GPT-4o 128K, Claude 3.5 200K)
- **Tool Description Length**: 50~200 토큰/도구 (길수록 성능^, 그러나 토큰 비용^)
- **Reflexion Triggers**: 3회 연속 동일 에러 시 사람 개입(Human-in-the-Loop)

- **📢 섹션 요약 비유**: 에이전트는 **셰프**와 같다. 손님(사용자) 주문을 듣고 -> **레시피를 계획**(Planner)하고 -> **재료를 꺼내고**(Tool Registry) -> **조리하고**(Executor) -> **맛을 보고**(Reflector) 부족하면 양념을 더한다. 이 과정을 자동화한 것이다.

---

## Ⅲ. 비교 및 연결

**계획 패턴별 비교**

| 구분 | ReAct | Plan-and-Execute | ReWOO | Reflexion |
| :--- | :--- | :--- | :--- | :--- |
| **계획 시점** | 매 액션마다 | 작업 시작 시 1회 | 작업 시작 시 1회 | 매 액션 후 재계획 |
| **도구 호출 횟수** | 많음 (3~10회) | 적음 (1~3회) | 적음 (병렬 가능) | 많음 (반복) |
| **컨텍스트 비용** | 높음 | 낮음 (계획만 LLM) | 매우 낮음 (도구 결과 미저장) | 매우 높음 |
| **적응성** | 높음 (실시간 조정) | 낮음 (사후 실패 시) | 중간 | 매우 높음 |
| **HotpotQA 정확도** | 27.4% | 28.7% | 51.0% | 35.2% (Reflection) |
| **적합한 워크로드** | 탐색적·동적 | 정형·반복 | 대량 병렬 처리 | 고난이도 다단계 |

**에이전트 vs 경쟁 기술**

| 구분 | AI Agent (LLM) | RPA (UiPath) | Workflow Engine (Airflow) | Microservice Orchestrator (Temporal) |
| :--- | :--- | :--- | :--- | :--- |
| **판단 방식** | LLM 추론 (확률적) | 규칙 기반 (결정적) | DAG 스케줄 | 상태 머신 |
| **도구 등록** | 자연어 설명 | UI 레코딩 | Python 코드 | 코드 워커 |
| **유연성** | ★★★★★ | ★★ | ★★★ | ★★★ |
| **신뢰성** | ★★ (환각 가능) | ★★★★★ | ★★★★★ | ★★★★★ |
| **신규 작업 적응** | 즉시 (제로샷) | 재설계 필요 | 재설계 필요 | 재설계 필요 |
| **적용 도메인** | 비정형·미정의 업무 | 정형 반복 업무 | ETL·배치 | 트랜잭션 워크플로 |

**연계 아키텍처**: AI 에이전트는 **RAG(Retrieval-Augmented Generation)** 와 결합되어 도구 사용 전 컨텍스트를 보강하며, **MCP(Model Context Protocol)** 가 2024년 Anthropic이 출시한 **표준 도구 호출 프로토콜**로 자리잡아 OpenAI·Google·IDE(vscode/Cursor)·DB·CRM이 통합된다. LangChain·LangGraph·LlamaIndex·CrewAI·AutoGen은 에이전트 오케스트레이션 프레임워크로, 다중 에이전트 협업(Multi-Agent Collaboration) 패턴을 지원한다.

- **📢 섹션 요약 비유**: RPA는 **정해진 줄에서만 노를 젓는 배**, 워크플로우 엔진은 **철도 신호