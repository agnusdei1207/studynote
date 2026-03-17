+++
title = "565. 파일 캐싱 및 일관성 문제 - Write-through vs Write-back"
date = "2026-03-14"
weight = 565
+++

# 565. 파일 캐싱 및 일관성 문제 - Write-through vs Write-back

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일 캐싱(File Caching)은 분산 시스템에서 네트워크 지연(Latency)을 숨김(Covering Latency)하기 위해 클라이언트의 로컬 저장소(Local Storage)에 데이터 복제본을 두는 핵심적인 성능 최적화 기법이다.
> 2. **가치**: 'Write-through'는 데이터 안전성(Data Integrity)과 일관성(Consistency)을 보장하여 RTO(복구 시간 목표)를 줄이는 데 유리하며, 반면 'Write-back'는 네트워크 패킷(Packet)을 대형화(Batching)하여 쓰기 성능(Throughput)을 비약적으로 향상시킨다.
> 3. **융합**: OS의 페이지 캐시(Page Cache), 데이터베이스의 WAL(Write-Ahead Logging), 분산 파일 시스템(NFS/AFS)의 기반이 되며, CAP 이론에서 Consistency(일관성)와 Availability(가용성)의 트레이드오프를 결정짓는 핵심 메커니즘이다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
파일 캐싱(File Caching)은 네트워크를 통해 접근하는 원격 서버(Remote Server)의 데이터를 클라이언트(Client)의 주기억장치(Main Memory)나 로컬 디스크(Local Disk)에 일시적으로 저장(Temporary Storage)해 두는 기술이다. 이를 통해 디스크 입출력(IO)이 발생할 때마다 네트워크 왕복(Round Trip)을 수행해야 하는 비용을 제거한다. 단순히 읽기(Read) 속도를 높이는 것을 넘어, 쓰기(Write) 작업의 시점을 조절하여 시스템 전체의 부하를 분산시키는 버퍼(Buffer)의 역할을 수행한다.

**💡 비유**
파일 캐싱은 마치 "책상 위의 참고서"와 같다. 도서관(서버)에 가서 책을 빌리려면 왕복 시간이 걸리지만, 필요한 페이지를 복사해 책상(캐시)에 두면 즉시 볼 수 있다. 하지만 책장을 필기할 때 도서관의 원본에 바로 반영할지, 아니면 내 책상에만 적어두었다가 나중에 반영할지에 대한 고민이 필요하다.

**등장 배경**
1.  **기존 한계**: 초기 분산 파일 시스템(DFS)은 모든 파일 접근에 서버 승인이 필요하여 네트워크 병목(Bottleneck)이 심각하고 클라이언트 응답성이 낮았다.
2.  **혁신적 패러다임**: 클라이언트 측에 독립적인 캐시 공간을 할당하고, OS 커널(Kernel) 차원에서 이를 관리하는 'Lazy Evaluation' 기법이 도입되었다. 이는 로컬 디스크의 빠른 접근 속도를 네트워크 파일 시스템에 투명하게(Transparently) 녹여내는 설계다.
3.  **현재의 비즈니스 요구**: 클라우드(Cloud) 환경과 SSD의 보급으로 대용량 처리가 요구됨에 따라, 단순 캐싱을 넘어 쓰기 일관성 모델(Strong vs Eventual Consistency)을 선택할 수 있는 정교한 아키텍처가 요구되었다.

**문제 해결 맥락**
파일 시스템의 성능은 디스크 접근 속도가 아닌 네트워크 지연 시간에 의해 좌우된다. 특히 쓰기 연산은 데이터 무결성을 확인해야 하므로 소요 시간이 길다. 따라서 캐싱 전략은 "언제 서버와 동기화할 것인가(Timing)"에 따라 시스템의 성능과 신뢰성이 갈리는 결정적인 분기점이 된다.

📢 **섹션 요약 비유**: 파일 캐싱 도입은 "회사 사무실과 본사"의 관계와 같습니다. 직원(클라이언트)이 본사(서버)에 있는 문서를 확인할 때마다 비행기를 타고 가는 대신, 자기 책상에 복사본을 두고 업무를 보는 것과 같아 업무 효율이 비약적으로 상승합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

파일 캐싱 시스템은 크게 클라이언트 캐시 매니저, 네트워크 계층, 그리고 서버 저장소 계층으로 구성된다. 쓰기 정책에 따라 데이터 흐름과 제어 로직이 결정적으로 달라진다.

