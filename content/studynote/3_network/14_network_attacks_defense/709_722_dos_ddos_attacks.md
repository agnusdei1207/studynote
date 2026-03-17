+++
title = "709-722. 서비스 거부 공격 (DoS/DDoS) 분석"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 709
+++

# 709-722. 서비스 거부 공격 (DoS/DDoS) 분석

### # 핵심 인사이트 (3줄 요약)
> 1. **본질**: DoS (Denial of Service)는 시스템의 정보 무결성이 아닌 **가용성(Availability)**을 타겟으로 하여, 자원 고갈(Resource Exhaustion)이나 논리적 결함을 유발하여 서비스를 중단시키는 공격입니다.
> 2. **가치**: 공격 대역폭과 규모가 기가(G)급에서 테라(T)급으로 비대해지며, **DRDoS (Distributed Reflection DoS)**와 같은 증폭 기술은 최소 1,000배 이상의 대역폭 리턴률(Bandwidth Multiplier)을 야기하여 기업의 운영 영향을 비약적으로 증폭시킵니다.
> 3. **융합**: 단순한 트래픽 폭주를 넘어, **OS (Operating System)**의 TCP/IP 스택 취약점, **애플리케이션 계층(L7)**의 세션 관리 로직, 그리고 **네트워크 장비**의 처리 한계를 복합적으로 공략하는 다층(Layer 3~7) 위협으로 진화하고 있습니다.

+++

### Ⅰ. 개요 (Context & Background) - DoS/DDoS의 정의와 철학

**개념**
서비스 거부 공격(Denial of Service)은 시스템의 정상적인 사용자가 서비스를 이용하지 못하게 하거나, 시스템의 기능을 저하시키는 공격을 의미합니다. 단일 공격자에 의한 공격을 DoS라고 하며, 다수의 좀비 PC(Botnet)를 이용해 분산적으로 수행하는 공격을 DDoS(Distributed DoS)라고 칭합니다. 이는 데이터를 탈취하는 것이 목적이 아니라, '서비스 불가' 상태를 강제하여 비즈니스 연속성을 파괴하는 데 있습니다.

**💡 비유**
편의점 문을 잠그고 손님의 출입을 막는 것이 아니라, 계산원 없이 물건만 던져주는 쇼핑 고객 수만 명을 몰아넣어 계산대를 마비시키는 '무료 나눔 행사'로 위장한 방해 공작입니다.

**등장 배경**
1.  **기존 한계**: 초기 인터넷은 신뢰할 수 있는 사용자 간의 통신을 전제로 설계되어, 프로토콜 자체에 무분별한 요청을 제어할 인증 메커니즘이 부족했습니다.
2.  **혁신적 패러다임**: 해커들은 시스템을 파괴하기보다 시스템이 가진 '동시 처리 가능한 연결 수'나 '대역폭'이라는 한정된 자원을 소진시키는 것이 훨씬 효과적임을 깨달았습니다.
3.  **현재의 비즈니스 요구**: 클라우드와 5G 시대로 접어들며, 공격 대상이 웹 서버에서 IoT(사물인터넷) 기기까지 확장되었고, 랜섬웨어와 결합한 '랜섬 DDoS' 형태로 금전적 extortion(협박)의 수단으로 악용되고 있습니다.

**📢 섹션 요약 비유**
> 마치 식당 주인을 혼내기 위해 친구들 100명을 시켜 "예약만 하고 나타나지 않기(No-show)"를 반복하여, 식당의 테이블을 모두 막아버려 실제 손님은 입장도 못 하게 만드는 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 네트워크 및 전송 계층(L3/L4)의 핵심 메커니즘을 악용하는 공격과, 자원을 증폭시키는 구조를 심층 분석합니다.

#### 1. 핵심 구성 요소 (표)

| 요소명 | 역할 | 내부 동작 및 공격 포인트 | 관련 프로토콜 | 비유 |
|:---|:---|:---|:---|:---|
| **Attacker (Master)** | 공격 지시자 | C&C (Command & Control) 서버를 통해 Botnet에게 공격 타겟과 명령을 전달 | TCP/UDP | 지하 세계의 보스 |
| **Zombie / Agent** | 공격 실행자 | 감염된 PC나 IoT 기기. 정상 사용자의 패킷으로 위장하여 타겟에 몰려감 | Various | 보스의 지시를 받는 조직원 |
| **Amplifier** | 트래픽 증폭기 | 요청 패킷보다 훨씬 큰 응답 패킷을 반환하는 공개형 서버(DNS, NTP 등) | UDP (주로) | 소리를 키우는 메가폰 |
| **Victim (Target)** | 피해자 | 방화벽이나 서버의 Backlog가 가득 차 정상 트래픽 처리 불가 | ALL | 장사가 망한 식당 |
| **Reflectors** | 반사 경로 | Source IP를 스푸핑하여 공격 트래픽을 타겟에게 우회시킴 | IP | 공범 몰래 이용한 우회 도로 |

