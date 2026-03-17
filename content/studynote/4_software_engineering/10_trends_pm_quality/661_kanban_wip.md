+++
title = "661. 칸반 WIP (Work In Progress) 제한"
date = "2026-03-15"
weight = 661
[extra]
categories = ["Software Engineering"]
tags = ["Agile", "Kanban", "WIP Limit", "Lean", "Workflow Optimization", "Just-In-Time"]
+++

# 661. 칸반 WIP (Work In Progress) 제한

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 칸반(Kanban) 시스템의 핵심 제어 장치로, 워크플로우(Workflow) 내 각 단계별 동시 처리 작업량을 인위적으로 제한하여 병목(Bottleneck)을 가시화하고 **흐름 효율(Flow Efficiency)**을 극대화하는 린(Lean) 관리 기법이다.
> 2. **메커니즘**: 풀(Pull) 시스템을 기반으로 하여, 다음 단계의 여유 용량(Slot)이 확보되었을 때만 이전 단계의 작업을 이동시킴으로써 시스템의 부하를 제어하고 **문맥 전환(Context Switching)** 비용을 최소화한다.
> 3. **가치**: 리드 타임(Lead Time)의 변동성을 줄이고 예측 가능성을 높여, **JIT (Just-In-Time)** 방식의 가치 전달을 실현하며, 지속적인 개선(Continuous Improvement)을 위한 데이터 기반의 의사결정 근거를 제공한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**WIP (Work In Progress)**, 즉 '진행 중인 작업' 제한은 1940년대 도요타 자동차의 **JIT (Just-In-Time)** 생산 시스템에서 유래한 칸반 방법론의 심장부이다. 소프트웨어 공학에서 이는 단순한 작업 시각화를 넘어, 시스템의 처리량(Throughput)을 보존하기 위해 '멀티태스킹'이라는 착각을 깨부수는 장치로 작용한다.

기존의 **폭포수(Waterfall)** 모델이나 계획 중심 방식론이 '활용률(Utilization Rate)' 극대화에 집중했다면, WIP 제한은 '흐름(Flow)'의 최적화에 집중한다. 시스템 이론(Theory of Constraints)에 입각하여, 전체 프로세스의 속도는 가장 느린 단계(병목 구간)의 속도를 초과할 수 없다는 사실을 직시하고, 모든 구간의 작업량을 균형 있게 유지함으로써 대기 시간(Queueing Time)을 제거한다.

### 2. 등장 배경 및 발전
① **한계**: 애자일(Agile) 전환 초기, 스크럼(Scrum)의 스프린트(Sprint) 주기 내에서도 작업이 끝없이 쌓이고, 개발자들은 동시에 5~10개의 티켓을 오가며 생산성이 급격히 떨어지는 '문맥 전화 비용'의 함정에 빠짐.
② **혁신**: 업무 시작(Begin)보다 업무 완료(Finish)를 우선시하는 풀 시스템을 도입하여, '진행 중'인 상태의 작업 수를 상한선(Cap)으로 물리적으로 차단함.
③ **현재**: **DevOps** 및 **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인과 결합하여, 코드 커밋부터 배포까지의 사이클 타임을 단축시키는 핵심 엔지니어링 기제로 발전함.

### 3. 다이어그램: 무제한 WIP vs 제한된 WIP

```text
[CASE A: WIP 제한 없음 (Push System)]
  ┌───┐    ┌───┐    ┌───┐    ┌───┐
  │ Push    │  Q  │    │  Q  │    │ Done
  └───┘ ─> └───┘ ─> └───┘ ─> └───┘
            ↑       ↑
            | (과적재) |
         대기 폭발    처리 불가
  => 결과: 리드 타임 증가, 병목 은폐

[CASE B: WIP 제한 있음 (Pull System)]
  ┌───┐    ┌───┐    ┌───┐    ┌───┐
  │ Pull    │  Q  │    │  Q  │    │ Done
  └───┘ <─ └───┘ <─ └───┘ <─ └───┘
            ↑       ↑
          (Slot    (Back-pressure
           Available) Signal)
  => 결과: 흐름 일관성, 병목 가시화
```

**해설**: 위 다이어그램은 WIP 제한의 적용 여부에 따른 시스템 거동을 도식화한 것이다. CASE A(Push)는 후공정으로 작업을 밀어넣기만 하기에 대기열(Queue)이 무한정 커질 수 있어 시스템 내부의 병목 지점이 어디인지 파악하기 어렵다. 반면, CASE B(Pull)는 WIP 한도가 찬 경우 새로운 작업 투입을 차단(Block)함으로써 시스템 전체에 '백 프레셔(Back-pressure)'를 가해, 병목이 발생하는 즉시 전체 팀이 이를 감지하고 해결하도록 강제한다.

