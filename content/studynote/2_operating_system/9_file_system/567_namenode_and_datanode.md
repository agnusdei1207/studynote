+++
title = "567. 네임노드 (NameNode)와 데이터노드 (DataNode)"
date = "2026-03-14"
weight = 567
+++

# 567. 네임노드 (NameNode)와 데이터노드 (DataNode)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: HDFS (Hadoop Distributed File System)는 **제어 플레인(Control Plane)**의 전담 관리자인 NameNode와 **데이터 플레인(Data Plane)**의 분산 저장소인 DataNode로 구성된 마스터-슬레이브(Master-Slave) 아키텍처를 기반으로, 메타데이터의 로우 레벨(Low-level) 관리와 데이터의 하이 레벨(High-level) 처리를 철저히 분리한다.
> 2. **가치**: 이 구조는 수 PB(Petabyte) 급 데이터의 수평 확장성(Scalability)을 제공하며, SPOF (Single Point of Failure) 완화를 위해 Active/Standby 구성과 QJM (Quorum Journal Manager)을 통한 HA (High Availability) 클러스터링을 통해 RTO (Recovery Time Objective)를 1분 이내로 최소화한다.
> 3. **융합**: 컴퓨터 과학의 OS 파일 시스템(Inode 개념)과 분산 시스템 이론(Gossip Protocol, Heartbeat)을 융합하여, 클라우드 환경의 Hypervisor 스케줄링 및 Container Storage Interface (CSI)의 기초가 되는 소프트웨어 정의 저장소(SDS) 계층을 형성한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 정의
HDFS (Hadoop Distributed File System)는 하드웨어 장애가 빈번하게 발생하는 상용 하드웨어(Commodity Hardware) 클러스터에서 대용량 데이터를 저장하고 처리하기 위해 설계된 분산 파일 시스템이다. 이 아키텍처의 핵심 설계 철학은 **"계산은 데이터로 이동한다(Move Computation to Data)"**는 원칙에 기반하며, 이를 실현하기 위해 **제어 플레인(Control Plane)**과 **데이터 플레인(Data Plane)**을 완벽하게 분리한다.

- **NameNode (마스터 노드)**: 파일 시스템의 전 지구적 네임스페이스(Global Namespace)를 관리하는 **단일 실패 지점(SPOF)**이자 중앙 관리자다. 파일 시스템 트리(File System Tree)와 블록 매핑 정보(Inode + Block Map)를 휘발성 메모리(RAM)에 상주시켜 메타데이터 연산 속도를 극대화한다.
- **DataNode (슬레이브 노드)**: 실제 데이터를 블록(Block, 기본 128MB) 단위로 로컬 디스크에 저장하고, NameNode의 지시에 따라 데이터의 생성(Replication), 삭제(Deletion), 복제(Rebalancing)를 수행하는 워커(Worker)다.

### 💡 비유: 거대한 물류 센터의 통제 시스템
거대한 물류 센터를 운영한다고 상상해 보자. 모든 물건의 위치와 재고 현황을 실시간으로 파악하고 주문을 처리하는 **중앙 통제실(NameNode)**이 있고, 실제 무거운 화물을 적재하는 **수많은 창고(DataNode)**가 있다. 통제실은 책상 위에 "A상자는 3번 창고 4번 칸에 있다"라고 적힌 지도(Map)만 가지고 있으며, 실제 화물 운반은 창고 직원들이 처리한다. 통제실 직원은 쉴 새 없이 전화(Heartbeat)를 받고 지시를 내려야 하므로 업무 속도가 매우 빨라야 하며(메모리 연산), 만약 통제실이 불타버리면 지도가 사라져 모든 물건을 찾을 수 없게 된다.

### 등장 배경 및 필요성
1.  **기존 파일 시스템의 한계 (Scale-up)**: 기존의 단일 서버 파일 시스템(예: ext4, NTFS)은 저장 용량과 처리량(Throughput)이 단일 장비의 물리적 스펙에 의존하며, 장비 교체 시 전체 서비스 중단(Downtime)이 불가피했다.
2.  **빅데이터 패러다임 등장 (Scale-out)**: 웹 로그, 센서 데이터, SNS 로그 등 TB/ZB 단위의 비정형 데이터가 폭증하면서, 수백 대의 저렴한 서버를 병렬 연결하여 네트워크상에 하나의 거대한 파일 시스템처럼 사용하는 기술이 요구되었다.
3.  **비즈니스 요구 (Fault-tolerance)**: 수천 대의 서버가 모이면 하드웨어 고장은 필연적 사실이 된다. 따라서 데이터 유실을 방지하기 위해 자동으로 복제본(Replica)을 생성하고 관리하며, 장애 발생 시 자동으로 복구하는 메커니즘이 필수적이 되었다.

