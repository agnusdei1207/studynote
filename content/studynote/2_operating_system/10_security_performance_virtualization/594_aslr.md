+++
title = "594. 가상 주소 공간 구조 무작위화 (ASLR) - 버퍼/스택 라이브러리 주소 랜덤 배치 방어망"
weight = 594
+++

# 594. CIFS/SMB (Common Internet File System / Server Message Block)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 윈도우 파일 공유 프로토콜
> 2. **가치**: 이기종 파일 공유, 프린터 공유
> 3. **융합**: Samba, Active Directory, 인증과 연관

---

## Ⅰ. 개요

### 개념 정의
**CIFS/SMB**는 **윈도우 네트워크에서 파일과 프린터를 공유하는 프로토콜**입니다.

### 💡 비유: 윈도우 네트워크 폴더
CIFS/SMB는 **윈도우 네트워크 폴더**와 같습니다. 다른 컴퓨터의 폴더를 내 컴퓨터처럼 씁니다.

### CIFS/SMB 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                CIFS/SMB 구조                                         │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【SMB 버전】                                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  버전            별칭           특징                           │ │   │
│  │  ────            ────           ────                           │ │   │
│  │  SMB 1.0        CIFS           레거시, 보안 취약                 │ │   │
│  │  SMB 2.0        -              성능 향상 (Vista)                 │ │   │
│  │  SMB 2.1        -              Win7/2008 R2                     │ │   │
│  │  SMB 3.0        -              Win8/2012, 암호화                 │ │   │
│  │  SMB 3.0.2      -              Win8.1/2012 R2                   │ │   │
│  │  SMB 3.1.1      -              Win10/2016, 최신                  │ │   │
│  │                                                             │ │   │
│  │  권장: SMB 3.x (보안, 성능)                                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【SMB 포트】                                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  포트              용도                                           │ │   │
│  │  ────              ────                                           │ │   │
│  │  139              NetBIOS Session Service                        │ │   │
│  │  445              SMB over TCP (Direct Hosting)                  │ │   │
│  │  137/UDP          NetBIOS Name Service                           │ │   │
│  │  138/UDP          NetBIOS Datagram Service                       │ │   │
│  │                                                             │ │   │
│  │  현대 SMB: 포트 445 주로 사용                                      │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Samba 구성 요소】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  데몬              역할                                           │ │   │
│  │  ────              ────                                           │ │   │
│  │  smbd             파일/프린터 공유, 인증                          │ │   │
│  │  nmbd             NetBIOS 이름 서비스                            │ │   │
│  │  winbindd         Windows 도메인 통합                            │ │   │
│  │                                                             │ │   │
│  │  주요 설정 파일: /etc/samba/smb.conf                              │ │   │
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
│                CIFS/SMB 상세                                         │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【smb.conf 구조】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  [global]                  # 전역 설정                           │ │   │
│  │  workgroup = WORKGROUP                                          │ │   │
│  │  server string = Samba Server                                   │ │   │
│  │  security = user                                                │ │   │
│  │                                                             │ │   │
│  │  [share]                   # 공유 정의                            │ │   │
│  │  path = /export/share                                           │ │   │
│  │  browseable = yes                                               │ │   │
│  │  read only = no                                                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 공유 옵션】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  옵션              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  path             공유 경로                                      │ │   │
│  │  browseable       네트워크에서 보이기                              │ │   │
│  │  read only        읽기 전용                                       │ │   │
│  │  writable         쓰기 허용                                       │ │   │
│  │  guest ok         게스트 접근 허용                                │ │   │
│  │  valid users      접근 허용 사용자                                 │ │   │
│  │  write list       쓰기 권한 사용자                                 │ │   │
│  │  create mask      파일 생성 권한                                  │ │   │
│  │  directory mask   디렉토리 생성 권한                               │ │   │
│  │  force user       강제 사용자                                      │ │   │
│  │  force group      강제 그룹                                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【보안 모드】                                                         │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  security = user      # 로컬 사용자 인증                          │ │   │
│  │  security = domain    # 도메인 컨트롤러 인증                       │ │   │
│  │  security = ads       # Active Directory 인증                    │ │   │
│  │  security = share     # 공유 레벨 인증 (레거시)                     │ │   │
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
│  【Samba 서버 설치】                                                  │ |
│  ──────────────────                                                │
│  // Ubuntu/Debian                                                    │
│  $ sudo apt install samba samba-common-bin                         │
│                                                                     │
│  // CentOS/RHEL                                                      │
│  $ sudo yum install samba samba-client                             │
│                                                                     │
│  // 서비스 시작                                                        │
│  $ sudo systemctl start smbd nmbd                                   │
│  $ sudo systemctl enable smbd nmbd                                  │
│                                                                     │
│  【Samba 사용자 관리】                                                 │ |
│  ──────────────────                                                │
│  // Samba 사용자 추가                                                  │
│  $ sudo smbpasswd -a username                                      │
│                                                                     │
│  // 비밀번호 변경                                                      │
│  $ sudo smbpasswd username                                          │
│                                                                     │
│  // 사용자 활성화/비활성화                                               │
│  $ sudo smbpasswd -e username                                       │
│  $ sudo smbpasswd -d username                                       │
│                                                                     │
│  // 사용자 목록                                                        │
│  $ sudo pdbedit -L                                                  │
│  $ sudo pdbedit -Lv                  // 상세                        │
│                                                                     │
│  【smb.conf 예시】                                                    │ |
│  ──────────────────                                                │
│  [global]                                                            │
│     workgroup = WORKGROUP                                           │
│     server string = Samba Server %v                                 │
│     security = user                                                 │
│     map to guest = bad user                                         │
│     dns proxy = no                                                  │
│                                                                     │
│  [public]                                                            │
│     path = /srv/samba/public                                        │
│     browseable = yes                                                │
│     read only = no                                                  │
│     guest ok = yes                                                  │
│     create mask = 0644                                              │
│     directory mask = 0755                                           │
│                                                                     │
│  [private]                                                           │
│     path = /srv/samba/private                                       │
│     browseable = no                                                 │
│     read only = no                                                  │
│     valid users = @smbgroup                                         │
│     create mask = 0660                                              │
│     directory mask = 0770                                           │
│                                                                     │
│  [homes]                                                             │
│     comment = Home Directories                                      │
│     browseable = no                                                 │
│     read only = no                                                  │
│     create mask = 0700                                              │
│     directory mask = 0700                                           │
│                                                                     │
│  // 설정 확인                                                         │
│  $ sudo testparm                                                    │
│                                                                     │
│  // 설정 적용                                                         │
│  $ sudo systemctl reload smbd                                       │
│                                                                     │
│  【Linux에서 SMB 마운트】                                              │ |
│  ──────────────────                                                │
│  // 패키지 설치                                                       │
│  $ sudo apt install cifs-utils                                     │
│                                                                     │
│  // 마운트                                                           │
│  $ sudo mount -t cifs //server/share /mnt/smb \                    │
│    -o username=user,password=pass                                  │
│                                                                     │
│  // 자격 증명 파일 사용                                                 │
│  $ sudo mount -t cifs //server/share /mnt/smb \                    │
│    -o credentials=/etc/smb.creds                                   │
│                                                                     │
│  // /etc/smb.creds                                                   │
│  username=user                                                      │
│  password=pass                                                      │
│  domain=WORKGROUP                                                   │
│  $ sudo chmod 600 /etc/smb.creds                                    │
│                                                                     │
│  // /etc/fstab                                                       │
│  //server/share  /mnt/smb  cifs  credentials=/etc/smb.creds,_netdev  0 0│
│                                                                     │
│  // 마운트 옵션                                                        │
│  $ sudo mount -t cifs //server/share /mnt/smb \                    │
│    -o username=user,uid=1000,gid=1000,vers=3.0                     │
│                                                                     │
│  【Windows에서 접근】                                                 │ |
│  ──────────────────                                                │
│  // 탐색기                                                            │
│  \\server\share                                                     │
│                                                                     │
│  // 네트워크 드라이브 연결                                               │
│  net use Z: \\server\share /user:username password                 │
│  net use Z: /delete                                                 │
│                                                                     │
│  // PowerShell                                                       │
│  New-SmbMapping -LocalPath Z: -RemotePath \\server\share           │
│  Remove-SmbMapping -LocalPath Z:                                   │
│                                                                     │
│  【Samba 관리 명령어】                                                 │ |
│  ──────────────────                                                │
│  // 연결 상태                                                         │
│  $ sudo smbstatus                                                   │
│  $ sudo smbstatus -b                 // 간단                        │
│  $ sudo smbstatus -u username        // 사용자별                     │
│                                                                     │
│  // 공유 목록 확인                                                      │
│  $ smbclient -L localhost -U username                              │
│  $ smbclient -L server -N            // 익명                        │
│                                                                     │
│  // smbclient로 접속                                                  │
│  $ smbclient //server/share -U username                            │
│  smb: \> ls                                                         │
│  smb: \> get file.txt                                               │
│  smb: \> put file.txt                                               │
│  smb: \> quit                                                       │
│                                                                     │
│  // nmblookup                                                        │
│  $ nmblookup -A 192.168.1.10                                        │
│  $ nmblookup server                                                  │
│                                                                     │
│  // 방화벽 설정                                                        │
│  $ sudo firewall-cmd --permanent --add-service=samba               │
│  $ sudo firewall-cmd --reload                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 윈도우 파일/프린터 공유 프로토콜
• 버전: SMB 1.0~3.1.1 (3.x 권장)
• 포트: 139 (NetBIOS), 445 (Direct)
• Samba: Linux SMB 서버 구현
• 데몬: smbd, nmbd, winbindd
• 설정: /etc/samba/smb.conf
• 사용자: smbpasswd -a
• 확인: testparm, smbstatus
• 클라이언트: smbclient, mount -t cifs
• 마운트: cifs-utils 패키지
• fstab: credentials 파일 사용
• 보안: security=user, valid users
• 게스트: guest ok = yes
• 권한: create mask, directory mask
• Windows: \\server\share
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [NFS](./593_nfs.md) → Unix/Linux 파일 공유
- [마운트](./580_mount.md) → CIFS 마운트
- [fstab](./582_fstab.md) → 영구 마운트

### 👶 어린이를 위한 3줄 비유 설명
**개념**: CIFS/SMB는 "윈도우 네트워크 폴더" 같아요!

**원리**: 다른 컴퓨터의 폴더를 내 컴퓨터처럼 써요!

**효과**: 윈도우와 리눅스가 파일을 공유해요!
