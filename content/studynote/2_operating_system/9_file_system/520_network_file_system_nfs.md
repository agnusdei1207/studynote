+++
title = "520. NFS (Network File System)"
date = "2026-03-14"
weight = 520
+++

# # [NFS (Network File System)]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: NFS (Network File System)는 **RPC (Remote Procedure Call)**와 **XDR (External Data Representation)**을 기반으로, 네트워크상의 원격 스토리지를 로컬 파일 시스템처럼 투명하게 마운트하여 사용하는 표준 분산 파일 시스템 프로토콜이다.
> 2. **가치**: 서버의 **Stateless (상태 비저장)** 설계를 통해 수평 확장성과 장애 복구력을 극대화하며, 이기종 간 데이터 공유를 통해 스토리지 관리 비용(CapEx/OpEx)을 획기적으로 절감한다.
> 3. **융합**: OS의 **VFS (Virtual File System)** 계층과 추상화되어 애플리케이션에 코드 변경 없이 분산 스토리지를 제공하며, 최신 버전인 v4에서는 **ACL (Access Control List)** 및 보안 강화를 통해 클라우드 및 엔터프라이즈 환경으로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
NFS (Network File System)는 썬 마이크로시스템즈(Sun Microsystems)가 1984년에 개발하여, 현재 업계 표준(ANSI/IEEE)으로 자리 잡은 분산 파일 시스템(Distributed File System)이다. 이 기술의 핵심 철학은 "네트워크 투명성(Network Transparency)"으로, 사용자가 네트워크상의 원격 파일에 접근할 때 로컬 디스크에 접근하는 것과 동일한 시스템 콜(System Call) 인터페이스를 제공한다는 점이다.

**2. 등장 배경 및 기술적 패러다임**
- **기존 한계**: 초기 컴퓨팅 환경에서는 각 워크스테이션이 독립적인 디스크를 사용하여 데이터 공유가 불가능했고, 이로 인해 중복된 데이터 저장 및 관리 비용 증가 문제가 발생했다.
- **혁신적 패러다임**: 중앙 집중식 서버에 고성능 스토리지를 두고, 네트워크로 연결된 클라이언트들이 이를 공유함으로써 "컴퓨팅 파워와 스토리지의 분리"라는 새로운 패러다임을 도입했다.
- **현재 비즈니스 요구**: 클라우드 네이티브 환경과 컨테이너 기반 아키텍처에서 PVC (Persistent Volume Claim) 등을 통해 여러 파드(Pod)가 동일한 데이터에 동시 접근해야 하는 요구사항을 NFS가 해결하고 있다.

**3. 작동 기반 기술**
NFS는 OSI 7계층 중 응용 계층(Application Layer)에 속하며, 전송 계층으로 초기에는 UDP를 주로 사용하였으나, 안정성을 위해 현재는 TCP를 기본으로 사용한다. 특히, 이기종 간 통신을 위해 **XDR (External Data Representation)**을 사용하여 데이터 표현을 표준화하고, 통신 메커니즘으로 **RPC (Remote Procedure Call)**를 사용한다.

> **📢 섹션 요약 비유**: NFS는 "공용 사물함"과 같습니다. 개인의 책상(로컬 디스크)에는 파일이 없지만, 복도에 위치한 커다란 공용 사물함(서버)을 내 서랍처럼 열어보고 꺼내 쓸 수 있는 것과 같습니다. 사용하는 입장에서는 사물함이 어디에 있는지 전혀 신경 쓰지 않아도 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 상세 분석**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 주요 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **NFS Server** | 파일 저장 및 관리 주체 | Export된 디렉토리를 관리하며, 클라이언트의 요청을 처리하고 디스크 I/O를 수행함. | nfsd (NFS Daemon) | 대형 창고 관리자 |
| **NFS Client** | 사용자 인터페이스 제공 | 애플리케이션의 시스템 콜을 가로채어 RPC 요청으로 변환하여 서버로 전송함. | VFS, rpc.lockd | 창고 이용 고객 |
| **VFS (Virtual File System)** | 추상화 계층 | 로컬 파일 시스템(ext4, xfs)과 NFS를 구분 없이 동일한 API로 처리하도록 중계함. | POSIX Interface | 통합 번역기 |
| **RPC (Remote Procedure Call)** | 통신 매커니즘 | 네트워크를 통해 원격 서버의 함수를 로컬 함수처럼 호출할 수 있게 함. | TCP/IP (Port 2049) | 전화 주문 시스템 |
| **XDR (External Data Representation)** | 데이터 표준화 | 서로 다른 하드웨어 아키텍처(Big Endian vs Little Endian) 간의 데이터 호환성 보장. | Encoding/Decoding | 통화 환전 |

