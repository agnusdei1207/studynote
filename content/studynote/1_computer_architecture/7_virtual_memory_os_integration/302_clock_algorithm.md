+++
title = "클럭 알고리즘 (Clock Algorithm)"
date = "2026-03-14"
weight = 302
+++

# 클럭 알고리즘 (Clock Algorithm)

> **3-line Insight**
> 1. **본질**: 클럭 알고리즘(Clock Algorithm)은 가상 메모리 관리에서 LRU (Least Recently Used)의 구현 복잡도와 FIFO (First-In First-Out)의 단순함을 절충한 하이브리드 페이지 교체 기술로, 원형 큐(Circular Queue)와 참조 비트(Reference Bit)를 기반으로 한다.
> 2. **가치**: 하드웨어(MMU)의 지원을 받아 페이지 참조 시점을 기록하는 데 드는 오버헤드를 비트 연산 수준으로 최소화하여, 높은 페이지 적중률(Hit Ratio)과 낮은 탐색 비용(Search Cost)을 동시에 확보하는 실무 표준 솔루션이다.
> 3. **융합**: 현대 OS(Windows, Linux)의 페이지 폴트(Page Fault) 핸들러 및 메모리 리클레이머(Reclaimer)의 핵심 엔진으로, 디스크 I/O 최소화를 위한 Dirty Bit(Modified Bit)와 결합하여 시스템 전체의 처리량(Throughput)을 최적화한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
클럭 알고리즘은 운영체제(OS)가 가상 메모리(Virtual Memory)를 관리하는 과정에서, 물리 메모리(Physical Memory, RAM)가 부족하여 페이지(Pages)를 스왑 영역(Swap Area)으로 교체(Replacement)해야 할 때, **"어떤 페이지를 희생(Victim)시킬 것인가"**를 결정하는 근사 알고리즘(Approximation Algorithm)이다.
이 알고리즘의 철학은 **"최근에 참조된 페이지는 곧 다시 참조될 가능성이 높다(Locality of Reference)"**는 지역성 원리에 기반한다. 그러나 이 원칙을 완벽하게 구현하는 LRU는 모든 접근마다 타임스탬프를 갱신해야 하는 막대한 오버헤드가 발생하므로, **하드웨어가 제공하는 단일 비트(Reference Bit)**와 **소프트웨어적인 순회 포인터(Clock Hand)**를 결합하여 LRU를 효율적으로 시뮬레이션하는 것을 목표로 한다.

**2. 등장 배경: LRU의 딜레마와 해결책**
- **① 기존 한계**: 순수 LRU 구현을 위해서는 메모리 참조가 발생할 때마다 해당 페이지의 접근 시간을 갱신하거나 연결 리스트(Linked List)의 순서를 재배치해야 한다. 명령어 하나 실행하는 데 수 나노초가 걸리는 현대의 CPU 속도에서, 소프트웨어가 매번 개입하여 리스트를 조작하는 것은 성능 저하(Slowdown)의 주된 원인이 된다.
- **② 혁신적 패러다임**: 참조 비트(Reference Bit)라는 매우 단순한 하드웨어 플래그를 도입하여, "최근 사용 여부"를 0과 1로만 구분한다. 페이지 폴트(Page Fault)가 발생해 운영체제 커널(Kernel)이 개입하는 순간에만 비트를 검사하고 초기화하는 지연 전략(Lazy Evaluation)을 취한다.
- **③ 현재의 비즈니스 요구**: 범용 OS(General Purpose OS)는 다양한 워크로드(Workload)를 처리해야 하므로, 페이지 교체 알고리즘 자체가 리소스를 소비해서는 안 된다. 클럭 알고리즘은 이 **구현 단순성(Simplicity)**과 **성능 효율성(Efficiency)**의 균형을 맞춘 최적의 해법으로 자리 잡았다.

> **💡 비유**: 마치 복잡한 고속도로 톨게이트에서 모든 차량의 통행 시간을 기록하는 대신, 하이패스 차선(고속 패스)을 별도로 운영하여 병목을 해결하는 것과 같습니다.

> **📢 섹션 요약 비유**
> 방문객 명부에 방문 시간을 초 단위까지 기록하는 완벽주의자 경비원(LRU) 대신, 입장할 때 문패에 형광펜 하나만 칠해두고 나중에 형광펜이 안 닿은 사람부터 내보내는 요령 좋은 경비원(Clock)이라 할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (Component Analysis)**

