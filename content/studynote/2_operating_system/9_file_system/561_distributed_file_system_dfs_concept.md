+++
title = "561. 분산 파일 시스템 (DFS, Distributed File System) 개념"
date = "2026-03-14"
weight = 561
+++

# # 561. 분산 파일 시스템 (DFS, Distributed File System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 파일 시스템(DFS, Distributed File System)은 물리적으로 분산된 저장소 리소스를 논리적 단일 네임스페이스(Namespace)로 통합하여, 네트워크를 통해 로컬 파일과 유사한 투명한 접근 계층을 제공하는 가상화 파일 시스템이다.
> 2. **가치**: Scale-out(수평 확장)을 통해 단일 서버의 용량/성능 한계를 극복하며, 데이터 복제(Replication)를 통해 고가용성(HA, High Availability)과 재해 복구(DR, Disaster Recovery) 능력을 확보한다. 이 과정에서 CAP 정리(Consistency, Availability, Partition Tolerance)에 따른 일관성과 지연 시간(Latency)의 트레이드오프 관리가 핵심 설계 변수가 된다.
> 3. **융합**: OS(운영체제)의 VFS(Virtual File System) 계층과 네트워크 프로토콜(TCP/IP, RDMA)을 결합하며, 빅데이터 처리(HDFS), 클라우드 스토리지(S3), 분산 DB의 기반 인프라로서 데이터 센터의 핵심 자산이다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 정의 및 철학**
분산 파일 시스템(DFS, Distributed File System)은 네트워크로 연결된 여러 노드의 저장 장치를 사용자에게 하나의 통합된 파일 계층 구조로 제공하는 소프트웨어 추상화 계층입니다. 사용자는 파일이 물리적으로 어디에 있는지(위치 투명성), 어떤 파일 시스템으로 포맷되었는지(이식성 투명성)를 알 필요 없이, 표준 시스템 콜(System Call)을 통해 데이터에 접근할 수 있습니다. 이는 단순한 파일 공유를 넘어, 대용량 데이터 처리와 중단 없는 서비스 제공을 목적으로 하는 고도화된 아키텍처입니다.

**등장 배경 및 기술적 패러다임 이동**
1.  **데이터 폭증과 Scale-up의 한계**: 기존 단일 서버(Scale-up) 방식은 저장 용량 확장 시 비용이 기하급수적으로 증가하고 하드웨어 교체 시 가동 중단(Downtime)이 불가피했습니다. 이를 해결하기 위해 저렴한 상용 하드웨어(Commodity Hardware)를 병렬로 연결하여 용량과 성능을 동시에 확보하는 **Scale-out** 패러다임이 등장했습니다.
2.  **네트워크 기술의 진보**: 기가비트 이더넷(10Gbps/100Gbps)과 **RDMA(Remote Direct Memory Access)** 기술의 발전으로, 네트워크를 통한 원격 디스크 접근의 지연 시간(Latency)이 크게 단축되어 로컬 스토리지에 근접한 성능을 낼 수 있는 환경이 조성되었습니다.
3.  **데이터 무결성 및 동시성 제어의 필요성**: 분산 환경에서 다수의 사용자가 동일한 파일을 수정할 때 발생할 수 있는 데이터 충돌을 방지하고, ACID(Atomicity, Consistency, Isolation, Durability) 트랜잭션 성질을 보장하기 위한 복잡한 동기화 메커니즘(Semaphore, Distributed Lock)의 필요성이 대두되었습니다.

> **💡 개념 비유**
> DFS는 **"프랜차이즈 통합 배달 시스템"**과 같습니다. 고객(사용자)은 어느 지점에 있든 동일한 메뉴(파일 시스템)를 주문할 수 있으며, 주문이 접수되면 본사 시스템(메타데이터 서버)이 가장 가까운 매장이나 창고(스토리지 노드)에서 즉시 배달을 지시합니다. 고객은 음식이 어느 창고에서 왔는지 모르며, 단지 빠르고 따뜻하게 배달되는 경험(투명성)만을 누리게 됩니다.

**로컬 파일 시스템(LFS, Local File System)과의 비교**

| 비교 항목 | 로컬 파일 시스템 (LFS) | 분산 파일 시스템 (DFS) |
|:---|:---|:---|
| **관리 대상** | 단일 컴퓨터 내의 부착된 디스크 | 네트워크상의 다수 원격 서버 |
| **네트워크 의존성** | 없음 (내부 버스) | 필수적 (TCP/IP, Infiniband 등) |
| **주요 장애 유형** | 디스크 섹터 오류, 포트 고장 | 네트워크 분할(Partition), 서버 다운 |
| **일관성 모델** | 강한 일관성 (Strong Consistency) | 상황에 따른 유연한 모델 (Eventual/Causal) |
| **확장성** | 제한적 (버스 슬롯, 케이블) | 무한 확장 가능 (노드 추가) |

