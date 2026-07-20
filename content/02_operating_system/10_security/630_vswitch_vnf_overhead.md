---
title: "Vswitch Vnf Overhead"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 630
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가상 스위치(vSwitch)는 하이퍼바이저 내부에 소프트웨어로 구현된 L2/L3 스위치로, 가상머신(VM) 간의 통신과 외부 네트워크 연결을 담당하지만 커널 네트워크 스택을 거치면서 발생하는 잦은 인터럽트와 문맥 교환으로 인해 치명적인 <strong>패킷 처리 지연(Overhead)</strong>을 유발한다.
> 2. <strong>혁신 (DPDK/XDP &amp; DPDK OVS)</strong>: 이 오버헤드를 극복하기 위해, 리눅스 커널을 거치지 않고 유저 공간(User Space)에서 폴링(Polling) 방식으로 패킷을 직접 가져오는 <strong>DPDK (Data Plane Development Kit)</strong> 기술과, 커널 최하단에서 eBPF로 패킷을 즉시 우회시키는 <strong>XDP</strong> 기반의 OVS(Open vSwitch) 구조가 VNF(가상 네트워크 기능)의 표준 아키텍처로 자리 잡았다.
> 3. **가치**: VNF에 DPDK 가속 기반 vSwitch를 적용함으로써 10Gbps~100Gbps 대역폭 환경에서도 와이어 스피드(Wire-speed) 패킷 처리가 가능해졌으며, 이는 5G 통신망의 코어 인프라(NFV)를 범용 x86 서버로 구축할 수 있게 만든 결정적 기술이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>vSwitch (가상 스위치)</strong>: 물리적인 스위치 장비를 소프트웨어로 에뮬레이션한 것으로, KVM/Xen 환경에서 여러 VM의 가상 랜카드(vNIC)를 물리 랜카드(pNIC)에 브릿지(Bridge) 해주는 역할을 한다. (대표작: Open vSwitch)
  - <strong>VNF (Virtual Network Function)</strong>: 과거 전용 하드웨어 장비(방화벽, 라우터, 로드밸런서)로 돌던 네트워크 기능을 소프트웨어(VM 또는 컨테이너) 형태로 x86 서버 위에서 구동하는 기술이다. (NFV의 핵심 단위)

- **필요성 (소프트웨어 네트워킹의 병목)**:
  - VNF가 제대로 동작하려면 1초에 수백만 개의 패킷(Mpps)을 처리해야 한다.
  - 전통적인 리눅스 커널 네트워크 스택(NAPI 기반)은 패킷이 들어올 때마다 하드웨어 인터럽트 $\rightarrow$ 소프트 인터럽트(SoftIRQ) $\rightarrow$ 소켓 버퍼(sk_buff) 할당 $\rightarrow$ 커널/유저 모드 복사 $\rightarrow$ vSwitch 전송이라는 지루하고 무거운 파이프라인을 거친다.
  - 이 과정에서 발생하는 CPU 오버헤드는 10Gbps는커녕 1Gbps 대역폭에서도 CPU 코어 하나를 100% 점유하게 만들어 VNF 상용화를 불가능하게 했다. 커널(OS)의 우회가 절대적으로 필요했다.

- **발전 과정**:
  1. <strong>Linux Bridge / TAP</strong>: 초기 가상 스위치. 커널 내부의 브릿지 모듈 사용. 성능 최하.
  2. <strong>Open vSwitch (OVS) Kernel Datapath</strong>: SDN(소프트웨어 정의 네트워크)을 위해 등장. OpenFlow 룰을 커널에서 캐싱하여 처리.
  3. <strong>OVS-DPDK</strong>: 커널을 완전히 바이패스(Kernel Bypass)하고 유저 공간에서 폴링으로 패킷을 처리하여 VNF 성능 극대화 (현재 5G NFV 표준).
  4. <strong>eBPF/XDP 가속 OVS</strong>: 폴링 방식의 CPU 낭비(항상 100% 사용)를 막기 위해 커널 네트워킹 가장 앞단에서 eBPF로 고속 라우팅.

- **📢 섹션 요약 비유**: 수많은 차(패킷)가 다니는 교차로에 매번 신호등(인터럽트)을 세워두는 대신, 신호등을 없애고 고가도로(Kernel Bypass)를 뚫어 차들이 멈추지 않고 지나가게 만든 교통 혁명입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 커널 네트워크 스택의 병목 원인

