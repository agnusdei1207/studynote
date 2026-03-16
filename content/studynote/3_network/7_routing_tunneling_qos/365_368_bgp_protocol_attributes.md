+++
title = "365-368. BGP(Border Gateway Protocol) 분석"
description = "AS 간의 통신을 책임지는 인터넷의 유일한 외부 라우팅 프로토콜 BGP의 경로 벡터 방식과 주요 속성 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 365
+++

# 365-368. BGP(Border Gateway Protocol) 분석

> **핵심 인사이트**: BGP는 세상에서 가장 느리고 보수적인 라우팅 프로토콜이다. 단순히 '빠른 길'을 찾는 게 목적이 아니라, 나라와 나라(AS) 사이의 정치적, 경제적 관계에 따라 '허용된 길'을 찾는 외교관 역할을 하며, 이를 위해 수많은 '속성(Attribute)' 값을 활용한다.

---

## Ⅰ. BGP 개요
TCP 포트 **179**번을 사용하는 신뢰성 기반의 **경로 벡터 (Path-Vector)** 라우팅 프로토콜입니다.

* **목적**: 전 세계 수만 개의 AS(자율 시스템)들을 연결하여 거대한 인터넷을 구성합니다.
* **특징**: 수렴 속도가 매우 느리지만(수분 이상), 수십만 개의 경로 정보를 안정적으로 관리할 수 있습니다. 
* **구분**:
  - **eBGP (Exterior BGP)**: 서로 다른 AS 간의 연결.
  - **iBGP (Interior BGP)**: 동일한 AS 내부의 BGP 라우터 간 연결. (루프 방지를 위해 Split Horizon 룰 적용)

---

## Ⅱ. BGP 경로 결정의 열쇠: 속성 (Attributes)
BGP는 메트릭 점수가 하나가 아닙니다. 여러 가지 '속성'들을 순차적으로 따져서 최적의 길을 결정합니다.

1. **Weight (Cisco 전용)**: 내가 설정한 내 라우터 내에서의 우선순위 (가장 먼저 따짐).
2. **Local Preference**: 우리 AS 내부에서 "이쪽 출구로 나가라"고 정한 값.
3. **AS_PATH**: 거쳐 가야 할 AS의 목록. **목록이 짧을수록(거리가 가까울수록)** 선호합니다. (루프 방지용으로도 쓰임)
4. **Origin**: 경로 정보를 어디서 처음 배웠는가? (IGP > EGP > Incomplete)
5. **MED (Multi-Discriminator)**: 외부 AS에게 "우리 AS로 들어올 때 이쪽 문으로 들어와"라고 제안하는 값 (낮을수록 선호).

---

## Ⅲ. BGP의 주요 용어 및 기술

### 1. BGP Neighbor (Peer)
OSPF처럼 Hello 패킷을 뿌려 자동으로 찾는 게 아니라, **관리자가 수동으로 상대방 IP를 지정**하여 1:1로 신뢰 관계를 맺어야 합니다.

### 2. Full-mesh 문제와 해결책
iBGP에서는 루프 방지를 위해 "iBGP로 배운 정보는 다른 iBGP에게 전달하지 않는다"는 규칙이 있습니다. 이 때문에 모든 라우터를 1:1로 다 연결해야 하는 부하가 생깁니다.
* **Route Reflector (RR)**: 특정 라우터를 '반장'으로 정해, 반장이 정보를 대신 전달(Reflect)하게 하여 연결 개수를 줄입니다.
* **Confederation**: 거대한 AS를 작은 가짜 AS들로 쪼개어 관리하는 방식입니다.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[BGP 속성 기반 경로 선택 순서]

1. Weight (Highest)
2. Local Preference (Highest)
3. Self-Originated (Local)
4. AS_PATH (Shortest) <── 인터넷 경로의 핵심 기준!
5. Origin Code (Lowest)
6. MED (Lowest)
7. eBGP over iBGP
... (등등 10단계가 넘음)
```

📢 **섹션 요약 비유**: **BGP**는 국경을 넘나드는 '국제 무역 물류망'입니다. 단순히 거리가 가깝다고 물건을 보내지 않습니다. "그 나라는 통행료가 비싸(MED)", "우리 정부는 이쪽 항구를 쓰기로 했어(Local Pref)", "거기는 전쟁 중이라 통과하면 안 돼(Policy)" 같은 복잡한 비즈니스 룰을 따집니다. **AS_PATH**는 여권에 찍힌 입국 도장 목록과 같아서, 내 도장이 찍힌 패킷이 다시 돌아오면 "어? 이거 뺑뺑이 돌고 있네?" 하고 즉시 폐기하는 루프 방지 장치로도 쓰입니다.