📢 **섹션 요약 비유**: 마치 **"거대한 연합 도서관 시스템"**과 같습니다. 이용자는 자신이 방문한 도서관(클라이언트)에서 통합 검색 시스템(DFS 네임스페이스)을 통해 책을 요청하면, 해당 책이 현재 도서관에 없더라도 다른 지역의 창고(원격 스토리지)에서 자동으로 대출(마운트) 처리해 줍니다. 이용자는 책의 물리적 위치에 상관없이 단일 회원증으로 모든 자원에 접근할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

DFS는 **C/S (Client/Server)** 구조를 기반으로 하며, 관리(Metadata)와 데이터(Data)를 분리하여 성능을 극대화하는 것이 일반적인 설계 패턴입니다. 이를 통해 단일 서버의 병목 현상을 해소하고 데이터 경로(Data Plane)와 제어 경로(Control Plane)를 독립적으로 확장할 수 있습니다.

#### 1. 구성 요소 상세 분석 (Depth)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **클라이언트 스텁 (Client Stub)** | 사용자 요청을 네트워크 RPC로 변환 | Application의 `open()`/`read()` 시스템 콜 인터셉트 → VFS 계층을 거쳐 원격 프로시저 호출로 패킹(Marshalling) | NFS, SMB/CIFS, gRPC | 배달 주문을 받는 직원 (고객 요구 번역) |
| **메타데이터 서버 (MDS)** | 파일 시스템 구조(INODE) 관리 및 권한 제어 | 파일명 ↔ 블록 주소 매핑 테이블 유지, Access Control List(ACL) 검증, Distributed Lock Management | LDAP, Kerberos, Paxos/Raft | 물류 센터의 통제 타워 (재고 및 배차 관리) |
| **데이터 스토리지 (DS)** | 실제 데이터 블록 저장 및 I/O 처리 | Striping(분할), Mirroring(복제) 된 raw 데이터에 대한 Block I/O 처리, Checksum을 통한 무결성 검증 | iSCSI, FCoE, Fiber Channel | 실제 화물이 적재된 트럭/창고 |
| **분산 잠금 관리자 (DLM)** | 동시성 제어 및 데이터 일관성 보장 | 파일/레코드 단위 잠금 토큰 발급, Lease 기반 타임아웃 관리 | Global Lock Manager | 독서실 좌석 배치 시스템 (중복 예약 방지) |
| **캐싱 매니저 (Cache Manager)** | 네트워크 왕복(RTT) 최소화 | LRU(Least Recently Used) 기반 데이터 프리패칭, Callback 기반 캐시 무효화(Invalidation) | io_uring, O_DIRECT | 자주 찾는 책을 테이블 위에 올려둠 |

#### 2. 아키텍처 데이터 흐름 (ASCII)

```text
    [ CLIENT NODE ]                [ CONTROL LAYER ]             [ DATA LAYER ]
┌─────────────────────┐      ┌──────────────────────────┐      ┌───────────────────────┐
│ Application         │      │  Metadata Server (MDS)   │      │  Data Server #1        │
│ (User Process)      │      │  ├─ Namespace (Dir Tree) │      │  ├─ Block Device: /sdb │
│                     │      │  ├─ Inode Map (Lookup)   │      │  └─ Chunk: [A][B][C]  │
│  fd = open("/A/B")  │  ①   │  └─ Lock Manager         │  ③   │                       │
└──────────┬──────────┘      │   (Auth: Valid?)         │      │  (Read I/O)           │
           │                 └───────────┬──────────────┘      └───────────┬───────────┘
           ▼                             │                              ▲
┌─────────────────────┐                 │  ② (Capability Token)         │
│  VFS (Virtual FS)   │                 │  Loc: /A/B -> DS#1            │
│  ├─ Mount Lookup    │◀────────────────┘                              │
│  └─ DFS Client Stub │                  │                              │
└──────────┬──────────┘                  ▼                              │
           │                 ┌──────────────────────────┐              │
           │                 │  Client Side Cache       │              │
           │                 │  (Buffer Cache)          │--------------│
           │                 │  └─ Validates Token      │ (Read Data)  │
           ▼                 └──────────────────────────┘              │
┌─────────────────────┐                                             │
│  Network Stack      │─────────────────────────────────────────────┘
│  [ TCP / IP ]       │    (RPC: READ req for Block 12345)
└─────────────────────┘
```

