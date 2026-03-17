+++
title = "380. 가비지 컬렉션 (Garbage Collection) 기초"
date = "2026-03-14"
weight = 380
+++

# 380. 가비지 컬렉션 (Garbage Collection) 기초

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 더 이상 참조되지 않는 동적 메모리 객체(Garbage)를 시스템이 자동으로 회수하여 재사용하는 메모리 관리 메커니즘이며, 개발자로부터 메모리 해제의 부담을 완전히 또는 부분적으로 해제시키는 기술입니다.
> 2. **가치**: **Double Free**나 **Dangling Pointer** 같은 치명적인 메모리 오류를 사전에 차단하여 시스템 안정성을 확보하고, 생산성을 비약적으로 증대시키나, **Stop-the-World (STW)**로 인한 지연 시간(Latency) 튜닝이 필수적인 성능 트레이드오프 관계에 있습니다.
> 3. **융합**: OS의 가상 메모리 관리와 밀접하게 연결되며, 컴파일러 타임과 런타임 환경의 상호작용(Write Barrier, Card Table 등)을 통해 최적화되는 고도화된 시스템 소프트웨어 아키텍처의 핵심입니다.

---

### Ⅰ. 개요 (Context & Background)

**가비지 컬렉션(Garbage Collection, GC)**은 컴퓨터 과학에서 자동 메모리 관리(Automatic Memory Management)의 핵심 기술로, 더 이상 사용되지 않는 메모리 객체(Garbage)를 시스템이 자동으로 탐지하고 회수(Reclamation)하여 재사용 가능한 메모리 풀(Memory Pool)로 반환하는 프로세스입니다. 수동 관리 방식(Manual Memory Management, 예: C언어의 `malloc`/`free`)에서는 개발자가 객체의 생명주기(Lifecycle)를 직접 제어해야 하므로, 복잡한 참조 관계에서 **Memory Leak**(메모리 누수), **Dangling Pointer**(야생 포인터), **Buffer Overflow** 등의 보안 취약점과 시스템 불안정성을 유발할 위험이 큽니다. GC는 이러한 부담을 런타임(Runtime) 환경의 **GC Engine**이 담당하게 하여 소프트웨어의 안정성과 개발 생산성을 동시에 확보합니다.

#### 💡 비유
마치 초대장 없는 무단 투숙객을 찾아내려고 경비원이 건물 전체를 수동으로 순찰하는 것이 아니라, 스마트 호텔 시스템이 투숙 기록이 끊긴 객실을 자동으로 인식하여 청소부(Garbage Collector)를 배치해 정리하고, 다음 손님을 위해 즉시 예약 가능 상태로 변경하는 자동화된 관리 시스템과 같습니다.

**등장 배경**:
1.  ① **기존 한계**: 하드웨어 성능이 발전함에 따라 소프트웨어 규모가 거대해지면서, 수동 메모리 관리의 복잡도가 기하급수적으로 증가. 복잡한 포인터 연결 고리 끊어짐으로 인한 누수 누적 및 서비스 장애(Out of Memory, OOM)가 빈번하게 발생함.
2.  ② **혁신적 패러다임**: 1959년 John McCarthy가 Lisp 개발 과정에서 최초로 GC 개념을 도입한 이후, 추상화된 메모리 관리를 통해 개발자가 비즈니스 로직에만 집중 가능하도록 개발 패러다임을 전환시킴.
3.  ③ **현재의 비즈니스 요구**: 클라우드(Cloud) 및 빅데이터 환경에서 대규모 힙(Heap) 메모리(수백 GB ~ TB)를 효율적으로 관리해야 하며, 24/365 무중단 서비스를 위해 **Stop-the-World** 시간을 최소화하는 Low-Latency GC 기술이 필수적인 요구사항으로 부상함.

📢 **섹션 요약 비유**: 호텔 객실(메모리)에서 투숙객(데이터/객체)이 나가고 키(참조)를 반납하지 않아도, IoT 센서(GC)가 이를 감지하고 청소팀을 자동으로 투입하여 다음 손님을 위해 방을 즉시 비워주는 고도화된 자동화 관리 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

GC의 핵심 기술적 난제는 '어떤 객체가 가비지인지 식별하는가(Identification)'와 '회수된 메모리를 어떻게 효율적으로 재할당하는가(Allocation)'입니다. 이를 해결하기 위해 현대적 GC는 크게 **Reference Counting**(참조 카운팅)과 **Tracing GC**(추적식 GC) 두 가지 패러다임으로 나뉘며, 성능 최적화를 위한 **Generational Hypothesis**(세대별 가설)를 기반으로 동작합니다.

