+++
title = "737. SBOM 규격 SPDX CycloneDX"
date = "2026-03-15"
weight = 737
[extra]
categories = ["Software Engineering"]
tags = ["Security", "SBOM", "SPDX", "CycloneDX", "Supply Chain", "Open Source", "Compliance"]
+++

# [주제명] 737. SBOM 규격 SPDX CycloneDX

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 공급망의 투명성을 확보하기 위해 소프트웨어 구성 요소(오픈소스, 라이브러리, 모듈)의 **Bill of Materials (BOM)**을 기계가 해석 가능한 표준화된 데이터 형식으로 정의하는 것으로, '디지털 제품의 성분표' 역할을 한다.
> 2. **가치**: 라이선스(License) 준수 여부를 자동화하여 법적 리스크를 제거하고, CVE (Common Vulnerabilities and Exposures) 발생 시 영향 범위를 분석하여 대응 시간(MTTD)을 획기적으로 단축시키며, 미 행정명령 14028(EO 14028) 등 글로벌 보안 규제 대응의 핵심 인프라다.
> 3. **융합**: DevSecOps 파이프라인과 CI/CD (Continuous Integration/Continuous Deployment) 툴체인과深度融合되어, SCA (Software Composition Analysis) 도구를 통해 빌드 시점마다 실시간으로 SBOM을 생성 및 갱신하는 '동적 공급망 보안 체계'로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**SBOM (Software Bill of Materials)**은 소프트웨어를 구성하는 모든 '부품'의 목록이다. 단순한 텍스트 목록이 아니라, **형상 관리(Configuration Management)**의 관점에서 각 부품의 버전, 라이선스, 저작자, 서명된 해시값, 그리고 부품 간의 의존성(Dependency) 관계까지 기계 판독 가능한 형식(JSON, XML, YAML 등)으로 체계화한 것이다. 이는 소프트웨어 공급망(Software Supply Chain)의 블랙박스를 열어 투명성을 확보하고, 공급자와 소비자 간의 신뢰 사슬을 구축하는 근간이 된다.

#### 2. 💡 비유: 식품의 영양 성분표와 자동차 정비 명세서
소프트웨어는 마치 복잡한 레스토랑 요리나 자동차와 같다. 우리가 음식을 먹을 때 알레르기 유발 성분을 확인하듯, 소프트웨어 사용자는 어떤 오픈소스가 포함되어 있고 어떤 라이선스(지적재산권 권리)가 적용되는지 확인해야 한다. 또한, 자동차에 리콜이 발생했을 때 정비공이 차량의 부품 번호를 조회하여 해당 부품이 내 차에 쓰였는지 즉시 확인하듯, SBOM은 보안 취약점(CVE) 발생 시 피해 범위를 즉각 파악하게 해주는 '디지털 정비 명세서'다.

#### 3. 등장 배경: 블랙박스에서 투명성으로
① **기존 한계 (Blackbox)**: 과거 개발자는 `copy-paste` 방식으로 코드를 재사용하거나, `package.json` 같은 선언 파일에 의존하여 라이브러리를 관리했다. 이는 전체 구조를 파악하기 어렵고, '좀비 의존성(Zombie Dependency)'이나 '트랜스티브 의존성(Transitive Dependency, 의존의 의존)' 관리가 불가능했다.
② **혁신적 패러다임 (Transparency)**: 2020년대 SolarWinds 해킹 사건 등 소프트웨어 공급망 공격이 대두되면서, 미국 NTSC(National Telecommunications and Information Administration)가 최소 요소 요건(Minimum Elements)을 정의하고 표준화를 주도했다.
③ **현재의 비즈니스 요구 (Compliance)**: 미국의 행정명령(EO 14028), 유럽의 Cyber Resilience Act(CRA) 등에서 SBOM 작성을 법적 의무화하고 있어, 이제는 선택이 아닌 필수 생존 전략이 되었다.

