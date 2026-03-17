+++
title = "566. 하둡 분산 파일 시스템 (HDFS) 아키텍처"
date = "2026-03-14"
weight = 566
+++

# # 566. 하둡 분산 파일 시스템 (HDFS) 아키텍처

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HDFS (Hadoop Distributed File System)는 고성능 범용 하드웨어(Cluster of Commodity Hardware)의 집합체 위에서 구축되는 분산형 블록 저장소로, 단일 시스템 이미지(Single System Image)를 제공한다.
> 2. **가치**: 낮은 비용의 하드웨어 장애를 자연스러운 현상으로 받아들이고 블록 레벨 복제(Replication)를 통해 데이터 내구성을 보장하며, 높은 데이터 처리량(High Throughput)을 통해 배치 처리 성능을 극대화한다.
> 3. **융합**: '연산은 데이터로'라는 철학을 구현하여 MapReduce나 Apache Spark 같은 데이터 분석 프레임워크와 결합하여 네트워크 병목을 최소화하고 대규모 데이터 처리를 가능하게 한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
HDFS는 Google File System (GFS)의 논문을 기반으로 설계된 Apache Hadoop 프로젝트의 저장소 계층이다. 기존의 POSIX (Portable Operating System Interface) 표준을 준수하는 파일 시스템과 달리, HDFS는 웹 검색 및 로그 분석과 같은 **"한 번 쓰고 여러 번 읽기(Write-once-read-many)"** 패턴에 특화되었다. 이 시스템은 낮은 비용의 상용 서버(Commodity Hardware) 수천 대를 연결하여 엔터프라이즈급 SAN (Storage Area Network)을 대체하며, 장애 발생을 예외가 아닌 일상적인 사건으로 취급한다.

### 2. 등장 배경 및 기술적 패러다임 변화
- **기존 한계**: 단일 서버의 저장소 한계 도달, NAS (Network Attached Storage)의 처리량 병목, 고가의 장애 허용 하드웨어 비용 부담.
- **혁신적 패러다임**: 수직적 확장(Scale-up)에서 수평적 확장(Scale-out)으로의 전환. 데이터 블록을 분산 저장하고 복제하여 하드웨어 고장에 대응하는 SW 기반의 결함 허용(Fault Tolerance) 메커니즘 도입.
- **현재 요구**: 빅데이터 시대의 PB (Petabyte)급 데이터 저장 및 배치 처리를 위한 안정적인 기반이 필요.

### 📢 섹션 요약 비유
HDFS는 수천 명의 일꾼들이 공사 현장에 모여 거대한 성을 짓는 것과 같습니다. 한 명의 뛰어난 초인(비싼 슈퍼컴퓨터)에게 모든 일을 맡기는 대신, 평범한 일꾼들(저가형 서버)들이 팀을 이루어 자재(데이터)를 나누어 보관하고, 누군가缺席해도 다른 팀원이 그 일을 대신 수행하여 완성을 해냅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

HDFS는 전형적인 마스터-슬레이브(Master-Slave) 아키텍처를 따르며, 중앙 관리자인 **NameNode**와 실 데이터를 저장하는 **DataNode**들로 구성된다.

### 1. 구성 요소 상세 분석

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/포트 | 비유 |
|:---|:---|:---|:---|:---|
| **NameNode** (Master) | 메타데이터 관리자 | 네임스페이스(파일 시스템 트리)와 블록 맵(File → Block mapping)을 RAM에 로드하여 관리. | IPC (Inter-Process Call) / 8020, 9000 | 도서관 사서 (목록 관리) |
| **DataNode** (Slave) | 저장소 워커 | 실제 블록 데이터를 로컬 디스크에 저장/삭제하며, 3초마다 Heartbeat와 Block Report 전송. | Data Transfer Protocol / 50010, 50020 | 책꽂이 (실제 책 보관) |
| **Secondary NameNode** | 체크포인트 노드 | NameNode의 메모리 상태 스냅샷을 주기적으로 가져와 FSImage와 Edit Log를 병합(Merge). | HTTP / 50090 | 부사서 (백업 및 정리) |
| **Client** | 사용자 인터페이스 | HDFS API를 통해 NameNode와 메타데이터를 주고받고, DataNode와 직접 데이터 스트림을 형성. | TCP/IP | 도서 관리 시스템 이용자 |

### 2. 아키텍처 데이터 플로우 (ASCII Diagram)

