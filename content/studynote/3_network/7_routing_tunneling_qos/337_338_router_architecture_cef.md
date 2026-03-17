+++
title = "337-338. 라우터의 내부 구조와 CEF 스위칭"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 337
+++

# 337-338. 라우터의 내부 구조와 CEF 스위칭

### # [라우터 내부 구조 및 스위칭 기술]
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 라우터의 성능 병목을 해소하기 위해 **제어 평면(Control Plane)**과 **데이터 평면(Data Plane)**을 분리하여, 경로 결정은 소프트웨어(CPU)가, 패킷 전송은 하드웨어(ASIC)가 담당하는 아키텍처로 진화함.
> 2. **가치**: **CEF (Cisco Express Forwarding)**와 같은 토폴로지 기반 스위칭 방식을 통해 CPU 개입 없이 와이어 스피드(Wire-speed) 포워딩을 구현하며, 이는 **RIB (Routing Information Base)**를 전처리된 **FIB (Forwarding Information Base)**로 변환하여 달성함.
> 3. **융합**: OSI 3계층(라우팅)과 2계층(재기록)의 융합 구조이며, SDN(Software Defined Networking)의 기반이 되는 평면 분리(Decoupling) 개념의 시초가 됨.

---

### Ⅰ. 개요 (Context & Background)
- **개념**: 라우터(Router)는 서로 다른 네트워크 간의 패킷을 중계하는 3계층(L3) 장비로, 내부적으로 **경로를 학습하고 결정하는 제어부**와 **패킷을 빠르게 포워딩하는 전송부**로 나뉩니다. 초기 라우터는 CPU가 모든 처리를 담당했으나, 트래픽 폭주로 인해 전용 하드웨어 기반의 분산 처리 아키텍처로 진화했습니다.
- **💡 비유**: 라우터는 거대한 물류 센터와 같습니다. 경로를 계획하는 '본사 관제팀(Control Plane)'과 실제 화물을 싣고 나르는 '고속 컨베이어 벨트(Data Plane)'가 분리되어야 물량이 몰려도 멈추지 않습니다.
- **등장 배경**: 
  ① **CPU 한계**: 과거 패킷별로 CPU가 연산하던 방식은 초당 수천 패킷(pps) 처리가 한계였음.
  ② **하드웨어 가속**: **ASIC (Application Specific Integrated Circuit)**의 발전으로 패킷 헤더 분석과 전송을 하드웨어적으로 수행 가능해짐.
  ③ **비즈니스 요구**: 초고속 인터넷과 실시간 트래픽(QoS) 요구로 인해 마이크로초(µs) 단위의 지연이 요구됨.
- **📢 섹션 요약 비유**: 과거에는 택배 기사가 손님마다 지도를 펴놓고 길을 찾았다면, 현대의 라우터는 본사에서 미리 길을 찾아 GPS에 입력해두고, 기사는 운전만 하는 시스템과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **구성 요소 (표)**

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Control Plane** | 경로 결정 및 라우팅 테이블 관리 | **OSPF**, **BGP** 등을 통해 이웃과 정보 교환 → **RIB** 구축 | CPU 기반 소프트웨어 | 물류 센터 본사 (관제팀) |
| **RIB (Routing Information Base)** | 모든 라우팅 경로 정보 저장 | 목적지별 Next-hop, Metric 정보 보유 (Admin Distance 비교) | IP Routing Table | 종합 지도 데이터베이스 |
| **FIB (Forwarding Information Base)** | 고속 포워딩을 위한 최적화 테이블 | RIB 정보를 바탕으로 **Prefix** 기반 인덱싱 (ASIC 조회 최적화) | CEF, TCAM | 네비게이션 검색용 DB |
| **Adjacency Table** | L2 헤더 재작성 정보 저장 | Next-hop의 **MAC 주소**, DLCI 등 2계층 정보 캐싱 | ARP, NDP | 목적지까지의 택시 회사 목록 |
| **Data Plane** | 실제 패킷 스위칭 및 포워딩 | ASIC이 FIB 조회 → Adjacency 결합 → L2 Rewrite → 송신 | Line Card, NP | 고속 컨베이어 벨트 |

#### ASCII 구조 다이어그램: 라우터 내부 패킷 흐름
아래 다이어그램은 패킷이 라우터에 유입되어 처리되는 과정을 제어 평면과 데이터 평면의 관점에서 도식화한 것입니다.

