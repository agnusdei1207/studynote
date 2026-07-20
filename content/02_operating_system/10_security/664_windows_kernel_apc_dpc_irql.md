---
title: "DPC"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 664
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Windows 운영체제는 하드웨어 인터럽트(ISR)가 시스템을 오래 멈추는 것을 막기 위해, 인터럽트 처리의 긴급한 부분만 ISR에서 끝내고, 덜 긴급한 나머지 작업은 나중에 처리하도록 지연시키는 <strong>DPC (Deferred Procedure Call)</strong>와 스레드 특정 비동기 작업인 <strong>APC (Asynchronous Procedure Call)</strong> 메커니즘을 사용한다. (리눅스의 Top/Bottom Half와 유사)
> 2. <strong>DPC (지연된 호출)</strong>: 하드웨어 인터럽트(IRQL: DIRQL)보다 한 단계 낮은 IRQL(DISPATCH_LEVEL)에서 실행되며, 스레드 문맥이 아니라 '프로세서(CPU 코어)' 자체에 묶여 컨텍스트 스위치를 막고 시스템 전역의 I/O 후처리를 담당한다.
> 3. **APC (비동기 호출)**: 특정 '스레드(Thread)'의 컨텍스트(IRQL: APC_LEVEL)에서 실행되며, 주로 I/O 비동기 완료 통보(Completion Routine)나 스레드 일시 정지/강제 종료 등 유저 스페이스와 커널 스페이스 간의 스레드 제어 통신에 사용된다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>IRQL (Interrupt Request Level)</strong>: Windows 커널이 CPU의 우선순위를 0(PASSIVE_LEVEL, 일반 스레드)부터 31(HIGH_LEVEL, 치명적 하드웨어)까지 나누어 관리하는 권한 레벨. (우선순위가 높은 작업이 낮은 작업을 선점함)
  - <strong>DPC (Deferred Procedure Call)</strong>: 하드웨어 인터럽트(DIRQL)가 발생했을 때, "이건 조금 이따가 처리할게"라고 DPC 큐(Queue)에 넣어두고 IRQL 2 (DISPATCH_LEVEL)에서 처리하는 커널 함수.
  - <strong>APC (Asynchronous Procedure Call)</strong>: 특정 스레드에게 "너 이 일 좀 비동기로 처리해 줘"라고 스레드의 APC 큐에 넣어두고 IRQL 1 (APC_LEVEL)에서 처리하는 함수.

- <strong>필요성 (인터럽트 지연과 스케줄링의 딜레마 극복)</strong>:
  - 네트워크 카드로 1GB 패킷이 들어와 인터럽트(ISR)가 걸렸다. 만약 ISR 안에서 이 1GB를 모두 메모리로 복사하고 TCP/IP 검사까지 다 해버린다면?
  - ISR이 도는 동안(DIRQL) CPU는 마우스 입력, 키보드 입력 등 다른 모든 하드웨어 인터럽트를 무시하게 된다(Interrupt Disable). 결국 마우스가 멈추고 시스템이 버벅거린다.
  - **해결책**: ISR은 딱 1초만 일하고 "패킷 왔음!" 깃발만 꽂은 채 재빨리 CPU를 반환해야 한다. 남은 1GB 패킷 복사 작업은 나중에 일반 스레드보다는 중요하지만 하드웨어보단 덜 중요한 중간 단계(DPC/APC)로 넘겨서 여유 있게 처리하는 이중화 구조가 필요했다.

  - <strong>하드웨어 인터럽트 (ISR)</strong>: 구급차 도착. 의사(CPU)는 하던 수술을 즉시 멈추고 구급차로 뛰어나가 피만 닦고 지혈만 한다(초긴급).
  - **DPC**: 피를 닦은 환자를 응급실 베드(DPC 큐)에 눕혀놓는다. 의사는 당장 죽을 사람(다른 ISR)이 없으면, 응급실 베드를 차례대로 돌며 뼈를 맞추고 붕대를 감는다(후처리).
  - **APC**: 붕대를 다 감고 병실로 올라간 환자(특정 스레드)에게 간호사가 메모지(APC)를 남긴다. "환자분, 링거 다 맞으면 직접 퇴원 수속 밟으세요." 환자(스레드)가 깨어나면 이 메모지를 보고 자기 몸(Context)으로 스스로 퇴원 수속(I/O 완료 처리)을 밟는다.