#### 1. 핵심 구성 요소 (GC Subsystems)
| 요소명 (Full Name) | 역할 | 내부 동작 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **Mutator** | 애플리케이션 실행 스레드 | 객체 생성 및 필드 참조 업데이트 수행, **Write Barrier**(쓰기 장벽) 실행을 통해 GC에게 변경 사항 통지 | 사용자 비즈니스 로직 실행부 |
| **Allocator** | 메모리 할당자 | 힙(Heap) 영역의 **Free List** 또는 **Bump Pointer** 기법을 사용하여 빠른 메모리 할당 수행 | TLAB(Thread-Local Allocation Buffer) 사용 가능 |
| **Collector** | GC 엔진 코어 | Root Set으로부터 그래프 탐색(Tracing)을 통해 객체 마킹, 스위핑, 압축(Compaction) 수행 | **STW(Stop-the-World)** 유발 주체 |
| **Root Set** | 탐색 시작점 그룹 | 스택(Stack) 로컬 변수, 전역 변수, 스태틱 필드, JNI 참소 등 절대 회수되지 않는 기준점 | 그래프 탐색의 루트 노드 |
| **Write Barrier** | 참조 변경 감시자 | Mutator가 객체 간 참조를 수정할 때 이를 감지하여 **Card Table**이나 **Remembered Set**에 기록 | Generational GC의 핵심 최적화 요소 |

#### 2. 핵심 아키텍처: Tracing GC (Mark-and-Sweep)
가장 널리 사용되는 **Tracing GC**의 기본 원리는 그래프 탐색을 통해 살아있는 객체를 찾아내는 것입니다.

**[ASCII Diagram: Tracing GC Flow (Mark-and-Sweep)]**
```text
      [Root Set] (Stack, Globals) ---> 그래프 탐색 시작
          |
          v
    +-----------+       (참조: Reference)       +-----------+
    |  Object A |------------------------------>|  Object C |
    +-----------+  (Mark Bit: 1 - Alive)        +-----------+
       (Marked)             ^                        (Marked)
          |                 |
          |                 | (순환 참조: Circular Ref)
          |                 |
    +-----------+           |
    |  Object B |-----------+
    +-----------+
    (Marked)

    -----------------------------------------
    [Heap Memory Scan (Sweep Phase)]
    -----------------------------------------
    +-----------+           +-----------+
    |  Object X |           |  Object Y |
    +-----------+           +-----------+
    (Mark Bit: 0)          (Mark Bit: 0)
    (Unreachable)          (Unreachable)
         |                       |
         v                       v
    [Freed to List]         [Freed to List]
```
1.  **Mark Phase (마킹 단계)**: Root Set부터 시작하여 DFS(Depth-First Search) 또는 BFS(Breadth-First Search) 알고리즘을 통해 도달 가능한 모든 객체의 헤더에 'Mark Bit'를 설정합니다. 이 과정에서 힙 내의 모든 살아있는 객체 그래프를 순회하므로, 객체 수가 많을 경우 CPU 자원을 많이 소모합니다.
2.  **Sweep Phase (소멸 단계)**: 힙(Heap) 전체를 선형(Linear)으로 순회하며 Mark Bit가 설정되지 않은(Unreachable) 객체를 메모리에서 해제하고 **Free List**에 반환합니다.

#### 3. 심층 최적화: Generational GC (세대별 수집)
모든 객체를 검사하는 것은 비효율적입니다. **Generational Hypothesis**("대부분의 객체는 수명이 짧다")에 기반하여 힙을 세대별로 분리합니다.

**[ASCII Diagram: Generational Heap Layout & Promotion]**
```text
+---------------------------------------------------------------+
|                    VIRTUAL MEMORY SPACE (Heap)                |
|                                                               |
|  +--------------------------+      +------------------------+ |
|  |     Young Generation     |      |    Old Generation     | |
|  |  (Short-lived Objects)   |      |   (Long-lived Objects)| |
|  |                          |      +------------------------+ |
|  |  +--------+ +--------+   |              ^  Promotion      | |
|  |  |  Eden  | |Survivor|   |              | (Minor -> Major) | |
|  |  | Space  | |  S0/S1  |   |              |                 | |
|  |  +--------+ +--------+   |              |                 | |
|  +--------------------------+              |                 | |
|         |        ^                       /                   | |
|         |        | Copy/Scavenge        /                    | |
|         +--------+                     /                     | |
|          (Minor GC, Frequent)         /                      | |
|                                     /                       | |
|                                    /                        | |
|  (Major GC / Full GC, Infrequent but Expensive)             | |
+---------------------------------------------------------------+
```
- **Young Generation**: 생명주기가 짧은 객체가 할당됨. **Eden** 영역이 가득 차면 **Minor GC**가 발생하며, 살아남은 객체는 **Survivor** 영역으로 이동(Copying GC)됨.
- **Old Generation**: Young Gen에서 일정 횟수 이상 생존한 객체가 승격(Promotion)됨. 공간이 크기 때문에 **Major GC** 발생 시 시간이 오래 걸리지만 빈도는 낮음.

#### 4. 핵심 알고리즘 및 코드
다음은 **Mark-and-Sweep** 알고리즘의 핵심 로직을 의사 코드(Pseudo-code)로 표현한 것입니다.

