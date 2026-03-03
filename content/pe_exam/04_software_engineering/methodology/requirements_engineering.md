+++
title = "요구사항 공학 (Requirements Engineering)"
date = 2026-03-02

[extra]
categories = "pe_exam-software_engineering-methodology"
+++

# 요구사항 공학 (Requirements Engineering)

## 핵심 인사이트 (3줄 요약)
> **소프트웨어가 무엇을 해야 하는지 명확히 정의**하는 체계적 활동으로, 기능적/비기능적 요구사항을 수집·분석·명세·검증한다. 요구사항 오류는 후반 수정 비용이 기하급수적으로 증가한다(100배). SMART, MoSCoW, 유스케이스가 핵심 도구다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 요구사항 공학(Requirements Engineering)은 **고객/이해관계자가 원하는 것을 발견하고, 분석하고, 문서화하고, 검증하는 체계적 프로세스**다. 소프트웨어의 성패를 결정하는 가장 중요한 단계다.

> 💡 **비유**: 요구사항 공학은 **"건축 설계도 작성 전 건축주 요구 파악"** 같아요. 무엇을 지을지 명확히 해야 제대로 된 설계가 가능하죠. "그냥 좋은 집 지어주세요"라고 하면 건축가는 망연자실해요!

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점 - 요구사항 불명확**: 전체 프로젝트 실패의 56%가 요구사항 문제(Standish Group). "알아서 잘 해줘" 식 요청으로 개발 착수

2. **기술적 필요성 - 변경 비용 폭증**: Boehm의 연구에 따르면 요구사항 단계 수정 비용 1배 → 운영 단계 100배. 조기 명확화 필수

3. **시장/산업 요구 - 복잡성 증가**: 현대 시스템은 수백 개의 이해관계자, 상충하는 요구사항, 규제 준수 요구. 체계적 관리 필요

**핵심 목적**: **명확하고 완전하며 검증 가능한 요구사항 도출로 프로젝트 실패 예방**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **도출 (Elicitation)** | 이해관계자로부터 요구 수집 | 인터뷰, 워크숍, 관찰 | 인터뷰 |
| **분석 (Analysis)** | 요구사항 충돌 해결, 우선순위 | MoSCoW, 협상 | 필터링 |
| **명세 (Specification)** | 문서화, SRS 작성 | SMART, 유스케이스 | 계약서 |
| **검증 (Validation)** | 요구사항 검토, 인수 테스트 | 인스펙션, 프로토타입 | 더블체크 |
| **관리 (Management)** | 변경 관리, 추적성 유지 | RTM, 기준선 | 버전 관리 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│              요구사항 공학 프로세스                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐                          ┌──────────────┐           │
│   │   이해관계자  │                          │    환경      │           │
│   │  (Stakeholder)│                          │ (Environment)│           │
│   └──────┬───────┘                          └──────┬───────┘           │
│          │                                         │                    │
│          ▼                                         ▼                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      요구사항 공학 프로세스                       │  │
│   │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐       │  │
│   │  │  도출   │ →  │  분석   │ →  │  명세   │ →  │  검증   │       │  │
│   │  │Elicitation│ Analysis│Specification│Validation│      │  │
│   │  └─────────┘    └─────────┘    └─────────┘    └─────────┘       │  │
│   │       ↑              ↑              ↑              ↑             │  │
│   │       └──────────────┴──────────────┴──────────────┘             │  │
│   │                     관리 (Management)                            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│                    ┌──────────────┐                                    │
│                    │  요구사항     │                                    │
│                    │  명세서(SRS)  │                                    │
│                    └──────────────┘                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│              요구사항 분류 체계                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  기능적 요구사항 (Functional Requirements)                              │
│  "시스템이 무엇을 해야 하는가"                                         │
│  예: 사용자는 로그인할 수 있어야 한다                                  │
│      상품 목록을 조회할 수 있어야 한다                                 │
│                                                                         │
│  비기능적 요구사항 (Non-Functional Requirements)                        │
│  "시스템이 어떻게 해야 하는가" (품질 속성)                             │
│  ├── 성능: 응답시간 1초 이내, TPS 1000                                │
│  ├── 가용성: 99.9% (연간 다운타임 8.7시간)                            │
│  ├── 보안: AES-256 암호화, 접근 제어                                  │
│  ├── 확장성: 사용자 10배 증가 시 성능 유지                            │
│  ├── 유지보수성: 모듈 교체 4시간 내 완료                              │
│  └── 이식성: Linux/Windows 동작                                       │
│                                                                         │
│  도메인 요구사항 (Domain Requirements)                                 │
│  "해당 분야 규정/제약"                                                 │
│  예: 금융 → IFRS 회계 기준, 개인정보보호법                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│              유스케이스 다이어그램                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                 온라인 쇼핑몰 시스템                              │  │
│   │                                                                 │  │
│   │  [고객]─────(상품 검색)                                         │  │
│   │      │────(장바구니 추가)                                       │  │
│   │      │────(주문하기)───────«include»──(결제처리)                │  │
│   │      │────(주문 취소)──────«extend»──(환불처리)                 │  │
│   │                                                                 │  │
│   │  [관리자]──(상품 등록)                                          │  │
│   │         ──(주문 관리)                                           │  │
│   │                                                                 │  │
│   │  include: 항상 포함됨 (주문 → 결제 필수)                        │  │
│   │  extend: 선택적 포함 (취소 → 환불 가능)                         │  │
│   │  generalization: 상속 관계                                      │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 도출 → ② 분석 → ③ 명세 → ④ 검증 → ⑤ 관리
```

- **1단계 (도출 - Elicitation)**: 인터뷰, 설문조사, 워크숍, 사용 사례(Use Case) 분석, 프로토타이핑, 문서 분석, 관찰
- **2단계 (분석 - Analysis)**: 충돌 요구사항 해결, 우선순위 결정(MoSCoW), 실현 가능성 검토, 프로토타입 검증
- **3단계 (명세 - Specification)**: SRS 작성, 유스케이스 다이어그램, 자연어→형식 언어 변환, 추적성 매트릭스
- **4단계 (검증 - Validation)**: 요구사항 리뷰/인스펙션, 완전성·일관성·명확성 확인, 프로토타입 검증, 인수 테스트 케이스
- **5단계 (관리 - Management)**: 변경 관리, 추적성(요구사항↔설계↔테스트), 기준선(Baseline) 설정

**핵심 알고리즘/공식**:

```
[요구사항 품질 기준 - SMART]

