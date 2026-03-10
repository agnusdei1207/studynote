+++
title = "592. 셸코드 (Shellcode) 인젝션"
weight = 592
+++

# 592. Btrfs (B-tree File System)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스 차세대 COW 파일시스템
> 2. **가치**: 스냅샷, 서브볼륨, 압축, RAID
> 3. **융합**: COW, B+ 트리, qgroup과 연관

---

## Ⅰ. 개요

### 개념 정의
**Btrfs(B-tree File System)**는 **리눅스를 위한 차세대 Copy-on-Write 파일시스템**입니다.

### 💡 비유: 블록 조립 시스템
Btrfs는 **블록 조립 시스템**과 같습니다. 유연하게 구조를 변경할 수 있습니다.

### Btrfs 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                Btrfs 구조                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Btrfs 특징】                                                       │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  항목              Btrfs              ext4                   │ │   │
│  │  ────              ────                ────                   │ │   │
│  │  최대 파일 크기      16 EB              16 TB                  │ │   │
│  │  최대 볼륨          16 EB              1 EB                   │ │   │
│  │  스냅샷             지원                미지원                  │ │   │
│  │  서브볼륨           지원                미지원                  │ │   │
│  │  압축              투명 압축             미지원                  │ │   │
│  │  RAID              자체 지원            미지원                  │ │   │
│  │  COW               지원                부분                    │ │   │
│  │  온라인 축소        지원                지원                    │ │   │
│  │  온라인 확장        지원                지원                    │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Btrfs 구조】                                                       │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  ┌─────────────────────────────────────────────────────┐    │ │   │
│  │  │               Btrfs 파일시스템                        │    │ │   │
│  │  ├─────────────────────────────────────────────────────┤    │ │   │
│  │  │  서브볼륨 1    서브볼륨 2    서브볼륨 3                  │    │ │   │
│  │  │  (root)       (home)       (snapshots)               │    │ │   │
│  │  │     │             │             │                     │    │ │   │
│  │  │  스냅샷        스냅샷                                │    │ │   │
│  │  │     │                                             │    │ │   │
│  │  │  ─────────────────────────────────────────────    │    │ │   │
│  │  │            B+ 트리 구조                             │    │ │   │
│  │  │  (Chunk Tree, Extent Tree, Root Tree, etc.)        │    │ │   │
│  │  │  ─────────────────────────────────────────────    │    │ │   │
│  │  │            장치 (Device)                            │    │ │   │
│  │  │  [/dev/sda] [/dev/sdb] [/dev/sdc]                   │    │ │   │
│  │  └─────────────────────────────────────────────────────┘    │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 기능】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  기능              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  서브볼륨           독립적인 파일시스템 트리                         │ │   │
│  │  스냅샷            서브볼륨의 특정 시점 복사본                        │ │   │
│  │  압축              투명 압축 (lzo, zstd, zlib)                      │ │   │
│  │  RAID              0, 1, 10, 5, 6, DUP                            │ │   │
│  │  중복 제거          파일/블록 레벨                                  │ │   │
│  │  할당량 (qgroup)     서브볼륨별 공간 제한                             │ │   │
│  │  밸런스            데이터 재배치                                    │ │   │
│  │  디바이스 추가/제거   온라인으로 장치 관리                             │ │   │
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
│                Btrfs 상세                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【서브볼륨】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징:                                                           │ │   │
│  │  • 독립된 파일시스템 트리                                          │ │   │
│  │  • 개별 마운트 가능                                               │ │   │
│  │  • 스냅샷의 기준                                                   │ │   │
│  │  • 할당량 적용 가능                                               │ │   │
│  │                                                             │ │   │
│  │  일반적인 구성:                                                    │ │   │
│  │  @         - 루트 서브볼륨                                        │ │   │
│  │  @home     - 홈 디렉토리                                          │ │   │
│  │  @snapshots - 스냅샷 저장                                          │ │   │
│  │  @var      - 가변 데이터                                          │ │   │
│  │  @tmp      - 임시 파일                                            │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【RAID 프로필】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  프로필         최소 디스크    설명                                │ │   │
│  │  ──────         ─────────    ────                                │ │   │
│  │  single         1            기본, 스트라이프 없음                  │ │   │
│  │  dup            1            중복 (같은 디스크)                     │ │   │
│  │  raid0          2            스트라이핑, 성능                        │ │   │
│  │  raid1          2            미러링                               │ │   │
│  │  raid10         4            미러+스트라이프                        │ │   │
│  │  raid5          3            분산 패리티                          │ │   │
│  │  raid6          4            이중 패리티                          │ │   │
│  │                                                             │ │   │
│  │  메타데이터와 데이터에 다른 프로필 적용 가능                           │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【압축】                                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  알고리즘:                                                        │ │   │
│  │  • lzo: 빠름, 낮은 압축률                                         │ │   │
│  │  • zstd: 균형 (권장)                                             │ │   │
│  │  • zlib: 높은 압축률, 느림                                         │ │   │
│  │  • no: 압축 없음                                                  │ │   │
│  │                                                             │ │   │
│  │  마운트 옵션: compress=zstd                                       │ │   │
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
│  【Btrfs 파일시스템 생성】                                             │ |
│  ──────────────────                                                │
│  // 기본 생성                                                        │
│  $ sudo mkfs.btrfs /dev/sdb1                                       │
│  $ sudo mkfs.btrfs -L mylabel /dev/sdb1                            │
│                                                                     │
│  // RAID 1                                                          │
│  $ sudo mkfs.btrfs -d raid1 -m raid1 /dev/sdb /dev/sdc             │
│                                                                     │
│  // RAID 10                                                         │
│  $ sudo mkfs.btrfs -d raid10 -m raid10 /dev/sd{b,c,d,e}            │
│                                                                     │
│  【Btrfs 마운트】                                                      │ |
│  ──────────────────                                                │
│  // 기본 마운트                                                       │
│  $ sudo mount /dev/sdb1 /mnt/btrfs                                 │
│                                                                     │
│  // 압축 옵션                                                         │
│  $ sudo mount -o compress=zstd /dev/sdb1 /mnt/btrfs                │
│                                                                     │
│  // /etc/fstab                                                       │
│  UUID=xxx  /mnt/btrfs  btrfs  defaults,compress=zstd  0  0         │
│                                                                     │
│  // 서브볼륨 마운트                                                    │
│  $ sudo mount -o subvol=@home /dev/sdb1 /home                      │
│                                                                     │
│  【서브볼륨 관리】                                                      │ |
│  ──────────────────                                                │
│  // 서브볼륨 생성                                                      │
│  $ sudo btrfs subvolume create /mnt/btrfs/@home                    │
│  $ sudo btrfs subvolume create /mnt/btrfs/@snapshots               │
│                                                                     │
│  // 서브볼륨 목록                                                      │
│  $ sudo btrfs subvolume list /mnt/btrfs                            │
│  $ sudo btrfs subvolume show /mnt/btrfs                            │
│                                                                     │
│  // 서브볼륨 삭제                                                      │
│  $ sudo btrfs subvolume delete /mnt/btrfs/@old                     │
│                                                                     │
│  // 기본 서브볼륨 설정                                                  │
│  $ sudo btrfs subvolume set-default @ /mnt/btrfs                   │
│                                                                     │
│  【스냅샷】                                                           │ |
│  ──────────────────                                                │
│  // 스냅샷 생성                                                        │
│  $ sudo btrfs subvolume snapshot /mnt/btrfs/@home \                │
│    /mnt/btrfs/@snapshots/home_$(date +%F)                          │
│                                                                     │
│  // 읽기 전용 스냅샷                                                    │
│  $ sudo btrfs subvolume snapshot -r /mnt/btrfs/@home \             │
│    /mnt/btrfs/@snapshots/home_ro_$(date +%F)                       │
│                                                                     │
│  // 스냅샷 복원 (삭제 후 스냅샷으로 교체)                                 │
│  $ sudo btrfs subvolume delete /mnt/btrfs/@home                    │
│  $ sudo btrfs subvolume snapshot /mnt/btrfs/@snapshots/home_backup \│
│    /mnt/btrfs/@home                                                 │
│                                                                     │
│  // 스냅샷 전송                                                        │
│  $ sudo btrfs send /mnt/btrfs/@snapshots/home_ro | \               │
│    sudo btrfs receive /backup/btrfs                                │
│                                                                     │
│  // 증분 전송                                                          │
│  $ sudo btrfs send -p @snapshots/home_1 @snapshots/home_2 | \      │
│    sudo btrfs receive /backup/btrfs                                │
│                                                                     │
│  【RAID 관리】                                                        │ |
│  ──────────────────                                                │
│  // 장치 추가                                                        │
│  $ sudo btrfs device add /dev/sdd /mnt/btrfs                       │
│                                                                     │
│  // 장치 제거                                                         │
│  $ sudo btrfs device remove /dev/sdb /mnt/btrfs                    │
│                                                                     │
│  // 장치 교체                                                         │
│  $ sudo btrfs replace start /dev/sdb /dev/sde /mnt/btrfs           │
│  $ sudo btrfs replace status /mnt/btrfs                            │
│                                                                     │
│  // RAID 프로필 변경                                                   │
│  $ sudo btrfs balance start -dconvert=raid1 -mconvert=raid1 /mnt   │
│                                                                     │
│  // 밸런스 (데이터 재배치)                                              │
│  $ sudo btrfs balance start /mnt/btrfs                             │
│  $ sudo btrfs balance start -dusage=50 /mnt/btrfs    // 50% 미만만   │
│                                                                     │
│  // 사용량 확인                                                        │
│  $ sudo btrfs filesystem df /mnt/btrfs                             │
│  $ sudo btrfs device usage /mnt/btrfs                              │
│                                                                     │
│  【할당량 (qgroup)】                                                   │ |
│  ──────────────────                                                │
│  // qgroup 활성화                                                     │
│  $ sudo btrfs quota enable /mnt/btrfs                              │
│                                                                     │
│  // qgroup 생성                                                      │
│  $ sudo btrfs qgroup create 1/100 /mnt/btrfs                       │
│                                                                     │
│  // 서브볼륨에 할당량 설정                                               │
│  $ sudo btrfs qgroup limit 100G /mnt/btrfs/@home                   │
│                                                                     │
│  // qgroup 확인                                                      │
│  $ sudo btrfs qgroup show /mnt/btrfs                               │
│                                                                     │
│  【유지보수】                                                         │ |
│  ──────────────────                                                │
│  // 파일시스템 정보                                                     │
│  $ sudo btrfs filesystem show                                       │
│  $ sudo btrfs filesystem usage /mnt/btrfs                          │
│                                                                     │
│  // 조각 모음                                                         │
│  $ sudo btrfs filesystem defragment /mnt/btrfs                     │
│  $ sudo btrfs filesystem defragment -r /mnt/btrfs     // 재귀        │
│                                                                     │
│  // 스크럽 (데이터 무결성 검사)                                          │
│  $ sudo btrfs scrub start /mnt/btrfs                               │
│  $ sudo btrfs scrub status /mnt/btrfs                              │
│                                                                     │
│  // 복구 모드로 마운트                                                   │
│  $ sudo mount -o recovery,ro /dev/sdb1 /mnt                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 리눅스 차세대 COW 파일시스템
• 최대 크기: 파일/볼륨 16 EB
• 서브볼륨: 독립적 파일시스템 트리
• 스냅샷: 서브볼륨의 특정 시점 복사본
• RAID: 0, 1, 10, 5, 6, dup, single
• 압축: lzo, zstd (권장), zlib
• COW: 쓰기 시 복사
• qgroup: 서브볼륨별 할당량
• 생성: mkfs.btrfs
• 서브볼륨: btrfs subvolume create
• 스냅샷: btrfs subvolume snapshot
• 밸런스: btrfs balance start
• 장치: btrfs device add/remove
• 스크럽: btrfs scrub start
• 전송: btrfs send | btrfs receive
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [파일 시스템](./575_file_system.md) → Btrfs의 상위 개념
- [ZFS](./591_zfs.md) → 유사한 COW 파일시스템
- [RAID](./584_raid.md) → Btrfs RAID

### 👶 어린이를 위한 3줄 비유 설명
**개념**: Btrfs는 "블록 조립 시스템" 같아요!

**원리**: 유연하게 구조를 변경할 수 있어요!

**효과**: 스냅샷으로 쉽게 복구해요!
