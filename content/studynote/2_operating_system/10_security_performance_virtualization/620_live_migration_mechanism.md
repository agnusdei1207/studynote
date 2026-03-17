+++
title = "620. 라이브 마이그레이션 (Live Migration) 메커니즘"
date = "2026-03-14"
weight = 620
+++

# 620. 라이브 마이그레이션 (Live Migration) 메커니즘

## 🎯 핵심 인사이트 (Core Insight)
> 1. **본질 (Essence)**: 라이브 마이그레이션(Live Migration)은 가상 머신(VM)의 실행 상태(Execution State)를 포함한 시스템 이미지를 서비스 중단(Downtime) 없이 물리 호스트 간 전송하는 가상화의 핵심 기술입니다. 이는 단순한 파일 복사가 아닌, 메모리 일관성과 CPU 레지스터 보존을 보장하는 복잡한 코히어런시(Coherency) 문제를 해결합니다.
> 2. **가치 (Value)**: 서비스 무중단(High Availability)을 통해 RTO (Recovery Time Objective)를 '0(Zero)'에 수렴하게 하며, 동적 자원 관리(Dynamic Resource Scheduling, DRS)를 통해 데이터 센터의 전력 효율을 최대 30%까지 향상시킬 수 있습니다.
> 3. **융합 (Convergence)**: 네트워크 스토리지(SAN/NAS) 아키텍처, 메모리 가상화 기술, 그리고 TCP/IP 네트워킹 프로토콜(특히 ARP)이 유기적으로 결합된 고도의 시스템 엔지니어링 결과물입니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
라이브 마이그레이션은 실행 중인 가상 머신(VM)의 **전체 시스템 상태(Total System State)**를 구성하는 메모리(Memory), CPU 레지스터, 디스크, 네트워크 I/O 상태를 네트워크를 통해 다른 물리 호스트(Destination Host)로 실시간 이동시키는 기술입니다. 단순한 장애 복구(Failover)와 달리, **사용자 세션(User Session)이나 네트워크 연결(TCP Connection)을 유지**한 상태에서 이동이 완료되어, 최종 사용자는 서비스가 이동했음을 인지하지 못합니다.

**2. 기술적 배경 및 철학**
전통적인 물리 서버 환경에서는 하드웨어 업그레이드나 유지보수를 위해 필연적으로 서비스 중단이 발생했습니다. 가상화 기술의 발전으로 VM의 상태를 파일 형태로 추상화할 수 있게 되었지만, 수 GB~수 TB에 달하는 메모리 이미지를 전송하는 동안 서비스가 멈추는 문제가 있었습니다. 이를 해결하기 위해 **Pre-copy(선제 복사)** 알고리즘 등을 통해 '실행 중인 상태'를 유지하면서 데이터를 전송하고, 마지막 순간에만 아주 짧게 멈추(Downtime < 1s), 마치 연속성이 유지되는 것처럼 보이게 만드는 것이 라이브 마이그레이션의 철학입니다.

**3. 비즈니스적 필요성**
- **무중단 유지보수**: 하드웨어 교체 펌웨어 업데이트 등 계획된 다운타임(Scheduled Downtime)을 제거하여 SLA (Service Level Agreement)를 준수합니다.
- **동적 부하 분산 (Load Balancing)**: 특정 호스트의 CPU/Memory 사용률이 임계치를 초과할 때, VM을 유휴 상태의 호스트로 자동 이동시켜 클러스터 전체의 성능을 최적화합니다.
- **에너지 효율화 (Green IT)**: 야간이나 주말과 같이 트래픽이 적은 시간대에 VM을 소수의 서버로 통합(Consolidation)하고 나머지 서버의 전원을 차단하여 전력 소모를 줄입니다.

**💡 직관적 비유**
> 라이브 마이그레이션은 **'달리는 고속버스의 승객들을 깨우지 않고, 운행 중인 다른 버스로 옮겨 태우는 것'**과 같습니다. 승객(서비스)은 잠시 졸거나 창밖을 보는 사이에 버스(물리 서버)가 바뀌었음을 알게 되지만, 여행(서비스)은 중단되지 않고 계속됩니다.

> 📢 **섹션 요약 비유**: 이 기술은 마치 **"도로 위를 달리는 자동차의 엔진을 끄지 않고, 운전자가 운전석에 앉은 채로 차량 통째로 다른 트레일러로 옮겨 태우는 것"**과 같습니다. 운전자(사용자)는 차가 바뀌는 동안에도 핸들을 잡고 주행을 계속합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 및 역할**

