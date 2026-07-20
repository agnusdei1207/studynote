---
title: "Kubernetes Container Image Security Scanning"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 116
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 이미지 보안 스캐닝은 Docker/OCI 이미지의 <strong>OS 패키지·언어 라이브러리에 포함된 알려진 취약점(CVE)</strong>을 자동으로 탐지하고, SBOM(Software Bill of Materials)을 생성하여 공급망 보안을 확보하는 프로세스다.
> 2. **가치**: 프로덕션 컨테이너의 <strong>76%가 High/Critical CVE</strong>를 포함하고 있으며(Sysdig 2024 보고서), 빌드 시점(Shift Left)에서 스캔하여 취약 이미지의 배포를 차단해야 한다.
> 3. **판단 포인트**: Trivy(OSS, 빠름)·Snyk(개발자 친화)·Grype(SBOM 통합)가 대표 도구이며, K8s Admission Controller와 연동하여 <strong>스캔 미통과 이미지의 배포를 자동 거부</strong>하는 정책 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    이미지 보안 스캐닝 파이프라인                       |
+-------------------------------------------------------+
|  1. 개발자: Dockerfile -> docker build                 |
|  2. CI: Trivy 스캔 -> CVE 탐지                        |
|     HIGH: 3개, CRITICAL: 1개 -> ❌ 빌드 실패          |
|  3. 수정: base image 업데이트, 라이브러리 패치        |
|  4. 재스캔 -> CVE 0개 -> ✅ 레지스트리 Push            |
|  5. K8s: Admission Controller -> 스캔 미통과 이미지   |
|     배포 자동 거부                                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 이미지 스캐닝은 공항 수하물 X-ray다. 위험물(CVE)이 발견되면 비행기(프로덕션)에 못 태운다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 도구 비교

| 도구 | 유형 | 특징 | SBOM |
|:---|:---|:---|:---|
| **Trivy** | OSS | 빠름, All-in-one | ✅ |
| **Grype** | OSS | Syft SBOM 연동 | ✅ |
| **Snyk** | SaaS | 개발자 IDE 통합 | ✅ |
| <strong>Docker Scout</strong> | SaaS | Docker Hub 내장 | ✅ |

### SBOM (Software Bill of Materials)
이미지 내 모든 패키지·버전을 <strong>재료 목록</strong>으로 생성 -> CVE 매칭·라이선스 감사에 활용.

- **📢 섹션 요약 비유**: SBOM은 식품 성분표이다. "이 컨테이너에 openssl 1.1.1이 들어있다"를 알아야 취약점 알림 시 영향 범위를 즉시 파악한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 스캔 없음 | CI 스캔 | CI + Admission |
|:---|:---|:---|:---|
| **배포 차단** | ✗ | 빌드만 | **빌드+배포** |
| **취약 이미지** | 프로덕션 진입 | 빌드 실패 | **완전 차단** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Shift Left 전략
- **IDE**: Snyk 플러그인으로 코딩 시점 CVE 감지.
- <strong>CI</strong>: Trivy를 GitHub Actions에 통합, Critical CVE 시 빌드 실패.
- <strong>Registry</strong>: Harbor 내장 스캐너로 Push 시 자동 스캔.
- **Runtime**: Falco로 실행 중 이상 행위 탐지.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 스캔 미도입 | 스캔 도입 | 개선 |
|:---|:---|:---|:---|
| 취약 이미지 배포 | 76% | <strong>0% (정책 적용)</strong> | 완전 차단 |
| CVE 패치 시간 | 발견 후 수일 | **빌드 시점 즉시** | Shift Left |
| SBOM 가시성 | 없음 | **전체 재료 목록** | 공급망 보안 |

컨테이너 이미지 보안은 SBOM 의무화(미국 행정명령 14028)와 함께 소프트웨어 공급망 보안의 핵심 요소로 부상하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>CVE</strong> | 알려진 취약점 데이터베이스 |
| <strong>SBOM</strong> | 이미지 내 패키지 재료 목록 |
| **Trivy** | 대표 OSS 이미지 스캐너 |
| **Admission Controller** | K8s 배포 시점 정책 적용 |
| <strong>소프트웨어 공급망 보안</strong> | 이미지 스캐닝이 속하는 상위 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 취약점 관리 (2010s)]
    |
    v
[Clair / Anchore (2016~) — 초기 이미지 스캐너]
    |
    v
[Trivy / Snyk (2019~) — All-in-one, 개발자 친화]
    |
    v
[SBOM 의무화 (2021, 미국 행정명령 14028)]
    |
    v
[현재: CI + Registry + Admission 전 구간 스캐닝]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 컨테이너 이미지는 <strong>도시락 상자</strong>예요. 안에 뭐가 들었는지 확인해야 해요.
2. 보안 스캐닝은 도시락을 <strong>X-ray로 검사</strong>해서 상한 음식(취약점)이 있으면 학교에 못 가져가게 해요.
3. SBOM은 <strong>성분표</strong>처럼 "이 도시락에 뭐가 들었는지" 목록을 만들어서 문제가 생기면 빠르게 찾아요!
