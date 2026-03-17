+++
title = "531-542. 공급망 공격 및 AI 모델 보안"
date = "2026-03-14"
[extra]
category = "Security"
id = 531
+++

# 531-542. 공급망 공격 및 AI 모델 보안

### # 공급망 공급망 보안 및 AI 모델 안정성

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 공급망(Software Supply Chain)의 무결성을 보장하고, AI(Artificial Intelligence) 모델의 적대적 공격(Adversarial Attack)을 방어하는 것이 핵심입니다.
> 2. **가치**: SolarWinds 사례와 같은 대규모 침해를 방지하여 RTO(Recovery Time Objective)를 획기적으로 단축하고, AI 서비스의 신뢰성을 확보합니다.
> 3. **융합**: DevSecOps, SLSA (Supply-chain Levels for Software Artifacts), MLOps(Machine Learning Operations) 등의 프레임워크가 융합되어 자동화된 방어 체계를 구축합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**소프트웨어 공급망 공격(Software Supply Chain Attack)**은 공격자가 직접 목표 시스템을 공격하는 대신, 목표 시스템이 신뢰하는 제3의 공급업체(라이브러리, CI/CD 툴, 개발자 계정 등)를 탈취하여 악성 코드를 주입하는 방식입니다. 최근에는 클라우드 네이티브(Cloud Native) 환경의 확대와 함께 오픈소스 의존도가 높아지면서, 이 공격 벡터가 가장 치명적인 위협으로 부상했습니다.

**AI 모델 보안**은 머신러닝(Machine Learning) 파이프라인(데이터 수집 → 학습 → 배포) 자체를 공격 표적으로 삼거나, 학습된 모델의 취약점을 파악하여 오분류를 유도하는 공격을 방어하는 영역을 포함합니다. 이는 단순한 데이터 유출을 넘어 시스템의 판단 근거를 무력화하는 **적대적 예제(Adversarial Example)** 공격과 데이터를 오염시키는 **데이터 포이즈닝(Data Poisoning)**으로 구분됩니다.

#### 2. 등장 배경
① **기존 한계**: 방화벽(Firewall)이나 침입 탐지 시스템(IDS)은 외부에서 들어오는 트래픽만 감시하므로, 신뢰하는 서명된 소프트웨어 내부에 숨어있는 악성코드를 탐지하지 못함.
② **혁신적 패러다임**: **"Zero Trust(신뢰하지 않음 및 검증)"** 원칙이 소프트웨어 개발 생애 주기(SDLC) 전체로 확장됨. 코드의 출처를 검증하는 서명(Signing)과 구성 요소를 명시하는 SBOM(Software Bill of Materials) 도입.
③ **비즈니스 요구**: 금융, 국방 등 고신뢰 산업에서는 규정 준수(Compliance)를 위해 소프트웨어 구성 요소에 대한 투명성과 추적 가능성을 법적으로 요구함.

#### 3. 핵심 용어
- **SBOM (Software Bill of Materials)**: 소프트웨어를 구성하는 모든 오픈소스 라이브러리, 모듈, 버전 정보를 나열한 '재료 명세서'.
- **SLSA (Supply-chain Levels for Software Artifacts)**: Google이 제안한 소프트웨어 공급망 보안을 위한 검증 체계 프레임워크.
- **CI/CD (Continuous Integration/Continuous Deployment)**: 지속적 통합 및 배포 파이프라인으로, 이 과정의 보안이 공급망 안전의 핵심임.

> **📢 섹션 요약 비유**: 공급망 보안은 **'식자재 유통 과정의 위생 검역'**과 같습니다. 식당(사용자)이 아무리 위생적인 곳이더라도, 납품되는 채소(라이브러리)에 납독(악성코드)이 묻어있으면 손님은 식중독(해킹)에 걸리게 됩니다. 따라서 납품업체의 출처를 추적하고(SBOM), 식재료 검증(서명된 커밋)을 해야 안전합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 역할 (표)
| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/포맷 (Protocol/Format) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **VCS (Version Control System)** | 소스코드 무결성 관리 | Git 등을 통한 변경 이력 추적 및 분산 관리 | Git Protocol | 안전한 금고 |
| **GPG (GNU Privacy Guard)** | 코드 서명 및 신원 보증 | 개발자의 개인키로 커밋 해시 암호화 | OpenPGP | 도장(인감) |
| **CI/CD Pipeline** | 자동화 빌드 및 배포 | 코드 통합, 테스트, 프로비저닝 자동화 | YAML, Jenkins API | 자동 생산 라인 |
| **SBOM Tool** | 의존성 목록화 | 라이선스 및 취약점 정보 자동 생성 | SPDX, CycloneDX | 영수증 발급기 |
| **Artifact Repository** | 빌드 결과물 저장 | 서명된 아티팩트(App/Docker Image) 저장 | OCI, Maven | 완제품 창고 |

