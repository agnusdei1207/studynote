+++
title = "606. 감사 (Auditing) 로깅 프레임워크 (Linux Auditd)"
weight = 606
+++

# 606. TRIM (Trim Command)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SSD에서 사용하지 않는 블록을 정리하는 명령어
> 2. **가치**: SSD 성능 유지, 수명 연장
> 3. **융합**: SSD, Garbage Collection, fstrim과 연관

---

## Ⅰ. 개요

### 개념 정의
**TRIM(Trim)**은 **SSD에서 삭제된 데이터가 차지하는 블록을 운영체제에 알리리는 명령어**입니다. 파일 삭제 시 해당 블록을 정리 대상으로 표시하여 SSD의 쓰기 성능을 유지합니다.

### 💡 비유: 청소 예약
TRIM은 **청소 예약**과 같습니다. "언제 청소할지" 미리 알려줍니다.
### TRIM 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                TRIM 구조                                             │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【TRIM 동작 원리】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. 파일 삭제 (OS)                                                │ │   │
│  │     └─▶ 파일 시스템이 삭제된 블록을 TRIM 명령으로 표시                   │ │   │
│  │                                                             │ │   │
│  │  2. TRIM 전달 (커널)                                              │ │   │
│  │     └─▶ TRIM 명령이 SSD 컨트롤러로 전달                        │ │   │
│  │                                                             │ │   │
│  │  3. 블록 마크 (SSD)                                               │ │   │
│  │     └─▶ 해당 블록이 "삭제됨"으로 표시                        │ │   │
│  │                                                             │ │   │
│  │  4. 가비지 회수 (GC)                                               │ │   │
│  │     └─▶ Garbage Collection 시 해당 블록 정리                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【TRIM vs 삭제】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  작업              TRIM 없이            TRIM 있이              │ │   │
│  │  ────              ────              ────                    │ │   │
│  │  파일 삭제          즉시 공간 해제        지연 공간 해제              │ │   │
│  │  블록 상태          "사용 중" 유지        "삭제됨"으로 표시             │ │   │
│  │  쓰기 성능          저하 가능            유지                       │ │   │
│  │  GC 부하           증가                감소                       │ │   │
│  │  SSD 수명           단축 가능            유지                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【TRIM 종류】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  종류              설명                    시기                     │ │   │
│  │  ────              ────                    ────                     │ │   │
│  │  수동 TRIM        사용자가 직접 실행        필요 시                   │ │   │
│  │  연속 TRIM        실시간 (discard)          쓰기 시                   │ │   │
│  │  주기적 TRIM      스케줄러 (fstrim.timer)   정기적                  │ │   │
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
│                TRIM 상세                                             │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【TRIM 구현 방식】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. discard 마운트 옵션                                             │ │   │
│  │     • mount -o discard /dev/sda1 /mnt                         │ │   │
│  │     • 쓰기 시마다 TRIM 전달                                       │ │   │
│  │     • 실시간성 보장, 오버헤드 가능                                  │ │   │
│  │                                                             │ │   │
│  │  2. fstrim.timer                                                  │ │   │
│  │     • systemd 타이머로 주기적 TRIM                                 │ │   │
│  │     • 기본: 주 1회                                                 │ │   │
│  │     • 시스템 부하 분산                                             │ │   │
│  │                                                             │ │   │
│  │  3. 수동 fstrim                                                    │ │   │
│  │     • fstrim -v /mountpoint                                   │ │   │
│  │     • 필요 시 수동 실행                                            │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【TRIM 장점】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 쓰기 성능 유지: 쓰기 전 증폭 불필요                              │ │   │
│  │  • SSD 수명 연장: 불필요한 쓰기 감소                               │ │   │
│  │  • GC 효율 증가: 가비지 회수 최적화                                 │ │   │
│  │  • 공간 효율: 사용 가능한 블록 증가                                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【TRIM 고려사항】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 연속 TRIM: 쓰기 지연 가능                                       │ │   │
│  │  • 주기적 TRIM: 일정 시간 부하                                     │ │   │
│  │  • RAID: 일부 컨트롤러에서 TRIM 지원 제한                            │ │   │
│  │  • 암호화: 암호화된 파티션에서 TRIM 효과 제한                         │ │   │
│  │  • 온라인: 온라인 TRIM (파티션 테이블만)                              │ │   │
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
│  【TRIM 실행】                                                        │
│  ──────────────────                                                │
│  // 수동 TRIM                                                         │
│  $ sudo fstrim -v /                                                 │
│  $ sudo fstrim -v /home                                              │
│  $ sudo fstrim -av           // 모든 마운트 포인트                      │
│                                                                     │
│  // TRIM 진행 상태                                                      │
│  $ sudo fstrim -v / 2>&1 | head -5                                 │
│  /: 123.45 GiBtrimmed                                              │
│                                                                     │
│  // 건조 시간 확인                                                      │
│  $ time sudo fstrim -v /                                            │
│                                                                     │
│  【주기적 TRIM 설정】                                                │
│  ──────────────────                                                │
│  // fstrim.timer 상태 확인                                            │
│  $ systemctl status fstrim.timer                                    │
│                                                                     │
│  // fstrim.timer 활성화                                              │
│  $ sudo systemctl enable fstrim.timer                              │
│  $ sudo systemctl start fstrim.timer                                │
│                                                                     │
│  // 타이머 설정 확인                                                  │
│  $ systemctl list-timers | grep fstrim                             │
│                                                                     │
│  // 타이머 설정 변경                                                  │
│  $ sudo systemctl edit fstrim.timer                                │
│  // [Timer]                                                          │
│  // OnCalendar=weekly                                               │
│                                                                     │
│  // 수동 실행 로그                                                      │
│  $ journalctl -u fstrim.service                                    │
│                                                                     │
│  【discard 마운트 옵션】                                              │
│  ──────────────────                                                │
│  // 실시간 TRIM 마운트                                                  │
│  $ sudo mount -o discard /dev/sda1 /mnt                             │
│                                                                     │
│  // /etc/fstab 설정                                                    │
│  /dev/sda1  /  ext4  defaults,discard  0  1                         │
│                                                                     │
│  // 현재 마운트 옵션 확인                                              │
│  $ findmnt -n /                                                      │
│  $ mount | grep discard                                             │
│                                                                     │
│  // discard vs nodiscard                                              │
│  // discard: 실시간 TRIM                                             │
│  // nodiscard: TRIM 비활성화                                         │
│                                                                     │
│  【TRIM 지원 확인】                                                    │
│  ──────────────────                                                │
│  // 장치 TRIM 지원                                                      │
│  $ sudo hdparm -I /dev/sda | grep -i "TRIM"                       │
│  *   TRIM supported                                                  │
│                                                                     │
│  // 파일시스템 TRIM 지원                                              │
│  $ sudo tune2fs -l /dev/sda1 | grep -i discard                      │
│  Filesystem features: has_journal, ext_attr, resize_inode,...        │
│                                                                     │
│  // 커널 TRIM 지원                                                    │
│  $ cat /sys/block/sda/queue/discard_granularity                     │
│  $ cat /sys/block/sda/queue/discard_max_bytes                       │
│                                                                     │
│  // 블록 장치 discard 지원                                              │
│  $ lsblk -D /dev/sda                                                │
│  DISC-GRAN DISC-MAX DISC-ZERO WSAME                               │
│        512B       2G        0B      512B                              │
│                                                                     │
│  【RAID와 TRIM】                                                        │
│  ──────────────────                                                │
│  // mdadm RAID TRIM 지원 확인                                          │
│  $ sudo mdadm --detail /dev/md0 | grep -i "TRIM"               │
│                                                                     │
│  // RAID에서 discard 활성화                                          │
│  $ sudo mdadm --grow /dev/md0 --raid-devices=3 /dev/sda /dev/sdb /dev/sdc │
│                                                                     │
│  // LVM TRIM 지원                                                      │
│  $ sudo lvdisplay /dev/mapper/vg0-lv0 | grep -i "discards"            │
│                                                                     │
│  // LVM discard 설정                                                  │
│  // /etc/lvm/lvm.conf                                                 │
│  devices {                                                           │
│    issue_discards = 1                                                │
│  }                                                                   │
│                                                                     │
│  【TRIM 성능 영향】                                                    │
│  ──────────────────                                                │
│  // TRIM 전/후 성능 비교                                                │
│  $ sudo fio --name=/dev/sda --rw=randwrite --bs=4k --iodepth=32 \        │
│    --numjobs=4 --size=1G --direct=1                             │
│                                                                     │
│  // TRIM 없이                                                          │
│  $ sudo mount -o nodiscard /dev/sda1 /mnt                             │
│  // ... 테스트 ...                                                      │
│                                                                     │
│  // TRIM 있이                                                          │
│  $ sudo mount -o discard /dev/sda1 /mnt                               │
│  // ... 테스트 ...                                                      │
│                                                                     │
│  【문제 해결】                                                        │
│  ──────────────────                                                │
│  // TRIM이 작동하지 않음                                                │
│  $ dmesg | grep -i trim                                              │
│  $ sudo smartctl -a /dev/sda | grep -i "TRIM"                     │
│                                                                     │
│  // TRIM이 너무 느림                                                   │
│  $ sudo systemctl stop fstrim.timer                                 │
│  $ sudo mount -o nodiscard /dev/sda1 /mnt                             │
│                                                                     │
│  // RAID에서 TRIM 문제                                                │
│  $ cat /proc/mdstat                                                 │
│  $ sudo mdadm --detail /dev/md0                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: SSD에서 삭제된 블록을 정리하는 명령어
• 목적: SSD 쓰기 성능 유지, 수명 연장
• 종류: 수동 TRIM, 연속 TRIM, 주기적 TRIM
• 수동: fstrim -v /마운트포인트
- 주기적: fstrim.timer (systemd)
- 연속: mount -o discard
 마운트 옵션
- 장점: 쓰기 성능 유지, GC 효율 증가, 수명 연장
- 확인: hdparm -I, lsblk -D, tune2fs -l
- RAID: mdadm --detail로 TRIM 지원 확인
- LVM: /etc/lvm/lvm.conf issue_discards 설정
- 문제: dmesg, smartctl로 진단
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [SSD](./605_ssd.md) → TRIM을 사용하는 장치
- [Garbage Collection](./607_garbage_collection.md) → TRIM과 연동
- [fstrim](./616_fstrim.md) → TRIM 명령어
- [fstab](./583_fstab.md) → discard 마운트 옵션
- [Wear Leveling](./608_wear_leveling.md) → SSD 수명 관리
- [SMART](./614_smart.md) → SSD 상태 모니터링

 - [NVMe](./603_nvme.md) → NVMe SSD TRIM

### 👶 어린이를 위한 3줄 비유 설명
**개념**: TRIM은 "청소 예약" 같아요!

**원리**: 언제 청소할지 미리 알려줘요!

**효과**: SSD가 깨끗하게 유지돼요!
