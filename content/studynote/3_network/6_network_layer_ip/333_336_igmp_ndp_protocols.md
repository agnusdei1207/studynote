+++
title = "333-336. 멀티캐스트 및 Neighbor 제어 (IGMP, NDP)"
date = "2026-03-14"
[extra]
category = "Network Layer"
id = 333
+++

# 333-336. 멀티캐스트 및 Neighbor 제어 (IGMP, NDP)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IPv4의 **IGMP (Internet Group Management Protocol)**와 IPv6의 **MLD (Multicast Listener Discovery)**는 스트리밍 서비스 등 대량 트래픽을 그룹원에게만 효율적으로 전달하기 위한 '멤버십 관리' 프로토콜이며, L2 스위치의 **IGMP Snooping** 기능과 결합하여 불필요한 방송(Flooding)을 억제한다.
> 2. **가치**: IPv6의 **NDP (Neighbor Discovery Protocol)**는 단순한 주소 결정(**ARP**)를 넘어, **RA (Router Advertisement)**를 통한 무상태 자동 주소 할당(**SLAAC**), 중복 주소 검출(**DAD**), Prefix 발급까지 수행하여 네트워크 관리의 자동화와 운영 효율성을 극대화한다.
> 3. **융합**: L3의 그룹 관리 프로토콜(IGMP/MLD)과 L2의 스위칭 기능(Snooping)이 연계되어 네트워크 대역폭을 절약하며, NDP는 **ICMPv6** 기반으로 보안 및 이동성(IPv6 Mobile)과 깊게 연관된 핵심 인프라다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 정의
*   **IGMP (Internet Group Management Protocol)**: IPv4 환경에서 호스트(Host)가 자신이 특정 멀티캐스트 그룹에 가입 또는 탈퇴했음을 직접 연결된 라우터(Multicast Router)에게 알리기 위해 사용하는 프로토콜이다. 이를 통해 라우터는 불필요한 멀티캐스트 패킷 전송을 방지하고 대역폭을 효율화한다.
*   **NDP (Neighbor Discovery Protocol)**: IPv6 환경에서 **ICMPv6**를 기반으로 동작하며, 링크 로컬 범위 내의 이웃 노드(Neighbor) 탐색, 주소 결정(ARP 대체), 라우터 발견, 주소 자동 설정, 중복 주소 검출 등의 기능을 수행하는 프로토콜 세트이다.

#### 2. 💡 비유
*   **IGMP**: 아파트 관리실(라우터)에서 수영 강습(멀티캐스트)을 알릴 때, 관심 있는 세대(호스트)만 신청하게 하여 강사가 방문할 때 해당 세대 초인종만 누르게 하는 시스템이다.
*   **NDP**: 새로 이사 온 사람이 이장님(라우터)에게 동네 네비게이션(Prefix)을 받거나, 옆집 주소(MAC)를 물어볼 때 사용하는 '동네 소통의 모든 것'이다.

#### 3. 등장 배경 및 필요성
1.  **유니캐스트의 한계 (Broadcast Storm)**: 1:N 스트리밍 서비스(IPTV 등)를 유니캐스트로 처리할 경우, 서버의 부하가 선형적으로 증가하며 네트워크 대역폭을 순식간에 고갈시킨다. 이를 해결하기 위해 멀티캐스트가 도입되었고, 이를 관리할 그룹 관리 프로토콜이 필수적이 되었다.
2.  **ARP의 보안 및 기능적 한계**: IPv4의 **ARP (Address Resolution Protocol)**는 브로드캐스팅에 의존하여 네트워크 성능 저하를 유발하고, 스푸핑(Spoofing) 공격에 취약하다. IPv6에서는 이를 **NDP**로 대체하여 멀티캐스트 기반의 효율성과 보안 강화(보다 정교한 검증)를 달성했다.
3.  **IPv6의 자동화 요구**: IPv6의 128비트 긴 주지를 수동으로 배포하기 어렵기 때문에, **RA (Router Advertisement)** 메시지를 통해 네트워크 정보를 자동으로 학습하는 메커니즘이 절실했다.

