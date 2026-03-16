+++
title = "Fast Recovery - 빠른 복구"
weight = 503
+++

# Fast Recovery - 빠른 복구

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Slow Start 없이 복구
> 2. **가치**: 빠른 처리량 회복
> 3. **융합:** TCP Reno, Fast Retransmit

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Fast Recovery는 Slow Start 없이 복구합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Fast Recovery                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              Fast Recovery 동작                                │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  1. 3 DupACK 감지                                    │   │ │
│   │   │  2. ssthresh = cwnd / 2                             │   │ │
│   │   │  3. cwnd = ssthresh + 3                             │   │ │
│   │   │  4. 재전송                                          │   │ │
│   │   │  5. DupACK마다 cwnd++                               │   │ │
│   │   │  6. ACK 수신 시 cwnd = ssthresh                     │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Fast Recovery는 Congestion Avoidance로 진입합니다.

**📢 섹션 요약 비유:** Fast Recovery = 빠른 정상화!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **cwnd** | Congestion Window |
| **ssthresh** | Slow Start Threshold |
| **DupACK** | 중복 ACK |
| **New ACK** | 새로운 ACK |

**핵심 알고리즸:** 윈도우 조정

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**TCP Tahoe vs Reno**

| 항목 | Tahoe | Reno |
|:---|:---|:---|
| **손실** | Slow Start | Fast Recovery |
| **복구** | 느림 | 빠름 |
| **버전** | 구형 | 현대 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 단일 손실 → Fast Recovery
**시나리오 2:** 다중 손실 → Timeout
**시나리오 3:** 고속망 → NewReno

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** RFC 2581, RFC 5681

---

### 📌 관련 개념 링크**:
- [Fast Retransmit](./502_fast_retransmit.md)
- [TCP](./332_tcp.md)
- [Slow Start](./504_slow_start.md)
