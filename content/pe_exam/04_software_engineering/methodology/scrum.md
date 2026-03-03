+++
title = "Scrum (스크럼)"
date = 2026-03-03

[extra]
categories = "pe_exam-software-engineering"
+++

# Scrum (스크럼)

## 핵심 인사이트 (3줄 요약)
> Scrum은 2~4주 Sprint로 반복적 Incremental 개발을 하는 Agile 프레임워크입니다.
> Product Owner, Scrum Master, Development Team의 3가지 역할과 5개 이벤트로 구성됩니다.
> Daily Standup, Sprint Review, Retrospective를 통해 지속적 개선을 실현합니다.

---

### Ⅰ. 개요

**개념**: 스크럼(Scrum)은 복잡한 제품 개발을 위해 팀이 함께 일하는 방식을 정의한 경량级的 프로세스 프레임워크로, 짧은 반복 주기(Sprint)를 통해 점진적으로 제품을 개발하고 지속적으로 개선해 나가는 애자일 방법론이다.

> 💡 **비유**: Scrum은 **럭비 경기에서 공을 앞으로 밀고 나가는 팀워크**와 같다. 럭비에서 스크럼은 팀원들이 서로 팔을 걸고 단합해서 공을 앞으로 밀어나가는 대형이다. 스크럼 개발에서도 팀원들이 서로 협력하며 목표(제품)를 향해 함께 나아간다.

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 전통적 Waterfall 방식은 요구사항 변경에 취약했다. 초기에 모든 요구사항을 정의해야 했고, 진행 상황 가시성이 낮았으며, 문서 중심으로 실제 동작하는 소프트웨어가 늦게 나왔다.

2. **기술적 필요성**: 불확실성이 높은 프로젝트에서 빠른 피드백과 적응이 필요했다. 점진적 개발을 통해 리스크를 조기에 발견하고 대응하는 방법이 요구되었다.

3. **시장/산업 요구**: 비즈니스 환경 변화 속도가 빨라지면서, Time-to-Market 단축과 고객 피드백 반영이 필수적이 되었다. 스타트업과 대기업 모두 민첩한 개발 방식이 필요했다.

