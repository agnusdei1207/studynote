+++
title = "798. 형상 통제 베이스라인 변경 심의 이력 추적"
date = "2026-03-15"
weight = 798
[extra]
categories = ["Software Engineering"]
tags = ["SCM", "Configuration Management", "Baseline", "Change Control", "Audit", "CCB", "Traceability"]
+++

# 798. 형상 통제 베이스라인 변경 심의 이력 추적

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 개발 생명주기(SDLC) 전반에 걸쳐 형상 항목(Configuration Item, CI)의 변경을 체계적으로 승인하고 관리하여 시스템의 **무결성(Integrity)**과 **가시성(Visibility)**을 확보하는 핵심 통제 활동이다.
> 2. **가치**: **형상 통제 위원회(Configuration Control Board, CCB)**의 공식적인 심의와 **베이스라인(Baseline)**의 版管理(버전 관리)를 통해 "누가, 언제, 왜, 무엇을" 변경했는지에 대한 완벽한 **추적성(Traceability)**을 제공하여, 장애 발생 시 신속한 원복(Rollback)과 근본 원인 분석(RCA)을 가능하게 한다.
> 3. **융합**: 단순한 버전 관리 도구(Version Control System, VCS)의 사용을 넘어, 조직의 프로세스, 거버넌스, DevOps 자동화 파이프라인과 결합하여 프로젝트 리스크를 최소화하고 제품 품질을 보증하는 품질 경영(Quality Management)의 핵심 축이다.

---

### Ⅰ. 개요 (Context & Background)

소프트웨어 개발 프로젝트는 불확실성 속에서 진행되며, 요구사항의 변경은 필연적이다. 그러나 무절제한 변경은 개발 일정 지연, 비용 초과, 그리고 시스템 불안정의 주범이 된다. **형상 통제(Configuration Control)**는 이러한 혼돈을 방지하기 위해, 변경이 발생했을 때 이를 공식적으로 접수, 분석, 승인, 반영하고 그 과정을 기록하는 일련의 관리 활동을 의미한다. 이는 단순히 파일의 버전을 나누는 것을 넘어, 시스템의 구성 요소가 서로 모순 없이 일치하도록 보장하는 **형상 통합(Configuration Auditing)**의 근간이 된다.

이 활동의 핵심은 **베이스라인(Baseline)**이다. 베이스라인은 형상 항목이 특정 시점에 합의된 상태로 고정된 것을 말하며, 이후의 변경은 반드시 형식적인 절차(Change Control Procedure)를 거쳐야만 베이스라인을 갱신할 수 있다. 이를 통해 프로젝트는 '진정한 수정(Modification)'과 '무질서한 변형(Tampering)'을 명확히 구분한다.

**💡 개념 비유: 건축 설계도면의 '청사진 보관' 및 '개정 승인' 시스템**
마치 건물을 짓는 과정에서 기공 설계도가 확정된 후, 설계 변경을 위해 건축사, 시공사, 주택주가 모여 회의를 거쳐 도장을 찍고 '개정판(Rev. A)'으로 재발행하는 과정과 같다. 승인 없이 현장에서 임의로 벽을 허물거나 문을 옮기면 불법 시공이 되듯이, 소프트웨어에서도 승인되지 않은 변경은 **치명적인 결함(Fatal Flaw)**을 유발할 수 있다.

> 📢 **섹션 요약 비유**
> 형상 통제와 베이스라인은 마치 **'은행 금고의 보안 절차'**와 같습니다. 정기적으로 입금된 장부(베이스라인)는 금고에 봉인되며, 이후 내역을 바꾸려면 반드시 관리자 몇 명의 다중 서명(CCB 승인)과 실명 기록(이력 추적)이 있어야만 금고를 열고 수정할 수 있습니다. 이를 통해 장부의 위변조를 막고 자산(시스템)의 안전을 지킵니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

형상 통제 프로세스는 단순한 승인 단계가 아니라, 변경 요청이 발생한 순간부터 해당 변경이 운영 환경에 반영되어 새로운 베이스라인이 형성될 때까지의 **생명주기(Lifecycle)**를 관리하는 아키텍처이다. 이 절차는 수동적인 문서화가 아닌, 능동적인 품질 방어 기제로 작동한다.

#### 1. 형상 통지 및 변경 통제 절차 (Workflow Components)

형상 통제 시스템(CCS)은 크게 변경 요청, 분석, 승인, 실행, 검증의 5단계로 구성된다. 각 단계는 독립적인 책임자(Role)를 가지며, 이들이 상호 작용하며 리스크를 차단한다.

