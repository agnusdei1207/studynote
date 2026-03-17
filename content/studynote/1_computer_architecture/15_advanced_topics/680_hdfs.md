+++
title = "HDFS (Hadoop Distributed File System)"
date = "2026-03-14"
weight = 680
+++

# HDFS (Hadoop Distributed File System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 저사향의 범용(Commodity) 하드웨어 군집을 활용하여 페타바이트(PB) 급 대용량 데이터를 저장하는 분산 스토리지 시스템으로, 소프트웨어적 중복성(Redundancy)으로 하드웨어 장애에 탄력적으로 대응하는 '신뢰성 있는 계층'을 제공합니다.
> 2. **가치**: '데이터 지역성(Data Locality)' 패러다임을 통해 네트워크 대역폭의 병목을 제거하여 대규모 배치(Batch) 처리 성능을 극대화하며, 기존 고가 SAN(Storage Area Network) 대비 비용 효율성을 10배 이상 향상시킵니다.
> 3. **융합**: 아파치 하둡(Apache Hadoop) 생태계(MapReduce, Spark, Hive)의 저장소 역할을 수행하며, 최근에는 컨테이너화(Kubernetes) 및 클라우드 네이티브 아키텍처와 결합하여 하이브리드 데이터 레이크의 핵심 기반으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**HDFS (Hadoop Distributed File System)**는 구글의 GFS (Google File System) 논문(2003)을 기반으로 설계된 Apache Hadoop 프로젝트의 핵심 스토리지 모듈입니다. 기존 파일 시스템과 달리 단일 서버의 용량 한계를 극복하기 위해 **'수평적 확장(Scale-out)'** 방식을 채택했습니다. 핵심 철학은 **"하드웨어는 고장이 나기 마련이며(Failure is the norm), 소프트웨어적으로 이를 감시하고 복구해야 한다"**는 가정에서 출发합니다. 이를 위해 블록 단위의 **다중 복제(Replication)** 기능을 기본으로 탑재하여 데이터 무결성과 고가용성(High Availability)을 보장합니다.

#### 2. 기술적 배경 및 진화
- **기존 한계 (NAS/SAN)**: 중앙집중식 스토리지는 확장 시 비용이 기하급수적으로 증가하며, 단일 실패점(SPOF) 취약성이 존재했습니다.
- **혁신적 패러다임**: 저렴한 x86 범용 서버(Commodity Hardware) 수천 대를 클러스터링하여 슈퍼컴퓨터 수준의 스토리지를 구축.
- **현재 비즈니스 요구**: 초기 대규모 웹 로그 분석에서 시작하여 현재는 AI/ML 학습 데이터셋 저장, 데이터 레이크(Data Lake) 구축의 표준 인프라로 자리 잡았습니다.

> **💡 개념 비유**
> 마치 도서관에 거대한 서가(HDFS)를 짓는데, 책(데이터) 한 권을 여러 곳에 복사해 두고, 사서(NameNode)가 어느 서가에 책이 있는지 머릿속에 기억하고 있어서, 건물이 무너져도 다른 곳의 책으로 내용을 복원할 수 있는 시스템입니다.

**📢 섹션 요약 비유**
한 명의 거인(고가의 메인프레임)에게 모든 짐을 지우는 대신, 만 명의 일반인(범용 서버)에게 짐을 잘게 쪼개어 나누어 들게 하고, 중요한 짐은 3명에게 똑같이 들게 하여(복제) 한 명이 쓰러져도 짐을 잃지 않는 '인력 난방(Human Crowd Computing)' 시스템입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 마스터/슬레이브 (Master/Slave) 토폴로지
HDFS는 **NameNode (마스터)**와 **DataNode (슬레이브)**로 구성된 계층형 아키텍처를 따릅니다. NameNode는 메타데이터(Metadata)를 전담하고, DataNode는 실제 데이터 블록을 저장합니다.

#### 2. 구성 요소 상세 분석

| 구성 요소 | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/저장소 | 비유 |
|:---:|:---|:---|:---|:---|
| **NameNode** | 마스터 관리자 | 파일 시스템 네임스페이스와 블록 맵(File → Block → DataNode Mapping)을 **RAM (Random Access Memory)**에 적재하여 관리함. | RPC / HTTP | 도서관장 (목차 관리) |
| **DataNode** | 저장소 워커 | 실제 데이터 블록(128MB 기본)을 로컬 디스크에 저장. NameNode에 3초마다 **Heartbeat** 전송 및 **Block Report** 제출. | Data Transfer Protocol | 서고 직원 (책 보관) |
| **Secondary NameNode** | 체크포인트 노드 | NameNode의 메모리 스냅샷(FsImage)과 편집 로그(EditLog)를 주기적으로 병합(Merge). 장애 복구를 위한 체크포인트 생성. (Hot Standby 아님) | HTTP | 정기 점검 직원 |
| **JournalNode** (HA) | 편집 로그 공유 | Active NameNode의 변경 사항을 Standby NameNode에 동기화하기 위한 공유 로그 저장소. (Quorum 기반) | TCP | 실시간 기록자 |

