+++
title = "업무 프로세스 재설계 (BPR)"
date = 2025-03-01

[extra]
categories = "enterprise_systems-methodology"
+++

# 업무 프로세스 재설계 (BPR)

## 핵심 인사이트 (3줄 요약)
> **기존 업무 방식을 근본적으로 재설계**하여 획기적 성과 달성. 프로세스 중심, 고객 중심, IT 활용이 핵심. 하머와 챔피가 제안한 경영 혁신 기법.

## 1. 개념
BPR(Business Process Reengineering)은 **기존의 업무 프로세스를 근본적으로 재고하고 완전히 새롭게 설계**하여 비용, 품질, 서비스, 속도 등에서 획기적인 향상을 이루는 경영 혁신 활동이다.

> 비유: "집 전체 리모델링" - 가구만 바꾸는 게 아니라 구조 자체를 변경

## 2. BPR 핵심 원칙

```
┌────────────────────────────────────────────────────────┐
│                  BPR 핵심 원칙                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 프로세스 중심                                      │
│     - 기능 중심 → 프로세스 중심                        │
│     - 부서 경계 허물기                                 │
│                                                        │
│  2. 고객 중심                                          │
│     - 고객 가치 창출에 집중                            │
│     - 고객 관점에서 프로세스 설계                      │
│                                                        │
│  3. 근본적 재고                                        │
│     - "왜 이 일을 하는가?"                             │
│     - 기존 가정 의문 제기                              │
│                                                        │
│  4. 획기적 향상                                        │
│     - 점진적 개선이 아닌 혁신                          │
│     - 10%가 아닌 100% 이상 개선                        │
│                                                        │
│  5. IT 활용                                            │
│     - 정보 기술을 변화의 도구로 활용                   │
│     - 자동화, 통합, 표준화                             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 기존 vs BPR 후

```
┌────────────────────────────────────────────────────────┐
│              기존 방식 vs BPR 후                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [기존] 기능 중심 조직                                 │
│                                                        │
│  고객 → 영업팀 → 재무팀 → 생산팀 → 배송팀 → 고객     │
│         ↓       ↓       ↓       ↓                      │
│       문서   문서    문서    문서                       │
│         ↓       ↓       ↓       ↓                      │
│       승인   승인    승인    승인                       │
│                                                        │
│  문제: 많은 승인 단계, 문서 이동, 대기 시간           │
│                                                        │
│  ──────────────────────────────────────────────────    │
│                                                        │
│  [BPR 후] 프로세스 중심 조직                           │
│                                                        │
│  고객 ↔ [통합 프로세스 팀] ↔ 고객                     │
│              ↓                                         │
│         단일 접점                                      │
│         권한 위임                                      │
│         IT 시스템                                      │
│                                                        │
│  개선: 승인 단계 축소, 실시간 처리, 고객 만족         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. BPR 추진 단계

