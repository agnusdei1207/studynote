+++
title = "페이지 교체 알고리즘 (Page Replacement)"
date = "2026-03-14"
weight = 300
+++

# 페이지 교체 알고리즘 (Page Replacement)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 운영체제(OS, Operating System)의 가상 메모리(Virtual Memory) 관리 핵심 기술로, 한정된 물리 메모리(Physical Memory) 자원을 초과하여 요청된 페이지(Page)를 디스크(Swap Area)와 교환하는 Swapping 메커니즘이다.
> 2. **가치**: 적절한 교체 정책 선정을 통해 디스크 I/O 병목을 완화하여 전체 시스템의 처리량(Throughput)을 극대화하고, 지역성(Locality)을 활용하여 페이지 폴트율(Page Fault Rate)을 최소화한다.
> 3. **융합**: 계산 이론(Computing Theory)의 최적화 문제와 컴퓨터 구조(Computer Architecture)의 하드웨어 지원(Reference Bit 등)이 결합된 분야로, 최근 DBMS의 버퍼 관리(Buffer Replacement)와 캐싱(Caching) 전략으로 응용된다.

---

## Ⅰ. 개요 (Context & Background)

페이지 교체(Page Replacement)는 운영체제(OS, Operating System)가 요구 페이징(Demand Paging) 환경에서 가상 메모리의 페이지를 물리 메모리의 프레임(Frame)에 로드하려 할 때, 가용한 빈 프레임(Free Frame)이 존재하지 않을 경우 기존 페이지 중 하나를 선택하여 보조 기억 장치(Backing Store)로 내보내고(Swap-out), 그 자리에 새로운 페이지를 로드(Swap-in)하는 핵심 관리 기법이다.

현대 컴퓨터 시스템은 주기억장치(Main Memory)의 용량 한계로 인해 모든 프로세스의 이미지를 상주시킬 수 없다. 따라서 OS는 프로세스를 페이지(Page)라는 고정 크기 단위로 분할하고, 필요할 때만 메모리에 적재하는 전략을 취한다. 문제는 메모리가 가득 찼을 때 발생한다. 어떤 페이지를 내보낼지 결정하는 알고리즘의 품질에 따라 시스템의 성능이 결정된다. 잘못된 페이지 교체는 자주 참조되는 페이지를 디스크로 내쫓게 만들어, 결과적으로 디스크 I/O가 빈번히 발생하고 CPU가 데이터를 기다리며 놀게 되는 '스래싱(Thrashing)' 현상을 초래할 수 있다.

### 💡 기술적 배경 및 발전
1.  **기존 한계 (Overlays & Swapping)**: 초기에는 전체 프로세스를 통째로 디스크와 교환하는 Swapping 방식을 사용했으나, 메모리 낭비가 심하고 Context Switching 비용이 컸다.
2.  **혁신적 패러다임 (Paging & Virtual Memory)**: 프로그램의 논리적 주소 공간(Logical Address Space)과 물리적 주소 공간(Physical Address Space)을 분리하여, 불연속적인 메모리 할당을 가능하게 하고 물리 메모리보다 큰 프로그램 실행을 지원하게 되었다.
3.  **현재의 비즈니스 요구 (Performance)**: 빅데이터 및 AI 워크로드의 등장으로 메모리 압박이 심해짐에 따라, 단순한 교체 알고리즘을 넘어 Learning-based Replacement 등 지능형 접근이 연구되고 있다.

> 📢 **섹션 요약 비유**
> 한정된 크기의 서재 책장(물리 메모리)에 새로운 책(새 페이지)을 꽂으려면, 가장 덜 중요하거나 다시 읽을 일이 없을 것 같은 책을 골라창고(디스크)로 옮겨야 하는 공간 관리 전략과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

페이지 교체는 OS의 메모리 관리자(Memory Manager)와 MMU(Memory Management Unit) 하드웨어가 긴밀히 협력하여 수행된다. 페이지 폴트(Page Fault) 트랩(Trap)이 발생하면 OS는 인터럽트 처리 루틴(Interrupt Service Routine)을 통해 교체 과정을 주도한다.

### 1. 시스템 구성 요소 분석
| 요소명 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 (Internal Operation) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **PMAT (Page Map Address Table)** | 논리-물리 주소 매핑 | TLB(Translation Lookaside Buffer) 캐시 미스 시 참조되며, Valid/Invalid 비트와 Frame 번호 관리 | 서재의 도서 대장 (책이 어디 있는지 위치표) |
| **Modify Bit (Dirty Bit)** | 쓰기 여부 플래그 | CPU가 해당 프레임에 **Store** 명령을 실행할 때 HW에 의해 **1**로 Set. Swap-out 시 디스크 기록 여부 결정 | 책에 필기가 있는지 확인 (필기 있으면 그대로 두면 안됨) |
| **Reference Bit** | 사용 여부 플래그 | 주기적인 인터럽트 또는 클럭 알고리즘 순회 시 참조 여부를 **0**으로 Reset하며, **1**이면 최근 사용됨 | 책장을 스쳐본 흔지 확인 (최근에 손이 갔는지) |
| **Swap Space** | 보조 기억 장치 | 디스크(Disk) 내의 독립된 영역으로, 메모리 페이지가 저장되는 Backing Store 역할 수행 | 지하 창고 (본창고에 못 넣은 책 보관함) |

