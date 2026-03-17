+++
title = "NUR (Not Used Recently)"
date = "2026-03-14"
weight = 303
+++

# NUR (Not Used Recently) 페이지 교체 알고리즘

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: NUR (Not Used Recently)은 하드웨어의 **참조 비트(Reference Bit)**와 **수정 비트(Modified Bit)**를 결합하여 페이지의 중요도를 4단계(Class 0~3)로 분류하는 **향상된 클럭 알고리즘(Enhanced Second-Chance Algorithm)**이다.
> 2. **가치**: 단순한 시간적 지역성 추정을 넘어, 디스크 **쓰기(Write-back) 연산 비용**을 고려하여 **'Clean 페이지'를 우선 교체**함으로써 시스템의 전반적인 I/O 병목을 획기적으로 완화한다.
> 3. **융합**: 가상 메모리 관리(Virtual Memory Management)와 파일 시스템(File System)의 동기화(Synchronization) 이슈를 연결하며, 최신 OS의 백그라운드 페이징 데몬(Paging Daemon) 및 LRU 2-LIST(Active/Inactive List) 구조의 설계적 기초가 된다.

---

### Ⅰ. 개요 (Context & Background) - [600자+]

**개념 및 정의**
NUR (Not Used Recently) 알고리즘은 운영체제(OS)가 메모리 부족 상황(Memory Pressure)에 직면했을 때, 물리 메모리(Physical Memory) 내의 어떤 페이지를 디스크(Swap Area)로 교체(Eviction)할지 결정하는 페이지 교체 정책(Page Replacement Policy)의 일종이다. 이는 기본적인 클럭 알고리즘(Clock Algorithm)의 확장판으로, 단순히 '최근에 참조되지 않은 페이지'를 선택하는 것에서 나아가, '디스크에 다시 기록해야 하는지(Dirty)' 여부까지 판단하여 교체 비용(Cost of Eviction)을 최소화하는 것을 핵심 목표로 한다.

**💡 비유: 도서관의 정리 대상 선정**
이는 도서관 사서가 책장이 꽉 차서 책을 폐기해야 할 때, 단순히 "오랫동안 안 빌려간 책"만 보는 것이 아니라, "내용이 수정되어 복사본을 다시 만들어야 하는지(신품 구매 비용 발생)"까지 고려하여, "안 빌려간 책 중 원본 그대로인(클린) 책"을 먼저 폐기하는 전략과 같다.

**등장 배경: 디스크 I/O의 병목**
① **기존 한계**: 기본적인 클럭 알고리즘이나 FIFO(First-In, First-Out) 알고리즘은 페이지의 참조 시점만 고려한다. 만약 교체 대상 페이지가 메모리에서 수정된(Modified) 상태라면, OS는 이를 버리기 전에 디스크의 스왑 영역(Swap Space)에 변경 사항을 기록(Write-back)해야 한다. 디스크 접근 속도는 메모리보다 10만 배 이상 느리기 때문에, 이러한 Dirty Page의 교체는 시스템 성능 저하(Thrashing 유발 등)의 주원인이 된다.
② **혁신적 패러다임**: NUR은 **"디스크 쓰기 작업(Write I/O)이 수반되는 Dirty Page보다, 단순히 덮어쓰면 되는 Clean Page를 우선적으로 희생(Victim)시키자"**는 경제적 접근 방식을 도입했다.
③ **비즈니스 요구**: 현대의 대용량 서버 및 클라우드 환경에서는 낮은 지연 시간(Latency)과 높은 처리량(Throughput)이 필수적이므로, 페이지 폴트(Page Fault) 처리 시 발생하는 디스크 I/O를 최소화하는 NUR의 철학이 필수적이다.

> 📢 **섹션 요약 비유**
> 방을 청소할 때, '오랫동안 안 본 물건'을 버리되, 그중에서도 '내가 낙서해서 나중에 새로 사려면 돈 드는 물건(Dirty Page)'은 가급적 남기고, '낙서 하나 없는 깨끗한 잡지(Clean Page)'를 먼저 버려 돈(I/O 시간)을 아끼는 똑똑한 청소법입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,200자+]

NUR 알고리즘은 MMU (Memory Management Unit)가 자동으로 설정하는 하드웨어 비트 두 개를 조합하여 페이지 프레임(Page Frame)의 상태를 정의한다.