```text
   +-------------------------------------------------------+
   |  [ HDFS Client (MapReduce / Spark / HBase CLI) ]      |
   +---------------------------+---------------------------+
                               |
             (1) Metadata Req/Rsp (RPC to Active NameNode)
                               |
                               V
   +------------------------------------------------------------------+
   | [ NameNode (Master) ]  << Namespace & Block Map in RAM >>        |
   | - Manages File System Tree                                        |
   | - Coordinates Block Replication & Recovery                        |
   +-----------------------------------+------------------------------+
                                       | (2) Pipeline Setup Instructions
                                       | (DataNode List & Allocation)
                                       V
+----------------------+     +----------------------+     +----------------------+
| [ DataNode 01 ]      |     | [ DataNode 02 ]      |     | [ DataNode 03 ]      |
| Block: blk_A_1001    |<--->| Block: blk_A_1001    |<--->| Block: blk_A_1001    |
| (Replica 1)          |     | (Replica 2)          |     | (Replica 3)          |
| +------------------+ |     | +------------------+ |     | +------------------+ |
| | Local Disk Ext  | |     | | Local Disk Ext  | |     | | Local Disk Ext  | |
| +------------------+ |     | +------------------+ |     | +------------------+ |
+----------+-----------+     +----------+-----------+     +----------+-----------+
           ^                              ^                              ^
           | (3) Data Stream (Packet based, 64KB chunks)
           | (Client writes to DN1 -> DN1 forwards to DN2 -> DN2 forwards to DN3)
           |
    (4) Acknowledgement (Reverse Pipeline)
```

### 3. 심층 동작 원리 (Deep Dive Mechanism)
- **읽기(Read) 동작**:
    1. 클라이언트가 NameNode에 파일 경로로 조회 요청.
    2. NameNode는 메타데이터를 스캔하여 파일을 구성하는 블록 목록과 해당 블록이 위치한 DataNode의 리스트(거리 순 정렬) 반환.
    3. 클라이언트는 가장 가까운 DataNode에 직접 연결하여 **FSDataInputStream**을 통해 데이터 스트리밍.
- **쓰기(Write) 동작 (파이프라인 복제)**:
    1. NameNode가 새 파일 생성 요청 승인 및 블록 할당.
    2. 클라이언트는 첫 번째 DataNode에 데이터 패킷(64KB Chunk) 전송.
    3. 첫 번째 DataNode는 데이터를 로컬에 저장하고, 두 번째 DataNode로 전송(Pipeline). 이 과정이 체인으로 연결됨.
    4. 마지막 DataNode까지 전송 완료되면, 역순으로 ACK (Acknowledgement) 전송. 파이프라인 중단 시 NameNode에 보고하여 복제 계수(Replication Factor)를 맞추기 위해 재복제 수행.

### 📢 섹션 요약 비유
HDFS의 쓰기 동작은 **"양동이에 담긴 물을 전달하여 대형 물탱크 채우기"**와 같습니다. 물(Client의 Data)을 받은 첫 번째 사람(DataNode 1)은 자신의 양동이를 채우고, 바로 옆 사람(DataNode 2)에게 물을 전달합니다. 이렇게 줄을 선 사람들이 연쇄적으로 물을 전달하고, 모두가 받았다는 신호(ACK)를 보내면 한 번의 물 나르기가 완료됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. HDFS vs 기존 파일 시스템 (Linux EXT4 vs NAS)

| 비교 항목 (Metric) | **HDFS (Hadoop Distributed File System)** | **Traditional File System (e.g., EXT4, NAS)** |
|:---|:---|:---|
| **저장 매체** | 저가형 Commodity Hardware (JBOD) | 고가용성 Enterprise RAID Array |
| **데이터 크기** | 대용량 (PB급, MB/GB 블록) | 소용량 (TB급, KB 블록) |
| **접근 패턴** | Streaming Access (순차 읽기 최적화) | Random Access (임의 읽기/쓰기) |
| **결함 허용** | SW 레벨 복제 (Replication Factor 3) | HW 레벨 RAID (RAID 5/6) |
| **일관성 모델** | Write-once-read-many (Append 지원) | Read-Write (다중 쓰기 허용) |
| **비용 효율** | 스토리지 당 $/GB 매우 낮음 | 스토리지 당 $/GB 높음 |

### 2. 데이터 지역성 (Data Locality)과의 융합
HDFS는 컴퓨팅 노드와 스토리지 노드가 동일한 물리적 서버에 위치(Co-located)하는 것을 전제로 한다.
- **네트워크 비용 절감**: MapReduce나 Spark의 Executor는 원격 데이터를 가져오는 대신, 로컬 디스크에 있는 블록을 읽어 연산을 수행.
- **Topologia Awareness**: NameNode는 클라이언트에게 블록 위치 정보를 줄 때, **랙 인식(Rack Awareness)** 알고리즘을 사용하여 동일 랙 내부의 데이터를 우선적으로 전달한다. 이는 스위치 간 트래픽(Rack-to-Rack Traffic)을 줄여 네트워크 병목을 방지한다.