| 기준 | 의미 | 나쁜 예 | 좋은 예 |
|------|------|---------|---------|
| S (Specific) | 구체적 | "빠르게" | "2초 이내" |
| M (Measurable) | 측정 가능 | "안정적" | "99.9% 가용성" |
| A (Achievable) | 달성 가능 | "완벽" | "결함 밀도 < 0.5/KLOC" |
| R (Relevant) | 관련성 | "AI 적용" | "추천 알고리즘으로 구매율 10% 향상" |
| T (Timely) | 시간 기준 | "나중에" | "v1.0 출시(6월 30일) 전" |

[MoSCoW 우선순위]

Must have:   반드시 있어야 함 (없으면 실패)
Should have: 있으면 상당히 좋음 (중요하지만 MVP 아님)
Could have:  있으면 좋음 (여유 시 포함)
Won't have:  이번에는 포함 안 함 (다음 버전)

예시:
"로그인" → Must (필수)
"소셜 로그인" → Should (중요하지만 MVP 아님)
"다크 모드" → Could (여유 시)
"AR 가상 피팅" → Won't (다음 버전)

[요구사항 오류 비용 (Boehm)]

           비용
            │                              ○ 운영 단계
            │                         ○
            │                    ○
            │               ○
            │          ○
            │     ○
            │ ○
            └──────────────────────────────── 개발 단계
          요구  설계 구현 테스트 검수 운영

요구사항 오류 수정 비용 = 1배
설계 단계 수정 = 5배
구현 단계 수정 = 10배
테스트 단계 수정 = 20배
운영 중 수정 = 100배+

→ 요구사항을 명확히 하는 것이 가장 큰 ROI

[요구사항 추적성 매트릭스 (RTM)]

| 요구사항 ID | 설계 문서 | 코드 모듈 | 테스트 케이스 |
|------------|----------|----------|--------------|
| REQ-001 | SDD-3.1 | auth.py | TC-101, TC-102 |
| REQ-002 | SDD-3.2 | payment.py | TC-201 |

