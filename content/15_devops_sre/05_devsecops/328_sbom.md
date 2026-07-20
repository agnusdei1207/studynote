---
title: "Software Bill of Materials Supply Chain Defense SPDX CycloneDX VEX"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 328
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SBOM (Software Bill of Materials)은 소프트웨어를 구성하는 모든 컴포넌트, 라이브러리, 버전, 라이선스의 공식 인벤토리로, 공급망 공격(SolarWinds, XZ Utils 사태) 이후 소프트웨어 투명성의 핵심 수단이 되었다.
> 2. **가치**: SBOM이 있으면 Log4Shell 같은 Critical CVE 발표 시 영향받는 제품을 수 시간 내에 파악할 수 있다. SBOM 없이는 수천 개 서비스를 수동으로 검토해야 한다.
> 3. **판단 포인트**: SBOM은 생성만으로 끝나지 않는다. 빌드마다 갱신되어야 하고, VEX (Vulnerability Exploitability eXchange)와 결합해 "이 CVE가 이 제품에서 실제로 악용 가능한가"까지 답해야 의미 있다.

---

## Ⅰ. 개요 및 필요성

2020년 SolarWinds 공급망 공격은 빌드 파이프라인에 악성 코드가 삽입된 채 배포된 사례로, 미국 정부 기관을 포함한 수천 개 조직이 침해되었다. 이 사건은 소프트웨어 공급망 보안에 대한 근본적인 재검토를 촉발했고, 2021년 미국 행정명령 14028에서 연방정부 소프트웨어 공급업체에 SBOM 제공을 의무화했다.

SBOM (Software Bill of Materials)은 제조업의 BOM (Bill of Materials, 부품 목록)에서 유래한 개념이다. 자동차를 구성하는 모든 부품의 목록처럼, 소프트웨어를 구성하는 모든 컴포넌트의 완전한 목록이다. 이는 단순한 문서가 아니라 기계가 읽을 수 있는 구조화된 형식으로 제공되어야 한다.

