+++
title = "폭포수 모델 (Waterfall Model)"
date = 2025-03-01

[extra]
categories = "pe_exam-software_engineering-methodology"
+++

# 폭포수 모델 (Waterfall Model)

## 핵심 인사이트 (3줄 요약)
> **순차적으로 진행하는 전통적 소프트웨어 개발 모델**로, 요구분석→설계→구현→테스트→유지보수 순서로 진행된다. 단계가 끝나면 다음 단계로만 진행하며 되돌아가기 어렵다. 안전 중요 시스템, 공공사업, 계약 기반 프로젝트에 적합하다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 폭포수 모델(Waterfall Model)은 **1970년 Winston Royce가 제안한 순차적 소프트웨어 개발 방법론**으로, 각 단계가 폭포처럼 아래로만 흐르는 특징이 있다. 각 단계가 완료되어야 다음 단계로 진행할 수 있다.

> 💡 **비유**: 폭포수 모델은 **"건축 시공"** 같아요. 설계도면 → 기초 공사 → 골조 세우기 → 지붕 → 내부 마감 순서로 진행하죠. 지붕을 올리다가 "기초를 다시 하자"라고 할 수 없어요!

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점 - 비체계적 개발**: 1960년대까지 소프트웨어는 코드 작성 위주. 계획 없이 개발하다 보니 일정 지연, 품질 저하 만연

2. **기술적 필요성 - 공학적 접근**: 하드웨어 개발처럼 체계적인 단계별 접근 필요. 각 단계별 산출물 정의로 진척 관리 가능

3. **시장/산업 요구 - 대규모 프로젝트**: 우주, 국방, 원자력 등 대규모 시스템 개발에 예측 가능한 프로세스 필요. 계약·입찰 기반 프로젝트에 적합

**핵심 목적**: **순차적 단계 완료로 일정·비용 예측 가능성 확보, 문서화 중심 품질 관리**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **요구사항 분석** | 사용자 요구 수집·명세 | SRS 문서 작성 | 건축주 요구 파악 |
| **설계** | 시스템 구조·상세 설계 | SDD 문서 작성 | 설계도면 작성 |
| **구현** | 코딩·단위 테스트 | 소스 코드 산출 | 시공 |
| **테스트** | 통합·시스템·인수 테스트 | 테스트 보고서 | 준공 검사 |
| **유지보수** | 운영·버그 수정·개선 | 지속적 관리 | 유지 보수 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        폭포수 모델 (Waterfall Model)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│        ┌─────────────────┐                                             │
│        │   요구사항 분석   │ ← 사용자 요구 수집, SRS 작성               │
│        └────────┬────────┘                                             │
│                 │ ↓                                                     │
│        ┌─────────────────┐                                             │
│        │      설계       │ ← 시스템 구조, 상세 설계, SDD 작성           │
│        └────────┬────────┘                                             │
│                 │ ↓                                                     │
│        ┌─────────────────┐                                             │
│        │      구현       │ ← 코딩, 단위 테스트, 소스 코드               │
│        └────────┬────────┘                                             │
│                 │ ↓                                                     │
│        ┌─────────────────┐                                             │
│        │     테스트      │ ← 통합, 시스템, 인수 테스트                  │
│        └────────┬────────┘                                             │
│                 │ ↓                                                     │
│        ┌─────────────────┐                                             │
│        │    운영/유지보수  │ ← 배포, 유지보수                           │
│        └─────────────────┘                                             │
│                                                                         │
│   각 단계의 결과물:                                                     │
│   요구분석 → 요구사항 명세서 (SRS)                                      │
│   설계 → 설계 문서 (SDD)                                                │
│   구현 → 소스 코드                                                      │
│   테스트 → 테스트 보고서                                                │
│   운영 → 사용자 매뉴얼                                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        V-모델 (V-Model)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│        폭포수 모델을 테스트 중심으로 확장한 것                           │
│                                                                         │
│         ┌──────────────┐                           ┌──────────────┐     │
│         │ 요구사항 분석 │                           │  인수 테스트  │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │    설계      │                           │ 시스템 테스트 │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │  상세 설계   │                           │ 통합 테스트  │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │    구현      │ ───────────────────────→  │  단위 테스트  │     │
│         └──────────────┘                           └──────────────┘     │
│                                                                         │
│   각 개발 단계에 대응하는 테스트 단계 존재                               │
│   요구분석 → 인수 테스트 계획                                           │
│   설계 → 시스템 테스트 계획                                             │
│   상세 설계 → 통합 테스트 계획                                          │
│   구현 → 단위 테스트                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 요구분석 → ② 설계 → ③ 구현 → ④ 테스트 → ⑤ 유지보수
```

- **1단계 (요구사항 분석)**: 사용자 요구 수집, 기능적/비기능적 요구사항 정의, 요구사항 명세서(SRS) 작성, 요구사항 검토
- **2단계 (설계)**: 시스템 아키텍처 설계, 상세 설계(모듈, DB, UI), 인터페이스 설계, 설계 문서(SDD) 작성
- **3단계 (구현)**: 코딩, 단위 테스트, 코드 리뷰, 실행 가능한 소스 코드 산출
- **4단계 (테스트)**: 통합 테스트, 시스템 테스트, 인수 테스트, 테스트 보고서 작성
- **5단계 (유지보수)**: 운영 배포, 오류 수정, 기능 개선, 업데이트

**핵심 알고리즘/공식**:

```
[폭포수 모델 단계별 문서]

