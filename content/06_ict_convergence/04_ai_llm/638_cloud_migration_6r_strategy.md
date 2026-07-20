---
title: "Cloud Migration 6R Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 638
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 마이그레이션 6R 전략(Rehost, Replatform, Repurchase, Refactor, Retain, Retire)은 AWS가 체계화하고 Gartner/McKinsey 등이 변형 채택한 워크로드 분류 의사결정 프레임워크로, 기존 온프레미스 자산을 클라우드로 이전할 때 **"어떻게(How)"** 이전할지를 6가지 표준화된 패턴으로 분류하여 일관된 의사결정 기준을 제공한다.
> 2. **가치**: AWS 마이그레이션 사례 분석에 따르면 6R 적용 시 평균 인프라 비용 **30~40% 절감**, 배포 주기 **60% 단축**, 그리고 마이그레이션 ROI 회수 기간이 무계획적 접근 대비 **18개월 -> 8~10개월** 수준으로 단축되며, 포트폴리오의 약 **60~70%는 Rehost, 20~30%는 Replatform, 5~10%는 Refactor/Repurchase**로 분산되어 TCO 최적화의 핵심 도구로 활용된다.
> 3. **판단 포인트**: 6R 선택은 단순 기술 결정이 아니라 **기술 부채 수준(Technical Debt), 비즈니스 민첩성 요구도(Cloud Native Maturity), 규제 준수 조건(데이터 레지던시/컴플라이언스), TCO 회수 기간**을 종합적으로 평가해야 하며, 특히 "리프트앤시프트"의 편의성 때문에 무분별하게 Rehost를 선택할 경우 **클라우드 락인(Lock-in)과 클라우드 낭비(Cloud Waste)**라는 양대 역효과를 유발하므로, 워크로드별 6R 의사결정 매트릭스를 반드시 사전에 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation)이 가속화되면서 전 세계 기업의 IT 인프라 재편이 본격화되고 있다. 한국 시장에서도 2023년 기준 공공부문 클라우드 전환 종합계획(2023~2027)에 따라 행정·공공기관의 클라우드 전환이 의무화되었고, 금융·제조·통신 등 민간 부문도 자체적인 마이그레이션 로드맵을 수립·실행 중이다. 그러나 마이그레이션 대상이 되는 워크로드는 수십~수천 개에 이르며, 그 성격·중요도·기술 부채 수준이 모두 상이하다. 동일하게 "클라우드화"한다 하더라도 ERP처럼 20년 노후화된 모놀리식(Java EJB, COBOL, AS/400)부터, 컨테이너 친화적인 Spring Boot 기반 API 서버까지 한 번에 같은 방식으로 이관할 수는 없다.

이 문제를 해결하기 위해 **AWS는 2016년경 "6R Strategy of Application Migration"** 을 발표했고, 이후 Gartner(Magic Quadrant for Cloud), McKinsey(Cloud Migration Survey), Microsoft(Azure Migration Framework), Google Cloud(Migration Center) 등 주요 분석기관과 CSP가 채택·확장하여 사실상 업계 표준 의사결정 프레임워크로 자리 잡았다. 6R은 단순한 마이그레이션 옵션이 아니라 **포트폴리오의 합리적 분류(Rationalization) 도구**이며, 이 분류의 품질이 곧 클라우드 마이그레이션의 TCO와 성패를 가른다.

```text
[클라우드 마이그레이션 6R 의사결정 흐름도]

            +--------------------------------------------+
            |  기업 IT 자산 포트폴리오(예: 1,200개 앱)     |
            |  - 비즈니스 크리티컬리티 평가 (Tier 0~3)    |
            |  - 기술 부채(Technical Debt) 스코어링       |
            |  - 클라우드 적합성(Cloud-Readiness) 측정     |
            +----------------------+---------------------+
                                   |
                                   v
        +--------------------------------------------------+
        |  Step 1. "Retire 후보" 필터링                      |
        |  (사용률 < 5%, 중복 기능, EOL 시스템 제거)         |
        |  -> 약 10~15% 제거                                 |
        +----------------------+---------------------------+
                               |
                               v
        +--------------------------------------------------+
        |  Step 2. "Retain 후보" 분리                       |
        |  (규제·저지연·데이터 레지던시 제약)                |
        |  -> 약 5~10% 유지                                  |
        +----------------------+---------------------------+
                               |
                               v
        +--------------------------------------------------+
        |  Step 3. "Repurchase 후보" 검토 (SaaS 전환)        |
        |  (CRM, ERP, ITSM, HR 등 패키지형)                |
        |  -> 약 5~10% SaaS 전환                             |
        +----------------------+---------------------------+
                               |
                               v
        +--------------------------------------------------+
        |  Step 4. "Replatform vs Refactor" 의사결정        |
        |  +--------------+         +------------------+  |
        |  | Replatform   |         | Refactor / Re-   |  |
        |  | (Lift-Tinker |         | Architect(Cloud- |  |
        |  |  -Shift)     |         |  Native)         |  |
        |  | 약 20~30%    |         | 약 5~15%         |  |
        |  +--------------+         +------------------+  |
        +----------------------+---------------------------+
                               |
                               v
        +--------------------------------------------------+
        |  Step 5. 잔여 워크로드 -> "Rehost" (Lift&Shift)    |
        |  (IaaS 이관: EC2, RDS, S3 등)                    |
        |  -> 약 30~40%                                     |
        +----------------------+---------------------------+
                               |
                               v
        +--------------------------------------------------+
        |  6R 분포 결과 합산(예시):                          |
        |  Rehost 40% | Replatform 25% | Refactor 10%      |
        |  Repurchase 10% | Retire 10% | Retain 5%         |
        +--------------------------------------------------+
```

