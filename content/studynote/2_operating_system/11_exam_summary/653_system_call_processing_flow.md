+++
title = "653. 시스템 콜(System Call) 처리 흐름 상세 분석"
date = "2024-05-23"
weight = 653
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "System Call", "Trap", "IDT", "Kernel Space", "Software Interrupt"]
+++

> **[Insight]**
> 시스템 콜(System Call)은 사용자 프로세스가 운영체제 커널이 제공하는 보호된 서비스에 접근할 수 있는 유일한 공식 창구이다.
> 응용 프로그램이 파일 I/O, 네트워크 통신, 메모리 할당 등의 작업을 수행할 때 직접 하드웨어를 제어하는 대신, 커널에 요청을 전달함으로써 시스템의 일관성과 보안을 보장한다.
> 시스템 콜 처리 흐름의 정교한 이해는 OS 내부 동작 메커니즘과 시스템 성능 최적화를 이해하는 핵심 열쇠가 된다.

+++

### Ⅰ. 시스템 콜(System Call)의 역할과 유형

1. 핵심 역할
   - 사용자 모드와 커널 모드 사이의 인터페이스 역할을 하며, 자원 보호 및 추상화를 제공한다.
2. 주요 유형별 예시
   - **프로세스 제어**: fork(), exit(), wait(), exec().
   - **파일 관리**: open(), read(), write(), close().
   - **장치 관리**: ioctl(), read(), write().
   - **정보 유지**: getpid(), alarm(), sleep().
   - **통신**: pipe(), shmget(), socket().

📢 섹션 요약 비유: 시스템 콜은 '고급 요리를 주문하는 메뉴판'과 같아서, 손님은 재료를 몰라도 메뉴 이름만으로 원하는 서비스를 받을 수 있습니다.

+++

### Ⅱ. 시스템 콜 처리 프로세스 분석

1. 실행 흐름 다이어그램
   - API 호출부터 커널 실행 후 복귀까지의 전 과정을 보여준다.

```text
[ System Call Execution Flow ]

    User Application
       |
    1. Call API Library (e.g., printf)
       |
    2. API invokes System Call Wrapper (e.g., write)
       |  [ Place Syscall Num in Register / Push Args ]
    3. TRAP / Software Interrupt (INT 0x80 / syscall)
       |
   ----|-------------------------------------------- Kernel Boundary
       |
    4. Interrupt Descriptor Table (IDT) Lookup
       |  [ Context Save / Switch to Kernel Stack ]
    5. System Call Handler Execution
       |  [ Look up System Call Table by Index ]
    6. Specific Kernel Routine Execution
       |  [ Verify Params / Perform Action ]
    7. Context Restore / Resume User Mode
       |
   ----|-------------------------------------------- Kernel Boundary
       |
    8. Return to Application with Result
```

2. 핵심 메커니즘 설명
   - **Trap**: 소프트웨어 인터럽트를 유발하여 CPU 모드를 커널 모드로 전환한다.
   - **System Call Table**: 시스템 콜 번호와 해당 커널 함수 주소를 매핑한 배열이다.
   - **Parameter Passing**: 레지스터, 스택, 또는 메모리 블록 주소를 통해 인자를 전달한다.

📢 섹션 요약 비유: 주문서(System Call Number)를 작성하여 창구에 넣으면(Trap), 직원이 번호표를 보고 알맞은 주방팀(Kernel Routine)에게 전달하는 과정입니다.

+++

### Ⅲ. API와 시스템 콜의 관계 (Standard C Library)

1. 추상화 계층
   - 프로그래머는 대개 커널의 로우 레벨 시스템 콜을 직접 호출하지 않고, 표준 라이브러리(libc)의 Wrapper 함수를 사용한다.
2. POSIX(Portable Operating System Interface) 표준
   - 다양한 운영체제 간의 호환성을 유지하기 위해 시스템 콜 인터페이스 규격을 정의한다.
3. 라이브러리의 역할
   - 인자 검증, 에러 처리(errno 설정), 시스템 콜 번호 로딩 및 실제 Trap 명령어 수행을 대행한다.

📢 섹션 요약 비유: 메뉴판(API)에서 요리를 고르면, 웨이터(Library)가 주방장만 이해할 수 있는 전문 용어(System Call)로 바꿔서 주문을 넣어주는 것과 같습니다.

+++

### Ⅳ. 커널의 매개변수 검증 및 보안

1. 주소 검증(Pointer Validation)
   - 사용자 프로세스가 전달한 포인터가 자신의 주소 영역 내에 있는지 엄격히 검사하여 커널 메모리 침범을 방지한다.
2. 복사 메커니즘 (copy_to_user / copy_from_user)
   - 사용자 공간과 커널 공간은 분리되어 있으므로, 안전한 데이터 복사 함수를 사용하여 데이터를 주고받는다.
3. 권한 체크
   - 요청한 프로세스가 해당 파일이나 자원에 접근할 권한이 있는지 수시로 확인한다.

📢 섹션 요약 비유: 직원이 주문서를 받았을 때, 손님이 지불 능력이 있는지 확인하고 주문서에 적힌 주소가 손님의 테이블 번호가 맞는지 검사하는 절차입니다.

+++

### Ⅴ. 시스템 콜 성능 최적화 기술

1. vDSO (Virtual Dynamic Shared Object)
   - gettimeofday()와 같이 자주 호출되지만 보안 위협이 적은 경우, 모드 전환 없이 사용자 공간에서 커널 데이터를 직접 읽게 하는 메커니즘이다.
2. System Call Batching
   - 여러 개의 시스템 콜을 하나로 묶어 전달하여 모드 전환 오버헤드를 줄인다. (예: io_uring)
3. Fast System Call Instructions
   - INT 0x80(느린 방식) 대신 SYSENTER / SYSEXIT 또는 SYSCALL / SYSRET와 같은 현대 CPU의 전용 명령어를 사용하여 속도를 개선한다.

📢 섹션 요약 비유: 매번 창구에 가는 대신, 자주 확인하는 정보는 게시판(vDSO)에 붙여두어 손님이 직접 보게 하는 것과 같습니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 운영체제 인터페이스(OS Interface)
- **자식 노드**: 시스템 콜 테이블(System Call Table), IDT(Interrupt Descriptor Table), libc
- **연관 키워드**: Trap, Software Interrupt, API, Kernel Entry, copy_from_user

### 👶 어린아이에게 설명하기
"컴퓨터 속에는 아주 바쁜 일꾼들이 사는 성이 있단다. 우리가 성 밖에서 장난감을 고쳐달라고 하고 싶을 때, 직접 성안으로 뛰어 들어가면 안 돼. 성문에 있는 작은 우체통(System Call)에 편지를 넣으면, 성을 지키는 기사님이 편지를 가져다가 성안의 기술자에게 전달해준단다. 기술자가 고쳐서 다시 우체통으로 보내주면 우리가 받을 수 있는 거야!"