### 2. 페이지 교체 프로세스 상세 (ASCII 다이어그램)

아래 다이어그램은 페이지 폴트(Page Fault) 발생 시 OS가 수행하는 Swap-out/Swap-in의 전체 흐름을 도식화한 것이다.

```text
       CPU (User Process)                      OS Kernel (Memory Manager)
         |                                                 |
    1. Access Logical Addr 'X'                            |
         |                                                 |
         v                                                 |
    [ MMU : TLB Lookup ]                                  |
         | (Not Found)                                     |
         v                                                 |
    [ Page Table Check ] --(Valid Bit: 0)--> Page Fault Trap---+
         |                                                 |   |
         |                                                 |   v
         |                                         +---------------+
         |                                         | Page Fault    |
         |                                         | Handler ISR   |
         |                                         +---------------+
         |                                                 |
         |                        --------------------------+--------------------------
         |                        |                          |                        |
         |                        v                          v                        |
         |                2. Find Victim Frame      3. Check Dirty Bit    4. Find Free Page on Disk
         |                [Replacement Algorithm]    (Swap-out Decision)    [Backing Store Scan]
         |                        |                          |                        |
         |                        |                          +----+                    |
         |                        |                               |                    |
         |                        |                               v                    |
         |                        |                    (If Dirty=1) Write Back to Disk  |
         |                        |                          (Disk I/O Write)          |
         |                        |                               |                    |
         |                        v                               v                    v
         |                 (Evict Victim) <--- Wait --- (Disk Write Complete)
         |                        |
         |                        +------------------------------------> |
         |                                                             |
         |                        5. Read Target Page from Disk (Swap-in)
         |                        |                                         |
         |                        v                                         |
         |                 [Disk I/O Read]                                  |
         |                        |                                         |
         |                        v                                         v
         |             [Load to Free Frame] <-- Physical Memory Update
         |                        |
         |                        v
         |                6. Update Page Table
         |                        |
         +------------------------+--------------------------> Restart Instruction
```

**[해설]**
1.  **Trap 발생**: CPU가 유효하지 않은 페이지에 접근하면 MMU는 OS에 Page Fault 예외를 발생시킨다.
2.  **희생자 선정 (Victim Selection)**: 메모리에 빈 공간이 없으므로, 교체 알고리즘(FIFO, LRU 등)에 따라 희생 페이지(Victim Page)를 선정한다.
3.  **Dirty Check 및 Swap-out**: 선정된 프레임의 Dirty Bit를 확인한다. 값이 1이면 메모리 내용이 변경된 상태이므로 디스크에 기록(Swap-out)해야 데이터 손실을 막을 수 있다. 0이면 디스크에 이미 최신본이 있으므로 기록을 생략한다. 이는 디스크 쓰기 연산을 줄여 성능을 높이는 핵심 최적화 로직이다.
4.  **Swap-in 및 매핑 갱신**: 디스크에서 요청된 페이지를 읽어 해제된 프레임에 적재하고, 페이지 테이블을 갱신(Valid Bit=1, Frame Number 업데이트)한 뒤 명령어를 재시작한다.

### 3. 핵심 알고리즘 코드 및 수식
페이지 폴트율(Page Fault Rate)은 아래와 같이 정의되며, 이를 최소화하는 것이 알고리즘의 목적함수(Objective Function)이다.

$$ \text{Page Fault Rate} = \frac{\text{Total Page Faults}}{\text{Total Memory Accesses}} $$

```c
// [Pseudo-code: Second-Chance Clock Algorithm Logic]
// 하드웨어 지원을 받는 가장 대중적인 LRU 근사 알고리즘

void page_replacement() {
    while (true) {
        // 현재 Clock Hand가 가리키는 페이지 확인
        Page current_page = frames[clock_hand];

        if (current_page.ref_bit == 1) {
            // 1단계: 최근 참조됨 -> 기회 부여 (Bit를 0으로 초기화 후 통과)
            current_page.ref_bit = 0;
            clock_hand = (clock_hand + 1) % total_frames;
        } else {
            // 2단계: 참조되지 않음 -> 희생자 선정 (Swap-out 진입)
            if (current_page.dirty_bit == 1) {
                disk_write(current_page); // Dirty Page면 디스크에 기록
            }
            swap_in(new_page, current_page.frame_index); // 새 페이지 로드
            current_page.ref_bit = 1; // 새 페이지는 당연히 참조됨
            break;
        }
    }
}
```