전통적인 vSwitch 아키텍처에서 1개의 패킷이 VM(VNF)으로 전달되기까지의 오버헤드는 다음과 같다.

1. <strong>Context Switch / Mode Switch</strong>: NIC $\rightarrow$ Kernel $\rightarrow$ vSwitch $\rightarrow$ Kernel $\rightarrow$ VM으로 이동하며 유저-커널 전환이 반복됨.
2. <strong>Data Copy</strong>: 물리 NIC의 링 버퍼에서 커널의 `sk_buff` 객체로, 다시 VM의 메모리로 데이터가 여러 번 복사됨 (캐시 오염 발생).
3. <strong>Interrupt Handling</strong>: 초당 1,000만 개 패킷이 들어올 때 NAPI(인터럽트 완화 기술)를 써도 엄청난 CPU 사이클이 인터럽트 처리에 소모됨.

---

### 커널 우회 (Kernel Bypass) 기법: DPDK (Data Plane Development Kit)

DPDK는 인텔이 개발한 '유저 모드 초고속 패킷 처리' 프레임워크다. OVS(Open vSwitch)에 이 DPDK를 결합한 <strong>OVS-DPDK</strong> 구조가 VNF 성능의 핵심이다.

```text
  +-----------------------------------------------------------------------+
  |                 전통적 OVS vs OVS-DPDK 가속 아키텍처 비교                  |
  +-----------------------------------------------------------------------+
  |                                                                       |
  |  [1. 전통적 OVS (Kernel Datapath)]                                       |
  |   [User Space]       OVS Daemon (ovs-vswitchd)      VNF (가상머신)         |
  |                          ^                                ^           |
  | -------------------------+--------------------------------+---------- |
  |   [Kernel Space]         v (Netlink)                      v           |
  |                      OVS Kernel Module <----(sk_buff)---> TAP Device    |
  |                          ^                                            |
  |                      (인터럽트 + 복사)                                    |
  |   [Hardware]           물리 NIC (pNIC)                                 |
  |                                                                       |
  |                                                                       |
  |  [2. OVS-DPDK (User Space Datapath) - Kernel Bypass]                  |
  |   [User Space]                                                        |
  |                      +--------------------------+     [공유 메모리]       |
  |                      | OVS-DPDK 데몬 (PMD 스레드) | <---(vhost-user)---> VNF|
  |                      +--------------------------+     (복사 없음!)      |
  |                          ^                                            |
  |                          | 폴링 (Polling) - 인터럽트 없음!                |
  | -------------------------+------------------------------------------- |
  |   [Kernel Space]         | UIO/VFIO (커널 드라이버 무시, 하드웨어 바인딩)     |
  |                          |                                            |
  |   [Hardware]           물리 NIC (pNIC의 RX/TX 링 버퍼에 직접 접근)         |
  +-----------------------------------------------------------------------+
```

**[다이어그램 해설]** 전통적 OVS는 패킷이 물리 NIC에 도착하면 커널 인터럽트가 발생하고, 커널이 패킷을 포장(`sk_buff`)하여 OVS 커널 모듈로 보낸다. OVS가 룰을 확인한 후 다시 커널의 TAP 디바이스를 통해 VM으로 보낸다. 매 단계가 병목이다.
반면 <strong>OVS-DPDK</strong> 구조에서는 물리 NIC를 리눅스 커널 드라이버(예: `ixgbe`)에서 빼앗아 VFIO(IOMMU 기반) 드라이버에 결합한다. 이제 OVS-DPDK 데몬(User Space)이 커널을 완전히 무시하고 물리 NIC의 링 버퍼 메모리에 직접 접근한다. 게다가 인터럽트를 기다리지 않고 **PMD (Poll Mode Driver)** 스레드가 무한 루프(`while(1)`)를 돌며 NIC에 패킷이 왔는지 직접 확인(Polling)한다. 패킷을 발견하면 유저 공간의 링 버퍼 메모리(vhost-user)에 주소만 적어주고 VNF에게 가져가라 한다(Zero-copy). 패킷이 OS 커널을 아예 밟지 않게 되어 10배 이상의 성능 향상이 일어난다.

---

### vhost-user 와 Virtio 최적화

DPDK가 물리 NIC에서 패킷을 빛의 속도로 퍼 올려도, 그걸 가상머신(VNF) 안으로 밀어 넣는 구멍이 느리면 소용없다. 이때 사용되는 기술이 **vhost-user** 이다.

