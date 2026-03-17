+++
title = "369-370. 멀티캐스트 라우팅과 PIM"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 369
+++

# 369-370. 멀티캐스트 라우팅과 PIM

> **1. 본질**: 멀티캐스트(Multicast)는 단일 송신자가 특정 그룹에 속한 다수의 수신자에게 트래픽을 효율적으로 전달하는 1:N 통신 기술입니다. 유니캐스트(Unicast)의 대역폭 중복 문제와 브로드캐스트(Broadcast)의 불필요한 폐쇄 부하를 동시에 해결하기 위해 **RPF (Reverse Path Forwarding)** 기반의 루프 프리 트리(Tree) 구조를 사용합니다.
> **2. 가치**: 네트워크 대역폭 효율성을 극대화하여 동일한 데이터를 다수가 수신하는 IPTV, 온라인 게임, 실시간 주식 정보 방송, 대규모 업데이트 배포 등에서 망 자원의 비용을 획기적으로 절감합니다. (트래픽 절감율: 수신자 수 N에 비례하여 $1/N$ 수준으로 최적화)
> **3. 융합**: L3 계층의 라우팅 기술로서, 하위 L2 스위칭에서의 **IGMP (Internet Group Management Protocol)** Snooping과 연동되며, 상위 응용 계층의 미디어 서버와 CDN 구조에서 필수적인 전송망 기술로 작용합니다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**멀티캐스트 (Multicast)**는 정보의 '출처(Source)' 하나가 특정 '그룹 주소(Group Address)'를 통해 다수의 '수신자(Receiver)'에게 패킷을 동시에 전송하는 통신 방식입니다. IP 멀티캐스트는 Class D 주소 영역(224.0.0.0 ~ 239.255.255.255)을 사용하며, 수신자는 이 그룹 주소에 대해 **IGMP (Internet Group Management Protocol)**를 통해 가입(Join) 및 탈퇴(Leave) 과정을 거쳐야 합니다. 이 기술의 핵심 철학은 "데이터는 필요한 곳에만 복사되어야 한다"는 것입니다.

### 2. 작동 배경 및 필요성
기존의 **유니캐스트 (Unicast)** 방식은 1,000명의 시청자가 있다면 송신자는 1,000번의 동일한 데이터를 전송해야 하므로 송신부와 코어 네트워크 망에서 대역폭 병목이 발생합니다. 반면 **브로드캐스트 (Broadcast)**는 모든 네트워크 세그먼트에 데이터를 뿌리기 때문에 수신 여부와 관계없이 모든 호스트가 CPU 인터럽트를 처리해야 하므로 심각한 성능 저하를 유발합니다. 멀티캐스트는 라우터가 데이터의 '사본(Copy)'을 트리 구조의 분기점(Router)에서만 생성하여, 망의 효율성을 지키면서 대규모 전송을 가능하게 합니다.

### 3. 핵심 기술 요소: RPF
멀티캐스트 라우팅의 가장 중요한 기반 기술은 **RPF (Reverse Path Forwarding)**입니다. 이는 라우터가 수신한 멀티캐스트 패킷의 출발지(Source) IP가 자신의 라우팅 테이블 상에서 수신 인터페이스를 통해 도달 가능한 경로와 일치하는지 검사하는 메커니즘입니다. 만약 패킷이 들어온 인터페이스가 출발지까지 가는 최단 경로가 아니라면, 이는 루프(Loop)가 형성되었다는 뜻이므로 패킷을 폐기(Drop)합니다. 이는 스패닝 트리 프로토콜(STP)이 L2에서 루프를 방지하듯, L3에서 루프 프루닝(Loop Pruning)을 수행하는 논리입니다.

> 📢 **섹션 요약 비유**: 멀티캐스트는 **'VIP 초청장 배달 시스템'**과 같습니다. 유니캐스트는 초대장을 받을 사람마다 택배 기사가 따로따로 집까지 보내는 낭비가 심한 방식이고, 브로드캐스트는 동네 방범대 순찰처럼 초대할 생각이 없는 집 문 앞에까지 다 뿌리고 가는 방식입니다. 멀티캐스트는 초대받은 사람이 사는 아파트 단지 입구(Router)에서만 초대장을 복사해서 배달하는 지능적인 시스템입니다. 여기서 RPF는 택배 기사가 "이 초대장이 발송지에서 제대로 온 게 맞나?"를 확인하고 가짜 택배를 바로 버리는 보안 검단 절차입니다.

