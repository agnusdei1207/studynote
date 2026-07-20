---
title: "Sli Service Level Indicator"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 122
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLI(Service Level Indicator)는 <strong>사용자 경험 관점에서 서비스 품질을 정량적으로 측정</strong>하는 지표이며, "좋은 이벤트 수 / 전체 이벤트 수"의 <strong>비율(0~100%)</strong>로 표현된다.
> 2. **가치**: "서비스가 잘 돌아가고 있다"를 주관이 아닌 <strong>데이터로 판단</strong>할 수 있으며, SLI->SLO(목표)->Error Budget(허용 범위)->SLA(계약)의 계층적 신뢰성 관리 체계의 출발점이다.
> 3. **판단 포인트**: 가용성(성공 요청/전체)·레이턴시(p99 < 200ms 요청/전체)·에러율(5xx 에러/전체)이 3대 SLI이며, <strong>사용자에게 의미 있는 지표</strong>를 선택하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    SLI 계산 예시                                      |
+-------------------------------------------------------+
|  [가용성 SLI]                                         |
|   성공 요청: 99,950건 / 전체: 100,000건              |
|   -> SLI = 99.95%                                     |
|                                                       |
|  [레이턴시 SLI]                                       |
|   p99 < 200ms 요청: 99,700건 / 전체: 100,000건      |
|   -> SLI = 99.7%                                      |
|                                                       |
|  SLO: SLI ≥ 99.9% (목표)                             |
|  Error Budget: 100% - 99.9% = 0.1%                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SLI는 학생의 <strong>시험 점수</strong>이고, SLO는 <strong>학습 기준(90점 이상)</strong>이며, Error Budget은 <strong>틀려도 되는 문제 수</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 SLI

| SLI | 측정 | 공식 |
|:---|:---|:---|
| <strong>가용성</strong> | 성공 요청 비율 | 성공/전체 × 100% |
| **레이턴시** | 기준 이내 요청 비율 | (p99 < 200ms)/전체 |
| **에러율** | 에러 미발생 비율 | (1 - 5xx/전체) × 100% |

### SLI 선택 원칙
- **사용자 관점**: 서버 CPU 사용률은 SLI가 아니다. 사용자가 느끼는 <strong>응답 속도·에러</strong>가 SLI다.
- **비율**: 항상 0~100%로 표현하여 SLO와 비교 가능.

- **📢 섹션 요약 비유**: CPU 사용률은 엔진 RPM이고, SLI는 승객이 느끼는 <strong>차량 속도</strong>이다. 승객에게 중요한 건 RPM이 아니라 속도이다.

---

## Ⅲ. 비교 및 연결

| 비교 | SLI | SLO | SLA |
|:---|:---|:---|:---|
| **정의** | 측정 지표 | <strong>목표 임계치</strong> | 계약 |
| **주체** | 엔지니어 | 팀 합의 | **고객 계약** |
| **예** | 99.95% | ≥ 99.9% | 위반 시 크레딧 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### SLI 측정 도구
- <strong>Prometheus + Grafana</strong>: SLI 대시보드.
- <strong>Datadog SLO</strong>: 자동 SLI 추적·알림.
- **OpenSLO**: SLI/SLO를 YAML로 정의하는 표준.

---

## Ⅴ. 기대효과 및 결론

SLI는 <strong>SRE의 모든 판단의 출발점</strong>이며, 올바른 SLI 선택이 SLO·Error Budget·운영 의사결정의 품질을 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>SLI</strong> | 서비스 수준 측정 (비율) |
| <strong>SLO</strong> | SLI의 목표 임계치 |
| <strong>Error Budget</strong> | 100% - SLO |
| <strong>SLA</strong> | SLO 기반 고객 계약 |
| **OpenSLO** | SLI/SLO YAML 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[가용성 99.999% 목표 (전통 운영)]
    |
    v
[SRE (Google, 2003~) — SLI/SLO/Error Budget 정의]
    |
    v
[Prometheus + Grafana SLI 대시보드 (2016~)]
    |
    v
[OpenSLO 표준 (2022~) — SLI/SLO YAML 정의]
    |
    v
[현재: AI SLI — 이상 탐지 기반 자동 SLI 추천]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SLI는 학교 <strong>시험 점수</strong>예요. "우리 서비스가 몇 점인지" 알 수 있어요.
2. SLO는 <strong>학습 기준(90점)</strong>이에요. 점수가 기준 이하면 <strong>공부(안정화)에 집중</strong>해야 해요.
3. 중요한 건 **학생(사용자)이 느끼는** 점수이지, 선생님(서버) 기분이 아니에요!
