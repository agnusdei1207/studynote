+++
title = "649. 기술사 기출 키워드 맵 - 운영체제 편"
date = "2024-05-23"
weight = 649
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "기출 키워드", "Keyword Map", "기술사 시험", "Exam Summary"]
+++

> **[Insight]**
> 정보관리/컴퓨터시스템응용 기술사 시험에서 운영체제는 컴퓨터 아키텍처와 소프트웨어 공학을 잇는 가장 기초적이면서도 변별력이 큰 과목이다.
> 단순 개념 나열을 넘어 각 기술의 등장 배경, 장단점, 트레이드오프 관계를 명확히 기술하는 것이 고득점의 비결이며, 특히 최신 IT 트렌드인 클라우드, 가상화와의 연계가 필수적이다.
> 본 키워드 맵은 빈출 토픽을 5대 영역으로 구조화하여 실전 시험 직전 핵심 개념을 빠르게 리마인드할 수 있도록 설계되었다.

+++

### Ⅰ. 프로세스 및 스레드 관리 (Core Layer)

1. 핵심 기출 키워드
   - **Process State**: 상태 전이도(Transition Diagram), 5단계 상태.
   - **PCB/TCB**: 구성 요소 및 관리 메커니즘.
   - **Context Switching**: 오버헤드 원인 및 해결 방안.
   - **IPC**: Message Passing, Shared Memory, Socket, Pipe.
   - **Multi-threading**: 장단점, 스레드 모델(M:1, 1:1, M:M), Thread Safe, Reentrant Code.

📢 섹션 요약 비유: 컴퓨터라는 도시의 '인구(Process)'와 그들이 '이동하는 수단(Context Switching/IPC)'을 관리하는 기본 규칙들입니다.

+++

### Ⅱ. CPU 스케줄링 및 동기화 (Decision Layer)

1. 핵심 기출 키워드
   - **Scheduling Algorithms**: FCFS, SJF, RR, MLQ, MLFQ, HRN, RMS, EDF.
   - **Priority Inversion**: 우선순위 역전 현상과 해결책(PIP, PCP).
   - **Critical Section Problem**: 3대 조건, Mutex, Semaphore, Monitor.
   - **Deadlock**: 4대 발생 조건, 해결 전략(예방, 회피-Banker's, 탐지, 복구).
   - **Liveness Problem**: Livelock, Starvation.

```text
[ Scheduling Complexity Map ]

   Simple <----------------------------> Sophisticated
    FCFS     RR     SJF     MLFQ     Real-time (EDF)
```

📢 섹션 요약 비유: 도시의 '교통 신호 체계(Scheduling)'와 좁은 길에서의 '양보 규칙(Synchronization)'을 정의하는 의사결정 체계입니다.

+++

### Ⅲ. 메모리 및 저장 장치 관리 (Resource Layer)

1. 핵심 기출 키워드
   - **Memory Management**: MMU, TLB, Fragmentation(Internal/External), Paging vs Segmentation.
   - **Virtual Memory**: Demand Paging, Page Fault, Page Replacement(LRU, LFU, Clock).
   - **Thrashing**: 원인, 해결 방안(Working Set, PFF), Locality(Temporal/Spatial).
   - **Disk I/O**: FCFS, SSTF, SCAN, C-SCAN, RAID Levels(0~6, 10), DMA.

📢 섹션 요약 비유: 도시의 '토지 구획 정리(Memory)'와 거대한 '물류 창고(Storage)'를 효율적으로 운영하는 자원 관리 전략입니다.

+++

### Ⅳ. 파일 시스템 및 운영체제 보호 (Infrastructure Layer)

1. 핵심 기출 키워드
   - **File System**: Metadata, Inode, FAT/NTFS/Ext4, Journaling.
   - **Distributed File System**: NFS, AFS, HDFS, CAP 이론.
   - **OS Security**: Access Control(DAC, MAC, RBAC), Protection Ring, Security Kernel.
   - **Virtualization**: Hypervisor(Type 1/2), Full/Para Virtualization, Container, Docker, K8s.

📢 섹션 요약 비유: 도시의 '기록 보관소(File System)'를 지키는 '경찰과 성벽(Security)' 그리고 '미니어처 도시(Virtualization)'를 만드는 기반 기술입니다.

+++

### Ⅴ. 차세대 OS 기술 및 융합 트렌드 (Trend Layer)

1. 핵심 기출 키워드
   - **Cloud OS**: OpenStack, AWS Nitro, Serverless Architecture.
   - **Mobile/IoT OS**: Android, iOS, RTOS, 임베디드 OS 특성.
   - **Edge Computing**: 로컬 처리 및 데이터 프라이버시.
   - **NVM/Persistent Memory**: 오퍼레이팅 시스템의 구조 변화.
   - **AI OS**: 자원 할당의 지능화, GPU/NPU 스케줄링.

📢 섹션 요약 비유: 미래 도시를 향한 '스마트 시티(Cloud/AI)' 계획과 새로운 '에너지원(NVM)'에 대응하는 진화된 운영 규칙들입니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 총론(Operating System General)
- **자식 노드**: 기술사 답안 작성 전략(Writing Strategy)
- **연관 키워드**: Roadmap, Exam Pattern, Core Concepts, Trend Analysis

### 👶 어린아이에게 설명하기
"얘야, 이건 컴퓨터 대장님이 시험을 볼 때 꼭 알아야 하는 '비법 지도'란다. 어떤 문제를 물어봐도 이 지도만 있으면 척척 대답할 수 있어! 도시를 어떻게 만들고, 도로를 어떻게 닦고, 도둑을 어떻게 잡을지 한눈에 볼 수 있는 보물지도 같은 거야."