| 요소명 | 역할 | 내부 동작 메커니즘 | 연관 프로토콜/용어 | 비유 |
|:---|:---|:---|:---|:---|
| **프레임 리스트 (Frame List)** | 페이지의 물리적 컨테이너 | 물리 메모리의 프레임들을 원형 큐(Circular Queue) 구조로 연결. 포인터가 끝에 도달하면 다시 처음으로 순환함. | Circular Queue | 회전초밥 벨트 |
| **시계 바늘 (Clock Hand / Pointer)** | 현재 검사 위치 가리킴 | 페이지 교체가 필요할 때 스캔을 시작하는 위치를 나타내는 포인터. 한 프레임 검사 시 다음 프레임으로 이동. | Current Pointer | 집행자의 검표 도구 |
| **참조 비트 (Reference Bit)** | 사용 여부 플래그 | MMU(Memory Management Unit)가 해당 페이지에 읽기/쓰기 발생 시 하드웨어적으로 `1`로 자동 세팅. OS는 주기적으로 `0`으로 초기화. | Use Bit, R-bit | 방문 스탬프 |
| **페이지 테이블 (Page Table)** | 주소 변환 및 메타데이터 | 가상 주소를 물리 주소로 매핑하며, 각 엔트리마다 참조 비트와 수정 비트(Modified Bit)를 포함. | Memory Management Unit | 지도 및 통계부 |

**2. 동작 아키텍처 및 데이터 흐름**

이 아키텍처는 하드웨어(MMU)와 소프트웨어(OS Kernel)의 명확한 역할 분담(Division of Responsibility)이 핵심이다.

```text
   [Hardware Layer: CPU/MMU]           [Software Layer: OS Kernel]
          |                                    ^
          | 1. Access Page                     | 4. Check Bit & Decide
          v                                    |
+-------------------+                 +-------------------+
|  Logical Address  |                 |   Page Replacement|
|       (VA)        |                 |     Algorithm     |
+--------+----------+                 +--------+----------+
          |                                    ^
          | TLB Miss / Page Write              |
          v                                    |
   +-----------------+   2. Set R=1      +------------+
   | Physical Memory | <-----------------| OS Routine |
   | [Frame: Ref=1]  |   (HW Interrupt)  | (Clock Algo)|
   +-----------------+                  +------+------+
          |                                    |
          | 3. Page Fault (Need Free Frame)    |
          ------------------------------------->

       [Circular Queue Structure - Logical View]

     +-------------------------------------------------------+
     |   [Frame 1]   [Frame 2]   [Frame 3]   [Frame 4]       |
     |  (Ref:1, M:0) (Ref:0, M:0) (Ref:1, M:1) (Ref:0, M:1)  |
     |      ^                                                        |
     |      | (Clock Pointer moves this way ->)                      |
     |      |                                                        |
     +-------------------------------------------------------+

[Scenario: Finding a Victim Page]
1. Scan Frame 1: Ref=1 -> Clear to 0 (Give second chance), Move Next.
2. Scan Frame 2: Ref=0 -> Found Victim! (Evict this).
3. Replace Frame 2 with new page, set Ref=1, M=0.
```

**3. 심층 동작 원리 (Deep Dive Mechanics)**

**단계 1: 하드웨어 트래킹 (Hardware Tracking)**
- 프로세스가 메모리에 접근하면 **MMU (Memory Management Unit)**는 해당 페이지 테이블 엔트리(PTE)의 **R-Bit (Reference Bit)**를 `1`로 설정한다.
- 이 과정은 OS 개입 없이 하드웨어적(Atomic)으로 수행되므로 오버헤드가 극히 낮다.
- 만약 페이지가 수정(Write)되었다면 **D-Bit (Dirty Bit / Modified Bit)**도 함께 `1`로 설정된다.

**단계 2: 희생자 탐색 (Victim Search)**
- 페이지 폴트(Page Fault)가 발생하여 빈 프레임이 필요할 때, OS는 **Clock Pointer**가 가리키는 프레임을 조사한다.
- **Case 1 (R=1):** 최근에 참조되었음을 의미한다. 알고리즘은 이 페이지를 즉시 쫓아내지 않고, R-bit를 `0`으로 **Clear** 한 뒤 포인터를 다음 프레임으로 이동시킨다. 이것이 바로 **"2차 기회(Second Chance)"**이다.
- **Case 2 (R=0):** 최근 한 바퀴를 도는 동안 단 한 번도 참조되지 않았음을 의미한다. 이 페이지는 즉시 **희생 페이지(Victim Page)**로 선정된다.

**단계 3: 교체 수행 (Replacement Execution)**
- 선정된 Victim 페이지가 **D=1 (Dirty)**이라면, 디스크의 스왑 영역에 내용을 기록(Page-out)하는 I/O 작업이 수반된다.
- **D=0 (Clean)**이라면 디스크 쓰기 없이 즉시 덮어쓴다.
- 새로운 페이지가 로드되면 해당 프레임의 R-bit는 `1`로 시작된다.

**4. 핵심 알고리즘 의사코드 (Pseudo-code)**