→ 변경 영향 분석, 커버리지 검증
```

**코드 예시** (필수: Python 요구사항 관리):

```python
"""
요구사항 공학 시스템
- 요구사항 도출, 분석, 명세, 검증
- MoSCoW 우선순위, SMART 검증
- RTM(추적성 매트릭스) 관리
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum, auto
from datetime import datetime
import re

class Priority(Enum):
    MUST = 1      # 필수
    SHOULD = 2    # 중요
    COULD = 3     # 희망
    WONT = 4      # 제외

class RequirementType(Enum):
    FUNCTIONAL = auto()      # 기능적
    NON_FUNCTIONAL = auto()  # 비기능적
    DOMAIN = auto()          # 도메인

class RequirementStatus(Enum):
    DRAFT = auto()
    ELICITED = auto()
    ANALYZED = auto()
    SPECIFIED = auto()
    VALIDATED = auto()
    APPROVED = auto()

@dataclass
class Stakeholder:
    """이해관계자"""
    name: str
    role: str
    contact: str
    priority: int = 1  # 1=최우선, 5=낮음

@dataclass
class Requirement:
    """요구사항"""
    id: str
    title: str
    description: str
    req_type: RequirementType
    priority: Priority
    status: RequirementStatus = RequirementStatus.DRAFT
    source: Optional[str] = None  # 출처 (이해관계자)
    rationale: str = ""  # 이유
    fit_criterion: str = ""  # 수용 기준 (측정 가능한)
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.priority.name})"


class SMARTValidator:
    """SMART 검증기"""

    @staticmethod
    def validate(req: Requirement) -> Dict[str, Tuple[bool, str]]:
        """요구사항 SMART 검증"""
        results = {}

        # Specific (구체적)
        vague_words = ["빠르게", "사용자 친화적", "유연한", "효율적인"]
        is_specific = not any(w in req.description for w in vague_words)
        results["Specific"] = (is_specific,
            "구체적임" if is_specific else "모호한 표현 포함")

        # Measurable (측정 가능)
        has_metric = bool(req.fit_criterion) or bool(
            re.search(r'\d+[%초분시일개건]', req.description)
        )
        results["Measurable"] = (has_metric,
            "측정 기준 있음" if has_metric else "측정 기준 없음")

        # Achievable (달성 가능)
        unrealistic_words = ["완벽", "100%", "무제한", "실시간 0초"]
        is_achievable = not any(w in req.description for w in unrealistic_words)
        results["Achievable"] = (is_achievable,
            "달성 가능" if is_achievable else "비현실적 목표")

        # Relevant (관련성)
        has_rationale = bool(req.rationale)
        results["Relevant"] = (has_rationale,
            "이유 명시됨" if has_rationale else "이유 미명시")

        # Timely (시간 기준)
        has_deadline = bool(
            re.search(r'\d+월|\d+일|\d+분기|v\d+', req.description)
        )
        results["Timely"] = (has_deadline or bool(req.fit_criterion),
            "시간 기준 있음" if has_deadline else "시간 기준 없음")

        return results


class RequirementsRepository:
    """요구사항 저장소"""

    def __init__(self):
        self.requirements: Dict[str, Requirement] = {}
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.rtm: Dict[str, Dict] = {}  # 추적성 매트릭스

    def add_requirement(self, req: Requirement) -> None:
        self.requirements[req.id] = req
        self.rtm[req.id] = {
            "design": [],
            "code": [],
            "test": []
        }

    def get_by_priority(self, priority: Priority) -> List[Requirement]:
        return [r for r in self.requirements.values() if r.priority == priority]

    def get_by_type(self, req_type: RequirementType) -> List[Requirement]:
        return [r for r in self.requirements.values() if r.req_type == req_type]

    def link_to_design(self, req_id: str, design_doc: str) -> None:
        if req_id in self.rtm:
            self.rtm[req_id]["design"].append(design_doc)

    def link_to_code(self, req_id: str, code_module: str) -> None:
        if req_id in self.rtm:
            self.rtm[req_id]["code"].append(code_module)

    def link_to_test(self, req_id: str, test_case: str) -> None:
        if req_id in self.rtm:
            self.rtm[req_id]["test"].append(test_case)

    def get_coverage_report(self) -> Dict:
        """커버리지 리포트"""
        total = len(self.requirements)
        with_tests = sum(1 for rtm in self.rtm.values() if rtm["test"])
        with_code = sum(1 for rtm in self.rtm.values() if rtm["code"])

        return {
            "total_requirements": total,
            "test_coverage": with_tests / total * 100 if total > 0 else 0,
            "code_coverage": with_code / total * 100 if total > 0 else 0
        }


class UseCase:
    """유스케이스"""

    def __init__(self, name: str, actor: str):
        self.name = name
        self.actor = actor
        self.preconditions: List[str] = []
        self.postconditions: List[str] = []
        self.main_flow: List[str] = []
        self.alternative_flows: List[str] = []
        self.exceptions: List[str] = []

    def add_step(self, step: str) -> None:
        self.main_flow.append(step)

    def generate_srs_section(self) -> str:
        """SRS 섹션 생성"""
        lines = [
            f"## 유스케이스: {self.name}",
            f"**액터**: {self.actor}",
            "",
            "**사전조건**:",
        ]
        for pre in self.preconditions:
            lines.append(f"- {pre}")

        lines.append("\n**기본 흐름**:")
        for i, step in enumerate(self.main_flow, 1):
            lines.append(f"{i}. {step}")

        if self.alternative_flows:
            lines.append("\n**대안 흐름**:")
            for alt in self.alternative_flows:
                lines.append(f"- {alt}")

        if self.exceptions:
            lines.append("\n**예외 처리**:")
            for exc in self.exceptions:
                lines.append(f"- {exc}")

        lines.append("\n**사후조건**:")
        for post in self.postconditions:
            lines.append(f"- {post}")

        return "\n".join(lines)


class SRSGenerator:
    """요구사항 명세서(SRS) 생성기"""

    def __init__(self, project_name: str, version: str):
        self.project_name = project_name
        self.version = version
        self.repository = RequirementsRepository()

    def add_requirement(self, req: Requirement) -> None:
        self.repository.add_requirement(req)

    def generate_srs(self) -> str:
        """SRS 문서 생성"""
        lines = [
            f"# 소프트웨어 요구사항 명세서 (SRS)",
            f"",
            f"**프로젝트명**: {self.project_name}",
            f"**버전**: {self.version}",
            f"**작성일**: {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "---",
            "",
            "## 1. 개요",
            "",
            "### 1.1 목적",
            "",
            "### 1.2 범위",
            "",
            "### 1.3 용어 정의",
            "",
            "---",
            "",
            "## 2. 기능적 요구사항",
            "",
        ]

        func_reqs = self.repository.get_by_type(RequirementType.FUNCTIONAL)
        for req in func_reqs:
            lines.extend([
                f"### {req.id}: {req.title}",
                f"",
                f"**설명**: {req.description}",
                f"",
                f"**우선순위**: {req.priority.name}",
                f"",
                f"**수용 기준**: {req.fit_criterion}",
                "",
                "---",
                ""
            ])

        lines.extend([
            "## 3. 비기능적 요구사항",
            "",
        ])

        nonfunc_reqs = self.repository.get_by_type(RequirementType.NON_FUNCTIONAL)
        for req in nonfunc_reqs:
            lines.extend([
                f"### {req.id}: {req.title}",
                f"",
                f"**설명**: {req.description}",
                f"",
                f"**수용 기준**: {req.fit_criterion}",
                "",
                "---",
                ""
            ])

        return "\n".join(lines)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("요구사항 공학 시스템")
    print("=" * 60)

    # 요구사항 생성
    reqs = [
        Requirement(
            id="REQ-001",
            title="사용자 로그인",
            description="사용자는 이메일과 비밀번호로 로그인할 수 있어야 한다. 로그인 응답시간은 2초 이내여야 한다.",
            req_type=RequirementType.FUNCTIONAL,
            priority=Priority.MUST,
            source="기획팀",
            rationale="사용자 인증은 서비스 이용의 필수 전제조건",
            fit_criterion="유효한 계정으로 로그인 시 2초 이내 메인 페이지 진입"
        ),
        Requirement(
            id="REQ-002",
            title="시스템 응답시간",
            description="모든 API 호출에 대한 응답시간은 1초 이내여야 한다.",
            req_type=RequirementType.NON_FUNCTIONAL,
            priority=Priority.MUST,
            source="운영팀",
            rationale="사용자 경험 향상",
            fit_criterion="부하 테스트에서 95% 요청이 1초 이내 응답"
        ),
        Requirement(
            id="REQ-003",
            title="소셜 로그인",
            description="사용자는 구글, 카카오 계정으로 로그인할 수 있다.",
            req_type=RequirementType.FUNCTIONAL,
            priority=Priority.SHOULD,
            source="마케팅팀",
            rationale="가입 장벽 낮춤",
            fit_criterion="OAuth 2.0 기반 소셜 로그인 성공"
        ),
    ]

    # SMART 검증
    print("\n1. SMART 검증")
    print("-" * 40)
    validator = SMARTValidator()
    for req in reqs:
        print(f"\n{req.id}: {req.title}")
        results = validator.validate(req)
        for criterion, (passed, msg) in results.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {criterion}: {msg}")

    # RTM 연결
    print("\n\n2. 추적성 매트릭스")
    print("-" * 40)
    repo = RequirementsRepository()
    for req in reqs:
        repo.add_requirement(req)

    repo.link_to_design("REQ-001", "SDD-3.1 인증 모듈")
    repo.link_to_code("REQ-001", "auth/login.py")
    repo.link_to_test("REQ-001", "TC-101 로그인 성공")
    repo.link_to_test("REQ-001", "TC-102 로그인 실패")

    coverage = repo.get_coverage_report()
    print(f"테스트 커버리지: {coverage['test_coverage']:.1f}%")

    # 유스케이스 생성
    print("\n\n3. 유스케이스")
    print("-" * 40)
    login_uc = UseCase("로그인", "사용자")
    login_uc.preconditions = ["회원가입 완료 상태"]
    login_uc.postconditions = ["인증 토큰 발급"]
    login_uc.add_step("사용자가 이메일 입력")
    login_uc.add_step("사용자가 비밀번호 입력")
    login_uc.add_step("로그인 버튼 클릭")
    login_uc.add_step("시스템이 인증 처리")
    login_uc.add_step("메인 페이지 이동")

    print(login_uc.generate_srs_section())
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **프로젝트 실패 예방**: 명확한 요구사항으로 재작업 감소 | **시간 소요**: 초기 단계에서 충분한 시간 필요 |
| **변경 비용 절감**: 조기 오류 발견으로 100배 비용 절감 | **이해관계자 동참 어려움**: 바쁜 이해관계자 확보 |
| **의사소통 개선**: 공통 이해 형성 | **과도한 문서화**: 형식적 문서 작성 오버헤드 |
| **테스트 기반**: 수용 기준이 테스트 케이스 도출 | **불완전성**: 모든 요구사항 발견 불가능 |

**요구사항 도출 기법 비교** (필수: 2개 대안):

| 비교 항목 | 인터뷰 | 워크숍 | 설문조사 | 관찰 |
|---------|-------|-------|----------|------|
| **깊이** | ★ 깊음 | 깊음 | 얕음 | 깊음 |
| **참여자 수** | 1~3명 | 5~15명 | ★ 수백 명 | 1~2명 |
| **비용** | 중간 | 높음 | 낮음 | 높음 |
| **시간** | 1~2시간 | 반나절~1일 | 수일 | 수일 |
| **적합 상황** | 핵심 이해관계자 | 요구사항 협업 | 대규모 사용자 | 현업 업무 파악 |

> **★ 선택 기준**: 핵심 의사결정자 → 인터뷰, 요구사항 충돌 해결 → 워크숍, 일반 사용자 → 설문조사, 실제 업무 파악 → 관찰

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **공공 SI** | SRS 표준 양식, RTM 필수 | 감사 이슈 0건, 요구사항 누락 90% 감소 |
| **애자일** | 사용자 스토리 + 인수 기준 | 스프린트 내 요구사항 변경 50% 감소 |
| **금융** | 규제 요구사항 추적성 | 컴플라이언스 위반 0건 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: NASA** - 체계적 요구사항 관리로 우주선 개발 실패율 80% 감소. 수만 개 요구사항 추적성 유지

- **사례 2: 토스** - 사용자 스토리 + 인수 기준으로 요구사항 명확화. 출시 후 결함 60% 감소

- **사례 3: 삼성전자** - DOORS 도구로 임베디드 요구사항 관리. RTM 자동화로 추적 비용 70% 절감

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: 요구사항 관리 도구(JIRA, DOORS), RTM 자동화, 형상 관리 연동
2. **운영적**: 이해관계자 동참 유도, 요구사항 리뷰 프로세스, 변경 통제위원회(CCB)
3. **보안적**: 보안 요구사항 도출(STRIDE), 개인정보 처리 요구사항
4. **경제적**: 초기 투자 vs 후반 재작업 비용 절감 (ROI: 5~10배)

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **"알아서 해줘"**: 모호한 요구사항으로 개발 착수. 해결: 프로토타입으로 구체화
- ❌ **요구사항 급증**: 무분별한 요구사항 추가. 해결: MoSCoW로 범위 통제
- ❌ **문서만 작성**: 검증 없이 문서만 작성. 해결: 인스펙션, 프로토타입 검증

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  요구사항 공학 핵심 연관 개념 맵                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [UML] ←──→ [요구사항 공학] ←──→ [소프트웨어 설계]              │
│        ↓              ↓               ↓                         │
│   [유스케이스]    [SRS]          [아키텍처]                      │
│        ↓              ↓               ↓                         │
│   [테스트 케이스] [RTM]          [CMMI]                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| UML | 표현 도구 | 유스케이스 다이어그램 | `[uml](../design/uml.md)` |
| 소프트웨어 설계 | 후속 활동 | 요구사항 기반 설계 | `[software_design](../design/software_design.md)` |
| 테스트 | 검증 활동 | 인수 테스트 기준 | `[software_testing](../testing/software_testing.md)` |
| 프로젝트 관리 | 지원 활동 | 범위 관리 | `[project_management](../management/project_management.md)` |
| CMMI | 성숙도 모델 | 요구사항 프로세스 | `[cmmi_model](../management/cmmi_model.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **재작업 감소** | 명확한 요구사항으로 후반 변경 감소 | 재작업 비용 60% 절감 |
| **프로젝트 성공률** | 요구사항 관련 실패 감소 | 성공률 30% 향상 |
| **테스트 효율** | 수용 기준 기반 테스트 케이스 | 테스트 작성 시간 40% 단축 |
| **의사소통** | 공통 이해 형성 | 오해로 인한 이슈 70% 감소 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 기반 요구사항 도출, 자연어 처리로 요구사항 자동 분류, 요구사항 충돌 자동 탐지

2. **시장 트렌드**: 애자일에서 사용자 스토리 중심, 프로토타입/POC로 조기 검증, 지속적 요구사항 관리

3. **후속 기술**: Behavior-Driven Development(BDD), Specification by Example, Living Documentation

> **결론**: 요구사항 공학은 **소프트웨어 개발의 가장 중요한 단계**다. 요구사항 오류는 개발 후반으로 갈수록 수정 비용이 기하급수적으로 증가한다. "요구사항을 명확히 하는 것"이 가장 큰 투자 효율이다.

> **※ 참고 표준**: IEEE 830(SRS), ISO/IEC/IEEE 29148, IIBA BABOK, INCOSE Systems Engineering Handbook

---

## 어린이를 위한 종합 설명

요구사항 공학은 마치 **"레스토랑에서 주문 받기"** 같아요!

**좋지 않은 주문:**
손님: "뭐 맛있는 거 주세요"
요리사: "..." (뭘 만들어야 하지? 😰)

**좋은 주문:**
손님: "스테이크 주세요. 미디엄 레어로, 감자튀김 곁들이기, 15분 안에"
요리사: "네!" (명확하죠? 😊)

**요구사항 공학의 5단계:**

1. **도출** (물어보기)
   "어떤 음식 좋아하세요?"

2. **분석** (정리하기)
   "매운 건 못 드시네요? 그럼 이건 빼요"

3. **명세** (적어두기)
   "주문서: 파스타, 알리오 올리오, 1인분"

4. **검증** (확인하기)
   "이거 맞으세요?"

5. **관리** (변경하기)
   "치즈 추가해주세요" → "네, 추가했어요"

**SMART하게 적기:**
- S (구체적): "빠른" 대신 "2초 이내"
- M (측정): "많이" 대신 "100명까지"
- A (가능): "완벽" 대신 "99%"
- R (관련): 왜 필요한지 이유 적기
- T (시간): "언제까지" 적기

이게 바로 요구사항 공학이에요! 📋