- **발전 과정**:
  1. <strong>초기 OS (Single Interrupt)</strong>: 인터럽트가 중첩되지 않고 한 번에 하나씩 다 처리함. 시스템 지연 극심.
  2. **Windows NT 계열 (IRQL 도입)**: 하드웨어 설계(PIC, APIC)에 맞춰 소프트웨어적으로 IRQL 0~31 단계를 정의.
  3. **DPC/APC 구조 완성**: 커널 스케줄러(DISPATCH_LEVEL)와 스레드 제어(APC_LEVEL)를 명확히 분리하여 현대 Windows의 고성능 비동기 I/O (IOCP)의 토대가 됨.

- **📢 섹션 요약 비유**: 전화벨(인터럽트)이 울리면 "여보세요, 네 이따 전화드릴게요" 하고 바로 끊어버리는 것(ISR)이 1단계, 조금 한가해졌을 때 메모장을 보고 다시 전화를 거는 것(DPC)이 2단계 비동기 처리의 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Windows IRQL (Interrupt Request Level) 스택

DPC와 APC를 이해하려면 윈도우의 심장인 IRQL 계층을 알아야 한다. (번호가 높을수록 권한이 셈)

| IRQL 레벨 | 명칭 | 역할 | 특징 (이 레벨에서 하면 안 되는 일) |
|:---|:---|:---|:---|
| **0** | **PASSIVE_LEVEL** | 일반적인 유저 스레드 및 커널 스레드 실행 | 자유로움 (Page Fault 허용, Sleep 허용) |
| **1** | **APC_LEVEL** | **APC (비동기 프로시저 호출) 실행** | Page Fault 허용 |
| **2** | **DISPATCH_LEVEL** | **DPC 실행**, 커널 스케줄러 작동 | <strong>Page Fault 절대 금지! (발생 시 블루스크린 IRQL_NOT_LESS_OR_EQUAL)</strong>, Sleep 불가 |
| **3 ~ 26**| **DIRQL (Device IRQL)**| 실제 하드웨어 디바이스 인터럽트 (ISR) 실행 | 초고속 처리 필수, 모든 메모리 접근은 Non-paged Pool만 가능 |
| **27 ~ 31**| HIGH_LEVEL 등 | 시스템 패닉, 머신 체크 예외 등 절대 권력 | - |

---

### DPC (Deferred Procedure Call) 동작 메커니즘

DPC는 특정 스레드에 속하지 않는다. CPU 코어(프로세서) 자체의 큐에 쌓여서 실행된다.

1. <strong>인터럽트 발생 (DIRQL)</strong>: 네트워크 카드(NIC)가 패킷을 받아 CPU에 INT를 날림.
2. <strong>ISR 실행 (DIRQL)</strong>: 커널이 `NIC_ISR()` 함수를 실행. "패킷이 왔군, 복사는 나중에 해야지." -> `KeInsertQueueDpc()`를 호출하여 DPC 객체를 현재 CPU의 DPC 큐에 넣음.
3. **IRQL 강등 (DIRQL $\rightarrow$ DISPATCH_LEVEL)**: 더 이상 처리할 하드웨어 인터럽트가 없으면 CPU의 IRQL이 2(DISPATCH_LEVEL)로 낮아짐.
4. **DPC 실행**: IRQL이 2로 내려오자마자, 커널은 일반 스레드(0)로 넘어가기 전에 DPC 큐를 뒤져서 쌓여있는 `NIC_DPC_Handler()`를 꺼내 패킷 복사(TCP/IP 처리)를 수행함.
5. **결과**: 무거운 패킷 처리 작업이 하드웨어 인터럽트를 막지 않게 되어 시스템 반응성이 유지됨.

---

### APC (Asynchronous Procedure Call) 동작 메커니즘

DPC가 "CPU 코어"의 숙제라면, APC는 <strong>"특정 스레드(Thread)"</strong>의 숙제다.

1. **I/O 완료 보고**: DPC에서 패킷 처리가 다 끝났다. 이제 이 패킷을 기다리던 앱(스레드 A)에게 "완료됐어!"라고 알려줘야 한다.
2. **APC 큐 삽입**: DPC 루틴이 스레드 A의 KAPC(커널 APC) 큐나 UAPC(유저 APC) 큐에 `완료_루틴()` 객체를 밀어 넣는다.
3. <strong>스레드 A 깨어남 (APC_LEVEL)</strong>: 스레드 A가 CPU를 할당받아 실행되려 할 때, 커널은 스레드 A의 IRQL을 1(APC_LEVEL)로 살짝 올리고 APC 큐에 있는 `완료_루틴()`을 먼저 강제로 실행시킨다.
4. **유저 코드 복귀 (PASSIVE_LEVEL)**: APC 루틴이 끝나면 IRQL이 0으로 떨어지며 스레드 A의 원래 코드가 마저 실행된다. (유저 앱 입장에서는 자기도 모르게 비동기 콜백 함수가 실행된 셈이다.)