**기존(On-Premise) 패러다임 vs. 클라우드 패러다임 비교**

- **기존 (Monolithic + CapEx)**: 3-tier 아키텍처(Web/App/DB)를 물리/가상 서버(Nutanix, VMware vSphere, Oracle Exadata)에 구축하고, 5년 주기 HW 리프레시, 최대 트래픽 기준 과잉 프로비저닝, 라이선스 선구매. 변경하려면 수개월 소요.
- **클라우드 (Microservices + OpEx)**: 12-Factor App, EKS/AKS/GKE 같은 Managed Kubernetes, Lambda/Functions 기반 Serverless, Aurora/CosmosDB 같은 Cloud-Native DB, IaC(Terraform/CloudFormation)로 선언적 프로비저닝. Auto Scaling, Pay-per-use, 분 단위 배포.

이 패러다임 전환을 워크로드 단위로 어떻게 적용할 것인지를 결정하는 것이 6R의 본질이며, 잘못된 6R 선택은 "단순히 서버만 옮기는 비효율"을 넘어 **클라우드의 핵심 가치(탄력성, 민첩성, 비용 최적화)를 포기하는 결과**를 낳는다.

- **📢 섹션 요약 비유**: 6R은 마치 **이사짐 정리 전략**과 같다. 버릴 것(Retire), 그대로 둘 것(Retain), 새 가구로 바꾸는 것(Repurchase), 박스만 바꿔 옮기는 것(Rehost), 약간 조립해서 옮기는 것(Replatform), 완전히 리모델링하는 것(Refactor) — 집(클라우드)에 맞는 가구를 가져오는 똑똑한 분류 작업이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

6R 각 전략은 단순한 "옵션"이 아니라 **고유한 기술 아키텍처, 비용 구조, 리스크 프로파일, ROI 기간**을 가진다. 마이그레이션 설계자는 워크로드의 속성(앱, DB, 미들웨어, 데이터)을 정밀 분석하여 어떤 R로 분류할지 결정한다.