**구성 요소 (Component Table)**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Client Cache Manager** | 캐시 히트/미스 판단 및 I/O 인터셉트 | VFS(Virtual File System) 레이어에서 시스템 콜(System Call)을 후킹(Hooking)하여 로컬 데이터 존재 여부 확인 | mmap, ioctl | 사무실의 서류 정리 담당자 |
| **Block Cache (Data)** | 실제 데이터 저장 공간 | Page 단위(4KB)로 메모리에 매핑하며 Dirty 비트 플래그를 통해 수정 여부 관리 | LRU, Clock Algorithm | 실제 서류가 들어있는 바인더 |
| **Network Transport** | 데이터 송수신 채널 | RPC(Remote Procedure Call) 또는 NFS 프로토콜을 통해 패킷 전송 | TCP/IP, NFSv4 | 인터넷 또는 본사로 가는 택배 |
| **Server Storage** | 데이터 원본 저장소 | ACID 속성을 보장하며 동시성 제어(Concurrency Control) 수행 | ZFS, EXT4 | 본사의 금고 |
| **Consistency Protocol** | 동기화 및 무효화 관리 | 잠금(Lease/Lock) 발급 및 변경 통신(Invalidation Message) 브로드캐스팅 | Callback Promise | 서류 변경 알림 뉴스레터 |

**ASCII 구조 다이어그램: 캐싱 아키텍처**
아래 다이어그램은 클라이언트의 쓰기 요청이 캐시 계층을 거쳐 서버로 전달되는 데이터 흐름과 제어 흐름(Control Flow)을 시각화한 것이다.

```text
   [User Space Application]
          │
          ▼ (write syscall)
   ┌─────────────────────────────────────────────────┐
   │  [Client Side]                                  │
   │  ┌───────────────────────────────────────────┐  │
   │  │  Cache Manager (VFS Layer)                │  │
   │  │  - Address Translation (Logical -> Phy)   │  │
   │  │  - Policy Checker (Write-through/Back)    │  │
   │  └───────────┬───────────────────────┬───────┘  │
   │              ▼ (Data Store)          ▼ (Signal) │
   │      ┌───────────────┐        ┌─────────────┐   │
   │      │ Local Cache   │        │   Control   │   │
   │      │ (Dirty Bit)   │        │   Module    │   │
   │      └───────┬───────┘        └──────┬──────┘   │
   └──────────────┼───────────────────────┼──────────┘
                  │ (Async / Sync)        │
                  ▼                       │
   ┌─────────────────────────────────────────────────┐
   │  [Network Layer] (Latency & Bandwidth)          │
   │  ───────────────────────────────────────────    │
   └─────────────────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────────────────┐
   │  [Server Side]                                  │
   │  ┌───────────────┐      ┌───────────────────┐   │
   │  │ File System   │◀─────│  Lock Manager     │   │
   │  │ (ZFS/EXT4)    │      │  (Metadata DB)    │   │
   │  └───────┬───────┘      └───────────────────┘   │
   │          ▼                                      │
   │  [Physical Disk Array]                          │
   └─────────────────────────────────────────────────┘
```

**다이어그램 해설**
1.  **요청 인터셉트**: 사용자 애플리케이션의 `write()` 시스템 콜은 커널의 VFS(Virtual File System) 계층에 도달한다. 여기서 파일이 로컬 캐시에 있는지 확인한다.
2.  **정책 분기점**: Cache Manager는 설정된 정책(Write-through vs Write-back)에 따라 동작을 결정한다. Write-through는 즉시 Control Module을 트리거하여 네트워크 전송을 시작한다. Write-back은 데이터만 Local Cache에 기록(Dirty Bit=1)하고 즉시 성공(Success)을 리턴한다.
3.  **동기화 충돌 관리**: 서버의 Lock Manager는 여러 클라이언트가 동시에 쓰기를 시도할 때 데이터 충돌을 방지하기 위해 잠금(Lock)을 관리하며, 캐시 무효화(Invalidation) 신호를 발송하는 권한을 가진다.

**심층 동작 원리 (Dirty Block Management)**
파일 캐싱의 핵심은 'Dirty Block(더티 블록)' 관리다. 클라이언트가 데이터를 수정하면 해당 메모리 블록의 Dirty Bit가 1로 설정된다.
-   **Write-through**: `Data Write` 시점과 `Network Transfer` 시점이 일치한다. `dirty bit`가 1이 되는 순간 서버로 전송이 완료되어야 하므로, 실제로는 캐시가 순간적인 버퍼 역할만 하고 Dirty 상태가 오래 유지되지 않는다.
-   **Write-back**: `Data Write`는 즉시 완료되지만 `Network Transfer`는 지연된다. 시스템은 `Flush` 메커니즘이 호출되거나 메모리 부족(Page Fault)이 발생하기 전까지 Dirty Block을 방치한다. 이때 전원이 나가면 데이터가 유실된다.

