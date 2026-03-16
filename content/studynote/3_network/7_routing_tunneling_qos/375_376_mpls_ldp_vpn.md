+++
title = "375-376. MPLS 제어 및 MPLS VPN"
description = "MPLS 라벨 분배를 위한 LDP 프로토콜과 가상 사설망(VPN) 구현을 위한 L3 MPLS VPN 구조"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 375
+++

# 375-376. MPLS 제어 및 MPLS VPN

> **핵심 인사이트**: MPLS 망에서 라벨은 저절로 생기지 않는다. 라우터끼리 "이 주소는 이 라벨로 부르자"고 약속하는 LDP 프로토콜이 필요하며, 이를 통해 구축된 망 위에 VRF를 얹으면 완벽하게 격리된 'MPLS VPN'이라는 전용선급 보안망이 탄생한다.

---

## Ⅰ. LDP (Label Distribution Protocol)
MPLS 라우터들 사이에서 라벨 정보를 자동으로 생성하고 분배하기 위해 사용하는 프로토콜입니다.

* **동작 원리**:
  1. 각 라우터는 자신의 라우팅 테이블에 있는 목적지 대역에 대해 로컬 라벨을 하나씩 부여합니다.
  2. 이 정보를 인접한 LSR(Label Switch Router)들에게 알려줍니다.
  3. 이웃 라우터는 받은 정보를 보고, "A 대역으로 가려면 이 라벨을 붙여서 보내야겠구나"라고 자신의 **LIB (Label Information Base)**를 업데이트합니다.
* **비교**: 데이터 전송 시에는 하드웨어가 읽기 편한 **LFIB (Label Forwarding Information Base)** 테이블을 사용합니다.

---

## Ⅱ. MPLS VPN (Layer 3 VPN)
인터넷망(공용망) 위에서 MPLS 기술을 사용하여 지사와 본사를 안전하게 연결하는 기술입니다.

### 1. 구성 요소
* **CE (Customer Edge)**: 고객사 사무실에 있는 라우터. MPLS를 모르며 일반 IP 패킷을 보냅니다.
* **PE (Provider Edge)**: 통신사(ISP)의 입구 라우터. 고객의 IP 패킷을 받아 **MPLS 라벨을 두 개(이중 라벨)** 씌웁니다.
* **P (Provider)**: 통신사 내부의 백본 라우터. 고객의 실제 IP는 보지 못하고 겉에 씌워진 MPLS 라벨만 보고 고속 전송합니다.

### 2. 이중 라벨 (Dual Labeling) 매커니즘
MPLS VPN 패킷은 두 겹의 라벨 옷을 입습니다.
1. **외곽 라벨 (Outer Label / Transport Label)**: 목적지 PE 라우터까지 가기 위한 고속도로 티켓입니다. 통신사 망 내부(P 라우터)에서만 사용됩니다.
2. **내부 라벨 (Inner Label / VPN Label)**: 목적지 PE에 도착했을 때, "이 패킷이 A사 패킷인지 B사 패킷인지" 구분하여 해당 VRF로 넘겨주기 위한 티켓입니다.

---

## Ⅲ. RSVP-TE (Resource Reservation Protocol - Traffic Engineering)
* **개념**: 단순한 라벨 분배를 넘어, 특정 경로의 **대역폭(Bandwidth)**을 미리 예약하거나 우회 경로를 강제로 지정하기 위해 사용하는 제어 프로토콜입니다.
* **용도**: 네트워크의 특정 구간에 트래픽이 몰리는 것을 방지하고, 경로의 품질(QoS)을 보장해야 할 때 필수적입니다.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[L3 MPLS VPN의 패킷 구조]

  [ L2 Header ] [ Outer Label ] [ Inner Label ] [ IP Packet ]
       │               │               │              │
       │               │               │              └─ 고객 데이터
       │               │               └─ 어느 고객사(VRF) 것인가?
       │               └─ 어느 통신사 지점(PE)으로 가는가?
       └─ 물리적 연결 정보
```

📢 **섹션 요약 비유**: **LDP**는 택배 지점들끼리 "앞으로 서울행 물건은 빨간 스티커를 붙여서 보내자"라고 규약을 정하는 회의입니다. **MPLS VPN**은 이 시스템을 이용한 '기업 전용 배송 서비스'입니다. 상자 안에 원래 송장(IP)을 넣고, 겉에는 '부산 지점행(Outer)' 스티커를 붙인 뒤 그 아래에 'A사 전용 창구행(Inner)' 스티커를 한 장 더 붙입니다. 중간 배달원(P 라우터)은 상자를 열어보지 않고 겉면의 지점 스티커만 보고 신속하게 배달합니다.
