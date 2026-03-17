+++
title = "714. FMEA / FTA 결함 분석망"
date = "2026-03-15"
weight = 714
[extra]
categories = ["Software Engineering"]
tags = ["Safety", "Quality", "FMEA", "FTA", "Reliability", "Root Cause Analysis", "Risk Assessment"]
+++

# 714. FMEA / FTA 결함 분석망

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 신뢰성 엔지니어링의 핵심 도구로, **FMEA (Failure Mode and Effects Analysis)**는 개별 부품의 고장 파급 효과를 예측하는 상향식(Bottom-up) 분석이며, **FTA (Fault Tree Analysis)**는 최상위 사고(Top Event)를 발생시킨 근본 원인 조합을 논리적으로 규명하는 하향식(Top-down) 분석 기법이다.
> 2. **메커니즘**: FMEA는 **RPN (Risk Priority Number)** 산출을 통해 위험 요소의 우선순위를 정량화하여 설계를 개선하고, FTA는 **부울 대수(Boolean Algebra)**와 논리 게이트를 활용하여 시스템 고장 확률을 수학적으로 계산하거나 **최소 컷셋(Minimal Cut Set)**을 도출한다.
> 3. **가치**: 설계 단계에서 잠재적 결함을 사전에 식별 및 제거하여 유지보수 비용을 획기적으로 절감하고, 항공, 원전, 자율주행 등 안전 중심(Safety-Critical) 시스템의 **기능 안전(Functional Safety)** 표준(IEC 61508, ISO 26262) 준수를 위한 필수 검증 수단이다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
현대의 소프트웨어 및 하드웨어 시스템은 대형화, 복잡화됨에 따라 단일 점의 고장이 전체 시스템의 마비나 인명 피해로 이어질 가능성이 농후합니다. 이에 따라 "사고가 나기 전에 예방하는 것"이 핵심 과제가 되었습니다. **FMEA**는 1950년대 미 항공 우주국(NASA)의 아폴로 프로젝트에서 신뢰성 확보를 위해 처음 도입되었고, **FTA**는 1962년 벨 연구소가 미니트맨 미사일의 발전 제어 시스템 분석을 위해 개발했습니다. 이 두 기법은 상호 보완적으로 작용하며 시스템의 잠재적 취약점을 체계적으로 드러냅니다.

**등장 배경 및 패러다임 변화**
① **기존 한계**: 사고 발생 후 원인을 분석하는 수동적 대응 방식(재발 방지 위주)으로는 복잡한 시스템의 잠재적 결함을 모두 커버 불가.
② **혁신적 패러다임**: 고장 회피(Fault Avoidance)와 고장 허용(Fault Tolerance) 개념을 설계 초기 단계부터 적용하는 '고장 예지(Forecasting)' 철학 등장.
③ **비즈니스 요구**: 리콜 비용 증가, 안전 규제 강화(ISO 26262 등), 서비스 가용성(SLA) 준수를 위한 정량적 위험 관리의 필요성 대두.

---

#### 📊 분석 접근법 시각화

```text
      [ 시간 축과 접근 방향성 ]

      과거 (Design Phase)          현재 (Operation)          미래 (Evolution)
          │                            │                         │
    ──────┴─────────────      ─────────┴───────────      ────────┴──────────
          │                            │                         │
    [PREVENTION]                  [MITIGATION]               [AI & AUTO]
  
    ┌───────────────────┐          ┌───────────────────┐       ┌──────────────────┐
    │  FMEA             │          │  RCA (Post)       │       │  AI-driven        │
    │  (사전 예방)       │    +     │  (사후 조치)       │  ->   │  Safety Analysis  │
    │                   │          │                   │       │                   │
    │  FTA              │          │  Real-time        │       │  Digital Twin     │
    │  (원인 규명)       │          │  Monitoring       │       │  Simulation       │
    └───────────────────┘          └───────────────────┘       └──────────────────┘
    
    ▲                            ▲
    │                            │
    [Bottom-up]                [Top-down]
    (부품 -> 시스템)             (시스템 -> 부품)
```

*도입 서술*: FMEA는 기본 구성 요소의 고장이 시스템 전체에 미칠 영향을 상향식으로 분석하는 반면, FTA는 특정 시스템 고장(최상위 사건)이 발생할 수 있는 원인 조합을 하향식으로 논리적으로 분해합니다. 위 다이어그램은 시간의 흐름에 따른 예방적 조치의 중요성과 두 기법의 접근 방향성을 대조적으로 보여줍니다.

