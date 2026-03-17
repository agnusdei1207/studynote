+++
title = "661. 방화벽 (Firewall)"
date = "2026-03-16"
weight = 661
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "방화벽", "Firewall", "iptables", "nftables", "패킷 필터링"]
+++

# 방화벽 (Firewall)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 방화벽(Firewall)은 신뢰할 수 없는 네트워크와 신뢰할 수 있는 네트워크 사이의 경계에서 **보안 정책에 따라 트래픽을 제어**하는 시스템이며, **SPI (Stateful Packet Inspection)** 기술을 통해 연결 지향성을 보장한다.
> 2. **가치**: **최소 권한 원칙 (Principle of Least Privilege)**을 네트워크 레벨에서 구현하여 공격 표면(Attack Surface)을 최소화하고, 무단 접근 시도를 사전에 차단하여 **RTO (Recovery Time Objective)**를 획기적으로 단축시킨다.
> 3. **융합**: 리눅스 커널 레벨의 **Netfilter** 서브시스템을 기반으로 **iptables**부터 현대적인 **nftables**로 진화하고 있으며, **OSI 7계층** 중 L3/L4(네트워크/전송) 계층 필터링의 핵심을 담당한다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**방화벽 (Firewall)**은 네트워크 트래픽을 모니터링하고 제어하는 보안 장치 또는 소프트웨어로, 사전에 정의된 보안 규칙을 기반으로 들어오고 나가는 패킷(Packet)을 허용하거나 차단한다. 물리적 벽화(Firewall)가 불의 확산을 막듯, 디지털 위협의 확산을 막는다는 의미를 담고 있다. 단순한 패킷 필터링을 넘어, 상태 기반 검사(Stateful Inspection), DPI(Deep Packet Inspection), 프록시 기능 등으로 발전해왔다.

#### 2. 💡 비유: '지능형 출입 통제 시스템'
방화벽은 마치 **"고급 보안 시설이 설치된 사무실 건물의 출입구(게이트)"**와 같다. 
- **패킷 필터링**: 출입자의 신분증(IP/Port)만 확인하고 통과시키는 단순 경비원.
- **Stateful**: 출입자가 "들어와서 나가는" 과정을 인지하고 있는 지능형 CCTV 시스템.
- **프록시/WAF**: 출입자의 짐(내용물)까지 직접 검사하는 엑스레이 스캐너.

#### 3. 등장 배경 및 발전 과정
① **초기 패킷 필터링 (1980년대 후반)**: Cisco 등 라우터의 ACL(Access Control List) 기능을 통해 IP 주소와 포트 번호만으로 트래픽을 통제.  
② **상태 기반 검사 (1990년대 중반)**: 단순 헤더 정보뿐만 아니라 TCP 연결의 상태(ESTABLISHED, NEW)를 추적하여 보안성 강화.  
③ **애플리케이션 계층 보안 (2000년대 이후)**: L7(애플리케이션) 페이로드를 분석하는 웹 방화벽(WAF), UTM(United Threat Management)으로 진화.  
현재는 클라우드 환경에 맞춰 가상화된 **Software-Defined Firewall (SD-Firewall)** 및 **NFV (Network Functions Virtualization)** 기술로 통합되는 추세다.

#### 4. 📢 섹션 요약 비유
> 마치 건물의 출입구에 **'보안 검색대'**를 설치하여, 무기(악성코드)를 소지한 사람(공격 트래픽)은 아예 건물 내부(내부 서버)로 진입조차 못하게 막는 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소
방화벽은 크게 **네트워크 인터페이스**, **검사 엔진**, **규칙셋(Ruleset)**으로 구성된다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Network Interface** | 외부/내부/DMZ 구분 | 트래픽의 경로(Routing)를 물리적/논리적으로 분리 | Ethernet, VLAN | 건물의 출입구 문 |
| **Inspection Engine** | 패킷 분석 및 판단 | 규칙셋과 패킷 헤더/페이로드를 매칭하여 결정 | IP, TCP, UDP, ICMP | 경비원의 판단력 |
| **Ruleset (Policy)** | 허용/거부 기준 | 순차적 매칭(First Match) 기반으로 Action 결정 | 관리자 정의 | 보안 규정手册 |
| **State Table** | 연결 상태 추적 | TCP Handshake 및 세션 정보 저장 (SPI) | TCP (3-way handshake) | 방문 기록부 |
| **Logging Module** | 이벤트 기록 | 차단/허용 로그를 시스템 로그로 전송 | Syslog, SNMP | CCTV 녹화기 |

