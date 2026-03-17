+++
title = "518-521. 보안 DNS와 로컬 이름 해석 (DNSSEC, DoH, mDNS)"
date = "2026-03-14"
[extra]
category = "DNS & Management"
id = 518
+++

# 518-521. 보안 DNS와 로컬 이름 해석 (DNSSEC, DoH, mDNS)

> **핵심 인사이트**
> 1. **본질**: DNS (Domain Name System)의 기본 설계 상 취약점인 '평문 통신' 및 '무결성 미보장'을 해결하기 위해 **DNSSEC (DNS Security Extensions)**는 무결성을, **DoH/DoT (DNS over HTTPS/TLS)**는 기밀성을 보장한다.
> 2. **가치**: 캐시 포이즈닝 등 공격을 원천 차단하여 신뢰할 수 있는 라우팅을 확립하고, 사용자의 조회 이력을 타인이 볼 수 없게 하여 **프라이버시(Privacy)**를 강화한다.
> 3. **융합**: 보안 아키텍처(PKI)와의 결합, 네트워크 성능(Latency)과의 트레이드오프 관계, 그리고 IoT 환경에서의 **mDNS (Multicast DNS)** 및 **LLMNR (Link-Local Multicast Name Resolution)**을 통한 자동화된 서비스 발견(Service Discovery)이 핵심이다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 개념 및 철학
전통적인 DNS (Domain Name System)는 인터넷의 전화번호부 역할을 하지만, 기본적으로 신뢰를 전제로 설계되었고 암호화되지 않은 평문(Clear Text) 프로토콜(UDP/53)을 사용한다. 이로 인해 두 가지 치명적인 약점이 존재한다.
1.  **스푸핑(Spoofing) 취약성**: 중간자(Man-in-the-Middle)가 가짜 응답을 보내면 클라이언트가 이를 진짜로 받아들여 악성 사이트로 유도될 수 있다. (예: 캐시 포이즈닝)
2.  **프라이버시 침해**: ISP (Internet Service Provider)나 네트워크 관리자가 사용자가 방문하는 사이트의 도메인(DNS Query)을 손쉽게 도청할 수 있다.

이를 해결하기 위해 등장한 기술들이 DNSSEC, DoH, DoT이다. DNSSEC은 응답의 **무결성(Integrity)**과 **진위성(Authenticity)**을 보장하고, DoH/DoT는 통신 내용의 **기밀성(Confidentiality)**을 보장한다. 또한, 서버가 없는 소규모 네트워크에서는 mDNS와 LLMNR이 분산형 이름 해석을 담당한다.

#### 💡 비유: 낯선 도시에서의 길 묻기
기존 DNS는 거리에서 무작위 사람에게 길을 묻는 것과 같다. (누구나 대답할 수 있고, 누가 들을지 모름) DNSSEC은 정부에서 발급한 자격증을 목에 건 가이드의 답변만 믿는 것이다. DoH/DoT는 길을 물을 때 속삭여서 옆 사람에게는 무슨 말을 하는지 알 수 없게 하는 것이다.

#### 등장 배경
① **기존 한계**: 2008년 'Kaminsky Attack'으로 대표되는 DNS 캐시 포이즈닝 취약점이 전 세계적으로 공개되며 DNS 스푸핑의 심각성 대두.
② **혁신적 패러다임**: 공개키 기반 구조(PKI)를 DNS 계층에 도입하여 '신뢰의 사슬(Chain of Trust)' 형성 및 TLS 1.3 기반의 암호화 프로토콜 적용.
③ **현재의 비즈니스 요구**: GDPR 등 개인정보 보호 법규 강화와 ISP의 추적 차단 및 검열 회피(IP Cloaking) 요구 증대.

> **📢 섹션 요약 비유**: DNS 보안 기술의 진화는 마치 집의 잠금 장치가 **'단순 현관문 초인종(평문 DNS)'에서 시작하여, **'방문자 신원 확인 시스템(DNSSEC)'을 거쳐, 최근에는 **'두꺼운 음성 방음 부스(DoH/DoT)'를 설치하여 밖에서 대화 내용이 전혀 들리지 않도록 만드는 보강 공사와 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 구성 요소 상세 분석

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비고/비유 |
|:---|:---|:---|:---|
| **DNSSEC** | 응답 무결성 검증 | ZSK(Zone Signing Key)로 RRSET 서명, KSK(Key Signing Key)로 ZSK 서명. **RRSIG** 레코드 사용. | 공인인증서 계층 구조 |
| **DoT (DNS over TLS)** | 채널 암호화 (전용) | **TCP 853** 포트 사용. TLS 핸드셰이크 후 DNS 메시지 교환. 별도 포트 때문에 식별 용이. | VPN과 유사한 전용 터널 |
| **DoH (DNS over HTTPS)** | 채널 암호화 (위장) | **TCP 443** 포트(HTTPS) 사용. DNS 메시지를 HTTP POST의 JSON/Payload로 encapsulation. | 일반 웹 트래픽에 위장 |
| **mDNS** | 로컬 이름 해석 | **UDP 5353**, IPv4 **224.0.0.251**, IPv6 **ff02::fb** 멀티캐스트. `.local` 도메인 사용. | 소규모 마을의 방송 |
| **LLMNR** | 윈도우 로컬 해석 | **UDP 5355**. Link-Local 멀티캐스트(224.0.0.252). NetBIOS 대체제. | 윈도우 전용 구내 방송 |

