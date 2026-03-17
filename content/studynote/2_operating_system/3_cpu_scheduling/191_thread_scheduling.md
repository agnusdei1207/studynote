+++
title = "[OS] 191. 스레드 스케줄링 (Thread Scheduling)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Thread Scheduling", "PCS", "SCS", "Kernel Level Thread"]
weight = 191
+++

# [OS] 스레드 스케줄링 (Thread Scheduling)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스레드 스케줄링은 CPU (Central Processing Unit)의 할당 단위를 중량급 프로세스에서 경량급 스레드로 전환하여 문맥 교환(Context Switching) 오버헤드를 줄이고 병렬성을 극대화하는 핵심 메커니즘입니다.
> 2. **가치**: 다중 코어 환경에서 **PCS (Process-Contention Scope)**와 **SCS (System-Contention Scope)**를 적절히 분리 및 통합 관리하여 애플리케이션의 응답 속도(Latency)와 처리량(Throughput)을 동시에 만족시킵니다.
> 3. **융합**: 커널 레벨 스케줄링과 사용자 레벨 라이브러리의 상호작용을 통해 가상화 및 클라우드 환경의 리소스 분배 효율을 결정짓는 OS의 심장부입니다.

+++

### Ⅰ. 개요 (Context & Background)

스레드 스케줄링이란 운영체제가 프로세서의 실행 시간을 할당함에 있어, 무거운 프로세스 단위가 아닌 **스레드(Thread, Light Weight Process)** 라는 더욱 작은 실행 단위를 대상으로 수행하는 결정 과정을 의미합니다.

전통적인 프로세스 중심의 스케줄링에서는 각 프로세스가 독립적인 주소 공간과 자원을 소유하여 문맥 교환 시 막대한 오버헤드(캐시 플러시, **TLB (Translation Lookaside Buffer)** 플러시 등)가 발생했습니다. 반면, 스레드는 같은 주소 공간을 공유하므로 스레드 간 전환은 훨씬 가볍습니다. 따라서 현대 OS는 이 경량성을 활용하여 다중 처리(Multiprocessing)와 병행성(Concurrency)을 극대화하고자 합니다. 여기서 중요한 개념은 '누가 스케줄링을 주도하는가'에 따라 그 범위(Scope)가 나뉜다는 점입니다.

**💡 비유**
이는 거대한 공장(프로세스) 안에서 일하는 작업자(스레드)들을 관리하는 시스템과 같습니다. 과거에는 공장 전체를 단위로 작업 지시를 내렸다면, 이제는 개별 작업자에게 직접 지시를 내려 작업 교체 시간을 획기적으로 줄이는 방식입니다.

**등장 배경**
1.  **기존 한계**: 단일 프로세스 스케줄링은 멀티태스킹 환경에서 빈번한 메모리 복사/복원으로 인한 성능 저하를 초래함.
2.  **혁신적 패러다임**: **LWP (Lightweight Process)** 개념의 도입과 사용자 수준 스레드 라이브러리(예: Pthreads)의 발전으로 애플리케이션 레벨에서의 스케줄링 필요성 대두.
3.  **현재 요구**: 클라우드 및 대규모 서버 환경에서 수천 개의 요청을 실시간으로 처리하기 위해 초미세 세분화(CPU Granularity)된 스케줄링이 필수적이 됨.

**📢 섹션 요약 비유**
마치 관공서의 창구가 '부서(프로세스)' 단위에서 '담당자(스레드)' 단위로 업무 분장이 바뀌면서, 민원인이 기다리는 시간을 줄이고 창구의 가동률을 높이는 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스레드 스케줄링의 아키텍처는 크게 경쟁 범위(Contention Scope)에 따라 **PCS (Process-Contention Scope)**와 **SCS (System-Contention Scope)**로 분류되며, 이는 스레드 모델(Many-to-One, One-to-One, Many-to-Many)과 밀접한 관계가 있습니다.

#### 1. 구성 요소 상세 분석

