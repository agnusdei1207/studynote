+++
title = "548. 저널링의 3단계 수준 - Journal, Ordered, Writeback"
date = "2026-03-14"
weight = 548
+++

# 548. 저널링의 3단계 수준 - Journal, Ordered, Writeback

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 저널링 수준(Journaling Levels)은 파일 시스템(File System)의 트랜잭션 안정성과 디스크 쓰기 성능 사이의 트레이드오프(Trade-off)를 제어하는 메커니즘이며, 메타데이터(Metadata)와 사용자 데이터(User Data)의 기록 순서를 결정한다.
> 2. **가치**: 시스템의 중요도와 워크로드(Workload) 특성에 따라 데이터 일관성을 완벽히 보장하는 `Journal` 모드, 성능과 안정성의 균형을 맞춘 `Ordered` 모드, 최고의 쓰기 성능을 내는 `Writeback` 모드를 선택하여 리소스를 최적화할 수 있다.
> 3. **융합**: OS(운영체제)의 커널(Kernel) I/O 스케줄링 정책 및 DBMS(데이터베이스 관리 시스템)의 WAL(Write-Ahead Logging) 전략과 연계하여, 스토리지 계층에서의 중복 로깅 오버헤드를 제거하고 전체 시스템의 처리량(Throughput)을 극대화하는 설계가 필요하다.

---

### Ⅰ. 개요 (Context & Background)

저널링 파일 시스템(Journaling File System)은 시스템 충돌(Crash)이나 정전 발생 시 파일 시스템의 무결성(Integrity)을 보장하기 위해 변경 사항을 로그에 먼저 기록하는 기법이다. 리눅스(Linux)의 EXT4나 XFS 같은 현대 파일 시스템은 단순한 '유무'의 차원을 넘어, '무엇을' 어디까지 기록할 것인가에 따라 세 가지 모드로 세분화하여 운영자에게 제공한다.

파일 시스템 관리의 핵심 딜레마는 **메타데이터**와 **사용자 데이터**의 관계에 있다. 메타데이터는 inode(Inode, Index Node)와 같이 파일의 위치, 크기, 권한을 관리하는 '지도' 역할을 하며, 사용자 데이터는 실제 파일 내용인 '집' 역할을 한다.
1.  **안전성(Safety)**: 모든 것을 기록하면 전원이 나가도 복구가 쉽지만, 디스크 대역폭(Bandwidth)을 2배로 소모하는 심각한 성능 저하가 발생한다.
2.  **성능(Performance)**: 반대로 지도(메타데이터)만 업데이트하면 성능은 좋아지지만, 시스템 붕괴 시 지도에는 '새 집'으로 표기되었는데 실제 땅에는 '허물어진 집'이 남아있는 '참조 훼손(Reference Corruption)'이 발생할 수 있다.

이러한 기술적 모순을 해결하기 위해, 데이터베이스의 ACID(Transaction Properties) 특성 중 원자성(Atomicity)과 내구성(Durability)을 파일 시스템 수준에서 구현하는 방식으로 진화해왔다. 이는 단순한 기술적 선택이 아니라, 비즈니스 연속성과 자원 효율성 사이의 균형점을 찾는 설계 과정이다.

**저널링 수준의 진화 과정**
기존의 FS(File System)는 `fsck`(File System Check)를 통해 부팅 시 전체 디스크를 스캔했으나, 용량이 테라바이트(TB) 단위로 커지면서 이 방식은 수십 분씩 시스템을 멈추게 하는 치명적 단점이 되었다. 저널링은 이 로그 영역만 확인하면 되므로 복구 시간을 RTO(Recovery Time Objective) 수초 단위로 줄여주었다.

```text
[ 초기 파일 시스템 (FAT, ext2) ]
   Crash 발생
      ↓
   부팅 시 전체 블록 스캔 ( consistency check )
      ↓ (시간 소모: 10분 ~ 수시간)
   시스템 복구

[ 저널링 파일 시스템 (ext3/4, XFS) ]
   Crash 발생
      ↓
   저널 영역(Transaction Log)만 재생 (Replay)
      ↓ (시간 소모: 수초)
   시스템 복구
```

📢 **섹션 요약 비유**: 저널링 모드를 선택하는 것은 복잡한 화물 운송 시스템에서 **'운송 보험'의 등급을 선택하는 것**과 같다. 
- **최상위 보험(Journal)**은 물건이 깨지면 100% 배상해주지만, 보험료(디스크 쓰기)가 비싸고 느리다.
- **기본 보험(Ordered)**은 운송 순서는 보장해주지만 내용물 파손에 대해선 책임이 약간 덜하며, 비용과 속도의 균형이 잡혀있다.
- **최저가 보험(Writeback)**은 박스가 배달은 되지만 안에 무엇이 들었는지, 혹은 순서가 맞는지 보증하지 않아 가장 빠르고 위험하다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