```
┌────────────────────────────────────────────────────────┐
│                   BPR 추진 단계                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1단계: 비전 수립                                      │
│     - 경영 목표 설정                                   │
│     - 혁신 범위 결정                                   │
│     - 추진 조직 구성                                   │
│                                                        │
│  2단계: 현황 분석                                      │
│     - AS-IS 프로세스 분석                              │
│     - 문제점 파악                                      │
│     - 벤치마킹                                         │
│                                                        │
│  3단계: 재설계                                         │
│     - TO-BE 프로세스 설계                              │
│     - IT 솔루션 선정                                   │
│     - 조직 재설계                                      │
│                                                        │
│  4단계: 구축                                           │
│     - 시스템 개발                                      │
│     - 교육 훈련                                        │
│     - 파일럿 운영                                      │
│                                                        │
│  5단계: 안정화                                         │
│     - 전면 확산                                        │
│     - 성과 측정                                        │
│     - 지속적 개선                                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum

class ProcessStatus(Enum):
    PENDING = "대기"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    REJECTED = "반려"

@dataclass
class ProcessStep:
    """프로세스 단계"""
    step_id: str
    name: str
    department: str
    handler: str
    duration_hours: float = 0
    status: ProcessStatus = ProcessStatus.PENDING

@dataclass
class BusinessProcess:
    """업무 프로세스"""
    process_id: str
    name: str
    steps: List[ProcessStep] = field(default_factory=list)
    start_time: datetime = None
    end_time: datetime = None

    def total_duration(self) -> float:
        return sum(step.duration_hours for step in self.steps)

    def add_step(self, step: ProcessStep):
        self.steps.append(step)

class TraditionalProcess:
    """전통적 프로세스 (AS-IS)"""

    def __init__(self):
        self.processes: Dict[str, BusinessProcess] = {}

    def create_order_process(self, order_id: str) -> BusinessProcess:
        """주문 프로세스 생성 (많은 단계)"""
        process = BusinessProcess(
            process_id=order_id,
            name="주문 처리",
            start_time=datetime.now()
        )

        # 많은 승인 단계
        steps = [
            ProcessStep("S1", "주문 접수", "영업팀", "영업사원"),
            ProcessStep("S2", "주문 검토", "영업팀", "영업팀장"),
            ProcessStep("S3", "신용 조회", "재무팀", "재무담당"),
            ProcessStep("S4", "재고 확인", "물류팀", "재고관리자"),
            ProcessStep("S5", "생산 요청", "생산팀", "생산계획자"),
            ProcessStep("S6", "출하 지시", "물류팀", "출하담당"),
            ProcessStep("S7", "배송 확인", "물류팀", "배송담당"),
            ProcessStep("S8", "대금 청구", "재무팀", "청구담당"),
        ]

        for step in steps:
            process.add_step(step)

        self.processes[order_id] = process
        return process

    def execute_process(self, process_id: str) -> float:
        """프로세스 실행 (시뮬레이션)"""
        process = self.processes.get(process_id)
        if not process:
            return 0

        total_hours = 0
        for i, step in enumerate(process.steps):
            step.status = ProcessStatus.IN_PROGRESS
            # 각 단계별 처리 시간 (승인 대기 포함)
            duration = 4 + (i % 3) * 2  # 4~8시간
            step.duration_hours = duration
            total_hours += duration
            step.status = ProcessStatus.COMPLETED

        process.end_time = datetime.now()
        return total_hours

class ReengineeredProcess:
    """재설계된 프로세스 (TO-BE)"""

    def __init__(self):
        self.processes: Dict[str, BusinessProcess] = {}

    def create_order_process(self, order_id: str) -> BusinessProcess:
        """주문 프로세스 생성 (간소화)"""
        process = BusinessProcess(
            process_id=order_id,
            name="주문 처리 (재설계)",
            start_time=datetime.now()
        )

        # 통합된 단계
        steps = [
            ProcessStep("S1", "주문 접수 및 처리", "통합팀", "주문담당자"),
            ProcessStep("S2", "자동 재고/신용 확인", "시스템", "IT시스템"),
            ProcessStep("S3", "출하 및 배송", "물류팀", "물류담당"),
        ]

        for step in steps:
            process.add_step(step)

        self.processes[order_id] = process
        return process

    def execute_process(self, process_id: str) -> float:
        """프로세스 실행 (시뮬레이션)"""
        process = self.processes.get(process_id)
        if not process:
            return 0

        total_hours = 0
        for step in process.steps:
            step.status = ProcessStatus.IN_PROGRESS
            if "시스템" in step.handler:
                duration = 0.1  # 자동화: 6분
            else:
                duration = 2  # 사람: 2시간
            step.duration_hours = duration
            total_hours += duration
            step.status = ProcessStatus.COMPLETED

        process.end_time = datetime.now()
        return total_hours

class BPRAnalyzer:
    """BPR 분석"""

    @staticmethod
    def compare_processes(as_is: BusinessProcess, to_be: BusinessProcess) -> Dict:
        """프로세스 비교"""
        return {
            'as_is_steps': len(as_is.steps),
            'to_be_steps': len(to_be.steps),
            'step_reduction': len(as_is.steps) - len(to_be.steps),
            'as_is_duration': as_is.total_duration(),
            'to_be_duration': to_be.total_duration(),
            'duration_improvement': (as_is.total_duration() - to_be.total_duration()) / as_is.total_duration() * 100
        }


# 사용 예시
print("=== BPR 시뮬레이션 ===\n")

# AS-IS (전통적 프로세스)
print("--- AS-IS (전통적 프로세스) ---")
traditional = TraditionalProcess()
as_is = traditional.create_order_process("ORD001")
as_is_duration = traditional.execute_process("ORD001")

print(f"단계 수: {len(as_is.steps)}개")
print(f"총 소요 시간: {as_is_duration}시간")
for step in as_is.steps:
    print(f"  {step.name} ({step.department}): {step.duration_hours}시간")

# TO-BE (재설계된 프로세스)
print("\n--- TO-BE (재설계된 프로세스) ---")
reengineered = ReengineeredProcess()
to_be = reengineered.create_order_process("ORD001")
to_be_duration = reengineered.execute_process("ORD001")

print(f"단계 수: {len(to_be.steps)}개")
print(f"총 소요 시간: {to_be_duration}시간")
for step in to_be.steps:
    print(f"  {step.name} ({step.department}): {step.duration_hours}시간")

# 비교 분석
print("\n--- BPR 효과 분석 ---")
analysis = BPRAnalyzer.compare_processes(as_is, to_be)
print(f"단계 감소: {analysis['as_is_steps']} → {analysis['to_be_steps']} "
      f"({analysis['step_reduction']}개 감소)")
print(f"소요 시간: {analysis['as_is_duration']}시간 → {analysis['to_be_duration']}시간")
print(f"개선율: {analysis['duration_improvement']:.1f}%")
