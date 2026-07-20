---
title: "SAST DAST IAST Security Testing Pipeline"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 326
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAST (Static Application Security Testing)는 코드를 실행하지 않고 소스코드를 분석해 취약점을 찾고, DAST (Dynamic Application Security Testing)는 실행 중인 애플리케이션에 공격을 시뮬레이션한다. IAST (Interactive Application Security Testing)는 두 방식을 결합해 런타임에 내부에서 모니터링한다.
> 2. <strong>파이프라인 배치</strong>: SAST는 코딩 단계(PR 리뷰 시), DAST는 스테이징 환경 배포 후, IAST는 통합 테스트 실행 시에 배치한다. 각각 다른 유형의 취약점을 찾으므로 상호 보완적이다.
> 3. **판단 포인트**: SAST의 최대 문제는 False Positive(오탐) 비율이 높다는 것이다. SAST 결과를 그대로 All-Block하면 개발팀이 경고를 무시하게 된다. 위험도 기반 필터링과 컨텍스트 인식 분석이 필요하다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 취약점의 대부분은 코딩 실수(SQL Injection, XSS, 버퍼 오버플로)에서 시작된다. 이 취약점들은 개발 단계에서 자동 도구로 잡을 수 있음에도, 전통적으로 운영 환경에서 침투 테스터나 실제 공격자에 의해 발견되는 경우가 많았다.

SAST/DAST/IAST는 이 취약점들을 개발 파이프라인 내에서 자동으로 찾는 도구들이다. OWASP (Open Web Application Security Project) Top 10 취약점 대부분이 이 도구들로 탐지 가능하다.