| 구성 요소 (Component) | 역할 (Role) | 상세 내부 동작 (Internal Logic) | 관련 프로토콜 (Protocol) |
| :--- | :--- | :--- | :--- |
| **Hypervisor (VMM)** | 마이그레이션 총괄 관리자 | VM의 메모리 페이지 추적, Dirty Page 관리, 전송 스케줄링 | proprietary (e.g., vMotion, Live Migration) |
| **Memory Mapper** | 메모리 상태 복제 | 소스 메모리 페이지를 대상 호스트의 물리 메모리에 매핑 (Shadow Page Table 활용) | - |
| **Dirty Bitmap** | 변경 데이터 추적기 | Pre-copy 과정에서 수정된 메모리 페이지를 비트(Bit) 단위로 기록 | - |
| **Network Channel** | 데이터 전송 파이프 | 고대역폭/저지연 네트워크를 통해 메모리 페이징 데이터 전송 | TCP (일반적), RDMA (고성능) |
| **VM State Manager** | 실행 상태 보존 | CPU 레지스터, PC(Program Counter), Device I/O 상태 직렬화(Serialization) | - |

**2. 라이브 마이그레이션 싸이클 (Pre-copy 방식 기반)**

가장 널리 사용되는 **Pre-copy (사전 복사)** 방식의 상세 동작 과정입니다.

```text
[Phase 1: Initialization]
   Source Host                           Destination Host
   -----------                           -----------------
   +----------+                         +------------------+
   |    VM    |                         | (Reservation)    |
   | RUNNING  |                         | [Reserve Memory] |
   +----------+                         +------------------+
        |                                      ^
        | "Request Migration"                  |
        +--------------------------------------+

[Phase 2: Iterative Pre-copy (Warming Up)]
   *Loop Start*
   +----------+    1. Bulk Transfer    +------------------+
   |    VM    | ------------------->  | Copy Memory Pages|
   | RUNNING  |   (All Memory)         | (Incoming Pages) |
   +----------+                        +------------------+
        |                                      ^
        | 2. Continue Execution                |
        V (Dirty Pages Generated)              |
   +----------+    3. Dirty Page Log   +------------------+
   |Bitmap DB | <-------------------- |  (Track Updates) |
   +----------+    (Modified Pages)    +------------------+
        |
        | 4. Send Only Dirty Pages
        +--------------------------------------->

   *(Repeat until Dirty Page size < Threshold)*

[Phase 3: Stop-and-Copy (The Cutover)]
   +----------+    5. Suspend VM      +------------------+
   |    VM    | ------------------->  | Suspend & Copy   |
   | STOPPED  |   (Downtime ~ms)     | Final State      |
   +----------+    (CPU/Reg/Mem)      +------------------+
                                            |
                                            | 6. Resume
                                            V
                                    +------------------+
                                    |    VM RUNNING   |
                                    +------------------+

[Phase 4: Commit & Cleanup]
        |                                      ^
        | 7. ACK Success                       |
        +--------------------------------------+
        |
        V
   +----------+
   | KILL VM  | (Source Terminated)
   +----------+
```

**3. 심층 동작 원리 및 핵심 알고리즘**

1.  **Initialization (초기화)**:
    소스 호스트의 Hypervisor가 마이그레이션을 시작하면, 대상 호스트는 동일한 사양의 VM을 생성할 리소스(CPU 코어, 메모리 공간)를 사전 확보(Reservation)합니다. 이 단계에서는 네트워크 연결 설정이 이루어집니다.

2.  **Iterative Pre-copy (반복적 선제 복사)**:
    핵심 최적화 단계입니다. VM을 멈추지 않은 상태에서 전체 메모리 페이지를 대상 호스트로 전송합니다. 하지만 전송하는 동안에도 VM은 실행되므로 메모리 내용은 계속 변합니다. Hypervisor는 페이지 테이블의 **Write Protection** 기능을 활용하거나 **Shadow Page Tables**를 통해 변경된 페이지(Dirty Page)를 추적합니다.
    -   **1회차**: 전체 메모리 전송 (가장 오래 걸림)
    -   **2회차 이후**: 1회차 전송 중 변경된 부분만 재전송
    -   이 과정은 전송해야 할 Dirty Page의 크기가 임계값(Threshold, 예: 100MB) 이하가 될 때까지 반복되며, 이를 **Convergence(수렴)**라고 합니다.

3.  **Stop-and-Copy (중단 및 최종 복사)**:
    Dirty Page가 충분히 줄어들면 VM을 아주 짧은 시간(수백 ms ~ 1s 이내) 동안 일시 중단(Suspend)합니다. 이때 변경되지 않은 CPU 레지스터 값, 장치 상태, 그리고 마지막 남은 Dirty Page를 전송합니다. 이 순간이 사용자가 경험하는 유일한 다운타임(Downtime)입니다.

4.  **Resume & Commit (재개 및 커밋)**:
    대상 호스트는 전달받은 메모리 이미지와 레지스터 상태를 로드하여 VM을 즉시 재개(Resume)합니다. 네트워크 연결을 유지하기 위해 **RARP (Reverse ARP)** 또는 **GARP (Gratuitous ARP)**를 브로드캐스팅하여 "VM의 IP 주소가 새로운 MAC 주스로 변경되었음"을 스위치에 알립니다.