1. 요구사항 분석
   ├── 요구사항 명세서 (SRS - Software Requirements Specification)
   ├── 유스케이스 명세서
   └── 요구사항 추적 매트릭스 (RTM)

2. 설계
   ├── 설계 문서 (SDD - Software Design Document)
   ├── 아키텍처 설계서
   ├── DB 설계서 (ERD)
   └── 인터페이스 설계서

3. 구현
   ├── 소스 코드
   ├── 단위 테스트 코드
   └── 코딩 표준 준수서

4. 테스트
   ├── 테스트 계획서
   ├── 테스트 케이스
   ├── 테스트 시나리오
   └── 테스트 보고서

5. 유지보수
   ├── 운영 매뉴얼
   ├── 사용자 가이드
   └── 변경 이력서

[단계별 노력 분포 (COCOMO)]

계획/요구분석: 8%
설계: 18%
구현: 46% (코딩 + 단위 테스트)
테스트: 28%
```

**코드 예시** (필수: Python 또는 의사코드):

```python
"""
폭포수 모델 프로세스 시뮬레이터
- 각 단계별 산출물 관리
- 단계 완료 조건 검증
- 진척도 추적
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum, auto
from datetime import datetime

class Phase(Enum):
    """개발 단계"""
    REQUIREMENTS = auto()
    DESIGN = auto()
    IMPLEMENTATION = auto()
    TESTING = auto()
    MAINTENANCE = auto()

@dataclass
class Deliverable:
    """산출물"""
    name: str
    description: str
    required: bool = True
    completed: bool = False
    approved: bool = False

@dataclass
class PhaseResult:
    """단계 결과"""
    phase: Phase
    start_date: datetime = None
    end_date: datetime = None
    deliverables: List[Deliverable] = field(default_factory=list)
    review_passed: bool = False

    @property
    def completion_rate(self) -> float:
        if not self.deliverables:
            return 0.0
        completed = sum(1 for d in self.deliverables if d.completed)
        return completed / len(self.deliverables) * 100

    @property
    def approval_rate(self) -> float:
        if not self.deliverables:
            return 0.0
        approved = sum(1 for d in self.deliverables if d.approved)
        return approved / len(self.deliverables) * 100


class WaterfallProject:
    """폭포수 모델 프로젝트 관리자"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.current_phase = Phase.REQUIREMENTS
        self.phase_results: Dict[Phase, PhaseResult] = {
            Phase.REQUIREMENTS: PhaseResult(
                phase=Phase.REQUIREMENTS,
                deliverables=[
                    Deliverable("SRS", "요구사항 명세서"),
                    Deliverable("유스케이스 명세서", "Use Case 명세서"),
                    Deliverable("RTM", "요구사항 추적 매트릭스"),
                ]
            ),
            Phase.DESIGN: PhaseResult(
                phase=Phase.DESIGN,
                deliverables=[
                    Deliverable("SDD", "설계 문서"),
                    Deliverable("아키텍처 설계서", "시스템 구조 설계"),
                    Deliverable("DB 설계서", "데이터베이스 설계"),
                    Deliverable("인터페이스 설계서", "API 명세서"),
                ]
            ),
            Phase.IMPLEMENTATION: PhaseResult(
                phase=Phase.IMPLEMENTATION,
                deliverables=[
                    Deliverable("소스 코드", "프로그램 소스"),
                    Deliverable("단위 테스트", "Unit Test 코드"),
                ]
            ),
            Phase.TESTING: PhaseResult(
                phase=Phase.TESTING,
                deliverables=[
                    Deliverable("테스트 계획서", "Test Plan"),
                    Deliverable("테스트 케이스", "Test Cases"),
                    Deliverable("테스트 보고서", "Test Report"),
                ]
            ),
            Phase.MAINTENANCE: PhaseResult(
                phase=Phase.MAINTENANCE,
                deliverables=[
                    Deliverable("운영 매뉴얼", "Operations Manual"),
                    Deliverable("사용자 가이드", "User Guide"),
                ]
            ),
        }
        self.history: List[Dict] = []

    def start_phase(self, phase: Phase) -> None:
        """단계 시작"""
        self.current_phase = phase
        self.phase_results[phase].start_date = datetime.now()
        print(f"\n[Waterfall] {phase.name} 단계 시작")

    def complete_deliverable(self, phase: Phase, deliverable_name: str,
                            approved: bool = True) -> None:
        """산출물 완료"""
        result = self.phase_results[phase]
        for d in result.deliverables:
            if d.name == deliverable_name:
                d.completed = True
                d.approved = approved
                print(f"  ✓ {deliverable_name} 완료 (승인: {approved})")

    def review_phase(self, phase: Phase) -> bool:
        """단계 검토 (Phase Review)"""
        result = self.phase_results[phase]

        # 필수 산출물 모두 완료되었는지 확인
        required_complete = all(
            d.completed and d.approved
            for d in result.deliverables if d.required
        )

        if required_complete:
            result.review_passed = True
            result.end_date = datetime.now()
            print(f"\n[Waterfall] {phase.name} 단계 검토 통과!")
            print(f"  완료율: {result.completion_rate:.1f}%")
            print(f"  승인율: {result.approval_rate:.1f}%")
            return True
        else:
            print(f"\n[Waterfall] {phase.name} 단계 검토 실패")
            incomplete = [d.name for d in result.deliverables
                         if d.required and not d.completed]
            print(f"  미완료 산출물: {incomplete}")
            return False

    def advance_to_next_phase(self) -> bool:
        """다음 단계로 진행"""
        current_result = self.phase_results[self.current_phase]

        if not current_result.review_passed:
            print(f"[Waterfall] 현재 단계 검토 미통과 - 진행 불가")
            return False

        phases = list(Phase)
        current_idx = phases.index(self.current_phase)

        if current_idx < len(phases) - 1:
            self.history.append({
                "phase": self.current_phase.name,
                "completed_at": datetime.now()
            })
            next_phase = phases[current_idx + 1]
            print(f"[Waterfall] {self.current_phase.name} → {next_phase.name}")
            self.current_phase = next_phase
            return True
        return False

    def get_project_status(self) -> Dict[str, Any]:
        """프로젝트 현황"""
        total_deliverables = sum(
            len(r.deliverables) for r in self.phase_results.values()
        )
        completed = sum(
            1 for r in self.phase_results.values()
            for d in r.deliverables if d.completed
        )

        return {
            "project_name": self.project_name,
            "current_phase": self.current_phase.name,
            "total_deliverables": total_deliverables,
            "completed_deliverables": completed,
            "overall_progress": f"{completed}/{total_deliverables}",
            "phases_completed": sum(1 for r in self.phase_results.values()
                                   if r.review_passed)
        }


