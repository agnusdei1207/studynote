+++
title = "738. 컨테이너 이미지 스캐닝 권한 통제"
date = "2026-03-15"
weight = 738
[extra]
categories = ["Software Engineering"]
tags = ["Security", "Container", "Docker", "Vulnerability Scanning", "RBAC", "Cloud Native", "Admission Control"]
+++

# 738. 컨테이너 이미지 스캐닝 권한 통제

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너(Cgroup, Namespace 기반 격리 기술)의 **이미지(Image)**는 레이어 형태의 파일 시스템이므로, 배포 전 내부 패키지의 취약점을 식별하는 **정적 분적 스캐닝**과, 신뢰할 수 있는 주체만 이미지를 생성/배포하도록 강제하는 **RBAC (Role-Based Access Control)** 및 **서명 검증** 체계가 필수적이다.
> 2. **메커니즘**: CI/CD 파이프라인 내에서 **CVE (Common Vulnerabilities and Exposures)** 데이터베이스와 대조하여 취약점을 탐지하고, **Admission Controller (准入 제어기)**를 통해 클러스터 진입 단계에서 정책 위배 이미지를 실시간 필터링하는 **Defense-in-Depth (심층 방어)** 구조를 형성한다.
> 3. **가치**: 공급망(Supply Chain) 공격 방지 및 미끄러진 사각지대 제로화를 통해, 운영 환경의 **Mean Time to Remediate (MTTR)**을 단축하고 컴플라이언스(Compliance) 요구사항을 자동화하여 보안 리스크를 정량적으로 저감한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
컨테이너 기술은 애플리케이션을 **Immutable Infrastructure (불변 인프라)**로 관리하는 패러다임을 가져왔으나, 기본적으로 **'신뢰할 수 없는 레지스트리(Registry)'**에서 가져온 이미지는 내부에 백도어나 오래된 라이브러리 취약점을 포함할 수 있다. 따라서 단순히 실행 격리만으로는 부족하며, **'이미지가 생성되는 순간(Shift-left)'**부터 **'실행되는 순간(Runtime)'**까지 이미지의 무결성과 안전성을 보장하는 **이중 통제 체계**가 요구된다. 이는 단순한 스캔 도구 도입이 아닌, 소프트웨어 공급망의 투명성을 확보하는 거버넌스(Governance) 설계이다.

#### 2. 배경 및 문제 정의
- **기존 한계**: 기존의 보안 스캐너는 운영 중인 서버(VM/Bare Metal)에 접속하여 주기적으로 점검하였으나, 컨테이너는 초단위로 생성되고 소멸(Ephemeral)하므로 스캔 시점과 실행 시점의 차이(Blind Spot)가 발생한다.
- **패러다임 변화**: 모놀리식(Monolithic) 구조에서 마이크로서비스(Microservices)로 전환됨에 따라, 수백 개의 이미지가 수시로 배포되므로 사람에 의한 수동 검증은 불가능하며 **Policy-as-Code**에 기반한 자동화된 통제가 필요하다.
- **비즈니스 요구**: 랜섬웨어(Ransomware) 및 공급망 공격(SolarWinds 사태 등)이 증가함에 따라, 규제 기관은 소프트웨어 구성 요소(SBOM)에 대한 투명성과 취약점 관리를 의무화하고 있다.

#### 3. 💡 핵심 비유
컨테이너 보안은 마치 **'고속도로 톨게이트의 자동 차단 시스템'**과 같다.
단순히 요금을 받고 통과시키는 것이 아니라, 차량이 톨게이트에 진입하기 전 **차량 번호(이미지 ID)**를 인식하고, **적재 화물(패키지)에 위험 물질(취약점)이 없는지 X-Ray(스캐닝)**로 확인한다. 만약 위험물이 발견되거나 **등록되지 않은 차량(권한 없는 사용자)**일 경우 진입 바리케이드(Admission Controller)를 자동으로 내려 차단하는 시스템이다.

```text
+-----------------------------------------------------------------------+
|                 ⚠️  보안 게이트 개념도 (Security Gate Concept)          |
+-----------------------------------------------------------------------+
|                                                                       |
|  1. BUILD STAGE (출발지)                                              |
|     [ 개발자 ] --(Push)--> [ 레지스트리 ]                             |
|                       ▲                                               |
|                       │ (Fail Return if Critical CVE)                 |
|                       │                                               |
|  2. SCAN STAGE (검문소)                                               |
|     [ Scanner Engine ] <--(Pull)----------------------------------+   |
|          │                                                           |   |
|          │  ◀ Static Analysis (Binary/Manifest)                      |   |
|          │  ◀ DB Matching (CVE/NVD)                                  |   |
|          ▼                                                           |   |
|     [ V-Report : CRITICAL ] --(Block)--> [ REJECT ]                  |   |
|                                                                       |   |
|  3. RUNTIME STAGE (도로 진입)                                         |   |
|     [ K8s Cluster ] <--(Deploy Request)----------------------------+   |
|          │                                                           |   |
|          ▼                                                           |   |
|     [ Admission Controller ]                                         |   |
|          │ (Check Policy: Is Signature Valid? Is Image Trusted?)     |   |
|          ▼                                                           |   |
|     [ PASS ] --(Schedule Pods)--> [ Node Run ]                       |   |
|          ▼                                                           |   |
|     [ DENY ] --(Audit Log)------------> [ Alert Sysadmin ]           |   |
|                                                                       |
+-----------------------------------------------------------------------+
```

