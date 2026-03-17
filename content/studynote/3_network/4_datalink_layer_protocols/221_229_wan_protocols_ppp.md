+++
title = "221-229. 광역 통신망(WAN) 프로토콜과 PPP"
date = "2026-03-14"
[extra]
category = "Data Link Layer"
id = 221
+++

# 221-229. 광역 통신망(WAN) 프로토콜과 PPP

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중 벤더 환경에서의 상호 운용성과 신뢰성을 보장하기 위해 ISO 표준 HDLC(High-level Data Link Control)를 기반으로 발전한 WAN 프로토콜군과, 현대 인터넷의 직렬 통신 표준인 PPP(Point-to-Point Protocol)의 아키텍처를 이해한다.
> 2. **가치**: IBM SNA(Systems Network Architecture)와 X.25 망의 한계를 넘어, 벤더 독립적인 LCP(Link Control Protocol)와 NCP(Network Control Protocol) 계층 분리를 통해 IP 망의 유연성과 확장성을 획기적으로 개선했다.
> 3. **융합**: 2계층(데이터 링크)의 프레이밍과 3계층(네트워크)의 라우팅을 연결하며, 보안(Security) 분야의 인증 메커니즘(Hashing, Handshake)을 물리 계층에 통합한 하이브리드 프로토콜의 진화 모델이다.

---

### Ⅰ. 개요 (Context & Background) - [WAN 프로토콜의 진화론]

**1. 개념 및 철학**
광역 통신망(WAN, Wide Area Network) 프로토콜은 지리적으로 떨어진 네트워크 장비 간에 데이터를 전송하기 위한 **데이터 링크 계층(Data Link Layer, Layer 2)**의 규약이다. 초기에는 각 벤더와 통신 환경에 최적화된 독자적인 프로토콜이 난립했으나, 인터넷의 발전과 함께 벤더 독립적인 표준화의 중요성이 부각되었다. 이 과정에서 IBM의 주도하에 개발된 SDLC(Synchronous Data Link Control)가 ISO의 표준인 HDLC로 발전했고, 이를 기반으로 X.25용 LAPB, ISDN용 LAPD 등 파생 프로토콜이 등장했다. 현재는 이러한 복잡한 파생 프로토콜을 통합하고, 다양한 네트워크 계층 프로토콜(IP, IPX 등)을 수용할 수 있는 PPP(Point-to-Point Protocol)가 인터넷接入의 사실상 표준(de facto standard)으로 자리 잡았다.

**2. 등장 배경 (역사적 맥락)**
*   **① IBM의 독주 (SDLC)**: 1970년대 IBM은 메인프레임 중심의 SNA 아키텍처를 구축하기 위해 SDLC를 개발했다. 이는 당시 혁신적인 '전이중(Full-Duplex)' 통신을 가능하게 했으나, IBM 장비가 아닌 곳에서는 사용할 수 없는 폐쇄적인 구조였다.
*   **② 표준화의 노력 (HDLC)**: ISO는 SDLC를 기반으로 범용적으로 사용할 수 있는 HDLC를 제정했다. HDLC는 비트 지향(Bit-oriented) 프로토콜로 효율적이었으나, 구현 옵션이 너무 다양하여 서로 다른 벤더 간 호환성 문제가 여전히 존재했다.
*   **③ 인터넷의 요구 (PPP 등장)**: 1990년대 인터넷 폭발적 성장과 함께, 전용선(Leased Line)이나 전화선(Dial-up)을 통해 서로 다른 라우터 벤더(Cisco, 3Com 등) 간에 원활한 IP 통신이 필요해졌다. 이에 IETF(Internet Engineering Task Force)는 RFC 1661을 통해 '어떤 장비와도 통신이 가능하고', '다양한 프로토콜을 실어 나를 수 있는' PPP를 표준으로 채택했다.

**💡 비유**: HDLC는 "한 자동차 회사만을 위한 전용 고속도로"였다면, PPP는 "모든 종류의 차량(승용차, 트럭, 오토바이)이 다닐 수 있고, 요금 징수와 통행 제어가 표준화된 일반 국도"와 같다.

**📢 섹션 요약 비유**: WAN 프로토콜의 발전 과정은 **'각 사정에 맞춰 만든 비포장도로(SDLC)에서 표준화된 포장도로(HDLC)를 거쳐, 모든 차량과 운전자가 이용하는 수준 높은 스마트 고속도로(PPP)로 진화한 과정'**과 같다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [PPP의 구조와 동작]

**1. PPP의 핵심 구성 요소**
PPP는 단순한 프레이밍 규칙이 아니라, 링크 설정부터 네트워크 계층 연결까지 담당하는 프로토콜 스위트(Suite)이다. 크게 세 가지 주요 구성 요소로 나뉜다.