#### 4. 📢 섹션 요약 비유
이 섹션은 마치 '고속도로 하이패스 차로(멀티캐스트)'를 위한 '차단기 관리 시스템(IGMP)'을 설치하고, 복잡한 '신호등 체계(ARP)'를 대신해 '지능형 교통 통신 시스템(NDP)'을 도입하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 동작 (IGMP & MLD)

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 사용 프로토콜/포트 | 비유 |
|:---:|:---|:---|:---|:---|
| **Host (Querier)** | 그룹 가입/탈퇴 요청 | 자신이 수신하고자 하는 그룹 주소(예: 239.1.1.1)를 라우터에 보고함. Leave 시 Specific Leave 메시지 전송 | IGMPv3 (IP Proto 2) | 동호회 회원 가입 신청서 |
| **Multicast Router** | 그룹 관리 및 트래픽 제어 | 주기적으로 **General Query** 전송(60초). 그룹별 가입자 유무 확인(**Membership Report**) 후 경로 유지/해제 | IGMP (TTL=1) | 동호회 총무(명단 관리) |
| **IGMP Snooping Switch** | L2 트래픽 최적화 | 라우터와 호스트 간의 IGMP 패킷을 '엿들어(Snoop)'서 MAC 주소 테이블에 멀티캐스트 그룹 매핑 정보를 등록. **Flooding** 방지 | L2 Switch Feature | 수신 확인 후 해당 반에만 배달 |
| **MLD (IPv6)** | IPv6 멀티캐스트 리스너 관리 | ICMPv6 메시지 타입(Type 130~132) 사용. IGMP와 논리는 동일하나 Link-Local 주소(FF02::1) 사용 | ICMPv6 | IPv6 버전의 동호회 총무 |

#### 2. IGMP/MLD 상태 전이 및 다이어그램
아래는 호스트가 멀티캐스트 그룹에 가입하고 유지하는 과정의 상세 흐름이다.

```ascii
   [Multicast Source]                  [L2 Switch(Igmp Snooping)]          [Router (Querier)]
(Video Server)                            |                                |
    |                                     |                                |
    |------------ Multicast Data -------->| (MGM Table Empty)              |
    |      (Dest: 224.1.1.1)              | X [Flooding to All Ports]      |
    |                                     |                                |
    v                                     v                                v
  [Time Pass] ...                                                            |
                                                                              |
                                                                              |--- General Query (Who wants 224.x.x.x?) --->
                                                                              |                                 |
[Host A] (Join)                                                             [Host B]
    |<-----------------------------------------------------------------------|
    |--- Report (I want 224.1.1.1) ----------------------------------------->|
    |                                                                        |
    |                                 (Learning: Map Port1 to 224.1.1.1)    |
    |<-------------- Multicast Data (Now Forwarded ONLY to Host A) ---------|
    |                                                                        |
```
**(해설)**: 초기에는 스위치가 멀티캐스트 그룹 정보를 모르므로 모든 포트로 데이터를 전송(Flooding)한다. 호스트가 Report를 보내면 스니핑 중인 스위치가 이를 학습하여 **Port 1**만 그룹에 등록하고, 이후 트래픽은 해당 포트로만 전송된다. 라우터는 주기적으로 쿼리를 보내 가입자가 계속 있는지 확인한다.

#### 3. NDP 핵심 메커니즘 및 상태 변환
NDP는 **ICMPv6** 메시지 타입을 사용하여 5가지 핵심 기능을 수행한다.

1.  **Neighbor Solicitation (NS; Type 135)**: "이 IP 주소를 쓰는 노드의 **Link-Layer Address(MAC)**를 알려줘." (IPv4 ARP Request 역할, Solicited-Node Multicast 주소 사용)
2.  **Neighbor Advertisement (NA; Type 136)**: "내가 바로 그 노드야. 내 MAC은 이거야." (ARP Reply 역할, Unicast 또는 Multicast로 응답)
3.  **Router Solicitation (RS; Type 133)**: "이 네트워크의 라우터 누구야? 접속 정보를 주세요."
4.  **Router Advertisement (RA; Type 134)**: "나 라우터야. Prefix, MTU, Hop Limit 등은 이렇다." (SLAAC의 핵심)
5.  **Redirect (Type 137)**: "너가 가려는 곳은 내가 아니라 저기 옆 라우터가 더 빨라. 경로 수정해."

```ascii
+------------------+                 +------------------+
|   Host A (Src)   |                 |   Host B (Dst)   |
|  IP: 2001::1/64  |                 |  IP: 2001::2/64  |
+------------------+                 +------------------+
        |                                    |
        | 1. NS (Who has 2001::2?)           |
        |    Target: 2001::2                 |
        |    Dest: FF02::1:FF00:2 (Solicited)|
        |----------------------------------->|
        |                                    |
        |                           (Cache Check & DAD)
        |                                    |
        | 2. NA (I have 2001::2, MAC: BBBB)  |
        |<-----------------------------------|
        |    Dest: 2001::1 (Unicast Reply)   |
        |                                    |
[ A의 Neighbor Cache: 2001::2 -> BBBB ]
```
**(해설)**: ARP와 달리 NDP는 **Solicited-Node Multicast Address**(`FF02::1:FFXX:XXXX`)를 사용한다. 이는 전체 브로드캐스트 도메인이 아닌, 해당 접미사에 관심 있는 노드들만 수신하므로 CPU 부하를 획기적으로 줄여준다. 또한 NA를 Unicast로 보내어 네트워크 잡음을 최소화한다.

