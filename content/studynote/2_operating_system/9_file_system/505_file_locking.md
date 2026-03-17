+++
title = "505. 파일 잠금 (File Locking) - 공유 락 vs 배타 락"
date = "2026-03-14"
weight = 505
+++

# # [505. 파일 잠금 (File Locking) - 공유 락 vs 배타 락]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일 잠금(File Locking)은 다중 프로세스(Multi-process) 환경 또는 분산 시스템에서 공유 자원인 파일의 **데이터 무결성(Data Integrity)**과 **일관성(Consistency)**을 보장하기 위해 동시 접근을 제어하는 상호 배제(Mutual Exclusion) 메커니즘이다.
> 2. **가치**: **읽기(Read) 연산의 병렬성을 극대화**하는 공유 락(Shared Lock, S-Lock)과 **쓰기(Write) 연산의 독점성을 보장**하는 배타 락(Exclusive Lock, X-Lock)을 전략적으로 분리하여, **Race Condition(경쟁 조건)**을 방지함과 동시에 시스템의 전체 처리량(Throughput)을 최적화한다.
> 3. **융합**: 운영체제(OS)의 커널 레벨 **시스템 콜(System Call)**(`flock`, `fcntl`)과 데이터베이스(DBMS)의 **트랜잭션 격리 수준(Isolation Level)**, 그리고 분산 환경의 분산 락(Distributed Lock) 등으로 확장되며, 고가용성(HA) 시스템의 핵심 요소로 작용한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**파일 잠금(File Locking)**은 파일 시스템(File System) 상의 특정 파일 또는 레코드에 대해, 특정 프로세스가 접근 권한을 선점(Precise)하거나 공유(Share)할 수 있도록 제어하는 기술이다. 이는 단순히 파일을 "열고 닫는" 것을 넘어, **Critical Section(임계 영역)**에 진입할 수 있는 프로세스의 수를 제어하여 데이터가 훼손되는 것을 방지하는 운영체제의 핵심 기능 중 하나이다.

### 2. 등장 배경: 일관성과 병행성의 딜레마
초기 컴퓨팅 환경에서는 파일을 순차적으로만 처리했으나, 시분할(Time-sharing) 시스템과 다중 사용자 환경이 도입되면서 다음과 같은 문제가 발생했다:
- **💥 Lost Update Problem**: 두 프로세스가 동시에 파일의 값을 읽어 각각 수정한 후 다시 쓸 때, 나중에 쓴 값이 먼저 쓴 값을 덮어써 버리는 현상.
- **💥 Inconsistent Read (Non-repeatable Read)**: 어떤 프로세스가 데이터를 읽는 도중 다른 프로세스가 그 데이터를 수정하여, 읽기 작업이 중반에 잘못되거나 모순된 결과를 도출하는 현상.

이를 해결하기 위해 **"읽기는 함께해도 되지만, 쓰기는 혼자만 해야 한다"**는 패러다임이 등장했고, 이것이 바로 공유 락과 배타 락의 기원이다.

### 3. 경쟁 조건(Race Condition)과 락의 필요성
락 메커니즘이 없는 상황에서의 메모리 또는 파일 접근은 예측 불가능한 상태가 된다. 이를 시각적으로 확인해보자.

```text
 [ Case A: No Lock (Race Condition) ]    [ Case B: File Locking (Protected) ]
 ──────────────────────────────────     ───────────────────────────────────
 Process A  Read X(100) ─┐              Process A  Lock(X) ── Read X(100)
 Process B  Read X(100) ─┘                           │
 Process A  Calc: 100+10                           Calc: 100+10
 Process B  Calc: 100+20                           │
 Process A  Write X(110) │                         Write X(110) ─┐
 Process B  Write X(120) │                         Process B     │ Wait...
      ▼                                      Process A  Unlock(X)│
   Result: 120 (Lost!)                              ▼
                                          Process B  Lock(X) ── Read X(110)
                                                      Calc: 110+20
                                                      Write X(130)
                                                           ▼
                                                   Result: 130 (Integrity OK)
```

**[다이어그램 해설]**
위의 ASCII 다이어그램은 잠금이 없을 때와 있을 때의 데이터 흐름을 비교한 것이다.
- **Case A (좌측)**: 프로세스 A와 B가 거의 동시에 `X=100`을 읽는다. 각자 연산을 수행(110, 120)하지만, A가 쓰기 직후 B가 쓰기를 수행하면 최종 값은 120이 된다. A의 노력이 사라진 **Lost Update**가 발생한다.
- **Case B (우측)**: A가 먼저 `Lock(X)`를 획득한다. B는 Lock이 해제될 때까지 `Wait` 상태로 대기한다. A가 110을 쓰고 퇴장(Unlock)하면, B가 진입하여 **110**을 읽고 20을 더해 **130**을 저장한다. 데이터의 무결성이 지켜진다.