**해설**:
FMEA는 개별 부품(예: 저항, 서브 루틴) 수준에서 시작하여 "이것이 고장 나면 시스템은 어떻게 되는가?"를 질문하며 위험도를 평가합니다. 반면 FTA는 "시스템이 멈췄다. 무엇이 원인인가?"라는 거시적인 질문에서 시작하여 논리 게이트(AND, OR)를 통해 근본 원인을 좁혀갑니다. 두 기법은 복잡한 시스템 안전을 확보하는 두 개의 바퀴와 같아서, 현대의 기술사는 이를 적절히 혼용하여 위험을 관리해야 합니다.

> **📢 섹션 요약 비유**: 마치 건물을 지을 때, FMEA는 **'각각의 벽돌과 시멘트의 강도를 미리 검사(상향식)'**하여 붕괴를 막는 공사이고, FTA는 **'건물이 무너진 가상의 시나리오를 가정하고 설계도면을 뒤져(하향식)'** 구조적 결함을 찾아내는 구조 안전 진단과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 FMEA와 FTA의 내부 매커니즘, 수학적 모델, 그리고 구현 프로세스를 심층적으로 분석합니다.

#### 1. FMEA (Failure Mode and Effects Analysis) 상세 구조

**구성 요소 및 상세 동작**

| 요소명 | 역할 | 내부 동작 메커니즘 | 산출물/지표 |
|:---:|:---|:---|:---|
| **아이템 (Item)** | 분석 대상 시스템 | 시스템을 기능적 블록이나 물리적 부품으로 분해 (WBS 작성) | 시스템 계층 구조도 |
| **고장 모드 (Failure Mode)** | 고장의 형태 | "단락(Short)", "개방(Open)", "노이즈", "지연" 등 구체적인 실패 형태 정의 | 고장 모드 목록 |
| **고장 영향 (Effect)** | 파급 효과 | 국부적(Local) -> 상위(System) -> 최종(End User) 단계로 영향 파급 분석 | 영향 분석 보고서 |
| **심각도 (Severity)** | 피해 규모 | 1(무시) ~ 10(재앙) 등급으로 매핑 (안전 규정 기반) | S 점수 |
| **발생 빈도 (Occurrence)** | 발생 확률 | 과거 데이터, MTBF(Mean Time Between Failures) 기반 빈도 산출 | O 점수 |
| **검출 난이도 (Detection)** | 발견 용이성 | 현재의 테스트나 모니터링으로 고장을 발견할 확률 (낮을수록 위험) | D 점수 |
| **RPN (Risk Priority Number)** | 위험 우선순위 | **$RPN = S \times O \times D$** 계산. 임계값(Cutoff) 이상 항목은 개선 조치 필수 | 위험 우선순위 리스트 |

#### 2. FTA (Fault Tree Analysis) 상세 구조

**핵심 논리 및 수학적 원리**
FTA는 **부울 대수(Boolean Algebra)**에 기초하며, 논리 게이트를 사용하여 기본 사건(Basic Event)들의 조합이 최상위 사간(Top Event)을 유발하는 경로를 트리 형태로 표현합니다.

*   **기호 정의**:
    *   **Top Event**: 분석하고자 하는 시스템의 최종 고장 상태.
    *   **Intermediate Event**: 중간 단계의 사건.
    *   **Basic Event**: 더 이상 분해되지 않는 최소 원인(예: 부품 고장).
    *   **AND Gate**: 입력 사건이 **모두** 동시에 발생해야 출력 사건이 발생 (중복 장치 등의 안전성 평가).
    *   **OR Gate**: 입력 사건 중 **하나라도** 발생하면 출력 사건이 발생 (단일 점 고장 취약성 평가).

*   **정량적 분석 (Quantitative Analysis)**:
    최상위 사건의 발생 확률 $P(Top)$은 기본 사건들의 확률 $P(E_i)$를 통해 계산합니다.
    *   OR Gate 연결 시: $P(Top) = 1 - \prod (1 - P(E_i))$
    *   AND Gate 연결 시: $P(Top) = \prod P(E_i)$

---

#### 📊 FTA 논리 게이트 및 최소 컷셋 분석

```text
      [ Top Event: 전력 공급 시스템 완전 정지 ]
                  │
          ┌───────┴────────┐
          ▼                ▼
     [ OR Gate ]      [ Main Power OK? ]
          │                │ (No)
    ┌─────┴──────┐         │
    ▼            ▼         ▼
[Backup Fail]  [Main Fail]
 (A)            (B)
    │            │
    ▼            ▼
[ AND Gate ]  [ Basic: S1 Cut ]
    │
  ──┴──
  │  │
  ▼  ▼
(B)  (C)
[Chg Fail] [Bat Fail]

[ 해설 ]
1. 최상위 사건(Top)은 '주전력 실패(B)' 혹은 '예비전력 실패(A)' 둘 중 하나만 발생해도 발생합니다. (OR 관계)
2. 예비전력 실패(A)는 충전기 고장(B)과 배터리 고장(C)이 **동시에** 발생해야만 합니다. (AND 관계)
3. 만약 B(주전력 실패)가 발생하면 시스템은 다운됩니다. (단일 장점 고장, Single Point of Failure)
4. 하지만 주전력이 정상일 때, 예비전력(A)가 작동하려면 B와 C가 모두 고장 나야 하므로 상대적으로 안전합니다.
5. 최소 컷셋(MCS):
   - { B }
   - { B, C } -> B만 있어도 실패하므로 {B}가 가장 치명적인 컷셋입니다.
```