### 📢 섹션 요약 비유
HDFS와 전통적 파일 시스템의 차이는 **"고속 열차(기존 시스템)와 화물 컨테이너 트럭(HDFS)"**의 차이와 같습니다. 고속 열차는 소수의 승객(작은 파일)을 빠르게 이동시키지만 정밀한 유지 보수가 필요합니다. 반면, 수천 대의 트럭(HDFS)은 갈림길에서 우회할 수 있고(분산), 몇 대의 트럭이 고장 나도 전체 물량은 멀쩡하게 목적지에 도착합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정
- **상황 A: 일일 10TB 로그 데이터 수집 시스템 구축**
    - **결정**: HDFS 도입 추진. 단일 파일 크기가 수백 MB 이상이고 '추가 전용(Append-Only)' 패턴을 가지므로 HDFS의 블록 구조에 적합.
- **상황 B: 수만 개의 작은 이미지 파일(Thumbnail) 저장**
    - **결정**: HDFS 비추천 (Anti-Pattern). NameNode의 메모리 효율이 급격히 저하됨(`Small File Problem`). 대신 Object Storage(S3 등)나 HBase와 같은 NoSQL 솔루션 권장.

### 2. 도입 체크리스트 (Checklist)

| 구분 | 항목 | 설명 |
|:---|:---|:---|
| **기술적** | **Latency vs Throughput** | 낮은 지연 시간(Low Latency)이 필요한 실시간 트랜잭션엔 부적합. 높은 처리량(High Throughput)이 중요한 배치 처리에 적합. |
| | **Block Size Tuning** | 64MB(Default) → 128MB/256MB 조정. 큰 블록은 메타데이터 부하를 줄이지만, Map 태스크의 병렬도를 낮출 수 있음. |
| **운영/보안적** | **Rack Awareness** | 机架感知 설정을 통하여 랙 단위 장애(Rack Failure)에 대비. 동일한 블록의 복제본을 서로 다른 랙에 분산. |
| | **Security** | Kerberos 인증 및 와이어(Wire) 암호화, ACL(Access Control List) 권한 관리 필수 적용. |

### 3. 안티패턴 (Critical Failure Points)
- **Small File Problem**: 파일 하나가 블록 하나 이상이므로, 작은 파일(예: 1KB)이 100만 개 있으면 NameNode에 100만 개의 메타데이터 레코드가 생성되어 RAM을 고갈시킴.
- **NameNode SPOF (Single Point of Failure)**: Hadoop 1.x까지는 NameNode 장애 시 클러스터 전체 중단. 이를 해소하기 위해 Hadoop 2.x 이후에서는 Active-Standy 구조의 HA (High Availability)와 **QJM (Quorum Journal Manager)** 도입이 필수적임.

### 📢 섹션 요약 비유
HDFS 운영은 **"거대한 창고의 관리"**와 같습니다. 쌀 한 톨씩 배달하는 것(작은 파일)으로는 창고 관리 대장(NameNode)의 머리가 아프지, 컨테이너 단위로 입고하는 것(대용량 파일)이야말로 이 창고의 진가가 발휘됩니다. 그리고 관리자가 쓰러지는 것(SPOF)을 막기 위해, 항상 대기 관리자(Standby NameNode)를 두어야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량/정성 기대효과 (ROI)
- **비용 절감**: 상용 SAN/NAS 대비 스토리지 도입 비용 약 1/10 수준 절감 (JBOD 활용).
- **확장성**: 노드 추가(Scale-out)만으로 저장 용량과 처리 대역폭을 선형적으로 확보 가능 (Linear Scalability).
- **데이터 안정성**: 3개의 복제본을 통해 연간 데이터 유실 확률(MTBF)을 비즈니스 무시 수준으로 낮춤.

### 2. 미래 전망 및 표준
- **Erasure Coding (EC)**: 기존 3-way 복제의 저장소 효율이 낮은 점(33% 활용)을 개선하여, Reed-Solomon 알고리즘 등을 통해 50% 수준의 저장소 효율을 유지하면서도 동일한 내구성을 확보하는 HDFS 3.0 기능 도입.
- **Cloud Native Integration**: AWS S3, Azure ADLS 등과 같은 객체 저장소와의 연동(Hadoop S3A FileSystem)을 통해 온프레미스 HDFS의 하이브리드 클라우드 전략으로 진화.

### 📢 섹션 요약 비유
HDFS의 진화는 **"복사본 3법칙에서 보존 기술로의 발전"**입니다. 과거에는 소중한 문서를 복사해서 3곳에 나누어 보관했다면(3-way Replication), 이제는 문서의 일부만 빠뜨려도 원본을 복구할 수 있는 수학적 코드(Erasure Coding)를