- 기존 Virtio-net은 QEMU(유저 모드)와 vhost-net(커널 모드)을 통해 호스트 커널을 거쳐 VM으로 통신했다.
- <strong>vhost-user</strong>는 호스트 커널(vhost-net)을 버리고, OVS-DPDK(유저 모드)와 QEMU(유저 모드)가 유닉스 도메인 소켓(Unix Domain Socket)으로 직접 제어 신호를 주고받은 뒤, 아예 <strong>Huge Page 기반의 공유 메모리(Shared Memory)</strong>를 매핑해 버린다.
- 즉, OVS-DPDK가 패킷을 공유 메모리에 쓰면, VNF 안의 게스트 DPDK 앱이 복사 없이 그 주소의 데이터를 즉시 읽어간다. (진정한 Zero-copy 달성)

- **📢 섹션 요약 비유**: 물건(패킷)을 택배 기사(커널)에게 넘기지 않고, 옆집(VM)과 아예 벽을 허물어 공용 창고(공유 메모리)를 만든 다음, 그곳에 물건을 던져두고 "가져가!"라고 소리만 치는 초고속 물류입니다.

---

## Ⅲ. 비교 및 연결

### 패킷 처리 아키텍처 비교

| 비교 항목 | Linux Bridge / OVS (커널) | SR-IOV (하드웨어 패스스루) | OVS-DPDK (유저 공간 가속) |
|:---|:---|:---|:---|
| **처리 주체** | 리눅스 커널 네트워크 스택 | 물리 NIC 하드웨어 스위치(eSwitch) | 유저 모드 OVS-DPDK 애플리케이션 |
| <strong>VM 간 통신/마이그레이션</strong> | L2/L3 유연함, 마이그레이션 쉬움 | H/W 종속적, 마이그레이션 매우 어려움 | <strong>L2/L3 유연함 (SDN 완벽 호환)</strong> |
| **CPU 점유율** | 패킷 올 때만 사용 (가변적) | CPU 개입 거의 없음 (0%) | <strong>PMD 스레드가 코어 100% 항시 점유</strong> |
| <strong>패킷 처리 성능</strong> | 낮음 (수백만 pps 한계) | 최고 (Wire-speed 보장) | **매우 높음 (수천만 pps 가능)** |

**트레이드오프 분석**:
SR-IOV가 성능은 가장 좋지만, VM이 특정 벤더의 하드웨어(NIC) 드라이버에 종속되고 Live Migration이 불가능해진다는 치명적 단점이 있다. 반면 OVS-DPDK는 SDN의 L2/L3 오버레이(VXLAN 등) 유연성과 Live Migration을 모두 지원하면서도 SR-IOV에 필적하는 성능을 내기 때문에 통신사 NFV의 표준(Defacto)이 되었다. 단, DPDK는 폴링 방식을 쓰기 때문에 패킷이 없어도 CPU 코어를 100% 풀로 돌리며 전기세를 태운다는 단점이 있다.

### 과목 융합 관점

- **네트워크 (NW)**: SDN(Software Defined Networking)과 NFV(Network Functions Virtualization) 결합 시 발생하는 I/O 병목을 해결하는 핵심 아키텍처다.
- <strong>컴퓨터구조 (CA)</strong>: DPDK 아키텍처가 제 성능을 내려면 NUMA(Non-Uniform Memory Access) 아키텍처에 대한 이해가 필수적이다. NIC이 꽂힌 PCIe 슬롯과 물리적으로 가까운(Local NUMA 노드) CPU 코어와 RAM에 PMD 스레드와 Huge Page를 할당해야 캐시 미스와 메모리 버스 지연을 막을 수 있다.

- **📢 섹션 요약 비유**: SR-IOV가 각 집에 전용 고속도로를 깔아주지만 이사 갈 때 길을 뜯어가야 하는 방식이라면, OVS-DPDK는 유연하게 경로를 바꿀 수 있는 지능형 스마트 고가도로를 소프트웨어로 띄운 것입니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오