- **📢 섹션 요약 비유**: DPC는 공장 전체의 컨베이어 벨트를 치우는 '공통 청소부(CPU 소속)'이고, APC는 특정 직원(스레드)의 책상 위에 올려놓은 '개인 우편물'입니다. 직원이 출근하면 무조건 자기 우편물부터 읽어야 본업을 시작할 수 있습니다.

---

## Ⅲ. 비교 및 연결

### 리눅스 vs 윈도우 커널 인터럽트 후처리 비교

두 OS는 이름만 다를 뿐 완벽히 같은 철학(Top Half / Bottom Half)을 공유한다.

| 기능 | Linux (리눅스 커널) | Windows (NT 커널) | 차이점 / 특징 |
|:---|:---|:---|:---|
| <strong>긴급 인터럽트 (Top Half)</strong>| <strong>Hard IRQ (ISR)</strong> | <strong>ISR (DIRQL)</strong> | 하드웨어 인터럽트를 직접 처리하고 차단하는 영역 |
| <strong>지연된 처리 (Bottom Half)</strong>| **SoftIRQ / Tasklet** | **DPC (DISPATCH_LEVEL)** | CPU 단위로 동작하며, I/O의 무거운 처리를 대행함 |
| <strong>스레드 문맥 지연 (Bottom Half)</strong>| **Workqueue** | <strong>System Worker Thread</strong> | Sleep이 필요할 때 사용하는 일반 스레드 기반 작업 |
| <strong>비동기 스레드 알림</strong> | Signal (시그널) | **APC (APC_LEVEL)** | 윈도우의 APC가 리눅스의 Signal보다 훨씬 정교한 비동기 I/O (IOCP) 지원 가능 |

### 과목 융합 관점

- **시스템 프로그래밍 (System Programming)**: Windows에서 비동기 I/O를 짤 때 `ReadFileEx` 같은 API를 쓰면, 작업 완료 시 호출될 콜백(Completion Routine)을 등록한다. 이 콜백 함수가 실행되는 근본적인 원리가 바로 유저 스레드의 **User APC** 큐에 커널이 객체를 삽입하고 알람(Alertable Wait State)을 주기 때문이다.
- <strong>보안 (Security)</strong>: 루트킷(Rootkit)이나 상용 안티바이러스(백신)는 커널에 모듈(.sys)을 올려 특정 프로세스를 강제로 죽일 때 `KeInsertQueueApc`를 악용한다. 타겟 스레드의 APC 큐에 '스레드 종료(Terminate)' 명령을 몰래 끼워 넣으면, 타겟 스레드가 켜지자마자 자기 자신을 자살(Suicide)시키는 해킹 기법으로 쓰인다.

- **📢 섹션 요약 비유**: 리눅스와 윈도우 모두 "급한 불부터 끄고(ISR), 남은 재는 나중에 치운다(DPC)"는 철학은 똑같습니다. 다만 윈도우는 IRQL이라는 계급(0~31)을 명확하게 나누어 군대처럼 통제하는 방식을 택했을 뿐입니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오

1. **시나리오 — 악명 높은 블루스크린(BSOD) "IRQL_NOT_LESS_OR_EQUAL" 해결**: 윈도우 서버에 새로 개발된 보안 솔루션 드라이버(.sys)를 올렸더니, 부팅 도중 파란 화면(BSOD)이 뜨며 뻗어버림. 에러 코드는 `0x0000000A (IRQL_NOT_LESS_OR_EQUAL)`.
   - **원인 분석**: 커널 덤프(Kdump)를 분석해 보니, 보안 드라이버가 **DPC 루틴(DISPATCH_LEVEL = 2)** 안에서 메모리를 동적 할당(`ExAllocatePoolWithTag`)하면서 `PagedPool` (가상 메모리로 스왑 아웃될 수 있는 공간)을 요구했다. DPC가 도는 도중에 스왑 아웃된 메모리를 읽으려다 페이지 폴트(Page Fault)가 났는데, IRQL 2에서는 스케줄러가 잠들어 있어 디스크에서 데이터를 가져올 수 없으므로 커널이 그 자리에서 붕괴한 것이다.
   - **대응 (실무적 가이드)**: DPC나 ISR 같은 높은 IRQL 환경(IRQL >= 2)에서는 절대로 Page Fault를 유발할 수 있는 코드를 짜면 안 된다. 메모리 할당은 무조건 물리 램에 고정된 `NonPagedPool`을 써야 하며, 뮤텍스(Mutex) 같은 Sleep 가능한 락을 쓰면 안 되고 무조건 스핀락(Spinlock)을 써야 한다.

