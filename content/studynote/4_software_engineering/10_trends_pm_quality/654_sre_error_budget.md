+++
title = "654. SRE SLI, SLO, SLA 에러 예산"
date = "2026-03-15"
weight = 654
[extra]
categories = ["Software Engineering"]
tags = ["SRE", "SLI", "SLO", "SLA", "Error Budget", "Reliability", "Google"]
+++

# 654. SRE SLI, SLO, SLA 에러 예산

### # 신뢰성 엔지니어링의 정량적 관리 체계

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구글(Google)이 정립한 **SRE (Site Reliability Engineering)**의 핵심 철학으로, 모호한 '안정성'을 **SLI (Service Level Indicator)**라는 정량적 수치로 치환하고, 이를 기반으로 한 **SLO (Service Level Objective)**를 통해 기술적 목표를 설정한다.
> 2. **메커니즘**: 100% 가용성의 달리기에서 비용 효율성을 잃는 것을 방지하기 위해 **에러 예산(Error Budget)**이라는 개념을 도입하여, '허용 가능한 실패'의 한도 내에서는 과감한 혁신(Release)을, 한도 초과 시에는 보존(Preservation)을 우선하는 **동적 의사결정 프로세스**를 제공한다.
> 3. **가치**: 개발팀(속도)과 운영팀(안정성) 간의 감정적 대립을 데이터 기반의 객관적 협상 테이블로 전환하며, **SLA (Service Level Agreement)** 이행을 위해 내부적으로 여유(Margin)를 두는 방어적 전략을 수립한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
**SRE (Site Reliability Engineering)**는 소프트웨어 엔지니어링 원칙을 IT 인프라 운영(Operation)에 적용하여, 시스템의 안정성(Reliability), 확장성(Scalability), 효율성(Efficiency)을 확보하는 방법론이다. 전통적인 "절대 멈추면 안 된다"는 사고방식에서 벗어나, **"어느 정도의 장애는 비즈니스 목표 달성을 위해 허용 가능하다"**는 실용주의적 접근을 취한다. 이를 통해 조직은 무분별한 기능 추가로 인한 시스템 붕괴나, 반대로 과도한 보수주의로 인한 시장 경쟁력 저하를 방지한다.

### 💡 비유: 자동차의 속도계와 내비게이션
시스템 운영은 자동차 여행과 같다.
- **SLI**는 자동차의 **속도계**이다. "현재 시속 100km로 달리고 있다"는 객관적 데이터를 제공한다.
- **SLO**는 운전자가 설정한 **목표 속도**이다. "시속 100km 이하로 유지하자"는 운영 팀의 내부 목표다.
- **SLA**는 승객(고객)과의 **운송 계약**이다. "약속 시간보다 늦으면 배상한다"는 약속이다.
- **에러 예산**은 교통 범칙금 **포인트**다. "한 달에 위반 10점까지는 용인한다"는 기준이 있어야, 운전자(개발자)가 안전하면서도 빠르게 목적지에 도달할 수 있다.

### 등장 배경
1.  **기존 한계**: 전통적인 운영(Admin)은 "장애 제로(Zero Downtime)"를 강조하여, 이로 인해 개발 속도가 현저히 저하되거나(Change Freeze), 야간 당직 인력의 번아웃이 심각해지는 문제가 있었다.
2.  **혁신적 패러다임**: 구글(Google)은 토렌스 크렌(Torrence Kreisen) 등을 중심으로 **'Toil(반복 업무)을 줄이고 자동화하여 얻은 시간만큼 개발에 투자하라'**는 원칙을 세웠다. 이를 위해 신뢰성을 숫자로 관리해야 했고, SLI/SLO/Error Budget 체계가 탄생했다.
3.  **현재의 비즈니스 요구**: 클라우드 네이티브(Cloud Native) 환경에서 MSA(Microservices Architecture)가 보편화되며, 서비스 간 의존성이 복잡해졌다. 이에 따라 무중단 배포와 신속한 기능 추가가 필수가 되었고, SRE는 현대적인 SaaS 기업의 표준 운영 모델로 자리 잡았다.

### 📢 섹션 요약 비유
> "복잡한 고속도로 톨게이트에서 **하이패스 차선(자동화된 우회로)**을 별도로 운영하여, 일반 차량(수동 운영)으로 인한 병목을 해결하고 교통 흐름을 최적화하는 것과 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 계층적 지표 구조 (SLI / SLO / SLA)
신뢰성 관리는 단계적 목표 설정을 통해 이루어진다. 각 용어의 정의와 상관관계를 이해하는 것이 핵심이다.

