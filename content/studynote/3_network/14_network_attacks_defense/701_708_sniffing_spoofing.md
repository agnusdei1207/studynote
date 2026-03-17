+++
title = "701-708. 네트워크 기만 공격: 스니핑과 스푸핑"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 701
+++

# 701-708. 네트워크 기만 공격: 스니핑과 스푸핑

> **핵심 인사이트**: 네트워크 보안의 근간은 '신뢰(Trust)'에 있다. 공격자는 이 신뢰를 무너뜨리기 위해 스니핑(Sniffing)으로 정보를 수집하고, 스푸핑(Spoofing)으로 신분을 위장하며, 세션 하이재킹(Session Hijacking)으로 권한을 탈취한다. 이는 L2~L7 계층의 프로토콜 취약점을 악용한 지능적인 공격 기법이다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
네트워크 기만 공격은 **MITM (Man-in-the-Middle, 중간자 공격)**의 일종으로, 송신자와 수신자 사이의 통신을 몰래 가로채거나(Method Interception), 통신의 주체를 사칭하여(Message Spoofing) 정보를 탈취하는 행위를 말한다. 크게 **스니핑(Sniffing)**과 **스푸핑(Spoofing)**으로 나뉘며, 이를 기반으로 **세션 하이재킹(Session Hijacking)**이 발생한다.

#### 2. 기술적 배경 및 원리
인터넷 프로토콜의 초기 설계는 **'데이터의 효율적 전달'**에 초점을 맞추었지, **'보안(Security)'**은 고려하지 않았다. 따라서 이더넷 프레임이나 IP 패킷의 출발지 주소(Source Address)는 사용자가 마음대로 조작할 수 있는 구조를 가지고 있다. 공격자는 이러한 **'신뢰할 수 없는 주소 필드'**의 취약점을 악용하여 네트워크 스위치나 라우터의 MAC 주소 테이블(MAC Table), ARP 캐시, DNS 캐시 등을 오염(Poisoning)시킨다.

#### 3. 비즈니스 파급 효과
*   **정보 유출**: 스니핑을 통해 암호화되지 않은 패스워드, 신용카드 정보, 이메일 내용 등이 탈취될 수 있다.
*   **시스템 장악**: 스푸핑을 통해 신뢰하는 서버에 접속하여 악성코드를 심거나 백도어를 설치한다.
*   **금융 사고**: 피싱 사이트로의 연결 유도(DNS 스푸핑)로 인한 2차 금융 피해 발생.

> **💡 비유**
> **스니핑**은 우체통에 손을 넣어 편지를 몰래 훔쳐보는 것이고, **스푸핑**은 택배 기사에게 "이 집 주인이 바뀌었으니 앞으로는 모든 택배를 내 집으로 줘"라고 거짓 주소를 알리는 것과 같습니다.

📢 **섹션 요약 비유**: 인터넷 고속도로에서 스니핑은 '도로 위의 모든 차량 내부를 훔쳐보는 감시 카메라'를 설치하는 것이고, 스푸핑은 '유료 하이패스 차로를 이용하기 위해 번호판을 위조하는 행위'에 비유할 수 있습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 스니핑 (Sniffing) 동작 메커니즘
스니핑은 네트워크 인터페이스를 **프라미스큐어스 모드(Promiscuous Mode, 혼합 모드)**로 설정하여 동작한다.

*   **Normal Mode**: 자신의 **MAC (Media Access Control)** 주소가 아닌 프레임은 NIC (Network Interface Card) 계층에서 폐기한다.
*   **Promiscuous Mode**: 자신의 MAC 주소가 아니더라도 전달되는 모든 프레임을 CPU로 전달하여 분석한다.

```ascii
[스위칭 환경에서의 스니핑 흐름]

   [ Attacker ]                           [ Switching Hub ]
        |                                      (CAM Table)
        | 1. Promiscuous Mode ON                    |
        +<------------------------------------------+
        | 2. ARP Spoofing / Flooding으로 스위치 학습 방해
        |
        v
   (모든 트래픽을 복사하여 수신)
```

#### 2. 스푸핑 (Spoofing) 기술 상세 분석
스푸핑은 프로토콜 스택의 신뢰성을 이용한다. 주요 유형별 상세 분석은 다음과 같다.

