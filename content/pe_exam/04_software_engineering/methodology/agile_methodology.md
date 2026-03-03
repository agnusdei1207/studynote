+++
title = "애자일 방법론 (Agile Methodology)"
date = 2025-03-01

[extra]
categories = "pe_exam-software_engineering-methodology"
+++

# 애자일 방법론 (Agile Methodology)

## 핵심 인사이트 (3줄 요약)
> **변화에 유연하게 대응하는 반복적·점진적 소프트웨어 개발 방식**으로, 1~4주 스프린트로 작동하는 SW를 지속 전달한다. 협업, 피드백, 적응이 핵심 가치다. 기술사 시험에서는 애자일 선언문 4가치·12원칙과 스크럼/칸반/XP 비교가 핵심이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 애자일(Agile) 방법론은 **2001년 애자일 선언문을 통해 정립된 유연한 소프트웨어 개발 철학과 실천법**으로, 변화를 수용하고 고객과 협업하며 작동하는 소프트웨어를 짧은 주기로 지속적으로 전달하는 것을 목적으로 한다.

> 💡 **비유**: 애자일은 **"요리의 맛보기 식사"** 같아요. 완성된 코스 요리를 한 번에 내는 대신, 요리 과정에서 계속 맛을 보며 조리법을 조정하죠. "짜면 소금을 줄이고, 달면 설탕을 줄이는" 식으로요. 결과적으로 손님(고객)이 원하는 맛에 가까워집니다!

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점 - 워터폴의 경직성**: 요구사항을 초기에 모두 정의해야 하며, 변경 비용이 기하급수적으로 증가. 요구사항 변경 1건이 수억 원 손실 초래

2. **기술적 필요성 - 불확실성 관리**: 소프트웨어는 복잡성(Complex)과 불확실성(Uncertain)이 높아 예측 기반 계획 불가. 탐색적 접근(Exploratory Approach) 필요

3. **시장/산업 요구 - Time-to-Market**: 인터넷 시대로 제품 출시 속도가 경쟁력의 핵심. 6개월 개발 → 2주 스프린트로 전환 필요

