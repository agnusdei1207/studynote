+++
title = "570. Ceph - 분산 객체 스토리지 및 파일 시스템"
date = "2026-03-14"
weight = 570
+++

# 570. Ceph - 분산 객체 스토리지 및 파일 시스템

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Ceph는 단일 분산 클러스터 내에서 객체(Object), 블록(Block), 파일(File) 스토리지를 통합 제공하는 소프트웨어 정의 스토리지(SDS, Software-Defined Storage) 플랫폼으로, 데이터의 위치를 계산하여 결정하는 **CRUSH (Controlled Replication Under Scalable Hashing)** 알고리즘을 핵심 경쟁력으로 가진다.
> 2. **가치**: 중앙 집중형 메타데이터 서버의 병목을 제거하여 수평적 확장성(Linear Scalability)을 확보하며, 노드 장애 시 자동으로 데이터를 리밸런싱하고 복구하는 무중단 운영(RTO near-zero)을 실현한다.
> 3. **융합**: POSIX 호환 파일 시스템과 S3 호환 객체 스토리지, 그리고 가상화 환경을 위한 블록 스토리지를 하이퍼바이저(KVM, VMware) 및 컨테이너 오케스트레이션(Kubernetes)과 융합하여 유연한 인프라를 구성한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**Ceph**는 상용 하드웨어(Commodity Hardware)를 기반으로 대용량 데이터를 저장 관리하는 오픈소스 분산 스토리지 시스템이다. 기존 스토리지가 중앙의 컨트롤러(Controller)나 메타데이터 룩업 테이블(Lookup Table)에 의존하여 확장성에 한계를 보였던 것과 달리, Ceph는 **CRUSH (Controlled Replication Under Scalable Hashing)** 알고리즘을 통해 클라이언트가 직접 데이터의 위치를 계산하도록 설계되었다. 이는 "스마트 데이터(Smart Data), 덤 노드(Dumb Node)"라는 철학을 구현한 것으로, 데이터가 자신의 위치를 스스로 알고 있으므로 별도의 조회 과정 없이 저장소 노드인 **OSD (Object Storage Device)**로 직접 접근한다.

### 2. 통합 스토리지 아키텍처 (Unified Storage)
Ceph는 서로 다른 세 가지 스토리지 인터페이스를 하나의 **RADOS (Reliable Autonomic Distributed Object Store)** 클러스터 위에 구축하여 데이터의 사일로(Silo) 현상을 제거한다. 이를 통해 사용자는 워크로드의 성격에 따라 최적化的인 스토리지 프로토콜을 선택하면서도, 백엔드 데이터는 중복 없이 단일 클러스터에 통합 관리된다.

```text
         +-------------------------------------------------------+
         |               User / Application Space                 |
         +-------------------------------------------------------+
                    |                |                |
         +----------+-------+  +-----+-------+  +----+----------+
         |  Ceph FS (File)  |  |   RBD (Block) |  | RADOSGW (S3) |
         +------------------+  +--------------+  +---------------+
         | POSIX Interface  |  | Librbd / iSCSI|  | RESTful API   |
         +------------------+  +--------------+  +---------------+
                    |                |                |
         +-------------------------------------------------------+
         |           LIBRADOS (Native Client Interface)           |
         +-------------------------------------------------------+
                                |
         +-------------------------------------------------------+
         |               RADOS (Storage Cluster)                 |
         |   (Consisting of Monitors, OSDs, MDS)                 |
         +-------------------------------------------------------+
```

### 3. 등장 배경 및 비즈니스 요구
① **확장성의 한계 극복**: 전통적인 **NAS (Network Attached Storage)**나 **SAN (Storage Area Network)**은 스토리지 컨트롤러의 성능과 메타데이터 서버의 처리량에 따라 병목이 발생했다. ② **비용 절감**: 고가의 전용 장비 대신 범용 하드웨어 사용을 통해 **CAPEX (Capital Expenditure)**를 낮추고자 했다. ③ **클라우드 네이티브**: OpenStack, Kubernetes와 같은 클라우드 환경에서 **API (Application Programming Interface)** 기반의 프로그래매틱한 스토리지 관리가 절실해졌다.

📢 **섹션 요약 비유**: Ceph는 "스스로 주소를 아는 지능형 우편물 시스템"과 같습니다. 기존 우편물은 중앙 우체국(메타데이터 서버)에 주소를 물어봐야 했지만, Ceph 우편물은 스스로 수신자 주소를 계산하여 분류되므로 우체국이 문이 닫혀도 배달이 멈추지 않습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 및 역할 (5개+ 모듈)

Ceph의 아키텍처는 수평 확장이 가능한 여러 데몬(Daemon)들로 구성된다.