```text
[6R 전략별 아키텍처 변화 패턴 (On-Prem -> Cloud)]

+----------------+                  +----------------+
| On-Premise     |                  | Cloud Target   |
|  (Legacy)      |                  |                |
+-------+--------+                  +--------+-------+
        |                                    |
        |  ① Rehost (Lift & Shift)           |
        |  VMware/Hyper-V VM 그대로          |
        |  +--------------+                  |
        |  |  Physical    |   -------►       |
        |  |  /VM (Linux, |   AWS EC2/       |
        |  |   Win)       |   Azure VM       |
        |  +--------------+                  |
        |   OS/MW 변경 없음, AMI로 변환      |
        |                                    |
        |  ② Replatform (Lift, Tinker, Shift)|
        |  +--------------+                  |
        |  | Self-hosted  |   -------►       |
        |  | MySQL on EC2 |   Amazon RDS /   |
        |  |              |   Aurora         |
        |  +--------------+   (Multi-AZ,     |
        |                      Automated     |
        |                      Backup)       |
        |                                    |
        |  ③ Repurchase (Drop & Shop)        |
        |  +--------------+                  |
        |  | Custom-built |   -------►       |
        |  | CRM on JBoss |   Salesforce /   |
        |  |              |   Dynamics 365   |
        |  +--------------+                  |
        |                                    |
        |  ④ Refactor / Re-architect         |
        |  +--------------+                  |
        |  | Monolithic   |   -------►       |
        |  | Java EAR     |   Microservices  |
        |  | Oracle DB    |   on EKS +       |
        |  |              |   DynamoDB/      |
        |  |              |   Aurora Server- |
        |  |              |   less           |
        |  +--------------+                  |
        |                                    |
        |  ⑤ Retain                          |
        |  +--------------+                  |
        |  | Mainframe    |   ✕ 변경 없음     |
        |  | z/OS + CICS  |   (Hybrid 구간    |
        |  |              |    에 잔존)       |
        |  +--------------+                  |
        |                                    |
        |  ⑥ Retire                          |
        |  +--------------+                  |
        |  | 10년 미사용  |   ✕ 폐기          |
        |  | 레거시 배치  |   (Archive 후     |
        |  |              |    삭제)          |
        |  +--------------+                  |
        +------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Rehost (Lift & Shift)** | 코드·런타임·미들웨어 변경 없이 인프라 단위 그대로 클라우드로 이전 | VMware vSphere 기반 VM을 **AWS Application Migration Service (MGN)**, **Azure Migrate**, **Google Migrate to Virtual Machines**로 복제. 온프레미스 디스크는 **Block-level Continuous Replication**으로 동기화 후 컷오버. AWS AMI/Google Image로 변환하여 EC2/Compute Engine에 부팅. 컨테이너화·MSA 전환 없음. **AWS Server Migration Service(SMS)**는 더 이상 신규 지원되지 않고 MGN으로 통합됨. |
| **Replatform (Lift, Tinker & Shift)** | 소규모 최적화(설정 변경, 관리형 서비스 교체)만 수행하고 코드 수정은 최소화 | Self-hosted MySQL/PostgreSQL을 **Amazon RDS / Aurora**로 마이그레이션(PaaS화), **Azure Database for PostgreSQL Flexible Server**, **Cloud SQL**로 전환. WebLogic/JBoss를 **Tomcat/Amazon EKS**로 가볍게 컨테이너화. OS 라이선스 비용 절감을 위해 **Windows -> Linux**로 변환(SQL Server Standard -> Amazon Linux + RDS 조합). 메시지 브로커를 자체 RabbitMQ에서 **Amazon MQ / Amazon SQS/SNS**로 교체. 코드는 거의 그대로 유지하되 운영 부담만 줄이는 전략. |
| **Repurchase (Drop & Shop)** | 자체 구축(On-Prem CRM/ERP/ITSM)을 SaaS 솔루션으로 전면 교체 | 자체 CRM -> **Salesforce**, 자체 ERP -> **SAP S/4HANA Cloud / Oracle Fusion Cloud ERP**, 자체 ITSM -> **ServiceNow**, 자체 HR -> **Workday**, 자체 그룹웨어 -> **Microsoft 365 / Google Workspace**, 자체 BI -> **Tableau / Power BI**. License/Subscription 모델로 전환(예전 CapEx -> OpEx). 데이터 마이그레이션은 ETL/DI 도구(**Informatica, AWS DMS, Azure Data Factory, Matillion**) 활용. **IaaS에서 SaaS로의 "Step-up" 모델**이라 별도의 클라우드 마이그레이션이 아닌 경우도 많음. |
| **Refactor / Re-architect (Cloud-Native)** | 애플리케이션을 클라우드 네이티브 아키텍처로 재설계 | Monolithic Java/Spring -> **Microservices on Kubernetes(EKS/AKS/GKE/OpenShift)**. 동기 REST -> **Event-Driven (Kafka, Amazon Kinesis, EventBridge)**. RDB -> **Polyglot Persistence(Redis, DynamoDB, Cassandra, CosmosDB, MongoDB Atlas)**. 배포는 **CI/CD(GitHub Actions, GitLab CI, ArgoCD, Jenkins X)** + **GitOps**. 상태 관리는 **HashiCorp Vault / AWS Secrets Manager**. Observability는 **OpenTelemetry + Prometheus + Grafana + Datadog/New Relic**. **12-Factor App** + **Domain-Driven Design(Bounded Context)** 기반 분리. 가장 비용·기간이 크지만 **장기 TCO와 비즈니스 민첩성 극대화**. |
| **Retain (Revisit)** | 보안·규제·기술·비용 사유로 클라우드 전환을 보류하고 온프레미스에 그대로 유지 | **데이터 주권(예: 공공데이터, 의료데이터, 위치데이터)**, **초저지연 요구(예: HFT, 산업용 PLC, 5G MEC)**, **레거시 의존성(AS/400, Mainframe)**, **전환 ROI 부족** 등의 사유. **Hybrid Cloud(예: AWS Outposts, Azure Stack, Google Anthos on-prem)** 형태로 클라우드 관리 평면과 통합 운영할 수도 있음. **"지금 옮기지 않음"이 곧 실패가 아니라 의도된 전략적 결정**임을 명확히 경영진과 합의해야 함. |
| **Retire (Decommission)** | 사용률이 낮거나 EOL(End-of-Life) 도달한 시스템을 폐기 | **CMDB/ITSM(ServiceNow, Jira Service Management)** 데이터를 활용해 **마지막 사용일(Last Access Date) < 180~365일**인 시스템 식별. 데이터 보존 정책에 따라 **Cold Archive(Amazon S3 Glacier Deep Archive, Azure Archive Storage)**로 이전 후 원 시스템 폐기. **NIS(Network Information Service)/SOX 컴플라이언스**상 보존 의무가 있는 데이터는 WORM(Write Once Read Many) 스토리지 활용. **약 10~15%는 Retire 후보**라는 것이 AWS의 정설(McKinsey도 유사한 수치 보고). |

**핵심 의사결정 파라미터 (6R 선택 매트릭스)**

| 평가 항목 | 가중치(예시) | Rehost 유리 조건 | Replatform 유리 조건 | Refactor 유리 조건 | Retain 유리 조건 |
| :--- | :--- | :--- | :