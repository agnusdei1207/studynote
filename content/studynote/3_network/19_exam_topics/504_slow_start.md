+++
title = "Slow Start - 느린 시작"
weight = 504
+++

# Slow Start - 느린 시작

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지수적 윈도우 증가
> 2. **가치**: 혼잡 탐지, 대역폭 탐색
> 3. **융합:** TCP, AIMD, ssthresh

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Slow Start는 윈도우를 지수적으로 증가시킵니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Slow Start                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              Slow Start 동작                                   │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  RTT 1: cwnd = 1  (1 MSS 전송)                      │   │ │
│   │   │  RTT 2: cwnd = 2  (2 MSS 전송)                      │   │ │
│   │   │  RTT 3: cwnd = 4  (4 MSS 전송)                      │   │ │
│   │   │  RTT 4: cwnd = 8  (8 MSS 전송)                      │   │ │
│   │   │  ...                                                 │   │ │
│   │   │  cwnd ≥ ssthresh → Congestion Avoidance              │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Slow Start는 지수적 증가로 빠르게 대역폭을 탐색합니다.

**📢 섹션 요약 비유:** Slow Start = 지수 증가!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **cwnd** | Congestion Window |
| **ssthresh** | Slow Start Threshold |
| **IW** | Initial Window |
| **MSS** | Maximum Segment Size |

**핵심 알고리즸:** cwnd *= 2 per RTT

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Slow Start vs Congestion Avoidance**

| 항목 | Slow Start | CA |
|:---|:---|:---|
| **증가** | 지수 | 선형 |
| **속도** | 빠름 | 느림 |
| **조건** | cwnd < ssthresh | cwnd ≥ ssthresh |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 연결 시작 → Slow Start
**시나리오 2:** Timeout → Slow Start
**시나리오 3:** Fast Recovery → CA

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** RFC 2581, RFC 5681

---

### 📌 관련 개념 링크**:
- [TCP](./332_tcp.md)
- [Fast Recovery](./503_fast_recovery.md)
- [AIMD](./505_aimd.md)
