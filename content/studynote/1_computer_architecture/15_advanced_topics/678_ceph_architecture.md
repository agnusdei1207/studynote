+++
title = "Ceph 스토리지 아키텍처"
date = "2026-03-14"
weight = 678
+++

# Ceph 스토리지 아키텍처 (Ceph Storage Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 클러스터에서 블록(Block), 객체(Object), 파일(File) 스토리지를 통합 제공하는 소프트웨어 정의 스토리지(SDS, Software-Defined Storage)로, RADOS(Reliable Autonomic Distributed Object Store)라는 분산 객체 저장소를 핵심 엔진으로 사용합니다.
> 2. **가치**: 중앙 메타데이터 서버의 병목을 제거하는 **CRUSH(Controlled Replication Under Scalable Hashing)** 알고리즘을 통해 무한 확장성(Scalability)과 고가용성(High Availability)을 확보하며, 벤더 락인(Vendor Lock-in)을 해제합니다.
> 3. **융합**: OpenStack, Kubernetes 등 클라우드 환경의 표준 백엔드로 활용되며, 최근 NVMe-oF(NVMe over Fabric)와 SPDK(Storage Performance Development Kit)를 결합하여 고성능 AI 워크로드까지 지원하는 진화형 인프라입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
Ceph(세프)는 2004년 Sage Weil가 박사학위 논문으로 시작하여 현재 오픈 소스계의 스타 프로젝트로 발전한 **소프트웨어 정의 스토리지(SDS)**입니다. 기존 스토리지가 고가의 전용 하드웨어 컨트롤러에 의존하는 반면, Ceph는 범용 x86 서버와 네트워크를 결합하여 거대한 스토리지 풀을 구축합니다.

Ceph 아키텍처의 핵심은 상위 서비스 계층과 하위 데이터 저장 계층의 철저한 분리에 있습니다. 하단에는 신뢰할 수 있고 자율적인 분산 객체 저장소인 **RADOS (Reliable Autonomic Distributed Object Store)**가 위치하며, 상단에는 이를 기반으로 블록 디바이스(RBD), 객체 인터페이스(RGW), 파일 시스템(CephFS)을 제공하는 게이트웨이들이 위치합니다. 이를 통해 사용자는 물리적 저장 위치에 상관없이 논리적으로 통합된 스토리지 자원을 활용할 수 있습니다.

#### 2. 등장 배경 및 철학
① **전통 스토리지의 한계**: 기존 **SAN (Storage Area Network)** 이나 **NAS (Network Attached Storage)**는 중앙의 메타데이터 컨트롤러가 데이터의 위치를 관리합니다. 데이터가 페타바이트(PB)급으로 증가하면 이 컨트롤러가 처리해야 할 요청이 폭주하여 병목(Bottleneck) 현상이 발생하고, 확장을 위해서는 고가의 장비를 교체해야 하는 **Scale-up** 방식의 한계가 있었습니다.
② **혁신적 패러다임**: Ceph는 메타데이터를 분산하여 관리하고, 데이터 위치를 클라이언트가 직접 계산하게 함으로써 중앙 병목을 제거했습니다. 저렴한 범용 서버를 추가하여 성능과 용량을 동시에 늘리는 **Scale-out** 방식을 지향합니다.
③ **현재의 비즈니스 요구**: 클라우드 네이티브(Cloud Native) 환경에서 가상머신과 컨테이너가 폭증함에 따라, 수평 확장이 가능하고 API 기반으로 자동화된 스토리지의 필요성이 대두되면서 Ceph는 프라이빗 클라우드의 표준이 되었습니다.

#### 📢 섹션 요약 비유
하나의 거대한 발전소(RADOS)에서 전기를 생산한 뒤, 사용자의 필요에 따라 220V 가정용 콘센트(블록), USB 포트처럼 쓰는 객체, 공장용 고압 전선(파일) 등으로 자유롭게 변환해서 공급하는 **만능 에너지 변환소**와 같습니다.

```ascii
+-------------------------------------------------------+
|               Legacy Storage vs Ceph                  |
+---------------------------+---------------------------+
|  Legacy (Centralized)     |  Ceph (Distributed)       |
+---------------------------+---------------------------+
|  [Controller]             |  [Client 1] [Client 2]... |
|    | / \ | / \ |          |    |         |            |
|  [Disk] [Disk] [Disk]     |  [OSD]--[OSD]--[OSD]      |
|  (Bottleneck)             |  (Scalable Cluster)       |
+---------------------------+---------------------------+
```
*(해설: 전통 스토리지는 모든 경로가 중앙 컨트롤러를 통해야 하므로 병목이 발생하지만, Ceph는 클라이언트와 OSD가 직접 통신하므로 수평 확장이 가능합니다.)*

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Ceph는 "동적 분산 객체 저장소"인 RADOS 위에서 구축됩니다. 모든 데이터는 기본적으로 Object 단위로 저장되며, CRUSH라는 해시 알고리즘을 통해 배치됩니다.