> 📢 **섹션 요약 비유**: SAST는 건물 도면의 구조적 결함을 찾고, DAST는 완성된 건물을 실제로 흔들어보는 내진 테스트다. IAST는 건물 내부 센서가 실시간으로 구조 이상을 감지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+----------------------------------------------------------------+
|              SAST / DAST / IAST 파이프라인 배치                  |
+----------------------------------------------------------------+
|                                                                |
|  [코드 커밋]--->[SAST]--->[빌드]--->[단위테스트]--->[스테이징 배포]|
|       |          |                                    |        |
|      PR 생성    정적 분석                         [DAST]       |
|                소스코드에서                      [IAST]        |
|                SQL Injection                  동적 공격        |
|                XSS 패턴 탐지                   시뮬레이션       |
|                하드코딩 시크릿                  런타임 내부      |
|                                                모니터링         |
+----------------------------------------------------------------+
```

| 항목 | SAST | DAST | IAST |
|:---|:---|:---|:---|
| 분석 대상 | 소스코드 (정적) | 실행 중 앱 (동적) | 런타임 내부 (하이브리드) |
| 실행 시점 | 빌드 전 | 스테이징 후 | 통합 테스트 중 |
| 언어 의존 | 언어별 분석기 필요 | 언어 무관 | 에이전트 언어 지원 |
| False Positive | 높음 | 낮음 | 낮음 |
| False Negative | 낮음 (코드 전수 분석) | 높음 (공격 경로 제한) | 중간 |
| 대표 도구 | SonarQube, Semgrep, Checkmarx | OWASP ZAP, Burp Suite | Contrast Security |

> 📢 **섹션 요약 비유**: SAST는 책의 오탈자를 편집자가 읽으면서 찾는 것이고, DAST는 독자가 실제 읽다가 오탈자를 발견하는 것이며, IAST는 책 내부에 센서가 있어 읽는 순간 오탈자를 알려주는 것이다.

---

## Ⅲ. 비교 및 연결

SAST 주요 탐지 취약점:
- <strong>SQL Injection</strong>: 사용자 입력이 직접 SQL 쿼리에 삽입되는 패턴
- <strong>XSS (Cross-Site Scripting)</strong>: 사용자 입력이 HTML에 직접 출력되는 패턴
- <strong>하드코딩된 시크릿</strong>: API 키, 비밀번호가 코드에 직접 기재
- <strong>취약한 암호화 알고리즘</strong>: MD5, SHA-1 사용

DAST 주요 탐지:
- <strong>인증 우회</strong>: 세션 관리 취약점
- <strong>API 엔드포인트 취약점</strong>: 숨겨진 파라미터, 인가 누락
- <strong>서버 설정 오류</strong>: 디버그 모드, 불필요한 HTTP 메서드 허용

> 📢 **섹션 요약 비유**: SAST와 DAST는 서로 다른 안경을 쓰고 보는 것이다. SAST는 설계 안경으로 코드의 패턴을 보고, DAST는 공격자 안경으로 실제 동작을 본다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### SAST False Positive 관리

1. **룰 튜닝**: 프로젝트 특성에 맞게 규칙 비활성화/조정
2. <strong>컨텍스트 필터</strong>: 테스트 코드, 생성된 코드 제외
3. **위험도 기반 게이트**: Critical/High만 차단, Medium 이하 경고
4. <strong>Baseline 설정</strong>: 기존 이슈 무시, 신규 이슈만 차단

### 도구 선택 기준

- **소규모 프로젝트**: Semgrep (빠름, 커스텀 룰 용이) + OWASP ZAP
- **엔터프라이즈**: SonarQube Enterprise + Checkmarx + Burp Suite Enterprise
- <strong>오픈소스 우선</strong>: Semgrep + OWASP ZAP + Trivy (컨테이너)

> 📢 **섹션 요약 비유**: SAST 룰 튜닝은 화재경보기 민감도 조정이다. 너무 민감하면 요리할 때마다 경보가 울리고, 너무 둔하면 실제 화재를 놓친다.

---

## Ⅴ. 기대효과 및 결론

SAST/DAST/IAST를 CI/CD에 통합하면 OWASP Top 10 취약점의 상당 부분을 운영 이전에 제거할 수 있다. 침투 테스터의 수동 작업 범위가 줄어들고, 실제 0-day와 비즈니스 로직 취약점에 집중할 수 있다.

핵심은 <strong>도구가 개발 속도를 방해하지 않는 것</strong>이다. PR에서 SAST가 30분이 걸린다면 개발자가 우회방법을 찾는다. 5분 내 피드백, 높은 신뢰도의 결과만이 문화로 정착한다.

> 📢 **섹션 요약 비유**: SAST/DAST는 신호등이다. 정확하게 작동하는 신호등은 교통을 안전하게 하지만, 오작동하는 신호등은 교통 혼란을 일으킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| SAST (Static Application Security Testing) | 소스코드 정적 분석, 언어 종속 |
| DAST (Dynamic Application Security Testing) | 실행 중 동적 공격 시뮬레이션 |
| IAST (Interactive Application Security Testing) | 런타임 에이전트 기반 하이브리드 |
| OWASP Top 10 | 웹 애플리케이션 10대 취약점 |
| SonarQube | 오픈소스 SAST 플랫폼 |
| Semgrep | 빠른 커스텀 룰 기반 SAST |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 보안 검수 시대         SAST/DAST 자동화             AI 보안 분석 시대
------------------   --------------------------   -----------------------
수동 코드 리뷰        ->  SAST CI 통합 (SonarQube) ->  AI 기반 취약점 분류
침투 테스터 전담           DAST 스테이징 자동화          Semgrep 커스텀 룰
운영 후 취약점 발견         IAST 하이브리드 접근          CNAPP 내 SAST 통합
                            False Positive 관리           LLM 코드 보안 리뷰
```

### 👶 어린이를 위한 3줄 비유 설명

1. SAST는 글을 쓰고 나서 맞춤법 검사기로 확인하는 거예요. 코드를 실행하지 않아도 실수를 찾을 수 있어요.
2. DAST는 완성된 음식을 직접 먹어보고 맛이 이상한지 확인하는 거예요. 실제로 해보지 않으면 모르는 문제가 있어요.
3. IAST는 음식 재료 안에 센서를 넣어서 요리하면서 자동으로 이상한 점을 알려주는 거예요.
