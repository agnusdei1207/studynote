+++
title = "652. 사용자 모드(User Mode)와 커널 모드(Kernel Mode)의 전환 과정 요약"
date = "2024-05-23"
weight = 652
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "User Mode", "Kernel Mode", "Privilege Level", "Mode Bit", "Trap"]
+++

> **[Insight]**
> 사용자 모드(User Mode)와 커널 모드(Kernel Mode)의 구분은 시스템의 무결성과 보안을 유지하기 위한 하드웨어 기반의 보호 메커니즘이다.
> 응용 프로그램의 오동작이나 악의적인 접근이 하드웨어 및 운영체제 전반에 치명적인 영향을 미치지 않도록 접근 권한을 엄격히 격리한다.
> 모드 전환(Mode Transition)은 반드시 정해진 통로(Trap, Interrupt)를 통해서만 이루어지며, 이 과정의 효율성이 전체 시스템 성능의 중요한 척도가 된다.

+++

### Ⅰ. 이중 모드 실행(Dual-mode Operation)의 원리

1. 개념 정의
   - CPU가 하드웨어적으로 지원하는 실행 권한 수준을 두 가지 이상으로 나누어 관리하는 방식이다.
2. 모드 비트(Mode Bit)
   - 현재 실행 중인 모드를 나타내는 하드웨어 레지스터의 비트이다. (0: Kernel Mode, 1: User Mode)
3. 권한의 차이
   - **Kernel Mode**: 모든 하드웨어 명령어(Privileged Instruction) 실행 및 자원 접근 가능.
   - **User Mode**: 제한된 명령만 실행 가능하며, 특권 명령 실행 시 예외(Exception) 발생.

📢 섹션 요약 비유: 이중 모드는 일반 구역(User Mode)과 출입 제한 구역(Kernel Mode)이 나누어진 '은행'과 같습니다.

+++

### Ⅱ. 모드 전환 과정(Mode Transition Flow)

1. 전환 메커니즘 다이어그램
   - 사용자 프로세스가 커널의 도움을 요청하거나 외부 이벤트가 발생했을 때의 흐름을 보여준다.

```text
[ Mode Transition Diagram ]

       User Space (User Mode)           Kernel Space (Kernel Mode)
      +------------------------+       +-------------------------+
      |  User Process Running  |       |                         |
      |  (Mode Bit = 1)        |       |                         |
      +-----------|------------+       +-------------------------+
                  |                                ^
        [ System Call / Trap ]                     |
                  |                                |
      +-----------v------------+       +-----------|-------------+
      |      Set Mode Bit = 0  |------>|   Handle Service /      |
      |      (Switch to Kernel)|       |   Interrupt Request     |
      +------------------------+       +-----------|-------------+
                                                   |
                                         [ Return from Trap ]
                                                   |
      +------------------------+       +-----------v-------------+
      |  User Process Resumes  |<------|      Set Mode Bit = 1   |
      |  (Mode Bit = 1)        |       |      (Switch to User)   |
      +------------------------+       +-------------------------+
```

2. 주요 단계 상세
   - **요청 발생**: 시스템 콜 호출 또는 인터럽트 발생.
   - **모드 전환**: 하드웨어가 Mode Bit를 0으로 변경하고 커널 엔트리 포인트(Entry Point)로 점프.
   - **상태 저장**: 현재 사용자 프로세스의 레지스터 및 PC(Program Counter) 값을 커널 스택에 저장.
   - **커널 작업 수행**: 요청된 서비스를 수행하거나 예외를 처리.
   - **상태 복구 및 복귀**: 저장된 상태를 복원하고 Mode Bit를 1로 변경하여 사용자 모드로 복귀.

📢 섹션 요약 비유: 일반 손님이 금고를 열어야 할 때, 직접 열지 못하고 '직원에게 요청(System Call)'하면 직원이 '열쇠로 모드를 변경(Mode Bit=0)'하여 처리해주는 과정입니다.

+++

### Ⅲ. 특권 명령(Privileged Instructions)과 보호

1. 특권 명령의 종류
   - I/O 명령(IN/OUT), 인터럽트 비활성화, 타이머 설정, 메모리 보호 레지스터 변경 등.
2. 예외 처리(Exception Handling)
   - 사용자 모드에서 특권 명령을 실행하려고 시도하면 CPU는 하드웨어 Trap을 발생시켜 제어권을 커널로 넘기고 해당 프로세스를 종료할 수 있다.
3. 시스템 보호의 핵심
   - 잘못된 사용자 프로그램이 다른 프로그램의 메모리를 읽거나 쓰지 못하게 하며, 시스템 전체를 다운시키는 것을 방지한다.

📢 섹션 요약 비유: 은행 손님이 허가 없이 카운터 안쪽 기계를 조작하려 하면 '경보(Trap)'가 울리고 보안 요원(Kernel)이 출동하는 것과 같습니다.

+++

### Ⅳ. 모드 전환과 성능 오버헤드

1. 오버헤드 발생 지점
   - 레지스터 저장/복구, 캐시 플러시(Cache Flush) 가능성, 커널 스택 전환 등.
2. 잦은 전환의 영향
   - 시스템 콜이 너무 빈번하게 발생하면 응용 프로그램의 순수 실행 시간(User Time)보다 관리 시간(System Time)이 길어져 성능이 저하된다.
3. 최적화 기법
   - 시스템 콜 배치 처리(Batching), vDSO(Virtual Dynamic Shared Object) 등을 통해 불필요한 모드 전환을 최소화한다.

📢 섹션 요약 비유: 창구 직원에게 물건을 하나씩 전달하며 묻는 것보다, 한꺼번에 모아서 물어보는 것이 훨씬 빠른 것과 같습니다.

+++

### Ⅴ. 현대 아키텍처에서의 확장 (Ring Levels)

1. 인텔 x86 Protection Rings
   - Ring 0 (Kernel), Ring 1/2 (Device Drivers), Ring 3 (User Applications).
2. 가상화(Virtualization)와 모드
   - 하이퍼바이저(Hypervisor) 모드와 같이 더 깊은 특권 수준이 추가되기도 한다. (Root/Non-root mode)
3. 보안 강화 (Enclave/TEE)
   - SGX(Software Guard Extensions)나 TrustZone과 같은 기술을 통해 커널조차 접근 못 하는 더 안전한 영역을 구축한다.

📢 섹션 요약 비유: 단순히 안과 밖이 아니라, 보안 등급에 따라 여러 겹의 성벽(Ring)을 쌓아 핵심 요소를 보호하는 요새와 같습니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 보호(Operating System Protection)
- **자식 노드**: 시스템 콜(System Call), 인터럽트(Interrupt), 특권 명령(Privileged Instruction)
- **연관 키워드**: Mode Bit, Trap, Ring 0/3, Hardware-based Security

### 👶 어린아이에게 설명하기
"컴퓨터는 아주 중요한 일을 하는 '왕의 방'과 우리가 노는 '거실'이 나뉘어 있단다. 우리가 장난을 치다가 왕의 방에 있는 중요한 물건을 망가뜨리면 안 되기 때문에, 왕의 방에 들어갈 때는 반드시 대장님께 허락을 받아야 해. 대장님이 문을 열어주고 일이 끝나면 다시 거실로 보내주는 규칙이 있어서 컴퓨터가 고장 나지 않고 안전하게 돌아가는 거란다!"