#### 2. 아키텍처 다이어그램 및 데이터 흐름

아래는 DNSSEC 검증 과정과 DoH/DoT의 패킷 캡슐화를 시각화한 것이다.

```ascii
[ A. DNSSEC Chain of Trust (신뢰의 사슬 구조) ]

  [ Root Zone ] (.)  <-- Trust Anchor
         |  signed by (Root KSK)
         v
  [ TLD Server ] (.com) <-- holds DS Record for example.com
         |  signed by (TLD ZSK)
         v
  [ Zone Server ] (example.com)
         |  signed by (Zone ZSK)
         +--- [ RRSET: A=1.2.3.4 ] + [ RRSIG (Signature) ]
         |
         v
  [ Resolver/Client ] : (검증 과정)
      1. Response 받음
      2. Root Public Key로 TLD Key 검증
      3. TLD Key로 Zone Key 검증
      4. Zone Key로 A Record 서명(RRSIG) 검증
      -----------------------------------
      [ B. DoH Encapsulation (암호화 계층) ]

      [ Network Layer (IP) ]
         |
      [ Transport Layer (TCP) ]  <-- Port 443
         |
      [ Security Layer (TLS 1.3) ] <-- 🔒 Encryption (Handshake)
         |
      [ Application Layer (HTTP/2) ] <-- Header: "Content-Type: application/dns-message"
         |
      [ DNS Message (Query/Response) ] <-- UDP Wire format inside body
```

#### 3. 심층 동작 원리 및 메커니즘

**① DNSSEC의 서명 및 검증 (Signing & Validation)**
DNSSEC은 기존 레코드(RRSET)에 **RRSIG (Resource Record Signature)** 레코드를 추가한다. 이 서명은 비대칭 키 알고리즘(RSA/SHA-256 또는 ECDSA)을 사용한다. 상위 서버는 하위 영역의 공개키 해시값을 담은 **DS (Delegation Signer)** 레코드를 제공하여, 하위 키가 신뢰할 수 있는 것임을 보증한다. 클라이언트(Resolver)는 이 사슬을 따라 내려가며 최종적으로 자신이 가진 신뢰의 출처(Trust Anchor)까지 검증한다.

**② DoH vs DoT의 세션 설정**
-   **DoT (RFC 7858)**: 전용 포트 **853**으로 연결 시도. TLS Handshake가 완료되면 전체 채널이 암호화된다. 네트워크 방화벽에서 'DNS-over-TLS'로 식별하여 차단하거나 우선순위를 조정하기 쉽다.
-   **DoH (RFC 8484)**: 표준 **HTTPS(443)** 포트 사용. 미들박스(방화벽, 프록시) 입장에서 일반 웹 서핑(YouTube, Netflix 등)과 전혀 구분할 수 없다. 이는 검열 회피(Censorship Circumvention)에 유리하지만, 기업 보안 관점에서는 악의적인 DNS 통신(C2 Server Communication)을 감지하기 어렵게 만든다.

**③ mDNS (Multicast DNS) 동작**
로컬 네트워크의 장치는 별도의 DNS 서버 없이 `.local` 도메인을 사용한다. 장치 A가 `printer.local`을 찾고 싶으면, 네트워크 전체에 **`224.0.0.251:5353`**으로 질의 패킷을 멀티캐스트한다. 해당 이름을 가진 장치 B가 이를 수신하면 자신의 IP 주소를 **유니캐스트**로 응답한다.

#### 4. 핵심 코드 및 수식 (Wire Format)

