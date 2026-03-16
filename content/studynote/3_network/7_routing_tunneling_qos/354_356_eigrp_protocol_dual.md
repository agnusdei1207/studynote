+++
title = "354-356. EIGRP(Enhanced IGRP) 프로토콜 분석"
description = "Cisco 독자적인 고급 거리 벡터 프로토콜인 EIGRP의 특징과 DUAL 알고리즘 및 용어 정리"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 354
+++

# 354-356. EIGRP(Enhanced IGRP) 프로토콜 분석

> **핵심 인사이트**: EIGRP는 거리 벡터의 단순함과 링크 상태의 빠른 속도를 결합한 '하이브리드'형 프로토콜이다. 전체 지도를 그리지는 않지만, DUAL 알고리즘을 통해 루프 없는 최적 경로와 우회 경로(Feasible Successor)를 미리 계산해두어 사고 시 즉각 대응한다.

---

## Ⅰ. EIGRP (Enhanced Interior Gateway Routing Protocol) 개요
시스코(Cisco)에서 독자적으로 개발한 프로토콜로, 현재는 일부 개방되었으나 여전히 시스코 장비 중심의 환경에서 강력한 성능을 발휘합니다.

* **방식**: **고급 거리 벡터 (Advanced Distance Vector)** 또는 하이브리드 방식.
* **알고리즘**: **DUAL (Diffusing Update Algorithm)** 을 사용하여 무한 루프를 원천 차단합니다.
* **메트릭 (Metric)**: **복합 메트릭 (Composite Metric)**
  - 대역폭(Bandwidth), 지연(Delay), 신뢰성(Reliability), 부하(Load), MTU 5가지를 조합합니다. (기본적으로는 **대역폭과 지연**만 사용)

---

## Ⅱ. EIGRP의 3가지 핵심 테이블
스마트한 경로 관리를 위해 3단계의 데이터베이스를 유지합니다.

1. **Neighbor Table (이웃 테이블)**: Hello 패킷을 통해 인사를 나눈 인접 라우터들의 목록입니다.
2. **Topology Table (토폴로지 테이블)**: 이웃들로부터 받은 **모든** 라우팅 정보가 담겨있습니다. (최적 경로 + 예비 경로)
3. **Routing Table (라우팅 테이블)**: 토폴로지 테이블 중 가장 좋은 길(최적 경로)만 골라 실제 패킷 전송에 사용하는 최종 명단입니다.

---

## Ⅲ. DUAL 알고리즘의 주요 용어
EIGRP의 빠른 수렴(Convergence) 비결은 '예비 후보'를 미리 뽑아두는 것입니다.

* **Successor (후계자)**: 라우팅 테이블에 등록된 **최적 경로** 라우터입니다.
* **Feasible Successor (잠재적 후계자)**: 최적 경로가 끊어질 경우를 대비한 **예비 경로** 라우터입니다. 루프가 생기지 않는다는 것이 증명된 경로만 이 자격을 얻습니다.
* **FD (Feasible Distance)**: 내 라우터에서 목적지까지 가는 총 거리 점수입니다.
* **AD (Advertised Distance)**: 이웃 라우터가 "거기까지 가려면 나를 통해 이만큼(AD) 가면 돼"라고 나에게 알려준 점수입니다.

---

## Ⅳ. EIGRP의 독보적 특징

* **빠른 수렴**: Successor가 죽으면 계산 없이 즉시 Feasible Successor를 투입합니다. (Convergence Time $\approx$ 0)
* **부분 업데이트 (Partial Update)**: 변화가 생겼을 때만, 변화된 부분의 정보만 보냅니다. (대역폭 절약)
* **不等비용 로드 밸런싱 (Unequal Cost Load Balancing)**: 메트릭 점수가 달라도 일정한 범위 내에 있다면 여러 길로 트래픽을 동시에 분산해서 보낼 수 있는 유일한 프로토콜입니다.

---

## Ⅴ. 개념 맵 및 요약

```ascii
[EIGRP 테이블 구성도]

 [ Hello ] ──> [ Neighbor Table ] (누구랑 친하니?)
                      │
 [ Update ] ──> [ Topology Table ] (어떤 길들이 있니? - 후보군 전체)
                      │
 [ DUAL Alg ] ─> [ Routing Table ]  (제일 좋은 길이 뭐니? - 1등(Successor))
                      │
                      └───> [ Feasible Successor ] (2등, 예비군 상시 대기)
```

📢 **섹션 요약 비유**: **EIGRP**는 아주 깐깐하고 준비성이 철저한 '엘리트 안내원'입니다. 단순히 거리만 보지 않고 도로 폭(대역폭)과 정체 시간(지연)을 다 따져서 최상의 길을 뽑습니다. 특히 이 안내원은 메인 도로가 공사 중일 때를 대비해 항상 '뒷길(Feasible Successor)'을 미리 지도에 표시해두고, 사고가 나자마자 단 1초의 망설임도 없이 차들을 뒷길로 안내하는 신공을 발휘합니다.
