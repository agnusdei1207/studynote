---
title: "Slo Service Level Objective"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 123
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLO는 <strong>SLI(측정 지표)에 대한 목표 임계치</strong>이며, "가용성 SLI ≥ 99.9%"처럼 정의하여 <strong>서비스 신뢰성의 정량적 기준</strong>을 제공한다.
> 2. **가치**: SLO가 없으면 "서비스가 괜찮은가?"에 대한 판단이 주관적이지만, SLO가 있으면 <strong>Error Budget(100%-SLO)이 남았는가?</strong>로 <strong>피처 개발 vs 안정화의 우선순위를 객관적으로</strong> 결정할 수 있다.
> 3. **판단 포인트**: SLO는 100%로 설정하면 안 되며(혁신 불가), <strong>사용자 기대+비즈니스 목표</strong>에 맞춰 설정해야 한다. SLO ≤ SLA(계약)이어야 내부 목표가 계약보다 엄격하다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    SLO -> Error Budget -> 의사결정                     |
+-------------------------------------------------------+
|  SLO = 99.9% (30일 기준)                              |
|  Error Budget = 0.1% = 43.2분/월                     |
|                                                       |
|  [Budget 남음 (장애 10분만 발생)]                     |
|   -> 피처 개발 계속! 카나리 배포 승인!                |
|                                                       |
|  [Budget 소진 (장애 50분 발생)]                       |
|   -> 피처 개발 중단! 안정화·테스트·관측성 개선!       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SLO는 <strong>학습 기준(90점)</strong>이고, Error Budget은 <strong>틀려도 되는 문제 수(10문제)</strong>이다. 10문제 이상 틀리면 보충 수업(안정화)을 받아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SLO 설정 원칙
1. **100% 금지**: 혁신·배포가 불가능해짐.
2. **사용자 기대 기반**: 내부 도구는 99.5%, 결제는 99.99%.
3. **SLO < SLA**: 내부 목표가 계약보다 엄격해야 여유 확보.

### SLI -> SLO -> Error Budget -> SLA 체인

| 단계 | 정의 | 예 |
|:---|:---|:---|
| <strong>SLI</strong> | 측정 | 가용성 99.95% |
| <strong>SLO</strong> | 목표 | ≥ 99.9% |
| <strong>Error Budget</strong> | 여유 | 0.1% (43분) |
| <strong>SLA</strong> | 계약 | ≥ 99.5% (위반 시 크레딧) |

- **📢 섹션 요약 비유**: SLO는 다이어트 목표(70kg 이하), Error Budget은 허용 체중 초과(1kg), SLA는 건강 검진 기준(80kg 이하)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | SLO 없음 | SLO 있음 |
|:---|:---|:---|
| **판단** | 주관적 | <strong>데이터 기반</strong> |
| **개발 속도** | 느림 (공포) | **Budget 내 빠름** |
| **안정화** | 장애 후 사후 | **Budget 소진 시 즉시** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Error Budget 정책 예시
- Budget > 50%: 공격적 배포·실험 허용.
- Budget 10~50%: 카나리·A/B 테스트로 신중 배포.
- Budget < 10%: 피처 동결, 안정화 집중.
- Budget 소진: **배포 중단 (Release Freeze)**.

---

## Ⅴ. 기대효과 및 결론

SLO는 <strong>SRE의 가장 핵심적 의사결정 도구</strong>이며, Error Budget을 통해 엔지니어링 팀과 비즈니스 팀 간의 갈등(속도 vs 안정)을 <strong>데이터로 해결</strong>한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>SLI</strong> | SLO의 측정 기반 |
| <strong>Error Budget</strong> | SLO에서 파생되는 허용 장애 시간 |
| <strong>SLA</strong> | SLO보다 느슨한 고객 계약 |
| **Release Freeze** | Budget 소진 시 배포 중단 |
| **Burn Rate Alert** | Budget 소진 속도 알림 |

### 📈 관련 키워드 및 발전 흐름도

```text
[가용성 99.999% 목표 (전통, ~2010s)]
    |
    v
[SRE SLO 개념 (Google, 2003~2016)]
    |
    v
[Error Budget 기반 의사결정 (Accelerate, 2018)]
    |
    v
[Burn Rate Alert (2020~) — Budget 소진 속도 알림]
    |
    v
[현재: OpenSLO — SLO를 코드로 정의 (SLO as Code)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SLO는 시험 <strong>학습 기준(90점)</strong>이에요. 90점 이상이면 합격!
2. Error Budget은 <strong>틀려도 되는 문제 수(10문제)</strong>예요. 10문제 이상 틀리면 보충 수업!
3. 덕분에 "얼마나 더 실험(피처)해도 되는지" <strong>숫자로 판단</strong>할 수 있답니다!