### 아키텍처 도해: 역할 분담
```text
   [ 제어 플레인 (Control Plane) ]          [ 데이터 플레인 (Data Plane) ]
  
   +-------------------------------+       +-------------------------------+
   |      NameNode (Master)        |       |      DataNode (Slave)         |
   |  ─────────────────────────    |       |  ─────────────────────────    |
   |  * Metadata (RAM)             |       |  * Block Storage (Disk)       |
   |  * Namespace Management       | <>--- |  * Block I/O Service          |
   |  * Replication Manager        |  Cmd  |  * Heartbeat Sender           |
   +-------------------------------+       +-------------------------------+
            |                                         |
            | RPC (Request)                           | Data Stream
            v                                         v
       [ 클라이언트 ]                          [ 실제 블록 데이터 ]
```

📢 **섹션 요약 비유**: 마치 거대한 항만의 **'통제 타워'**와 **'컨테이너 야드'**로 나누어 운영하는 것과 같습니다. 타워는 선박(데이터)의 입출고를 관리하고 위치를 지시하는 두뇌 역할을 하고, 야드는 실제 화물을 적재하고 보관하는 근육 역할을 하여, 뇌의 과부하 없이 물량을 폭발적으로 증대시키는 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 (Internal Operation) | 주요 파라미터 (Parameters) | 비유 |
|:---|:---|:---|:---|:---|
| **NameNode** | 마스터 서버 | - **Namespace 관리**: 디렉터리 트리, 파일 권한 유지<br>- **Block Mapping**: 파일 → 블록 리스트 → DataNode 리스트 매핑<br>- **Coordination**: DataNode 상태 감시 및 복제 스케줄링 | `dfs.namenode.handler.count` (RPC 스레드 수)<br>`dfs.replication` (기본 복제 계수, 기본값 3) | 중앙 통제실 |
| **DataNode** | 슬레이브 서버 | - **Storage**: 블록을 로컬 파일 시스템(Linux FS)에 저장<br>- **Service**: 스트리밍 방식으로 데이터 송수신<br>- **Reporting**: 주기적으로 Block Report 전송 | `dfs.datanode.data.dir` (저장 경로)<br>`dfs.heartbeat.interval` (기본 3초) | 창고 직원 |
| **FSImage** | 영속성 저장소 | - **Snapshot**: 네임스페이스의 특정 시점 구조를 직렬화(Serialize)하여 파일로 저장<br>- **Boot**: 시스템 시작 시 RAM으로 로드됨 | `dfs.namenode.name.dir` | 가계부 결산서 |
| **Edit Log** | 트랜잭션 로그 | - **Journaling**: 모든 메타데이터 변경사항(생성/이동/삭제)을 순차적으로 기록<br>- **Recovery**: 장애 복구 시 재연(Replay)에 사용 | `dfs.namenode.edit.log.autoroll.multiplier.threshold` | 장부 입력용 영수증 |

### 2. HDFS Read/Write 아키텍처 및 데이터 흐름도 (ASCII)

HDFS의 데이터 처리는 NameNode를 거쳐 메타데이터를 조회한 후, 실제 데이터는 클라이언트와 DataNode 간에 직접 전송되는 방식을 취한다.