### 📢 섹션 요약 비유
이는 **고속도로 톨게이트에 하이패스 차로를 별도로 운영하여, 진입 차량 수를 제어함으로써 교통 체증을 원천적으로 방지하는 것**과 같다. 도로(프로세스)에 차량(작업)이 너무 많으면 아무도 못 가지만, 진입을 적절히 제한하면 오히려 통행 속도(처리량)가 빨라지는 원리이다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 상세 동작

WIP 제한을 구현하기 위한 시스템은 다음과 같은 요소들로 상호 작용한다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 관련 프로토콜/메트릭 |
|:---|:---|:---|:---|
| **Work Item (작업 단위)** | 가치를 전달하는 최소 단위 | 사용자 스토리(User Story), 버그 수정, 기술 부채 상환 등으로 분리 | Story Points, Bug ID |
| **Workflow State (상태)** | 작업의 수명 주기 단계 | Backlog → To Do → In Progress (Dev) → Review → Done | State Machine |
| **WIP Limit (제한치)** | 상태별 수용 가능한 작업량 상한 | 컬럼(Column) 헤더에 숫자로 표기 (예: `Dev: 3`) | Capacity Planning |
| **Pull Mechanism (풀 메커니즘)** | 작업 이동의 규칙 강제 | 다음 단계의 여유(Slot)가 발생할 때만 작업 이동을 허용하는 신호 체계 | Handshake Protocol |
| **Visual Board (시각화 도구)** | 시스템 상태를 투명하게 공유 | Jira, Trello, Azure Boards 등을 통해 현재 WIP 현황을 전사 공개 | Real-time Monitoring |

### 2. 아키텍처 다이어그램: 칸반 시스템의 데이터 흐름

아래는 WIP 제한이 적용된 칸반 보드의 논리적 아키텍처이다.

```text
+-----------------------------------------------------------------------+
|                         KANBAN BOARD ARCHITECTURE                      |
+-----------------------------------------------------------------------+
|                               (Upstream)                               |
|   ┌─────────┐    ┌─────────┐    ┌─────────────────────────────────┐   |
|   │ Backlog │ ─> │ To Do   │ ─> │      IN PROGRESS (WIP: 4)       │   |
|   └─────────┘    └─────────┘    │  ┌───┐  ┌───┐  ┌───┐  ┌───┐    │   |
|                                 │  │ A │  │ B │  │ C │  │ D │    │   |
|                                 │  └───┘  └───┘  └───┘  └───┘    │   |
|                                 └─────────────────────────────────┘   |
|                                              │                        |
|                                              v (PULL Only)            |
|                                 ┌─────────────────────────────────┐   |
|                                 │       TESTING (WIP: 2)          │   |
|                                 │  ┌───┐  ┌───┐  (BLOCKED)        │   |
|                                 │  │ E │  │ F │  [No Slot]        │   |
|                                 └─────────────────────────────────┘   |
|                                              │                        |
|                                              v                         |
|   ┌─────────┐    ┌─────────┐    ┌─────────────────────────────────┐   |
|   │ Deploy  │ <─ │  Done   │ <─ │      VALIDATION (WIP: 3)        │   |
|   └─────────┘    └─────────┘    └─────────────────────────────────┘   |
|                               (Downstream)                              |
+-----------------------------------------------------------------------+
```

**해설**:
1.  **① & ② (To Do → In Progress)**: `In Progress`의 WIP Limit이 4로 설정되어 있다. 현재 4개의 슬롯(A, B, C, D)이 모두 점유되어 있으므로, `To Do` 단계에 있는 다른 작업은 `In Progress`로 들어갈 수 없다. 이때 팀원은 새로운 작업을 시작하는 대신, 기존 4개의 작업 중 하나를 완료(또는 도움)하여 슬롯을 비워야 한다.
2.  **③ (In Progress → Testing)**: `Testing` 단계의 WIP Limit은 2이다. 현재 E, F가 처리 중이므로 `In Progress`에 있는 작업 A~D 중 하나가 완료되더라도 즉시 테스트로 넘어갈 수 없으며, `Testing` 슬롯이 날 때까지 대기해야 한다.
3.  **④ (Bottleneck Visualization)**: `Testing` 단계가 가장 낮은 WIP Limit(2)를 가지므로, 병목이 발생하기 쉽다. 만약 `In Progress`에서 작업이 빠르게 완료되는데 `Testing` 대기열이 길어진다면, 팀은 즉시 테스트 인력을 지원(Swarming)하거나 `Testing` WIP를 조정해야 할 필요성을 느끼게 된다.