> 📢 **섹션 요약 비유**: SBOM은 식품의 영양 성분 표시와 같다. 과자 봉지에 원재료명, 함량, 알레르기 유발 성분이 표시되어 있어야 소비자(사용 조직)가 안전 여부를 판단할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------+
|              SBOM 생성 및 활용 파이프라인          |
+------------------------------------------------+
|  소스코드 + 의존성 파일                           |
|          |                                     |
|          v                                     |
|  +----------------+                            |
|  |  SCA 도구       |  (Syft, Trivy, CycloneDX) |
|  +-------+--------+                            |
|          |                                     |
|          v                                     |
|  +----------------------------------------+   |
|  |  SBOM 파일 (SPDX 또는 CycloneDX 형식)  |   |
|  |  - 컴포넌트명, 버전, 공급자              |   |
|  |  - 라이선스 (MIT, Apache 2.0, GPL)      |   |
|  |  - 체크섬 (SHA-256)                     |   |
|  +------+---------------+-----------------+   |
|         |               |                      |
|         v               v                      |
|  CVE 취약점 조회    라이선스 컴플라이언스  VEX  |
|  (NVD, OSV)        분석                악용 가능성|
+------------------------------------------------+
```

| SBOM 형식 | 특징 | 주도 기관 |
|:---|:---|:---|
| SPDX (Software Package Data Exchange) | ISO 국제 표준, 광범위한 생태계 지원 | Linux Foundation |
| CycloneDX | 보안 중심, VEX 기본 지원 | OWASP |

VEX (Vulnerability Exploitability eXchange)는 SBOM의 보완 문서로 "이 제품의 특정 CVE는 악용 가능하다/불가하다/조사 중이다"를 공식 표명한다.

> 📢 **섹션 요약 비유**: SBOM은 약품 첨부 문서다. 약의 성분, 함량, 부작용, 주의사항이 모두 기재되어야 의사(보안팀)가 적절히 처방(대응)할 수 있다.

---

## Ⅲ. 비교 및 연결

| 항목 | SBOM | SCA | VEX |
|:---|:---|:---|:---|
| 유형 | 산출물 (정적 목록) | 프로세스 (동적 분석) | 보완 문서 (악용 가능성) |
| 업데이트 | 빌드마다 생성 | CI에서 지속 실행 | CVE 발표 시 작성 |
| 형식 | SPDX, CycloneDX | 도구별 다양 | CycloneDX VEX |
| 법적 요건 | EO 14028 의무화 | 내부 프로세스 | 자발적/일부 의무화 |

Syft는 OCI (Open Container Initiative) 이미지에서 SBOM을 추출하고, Grype는 이 SBOM으로 CVE를 스캔한다. 이미지 레지스트리(Harbor)에 SBOM을 저장하면 운영 중인 컨테이너의 취약점도 실시간 추적이 가능하다.

> 📢 **섹션 요약 비유**: SCA는 냉장고 내용물을 검사하는 과정이고, SBOM은 그 결과를 정리한 재료 목록표이며, VEX는 "이 재료는 지금 상하지 않았다"는 확인서다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### SBOM 생성 도구

- **Syft**: 컨테이너 이미지, 파일시스템, 소스코드에서 SBOM 생성 (SPDX, CycloneDX 지원)
- **Trivy**: 이미지 스캔 + SBOM 생성 통합 도구
- **CycloneDX Maven/npm 플러그인**: 빌드 도구에서 직접 SBOM 생성

### 체크리스트

1. 모든 배포 아티팩트에 SBOM이 자동 생성되는가?
2. SBOM이 아티팩트 저장소(Harbor, Nexus)에 연결 저장되는가?
3. Critical CVE 발표 시 SBOM을 조회해 영향 서비스 목록을 30분 내 생성할 수 있는가?
4. VEX 문서 작성 프로세스가 정의되어 False Positive CVE를 공식 처리하는가?

### 안티패턴

- <strong>SBOM 1회 생성 후 방치</strong>: 의존성이 바뀔 때마다 갱신하지 않으면 실효성 없음
- <strong>VEX 없는 SBOM</strong>: CVE 우선순위 관리 어려움, 보안팀 과부하

> 📢 **섹션 요약 비유**: SBOM 없이 보안 대응은 화재 시 건물 도면 없이 소방 활동하는 것이다. 어느 방에 무엇이 있는지 모르면 구조도, 진압도 늦어진다.

---

## Ⅴ. 기대효과 및 결론

SBOM 도입 조직은 신규 CVE 발표 시 영향받는 시스템을 수 시간 내에 파악하고 패치 우선순위를 설정할 수 있다. SolarWinds, Log4Shell 같은 공급망 사고에 대한 대응 시간이 수 주에서 수 시간으로 단축된다.

SBOM의 본질은 <strong>알 권리의 자동화</strong>다. 내가 사용하는 소프트웨어에 무엇이 들어있는지 아는 것이 보안의 첫 번째 단계다. 모르는 것은 보호할 수 없다.

> 📢 **섹션 요약 비유**: SBOM 없는 소프트웨어 보안은 내용물 표시 없는 택배 박스다. 박스가 안전한지 확인하려면 안에 무엇이 있는지 알아야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| SBOM (Software Bill of Materials) | 소프트웨어 컴포넌트 완전한 목록 |
| SPDX (Software Package Data Exchange) | ISO 표준 SBOM 형식 |
| CycloneDX | OWASP 주도 보안 중심 SBOM 형식 |
| VEX (Vulnerability Exploitability eXchange) | SBOM + CVE 악용 가능성 표명 |
| SCA (Software Composition Analysis) | SBOM 생성 프로세스 |
| SLSA (Supply chain Levels for Software Artifacts) | 빌드 출처 보증 프레임워크 |

### 📈 관련 키워드 및 발전 흐름도

```text
공급망 보안 인식 전          SBOM 표준화 시대            법제화/자동화 시대
------------------    --------------------------   -----------------------
수동 의존성 추적      ->  SPDX, CycloneDX 표준    ->  EO 14028 의무화
SolarWinds 사고           Syft, Trivy 도구 등장       VEX 도입
Log4Shell 대응 지연        이미지 레지스트리 통합         SLSA 프레임워크
```

### 👶 어린이를 위한 3줄 비유 설명

1. SBOM은 레고 박스 안에 든 블록 목록이에요. 어떤 블록이 몇 개 들어있는지 정확히 알아야 불량 블록을 바로 찾을 수 있어요.
2. 나쁜 블록(CVE 취약점)이 발견되면 SBOM 목록을 보고 어느 레고 세트에 그 블록이 들어있는지 바로 알 수 있어요.
3. SBOM 없이는 모든 레고 세트를 하나하나 뜯어봐야 해서 시간이 너무 오래 걸려요.
