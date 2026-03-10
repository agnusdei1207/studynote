+++
title = "595. 카나리 (Canary) / 스택 스매싱 가드 (Stack Smashing Protector) - 컴파일러 수준 버퍼 변조 탐지"
weight = 595
+++

# 595. iSCSI (Internet Small Computer System Interface)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IP 네트워크를 통한 SCSI 블록 전송
> 2. **가치**: SAN 구축, 원격 블록 스토리지
> 3. **융합**: Target, Initiator, LUN과 연관

---

## Ⅰ. 개요

### 개념 정의
**iSCSI**는 **IP 네트워크를 통해 SCSI 명령을 전송하여 블록 스토리지에 접근하는 프로토콜**입니다.

### 💡 비유: 네트워크 하드디스크
iSCSI는 **네트워크 하드디스크**와 같습니다. 멀리 있는 디스크를 내 컴퓨터에 직접 연결합니다.

### iSCSI 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                iSCSI 구조                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【iSCSI 아키텍처】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  iSCSI Initiator                  iSCSI Target               │ │   │
│  │  (클라이언트)                      (서버)                      │ │   │
│  │  ┌─────────────────┐              ┌─────────────────┐        │ │   │
│  │  │                 │              │                 │        │ │   │
│  │  │   애플리케이션    │              │   스토리지       │        │ │   │
│  │  │       │         │              │   (LUN)         │        │ │   │
│  │  │       ▼         │              │       ↑         │        │ │   │
│  │  │   파일시스템     │              │   SCSI 명령     │        │ │   │
│  │  │       │         │              │       │         │        │ │   │
│  │  │       ▼         │              │       ▼         │        │ │   │
│  │  │   iSCSI Initiator│◄───────────►│   iSCSI Target  │        │ │   │
│  │  │   (소프트웨어)    │    TCP/IP     │   (소프트웨어/   │        │ │   │
│  │  │                 │              │    하드웨어)     │        │ │   │
│  │  └─────────────────┘              └─────────────────┘        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【iSCSI 용어】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  용어              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  Initiator         iSCSI 클라이언트 (접근 요청)                    │ │   │
│  │  Target            iSCSI 서버 (스토리지 제공)                      │ │   │
│  │  LUN               Logical Unit Number (논리 단위 번호)            │ │   │
│  │  IQN               iSCSI Qualified Name (고유 식별자)              │ │   │
│  │  Portal            IP 주소 + 포트 (접속점)                         │ │   │
│  │  TPG               Target Portal Group                           │ │   │
│  │  Node              iSCSI 노드 (Initiator 또는 Target)             │ │   │
│  │  Session           Initiator-Target 간 연결                       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【IQN 형식】                                                          │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  iqn.yyyy-mm.reverse-domain:identifier                          │ │   │
│  │                                                             │ │   │
│  │  예:                                                             │ │   │
│  │  iqn.2024-01.com.example:storage.target00                       │ │   │
│  │  iqn.1994-05.com.redhat:rhel7                                   │ │   │
│  │                                                             │ │   │
│  │  포트: 기본 3260                                                   │ │   │
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
│                iSCSI 상세                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【iSCSI vs 다른 프로토콜】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  프로토콜       레벨        용도            장점/단점            │ │   │
│  │  ────────       ────        ────            ────────            │ │   │
│  │  iSCSI          블록        SAN            저렴, IP 기반          │ │   │
│  │  Fibre Channel  블록        SAN            고성능, 비쌈           │ │   │
│  │  NFS            파일        NAS            간편, 파일 단위         │ │   │
│  │  SMB/CIFS       파일        NAS            윈도우 친화적          │ │   │
│  │                                                             │ │   │
│  │  SAN (Storage Area Network): 블록 레벨 접근                      │ │   │
│  │  NAS (Network Attached Storage): 파일 레벨 접근                   │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【인증 방식】                                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  방식              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  None             인증 없음                                      │ │   │
│  │  CHAP             Challenge-Handshake Authentication            │ │   │
│  │  Mutual CHAP      양방향 CHAP                                    │ │   │
│  │                                                             │ │   │
│  │  CHAP:                                                            │ │   │
│  │  • 사용자명/비밀번호 기반                                           │ │   │
│  │  • 비밀번호 평문 전송 안 함                                         │ │   │
│  │  • 단방향 또는 양방향                                               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【성능 고려사항】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 네트워크 대역폭: 최소 1Gbps, 권장 10Gbps                        │ │   │
│  │  • Jumbo Frame: MTU 9000으로 설정                               │ │   │
│  │  • TCP 오프로드: TOE (TCP Offload Engine)                        │ │   │
│  │  • 다중 세션: 다중 경로 I/O (MPIO)                                │ │   │
│  │  • 전용 네트워크: 스토리지 트래픽 분리                               │ │   │
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
│  【iSCSI Target 설정 (Linux)】                                        │ |
│  ──────────────────                                                │
│  // 패키지 설치                                                       │
│  $ sudo apt install targetcli-fb    // Ubuntu                      │
│  $ sudo yum install targetcli       // CentOS/RHEL                 │
│                                                                     │
│  // targetcli 실행                                                    │
│  $ sudo targetcli                                                   │
│                                                                     │
│  // 백스토어 생성 (파일)                                               │
│  /> backstores/fileio create file1 /var/lib/iscsi/file1.img 10G    │
│                                                                     │
│  // 백스토어 생성 (블록 장치)                                           │
│  /> backstores/block create disk1 /dev/sdb1                        │
│                                                                     │
│  // Target 생성                                                       │
│  /> iscsi/ create iqn.2024-01.com.example:storage.target1          │
│                                                                     │
│  // LUN 생성                                                          │
│  /> iscsi/iqn.../tpg1/luns create /backstores/fileio/file1         │
│                                                                     │
│  // ACL 생성 (Initiator 접근 허용)                                     │
│  /> iscsi/iqn.../tpg1/acls create iqn.2024-01.com.example:init1    │
│                                                                     │
│  // 포털 생성                                                          │
│  /> iscsi/iqn.../tpg1/portals create 0.0.0.0                       │
│                                                                     │
│  // 설정 저장                                                         │
│  /> saveconfig                                                       │
│  /> exit                                                             │
│                                                                     │
│  // 서비스 시작                                                        │
│  $ sudo systemctl enable target                                    │
│  $ sudo systemctl start target                                      │
│                                                                     │
│  【iSCSI Initiator 설정 (Linux)】                                     │ |
│  ──────────────────                                                │
│  // 패키지 설치                                                       │
│  $ sudo apt install open-iscsi                                     │
│  $ sudo yum install iscsi-initiator-utils                          │
│                                                                     │
│  // Initiator 이름 설정                                                │
│  $ sudo vim /etc/iscsi/initiatorname.iscsi                         │
│  InitiatorName=iqn.2024-01.com.example:init1                       │
│                                                                     │
│  // Target 검색                                                       │
│  $ sudo iscsiadm -m discovery -t st -p 192.168.1.100               │
│  192.168.1.100:3260,1 iqn.2024-01.com.example:storage.target1      │
│                                                                     │
│  // Target 로그인                                                     │
│  $ sudo iscsiadm -m node -T iqn.2024-01.com.example:storage.target1 \│
│    -p 192.168.1.100 --login                                         │
│                                                                     │
│  // 세션 확인                                                         │
│  $ sudo iscsiadm -m session                                         │
│  $ lsblk                                                            │
│                                                                     │
│  // 파티션 생성 및 마운트                                               │
│  $ sudo fdisk /dev/sdb                                              │
│  $ sudo mkfs.ext4 /dev/sdb1                                         │
│  $ sudo mount /dev/sdb1 /mnt/iscsi                                  │
│                                                                     │
│  // 로그아웃                                                           │
│  $ sudo iscsiadm -m node -T iqn... -p 192.168.1.100 --logout       │
│                                                                     │
│  // 노드 삭제                                                         │
│  $ sudo iscsiadm -m node -T iqn... -p 192.168.1.100 -o delete      │
│                                                                     │
│  【CHAP 인증 설정】                                                    │ |
│  ──────────────────                                                │
│  // Target 측 (targetcli)                                            │
│  /> iscsi/iqn.../tpg1/acls/iqn... set auth userid=user1            │
│  /> iscsi/iqn.../tpg1/acls/iqn... set auth password=pass123        │
│                                                                     │
│  // Initiator 측 (/etc/iscsi/iscsid.conf)                            │
│  node.session.auth.authmethod = CHAP                                │
│  node.session.auth.username = user1                                 │
│  node.session.auth.password = pass123                               │
│                                                                     │
│  【Windows iSCSI Initiator】                                         │ |
│  ──────────────────                                                │
│  // iSCSI Initiator 실행                                              │
│  > iscsicpl                                                         │
│                                                                     │
│  // Discovery 탭 → Discover Portal                                  │
│  // IP 주소 입력                                                      │
│  // Targets 탭 → Connect                                             │
│                                                                     │
│  // PowerShell                                                        │
│  > New-IscsiTargetPortal -TargetPortalAddress 192.168.1.100        │
│  > Get-IscsiTarget                                                   │
│  > Connect-IscsiTarget -NodeAddress iqn...                          │
│  > Get-IscsiSession                                                  │
│                                                                     │
│  【MPIO (다중 경로)】                                                  │ |
│  ──────────────────                                                │
│  // 패키지 설치                                                       │
│  $ sudo apt install multipath-tools                                 │
│                                                                     │
│  // /etc/multipath.conf                                               │
│  defaults {                                                          │
│    find_multipaths yes                                               │
│    user_friendly_names yes                                           │
│  }                                                                   │
│                                                                     │
│  // 서비스 시작                                                        │
│  $ sudo systemctl enable multipath-tools                            │
│  $ sudo systemctl start multipath-tools                             │
│                                                                     │
│  // 다중 경로 확인                                                      │
│  $ sudo multipath -ll                                               │
│  $ sudo multipath -v2                                               │
│                                                                     │
│  // 다중 세션 연결                                                      │
│  $ sudo iscsiadm -m node -T iqn... -p 192.168.1.100 --login        │
│  $ sudo iscsiadm -m node -T iqn... -p 192.168.1.101 --login        │
│                                                                     │
│  【문제 해결】                                                         │ |
│  ──────────────────                                                │
│  // Target 상태 확인                                                   │
│  $ sudo targetcli ls                                                 │
│  $ sudo systemctl status target                                     │
│                                                                     │
│  // 세션 상태                                                          │
│  $ sudo iscsiadm -m session -P 3                                   │
│                                                                     │
│  // 로그 확인                                                          │
│  $ journalctl -u iscsid -f                                          │
│  $ dmesg | grep -i scsi                                             │
│                                                                     │
│  // 방화벽                                                             │
│  $ sudo firewall-cmd --add-port=3260/tcp --permanent               │
│  $ sudo firewall-cmd --reload                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: IP 네트워크를 통한 SCSI 블록 전송
• Initiator: iSCSI 클라이언트
• Target: iSCSI 서버 (스토리지 제공)
• LUN: Logical Unit Number
• IQN: iSCSI Qualified Name
• 포트: 3260 (기본)
• 인증: None, CHAP, Mutual CHAP
• Target 도구: targetcli
• Initiator 도구: open-iscsi, iscsi-initiator-utils
• 검색: iscsiadm -m discovery
• 로그인: iscsiadm -m node --login
• 로그아웃: iscsiadm -m node --logout
• SAN: 블록 레벨 스토리지 네트워크
• MPIO: 다중 경로 I/O
• 성능: 10Gbps+, Jumbo Frame
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [NFS](./593_nfs.md) → 파일 레벨 공유
- [LVM](./587_lvm.md) → iSCSI 위에 LVM 구성
- [RAID](./584_raid.md) → iSCSI 스토리지 RAID

### 👶 어린이를 위한 3줄 비유 설명
**개념**: iSCSI는 "네트워크 하드디스크" 같아요!

**원리**: 멀리 있는 디스크를 내 컴퓨터에 직접 연결해요!

**효과**: 네트워크로 대용량 스토리지를 써요!