#### 📢 섹션 요약 비유
이 섹션에서 다룬 내용은 **"공항 수하물 검색대와 보안 검색대를 통합한 관제 시스템"**을 설계하는 것과 같습니다. 여행객(개발자)이 짐(이미지)을 부치자마자 폭발물(취약점)이 있는지 자동으로 스캔하여 위험한 가방은 애초에 보내지 못하게 막고, 탑승수속(배포) 단계에서는 위조된 여권(권한 없는 이미지)을 소지한 사람이 비행기(클러스터)에 타는 것을 원천 봉쇄하는 보안 프로세스를 구축하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석 (Component Analysis)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Mechanism) | 주요 프로토콜/표준 | 관련 비유 |
|:---:|:---|:---|:---|:---|
| **Registry (레지스트리)** | 이미지 저장소 | 이미지를 레이어 단위로 저장 및 배포, 암호화 전송 지원 | HTTP/REST, OAuth2 | 창고 (Warehouse) |
| **Scanner (스캐너)** | 정적 분석 엔진 | 이미지 파일 시스템을 마운트 후 패키지 매니저(DB) 해석 및 CVE DB와 해시 매칭 | CVE, CVSS | X-Ray 검색기 |
| **Signer (서명기)** | 무결성 보장 | 이미지 다이제스트(Digest)에 개인키로 전자 서명 생성 및 검증 | Cosign, Notary V2 | 진품 인증 스티커 |
| **Admission Controller** | 진입 통제 | K8s API 서버의 훅(Hook)을 통해 Pod 생성 요청을 가로채 정책 검증 | Webhook, JSON | 입국 심사관 |
| **Policy Engine** | 정책 관리 | OPA(Open Policy Agent) 등을 통해 스캔 결과 점수 기반 배포 허용/거부 규칙 작성 | Rego Language | 법률 (Law) |

#### 2. 이미지 스캐닝 심층 원리 (Deep Dive: Vulnerability Scanning)

이미지 스캐닝은 단순히 파일 스트링 검색이 아닌, 패키지 매니저의 의존성 트리(Dependency Tree)를 분석하는 과정이다.

```text
+-----------------------------------------------------------------------+
|             🔍 이미지 취약점 스캐닝 프로세스 (Scanning Process)         |
+-----------------------------------------------------------------------+
|                                                                       |
|  [Step 1] Image Pull & Unpack                                         |
|  ──────────────────────                                              |
|  Registry로부터 이미지를 Pull 받은 후, Tarball 형태의 레이어들을      |
|  임시 디렉토리에 압축 해제(Decompress).                                |
|                                                                       |
|  [Step 2] Manifest & Layer Analysis                                   |
|  ────────────────────────────────                                    |
|  Manifest(JSON)를 파싱하여 각 레이어의 ChainID를 확인하고,             |
|  OS 종류(Alpine, Ubuntu, Distroless)를 식별.                          |
|                                                                       |
|  [Step 3] Indexing (File System Crawling)                             |
|  ────────────────────────────────────                                |
|  ┌─────────────────────────────────────┐                             |
|  │ Layer A  : /usr/bin/nginx (Binary)  │  -> (1) 파일 해시 계산       |
|  │ Layer B  : /lib/x86_64/libc.so.6    │  -> (2) 패키지 DB 탐색       |
|  │ Layer C  : /var/lib/apt/lists       │  -> (3) 소스코드 경로 확인   |
|  └─────────────────────────────────────┘                             |
|     ▲                                                             │   |
|     └───────────┐                                                   │   |
|                 ▼                                                   │   |
|  [Step 4] Package DB Parsing                                        │   |
|  ──────────────────────────────                                     │   |
|  OS별 패키지 DB에 접근하여 설치된 패키지 목록 추출:                  │   |
|  - Debian/Ubuntu : /var/lib/dpkg/status                              │   |
|  - RHEL/CentOS   : /var/lib/rpm/Packages                             │   |
|  - Alpine        : /lib/apk/db/installed                             │   |
|                 + Language Pkg (package.json, go.mod)                │   |
|                                                                       |
|  [Step 5] CVE Matching & Scoring                                     │   |
|  ─────────────────────────────────                                 │   |
|  추출된 [Package Name + Version]을 NVD(National Vulnerability DB)    │   |
|  및 사내 CVE Feed와 대조.                                             │   |
|  해당 패키지의 버전이 취약점 범위에 포함되는지 확인.                  │   |
|  결과 : CVE-2023-xxxx (CVSS 9.8 Critical)                            │   |
|                                                                       |
+-----------------------------------------------------------------------+
```

