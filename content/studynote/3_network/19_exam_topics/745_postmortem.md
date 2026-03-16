+++
title = "Postmortem - 포스트모템"
weight = 745
+++

# Postmortem - 포스트모템

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 장애 사후 분석
> 2. **가치**: 학습, 재발 방지
> 3. **융합:** Blameless Culture, RCA, Action Items

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Postmortem은 장애 후 분석을 수행합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Postmortem                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              포스트모템 구조                                    │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Incident Summary                                    │   │ │
│   │   │  - Date: 2024-01-15                                 │   │ │
│   │   │  - Duration: 45 minutes                             │   │ │
│   │   │  - Impact: 10% users affected                       │   │ │
│   │   │                                                      │   │ │
│   │   │  Timeline                                            │   │ │
│   │   │  - 14:00 Alert triggered                             │   │ │
│   │   │  - 14:05 Engineer paged                              │   │ │
│   │   │  - 14:20 Root cause identified                       │   │ │
│   │   │  - 14:45 Fix deployed                                │   │ │
│   │   │                                                      │   │ │
│   │   │  Root Cause Analysis (5 Whys)                        │   │ │
│   │   │  - Why 1: Service crashed → DB connection failed     │   │ │
│   │   │  - Why 2: Pool exhausted → Long-running queries      │   │ │
│   │   │  - Why 3: No timeout → Missing configuration         │   │ │
│   │   │                                                      │   │ │
│   │   │  Action Items                                        │   │ │
│   │   │  - [ ] Add query timeout (P1)                        │   │ │
│   │   │  - [ ] Add connection pool monitoring (P2)           │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: 포스트모템은 비난 없이 학습에 집중합니다.

**📢 섹션 요약 비유:** Postmortem = 부검 보고서!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Summary** | 요약 |
| **Timeline** | 타임라인 |
| **RCA** | 근본 원인 분석 |
| **Action Items** | 조치 항목 |
| **Lessons** | 교훈 |

**핵심 알고리즸:** 장애 → 타임라인 → RCA → 조치

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**분석 기법**

| 기법 | 설명 |
|:---|:---|
| **5 Whys** | 5번 왜? |
| **Fishbone** | 이시카와 다이어그램 |
| **Fault Tree** | 결함 트리 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** SEV1/SEV2 → 필수 포스트모템
**시나리오 2:** SEV3/4 → 선택적
**시나리오 3:** Near-miss → 간소화

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** Google SRE Postmortem

---

### 📌 관련 개념 링크**:
- [Incident Management](./742_incident_management.md)
- [Blameless Culture](./746_blameless.md)
- [Error Budget](./741_error_budget.md)