| 요소명 | 전체 명칭 (Abbreviation) | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **OSD** | **Object Storage Device** | 실제 데이터를 저장/복제/복구하는 데몬. 디스크 하나당 하나의 OSD가 매핑되며 Heartbeat를 주고받으며 상태를 감시함. | TCP/IP, Heartbeat | 현장 작업반 |
| **MON** | **Monitor** | 클러스터 맵(**Cluster Map**)을 유지하고 쿼럼(**Quorum**)을 형성하여 클러스터의 상태를 관리. 리더 선출은 Paxos 합의 알고리즘 사용. | Paxos | 관제 센터 |
| **MDS** | **Metadata Server** | **CephFS** (파일 시스템) 사용 시에만 활성화. 파일의 디렉터리 구조와 메타데이터 캐싱을 담당하여 POSIX 호환성 보장. | POSIX | 도서관 사서 |
| **MGR** | **Manager** | 클러스터의 성능 지표(**Throughput**, **Latency** 등)를 수집하고 대시보드를 제공하며 모니터링 및 플러그인 기능 지원. | REST API | 경영 지원팀 |
| **RGW** | **RADOS Gateway** | **S3 (Simple Storage Service)** / Swift API와 같은 RESTful 인터페이스를 제공하여 애플리케이션이 객체 스토리지에 접근하게 하는 게이트웨이. | S3/Swift API | 접수 창구 |

### 2. CRUSH 알고리즘과 데이터 배치 로직

Ceph의 핵심은 **RADOS**로, 모든 데이터는 OSD에 객체 형태로 저장된다. 아래는 클라이언트가 데이터를 쓰는 과정이다.

```text
[ Client (User/App) ]
      |
      | 1. I/O Request (File/Object)
      ▼
[ LIBRADOS (Library) ]
      |
      | 2. Get Cluster Map from MON (Cached)
      ▼
[ CRUSH Algorithm ]
      |
      | 3. Calculate Location (Deterministic Hashing)
      | Input: Object ID + Pool ID + Rule
      ▼
    [ PG (Placement Group) ]
      | (Logical grouping of objects)
      |
      +-----------------------------------+
      |            Acting Set             |
      |  [ OSD 1 (Primary) ] [ OSD 2 ] [ OSD 3 ]  <--- Target OSDs
      +-----------------------------------+
      |
      | 4. Direct Write & Replicate
      ▼
[ Physical Disks (HDD/SSD/NVMe) ]
```

**해설:**
1.  **CRUSH 계산**: 클라이언트는 MON으로부터 클러스터의 토폴로지 정보(맵)를 받는다. 이 맵은 디스크의 위치(Host → Rack → Row → DC)까지 계층적으로 표현된다.
2.  **OSD 선정**: CRUSH 알고리즘은 입력값(Object ID)과 클러스터 맵을 해싱(Hashing)하여 데이터가 저장될 OSD들을 '계산'해낸다. 이때 중간에 **PG (Placement Group)**라는 논리적 그룹 개념을 사용하여 관리 부하를 줄인다.
3.  **직접 I/O**: 별도의 헤비급 데이터 라우터가 없으므로, 클라이언트는 계산된 OSD로 직접 데이터를 전송한다(Primary OSD에 쓰고, 이를 복제하여 Secondary OSD들로 전송).
4.  **복제**: 가용성을 위해 데이터를 여러 OSD에 중복 저장(Replication)하거나 **Erasure Coding**으로 분산 저장한다.

### 3. 심층 동작 원리: PG (Placement Group)의 상태 전이

수십억 개의 객체(Objects)를 개별적으로 관리하는 것은 불가능하다. Ceph는 객체들을 해시 파티셔닝(Partitioning)하여 PG라는 버킷(Bucket)에 묶어 관리한다. PG는 생성되어 `Active` 상태가 되기까지 여러 단계를 거치며, 이는 클러스터의 건강 상태를 나타낸다.

```text
        +--------+
        |  CREATING  | (Initial State)
        +--------+
             |
             v
        +--------+        Peering (Replicas sync logs)
        |  PEERING  | <-------------------------------+
        +--------+                                 |
             |                                       |
             v (Data is available for I/O)           | (Failure detected)
        +--------+                                 |
        |  ACTIVE  | --------------------------------+
        +--------+                                 |
             |                                       v
             | ( OSD failure or rebalancing )    +--------+
             v                                    | DEGRADED|
        +--------+                                +--------+
        |  RECOVERING  | (Replicating missing objects)
        +--------+
```

```python
# Python-style Pseudo Code for CRUSH Mapping
def get_osds_for_object(object_id, pool_id, crush_map):
    # 1. Hash the object ID to an integer
    # This ensures uniform distribution
    hash_val = hash(object_id) 
    
    # 2. Map to a Placement Group (PG)
    # pg_num determines the granularity of the map
    pg_id = (hash_val % pool_pgs) + pool_pg_offset
    
    # 3. Use CRUSH rules to map PG to specific OSDs
    # Considering topology: Host -> Rack -> Row -> DC
    # It tries to select OSDs from different failure domains
    osd_list = crush_map.calc_replicated_osds(pg_id, replica_size)
    
    return osd_list # e.g., [osd.12, osd.5, osd.20]
```

