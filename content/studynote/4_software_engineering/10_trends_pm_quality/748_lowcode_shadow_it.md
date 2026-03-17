+++
title = "748. 로우코드/노코드 섀도우 IT 거버넌스"
date = "2026-03-15"
weight = 748
[extra]
categories = ["Software Engineering"]
tags = ["Development", "Low-code", "No-code", "Shadow IT", "Governance", "Citizen Developer", "Compliance"]
+++

# 748. 로우코드/노코드 섀도우 IT 거버넌스

## # [로우코드/노코드 섀도우 IT 거버넌스]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기업의 **시민 개발자 (Citizen Developer)**들이 로우코드/노코드(LCNC) 플랫폼을 활용해 **섀도우 IT (Shadow IT)**를 양산하는 현황에서, **IT 거버넌스 (IT Governance)** 체계를 통해 '민주화된 개발의 속도'와 '중앙 통제의 안정성'을 동시에 확보하는 통제 메커니즘이다.
> 2. **가치**: 전사적인 **앱 개발 생산성 (Productivity)**을 비약적으로 높이면서도, **데이터 유출 (Data Leakage)**, **컴플라이언스 (Compliance)** 위반, 잠재적 보안 허점을 체계적으로 관리하여 기술 부채를 최소화한다.
> 3. **융합**: **아이덴티티 및 액세스 관리 (IAM)**, **DLP (Data Loss Prevention, 데이터 손실 방지)**, 그리고 **API (Application Programming Interface)** 거버넌스와 결합하여 안전한 디지털 혁신 생태계를 구축한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**로우코드/노코드 (Low-Code/No-Code, LCNC)**란 코딩 없이 혹은 최소한의 코드로 애플리케이션을 개발하는 플랫폼을 의미하며, 이를 활용하는 비전문가 개발자를 **시민 개발자 (Citizen Developer)**라 칭한다. 이러한 기술의 확산은 개발의 민주화를 이끌었으나, 동시에 IT 부서의 모니터링 밖에서 진행되는 **섀도우 IT (Shadow IT)**라는 심각한 리스크를 야기했다. **LCNC 섀도우 IT 거버넌스**는 이러한 비공식 앱들을 발굴하고, 보안 정책을 적용하며, 제도권 내로 편입시켜 관리하는 체계적인 접근 방식이다.

#### 2. 등장 배경: 급증하는 민주화와 통제의 딜레마
과거 IT 요청은 중앙 조직을 거쳐야 했으나, 클라우드 시대가 도래하며 현업 부서는 신용카드 하나면 즉시 SaaS(Software as a Service)나 LCNC 툴을 구매할 수 있게 되었다. 이는 **타임 투 마켓 (Time-to-Market)** 단축에 기여했으나, 관리되지 않은 데이터 복제, 잠재적 보안 후문, 그리고 **좀비 앱 (Zombie App, 유지보수 단절된 앱)** 문제를 만들었다. 결국 기업은 민첩성을 포기하지 않으면서도 통제를 되찾기 위해 **CoE (Center of Excellence, 전문성 센터)** 중심의 거버넌스 구축에 나서게 되었다.

#### 3. 핵심 이슈: 왜 거버넌스인가?
섀도우 IT는 단순히 '몰래 쓰는 도구'가 아니다. 현업의 요구를 반영하지 못하는 중앙 IT의 병목 현상이 만들어낸 구조적 결과물이다. 따라서 거버넌스의 목표는 '금지'가 아닌 **'가이드레일 (Guardrails)'** 설치에 있다. 즉, 위험한 요소는 차단하되, 안전한 범위 내에서 현업이 자율적으로 혁신할 수 있도록 **플랫폼화 (Platform Engineering)**하는 것이 핵심이다.

#### ASCII: 섀도우 IT 발생 프로세스 및 거버넌스 필요성
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       섀도우 IT 생성 및 리스크 확산 경로                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ 1. Business Need ]                                                       │
│   "앱이 필요한데 IT 티켓을 넣으면 3개월 뒤에나 처리됨."                         │
│          │                                                                  │
│          ▼                                                                  │
│  [ 2. Shadow IT Action ]                                                    │
│   개인 카드로 LCNC 툴 구매 -> 개인 클라우드 스토리지(DB) 연동 -> 급조 개발      │
│          │                                                                  │
│          ├─▶ [ Risk A: Data Silo ] (중요 데이터가 개인 계정에 뜀)              │
│          ├─▶ [ Risk B: Compliance ] (규정 미준수 PII 포함)                    │
│          └─▶ [ Risk C: Orphaned App ] (직원 퇴사 시 작동 멈춤)                 │
│                                                                             │
│          │                                                                  │
│          ▼                                                                  │
│  [ 3. Governance Required ]                                                 │
│   LCNC 플랫폼 표준화 및 자동화된 보안 가드레일(Guardrail) 적용 필요              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
**해설**: 위 다이어그램은 현업의 답답함이 어떻게 섀도우 IT로 이어지는지를 보여준다. IT 부서의 반응 속도가 비즈니스 속도를 따라가지 못할 때, 현업은 허가되지 않은 수단을 사용하게 된다. 이때 발생하는 데이터 사일로(Data Silo), 보안 규정 위반, 방치된 앱(Orphaned App) 문제는 기업 전체의 리스크로 확산된다. 이를 해결하기 위해 임기응변식이 아닌 체계적인 거버넌스 체계가 요구된다.

