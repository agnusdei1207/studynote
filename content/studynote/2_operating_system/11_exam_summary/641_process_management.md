+++
title = "641. 운영체제 핵심 요약 - 프로세스 관리"
date = "2024-05-23"
weight = 641
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "프로세스 관리", "Process Management", "PCB", "Context Switching", "IPC"]
+++

> **[Insight]**
> 프로세스 관리는 운영체제가 자원을 할당하는 가장 기본적인 단위로, 프로그램의 정적 상태를 실행 중인 동적 상태로 전환하여 관리하는 핵심 메커니즘이다.
> 효율적인 프로세스 관리는 시스템의 멀티태스킹(Multitasking) 성능과 안정성을 결정짓는 결정적 요인이며, PCB(Process Control Block)를 통한 상태 추적과 컨텍스트 스위칭(Context Switching)의 오버헤드 최소화가 기술적 완성도의 척도가 된다.
> 현대 OS에서는 프로세스 간 격리와 보호를 보장하면서도 IPC(Inter-Process Communication)를 통한 효율적인 협업 구조를 설계하는 것이 필수적이다.

+++

### Ⅰ. 프로세스의 본질과 생명주기 관리

1. 프로세스(Process)의 정의
   - 실행 중인 프로그램(Program in Execution)으로, OS로부터 주소 공간, 파일, 메모리 등을 할당받은 능동적인 개체이다.
2. 프로세스 상태 전이(State Transition)
   - **생성(New)**: 프로세스가 생성 중인 상태.
   - **준비(Ready)**: CPU 점유를 기다리는 상태.
   - **실행(Running)**: CPU를 할당받아 명령을 수행 중인 상태.
   - **대기(Waiting/Blocked)**: I/O 완료 등 특정 이벤트를 기다리는 상태.
   - **종료(Terminated)**: 실행이 완료되어 자원을 반납하는 상태.

📢 섹션 요약 비유: 프로세스는 '요리법(Program)'에 따라 실제로 주방에서 '요리를 하고 있는 상태(Process)'이며, 재료가 떨어지면 '대기'하고 화구가 비기를 '준비'하는 과정과 같습니다.

+++

### Ⅱ. PCB(Process Control Block)와 컨텍스트 스위칭

1. PCB(Process Control Block)의 구조
   - OS가 프로세스를 제어하기 위해 필요한 정보를 저장하는 자료구조이다.
   - 구성 요소: PID(Process ID), PC(Program Counter), Registers, CPU Scheduling Info, Memory Management Info 등.

2. 컨텍스트 스위칭(Context Switching) 메커니즘
   - CPU가 한 프로세스에서 다른 프로세스로 전환할 때, 현재 프로세스의 상태를 저장하고 새로운 프로세스의 상태를 복구하는 과정이다.

```text
[ Context Switching Diagram ]

   Process A           OS (Kernel)          Process B
      |                    |                    |
   Running  --- Interrupt -->                   |
      |        (Save State to PCB_A)            |
      |                    |                    |
      |              (Schedule B)               |
      |                    |                    |
      |        (Load State from PCB_B)          |
      |                    | <--- Restore ---  Idle
      |                    |                 Running
```

3. 오버헤드(Overhead) 관리
   - 컨텍스트 스위칭 빈도가 높으면 실질적인 계산 작업보다 관리 작업에 더 많은 CPU가 소모되므로, 적절한 타임 슬라이스(Time Slice) 설정이 중요하다.

📢 섹션 요약 비유: PCB는 요리사의 '메모장'과 같아서, 다른 요리를 하러 갈 때 어디까지 했는지 기록해두고 돌아와서 다시 이어갈 수 있게 해주는 장치입니다.

+++

### Ⅲ. 프로세스 생성과 계층 구조

1. fork()와 exec() 시스템 콜
   - **fork()**: 부모 프로세스를 복제하여 새로운 자식 프로세스를 생성한다.
   - **exec()**: 프로세스의 메모리 공간을 새로운 프로그램으로 덮어씌워 실행한다.
2. 계층 구조의 의의
   - 부모-자식 관계를 통해 자원 상속 및 관리가 용이하며, 프로세스 트리(Process Tree)를 형성한다.
   - 고립된 자식 프로세스가 생기지 않도록 고아 프로세스(Orphan Process) 및 좀비 프로세스(Zombie Process) 관리가 수반된다.

📢 섹션 요약 비유: 부모 요리사가 보조 요리사를 '복제(fork)'한 뒤, 보조 요리사에게 '새로운 레시피(exec)'를 주어 다른 요리를 시키는 구조와 같습니다.

+++

### Ⅳ. IPC(Inter-Process Communication) 메커니즘

1. 공유 메모리(Shared Memory)
   - 프로세스 간 공통의 메모리 영역을 설정하여 데이터를 교환한다. 속도가 빠르나 동기화(Synchronization) 문제가 발생한다.
2. 메시지 패싱(Message Passing)
   - 커널을 통해 메시지를 주고받는 방식이다. 구현이 단순하고 안정적이나 시스템 콜 오버헤드가 발생한다. (Direct/Indirect Communication)
3. 파이프(Pipe) 및 소켓(Socket)
   - 단방향/양방향 통신 스트림을 제공하며, 특히 소켓은 네트워크를 통한 프로세스 간 통신을 지원한다.

📢 섹션 요약 비유: 공유 메모리는 '공용 식탁'에 음식을 두는 것이고, 메시지 패싱은 '웨이터(Kernel)'를 통해 주문서를 전달하는 것과 같습니다.

+++

### Ⅴ. 스레드(Thread)로의 확장과 멀티태스킹

1. 스레드(Thread)의 정의
   - 프로세스 내 실행의 흐름 단위(Unit of Execution)로, 코드/데이터/힙 영역을 공유하며 스택과 레지스터만 독립적으로 가진다.
2. 멀티스레딩(Multi-threading)의 이점
   - 응답성(Responsiveness) 향상, 자원 공유(Resource Sharing), 경제성(Economy), 멀티프로세서 활용성 극대화.
3. 스레드 모델
   - User-level Thread vs Kernel-level Thread.

📢 섹션 요약 비유: 한 주방(Process)에서 여러 명의 요리사(Thread)가 도구와 재료를 공유하며 각자 맡은 파트의 요리를 동시에 완성하는 효율적 협업 방식입니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 자원 관리(Resource Management)
- **자식 노드**: CPU 스케줄링(CPU Scheduling), 프로세스 동기화(Synchronization), 교착상태(Deadlock)
- **연관 키워드**: PCB, Context Switching, IPC, Thread, TCB(Thread Control Block)

### 👶 어린아이에게 설명하기
"얘야, 프로세스는 스마트폰에서 우리가 켜놓은 '앱' 하나하나와 같단다. 앱이 여러 개 켜져 있어도 스마트폰이 느려지지 않게, 운영체제라는 대장님이 각 앱에게 '지금은 네가 움직일 차례야'라고 순서를 정해주고, 앱이 하던 일을 잠깐 멈출 때는 어디까지 했는지 일기장(PCB)에 적어두는 거야. 그래서 우리가 앱을 다시 켜도 아까 하던 화면부터 바로 볼 수 있는 거란다!"