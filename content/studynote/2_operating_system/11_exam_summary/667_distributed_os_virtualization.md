+++
title = "667. 분산 운영체제(Distributed OS) 및 가상화 핵심 기술 요약"
date = "2024-05-23"
weight = 667
[extra]
categories = "studynote-operating-system"
keywords = ["Distributed OS", "Virtualization", "Hypervisor", "Container", "Transparency"]
+++

> **[Insight]**
> 분산 운영체제는 네트워크로 연결된 여러 독립된 노드를 하나의 논리적인 시스템으로 통합하여 사용자에게 단일 시스템 이미지(SSI, Single System Image)를 제공하는 고성능 컴퓨팅 환경이다.
> 가상화 기술은 하드웨어 자원을 논리적으로 분리하여 자원 활용도를 극대화하고, 하이퍼바이저(Hypervisor)와 컨테이너(Container)를 통해 격리된 실행 환경을 구축함으로써 클라우드 컴퓨팅의 기반을 형성한다.
> 현대 시스템은 분산 구조의 확장성과 가상화의 유연성을 결합하여 대규모 데이터 처리와 서비스의 가용성(Availability)을 동시에 확보하는 방향으로 진화하고 있다.

+++

### Ⅰ. 분산 운영체제의 핵심 원칙과 투명성(Transparency)

1. 분산 OS의 정의
   - 여러 컴퓨터의 자원을 통합 관리하여 사용자가 마치 한 대의 강력한 컴퓨터를 쓰는 것처럼 느끼게 해주는 OS이다.
2. 8대 투명성 요소
   - 위치(Location), 접근(Access), 이주(Migration), 복제(Replication), 병행(Concurrency), 장애(Failure), 성능(Performance), 규모(Scaling) 투명성이 확보되어야 한다.
3. 통신 방식
   - RPC(Remote Procedure Call) 및 메시지 패싱(Message Passing)을 통해 노드 간 동기화를 수행한다.

📢 섹션 요약 비유: 분산 OS는 '여러 명의 요리사가 하나의 거대한 주방에서 일하는 것'과 같아서, 손님은 누가 요리를 했는지 모르지만 음식이 아주 빨리 나오는 마법과 같습니다.

+++

### Ⅱ. 서버 가상화(Server Virtualization) 기술

1. 하이퍼바이저(Hypervisor)의 유형
   - **Type 1 (Native/Bare-metal)**: 하드웨어 바로 위에서 실행되며 성능이 우수하다 (예: Xen, KVM).
   - **Type 2 (Hosted)**: 호스트 OS 위에서 실행되며 설치가 간편하다 (예: VMware Workstation, VirtualBox).

```text
[ Virtualization Architecture Map ]

      Type 1 Hypervisor            Type 2 Hypervisor
    +-------------------+        +-------------------+
    | [VM1] [VM2] [VM3] |        | [VM1] [VM2] [VM3] |
    +-------------------+        +-------------------+
    |    Hypervisor     |        |    Hypervisor     |
    +-------------------+        +-------------------+
    |     Hardware      |        |     Host OS       |
    +-------------------+        +-------------------+
                                 |     Hardware      |
                                 +-------------------+
```

2. 전가상화(Full Virtualization) vs 반가상화(Para-virtualization)
   - **전가상화**: 게스트 OS 수정 없이 실행하나 바이너리 번역 오버헤드가 발생한다.
   - **반가상화**: 게스트 OS 커널을 수정하여 하이퍼콜(Hypercall)을 사용함으로써 성능을 향상시킨다.

📢 섹션 요약 비유: 가상화는 '한 채의 집을 칸막이로 나눠서 여러 가구가 살게 하는 것'과 같아서, 실제 집(하드웨어)은 하나지만 각 가구는 자기만의 집(VM)이 있다고 느끼는 기술입니다.

+++

### Ⅲ. 컨테이너(Container) 기술과 OS 수준 가상화

1. 컨테이너의 정의
   - 호스트 OS의 커널을 공유하면서 프로세스 수준에서 자원을 격리하는 경량화된 가상화 방식이다.
2. 핵심 기술 요소
   - **Namespaces**: 프로세스, 네트워크, 파일 시스템 등을 논리적으로 격리한다.
   - **Cgroups (Control Groups)**: CPU, 메모리 등 자원 사용량을 제한하고 제어한다.
3. 하이퍼바이저와의 차이
   - Guest OS가 필요 없어 부팅이 빠르고 자원 효율성이 극대화된다. (예: Docker, Podman)

📢 섹션 요약 비유: 하이퍼바이저가 '개별 주택'을 짓는 것이라면, 컨테이너는 '고시원'과 같아서 공용 시설(커널)은 같이 쓰되 방(컨테이너)만 따로 쓰는 효율적인 구조입니다.

+++

### Ⅳ. 분산 파일 시스템(DFS)과 데이터 일관성

1. NFS(Network File System)
   - 네트워크를 통해 원격지의 파일 시스템을 로컬처럼 마운트하여 사용하는 전통적인 방식이다.
2. HDFS(Hadoop Distributed File System)
   - 대규모 데이터를 블록 단위로 여러 노드에 분산 저장하고 복제본을 유지하여 결함 허용(Fault Tolerance)을 보장한다.
3. 일관성 모델(Consistency Model)
   - 강한 일관성(Strict Consistency)과 결과적 일관성(Eventual Consistency) 사이의 트레이드오프를 관리한다.

📢 섹션 요약 비유: 분산 파일 시스템은 '마을 공동 창고'와 같아서, 물건을 여러 곳에 나눠 보관해도 내가 필요할 때 어디서든 꺼내 쓸 수 있게 관리해주는 시스템입니다.

+++

### Ⅴ. 클라우드 오케스트레이션 및 미래 전망

1. 쿠버네티스(Kubernetes, K8s)
   - 수많은 컨테이너의 배포, 확장, 관리를 자동화하는 분산 자원 오케스트레이션 플랫폼이다.
2. 에지 가상화(Edge Virtualization)
   - 중앙 클라우드가 아닌 현장(Edge) 장치에서 가상화 기술을 통해 실시간 처리를 수행한다.
3. 서버리스(Serverless) 컴퓨팅
   - 사용자가 서버 관리를 신경 쓰지 않고 코드 단위의 실행만 요청하면 OS와 인프라가 자동으로 자원을 할당한다.

📢 섹션 요약 비유: 오케스트레이션은 '거대한 오케스트라의 지휘자'와 같아서, 수천 명의 연주자(컨테이너)가 제시간에 맞춰 정확한 소리를 내도록 조율하는 역할을 합니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 현대 인프라 기술(Modern Infrastructure)
- **자식 노드**: Docker, Kubernetes, Xen, KVM, HDFS
- **연관 키워드**: Hypervisor, Container, SSI, RPC, Fault Tolerance

### 👶 어린아이에게 설명하기
"얘야, 분산 시스템은 여러 명의 친구가 힘을 합쳐서 아주 무거운 상자를 옮기는 것과 같단다. 그리고 가상화는 커다란 케이크 한 개를 아주 정교하게 나눠서, 친구들 모두가 자기만의 작은 케이크를 가진 것처럼 느끼게 해주는 마술이란다. 이 마술 덕분에 우리는 아주 큰 컴퓨터가 없어도 인터넷 세상을 빠르고 즐겁게 이용할 수 있는 거야!"