*도입 서술*: FTA는 복잡한 시스템의 고장 경로를 논리적으로 시각화합니다. 위 다이어그램은 전력 공급 시스템의 안정성을 분석하는 간단한 결함 수 트리(Fault Tree)를 예시로 보여줍니다. OR 게이트는 단일 고장에 대한 취약성을, AND 게이트는 중복 설계(Redundancy)의 효과를 나타냅니다.

**해설**:
FTA의 가장 강력한 기능은 **최소 컷셋(Minimal Cut Set, MCS)**을 찾아내는 것입니다. MCS는 시스템 고장을 일으키기에 충분한 최소한의 기본 사건들의 집합입니다. 위 예제에서 `{주전력 실패}`는 MCS이므로, 이 주전력 라인이 단일 점 고장(SPOF)이 될 가능성이 높음을 즉시 파악할 수 있습니다. 기술사는 이 분석을 바탕으로 SPOF를 제거하기 위해 주전력 라인을 이중화하는 등의 설계 변경을 제안할 수 있습니다. 또한, AND 게이트에 연결된 `{충전기 고장, 배터리 고장}` 집합은 두 가지가 동시에 발생해야 문제가 되므로, 상대적으로 안전한 경로임을 알 수 있습니다.

#### 3. FMEA RPN 계산 예시 (코드 스타일)

FMEA 분석은 보통 엑셀이나 전문 도구를 통해 수행되지만, 그 핵심 로직은 아래와 같은 의사코드로 정리할 수 있습니다.

```python
# FMEA Risk Priority Calculation Logic
def calculate_rpn(severity, occurrence, detection):
    """
    Calculate Risk Priority Number (RPN).
    ref: MIL-STD-1629A
    """
    if not (1 <= severity <= 10): raise ValueError("Severity out of range")
    if not (1 <= occurrence <= 10): raise ValueError("Occurrence out of range")
    if not (1 <= detection <= 10): raise ValueError("Detection out of range")
    
    rpn = severity * occurrence * detection
    return rpn

# Example Scenario: Disk Controller Failure
# Severity: 9 (Data Loss, Critical)
# Occurrence: 4 (Low Frequency)
# Detection: 7 (Hard to detect before crash)

disk_risk = calculate_rpn(9, 4, 7) # Result: 252
# Action Required: If RPN > 100 (Threshold), Mitigation is mandatory.
```

> **📢 섹션 요약 비유**: FMEA는 각 선수들의 **'개인 기량 부족(RPN)을 점검하는 리스트'**라면, FTA는 **'팀이 패배한 경기(Top Event)를 분석하기 위해 경기 영상을 다시 보며 패스 플레이(Logic Gate)를 추적하는 분석가'**와 같습니다. FMEA가 "개인", FTA는 "조합 및 경로"에 집중합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

FMEA와 FTA는 상호 배타적이지 않으며, 실무에서는 이 두 기법을 결합하여 시스템의 안전성을 입증(Verification & Validation)합니다.

#### 1. 심층 기술 비교 분석표

| 구분 | FMEA (Failure Mode and Effects Analysis) | FTA (Fault Tree Analysis) |
|:---|:---|:---|
| **분석 방향** | **상향식 (Bottom-up)**: 개별 부품 → 시스템 | **하향식 (Top-down)**: 시스템 → 부품 |
| **접근 방식** | 귀납적 (Inductive): "이 부품이 고장 나면?" | 연역적 (Deductive): "사고는 무엇 때문에?" |
| **주요 산출물** | FMEA 시트, RPN 리스트, 개선 권고안 | Fault Tree 다이어그램, MCS, 고장 확률 |
| **강점 (Strength)** | 모든 가능한 고장 모드를 누락 없이 식별 가능. 설계 초기에 효과적. | 특정 중대 사고의 근본 원인과 확률적 의존성을 명확히 규명. |
| **약점 (Weakness)** | 고장 간의 복잡한 상호작용(결합 고장) 분석이 어려움. 분석이 방대해짐. | 중요하