```python
# GC Algorithm Pseudo-code: Mark-and-Sweep
# Global Variable
heap = [...] # Entire Heap Memory

def gc_collect():
    # 1. Stop-the-World (Mutator Pause)
    pause_mutators()

    # 2. Mark Phase: Root Set부터 그래프 순회
    for root in Root_Set:
        mark_object(root)

    # 3. Sweep Phase: 전체 힙 스캔 및 회수
    freed_bytes = 0
    for object in heap:
        if not object.is_marked:
            free(object) # Memory Deallocation
            freed_bytes += object.size
        else:
            object.is_marked = False # 다음 사이클을 위해 플래그 리셋

    # 4. Resume World
    resume_mutators()
    log_gc_stats(freed_bytes)

def mark_object(obj):
    # 이미 방문했거나 null이면 종료 (Cycle 방지)
    if obj is None or obj.is_marked:
        return
    
    obj.is_marked = True # Mark 설정
    
    # 객체 내의 모든 참조 필드(포인터)를 재귀적으로 탐색
    # Write Barrier에 의해 보호됨
    for ref in object.references:
        mark_object(ref)
```

📢 **섹션 요약 비유**: 도서관(메모리) 사서(GC)가 대출 기록(참조 관계)을 확인하여 정리하는 과정입니다. 정리하려면 독자(Mutator)들이 모두 밖으로 나가야(STW) 하지만, 독자들이 계속 책을 빌리고 반납하는 동안에도 사서가 조용히 카탈로그만 수정하여(Marking) 정리할 수 있게 하거나, 신간은 별도 칸대(Young Gen)에 두어 자주 정리하고, 고전은 서고(Old Gen)로 옮겨 가끔 정리하는 식의 효율적인 운영 전략입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

GC 기술은 단순한 런타임 라이브러리를 넘어, OS의 가상 메모리(Virtual Memory) 관리, CPU의 캐시(Cache) 계층 구조와 밀접하게 상호작용하며 전체 시스템 성능을 좌우합니다.

#### 1. 핵심 기술 비교: GC 알고리즘 심층 분석

| 구분 | Reference Counting (참조 카운팅) | Mark-and-Sweep (추적 방식) | Compacting (압축) & Copying |
|:---|:---|:---|:---|
| **동작 방식** | 객체 생성/파괴 시 참조 횟수 증감. 0 시 즉시 회수. | Root로부터 연결된 객체를 추적(Mark) 후 나머지 해제(Sweep). | 살아있는 객체를 새로운 영역으로 복사하여 메모리를 연속적으로 배치. |
| **성능 특성** | **Real-time**: 회수 지연 없음. 하지만 참조 변경마다 오버헤드 발생. | **Burst**: STW에 의한 일시적 멈춤 발생. Throughput 중심. | **High Allocation**: 복사 비용이 들지만, 압축으로 인해 할당 속도(Bump Pointer)가 매우 빠름. |
| **주요 장점** | 즉시 회수, 별도의 STW 불필요, 구현 단순. | 순환 참조(Circular Reference) 처리 가능, 전체 힙 관리 효율. | **Fragmentation**(단편화) 해결, Cache Locality(캐시 지역성) 개선. |
| **주요 단점** | **순환 참조 불가**, 오버헤드 큼, Thread Safety 비용. | 전체 힙 스캔으로 인한 지연 시간 길어짐, 단편화 발생 가능. | 메모리 공간을 1/2만 사용 가능(Copying 시), 복사 비용. |
| **대표 언어/환경** | Python, Swift, Objective-C (ARC) | Ruby, V8 (Chrome JS), Lua | Java (G1, ZGC), Go, .NET |

#### 2. 과목 융합 관점 (OS & Computer Architecture)
- **가상 메모리(Virtual Memory) 및 Paging과의 관계**:
    - GC의 Sweep 단계에서 물리 메모리가 해제되면 OS의 **Page Table** 갱신이 필요합니다.
    - 대규모 힙을 가진 시스템에서 GC 실행 중 다량의 페이지 접근이 발생하면 **Page Fault**가 폭주하여 디스크 I/O가 발생하고, 이는 시스템 전체의 **Thrashing** 현상으로 이어질 수 있습니다.
- **CPU Cache Locality (캐시 지역성)**:
    - Mark-and-Sweep 알고리즘은 객체가 힙에 흩어져 있을 경우(Scattered) **Cache Miss**가 빈번하여 CPU 성능을 저하시킵니다.
    - **Compacting GC**는 객체를 물리적으로 연속된 메모리 공간으로 모으기 때문에, CPU가 연속된 메모리 라인을 가져오는 **Spatial Locality(공간 지역성)**을 극대화하여 연산 속도를 높입니다.

#### 3. 메모리 단편화(Memory Fragmentation) 해결 과정 시각화

**[ASCII Diagram: Fragmentation vs Comp