| 모듈 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 주요 프로토콜/산출물 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **CR Generator** | 변경 요청자 | 문제점이나 개선 필요성을 인지하고 양식에 맞춰 요청서 생성 | **CR (Change Request)**, 이슈 티켓 | 민원인 |
| **Impact Analyzer** | 형상 분석가 | CR이 코드, DB, 성능, 일정에 미칠 영향을 기술적/비즈니스적으로 분석 | **IA (Impact Analysis)** 보고서, 위험도(Risk Score) | 시뮬레이터 |
| **CCB (Committee)** | 심의 위원 | 영향 분석 결과를 바탕으로 승인/거부/연기 여부 결정 (의사결정) | **CMO (Change Order)**, 승인 서명 | 재판관 |
| **Executor** | 개발자 | 승인된 변경 사항을 실제 코드/문서에 적용 (구현) | 소스코드 패치, Diff 파일 | 집행자 |
| **Auditor** | 품질 보증팀 | 변경 결과가 요구사항과 일치하는지 검증하고 베이스라인 갱신 | **CA (Configuration Audit)** 리포트 | 감사원 |

#### 2. 통제 절차 및 데이터 흐름 (ASCII Architecture)

아래 다이어그램은 변경 요청이 발생하여 새로운 베이스라인으로 확정되기까지의 데이터 흐름과 의사결정 포인트(Gate)를 도식화한 것이다. 특히 CCB의 **승인 게이트(Approval Gate)**가 통제의 핵심 축(Axis)임을 알 수 있다.

```text
      [ 개발자/사용자 ]            [ 형상 관리자/분석가 ]              [ 형상 통제 위원회(CCB) ]
           │                          │                              │
           │  ① 문제/개선 발생        │                              │
           ├──────────────▶ ② CR 등록 (Change Request)               │
           │                          │                              │
           │                          ├──────────────▶ ③ 영향도 분석 (Impact Analysis)
           │                          │  (범위, 비용, 리스크 산출)        │
           │                          │                              │
           │                          │◀─────────────┤ ④ 심의 및 의결 (Approve/Reject)
           │                          │                              │
           │                          │  ⑤ CMO 발급 (Change Order)       │
           │  ◀───────────────       │                              │
           │   (반려 시 수정)         │                              │
           │                          │                              │
           │  ⑥ 변경 실행 (Coding)    │                              │
           │                          │                              │
           │  ⑦ 테스트 및 검증        │                              │
           ├──────────────▶ ⑧ 형상 감사 (Configuration Audit)      │
           │   (기능/물리 검증)         │                              │
           │                          │                              │
           │                   [ New Baseline ] ◀───────────────────┤ ⑨ 공식 승인 및 버전 태그
           │                   (v1.0.1 Released)                     │    (이력 저장소에 기록)
```

**[다이어그램 해설]**
1. **요청 및 등록 (Request & Registration)**: 모든 변경은 **CR (Change Request)** 형태로 기록된다. 여기에는 변경 이유와 예상 효과가 포함되어야 한다.
2. **영향 분석 (Impact Analysis)**: CCB가 판단을 내리기 전, 분석가는 해당 변경이 다른 모듈(MMI)이나 성능(SLA)에 미칠 파급 효과를 분석한다. 이 단계에서 수정이 불가능하거나 리스크가 크다면 CR은 기각된다.
3. **CCB 심의 (CCB Review)**: **CCB (Configuration Control Board)**는 프로젝트 관리자, 기술 리드, 고객 대표 등으로 구성된다. 이들은 **CMO (Change Management Order)**를 통해 변경에 대한 최종 권한을 행사한다.
4. **실행 및 감사 (Execution & Audit)**: 승인된 변경만 실행되며, 실행 후에는 **FCA (Functional Configuration Audit)**와 **PCA (Physical Configuration Audit)**를 거쳐 의도한 대로 변경되었는지 확인한다.
5. **베이스라인 갱신 (Baseline Update)**: 감사까지 통과한 변경 사항은 형상 관리 시스템(SCM)에 Commit되어 새로운 **베이스라인**을 형성한다. 이 순간부터 시스템은 새로운 기준선을 가지게 된다.

#### 3. 핵심 알고리즘: 버전 네이밍 및 추적 코드
실무에서는 베이스라인의 변화를 추적하기 위해 **SEMVER (Semantic Versioning)**나 4단위 번호(Major.Minor.Patch.Build)를 사용한다.

