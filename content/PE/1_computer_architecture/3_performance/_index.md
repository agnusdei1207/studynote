+++
title = "03. 아키텍처 성능 평가 (Performance)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "컴퓨터라는 경주 자동차가 얼마나 빨리 달리는지 '속도계'를 보는 법을 배우는 곳이에요. 어떤 자동차가 더 힘이 세고 기름을 적게 먹는지 과학적으로 비교하는 방법을 공부한답니다!"
+++

# 03. 아키텍처 성능 평가 (Performance)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실행 시간(Execution Time), 처리량(Throughput), 응답 시간(Response Time)의 상관관계 분석을 통한 시스템 효율 측정.
> 2. **가치**: 암달의 법칙(Amdahl's Law)과 MIPS/MFLOPS 지표를 활용한 하드웨어 설계의 투자 대비 성능(ROI) 최적화.
> 3. **융합**: 전력 효율(Performance per Watt) 및 확장성(Scalability) 관점의 분석을 통해 지속 가능한 아키텍처 설계의 기준 제시.

---

### Ⅰ. 개요 (Context & Background)
성능 평가는 아키텍처 설계의 나침반이다. "성능이란 무엇인가?"라는 질문에 대해 객관적인 지표를 제시하고, 특정 하드웨어 개선이 전체 시스템에 미치는 영향을 정량적으로 계산하는 과정이다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 핵심 지표 및 공식
- **CPU Time**: $Instruction Count \times CPI \times Clock Cycle Time$
- **Amdahl's Law**: 시스템의 일부분만 개선했을 때 전체 성능 향상 폭의 한계 규명
- **Benchmarks**: SPEC (Standard Performance Evaluation Corporation)
- **Power Wall**: 전력 소모의 한계가 성능 향상을 가로막는 병목 현상

#### 2. 성능 분석 레이어 (ASCII)
```text
    [ Performance Metrics Layer ]
    
    (System) +--------------------------+
             | Throughput (Jobs/sec)    |  <-- Macro View
             +--------------------------+
             | Response Time (sec)      |  <-- User View
             +--------------------------+
             | Clock Cycles (Hz)        |  <-- Micro View
    (Chip)   +--------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### Amdahl's Law vs Gustafson's Law
| 구분 | 암달의 법칙 (Amdahl) | 구스타프슨의 법칙 (Gustafson) |
| :--- | :--- | :--- |
| **관점** | 고정된 문제 크기 (Fixed workload) | 고정된 시간 (Fixed time) |
| **핵심** | 병렬화할 수 없는 영역이 전체 성능 한계 결정 | 병렬 처리 시 문제 크기를 키워 성능 향량 극대화 |
| **시사점** | 코어 수 증가의 한계 지적 | 빅데이터/병렬 처리에 대한 긍정적 전망 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
현대 데이터센터 설계 시 가장 중요한 것은 단순히 속도(Peak Performance)가 아니라 **TCO(Total Cost of Ownership)**와 **PUE(Power Usage Effectiveness)**다. 기술사는 특정 워크로드(AI vs Web)에 최적화된 하드웨어를 선택할 때 정량적인 벤치마크 데이터를 기반으로 의사결정을 내려야 한다.

---

### Ⅴ. 기대효과 및 결론
성능 평가는 클라우드 네이티브 아키텍처와 서버리스 환경에서 더욱 중요해지고 있다. 하드웨어의 성능을 소프트웨어가 얼마나 투명하게 사용할 수 있는지가 차세대 아키텍처의 핵심 경쟁력이 될 것이다.