| 요소명 | 역할 | 내부 동작 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **ULT (User-Level Thread)** | 애플리케이션 로직의 실행 흐름 | 사용자 공간 라이브러리에 의해 관리되며, 커널은 이의 존재를 직접 인지 못함 | POSIX Threads (Pthreads) | 공장 내부 팀원 |
| **KLT (Kernel-Level Thread)** | 커널이 스케줄링할 수 있는 실제 실행 단위 | 시스템 콜이나 인터럽트 처리를 위해 커널에 의해 직접 관리됨 | OS Kernel Scheduler | 정규직 등록된 직원 |
| **LWP (Lightweight Process)** | 사용자 스레드와 커널 스레드 간의 가상 인터페이스 | ULT가 시스템 자원을 요청할 때 이를 중계하여 KLT로 매핑 | Unix System V | 가상의 업무 종이 |
| **Thread Library** | 사용자 수준 스케줄링 담당 | PCS 환경에서 스레드 간 실행 순서를 결정하고 Context Saving을 수행 | GNU Pth, Win32 threads | 팀장(인력 배치표) |
| **Scheduler Activation** | 커널과 라이브러리 간의 동기화 매커니즘 | 커널이 이벤트(예: 페이지 폴트)를 알려주면 라이브러리가 스레드를 재스케줄링 | Upcall Mechanism | 본사의 긴급 공지 |

#### 2. 스케줄링 경쟁 범위 아키텍처 다이어그램
아래는 Many-to-Many 모델에서의 PCS와 SCS의 상호작용을 도식화한 것입니다. 사용자 스레드는 PCS 영역에서 경쟁하여 가용 LWP를 확보하고, LWP는 SCS 영역에서 다른 프로세스의 LWP들과 경쟁하여 CPU를 할당받습니다.

```text
   [ User Space : PCS (Process-Contention Scope) ]
   +-------------------------------------------------------+
   | Application Process                                   |
   |  +-------+  +-------+  +-------+  +-------+           |
   |  | U-Thread A1|  | U-Thread A2|  | U-Thread A3|  |   | <-- Library Run Queue
   |  | (Runable) |  | (Blocked) |  | (Runable) |  |   |
   |  +----+-------+  +----+-------+  +----+-------+  |   |
   |       \               |                /        |   |
   |        \              |               /         |   |
   |         +-------------+--------------+          |   |
   |                       |                         |   |
   |                       v                         |   |
   |  +----------------------------------------------------+ |
   |  |  LWP 1   |  LWP 2   |  LWP 3   |   (Virtual CPU)    | |
   |  +-----+---------+---------+---------+------------+   | |
   +--------|---------|---------|---------|------------|-----+
            |         |         |         |            |
   =========|=========================================|======== [ Kernel Boundary ]
            |         |         |         |            |
            v         v         v         v            v
   [ Kernel Space : SCS (System-Contention Scope) ]
   +-------------------------------------------------------+
   | Kernel Scheduler (O(1), CFS)                          |
   |  +-------+  +-------+  +-------+  +-------+           |
   |  | KLT 1 |  | KLT 2 |  | KLT 3 |  | ...   | <-- Global Run Queue
   |  +---+---+  +---+---+  +---+---+  +---+---+           |
   +------|---------|---------|---------|-----------------+
          |         |         |         |
          v         v         v         v
   [ Hardware : CPU Core 0, 1, 2, ... ]
```

#### 3. 심층 동작 원리
1.  **PCS 동작 (User-Level)**: 애플리케이션은 스레드 라이브러리를 통해 자신만의 **Ready Queue (대기열)**를 유지합니다. 스레드 A가 I/O 작업 등으로 블록(Block)되면, 라이브러리는 즉시 같은 프로세스 내의 다른 스레드 B를 LWP에 연결하여 실행합니다. 이때 커널은 개입하지 않으므로 매우 빠릅니다.
2.  **SCS 동작 (Kernel-Level)**: 모든 LWP(또는 KLT)는 커널의 글로벌 **Run Queue**에 등록됩니다. CPU는 유휴 상태가 되면 이 큐에서 다음 LWP를 선택합니다. 이때는 프로세스 간의 우선순위, CPU 타임 슬라이스, 캐시 친화성(CPU Affinity) 등이 복합적으로 고려됩니다.
3.  **매핑(Mapping) 및 전달**: 만약 PCS에서 스케줄링 가능한 스레드는 있는데 할당된 LWP가 부족하다면, 라이브러리는 커널에 새로운 LWP를 요청합니다. 반대로, LWP가 할 일이 없으면 커널은 이를 회수하여 다른 프로세스에게 제공할 수 있습니다.

#### 4. 핵심 알고리즘 및 코드
다음은 스케줄러 결정을 내리는 가상의 로직을 C 언어 스타일로 표현한 것입니다. PCS와 SCS의 결정 지점을 확인하십시오.