| 구분 | 약어 (Full Name) | 정의 및 내부 동작 | 비고 (Margin) | 비유 |
|:---:|:---|:---|:---:|:---|
| **지표** | **SLI (Service Level Indicator)** | 서비스의 수준을 측정하는 **정량적 수치**. (예: Latency, Traffic, Errors, Saturation) | 데이터 원천 | 속도계 |
| **목표** | **SLO (Service Level Objective)** | 조직이나 팀이 달성하기 위해 설정한 **SLI의 목표치**. (예: 99.9% Availability) | 내부 목표 | 내비게이션 설정 속도 |
| **계약** | **SLA (Service Level Agreement)** | 고객과의 법적 계약에 명시된 **서비스 수준 보장 약속**. SLO 미 달성 시 페널티(Penalty) 발생. | **SLO < SLA** (일반적으로 SLO가 더 엄격함) | 승객과의 약속 |

> **설명**: 만약 고객과 99.9%의 SLA를 맺었다면, 내부적으로는 99.95%의 SLO를 설정하여 예기치 못한 돌발 상황(Margin)에 대비해야 한다. 이를 **Performance Budget**이라고도 한다.

### 2. 에러 예산 (Error Budget)의 메커니즘
에러 예산은 $100\% - SLO$로 계산된다. 이것은 단순히 허용된 오차율이 아니라, **"새로운 기능을 출시할 수 있는 통화"**이다.

```text
    [ 에러 예산의 순환 구조 (Error Budget Lifecycle) ]
    
    1. 에러 예산 설정 (Target SLO: 99.9%)
       └──> 허용 가능한 장애 시간: 월 43.2분 (Budget)
    
    2. 실시간 모니터링 및 소모 (Monitoring)
       ┌─────────────────────────────────────┐
       │  (예산 소모 상황)                    │
       │  [●●●●●●●●●●●●●●○○○○○] 75% 소진  │
       └─────────────────────────────────────┘
       └──> Burn Rate: 예산 소모 속도 (현재 속도라면 며칠 뒤 예산 고갈?)
    
    3. 의사결사 게이트 (Decision Gate)
       ├──> 예산 잔여: [Push Mode] ✅
       │    └──> 신규 기능 배포, 위험한 실험, 리팩토링 등 가속화 (Aggressive)
       │
       └──> 예산 소진: [Brake Mode] 🛑
            └──> 기능 배포 중지(Freeze), 안정화 패치 적용, 아키텍처 개선 ONLY
```

### 3. 핵심 수식 및 코드 로직
SLO를 달성하기 위해 SLI를 어떻게 집계하는지는 매우 중요하다. 단순 평균(Average)은 이상치(Outlier)를 감추기 때문에, 주로 백분위수(Percentile)를 사용한다.

- **지연 시간(Latency) SLI 예시**:
    - `avg`: 전체 요청의 평균 (권장하지 않음)
    - `p50`: 중앙값
    - `p99`: 상위 1% 사용자의 경험 (UX에 치명적이므로 중요하게 관리)
    - `p99.9`: 테일 레이턴시(Tail Latency)

```python
# Pseudocode: Calculating Error Budget Status
# SLI: Successful Requests / Total Requests
# SLO: 0.999 (99.9%)

current_sli = calculate_success_rate(time_window="last_30d")
target_slo = 0.999

# 에러 예산 계산 (Error Budget = 1 - SLO achievement)
# 현재 SLO 달성률이 99.8%라면, 우리는 0.1% 목표 대비 0.2% 실패
# 따라서 예산을 초과한 상태임.
budget_remaining = target_slo - (1 - current_sli) # Simplified logic

if budget_remaining > 0:
    policy = "DEPLOY_FREELY"
else:
    policy = "STOP_DEPLOYMENT_FIX_RELIABILITY"
```

### 📢 섹션 요약 비유
> "마치 **적정 체중 관리 프로그램**과 같습니다. SLO는 목표 체중이고, 에러 예산은 '허용된 칼로리 섭취량'입니다. 목표 체중을 지키고 있는 한(SLO 달성), 맛있는 디저트(신규 기능)를 즐길 수 있지만, 한계를 넘어서면 즉시 다이어트(안정화 작업)로 돌아와야 합니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: Waterfall vs DevOps vs SRE