#### 2. TCP 3-Way Handshake 악용: SYN Flood

SYN Flood는 TCP (Transmission Control Protocol) 연결 설정 과정인 3-Way Handshake의 취약점을 공격합니다.

**[도입 서술]**
정상적인 TCP 연결은 클라이언트가 `SYN`을 보내면, 서버는 `SYN-ACK`를 보내고 `ESTABLISHED` 상태가 되기 전까지 `SYN_RECV` 대기 큐(Backlog Queue)에 자원을 할당합니다. 공격자는 이 과정에서 3단계인 `ACK`를 보내지 않음으로써, 서버의 대기 큐를 가득 채워버립니다.

```ascii
[SYN Flood 공격 구조]

Attacker                       Victim Server
   |                               |
   |----[SYN A]------------------->| (Allocate Memory in Backlog)
   |                               |----[SYN-ACK A']----> X (Lost/Blocked)
   |                               |   (Waiting ACK...)
   |                               |
   |----[SYN B]------------------->| (Allocate Memory)
   |                               |----[SYN-ACK B']----> X
   |                               |   (Waiting ACK...)
   |    [Repeating Rapidly]        |   [Backlog Queue Full 100%]
   |                               |
   |----[Real User SYN]----------->| X (Drop: Connection Refused)
   |                               |
```

**[해설]**
위 다이어그램에서 공격자는 매우 빠른 속도로 SYN 패킷(A, B...)을 전송합니다. 피해 서버는 각 요청마다 메모리 커널 자원을 할당하고 응답을 보내지만, 공격자는 이를 무시하거나 위조된 IP에서 왔으므로 ACK가 도착하지 않습니다. 결과적으로 서버의 `Backlog`가 가득 차면, 정상적인 사용자(Real User)의 SYN은 'Connection Refused' 또는 응답 없이 버려집니다.

**[기술적 대응: SYN Cookie]**
서버는 SYN을 받을 때 즉시 자원을 할당하는 대신, TCP 옵션 필드에 암호화된 쿠키(Cookie)를 담아 SYN-ACK를 보냅니다. 정상적인 클라이언트가 ACK를 보낼 때 이 쿠키를 되돌려주면, 그때 자원을 할당하여 연결을 완료합니다. 이를 통해 Backlog Overflow를 방지합니다.

#### 3. 증폭 공격 (Amplification Attack)

UDP (User Datagram Protocol)는 연결 지향적이지 않고 소켓 확인이 없으므로, Source IP를 위조하기(Spoofing) 쉽습니다. 이를 이용해 작은 패킷으로 큰 패킷을 유도하는 기법입니다.

```ascii
[Amplification Attack Flow]

1. Request: Query *GetBestPlayers*
   (Size: 60 Bytes)

Attacker (IP: Victim)                 Amplifier (Game Server)
(Spoofed IP)          |                    |
                      |---[UDP Req]------->|
                      |   (Small Packet)   |
                      |                    |---[UDP Res]------------------------------->|
                      |                    | (Huge List: 3000 Bytes)                   | X
                      |                    |                                            |--> Victim
                                                                  (Traffic Ratio: 50x)
```

**[해설]**
공격자는 피해자의 IP를 자신의 Source IP로 위조하여 DNS, NTP, SNMP, Memcached 등의 공개 서버에 요청을 보냅니다. 응답은 피해자에게 향하게 됩니다. 이때 요청 패킷 대비 응답 패킷이 매우 큰 서비스(예: Memcached의 경우 최대 51,000배 증폭 가능)를 악용하면, 공격자는 적은 대역폭으로 피해자에게 엄청난 양의 트래픽을 쏟아부을 수 있습니다.

**📢 섹션 요약 비유**
> 마치 복잡한 고속도로 톨게이트에서, 하이패스 차선(정상 연결)을 이용하려는 차량들 앞에 동전만 던지고 통행권을 얻지 않은 차량(SYN 공격)이 끝없이 진입하여 진입로를 막아버리는 것과 같습니다. 증폭 공격은 내가 편의점에 100원짜리 사탕 한 알을 주문했는데, 편의점이 대신 배달해야 할 주소지에 100만 원어치 짐 보내기를 강요하는 것과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

공격 유형을 네트워크 계층(L3/L4)과 애플리케이션 계층(L7)으로 나누어 기술적 특성을 비교 분석합니다.

#### 1. 심층 기술 비교 (정량적 분석)

