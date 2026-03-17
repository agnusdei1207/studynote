+++
title = "254. 메모리 인터리빙 (Memory Interleaving)"
date = "2026-03-14"
weight = 254
+++

# 254. 메모리 인터리빙 (Memory Interleaving)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리적으로 분리된 복수의 메모리 모듈(뱅크)에 연속된 주소를 교차 매핑하여, 하나의 모듈이 활성화(Active)되어 있는 동안 다른 모듈을 준비(Precharge)시킴으로써 병렬성을 극대화하는 **아키텍처적 파이프라이닝** 기법이다.
> 2. **가치**: DRAM (Dynamic Random Access Memory)의 고유한 복구 지연(tRC)을 시스템 버스의 유휴 시간에서 숨겨(Hiding), 메모리 대역폭(Bandwidth)을 모듈 수(N)에 비례하여 거의 선형적으로 증가시킨다.
> 3. **융합**: 이 원리는 캐시 메모리(Cache Memory)의 Set-Associative 구조, SSD (Solid State Drive)의 멀티-채널(Multi-Channel) 컨트롤러, 그리고 고성능 스토리지의 RAID 0 (Redundant Array of Independent Disks Level 0) 스트라이핑(Striping) 기법까지 확장되는 범용 병렬 처리 패러다임이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 정의
메모리 인터리빙(Memory Interleaving)은 고속의 프로세서(CPU)와 상대적으로 저속인 메모리 간의 속도 격차(Memory Wall)를 해소하기 위해, 메모리 시스템을 **접근 단위(Access Unit)**보다 큰 **논리적 블록(Logical Block)**들로 나누고 이를 동시에 운영하는 기술이다. 단순히 메모리 용량을 늘리는 것이 아니라, **메모리 접근 횟수(Memory Access Cycles)당 전송되는 데이터 양(Throughput)**을 극대화하는 것이 핵심 목표이다. 이를 구현하기 위해 시스템은 **주소 버스(Address Bus)**의 제어 로직을 수정하여 연속된 워드(Word)들이 서로 다른 메모리 모듈에 위치하도록 주소를 배치한다.

### 💡 비유
마치 텅 빈 고속도로에 차량이 한 대씩만 달려 도로 이용률이 낮은 것을, 4차선 도로로 만들어 차량들이 끊기지 않고 이어지도록 하는 것과 같다. 단일 차선에서는 앞차가 고장 나거나 느리면 뒤차가 멈추지만, 4차선 인터리빙에서는 한 차선이 정비 중이라도 다른 차선들이 교대로 소통하여 전체 통행량(대역폭)을 유지한다.

### 등장 배경 및 기술적 필요성
1.  **CPU-메모리 속도 격차 확대 (Memory Wall)**: 프로세서의 클럭 속도는 무어의 법칙에 따라 기하급수적으로 증가했으나, DRAM은 셀의 데이터 판독 후 충전(Recharge)이 필요한 물리적 구조로 인해 지연 시간(Latency) 개선에 물리적 한계가 존재했다.
2.  **버스 대역폭의 낭비**: 기존의 단일 뱅크 구조에서는 CPU가 메모리에서 데이터를 가져오는 Read 사이클과 메모리가 다음 데이터를 준비하는 Precharge 사이클이 명확히 구분되어, 데이터가 전송되지 않는 '데드 타임(Dead Time)'이 발생했다. 고속의 시스템 버스(System Bus)가 이 데드 타임 동안 유휴(Idle) 상태로 남는 것은 심각한 자원 낭비였다.
3.  **프로그램의 국부성(Locality)**: 대부분의 프로그램은 명령어와 데이터가 물리적으로 인접한 위치에 있을 확률이 높은 **공간적 지역성(Spatial Locality)**을 가진다. 인터리빙은 이러한 순차적 접근 패턴(Sequential Access Pattern)을 이용하여, 물리적으로 분리된 메모리 모듈들이 번갈아 가며 작동하도록 유도한다.

