+++
title = "221-229. 광역 통신망(WAN) 프로토콜과 PPP"
description = "HDLC의 파생 프로토콜(SDLC, LAPB)과 현대 인터넷의 핵심 직렬 통신 프로토콜인 PPP의 구조 및 인증 방식(PAP, CHAP)"
date = 2026-03-14
[extra]
subject = "NW"
category = "Data Link Layer"
id = 221
+++

# 221-229. 광역 통신망(WAN) 프로토콜과 PPP

> **핵심 인사이트**: 인터넷이 대중화되기 전 기업 통신망을 지배했던 HDLC 파생 프로토콜들(SDLC, LAPB 등)은 점차 자취를 감추고, 서로 다른 장비 간의 호환성과 강력한 인증 기능을 무기로 한 **PPP(Point-to-Point Protocol)**가 현대 직렬 통신망(WAN)의 표준으로 자리 잡았다.

---

## Ⅰ. HDLC 파생 프로토콜의 역사
HDLC는 훌륭했지만 너무 방대했습니다. 각 벤더와 네트워크 환경은 HDLC를 입맛에 맞게 변형하여 사용했습니다.

* **SDLC (Synchronous Data Link Control)**: IBM에서 개발한 프로토콜로, HDLC의 원조 격입니다. 주로 IBM 메인프레임 환경의 SNA(Systems Network Architecture)에서 사용되었습니다.
* **LAPB (Link Access Procedure Balanced)**: 과거 전용선과 패킷 교환망의 표준이었던 **X.25 네트워크**에서 단말(DTE)과 교환기(DCE) 사이의 신뢰성 있는 통신을 위해 사용된 HDLC의 ABM(비동기 균형 모드) 변형판입니다.
* **LAPD (Link Access Procedure on the D channel)**: 음성과 데이터를 통합 전송하던 **ISDN 네트워크**의 D 채널(제어 채널)에서 사용되던 프로토콜입니다.

---

## Ⅱ. PPP (Point-to-Point Protocol)
HDLC의 파생형들이 특정 벤더(IBM)나 특정 망(X.25)에 종속적이었던 반면, **PPP는 IETF가 만든 완벽한 개방형 인터넷 표준(RFC 1661)**입니다. 두 노드를 1:1로 직접 연결하는 직렬 회선(전화선, 전용선, 광케이블)에서 IP 패킷을 전송하기 위해 만들어졌습니다.

### 1. PPP의 주요 특징
* **바이트 지향(Byte-oriented)**: 비트 단위로 스터핑을 하던 HDLC와 달리, PPP는 처리 속도가 빠른 바이트(문자) 단위로 프레이밍을 합니다.
* **다중 프로토콜 지원**: 하나의 링크에서 IPv4, IPv6, IPX 등 여러 네트워크 계층 프로토콜을 동시에 전송할 수 있습니다.
* **강력한 인증 및 압축**: 연결을 맺을 때 사용자 신원을 확인(Authentication)하고 데이터를 압축하는 기능이 내장되어 있습니다.

### 2. PPP의 핵심 하위 프로토콜
PPP는 단순한 프레이밍 기술이 아니라, 여러 프로토콜의 집합체입니다.
* **LCP (Link Control Protocol)**: 통신을 시작할 때, 링크를 맺고(Establish), 옵션(인증 방식, 최대 프레임 크기 등)을 협상(Configure)하며, 통신이 끝나면 링크를 끊는(Terminate) **물리적 링크 제어 담당관**입니다.
* **NCP (Network Control Protocol)**: LCP가 길을 닦아놓으면, 그 위에 어떤 네트워크 프로토콜(IP)을 올릴지 협상하는 역할을 합니다. IP를 올릴 때는 IPCP(IP Control Protocol)가 작동하여 동적으로 IP 주소를 할당받게 해 줍니다.

---

## Ⅲ. PPP의 인증 프로토콜 (PAP vs CHAP vs EAP)
LCP 단계에서 링크가 맺어지면, 데이터를 보내기 전 접속자가 정당한 사용자인지 검사합니다.

### 1. PAP (Password Authentication Protocol)
* **방식**: 클라이언트가 서버에게 **아이디와 비밀번호를 평문(Cleartext)**으로 그대로 전송합니다. (2-Way Handshake)
* **단점**: 중간에 해커가 스니핑(Sniffing)하면 비밀번호가 고스란히 유출되는 치명적인 보안 취약점이 있습니다.

### 2. CHAP (Challenge Handshake Authentication Protocol)
* **방식 (3-Way Handshake)**: 
  1. 서버가 클라이언트에게 무작위 난수 문자열(Challenge)을 보냅니다.
  2. 클라이언트는 자신의 비밀번호와 이 난수를 섞어서 **일방향 해시(MD5 등)**로 만든 뒤 결과값만 서버로 보냅니다. (비밀번호는 네트워크를 타지 않음)
  3. 서버도 자신이 저장한 비밀번호로 똑같이 해시를 만들어보고, 결과가 일치하면(Handshake) 승인합니다.
* **장점**: 네트워크 상에 비밀번호가 노출되지 않으며, 주기적으로 새로운 난수를 보내 재인증을 요구하므로 보안성이 매우 뛰어납니다.

### 3. EAP (Extensible Authentication Protocol)
* PAP와 CHAP의 한계를 넘어, 스마트카드, OTP, 생체인식 등 **원하는 모든 종류의 인증 방식을 플러그인처럼 꽂아서 쓸 수 있도록 확장성(Extensible)**을 부여한 인증 프레임워크입니다. 오늘날 무선 LAN(WPA2/WPA3 엔터프라이즈) 인증의 핵심 기술입니다.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[PPP 접속 및 통신 흐름도]

1. LCP (링크 제어) : "우리 서로 연결하자. 인증은 CHAP으로 할까?"
       ↓
2. Auth (인증)     : [CHAP 3-Way Handshake 진행] -> "비밀번호 해시 검증 완료!"
       ↓
3. NCP (네트워크)  : "IP 통신을 할 거니까 IPCP를 켜자. 내 IP 주소 좀 할당해 줘."
       ↓
4. Data 전송       : 인터넷 통신 시작 (IP 패킷이 PPP 프레임에 담겨 날아감)
       ↓
5. LCP (링크 종료) : "나 이제 연결 끊을게. 수고했어."
```

📢 **섹션 요약 비유**: PPP는 전화 통화(1:1 연결)의 표준 예절입니다. 전화를 걸면 먼저 LCP가 "여보세요? 잘 들려요?" 하고 회선 상태를 확인합니다. 그다음 Auth가 "근데 누구세요? 암구호 대보세요(CHAP)" 하고 신원을 확인합니다. 인증이 끝나면 NCP가 "우리 한국어(IPv4)로 대화할까요?" 하고 언어를 맞춥니다. 모든 조율이 끝나면 비로소 용건(Data)을 말하기 시작합니다.