#### 📢 섹션 요약 비유
**"마치 도심에서 각자 편리하게 이동하고자 개인 오토바이(섀도우 IT)를 몰고 다니는 상황과 같습니다. 빠르� 하지만 사고 위험이 크기에, 관공서(IT 조직)는 전용 자전거 도로(LCNC 플랫폼)와 안전 교육(가이드라인)을 통해 안전하게 빠르게 이동하게 하는 것과 같습니다."**

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. LCNC 거버넌스 아키텍처 구성 요소
LCNC 거버넌스를 구현하기 위해서는 단순히 규정을 만드는 것을 넘어, 플랫폼 차원에서의 기술적 통제가 필요하다. 주요 구성 요소는 다음과 같다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 연동 프로토콜/기술 |
|:---|:---|:---|:---|
| **CoE (Center of Excellence)** | 거버넌스 운영 주체 | 표준 플랫폼 선정, 시민 개발자 교육, 앱 심의 및 승인 | N/A (조칙) |
| **IDP (Identity Provider)** | 통합 인증 및 권한 관리 | SSO(Single Sign-On)를 통해 LCNC 접속 제어, 속성 기반 접근 제어(ABAC) | SAML 2.0, OIDC |
| **DLP (Data Loss Prevention)** | 데이터 반출 방지 | 커넥터 수준에서 데이터 이동 제어(예: PII 데이터 비즈니스 메신저 전송 차단) | API Hook, Agent |
| **Environment Strategy** | 환경 분리 운영 | Dev(개발), Test(시험), Prod(생산) 환경을 분리하여 배포 파이프라인 구성 | CI/CD Pipeline |
| **Automated Governance** | 정책 자동 적용 | 코드 없이 보안 스캔, 규정 준수 검사를 자동화하여 배포 전 차단 | Static Analysis, Bot |

#### 2. 심층 동작 원리: 가드레일(Guardrail) 설계
LCNC 거버넌스의 핵심은 **'사전 예방적 통제'**다. 전통적인 개발에서의 코드 리뷰를, LCNC에서는 플랫폼 설정과 정책(Policy)으로 대체한다.

**[동작 단계]**
1. **요청 (Request)**: 시민 개발자가 LCNC 플랫폼에 접속하여 앱 개발을 요청한다.
2. **검증 (Verification)**: 시스템은 개발자의 권한(Role)과 사용하려는 커넥터(Connector)의 안전성을 실시간으로 검증한다.
3. **개발 (Development)**: 승인된 **샌드박스 (Sandbox)** 환경에서 개발이 진행되며, PII(개인정보) 등 민감한 데이터 라벨링이 자동으로 적용된다.
4. **배포 (Deployment)**: 앱 배포 시 자동화된 **Governance Bot**이 보안 취약점을 스캔하고, 문제가 없을 경우에만 프로덕션(Production) 환경으로 승격한다.
5. **모니터링 (Monitoring)**: 운영 중인 앱의 접속 로그와 데이터 사용량을 중앙 **SIEM (Security Information and Event Management)** 시스템으로 전송한다.

