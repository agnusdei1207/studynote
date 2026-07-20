---
title: "Cloud Security CSPM CWPP CNAPP"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 632
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CSPM(Cloud Security Posture Management)은 클라우드 설정 오류(Misconfiguration)와 컴플라이언스 위반을 IaC·API 기반으로 지속 탐지하는 **클라우드 구성 보안(Control Plane)** 기술이며, CWPP(Cloud Workload Protection Platform)는 VM·컨테이너·서버리스 등 **워크로드 런타임 행위 기반** 보호에 특화된 **컴퓨트 계층 보안 기술**이고, CNAPP(Cloud-Native Application Protection Platform)은 CSPM·CWPP·CIEM·DSPM·IaC Scanning·KSPM을 단일 데이터 그래프(Single Data Graph) 위에 통합한 **클라우드 네이티브 종합 방어 체계**이다.
> 2. **가치**: Gartner 보고(2022~2024)에 따르면 클라우드 침해의 **80% 이상이 설정 오류 및 자격증명 노출에서 발생**하며, CNAPP 도입 시 보안 운영 가시성(Security Posture Visibility)이 약 70% 향상, MTTD(평균 탐지 시간)는 단일 도구 대비 60% 단축, 인시던트 대응 비용은 **연 1,500만 원~수십억 원 절감**(Ponemon 2023 기준) 효과를 기대할 수 있다.
> 3. **판단 포인트**: CSPM·CWPP을 별도 벤더로 운영할 경우 **데이터 사일로(Silo)와 라이선스 중복**, 정책 불일치로 인해 운영 효율이 저하되므로, **Agent 기반 vs Agentless 스캔의 트레이드오프**, 멀티클라우드 통합성, K8s·서버리스 등 **동적 워크로드 지원 범위**, 그리고 **Shift-Left(IaC 스캔) vs Runtime Protection 우선순위**를 고려한 통합 CNAPP 전략이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅의 광범위한 도입과 함께 전통적인 경계 기반 보안(Perimeter-based Security) 모델은 **무력화**되었다. AWS·Azure·GCP 등 하이퍼스케일러는 매년 수백 개의 신규 서비스를 출시하며, IaaS·PaaS·SaaS·FaaS·CaaS 등 **다층 책임 분담 모델(Shared Responsibility Model)** 하에서 보안 책임이 분산된다. 기업은 평균 3.4개의 퍼블릭 클라우드와 1,000개 이상의 SaaS 애플리케이션을 동시에 운영하며, 그 결과 **Configuration Drift**, **권한 남용(Privilege Creep)**, **취약한 컨테이너 이미지**, **노출된 S3 버킷**, **과도한 IAM 정책** 등 클라우드 네이티브 리스크가 기하급수적으로 증가하고 있다.

전통적 SIEM·IDS/IPS·WAF는 클라우드 **제어 평면(Control Plane)**의 설정 오류와 **워크로드 평면(Workload Plane)**의 런타임 행위를 동시에 가시화하지 못하는 한계를 가진다. AWS Config·Azure Policy 같은 **네이티브 도구**는 해당 CSP에 종속(CSP Lock-in)되며, 멀티클라우드 환경에서는 정책 일관성을 유지하기 어렵다. 또한, GitHub·GitLab 등 코드 저장소에서 발생하는 **IaC(Infrastructure as Code) 결함**은 배포 전 탐지하지 않으면 프로덕션 환경에 그대로 반영되어 공격 표면(Attack Surface)을 확대한다.

이에 따라 Gartner는 2019년 **CSPM**, 2019년 **CWPP**를 각각 매직 쿼드런트에 등재한 데 이어, 2021년 **CNAPP**이라는 통합 카테고리를 정의하며 클라우드 보안 패러다임의 전환을 예고했다. CNAPP는 단순한 도구 묶음이 아니라 **DevSecOps 파이프라인부터 런타임 워크로드까지 전 생애주기를 단일 그래프 모델로 연결**하는 아키텍처 철학이다.

```text
+--------------------------------------------------------------------------+
|                클라우드 보안 진화: 전통 보안 -> CSPM/CWPP -> CNAPP         |
+--------------------------------------------------------------------------+
|                                                                          |
|   [1세대: 전통 경계보안]   [2세대: 개별 포인트솔루션]   [3세대: CNAPP 통합] |
|   +--------------+        +--------------+        +--------------+      |
|   |  Firewall    |        |   CSPM (예)  |        |              |      |
|   |  IDS/IPS     |   ->    |  + CWPP (예) |   ->    |    CNAPP     |      |
|   |  SIEM        |        |  + CIEM (예) |        | (단일플랫폼) |      |
|   |  WAF         |        |  + DSPM (예) |        |              |      |
|   +--------------+        +--------------+        +--------------+      |
|   문제: 클라우드 비가시성    문제: 데이터 사일로        해결: 통합 가시성   |
|                                                                          |
|   +------------------------------------------------------------+         |
|   |  DevSecOps 파이프라인 통합 (Shift-Left Security)            |         |
|   |  Code -> Build -> Test -> Deploy -> Runtime -> Monitor         |         |
|   +------------------------------------------------------------+         |
|                                                                          |
|   +------------------------------------------------------------+         |
|   |  멀티클라우드·멀티워크로드 통합 가시성 (Single Pane of Glass)|         |
|   |  AWS · Azure · GCP · Alibaba · OCI · K8s · Serverless      |         |
|   +------------------------------------------------------------+         |
+--------------------------------------------------------------------------+
```