**[데이터 흐름 해설]**
1.  **Metadata Lookup**: 클라이언트가 파일 `/A/B`를 열면, VFS는 이를 DFS 클라이언트 스텁으로 넘깁니다. 스텁은 메타데이터 서버(MDS)에 RPC 요청을 보내 파일의 위치(블록 번호)를 질의합니다.
2.  **Capability issuance**: MDS는 사용자의 권한을 확인한 후, 해당 파일이 위치한 데이터 서버(DS #1)의 주소와 접근을 위한 **Capability(토큰)**를 클라이언트에 발급합니다. 이데이터 경로는 클라이언트와 데이터 서버 간에 직접 형성됩니다.
3.  **Data Transfer**: 클라이언트는 발급받은 토큰을 사용하여 데이터 서버에 직접 접속하여 대용량 데이터를 주고받습니다(Cut-through Routing). MDS는 이 데이터 전송 과정에 관여하지 않아 병목을 피할 수 있습니다.

#### 3. 핵심 설계 철학: 투명성 (Transparency)의 4가지 차원

1.  **접근 투명성 (Access Transparency)**: 로컬 파일(`/etc/hosts`)과 원격 파일(`/dfs/project/data.txt`)을 여는 코드가 동일해야 합니다.
2.  **위치 투명성 (Location Transparency)**: 파일 이름에 서버의 IP나 물리적 경로가 노출되어서는 안 됩니다.
3.  **복제 투명성 (Replication Transparency)**: 시스템이 성능을 위해 파일을 여러 곳에 복제해 두었더라도, 사용자는 원본 파일 하나만 접근하는 것처럼 느껴야 합니다.
4.  **동시성 투명성 (Concurrency Transparency)**: 다수의 사용자가 동시에 파일을 수정하더라도, 잠금(Lock) 메커니즘을 통해 결과적 일관성을 보장해야 합니다.

#### 4. 성능 최적화 핵심 알고리즘 & 코드

DFS의 성능은 캐싱 전략에 달려 있으며, 특히 **콜백(Callback) 기반 무효화**는 네트워크 트래픽을 획기적으로 줄이는 방법입니다.

```python
# Pseudo-code for Client-Side Caching with Callback Promise
# Class: DFSClientCache

class DFSClientCache:
    def __init__(self):
        self.cache_store = {}  # {filename: (data, callback_token)}
        self.server_stub = ServerStub()

    def read_file(self, filename):
        # 1. Check Cache
        if filename in self.cache_store and self.cache_store[filename].is_valid():
            print(f"[Cache Hit] Returning local data for {filename}")
            return self.cache_store[filename].data
        
        # 2. Cache Miss or Invalidated
        print(f"[Cache Miss] Fetching {filename} from Metadata Server...")
        
        # 3. Request Metadata (Location + Token)
        # MDS returns: Data Server IP + Capability Token + Callback Promise
        location, token, callback_promise = self.server_stub.lookup(filename)
        
        # 4. Fetch Data directly from Data Server using Token
        data = self.server_stub.read_data(location, token)
        
        # 5. Update Local Cache with Callback Promise
        # 'callback_promise' allows server to revoke this cache later
        self.cache_store[filename] = CacheEntry(data, callback_promise)
        return data

    def handle_server_callback(self, filename):
        # Server revokes the promise because another client modified the file
        if filename in self.cache_store:
            print(f"[Callback] Server invalidated cache for {filename}")
            self.cache_store[filename].invalidate()
```

📢 **섹션 요약 비유**: 이는 **"고속도로 통행료 징수 시스템(Hi-Pass)"**과 유사합니다. 메타데이터 서버는 영업소(진입로)에서 차량이 어디로 가야 할지 알려주고 통행권(Token)을 발급합니다. 이후 차량(데이터 패킷)은 영업소에 매번 멈추지 않고, 발급받은 통행권을 통해 하이패스 차선(데이터 경로)을 이용해 목적지로 무중단 전송됩니다. 영업소는 진입/진출 흐름만 제어할 뿐, 고속도로 위의 주행 속도에는 관여하지 않습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

DFS는 OS, 네트워크, 데이터베이스 기술이 집약된 결정체입니다. 특히 **POSIX(Portable Operating System Interface)** 호환성을 준수하는 전통적인 DFS(NFS)와 빅데이터 처리를 위해 **일관성을 포기한 DFS(HDFS)** 간의 기술적 트레이드오프를 이해하는 것이 중요합니다.

#### 1. 접근 방식 비교: Stateful vs Stateless

| 비교 항목 | Stateful (상태 유지형) | Stateless (무상태형) |
|:---|:---|:---|
| **대표 시스템** | **AFS** (Andrew File System), CIFS/SMB | **NFS** (Version 3/4) |
| **서버 부하** | 높음 (클라이언트의 열린 파일 정보를 메모리로 유지 관리) | 낮음 (모든 요청을 독립적으로 처리, Crash Recovery 용이) |
| **복구