| 구분 | Waterfall (전통적) | DevOps | SRE (Site Reliability Engineering) |
|:---|:---|:---|:---|
| **핵심 목표** | 문서화된 계획 준수 | 개발(Dev)과 운영(Ops)의 **협업** | **자동화**와 **수치적 목표**를 통한 안정성 확보 |
| **장애 관점** | 장애는 실패 | 장애는 개선의 기회 | 장애는 **예산 소모**이자 관리 대상 |
| **속도 vs 안정성** | 속도 우선 (나중에 유지보수) | 양립을 추구하지만 갈등 빈발 | **에러 예산**으로 트레이드 오프(Trade-off) 관리 |
| **핵심 도구** | Gantt Chart, MS Project | CI/CD, Jenkins | SLI/SLO Dashboard, Error Budget Policy |

### 2. 과목 융합 관점: 네트워크/OS 및 AI와의 시너지
- **네트워크/하드웨어 (Infrastructure)**:
    - 물리 장비의 **MTBF (Mean Time Between Failures)**와 **MTTR (Mean Time To Repair)**은 하드웨어적 SLI의 기초가 된다.
    - L4/L7 스위치의 헬스 체크(Health Check)가 SLI 수집의 원천이다.
- **인공지능 (AIOps)**:
    - 에러 예산의 **Burn Rate (소모 속도)**가 비정상적으로 빠를 때, AI 모델이 이상 징후(Anomaly Detection)를 미리 감지하고 사전에 "Deploy Freeze"를 제안할 수 있다. 이는 단순 모니터링을 넘어 **예지 보안(Predictive Reliability)**으로 진화한다.

### 3. SLI 측정 대상 비교 (정량적 지표)

| SLI 카테고리 | 주요 지표 (Metrics) | 상세 설명 |
|:---|:---|:---|
| **가용성 (Availability)** | Success Rate, Uptime | "시스템이 살아있는가?" (전체 요청 대비 200 OK 응답 비율) |
| **지연 시간 (Latency)** | p50, p95, p99, p99.9 | "얼마나 빠른가?" (사용자가 느끼는 속도, Tail Latency 중요) |
| **처리량 (Throughput)** | RPS (Requests Per Sec) | "얼마나 많이 처리하는가?" (시스템의 용량) |
| **포화 상태 (Saturation)** | CPU, Memory, Disk I/O | "얼마나 바빠지는가?" (성능 저하가 발생하기 직전의 리소스 사용량) |

### 📢 섹션 요약 비유
> "자동차의 **계기판 센서와 네비게이션의 교통 정보**가 융합된 것과 같습니다. 단순히 엔진 열(시스템 부하)만 보는 것이 아니라, 앞으로의 도로 상황(트래픽)을 분석하여 여행 시간을 예측하고 최적의 경로(SLO)를 제안하는 통합 관제 시스템입니다."

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 피크 시즌 전략적 배포 관리
- **상황**: 이커머스 기업의 '블랙프라이데이' 이벤트 2주 전. 현재 에러 예산이 90% 소진되어 위험 상태임.
- **문제**: 마케팅 팀은 이벤트 당일에 적용할 '쿠폰 발급 기능'을 배포하려 함.
- **의사결정 매트릭스**:
    1.  **안정성(SLO) 리스크 분석**: 신규 기능 배포 시 잠재적 버그 발생 가능성이 높음. 이때 장애가 발생하면 예산이 음수로 떨어지며 SLA 위반 보상을 해야 함.
    2.  **비즈니스 임팩트 분석**: 신규 기능 미배포로 인한 매출 기회 손실 vs 장애 발생 시 브랜드 신뢰도 하락 및 보상 비용 지출.
- **결론**: **"정지(Freeze)" 결정**.
    - 이벤트 기간 중에는 모든 신규 배포를 금지.
    - 대신, 오토 스케일링(Auto-scaling) 설정을 튜닝하여 기존 기능의 SLO를 지키는 데 집중.

### 2. 도입 체크리스트
- **기술적 측면**
    - [ ] **측정 가능한가?**: 우리 서비스의 핵심 SLI가 무엇인가? (가용성? 지연 시간?)
    - [ ] **데이터 무결성**: 로그나 메트릭 수집 체계가 신뢰할 수 있는가? (Sampling 오차 등 확인)
    - [ ] **알림 테스트**: SLO 미달 시 온콜(On-call) 엔지니어에게 즉시 PagerDuty 등으로 알림이 가는가?

- **운영 및 보안적 측면**
    - [ ] **조직적 합의**: SLO 수치를 개발팀, 경영진, 고객 모두가 합의했는가?
    - [ ] **롤백 계