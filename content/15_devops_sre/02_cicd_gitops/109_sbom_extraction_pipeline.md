---
title: "Sbom Extraction Pipeline"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 109
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SBOM(Software Bill of Materials)은 소프트웨어를 구성하는 <strong>모든 오픈소스 라이브러리·버전·의존성 관계를 기계 판독 가능한 표준 포맷(SPDX, CycloneDX)으로 기록한 디지털 자재 명세서</strong>다.
> 2. **가치**: CI/CD 파이프라인에서 빌드 시점에 자동 추출하여, Log4j 같은 <strong>공급망 공격(Supply Chain Attack) 발생 시 취약 컴포넌트 포함 여부를 수초 내 전수 조사</strong>할 수 있다.
> 3. **판단 포인트**: 미 행정명령(EO 14028)으로 연방 납품 소프트웨어에 SBOM 제출이 <strong>법적 의무화</strong>되었으며, SBOM + VEX(실제 악용 가능성 평가) + 디지털 서명(Sigstore)의 3단 결합이 DevSecOps 표준이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어의 80~90%는 오픈소스 컴포넌트로 구성된다. 직접 설치한 라이브러리뿐 아니라 그것이 끌어오는 하위 의존성(Transitive Dependency)까지 합치면 수백~수천 개에 달한다. Log4Shell(2021) 사태에서 전 세계 기업이 "우리 시스템에 Log4j가 있는가?"라는 질문에 수주간 답하지 못한 것이 SBOM 의무화의 직접적 계기다.