**핵심 알고리즘 (Pseudo-code: Write Policy Decision)**

```c
// 가상의 캐시 라이터 로직
void cache_write(File *file, Offset offset, Data *data) {
    // 1. 로컬 캐시에 데이터 기록 (Copy-on-Write 혹은 In-place)
    Block *block = get_local_cache_block(file, offset);
    write_to_memory(block, data);
    block->is_dirty = TRUE; // 상태 변경

    if (policy == WRITE_THROUGH) {
        // 2. 즉시 서버로 전송 (동기식)
        send_network_request(SERVER, WRITE_CMD, block);
        await_ack();        // 네트워크 지연 발생 지점
        block->is_dirty = FALSE; // 동기화 완료
    } else if (policy == WRITE_BACK) {
        // 3. 로컬 작업 완료만 알리고 즉시 반환 (비동기식)
        return SUCCESS;    // 매우 빠른 응답
        // 나중에 flusher_thread()에 의해 비동기적으로 전송됨
    }
}
```

**일관성 유지 메커니즘 (Coherency Protocols)**
분산 환경에서 여러 클라이언트가 캐싱을 사용할 때 데이터의 최신성을 보장하는 것은 매우 복잡하다. 주로 다음 4가지 기법이 사용된다.
1.  **Client-initiated Polling**: 클라이언트가 데이터를 사용하기 전 서버에 "이 데이터가 변경되었습니까?"라고 묻는 방식. (Simple but High Traffic)
2.  **Server-initiated Callback (Lease)**: 서버가 데이터를 변경하려 할 때, 해당 데이터를 캐싱하고 있는 클라이언트에게 "너의 캐시를 무효화(Invalidation)하라"고 명령하는 방식. AFS에서 주로 사용.
3.  **Write-Invalidation vs Write-Update**: 
    -   *Invalidate*: 다른 클라이언트가 쓰면 나의 캐시를 단순 무효화.
    -   *Update*: 다른 클라이언트가 쓰면 변경된 데이터를 나에게도 푸시(Push).

📢 **섹션 요약 비유**: 캐싱 아키텍처는 "복잡한 고속도로 톨게이트 시스템"과 같습니다. 하이패스 차선(캐시 히트)을 별도로 운영하여 병목을 해결하되, 통행료(데이터)를 정산하는 시점을 통행할 때마다(Write-through) 할지, 한 달에 한 번 묶어서(Write-back) 할지를 결정하는 설계 구조입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

쓰기 정책의 선택은 시스템의 전체 성능과 안정성에 지대한 영향을 미친다.

**심층 기술 비교 (Write-through vs Write-back)**

| 비교 항목 | Write-through (통과 쓰기) | Write-back (지연 쓰기 / 회수 쓰기) |
|:---|:---|:---|
| **데이터 무결성** | **높음 (High)**<br>서버와 캐시가 항상 동일 상태 유지. 장애 발생 시 데이터 손실 없음. | **낮음 (Low)**<br>캐시와 서버 간 불일치 발생. 클라이언트 장애 시 최신 변경 내역 소실 위험. |
| **쓰기 성능 (Latency)** | **낮음 (Slow)**<br>매 쓰기마다 네트워크 왕복 지연(RTT)이 발생. | **높음 (Fast)**<br>로컬 메모리 속도로 쓰기 응답. 사용자 경험(UX) 우수. |
| **네트워크 트래픽** | **빈번함**<br>작은 쓰기 요청이 자주 전송되어 효율이 낮을 수 있음. | **최적화됨**<br>여러 변경 사항을 하나의 트랜잭션으로 묶어(Batching) 전송. |
| **구현 복잡도** | **단순함**<br>동기화 로직이 단순하여 디버깅이 쉬움. | **복잡함**<br>Dirty Block 추적, 충돌 해결(Write-Back과 Write-Allocate의 연계), 복구 메커니즘 필요. |
| **주요 용도** | 금융 거래, 데이터베이스 로그(WAL) 등 신뢰성이 중요한 시스템. | 멀티미디어 편집, 로컬 백업, 임시 파일 생성 등 처리량이 중요한 시스템. |

**과목 융합 관점**
1.  **운영체제(OS