| 구성 요소 | 전체 명칭 | 핵심 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---:|:---|:---|:---|:---|
| **HL** | HDLC-like Framing | **물리적 전송 단위 정의** | 비트 스터핑(Bit Stuffing) 기반의 프레임 구조 정의. Flag(`01111110`)으로 프레임 시작/종료 식별. | **우편물 봉투** |
| **LCP** | Link Control Protocol | **링크 설정/유지/종료** | 통신 시작 시 전송 매개변수(MRU, Magic Number 등) 협상. 연결 상태 모니터링. | **통신사 직원** (회선 개통) |
| **NCP** | Network Control Protocol | **네트워크 계층 협상** | 각 네트워크 계층 프로토콜(IP, IPX, AppleTalk)에 맞는 파라미터(IP 주소 할당 등) 협상. 예: IPCP. | **번지 할당** (주소 배정) |

**2. PPP 프레임 구조 분석**
PPP는 HDLC의 프레임 형식을 차용하되, `Protocol` 필드를 추가하여 다중 프로토콜 지원이 가능하도록 설계되었다.

```ascii
<PPP Frame Format (RFC 1662)>

+----------+----------+----------+----------+----------+----------+
|  Flag    | Address  | Control  | Protocol |  Payload |   FCS    |
|(1 Byte)  | (1 Byte) | (1 Byte) | (2 Bytes)| (N Bytes)| (2/4 B)  |
+----------+----------+----------+----------+----------+----------+
| 01111110 |   11111111|   00000011| 0x0021   |  IP DATAGRAM |  CRC  |
+----------+----------+----------+----------+----------+----------+

[핵심 필드 해설]
1. Flag (0x7E): 프레임의 시작과 끝을 알리는 경계 문자.
2. Address (0xFF): 모든 스테이션을 의미하는 브로드캐스트 주소(PPP는 1:1이므로 고정값).
3. Control (0x03): 연결형 모드를 의미하는 고정값.
4. Protocol (0x0021): 상위 계층이 무엇인지 식별 (예: 0x0021=IPv4, 0x8021=IPCP).
5. FCS (Frame Check Sequence): 전송 중 오류 검출을 위한 CRC(Cyclic Redundancy Check) 코드.
```

**3. PPP 동작 상태 머신 (State Machine)**
PPP 연결은 정교한 상태 천이(State Transition) 과정을 거친다. `Link Dead` 상태에서 물리적 회선이 연결되면 데이터 통신이 가능한 `Network-Layer Protocol Open` 상태로 넘어간다.

```ascii
[PPP Connection State Diagram]

      Link Dead             Link Establishment       Authentication
   (전원 off/선 연결 끊)   --------> (LCP Negotiation) --------> (PAP/CHAP)
          ^                         |        |                    |
          |                         |        v                    |
          |                         |   Link Open                |
          |                         |  (No Auth Request)         v
          |                         |         |          Network-Layer Protocol Open
          |                         |         |         (NCP: IP Address Assigned)
          |                         |         v                    |
          |                         |   Links Terminated <---------
          |                         |   (LCP Close)        ^
          |                         |______________________|
          |                              Data Transfer
          |                              (Actual Traffic)
          +_______________________________________________
```

*   **해설**: 먼저 LCP가 링크 설정(`Link Establishment`)을 위해 협상을 진행한다. 인증이 필요하면 `Authentication` 단계로 넘어가 PAP/CHAP을 수행한다. 인증에 성공하면 NCP가 IP 주소를 할당받는 등의 네트워크 계층 설정(`Network-Layer Protocol Open`)을 진행한다. 이제 데이터 전송(`Data Transfer`)이 가능해지며, 통신 종료 시 LCP가 연결을 끊는다.

**4. 핵심 알고리즘: LCP 협상 코드**
LCP 협상 과정에서 사용자는 원하는 링크 옵션을 요청하고, 수신측은 이에 대해 동의(Configure-Ack)하거나 거부(Configure-Nak/Reject)한다. 다음은 협상 패킷의 논리적 구조 예시이다.

```python
# Pseudo-code for LCP Configure-Request
def send_lcp_configure_request():
    packet = {
        "Code": 1,            # Configure-Request
        "Identifier": 1,      # Matching ID for Response
        "Length": 14,
        "Options": [
            {"Type": 1, "Length": 2, "Value": 4},  # MRU: 1500 bytes
            {"Type": 3, "Length": 4, "Value": 0xC023}, # Auth Protocol: PAP
            {"Type": 5, "Length": 4, "Value": 0x0001}  # Magic Number
        ]
    }
    # 이 패킷을 PPP 프레임의 Payload에 담아 전송
    # Peer는 같은 ID로 Configure-Ack(2), Nak(3), Reject(4) 중 하나를 응답
```