> **📢 섹션 요약 비유**: 단일 창구 은행에서 줄이 길게 늘어지는 병목 현상을, 여러 창구에 고객을 번갈아 배정하여 대기 시간을 1/N으로 줄이는 **은행 창구 다중화(Multi-Teller Service)** 시스템과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 및 기능 (Role) | 내부 동작 메커니즘 (Internal Mechanism) | 관련 기술 및 프로토콜 (Tech/Protocol) | 실무적 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **메모리 컨트롤러 (Memory Controller)** | 주소 해석 및 명령 분배 | 주소의 특정 비트(인터리빙 비트)를 추출하여 **CS# (Chip Select)** 신호를 활성화하고, Row/Column 주소를 멀티플렉싱(Multiplexing)하여 전송 | DDR (Double Data Rate) Timing, tRC, tRCD | 교통 정리 통제관 |
| **메모리 뱅크 (Memory Bank)** | 독립적 데이터 입출력 수행 | 자신만의 Sense Amplifier와 Row Buffer를 보유하여, 다른 뱅크의 활성화/복구(Precharge) 작업과 무관하게 독립적인 Read/Write 수행 | Bank Grouping, Rank Switching | 독립적인 작업 반 |
| **인터리빙 로직 (Interleaving Logic)** | 주소 매핑(Address Mapping) | 주소 버스의 상위 비트(High Order) 또는 하위 비트(Low Order)를 선택하여 뱅크를 결정하고, 남은 비트를 뱅크 내 오프셋으로 사용 | Address Decoding | 번호표 뽑는 기계 |
| **데이터 버스 (Data Bus)** | 병렬 데이터 전송 | 각 뱅크로부터 출력되는 데이터를 시분할(Time-sharing) 하지 않고, 독립된 라인을 통해 CPU로 직접 전송 (Bus Width 증가 효과) | Burst Transfer, Data Mask | 고속도로 본선 |
| **어드레스 버스 (Address Bus)** | 요청 브로드캐스팅 | 모든 뱅크에 동일한 행(Row) 주소를 전송(Activate)하거나, 특정 뱅크에만 열(Column) 주소를 전송 | Fly-by Topology (DDR3+) | 방송 송출 시스템 |

---

### Low-Order vs High-Order 인터리빙 구조 비교

인터리빙의 성능은 주소를 어떻게 분할하느냐(Address Interleaving Scheme)에 따라 결정된다. 아래 다이어그램은 동일한 4개의 메모리 모듈에 주소 0, 1, 2, 3을 할당하는 두 가지 방식을 보여준다.

```text
      [System Address Space]
          32-bit Address
     ┌─────────────────────┐
     │ 31    ...    2  1 0 │  Bit Index
     └─────────────────────┘
           ▼      ▼  ▼ ▼
      ┌─────┐  ┌───────┐
      │ Row │  │ Bank  │
      │ Addr│  │ Sel   │
      └─────┘  └───────┘
      
  ┌─────────────────────────────────────────────────────────────────────┐
  │                     Address Mapping Architecture                    │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  [High-Order Interleaving] (상위 비트 매핑)                          │
  │  - 순차 접근 시 같은 뱅크에 집중됨 (Bank Conflict 발생 가능)          │
  │                                                                     │
  │  Bank 0: [Block 0] [Block 1] [Block 2] ...  (Starts at 0x00000000)  │
  │  Bank 1: [Block 3] [Block 4] [Block 5] ...  (Starts at 0x40000000)  │
  │  Bank 2: [Block 6] [Block 7] [Block 8] ...  (Starts at 0x80000000)  │
  │  Bank 3: [Block 9] [Block A] [Block B] ...  (Starts at 0xC0000000)  │
  │                                                                     │
  │  Address 0, 1, 2 는 모두 Bank 0 내부에 존재 -> 순차 읽기 시 병렬화 X   │
  │                                                                     │
  │  ─────────────────────────────────────────────────────────────────  │
  │                                                                     │
  │  [Low-Order Interleaving] (하위 비트 매핑) ★ 성능 핵심 ★             │
  │  - 순차 접근 시 자동으로 뱅크 교차 발생 (순차 대역폭 극대화)           │
  │                                                                     │
  │  Address Mapping: [Row] [Col] [Bank Bits(2)]                        │
  │                                                                     │
  │  Addr 00 (..00) -> Bank 0                                           │
  │  Addr 01 (..01) -> Bank 1                                           │
  │  Addr 02 (..10) -> Bank 2                                           │
  │  Addr 03 (..11) -> Bank 3                                           │
  │  Addr 04 (..00) -> Bank 0                                            │
  │  Addr 05 (..01) -> Bank 1                                            │
  │                                                                     │
  │  ▶ Result: 데이터가 Bank 0→1→2→3 순으로 쏟아져 나옴!                 │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 심층 해설]**
상위 비트(High-Order) 방식은 메모리 확장성은 좋지만, 연속된 주소(0, 1, 2...)가 모두 같은 뱅크(Bank 0)에 할당되므로 순차 접근 시에는 단일 뱅크 성능으로만 동작한다. 반면, **하위 비트(Low-Order) 방식**은 주소의 하위 2비트를 뱅크 선택 신호로 사용한다. 따라서 CPU가 0번지를 요청하면 뱅크 0이, 1번지를 요청하면 뱅크 1이 동작한다. 이로 인해 4-Way 인터리빙 시스템에서 연속된 4개의 데이터는 4개의 서로 다른 뱅크에서 완벽하게 병렬 추출된다. 이는 DRAM의 **tRC (Row Cycle Time)** 동안 발생하는 대기 시간을 다른 뱅크의 데이터로 채워주는 핵심 메커니즘이다.

---

### 인터리빙 파이프라이닝 타이밍 분석

실제적인 성능 향상은 DRAM의 동작 타이밍을 파이프라인(Pipeline)화하여 겹치게(Overlap) 만듦으로써 달성된다. 여기서는 4-Way Interleaved 시스템의 동작을 수식으로 분석한다.

*   **단일 뱅크 대역폭**: $BW_{single} = \frac{DataSize}{t_{RC}}$ (Cycle Time 동안 1개 블록 전송)
*   **인터리빙 대역폭**: $BW_{interleaved} \approx \frac{N \times DataSize}{t_{RC}}$ (단, $N \le$ Interleaving Factor)

```text
   [DRAM Internal Timing & Bus Utilization Analysis]

   Time  ->  t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
   ─────────────────────────────────────────────────────────────
   
   Request Stream:  R0   R1   R2   R3   R4   R5   R6   R7   R8
                  (Read Addr 0, 1, 2...)

   [Single Bank System - Bottleneck]
   Bank 0: [ACT/RD]---[PRE]---[ACT/RD]---[PRE]---[ACT/RD]
   Bus   :  ==D0==  [Idle]   ==D1==  [Idle]   ==D2==
   
   [4-Way Interleaved System - Pipeline]
   Bank 0: [ACT/RD]---[PRE]---[ACT/RD]---[PRE]---[ACT/RD]
            (D0 out)         (Wait)   (D4 out)
   
   Bank 1:    [ACT/RD]---[PRE]---[ACT/RD]---[PRE]---[ACT/RD]
               (D1 out)         (Wait)   (D5 out)
   
   Bank 2:       [ACT/RD]---[PRE]---[ACT/RD]---[PRE]---[ACT/RD]
                 (D2 out)         (Wait)   (D6 out)
   
   Bank 3:          [ACT/RD]---[PRE]---[ACT/RD]---[PRE]---[ACT/RD]
                   (D3 out)         (Wait)   (D7 out)
   
   System Bus:  ==D0==D1==D2==D3==D4==D5==D6==D7==D8==
                └─────────────── 100% Utilization ─────────────┘