**핵심 목적**: 불확실성이 높은 복잡한 문제 해결을 위해 팀의 협업을 최적화하고, 짧은 주기로 가치를 전달하며, 지속적으로 개선하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **Product Owner** | 제품 비전, 백로그 관리, 우선순위 결정 | "무엇을" 만들지 결정 | 영화 감독 |
| **Scrum Master** | 프로세스 촉진, 장애물 제거, 코칭 | "어떻게" 협업할지 지원 | 코치 |
| **Development Team** | 실제 제품 개발, 자기 조직화 | 3~9명, 교기능팀 | 배우진 |
| **Product Backlog** | 제품에 필요한 모든 요구사항 목록 | 우선순위 정렬, 지속적 업데이트 | 대본 |
| **Sprint Backlog** | Sprint에서 수행할 작업 목록 | 팀이 스스로 선정 | 이번 회차 대본 |
| **Increment** | Sprint 결과물, 잠재적으로 출시 가능 | Done 기준 충족 | 완성된 장면 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Scrum Framework                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    Scrum Roles (3가지 역할)                      │  │
│   │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │  │
│   │  │Product Owner │ │Scrum Master  │ │   Development Team       │ │  │
│   │  │  - 비전 관리 │ │  - 촉진자    │ │   - 자기조직화            │ │  │
│   │  │  - 우선순위  │ │  - 장애제거  │ │   - 교기능팀 (3~9명)     │ │  │
│   │  └──────────────┘ └──────────────┘ └──────────────────────────┘ │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    Scrum Events (5가지 이벤트)                   │  │
│   │                                                                  │  │
│   │   Sprint (2~4주)                                                 │  │
│   │  ┌────────────────────────────────────────────────────────────┐ │  │
│   │  │ ┌─────────┐  ┌───────────┐  ┌─────────┐  ┌─────────────┐  │ │  │
│   │  │ │ Sprint  │  │   Daily   │  │ Sprint  │  │  Sprint     │  │ │  │
│   │  │ │Planning │→ │  Scrum    │→ │ Review  │→ │ Retrospect  │  │ │  │
│   │  │ │ (최대8h)│  │  (15분)   │  │ (최대4h)│  │   (최대3h)  │  │ │  │
│   │  │ └─────────┘  └───────────┘  └─────────┘  └─────────────┘  │ │  │
│   │  └────────────────────────────────────────────────────────────┘ │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    Scrum Artifacts (3가지 산출물)                │  │
│   │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │  │
│   │  │   Product    │ →  │   Sprint     │ →  │  Increment   │      │  │
│   │  │   Backlog    │    │   Backlog    │    │  (완성품)    │      │  │
│   │  │  (전체 목록) │    │  (이번 할일) │    │              │      │  │
│   │  └──────────────┘    └──────────────┘    └──────────────┘      │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① Sprint Planning → ② Daily Scrum (매일) → ③ 개발 작업 → ④ Sprint Review → ⑤ Retrospective → ⑥ 반복
```

- **1단계 (Sprint Planning)**: Product Owner가 우선순위 높은 백로그 설명, 팀이 이번 Sprint에서 수행할 항목 선정, 목표(Sprint Goal) 설정
- **2단계 (Daily Scrum)**: 매일 15분, 어제 한 일/오늘 할 일/장애물 공유. 팀 동기화 및 문제 조기 발견
- **3단계 (개발 작업)**: 백로그 항목을 완료(Definition of Done) 상태로 개발. 필요 시 Product Owner와 소통
- **4단계 (Sprint Review)**: Sprint 결과를 이해관계자에게 시연. 피드백 수집, 백로그 업데이트
- **5단계 (Retrospective)**: 팀이 프로세스 개선점 논의. 무엇이 잘됐는지/개선할 점/실행 계획 도출
- **6단계 (반복)**: 새 Sprint 시작

**핵심 알고리즘/공식** (해당 시 필수):

**Sprint Planning 시간 제한**:
```
Sprint Planning (최대) = 8시간 (2주 Sprint 기준)
```

**Velocity (팀 속도)**:
```
Velocity = 완료된 Story Point 합계 / Sprint 수
```

**Burndown Chart**:
```
잔여 작업량 = 총 작업량 - (완료 속도 × 경과 일수)
```

**코드 예시** (필수: Python 또는 의사코드):

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

class Priority(Enum):
    HIGHEST = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    LOWEST = 5

@dataclass
class UserStory:
    """사용자 스토리 (Product Backlog Item)"""
    id: str
    title: str
    description: str
    priority: Priority
    story_points: int
    acceptance_criteria: List[str]
    status: str = "Backlog"

@dataclass
class Task:
    """개발 태스크"""
    id: str
    story_id: str
    title: str
    assignee: str
    estimated_hours: float
    remaining_hours: float
    status: str = "To Do"

class ProductBacklog:
    """제품 백로그"""

    def __init__(self):
        self.items: List[UserStory] = []

    def add_item(self, story: UserStory):
        self.items.append(story)
        self.sort_by_priority()

    def sort_by_priority(self):
        self.items.sort(key=lambda x: x.priority.value)

    def get_top_items(self, velocity: int) -> List[UserStory]:
        """Velocity에 맞춰 상위 항목 반환"""
        selected = []
        total_points = 0

        for item in self.items:
            if total_points + item.story_points <= velocity:
                selected.append(item)
                total_points += item.story_points

        return selected


class Sprint:
    """스프린트"""

    def __init__(self, number: int, duration_days: int = 14):
        self.number = number
        self.duration = timedelta(days=duration_days)
        self.start_date = datetime.now()
        self.end_date = self.start_date + self.duration
        self.backlog: List[UserStory] = []
        self.tasks: List[Task] = []
        self.goal: str = ""

    def add_item(self, story: UserStory):
        story.status = "Sprint Backlog"
        self.backlog.append(story)

    def get_velocity(self) -> int:
        """완료된 스토리 포인트 합계"""
        return sum(s.story_points for s in self.backlog if s.status == "Done")

    def get_burndown_data(self) -> List[tuple]:
        """번다운 차트 데이터"""
        total_points = sum(s.story_points for s in self.backlog)
        days = []
        for i in range(self.duration.days):
            date = self.start_date + timedelta(days=i)
            # 실제로는 매일 잔여 포인트 기록
            remaining = total_points - (total_points / self.duration.days * i)
            days.append((date, remaining))
        return days


class DailyScrum:
    """데일리 스크럼"""

    @staticmethod
    def standup_report(member: str, yesterday: str, today: str, blockers: str) -> str:
        """스탠드업 리포트 생성"""
        return f"""
        👤 {member}의 데일리 스크럼
        ────────────────────────────
        ✅ 어제 한 일: {yesterday}
        📋 오늘 할 일: {today}
        🚧 장애물: {blockers or '없음'}
        """


class SprintReview:
    """스프린트 리뷰"""

    def __init__(self, sprint: Sprint):
        self.sprint = sprint
        self.demo_items: List[str] = []
        self.feedback: List[str] = []

    def add_demo_item(self, item: str):
        self.demo_items.append(item)

    def add_feedback(self, stakeholder: str, comment: str):
        self.feedback.append(f"{stakeholder}: {comment}")

    def generate_report(self) -> str:
        completed = [s for s in self.sprint.backlog if s.status == "Done"]
        return f"""
        📊 Sprint {self.sprint.number} Review
        ────────────────────────────
        Sprint Goal: {self.sprint.goal}
        완료 항목: {len(completed)}/{len(self.sprint.backlog)}
        Velocity: {self.sprint.get_velocity()} SP

        🎬 데모 항목:
        {chr(10).join(f'- {item}' for item in self.demo_items)}

        💬 피드백:
        {chr(10).join(f'- {fb}' for fb in self.feedback)}
        """


class Retrospective:
    """스프린트 회고"""

    def __init__(self, sprint: Sprint):
        self.sprint = sprint
        self.what_went_well: List[str] = []
        self.what_to_improve: List[str] = []
        self.action_items: List[str] = []

    def add_positive(self, item: str):
        self.what_went_well.append(item)

    def add_improvement(self, item: str):
        self.what_to_improve.append(item)

    def add_action(self, action: str, owner: str):
        self.action_items.append(f"[{owner}] {action}")

    def generate_report(self) -> str:
        return f"""
        🔄 Sprint {self.sprint.number} Retrospective
        ────────────────────────────

        ✨ 잘한 점 (Keep):
        {chr(10).join(f'- {item}' for item in self.what_went_well)}

        🔧 개선할 점 (Problem):
        {chr(10).join(f'- {item}' for item in self.what_to_improve)}

        📝 실행 계획 (Try):
        {chr(10).join(f'- {item}' for item in self.action_items)}
        """


# 실행 예시
if __name__ == "__main__":
    # 제품 백로그 생성
    backlog = ProductBacklog()

    backlog.add_item(UserStory(
        id="US-001",
        title="로그인 기능",
        description="사용자가 이메일로 로그인할 수 있다",
        priority=Priority.HIGHEST,
        story_points=5,
        acceptance_criteria=["이메일 입력", "비밀번호 입력", "로그인 버튼"]
    ))

    backlog.add_item(UserStory(
        id="US-002",
        title="회원가입 기능",
        description="새 사용자가 계정을 만들 수 있다",
        priority=Priority.HIGH,
        story_points=8,
        acceptance_criteria=["이메일 인증", "비밀번호 확인"]
    ))

    # 스프린트 생성
    sprint = Sprint(number=1, duration_days=14)
    sprint.goal = "사용자 인증 기능 완성"

    # 팀 Velocity 10이라 가정하고 상위 항목 선택
    for item in backlog.get_top_items(velocity=10):
        sprint.add_item(item)

    # 데일리 스크럼 예시
    print(DailyScrum.standup_report(
        member="김개발",
        yesterday="로그인 API 구현",
        today="로그인 UI 연동",
        blockers="없음"
    ))

    print(f"Sprint {sprint.number} 시작: {sprint.start_date}")
    print(f"종료 예정: {sprint.end_date}")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| 빠른 피드백과 적응 가능 | 높은 팀 자율성 요구, 성숙도 필요 |
| 진행 상황 가시성 높음 | 일정 예측 어려움 (초기) |
| 지속적 개선 문화 정착 | 회의(Events)가 많다고 느낄 수 있음 |
| 이해관계자 참여 증대 | 문서화가 부족해질 수 있음 |

**대안 기술 비교** (필수: 최소 2개 대안):

| 비교 항목 | Scrum | Kanban | Waterfall |
|---------|-------|--------|-----------|
| 핵심 특성 | ★ Sprint 기반 반복 | 연속적 흐름, WIP 제한 | 단계별 순차 진행 |
| 주기 | 고정 (2~4주) | ★ 유연함 | 프로젝트 단위 |
| 변경 대응 | Sprint 경계에서만 | ★ 실시간 | 어려움 |
| 계획성 | 중간 | 낮음 | ★ 높음 |
| 적합 환경 | ★ 신규 개발, 혁신 | 운영/유지보수 | 요구사항 명확한 프로젝트 |

> **★ 선택 기준**:
> - **Scrum**: 신규 제품 개발, 높은 불확실성, 팀이 자율적
> - **Kanban**: 운영/유지보수, 지속적 배포, 긴급 이슈 많음
> - **Waterfall**: 요구사항 명확, 규제 산업, 계약 기반 프로젝트

**Scrum @ Scale 프레임워크**:

| 프레임워크 | 특징 | 적합 규모 |
|-----------|------|----------|
| Nexus | Scrum.org, 3~9개 팀 | 중형 |
| LeSS (Large-Scale Scrum) | 최소한의 확장 | 2~8개 팀 |
| SAFe (Scaled Agile Framework) | 기업급, 계층적 | 대규모 조직 |
| Spotify Model | 팀 자율성 강조 | 테크 기업 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **신규 서비스 개발** | 2주 Sprint, MVP 우선 | Time-to-Market 50% 단축 |
| **레거시 현대화** | Sprint로 점진적 마이그레이션 | 리스크 70% 감소 |
| **디지털 트랜스포메이션** | Scrum @ Scale 적용 | 혁신 속도 2배 향상 |
| **스타트업** | 1주 Sprint, 빠른 피벗 | 제품-시장 적합성 3개월 내 검증 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Spotify** - Squad, Tribe, Chapter, Guild 구조로 확장. 팀 자율성 극대화. 100개 이상 팀이 독립적 배포.

- **사례 2: ING 은행** - 전 조직 애자일 전환. 3,500명 IT 인력을 Scrum 팀으로 재구성. 제품 출시 속도 2배 향상.

- **사례 3: Samsung SDS** - 사내 프로젝트에 Scrum 도입. 결함 발생률 40% 감소, 고객 만족도 25% 향상.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: CI/CD 파이프라인 구축 필수, 자동화 테스트로 품질 보장, Definition of Done 명확화

2. **운영적**: 팀 구성 변경 (역할 재정의), 교육 및 코칭, Scrum Master 양성

3. **보안적**: 각 Sprint에서 보안 요구사항 포함, Penetration Testing 주기적 수행

4. **경제적**: 초기 교육비용, 도구(Jira 등) 비용, 생산성 저하 기간 (학습 곡선)

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **Zombie Scrum**: 형식만 따르고 실제 개선 없음. 해결: Retrospective에서 솔직한 회고, 실질적 액션 아이템
- ❌ **Sprint 변경**: 진행 중 Sprint 범위 변경. 해결: Sprint Goal 준수, 긴급건은 다음 Sprint로
- ❌ **Product Owner 부재**: 의사결정 지연. 해결: PO 권한 강화, 단일 의사결정권자 명확화
- ❌ **기술 부채 무시**: 기능만 추가하고 리팩토링 무시. 해결: 백로그에 기술 항목 포함

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  Scrum 핵심 연관 개념 맵                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Waterfall] ←──→ [Agile] ←──→ [Scrum]                        │
│        ↓              ↓               ↓                         │
│   [폭포수 모델]   [XP/Kanban]   [Sprint/Backlog]               │
│        ↓              ↓               ↓                         │
│   [계획 중심] ←──→ [DevOps] ←──→ [CI/CD]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| Agile | 상위 개념 | 스크럼을 포함하는 애자일 철학 | `[agile_methodology](./agile_methodology.md)` |
| Kanban | 대안 방법론 | 연속적 흐름 기반 애자일 | `[kanban](./kanban.md)` |
| DevOps | 확장 개념 | 개발-운영 통합 | `[devops](./devops.md)` |
| User Story | 기법 | 백로그 작성 방식 | `[user_story](../design/user_story.md)` |
| CI/CD | 기술적 지원 | 지속적 통합/배포 | `[ci_cd](../testing/ci_cd.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| Time-to-Market | 제품 출시 속도 | 기존 대비 40~60% 단축 |
| 품질 | 결함 밀도 | 30~50% 감소 |
| 생산성 | Velocity 향상 | 초기 대비 2배 증가 (6개월 후) |
| 만족도 | 팀/고객 만족 | NPS 20점 향상 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 기반 스크럼 도구, 자동화된 Velocity 예측, 실시간 리스크 감지

2. **시장 트렌드**: 원격 근무에 맞는 Virtual Scrum, 비개발 부서로 확산(마케팅, HR 등)

3. **후속 기술**: Product Ops, Platform Engineering과 결합, Lean Startup과 통합

> **결론**: 스크럼은 불확실성이 높은 소프트웨어 개발에서 가장 널리 사용되는 애자일 프레임워크다. 기술사로서 스크럼의 역할, 이벤트, 산출물을 이해하고, 조직에 맞게 적용하는 능력이 필수적이다.

> **※ 참고 표준**: Scrum Guide (Schwaber & Sutherland, 2020), Agile Manifesto (2001), ISO/IEC 26515

---

## 어린이를 위한 종합 설명

스크럼은 마치 **학교에서 조별 과제를 하는 것**과 같아요.

여러분이 친구들과 함께 "우리 마을 만들기" 프로젝트를 한다고 해요. 그런데 한 번에 다 만들려면 너무 힘들겠죠?

**스크럼 방식**으로 해봐요:

1. **2주마다 목표 세우기 (Sprint Planning)**
   "이번 2주 동안은 집 3채 만들자!"

2. **매일 아침 15분 회의 (Daily Scrum)**
   "어제 내가 지붕 만들었어!"
   "오늘은 창문 달 거야!"
   "힘든 점은 없어?"

3. **2주 후 발표 (Sprint Review)**
   "여기 집 3채 완성했어요! 어때요?"
   선생님이나 다른 조가 와서 봐주고 의견도 줘요.

4. **회고 (Retrospective)**
   "다음엔 이렇게 하면 더 잘할 수 있겠다!"
   "서로 도우면 더 빨리 끝나겠네!"

5. **반복!**
   또 2주 동안 다른 것을 만들어요. 이렇게 조금씩 완성해 나가는 거예요!

**역할도 있어요**:
- **Product Owner**: "이걸 만들고 싶어!" 하는 사람 (주문하는 손님)
- **Scrum Master**: 회의가 잘 되게 도와주는 사람 (조장)
- **Development Team**: 실제로 만드는 사람들 (조원)

이렇게 하면 큰 프로젝트도 지치지 않고 완성할 수 있어요! 🏗️✨