DNSSEC 검증 로직(의사코드):
```python
def validate_dnssec(response, trust_anchor):
    # 1. Response에 RRSIG 레코드가 있는지 확인
    if not response.rrsig: return False

    # 2. 현재 시간이 서명 유효 기간(Inception ~ Expiration) 내인지 확인
    current_time = now()
    if not (response.rrsig.inception <= current_time <= response.rrsig.expiration):
        return False

    # 3. 상위 키(Key Tag)를 통해 서명자의 공개키 찾기
    signer_key = get_key_from_ksk(response.rrsig.key_tag)

    # 4. 서명 검증 (Verify Signature)
    # verify(data, signature, public_key)
    is_valid = crypto_verify(response.rrset, response.rrsig.signature, signer_key)
    
    # 5. 재귀적으로 상위 DS 레코드와 대조 (Chain of Trust)
    return is_valid and validate_ds_against_parent(signer_key)
```

> **📢 섹션 요약 비유**: DNSSEC은 **'공증된 계약서'**와 같아서, 내용이 조금이라도 변경되면 서명이 맞지 않아 종이조각이 됩니다. DoH는 **'은행 금고 트럭'**처럼 내용물을 볼 수 없게 운반하는 것이고, mDNS는 **'장터에서 큰 소리로 물건 찾기'**처럼 내 주변에 있는 사람들에게만 소리쳐 물어보는 방식입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교표 (DoT vs DoH)

| 구분 | **DoT (DNS over TLS)** | **DoH (DNS over HTTPS)** |
|:---|:---|:---|
| **표준 RFC** | RFC 7858 | RFC 8484 |
| **전송 계층** | TLS 1.3 over TCP | TLS 1.3 over HTTP/2 over TCP |
| **사용 포트** | **853** (전용) | **443** (HTTPS 재사용) |
| **식별 용이성** | 용이함 (포트 기반 필터링 가능) | **어려움** (일반 HTTPS와 혼재) |
| **오버헤드** | 상대적으로 낮음 (TLS만 추가) | 상대적으로 높음 (HTTP Header 오버헤드) |
| **주요 용도** | ISP/기업 내 보안 DNS 채널 구성 | 검열 회피, 사용자 프라이버시 강화 |
| **대표 서비스** | Cloudflare, Quad9 (일부) | Google Chrome, Firefox (기본 지원) |

#### 2. 과목 융합 관점 (Security & OS & IoT)

-   **보안(Security) 융합**: DNSSEC은 **PKI (Public Key Infrastructure)** 아키텍처를 그대로 따르므로, 인증서 관리 및 키 롤오버(Key Rollover) 전략이 필수적이다. KSK(키 사이닝 키) 롤오버 시 인터넷 루트 영역이 마비되지 않도록 신중한 절차가 필요하다.
-   **운영체제(OS) 융합**:
    -   **macOS/iOS**: Bonjour(mDNS)를 핵심 컴포넌트로 사용하여 AirDrop, 프린터 자동 발견 수행.
    -   **Windows**: LLMNR을 사용하며, NBT-NS(NetBIOS)가 실패할 때 폴백(Fallback) 메커니즘으로 작동. (※ 보안 위험: NBT-NS/LLMNR Spoofing을 통한 해시 전달 공격에 취약함)
-   **성능(Performance) 고려**: DoH/DoT는 **Connection Reuse**를 통해 오버헤드를 줄인다. TCP 3-way 핸드셰이크와 TLS 핸드셰이크로 인한 초기 Latency가 존재하므로, UDP 53을 사용하는 기존 DNS보다 첫 번째 응답 속도가 느릴 수 있다. 따라서 성능 민감 서비스는 **Performance Considerations**가 필요하다.

> **📢 섹션 요약 비유**: DoT와 DoH의 선택은 **'고속도로 진입 방식'**과 같습니다. DoT는 **'요금소 전용 차선'**을 이용해 빠르게 통과하지만 도로관청(ISP)에서 내가 무엇을 싣고 가는지 알기 쉽습니다. DoH는 **'일반 차량들 섞여서 다니는 일반 차선'**을 이용해 무엇을 싣고 가는지 숨기지만, 차량이 많아서(헤더 오버헤드) 연료 조금 더 듭니다. mDNS는 **'주차장에서 키를 잃어버리고 비상등을 켜고 자동차 찾는 것'**과 같습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**시나리오 A: 금융권 보안 강화**
-   **상황**: 보안 팀에서 내부 직원의 DNS 변조 우려 및 고객 정보 유출 방지 필요.
-   **의사결정**:
    1.  **내부 DNS 서버**는 **DNSSEC Validating Resolver**로 구성하여 외부 응답 검증.
    2.  **사내 PC**는 내부 DNS 서버로의 **DoT(혹은 VPN 내부)**를 강제하여 ISP 감시 차단.
    3.  포트 853을 화이트리스팅하고 나머지는 차단.
-   **이유**: 금융권은 방화벽 정책 관리가 중요하므로, 식별이 용이한 DoT가 관리에 유리함.

**시나리오 B: 공공