class VModelProject(WaterfallProject):
    """V-모델 프로젝트 - 테스트 중심"""

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self.test_mapping = {
            Phase.REQUIREMENTS: "인수 테스트",
            Phase.DESIGN: "시스템 테스트",
            Phase.IMPLEMENTATION: "통합 테스트",
            # 구현 단계는 단위 테스트
        }

    def create_test_plan(self, phase: Phase) -> str:
        """개발 단계에 대응하는 테스트 계획 수립"""
        if phase in self.test_mapping:
            test_type = self.test_mapping[phase]
            print(f"[V-Model] {phase.name} → {test_type} 계획 수립")
            return test_type
        elif phase == Phase.IMPLEMENTATION:
            print(f"[V-Model] 구현 → 단위 테스트 수행")
            return "단위 테스트"
        return None


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("폭포수 모델 시뮬레이터")
    print("=" * 60)

    # 프로젝트 생성
    project = WaterfallProject("공공 SI 프로젝트")

    # 요구사항 분석 단계
    project.start_phase(Phase.REQUIREMENTS)
    project.complete_deliverable(Phase.REQUIREMENTS, "SRS", approved=True)
    project.complete_deliverable(Phase.REQUIREMENTS, "유스케이스 명세서", approved=True)
    project.complete_deliverable(Phase.REQUIREMENTS, "RTM", approved=True)

    if project.review_phase(Phase.REQUIREMENTS):
        project.advance_to_next_phase()

    # 설계 단계
    project.start_phase(Phase.DESIGN)
    project.complete_deliverable(Phase.DESIGN, "SDD", approved=True)
    project.complete_deliverable(Phase.DESIGN, "아키텍처 설계서", approved=True)
    project.complete_deliverable(Phase.DESIGN, "DB 설계서", approved=True)
    project.complete_deliverable(Phase.DESIGN, "인터페이스 설계서", approved=True)

    if project.review_phase(Phase.DESIGN):
        project.advance_to_next_phase()

    # 현황 출력
    print(f"\n📊 프로젝트 현황:")
    status = project.get_project_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # V-모델 예시
    print("\n" + "=" * 60)
    print("V-모델 시뮬레이터")
    print("=" * 60)

    v_project = VModelProject("안전 중요 시스템")
    v_project.create_test_plan(Phase.REQUIREMENTS)
    v_project.create_test_plan(Phase.DESIGN)
    v_project.create_test_plan(Phase.IMPLEMENTATION)
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **명확한 단계 구분**: 각 단계가 명확히 구분됨, 진행 상황 파악 용이 | **유연성 부족**: 요구사항 변경 어려움, 이전 단계로 복귀 곤란 |
| **문서화 중심**: 모든 단계에서 문서 산출물, 유지보수에 유리 | **실제 개발과 불일치**: 실제로는 순차적으로 진행 안 됨 |
| **관리 용이**: 진척도 관리 쉬움, 예측 가능한 일정 | **사용자 피드백 지연**: 개발 후반에야 결과 확인 |
| **요구사항 고정**: 초기에 요구사항 확정, 범위 관리 용이 | **위험 노출 지연**: 문제를 나중에 발견, 수정 비용 증가 |