#### 📢 섹션 요약 비유
> **"마치 고급 레스토랑에서 요리의 모든 재료 산지, 알레르기 유무, 그리고 조리 과정을 담은 '디지털 성분표'를 QR 코드로 제공하여, 손님이 믿고 먹을 수 있게 하는 것과 같습니다."**

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표): SBOM의 해부학적 구조
표준화된 SBOM 문서는 최소 5개 이상의 핵심 모듈로 구성되어야 하며, 이는 기계적 분석의 기초가 된다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 및 상세 | 필수 여부 | 비유 (Analogy) |
|:---:|:---|:---|:---:|:---|
| **Metadata** | SBOM 문서 자체의 식별 정보 | 생성일, 생성 도구(Tool), 작성자, 문서 이름(Name), 고유 UUID | **필수** | 제품 출고지, 제조일자 스티커 |
| **Components** | 실제 소프트웨어 부품 리스트 | 라이브러리명, 버전(Version), 파일 해시(Hash), 다운로드 URL, 라이선스 | **필수** | 자동차 부품 catalog |
| **Relationships** | 부품 간의 연결 고리 | `DEPENDS_ON`(의존), `PATCHES_FOR`(수정), `CONTAINS`(포함) 등 방향성 그래프 | **필수** | 부품 조립도(Explosion View) |
| **Licenses** | 법적 권리 및 의무 | **SPDX License ID** (예: Apache-2.0, MIT), 라이선스 텍스트 전문 | **필수** | 사용권 계약서 (EULA) |
| **Signatures** | 무결성 및 신뢰성 보장 | 작성자의 디지털 서명(Digital Signature), 서명 알고리즘(예: PGP) | 선택 | 진품 인증 홀로그램 |
| **Vulnerabilities** | 보안 취약점 분석 정보 | **CVE ID**, CVSS 점수, 패치 가능 여부 (주로 CycloneDX VEX 포함) | 선택 | 결함 수리 리콜 명단 |

#### 2. ASCII 구조 다이어그램: 양대 표준의 데이터 모델 비교
아래는 대표적인 두 표준인 **SPDX**와 **CycloneDX**의 계층 구조를 시각화한 것이다. **SPDX**는 '문서(Document)' 중심의 평면 구조에 가깝고, **CycloneDX**는 '의존성 그래프(Dependency Graph)' 중심의 계층 구조를 지향한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SBOM Data Structure Models                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [ SPDX Model ]               [ CycloneDX Model ]                           │
│  (Document Centric)           (Graph Centric)                               │
│                                                                             │
│  ┌─────────────────┐         ┌───────────────────┐                          │
│  │  SPDX Document  │         │  Bom (Root)       │                          │
│  │  { CreationInfo }│         │  { Metadata }     │                          │
│  └────────┬────────┘         └─────────┬─────────┘                          │
│           │                            │                                     │
│           ▼                            ▼                                     │
│  ┌─────────────────┐         ┌───────────────────┐                          │
│  │  Package List   │         │  Components       │                          │
│  │  (Flat List)    │         │  (Array/Tree)     │                          │
│  │  * pkg A        │         │  * comp A         │                          │
│  │  * pkg B        │         │  * comp B         │                          │
│  │    └─ licenses  │         │       └─ purl     │                          │
│  │    └─ files     │         └─────────┬─────────┘                          │
│  └─────────────────┘                   │                                     │
│                                       │ Reference                            │
│                                       ▼                                      │
│                              ┌───────────────────┐                          │
│                              │  Dependencies     │                          │
│                              │  (Graph Edges)    │                          │
│                              │  * A relies on B  │                          │
│                              │  * B relies on C  │                          │
│                              └───────────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 식별자 체계 (PURL & CPE)
SBOM의 핵심은 부품을 정확히 식별하는 것이다. 이를 위해 다음과 같은 식별자 표준을 사용한다.

1.  **PURL (Package URL)**: 소프트웨어 패키지의 위치를 통합하여 표현하는 표준 식별자.
    *   *형식*: `scheme:type/namespace/name@version?qualifiers#subpath`
    *   *예시*: `pkg:npm/%40angular/core@12.0.0` (NPM Registry의 Angular Core 버전 12.0.0)
    *   *역할*: 의존성 관리 도구가 패키지의 위치를 찾아 메타데이터를 가져오는 'GPS 좌표' 역할.
2.  **CPE (Common Platform Enumeration)**: 하드웨어, 운영체제, 소프트웨어의 취약점을 확인하기 위한 표준 이름.
    *   *형식*: `cpe:2.3:part:vendor:product:version:update:edition:language`
    *   *예시*: `cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*`
    *   *역할*: NVD (National Vulnerability Database)와 연동하여 보안 취약점 데이터를 매칭하는 '식별 번호판'.

#### 4. 핵심 알고리즘 및 코드: VEX (Vulnerability Exploitability eXchange) 분석 로직
VEX는 "A 라이브러리에 취약점이 있지만, 우리 시스템에서는 취약하지 않음(Not Exploitable)"을 선언하는 분석 결과다.