2. **시나리오 — 오디오/영상 편집기에서의 끊김(Audio Stuttering/Glitch) 현상**: 고사양 Windows PC에서 DAW(음악 작업 프로그램)를 돌리는데, 마우스를 움직이거나 랜선에 데이터를 받을 때마다 스피커에서 "찌직" 하는 소리가 난다.
   - <strong>원인 분석 (DPC Latency)</strong>: 네트워크 카드나 그래픽 카드의 후잡한 드라이버가 DPC 루틴을 너무 길게(수 밀리초 이상) 잡고 있는 것이 원인이다. DPC가 큐를 독점(DISPATCH_LEVEL)하면, IRQL 0에서 도는 오디오 처리 스레드(아무리 우선순위가 높아도)가 CPU를 배정받지 못해 오디오 버퍼가 고갈(Under-run)되어 소리가 끊기는 것이다.
   - **대응**: `LatencyMon` 같은 DPC 지연 분석 도구를 통해 어느 `.sys` (예: `ndis.sys`, `nvlddmkm.sys`)가 DPC 시간을 깎아 먹고 있는지 찾아내어 드라이버를 롤백하거나 전원 옵션(PCIe ASPM)을 튜닝해야 한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 Windows 커널 드라이버 비동기 처리 설계 플로우            |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [하드웨어 인터럽트(ISR) 발생 후 대용량 데이터 처리 로직 구현]              |
  |                |                                                  |
  |                v                                                  |
  |      처리해야 할 작업이 밀리초(ms) 단위 이상 오래 걸리거나 Sleep이 필요한가? |
  |          +- 예 ------> [System Worker Thread (PASSIVE_LEVEL) 위임]  |
  |          |            (DPC에서 워커 스레드로 큐잉하여 안전하게 처리)         |
  |          +- 아니오 (순수 메모리 연산, 매우 빠름)                          |
  |                |                                                  |
  |                v                                                  |
  |      결과를 특정 사용자 스레드(User Thread)의 컨텍스트에서 실행해야 하는가?  |
  |          +- 예 ------> [APC (Asynchronous Procedure Call) 삽입]     |
  |          |            (해당 스레드가 Alertable 상태가 되면 콜백 실행)     |
  |          |                                                        |
  |          +- 아니오 ---> [DPC (Deferred Procedure Call) 로 직접 처리]  |
  |                         (단, Page Fault 주의, NonPagedPool만 사용)    |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 윈도우 시스템 프로그래밍의 정수는 "IRQL의 룰을 거스르지 않는 것"이다. 초보 드라이버 개발자들은 인터럽트나 DPC 안에서 무거운 암호화 연산을 돌리거나 파일 I/O를 날려 시스템 전체를 벽돌로 만든다. 우수한 아키텍트는 작업을 3단계(ISR $\rightarrow$ DPC $\rightarrow$ Worker Thread)로 폭포수처럼 잘게 쪼개어 시스템의 반응성(Responsiveness)을 극한으로 끌어올린다.

### 도입 체크리스트
- **Threaded DPC**: 실시간성(Real-time)이 요구되는 오디오/산업용 윈도우 환경에서는, 악성 DPC가 시스템을 멈추는 것을 막기 위해 커널 레지스트리를 튜닝하여 DPC를 아예 일반 스레드처럼 우선순위를 깎아버리는 기능(Threaded DPC)의 적용을 검토했는가?
- <strong>Alertable Wait State</strong>: 유저 스페이스에서 앱이 커널의 APC 콜백(I/O 완료 등)을 받으려면, 스레드가 멍청하게 무한 루프를 돌면 안 되고 반드시 `SleepEx()`, `WaitForSingleObjectEx()` 같은 함수를 호출해 자신을 "Alertable(알람을 받을 수 있는 상태)"로 만들어야 APC가 꽂힌다는 점을 숙지했는가?