> 📢 **섹션 요약 비유**: 이 과정은 **"이사 짐을 싸는 동안에도 계속 생활하다가, 짐이 거의 다 옮겨졌을 때 마지막 가방 하나만 들고 휙 넘어가는 것"**과 같습니다. 처음엔 짐 전부를 싸서 보내고, 포장하는 동안 사용한 물건들만 다시 싸서 보내는 식이죠. 마지막엔 집 문을 잠그고 떠납니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Analysis)

**1. Pre-copy vs Post-copy (기술적 비교 분석)**

| 구분 | Pre-copy (선제 복사) | Post-copy (사후 복사) |
| :--- | :--- | :--- |
| **메커니즘** | 메모리 전체를 대상 서버에 미리 복사하고, 변경분만 반복 전송 | VM 실행 상태(레지스터)만 먼저 보내 대상에서 실행 시작 후, 필요한 메모리 페이지를 요청 시점에 가져옴 |
| **서비스 중단 시간** | 짧음 (수십~수백 ms) | 짧음 (페이지 부재 시 깜빡임 발생 가능성) |
| **안정성/안전성** | **높음** (전송 실패 시 소스에서 계속 실행) | **낮음** (전송 중 장애 시 VM 즉시 크래시, 상태 소실) |
| **성능 이슈** | 쓰기 작업이 많은 VM은 수렴이 늦어질 수 있음 | Page Fault 발생 시 네트워크 지연으로 인해 성능 저우(Demand Paging) |
| **주요 사용처�** | 일반적인 데이터 센터, 상용 환경 (Standard) | 실험적 환경, 네트워크가 매우 빠르고 전원 소비를 줄여야 할 때 |

**2. 다른 기술 영역과의 융합 (Synergy)**

-   **네트워킹 (TCP/IP)**: 라이브 마이그레이션 성공은 네트워크 대역폭에 좌우됩니다. 대역폭이 좁으면 Pre-copy 수렴 속도보다 Dirty Page 발생 속도가 빨라 마이그레이션이 '무한 루프'에 빠질 수 있습니다. 또한, **GARP (Gratuitous ARP)**를 통한 MAC 주소 갱신이 L2 스위치에서 즉시 처리되지 않으면 패킷 유실(Packet Loss)이 발생합니다.
-   **스토리지 (Storage)**: VM의 디스크 이미지(VMDK, VDI)까지 이주시키는 것은 비효율적입니다. 따라서 **SAN (Storage Area Network)**이나 **NAS (Network Attached Storage)**와 같은 공유 스토리지 환경을 전제로 하여, 계산 장치(Host)만 이동하고 데이터는 그대로 두는 방식이 일반적입니다.

> 📢 **섹션 요약 비유**: Pre-copy는 **"짐을 다 옮기고 집에 들어가는 방식"**이라 실패해도 원래 집으로 돌아가면 그만이지만, Post-copy는 **"일단 집에 들어가서 필요한 물건을 전화해 하나씩 달라고 하는 방식"**이라 전화선(네트워크)이 끊기면 아무것도 할 수 없게 됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 트리**

1.  **시나리오: 하드웨어 유지보수 예정**
    -   **상황**: 서버 A의 전원 공급장치 교체 필요.
    -   **판단**: 서비스 중단이 허용되지 않음.
    -   **전략**: vMotion/Live Migration 활용. VM을 서버 B로 이주 후 작업. 완료 후 다시 복귀하거나 로드 밸런싱에 따라 유지.
    -   **Point**: 대상 호스트의 리소스 여유(CPU/RAM)와 네트워크 대역폭을 사전에 모니터링해야 합니다.

2.  **시나리오: 썬더링 헤드(Thundering Herd) 발생**
    -   **상황**: 이벤트 시작으로 특정 호스트 부하 급증.
    -   **판단**: 성능 병목으로 서비스 지연 발생.
    -   **전략**: DRS(Dynamic Resource Scheduling) 정책에 따라 자동으로 일부 VM을 유휴 호스트로 분산. Auto-Convergence 옵션을 켜서 쓰기 부하가 심한 VM도 강제 이주.

3.  **시나리오: 공유 스토리지 미비 환경**
    -   **상황**: 로컬 디스크(Local Storage)만 사용 중.
    -   **판단**: 스토리지 데이터 전송 시간 과다로 실시간 마이그레이션 불가.
    -   **전략**: Storage vMotion 등을 사용하여 스토리지 이주 후 계산 이주를 진행하거나, Cold Migration(정지 시킨 후 이동) 사용.

**2. 도입 체크리스트 (Checklist)**

-   [ ] **Shared Storage**: 소스와 대상 호스트가 동일한 LUN/Datastore에