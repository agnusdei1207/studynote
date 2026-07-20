---
title: "Error Budget"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 125
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Error Budget은 <strong>SLO에서 파생되는 허용 가능 장애 시간/비율</strong>이며, "100% - SLO"로 계산한다. SLO=99.9%이면 Error Budget=0.1%=**30일 기준 약 43분**.
> 2. **가치**: Error Budget은 <strong>"얼마나 더 위험을 감수(배포·실험)해도 되는가"의 정량적 기준</strong>이다. Budget이 남아있으면 공격적 배포, 소진되면 안정화에 집중하여 <strong>속도와 안정의 갈등을 데이터로 해결</strong>한다.
> 3. **판단 포인트**: Burn Rate(소진 속도) 알림을 설정하여 Budget이 빠르게 소진될 때 조기 경고하고, Budget 소진 시 **Release Freeze(배포 동결)** 정책을 실행한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Error Budget 계산 및 의사결정                      |
+-------------------------------------------------------+
|  SLO = 99.9% (30일 기준)                              |
|  Error Budget = 0.1% = 43.2분                        |
|                                                       |
|  [이번 달 장애 10분 발생]                             |
|   남은 Budget = 33.2분 -> 배포 계속 OK ✅             |
|                                                       |
|  [이번 달 장애 50분 발생]                             |
|   남은 Budget = -6.8분 -> Budget 소진!                |
|   -> Release Freeze! 안정화 집중 🚨                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Error Budget은 <strong>매월 주어지는 용돈(43분)</strong>이다. 장애가 나면 용돈이 줄고, 다 쓰면 <strong>새 장난감(피처) 구매 금지(Release Freeze)</strong>.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Burn Rate Alert

| 소진 속도 | 상황 | 알림 |
|:---|:---|:---|
| **1× (정상)** | 30일에 Budget 소진 | 안전 |
| **2×** | **15일에 소진 예상** | ⚠️ 주의 |
| <strong>10×</strong> | **3일에 소진 예상** | 🚨 긴급 |
| **14.4×** | **1시간에 1% 소진** | 즉시 대응 |

- **📢 섹션 요약 비유**: Burn Rate는 용돈 소비 속도이다. 하루에 10만원씩 쓰면 월급 전에 바닥나므로 경고(Alert)가 필요하다.

---

## Ⅲ. 비교 및 연결

| 비교 | Budget 없음 | Budget 있음 |
|:---|:---|:---|
| **배포** | 공포 (변경 회피) | **Budget 내 자유** |
| **안정화** | 장애 후 사후 | **Budget 소진 시 즉시** |
| **판단** | 주관적 | <strong>데이터 기반</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Error Budget 정책

| Budget 잔량 | 정책 |
|:---|:---|
| **> 50%** | 공격적 배포·실험 허용 |
| <strong>10~50%</strong> | 카나리 배포로 신중하게 |
| **< 10%** | 피처 동결, 안정화 집중 |
| **소진** | **Release Freeze** |

---

## Ⅴ. 기대효과 및 결론

Error Budget은 <strong>SRE의 가장 혁신적 도구</strong>이며, 개발팀(속도)과 운영팀(안정)의 갈등을 <strong>수치로 해결</strong>하는 공통 언어이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Error Budget</strong> | 100% - SLO (허용 장애 시간) |
| **Burn Rate** | Budget 소진 속도 |
| **Release Freeze** | Budget 소진 시 배포 동결 |
| <strong>SLO</strong> | Error Budget의 원천 |
| <strong>Toil</strong> | Budget 소진 시 자동화 투자 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
[100% 가용성 목표 (전통, 비현실적)]
    |
    v
[Error Budget 개념 (Google SRE, 2003~)]
    |
    v
[SRE Book 공개 (2016) — Error Budget 대중화]
    |
    v
[Burn Rate Alert (2020~) — 소진 속도 알림]
    |
    v
[현재: AI Error Budget — 자동 Budget 추천·정책 실행]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Error Budget은 <strong>매달 받는 용돈(43분)</strong>이에요. 장애가 나면 용돈이 줄어요.
2. 용돈이 다 떨어지면 <strong>새 장난감(피처) 금지! 저축(안정화)</strong>에 집중해야 해요.
3. 용돈이 빨리 줄면 <strong>"조심해!"라는 알림(Burn Rate Alert)</strong>이 울려요!