#### 3. 아키텍처 다이어그램 및 데이터 흐름

아래는 HDFS의 읽기/쓰기 동작과 HA 구성을 포함한 아키텍처입니다.

```ascii
+-----------------------------------------------------------------------+
|                           Hadoop Client                                |
|  (HDFS Commands, MapReduce Job, Spark Application)                    |
+--------+--------------------------------------------------------------+
         | (1) Request File Metadata (Open/GetBlockLocations)
+--------v----------------------+    (3) Direct Data Streaming           |
|  NameNode (Active)           | <-----------------------------------+  |
|  - Manage FS Image (RAM)     |                                    |  |
|  - Execute EditLog           |                                    |  |
+-------+------------+---------+                                    |  |
        | (2) Get Locations| (5) Log Edits                         |  |
        v                 v (To Journal Nodes)                       v  v
+-------+--------+  +-----------+                          +---------+--------+
| Journal Nodes  |  | DataNode 1 | <---(Block Replication)---> | DataNode 2 |
| (QJM Cluster)  |  | Rack A     |                            | Rack B      |
+----------------+  | [Block A_1]|                            | [Block A_2]|
                    +-----------+                            +------------+
                           ^
                            | (2) Data Transfer (Pipeline)
                    +-----------+      +---------+
                    | DataNode 3 | <----+ Client  |
                    | Rack B     |      | (Write) |
                    | [Block A_3]|      +---------+
                    +-----------+         
```

**[다이어그램 해설]**
1.  **메타데이터 조회**: 클라이언트는 NameNode(Acitve)에 파일 접근을 요청합니다. NameNode는 RAM에서 블록 위치 정보를 반환합니다.
2.  **데이터 스트리밍**: 클라이언트는 NameNode를 거치지 않고, 직접 DataNode에 접속하여 데이터를 읽거나 씁니다.
3.  **파이프라인 복제**: 쓰기 작업 시 클라이언트는 첫 번째 DataNode에 데이터를 전송하고, 해당 DataNode는 두 번째로, 두 번째는 세 번째로 데이터를 전달하는 파이프라인을 형성하여 복제 효율을 높입니다.
4.  **HA 동기화**: Active NameNode의 변경 사항은 JournalNode들을 통해 Standby NameNode로 실시간 전파됩니다.

#### 4. 핵심 동작 원리 (Data Locality & Block Size)
-   **Data Locality (데이터 지역성)**: 네트워크 혼잡을 방지하기 위해 연산(Compute)을 데이터가 있는 곳으로 이동시킵�습니다.
-   **Block Size (기본 128MB)**: 디스크 Seek 시간을 줄이고 전송 효율을 높이기 위해 큰 블록을 사용합니다. 또한, 하나의 파일이 여러 디스크에 분산되어 병렬 처리(I/O Throughput)가 가능합니다.

**📢 섹션 요약 비유**
도서관장(NameNode)은 책의 위치만 가르쳐주고, 독자(클라이언트)는 사서(DataNode)가 있는 곳으로 직접 가서 책을 읽습니다. 만약 연구원(컴퓨팅)이 분석을 해야 한다면, 책을 가지고 연구실로 오는 게 아니라 연구원이 도서관 서고(DataNode)로 이동하여 그 자리에서 분석(Data Locality)을 수행합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. HDFS vs 기존 파일 시스템 (POSIX)
기존 OS의 파일 시스템(예: ext4, XFS)은 저지연성(Low Latency)과 임의 접근(Random Access)에 최적화되어 있습니다. 반면 HDFS는 높은 처리량(High Throughput)과 순차 접근(Sequential Access)에 최적화되어 있습니다.

| 비교 항목 | POSIX File System (Local FS) | HDFS (Hadoop Distributed FS) |
|:---|:---|:---|
| **접근 패턴** | Random Read/Write (일반적) | Write-Once-Read-Many (WORM) |
| **데이터 크기** | KB ~ MB 단위 (Small File) | TB ~ PB 단위 (Big Data) |
| **전송 대역폭** | 낮은 Latency 중시 | 높은 Throughput 중시 |
| **노드 장애 처리** | 사용자 개입 필요 (fsck 등) | 자동 복구 (Replication) |

#### 2. HDFS vs Cloud Object Storage (S3)
빅데이터 저장소의 두 축인 HDFS와 AWS S3 (Simple Storage Service)를 비교 분석합니다.

