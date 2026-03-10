+++
title = "591. 버퍼 오버플로우 (Buffer Overflow) 원리 - C언어 취약 함수 악용 리턴 주소 덮어쓰기"
weight = 591
+++

# 591. ZFS (Zettabyte File System)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Sun 개발 128비트 통합 파일시스템/볼륨 매니저
> 2. **가치**: 데이터 무결성, 스냅샷, 압축, 중복 제거
> 3. **융합**: RAID-Z, COW, ARC 캐시와 연관

---

## Ⅰ. 개요

### 개념 정의
**ZFS(Zettabyte File System)**는 **Sun Microsystems가 개발한 통합 파일시스템과 볼륨 매니저**입니다.

### 💡 비유: 종합 저장소 관리 시스템
ZFS는 **종합 저장소 관리 시스템**과 같습니다. 모든 기능이 하나로 통합되어 있습니다.

### ZFS 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                ZFS 구조                                              │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【ZFS 계층 구조】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │                    ZFS 파일시스템 (Dataset)                      │ │   │
│  │                    ┌──────────────────────┐                   │ │   │
│  │                    │    zpool/filesystem   │                   │ │   │
│  │                    └──────────┬───────────┘                   │ │   │
│  │                               │                                │ │   │
│  │                    ZFS 풀 (Zpool)                               │ │   │
│  │                    ┌──────────────────────┐                   │ │   │
│  │                    │       zpool           │                   │ │   │
│  │                    └──────────┬───────────┘                   │ │   │
│  │                               │                                │ │   │
│  │                    가상 장치 (Vdev)                              │ │   │
│  │              ┌────────────────┼────────────────┐               │ │   │
│  │              │                │                │                │ │   │
│  │           ┌──┴──┐         ┌──┴──┐         ┌──┴──┐             │ │   │
│  │           │vdev1│         │vdev2│         │vdev3│             │ │   │
│  │           └──┬──┘         └──┬──┘         └──┬──┘             │ │   │
│  │              │                │                │                │ │   │
│  │           물리적             물리적            물리적             │ │   │
│  │           디스크             디스크            디스크              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ZFS 주요 기능】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  기능              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  Copy-on-Write     쓰기 시 복사, 무결성 보장                        │ │   │
│  │  RAID-Z            소프트웨어 RAID (Z1, Z2, Z3)                     │ │   │
│  │  스냅샷            특정 시점 복사본                                 │ │   │
│  │  클론              스냅샷 기반 쓰기 가능 복사본                        │ │   │
│  │  압축              투명 압축 (lz4, gzip, zstd)                      │ │   │
│  │  중복 제거          Deduplication                                 │ │   │
│  │  ARC              적응적 읽기 캐시 (RAM)                           │ │   │
│  │  L2ARC            2차 캐시 (SSD)                                  │ │   │
│  │  ZIL              쓰기 로그 (SLOG)                                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【RAID-Z 레벨】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  레벨        최소 디스크    보호            특징                   │ │   │
│  │  ────        ─────────    ────            ────                   │ │   │
│  │  RAID-Z1     3            1디스크          단일 패리티             │ │   │
│  │  RAID-Z2     4            2디스크          이중 패리티             │ │   │
│  │  RAID-Z3     5            3디스크          삼중 패리티             │ │   │
│  │  Mirror      2            1디스크          미러링                  │ │   │
│  │  Stripe      1            없음            성능                    │ │   │
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
│                ZFS 상세                                              │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【데이터 무결성】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  체크섬:                                                         │ │   │
│  │  • 모든 블록에 256비트 체크섬                                      │ │   │
│  │  • fletcher4 (기본), sha256, skein, edon-r                      │ │   │
│  │                                                             │ │   │
│  │  COW (Copy-On-Write):                                            │ │   │
│  │  • 기존 데이터 덮어쓰지 않음                                        │ │   │
│  │  • 새 블록에 쓰고 포인터 갱신                                       │ │   │
│  │  • 트랜잭션 원자성 보장                                            │ │   │
│  │                                                             │ │   │
│  │  자가 치유 (Self-Healing):                                        │ │   │
│  │  • 체크섬 불일치 시 자동 복구                                       │ │   │
│  │  • 미러/패리티에서 정상 블록 복사                                    │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ARC (Adaptive Replacement Cache)】                                 │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  RAM을 사용한 읽기 캐시                                            │ │   │
│  │  ┌────────────────────────────────────────┐                   │ │   │
│  │  │                ARC                      │                   │ │   │
│  │  ├────────────────────────────────────────┤                   │ │   │
│  │  │  MFU (Most Frequently Used)            │                   │ │   │
│  │  │  MRU (Most Recently Used)              │                   │ │   │
│  │  │  Ghost MFU                             │                   │ │   │
│  │  │  Ghost MRU                             │                   │ │   │
│  │  └────────────────────────────────────────┘                   │ │   │
│  │                                                             │ │   │
│  │  L2ARC: RAM 초과 시 SSD를 2차 캐시로 사용                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【ZIL (ZFS Intent Log)】                                             │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  동기 쓰기 보장:                                                   │ │   │
│  │  • SLOG (Separate Log Device): 전용 SSD로 성능 향상              │ │   │
│  │  • 정전 시 ZIL에서 재생                                            │ │   │
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
│  【ZFS 설치】                                                         │ |
│  ──────────────────                                                │
│  // Ubuntu                                                          │
│  $ sudo apt install zfsutils-linux                                 │
│                                                                     │
│  // CentOS/RHEL                                                      │
│  $ sudo yum install zfs                                             │
│                                                                     │
│  // 확인                                                            │
│  $ zfs --version                                                    │
│  $ modprobe zfs                                                     │
│                                                                     │
│  【Zpool 생성】                                                       │
│  ──────────────────                                                │
│  // 기본 풀                                                           │
│  $ sudo zpool create mypool /dev/sdb                               │
│                                                                     │
│  // 미러                                                             │
│  $ sudo zpool create mypool mirror /dev/sdb /dev/sdc               │
│                                                                     │
│  // RAID-Z1                                                          │
│  $ sudo zpool create mypool raidz /dev/sd{b,c,d}                   │
│                                                                     │
│  // RAID-Z2                                                          │
│  $ sudo zpool create mypool raidz2 /dev/sd{b,c,d,e}                │
│                                                                     │
│  // 캐시/로그 추가                                                     │
│  $ sudo zpool create mypool raidz /dev/sd{b,c,d} \                 │
│    cache /dev/sde log /dev/sdf                                     │
│                                                                     │
│  // 풀 확인                                                          │
│  $ sudo zpool status                                                │
│  $ sudo zpool list                                                  │
│  $ sudo zpool status -v mypool                                      │
│                                                                     │
│  【ZFS 파일시스템 생성】                                               │ |
│  ──────────────────                                                │
│  // 파일시스템 생성                                                    │
│  $ sudo zfs create mypool/data                                     │
│  $ sudo zfs create mypool/home                                     │
│                                                                     │
│  // 마운트 포인트 변경                                                  │
│  $ sudo zfs set mountpoint=/data mypool/data                       │
│                                                                     │
│  // 확인                                                            │
│  $ sudo zfs list                                                    │
│  $ df -h | grep zfs                                                 │
│                                                                     │
│  【ZFS 속성 설정】                                                    │ |
│  ──────────────────                                                │
│  // 압축                                                            │
│  $ sudo zfs set compression=lz4 mypool/data                        │
│  $ sudo zfs set compression=zstd mypool/data                       │
│                                                                     │
│  // 중복 제거                                                        │
│  $ sudo zfs set dedup=on mypool/data                               │
│                                                                     │
│  // 할당량                                                           │
│  $ sudo zfs set quota=100G mypool/data                             │
│  $ sudo zfs set refquota=50G mypool/data                           │
│                                                                     │
│  // 예약                                                            │
│  $ sudo zfs set reservation=10G mypool/data                        │
│                                                                     │
│  // atime 비활성화                                                    │
│  $ sudo zfs set atime=off mypool/data                              │
│                                                                     │
│  // 속성 확인                                                        │
│  $ sudo zfs get all mypool/data                                    │
│  $ sudo zfs get compression,quota mypool/data                      │
│                                                                     │
│  【스냅샷/클론】                                                       │ |
│  ──────────────────                                                │
│  // 스냅샷 생성                                                        │
│  $ sudo zfs snapshot mypool/data@backup_$(date +%F)                │
│                                                                     │
│  // 스냅샷 목록                                                        │
│  $ sudo zfs list -t snapshot                                        │
│                                                                     │
│  // 스냅샷 롤백                                                        │
│  $ sudo zfs rollback mypool/data@backup_20240115                   │
│                                                                     │
│  // 스냅샷 복구 (다른 위치)                                             │
│  $ sudo zfs send mypool/data@backup_20240115 | \                   │
│    sudo zfs receive mypool/restore                                 │
│                                                                     │
│  // 원격 복제                                                          │
│  $ sudo zfs send mypool/data@backup | \                            │
│    ssh user@backup zfs receive backuppool/data                     │
│                                                                     │
│  // 클론 생성                                                         │
│  $ sudo zfs clone mypool/data@backup mypool/clone                  │
│                                                                     │
│  // 스냅샷 삭제                                                        │
│  $ sudo zfs destroy mypool/data@backup                             │
│                                                                     │
│  【유지보수】                                                         │ |
│  ──────────────────                                                │
│  // 스크럽 (데이터 무결성 검사)                                          │
│  $ sudo zpool scrub mypool                                         │
│  $ sudo zpool status               // 진행 상황 확인                  │
│                                                                     │
│  // 디스크 교체                                                        │
│  $ sudo zpool replace mypool /dev/sdb /dev/sde                     │
│                                                                     │
│  // 디스크 추가                                                        │
│  $ sudo zpool add mypool /dev/sde                                  │
│                                                                     │
│  // 확장 (RAID-Z 확장은 복잡함)                                        │
│  $ sudo zpool add mypool raidz /dev/sd{e,f,g}                      │
│                                                                     │
│  // 내보내기/가져오기                                                   │
│  $ sudo zpool export mypool                                        │
│  $ sudo zpool import mypool                                        │
│  $ sudo zpool import -d /dev/disk/by-id                            │
│                                                                     │
│  // 이력 확인                                                          │
│  $ sudo zpool history mypool                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: Sun 개발 128비트 통합 파일시스템
• 구조: zpool → vdev → 파일시스템
• RAID-Z: Z1(1디스크), Z2(2), Z3(3) 보호
• COW: 쓰기 시 복사, 무결성 보장
• 체크섬: 256비트, 자가 치유
• ARC: RAM 읽기 캐시
• L2ARC: SSD 2차 캐시
• ZIL/SLOG: 쓰기 로그
• 스냅샷: zfs snapshot
• 클론: zfs clone
• 압축: compression=lz4, zstd
• 중복 제거: dedup=on
• 복제: zfs send | zfs receive
• 스크럽: zpool scrub
• 생성: zpool create
• 확인: zpool status, zfs list
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [파일 시스템](./575_file_system.md) → ZFS의 상위 개념
- [RAID](./584_raid.md) → RAID-Z
- [백업](./590_backup.md) → ZFS 스냅샷

### 👶 어린이를 위한 3줄 비유 설명
**개념**: ZFS는 "종합 저장소 관리 시스템" 같아요!

**원리**: 모든 기능이 하나로 통합되어 있어요!

**효과**: 데이터를 안전하고 효율적으로 관리해요!
