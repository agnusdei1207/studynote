+++
title = "940-1000. 네트워크 시험 빈출 핵심 토픽 요약"
description = "네트워크 기술사 및 자격증 시험에 자주 등장하는 핵심 개념들의 정의와 동작 원리 요약"
date = 2026-03-14
[extra]
subject = "NW"
category = "Exam Topics"
id = 940
+++

# 940-1000. 네트워크 시험 빈출 핵심 토픽 요약

> **핵심 인사이트**: 네트워크 인프라 지식은 계층별 핵심 메커니즘의 이해에서 시작된다. L2의 스위칭과 루프 방지, L3의 IP 체계와 라우팅, L4의 신뢰 전송, 그리고 최신 클라우드/가상화 기술까지의 연결 고리를 파악하는 것이 시험 합격의 열쇠다.

---

## Ⅰ. L1 & L2: 전송 매체와 데이터 링크
1. **RZ / NRZ / Manchester**: 기저대역 전송을 위한 선로 부호화 방식. (동기화와 대역폭 효율성)
2. **PCM (Pulse Code Modulation)**: 아날로그 음성을 디지털로 변환하는 3단계(표본화-양자화-부호화) 과정.
3. **CSMA/CD vs CSMA/CA**: 유선 이더넷(충돌 검출)과 무선 Wi-Fi(충돌 회피)의 매체 접근 제어 방식 차이.
4. **STP (Spanning Tree Protocol)**: L2 루프(Broadcast Storm)를 방지하기 위해 특정 포트를 차단하는 기술.
5. **VLAN 트렁킹 (802.1Q)**: 하나의 물리 선에 여러 가상 망 트래픽을 구분(Tagging)하여 전달하는 기술.

---

## Ⅱ. L3 & L4: 네트워크와 전송 계층
1. **CIDR / VLSM**: 클래스 없이 비트 단위로 주소를 쪼개어 IP 낭비를 막는 현대적 주소 체계.
2. **ARP / RARP / G-ARP**: IP와 MAC 사이의 변환 및 IP 중복 감지(G-ARP) 메커니즘.
3. **OSPF (Link State) vs BGP (Path Vector)**: 최단 경로(SPF)를 찾는 내부망 방식과 정책(AS-Path)을 중시하는 외부망 방식.
4. **TCP 3-Way Handshake**: 신뢰성 있는 연결 설정을 위한 'SYN - SYN/ACK - ACK' 과정.
5. **Slow Start / Congestion Avoidance**: 혼잡 발생 전 대역폭을 탐색하고 조절하는 TCP의 지능형 전송 제어.

---

## Ⅲ. L7 & 보안 및 가상화
1. **HTTP/2 & HTTP/3**: 멀티플렉싱과 UDP(QUIC) 기반 전송을 통한 웹 지연 시간의 혁신적 단축.
2. **SSL/TLS 1.3**: 핸드셰이크를 1-RTT로 줄이고 취약한 암호를 제거한 현대 웹 보안의 표준.
3. **IPsec (AH/ESP)**: 네트워크 계층에서 VPN을 구축하기 위한 암호화 및 인증 프레임워크.
4. **VXLAN / EVPN**: 물리망(Underlay) 위에 1,600만 개의 가상망(Overlay)을 만드는 데이터센터 핵심 기술.
5. **SDN / NFV**: 제어 평면을 분리하고(SDN), 전용 하드웨어를 소프트웨어(NFV)로 전환하는 인프라 혁명.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[네트워크 계층별 핵심 키워드]

  [ L7 App ]  HTTP/3, DNS, MQTT, OAuth, JWT
      │
  [ L4 Trp ]  TCP(Congestion), UDP, QUIC, Port
      │
  [ L3 Net ]  IP, ICMP, ARP, OSPF, BGP, SDN
      │
  [ L2 Lnk ]  Ethernet, STP, VLAN, MAC
      │
  [ L1 Phy ]  UTP, Fiber, PCM, Modulation
```

📢 **섹션 요약 비유**: **네트워크**는 거대한 '도시 인프라'입니다. **L1/L2**는 도로를 닦고 표지판을 세우는 기초 공사이고, **L3/L4**는 택배 회사가 정확하고 안전하게 물건을 배달하는 시스템입니다. **L7과 보안**은 그 도로 위에서 비즈니스를 하고 도둑을 막는 상거래와 경찰 시스템과 같습니다. **SDN/NFV**는 이 모든 도시 관리를 컴퓨터 시뮬레이션 게임처럼 클릭 몇 번으로 통제하는 '스마트 시티 운영 센터'입니다.