**핵심 목적**: **불확실한 환경에서 고객 가치를 빠르게 전달하고 지속적으로 개선**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**애자일 선언문 4가치** (필수):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **개인과 상호작용** | 공정과 도구보다 중요 | 사람 중심 | 밴드 연주 |
| **작동하는 소프트웨어** | 포괄적 문서보다 중요 | 실물 우선 | 시제품 |
| **고객과의 협력** | 계약 협상보다 중요 | 파트너십 | 공동 설계 |
| **변화에 대응** | 계획 따르기보다 중요 | 유연성 | 카멜레온 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│              애자일 소프트웨어 개발 선언 (2001. 2. 11~13)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   우리는 소프트웨어를 개발하면서 더 나은 방법을 찾고                     │
│   다른 사람들을 도와주면서 다음 가치를 더 중요하게 여깁니다:             │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                                                                 │   │
│   │  공정과 도구보다         [개인과 상호작용]을                     │   │
│   │  (Processes and tools) → (Individuals and interactions)        │   │
│   │                                                                 │   │
│   │  포괄적인 문서보다       [작동하는 소프트웨어]을                 │   │
│   │  (Comprehensive docs)   → (Working software)                   │   │
│   │                                                                 │   │
│   │  계약 협상보다           [고객과의 협력]을                       │   │
│   │  (Contract negotiation) → (Customer collaboration)             │   │
│   │                                                                 │   │
│   │  계획을 따르기보다       [변화에 대응]을                         │   │
│   │  (Following a plan)     → (Responding to change)               │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   즉, 오른쪽의 가치도 중요하지만, 우리는 왼쪽의 가치에                   │
│   더 높은 가치를 둡니다.                                                │
│                                                                         │
│   - 17명의 서명자: Kent Beck, Martin Fowler, Ken Schwaber 등           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        스크럼 프로세스                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                     Product Backlog                               │  │
│   │        (제품 백로그: 우선순위 있는 사용자 스토리 목록)            │  │
│   │   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │  │
│   │   │ US1 │ │ US2 │ │ US3 │ │ US4 │ │ US5 │ │ ... │              │  │
│   │   └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              │ 스프린트 계획                             │
│                              ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                     Sprint (2~4주)                                │  │
│   │  ┌──────────────────────────────────────────────────────────┐   │  │
│   │  │              Daily Scrum (15분)                          │   │  │
│   │  │  • 어제 뭘 했나?                                          │   │  │
│   │  │  • 오늘 뭘 할 건가?                                       │   │  │
│   │  │  • 장애물이 있나?                                         │   │  │
│   │  └──────────────────────────────────────────────────────────┘   │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌──────────────────┐    ┌──────────────────┐                         │
│   │  Sprint Review   │    │ Sprint Retrospect│                         │
│   │ (결과 시연)       │    │  (프로세스 개선)  │                         │
│   └──────────────────┘    └──────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        칸반 보드 (Kanban Board)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   │
│   │   할 일    │   │   진행중   │   │   검토중   │   │   완료     │   │
│   │   (To Do)  │   │  (Doing)   │   │  (Review)  │   │   (Done)   │   │
│   ├────────────┤   ├────────────┤   ├────────────┤   ├────────────┤   │
│   │  [WIP: ∞]  │   │  [WIP: 3]  │   │  [WIP: 2]  │   │            │   │
│   ├────────────┤   ├────────────┤   ├────────────┤   ├────────────┤   │
│   │ □ 기능 A   │   │ ■ 기능 D   │   │ ■ 기능 F   │   │ ✓ 기능 H   │   │
│   │ □ 기능 B   │   │ ■ 기능 E   │   │ ■ 기능 G   │   │ ✓ 기능 I   │   │
│   │ □ 기능 C   │   │            │   │            │   │ ✓ 기능 J   │   │
│   └────────────┘   └────────────┘   └────────────┘   └────────────┘   │
│                                                                         │
│   WIP(Work In Progress) 제한: 동시 진행 작업 수 제한으로 병목 가시화    │
│   Little's Law: 리드타임 = WIP / 처리율                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 백로그 작성 → ② 스프린트 계획 → ③ 일일 스크럼 → ④ 개발 → ⑤ 리뷰 → ⑥ 회고
```

- **1단계 (백로그 작성)**: PO가 제품 비전을 바탕으로 사용자 스토리 수집, 우선순위 설정, 스토리 포인트 추정
- **2단계 (스프린트 계획)**: 팀이 이번 스프린트 목표 설정, 백로그 항목 선정, 태스크 분해
- **3단계 (일일 스크럼)**: 매일 15분 스탠드업 미팅, 진행 상황 공유, 장애물 식별
- **4단계 (개발)**: TDD, 페어 프로그래밍, 지속적 통합으로 품질 확보
- **5단계 (스프린트 리뷰)**: 완성물 시연, 이해관계자 피드백 수집, 백로그 업데이트
- **6단계 (회고)**: 프로세스 개선점 논의, 액션 아이템 도출, 다음 스프린트 적용

**핵심 알고리즘/공식**:

```
[벨로시티 (Velocity)]

벨로시티 = 완료된 스토리 포인트 합계 / 스프린트 수

예시:
- 스프린트 1: 21점 완료
- 스프린트 2: 24점 완료
- 스프린트 3: 18점 완료

평균 벨로시티 = (21 + 24 + 18) / 3 = 21 포인트/스프린트

예상 완료일 = 남은 총 포인트 / 평균 벨로시티 × 스프린트 기간

[리드 타임 & 사이클 타임 (칸반)]

Lead Time = 작업 요청 시점 → 완료 시점 (고객 관점)
Cycle Time = 작업 시작 시점 → 완료 시점 (팀 관점)

Little's Law:
WIP = Throughput × Lead Time
→ Lead Time = WIP / Throughput

예: WIP=5, Throughput=2/일
→ Lead Time = 5 / 2 = 2.5일

