+++
title = "602. 샌드박싱 (Sandboxing) 기술 커널 래퍼"
weight = 602
+++

# 602. SATA (Serial ATA)

weight = 602
+++

# 602. SATA (Serial ATA)

weight = 602
+++

# 602. SATA (Serial ATA)

weight = 602
+++

# 602. SATA (Serial ATA)
weight = 602
+++

# 602. SATA (Serial ATA)
weight = 602
+++

# 602. SATA (Serial ATA)

Serial ATA)은 **직렬 방식으로 데이터를 전송하는 저장 장치 인터페이스**입니다.

### 💡 비유: 직렬 도로
SATA는 **직렬 도로**와 같습니다. 한 차선씩 빠르게 이동합니다.

### SATA 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                SATA 구조                                              │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【SATA 표준】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  표준              속도            대역폭         케이블         │ │   │
│  │  ────              ────            ────          ────          │ │   │
│  │  SATA 1.0          150 MB/s       1.5 Gb/s       7-pin         │ │   │
│  │  SATA 2.0          300 MB/s       3 Gb/s       7-pin         │ │   │
│  │  SATA 3.0          600 MB/s       6 Gb/s       7-pin         │ │   │
│  │  SATA 3.2          750 MB/s       6 Gb/s       7-pin         │ │   │
│  │  eSATA            300 MB/s       3 Gb/s       외부 포트        │ │   │
│  │  eSATAp           600 MB/s       6 Gb/s       외부 포트        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【SATA 케이블】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  케이블 타입          길이              용도                     │ │   │
│  │  ────────            ────              ────                    │ │   │
│  │  내부용            최대 1m            케이스 내부               │ │   │
│  │  eSATA             최대 2m            외부 연결                 │ │   │
│  │                                                             │ │   │
│  │  핀 구성 (7-pin):                                              │ │   │
│  │  • 1: GND                                                       │ │   │
│  │  • 2: TX+ (송신)                                                 │ │   │
│  │  • 3: TX- (수신)                                                 │ │   │
│  │  • 4: GND                                                        │ │   │
│  │  • 5: B+ (신호)                                                    │ │   │
│  │  • 6: B- (신호)                                                    │ │   │
│  │  • 7: GND                                                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【SATA vs PATA vs SCSI】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  항목            PATA             SATA              SCSI            │ │   │
│  │  ────            ────             ────              ────            │ │   │
│  │  전송 방식        병렬 (40/80핀)    직렬               병렬             │ │   │
│  │  속도            133 MB/s        150-750 MB/s      640 MB/s         │ │   │
│  │  케이블          40/80선          7선               50선 (Wide)       │ │   │
│  │  케이블 길이       46cm            1m/2m             12m             │ │   │
│  │  장치 수          2               1 (포트당)          15 (Wide)         │ │   │
│  │  핫 스왑          미지원            지원               지원              │ │   │
│  │  비용            낮음             낮음               높음              │ │   │
│  │  용도            구형 PC          데스크탑/PC         서버              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【SATA 데이터 전송】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  호스트 (HBA)                    장치 (HDD/SSD)                      │ │   │
│  │  ┌─────────────┐               ┌─────────────┐                    │ │   │
│  │  │   TX+        │──────────────▶│   RX-        │                    │ │   │
│  │  │   TX-        │◀──────────────│   TX+        │                    │ │   │
│  │  │   B+         │◀──────▶│   B-         │ (클럭 신호)            │ │   │
│  │  │   B-         │◀──────▶│   B+         │                    │ │   │
│  │  │   GND        │          │   GND        │                    │ │   │
│  │  └─────────────┘               └─────────────┘                    │ │   │
│  │                                                             │ │   │
│  │  LVDS (Low Voltage Differential Signaling):                       │ │   │
│  │  • 저전력 차동 신호 전송                                           │ │   │
│  │  • 높은 노이즈 내성                                                 │ │   │
│  │  • 8b/10b 인코딩                                                    │ │   │
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
│                SATA 상세                                              │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【SATA 명령 구조】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  Frame Information Structure (FIS):                             │ │   │
│  │  • 64비트 FIS 구조                                                 │ │   │
│  │  • LBA (Logical Block Address) 지원                               │ │   │
│  │  • 48비트 LBA = 128PB 이상 지원                                      │ │   │
│  │                                                             │ │   │
│  │  NCQ (Native Command Queuing):                                     │ │   │
│  │  • SATA 2.0 이상 지원                                                │ │   │
│  │  • 최대 32개 명령 동시 처리                                          │ │   │
│  │  • 순서 최적화 (Seek + Rotational Latency)                        │ │   │
│  │                                                             │ │   │
│  │  Command Types:                                                   │ │   │
│  │  • READ DMA: 데이터 읽기                                              │ │   │
│  │  • WRITE DMA: 데이터 쓰기                                             │ │   │
│  │  • READ FPD: FPD(Feature Protection Data) 읽기                      │ │   │
│  │  • SMART: SMART 데이터                                               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【SATA 기능】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  핫 스왑 (Hot Plug):                                               │ │   │
│  │  • 시스템 전원 켜진 상태에서 장치 연결/분리                               │ │   │
│  │  • AHCI 모드에서 지원                                                │ │   │
│  │                                                             │ │   │
│  │  APM (Advanced Power Management):                                   │ │   │
│  │  • 저전력 모드 지원                                                  │ │   │
│  │  • Partial/Slumber/DevSleep                                         │ │   │
│  │                                                             │ │   │
│  │  SMART (Self-Monitoring, Analysis, Reporting Technology):          │ │   │
│  │  • 드라이브 상태 모니터링                                             │ │   │
│  │  • 온도, 에러율, 가용 예비 영역                                        │ │   │
│  │                                                             │ │   │
│  │  TRIM (SSD):                                                        │ │   │
│  │  • 불필요한 블록 표시                                                  │ │   │
│  │  • SSD 성능 향상                                                      │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【AHCI 모드】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  AHCI (Advanced Host Controller Interface):                        │ │   │
│  │  • SATA 고급 기능 활성화                                              │ │   │
│  │  • NCQ, 핫 스왑, APM 지원                                             │ │   │
│  │  • BIOS/UEFI에서 설정                                                 │ │   │
│  │                                                             │ │   │
│  │  IDE 모드 (Legacy):                                                 │ │   │
│  │  • PATA 호환 모드                                                    │ │   │
│  │  • NCQ 미지원                                                        │ │   │
│  │  • 구형 OS 호환용                                                    │ │   │
│  │                                                             │ │   │
│  │  RAID 모드:                                                         │ │   │
│  │  • 컨트롤러 레벨 RAID                                                  │ │   │
│  │  • AHCI 기반                                                         │ │   │
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
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【SATA 장치 확인】                                                    │
│  ──────────────────                                                │
│  // lsblk                                                            │
│  $ lsblk                                                             │
│  NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT                        │
│  sda      8:0    0 238.5G  0 disk                                   │
│  ├─sda1   8:1    0   512M  0 part /boot/efi                        │
│  └─sda2   8:2    0   238G  0 part /                                │
│                                                                     │
│  // hdparm                                                            │
│  $ sudo hdparm -I /dev/sda                                           │
│  // SATA 버전, 속도, 기능 확인                                         │
│                                                                     │
│  // 현재 전송 모드                                                      │
│  $ sudo hdparm -I /dev/sda | grep -i sata                            │
│  *    SATA version is: SATA 3.2                                     │
│  *    transport: Serial, SATA1.0, SATA2.0, SATA3.0                  │
│                                                                     │
│  【SATA 성능 테스트】                                                   │
│  ──────────────────                                                │
│  // hdparm 읽기 테스트                                                  │
│  $ sudo hdparm -t /dev/sda                                           │
│  /dev/sda:                                                           │
│   Timing buffered disk reads: 500 MB in  3.00 seconds = 166.67 MB/sec│
│                                                                     │
│  // 캐시 포함                                                          │
│  $ sudo hdparm -T /dev/sda                                           │
│   Timing cached reads:   2000 MB in  2.00 seconds = 1000.00 MB/sec   │
│                                                                     │
│  // dd 순차 읽기                                                        │
│  $ sudo dd if=/dev/sda of=/dev/null bs=1M count=1000                │
│  1000+0 records in                                                   │
│  1000+0 records out                                                  │
│  1048576000 bytes (1.0 GB) copied, 6.0 s, 174.8 MB/s                │
│                                                                     │
│  【AHCI 모드 확인】                                                    │
│  ──────────────────                                                │
│  // dmesg                                                             │
│  $ dmesg | grep -i ahci                                              │
│  [    1.234567] ahci 0000:00:1f.2: AHCI 0001.0301 32 slots 6 ports   │
│                                                                     │
│  // /sys                                                              │
│  $ ls /sys/class/ata_port/                                           │
│  ata1  ata2  ata3                                                    │
│                                                                     │
│  // 포트 속도                                                           │
│  $ cat /sys/class/ata_port/ata1/ahci_port_speed                     │
│  6.0 Gbps                                                             │
│                                                                     │
│  【NCQ 확인】                                                          │
│  ──────────────────                                                │
│  // NCQ 지원 여부                                                      │
│  $ sudo hdparm -I /dev/sda | grep -i "queue depth"                  │
│  *    Queue Depth: 32                                                │
│                                                                     │
│  // NCQ 사용 중인지 확인                                                │
│  $ cat /sys/block/sda/device/queue_depth                            │
│  31                                                                  │
│                                                                     │
│  // I/O 스케줄러 (cfq = NCQ 활용)                                      │
│  $ cat /sys/block/sda/queue/scheduler                               │
│  [mq-deadline] none bfq                                              │
│                                                                     │
│  【SMART 정보】                                                        │
│  ──────────────────                                                │
│  // smartctl 전체 정보                                                 │
│  $ sudo smartctl -a /dev/sda                                         │
│                                                                     │
│  // SMART 상태만                                                        │
│  $ sudo smartctl -H /dev/sda                                         │
│  SMART overall-health self-assessment test result: PASSED            │
│                                                                     │
│  // 온도 확인                                                          │
│  $ sudo smartctl -A /dev/sda | grep -i temperature                  │
│  194 Temperature_Celsius     0x0022   100   100   000    35          │
│                                                                     │
│  // 에러 로그                                                           │
│  $ sudo smartctl -l error /dev/sda                                  │
│                                                                     │
│  【APM 설정】                                                          │
│  ──────────────────                                                │
│  // APM 상태 확인                                                      │
│  $ sudo hdparm -B /dev/sda                                           │
│  APM_level = 128                                                     │
│                                                                     │
│  // APM 비활성화 (서버용)                                               │
│  $ sudo hdparm -B 255 /dev/sda                                       │
│                                                                     │
│  // 자동 스핀다운 비활성화                                               │
│  $ sudo hdparm -S 0 /dev/sda                                         │
│                                                                     │
│  【eSATA 장치】                                                        │
│  ──────────────────                                                │
│  // eSATA 장치 연결 시                                                  │
│  $ dmesg | tail -20                                                  │
│  [12345.678901] sd 8:0:0:0: Attached SCSI disk                      │
│  [12345.678902] sd 8:0:0:0: [sdb] 976748448 512-byte logical blocks  │
│                                                                     │
│  // 마운트                                                             │
│  $ sudo mount /dev/sdb1 /mnt/external                               │
│                                                                     │
│  // 핫 언플러그                                                         │
│  $ sudo umount /mnt/external                                         │
│  $ echo 1 | sudo tee /sys/block/sdb/device/delete                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 직렬 방식으로 데이터를 전송하는 저장 장치 인터페이스
• 속도: 150 MB/s (SATA 1.0) ~ 750 MB/s (SATA 3.2)
• 케이블: 7-pin, 최대 1m (내부), 2m (eSATA)
• 핀 구성: 2개의 차동 신호 쌍 + 클럭 + GND
• 전송 방식: LVDS (저전력 차동 신호)
• NCQ: 최대 32개 명령 큐잉
• 핫 스왑: AHCI 모드에서 지원
• APM: 전력 관리 (Partial/Slumber/DevSleep)
• SMART: 자가 진단 기술
• TRIM: SSD 최적화
• AHCI: 고급 호스트 컨트롤러 인터페이스
• IDE: 레거시 호환 모드
• RAID: 컨트롤러 레벨 RAID 지원
• 확인: hdparm -I, lsblk
• 성능: hdparm -t, dd
• SMART: smartctl -a
• 모드: /sys/class/ata_port/
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [SCSI](./601_scsi.md) → 병렬 인터페이스, 서버급
- [NVMe](./603_nvme.md) → PCIe 기반 고속 인터페이스
- [HDD](./604_hdd.md) → SATA 장착 저장 장치
- [SSD](./605_ssd.md) → SATA 장착 SSD

### 👶 어린이를 위한 3줄 비유 설명
**개념**: SATA는 "직렬 도로" 같아요!

**원리**: 한 차선씩 빠르게 이동해요!

**효과**: PC에서 널리 사용하는 표준이에요!
