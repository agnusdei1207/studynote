---
title: "Ai Agents Function Calling Agentic Loop"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
weight: 155
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AI 에이전트(AI Agent)는 LLM이 외부 도구(웹 검색, 코드 실행, DB 쿼리 등)를 함수 호출(Function Calling)로 자율적으로 사용하며 목표를 달성하는 ReAct (Reasoning + Acting) 루프 시스템이다.
> 2. **가치**: 단순 질답을 넘어 "주식 포트폴리오를 분석하고 리포트를 생성하라" 같은 복잡한 멀티스텝 과업을 자율적으로 실행해 AI의 실용적 가치를 극대화한다.
> 3. **판단 포인트**: 에이전트의 핵심 과제는 신뢰성(Reliability)과 루프 탈출이다 — 계획(Plan), 실행(Act), 관찰(Observe) 반복 루프에서 오류가 누적되지 않도록 오류 처리와 최대 스텝 제한이 필수이다.

## Ⅰ. 개요 및 필요성

ChatGPT는 질문에 답하지만, "내 캘린더를 확인해서 다음 주 일정 요약 후 팀원들에게 이메일 보내"처럼 여러 도구를 순차적으로 활용하는 작업은 못 한다. AI 에이전트는 이를 가능하게 한다.

<strong>에이전트 vs 일반 LLM 호출</strong>
- 일반 LLM: 입력 -> 1회 출력
- AI 에이전트: 목표 -> 계획 -> 도구 호출 -> 관찰 -> 재계획 -> ... -> 결과

📢 **섹션 요약 비유**: AI 에이전트는 단순히 지시를 따르는 사무직 직원이 아니라, 목표를 주면 스스로 방법을 찾아 실행하는 자율적인 프로젝트 매니저다.

## Ⅱ. 아키텍처 및 핵심 원리

| 컴포넌트 | 역할 | 예시 |
|:---|:---|:---|
| LLM 계획자 | 목표 분해, 다음 행동 결정 | GPT-4, Claude |
| 도구 (Tools) | 외부 작업 실행 | 웹 검색, 코드 실행, DB |
| 메모리 | 작업 상태 기억 | 단기(컨텍스트), 장기(벡터 DB) |
| 오케스트레이터 | 에이전트 루프 관리 | LangChain, AutoGen |
| 함수 호출 (Function Calling) | 구조화된 도구 인터페이스 | JSON 스키마 정의 |

```
[ReAct 에이전트 루프]

목표: "2024년 삼성전자 주가 분석 후 리포트 작성"
          |
          v
  [THINK/REASON]
  "먼저 주가 데이터를 검색해야 해"
          |
          v
  [ACT - Function Call]
  {
    "function": "web_search",
    "args": {"query": "삼성전자 2024 주가 데이터"}
  }
          |
          v
  [OBSERVE]
  검색 결과 반환
          |
          v
  [THINK] "데이터를 분석해야 해"
          |
          v
  [ACT - Function Call]
  {
    "function": "code_interpreter",
    "args": {"code": "import pandas as pd; ..."}
  }
          |
          v
  [OBSERVE] 분석 결과
          |
          v
  [THINK] "이제 리포트를 작성할 수 있어"
          |
          v
  최종 리포트 생성

[멀티 에이전트 협업]
    목표
      |
  오케스트레이터 에이전트
  +---+-----------+
  v   v           v
검색  코드 실행  문서 작성
에이전트 에이전트 에이전트
```

**Function Calling 예시 (OpenAI 형식)**
```json
{
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_stock_price",
      "description": "현재 주가 조회",
      "parameters": {
        "type": "object",
        "properties": {
          "ticker": {"type": "string", "description": "종목 코드"}
        }
      }
    }
  }]
}
```

📢 **섹션 요약 비유**: Function Calling은 LLM에게 "이 도구들을 사용해도 좋아"라고 권한을 주는 것이다. LLM은 상황에 맞는 도구를 선택해 실제로 사용한다.

## Ⅲ. 비교 및 연결

