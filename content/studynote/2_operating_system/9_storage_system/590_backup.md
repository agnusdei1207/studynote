+++
title = "590. 백업"
weight = 590
+++

# 590. 백업 (Backup)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터를 복사하여 보관
> 2. **가치**: 데이터 손실 방지, 재해 복구
> 3. **융합**: 전체/증분/차등 백업, 압축과 연관

---

## Ⅰ. 개요

### 개념 정의
**백업(Backup)**은 **원본 데이터 손실 시 복구를 위해 데이터를 복사하여 보관하는 작업**입니다.

### 💡 비유: 복사본 만들기
백업은 **복사본 만들기**와 같습니다. 중요한 문서의 사본을 따로 보관합니다.

### 백업 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                백업 종류                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【백업 유형】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  유형              설명                    장점          단점          │ │   │
│  │  ────              ────                    ────          ────          │ │   │
│  │  전체 백업          모든 데이터              복구 쉬움     시간/공간      │ │   │
│  │                  (Full Backup)                                         │ │   │
│  │                                                             │ │   │
│  │  증분 백업          마지막 백업 후           빠름, 작음    복구 복잡      │ │   │
│  │                  변경분만 (Incremental)                                  │ │   │
│  │                                                             │ │   │
│  │  차등 백업          마지막 전체 백업          중간          중간          │ │   │
│  │                  후 변경분 (Differential)                                │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【백업 전략 예시】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  일    월    화    수    목    금    토                         │ │   │
│  │  ───  ───  ───  ───  ───  ───  ───                             │ │   │
│  │  전체  증분  증분  증분  증분  증분  전체                         │ │   │
│  │   F    I    I    I    I    I     F                             │ │   │
│  │                                                             │ │   │
│  │  복구 순서:                                                       │ │   │
│  │  화요일 복구: F(일) → I(월) → I(화)                               │ │   │
│  │                                                             │ │   │
│  │  GFS (Grandfather-Father-Son) 회전:                              │ │   │
│  │  • 일일 백업: Son (토요일까지)                                     │ │   │
│  │  • 주간 백업: Father (4주까지)                                     │ │   │
│  │  • 월간 백업: Grandfather (1년까지)                                │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【백업 레벨 (dump/restore)】                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  레벨    설명                                                      │ │   │
│  │  ────    ────                                                      │ │   │
│  │  0       전체 백업                                                 │ │   │
│  │  1       레벨 0 이후 변경분                                         │ │   │
│  │  2       레벨 1 이후 변경분                                         │ │   │
│  │  ...                                                              │ │   │
│  │  9       레벨 8 이후 변경분                                         │ │   │
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
│                백업 상세                                              │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【백업 대상】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  시스템 파일:                                                     │ │   │
│  │  • /etc/          설정 파일                                       │ │   │
│  │  • /var/          로그, 데이터                                     │ │   │
│  │  • /home/         사용자 데이터                                    │ │   │
│  │  • /root/         root 홈                                         │ │   │
│  │  • /usr/local/    로컬 설치                                       │ │   │
│  │                                                             │ │   │
│  │  데이터베이스:                                                      │ │   │
│  │  • mysqldump, pg_dump                                            │ │   │
│  │  • mongoexport, redis-cli --rdb                                  │ │   │
│  │                                                             │ │   │
│  │  제외 권장:                                                        │ │   │
│  │  • /proc, /sys, /dev (가상 파일시스템)                              │ │   │
│  │  • /tmp, /var/tmp (임시 파일)                                      │ │   │
│  │  • /var/cache (캐시)                                              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【백업 저장 매체】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  매체              장점              단점            용도             │ │   │
│  │  ────              ────              ────            ────             │ │   │
│  │  로컬 디스크         빠름              같은 장애        단기            │ │   │
│  │  외장 HDD/SSD        휴대성            분실 위험        이동            │ │   │
│  │  NAS                네트워크           비용            소규모           │ │   │
│  │  테이프              저렴, 장기          느림            대량/장기        │ │   │
│  │  클라우드           异地 보관           비용, 속도      재해 복구        │ │   │
│  │  (AWS S3, etc.)                                                    │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【3-2-1 백업 규칙】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  3: 데이터 사본 3개 유지 (원본 포함)                                │ │   │
│  │  2: 서로 다른 저장 매체 2종류 사용                                  │ │   │
│  │  1: 1개는 오프사이트(异地) 보관                                      │ │   │
│  │                                                             │ │   │
│  │  예시:                                                           │ │   │
│  │  1. 원본 (서버 내부)                                               │ │   │
│  │  2. 로컬 백업 (외장 HDD)                                           │ │   │
│  │  3. 원격 백업 (클라우드)                                            │ │   │
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
│  【tar 백업】                                                         │
│  ──────────────────                                                │
│  // 전체 백업                                                         │
│  $ tar -czvf backup_$(date +%Y%m%d).tar.gz /home /etc /var         │
│                                                                     │
│  // 증분 백업 (--listed-incremental)                                  │
│  $ tar --listed-incremental=backup.snar -czvf backup_full.tar.gz /data│
│  $ tar --listed-incremental=backup.snar -czvf backup_inc1.tar.gz /data│
│  $ tar --listed-incremental=backup.snar -czvf backup_inc2.tar.gz /data│
│                                                                     │
│  // 복원                                                             │
│  $ tar -xzvf backup_full.tar.gz                                     │
│  $ tar --listed-incremental=backup.snar -xzvf backup_inc1.tar.gz   │
│                                                                     │
│  【rsync 백업】                                                       │
│  ──────────────────                                                │
│  // 기본 동기화                                                        │
│  $ rsync -avz /data/ /backup/                                       │
│                                                                     │
│  // 원격 백업                                                         │
│  $ rsync -avz -e ssh /data/ user@backup-server:/backup/            │
│                                                                     │
│  // 증분 백업 (--link-dest)                                           │
│  $ rsync -avz --link-dest=/backup/current /data/ /backup/$(date +%F)│
│                                                                     │
│  // 삭제된 파일 동기화                                                  │
│  $ rsync -avz --delete /data/ /backup/                              │
│                                                                     │
│  // 제외 패턴                                                         │
│  $ rsync -avz --exclude '*.log' --exclude 'tmp/' /data/ /backup/   │
│                                                                     │
│  // Dry run                                                          │
│  $ rsync -avzn /data/ /backup/                                      │
│                                                                     │
│  【dd 백업 (이미지)】                                                  │ |
│  ──────────────────                                                │
│  // 디스크 이미지 생성                                                  │
│  $ sudo dd if=/dev/sda of=/backup/disk.img bs=4M status=progress   │
│                                                                     │
│  // 압축과 함께                                                        │
│  $ sudo dd if=/dev/sda | gzip > /backup/disk.img.gz                │
│                                                                     │
│  // 복원                                                             │
│  $ sudo dd if=/backup/disk.img of=/dev/sda bs=4M                   │
│  $ gunzip -c /backup/disk.img.gz | sudo dd of=/dev/sda             │
│                                                                     │
│  // 파티션 백업                                                        │
│  $ sudo dd if=/dev/sda1 of=/backup/partition.img bs=4M             │
│                                                                     │
│  【dump/restore】                                                    │ |
│  ──────────────────                                                │
│  // 전체 백업 (레벨 0)                                                 │
│  $ sudo dump -0uf /backup/full.dump /dev/sda1                       │
│                                                                     │
│  // 증분 백업 (레벨 1)                                                 │
│  $ sudo dump -1uf /backup/inc1.dump /dev/sda1                       │
│                                                                     │
│  // 복원                                                             │
│  $ sudo restore -rf /backup/full.dump                               │
│  $ sudo restore -rf /backup/inc1.dump                               │
│                                                                     │
│  // 대화형 복원                                                        │
│  $ sudo restore -if /backup/full.dump                               │
│                                                                     │
│  【데이터베이스 백업】                                                  │ |
│  ──────────────────                                                │
│  // MySQL                                                            │
│  $ mysqldump -u root -p --all-databases > all_db.sql               │
│  $ mysqldump -u root -p mydb > mydb.sql                            │
│  $ mysqldump -u root -p --single-transaction --routines mydb > backup.sql│
│                                                                     │
│  // PostgreSQL                                                       │
│  $ pg_dump -U postgres mydb > mydb.sql                              │
│  $ pg_dumpall -U postgres > all_db.sql                              │
│  $ pg_dump -U postgres -Fc mydb > mydb.dump                         │
│                                                                     │
│  // Redis                                                            │
│  $ redis-cli BGSAVE                                                  │
│  $ cp /var/lib/redis/dump.rdb /backup/redis_$(date +%F).rdb        │
│                                                                     │
│  // MongoDB                                                          │
│  $ mongodump --out /backup/mongodb_$(date +%F)                     │
│  $ mongodump --db mydb --out /backup/mydb                          │
│                                                                     │
│  【자동 백업 스크립트】                                                 │ |
│  ──────────────────                                                │
│  // /etc/cron.daily/backup                                           │
│  #!/bin/bash                                                         │
│  DATE=$(date +%Y%m%d)                                               │
│  BACKUP_DIR="/backup"                                               │
│  SRC_DIR="/data"                                                     │
│                                                                     │
│  # 전체 백업 (일요일)                                                   │
│  if [ $(date +%u) -eq 7 ]; then                                      │
│    tar -czvf $BACKUP_DIR/full_$DATE.tar.gz $SRC_DIR                 │
│  else                                                                │
│    # 증분 백업                                                         │
│    tar -czvf $BACKUP_DIR/inc_$DATE.tar.gz $SRC_DIR                  │
│  fi                                                                  │
│                                                                     │
│  # 30일 이상 된 백업 삭제                                               │
│  find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete               │
│                                                                     │
│  【클라우드 백업】                                                      │ |
│  ──────────────────                                                │
│  // AWS S3                                                           │
│  $ aws s3 sync /data s3://mybucket/backup/                          │
│  $ aws s3 cp backup.tar.gz s3://mybucket/backup/                    │
│                                                                     │
│  // rclone (범용)                                                      │
│  $ rclone sync /data remote:backup                                  │
│  $ rclone copy backup.tar.gz remote:backup/                         │
│                                                                     │
│  // restic (중복 제거)                                                 │
│  $ restic init -r /backup/repo                                      │
│  $ restic backup /data -r /backup/repo                              │
│  $ restic restore latest -r /backup/repo -t /restore               │
│                                                                     │
│  // borgbackup                                                       │
│  $ borg init /backup/repo                                           │
│  $ borg create /backup/repo::backup_$(date +%F) /data               │
│  $ borg extract /backup/repo::backup_20240115                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 데이터 복사하여 보관
• 전체 백업: 모든 데이터, 복구 쉬움
• 증분 백업: 마지막 백업 후 변경분, 작음
• 차등 백업: 마지막 전체 백업 후 변경분
• 3-2-1 규칙: 3개 사본, 2종 매체, 1개 오프사이트
• tar: 파일 백업, 증분 가능
• rsync: 동기화, --link-dest 증분
• dd: 디스크 이미지
• dump/restore: 파일시스템 레벨
• DB: mysqldump, pg_dump
• 클라우드: S3, rclone, restic, borg
• 자동화: cron, systemd timer
• 검증: 주기적 복구 테스트 필수
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [파일 시스템](./575_file_system.md) → 백업 대상
- [압축](../4_file_io/231_compression.md) → 백업 압축
- [RAID](./584_raid.md) → RAID는 백업이 아님

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 백업은 "복사본 만들기" 같아요!

**원리**: 중요한 문서의 사본을 따로 보관해요!

**효과**: 잃어버려도 다시 찾을 수 있어요!