1. <strong>시나리오 — 5G 모바일 코어망 (UPF) 가상화 구축 시 성능 병목</strong>: 통신사가 기존의 Cisco/Huawei 하드웨어 라우터를 버리고 x86 서버 VM에 오픈소스 UPF(User Plane Function)를 올렸으나(NFV 도입), 10Gbps 트래픽 인입 시 CPU 부하로 패킷 드랍(Packet Drop)이 대량 발생.
   - **아키텍처 적용**: 하이퍼바이저 노드에 OVS-DPDK를 구축한다. 물리 서버의 CPU 40코어 중 4개 코어를 OS 스케줄러에서 분리(Isolcpus)하여 오직 OVS-DPDK의 PMD(폴링) 스레드 전용으로 고정(Pinning)시킨다. VNF(VM) 내부에도 일반 커널 네트워크 드라이버가 아닌 DPDK 앱을 구동시키고 호스트와 `vhost-user` 소켓으로 연결한다. 이를 통해 커널을 우회한 10Gbps 라인 레이트 처리를 달성한다.

2. <strong>시나리오 — DPDK의 전력 소모(CPU 100%) 문제 극복을 위한 XDP/eBPF 도입</strong>: 클라우드 데이터센터에서 DPDK를 적용하니, 트래픽이 없는 야간에도 PMD 스레드가 CPU를 100% 사용하며 폴링을 돌려 서버 발열과 전력 낭비가 극심함.
   - <strong>차세대 기술 적용 (eBPF/XDP)</strong>: 최신 리눅스 환경에서는 DPDK의 맹점을 보완하기 위해 <strong>XDP (eXpress Data Path)</strong>를 활용한다. XDP는 패킷이 물리 NIC 드라이버에 도착하자마자(커널 `sk_buff` 객체가 만들어지기도 전에) 커널 내부에서 eBPF(안전하게 검증된 커널 샌드박스 코드) 프로그램을 실행하여 즉시 패킷을 드롭(Drop)하거나 다른 포트로 리다이렉트(Redirect) 해버린다. 인터럽트 기반으로 동작하여 CPU 전력 소모를 줄이면서도 DPDK에 버금가는 소프트웨어 가속을 제공한다. 최신 OVS(OVS-eBPF)는 이 기능을 적극 도입 중이다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 VNF 환경 가상 스위치(vSwitch) 가속 튜닝 플로우             |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [VNF (방화벽/라우터 VM) 성능이 요구 대역폭(Gbps/Mpps)에 미달함]          |
  |                |                                                  |
  |                v                                                  |
  |      VNF가 하드웨어 종속 및 마이그레이션 불가(Downtime)를 감수할 수 있는가? |
  |          +- 예 ------> [SR-IOV 물리 VF 직접 할당 (성능 최상, 유연성 최하)] |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      호스트 서버의 여유 CPU 코어를 100% 점유(희생)시킬 수 있는가?           |
  |          +- 예 ------> [OVS-DPDK 도입 (PMD 폴링 기반)]              |
  |          |            (NUMA Pinning, Huge Page 설정 필수 동반)        |
  |          |                                                        |
  |          +- 아니오 ---> [eBPF / XDP 기반 OVS 오프로드 검토]             |
  |                         (인터럽트 구동 유지 + sk_buff 할당 전 처리)       |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** VNF 아키텍처 설계에서 '공짜 점심'은 없다. 커널을 쓰면 유연하지만 느리고, SR-IOV를 쓰면 빠르지만 유연성이 죽는다. DPDK를 쓰면 유연하고 빠르지만 CPU 코어(전기)를 잡아먹는다. 실무자는 시스템의 목적(통신사 코어망인지, 일반 엔터프라이즈 웹 서버인지)에 따라 이 삼각 트레이드오프에서 최적점을 선택해야 한다.

### 도입 체크리스트
- <strong>NUMA 정렬 (NUMA Affinity)</strong>: OVS-DPDK 설정 시, 물리 랜카드가 꽂힌 NUMA 노드 번호(예: NUMA 0)를 확인하고, PMD 스레드와 VNF 가상머신, 그리고 Huge Page 메모리가 전부 동일한 NUMA 0번에 할당되도록 스케줄러 튜닝(CPU Pinning)을 완료했는가? (NUMA 경계를 넘으면 QPI/UPI 버스 지연으로 성능이 30% 폭락함)
- <strong>Huge Page 할당</strong>: DPDK의 메모리 풀과 vhost-user 버퍼를 담기 위해, 호스트 OS 부팅 파라미터에 충분한 양의 1GB 크기 Huge Page(`default_hugepagesz=1G hugepages=16`)를 사전 할당했는가?