**폭포수 vs 애자일 비교** (필수: 2개 대안):

| 비교 항목 | 폭포수 모델 | 애자일 | 하이브리드 |
|---------|------------|--------|-----------|
| **핵심 특성** | ★ 순차적, 문서 중심 | 반복적, 협업 중심 | 단계는 폭포수, 내부는 애자일 |
| **요구사항** | 초기 고정 | 지속적 변경 | 주요 건은 고정, 세부는 유연 |
| **고객 참여** | 시작/끝 | ★ 지속적 | 마일스톤별 참여 |
| **변경 대응** | 어려움 | ★ 유연함 | 단계 내에서 유연 |
| **문서화** | ★ 강조 | 최소화 | 주요 산출물만 |
| **적합 환경** | 안전 중요, 공공, SI | 스타트업, 신규 개발 | 대규모 엔터프라이즈 |

> **★ 선택 기준**: 요구사항 명확·안전 중요 → 폭포수, 불확실성 높음·빠른 피드백 → 애자일, 규모 크고 통제 필요 → 하이브리드

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **공공 SI** | 폭포수 + CMMI, 철저한 문서화 | 계약 이행률 100%, 감사 대응 용이 |
| **안전 중요 시스템** | V-모델, 테스트 중심 | 안전성 99.99%, 인증 획득 |
| **대규모 엔터프라이즈** | 하이브리드 (마일스톤별 리뷰) | 통제력 + 유연성 동시 확보 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: NASA 우주선 개발** - 폭포수 + V-모델로 안전성 확보. 수천 페이지 문서화, 엄격한 단계별 검증. 99.999% 신뢰성 달성

- **사례 2: 원자력 발전소 제어 시스템** - IEC 61513 표준 기반 폭포수. 안전 등급 SIL 4 달성. 10년 개발 기간, 0건 치명적 결함