**[해설]**
위 다이어그램은 컨테이너 이미지가 어떻게 스캔되는지를 5단계로 상세화한 것이다.
① **Pull & Unpack**: 단순 텍스트가 아닌 바이너리 형태로 존재하는 이미지를 분석 가능한 상태로 변환한다.
② **Manifest 분석**: 도커 이미지의 구조 정보를 파악한다.
③ **Indexing**: 각 레이어를 순회하며 파일 시스템 내의 패키지 매니저 데이터베이스 파일을 찾아낸다. 이때 단순 문자열 매칭이 아닌 **바이너리 분석(Binary Hardening)** 기술도 사용된다.
④ **DB Parsing**: `dpkg`, `rpm`, `apk` 등의 고유 데이터베이스 포맷을 파싱하여 정확한 버전 정보를 추출한다. 예를 들어 `openssl 1.1.1`이 설치되어 있는지 확인한다.
⑤ **CVE Matching**: 추출된 버전 정보와 취약점 데이터베이스를 조인(Join)한다. 만약 `openssl 1.1.1`이 Heartbleed 취약점이 있다고 판명되면 해당 레이어를 **Vulnerable Layer**로 표시한다.

#### 3. 핵심 알고리즘 및 권한 통제 로직

이미지 스캐닝 결과를 바탕으로 배포를 제어하는 것은 **Admission Control**의 영역이다. 쿠버네티스는 **Mutating**과 **Validating** 웹훅을 제공하는데, 보안을 위해 **Validating Webhook**을 주로 사용한다.

```python
# [Pseudo Code] Kubernetes Admission Controller Logic
# 단순화한 웹훅 핸들러 예제 (Python-like)

def admit_pod(review_request):
    # 1. 요청 파싱
    pod = review_request["object"]
    containers = pod["spec"]["containers"]

    for container in containers:
        image_name = container["image"]
        image_digest = resolve_image_digest(image_name) # SHA256 해시값 획득

        # 2. 서명 검증 (Cosign / Notary)
        if not verify_signature(image_digest):
            return build_response(False, "Image Signature is INVALID.")

        # 3. 취약점 스캔 결과 조회 (선행 스캔 가정)
        vuln_report = get_scan_report(image_digest)
        
        # 4. 정책 평가 (Policy Evaluation)
        # Critical 취약점이 1개라도 있거나, High가 3개 이상일 경우 거부
        if vuln_report["critical_count"] > 0:
             return build_response(False, f"CRITICAL CVEs found in {image_name}")
        
        if vuln_report["high_count"] >= 3:
             return build_response(False, f"Too many HIGH CVEs in {image_name}")

        # 5. 레지스트리 신뢰성 확인
        registry_host = extract_registry(image_name)
        if registry_host not in TRUSTED_REGISTRIES:
             return build_response(False, "Untrusted Registry Source")

    # 모든 검증 통과
    return build_response(True, "Admission Allowed")

def build_response(allowed, message):
    return {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {"allowed": allowed, "status": {"message": message}}
    }
```

#### 📢 섹션 요약 비유
이 섹션의 아키텍처와 원리는 **"엄격한 식당 위생 검사관과 예약 시스템"**과 같습니다.
① 스캐닝은 식재료(이미지)가 들어왔을 때 **위생 검사관**이 꼼꼼하게 재료의 원산지와 유통기한(패키지 버전)을 검사하고 세균(CVE)을 배양하는 과정입니다.
② 권한 통제는 **예약 직원**이 검사를 통과하고 위생 등급이 매겨진 식재료만 식탁(클러스터)에 내놓도록 통제하는 시스템입니다.
③ 이 모든 과정은 요리사(개발자)가 주방에 들어가기 전, 키친 입구에서 자동으로 이루어지므로, 한번 들어간 재료가 바뀌지 않음을 보장합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 비교: 전통 보안 vs 컨테이너 보안 (Traditional vs. Container)

| 비교 항목 (Metric) | 전통 서버 보안 (VM/Bare Metal) | 컨테이너 보안 (Container) | 시사점 (Implication) |
|:---:|:---|:---|:---|
| **보안 경계** | 물리적 머신 및 OS 경계 | **애플리케이션 (Image)