#### 1. 구성 요소 (표)

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/비트 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Reference Bit (R)** | 시간적 지역성 판단 | 페이지가 읽히거나(Read) 쓰일 때(Write) 하드웨어에 의해 **1**로 설정됨. 주기적으로 OS에 의해 **0**으로 초기화(Reset)됨. | 하드웨어 비트 (1/0) | **"최근 방문 여부(도장)"**: 방문자 명단에 최근 도장이 찍혔는지 여부 |
| **Modified Bit (M)** | 디스크 동기화 비용 판단 | 페이지에 데이터 쓰기(Write) 연산이 발생하면 **1**로 설정됨. Dirty 상태를 의미함. 디스크 Write-back 완료 시 **0**으로 변경됨. | 하드웨어 비트 (Dirty/Clean) | **"훼손 여부(낙서)"**: 책에 필기가 되어 있어 복사본을 만들어야 하는지 여부 |
| **Page Table Entry (PTE)** | 상태 저장소 | 각 페이지의 메타데이터를 저장하는 메모리 영역으로, 위 R 비트와 M 비트를 플래그로 보유함. | 메모리 구조 | **"사물함 태그"**: 물품의 상태를 적어둔 라벨 |
| **Clock Hand Pointer** | 순차적 스캔 | 원형 리스트(Circular List) 형태의 페이지 프레임들을 순회하며 희생양을 탐색하는 포인터. | SW 포인터 | **"순회 감독관"**: 줄을 서서 돌며 확인하는 사람 |
| **Daemon (kswapd)** | 선제적 페이지 정리 | 메모리 부족이 발생하기 전, 백그라운드에서 Dirty Page를 미리 Clean Page로 변환(Swap Out)하는 프로세스. | 백그라운드 스레드 | **"예비 요리사"**: 손님이 오기 전 미리 설거지를 해두는 역할 |

#### 2. ASCII 구조 다이어그램: 4가지 클래스 분류

NUR은 (R, M) 비트의 조합에 따라 페이지를 4개의 클래스(Class)로 나누며, 교체 우선순위는 **Class 0 > Class 1 > Class 2 > Class 3** 순서다.

```text
[NUR Page Replacement Priority Matrix]

 Modified Bit (M)
 |
 |      (Clean)         (Dirty)
 |       M=0             M=1
 |   +-----------+   +-----------+
 |   | Class (0,0)|   | Class (0,1)|
R=0 | (Not Used, |   | (Not Used, |  <-- Low Priority
(Not |  Clean)    |   |  Dirty)    |      (Victim Candidates)
Ref) |   #1 BEST  |   |   #2 OK    |
 |   +-----------+   +-----------+
 |       |                 |
 |       v                 v
 |   [No Disk Write]   [Needs Disk Write]
 |
 |
 |   +-----------+   +-----------+
 |   | Class (1,0)|   | Class (1,1)|
R=1 | (Used,     |   | (Used,     |  <-- High Priority
(Ref)|  Clean)    |   |  Dirty)    |      (Save Candidates)
 |   |   #3 SAVE  |   |   #4 SAVE  |
 |   +-----------+   +-----------+
 |       |                 |
 |       v                 v
 |  [Reuse Likely]   [Reuse Likely + Expensive to Evict]
 |
 v
```

**다이어그램 해설:**
1.  **Class 0 (R=0, M=0)**: **"이상적인 희생양(Ideal Victim)"**. 최근에 참조되지 않았고(R=0), 메모리 내용도 변경되지 않아(M=0) 디스크와 동기화가 필요 없는 상태다. 이 페이지를 교체할 때는 디스크 쓰기 작업이 전혀 필요 없으므로, Overhead가 가장 적다.
2.  **Class 1 (R=0, M=1)**: **"아쉬운 희생양(Necessary Victim)"**. 최근에 참조되지는 않았지만(R=0), 데이터가 변경되었으므로(M=1) 교체 전 디스크에 Write-back을 수행해야 한다. I/O 비용이 발생하지만, 메모리 부족을 해소해야 하므로 선택된다.
3.  **Class 2 (R=1, M=0)**: **"보호 대상(Protected Clean)"**. 최근에 참조되었으므로 지역성(Temporal Locality)이 있다고 판단하여 보존한다. 비록 M=0이지만 R=1이 우선순위가 높다.
4.  **Class 3 (R=1, M=1)**: **"최우선 보호 대상(Hot & Dirty)"**. 최근에 활발히 사용되었고 변경까지 일어났다. 이를 교체하려면 막대한 I/O 비용이 듦과 동시에 성능 저하를 유발하므로 가장 마지막에 선택된다.

#### 3. 심층 동작 원리 (알고리즘 로직)

NUR 알고리즘은 단일 패스(Single Pass)가 아닌, 필요에 따라 페이지 테이블을 여러 번 스캔할 수 있는 복합적인 로직을 가진다.