```ascii
         [ 인터넷 또는 코어망 ]
                 │
        ┌────────┴────────┐
        │  RPF Checkpoint │
        │  (ループ 방지)   │
        └────────┬────────┘
             │  │
      (Pass) │  │ (Fail/Drop)
             ▼  ▼
    [ Forward ]   [ Drop ]
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 상세 동작
멀티캐스트 라우팅을 구성하는 핵심 요소들은 송신자, 수신자, 그리고 이를 연결하는 라우터들로 구성되며, 각각의 역할과 프로토콜은 다음과 같습니다.

| 구성 요소 (Component) | 영문 명칭 (Full Name) | 역할 및 내부 동작 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **속성 그룹** | Multicast Group | 데이터를 수신할 대상들의 논리적 집합. Class D IP(224.x~239.x) 사용. | IGMP, MLD | TV 채널 번호 |
| **최초 홉 라우터** | First-Hop Router (FHR) | 송신자가 직접 연결된 라우터. 송신자 트래픽을 인지하여 멀티캐스트 트리로 주입(DR 역할 수행). | PIM, IGMP | 방송국 송신 타워 |
| **마지막 홉 라우터** | Last-Hop Router (LHR) | 수신자가 연결된 라우터. 수신자의 가입 요청(IGMP Join)을 받아 트리를 확장. | IGMP, PIM | 가입자 집 단자함 |
| **만남의 장소** | Rendezvous Point (RP) | PIM-SM 모드에서 사용. 송신자와 수신자가 처음 만나는 중계 지점. | PIM-SM, MSDP | 중계 허브 센터 |
| **역경로 전달** | Reverse Path Forwarding | 패킷 수신 인터페이스가 출발지로 가는 최단 경로인지 확인하여 루프 방지. | RPF Check | 택배 출고지 확인 |

### 2. PIM (Protocol Independent Multicast) 아키텍처
**PIM (Protocol Independent Multicast)**은 기존의 유니캐스트 라우팅 정보(OSPF, RIP, BGP 등)를 그대로 사용하면서, 멀티캐스트만의 고유한 트리(Tree)를 형성하는 라우팅 프로토콜입니다. 멀티캐스트를 위한 별도의 라우팅 테이블을 유지하지 않고 유니캐스트 RIB(Routing Information Base)를 공유하기 때문에 'Protocol Independent'라는 이름이 붙었습니다. 크게 **PIM-DM (Dense Mode)**과 **PIM-SM (Sparse Mode)** 두 가지 모드로 나뉩니다.

#### A. PIM-DM (Dense Mode, 조밀 모드)
- **핵심 전략**: **"Push (밀어내기)"** - 일단 모든 경로에 플러딩(Flooding) 후, 수신자가 없는 경로를 가지치기(Pruning).
- **동작 원리**:
  1. **Flooding**: 송신자로부터 들어온 데이터를 모든 인터페이스로 전송.
  2. **Pruning**: 하위 라우터가 수신자가 없음을 확인하면 상위 라우터에게 Prune 메시지 전송.
  3. **Grafting**: 나중에 수신자가 생기면 다시 Join 요청.
- **특징**: 소규모 네트워크나 수신자가 밀집된 환경에 적합하지만, 초기 플러딩으로 인한 망 부하가 심합니다.

#### B. PIM-SM (Sparse Mode, 희소 모드)
- **핵심 전략**: **"Pull (당겨오기)"** - 데이터는 필요할 때만 명시적으로 요청하여 받음. 중앙 집중 관리자(RP) 사용.
- **동작 원리**:
  1. **Join**: 수신자(LHR)가 그룹 가입 요청을 상위 라우터로 전송.
  2. **RP Registration**: 송신자(FHR)가 데이터를 RP로 등록(Register).
  3. **Distribution**: RP가 수신자들로 데이터를 내려보냄.
- **특징**: 광대역 인터넷(WAN)처럼 수신자가 흩어져 있는 대형 네트워크에 필수적입니다.

```ascii
      [ PIM-DM (Dense Mode) ]           [ PIM-SM (Sparse Mode) ]
      =======================           =======================

   Source ──┐                            Source ──┐
            │                                      │
        (Flooding)                             (Register)
            │                                      ▼
          [ R1 ] ──┐                          [ RP ]
            │       │                             │
         (Prune)  (Prune)                     (Join * Join)
            │       │                             │
          [ R2 ]   [ R3 ] ──┐                [ R1 ]──┐
            │             (Prune)               │    │
         (No Receiver)                         │    │
                                               ▼    ▼
                                            [ R2 ]  [ R3 ]
                                             │      │
                                          Receiver Receiver