- **📢 섹션 요약 비유**: 경주용 자동차(DPDK)를 샀다고 끝이 아닙니다. 이 차가 달릴 전용 트랙(CPU Pinning)을 치워주고, 가장 크고 매끄러운 아스팔트(Huge Page)를 깔아주어야 진짜 스피드가 나옵니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 OVS (커널 스택) | OVS-DPDK 가속 (유저 스택) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (처리량)</strong> | 약 1 ~ 2 Mpps (64B 패킷) | **약 15 ~ 20 Mpps 이상** | 패킷 처리량(Throughput) **10배 향상** |
| <strong>정량 (지연)</strong> | 수십 ~ 수백 µs (인터럽트 지터) | **단일 µs (마이크로초)** | 극저지연(Ultra-low Latency) 보장 |
| **정성** | 하드웨어 장비 대비 성능 경쟁력 전무 | 범용 x86으로 텔코(Telco) 장비 대체 | 통신사 5G NFV 도입 및 투자비(CAPEX) 절감의 마중물 |

### 미래 전망
- <strong>스마트 NIC (DPU) 완전 오프로딩</strong>: 서버의 메인 CPU 코어를 PMD 폴링에 낭비하는 것조차 아깝기 때문에, 물리 랜카드 자체에 ARM 코어와 메모리가 내장된 DPU(Data Processing Unit, 예: NVIDIA BlueField)가 등장했다. OVS의 룰셋 컨트롤 플레인은 서버 CPU에 남겨두고, 데이터 플레인(DPDK 패킷 처리)을 DPU 내부의 칩으로 완전히 오프로딩하여 서버 CPU 소모를 0%로 만드는 기술이 최신 클라우드의 표준이 되고 있다.
- <strong>P4 랭귀지 지원 소프트웨어 스위치</strong>: 하드웨어 스위치의 동작을 정의하는 P4 언어가 vSwitch에도 통합되어, eBPF와 연동된 동적 파이프라인 컴파일을 통해 네트워크 펑션의 처리 속도를 하드웨어 수준으로 이끌어 올리는 연구가 진행 중이다.

### 결론
가상 스위치(vSwitch)의 패킷 처리 오버헤드 극복 역사는 "커널을 어떻게 똑똑하게 배제할 것인가"의 역사다. DPDK의 등장으로 NFV(네트워크 기능 가상화)는 망상이 아닌 현실이 되었고, 통신 네트워크 인프라가 경직된 깡통 장비에서 벗어나 클라우드 소프트웨어 생태계로 통합되는 혁명을 이뤘다. 앞으로의 VNF 구조는 eBPF/XDP와 하드웨어 DPU 오프로딩이 결합된, 성능과 효율의 타협 없는 차세대 아키텍처로 진화할 것이다.

- **📢 섹션 요약 비유**: 꽉 막힌 도심의 교차로(OS 커널)를 없애고 그 위로 끝없는 고가도로(DPDK)를 세운 끝에, 이제는 아예 배달 드론(DPU)에게 짐을 맡겨버리는 하늘길의 시대로 접어들고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 컨테이너 런타임 (runc, containerd) OCI 규격 표준화 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 메모리 KSM (Kernel Samepage Merging) 가상머신 간 중복 메모리 통합 절약 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 벌루닝 (Ballooning) 하이퍼바이저 가상머신 동적 메모리 회수 기법 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식]
    |
    v
[가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식]
    |
    +---> [메모리 KSM (Kernel Samepage Merging) 가상머신 간 중복 메모리 통합 절약]
    +---> [벌루닝 (Ballooning) 하이퍼바이저 가상머신 동적 메모리 회수 기법 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 가상머신(가짜 컴퓨터)끼리 인터넷을 하려면 가상 스위치(우체국)를 거쳐야 하는데, 소포가 너무 많이 오면 우체국 직원이 쓰러져서 인터넷이 느려져요.
2. 그래서 'DPDK'라는 슈퍼 배달 시스템을 만들었어요. 이 시스템은 우체국을 안 거치고, 배달 트럭이 아예 창고(메모리)에 바로 차를 대고 물건을 미친 듯이 쏟아내요.
3. 대신 이 배달 트럭은 시동을 절대 끄지 않고 계속 돌아가기 때문에(폴링) 기름(전기)은 좀 많이 먹지만, 세상에서 제일 빠르게 인터넷 데이터를 배달한답니다!
