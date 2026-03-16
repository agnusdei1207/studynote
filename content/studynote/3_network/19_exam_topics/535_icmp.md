+++
title = "ICMP (Internet Control Message Protocol) - 인터넷 제어 메시지 프로토콜"
weight = 535
+++

# ICMP (Internet Control Message Protocol) - 인터넷 제어 메시지 프로토콜

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IP 계층 오류 및 진단 메시지
> 2. **가치**: 네트워크 문제 탐지
> 3. **융합:** ping, traceroute, PMTUD

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

ICMP는 IP 계층의 제어 메시지 프로토콜입니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ICMP                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              ICMP 메시지 유형                                  │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Type 0/8:  Echo Reply/Request (ping)               │   │ │
│   │   │  Type 3:   Destination Unreachable                  │   │ │
│   │   │  Type 4:   Source Quench (deprecated)               │   │ │
│   │   │  Type 5:   Redirect                                 │   │ │
│   │   │  Type 11:  Time Exceeded (TTL=0)                    │   │ │
│   │   │  Type 12:  Parameter Problem                        │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: ICMP는 네트워크 진단과 오류 보고에 사용됩니다.

**📢 섹션 요약 비유:** ICMP = 네트워크 신호등!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| Type | 이름 | 설명 |
|:---|:---|:---|
| **0** | Echo Reply | ping 응답 |
| **3** | Dest Unreachable | 도달 불가 |
| **5** | Redirect | 경로 변경 |
| **8** | Echo Request | ping 요청 |
| **11** | Time Exceeded | TTL 초과 |

**핵심 알고리즸:** 오류 발생 → ICMP 메시지 생성 → 송신자에게 전송

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**ICMP Type 3 Code**

| Code | 설명 |
|:---|:---|
| **0** | Network Unreachable |
| **1** | Host Unreachable |
| **3** | Port Unreachable |
| **4** | Fragmentation Needed (PMTUD) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** ping → Echo Request/Reply
**시나리오 2:** traceroute → Time Exceeded
**시나리오 3:** 방화벽 → ICMP 차단 주의

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** RFC 792

---

### 📌 관련 개념 링크**:
- [IP](./330_ip.md)
- [ping](./536_ping.md)
- [traceroute](./537_traceroute.md)