저널링의 핵심은 **커밋(Commit)** 시점과 **체크포인트(Checkpoint)**, 그리고 **플러시(Flushing)** 순서 제어에 있다. 커널의 VFS(Virtual File System, 가상 파일 시스템) 계층은 파일 시스템 드라이버에게 데이터 기록을 요청하며, 이때 설정된 저널링 모드에 따라 JBD(Journaling Block Device) 계층의 동작이 결정된다.

#### 1. 구성 요소 및 동작 비교 (Component Analysis)

파일 시스템의 쓰기 작업은 크게 **사용자 데이터 블록(Data Block)** 쓰기와 **메타데이터 블록(Metadata Block, Bitmap/Inode Table)** 쓰기로 나뉜다. 이 두 요소의 처리 순서(Sequence)와 로깅 여부가 세 가지 모드를 결정짓는다.

| 구성 요소 | 역할 | Journal Mode (Full Data) | Ordered Mode (Default) | Writeback Mode |
| :--- | :--- | :--- | :--- | :--- |
| **Data Log** | 사용자 데이터 기록 여부 | 저널에 기록 | 저널에 미기록 (Main FS 직접) | 저널에 미기록 |
| **Meta Log** | 메타데이터 기록 여부 | 저널에 기록 | 저널에 기록 | 저널에 기록 |
| **Commit Logic** | 트랜잭션 커밋 조건 | Meta와 Data가 모두 저널에 기록됨 | **Data가 메인 영역에 flush됨이 보장**된 후 Meta 저널 커밋 | Meta 저널 커밋 (Data flush 미보장) |
| **Integrity** | 크래시 복구 시 정합성 | 완벽 (모든 데이터 복구) | 높음 (파일 시스템 구조는 유지, 파일 내용은 0 가능) | 낮음 (메타만 복구, 파일 내용에 쓰레기 데이터 가능) |

#### 2. 저널링 모드별 아키텍처 및 데이터 흐름

아래는 사용자 프로세스가 `write()` 시스템 콜을 호출했을 때, 커널 내부에서 발생하는 디스크 쓰기 순서를 도식화한 것이다.

**[ Flow 1: Journal Mode (Full Data Journaling) ]**
데이터베이스의 WAL(Write-Ahead Logging)과 가장 유사하다. 모든 변경 사항이 저널 영역에 먼저 기록된다. 데이터 안정성은 가장 높지만, 쓰기 증폭(Write Amplification)이 2배 발생한다.

```text
Step 1: User Data Write
  ──[Data Block]──→ [ Journal Area (Log) ]
                                        │
Step 2: Metadata Write                  │
  ──[Inode]──────→ [ Journal Area (Log) ]
                                        │
Step 3: Commit Transaction              ▼
                   (Low-level I/O to Disk)
                                        │
Step 4: Checkpoint (Async) ───────────→ [ Main Filesystem Area ]
                   (Log → Main Move)
```

**[ Flow 2: Ordered Mode (Default for ext4) ]**
리눅스 커널이 가장 권장하는 모드이다. 메타데이터를 저널에 커밋하기 전에, 반드시 연관된 사용자 데이터가 물리적 디스크(Main Filesystem Area)에 안전히 기록되었음을 보장한다. 데이터 이중 기록의 오버헤드를 없애면서, 파일 시스템 구조가 깨지는 것을 방지한다.

```text
Step 1: User Data Write (Must be First!)
  ──[Data Block]──→ [ Main Filesystem Area ] 
        ▲               (Physical Disk Flush Guarantee)
        │
        │ (Wait for I/O Complete)
        │
Step 2: Metadata Write
  ──[Inode]──────→ [ Journal Area (Log) ]
                                        │
Step 3: Commit Transaction              ▼
                   (Log Safe)
```

**[ Flow 3: Writeback Mode ]**
가장 높은 성능을 제공한다. 사용자 데이터는 OS의 페이지 캐시(Page Cache)에 머물러 있다가 백그라운드 플러시(Flush) Thread에 의해 비동기적으로 기록된다. 메타데이터는 저널링되지만, 데이터보다 먼저 디스크에 기록될 수 있다. 전원 차단 시 '파일은 존재하는데 내용은 옛날 데이터'인 상태가 될 수 있다.

```text
Step 1: User Data Write
  ──[Data Block]──→ [ Page Cache (Memory) ]
                                    │
                                    │ (Async / Unordered)
                                    ▼
Step 2: Metadata Write             [ Main Filesystem Area ]
  ──[Inode]──────→ [ Journal Area (Log) ]
     (Could be written before data!)
```

#### 3. 심층 기술 해설 및 코드 레벨 분석