📢 **섹션 요약 비유**: Ceph의 아키텍처는 "자율 주행 자동차 시스템"과 같습니다. 중앙 교통 통제소(MON)가 도로 상태(맵)만 알려주면, 각 자동차(OSD)는 스스로 경로를 계산(CRUSH)하여 목적지로 이동합니다. 중앙 통제소가 모든 차량의 움직임을 명령하는 것이 아니므로 교통체증(병목)이 발생하지 않습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술 심층 비교: Ceph vs. Legacy Hadoop HDFS

현대의 빅데이터 및 클라우드 환경에서 Ceph와 HDFS는 가장 대표적인 분산 스토리지이지만, 내부 동작 메커니즘에는 큰 차이가 있다.

| 비교 항목 | Ceph (RADOS) | Legacy HDFS (Hadoop Distributed File System) | Winner (Context) |
|:---|:---|:---|:---|
| **아키텍처** | Metadata-less (Compute-based) | Centralized Metadata (NameNode) | **Ceph** (확장성) |
| **데이터 단위** | 작은 Object (수 MB ~ GB) | 큰 Block (기본 128MB) | **HDFS** (배치 처리) |
| **데이터 접근** | Random Access 가능 (RBD) | Write-Once-Read-Many (Sequential) | **Ceph** (다용도) |
| **일관성 모델** | Strong Consistency | Close-to-Consistency | **Ceph** (실시간성) |
| **프로토콜** | Ceph Native, S3, NFS, iSCSI | WebHDFS, NFS Gateway | **Ceph** (호환성) |
| **네트워크** | TCP/IP (Low Latency 필요) | TCP/IP (Short-Circuit Local Read) | **HDFS** (대용량 스캔) |

### 2. 타 과목 및 기술 융합 분석

**A. 네트워크 & 하드웨어 (Network & Hardware)**
-   **패킷 처리**: Ceph는 데이터 복제(Replication)를 위해 네트워크 대역폭을 많이 소모한다. 특히 복구(Recovery) 시 트래픽 폭증이 발생하므로, 10Gbps 이상의 고속 네트워크와 분리된 **Cluster Network** 구성이 필수적이다.
-   **CPU 의존도**: CRUSH 연산과 **Erasure Coding** (纠删码) 암호화/복호화 연산을 위해 디스크보다는 **CPU**의 성능에 의존적인 경향이 있다.

**B. 운영체제 및 가상화 (OS & Virtualization)**
-   **Libvirt/Qemu 통합**: Ceph **RBD (RADOS Block Device)**는 Kernel 모듈이 아닌 Userspace 라이브러리(`librbd`)를 통해 **KVM (Kernel-based Virtual Machine)**과 직접 통신할 수 있다. 이를 `rbd` 명령어 없이 VM 내부에서 직접 Ceph 볼륨을 마운트하는 것이 가능하며, 커널 컨텍스트 스위칭 오버헤드를 줄여 성능을 향상시킨다.
-   **Kubernetes CSI**: `Ceph-CSI` 드라이버를 통해 Pod가 **PVC (Persistent Volume Claim)**을 요청하면, Ceph는 동적으로 RBD 이미지를 생성하여 마운트해 준다. 이는 **CSP (Cloud Service Provider)**의 블록 스토리지와 완벽히 동일한 인터페이스를 제공한다.

```text
   [ Pod (App) ]
        |
        | mount
        v
   [ PVC ]
        |
        | Bind
        v
+--------------------------+
|        K8s Master        |
|  (Dynamic Provisioning)  |
+--------------------------+
        |
        | RBD Create / Map
        v
+--------------------------+
|      Ceph Cluster        |
|  (RBD Image created)     |
+--------------------------+
```

📢 **섹션 요약 비유**: Ceph는 "스위스 아미 나이프"와 같습니다. 단순한 칼(파일 저장)만 하는 것이 아니라, 드라이버(블록 저장), 집게(객체 저장), 가위(Erasure Coding) 등 다양한 도구를 한 자루에 통합하여 어떤 작업(앱 유형)이든 처리할 수 있는 만능 도구입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 매트릭스

**시나리오 A: AI 학습 데이터 레이크 구축**
-   **요구사항**: 수십 **PB (Petabyte)** 규모의 이미지/영상 데이터 저장, 높은 쓰기 처리량.
-   **기술사적 판단**: Ceph Object Storage(**RADOSGW**)를 선택하고 **EC (Erasure Coding)** 프로파일을 적용한다.
    -   이유: 3중 복제(Replication)는 스토리지 효율이 33%에 불과하지만, EC(예: 8+2