📢 **섹션 요약 비유**: 파일 잠금은 **"공용 화장실의 문잠금 장치"**와 같다. 화장실(파일) 안에서는 한 명(프로세스)만 깨끗하게 청소(쓰기)할 수 있어야 하며, 문을 잠그지 않으면 다른 사람이 들어와 청소 상태를 망칠 수 있기 때문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석 (5개 모듈)
파일 잠금 시스템을 구현하기 위해서는 운영체제 커널(Kernel) 내부의 여러 구성 요소가 유기적으로 작용해야 한다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 관련 프로토콜/시스템 콜 | 비유 |
|:---|:---|:---|:---|:---|
| **Lock Manager (락 관리자)** | 잠금 상태를 유지하고 요청을 승인/거부하는 중재자 | **Kernel Space**에서 **Lock Table(해시 테이블)**을 관리하며, 요청된 Lock의 유형(S/X)과 현재 보유자를 비교하여 상태 배정 | OS Kernel, `flock()`, `fcntl()` | 경비원 |
| **File Descriptor (파일 디스크립터)** | 프로세스와 파일 간의 채널 및 잠금 키(Key) | Open 시 생성되며, 이 FD를 기반으로 특정 바이트 범위(Byte-range)에 Lock을 설정 | File Table Entry, Inode | 출입증 |
| **Lock State (락 상태)** | 현재 자원의 보호 모드를 정의 | **Shared(공유)**: Read-Read 허용 / **Exclusive(배타)**: 모든 접근 차단 | State Bits (S-bit, X-bit) | 현황판 |
| **Waiting Queue (대기 큐)** | 충돌하는 Lock 요청을 순서대로 대기시키는 자료구조 | Semaphore 개념을 활용하여, Lock이 해제될 때까지 **Blocked 상태**의 프로세스를 큐잉 | Wait/Sleep Queue | 줄 서는 곳 |
| **Lock Granularity (잠금 단위)** | 동시성 제어의 정교함을 결정 | 파일 전체 vs **Byte-range Locking**(바이트 단위) -> 정교할수록 오버헤드 증가 but 병렬성 향상 | Record Locking, Page Locking | 구역 나누기 |

### 2. 공유 락(S-Lock)과 배타 락(X-Lock)의 상세 기술
잠금의 핵심은 **호환성(Compatibility)**에 달려 있다. 이 두 가지 모드의 상호작용 방식을 분석한다.

#### A. Shared Lock (S-Lock, 공유 잠금)
- **정의**: 데이터를 **읽기(Read)**만 수행할 때 사용하는 잠금.
- **동작 원리**:
    1. 프로세스 A가 `READ_LOCK` 요청.
    2. 락 관리자는 현재 해당 파일에 **X-Lock(배타)**이 있는지 확인.
    3. X-Lock이 없다면, **다른 프로세스의 S-Lock 요청을 모두 허용**하여 동시 다중 접근을 허용.
    4. 데이터 변경을 방지하기 위해, S-Lock이 걸려 있는 동안 X-Lock 요청은 **Block(대기)** 시킴.
- **목적**: **Concurrency(동시성)**을 높이는 것이 주 목적.

#### B. Exclusive Lock (X-Lock, 배타 잠금)
- **정의**: 데이터를 **쓰기(Write)**하거나 **갱신(Update)**할 때 사용하는 잠금.
- **동작 원리**:
    1. 프로세스 B가 `WRITE_LOCK` 요청.
    2. 락 관리자는 현재 파일에 **어떤 종류의 Lock(S 또는 X)**이라도 걸려 있는지 확인.
    3. 다른 Lock이 존재하면, **모든 요청을 Block**하고 자신의 차례가 올 때까지 대기(Wait).
    4. 획득 후에는 다른 모든 프로세스(읽기 포함)의 접근을 물리적/논리적으로 차단.
- **목적**: **Isolation(독립성)**과 **Integrity(무결성)**이 주 목적.

### 3. 잠금 호환성 행렬 (Lock Compatibility Matrix)

```text
      [ Requested Lock ]
      +-------+-------+
      |   S   |   X   |
  ────┼───────┼───────┼─────────────────────────────────────
 H S  │  YES  │  NO   │  [S on S]: 동시 읽기 허용 (성능 UP)
 o ───┼───────┼───────┼─────────────────────────────────────
 l X  │  NO   │  NO   │  [X on ?]: 쓰기는 모든 것을 배제 (안전)
 d    +-------+-------+
 (Current Lock Holder)

 YES : Granted (Lock 획득 성공)
 NO  : Wait (대기 큐로 이동 -> Blocking)
```