| 에이전트 패턴 | 구조 | 특징 |
|:---|:---|:---|
| ReAct | 추론 + 행동 교대 | 단순, 투명한 추론 |
| Plan-and-Execute | 전체 계획 후 실행 | 복잡 작업 효율적 |
| Reflexion | 실행 후 반성·피드백 | 오류 자기 수정 |
| Multi-Agent | 역할별 에이전트 협업 | 병렬 작업, 전문화 |
| LangGraph | 상태 그래프 기반 | 복잡한 워크플로 |

**에이전트 프레임워크**
- LangChain Agents: 도구 연결 표준 프레임워크
- AutoGen (Microsoft): 멀티 에이전트 대화
- CrewAI: 역할 기반 에이전트 팀
- LangGraph: 스테이트풀 그래프 기반 에이전트

📢 **섹션 요약 비유**: 단일 에이전트가 만능 직원이라면, 멀티 에이전트는 각 분야 전문가들이 협업하는 팀이다.

## Ⅳ. 실무 적용 및 실무자 판단

**에이전트 설계 원칙**
- 최소 권한: 필요한 도구만 접근 허용
- 실행 확인: 위험한 작업(삭제, 결제) 전 사람 승인
- 최대 스텝 제한: 무한 루프 방지 (max_iterations)
- 오류 처리: 도구 실패 시 재시도 또는 대안 계획

<strong>도구 카탈로그 (Tool Catalog)</strong>
- 정보 수집: 웹 검색, 뉴스 API, 데이터베이스 쿼리
- 코드 실행: Python 인터프리터, Bash
- 파일 작업: 파일 읽기/쓰기/생성
- 커뮤니케이션: 이메일 발송, 캘린더 관리
- 외부 API: 날씨, 주가, 지도

**학습 주제 포인트**
- "AI 에이전트의 ReAct 루프를 설명하고, 단일 LLM 호출과의 차이를 설명하시오"
- "Function Calling이 AI 에이전트에서 갖는 역할을 설명하시오"

📢 **섹션 요약 비유**: AI 에이전트는 스스로 할 일을 정하고, 도구를 선택하고, 실행하고, 결과를 보고 다시 계획하는 자율적인 일꾼이다.

## Ⅴ. 기대효과 및 결론

AI 에이전트는 2024~2025년 AI 산업의 핵심 트렌드로, 단순 챗봇을 넘어 실제 업무를 자동화하는 방향으로 발전하고 있다. RPA (Robotic Process Automation) + LLM 결합으로 문서 처리, 데이터 분석, 고객 서비스 자동화가 가능해졌다.

📢 **섹션 요약 비유**: AI 에이전트는 LLM에게 "생각하는 능력"에 "행동하는 능력"을 추가한 것이다. AI가 말뿐만 아니라 실제로 일을 처리하게 됐다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 패턴 | ReAct | 추론-행동 반복 루프 |
| 인터페이스 | Function Calling | 구조화된 도구 호출 |
| 구성 | 도구 (Tools) | 외부 시스템 인터페이스 |
| 확장 | Multi-Agent | 다수 에이전트 협업 |
| 기억 | Memory (단기/장기) | 상태 유지 |
| 프레임워크 | LangChain, AutoGen | 에이전트 구현 도구 |

### 👶 어린이를 위한 3줄 비유 설명
1. AI 에이전트는 "숙제 해줘"라고 하면 스스로 검색도 하고, 계산도 하고, 정리까지 하는 자동 비서예요.
2. 목표를 주면 혼자 계획을 세우고, 도구를 사용하면서 조금씩 완성해나가요.
3. 한 번에 다 못 해도 결과를 보면서 다시 계획하고, 결국 목표를 이루는 것이 에이전트의 힘이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
LLM 단순 채팅 (단일 턴 응답)
    |
    v
Function Calling — LLM이 외부 도구/API 호출
    |
    v
ReAct 패턴 (Reasoning + Acting 반복)
    |
    v
AI 에이전트 (Agentic Loop)
    +-► Planning: 목표 분해 -> 서브태스크
    +-► Tool Use: 검색 · 코드 실행 · API 호출
    +-► Memory: 단기(대화) · 장기(벡터 DB)
    +-► Reflection: 자기 평가 · 재계획
    |
    v
멀티 에이전트: CrewAI · AutoGen · LangGraph
```