**2. NFS 아키텍처 데이터 흐름 (ASCII Diagram)**

```text
      [ Client Side ]                                      [ Server Side ]
                       ┌─────────────────────────────────────────────────┐
                       │            Network (TCP/IP, Port 2049)         │
                       └─────────────────────────────────────────────────┘
       ┌──────────────┐                                 ┌──────────────┐
       │ Application  │                                 │ File System  │
       │ (e.g., vi)   │                                 │ (ext4/xfs)   │
       └───────┬──────┘                                 └───────▲──────┘
               │                                                │
       ┌───────▼──────┐                                 ┌───────┴──────┐
       │  VFS Layer   │                                 │  VFS Layer   │
       │ (Path Lookup)│                                 │ (Permission  │
       └───────┬──────┘                                 │  Check)      │
               │                                        └───────▲──────┘
       ┌───────▼──────┐                                         │
       │ NFS Client   │    ① RPC CALL (READ, FH, Offset)        │
       │   Stub       │◄─────────────────────────────────────────┤
       │ (Generates   │    ③ RPC REPLY (Data, Attributes)       │
       │   Request)   │─────────────────────────────────────────►│
       └───────▲──────┘                                         │
               │                                        ┌───────┴──────┐
               │  ② Client Cache Check                   │ NFS Server   │
               └────────────────────────────────────────┤   Daemon     │
                                                         │ (nfsd)       │
                                                         └──────────────┘
```

**[다이어그램 해설]**
위 다이어그램은 사용자 프로세스가 원격 파일을 요청할 때의 계층별 데이터 흐름을 도식화한 것이다.
① **애플리케이션 계층**: 사용자가 `vi` 등의 프로그램으로 파일 열기를 시도하면, 커널의 **VFS (Virtual File System)**가 해당 경로가 NFS 마운트 포인트임을 식별한다.
② **클라이언트 스텁(Stub)**: VFS는 요청을 NFS 클라이언트 모듈로 전달하고, 이는 **RPC (Remote Procedure Call)** 런타임을 통해 파일 핸들(File Handle)과 오프셋 정보를 캡슐화한다.
③ **서버 처리**: 네트워크를 통해 도착한 패킷은 NFS 서버 데몬(`nfsd`)에 의해 수신되며, 로컬 VFS 계층을 거쳐 실제 디스크(File System)로부터 데이터를 읽는다.
④ **응답 반환**: 읽힌 데이터는 다시 RPC 패킷에 담겨 클라이언트로 전송되며, 클라이언트의 캐시를 거쳐 최종적으로 사용자 프로세스에게 전달된다. 이 과정에서 애플리케이션은 네트워크 존재를 인지하지 못한다(투명성).

**3. 핵심 동작 원리 및 메커니즘**
① **마운트(Mount) 및 파일 핸들 획득**: 클라이언트는 `mount` 시스템 콜을 통해 서버에 접속하고, 서버는 해당 파일 시스템의 루트 정보를 포함한 고유 식별자인 **File Handle**을 부여한다. 이 File Handle은 파일의 메타데이터(Inode 번호 등)를 암호화하거나 인코딩한 것으로, 이후 모든 요청은 파일명이 아닌 이 File Handle을 사용한다.
② **VFS 추상화**: 사용자 프로그램이 `open()`, `read()` 시스템 콜을 호출하면 커널의 VFS 계층은 이 파일이 로컬 디스크에 있는지 NFS 마운트 포인트에 있는지 확인한다. NFS인 경우, 요청을 NFS 클라이언트 모듈로 넘긴다.
③ **RPC (Remote Procedure Call) 실행**: NFS 클라이언트는 XDR을 통해 데이터를 직렬화(Serialization)하고, RPC를 통해 네트워크로 요청을 전송한다. 요청은 Idempotent(멱등성)을 보장하여 재시도가 가능하도록 설계된다.
④ **Stateless 서버 처리**: NFS 서버는 클라이언트의 연결 상태를 저장하지 않는다. 단지 File Handle과 오프셋(Offset)을 받아 디스크를 읽고 결과를 반환한다.
⑤ **클라이언트 캐싱**: 네트워크 대역폭 절약을 위해 클라이언트는 읽은 데이터를 메모리에 캐싱한다. 이로 인해 발생하는 데이터 일관성 문제는 속성 캐시(Attribute Caching) 타임아웃(acregmin, acregmax) 조정으로 해결한다.

**4. 핵심 알고리즘: 파일 핸들 생성 (Pseudo-code)**