#### 1. 주요 구성 요소 상세
| 요소 | 전체 명칭 (Abbreviation) | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **OSD** | **Object Storage Daemon** | - 물리 디스크당 1개 프로세스 실행<br>- 데이터 I/O 처리, 복제(Replication), 복구(Recovery) 담당<br>- Heartbeat를 통해 서로 감시 | 네트워크, 디스크 I/O | 창고 관리자 (물건 직접 보관) |
| **MON** | **Monitor** | - 클러스터 맵(OSD 상태, 네트워크) 유지<br>- Paxos 합의 알고리즘을 통해 Quorum 형성<br>- 데이터 위치는 알지 못하며 클러스터 건강성만 관리 | Paxos Algorithm | CCTV 관제실 (건물 상태만 모니터링) |
| **MDS** | **Metadata Server** | - CephFS(파일 시스템)에서만 사용<br>- 디렉터리 구조, 파일 권한 등 메타데이터 관리<br>- 데이터 I/O는 OSD로 직접 전달 | POSIX, Kernel | 사무실 도서관 관리자 (카탈로그 정리) |
| **LibRADOS** | RADOS Library | - 클라이언트 프로세스 내에 탑재되는 라이브러리<br>- MON에게 맵을 받고 CRUSH 연산을 수행하여 OSD 직접 통신 | TCP/IP, CRUSH | 내비게이션 앱 (길 찾기 연산) |
| **CRUSH** | **Controlled Replication Under Scalable Hashing** | - 일관성 해시 함수(Consistent Hashing) 기반<br>- 클라이언트 측에서 데이터 위치를 계산하는 알고리즘<br>- 디스크 장애 시 데이터 재배치 알고리즘 수행 | Hash Map, Pseudo-Random | 스마트폰 주소 검색 로직 |

#### 2. 아키텍처 구조 및 데이터 흐름
데이터 입장에서 가장 효율적인 경로를 통해 I/O가 처리되는 구조입니다.

```ascii
+-----------------------------------------------------------------+
| [Client] (e.g., OpenStack Nova, Kubernetes Pod)                |
|                                                                 |
|   ① Request: "Write Data 'IMG_A01'"                             |
|      ↓                                                          |
|   ② Fetch Cluster Map from MON (only if stale)                 |
|      ↓                                                          |
|   ③ Run CRUSH Algorithm locally:                                |
|      Input: Object ID -> Hash -> Rule Set -> Output: OSD Set    |
|      Result: Target OSD 3, 7, 23 (Primary + Replicas)           |
|      ↓                                                          |
|   ④ Direct TCP/IP Connection to Target OSDs (No Proxy!)         |
+-----------------------------------------------------------------+
                             | Network (Public/Cluster Network)
                             v
+-----------------------------------------------------------------+
| [OSD Cluster] (The RADOS Layer)                                 |
|                                                                 |
|  [OSD 3] (Primary)      [OSD 7] (Replica)      [OSD 23] (Replica)|
|   +---------+            +---------+            +---------+    |
|   | Journal |            | Journal |            | Journal |    |
|   +----+----+            +----+----+            +----+----+    |
|        |                      |                      |        |
|  [Disk/Store]            [Disk/Store]            [Disk/Store]   |
|                                                                 |
|  [MON] [MON] [MON]  <-- Paxos Quorum -->  [MDS] (for CephFS)   |
+-----------------------------------------------------------------+
```

*(해설: 클라이언트는 데이터를 쓸 때 중앙 서버를 거치지 않습니다. MON으로부터 전체 지도(Map)를 받아 로컬에서 CRUSH 연산을 수행한 뒤, 데이터가 저장될 OSD 3대(Primary 1개 + Replica 2개)를 계산하고 곧바로 접속합니다. 이러한 **Direct Communication(직접 통신)** 구조가 Ceph의 고성능 비결입니다.)*

#### 3. 심층 동작 원리: CRUSH 알고리즘 (중요)
CRUSH는 단순 해싱이 아니라 스토리지 클러스터의 물리적 토폴로지(Rack, Room, Row)를 반영하여 데이터를 배치합니다. 이는 장애 도메인(Failure Domain) 분리에 필수적입니다.

**동작 과정:**
1. **Placement Group (PG) 그룹화**: 수십억 개의 오브젝트를 직접 관리하면 부담이 크므로, Ceph는 오브젝트를 PG라는 논리적 그룹으로 묶어 관리합니다.
2. **CRUSH Lookup**: `Hash(Object ID) -> PG ID -> CRUSH Map(Ruleset) -> Target OSDs` 순서로 계산됩니다.
3. **Replication**: PG는 여러 OSD에 복제됩니다. 이때 CRUSH Map 설정에 따라 "같은 랙(Rack)에 복제본을 두지 않는다"는 같은 제약 조건을 적용할 수 있습니다.
4. **Rebalancing**: 새로운 OSD가 추가되면 CRUSH 맵만 변경되므로, 데이터의 일부만 이동(Rebalance)하여 전체 클러스터의 균형을 맞춥니다.