| 구분 | 대상 프로토콜 | 핵심 공격 벡터 (Vector) | 방어 기술 (Countermeasure) |
|:---:|:---:|:---|:---|
| **ARP Spoofing** | **ARP (Address Resolution Protocol)** | ARP Reply(Gratuitous ARP)를 스누핑하여受害者의 ARP Table 공략 | Static ARP, **DAI (Dynamic ARP Inspection)** |
| **IP Spoofing** | **IP (Internet Protocol)** | 패킷 헤더의 Source IP를 위조하여 필터링 우회 | **Ingress Filtering** (입구 필터링), uRPF |
| **DNS Spoofing** | **DNS (Domain Name System)** | DNS Query ID를 추측하여 가짜 응답 전송 (Cache Poisoning) | **DNSSEC (DNS Security Extensions)** |

**① ARP 스푸핑 심층 분석**
가장 흔한 형태의 LAN 내부 공격이다. 해커(K)는 **"나는 게이트웨이(G)다"**라고 피해자(V)에게 알리고, **"나는 피해자(V)다"**라고 게이트웨이(G)에게 알려 **양방향 MITM**을 구축한다.

```ascii
[ARP Spoofing Traffic Flow]

 [ Victim PC ]      [ Hacker (Attacker) ]      [ Gateway (ISP) ]
      |                      ^  ^                      ^
      | (Original: Dest GW)  |  | (Original: Dest V)   |
      v                      |  |                      v
      <----------------------+--+----------------------> 
       (Hacker MAC으로 스누핑)  (Re-routing / Relay)
       
 * ARP Cache State
   - Victim Table: Gateway IP -> Hacker MAC
   - Gateway Table: Victim IP -> Hacker MAC
```

**② TCP Sequence Number Prediction (세션 하이재킹)**
TCP 통신은 **3-Way Handshake** 이후 **ISN (Initial Sequence Number)**을 기반으로 데이터를 주고받는다. 공격자는 ISN을 추측하여 `ACK` 패킷을 위조하고, 정상적인 사용자의 세션을 끊거나(RST), 자신이 정상 사용자인 것처럼 세션을 탈취한다.

> **[코드 스니펫] ARP 스푸핑 공격 로직 (Pseudo Code)**
> ```python
> # ARP Spoofer Logic
> def arp_poison(target_ip, gateway_ip, attacker_mac):
>     # 1. Construct Fake ARP Reply
>     # target에게 "Gateway IP는 나(Attacker)의 MAC 주소다"라고 알림
>     packet = Ether() / ARP(
>         op="is-at",          # ARP Reply
>         pdst=target_ip,      # Target IP
>         psrc=gateway_ip,     # Spoofed IP (Gateway)
>         hwsrc=attacker_mac   # Real MAC (Attacker)
>     )
>     # 2. Send continuously to keep entry in ARP Table
>     sendp(packet, inter=2, loop=1)
> ```

📢 **섹션 요약 비유**: 스니핑은 '돋보기를 들고 남의 휴대폰 화면을 훔쳐보는 행위'이고, ARP 스푸핑은 '친구에게 내가 '교무실 선생님'이라고 믿게 만들어 전달되는 쪽지를 모두 내가 먼저 읽고 전달해주는 중간 역할을 자처하는 것'과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 계층별(Layer-by-Layer) 공격 기법 비교
OSI 7계층 관점에서 공격 기법을 분석하면 상호 보완적 관계를 파악할 수 있다.

| 계층 (Layer) | 공격 유형 | 핵심 파라미터 | 융합 시너지 (Synergy) |
|:---:|:---|:---|:---|
| **L2 (Data Link)** | **ARP Spoofing** | MAC Address, ARP Table | L3 IP Spoofing 시 실제 트래픽 수집을 위한 기반 마련 |
| **L3 (Network)** | **IP Spoofing** | Source IP Address | DDoS Botnet이나 Reflection 공격의 출처 은폐 수단 |
| **L7 (Application)** | **DNS Spoofing** | Domain Name -> IP Mapping | 사용자의 의도를 변조하여 Phishing 사이트로 유도 |

#### 2. 심층 기술 비교: Sniffing vs Spoofing
| 비교 항목 | 스니핑 (Sniffing) | 스푸핑 (Spoofing) |
|:---|:---|:---|
| **행위 성격** | 수동적 (Passive) - 감시 | 능동적 (Active) - 개입 |
| **발견 난이도** | 높음 (트래픽 패턴 변화 없음) | 중간 (ARP Table 오염 감지 가능) |
| **주요 위험** | 정보 노출 (Credential Leak) | 데이터 변조, 세션 탈취 |
| **주요 대응** | 포트 보안(Port Security), 암호화(SSL/TLS) | 인증 메커니즘 강화, 정적 라우팅 |