```python
# Pseudo-code: CycloneDX VEX Status Check Logic
def analyze_vex_impact(component, vuln_cve):
    """
    Analyzes if a component's vulnerability is exploitable in the current context.
    """
    # 1. Check if component is actually loaded in runtime (Runtime SBOM)
    if not is_loaded(component):
        return "NOT_IN_USE" 

    # 2. Check if vulnerable function is called
    if not calls_vulnerable_function(component, vuln_cve):
        return "NOT_EXPLOITABLE"

    # 3. Check if mitigations exist (e.g., WAF, Sandboxing)
    if has_mitigation(component, vuln_cve):
        return "MITIGATED"

    # 4. Default status
    return "EXPLOITABLE"
```

#### 📢 섹션 요약 비유
> **"마치 복잡한 기계식 시계의 부품 하나하나에 고유 부품 번호를 새겨두고, 어느 나사가 어디에 끼워지는지 설명하는 3D 설계도를 작성해두는 것과 같습니다. 이 설계도가 있어야 나사가 하나 빠져도(취약점) 정확히 그 위치를 찾아 교체할 수 있습니다."**

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: SPDX vs. CycloneDX
이 두 표준은 경쟁 관계라기보다 목적에 따라 선택 가능한 상호 보완적 관계에 있다.

| 비교 항목 | **SPDX (Software Package Data Exchange)** | **CycloneDX** |
|:---|:---|:---|
| **주관 기관** | **Linux Foundation** (ISO/IEC 5962 표준) | **OWASP Foundation** (OASIS 표준) |
| **핵심 철학** | **법적 준수(Legal Compliance)** 강화 | **보안 위주(Security First)**, 경량화 |
| **주요 데이터 포맷** | TagValue(.spdx), JSON, RDF, YAML | JSON, XML, **Protocol Buffers** (이진 직렬화) |
| **구조적 특징** | 평면적 파일 구조, 각 파일별 라이선스 명세 강세 | 계층적 의존성 그래프, 서비스(SBOM) 포함 |
| **고유 기능** | Snippet(코드 조각) 라이선스 관리 | **VEX**(취약성 분석 결과) 포함, **Signature** 표준화 |
| **자동화 친화성** | 상대적으로 복잡하여 파싱 오류 가능성 존재 | 가볍고 간결하여 스캐너/CI 도구 연동에 최적화 |

#### 2. 과목 융합 관점: SLSA (Supply-chain Levels for Software Artifacts)와의 연계
**SLSA**는 Google이 제안한 소프트웨어 공급망 보안 프레임워크로, 소스 코드부터 최종 아티팩트(Artifact)까지의 무결성을 보장한다. SBOM은 SLSA의 **Provenance(기원, 출처)** 증명서 내에 필수적인 메타 데이터로 포함된다.
*   **관계**: SBOM은 "재료 목록"이라면, SLSA는 "재료가 조리 과정을 거쳐 최종 요리가 되기까지의 CCTV 영상+요리사 인증서"다.
*   **시너지**: SBOM(내용물) + SLSA(무결성/작성자 서명)가 결합될 때, '이 소프트웨어가 변조되지 않았고, 내용물을 정확히 알고 있음'을 수학적으로 증명할 수 있다.

#### 3. 정량적 지표 활용 (Latency & Overhead)
실무 아키텍처에서 SBOM 생성 및 파싱이 시스템에 주는 영향을 분석한다.
*   **Storage Overhead**: 일반적인 대형 애플리케이션(라이브러리 500개 사용)의 CycloneDX JSON 파일 크기는 약 **50KB ~ 200KB** 수준으로, 이미지나 바이너리에 비해 미미한 수준이다.
*   **Scan Latency**: Dependency-Track 같은 도구를 사용할 때, 업로드된 SBOM 분석 및 취약점 매칭 시간은 평균 **2초 이내**로 수행되어 CI/CD 파이프라인에서 병목(Bottleneck)을 거의 유발하지 않는다.

#### 📢 섹션 요약 비유
> **"법률가가 계약서를 검토하듯 꼼꼼한 '서류 가방(SPX)'을 들고 다니는 전문가와, 응급 상황에 가볍게 튀어나가 신속하게 환자를 진단하는 '응급 키트(CycloneDX)'를 든 의사의 차이와 같습니다. 상황에 맞는 도구를 선택해야 합니다."**

---

### Ⅳ. 실무 적용 및 기술사