#### 2. 리눅스 방화벽 아키텍처 (Netfilter Hook)
리눅스 커널의 **Netfilter**는 패킷이 커널을 통과하는 지점(Hook)에 개입할 수 있는 프레임워크를 제공한다.

```text
   ┌───────────────────────────────────────────────────────────────┐
   │                    Network Stack (OSI Layers)                 │
   └───────────────────────────────────────────────────────────────┘
   ▲                                                    │
   │ [1. NF_INET_PRE_ROUTING] ─────────────────────────┘
   │ (인터페이스 진입 후 라우팅 전) -> Destination NAT (DNAT) 가능
   │
   │
   ├───────────────────────────────────────────────────────────────┐
   │                    [Routing Decision]                        │
   │      (Local: 내부 프로세스 vs Forward: 다른 인터페이스)       │
   └───────────────────────────────────────────────────────────────┘
   │                       │                       │
   │ [2. NF_INET_LOCAL_IN] │                       │ [3. NF_INET_FORWARD]
   │ (내부로 들어옴)        │                       │ (통과/Forwarding)
   │                       │                       │
   │ ▼                     │                       │ ▼
   │  [Local Process]      │                  ┌───▼──────────────┐
   │                       │                  │  [Filter Table]  │
   │ ▲                     │                  └───▲──────────────┘
   │ [4. NF_INET_LOCAL_OUT]│                       │
   │ (내부에서 나감)        │                       │
   │                       │                       │
   └───────────────────────┴───────────────────────┘
   │
   │ [5. NF_INET_POST_ROUTING] ───────────────────────▶ [Interface Out]
   │ (인터페이스 나가기 직전) -> Source NAT (SNAT) 가능
   │
```

**[다이어그램 해설]**
위 다이어그램은 리눅스 커널 Netfilter 프레임워크의 5가지 주요 후킹 지점을 도식화한 것이다. 패킷은 **PRE_ROUTING**으로 진입하여 라우팅 결정(Routing Decision)을 거치게 된다. 만약 목적지가 현재 리눅스 박스 자체라면 **LOCAL_IN**으로 향하고, 다른 곳으로 통과해야 한다면 **FORWARD** 체인으로 넘어간다. 방화벽 규칙(iptables/nftables)은 주로 FORWARD 체인이나 INPUT/OUTPUT 체인에서 로딩되어 패킷을 필터링한다. 마지막으로 **POST_ROUTING**을 거쳐 외부로 나가기 전에 Source NAT 등의 주소 변환이 이루어진다.

#### 3. 심층 동작 원리: Stateful Packet Inspection (SPI)
SPI는 단순히 개별 패킷을 보는 것이 아니라, **연결의 맥락(Context)**을 이해한다. TCP 3-way handshake를 통해 생성된 **Connection Tracking (conntrack)** 엔트리를 활용한다.

1. **SYN 패킷 수신**: 새로운 연결 요청이 들어오면 `conntrack` 테이블에 NEW 상태로 기록.
2. **SYN-ACK 수신**: 응답 패킷이 돌아오면 이를 기존 NEW 엔트리와 매칭 후 ESTABLISHED 상태로 변경.
3. **ACK 수신 및 데이터 전송**: 이후 양방향 패킷은 `conntrack` 테이블을 조회하여 기존 연결에 속하는지 확인.
4. **FIN/RST 수신**: 연결 종료 시도가 있으면 시간 제한(Time-wait) 후 엔트리 삭제.

```python
# 의사코드 (Pseudo-code) for SPI Logic
def process_packet(packet):
    conn_info = lookup_conntrack_table(packet)
    
    if packet.protocol == "TCP":
        if packet.flags.SYN and not conn_info:
            # 새로운 연결 시도
            if rule_check(packet) == ALLOW:
                create_conntrack_entry(packet, state=NEW)
                forward(packet)
            else:
                drop(packet)
        elif conn_info and conn_info.state in [ESTABLISHED, RELATED]:
            # 기존 연결에 속한 패킷 (규칙 검사 없이 통과)
            update_conntrack_timestamp(conn_info)
            forward(packet)
        else:
            # 비정상 패킷 (잘못된 플래그 등)
            drop(packet)
    else:
        # UDP/ICMP 등은 Timeout 기반 관리
        handle_stateless(packet)
```

#### 4. 📢 섹션 요약 비유
> 마치 단순히 출입증을 확인하는 것이 아니라, **"방문객이 입장했을 때 발급한 랜야드와 나갈 때 반납하는 랜야드의 번호가 일치하는지 확인"**하는 과정과 같습니다. 아무리 출입증이 좋아도 입장 기록이 없으면 나갈 수도 없게 하는 것입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. iptables vs nftables (기술적 비교)