**[다이어그램 해설]**
이 행렬은 잠금 관리자의 의사결정 로직을 나타낸다. 
- **S-Lock은 S-Lock과 호환(YES)**: 독자(Reader)들은 서로 방해하지 않는다. 
- **X-Lock은 누구와도 호환되지 않는다(NO)**: 작성자(Writer)는 독점적이어야 한다. 이 매트릭스는 데드락(Deadlock) 가능성을 판단하는 기초 자료이기도 하다.

### 4. 핵심 알고리즘: POSIX fcntl을 활용한 바이트 범위 잠금 (C 코드 예시)

```c
#include <fcntl.h>
#include <unistd.h>

// 구조체 설정
struct flock fl;
fl.l_type = F_WRLCK;    // 잠금 타입: F_RDLCK(S-Lock), F_WRLCK(X-Lock)
fl.l_whence = SEEK_SET; // 기준점: 파일 시작
fl.l_start = 0;         // 시작 오프셋
fl.l_len = 0;           // 길이: 0은 파일 끝(EOF)까지 의미
fl.l_pid = getpid();    // 프로세스 ID

// 시스템 콜 실행 (fd: 파일 디스크립터)
if (fcntl(fd, F_SETLK, &fl) == -1) {
    // 잠금 획득 실패 (EAGAIN, EACCES 등)
    perror("Lock Failed: Resource busy or conflict");
    return -1;
}
// -------------------------------------------------
// [Critical Section]
// 여기서 안전하게 파일 입출력 수행 (Read/Write)
// -------------------------------------------------

fl.l_type = F_UNLCK;    // 잠금 해제
fcntl(fd, F_SETLK, &fl);
```

**[코드 해설]**
위 코드는 **UNIX/Linux 계열의 표준 API**인 `fcntl`을 사용한 예제이다. 
- `l_type`을 통해 S-Lock(`F_RDLCK`)과 X-Lock(`F_WRLCK`)을 선택할 수 있으며, 
- `l_start`와 `l_len`을 통해 **파일의 일부분(특정 레코드)에만 락**을 걸 수 있다. 
이를 통해 A 프로세스는 파일 앞부분을 쓰고, B 프로세스는 뒷부분을 쓰는 **Parallel Write(병렬 쓰기)**가 가능해져 대역폭 효율이 비약적으로 증가한다.

📢 **섹션 요약 비유**: 공유 락과 배타 락의 관계는 **"전시회의 그림 관람(공유)과 그림 복원 작업(배타)"**과 같다. 관람객(읽기)들은 여러 명이 동시에 그림을 감상해도 문제가 없지만, 복원가(쓰기)가 작업할 때는 어떤 관람객도 방해하거나 먼지를 일으켜서는 안 되므로 전시실을 폐쇄해야 한다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 운영체제별 구현 전략 비교 (Mandatory vs Advisory)

| 비교 항목 | **Mandatory Locking (강제적 잠금)** | **Advisory Locking (권고적 잠금)** |
|:---|:---|:---|
| **동작 방식** | **OS Kernel**이 파일 접근 시스템 콜(`read`, `write`) 자체를 가로채어 락이 없으면 **강제로 실패(EACCES)** 처리함. | OS는 락 상태를 관리하지만, `read`/`write`를 막지 않음. **프로세스가 스스로 락 확인(`fcntl`) 후 접근**하는 '신뢰 모델'임. |
| **주요 환경** | Windows OS (기본 동작), SMB/CIFS 프로토콜 | UNIX/Linux (주로 `flock` 사용), NFS(Network File System) |
| **장점** | 데이터 무결성이 **물리적으로 보장**됨. 악의적인 프로세스나 버그로부터 안전. | 구현이 단순하고 유연함. **Cooperative Multitasking** 환경에서 빠름. |
| **단점** | 락 관리를 위한 커널 오버헤드가 큼. 잘못된 락 설정으로 인한 **시스템 교착(Deadlock)** 위험 증가. | 규칙을 지키지 않는 프로세스(Bad Actor)는 락을 무시하고 접근 가능하여 **데이터 충돌 발생 가능**. |
| **성능 지표** | Latency는 다소 높으나 Safety가 중요한 금융/결제 시스템에 적합. | Latency가 낮고 Throughput이 높아 대용량 로그 처리 등에 적합. |

### 2. 타 과목 융합 관점 (OS, DB, Network)

#### A. 데이터베이스(DB)와의 연계: 트랜잭션 격리 수준 (Transaction Isolation)
파일 시스템의 락은 데이터베이스의 **Isolation Level**로 정교하게 발전했다.
- **Read Uncommitted**: 락을 거의 사용하지 않음 (성능 최우선, 일관성 최악).
- **Repeatable Read**: 트랜잭션 시작 시