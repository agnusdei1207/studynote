+++
weight = 658
title = "658. 메모리 할당 및 가상 메모리 관리 핵심 요약"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Memory Management", "Virtual Memory", "Paging", "Segmentation", "MMU"]
+++

> **[Insight]**
> 메모리 관리는 한정된 물리 자원을 다수의 프로세스에게 효율적이고 안전하게 분배하기 위한 운영체제의 핵심 기능이다.
> 가상 메모리(Virtual Memory)는 프로세스에게 실제 물리 메모리보다 큰 주소 공간을 제공하는 동시에, 프로세스 간 격리와 보호를 완벽히 실현하는 현대 OS의 필수 기술이다.
> 페이징(Paging)과 세그멘테이션(Segmentation) 아키텍처는 외부 단편화(External Fragmentation) 문제를 해결하고, 메모리 할당의 유연성을 극대화하는 근간이 된다.

---

### Ⅰ. 메모리 관리의 기본 원칙과 단편화

1. 연속 할당 vs 불연속 할당
   - **연속 할당**: 프로세스를 메모리의 하나의 연속된 블록에 배치 (단편화 발생).
   - **불연속 할당**: 프로세스를 여러 조각으로 나누어 메모리 곳곳에 배치 (페이징, 세그멘테이션).
2. 단편화(Fragmentation) 문제
   - **Internal Fragmentation**: 할당된 블록 내부에 남는 공간.
   - **External Fragmentation**: 총 빈 공간은 충분하나, 연속되지 않아 할당 불가능한 공간.

📢 섹션 요약 비유: 메모리 관리는 '이사 가려는 짐들을 창고에 빈틈없이 쌓는 기술'과 같습니다.

---

### Ⅱ. 가상 메모리(Virtual Memory)와 주소 변환 아키텍처

1. 핵심 개념
   - 프로그램 실행에 필요한 부분만 메모리에 올리고, 나머지는 디스크(Swap Area)에 두는 방식이다.
2. MMU(Memory Management Unit) 다이어그램
   - 가상 주소가 물리 주소로 변환되는 하드웨어적 흐름을 보여준다.

```text
[ Virtual to Physical Address Translation ]

   CPU (Virtual Address)
     |  [Page Number | Offset]
     v
   +-------------------------+
   | TLB (Fast Cache)        | --- Hit ---> [Frame Number | Offset] ---+
   +-------------------------+                                         |
     | Miss                                                            |
     v                                                                 |
   +-------------------------+                                         |
   | Page Table (In RAM)     | --- Valid bit --- [Frame Number] -------+
   +-------------------------+                                         |
     | Invalid (Page Fault)                                            |
     v                                                                 v
   [ Disk (Swap) ] <--- I/O ---> [ Physical RAM ] <--------------------+
```

3. TLB(Translation Lookaside Buffer)
   - 주소 변환 성능을 높이기 위한 고속 하드웨어 캐시이다.

📢 섹션 요약 비유: 가상 메모리는 '책상(RAM)'과 '책꽂이(Disk)' 시스템과 같아서, 지금 보는 페이지만 책상에 두고 나머지는 책꽂이에 넣어두는 것과 같습니다.

---

### Ⅲ. 페이징(Paging) 및 세그멘테이션(Segmentation)

1. Paging (고정 분할)
   - 메모리를 고정된 크기(Page/Frame)로 나누어 할당한다. 외부 단편화는 없으나 내부 단편화가 발생할 수 있다.
2. Segmentation (가변 분할)
   - 코드, 데이터, 스택 등 논리적인 단위로 나누어 할당한다. 내부 단편화는 없으나 외부 단편화가 발생할 수 있다.
3. 혼용 기법 (Paged Segmentation)
   - 세그먼트를 다시 페이지로 나누어 관리함으로써 두 방식의 장점을 취한다.

📢 섹션 요약 비유: 페이징은 책의 모든 페이지를 '똑같은 크기'로 자르는 것이고, 세그멘테이션은 '단원별'로 두께가 다르게 자르는 것과 같습니다.

---

### Ⅳ. 페이지 교체 알고리즘(Page Replacement)

1. 발생 배경
   - 물리 메모리가 가득 찼을 때(Page Fault), 새로운 페이지를 위해 기존 페이지 중 하나를 선택해 내보내야 한다.
2. 주요 알고리즘
   - **FIFO**: 가장 먼저 들어온 페이지 교체. (Belady's Anomaly 발생 가능)
   - **LRU (Least Recently Used)**: 가장 오랫동안 사용되지 않은 페이지 교체 (성능 우수, 구현 복잡).
   - **LFU (Least Frequently Used)**: 참조 횟수가 가장 적은 페이지 교체.
   - **NUR (Not Used Recently)**: 최근 참조/수정 여부(Reference/Modified bits)를 기준으로 교체.

📢 섹션 요약 비유: 책상에 자리가 없으면 '가장 오래전에 본 책'을 책꽂이로 돌려보내는 것과 같습니다.

---

### Ⅴ. 스래싱(Thrashing)과 성능 최적화

1. 스래싱(Thrashing) 정의
   - 빈번한 페이지 부재(Page Fault)로 인해 실제 작업 시간보다 페이지 교체 시간이 더 많아져 CPU 이용률이 급감하는 현상이다.
2. 해결 전략
   - **Working Set 모델**: 프로세스가 일정 시간 동안 자주 참조하는 페이지 집합을 메모리에 상주시킨다.
   - **PFF (Page Fault Frequency)**: 페이지 부재율의 상한과 하한을 정해 프레임 할당량을 조절한다.
3. Locality(국부성/국소성)의 원리
   - 프로세스는 짧은 시간 동안 특정 지역의 메모리를 집중적으로 참조하는 특성을 이용한다 (시간적/공간적 국소성).

📢 섹션 요약 비유: 너무 많은 과목을 동시에 공부하려다 보면 책을 바꾸느라 실제 공부를 하나도 못 하는 '멘붕' 상태와 같습니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 자원 관리(Resource Management)
- **자식 노드**: 페이징(Paging), 세그멘테이션(Segmentation), 가상 메모리(Virtual Memory), 페이지 교체 알고리즘
- **연관 키워드**: MMU, TLB, Page Fault, External Fragmentation, Working Set, Thrashing

### 👶 어린아이에게 설명하기
"우리 집 거실 바닥(물리 메모리)은 좁은데, 장난감 박스(전체 프로그램)는 아주 많지? 그래서 대장님은 지금 가지고 놀 장난감만 거실에 꺼내주고, 다 놀면 다시 박스에 넣어서 창고에 보관한단다. 이렇게 하면 거실이 좁아도 세상의 모든 장난감을 다 가지고 놀 수 있는 것처럼 느껴지는 거야!"