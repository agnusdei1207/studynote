+++
title = "TCP State Machine - TCP 상태 머신"
weight = 513
+++

# TCP State Machine - TCP 상태 머신

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연결 생명주기 상태
> 2. **가치**: 연결 관리, 문제 진단
> 3. **융합:** Handshake, Close, netstat

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

TCP State Machine은 연결의 상태 전이를 정의합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TCP State Machine                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              상태 전이                                         │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  CLOSED ──SYN──→ SYN_SENT ──SYN+ACK──→ ESTABLISHED  │   │ │
│   │   │                                                      │   │ │
│   │   │  CLOSED ──SYN+ACK──→ SYN_RCVD ──ACK──→ ESTABLISHED  │   │ │
│   │   │                                                      │   │ │
│   │   │  ESTABLISHED ──FIN──→ FIN_WAIT_1                    │   │ │
│   │   │  FIN_WAIT_1 ──ACK──→ FIN_WAIT_2                     │   │ │
│   │   │  FIN_WAIT_2 ──FIN──→ TIME_WAIT                      │   │ │
│   │   │  TIME_WAIT ──2MSL──→ CLOSED                         │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: TCP 연결은 명확한 상태 전이를 따릅니다.

**📢 섹션 요약 비유:** TCP State = 연결의 여정!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 상태 | 설명 |
|:---|:---|
| **CLOSED** | 연결 없음 |
| **LISTEN** | 대기 중 |
| **SYN_SENT** | SYN 전송 |
| **SYN_RCVD** | SYN 수신 |
| **ESTABLISHED** | 연결됨 |
| **FIN_WAIT_1** | FIN 전송 |
| **FIN_WAIT_2** | FIN ACK 수신 |
| **TIME_WAIT** | 종료 대기 |
| **CLOSE_WAIT** | FIN 수신 |
| **LAST_ACK** | 마지막 ACK 대기 |

**핵심 알고리즸:** 이벤트 기반 상태 전이

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Active vs Passive Close**

| 항목 | Active | Passive |
|:---|:---|:---|
| **시작** | FIN 전송 | FIN 수신 |
| **상태** | TIME_WAIT | CLOSE_WAIT |
| **주체** | 클라이언트 | 서버 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** netstat -an | grep ESTABLISHED
**시나리오 2:** TIME_WAIT 많음 → SO_REUSEADDR
**시나리오 3:** CLOSE_WAIT 많음 → 버그 의심

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** RFC 793

---

### 📌 관련 개념 링크**:
- [TCP](./332_tcp.md)
- [TCP Handshake](./333_tcp_handshake.md)
- [TCP Close](./512_tcp_close.md)