```

**[동작 원리 코드 및 해설]**
위 그림과 같이 Bank 0이 D0를 출력하고 복구(Precharge)하는 동안, Bus는 Bank 1이 준비한 D1을, 이어서 Bank 2의 D2를 출력한다. 결과적으로 시스템 버스는 쉴 새 없이 데이터로 채워진다.

```c
// C언어적 의사 코드로 표현한 Low-Order Interleaving 주소 계산
// CPU 요청 주소: physical_address

#define NUM_BANKS 4
#define BANK_MASK 0x3  // 하위 2비트 마스크 (Binary: 11)

void memory_access(uint32_t physical_address) {
    // 1. 뱅크 선택 (하위 비트 추출)
    int target_bank = physical_address & BANK_MASK; 
    
    // 2. 뱅크 내부 오프셋 (상위 비트 시프트)
    int internal_offset = physical_address >> 2; 

    // 3. 병렬 접근 시뮬레이션
    // Bank 0은 t=0에, Bank 1은 t=1에 Active되어 파이프라인 형성
    activate_bank(target_bank, internal_offset);
}
```
이 로직에 따르면, 연속된 배열(Array)을 순회하는 `for` 루프에서는 CPU가 매 틱(Tick)마다 다른 뱅크를 선택하게 되어 메모리 병목이 제거된다.

> **📢 섹션 요약 비유**: 피자 가게에서 한 명의 직원이 도우를 만들고 구워내는 동안 손님이 기다리는 것이 아니라, 도우 만드는 사람, 소스 바르는 사람, 굽는 사람이 **조립 라인(Assembly Line)**을 이루어 흐르듯이 처리하는 생산 공정과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 심층 기술 비교: Interleaving vs Crossbar

| 비교 항목 (Criteria) | 메모리 인터리빙 (Memory Interleaving) | 크로스바 스위치 (Crossbar Switch) |
|:---:|:---|:---|
| **접속 방식** | 공용 버스(Common Bus)를 통해 뱅크가 Time