> 📢 **섹션 요약 비유**
> 진열장(메모리) 정리 과정이다. 관리자(OS)는 손님(CPU)이 요청한 물건이 없으면 창고에서 가져온다. 그런데 진열장이 꽉 차 있다면, '방금 손님이 만졌던 상품(Ref Bit=1)'은 아직 필요할 수 있으니 표시만 해두고 넘어가고, '아무도 안 만진 상품(Ref Bit=0)'을 골라내어 만약 상품에 손때가 묻었다면(Dirty=1) 닦아서 포장한 뒤 창고로 보낸다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

페이지 교체 알고리즘은 "Stack Algorithm" 성질을 가지느냐에 따라 성능 보장성이 달라지며, 계산 이론적으로 Belady's Anomaly 현상 유무로 구분된다.

### 1. 심층 기술 비교 분석표
| 비교 항목 | FIFO (First-In First-Out) | OPT (Optimal Algorithm) | LRU (Least Recently Used) |
|:---|:---|:---|:---|
| **동작 원리** | 메모리에 먼저 적재된 페이지를 교체. Queue 구조. | 미래에 참조되지 않을 시간이 가장 긴 페이지를 교체. | 과거에 가장 오랫동안 참조되지 않은 페이지를 교체. |
| **필요 정보** | 적재 시간(Load Time). | 미래의 참조 패턴(Future Reference String). | 최근 참조 이력(Past Reference History). |
| **Belady's Anomaly** | **발생함** (프레임 수를 늘려도 Page Fault 증가 가능). | 발생하지 않음 (Stack Algo). | 발생하지 않음 (Stack Algo). |
| **구현 난이도** | 매우 쉬움 (단순 포인터 이동). | 불가능함 (Offline Algorithm). | 어려움 (Counter나 List 구조 필요). |
| **주요 용도** | 단순한 시스템, 버퍼 캐시의 일부. | 성능 비교의 상한선(Benchmark). | 범용 OS 메모리 관리 (Linux, Windows). |

### 2. Belady's Anomaly 시각화 (ASCII)
벨라디의 모순은 페이지 프레임 수를 늘렸음에도 불구하고 페이지 폴트가 증가하는 역설적인 현상을 말한다. FIFO에서 주로 발생한다.

```text
[Scenario] Reference String: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5

[Case 1: Frames = 3 (FIFO)]
Ref:  1    2    3    4    1    2    5    1    2    3    4    5
F1:   [1]  [1]  [1]  [4]  [4]  [4]  [5]  [5]  [5]  [3]  [3]  [3]
F2:        [2]  [2]  [2]  [1]  [1]  [1]  [1]  [1]  [1]  [4]  [4]
F3:             [3]  [3]  [3]  [2]  [2]  [2]  [2]  [2]  [2]  [5]
Fault: ^    ^    ^    ^    ^    ^    ^         ^    ^    ^    ^
Total Faults: 9

[Case 2: Frames = 4 (FIFO)] <-- Memory Increased!
Ref:  1    2    3    4    1    2    5    1    2    3    4    5
F1:   [1]  [1]  [1]  [1]  [1]  [1]  [5]  [5]  [5]  [5]  [4]  [4]
F2:        [2]  [2]  [2]  [2]  [2]  [2]  [1]  [1]  [1]  [1]  [5]
F3:             [3]  [3]  [3]  [3]  [3]  [3]  [2]  [2]  [2]  [2]
F4:                  [4]  [4]  [4]  [4]  [4]  [4]  [3]  [3]  [3]
Fault: ^    ^    ^    ^              ^    ^    ^    ^    ^    ^
Total Faults: 10 (Increased!) <-- Belady's Anomaly Detected
```

### 3. 과목 융합 관점
*   **OS & 컴퓨터 구조 (Architecture)**: LRU를 완벽하게 구현하기 위해서는 매 메모리 접근마다 시간스탬프를 기록해야 하므로 하드웨어 오버헤드가 크다. 따라서 TLB의 Hit Ratio를 높이기 위해 참조 비트(Reference Bit)와 같은 하드웨어적 지원을 받는 'Approximate LRU'가 설계된다.
*   **데이터베이스 (DB)**: DBMS의 Buffer Management에서도 동일한 교체 알고리즘이 사용된다. 다만 DB는 데이터 일관성이 중요하므로 Dirty Page를 비우는(Checkpoint) 전략이 로그(Log)와 결합하여 더 복잡하게 설계된다.

> 📢 **섹션 요약 비유**
> FIFO는 아무리 진열장을 더 사와도(Frames 증가