```c
// [Pseudo-code: Hybrid Scheduler Decision Logic]

void schedule_next_thread() {
    // 1. PCS Level Decision (User Space Library)
    if (current_thread.state == BLOCKED) {
        // 현재 스레드가 블록되면 같은 프로세스 내의 다른 스레드 검색
        Thread* candidate = find_ready_thread_in_process(current_process);
        
        if (candidate != NULL) {
            // LWP가 가용하다면 즉시 교체 (Context Switch仅在User Stack)
            switch_to(candidate); 
            return; // 커널 진입 없음
        }
    }

    // 2. SCS Level Decision (Kernel Space)
    // 더 이상 실행할 스레드가 없거나 Time Quantum이 만료된 경우
    if (need_reschedule()) {
        // 커널 모드 진입 후 시스템 전체 대기열에서 경쟁
        LWP* target_lwp = kernel_scheduler.pick_next_lwp();
        
        if (target_lwp->process != current_process) {
            // 주소 공간이 다르면 TLB Flush 등 무거운 작업 수반
            switch_address_space(target_lwp->process->page_table);
        }
        
        dispatch_context(target_lwp);
    }
}
```

**📢 섹션 요약 비유**
마치 대형 쇼핑몰(시스템)의 주차장(CPU)을 이용하는 것과 같습니다. PCS는 각 매장(프로세스) 내부에서 직원(스레드)들끼리 '골판지 박스 운반차(LWP)'를 누가 쓸지 싸우는 내부 경쟁이고, SCS는 모든 매장의 차량이 주차장 입구에서 누가 먼저 들어갈지 겪는 외부 경쟁입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: PCS vs SCS

| 비교 항목 | PCS (Process-Contention Scope) | SCS (System-Contention Scope) |
|:---|:---|:---|
| **스케줄링 주체** | 사용자 수준 스레드 라이브러리 (예: Pthreads 라이브러리) | 운영체제 커널 (OS Kernel) |
| **경쟁 상대** | 동일한 프로세스 내의 다른 스레드들 | 시스템 전체의 모든 스레드/KLT |
| **문맥 교환 속도** | 매우 빠름 (User Stack만 교체) | 상대적으로 느림 (Kernel Stack, Registers, TLB 등) |
| **커널 개입 여부** | 없음 (Non-preemptive within process) | 필수 (Preemptive Scheduling) |
| **주요 장점** | 스케줄링 오버헤드가 적어 스위칭이 빠름 | 전체 시스템의 부하를 균등하게 분산 및 병렬 처리 가능 |
| **주요 단점** | 하나의 스레드가 블록되면 프로세스 전체가 정될 수 있 | 잦은 커널 모드 전환으로 인한 오버헤드 발생 |

#### 2. 과목 융합 관점
*   **OS & 데이터베이스 (DB)**: 데이터베이스 서버(예: Oracle, PostgreSQL)는 **Multi-threaded Architecture**를 사용합니다. PCS를 통해 각 클라이언트 요청을 처리하는 사용자 스레드를 빠르게 전환하고, SCS를 통해 백그라운드 작업(Checkpoint, WAL Writing)을 별도의 KLT로 분리하여 전체 DBMS의 처리량(Throughput)을 저해하지 않도록 설계됩니다.
*   **OS & 네트워크 (Network)**: 웹 서버(예: Nginx, Apache Event MPM)는 수만 개의 연결을 처리해야 합니다. **SCS**를 통해 각 코어에 워커 스레드(KLT)를 고정(CPU Affinity)시켜 캐시 적중률을 높이고, 각 워커 내부에서는 이벤트 기반의 **PCS** 로직을 사용하여 비동기 I/O를 처리하는 하이브리드 모델이 주류입니다.

**📢 섹션 요약 비유**
PCS는 '부서 내 업무 협조'라면, SCS는 '전사 간 차량 배정'입니다. PCS는 팀 내 유연함을, SCS는 회사 전체의 형평성과 안정성을 담당합니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정
*   **시나리오 1: 대규모 I/O 바운드 웹 서버 구축**
    *   **문제**: 수십만 개의 동시 접속자를 처리해야 하며, 각 연결은 대부분 I/O 대기 상태임.
    *   **의사결정**: **Many-to-Many 모델** 또는 **One-to-One 모델 + 비동기 I/O** 채택. SCS(OS)가 제공하는 KLT 수를 물리 코어 수에 맞춰 최적화하고, 애플리케이션 레벨(PCS)에서 수많은 가상 스레드(Green Thread 등)를 생성해 대기열을 관리하도록 설계.
    *   **이유**: 커널 스레드를 무한정 생성하면 Context Switching 비용이 폭증하여 성능이 급락(Thrashing)함.

*   **시나리오 2: 고성능 연산 엔진 (HPC, 게임 서버)**
    *   **문제**: CPU 연산이 많고(CPU-bound), 캐시 locality가 성능에 지대한 영향을 미침.
    *   **의사결정**: