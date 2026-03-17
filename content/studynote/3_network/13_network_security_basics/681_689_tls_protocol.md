+++
title = "681-689. SSL/TLS 프로토콜과 핸드셰이크"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 681
+++

# 681-689. SSL/TLS 프로토콜과 핸드셰이크

### # SSL/TLS 프로토콜과 핸드셰이크
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: TLS (Transport Layer Security)는 전송 계층과 애플리케이션 계층 사이의 **보안 계층(Security Layer)**으로, 무결성과 기밀성을 보장하기 위해 핸드셰이크(Handshake)를 통해 세션 키를 협상하는 프로토콜이다.
> 2. **가치**: 공개키 기반구조(PKI, Public Key Infrastructure)를 통해 신뢰를 설정하고, 이후에는 고성능 대칭키 암호화를 사용하여 **보안성과 성능의 균형**을 달성한다. 특히 PFS(Perfect Forward Secrecy)를 통해 과거 통신 내용의 안전성을 보장한다.
> 3. **융합**: 네트워크 계층의 TCP/IP와 밀접하게 결합하며, 최신 **TLS 1.3**은 핸드셰이크를 1-RTT로 단축하여 HTTP/3 및 QUIC와 같은 고성능 프로토콜의 기반 기술로 작용한다.

+++

### Ⅰ. 개요 (Context & Background) - 암호화 계층의 탄생과 진화

**개념 및 정의**
SSL (Secure Sockets Layer)은 넷스케이프(Netscape)가 개발한 보안 프로토콜로 시작했으나, 보안 취약점이 발견되며 표준화 기구인 IETF (Internet Engineering Task Force)에 의해 **TLS (Transport Layer Security)**로 표준화되었다. 이는 OSI 7계층의 전송 계층(Transport Layer, L4) 위에서 응용 계층(Application Layer, L7) 사이에 위치하여, 개발자가 애플리케이션 코드를 수정하지 않고도 데이터 암호화를 제공하는 투명한 계층이다.

**💡 비유: 우편물의 봉투와 검인**
TLS는 평문으로 작성된 편지(데이터)를 투명한 봉투가 아닌 **검은색 불투명 봉투(암호화)**에 넣어 우편을 보내는 시스템이다. 그리고 이 봉투의 봉인지에는 위조 불가능한 **정부 인감(디지털 서명)**이 찍혀 있어, 받는 사람은 이 봉투가 진짜 우체국에서 보낸 것인지 확인할 수 있다. 

**등장 배경 및 필요성**
초기 인터넷은 신뢰 기반의 학술 및 군사 네트워크였으나, 전자상거래(E-Commerce)가 등장하며 **도청(Eavesdropping)**과 **위장(Spoofing)**의 위험이 급증했다.
1. ① 기존 한계: HTTP의 텍스트 전송 방식은 네트워크 중간자(MITM, Man-In-The-Middle)가 내용을 훔쳐보거나 조작하기 쉬웠다.
2. ② 혁신적 패러다임: 암호화 알고리즘을 네트워크 스택에 통합하여, 계층 5(Session)와 6(Presentation)의 역할을 수행하는 독립적인 보안 계층을 도입했다.
3. ③ 현재 비즈니스 요구: 구글(Google) 등 검색 엔진의 SEO(검색 최적화) 정책에 HTTPS 채택이 필수화되었으며, 개인정보보호법(GDPR 등)과 같은 법적 규제 준수를 위한 필수 요건이 되었다.

**ASCII 다이어그램: 프로토콜 스택 내 위치**

```ascii
+-----------------------+---------------------+
| 응용 계층 (L7)         | HTTP, FTP, SMTP ... |
+-----------------------+---------------------+
| **TLS/SSL (L5/L6)**    | <-- [보안 계층]      |
|-----------------------| Handshake, Record   |
| 전송 계층 (L4)         | TCP / UDP           |
+-----------------------+---------------------+
| 인터넷 계층 (L3)       | IP                  |
+-----------------------+---------------------+

<데이터 흐름>
HTTP 데이터 --[TLS Encapsulation]--> TLS 데이터 --[TCP Segment]--> IP 패킷
```

*(해설: TLS는 응용 계층 데이터를 받아 'TLS Record'라는 단위로 캡슐화하고, 이를 다시 TCP 세그먼트로 실어 보낸다. 응용 계층 입장에서는 TCP Socket 위에서 안전하게 통신하는 것처럼 보인다.)*

> **📢 섹션 요약 비유**: TLS 구축은 일반 도로 위에 **'음�색으로 도장된 특수 차선'**을 추가하는 것과 같습니다. 기존 도로(TCP/IP)의 흐름을 그대로 유지하면서, 유리차 안에서만 서로의 얼굴을 확인하고 대화할 수 있는 프라이빗 공간을 제공합니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - 핸드셰이크와 암호화 스위트

TLS의 핵심은 무겁고 느린 **비대칭키 암호화(공개키)**를 통해 신뢰와 세션 키를 안전하게 교환한 뒤, 빠르고 효율적인 **대칭키 암호화**로 전환하여 데이터를 송수수하는 '하이브리드 암호화 시스템'이다.

**구성 요소 상세 분석**

| 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Handshake Protocol** | 인증 및 키 협상 | 암호 알고리즘(Cipher Suite) 협상, 인증서 교환, 키 생성 (Key Exchange) | 외교관 신분증 검사 및 회의 코드 결정 |
| **Record Protocol** | 데이터 암호화/복호화 | 데이터를 분할(Fragmentation), 압축(Compression), MAC(Message Authentication Code) 생성, 암호화 | 보내는 편지지를 찢어서 봉투에 밀봉 |
| **Alert Protocol** | 오류 및 경고 전달 | 치명적 오류(Fatal) 시 연결 강제 종료, 경고(Warning) 시 재협상 요청 | 비상시 알람 sirene |
| **Change Cipher Spec** | 암호 상태 전환 | 협상된 상태(State)에서 실제 암호화 모드로 전환하는 신호 플래그 | "지금부터 암호 모드 ON" 스위치 |

**심층 동작 원리: TLS 1.2 핸드셰이크 (Full Handshake)**
이 과정은 총 **2-RTT (Round Trip Time)**가 소요되는 구형 프로세스이다.
1. **Client Hello**: 지원하는 Cipher Suite 목록과 난수(Random Byte)를 전송.
2. **Server Hello + Certificate**: 선택된 Cipher Suite와 서버 인증서(X.509), Server Hello Random 전송.
3. **Certificate Verify (Client)**: CA (Certificate Authority)의 공개키로 인증서를 검증하고 서버의 신원을 확인.
4. **Key Exchange (Pre-Master Secret)**: 클라이언트가 난수를 생성하여 서버의 공개키로 암호화하여 전송.
5. **Master Secret Generation**: 클라이언트와 서버는 각자의 Random과 Pre-Master Secret을 혼합하여 **Master Secret**을 생성.
6. **Finished**: Master Secret으로부터 세션 키(Session Key)를 파생시키고, 이를 통해 "Finished" 메시지를 암호화하여 교환. 성공 시 데이터 전송 시작.

**핵심 알고리즘: Pseudo-Random Function (PRF)**
세션 키 생성은 수학적 난수 생성 함수에 의존한다.

```python
# [Pseudo Code] Master Secret 계산 (TLS 1.2 표준)
# PRF(Pseudo-Random Function) 함수를 사용해 난수들을 혼합

def generate_master_secret(pre_master_secret, client_random, server_random):
    seed = client_random + server_random
    # PRF 함수는 해시 함수(SHA256 등)를 반복 적용하여 확장된 키 생성
    master_secret = PRF(secret=pre_master_secret, label="master secret", seed=seed, output_length=48)
    return master_secret

# 생성된 Master Secret은 데이터 암호화를 위한 
# Client Write Key(송신용)와 Server Write Key(수신용)로 파생됨.
```

**ASCII 다이어그램: 키 파생(Key Derivation) 구조**

```ascii
[ 난수 Pool ]
              +-----------------+
              | Pre-Master      | <-- (공개키 암호화로 안전하게 교환)
              | Secret          |
              +--------+--------+
                       |
          +------------v-------------+
          |   PRF (Pseudo Random    |
          |    Function) Mixing     |
          +------------+-------------+
                       |
            +----------v----------+
            |  Master Secret (48B)|
            +----------+----------+
                       |
      +----------------+----------------+
      |                                 |
+-----v-----+                     +-----v-----+
| Client    |                     | Server    |
| Write Key |                     | Write Key |
+-----------+                     +-----------+
(데이터 송신 암호화)              (데이터 수신 복호화)
```

*(해설: Master Secret은 마치 하나의 '마스터 열쇠'와 같으며, 여기서 실제 통신에 쓰이는 송신용/수신용 키가 뻗어 나온다. 이 과정에서 단방향 해시 함수가 사용되어 역추적이 불가능하다.)*

> **📢 섹션 요약 비유**: TLS 핸드셰이크는 두 사람이 **'일회용 비밀 통신 코드북'**을 만드는 과정입니다. 첫 만남에서는 복잡한 절차(핸드셰이크)를 거쳐 신원을 확인하고 코드북을 만들지만, 그 후에는 그 코드북만 보고 눈치껏 빠르게 대화하는 것과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