- **사례 3: 삼성전자 임베디드** - 초기 설계는 폭포수, 세부 구현은 애자일. 하이브리드로 품질·속도 균형

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: 요구사항 안정성, 시스템 복잡도, 레거시 연동 필요성
2. **운영적**: 프로젝트 관리 성숙도, PM 역량, 문서화 문화
3. **보안적**: 보안 요구사항 명확화, 컴플라이언스 준수, 감사 대응
4. **경제적**: 초기 문서화 비용, 변경 비용, 계약 구조

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **문서 형식주의**: 산출물만 만들고 내용은 부실 - 실용적 문서화 필요
- ❌ **단계 역행 금지**: 변경 요청 무조건 거부 - 적절한 변경 관리 프로세스 필요
- ❌ **테스트 후행**: 테스트를 마지막에 몰아서 - V-모델로 조기 테스트 계획

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  폭포수 모델 핵심 연관 개념 맵                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [V-모델] ←──→ [폭포수] ←──→ [애자일]                          │
│        ↓              ↓               ↓                         │
│   [테스트 중심]    [CMMI]         [스크럼]                       │
│        ↓              ↓               ↓                         │
│   [안전 시스템]    [공공 SI]      [DevOps]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| V-모델 | 확장 모델 | 테스트 중심 폭포수 | `[software_testing](../testing/software_testing.md)` |
| 애자일 | 대안 방법론 | 반복적 접근 | `[agile_methodology](./agile_methodology.md)` |
| CMMI | 성숙도 모델 | 프로세스 품질 평가 | `[cmmi_model](../management/cmmi_model.md)` |
| 요구사항 공학 | 선행 활동 | SRS 작성 기법 | `[requirements_engineering](./requirements_engineering.md)` |
| 프로젝트 관리 | 지원 활동 | 일정·비용 관리 | `[project_management](../management/project_management.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **예측 가능성** | 일정·비용 추정 정확도 | 일정 준수율 90% 이상 |
| **문서화** | 체계적 산출물 관리 | 감사 이슈 0건 |
| **품질** | 단계별 검증으로 결함 조기 발견 | 후반 결함 50% 감소 |
| **계약 준수** | 명확한 인도물 정의 | 계약 이행률 100% |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 기반 문서 자동 생성, 자동화된 단계 검증, 디지털 트윈으로 시뮬레이션

2. **시장 트렌드**: 안전 중요 시스템(자율주행, 의료AI) 수요 증가로 폭포수+V-모델 수요 지속

3. **후속 기술**: Hybrid Agile-Waterfall, Scaled Agile(SAFe)에서의 폭포수 요소 통합

> **결론**: 폭포수 모델은 **요구사항이 명확하고 변경이 적은 프로젝트**에 최적이다. 안전 중요 시스템, 공공 SI, 계약 기반 프로젝트에서는 여전히 유효한 방법론이다. 단, 현대적 환경에서는 **하이브리드 접근**으로 유연성을 확보해야 한다.

> **※ 참고 표준**: IEEE 830(SRS), IEEE 1016(SDD), ISO/IEC 12207(SDLC), IEC 61513(원자력)

---

## 어린이를 위한 종합 설명

폭포수 모델은 마치 **"단계별로 내려가는 미끄럼틀"** 같아요!

미끄럼틀을 탈 때, 한 번 내려가면 다시 올라갈 수 없죠?

**폭포수 모델의 5단계:**

1. **요구사항 분석** (무엇을 만들까?)
   "어떤 장난감을 만들지 정해요!"

2. **설계** (어떻게 만들까?)
   "설계도면을 그려요!"

3. **구현** (만들기!)
   "실제로 조립해요!"

4. **테스트** (잘 작동하나?)
   "작동하는지 확인해요!"

5. **유지보수** (고치기)
   "고장나면 고쳐요!"

**폭포수 모델이 좋을 때:**
- 무엇을 만들지 이미 정확히 알 때
- 중간에 바꾸면 안 되는 중요한 것 (비행기, 원자력발전소)
- 계약서에 적힌 대로 만들어야 할 때

**폭포수 모델이 어려울 때:**
- "이거 좀 바꿔줘!" 하고 자주 말할 때
- 뭘 만들지 아직 확실히 모를 때

이게 바로 폭포수 모델이에요! 🌊
