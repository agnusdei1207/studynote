+++
title = "717. 클라우드 네이티브 스토리지 컴퓨팅 분리"
date = "2026-03-15"
weight = 717
[extra]
categories = ["Software Engineering"]
tags = ["Cloud Native", "Separation of Storage and Compute", "Scalability", "Infrastructure", "Architecture Pattern", "Efficiency"]
+++

# 717. 클라우드 네이티브 스토리지 컴퓨팅 분리

> ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터의 저장소(**Storage**)와 이를 처리하는 연산 자원(**Compute**)을 물리적·논리적으로 분리하여, 각 자원을 독립적으로 확장하고 최적화할 수 있게 하는 **클라우드 네이티브의 핵심 아키텍처 원리**이다.
> 2. **가치**: 컴퓨팅 자원의 **수평적 확장(Horizontal Scaling)**을 탈부착 가능한 형태로 구현하여, 인프라 비용(CAPEX/OPEX)을 획기적으로 절감하고 시스템의 **회복탄력성(Resilience)**을 보장한다.
> 3. **융합**: **서버리스(Serverless)** 및 **데이터 레이크하우스(Data Lakehouse)** 등 현대 데이터 아키텍처의 근간이 되며, **Ephemeral(일시적) 자원**과 **Persistent(영구) 데이터**의 생명주기를 분리하여 운영 효율을 극대화한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**스토리지-컴퓨팅 분리(Disaggregated Storage and Compute)**는 데이터를 처리하는 두뇌(CPU/Memory)와 데이터를 기억하는 창고(Disk/SSD)를 하나의 섀시(Chassis)에 통합하여 묶어두던 전통적인 **Monolithic Architecture(단일형 아키텍처)**의 한계를 극복하기 위해 등장했다. 

과거에는 데이터 양이 서버의 디스크 용량에 종속되었으나, 클라우드 환경에서는 **S3 (Simple Storage Service)**나 **NFS (Network File System)**와 같은 네트워크 부착형 스토리지를 통해 데이터를 **"공유 풀(Pool)"**에 보관하고, 필요할 때마다 **EC2 (Elastic Compute Cloud)**나 **Lambda** 같은 연산 자원을 붙였다 떼는 방식이 표준으로 자리 잡았다. 이는 애플리케이션이 **Stateless (무상태)** 설계를 따르도록 강제하여 시스템의 복잡도를 낮추고 유지보수성을 높이는 결과를 가져왔다.

#### 2. 등장 배경 및 패러다임 이동
- **① 기존 한계 (The Limitation)**: 특정 서버의 디스크가 꽉 차면, 연산 자원이 남아돌아도 더 이상 데이터를 저장할 수 없는 **Scale-up(수직 확장)**의 비효율 발생.
- **② 혁신적 패러다임 (Innovation)**: **SAN (Storage Area Network)** 및 클라우드 객체 스토리지의 발전으로 "네트워크 속도"가 "디스크 속도"를 따라잡거나, 디스크 병목을 회피할 수 있는 수준에 도달함.
- **③ 비즈니스 요구 (Business Demand)**: 빅데이터 분석 및 AI 학습 workload처럼, "몇 시간만 굴러가면 되는" 일시적 연산 자원 수요가 급증함에 따라 항시 켜져 있는 고가 서버 대신 **"불 때 쓰고 끄는"** 경제 모델 요구.

#### 3. 비유 시각화 (ASCII)
아래 다이어그램은 데이터와 연산이 결합된 구조에서 분리된 구조로의 변천을 나타낸다.

```text
[ Phase 1: Traditional (Coupled Architecture) ]
    Server 1            Server 2            Server 3
  [CPU+Disk]           [CPU+Disk]           [CPU+Disk]
   (Data A)             (Data B)             (Data C)
   └─ Data A는 Server 1을 벗어날 수 없음 (Silo)

[ Phase 2: Cloud Native (Disaggregated Architecture) ]
        
    [Compute Plane]                   [Storage Plane]
 ┌────────┐ ┌────────┐ ┌────────┐      ┌──────────────────────┐
 │ Node A │ │ Node B │ │ Node C │      │  Shared Data Pool    │
 │(State) │ │(State) │ │(State) │      │ (S3, HDFS, DB)       │
 └───┬────┘ └───┬────┘ └───┬────┘      └──────────┬───────────┘
     │          │          │                     │
     └──────────┴──────────┴────── [Network] ─────┘
            ▲
            │  (On-Demand Attachment)
            │  Compute nodes can be scaled independently
```
*(해설: Phase 1에서 데이터는 갇혀있으나, Phase 2에서는 Compute 노드가 유연하게 증설되고 교체 가능하며, 데이터는 영구적으로 보존됨.)*

