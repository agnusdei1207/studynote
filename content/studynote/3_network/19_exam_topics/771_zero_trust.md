+++
title = "Zero Trust - 제로 트러스트"
weight = 771
+++

# Zero Trust - 제로 트러스트

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 신뢰하지 않고 검증
> 2. **가치**: 내부 위협 방지
> 3. **융합:** MFA, Microsegmentation, Least Privilege

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Zero Trust는 모든 접근을 검증합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Zero Trust                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              Zero Trust 원칙                                   │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  기존 보안 (Perimeter-based):                         │   │ │
│   │   │  "내부는 안전, 외부는 위험"                            │   │ │
│   │   │                                                      │   │ │
│   │   │  Zero Trust:                                          │   │ │
│   │   │  "모든 곳이 위험, 항상 검증"                            │   │ │
│   │   │                                                      │   │ │
│   │   │  핵심 원칙:                                            │   │ │
│   │   │  1. Never Trust, Always Verify                       │   │ │
│   │   │  2. Least Privilege Access                            │   │ │
│   │   │  3. Assume Breach                                     │   │ │
│   │   │  4. Microsegmentation                                 │   │ │
│   │   │  5. Continuous Monitoring                             │   │ │
│   │   │                                                      │   │ │
│   │   │  구현:                                                │   │ │
│   │   │  - Identity-based access                              │   │ │
│   │   │  - Device health check                                │   │ │
│   │   │  - Context-aware policies                             │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Zero Trust는 신뢰 경계를 없애고 항상 검증합니다.

**📢 섹션 요약 비유:** Zero Trust = 공항 보안!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Identity** | 신원 |
| **Device** | 장치 |
| **Network** | 네트워크 |
| **Application** | 애플리케이션 |
| **Data** | 데이터 |

**핵심 알고리즸:** 요청 → 신원/장치/컨텍스트 검증 → 접근

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Zero Trust 구성요소**

| 구성요소 | 기술 |
|:---|:---|
| **Identity** | MFA, SSO |
| **Device** | MDM, EDR |
| **Network** | ZTNA, SASE |
| **Policy** | ABAC, RBAC |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 원격 근무 → ZTNA
**시나리오 2:** 클라우드 → SASE
**시나리오 3:** 레거시 → 점진적 도입

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** NIST SP 800-207

---

### 📌 관련 개념 링크**:
- [MFA](./770_mfa.md)
- [Network Security](./xxx_network_security.md)
- [Access Control](./xxx_access_control.md)
