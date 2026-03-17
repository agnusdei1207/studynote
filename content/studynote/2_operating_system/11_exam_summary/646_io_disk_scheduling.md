+++
title = "646. 운영체제 핵심 요약 - 입출력 및 디스크 스케줄링"
date = "2024-05-23"
weight = 646
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "입출력 시스템", "I/O System", "Disk Scheduling", "DMA", "Interrupt", "RAID"]
+++

> **[Insight]**
> 입출력(I/O) 시스템은 다양한 성능과 특성을 가진 외부 하드웨어 장치들을 운영체제가 일관된 인터페이스를 통해 효율적으로 제어하고 관리하도록 설계된 메커니즘이다.
> CPU와 I/O 장치 간의 속도 차이를 극복하기 위해 버퍼링(Buffering), 캐싱(Caching), 스풀링(Spooling) 기법이 사용되며, DMA(Direct Memory Access)를 통해 CPU의 부하를 최소화한다.
> 특히 보조기억장치인 디스크 I/O 성능 최적화를 위한 디스크 스케줄링(Disk Scheduling) 알고리즘과 데이터 신뢰성 확보를 위한 RAID 기술이 기술적 핵심을 이룬다.

+++

### Ⅰ. 입출력 하드웨어와 제어 방식

1. I/O 하드웨어 구성 요소
   - **컨트롤러(Controller)**: 장치를 직접 제어하는 전자 부품.
   - **레지스터(Registers)**: 데이터, 상태, 제어 정보를 저장 (Data In/Out, Status, Control).
2. I/O 제어 방식
   - **폴링(Polling)**: CPU가 장치 상태를 반복적으로 확인. CPU 낭비 심함.
   - **인터럽트(Interrupt)**: 장치가 준비되면 CPU에 신호를 보내 알림. 비동기적 처리 가능.
   - **DMA(Direct Memory Access)**: CPU 개입 없이 장치 컨트롤러가 직접 메모리에 데이터를 전송. 대량 데이터 처리에 필수적.

📢 섹션 요약 비유: 요리사가 음식이 다 됐는지 계속 확인하는 것이 폴링, 벨이 울리면 나가는 것이 인터럽트, 보조 요리사가 재료를 냉장고에서 꺼내 손질해두는 것이 DMA입니다.

+++

### Ⅱ. 디스크 스케줄링(Disk Scheduling) 알고리즘

1. 목적
   - 디스크 헤드의 이동 거리(Seek Time)를 최소화하여 처리량을 높이고 응답 시간을 단축함.
2. 주요 알고리즘
   - **FCFS(First-Come, First-Served)**: 요청이 들어온 순서대로 처리.
   - **SSTF(Shortest Seek Time First)**: 현재 헤드 위치에서 가장 가까운 요청 먼저 처리. 기아(Starvation) 발생 가능.
   - **SCAN (엘리베이터 알고리즘)**: 헤드가 한쪽 끝에서 반대쪽 끝으로 이동하며 경로상의 요청 처리.
   - **C-SCAN (Circular SCAN)**: 한 방향으로만 이동하며 처리하고, 끝에 도달하면 시작점으로 즉시 복귀. 균등한 대기 시간 보장.
   - **LOOK / C-LOOK**: SCAN/C-SCAN의 변형으로, 요청이 있는 마지막 지점까지만 이동함.

```text
[ Disk Scheduling (SCAN Example) ]

   Requests: 98, 183, 37, 122, 14, 124, 65, 67
   Head: 53
   
   Direction: 0 (Lower)
   Order: 53 -> 37 -> 14 -> 0 -> 65 -> 67 -> 98 -> 122 -> 124 -> 183
```

📢 섹션 요약 비유: 엘리베이터가 층마다 멈추며 승객을 태우듯, 디스크 헤드가 트랙을 따라 움직이며 데이터를 읽는 효율적인 동선 설계입니다.

+++