#### 3. 타 과목 융합 분석
*   **(보안/운영체제) 융합**: 리눅스 커널 레벨에서 **`netfilter`** 후킹을 통해 내부 시스템에서의 스니핑을 방지하거나, **SELinux** 정책을 통해 네트워크 소켓 권한을 제어해야 한다.
*   **(데이터베이스) 융합**: DB 서버로의 접근 로그가 해커에 의해 스푸핑당할 경우, **감사 로그(Audit Log)**가 변조될 수 있으므로 DB 접근 시에도 **SSH 터널링**이나 **VPN (Virtual Private Network)**을 강제해야 한다.

📢 **섹션 요약 비유**: '스니핑'은 '숨어서 잠복하는 저격수'라면, '스푸핑'은 '적군의 군복을 입고 침투하는 간첩'입니다. 이 둘이 합쳐질 때('하이재킹')는 간첩이 침투해 문을 열어주고 저격수가 총을 쏘는 치명적인 타격을 줍니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 (Decision Matrix)
**상황**: 금융권 본사 망에서 내부 직원 PC의 트래픽이 의심스러운 서버로 유출되는 정황이 포착됨.

| 문제 상황 | 의사결정 포인트 | 기술적 판단 (Decision) | 이유 (Rationale) |
|:---|:---|:---|:---|
| **1단계** | 스니핑 탐지 | **스위치 SPAN/Mirroring 포트 설정** | 스위치가 해커의 패킷 복사를 요청하는지 확인하기 위해 트래픽 복사 분석 수행 |
| **2단계** | 근본적 차단 | **DAI (Dynamic ARP Inspection) 및 IP Source Guard 활성화** | DHCP Snooping DB를 기반으로 ARP 패킷과 IP 패킷의 출처를 검증하여 L2/L3 위장 차단 |
| **3단계** | 예방적 조치 | **802.1X 포트 기반 인증(NAC) 도입** | 단말 인증 없이는 포트가 활성화되지 않도록 하여 미인증 단말의 스니핑 시도 원천 봉쇄 |

#### 2. 도입 체크리스트 (Security Checklist)
*   [ ] **네트워크 장비 설정**
    *   스위치 포트별 `port security` 설정으로 MAC 주소 잠금 (Sticky MAC)
    *   DHCP Snooping을 통한 신뢰할 수 있는 포트(DHCP Server 포트)만 허용
*   [ ] **통신 암호화**
    *   내부 통신 및 외부 통신 모두 **SSH**, **SFTP**, **HTTPS (TLS 1.3)** 사용 강제
    *   스니핑으로 인한 데이터 유출 시에도 내용을 알 수 없도록 End-to-End 암호화
*   [ ] **시스템 강화**
    *   방화벽의 **Ingress/Egress Filtering** (들어오고 나가는 패킷의 Source IP 검증) 규칙 적용

#### 3. 안티패턴 (Anti-Patterns)
*   **에러**: "허브(Hub)는 스니핑 위험이 있으니 스위치로 교체했으니 안전하다."
    *   **수정**: 스위치 환경에서도 ARP 스푸핑을 통해 스위치를 우회하여 스니핑할 수 있음을 인지해야 한다.
*   **에러**: "DNS 서버에 방화벽을 설치했으니 DNS 스푸핑이 불가능하다."
    *   **수정**: 내부 네트워크에 감염된 PC가 Botnet이 되어 내부 DNS 서버를 공격하거나, Cache Poisoning을 시도할 수 있음을 고려하여 DNSSEC 도입이 필요하다.

📢 **섹션 요약 비유**: 방어는 단순히 벽을 높이 쌓는 것(스위치 도입)이 아니라, 출입구마다 **신분증을 확인하는 경비원(802.1X, DAI)**을 배치하고, **서류 내용을 암호화(SSL/TLS)**하여 운반하는 것과 같습니다.

+++

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과
네트워크 기만 공격 방어 체계 구축 시 다음과 같은 효과를 기대할 수 있다.

| 구분 | 도입 전 (Before) | 도입 후 (After) |
|:---|:---|:---|
| **기밀성** | 평문 트래픽 노출 시 정보 탈취 확률 **100%** | 암호화 및 스푸핑 차단으로 탈취 위험 **90% 이상 감소** |
| **무결성** | 패킷 변조 가능 (RST Injection 등) | DAI/IPSG로 인한 변조 불가능성 확보 |
| **가용성** | ARP 스푸핑에 의한 네트워크 불안 정기적 발생 | Stable Network, 신뢰할 수 있는 통신 경로 확보 |

#### 2. 미래 전망 및 표준
*   **AI 기반 탐지**: 일정한 패턴을 가진 ARP 스푸