#### 2. 보안 아키텍처 (다이어그램)
다음은 신뢰할 수 있는 소프트웨어 공급망을 구축하기 위한 **SLSA 기반 아키텍처**의 흐름입니다. 개발자부터 최종 배포 환경까지의 신뢰 사슬(Chain of Trust)을 시각화했습니다.

```ascii
[SLSA 기반 Secure Supply Chain Architecture]

+----------------+           +----------------+           +----------------+
|   Developer    |           | Source Control |           | Build System  |
| (Workstation) |  (1) Push |   (GitHub/Git) |  (2) Fetch|  (Jenkins/CI) |
+-------+--------+----------+-------+--------+----------+-------+--------+
        |                               |                          |
        | GPG Sign                      | Verify Signature         |
        v                               v                          v
+----------------+           +----------------+           +----------------+
|  Signed Commit | -------->|  Trusted Repo  | -------->|  SAST/DAST Scan|
+-------+--------+           +----------------+           +-------+--------+
                                                                        |
                                                                        | (3) Generate
                                                                        v
+----------------+           +----------------+           +----------------+
|  End Users     | <---------|  Artifact Repo| <---------|  Signed Build  |
|  (Production)  |  (7) Pull |   (Harbor/Arti)|  (6) Store|  (Docker/Image)|
+----------------+           +----------------+           +----------------+
        ^                                                               |
        |                                                               |
        |                     +----------------+                       |
        +---------------------|  SBOM Gen/Scan| <----------------------+
                             |  (CycloneDX)   |
                             +----------------+
```

**[다이어그램 해설]**
1.  **개발 단계 (Developer → Source Control)**: 개발자는 자신의 **GPG (GNU Privacy Guard)** 개인키를 사용하여 커밋(Code Commit)에 서명합니다. 이는 "내가 이 코드를 작성했음을 증명"하는 디지털 서명입니다.
2.  **빌드 단계 (Build System)**: CI 서버는 소스 코드를 가져올 때(Fetch) 서명이 유효한지 검증(Verify)합니다. 통과된 코드만 빌드되며, 이 과정에서 **SAST (Static Application Security Testing)** 및 **DAST (Dynamic Application Security Testing)** 수행.
3.  **결과물 생성 (Signed Build)**: 빌드가 완료되면 최종 아티팩트(도커 이미지, 실행 파일)가 생성됩니다. 이때 빌드 시스템의 키로 아티팩트에 서명하고, 해당 아티팩트의 구성 정보를 담은 **SBOM**을 자동으로 생성합니다.
4.  **저장 및 배포 (Artifact Repo → Users)**: 서명이 완료된 아티팩트는 Artifact Repository에 저장되며, 운영 환경(Production)은 서명 검증이 통과된 아티팩트만 배포(Pull)하여 실행합니다.

#### 3. 핵심 기술: SBOM (Software Bill of Materials) 구조
SBOM은 소프트웨어의 성분표입니다. 대표적인 포맷인 **SPDX (Software Package Data Exchange)**와 **CycloneDX**의 구조를 JSON 스니펫으로 비교 분석합니다.

```json
// CycloneDX 예시 (v1.4)
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "metadata": {
    "component": {
      "name": "web-payment-app",
      "version": "1.0.0",
      "purl": "pkg:generic/payment-app@1.0.0"
    }
  },
  "components": [
    {
      "name": "axios",
      "version": "0.24.0",
      "purl": "pkg:npm/axios@0.24.0",
      "licenses": [{"license": {"id": "MIT"}}],
      "externalReferences": [
        {
          "type": "vulnerabilities",
          "url": "https://services.nvd.nist.gov/rest/json/cves/1.0?cpeId=cpe:2.3:a:axios:axios:0.24.0:**"
        }
      ]
    }
  ]
}
```
*   **분석**: 위 `components` 배열은 의존성 라이브러리를 나열합니다. `externalReferences`를 통해 해당 라이브러리의 CVE(Common Vulnerabilities and Exposures) 정보를 자동으로 연동할 수 있어 취약점 대응이 용이합니다.