기존의 **"네트워크 -> 호스트 -> 애플리케이션"** 중심 보안 사고방식은, 클라우드에서 **"코드(IaC) -> ID/자격증명 -> 구성(Control Plane) -> 워크로드(Workload) -> 데이터(Data)"** 라는 5차원 모델로 재편되어야 한다. CNAPP는 정확히 이 5개 차원을 단일 그래프(Graph)로 정규화하여 분석한다.

- **📢 섹션 요약 비유**: CSPM은 **건물의 CCTV·출입통제 시스템**(누가 어디에 무엇을 두었나 확인), CWPP는 **각 방마다 설치된 연기감지기·도난경보기**(안에 든 보물을 실시간 보호), CNAPP는 이 모든 것을 **단일 관제센터(통합상황실)**에서 24시간 통합 관제하는 **스마트 빌딩 보안 시스템**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CNAPP는 일반적으로 다음 **5개 핵심 모듈**과 **공통 데이터 레이어**로 구성된다. 각 모듈은 독립적으로 운영 가능하지만, CNAPP는 이를 **단일 에이전트/에이전트리스 컬렉터**와 **통합 정책 엔진**으로 연결한다.

```text
+--------------------------------------------------------------------------+
|                          CNAPP 통합 아키텍처                              |
+--------------------------------------------------------------------------+
|                                                                          |
|  +------------------------------------------------------------+         |
|  |              통합 데이터 그래프 (Unified Data Graph)         |         |
|  |  Asset · Identity · Network · Vulnerability · Threat · Data |         |
|  +------------------------------------------------------------+         |
|       ^            ^            ^            ^            ^             |
|       |            |            |            |            |             |
|  +----+---+  +-----+----+  +----+----+  +----+----+  +----+----+       |
|  |  CSPM  |  |   CIEM   |  |  CWPP   |  |  DSPM   |  | IaC Sec |       |
|  |(구성)  |  |(자격증명)|  |(워크로드)|  |(데이터) |  |(코드)   |       |
|  +----+---+  +-----+----+  +----+----+  +----+----+  +----+----+       |
|       |            |            |            |            |             |
|       v            v            v            v            v             |
|  +------------------------------------------------------------+         |
|  |   API Connectors      Agent-based      Agentless Scanning   |         |
|  |   (AWS Config, Azure  (Falcon, Aqua,    (Snapshot Diff,      |         |
|  |    Resource Graph)    Defender)         Side-Scanner)       |         |
|  +------------------------------------------------------------+         |
|       |            |            |            |            |             |
|       v            v            v            v            v             |
|  +------------------------------------------------------------+         |
|  |   멀티클라우드 환경: AWS · Azure · GCP · OCI · Alibaba      |         |
|  |   멀티워크로드:   VM · Container · K8s · Serverless · PaaS  |         |
|  +------------------------------------------------------------+         |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CSPM** (Cloud Security Posture Management) | 클라우드 리소스 **구성 오류** 및 **컴플라이언스 위반** 지속 탐지 | • **API 기반 에이전트리스 스캔**: AWS Config Rule, Azure Resource Graph, GCP Cloud Asset Inventory API 호출<br>• **벤치마크 매핑**: CIS AWS Foundations v1.5+, CIS Azure 2.0, CIS GCP 2.0, PCI DSS 4.0, NIST 800-53 Rev.5, K-ISMS-P, ISO 27001/27017/27018<br>• **정책 엔진**: Rego(OPA), Cedar, JSON Policy 기반 DSL<br>• **Drift Detection**: 기준선(Baseline)과 현재 상태의 차이 분석, 5~15분 주기 폴링 |
| **CWPP** (Cloud Workload Protection Platform) | VM·컨테이너·서버리스 **런타임 보호** 및 취약점·악성코드 탐지 | • **호스트/컨테이너 에이전트**: eBPF 기반 syscall 모니터링(Cilium Tetragon, Falco), 커널 후킹<br>• **이미지 스캔**: Trivy, Clair, Anchore, Snyk Container — CVE·SBOM 분석, **SLSA L3** 검증<br>• **런타임 행위 분석**: 프로세스 트리, 네트워크 eBPF 캡처, 파일 무결성 모니터링(FIM)<br>• **취약점 우선순위**: EPSS(Exploit Prediction Scoring System)·KEV(known Exploited Vulnerabilities)·CVSS v3.1 통합 위험도 산정 |
| **CIEM** (Cloud Infrastructure Entitlement Management) | **과도한 권한(Over-Privilege)** 및 **권한 그래프** 분석 | • **권한 그래프(Privilege Graph)**: IAM Role, Policy, Resource 간 관계 모델링(Zscaler CIEM, Sonrai, Microsoft Entra Permissions Management)<br>• **JIT(Just-In-Time) 권한 부여**: 권한 사용 시간·빈도 분석을 통한 미사용 권한 제거<br>• **Toxic Combination 탐지**: 예) S3:GetObject + kms:Decrypt + iam:PassRole 조합으로 데이터 유출 가능 시나리오 |
| **DSPM** (Data Security Posture Management) | 클라우드 저장 데이터(**S3, RDS, BigQuery, Blob**) 분류·암호화·접근 추적 | • **자동 데이터 분류**: 정규식·ML 기반 PII(개인식별정보)·PHI·금융정보 자동 태깅<br>• **암호화 검증**: KMS 키 회전 주기, 전송 중(TLS 1.3)·저장 시(AES-256) 암호화 적용 여부<br>• **데이터 흐름 추적**: Lineage 그래프(예: Wiz Data Security Posture, Dig Security, Sentra) |
| **IaC Scanning** (Shift-Left) | Terraform·CloudFormation·ARM·Pulumi·Kubernetes YAML의 **배포 전 결함 탐지** | • **정적 분석**: Terraform Plan Diff 분석(tflint, checkov, tfsec, kics)<br>• **PR Gate**: GitHub Actions·GitLab CI에서 정책 위반 시 병합 차단<br>• **드리프트 방지**: 배포된 실제 리소스와 IaC 코드 일치성 검증(예: driftctl) |

**핵심 원리 심층 분석**:

1. **에이전트리스(Agentless) vs 에이전트 기반(Agent-based) 트레이드오프**
   - **에이전트리스**: 클라우드 API 호출 또는 **디스크 스냅샷 + Side-Scanning VM**(Wiz, Orca 방식)으로 워크로드 내부 스캔. 운영 부담 적음, **런타임 행위 탐지 불가**, API 호출 비용 발생
   - **에이전트 기반**: 워크로드 내부에 데몬(예: Aqua Enforcer, CrowdStrike Falcon Sensor, Datadog Agent) 설치. **eBPF/Cilium**으로 syscall·네트워크 실시간 캡처. **런타임 보호 가능**, 에이전트 관리 오버헤드·호환성 이슈 존재
   - **하이브리드 전략**: 메타데이터는 에이전트리스, 런타임 행위는 에이전트로 수집(예: Palo Alto Prisma Cloud, Microsoft Defender for Cloud P2)

2. **위험도 우선순위화(Risk Prioritization) 알고리즘**
   단순한 CVE 점수(CVSS)가 아닌 **컨텍스트 기반 위험도** 산정:
   - **공격 도달성(Attack Path)**: 그래프 분석으로 인터넷 노출 -> 취약 컨테이너 -> 권한 상승 -> 데이터 유출 경로 자동 식별
   - **민감도(Sensitivity)**: 대상 리소스가 PII·금융정보 포함 시 가중치 부여
   - **악용 가능성(EPSS)**: 실제 CISA KEV 등재·PoC 공개·웹 위협 인텔리전스 통합

3. **정책 코드화(Policy as Code)**
   ```rego
   # OPA/Rego 예시: S3 퍼블릭 액세스 차단 정책
   package aws.s3.deny_public

   deny[msg] {
       input.resource_type == "aws_s3_bucket"
       input.acl == "public-read"
       msg := sprintf("S3 버킷 '%s'은(는) public-read로 설정될 수 없습니다 (CIS AWS 2.1.5)", [input.name])
   }
   ```

- **📢 섹션 요약 비유**: CNAPP의 **통합 데이터 그래프**는 **병원 통합 차트 시스템**과 같다. 환자의 혈압·맥박·X-ray·약물 이력을 **한 장의 차트**에 통합해 보여주므로, 각과 전문의(보안 분석가)가 단일 맥락에서 종합 진단(위험 분석)을 내릴 수 있다. CSPM은 **기초 검사 결과**, CWPP는 **수술 중 모니터링**, CIEM은 **수술 권한 관리**, DSPM은 **환자 프라이버시 보호**, IaC 스캔은 **수술 전 사전 검사**에 해당한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **CSPM** | **CWPP** | **CNAPP** |
| :--- | :--- | :--- | :--- |
| **주 대상** | 클라우드 **제어 평면** (계정, 네트워크, 스토리지, IAM 설정) | 클라우드 **워크로드 평면** (VM, 컨테이너, K8s, 서버리스 코드) | **제어 평면 + 워크로드 평면 + 데이터 평면 + ID 평면 통합** |
| **탐지 시점** | 구성 변경 후 (Posture-Time), **수 초~수 분** 내 | 런타임 행위 기반 (Real-Time), **수 밀리초~수 초** 내 | IaC 코드 단계부터 런타임까지 **전 생애주기** |
| **데이터 소스** | 클라우드 API (AWS Config, Azure Policy, GCP Org Policy) | 에이전트(eBPF), 컨테이너 런타임, 이미지 레지스트리 | 모든 CSP/CWPP/CIEM/DSPM 소스 + 외부 위협 인텔리전스 |
| **기술 방식** | 에이전트리스 API 스캔, 정책 코드(Rego/Cedar) | 에이전트 기반 syscall·파일·네