> **📢 섹션 요약 비유**: 마치 요리사가 자신의 칼만 가지고 다니며, 필요할 때마다 공용 냉장고(Storage)에서 식재료를 꺼내 빈 주방(Compute)에 들어가 요리를 하고 나오는 **'이동식 푸드트럭'** 시스템과 같습니다. 주방 공간이 부족하면 트럭을 더 대기만 하면 되고, 냉장고가 꽉 차면 냉장고만 더 크게 교체하면 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 기술 스택 (상세 분석)
스토리지-컴퓨팅 분리를 구현하기 위해서는 각 계층의 명확한 역할 분담과 메타데이터 관리가 필수적이다.

| 구성 요소 (Component) | 핵심 역할 | 상세 내부 동작 및 기술 | 주요 프로토콜/스택 |
|:---|:---|:---|:---|
| **Compute Layer**<br>(컴퓨팅 계층) | **순수 연산 처리** | 로컬 디스크에 상태(State)를 저장하지 않음. 모든 데이터는 네트워크를 통해 Remote Storage에서 읽고 쓴다. | **Kubernetes (K8s)**, **AWS Lambda**, **Apache Spark** |
| **Storage Layer**<br>(스토리지 계층) | **영구 데이터 보관** | EC2 인스턴스나 Pod가 종료되더라도 데이터는 유지됨. 고가용성을 위해 데이터 분산/복제(RAID, Erasure Coding) 수행. | **Amazon S3**, **EFS (Elastic File System)**, **HDFS** |
| **Metadata Layer**<br>(메타데이터 계층) | **데이터 지도(Map)** | 파일이 실제 어느 스토리지 노드에 있는지, 데이터의 Schema가 무엇인지 관리. 분리 아키텍처의 '디렉토리' 역할. | **Hive Metastore**, **AWS Glue**, **etcd** |
| **Interconnect**<br>(상호 연결망) | **고속 데이터 통로** | Compute와 Storage �의 병목을 방지하기 위해 **NVMe-oF (Non-Volatile Memory over Fabric)** 등의 고속 프로토콜 사용. | **100Gbps+ Ethernet**, **RDMA (Remote Direct Memory Access)** |

#### 2. 상세 아키텍처 다이어그램
다음은 AWS 기반의 MPP (Massively Parallel Processing) 환경에서 분리 아키텍처가 동작하는 구조이다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                         Compute Cluster (Auto-scaling)                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │   Leader  │  │  Worker 1 │  │  Worker 2 │  │  Worker N │  (Stateless)  │
│  │ (Driver)  │  │  (Node)   │  │  (Node)   │  │  (Node)   │               │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘               │
│        │             │             │             │                        │
│        └─────────────┴─────────────┴─────────────┘                        │
│                         ▲         │                                       │
│                         │         │ (High Throughput Network)             │
│                         │         ▼                                       │
└─────────────────────────┼─────────────────────────────────────────────────┘
                          │
┌─────────────────────────┼─────────────────────────────────────────────────┐
│                         │    Metadata Service                             │
│                         │  (Catalog, Schema, Partitioning Info)           │
├─────────────────────────┼─────────────────────────────────────────────────┤
│                         ▼                                                 │
│  ┌──────────────────────────────────────────────────────────────┐        │
│  │              Shared Storage Layer (Distributed)              │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │        │
│  │  │  Node 1  │  │  Node 2  │  │  Node 3  │  │  Node N  │    │        │
│  │  │ (Hot Data│  │ (Cold    │  │ (Replica │  │ (Archive │    │        │
│  │  │  Cache)  │  │  Data)   │  │  Set)    │  │  Tier)   │    │        │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │        │
│  └──────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────────────────┘
```

*(해설: Compute 계층의 Worker 노드들은 작업이 끝나면 즉시 소멸(Ephemeral)된다. 하지만 Storage 계층의 Node들은 데이터 영속성을 위해 항상 유지되거나, S3 Object Storage처럼 무한히 확장 가능한 형태로 존재한다.)*

#### 3. 심층 동작 원리 (Worker Lifecycle in Decoupled System)
1. **Job Initiation**: 사용자가 Batch Job이나 Query를 요청하면, Master Node는 **Metadata Store**에 접근하여 데이터의 위치 정보를 파악한다.
2. **Provisioning**: **Cluster Manager (예: YARN, K8s)**는 필요한 만큼의 Compute Node(VM or Container)를 스토리지 상태와 무관하게 즉시 생성한다.
3. **Data Fetching**: Compute Node는 Metadata를 참조하여 **Storage Node**에 직접 접속(접속은 병렬로 이루어짐)하여 데이터를 로컬 캐시나 메모리로 로딩한다.
4. **Processing**: 연산을 수행하며 결과를 Intermediate Storage(예: Redis, S3 Staging)에 저장한다.
5. **Teardown**: 작업 완료 후 Compute Node는 즉시 종료(Terminate)되어 비용이 발생하지 않는다.

#### 4. 핵심 코드 예시 (Python/Pseudocode)
```python
# Decoupled computing pattern using AWS Boto3 (Pseudo)
import boto3

