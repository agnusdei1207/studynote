---
title: "Secret Manager HashiCorp Vault Dynamic Secret TTL Hardcoding Prevention"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 329
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시크릿(Secret)은 API 키, DB 비밀번호, TLS 인증서처럼 노출되면 즉각적인 보안 사고로 이어지는 민감 정보다. 하드코딩이나 환경변수 평문 저장은 Git 이력, 로그, 컨테이너 이미지 등 수십 개 경로로 유출된다.
> 2. **해결 원리**: HashiCorp Vault는 시크릿을 중앙화하고, 동적 시크릿(Dynamic Secret)을 통해 DB 접속 자격증명을 요청마다 TTL (Time-To-Live)이 붙은 임시 자격증명으로 발급한다. 영구 비밀번호 자체가 존재하지 않아 탈취해도 시간이 지나면 무효화된다.
> 3. **판단 포인트**: 정적 시크릿(Static Secret)은 최소화하고 동적 시크릿을 최대화해야 한다. GitGuardian, Gitleaks 같은 Secret Scanning 도구로 CI에서 하드코딩을 사전 차단하는 Shift-Left 접근도 필수다.

---

## Ⅰ. 개요 및 필요성

2022년 Twitch 소스코드 유출 사건, 삼성 소스코드 유출 사건 모두 하드코딩된 자격증명이나 부적절하게 관리된 시크릿이 원인이었다. Git 저장소에 한 번 커밋된 시크릿은 히스토리에서 삭제해도 fork 저장소, 빌드 아티팩트 등에 남아있을 수 있다.

시크릿 관리의 진화 단계:
1. <strong>하드코딩 (Anti-pattern)</strong>: 소스코드에 직접 시크릿 삽입, Git에 노출
2. **환경변수 (개선)**: 평문 환경변수는 컨테이너 인스펙션, 로그에 노출
3. <strong>Secret Manager (권장)</strong>: HashiCorp Vault, AWS Secrets Manager 등 중앙화된 시크릿 저장소