#### 4. SLAAC (Stateless Address Autoconfiguration) 코드 및 로직
RA 메시지를 수신한 호스트의 주소 생성 로직(의사코드)은 다음과 같다.

```c
// Pseudo-code for SLAAC Address Generation
function configure_ipv6(interface, ra_msg) {
    // 1. RA 수신 및 Prefix 추출
    prefix = ra_msg.prefix;       // 예: 2001:db8::/64
    flag_auto = ra_msg.autonomous_flag;

    if (flag_auto == TRUE) {
        // 2. Interface ID 생성 (EUI-64 또는 Privacy Extension)
        interface_id = generate_interface_id(interface); // MAC based or Random
        
        // 3. 주소 조립
        global_addr = prefix + interface_id;

        // 4. 중복 주소 검출 (DAD - Duplicate Address Detection)
        if (perform_dad(global_addr) == SUCCESS) {
            assign_ip(interface, global_addr);
            set_default_gateway(ra_msg.router_lifetime);
        } else {
            log("Address Duplicated. Retry with new random ID.");
        }
    }
}
```

#### 5. 📢 섹션 요약 비유
이 과정은 마치 방대한 아파트 단지(네트워크)에서, 우편배달부(라우터)가 **동호회 신청 명단(IGMP)**을 보고 우편을 정확한 세대(포트)에만 배달하며, 새로 이사 온 입주자(Host)가 **반상회 앱(NDP)**을 통해 이웃의 집 호수와 동네 규칙(Prefix)을 자동으로 등록하는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. IGMP vs MLD (IPv4 vs IPv6)
| 비교 항목 | IGMP (IPv4) | MLD (IPv6) | 기술적 함의 |
|:---|:---|:---|:---|
| **기반 프로토콜** | 독립적 IP Protocol 번호 (2) | **ICMPv6** 메시지 기반 | 프로토콜 스택 간소화 (IPv6은 ICMPv6 하나로 여러 기능 처리) |
| **주소 체계** | Class D (224.0.0.0 ~ 239.255.255.255) | IPv6 Multicast (FF00::/8) | IPv6는 Scope 범위가 더 세분화됨 (Node-local, Link-local 등) |
| **Query 전송 주소** | 224.0.0.1 (All Hosts) | FF02::1 (All Nodes) | 주소 체계 변화에 따른 차이 |
| **Snooping 필수성** | 매우 높음 (Broadcast Storm 방지) | 필수적이지만 IPv6의 Scope 구조 덕분에 더 효율적일 수 있음 | 레거시 L2 스위치와의 호환성 고려 필요 |

#### 2. ARP (IPv4) vs NDP (IPv6)
| 비교 항목 | ARP (IPv4) | NDP (IPv6) | 기술적 함의 |
|:---|:---|:---|:---|
| **기능 범위** | 주소 결정(IP->MAC) 단일 목적 | 주소 결정 + 라우터 발견 + 주소 자동 할당 + Prefix 발급 | 애플리케이션 의존성 감소, 네트워크 자율성 증대 |
| **전송 방식** | Broadcast (L2 Flood) | **Multicast** (Solicited-Node) | 스위치 및 모든 노드의 CPU 부하 감소 (전체 브로드캐스트 아님) |
| **보안성** | 낮음 (Plain Trust, 스푸핑 취약) | 상대적 높음 (**SEND**: Secure NDP, Cryptographic Authentication) | VPN/Phishing 등 보안 위협 방어에 유리 |
| **캐싱 주기** | 일반적으로 4시간(Timeout 기반) | Reachability 확인에 따른 동적 관리 (NUD - Neighbor Unreachability Detection) | **NUD**는 장애 발생 시 빠른 경로 복구 가능 |

#### 3. OS/보안 융합 분석
*   **OS 커널 및 스택 관점**: 리눅스 커널 등의 OS는 Neighbor Cache(ARP Table, NDISC Cache)를 매핑 테이블로 관리한다. **IGMP Snooping**이 비활성화된 L2 스위치 환경에서는 CPU가 모든 Broadcast를 처리해야 하므로 시스템 부하가 급증한다. (Soft Interrupt `NET_RX` napi spike 유발)
*   **보안 (Security) 융합**: NDP는 **RA Guard** 기능이 필수적이다. 악의적인 사용자가 가짜 RA를 전송하여 트래픽을 자신의 라우터로 유도하는 'Man-in-the-Middle' 공격을 방어하기 위해 L2 스위치 수준에서 RA 필터링이 이루어져야 한다.

#### 4. 📢 섹션 요약 비유
**IGMP**는 옛날식 소식지(단순 신청 관리)라면, **MLD**는 최신 스마트폰 앱(정보 통합)이며, **ARP**가 골목길 소리치는 방식이었다면 **NDP**는 정확한 목적지를 찾아가는 '네비