```text
+-------------------------------------------------------+
|              SBOM 추출 파이프라인 흐름도                |
+-------------------------------------------------------+
|  [Source Code]  ->  [Build Engine]  ->  [SBOM Generator]|
|  (pom, npm)       (Maven, npm)      (Syft, Trivy)    |
|                                          |            |
|                         +----------------v----------+ |
|                         | Standard SBOM Format      | |
|                         | - SPDX (ISO 5962:2021)    | |
|                         | - CycloneDX (OWASP)       | |
|                         +------------+--------------+ |
|                                      |                |
|                    +-----------------v----------+     |
|                    | CVE DB 대조 (취약점 스캔)    |     |
|                    | + VEX (악용 가능성 평가)     |     |
|                    | + Sigstore 서명 (무결성)     |     |
|                    +-----------------------------+     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SBOM은 식품 뒷면의 <strong>성분표</strong>다. 나쁜 재료(취약점)가 발견되면 성분표를 보고 우리 과자가 안전한지 즉시 확인한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SBOM 표준 포맷

| 포맷 | 주관 | 특징 | 형식 |
|:---|:---|:---|:---|
| **SPDX** | Linux Foundation (ISO 5962) | 법적 라이선스 추적에 강점 | JSON, RDF, Tag-Value |
| **CycloneDX** | OWASP | 보안 취약점 연계에 강점 | JSON, XML, Protobuf |

### 핵심 구성 요소

| 요소 | 설명 |
|:---|:---|
| **Inventory** | 포함된 모든 컴포넌트(이름·버전·해시) 목록 |
| <strong>Dependency Graph</strong> | 직접·간접 의존성의 트리 구조 |
| **License Info** | 각 컴포넌트의 라이선스 유형 (MIT, GPL 등) |
| **Provenance** | 소스 출처, 빌드 환경, 빌더 정보 |

### 3단 보안 결합

1. <strong>SBOM</strong>: "우리가 뭘 쓰고 있는가?" -> 재고 파악
2. **VEX (Vulnerability Exploitability eXchange)**: "취약하지만 우리 코드에서 실제 실행되는가?" -> 오탐 제거
3. **Sigstore/Cosign**: "이 SBOM은 위조되지 않았는가?" -> 무결성 보증

- **📢 섹션 요약 비유**: SBOM은 재료 목록, VEX는 "이 재료가 진짜 위험한가?" 판단, Sigstore는 목록 자체의 위조 방지 인감이다.

---

## Ⅲ. 비교 및 연결

| 비교 | SAST (정적 분석) | SCA (오픈소스 스캔) | SBOM 추출 |
|:---|:---|:---|:---|
| **분석 대상** | 내가 짠 코드 | 사용 중 라이브러리 CVE | **전체 구성요소 명세** |
| **목적** | 코딩 실수 탐지 | 알려진 취약점 탐지 | <strong>투명성·공급망 관리</strong> |
| **산출물** | 취약점 리포트 | 패치 권고 | <strong>표준 명세서 (JSON)</strong> |
| **상호작용** | - | SBOM을 입력으로 사용 | SCA의 기초 데이터 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 파이프라인 통합 체크리스트
1. <strong>Syft/Trivy</strong>를 CI 빌드 스텝에 추가하여 매 빌드마다 SBOM 자동 생성.
2. **Full Inventory**: 직접 의존성뿐 아니라 Transitive Dependency까지 포함.
3. **서명**: Cosign으로 SBOM에 디지털 서명 부착 -> 배포 시 검증.
4. **저장**: OCI Registry에 SBOM을 컨테이너 이미지와 함께 Attestation으로 첨부.

### 안티패턴
- <strong>빌드 후 수동 생성</strong>: 빌드 환경과 불일치하는 SBOM -> 신뢰도 0.
- <strong>SBOM 생성만 하고 스캔 미연동</strong>: 명세서를 만들어놓고 CVE 대조를 안 하면 의미 없음.

---

## Ⅴ. 기대효과 및 결론

| 지표 | SBOM 미도입 | SBOM 파이프라인 | 개선 |
|:---|:---|:---|:---|
| Log4j 포함 확인 | **수주** (수동 조사) | **수초** (자동 대조) | 99.9% 단축 |
| 라이선스 컴플라이언스 | 사후 감사 | <strong>빌드 시 자동 검증</strong> | 법적 리스크 제거 |
| 공급망 투명성 | 블랙박스 | **완전 가시성** | 고객 신뢰 확보 |

SBOM은 Google SLSA 프레임워크와 결합하여 빌드 전 과정의 무결성을 증명하는 핵심 증거로 진화하고 있으며, 모든 소프트웨어 납품 시 '영양성분표'처럼 SBOM 제출을 요구하는 시대가 도래했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Supply Chain Security</strong> | SBOM이 해결하려는 전체 맥락 |
| **SPDX / CycloneDX** | SBOM 데이터의 표준 포맷 |
| <strong>CVE (Common Vulnerabilities)</strong> | SBOM과 대조하는 취약점 데이터베이스 |
| **VEX** | 취약점의 실제 악용 가능성을 평가하는 보충 문서 |
| **SLSA (Supply-chain Levels)** | 빌드 무결성 보안 등급 체계 |
| **Sigstore / Cosign** | SBOM 및 컨테이너 이미지의 디지털 서명 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Log4Shell 사태 (2021.12) — 공급망 취약점 충격]
    |
    v
[미 행정명령 EO 14028 (2021) — 연방 SW에 SBOM 의무화]
    |
    v
[SPDX ISO 표준화 (2021) — ISO/IEC 5962:2021]
    |
    v
[Sigstore + SLSA (2022~) — 빌드 무결성 + 서명 자동화]
    |
    v
[현재: SBOM + VEX + SLSA 3단 결합이 DevSecOps 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 우리가 먹는 과자 뒤에 어떤 재료가 들어갔는지 적힌 <strong>성분표</strong>를 본 적 있니?
2. SBOM은 컴퓨터 프로그램에 어떤 재료(라이브러리)가 들어갔는지 꼼꼼히 적어둔 명세서야.
3. 나쁜 재료(취약점)가 발견되면 이 명세서를 보고 우리 프로그램이 안전한지 바로 확인할 수 있단다!
