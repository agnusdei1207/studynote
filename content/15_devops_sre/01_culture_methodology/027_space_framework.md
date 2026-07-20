---
title: "Space Framework"
date: "2026-04-29"
tags:
  - "studynote-devops-sre"
weight: 27
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SPACE 프레임워크는 GitHub Research와 Microsoft가 2021년 발표한 개발자 생산성(Developer Productivity) 측정 모델로, Satisfaction & Wellbeing, Performance, Activity, Communication & Collaboration, Efficiency & Flow의 5차원을 통해 생산성을 다면적으로 측정한다.
> 2. **가치**: SPACE 이전에는 커밋 수, PR 수 같은 활동(Activity) 지표만으로 개발자 생산성을 측정했다. 이 접근은 "바쁜 것처럼 보이지만 실제 가치를 안 만드는" 문제를 유발한다. SPACE는 만족도·성과·흐름(Flow) 같은 질적 차원을 포함하여 진정한 생산성을 측정한다.
> 3. **판단 포인트**: DORA 메트릭(배포 주기·변경 리드 타임·CFR·MTTR)이 팀/시스템 수준 성과를 측정한다면, SPACE는 개발자 개인·팀·조직 수준의 다차원 생산성을 측정한다. 두 프레임워크를 함께 사용하면 기술적 성과와 인적 요소를 통합 분석할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
+--------------------------------------------------------+
|              SPACE 5차원 프레임워크                      |
+--------------------------------------------------------+
| S - Satisfaction & Wellbeing  : 직무 만족·번아웃 방지   |
| P - Performance               : 결과물 품질·신뢰성      |
| A - Activity                  : 코드·배포·리뷰 활동     |
| C - Communication & Collaboration : 협업·지식 공유     |
| E - Efficiency & Flow         : 방해 최소화, 집중 시간  |
+--------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SPACE는 운동선수 종합 체력 검진이다. 심폐 지구력(활동량)만 재는 게 아니라 정신 건강(만족도), 시합 결과(성과), 팀 협력(협업), 집중력(흐름) 다섯 가지를 모두 측정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SPACE 5차원 측정 방법

| 차원 | 측정 방법 | 지표 예시 |
|:---|:---|:---|
| **Satisfaction** | 설문 (eNPS, 번아웃 지수) | 직무 만족도 점수 |
| <strong>Performance</strong> | 결과 측정 | 버그율, 코드 리뷰 품질 |
| **Activity** | 시스템 로그 | 일일 커밋 수, PR 머지 수 |
| **Communication** | 협업 도구 분석 | PR 리뷰 응답 시간, 문서화 |
| **Efficiency & Flow** | 시간 추적 | 딥 워크 시간, 컨텍스트 전환 |

### Activity 지표의 함정

```text
❌ 잘못된 사용: 커밋 수 = 생산성
   -> 작은 커밋을 많이 쪼개거나, 불필요한 코드 추가 유발

✅ 올바른 사용: Activity를 다른 4차원과 함께 해석
   -> Activity 높은데 Satisfaction 낮음 -> 번아웃 위험 신호
   -> Activity 낮은데 Performance 높음 -> 효율적 고품질 개발
```

- **📢 섹션 요약 비유**: Activity만 측정하는 건 선생님이 칠판 필기 횟수로 수업 품질을 평가하는 것이다. 칠판을 많이 써도 학생이 이해 못하면(Performance), 선생님이 지쳐있으면(Satisfaction) 좋은 수업이 아니다.

---

## Ⅲ. 비교 및 연결

| 비교 | SPACE | DORA Metrics |
|:---|:---|:---|
| 대상 | 개발자 개인·팀 생산성 | 팀·시스템 배포 성과 |
| 차원 | 5차원 (정성+정량) | 4지표 (정량) |
| 활용 | HR·엔지니어링 리더십 | DevOps 성숙도 |

- **📢 섹션 요약 비유**: SPACE와 DORA는 회사 경영의 두 거울이다. DORA는 재무 성과(매출·이익) 같은 숫자 중심, SPACE는 직원 만족도·문화 같은 사람 중심이다. 두 거울을 동시에 봐야 회사 전체 모습이 보인다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 엔지니어링 리더십 활용
1. **Efficiency & Flow**: 회의 최소화, 딥 워크 보호 시간 블록.
2. **Communication**: PR 리뷰 2일 내 처리 SLA 설정.
3. **Satisfaction**: 분기별 eNPS 조사 -> 번아웃 조기 감지.

### GenAI 도구 도입 효과 측정
- GitHub Copilot 도입 전후 SPACE 비교:
  - Activity: PR 수 25% 증가.
  - Efficiency: 보일러플레이트 코드 시간 40% 감소.
  - Satisfaction: 반복 작업 감소로 만족도 향상.

- **📢 섹션 요약 비유**: GenAI 도입 SPACE 측정은 자동화 설비 투자 ROI 분석이다. 기계(AI)가 단순 작업을 대신하면 직원(개발자) 활동 패턴, 만족도, 성과가 어떻게 변하는지 5차원으로 측정한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **번아웃 예방** | Satisfaction 조기 경고로 개발자 유지 |
| **진정한 생산성** | 활동 수 아닌 결과·흐름 기반 측정 |
| <strong>도구 ROI 검증</strong> | GenAI·DevOps 도구 도입 효과 정량화 |

AI 코딩 어시스턴트(GitHub Copilot, Cursor) 등장으로 SPACE의 Activity·Efficiency 차원이 급격히 변화하면서, "AI와 협력하는 개발자 생산성"을 새롭게 정의하는 SPACE 2.0 논의가 진행 중이다.

- **📢 섹션 요약 비유**: AI 코파일럿 시대의 SPACE는 인간-로봇 협력 팀의 생산성 지표다. 로봇(AI)이 반복 작업을 하면 인간은 창의·의사결정에 집중한다 — 이 새로운 협력의 생산성을 어떻게 측정할 것인가가 핵심 과제다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DORA Metrics</strong> | SPACE와 함께 사용하는 DevOps 성과 지표 |
| <strong>개발자 경험(DevEx)</strong> | SPACE의 실천적 개선 활동 |
| **번아웃** | Satisfaction 차원의 핵심 위험 지표 |
| **딥 워크** | Efficiency & Flow 차원의 핵심 개념 |
| **GitHub Copilot** | SPACE Activity·Efficiency에 영향 주는 AI 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Activity 단일 지표 — 커밋·PR 수 기반 생산성]
    |
    v
[DORA Metrics — 4지표 기반 팀 성과 측정]
    |
    v
[SPACE 프레임워크 — 5차원 개발자 생산성 측정]
    |
    v
[GenAI 도구 통합 SPACE — AI 협력 효과 정량화]
    |
    v
[SPACE 2.0 — AI+인간 협력 생산성 새 정의]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SPACE는 개발자 건강 종합 검진이에요! 만족도, 성과, 활동량, 협업, 집중도 다섯 가지를 동시에 측정해요.
2. 커밋 수(활동)만 재면 바쁜 척하는 개발자가 높은 점수를 받아요 — SPACE는 진짜 실력(성과)과 행복(만족도)도 함께 봐요!
3. AI 코딩 도구(GitHub Copilot)가 활동량을 늘려주면 SPACE 점수가 어떻게 변하는지도 측정할 수 있답니다!