```ascii
   [ 라우터 내부 아키텍처: CEF (Cisco Express Forwarding) 모델 ]

   (상단: 제어 평면 - Slow Path)          (하단: 데이터 평면 - Fast Path)
   ┌──────────────────────┐             ┌───────────────────────────────┐
   │  Routing Protocols   │             │      Ingress Interface        │
   │  (OSPF / BGP / RIP)  │             │        (RX Queue)             │
   └──────────┬───────────┘             └───────────────┬───────────────┘
              │                                        │
              ▼                                        ▼
   ┌──────────────────────┐             ┌───────────────────────────────────┐
   │        RIB           │             │         L2 Header De-encap        │
   │ (Routing Table Info) │             │   (Ethernet Header Removed)      │
   └──────────┬───────────┘             └───────────────┬───────────────────┘
              │                                        │
              │ (경로 정보 갱신 신호)                   │
              └───────────────┬────────────────────────┘
                              │
                ┌─────────────▼──────────────┐
                │     CEF Pre-computation    │
                │     (FIB & Adjacency)      │
                └─────────────┬──────────────┘
                              │ (Copy to Hardware)
                              ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          Hardware Forwarding Engine                       │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   [Incoming Packet]                                                       │
│         │                                                                 │
│         ▼                                                                 │
│   ┌─────────────────┐    ┌───────────────────┐    ┌───────────────────┐  │
│   │   L3 Lookup     │───▶│   Adjacency       │───▶│   L2 Rewrite &    │  │
│   │   (TCAM/MEM)    │    │   (MAC Pairing)   │    │   Encapsulation   │  │
│   └────────▲────────┘    └───────────────────┘    └─────────┬─────────┘  │
│            │                                                  │          │
│            │ (Match FIB Entry)                               │          │
│            │                                                  │          │
│   [FIB: 192.168.1.0/24 -> NextHop: 10.0.0.2]                 │          │
│            │                                                  ▼          │
│            │                                     [Egress Interface]      │
│            │                                                             │
└───────────────────────────────────────────────────────────────────────────┘
```

**해설 (Diagram Explanation)**:
1. **제어 평면(상단)**: 라우팅 프로토콜(RIP, OSPF, BGP 등)이 실행되어 네트워크 토폴로지 정보를 수집합니다. 이 정보는 RIB에 저장되며, RIB의 정보는 CEF 프로세스에 의해 하드웨어가 바로 읽을 수 있는 형태인 FIB와 Adjacency Table로 변환되어 데이터 평면으로 복사됩니다.
2. **데이터 평면(하단)**: 실제 패킷은 수신 포트(Ingress)로 들어와 L2 헤더가 제거됩니다. 이후 ASIC 칩셋은 FIB를 검색하여 목적지 IP에 해당하는 Next-hop을 찾고, Adjacency Table에서 해당 Next-hop의 MAC 주소를 가져와 패킷 헤더를 재작성(Rewrite)한 뒤 송신 포트(Egress)로 전송합니다. 이 과정은 CPU의 개입 없이 완전히 하드웨어적으로 처리됩니다.

- **심층 동작 원리**: 
  1. **경로 학습**: 라우터가 시동 시 OSPF 등으로 이웃과 정보를 주고받아 RIB를 완성합니다.
  2. **FIB 구축 (FIB Build)**: RIB의 정보를 기반으로 CPU가 **FIB**를 생성합니다. FIB는 최적 경로만 저장하며, **Recursive Lookup(재귀적 탐색)**이 완료된 최종 Next-hop 정보를 담고 있습니다.
  3. **인접 테이블 구축 (Adjacency Build)**: **ARP (Address Resolution Protocol)**를 통해 Next-hop IP에 대응하는 MAC 주소를 미리解析(파싱)해 둡니다.
  4. **패킷 포워딩 (Packet Switching)**: 패킷 도착 시, ASIC이 FIB에서 `Output Interface`를 찾고(`Longest Prefix Match`), Adjacency Table에서 `Destination MAC`과 `Source MAC`을 가져와 L2 헤더를 교체합니다.

- **핵심 알고리즘 및 코드**: 
  라우터의 경로 선택 로직은 관리 거리(Admin Distance)와 메트릭(Metric)에 의해 결정됩니다.
  
  ```python
  # Pseudo-code: RIB to FIB Selection Logic
  def build_fib(rib_entries):
      fib = {}
      # 1. RIB 내 여러 경로 중 최적 경로 선정 (AD & Metric 비교)
      # AD(Administrative Distance): 경로 출처의 신뢰도 (Connected=0, Static=1, OSPF=110, BGP=20...)
      best_routes = []
      
      for prefix, routes in rib_entries.groupby('prefix'):
          # AD가 낮은 순, AD가 같으면 Metric이 낮은 순 정렬
          best_route = sorted(routes, key=lambda x: (x.ad, x.metric))[0]
          
          # 2. Recursive Lookup 확인 (Next-hop이 실제 연결된 링크인지)
          if is_recursive_lookup_needed(best_route):
               next_hop = resolve_next_hop(best_route.next_hop)
          else:
               next_hop = best_route.next_hop
               
          fib[prefix] = {
              'next_hop': next_hop,
              'interface': best_route.interface
          }
      
      # 3. Hardware Download (ASIC에 푸시)
      asic.download_fib(fib)
  ```