> 📢 **섹션 요약 비유**: 은행 금고(Secret Manager) 없이 지갑(코드)에 현금(시크릿)을 보관하는 것과 같다. 지갑은 잃어버리기 쉽지만 금고는 잠금장치가 있고 접근 기록이 남는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+----------------------------------------------------+
|           HashiCorp Vault 동적 시크릿 흐름           |
+----------------------------------------------------+
|                                                    |
|  애플리케이션 (Pod/Lambda)                           |
|       |  1. Vault에 인증 (AppRole / K8s SA)         |
|       v                                            |
|  +---------------------+                           |
|  |  HashiCorp Vault     |                          |
|  |  - Auth Engine       |                          |
|  |  - Secrets Engine    |                          |
|  |  - Audit Log         |                          |
|  +----------+----------+                           |
|             |  2. 동적 자격증명 발급 (TTL=1h)         |
|             v                                      |
|  +-----------------------+                         |
|  |  PostgreSQL           |                         |
|  |  (임시 계정 자동 생성) |                          |
|  +-----------------------+                         |
|             |  3. TTL 만료 시 자동 삭제              |
|             v                                      |
|  감사 로그 (누가, 언제, 어떤 시크릿 요청했는지)         |
+----------------------------------------------------+
```

| 방식 | 시크릿 수명 | 탈취 시 위험 | 감사 로그 |
|:---|:---|:---|:---|
| 하드코딩 정적 비밀번호 | 영구 | 무제한 침해 | 없음 |
| 환경변수 정적 비밀번호 | 영구 | 무제한 침해 | 없음 |
| Vault 동적 시크릿 | TTL(1h~24h) | TTL 만료 후 무효 | 완전 감사 |

Secret Scanning: GitGuardian, Gitleaks, GitHub Secret Scanning은 커밋에 포함된 시크릿 패턴을 CI 단계에서 감지한다. Pre-commit hook으로 로컬에서도 사전 차단 가능하다.

> 📢 **섹션 요약 비유**: Vault 동적 시크릿은 호텔 키카드다. 체크인 시 발급되고 체크아웃 시 자동 비활성화된다. 누군가 키카드를 복사해도 체크아웃 후에는 열리지 않는다.

---

## Ⅲ. 비교 및 연결

| 항목 | HashiCorp Vault | AWS Secrets Manager | K8s Secret |
|:---|:---|:---|:---|
| 동적 시크릿 | 완전 지원 | DB 자격증명 지원 | 미지원 (정적만) |
| 감사 로그 | 상세 | CloudTrail 연동 | RBAC 로그 |
| 오픈소스 | 코어 오픈소스 | 상용 | 오픈소스 |
| 멀티클라우드 | 지원 | AWS 전용 | K8s 내부 |

Kubernetes Secret의 한계: 기본적으로 Base64 인코딩(암호화 아님)으로 저장된다. External Secrets Operator를 사용해 Vault와 통합하는 것이 권장된다.

> 📢 **섹션 요약 비유**: K8s Secret은 종이 봉투, Vault는 금고다. 봉투는 겉으로는 내용이 안 보이지만 봉투 자체를 열 수 있다. 금고는 열쇠(인증)가 있어야만 열린다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 하드코딩 방지 체크리스트

1. CI 파이프라인에 Secret Scanning(Gitleaks/GitGuardian) 단계가 있는가?
2. Pre-commit hook으로 로컬 커밋 시점에 시크릿을 차단하는가?
3. 모든 시크릿이 Secret Manager에서 관리되고, 소스코드/환경변수에 평문이 없는가?
4. 동적 시크릿을 사용해 영구 자격증명을 최소화했는가?

### Vault 핵심 개념

- **Auth Method**: AppRole(서비스 간), K8s ServiceAccount, LDAP(사람) 인증
- **Secrets 엔진**: KV (Key-Value), Database, PKI (인증서 발급), AWS (IAM 자격증명)
- <strong>Policy</strong>: HCL (HashiCorp Configuration Language) 기반 세밀한 접근 제어

> 📢 **섹션 요약 비유**: 동적 시크릿은 유효기간이 지나면 자동으로 잠기는 자물쇠다. 훔쳐도 시간이 지나면 쓸모없어진다.

---

## Ⅴ. 기대효과 및 결론

시크릿 중앙화 관리로 유출 경로가 단일화되고, 동적 시크릿으로 탈취 시 피해 시간이 제한된다. 감사 로그로 "어느 서비스가 어떤 시크릿을 언제 요청했는지" 추적이 가능해 침해 조사가 용이해진다.

시크릿 관리의 본질은 <strong>최소 권한 원칙의 시간 축 적용</strong>이다. 필요한 순간에만, 최소한으로, 짧은 수명으로 시크릿을 발급하는 것이 목표다.

> 📢 **섹션 요약 비유**: 시크릿 관리는 마스터키 대신 각 방마다 다른 키를 주는 호텔 시스템이다. 키가 하나 분실되어도 모든 방이 위험해지지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HashiCorp Vault | 동적 시크릿, 감사 로그, 중앙 시크릿 관리 |
| Dynamic Secret | TTL 기반 임시 자격증명, DB/Cloud 자격증명 |
| Secret Scanning | GitGuardian, Gitleaks - CI/Pre-commit 하드코딩 탐지 |
| External Secrets Operator | K8s와 Vault 연동 브리지 |
| AppRole Auth | 서비스 간 Vault 인증 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
하드코딩 시대             환경변수 시대             동적 시크릿 시대
------------------   ----------------------   -------------------------
API 키 소스 코드 삽입 -> .env 파일, CI 변수  ->  HashiCorp Vault
Git 유출 사고           컨테이너 인스펙션 위험     동적 시크릿 TTL
수동 로테이션           수동 로테이션              자동 로테이션/폐기
                                               Secret Scanning CI
```

### 👶 어린이를 위한 3줄 비유 설명

1. 시크릿(비밀번호)을 코드에 적어두는 건 집 열쇠를 현관문에 붙여두는 거예요.
2. Vault는 열쇠를 금고에 보관하고, 필요할 때만 잠깐 빌려주는 시스템이에요.
3. 빌려준 열쇠는 시간이 지나면 저절로 못 쓰게 되니까, 누군가 열쇠를 훔쳐도 곧 쓸모없어져요.
