+++
title = "482. NVMe (Non-Volatile Memory Express) - PCIe 버스 기반 고속 플래시 프로토콜 (다중/깊은 큐 지원)"
weight = 482
+++

# 540. NVMe (Non-Volatile Memory Express)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SSD를 위한 고성능 스토리지 프로토콜
> 2. **가치**: 낮은 지연 시간과 높은 처리량
> 3. **융합**: PCIe, SSD, 고성능 I/O와 연관

---

## Ⅰ. 개요

### 개념 정의
**NVMe(Non-Volatile Memory Express)**는 **PCIe 기반 SSD를 위한 고성능 스토리지 프로토콜**입니다. 기존 AHCI/SATA의 한계를 극복합니다.

### 💡 비유: 고속도로
NVMe는 **일반 도로(SATA)를 고속도로(PCIe)로 바꾸는 것**과 같습니다. 더 많은 차선으로 더 빠르게 이동합니다.

### NVMe 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                NVMe 구조                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【NVMe vs SATA/AHCI】                                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징                SATA/AHCI               NVMe                        │ │   │
│  │  ────                ──────────                ────                        │ │   │
│  │  인터페이스          SATA                     PCIe                        │ │   │
│  │  큐 수               1 (NCQ)                   65536                       │ │   │
│  │  최대 처리량          ~600 MB/s               ~3500 MB/s (x4)            │ │   │
│  │  지연 시간            ~100 μs                 ~10 μs                      │ │   │
│  │  CPU 오버헤드         높음                     낮음                         │ │   │
│  │  명령어 세트          AHCI                    NVMe                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【아키텍처】                                                           │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  호스트 (CPU/메모리)                                            │ │   │
│  │  ────────────────                                              │ │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │ │   │
│  │  │                  Submissions Queue (SQ)                    │   │ │   │
│  │  │  [cmd] → [cmd] → [cmd] → ...                               │   │ │   │
│  │  │    admin SQ (관리용)                                        │   │ │   │
│  │  │    I/O SQs (데이터 전송용)                                  │   │ │   │
│  │  └─────────────────────────────────────────────────────────┘   │ │   │
│  │                         │                                       │ │   │
│  │                         ▼                                       │ │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │ │   │
│  │  │                  Completion Queue (CQ)                     │   │ │   │
│  │  │  [result] → [result] → [result] → ...                      │   │ │   │
│  │  │    admin CQ                                                 │   │ │   │
│  │  │    I/O CQs                                                  │   │ │   │
│  │  └─────────────────────────────────────────────────────────┘   │ │   │
│  │                                                             │ │   │
│  │                         │                                       │ │   │
│  │                         ▼                                       │ │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │ │   │
│  │  │                    NVMe SSD                                │   │ │   │
│  │  │  ─────────────────────────────────────                   │   │ │   │
│  │  │  Controller 0: Namespace 1, Namespace 2, ...               │   │ │   │
│  │  │  Controller 1: Namespace 3, Namespace 4, ...               │   │ │   │
│  │  │                                                         │   │ │   │
│  │  │  Namespace: 논리적 볼륨 (LBA 공간)                          │   │ │   │
│  │  │  Controller: 명령 처리 장치                                 │   │ │   │
│  │  │                                                         │   │ │   │
│  │  └─────────────────────────────────────────────────────────┘   │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                NVMe 상세                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【주요 명령어】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  관리 명령어 (Admin Commands)                                   │ │   │
│  │  ────────────────────────                                      │ │   │
│  │  • Identify: 컨트롤러/네임스페이스 정보 반환                        │ │   │
│  │  • Create/Delete I/O Queue: 큐 생성/삭제                         │ │   │
│  │  • Get Log Page: 로그 정보 반환                                  │ │   │
│  │  • Abort: 명령어 취소                                           │ │   │
│  │  • Set/Get Features: 기능 설정/조회                              │ │   │
│  │  • Format NVM: 포맷                                             │ │   │
│  │                                                             │ │   │
│  │  I/O 명령어 (NVM Commands)                                      │ │   │
│  │  ────────────────────────                                      │ │   │
│  │  • Read: 데이터 읽기                                            │ │   │
│  │  • Write: 데이터 쓰기                                           │ │   │
│  │  • Write Zeroes: 0으로 채우기                                    │ │   │
│  │  • Flush: 캐시 플러시                                            │ │   │
│  │  • Compare: 데이터 비교                                         │ │   │
│  │  • Dataset Management: 힌트 제공 (trim, etc)                     │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【PCIe 레인 구성】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  레인 수        대역폭 (PCIe 3.0)        대역폭 (PCIe 4.0)          │ │   │
│  │  ──────        ─────────────────        ─────────────────          │ │   │
│  │  x1            ~1 GB/s               ~2 GB/s                       │ │   │
│  │  x2            ~2 GB/s               ~4 GB/s                       │ │   │
│  │  x4            ~4 GB/s               ~8 GB/s                       │ │   │
│  │  x8            ~8 GB/s               ~16 GB/s                      │ │   │
│  │  x16           ~16 GB/s              ~32 GB/s                      │ │   │
│  │                                                             │ │   │
│  │  일반적인 NVMe SSD: PCIe 3.0 x4 또는 PCIe 4.0 x4                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【메모리 mapped I/O (MMIO)】                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  // Controller Registers (BAR0/BAR1)                           │ │   │
│  │  ────────────────────────────────────────                      │ │   │
│  │  Offset       Register                   Size                   │ │   │
│  │  ──────       ─────────────────────        ────                   │ │   │
│  │  0x0000      CAP (Capabilities)            64-bit               │ │   │
│  │  0x0008      VS (Version)                 32-bit               │ │   │
│  │  0x000C      INTMS (Interrupt Mask)       32-bit               │ │   │
│  │  0x0010      INTMC (Interrupt Clear)      32-bit               │ │   │
│  │  0x0014      CC (Controller Config)       32-bit               │ │   │
│  │  0x0018      CSTS (Controller Status)     32-bit               │ │   │
│  │  0x001C      NSSR (NVM Subsystem Reset)   32-bit               │ │   │
│  │  0x0020      AQA (Admin Queue Attrs)      32-bit               │ │   │
│  │  0x0024      ASQ (Admin SQ Base)          64-bit               │ │   │
│  │  0x002C      ACQ (Admin CQ Base)          64-bit               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【NVMe 장치 확인】                                                   │
│  ──────────────────                                                │
│  // 장치 목록                                                        │
│  $ ls /dev/nvme*                                                      │
│  /dev/nvme0  /dev/nvme0n1  /dev/nvme0n2                               │
│                                                                     │
│  // 장치 정보                                                        │
│  $ nvme list                                                         │
│  Node   SN                   Model                Namespace  Usage      │
│  -----  -------------------- -------------------- ---------  ---------  │
│  nvme0n1 S5H2NS0N300001P     Samsung SSD 970        1         256 GB     │
│                                                                     │
│  // 상세 정보                                                        │
│  $ sudo nvme id-ctrl /dev/nvme0                                       │
│  $ sudo nvme id-ns /dev/nvme0n1                                      │
│                                                                     │
│  【성능 측정】                                                        │
│  ──────────────────                                                │
│  // 읽기 성능                                                        │
│  $ sudo nvme read /dev/nvme0n1 --start-block=0 --block-count=1000   │
│  // 또는 fio 사용                                                     │
│  $ fio --name=randread --ioengine=libaio --iodepth=32 \                 │
│       --filename=/dev/nvme0n1 --bs=4k --rw=randread --size=10G           │
│                                                                     │
│  // 쓰기 성능                                                        │
│  $ sudo fio --name=write --ioengine=libaio --iodepth=32 \              │
│       --filename=/dev/nvme0n1 --bs=4k --rw=write --size=1G              │
│                                                                     │
│  // IOPS 측정                                                        │
│  $ sudo fio --name=randread --ioengine=io_uring --iodepth=128 \        │
│       --filename=/dev/nvme0n1 --bs=4k --rw=randread --size=10G \        │
│       --numjobs=4 --group_reporting                                    │
│                                                                     │
│  【SMART 상태 확인】                                                  │
│  ──────────────────                                                │
│  // SMART 정보                                                        │
│  $ sudo nvme smart-log /dev/nvme0                                    │
│  Smart Log for NVMe device:nvme0 namespace-id:ffffffff              │
│  critical_warning                    : 0                               │
│  temperature                          : 35 C                           │
│  available_spare                       : 100%                           │
│  available_spare_threshold             : 10%                           │
│  percentage_used                       : 2%                             │
│  data_units_read                       : 1,234,567                       │
│  data_units_written                    : 567,890                         │
│  host_read_commands                    : 12,345,678                       │
│  host_write_commands                   : 5,678,901                       │
│  ...                                                                │
│                                                                     │
│  【포맷 및 보안 erase】                                               │
│  ──────────────────                                                │
│  // 빠른 포맷                                                         │
│  $ sudo nvme format /dev/nvme0n1 --ses=0                             │
│                                                                     │
│  // 보안 erase ( cryptographic)                                     │
│  $ sudo nvme format /dev/nvme0n1 --ses=1                             │
│                                                                     │
│  // 사용자 데이터 erase                                              │
│  $ sudo nvme format /dev/nvme0n1 --ses=2                             │
│                                                                     │
│  【네임스페이스 관리】                                                 │
│  ──────────────────                                                │
│  // 네임스페이스 생성                                                  │
│  $ sudo nvme create-ns /dev/nvme0 --nsze=1000000 --ncap=1000000       │
│  $ sudo nvme attach-ns /dev/nvme0 --namespace-id=2                  │
│                                                                     │
│  // 네임스페이스 삭제                                                  │
│  $ sudo nvme detach-ns /dev/nvme0 --namespace-id=2                  │
│  $ sudo nvme delete-ns /dev/nvme0 --namespace-id=2                  │
│                                                                     │
│  【Linux 다중 큐 (blk-mq)】                                           │
│  ──────────────────                                                │
│  // NVMe는 기본적으로 blk-mq 사용                                      │
│  $ cat /sys/block/nvme0n1/queue/scheduler                           │
│  [none] mq-deadline                                                 │
│                                                                     │
│  // 하드웨어 큐 확인                                                   │
│  $ ls /sys/block/nvme0n1/mq/                                         │
│  0  1  2 3  // CPU별 큐                                               │
│                                                                     │
│  // 큐 깊이 확인                                                       │
│  $ cat /sys/block/nvme0n1/queue/nr_requests                          │
│  256                                                                │
│                                                                     │
│  【성능 비교 (일반적인 값)】                                           │
│  ──────────────────                                                │
│  장치                    순차 읽기        순차 쓰기      랜덤 IOPS        │
│  ────                    ────────        ────────        ────────        │
│  SATA SSD               550 MB/s       520 MB/s       90,000            │
│  NVMe PCIe 3.0 x4       3,500 MB/s     3,300 MB/s     500,000           │
│  NVMe PCIe 4.0 x4       7,000 MB/s     6,500 MB/s     1,000,000          │
│  NVMe PCIe 5.0 x4       14,000 MB/s    12,000 MB/s    2,000,000          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: PCIe 기반 SSD를 위한 고성능 프로토콜
• 비교: SATA/AHCI 대비 6배 이상 처리량
• 큐: 최대 65536개 (SATA는 1개)
• 구조: SQ(제출 큐) + CQ(완료 큐)
• 명령어: Admin(관리) + NVM(I/O)
• 레인: x1, x2, x4, x8, x16
• Namespace: 논리적 볼륨
• Linux: blk-mq, none 스케줄러
• 용도: 고성능 스토리지, 데이터베이스, 클라우드
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [I/O 스케줄링](./516_io_scheduling.md) → 스케줄러
- [SSD](../9_file_system/xxx.md) → 저장 장치
- [PCIe](./502_io_ports.md) → 버스 인터페이스

### 👶 어린이를 위한 3줄 비유 설명
**개념**: NVMe는 "고속도로" 같아요!

**원리**: 더 많은 차선으로 더 빠르게 가요!

**효과**: 아주 빠르게 데이터를 옮겨요!