#### 4. 핵심 코드 로직 (Pseudo-code)
```python
# CRUSH Algorithm Logic (Simplified)
def get_osd_for_object(object_name, pg_num, replica_count, crush_map):
    # 1. Hash Object Name to get PG ID
    pg_hash = hash(object_name)
    pg_id = pg_hash % pg_num

    # 2. Get Rules for specific Pool (e.g., Replicated Rule)
    rule = crush_map.rules[pg_id.pool_id]

    # 3. Select Root (e.g., 'default') and Failure Domain (e.g., 'host')
    current_bucket = crush_map.root
    
    selected_osds = []
    
    # 4. Select 'replica_count' distinct OSDs
    for r in range(replica_count):
        # R' value (replica rank) is used as seed for randomness
        seed = (pg_id << 32) | r 
        osd_bucket = crush_bucket_select(current_bucket, seed, rule.type)
        
        if osd_bucket == -1: # Fail to find distinct bucket
            return "Not enough OSDs"
            
        selected_osds.append(osd_bucket.id)
        
        # Apply 'take_next' constraint to ensure OSDs are on different hosts/racks
        current_bucket = crush_map.get_next_exclusive_bucket(osd_bucket, rule.type)

    return selected_osds # Returns e.g., [12, 45, 89]
```

#### 📢 섹션 요약 비유
여행자(Client)가 관광정보센터(MON)에서 "가까운 맛집 좀 찾아주세요"라고 묻는 것이 아니라, 관광객 스스로 스마트폰(CRUSH) 앱으로 지도를 검색하여 주소를 찾아내고, 직접 렌터카를 몰고 식당(OSD)으로 찾아가는 **자율 주행 내비게이션 시스템**과 같습니다. 정보센터가 고장 나도 스마트폰이 있으면 맛집을 찾을 수 있는 것처럼, Ceph는 MON 고장에도 데이터 읽기/쓰기가 가능합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

Ceph는 다양한 스토리지 인터페이스를 제공하며, 이를 통해 계층별로 다른 기술 스택과 시너지를 냅니다.

#### 1. 주요 인터페이스 비교 분석

| 비교 항목 | RBD (RADOS Block Device) | CephFS (Ceph File System) | RGW (RADOS Gateway) |
|:---|:---|:---|:---|
| **인터페이스 타입** | 블록 (Block) | 파일 (File, POSIX) | 객체 (Object, S3/Swift) |
| **데이터 단위** | Image (Fixed size 4MB objects) | File & Directory hierarchy | Object (Key/Value) |
| **사용 사례** | **Cloud Volumes**<br>(OpenStack Cinder, K8s CSI) | **Home directories**<br>(HPC, Legacy NAS migration) | **Archival & Backup**<br>(AWS S3 Compatible) |
| **메타데이터 처리** | In-image inode (OSD 내부) | **MDS Cluster** (별도 서버 필요) | RGW Daemon (Buckets index) |
| **성능 특징** | 가장 빠름 (Low Latency) | 중간 (Metadata Overhead 존재) | 높은 Throughput (쓰기 최적화) |

#### 2. 기술적 심층 비교: Filestore vs BlueStore
Ceph의 OSD는 데이터를 디스크에 기록하는 방식으로 두 가지 엔진을 지원합니다.

```ascii
+--------------------------+    +--------------------------+
|      Legacy FileStore    |    |      Modern BlueStore    |
+--------------------------+    +--------------------------+
|   Application (Ceph)     |    |   Application (Ceph)     |
+------------+-------------+    +------------+-------------+
| Filesystem (XFS/EXT4)    |    |   BlueStore User-space    |
+------------+-------------+    +------------+-------------+
| Journal (WAL)            |    | RocksDB (DB)   | WAL (DB) |
| (Separate Disk/SSD)      |    | (Metadata)     +----------+
+------------+-------------+    +------------+-------------+
| Block Device (HDD/SSD)   |    | Block Device (NVMe/HDD)   |
+--------------------------+    +--------------------------+
```

*(해설: FileStore는 Linux 파일시스템(XFS)을 그대로 사용하여 이중 기록(Double Write) 오버헤드가 있었습니다. 반면 BlueStore는 사용자 공간(User-space)에서 블록 디바이스를 직접 관리하여 파일시스템 오버헤드를 제거하고, 메타데이터는 RocksDB에 저장하여 **NVMe SSD** 환경에서 극도의 성능을 냅니다.)*

#### 3. 타 영역(네트워크, 컴퓨팅)과의 시너지 및 관계
- **네트워크 (Public Network vs Cluster Network)**: Ceph는 복제본을 전송하는 트래픽(Cluster Network)과 클라이언트 트래픽(Public Network)을 분리하는 **Dual Network Architecture**를 권장합니다. 10Gbps 이하의 네트워크에서는 Rebalancing 시 대역폭 병목이 발생할 수 있습니다.
- **운영체제 (OS)**: Linux Kernel(KVM)과의 결합도가 매우 높습니다. `rbd` 커널 모듈을 통해 로컬 디스크처럼 마운트하거나 `