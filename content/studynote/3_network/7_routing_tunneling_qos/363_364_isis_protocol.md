+++
title = "363-364. IS-IS(Intermediate System to Intermediate System) 프로토콜"
description = "데이터 링크 계층 위에서 동작하는 강력한 링크 상태 프로토콜 IS-IS의 계층 구조와 특징"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 363
+++

# 363-364. IS-IS(Intermediate System to Intermediate System) 프로토콜

> **핵심 인사이트**: IS-IS는 OSPF와 쌍벽을 이루는 링크 상태 프로토콜로, IP가 아닌 OSI 프로토콜(CLNP) 위에서 동작하는 독특한 태생을 가졌다. 덕분에 IP 헤더의 취약점에 영향을 받지 않고 엄청난 수의 라우터를 수용할 수 있어, 전 세계 대형 통신사(ISP)들의 백본망에서 가장 선호하는 프로토콜이다.

---

## Ⅰ. IS-IS 개요
ISO 10589 표준으로 정의된 링크 상태(Link State) 라우팅 프로토콜입니다.

* **태생**: 원래 TCP/IP가 아닌 OSI 모델의 네트워크 계층 프로토콜인 **CLNS/CLNP**를 위해 개발되었습니다. 나중에 IP 라우팅 기능이 추가되어 **Integrated IS-IS**라는 이름으로 현대 인터넷에서 쓰이고 있습니다.
* **계층**: IP 패킷 안에 들어가는 OSPF와 달리, IS-IS는 **데이터 링크 계층(Layer 2) 바로 위**에서 캡슐화되어 동작합니다. (IP가 깨져도 라우팅은 돌아갑니다!)

---

## Ⅱ. IS-IS의 계층적 구조 (Level)
OSPF가 Area 0를 중심으로 쪼개진다면, IS-IS는 라우터의 '레벨'을 기준으로 나뉩니다.

* **Level 1 (L1) 라우터**: 같은 Area 내부에서만 길을 찾는 라우터입니다. (OSPF의 Internal Router와 유사)
* **Level 2 (L2) 라우터**: 서로 다른 Area 사이의 백본 경로를 담당하는 라우터입니다. (OSPF의 Backbone Router와 유사)
* **L1/L2 라우터**: L1과 L2의 기능을 모두 수행하며 Area 간의 징검다리 역할을 합니다. (OSPF의 ABR과 유사)

---

## Ⅲ. IS-IS vs OSPF 차이점

| 구분 | OSPF (Open Shortest Path First) | IS-IS |
| :--- | :--- | :--- |
| **기반 프로토콜** | IP (Protocol 89) | **L2 데이터 링크 (직접 캡슐화)** |
| **Area 구분** | 인터페이스(Port) 단위로 구분 | **라우터 전체**가 하나의 Area에 소속 |
| **용어** | Router, LSA, Hello | **IS** (Intermediate System), **LSP**, **IIH** |
| **확장성** | 보통 수준 (엔터프라이즈 선호) | **매우 높음 (대형 ISP 백본 선호)** |
| **유연성** | 헤더가 고정적임 | TLV(Type-Length-Value) 구조로 새 기능 추가가 쉬움 |

---

## Ⅳ. 개념 맵 및 요약

```ascii
[IS-IS 계층 구조]

      (Area A)                (Area B - Backbone)               (Area C)
   ┌───────────┐            ┌────────────────────┐            ┌───────────┐
   │ [ L1 ] ───┼─── [ L1/L2 ] ─── [ L2 ] ─── [ L1/L2 ] ───┼─── [ L1 ] │
   └───────────┘            └────────────────────┘            └───────────┘
```

📢 **섹션 요약 비유**: **OSPF**가 '윈도우 OS'처럼 대중적이고 인터페이스가 친절한 프로그램이라면, **IS-IS**는 '리눅스 커널'처럼 투박하지만 뼈대부터 튼튼하고 웬만해서는 죽지 않는 시스템입니다. 특히 IS-IS는 IP라는 손님(패킷)을 태우기 전에 도로(L2) 자체가 먼저 닦여있는 구조라, 손님이 소란을 피워도(IP 장애) 도로 상황을 파악하는 데는 아무 문제가 없는 강력한 백본 전용 내비게이션입니다.