[번업/번다운 차트]

        포인트
          ▲
     100  │     ╭───────────────────── 완료 누적 (Actual)
          │    ╱
      80  │   ╱
          │  ╱    ╭─────────────────── 계획 (Planned)
      60  │ ╱    ╱
          │╱    ╱
      40  │    ╱
          │   ╱
      20  │  ╱
          │ ╱
       0  └──────────────────────→ 스프린트
           S1   S2   S3   S4   S5

스코프 변경 감지: 계획선이 올라가면 요구사항 추가
```

**코드 예시** (필수: Python 스크럼 시뮬레이터):

```python
"""
애자일 스크럼 시뮬레이터
- 스프린트 계획, 데일리 스크럼, 회고
- 벨로시티 추적, 번다운 차트
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum, auto
from datetime import datetime, timedelta

class Priority(Enum):
    HIGHEST = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    LOWEST = 5

class StoryStatus(Enum):
    TODO = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    BLOCKED = auto()

@dataclass
class UserStory:
    """사용자 스토리"""
    id: str
    title: str
    description: str
    story_points: int  # 1, 2, 3, 5, 8, 13, 21 (피보나치)
    priority: Priority
    status: StoryStatus = StoryStatus.TODO
    assignee: Optional[str] = None

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.story_points}SP)"

@dataclass
class Sprint:
    """스프린트"""
    number: int
    start_date: datetime
    duration_days: int = 14
    stories: List[UserStory] = field(default_factory=list)
    completed_stories: List[UserStory] = field(default_factory=list)

    @property
    def end_date(self) -> datetime:
        return self.start_date + timedelta(days=self.duration_days)

    @property
    def committed_points(self) -> int:
        return sum(s.story_points for s in self.stories)

    @property
    def completed_points(self) -> int:
        return sum(s.story_points for s in self.completed_stories)

    def add_story(self, story: UserStory) -> None:
        self.stories.append(story)

    def complete_story(self, story: UserStory) -> None:
        if story in self.stories and story not in self.completed_stories:
            story.status = StoryStatus.DONE
            self.completed_stories.append(story)


class ProductBacklog:
    """제품 백로그"""
    def __init__(self):
        self.stories: List[UserStory] = []

    def add_story(self, story: UserStory) -> None:
        self.stories.append(story)
        self._sort_by_priority()

    def _sort_by_priority(self) -> None:
        self.stories.sort(key=lambda s: s.priority.value)

    def get_top_stories(self, max_points: int) -> List[UserStory]:
        """벨로시티에 맞춰 상위 스토리 선택"""
        selected = []
        total = 0
        for story in self.stories:
            if total + story.story_points <= max_points:
                selected.append(story)
                total += story.story_points
        return selected

    @property
    def total_points(self) -> int:
        return sum(s.story_points for s in self.stories)


class ScrumTeam:
    """스크럼 팀"""
    def __init__(self, name: str):
        self.name = name
        self.velocity_history: List[int] = []
        self.product_owner: Optional[str] = None
        self.scrum_master: Optional[str] = None

    @property
    def average_velocity(self) -> float:
        if not self.velocity_history:
            return 0
        recent = self.velocity_history[-3:]
        return sum(recent) / len(recent)

    def record_velocity(self, velocity: int) -> None:
        self.velocity_history.append(velocity)


class DailyScrum:
    """데일리 스크럼"""
    @dataclass
    class Update:
        member: str
        yesterday: str
        today: str
        blockers: List[str]

    def __init__(self, date: datetime):
        self.date = date
        self.updates: List[DailyScrum.Update] = []
        self.blockers_identified: List[str] = []

    def add_update(self, member: str, yesterday: str,
                   today: str, blockers: List[str] = None) -> None:
        update = DailyScrum.Update(
            member=member,
            yesterday=yesterday,
            today=today,
            blockers=blockers or []
        )
        self.updates.append(update)
        self.blockers_identified.extend(blockers or [])

    def summary(self) -> str:
        lines = [f"\n=== Daily Scrum ({self.date.strftime('%Y-%m-%d')}) ==="]
        for u in self.updates:
            lines.append(f"\n{u.member}:")
            lines.append(f"  어제: {u.yesterday}")
            lines.append(f"  오늘: {u.today}")
            if u.blockers:
                lines.append(f"  ⚠️ 장애물: {', '.join(u.blockers)}")
        return "\n".join(lines)


class SprintRetrospective:
    """스프린트 회고"""
    def __init__(self, sprint_number: int):
        self.sprint_number = sprint_number
        self.what_went_well: List[str] = []
        self.what_to_improve: List[str] = []
        self.action_items: List[str] = []

    def add_good(self, item: str) -> None:
        self.what_went_well.append(item)

    def add_improvement(self, item: str) -> None:
        self.what_to_improve.append(item)

    def add_action(self, action: str, owner: str) -> None:
        self.action_items.append(f"[{owner}] {action}")

    def summary(self) -> str:
        lines = [f"\n=== Sprint {self.sprint_number} 회고 ==="]
        lines.append("\n👍 잘한 점:")
        for item in self.what_went_well:
            lines.append(f"  • {item}")
        lines.append("\n🔧 개선할 점:")
        for item in self.what_to_improve:
            lines.append(f"  • {item}")
        lines.append("\n✅ 액션 아이템:")
        for item in self.action_items:
            lines.append(f"  • {item}")
        return "\n".join(lines)


class ScrumSimulator:
    """스크럼 시뮬레이터"""
    def __init__(self, team: ScrumTeam, backlog: ProductBacklog):
        self.team = team
        self.backlog = backlog
        self.sprints: List[Sprint] = []
        self.current_sprint: Optional[Sprint] = None

    def plan_sprint(self, sprint_number: int, duration_days: int = 14) -> Sprint:
        """스프린트 계획"""
        target_velocity = max(self.team.average_velocity, 20)

        sprint = Sprint(
            number=sprint_number,
            start_date=datetime.now() + timedelta(days=len(self.sprints) * duration_days),
            duration_days=duration_days
        )

        selected_stories = self.backlog.get_top_stories(int(target_velocity * 1.1))
        for story in selected_stories:
            sprint.add_story(story)
            self.backlog.stories.remove(story)

        print(f"\n📋 Sprint {sprint_number} 계획:")
        print(f"   목표 벨로시티: {target_velocity:.1f} SP")
        print(f"   커밋: {len(sprint.stories)}개 ({sprint.committed_points}SP)")

        self.current_sprint = sprint
        self.sprints.append(sprint)
        return sprint

    def end_sprint(self, completion_rate: float = 0.85) -> None:
        """스프린트 종료"""
        if not self.current_sprint:
            return

        # 완료율만큼 스토리 완료 처리
        import random
        num_to_complete = int(len(self.current_sprint.stories) * completion_rate)
        stories_to_complete = random.sample(
            self.current_sprint.stories,
            min(num_to_complete, len(self.current_sprint.stories))
        )
        for story in stories_to_complete:
            self.current_sprint.complete_story(story)

        self.team.record_velocity(self.current_sprint.completed_points)

        print(f"\n🏁 Sprint {self.current_sprint.number} 종료:")
        print(f"   완료: {len(self.current_sprint.completed_stories)}/{len(self.current_sprint.stories)}")
        print(f"   벨로시티: {self.current_sprint.completed_points}SP")

        # 회고
        retro = SprintRetrospective(self.current_sprint.number)
        retro.add_good("팀 협업 원활")
        retro.add_improvement("스토리 추정 정확도 향상 필요")
        retro.add_action("플래닝 포커 시간 늘리기", "SM")
        print(retro.summary())

        self.current_sprint = None

    def get_burndown_data(self, sprint: Sprint) -> Dict:
        """번다운 차트 데이터"""
        days = sprint.duration_days
        total = sprint.committed_points
        ideal_daily = total / days

        ideal = [total - (ideal_daily * i) for i in range(days + 1)]
        actual = [total]
        remaining = total
        for i in range(1, days + 1):
            burn = ideal_daily * 1.1  # 약간의 변동
            remaining = max(0, remaining - burn)
            actual.append(remaining)

        return {"days": list(range(days + 1)), "ideal": ideal, "actual": actual}


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("애자일 스크럼 시뮬레이터")
    print("=" * 60)

    # 팀 생성
    team = ScrumTeam("애자일 개발팀")
    team.product_owner = "김PO"
    team.scrum_master = "이SM"

    # 제품 백로그 생성
    backlog = ProductBacklog()
    stories = [
        UserStory("US-001", "로그인", "이메일 로그인", 5, Priority.HIGHEST),
        UserStory("US-002", "회원가입", "신규 가입", 8, Priority.HIGHEST),
        UserStory("US-003", "비번 찾기", "비번 재설정", 3, Priority.HIGH),
        UserStory("US-004", "프로필", "프로필 수정", 5, Priority.MEDIUM),
        UserStory("US-005", "검색", "게시물 검색", 8, Priority.LOW),
    ]
    for story in stories:
        backlog.add_story(story)

    print(f"\n📦 백로그: {backlog.total_points}SP, {len(backlog.stories)}개")

    # 시뮬레이터 실행
    simulator = ScrumSimulator(team, backlog)

    # Sprint 1
    simulator.plan_sprint(1)
    daily = DailyScrum(datetime.now())
    daily.add_update("박개발", "로그인 API 구현", "로그인 UI 연동", [])
    print(daily.summary())
    simulator.end_sprint(0.8)

    # Sprint 2
    simulator.plan_sprint(2)
    simulator.end_sprint(0.9)

    print(f"\n📊 평균 벨로시티: {team.average_velocity:.1f}SP")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **빠른 피드백**: 짧은 주기로 고객 반응 확인 | **높은 팀 성숙도 필요**: 자기 조직화 팀 전제 |
| **변화 대응**: 요구사항 변경 유연히 수용 | **일정 예측 어려움**: 초기 벨로시티 불안정 |
| **가시성 높음**: 진행 상황 투명 공유 | **문서화 부족**: 나중에 유지보수 어려울 수 있음 |
| **동기 부여**: 팀 자율성으로 몰입도 향상 | **규모 확장 어려움**: 대규모는 SAFe/LeSS 필요 |

**주요 애자일 프레임워크 비교** (필수: 2개 대안):

| 비교 항목 | 스크럼 (Scrum) | XP (Extreme Programming) | 칸반 (Kanban) |
|---------|---------------|-------------------------|---------------|
| **핵심 특성** | ★ Sprint 기반 반복 | 기술적 실천법 강조 | 연속적 흐름 |
| **반복 주기** | 2~4주 (고정) | 1~2주 | 없음 |
| **역할** | PO, SM, 개발팀 | Coach, Customer | 제한 없음 |
| **핵심 실천법** | 데일리 스크럼, 회고 | TDD, 페어, CI | WIP 제한 |
| **변경 시점** | Sprint 간에만 | 이터레이션 간에만 | ★ 언제든 |
| **적합 환경** | ★ 신규 개발 | 품질 중심 | 운영/유지보수 |

> **★ 선택 기준**: 신규 제품 개발 → 스크럼, 품질/기술 부채 해결 → XP, 운영/지원 → 칸반

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **신규 서비스** | 2주 스프린트, MVP 우선 | Time-to-Market 50% 단축 |
| **레거시 현대화** | 스프린트로 점진적 마이그레이션 | 리스크 70% 감소 |
| **디지털 트랜스포메이션** | SAFe로 대규모 확장 | 혁신 속도 2배 향상 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Spotify** - Squad, Tribe, Chapter, Guild 구조로 확장. 팀 자율성 극대화. 100개 이상 팀이 독립적 배포

- **사례 2: ING 은행** - 전 조직 애자일 전환. 3,500명 IT 인력을 스크럼 팀으로 재구성. 제품 출시 속도 2배 향상

- **사례 3: 삼성 SDS** - 사내 프로젝트에 스크럼 도입. 결함 발생률 40% 감소, 고객 만족도 25% 향상

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: CI/CD 파이프라인 필수, 자동화 테스트로 품질 보장, DoD(Definition of Done) 명확화
2. **운영적**: 팀 구조 변경, 교육·코칭, 스크럼 마스터 양성
3. **보안적**: 각 스프린트에 보안 요구사항 포함, 침투 테스트 주기적 수행
4. **경제적**: 초기 교육비용, 도구 비용, 학습 곡선 기간

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **Zombie Scrum**: 형식만 따르고 실제 개선 없음. 해결: 회고에서 솔직한 논의, 실질적 액션
- ❌ **스프린트 중 변경**: 진행 중 스프린트 범위 변경. 해결: Sprint Goal 준수
- ❌ **PO 부재**: 의사결정 지연. 해결: PO 권한 강화, 단일 의사결정권자 명확화

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  애자일 핵심 연관 개념 맵                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [폭포수] ←──→ [애자일] ←──→ [DevOps]                          │
│        ↓              ↓               ↓                         │
│   [V-모델]       [Scrum/XP]       [CI/CD]                       │
│        ↓              ↓               ↓                         │
│   [계획 중심]    [칸반]          [플랫폼 엔지니어링]              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 스크럼 | 하위 프레임워크 | 애자일 구현체 | `[scrum](./scrum.md)` |
| 워터폴 | 대안 방법론 | 전통적 순차 접근 | `[waterfall_model](./waterfall_model.md)` |
| DevOps | 확장 개념 | 개발-운영 통합 | `[devsecops](./devsecops.md)` |
| 요구사항 공학 | 선행 활동 | 사용자 스토리 도출 | `[requirements_engineering](./requirements_engineering.md)` |
| CI/CD | 기술적 지원 | 지속적 통합/배포 | `[software_testing](../testing/software_testing.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **Time-to-Market** | 제품 출시 속도 | 기존 대비 40~60% 단축 |
| **품질** | 결함 밀도 | 30~50% 감소 |
| **생산성** | 벨로시티 | 초기 대비 2배 증가 (6개월 후) |
| **만족도** | 팀/고객 만족 | NPS 20점 향상 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 기반 스크럼 도구, 자동화된 벨로시티 예측, 실시간 리스크 감지

2. **시장 트렌드**: 원격 근무에 맞는 Virtual Scrum, 비개발 부서로 확산(마케팅, HR 등)

3. **후속 기술**: Product Ops, Platform Engineering과 결합, Lean Startup과 통합

> **결론**: 애자일은 방법론이 아니라 **마인드셋**이다. "계획을 따르기보다 변화에 대응"이라는 철학을 조직 문화로 내재화하는 것이 핵심이다. 도구·프로세스보다 **사람과 협업**이 성패를 가른다.

> **※ 참고 표준**: Agile Manifesto (2001), Scrum Guide (Schwaber & Sutherland), ISO/IEC 26515

---

## 어린이를 위한 종합 설명

애자일은 마치 **"요리의 맛보기 식사"** 같아요!

**기존 방식(워터폴)은:**
처음에 모든 메뉴를 다 정하고, 주방에서 한 달간 요리한 뒤, 완성된 코스 요리를 한 번에 내요. 근데 손님이 "이거 너무 짜!"라고 하면? 처음부터 다시 만들어야 해요. 😭

**애자일 방식은:**
1. "오늘은 스프 먼저 만들어볼까?"
2. 스프를 30분 만들어서 맛보여줘요
3. 손님이 "조금 더 간을 해주세요!" 하면 바로 수정!
4. 수정한 걸 다시 맛보여줘요
5. 이 과정을 계속 반복해요

이렇게 하면 손님이 정말 원하는 맛을 찾을 수 있어요! 🍲

**핵심 4가지:**
1. **사람이 최우선**: 도구보다 사람 간 대화가 중요
2. **작동하는 게 최고**: 문서보다 실제 프로그램이 중요
3. **함께 만들기**: 계약보다 고객과 협력이 중요
4. **변화 OK**: 계획보다 변화 대응이 중요

이게 바로 애자일이에요! 🚀