| 구분 | Volume-Based Attack (L3/L4) | Protocol/Resource Attack (L7) |
|:---|:---|:---|
| **타겟** | 대역폭(Bandwidth), 네트워크 회선 | 웹 서버 자원(CPU, RAM, DB Connection), Thread |
| **주요 유형** | UDP Flood, ICMP Flood, SYN Flood | HTTP Flood, Slowloris, Slow POST |
| **트래픽 양** | 네트워크 회선을 포화시킬 만큼 매우 큼 (Gbps~Tbps) | 트래픽 양은 적으나 요청 횟수가 많거나 세션 유지 시간이 김 |
| **탐지 난이도** | 비교적 쉬움 (임계치 초과 감지) | 매우 어려움 (정상 트래픽과 유사함) |
| **대응 방식** | **Traffic Scrubbing** (ISP 레벨 필터링), **Rate Limiting** | **WAF (Web Application Firewall)**, Timeout 설정, Challenge/Response |

#### 2. Slowloris 공격의 세부 동작 (L7 Low-and-Slow)

Slowloris는 웹 서버의 최대 동시 연결 수(Max Connections)를 소진시키는 공격입니다.

```ascii
[Slowloris Attack Mechanism]

Attacker                    Web Server (Apache, etc.)
  |                               |
  |---[GET / HTTP/1.1]----------->| (Connection Open: 1/100)
  |---[X-a: b]------------------->|
  |---[X-c: d]------------------->| (Keep-Alive)
  |... (Send Header very slowly) |
  |                               | (Waiting for Header End...)
  |                               |
  |---[GET / HTTP/1.1]----------->| (Connection Open: 2/100)
  |... (Slow Send)                |
```

**[해설]**
정상적인 HTTP 요청은 헤더 전송 후 빈 줄로 끝을 알립니다. Slowloris는 헤더를 끝내지 않고 주기적으로 아주 작은 데이터(불완전한 헤더)만 보냅니다. 서버는 타임아웃(Timeout) 되지 않도록 연결을 유지하며 계속 대기합니다. 공격자가 수천 개의 이런 "잠시 멈춘" 연결을 생성하면, 서버의 Max Client limit에 도달하여 새로운 정상 사용자를 받아들일 수 없게 됩니다.

#### 3. 과목 융합 관점
-   **OS (Operating System)**: SYN Flood 대응을 위해 OS 커널 레벨에서 `tcp_max_syn_backlog` 값 조정 및 SYN Cache 기법이 탑재되어야 합니다.
-   **DB (Database)**: L7 HTTP Flood가 데이터베이스로 연결될 경우, Connection Pool 고갈로 인해 DB 서버까지 다운되는 연쇄 반응(Cascading Failure)이 발생할 수 있습니다.

**📢 섹션 요약 비유**
> 대형 쇼핑몰에 **L3 공격**은 입구를 막아서 아무도 못 들어오게 하는 '물리적 봉쇄'라면, **L7 공격(Slowloris)**은 피팅룸에 들어가 옷만 보고 안 사고 10시간 동안 나오지 않아, 피팅룸을 다 채워버려 다른 고객들이 옷을 못 입어보게 만드는 '교양 없는 점유' 행위와 같습니다. 트래픽 양은 적지만 서비스 자원을 효율적으로 죽입니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실제 현장에서 DDoS를 방어하기 위해서는 네트워크 인프라부터 애플리케이션 설정까지 다층적 방어 전략이 필요합니다.

#### 1. 실무 시나리오 및 의사결정 프로세스

**[시나리오 A: 대규모 DDoS 발생 (50 Gbps 이상)]**
1.  **진단**: NetFlow 분석 결과 특정 국가/ISP에서 오는 UDP/ICMP 트래픽이 회선 대역폭(1 Gbps)의 50배 발생.
2.  **결정**: 온프레미스 방어 장비(Firewall)의 하드웨어 처리 용량 초과로 장비 자체가 다운될 위험이 있음.
3.  **조치**: 즉시 **네트워크 사업자(ISP)** 또는 전문 보안 업체의 **DDoS Cleaning Center(클린존)** 루팅(스크리빙) 서비스로 트래픽을 우회(U-Turn)시킵니다.
4.  **복구**: 정화된 트래픽만 안전한 경로(터널)로 서버로 전달됩니다.

**[시나리오 B: Slowloris(웹 서버 점유) 발생]**
1.  **진단**: Netstat 확인 시 `SYN_RECEIVED` 상태는 적으나, `ESTABLISHED` 상태이자 데이터 전송이 거의 없는 수천 개의 연결이 존재함. IP가 다양함.
2.  **결정**: 트래픽 양은 적으므로 ISP 스크리빙은 무용지물임.
3.  **조치**: 웹