| 구분 | HDFS (On-Premise) | S3 (Cloud Object Storage) |
|:---|:---|:---|
| **아키텍처 스타일** | **Tight Coupling**: 컴퓨팅 클러스터와 스토리지가 물리적으로 결합됨. (Compute near Storage) | **Loose Coupling**: 완전히 분리된 엔티티. (Compute and Storage Scaling independently) |
| **일관성 모델** | Strong Consistency (쓰기 즉시 반영) | Eventual Consistency (리전 간 복제 시) / Read-after-Write (단일 리전) |
| **비용 구조** | 하드웨어 도입 비용(CAPEX) + 유지보수 비용(OPEX) | 사용량 과금제(No upfront cost) |
| **융합성** | On-Premise Hadoop 생태계(Hive, Presto)와 최적화됨 | EMR, Redshift, Athena 등 클라우드 네이티브 서비스와 연동 용이 |

**⚠️ 과제 융합 관점 (OS & Network)**
-   **OS**: HDFS는 OS 파일 시스템 위에 구축되지만, OS의 캐시(Page Cache)를 우회하거나 직접 디스크 I/O를 제어하여 표준 계층을 오버라이딩합니다. 따라서 HDFS를 운영할 때는 OS의 스왑(Swap) 메모리 사용을 억제하고 커널 파라미터(Tuning)가 필수적입니다.
-   **Network**: Topology-Aware Scheduling (랙 인식 스케줄링)을 통해 네트워크 스위치 간 트래픽을 최소화합니다. 같은 랙 내에서 복제본을 우선 배치하여 스위치 대역폭을 절약하는 설계가 되어 있습니다.

**📢 섹션 요약 비유**
HDFS는 '주택 겸 주점(자가 운영)'과 같아서 빌딩을 직접 짓고 관리해야 하지만 맛집(데이터)이 바로 옆에 있어 이동 시간이 없습니다. S3는 '외부 창고(위탁 관리)'와 같아서 필요할 때마다 택배(네트워크)로 재료를 가져와야 하지만, 창고 크기를 마음대로 늘릴 수 있고 관리 주인이 따로 있습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 도입 의사결정 매트릭스 (Decision Matrix)
기업에서 HDFS 도입을 고려할 때 다음의 정량적/정성적 지표를 활용하여 결정합니다.

| 시나리오 | HDFS 도입 추천 | 대안 제시 (No HDFS) |
|:---|:---:|:---|
| **데이터 양** | 100TB 이상의 대용량 정형/반정형 데이터 | 수십 TB 미만의 중소규모 데이터 (NAS나 DB 충분) |
| **파일 크기** | 대용량 파일 (GB 단위) 위주 | 수천만 개의 소규모 파일 (Small File Issue 발생) |
| **처리 방식** | 배치 처리 (Batch), 일괄 분석 | 실시간 트랜잭션 (OLTP), Low Latency 요구 |
| **운영 역량** | DevOps 팀이 하드웨어/OS 관리에 능숙함 | 클라우드 관리형 서비스(MSA) 선호 |

#### 2. 실무 시나리오 및 문제 해결
-   **상황 1: NameNode 메모리 부족 (Small File Problem)**
    -   **증상**: 파일 수가 1억 개를 넘어가면서 NameNode Heap이 가득 차 OOM(Out Of Memory)이 발생. 각 파일/블록마다 약 150바이트의 메타데이터가 소요됨.
    -   **해결**: HDFS Archive(HAR) 파일 생성, 또는 Ozone(객체 스토리지 레이어) 도입하여 메타데이터 부하 분산.
-   **상황 2: DataNode 디스크 불균형 (Balancer)**
    -   **증상**: 특정 노드만 90% 찼는데 다른 노드는 20%인 상황. 특정 노드에만 부하가 집중됨.
    -   **해결**: `hdfs balancer` 명령어를 통해 임계값(Threshold)을 설정하고 블록을 재분배.

#### 3. 도입 체크리스트
-   **기술적 요건**: 
    -   [ ] 10Gbps 이상의 고속 스위치 네트워크 환경
    -   [ ] RAID 0 또는 JBOD 구성의 대용량 디스크 (6~12TB x 12ea)
    -   [ ] Linux OS 튜닝 (swappiness=0, max open files=100000)
-   **운영/보안적 요건**: 
    -   [ ] Kerberos 인증 기반의 보안 설정
    -   [ ] 정기적인 백업 및 재해 복구(Disaster Recovery) 훈련

#### 4. 안티패턴 (Anti-Patterns)
-   ❌ HDFS 위에 E-mail 서버 데이터 저장: 작은 파일이 너무 많아 NameNode가 마비됨.
-   ❌ 실시간 뱅킹 트랜잭션 처리: HDFS는 WORM 모델이라 잦은 업데이트/삭제가 불가능함.

**