- **📢 섹션 요약 비유**: 
  제어 평면은 **항공 관제탑**이고, 데이터 평면은 **비행기(자동조종장치)**입니다. 관제탑이 모든 비행기의 경로를 실시간으로 직접 조종하면(CPU 처리) 항공사가 망합니다. 대신 관제탑은 이륙 전에 비행 계획서(FIB)를 내려주고, 비행기는 그 계획에 따라 스스로 날아가는 것입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
- **심층 기술 비교표**: Process Switching vs Fast Switching vs CEF

| 구분 | Process Switching | Fast Switching | CEF (Cisco Express Forwarding) |
|:---|:---|:---|:---|
| **검색 방식** | 패킷 도착 시마다 **RIB** 전체 탐색 | 첫 패킷은 RIB 탐색, 이후 **Route Cache** 활용 | RIB 기반 **FIB**와 **Adjacency** 테이블 선행 구축 |
| **주체** | CPU (Interrupt Driven) | CPU (Cache Hit 시는 빠름) | **ASIC / NPU** (Hardware) |
| **소요 시간** | 매우 느림 (MS 단위) | 중간 (Cache Miss 시 급격히 저하) | 매우 빠름 (Wire-speed) |
| **부하 패턴** | 트래픽 증가 시 **CPU Spike** | Cache 갱신 빈번 시 오버헤드 | **Load Balancing**(ECMP)에 유리 |
| **토폴로지** | Demand-based (On-demand) | Traffic-triggered | **Topology-based** (사전 구축) |
| **주요 용도** | 디버깅, 패킷 생성 | 구형 장비, 특수 목적 | 현대 라우터의 표준 (기본값) |

- **과목 융합 관점**:
  - **OS (Operating System)**: 인터럽트(Interrupt) 핸들링 관점에서 프로세스 스위칭은 매 패킷마다 인터럽트를 발생시켜 Context Switching 오버헤드가 큽니다. CEF는 이를 Zero-copy 및 DMA(Direct Memory Access) 기술로 해결하는 네트워크 전용 최적화 기술입니다.
  - **컴퓨터 구조 (Computer Architecture)**: **ASIC (Application Specific Integrated Circuit)** 설계 기술과 밀접합니다. TCAM (Ternary CAM) 메모리를 사용하여 FIB를 O(1) 시간 복잡도로 검색하는 하드웨어적 최적화가 핵심입니다.

```ascii
   [스위칭 방식의 처리 속도 및 부하 비교]

   CPU 사용률
       ▲
   100%│      Process Switching (Line Up - Packet per Interrupt)
       │      /  /  /  /  /  /  /  /
   80% │     /  /  /  /  /  /  /  /
       │    /  Fast Switching (Cache Hit/Miss fluctuations)
   60% │   /  /--------------------
       │  /  /
   40% │ /  /   CEF (Hardware Offloading - Constant Line Rate)
       │/  /____________________________________________________
   20% │                                           
       └───────────────────────────────────────────────────▶ 시간
            (Traffic Load Increasing)
```
*(해설: 트래픽이 증가할수록 Process Switching은 포화 상태에 빠지지만, CEF는 하드웨어가 처리하므로 CPU 사용률이 일정하게 유지됨을 보여줍니다.)*

- **📢 섹션 요약 비유**: 
  프로세스 스위칭은 **사용자 정의 조립식 PC**(호환성은 좋지만 조립이 느림)이고, 패스트 스위칭은 **부품 몇 개를 미리 조립해둔 키트**, CEF는 **공장에서 완제품으로 찍어내는 현대식 자동차 생산 라인**과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 시나리오**:
  1. **네트워크 정체(Network Congestion) 해결**: 메인 라우터의 CPU 사용률이 90%를 넘고 throughput이 나오지 않을 때, CEF가 비활성화되었거나Route Cache 오류를 의심하고 `show ip cef` 명령어로 확인 후 재활성화한다.
  2. **비대칭 라우팅(Asymmetric Routing) 진단**: CEF는 로드 밸런싱(Per-packet, Per-destination)을 지원한다. Path MTU 문제나 패킷 순서 뒤집