- **Journal Mode**: `ext4`에서 `data=journal` 옵션을 사용할 때 활성화된다. 모든 데이터가 저널을 거치므로, 트랜잭션 오버헤드가 매우 크다. 주로 특수한 목적의 시스템에서 사용된다.
- **Ordered Mode**: 핵심은 `wait_for_io_completion()` 이다. 파일 시스템 드라이버는 저널 트랜잭션을 닫기(Close Transaction) 전에, 해당 파일의 데이터 블록에 대한 I/O 완료 인터럽트(Interrupt)를 반드시 확인한다.
- **Writeback Mode**: 메타데이터만 순서를 보장하고, 사용자 데이터는 OS의 페이지 캐시 정책(Dirty Ratio, Dirty Background Ratio)에 완전히 위임한다. 순서가 보장되지 않으므로, 전원이 나갔을 때 메타데이터는 "새 파일이 생성됨"이라고 로깅하는데, 실제 데이터 블록에는 "이전 파일의 잔재"나 "0"이 남아있는 모순이 발생할 수 있다.

```c
// Ordered Mode Journaling Logic (Simplified Kernel Concept)
// JBD2 (Journaling Block Device 2) Layer Logic

void ordered_write_transaction(inode *ino, data_block *blk) {
    
    // Phase 1: 데이터 플러시 (Data Ordering Guarantee)
    // 실제 하드웨어에 쓰기 명령을 내리고 완료될 때까지 대기
    submit_bio(WRITE_SYNC, blk); 
    wait_for_io_completion(blk); 

    // Phase 2: 메타데이터 로깅
    // 데이터가 안전한 것을 확인 후 트랜잭션 시작
    handle_t *handle = journal_start(ino->i_journal);
    journal_add_transaction(handle, ino->metadata); 

    // Phase 3: 저널 커밋 (Transaction Atomicity)
    journal_commit(handle);
    
    // Phase 4: 체크포인트 (Checkpointing)
    // 저널의 내용을 실제 파일 시스템 위치로 비동기 복사
    // 이후 저널 공간 재사용 가능
    journal_checkpoint(ino->i_journal);
}
```

📢 **섹션 요약 비유**: 이는 **'복사기(Copier)의 작업 방식'**과 같다. 
- **Journal**은 원본과 복사본 모두를 금고(Journal)에 넣고 나서 작업 완료 표시를 하는 가장 깐깐한 방식이다 (느림).
- **Ordered**는 원본은 먼저 서랍(Filesystem)에 확실히 넣어둔 후, 목차(메타데이터)만 금고에 넣는 방식이다. 원본을 잃어버릴 염려는 없으므로 합리적이다.
- **Writeback**은 목차부터 마음대로 수정하고, 원본은 나중에 시간 날 때 아무 때나 넣는 방식이다. 업무 속도는 빠르지만 정전되면 엉망이 된다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 분석표 (Metrics-based Comparison)

단순한 '빠름/느림'을 넘어, 시스템 엔지니어가 의사결정 할 때 필요한 정량적 지표와 정성적 특성을 비교한다.

| 구분 | Journal Mode | Ordered Mode | Writeback Mode |
| :--- | :--- | :--- | :--- |
| **데이터 무결성** | **최상** (System + User) | **상** (System 무결성 보장, User 데이터 손실 가능성 있음) | **중** (System 구조 보장, User 데이터 훼손 위험 높음) |
| **쓰기 성능** | 낮음 (Low) | 중간 (Medium) | 높음 (High) |
| **CPU/메모리 사용** | 높음 (데이터 복사 오버헤드) | 낮음 (순서 제어 오버헤드만 존재) | 가장 낮음 (순서 제어 없음) |
| **RTO/RPO** | RPO=0 (데이터 손실 없음) | RPO≠0 (최근 쓰기 손실 가능) | RPO≠0 (데이터 훼손 가능) |
| **디스크 I/O 패턴** | 순차 쓰기 유리 (저널 영역에 몰아서 쓰임) | 혼합 (데이터는 랜덤, 저널은 순차) | 순차 쓰기 유리 (버퍼링 후 배치 쓰기 가능) |
| **주요 사용처** | 극히 중요한 시스템 로그, 특수 목적의 DB 전용 볼륨 | **일반 서버, 데스크탑, 웹 서버 (Standard)** | 임시 파일(/tmp), 빌드 output, VM Disk Image |

#### 2. 타 영역(운영체제/DB/스토리지)과의 융합 시너지

**A. 데이터베이스와의 관계 (DBMS & File System)**
대부분의 RDBMS(Oracle, MySQL PostgreSQL 등)는 이미 내부적으로 **Redo Log**나 **WAL(Write-Ahead Logging)**을 통해 데이터 무결성을 관리한다. 
- **중복 로깅(Double Logging