```c
// OS Kernel Page Replacement Routine
struct Frame *clock_hand = head_of_frame_list;

struct Frame* select_victim_frame() {
    while (true) {
        if (clock_hand->ref_bit == 1) {
            // 최근 사용됨: 기회를 주고 비트 클리어
            clock_hand->ref_bit = 0;
            clock_hand = clock_hand->next; // 다음 프레임으로 이동
        } else {
            // 희생자 발견 (Ref bit가 0)
            struct Frame *victim = clock_hand;
            clock_hand = clock_hand->next; // 포인터는 다음을 가리키게 유지
            return victim;
        }
    }
}
```

> **📢 섹션 요약 비유**
> 시곗바늘이 돌면서 "최근에 쓰였니(비트=1)?"라고 묻습니다. 쓰였다고 하면 "그럼 표시는 지울 테니(비트=0) 다음번 바퀴 때까지 살려두겠다" 하고 넘어가며, 만약 "표시가 지워져 있네(비트=0)?" 하면 그때는 가차 없이 내보내는 방식입니다. 1비트의 표시로 생사를 결정하는 매우 잔인하지만 효율적인 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 상세 비교 분석표**

| 비교 항목 | FIFO (First-In First-Out) | LRU (Least Recently Used) | **Clock Algorithm** |
|:---|:---|:---|:---|
| **구현 복잡도** | 매우 낮음 (단순 큐) | 매우 높음 (타임스탬프/리스트) | **중간 (큐 + 비트)** |
| **하드웨어 오버헤드** | 없음 | 매우 높음 (매 접근시 갱신) | **낮음 (비트 셋만 HW 처리)** |
| **성능 (Hit Ratio)** | 낮음 (Belady's Anomaly 발생 가능) | 가장 높음 (Optimal에 근접) | **중상~높음 (LRU 근사)** |
| **최악의 시나리오** | 자주 쓰이는 페이지가 교체됨 | 오버헤드로 인한 시스템 느려짐 | **모든 비트가 1일 시 FIFO와 동일** |
| **실무 사용 여부** | 거의 사용 안 함 | 캐시(Cache) 메모리 등 일부 | **범용 OS 메모리 관리 표준** |

**2. 시너지 및 오버헤드 분석 (Convergence)**

- **과목 융합: 컴퓨터 구조 (Computer Architecture)와의 관계**
  클럭 알고리즘은 **TLB (Translation Lookaside Buffer)**의 **LRU 교체 정책**과 성격이 다르다. TLB는 하드웨어적으로 매우 빨라야 하므로 진짜 LRU를 구현하지만(회로 복잡도 감수), 주 메모리는 소프트웨어(OS)가 관리하므로 **Clock Algorithm**을 사용하여 **명령어 파이프라인(Instruction Pipeline)**의 스톨(Stall)을 방지한다. 만약 주 메모리에서 하드웨어 LRU를 강제하면 CPU의 명령어 사이클(Cycle)이 메모리 갱신 작업 때문에 늘어나 전체 시스템 성능이 저하된다.

- **과목 융합: 데이터베이스 (Database Buffer Management)**
  DBMS의 버퍼 관리자(Buffer Manager) 또한 유사한 알고리즘을 사용한다. 특히 **LRU-K** 알고리즘처럼 최근 K번의 참조 히스토리를 고려하는 방식은 클럭 알고리즘의 참조 비트 개념을 확장한 것으로 볼 수 있다.

**3. 성능 메트릭 (Quantitative Metrics)**
- **탐색 비용 (Search Cost)**: 최악의 경우(All R=1) 리스트의 전체 길이(N)를 순회해야 하므로 $O(N)$이지만, 평균적인 경우(Watermark 이하)는 매우 빠르게 Victim을 찾는다.
- **공간 복잡도 (Space Complexity)**: 페이지당 1비트(Ref Bit)만 추가로 필요하므로, 타임스탬프(8 bytes)를 사용하는 것에 비해 메모리 오버헤드가 **약 1/64 수준**으로 획기적으로 낮다.

> **📢 섹션 요약 비유**
> LRU가 모든 물건의 사용 시간을 초 단위로 기록하는 무거운 전자장부라면, 클럭 알고리즘은 물건을 만질 때 먼지만 털어주고, 나중에 먼지가 소복이 쌓인(비트=0) 물건만 골라서 버리는 가벼운 먼지떨이 기법입니다. 정확성은 조금 부족해도 처리 속도가 훨씬 빠릅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 트리**

시스템 엔지니어가 메모리 관리 전략을 수립할 때 다음과 같은 의사결정이 필요하다.

**[시나리오 A: 고성능 웹 서버 (High Throughput Web Server)]**
- **상황**: 대부분의 요청이 정적 파일(Static Content)이며, 이미 캐싱된 데이터가 주를 이룬다.
- **의사결정**: 페이지 폴트가 드물게 발생하므로, 기본 클럭 알고리즘으로 충분하다.
- **판단 이유**: 복잡한 Enhanced Clock을 사용하여 Ref/Dirty 비트를 모두 검