**📢 섹션 요약 비유**: PPP의 동작 과정은 **'이사를 갈 때 인테리어 공사부터 주소 등록까지 하는 과정'**과 같다. LCP는 집 구조를 잡고 문을 설치하는 건축가(링크 설정)이고, 인증은 이사 짐을 가져오기 전 신원을 확인하는 경비원(Authentication)이며, NCP는 집 번호를 할당하고 우편물을 받을 준비를 하는 행정 담당자(IP 할당) 역할을 한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. PPP vs HDLC (기술적 비교 분석)**
과거 WAN 표준이었던 HDLC와 현대 표준인 PPP는 구조적으로 유사하지만, 목적과 기능 면에서 명확한 차이가 있다.

| 비교 항목 | HDLC (High-level Data Link Control) | PPP (Point-to-Point Protocol) |
|:---|:---|:---|
| **표준화 주체** | ISO (국제 표준화 기구) | IETF (인터넷 엔지니어링 태스크 포스) |
| **프레이밍** | 비트 지향 (Bit-oriented) | 바이트 지향 (Byte-oriented, 문자 지향) |
| **벤더 호환성** | 벤더별 Sub-type 존재으로 호환성 이슈 있음 | 벤더 독립적, 전 세계 공통 표준 |
| **프로토콜 지원** | 단일 프로토콜 전용 (일반적으로) | 다중 프로토콜 동시 지원 (IPv4, IPv6, IPX 등) |
| **링크 제어** | 내장되어 있으나 제한적 | LCP라는 독립적인 계층으로 강력한 제어 기능 제공 |
| **인증 기능** | 없음 (별도 장비 의존) | PAP, CHAP, EAP 등 내장된 보안 기능 제공 |
| **오류 제어** | Selective Reject(선택적 재전송) 가능 | 기본적으로 단순하지만 옵션으로 확장 가능 |

**2. 과목 융합: 네트워크 vs 보안**
PPP는 단순한 전송 기술을 넘어 **보안(Security) 아키텍처**를 데이터 링크 계층에 통합한 대표적인 사례이다.

*   **암호학적 적용 (Cryptography)**:
    *   **PAP (Password Authentication Protocol)**는 평문(Cleartext)을 사용하므로 기밀성(Confidentiality)이 전무하다. 이는 보안 원칙 중 '최소 권한' 및 '암호화' 원칙을 위배하는 고전적인 방식이다.
    *   **CHAP (Challenge Handshake Authentication Protocol)**는 **해시(Hash) 함수**와 **랜덤 챌린지(Nonce)**를 사용한다. 비밀번호가 네트워크를 직접 타지 않으므로 도청(Eavesdropping) 공격에 방어하며, 매번 챌린지 값이 달라지므로 **재전송 공격(Replay Attack) 방지**가 가능하다. 이는 현대 보안 인증(MD5, HMAC)의 기초 원리가 된다.
*   **시스템 아키텍처 (OS/Arch)**:
    *   PPP의 NCP(Network Control Protocol)는 OS에서 **드라이버가 인터페이스를 초기화하고 IP 주소를 할당받는 과정**와 유사하다. 시스템 부팅 시 네트워크 인터페이스가 `DOWN` 상태에서 `UP` 상태로 변하며 IP를 획득하는 과정은 PPP 연결 과정(LCP -> Auth -> NCP)과 1:1 매핑된다.

**3. 인증 프로토콜 심층 비교 (PAP vs CHAP)**

```ascii
[Authentication Flow Comparison]

< PAP (2-Way Handshake) >
Client                  Server
   |   (1) ID/Passwd      |
   |--------------------->|
   |                      | --[Validate DB]-->
   |   (2) ACK/NAK        |
   |<---------------------|
   | (Weak: Cleartext)    |

< CHAP (3-Way Handshake) >
Client                  Server
   |                      |
   |   (1) Challenge      | (Random String)
   |<---------------------|
   |                      |
   |   (2) Response       | (Hash(ID|Passwd|Challenge))
   |--------------------->|
   |                      |
   |   (3) Success/Fail   |
   |<---------------------|
   | (Strong: No Secret)  |
```

**📢 섹션 요약 비유**: HDLC와 PPP의 차이는 **'자동차 엔진의 구조'**와 같다. HDLC는 성능 위주의 단순한 엔진(구조는 튼튼하나 옵션 부족)이라면, PPP는 최신 자동차처럼 연비 최적화, 내비게이션 연동, 스마트 키 보안(인증)까지 하나로 통합한 **'통합 제어 시스템(Smart Car Platform)'**이라고 볼 수 있다.

---

### Ⅳ. 실무 적용 및 기술사