+++
title = "357-362. OSPF(Open Shortest Path First) 프로토콜"
description = "대표적인 링크 상태 라우팅 프로토콜인 OSPF의 동작 원리, Area 구조, 그리고 LSA 광고 메커니즘"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 357
+++

# 357-362. OSPF(Open Shortest Path First) 프로토콜

> **핵심 인사이트**: OSPF는 소문에 의존하지 않고 각자가 지도를 그려 길을 찾는 '링크 상태' 프로토콜이다. 모든 라우터가 동일한 지형도(LSDB)를 공유하고 SPF 알고리즘(Dijkstra)으로 최단 거리를 계산하며, Area 단위의 계층적 설계를 통해 대규모 망에서도 효율적인 관리가 가능하다.

---

## Ⅰ. OSPF 개요
IP 헤더의 프로토콜 번호 **89**번을 사용하는 표준 링크 상태(Link State) 프로토콜입니다.

* **메트릭 (Metric)**: **Cost (코스트)**
  - $Cost = \frac{10^8 (100Mbps)}{\text{Interface Bandwidth}}$
  - 즉, 대역폭이 빠를수록 코스트가 낮아져 최적 경로가 됩니다.
* **알고리즘**: **SPF (Shortest Path First)** 또는 **Dijkstra** 알고리즘을 사용하여 루프 없는 최단 경로 트리를 만듭니다.

---

## Ⅱ. OSPF의 계층적 Area 구조
네트워크가 커지면 LSA(광고) 패킷이 너무 많아져 부하가 생깁니다. 이를 방지하기 위해 구역을 나눕니다.

* **Area 0 (Backbone Area)**: 모든 Area의 중심입니다. 다른 Area들은 반드시 Area 0를 거쳐야 통신할 수 있습니다.
* **ABR (Area Border Router)**: 서로 다른 Area 사이에 걸쳐 있는 경계 라우터입니다.
* **ASBR (AS Boundary Router)**: OSPF 망과 외부망(RIP, BGP 등) 사이를 연결하는 라우터입니다.

---

## Ⅲ. 인접성(Adjacency)과 전송 방식

### 1. Neighbor와 Adjacency
* **Neighbor**: 단순히 Hello 패킷을 주고받아 서로의 존재를 확인한 상태입니다.
* **Adjacency**: 지도를 완전히 공유(Database Sync)하여 데이터를 주고받을 준비가 끝난 친밀한 상태입니다.

### 2. DR (Designated Router) 과 BDR
이더넷 같은 브로드캐스트 망에서 모든 라우터가 1:1로 지도를 공유하면 트래픽이 터집니다.
* **DR (반장)**: 해당 망의 대표 라우터입니다. 모든 라우터는 DR에게만 지도를 보고합니다.
* **BDR (부반장)**: DR이 고장 날 때를 대비한 예비 라우터입니다.
* **Drother**: DR/BDR이 아닌 일반 라우터들입니다.

---

## Ⅳ. LSA (Link State Advertisement)
라우터가 자신의 연결 상태를 광고하는 메시지 조각입니다.

* **LSA Type 1 (Router)**: 자신의 포트와 연결된 정보를 Area 내에 광고.
* **LSA Type 2 (Network)**: DR이 해당 세그먼트의 정보를 광고.
* **LSA Type 3 (Summary)**: ABR이 다른 Area의 정보를 요약해서 전달.
* **LSA Type 5 (AS External)**: ASBR이 외부 네트워크 정보를 전달.

---

## Ⅴ. 개념 맵 및 요약

```ascii
[OSPF Area 구성 예시]

      [ ASBR ] ── (External Net)
         │
  ┌── Area 1 ──┐      [ Area 0 ]      ┌── Area 2 ──┐
  │  Router A  │ ─── [ ABR ] ─── │  Router B  │
  └────────────┘    (Backbone)   └────────────┘
```

📢 **섹션 요약 비유**: **OSPF**는 모든 라우터가 '구글 지도' 앱을 하나씩 들고 있는 것과 같습니다. 사고가 나면 옆 사람에게 "사고 났대"라고 말하는 게 아니라, 사고 지점 좌표(LSA)를 서버(DR)에 올리고 전원이 자기 지도를 실시간 업데이트합니다. 그리고 앱(SPF 알고리즘)이 내 위치에서 목적지까지 가장 빠른 길을 수학적으로 찍어줍니다. 너무 복잡해지는 걸 막기 위해 '서울(Area 0)', '경기도(Area 1)'처럼 구역을 나눠서 지도를 관리하는 똑똑한 시스템입니다.