### 3. 핵심 알고리즘: 리틀의 법칙 (Little's Law) 적용

WIP 제한의 수학적 근거는 큐잉 이론(Queueing Theory)인 리틀의 법칙에 있다.

$$ L = \lambda \times W $$

*   **$L$ (Length)**: 시스템 내 평균 작업 수 (WIP)
*   **$\lambda$ (Lambda)**: 처리량 (Throughput), 단위 시간당 완료되는 작업 수
*   **$W$ (Wait)**: 평균 리드 타임 (Lead Time), 시스템 내 체류 시간

이 공식을 변형하면 **$W = L / \lambda$**가 된다.
여기서 처리량($\lambda$)이 일정하다고 가정할 때, 시스템 내 작업 수($L$, WIP)를 줄이면 평균 리드 타임($W$)이 **선형적으로 감소**함을 증명할 수 있다. 기술사는 이 수식을 통해 WIP 제한이 단순한 '규율'이 아니라 '수학적 응답 속도 최적화' 기법임을 설명해야 한다.

**코드 예시 (Python을 이용한 WIP 제한 로직 시뮬레이션)**:

```python
class KanbanColumn:
    def __init__(self, name, wip_limit):
        self.name = name
        self.wip_limit = wip_limit
        self.items = []

    def add_item(self, item):
        if len(self.items) >= self.wip_limit:
            return False # WIP Limit 초과로 투입 불가 (Pull System 작동)
        self.items.append(item)
        return True

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

# Example Usage
dev_column = KanbanColumn("Development", wip_limit=3)

# WIP 제한에 의한 작업 투입 제어 시뮬레이션
task_new = "User Authentication Feature"
if not dev_column.add_item(task_new):
    print(f"[BLOCKED] Cannot start '{task_new}'. {dev_column.name} column is full!")
    print("Action: Focus on finishing current work to free up a slot.")
else:
    print(f"[PULLED] '{task_new}' entered {dev_column.name}.")
```

### 📢 섹션 요약 비유
이는 **주방의 주방장과 파트타이너 간의 주방 설계와 같다.** 아무리 많은 재료(WIP)를 주방에 들이부어도, 조리대(Work Space)가 한정되어 있고 요리사(Developer) 수가 정해져 있다면 요리는 더뎌질 뿐이다. 조리대에 놓일 수 있는 접시 수를 제한하고, 한 요리가 완성되어 나가야만 다음 요리를 시작하게 함으로써(Start-Finish Principle), 주방 전체의 혼잡도를 줄이고 손님에게 음식을 더 빨리 제공하는 원리이다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 스크럼(Scrum) vs 칸반(Kanban)

WIP 제한은 칸반의 고유 영역이나, 스크럼과의 비교를 통해 그 특성을 명확히 할 수 있다.

| 구분 | 스크럼 (Scrum) | 칸반 (Kanban) with WIP Limit |
|:---:|:---|:---|
| **기본 철학** | **Time-boxed (시간 중심)** | **Flow-based (흐름 중심)** |
| **WIP 제한 방식** | 스프린트 백로그(Sprint Backlog) 전체에 대한 암묵적 제한 (스프린트 기간 내 가능량) | 각 워크플로우 상태(State)별 **명시적(Explicit)** 수치 제한 |
| **변경 관리** | 스프린트 중간에는 스프린트 목표 변경 지양 | 언제든지 우선순위 변경 가능 (단, WIP Limit 준수하에) |
| **주요 메트릭** | 속도(Velocity, 스프린트당 완료 포인트) | 사이클 타임(Cycle Time), 리드 타임, 처리량(Throughput) |
| **팀 역할** | 스쿼마스터(Scrum Master), PO(Product Owner) 등 역할 명시 | 기존 역할 유지하며 프로세스만 점진적 변경 |

### 2. 과목 융합 관점: 데이터베스 & 운영체제(OS) 원리

WIP 제한은 타 IT 영역의 성능 튜닝 원리와 맥락을 같이한다.

1.  **데이터베이스 (DB) - Connection Pool**:
    *   DB 서버는 무한정의 커넥션을 허용하지 않는다. **Connection Pool (커넥션 풀)**의 최대 크기를 설정하는 것과 동일한 이치이다. WIP를 제한하지 않으면 DB Connection