```python
# Pseudo-code: Change Control Logic
class ConfigurationItem:
    def __init__(self, id, version, status):
        self.id = id
        self.version = version  # Current Baseline
        self.status = status    # 'BASELINED', 'UNDER_MODIFICATION'

def request_change(item, cr_details):
    if item.status != 'BASELINED':
        return "Error: Item is already being modified"
    
    # 1. Create Change Request
    cr_id = create_cr(cr_details)
    
    # 2. Impact Analysis (Simulation)
    impact_score = analyze_impact(cr_id)
    
    # 3. CCB Approval Simulation
    if ccb_review(impact_score) == 'APPROVED':
        # 4. Execute Change
        apply_change(item)
        item.version += 1  # Increment Version
        # 5. New Baseline
        save_audit_log(f"Baseline updated to v{item.version} by CCB")
        return "Change Accepted"
    else:
        return "Change Rejected"
```

> 📢 **섹션 요약 비유**
> 이 과정은 **'고속도로 톨게이트의 하이패스 차선 관리'**와 유사합니다. 모든 차량(변경 요청)이 무작정 들어올 수 없습니다. 하이패스 차단봉(CCB)이 내려가 있고, 요금 결제(영향 분석 및 승인)가 완료된 차량만 차단봉이 올라가며 진입(변경 실행)할 수 있습니다. 진입 기록은 모두 카메라(감사 로그)에 찍혀 나중에 어디서 왔는지 확인할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

형상 통제는 단순한 문서 관리가 아니며, 소프트웨어 공학의 전 분야와 연결된다. 특히 DevOps 환경에서는 이 개념이 **GitOps**나 **Infrastructure as Code (IaC)**와 깊게 융합된다.

#### 1. 기술 비교: 단순 버전 관리(VCS) vs 형상 통제(SCM)

많은 사람들이 Git을 사용하는 것을 형상 관리라고 착각하지만, Git은 도구(Tool)일 뿐이며 형상 통제는 프로세스(Process)이다.

| 비교 항목 | VCS (Version Control System) | SCM (Configuration Management) |
|:---|:---|:---|
| **대상** | 소스코드(Source Code) 중심 | 코드, 문서, 하드웨어, 데이터, 설정 파일 등 **CI 전체** |
| **목표** | 변경 이력(Diff) 저장 및 병행 개발 지원 | 시스템 **무결성(Integrity)** 보장 및 변경 통제 |
| **통제 수준** | 개발자 자율(Commit 가능) | 조직적 통제(CCB 승인 필요) |
| **키워드** | Git, SVN, Branch, Merge | Baseline, CCB, Audit, Traceability |
| **결과물** | 저장소(Repository) | 공식 릴리즈(Release) 및 품질 보고서 |

#### 2. DevOps 및 CI/CD 파이프라인과의 융합

현대의 애자일 환경에서는 전통적인 수동 CCB 회의가 병목이 된다. 따라서 **자동화된 형상 통제**가 필요하다.
- **Pull Request (PR) = CR**: 코드 변경 요청 시 PR을 생성하면 시스템이 자동으로 영향 분석(Static Analysis, Test Coverage)을 수행한다.
- **Code Review = CCB**: 승인 권한이 있는 리뷰어(Approver)들의 리뷰와 승인(LGTM)이 곧 CCB의 승인 역할을 대체한다.
- **Main Branch = Baseline**: `main` 브랜치는 보호되며(Protected Branch), 모든 검증(CI/CD Pipeline)이 통과된 코드만 Merge 되어 새로운 베이스라인이 된다.

```text
[ Traditional Model ]          [ Modern GitOps Model ]
Developer ──▶ CR Paper         Developer ──▶ Pull Request (PR)
              │                              │
              ▼                              ▼
          Manual Review                  Auto Test (CI)
              │                              │
              ▼                              ▼
            CCB Meeting ──▶ Decision      Code Review (CCB)
              │                              │
              ▼                              ▼
          Manual Update                  Auto Merge to Main (Baseline)
              │                              │
              ▼                              ▼
          Release                    Auto Deploy (CD)
```

#### 3. 보안과의 연계 (Audit Trail)

형상 통제의 이력 추적 기능은 보안 감사(Security Audit)의 핵심이다.
- **Non-repudiation (부인 방지)**: 누가 변경했는지 로그가 남으므로, 보안 사고 발생 시 담당자를 명확히 할 수 있다.
- **Compliance (준법)**: 금융이나 의료 분야에서 규정에 따라 변경 이력을 몇 년간 보관해야 하는 의무를 충족시킨다.

> 📢 **섹션 요약 비유**
> 단순 VCS는 **'개인 다이어리'**와 같아서 기록이 남지만 타인의 간섭이 없다면 잘못된 내용도 적힐 수 있습니다. 반면, 형상 통제(SCM)는 **'공공 기관의 공문 시스템'**과 같습니다. 수신, 결재, 시행, 보관의 절차를 모두 거치며, 결재 도장(CCB)이 찍힌 문서만이 공식적인 효력(Baseline)을 가집니다. GitOps는 이 결재 과정을 전자 서명 시스템으로 자동화한 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

기술