> **📢 섹션 요약 비유**: 소프트웨어 개발 과정은 **'자동차 자동 조립 라인'**과 같습니다. 부품(코드)을 조립하는 기계(CI)가 아무리 좋아도, 납품업체가 브레이크 대신 얇은 판자를 보내면 사고가 납니다. SBOM은 "이 자동차의 부품번호 X가 Y회사 제품이다"라고 적힌 **'부품 명세서'** 역할을 하여, 리콜 사태 발생 시 어느 부품을 교체해야 할지 즉시 알려줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 공급망 공격 유형

| 분류 | 공격 유형 | 기술적 메커니즘 | 주요 사례 | 대응 전략 |
|:---|:---|:---|:---|:---|
| **Upstream** | **Dependency Confusion** | 공개 레포지토리에 내부 패키지와 같은 이름의 악성 패키지를 업로드하여 의존성 주입을 유도함. | Codecov 사건 (2021) | Private Registry 사용, Dependabot 경고 설정 |
| **Build** | **CI/CD Pipeline Compromise** | 빌드 서버의 설정 오류나 취약한 플러그인을 이용해 빌드 과정에 악성 스크립트 삽입. | SolarWinds (2020) | 빌드 서버 격리, 최소 권한 원칙(PoLP) 적용 |
| **Runtime** | **Typosquatting** | 인기 라이브러리 이름과 유사한 철자(예: `react-nativ` vs `react-native`)로 악성 패키지 업로드. | PyPI 탈취 사례 다수 | 코드 리뷰 강화, 정확한 패키지명 명시 |

#### 2. 과목 융합 관점: DevSecOps + AI + 네트워크
-   **DevSecOps와의 시너지**: 보안을 개발 이후 단계가 아닌 **'Shift Left(좌측 이동)'**하여 설계 및 코딩 단계에 통합합니다. **"Compliance as Code"** 개념을 적용하여 인가되지 않은 라이브러리 사용 시 빌드를 즉시 중단(Fail Fast)시킵니다.
-   **AI/ML 보안과의 융합**: 데이터 파이프라인에 **ETL (Extract, Transform, Load)** 과정을 거칠 때, 데이터 중독(Poisoning) 여부를 확인하는 **'Sanity Check'** 노드를 삽입해야 합니다.
-   **네트워크 보안과의 연계**: 서명되지 않은 아티팩트가 레지스트리에서 풀(Pull) 당할 경우, API Gateway 레벨에서 트래픽을 차단하는 정책을 수립할 수 있습니다.

> **📢 섹션 요약 비유**: 보안 방어는 **'성곽(Castle) 방어 시스템'**의 진화입니다. 과거에는 성벽(Perimeter)만 높이면 됐지만, 지금은 성 내부의 식량 공급책(공급망)이 적의 스파이일 가능성을 열어두고 있습니다. 따라서 성 입구(게이트웨이)뿐만 아니라 **식량을 나르는 마차(라이브러리)를 검문하고, 요리사(빌드 서버)를 신원 보증하는 다중 방어 체계**가 필요합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: SolarWords와 유사한 공급망 공격 감지
**상황**: 기업의 주요 배포 서버에서 미확인 프로세스가 탐지됨. 로그 분석 결과, 내부에서 사용하던 라이브러리 `utils-core` 버전 업데이트 이후 의심스러운 외부 송신이 발생함.
**의사결정 과정**:
1.  **즉시 차단 (Containment)**: 영향받는 서버를 격리(Isolation)하고, 해당 커밋의 **GPG 서명**을 검증합니다. (결과: 서명이 없거나, 알 수 없는 키로 서명됨 확인).
2.  **롤백 (Rollback)**: 이전의 안전한 아티팩트 버전으로 롤백합니다. 이때 **SBOM**을 참조하여 영향을 받은 범위를 신속하게 파악합니다.
3.  **근본 원인 분석 (RCA)**: 개발자 계정 토큰 노출 여부 확인 및 CI 파이프라인의 권한 설정을 재검토합니다.

#### 2. 도입 체크리스트
-   **기술적 검토**
    -   [ ] 모든 외부 라이브러리의 라이선스(GPL, MIT, Apache 등)와 CVE 취약점을 스캔하는 도구(예: **Snyk**, **OWASP Dependency-Check**) 도입 여부.
    -   [ ] Git 커밋 시 GPG 서명 강제 정책(`require signing`) 적용 여부.
    -   [ ] 빌드 아티팩트 생성 시 해시(Hash) 값 검증 로직 존재 여부.
-   **운영/보안적 검토**
    -   [ ] 개발자의 키(Key) 만료