```text
[Algorithm Workflow]
1. Scan Start: Pointer가 가리키는 페이지부터 순회 시작.
2. Evaluation: 현재 페이지의 (R, M) 비트 확인.

Case A: Class 0 (0, 0) 발견 시
   -> 즉시 교체(Swap Out)하고 종료. (Best Case)

Case B: Class 0 미발견 시 (1회전 완료)
   -> 다시 처음부터 순회하며, 이번에는 R 비트를 0으로 초기화(Reset)하며 진행.
   -> 만약 이 과정에서 Class 1 (0, 1) 발견 시
      -> 해당 페이지 선택 및 디스크 기록 후 교체.
   
Case C: 그래도 실패 시
   -> 이미 모든 R 비트가 0이 되었으므로, 기존의 Class 2, 3이 Class 0, 1로 변환됨.
   -> 다시 Case A/B 로직 수행.
```

**핵심 코드 (C 스타일 의사 코드)**
```c
// PTE: Page Table Entry
struct PTE {
    bool ref_bit;  // Reference Bit
    bool mod_bit;  // Modified Bit
};

// NUR 페이지 교체 함수
int select_victim_nur() {
    while (true) {
        // 1차 스캔: Class 0 (0, 0) 탐색 (Write-back 필요 없음)
        for (int i = 0; i < num_frames; i++) {
            if (!frames[i].ref_bit && !frames[i].mod_bit) {
                return i; // 즉시 반환, 가장 빠름
            }
        }

        // 2차 스캔: Class 1 (0, 1) 탐색 및 R 비트 초기화
        for (int i = 0; i < num_frames; i++) {
            if (!frames[i].ref_bit && frames[i].mod_bit) {
                schedule_async_write(i); // 디스크 쓰기 예약
                return i;
            }
            // 이 과정에서 스캔한 페이지들의 ref_bit를 0으로 리셋
            // (다음 회차를 위해 기회 부여)
            frames[i].ref_bit = 0; 
        }
        
        // 2차 스캔을 돌고 나면 모든 R 비트가 0이 되었으므로,
        // 루프를 돌면 Class 0나 Class 1이 반드시 나옴.
    }
}
```

> 📢 **섹션 요약 비유**
> 마치 복잡한 고속도로 톨게이트에서 하이패스 차선(고속 패스)을 별도로 운영하여 병목을 해결하는 것과 같습니다. NUR은 "요금(디스크 쓰기)을 안 내도 되는 차량(Class 0)"을 우선으로 통과시켜 전체 통행료(시스템 부하)를 줄입니다. 만약 그런 차가 없으면, "요금을 내야 하지만 지금 안 타는 차(Class 1)"를 내보내고, 그동안 다른 차들의 "하이패스(R 비트)"를 리셋하여 다음 번에 우선순위를 다시 매기는 정교한 통제 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: NUR vs LRU vs FIFO

| 비교 항목 | NUR (Not Used Recently) | LRU (Least Recently Used) | FIFO (First-In, First-Out) |
|:---|:---|:---|:---|
| **핵심 메커니즘** | **참조 비트(R) + 수정 비트(M)** 조합 | **완전한 참조 시간 스탬프** (또는 Counter) | 페이지가 메모리에 들어온 순서 |
| **구현 복잡도** | 낮음 (Low): 하드웨어 지원 비트만 사용 | 매우 높음 (High): 링크드 리스트 수정 또는 스택 연산 | 매우 낮음 (Very Low): 큐(Queue) 구조 |
| **성능 (Page Fault Rate)** | **우수**: LRU와 유사한 지역성 반영 | 최고 (Best): 가장 이상적인 지역성 반영 | 낮음 (Poor): Belady's Anomaly 발생 가능 |
| **디스크 I/O 비용** | **최적화**: Clean Page 우선 선정으로 Write 최소화 | 비고만 하므로 Dirty Page 교체 가능성 높음 | 비고를 하지 않으므로 I/O 비용 예측 불가 |
| **실무 적용성** | **매우 높음**: Unix, Linux, Windows 등 대부분의 범용 OS | 거의 불가능: 전체 스캔 오버헤드가 너무 큼 | 단순한 임베디드 시스템 등에서 제한적 사용 |

#### 2. 타 과목 융합 관점 (OS & 데이터베이스)

**① 데이터베이스 시스템 (DBMS) - Buffer Management**
NUR 알고리즘은 데이터베이스의 **버퍼 관리자(Buffer Manager)**가 디스크 블록을 메모리에 캐싱할 때도 동일한 원리로 사용된다.
- **시너지**: DBMS는 **로그 순서(Log Sequence Number)**나 **테이블 스페이스(Tablespace)**의 특성을 고려하여 NUR을 변형한 **LRU-K**나 **CLOCK-Pro** 알고리즘을 사용한다. 여기서 '수정 비트(M)'는 해당 데이터 블록이 수정되었는지(Dirty)를 판단하여, **Checkpoint(체크포인트)** 시 디스크에 플러시(Flush)해야 할 페이지를 결정하는 