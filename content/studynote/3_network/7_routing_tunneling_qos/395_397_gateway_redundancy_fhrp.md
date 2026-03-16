+++
title = "395-397. 게이트웨이 이중화 프로토콜(FHRP)"
description = "네트워크 가용성 확보를 위한 첫 번째 홉 라우터 이중화 기술: HSRP, VRRP, GLBP 비교"
date = 2026-03-14
[extra]
subject = "NW"
category = "Routing & QoS"
id = 395
+++

# 395-397. 게이트웨이 이중화 프로토콜(FHRP)

> **핵심 인사이트**: 사용자의 컴퓨터에 설정된 '디폴트 게이트웨이' IP는 하나뿐이다. 만약 이 라우터가 고장 나면 인터넷이 끊긴다. 이를 막기 위해 물리적으로는 두 대 이상의 라우터를 두고, 사용자에게는 하나의 '가상 IP'로 보이게 속이는 기술이 FHRP이다.

---

## Ⅰ. FHRP (First Hop Redundancy Protocol) 개요
단말기(PC)가 외부 네트워크로 나가는 첫 번째 관문(First Hop)인 라우터를 이중화하여 장애 대비(High Availability)를 하는 기술입니다.

* **동작 원리**: 두 대 이상의 라우터가 하나의 **가상 IP(Virtual IP)**와 **가상 MAC 주소**를 공유합니다. PC는 이 가상 IP를 게이트웨이로 설정합니다.

---

## Ⅱ. 주요 FHRP 프로토콜 종류

### 1. HSRP (Hot Standby Router Protocol)
* **특징**: **시스코(Cisco)** 독자 프로토콜입니다.
* **상태**: 한 대는 **Active**(실제 동작), 다른 한 대는 **Standby**(대기) 상태로 유지됩니다.
* **동작**: Active 라우터가 죽으면 Standby가 즉시 가상 IP를 넘겨받아 업무를 수행합니다.

### 2. VRRP (Virtual Router Redundancy Protocol)
* **특징**: IEEE 표준으로 정의된 **개방형 표준** 프로토콜입니다. (대부분의 벤더 장비 호환)
* **상태**: 한 대는 **Master**, 나머지는 **Backup** 상태라고 부릅니다.
* **동작**: HSRP와 거의 동일하지만, 실제 물리 인터페이스 IP를 가상 IP로 그대로 사용할 수 있다는 차이점이 있습니다.

### 3. GLBP (Gateway Load Balancing Protocol)
* **특징**: HSRP와 VRRP의 단점을 보완한 시스코 독자 프로토콜입니다.
* **차별점**: HSRP/VRRP는 한 번에 한 대만 일하고 나머지는 놀고 있는데(Active-Standby), GLBP는 **모든 라우터가 동시에 트래픽을 처리(Active-Active)**할 수 있도록 로드 밸런싱을 지원합니다.
* **원리**: PC들이 ARP 요청을 보낼 때마다 라우터들이 서로 다른 가상 MAC 주소를 번갈아 알려주어(Round Robin) 트래픽을 분산시킵니다.

---

## Ⅲ. FHRP 기술 비교 요약

| 구분 | HSRP | VRRP | GLBP |
| :--- | :--- | :--- | :--- |
| **표준 여부** | 시스코 독자 | **국제 표준 (RFC)** | 시스코 독자 |
| **동작 방식** | Active / Standby | Master / Backup | **Active / Active (Load Balancing)** |
| **가상 MAC** | 0000.0c07.acXX | 0000.5e00.01XX | 0007.b4XX.XXXX |
| **헬로 주기** | 3초 | 1초 | 3초 |

---

## Ⅳ. 개념 맵 및 요약

```ascii
[게이트웨이 이중화 구성]

      [ 가상 게이트웨이 IP: 192.168.1.1 ]
               /              \
        (Active)              (Standby)
      [ Router A ]          [ Router B ]
      IP: .2                IP: .3
               \              /
          ──────[ L2 스위치 ]──────
                    |
                [ User PC ]
          Gateway: 192.168.1.1
```

📢 **섹션 요약 비유**: **FHRP**는 2인 1조로 일하는 편의점 아르바이트생입니다. **HSRP/VRRP**는 한 명만 카운터에 서 있고 다른 한 명은 휴게실에서 자고 있다가, 일하던 친구가 쓰러지면 교대하는 방식입니다. 반면 **GLBP**는 두 개의 계산대를 동시에 열고 손님(패킷)을 나눠서 받는 훨씬 효율적인 시스템입니다.