```

### 3. 핵심 알고리즘: 라우팅 테이블 구조
멀티캐스트 라우터는 유니캐스트 라우팅 테이블과는 별도로 멀티캐스트 라우팅 테이블(MRoute Table)을 유지합니다. 이 테이블의 핵심은 **(S, G)**와 **(\*, G)** 상태입니다.

```python
# Multicast Routing Entry Structure (Pseudo Code)

class MulticastRouteEntry:
    source_address = "192.168.1.10"    # S (Source IP)
    group_address  = "239.1.1.1"       # G (Group IP)
    
    # Incoming Interface List (IIF) - RPF Interface
    incoming_interface = "GigabitEthernet0/0"
    
    # Outgoing Interface List (OIF) - Forwarding List
    outgoing_interfaces = [
        "GigabitEthernet0/1", 
        "GigabitEthernet0/2"
    ]
    
    # State Flags
    flags = ["SPT", "Register"]        # SPT: Shortest Path Tree Bit
    
    def forward_packet(self, packet):
        if packet.in_iface != self.incoming_interface:
            # RPF Check Fail
            drop(packet)
            return
        
        for iface in self.outgoing_interfaces:
            # Replicate and Forward out
            iface.send(packet.clone())
```

> 📢 **섹션 요약 비유**: PIM-DM은 **'무료 샘플 나누기'**와 같습니다. 일단 거리에 나가서 사람들에게 다 주고(Flooding), "안 먹을 거야?" 하는 사람만 골라내서(Prune) 남은 사람에게 줍니다. PIM-SM은 **'택시 호출 앱(Call Taxi)'**과 같습니다. 승객(수신자)이 앱으로 호출(Join)을 하지 않으면 택시(데이터)는 운행을 시작하지 않습니다. 여기서 RP는 택시 회사의 총사령탑으로, 승객과 기사를 매칭시켜주는 역할을 합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 배달 트리(Delivery Tree) 기술 심층 분석
멀티캐스트 라우팅은 데이터를 전달하는 경로인 '트리(Tree)'를 어떻게 구성하느냐에 따라 성능 특징이 달라집니다.

| 구분 | Source Tree (SPT) | Shared Tree (RPT) |
|:---|:---|:---|
| **약어** | SPT: Shortest Path Tree | RPT: Rendezvous Point Tree |
| **트리 기준** | 송신자(Source)를 뿌리(Root)로 함 | RP(Rendezvous Point)를 뿌리(Root)로 함 |
| **표기법** | **(S, G)**<br>ex) (192.168.1.1, 239.1.1.1) | **(\*, G)**<br>ex) (*, 239.1.1.1) |
| **장점** | 송신자에서 수신자까지의 지연 시간(Latency)이 최단화됨. | 라우터가 유지해야 할 라우팅 정보가 적어 메모리 효율적. |
| **단점** | 모든 송신자별로 경로를 계산해야 하므로 라우터 부하가 큼. | 최단 경로가 아닐 수 있어 지연 시간이 길어질 수 있음. |
| **주요 사용** | 고화질 화상 회의, 낮은 지연이 필요한 실시간 트래픽. | 대규모 IPTV VOD, 다수의 송신자가 존재하는 방송. |

### 2. 기술 비교 및 정량적 분석
유니캐스트와 멀티캐스트의 망 자원 소모량을 수식으로 비교하면 다음과 같습니다.
- **유니캐스트 트래픽**: $T_{unicast} \approx N \times R$ (N: 수신자 수, R: 전송률)
- **멀티캐스트 트래픽**: $T_{multicast} \approx R \times H$ (H: 소스에서 수신자까지의 홉(Hop) 수 평균)
  - $H$는 $\log N$에 비례하므로, 수신자가 늘어날수록 상대적 망 부하가 급격히 줄어듭니다.

```ascii
       [ Source Tree (SPT) ]              [ Shared Tree (RPT) ]
       ====================              ====================
       
       (Source)                           (Source)
          │                                  │
          ▼ (Root)                          ▼ (First Hop)
       [ Source ]                        [ Source ]
          │                                  │
       ┌─┴─┐                             [ Register ]
       │   │                                  │
      [R1] [R2]  <-- 최단 경로 보장          ▼
       │   │                              [ RP ] (Root)
      [R3] [R4]                             │
       │   │                          (Shared Path)
       ▼   