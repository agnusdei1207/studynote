+++
weight = 659
title = "659. 파일 시스템(File System) 아키텍처 비교 요약"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "File System", "Inode", "FAT", "NTFS", "VFS"]
+++

> **[Insight]**
> 파일 시스템(File System)은 비휘발성 저장 장치(Storage)에 데이터를 논리적인 구조로 조직화하여 저장, 검색, 갱신하는 운영체제의 핵심 서비스이다.
> 각 파일 시스템 아키텍처는 공간 효율성, 접근 속도, 안정성(복구 성능) 측면에서 서로 다른 설계 철학을 가지고 발달해 왔다.
> 현대 OS는 VFS(Virtual File System)를 통해 서로 다른 파일 시스템을 단일한 인터페이스로 통합 관리하며, 저널링(Journaling) 등의 기술을 통해 데이터 무결성을 보장한다.

---

### Ⅰ. 파일 시스템의 계층적 구조와 추상화

1. VFS (Virtual File System)
   - 서로 다른 하위 파일 시스템(FAT, NTFS, ext4 등)에 대해 통일된 API(Open, Read, Write)를 제공한다.
2. 파일 시스템의 주요 역할
   - **저장소 관리**: 빈 블록 관리 및 할당.
   - **네이밍 서비스**: 계층적 디렉토리 구조 제공.
   - **무결성 유지**: 시스템 충돌 시 복구 메커니즘 제공.

📢 섹션 요약 비유: VFS는 '어떤 종류의 식재료(File System)'든 똑같이 생긴 '칼과 도마(API)'로 손질할 수 있게 해주는 주방의 표준화된 작업 환경과 같습니다.

---

### Ⅱ. 파일 할당 및 인덱싱 아키텍처

1. 할당 방식 비교 다이어그램
   - 연속, 연결, 인덱스 할당의 차이를 보여준다.

```text
[ File Allocation Strategies ]

 Continuous      Linked           Indexed (Inode)
 +---+---+---+   +---+    +---+   +-------------+
 | 1 | 2 | 3 |   | 1 |--->| 2 |   | Index Block |
 +---+---+---+   +---+    +---+   +-------------+
 (Fast Seek)     (Internal Frag)  | 1 | 2 | 3 | |
 (External Frag) (No External)    +-------------+
```

2. FAT (File Allocation Table)
   - 각 블록의 다음 블록 위치를 하나의 거대한 테이블(FAT)에서 관리한다. 단순하지만 테이블이 손상되면 전체 데이터가 위험해진다.
3. Inode (Index-node) 기반
   - 유닉스 계열에서 사용하며, 파일의 메타데이터와 데이터 블록의 포인터 리스트를 독립적인 노드에 저장한다 (다중 인덱스 구조).

📢 섹션 요약 비유: FAT는 책 맨 뒤의 '찾아보기 표'와 같고, Inode는 각 단원 첫 페이지에 있는 '세부 목차'와 같습니다.

---

### Ⅲ. 주요 파일 시스템 비교 분석

1. 특징 요약표

```text
 System | Developer | Max File Size | Journaling | Recovery | Key Features
--------|-----------|---------------|------------|----------|--------------
 FAT32  | Microsoft | 4GB           | No         | Weak     | Compatibility
 NTFS   | Microsoft | 16EB          | Yes        | Strong   | Permissions
 ext4   | Linux     | 16TB          | Yes        | Excellent| Performance
 APFS   | Apple     | 8EB           | No (COW)   | High     | Snapshot, Space
```

2. NTFS (New Technology File System)
   - MFT(Master File Table)를 통한 정교한 관리, 보안 권한 부여, 압축 기능을 제공한다.
3. APFS (Apple File System)
   - 스냅샷(Snapshot)과 복제(Cloning)에 최적화된 COW(Copy-on-Write) 메커니즘을 사용한다.

📢 섹션 요약 비유: FAT32는 누구나 쓸 수 있는 '종이 메모장'이고, NTFS는 비밀번호와 일기가 적힌 '전자 수첩'과 같습니다.

---

### Ⅳ. 디스크 공간 관리 및 무결성 보장

1. 프리 블록 관리 (Free-Space Management)
   - 비트맵(Bitmap) 또는 연결 리스트(Linked List)를 사용하여 비어있는 디스크 블록을 추적한다.
2. 저널링 (Journaling)
   - 데이터를 실제로 기록하기 전에 메타데이터 변경 사항을 로그(Journal)에 먼저 기록하여, 시스템 중단 시 빠른 복구를 가능하게 한다.
3. 마운트 (Mounting)
   - 별개의 파일 시스템을 기존 디렉토리 트리의 특정 위치에 연결하여 하나의 시스템처럼 보이게 한다.

📢 섹션 요약 비유: 요리하기 전에 '오늘 할 일 목록(Journal)'을 미리 적어두면, 갑자기 정전이 되어도 어디까지 했는지 바로 알 수 있는 것과 같습니다.

---

### Ⅴ. 파일 시스템 성능 최적화 기술

1. 버퍼 캐시(Buffer Cache) / 페이지 캐시(Page Cache)
   - 자주 사용하는 디스크 블록을 메모리에 상주시킨다.
2. 디스크 스케줄링(Disk Scheduling)
   - 암(Arm)의 이동을 최소화하도록 요청 순서를 재조정한다 (SCAN, C-SCAN 등).
3. RAID (Redundant Array of Independent Disks)
   - 여러 개의 디스크를 묶어 성능 향상(Stripping) 또는 신뢰성 확보(Mirroring)를 달성한다.

📢 섹션 요약 비유: 자주 쓰는 양념을 조리대 위에 꺼내두는 것(Cache)이 창고에 매번 가는 것보다 훨씬 빠른 것과 같습니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 입출력 시스템(OS I/O System)
- **자식 노드**: FAT, NTFS, ext4, Inode, VFS, Journaling
- **연관 키워드**: Block, Metadata, Fragmentation, RAID, Buffer Cache, Snapshot

### 👶 어린아이에게 설명하기
"네 방에 장난감이 아주 많지? 어떤 장난감은 서랍에 있고, 어떤 건 상자에 들어있을 거야. '파일 시스템'은 이 장난감들이 어디에 있는지 알려주는 '이름표'와 '지도' 같은 거야. 지도가 잘 그려져 있어야 네가 놀고 싶을 때 장난감을 금방 찾을 수 있고, 정리도 깨끗하게 할 수 있단다!"