def run_decoupled_job():
    s3_client = boto3.client('s3')      # Storage Interface
    ec2_client = boto3.client('ec2')    # Compute Interface
    
    # 1. Data exists in Storage regardless of Compute
    data_location = "s3://raw-data-bucket/january_logs/"
    
    # 2. Spin up Compute only when needed (Scale-out)
    new_instances = ec2_client.run_instances(
        ImageId="ami-data-processing-image",
        MinCount=10, MaxCount=50,  # Flexible Compute
        InstanceType="c5.9xlarge", # High Compute, Low Storage
        UserData=f"#!/bin/bash\npython process.py --input {data_location}"
    )
    
    # 3. Compute nodes process data from S3 and write results back
    # result -> "s3://results-bucket/output/"
    return "Job started, compute nodes will auto-terminate on finish."
```

> **📢 섹션 요약 비유**: **'렌터카와 주차장'** 시스템과 같습니다. 여행객(Compute)은 필요할 때만 렌터카를 빌려 목적지로 이동하고, 여행이 끝나면 차를 반납합니다. 중요한 짐(Data)은 주차장(Storage)에 안전하게 보관되므로, 차가 바뀌어도 짐은 그대로 남습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Shared-Nothing vs. Shared-Disk
스토리지 분리를 구현하는 두 가지 주요 접근 방식(MPP Shared-Nothing vs. Disaggregated Shared-Disk)의 비교 분석이다.

| 비교 항목 | **Shared-Nothing (Cluster)** | **Disaggregated (Cloud Native)** |
|:---|:---|:---|
| **구조** | 각 서버가 CPU와 Disk를 모두 가짐. 데이터가 샤딩(Sharding)되어 분산 저장됨. | **Centralized Shared Storage**와 **Stateless Compute**로 완전 분리. |
| **확장성 (Scalability)** | 데이터를 **Re-partitioning(재분배)**해야 하므로 확장이 번거로움 (Ex: Cassandra, Hadoop HDFS Legacy). | **Compute**와 **Storage**가 독립적. 스토리지 용량에 맞춰 연산 자원만 10배로 증설 가능. |
| **유연성 (Agility)** | 노드 장애 시 해당 노드에 있는 **데이터 유실** 또는 복구 시간 소요. | 노드 장애 시 다른 노드가 즉시 Storage에 연결하여 **복구(Resilient)**. |
| **비용 효율** | 연산 증설 시 불필요한 디스크 비용까지 같이 발생. | 연산 작업이 없을 때는 **Compute 비용 0** (Stop/Terminate). |
| **Latency** | 로컬 디스크 접근이라 **지연율이 낮음(Low Latency)**. | 네트워크를 통해 접근하므로 대역폭에 의존적 (High Bandwidth 필요). |

#### 2. 융합 관점 (Convergence)
- **DevOps와의 결합**: **Blue-Green Deployment**나 **Canary Deployment** 시, 컴퓨팅 서버를 새 버전으로 교체하는 동안 기존 스토리지에 접속하여 데이터 무손실 배포가 가능하다.
- **보안 (Security)**: 스토리지 계층에 **IAM (Identity and Access Management)** 정책을 적용하여, 컴퓨팅 노드가 해킹당하더라도 스토리지의 데이터는 직접 접근을 막거나 Encryption된 상태로 보호할 수 있는 **Defense in Depth** 구현이 용이하다.

#### 3. 성능 지표 분석 (Latency vs Throughput)
```text
   (Processing Time)
      ▲
      │     ┌────────── Shared-Nothing (Local Disk)
      │     │  (속도는 빠르지만 병목 발생 시 확장 어려움)
Time │   ──┘
      │     
      │             ┌────────── Disaggregated (Network Storage)
      │             │  (초기 Latency는 있으지만 병렬 처리 Throughput은 압도적)
      │         ─