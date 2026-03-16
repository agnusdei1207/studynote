+++
title = "ICMP Code - ICMP 코드"
weight = 976
+++

# ICMP Code - ICMP 코드

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ICMP 세부 원인
> 2. **가치**: 정확한 오류 진단
> 3. **융합:** Destination Unreachable, Time Exceeded

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

ICMP Code는 ICMP Type의 세부 원인을 나타냅니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ICMP Code                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              ICMP Code 상세                                     │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Type 3 (Destination Unreachable) Codes:               │   │ │
│   │   │  ┌─────────────────────────────────────────────────┐│   │ │
│   │   │  │                                                 ││   │ │
│   │   │  │  Code 0: Network Unreachable                    ││   │ │
│   │   │  │  Code 1: Host Unreachable                       ││   │ │
│   │   │  │  Code 2: Protocol Unreachable                   ││   │ │
│   │   │  │  Code 3: Port Unreachable                       ││   │ │
│   │   │  │  Code 4: Fragmentation Needed                   ││   │ │
│   │   │  │  Code 5: Source Route Failed                    ││   │ │
│   │   │  │  Code 6: Network Unknown                        ││   │ │
│   │   │  │  Code 7: Host Unknown                           ││   │ │
│   │   │  │  Code 9: Network Prohibited                     ││   │ │
│   │   │  │  Code 10: Host Prohibited                       ││   │ │
│   │   │  │  Code 11: TOS Network Unreachable               ││   │ │
│   │   │  │  Code 12: TOS Host Unreachable                  ││   │ │
│   │   │  │  Code 13: Communication Prohibited              ││   │ │
│   │   │  │                                                 ││   │ │
│   │   │  └─────────────────────────────────────────────────┘│   │ │
│   │   │                                                      │   │ │
│   │   │  Type 11 (Time Exceeded) Codes:                        │   │ │
│   │   │  Code 0: TTL Exceeded in Transit                      │   │ │
│   │   │  Code 1: Fragment Reassembly Time Exceeded            │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └────────────────────────────────────────ational──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: ICMP Code는 오류의 구체적 원인을 제공합니다.

**📢 섹션 요약 비유:** ICMP Code = 에러 코드!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Network** | 네트워크 도달 불가 |
| **Host** | 호스트 도달 불가 |
| **Port** | 포트 도달 불가 |
| **TTL** | TTL 초과 |
| **Fragment** | 단편화 필요 |

**핵심 알고리듬:** 오류 → Type/Code 매핑 → 메시지 전송

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**자주 발생하는 Code**

| Type | Code | 의미 |
|:---|:---|:---|
| **3** | 1 | 호스트 도달 불가 |
| **3** | 3 | 포트 도달 불가 |
| **3** | 4 | 단편화 필요 |
| **11** | 0 | TTL 초과 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** Ping 실패 → Type 3 Code 1
**시나리오 2:** 방화벽 차단 → Type 3 Code 13
**시나리오 3:** MTU 문제 → Type 3 Code 4

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** RFC 792 (ICMP)

---

### 📌 관련 개념 링크**:
- [ICMP](./888_icmp.md)
- [ICMP Type](./975_icmp_type.md)
- [Ping](./889_ping.md)