#### ASCII: LCNC 거버넌스 제어 레이어 구조도
```text
+-----------------------------------------------------------------------+
|                   Business Users (Citizen Developers)                 |
+-----------------------------------------------------------------------+
                                    │
                                    ▼
+-----------------------------------------------------------------------+
|              ① LCNC Platform Layer (e.g., MS Power Platform)          |
|  ┌─────────────────────────────────────────────────────────────────┐  |
|  │  ② Governance Controls (Guardrails)                             │  |
|  │  ┌──────────────┐  ┌──────────────────────┐  ┌──────────────┐   │  |
│  │  │   DLP        │  │  Environment Mgmt     │  │   Auto Review│   │  |
│  │  │ (Prevent Data│  │ (Separate Dev/Test)  │  │ (Security    │   │  |
│  │  │  Leakage)    │  │                      │  │  Check)      │   │  |
│  │  └──────┬───────┘  └──────────┬───────────┘  └──────┬───────┘   │  |
│  └─────────┼─────────────────────┼─────────────────────┼───────────┘  |
+------------┼─────────────────────┼─────────────────────┼---------------+
             │                     │                     │
             ▼                     ▼                     ▼
+-----------------------------------------------------------------------+
|                 ③ Enterprise IT & Security Backend                    |
|  ┌──────────────────┐     ┌──────────────────────┐                    |
|  │  IDP / IAM       │     │  Managed Connectors  │                    |
|  │ (Azure AD / SSO) │     │ (SQL, ERP, APIs)    │                    |
|  └──────────────────┘     └──────────────────────┘                    |
+-----------------------------------------------------------------------+
```
**해설**: 이 구조도는 시민 개발자가 LCNC 플랫폼을 통해 자원에 접근할 때, 거버넌스 계층이 어떻게 개입하는지 보여준다. ② Governance Controls 계층이 핵심이다. 사용자는 자유롭게 개발하지만, DLP 정책에 의해 데이터가 유출되지 않으며, 환경 관리 정책에 의해 테스트 거치지 않은 앱은 바로 운영될 수 없다. 하단의 Enterprise IT는 이러한 보안 정책이 실제로 적용되도록 IDP와 관리형 커넥터를 통해 기술적 루트를 제공한다.

#### 3. 핵심 알고리즘: 라이프사이클 관리 프로세스
LCNC 앱의 생명 주기 관리는 전통적인 SDLC(Software Development Life Cycle)와 유사하나, 자동화의 비중이 훨씬 높다.

```python
# LCNC Governance Lifecycle Logic (Pseudo-code)

def manage_lifecycle(app_request):
    # 1. Provisioning
    citizen_dev = get_user(app_request.user_id)
    if not citizen_dev.certified:
        return "Error: Mandatory Governance Training Required"

    # 2. Development Environment Setup
    env = create_sandbox(tenant=citizen_dev.dept)
    assign_policy(env, data_classification="INTERNAL_ONLY")

    # 3. Pre-deployment Check (Automated Governance)
    if app_request.contains_pii() and not app_request.has_encryption():
        block_deployment("Violation: PII data requires encryption.")

    # 4. Deployment
    if auto_security_scan(app_request.source_code).passed:
        deploy_to_production(app_request)
        register_to_catalog(app_request) # Inventory update
    else:
        send_feedback_to_developer("Security vulnerabilities found.")

    # 5. Monitoring & Decommission
    if get_last_accessed_date(app_request) > 180_days:
        notify_owner("App will be archived due to inactivity.")
        archive_app(app_request)
```

#### 📢 섹션 요약 비유
**"고속도로 건설 톨게이트 시스템과 같습니다. 차량(앱)이 자유롭게 달릴 수 있도록 도로(플랫폼)를 깔아주되, 통행료(보안 검사)를 자동으로 정수하고, 과속하는 차량(위반 앱)은 자동으로 단속 카메라(가드레일)가 걸러내는 시스템입니다."**

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 전통적 개발 vs LCNC 거버넌스
섀도우 IT 거버넌스를 도입했을 때, 기존의 Waterfall이나 Agile 방식과 어떻게 다른지 비교 분석한다.

| 구분 | 전통적 전담 개발 (Traditional IT) | 섀도우 IT (관리 전) | LCNC 거버넌스 (관리 후) |
|:---|:---|:---|:---|
| **개발 주체** | 프로 개발러 (Professional Dev) | 현업 비전문가 (Amateur) | **시민 개발자 (Citizen Dev)** |
| **속도 (TTM)** | 느림 (개월 단위) | 매우 빠름 (일 단위) | **빠름 (주 단위)** |
| **품질 관리** | 높음 (Formal QA/Testing) | 낮음 (테스트 없음) | **중간 (자동화된 스캔)** |
| **보안 가시성** | 100% 투명함 | 0% (블랙박스) | **100% (로그 및 감사)** |
| **유지보수** | 문서화됨, 인수인계 용이 | 개발자 의존적 (좀비 앱) | **표준화, 플랫폼 도구 의존** |
| **비용 구조** | 높은 인건비 | 숨겨진 비용(Risk Cost) | **플랫폼 라이선스 비용** |

#### 2. 타 영역 융합 분석
1.  **데이터 통합 (Data Integration) 관점**:
    섀도우 IT의 가장 큰 문제는 데이터가 **데이터 호수 (Data Swamp)**화되는 것이다. LCNC 거버넌스는 **CDE (Common Data Exchange)** 패턴을 사용한다. 중앙 IT는 API 형태로 정제된 데이터를 제공하고