TLS는 단순히 암호화만 제공하는 것이 아니라, TCP 네트워크의 흐름 제어와 애플리케이션의 성능(웹 로딩 속도) 사이에서 상충 관계(Trade-off)를 조율해야 하는 기술이다.

**심층 기술 비교표: TLS 버전 및 암호화 알고리즘**

| 구분 | TLS 1.0 / 1.1 | TLS 1.2 (Legacy) | **TLS 1.3 (Modern)** |
|:---|:---:|:---:|:---:|
| **핸드셰이크 지연** | 2-RTT | 2-RTT | **1-RTT** (데이터 동시 전송) |
| **Key Exchange** | RSA, DH, ECDH | ECDHE (권장) | **ECDHE / PSK** (강제) |
| **암호화 방식** | CBC (Block) | CBC, GCM (AEAD) | **AEAD (GCM, ChaCha20-Poly1305) 만 허용** |
| **PFS (전방향 안전성)** | 지원 안함(RSA Key Exchange 시) | 지원 (ECDHE 사용 시) | **기본 지원 (강제)** |
| **보안 취약점** | BEAST, POODLE 등 다수 | RC4, CBC 관련 이슈 | **취약한 알고리즘 완전 제거** |

**과목 융합 관점 분석**
1.  **네트워크 (TCP)와의 관계**: TLS는 **Connection-Oriented**인 TCP 위에서만 정상 작동한다(UDP 위 구현은 DTLS). TCP의 3-Way Handshake(1-RTT)가 완료된 후 TLS Handshake가 추가로 수행되므로, 초기 연결 설정 시 **최소 3-RTT**의 지연이 발생한다. 이를 해결하기 위해 **TCP Fast Open**이나 **TLS 1.3**의 핸드셰이크 축소가 필수적이다.
2.  **컴퓨터 구조 (CPU)와의 관계**: 암호화 연산(AES-GCM 등)은 CPU 자원을 많이 소모한다. 따라서 현대 서버는 이러한 연산을 전용 하드웨어인 **AES-NI (Advanced Encryption Standard New Instructions)** 명령어 셋으로 오프로딩하여 CPU 부하를 줄인다.
3.  **보안 (Cryptography)과의 관계**: 단순히 키를 교환하는 것을 넘어 **인증서 기반의 PKI (Public Key Infrastructure)** 생태계와 연결된다. 루트 CA의 신뢰가 무너지면 TLS 자체의 신뢰도 붕괴하므로, CRL (Certificate Revocation List)이나 **OCSP (Online Certificate Status Protocol)** 검증 과정이 필수적이다.

**ASCII 다이어그램: TLS 1.2 vs TLS 1.3 핸드셰이크 비교**

```ascii
[TLS 1.2 (2-RTT Latency)]

Client -------(1) Client Hello------> Server
Client <------(2) Server Hello-------
             (Certificate, Server Hello Done)
Client -------(3) Client Key Exchange> Server
             (Change Cipher Spec, Finished)
Client <------(4) Change Cipher Spec- Server
             (Finished)
Client ================= (Application Data) =================> Server


[TLS 1.3 (1-RTT Latency, Optimized)]

Client -------(1) Client Hello--------> Server
             [Key Share included!]     (Server can calculate key now)
Client <------(2) Server Hello-------- Server
             [Key Share, Finished]
Client ======= (3) Application Data =======> Server
             (No separate wait for Finished!)
```

*(해설: TLS 1.3은 첫 번째 메시지에 키 교환용 파라미터(Key Share)를 포함하여 보냄으로써, 서버가 응답할 때 즉시 데이터를 함께 보낼 수 있게 하여 왕복 횟수를 획기적으로 줄였다.)*

> **📢 섹션 요약 비유**: TLS 1.2는 "초대장을 보내고, 답장이 오면 초대장을 가지고 입장권을 교환하고, 그제야 입장"하는 절차가 복잡한 **'VIP 라운지'**였다면, TLS 1.3은 "초대장과 입장권을 동시에 제시하자마자 바로 통과"하는 **'무인 초고속 터미널'**과 같습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 환경에서 TLS는 단순히 "켜는 것(Enable)"이 아니라, 어떤 Cipher Suite를 선택하고 어떤 정책을 적용할지가 서버의 성능과 보안 안전성(Safety)을 좌우한다.

**실무 시나리오: 대규모 전자상거래 사이트 TLS 구축**
*   **상황**: 글로벌 트래픽이 몰리는 쇼핑몰에서 SSL/TLS 처리로 인해 웹 서버(WAS)의 CPU 사용률이 90%를 넘어 응답 지연이 발생함.
*   **의사결정 과정**:
    1.  **하드웨어 가속**: 서버 CPU가