- **📢 섹션 요약 비유**: IRQL은 커널 세계의 엄격한 '신분제도'입니다. 평민(스레드, IRQL 0)은 잠을 자도 되지만, 귀족(DPC, IRQL 2)은 근무 중 절대 졸아서(Page Fault)는 안 되며, 왕(ISR, IRQL 3+)은 아주 잠깐만 통치하고 물러나야 나라가 평화롭습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 단일 인터럽트 구조 (Legacy) | DPC/APC 분할 구조 적용 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (인터럽트 지연)</strong>| 수 밀리초 동안 하드웨어 멈춤 | <strong>수 마이크로초(µs) 내 ISR 종료</strong> | 시스템 응답성 및 Jitter 대폭 감소 |
| <strong>정량 (I/O 성능)</strong> | 동기식 I/O로 스레드 대기 낭비 | APC/IOCP를 통한 비동기 처리 | 웹 서버/DB의 초당 처리량(TPS) 극대화 |
| **정성 (안정성)** | 인터럽트 간 충돌로 패닉 발생 | IRQL 레벨 기반의 안전한 락킹 보장 | 고가용성 드라이버 아키텍처 완성 |

### 미래 전망
- <strong>IOCP (I/O Completion Port)와의 결합 강화</strong>: Windows 서버가 Nginx나 Node.js(libuv)를 돌릴 때 리눅스의 `epoll`에 필적하거나 그 이상으로 빠른 이유가 바로 이 커널 레벨의 DPC/APC 기반 비동기 I/O(IOCP) 덕분이다. 향후 클라우드 네이티브의 하이퍼 스케일 웹 서버 환경에서도 이 커널 비동기 큐잉 기술은 변함없는 코어로 동작할 것이다.
- <strong>eBPF for Windows</strong>: 윈도우에도 리눅스의 eBPF가 이식되고 있다. 과거에는 패킷 필터링이나 보안 감시를 위해 DPC/APC 레벨의 무거운 커널 필터 드라이버(WFP)를 짜야 했으나, 미래에는 안전한 eBPF 샌드박스가 이를 대체하여 윈도우 시스템의 블루스크린(BSOD) 공포를 획기적으로 줄여줄 것이다.

### 결론
Windows 커널의 DPC(Deferred Procedure Call)와 APC(Asynchronous Procedure Call)는 "복잡하고 무거운 작업은 하드웨어와 사용자의 눈에 띄지 않는 곳으로 숨긴다"는 운영체제 비동기 철학의 결정체다. IRQL이라는 정교한 우선순위 계단 위에서 물 흐르듯 작업을 미루고(Defer) 넘겨주는(Async) 이 톱니바퀴 설계 덕분에, 윈도우는 무거운 GUI와 수천 개의 백그라운드 서비스, 10기가비트 네트워크를 동시에 돌리면서도 마우스 커서가 끊기지 않는 마법을 유지할 수 있었다.

- **📢 섹션 요약 비유**: 쏟아지는 폭우(인터럽트)를 작은 양동이(ISR)로 막는 대신, 거대한 댐(DPC 큐)에 가둬두고 수로(APC)를 통해 필요한 논밭(스레드)으로 차분하게 흘려보내는 완벽한 치수(治水) 공학입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 안드로이드 바인더(Binder) IPC 스레드 풀 및 객체 참조 매핑 메커니즘 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| macOS/iOS Grand Central Dispatch (GCD) 블록 및 디스패치 큐 기반 동시성 구조 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 보안 엔클레이브 (TrustZone, SGX)와 OS TEE (Trusted Execution Environment) 연동 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[macOS/iOS Grand Central Dispatch (GCD) 블록 및 디스패치 큐 기반 동시성 구조]
    |
    v
[Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)]
    |
    +---> [시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조]
    +---> [보안 엔클레이브 (TrustZone, SGX)와 OS TEE (Trusted Execution Environment) 연동 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 피자 가게에 전화 주문(인터럽트)이 미친 듯이 쏟아져요. 전화를 받으면서 피자까지 만들면 전화기가 터져버릴 거예요.
2. 그래서 사장님은 일단 전화(ISR)만 1초 만에 받고 영수증을 바구니에 휙 던져놔요. 그리고 짬이 날 때마다 요리사(DPC)가 바구니에서 영수증을 꺼내 피자를 만들죠.
3. 피자가 다 구워지면 배달부(APC) 오토바이에 실어 보내요. 배달부는 손님(스레드)이 문을 열어줄 때(Alertable)까지 기다렸다가 피자를 완벽하게 전달한답니다!