```text
   [ CLIENT ]                   ┌───────────────────────┐
      |  ^                      │  Secondary NameNode   │
      |  | Metadata(RPC)        │  / Checkpoint Node    │
      |  +---------------------->  (FsImage + Edit Log) │
      |  |                      └───────────────────────┘
      v  |
   ┌───────────────────┐
   │    NameNode       │ <─────(Heartbeat & Block Report)────┐
   │  (RAM: Metadata)  │                                        │
   └─────────┬─────────┘                                        │
             │ 1. Get Block Locations                          │
             │ 2. Return List of DNs                            │
             │                                                 │
   ┌─────────┴─────────────────────────────────────────────────┘
   |                                                           |
   | 3. Data Transfer (Direct Pipeline)                        |
   |                                                           |
   v                                                           v
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   [DataNode 1]   │─────>│   [DataNode 2]   │─────>│   [DataNode 3]   │
│  ┌──────────┐    │ Pipe │  ┌──────────┐    │ Pipe │  ┌──────────┐    │
│  │ Block A  │    │ line │  │ Block A  │    │ line │  │ Block A  │    │
│  │ Block B  │    │      │  │ Block B  │    │      │  │ Block B  │    │
│  └──────────┘    │      │  └──────────┘    │      │  └──────────┘    │
│   Local Disk     │      │   Local Disk     │      │   Local Disk     │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

#### 다이어그램 해설
위 다이어그램은 HDFS의 **Read/Write 경로**와 **제어 흐름(Management Flow)**을 시각화한 것이다.
1.  **제어 흐름 (Control Flow)**: 클라이언트는 NameNode에게 RPC (Remote Procedure Call)를 통해 파일의 메타데이터(블록이 어디에 있는지)를 요청한다. NameNode는 메모리(RAM)에 상주하는 맵(Map)을 조회하여 블록이 위치한 DataNode의 목록을 반환한다.
2.  **데이터 흐름 (Data Flow)**: 실제 데이터 전송은 NameNode를 거치지 않고, 클라이언트와 DataNode 간에 직접 이루어진다. Write 시 클라이언트는 파이프라인(Pipeline)을 통해 첫 번째 DataNode에 데이터를 쓰면, 해당 DataNode는 두 번째로, 두 번째는 세 번째로 순차적으로 전송하여 복제본을 생성한다.
3.  **상태 보고 (Status Reporting)**: DataNode는 3초 간격으로 NameNode에게 Heartbeat를 전송하여 생존 신호를 보내며, 6시간(기본)마다 자신이 가진 모든 블록의 목록(Block Report)을 NameNode에게 보내어 메타데이터 동기화를 수행한다.

### 3. 심층 동작 원리: 파일 쓰기 파이프라인 (Write Pipeline)
HDFS에서 파일을 쓸 때의 데이터 흐름은 파이프라인(Pipeline) 형태로 이루어지며, 다음과 같은 단계를 거친다.
1.  **요청**: 클라이언트가 NameNode에 `create()` 호출. NameNode는 블록을 저장할 DataNode 목록(예: DN1, DN2, DN3)을 반환.
2.  **스트리밍**: 클라이언트가 첫 번째 DataNode(DN1)에 데이터 패킷 전송.
3.  **파이프라인 복제**: DN1은 패킷을 로컬에 저장하고 즉시 두 번째 DataNode(DN2)로 전달. DN2는 DN3로 전달.
4.  **ACK (Acknowledgment)**: 파이프라인의 끝(DN3)에서부터 역순으로 확인 응답(ACK)이 클라이언트에게 전송됨.
5.  **완료**: 모든 복제본이 저장되면 다음 블록으로 넘어감.

### 4. 핵심 메커니즘: Safe Mode (안전 모드) 및 장애 복구
NameNode가 시동될 때, 데이터 무결성을 보장하기 위해 **Safe Mode**가 활성화된다.
```text
[Safe Mode Exit Condition]
if (DataBlocksReported >= Min_DataBlocks) AND
   (LiveDataNodes >= Min_LiveNodes) {
    Leave Safe Mode;
    Allow Write Operations;
 }
```
시스템 시작 시 FSImage(메모리 스냅샷)를 RAM으로 로드한 후, Edit Log(트랜잭션 로그)를 재연(Replay)한다. 이후 충분한 수의 DataNode로부터 블록 리포트를 받아 최소 복제 계수(Min Replication, 기본 1)가 충족되었다고 판단될 때만 Safe Mode를 해제하고 쓰기 작업을 허용한다. 이 과정에서 복제본이 부족한 블록(Under-replicated blocks)을 발견하면 즉시 복제 큐에 등록하여 데이터를 복구한다.

📢 **섹션 요약 비유**: 이는 고속도로 하이패스 시스템과 유사합니다. **NameNode**는 전국의 톨게이트 상황을 보는 중앙 관제실이고, **DataNode**는 각 톨게이트 부스입니다. 차량(데이터)이 지나가면 부스가 중앙관제실에 "차량 지나감(Block Report)"을 보내며, 관제실은 "부스 3번 고장 났으니 4번으로 우회시켜라(Replication)"라고 지시를 내립니다. 관제실이 정신을 차리기 전(Safe Mode)까지는 차량 진입을 막는 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 구조적 차이 분석

| 비교 항목 | HDFS (Master-Slave) | POSIX 파일 시스템 (Local FS) | 분석 및 의사결정 |
|:---|:---|:---|:---|
| **Metadata 관리** | 중앙 집중식 (NameNode RAM) | 분산 (Inode per File System) | **HDFS**는 메타데이터 조회가 매우 빠르지만, 파일 개수가 수억 개를 넘어가면 NameNode의 **Heap Memory** 한계에 부딪힘. 이를 해결하기 위해 HDFS Federation 도입 필요. |
| **데이터 모델** | Write-Once-Read-Many (WORM) | Read-Write (Random Update) | HDFS는 순차 쓰기(Sequential Write)에 최적화되어 있어, 기존 파일 수정(Modification)보다는 **추가(Append)**에 특화되어 있음. 배치 처리에 유리하나 실시간 랜덤 쓰기에는 부적합. |
| **일관성 모델** | Strong Consistency (Write 후) | Strong Consistency | 쓰기 작업은 파이프라인의 모든 복제본이 완료해야 성공