### Ⅲ. RAID(Redundant Array of Independent Disks) 기술

1. 개념
   - 여러 개의 물리적 디스크를 하나의 논리적 단위로 묶어 성능 향상(Performance)과 데이터 중복(Redundancy)을 통한 신뢰성을 확보함.
2. 주요 레벨
   - **RAID 0 (Stripping)**: 데이터를 분산 저장. 성능 극대화, 결함 허용(Fault Tolerance) 없음.
   - **RAID 1 (Mirroring)**: 똑같은 데이터를 복제 저장. 신뢰성 높음, 비용 두 배.
   - **RAID 5 (Parity)**: 분산 스트라이핑과 분산 패리티(Parity) 사용. 성능과 신뢰성의 균형. 하나까지 고장 복구 가능.
   - **RAID 6**: 두 개의 패리티 사용. 두 개까지 고장 복구 가능.
   - **RAID 10 (1+0)**: 미러링과 스트라이핑의 결합.

📢 섹션 요약 비유: 중요한 서류를 한 곳에 두지 않고 여러 복사본을 만들거나(Mirroring), 나누어 보관하여(Stripping) 유실을 막는 안전 금고 시스템입니다.

+++

### Ⅳ. I/O 성능 향상 기법 (Buffering & Caching)

1. 버퍼링(Buffering)
   - 전송되는 데이터를 일시적으로 저장하여 생산자와 소비자 간의 속도 차이를 조절함.
2. 캐싱(Caching)
   - 자주 사용되는 데이터를 고속 메모리에 유지하여 성능을 대폭 향상함 (Disk Cache).
3. 스풀링(Spooling)
   - 프린터와 같은 저속 공유 장치를 위해 디스크를 버퍼처럼 사용하는 기술.
4. 블록 장치(Block Device) vs 문자 장치(Character Device)
   - 블록: 디스크처럼 블록 단위로 읽기/쓰기 가능.
   - 문자: 키보드, 마우스처럼 한 글자씩 순차적으로 전송.

📢 섹션 요약 비유: 유튜브 영상을 미리 '버퍼'에 담아 끊김 없이 보게 하거나, 자주 보는 자료는 '캐시'처럼 책상 위에 두는 효율화 전략입니다.

+++

### Ⅴ. 최신 저장 장치 기술과 트렌드

1. SSD(Solid State Drive)와 NVMe
   - 기계적 회전이 없는 낸드 플래시 메모리 기반 저장 장치. 탐색 시간(Seek Time)이 거의 없음.
   - 병렬 처리가 가능한 NVMe 프로토콜을 통한 속도 혁신.
2. NVM(Non-Volatile Memory)
   - 전원이 꺼져도 유지되면서 메모리 수준의 속도를 제공하는 차세대 저장 매체.
3. 클라우드 스토리지(Cloud Storage)
   - 네트워크를 통해 접근하는 분산형 데이터 저장 공간.

📢 섹션 요약 비유: LP판을 돌리며 바늘을 옮기던 시대(HDD)에서, 전구 스위치를 켜듯 즉시 데이터를 얻는 시대(SSD)로의 진화입니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 자원 관리(Resource Management)
- **자식 노드**: 파일 시스템(File Systems), 분산 시스템(Distributed Systems)
- **연관 키워드**: DMA, Interrupt, Disk Scheduling, RAID, Buffering, SSD

### 👶 어린아이에게 설명하기
"얘야, 컴퓨터가 장난감 상자(디스크)에서 장난감을 꺼낼 때, 대장님이 '어떤 순서로 꺼낼까?' 하고 고민하는 게 '디스크 스케줄링'이야. 한꺼번에 여러 개를 꺼낼 때는 보조 요리사(DMA)를 시키기도 하고, 중요한 장난감은 잃어버리지 않게 여러 상자에 똑같이 나눠 담기도 해(RAID). 덕분에 우리는 아주 빠르게 장난감을 가지고 놀 수 있단다!"