| 비교 항목 (Feature) | **iptables (Legacy)** | **nftables (Modern)** |
|:---|:---|:---|
| **아키텍처** | 각 프로토콜별 별도 모듈 (iptables, ip6tables, arptables, ebtables) | 단일 통합 아키텍처 (nft) |
| **규칙 처리 방식** | 규칙 집합(Rule list) 순차 검색 (Linear Search) | 단순화 가상 머신 기반 처리 (Tiny VM), Netlink 소켓 통신 |
| **성능 (Latency)** | 규칙이 많을수록 지연(Latency) 급증 | 엔진 내부 최적화로 대규모 규칙에서도 안정적 |
| **가독성** | 복잡한 명령어 구조, 확장 모듈 충돌 가능성 | JSON 스타일의 설정, 일관된 문법 |
| **업데이트 주기** | Kernel 3.x대 | Kernel 3.13+ (현재 표준) |

#### 2. 방화벽 유형별 융합 분석

| 유형 | 계층 (OSI Layer) | 장점 (Pros) | 단점 (Cons) | 융합 관점 (Synergy) |
|:---|:---|:---|:---|:---|
| **패킷 필터링** | L3 (Network) / L4 (Transport) | **고속 처리**, 낮은 리소스 | 세션 정보 부재, 스푸핑(Spoofing) 취약 | L3 스위치/라우터와 **하드웨어적 결합** |
| **Stateful Inspection** | L3 / L4 / (부분 L5) | 연결 상태 추적으로 **보안성 강화** | 대량 연합 시 메모리/부하 문제 | **OS**의 TCP 스택과 밀접하게 연동 |
| **Application Layer (Proxy/WAF)** | L7 (Application) | 페이로드 내용 검사 가능 (공격 차단) | **CPU/지연 시간(Latency) 큰 증가** | **IDS/IPS**, **암호화(SSL/TLS)** 복호화 모듈 필요 |

#### 3. 다른 분야와의 시너지
- **보안 (Security)**: 방화벽은 IDS(Intrusion Detection System)와 연동하여 탐지된 공격 IP를 **실시간으로 방화벽 룰에 추가(Dynamic Blocking)**하는 자동화된 보안 체계를 구축할 수 있다.
- **운영체제 (OS)**: 방화벽은 커널 스페이스(Kernel Space)와 유저 스페이스(User Space) 간의 데이터 교환을 제어하며, **SELinux(Security-Enhanced Linux)**와 같은 MAC(Mandatory Access Control) 시스템과 함께 **Defense in Depth(심층 방어)** 전략을 완성한다.

#### 4. 📢 섹션 요약 비유
> iptables는 **"오래된 철도 선로 열차 system"** (다른 열차를 위해 선로 하나를 통째로 점유)이라면, nftables는 **"첨단 스마트 물류 센터"** (AI가 실시간으로 최적 경로를 배정)와 같습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 웹 서버 보안 정책 수립
**문제 상황**: 공인 IP가 할당된 웹 서버(Apache)가 주기적인 SSH 무작위 대입 공격(Brute-force)과 DDoS 공격에 노출됨.
**의사결정 과정**:
1. **기본 정책 수립**: INPUT 체인 기본 정책을 **DROP(거부)**으로 설정.
2. **필수 트래픽 허용**: Loopback(lo) 허용, Established/Related 연결 허용.
3. **서비스 포트 노출**: HTTP(80), HTTPS(443)는 전체 허용 (PUBLIC).
4. **관리 포트 제한**: SSH(22)는 특정 관리자 대역(예: 1.1.1.1/32)만 허용 (ADMIN).
5. **동적 IP 관리**: 사무실 IP가 유동(DHCP)일 경우, **DDNS + Port Knocking** 기법 활용 고려.

#### 2. 기술 도입 체크리스트

| 구분 | 체크항목 | 설명 |
|:---|:---|:---|
| **기술적** | **성능 영향 평가** | 패킷 처리 속도(PPS)가 NIC(Network Interface Card) 대역폭을 병목시키지 않는지? |
| **기술적** | **규칙 최적화** | 상위에 빈도가 높은 Allow 규칙을 배치하여 검사 횟수를 최소화하는가? |
| **운영/보안** | **로그 관리** | 거부된 패킷 로그를 별도 로그 서버로 전송(Log Rotation)하여 디스크 꽉 현상을 방지하는가? |
| **운영/보안** | **Fail-Open 정책** | 방화벽 서비스 장애 시 모든 트래픽을 막는지(Fail-Closed),