```python
# NFS File Handle Generation Concept (Pseudo-code)
# File Handle은 보안과 효율성을 위해 보통 인코딩되어 전달됨.

def generate_file_handle(inode_number, generation_number, fs_id):
    """
    inode_number : 파일 시스템 내 고유 번호
    generation_number : 파일이 재사용되더라도 구분하기 위한 버전 번호
    fs_id       : 파일 시스템 식별자 (Export된 볼륨 구분)
    """
    
    # XDR (External Data Representation) 인코딩 규칙에 따라 패킹
    handle_payload = {
        "fileid": inode_number,
        "generation": generation_number,
        "fsid": fs_id
    }
    
    # 네트워크 전송을 위해 바이너리 포맷으로 변환
    encoded_handle = xdr_encode(handle_payload)
    
    return encoded_handle

# 실제 통신에서는 이 바이너리 핸들이 주고받아짐
# Client: read(fh=encoded_handle, offset=0, count=4096)
```

> **📢 섹션 요약 비유**: NFS의 동작은 "배달 앱 서비스"와 유사합니다. 고객(클라이언트)은 앱을 통해 메뉴(VFS)를 선택하고 주문(RPC)합니다. 주방(서버)은 고객이 누구인지 매번 기억할 필요 없이, 단지 주문서(File Handle)에 적힌 대로 요리해서 배달원(RPC)에게 맡깁니다. 고객은 음식이 어디서 만들어졌는지 몰라도 집에서 바로 먹을 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Stateless vs Stateful**

| 비교 항목 | NFS (Stateless Design) | SMB/CIFS (Stateful Design) | FTP (File Transfer Protocol) |
|:---|:---|:---|:---|
| **서버 부하 관리** | 서버가 클라이언트 상태를 저장하지 않아 메모리 사용량이 일정하며 장애 복구가 용이함. | 세션별 상태를 유지해야 하므로 메모리 사용량이 클라이언트 수에 비례하여 증가함. | 제어 연결(Control Connection)과 데이터 연결이 분리되어 있음. |
| **네트워크 장애 복구** | 요청이 실패해도 재시도만 하면 됨(Idempotent). 네트워크가 불안정한 환경에서 강함. | 연결이 끊기면 세션이 종료될 수 있으며, 파일 잠금 등의 복구 절차가 복잡함. | 전송이 중단되면 재개(Resume)가 가능하나 연결을 다시 맺어야 함. |
| **데이터 일관성 모델** | Close-to-Open 일관성 (쓰기 후 닫을 때 서버 동기화). | Op-lock (Opportunistic Locking)을 통해 강력한 캐싱 및 일관성 제공. | 전체 파일 전송 후 업데이트되므로 실시간 공유가 불가능함. |
| **주요 사용 환경** | 리눅스/유닉스 환경, 웹 서버의 정적 컨텐츠 공유. | 윈도우 환경, 폴더 공유, AD(Active Directory) 연계. | 대용량 일회성 파일 전송, 백업 서버. |

**2. OS 및 네트워크 융합 분석**
- **운영체제 커널 융합 (VFS Integration)**: NFS는 단순한 애플리케이션이 아니라 OS 커널 레벨에서 동작한다. 리눅스 커널의 `fs/nfs/` 모듈은 로컬 파일 시스템 드라이버(Ext4 등)와 동등한 권한으로 VFS에 등록된다. 이로 인해 `read()`, `write()` 같은 표준 시스템 콜을 사용하여 데이터 입출력이 가능하며, 이는 애플리케이션에게 네트워크 존재를 완전히 은폐(Transparent)한다.
- **네트워크 성능과의 상관관계**: NFS는 전통적으로 LAN(Local Area Network) 환경을 가정한다. RTT(Round Trip Time)가 짧은 환경에서는 **Caching** 덕분에 로컬 디스크에 근접한 성능을 내지만, WAN(Wide Area Network)이나 높은 지연(Latency)이 있는 환경에서는 마운트 옵션(`sync` vs `async`, `rsize`/`wsize`)에 따라 성능 편차가 크다. 최신 버전인 NFS v4.1부터는 **pNFS (Parallel NFS)**를 도입하여 메타데이터 서버와 데이터 서버를 분리, 병렬 I/O를 통해 단일 마운트 포인트의 대역폭 병목을 해결했다.

> **📢 섹션 요약 비유**: 로컬 파일 시스템은 "내 집 냉장고"이고, SMB는 "식당 좌석 예약(상태 유지)"이라서 자리를 비우면 정리되지만, NFS는 "편의점(상태 비저장)"입니다. 편의점은 내가 가서 물건을 사고 나가더라도 점원이 내 기록을 계속 기억할 필요가