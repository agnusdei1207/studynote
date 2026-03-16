+++
title = "333-336. 멀티캐스트 및 Neighbor 제어 (IGMP, NDP)"
description = "멀티캐스트 그룹 관리를 위한 IGMP와 IPv6 환경에서 ARP를 대체하는 Neighbor Discovery Protocol(NDP) 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "Network Layer"
id = 333
+++

# 333-336. 멀티캐스트 및 Neighbor 제어 (IGMP, NDP)

> **핵심 인사이트**: 인터넷에는 1:1 대화만 있는 것이 아니다. 동호회 회원들(그룹)끼리만 대화하기 위한 관리 프로토콜(IGMP)이 필요하며, 특히 IPv6에서는 옆집 사람을 찾기 위해 과거의 ARP 대신 더 세련된 NDP 방식을 사용한다.

---

## Ⅰ. IGMP (Internet Group Management Protocol)
IPv4 환경에서 호스트가 멀티캐스트 그룹에 가입하거나 탈퇴할 때, 이를 **주변 라우터에게 알리기 위해** 사용하는 프로토콜입니다.

* **동작**:
  - **Join**: "나 224.1.1.1 그룹(TV 채널 등)에 가입할래!" 라고 라우터에게 말합니다.
  - **Query**: 라우터가 주기적으로 "아직 이 그룹에 남아있는 사람 있니?"라고 묻습니다.
  - **Report**: 호스트가 "응, 나 아직 듣고 있어"라고 답합니다.
* **IGMP Snooping**: 똑똑한 L2 스위치가 IGMP 메시지를 엿듣고(Snoop), 멀티캐스트 트래픽을 해당 그룹 가입자가 있는 포트로만 정확히 전달하여 네트워크 부하를 줄여주는 기술입니다.

---

## Ⅱ. NDP (Neighbor Discovery Protocol)
IPv6 환경에서 가장 중요한 역할을 수행하는 프로토콜입니다. IPv4의 **ARP, ICMP Redirect, Router Discovery** 기능을 하나로 통합했습니다.

### 핵심 메시지 4종 세트
1. **NS (Neighbor Solicitation)**: "IP 주소가 A인 사람 누구니? MAC 주소 좀 알려줘!" (IPv4의 ARP Request 역할)
2. **NA (Neighbor Advertisement)**: "그거 난데, 내 MAC은 이거야!" (IPv4의 ARP Reply 역할)
3. **RS (Router Solicitation)**: "주변에 라우터님 계신가요? 네트워크 정보 좀 주세요!" (SLAAC의 시작)
4. **RA (Router Advertisement)**: "여기 라우터 있다! 이 동네 번호(Prefix)는 이거야." (SLAAC 주소 생성의 핵심)

---

## Ⅲ. IGMP와 MLD의 관계
* **MLD (Multicast Listener Discovery)**: IPv6 환경에서 사용하는 IGMP의 버전입니다. 동작 원리는 IGMP와 거의 같지만, ICMPv6 메시지를 기반으로 동작한다는 점이 다릅니다.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[멀티캐스트 그룹 관리 (IGMP)]
  [ Host ] --(Join: 224.1.1.1)--> [ Router ]
  [ Router ] --(Multicast Data)--> [ 가입한 Host들에게만 전달 ]

[IPv6 옆집 찾기 (NDP)]
  [ PC A ] --(NS: 너 누구니?)--> [ PC B ]
  [ PC A ] <--(NA: 나야 나!)--- [ PC B ]
  (이 과정을 통해 MAC 주소를 알아냄)
```

📢 **섹션 요약 비유**: **IGMP**는 아파트 방송에서 "내일 등산 가실 분 신청하세요"라고 할 때 손을 드는 행위입니다. 경비 아저씨(라우터)는 손든 집(호스트)에만 안내문을 배달합니다. **NDP**는 IPv6 마을의 '반상회'와 같습니다. 옆집 이름(MAC)을 물어보기도 하고(NS/NA), 새로 부임한 이장님(라우터)에게 동네 규칙을 물어보기도(RS/RA) 하는 다목적 커뮤니케이션 도구입니다.
