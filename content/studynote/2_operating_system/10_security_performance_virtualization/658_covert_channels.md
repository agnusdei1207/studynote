+++
title = "658. 커버트 채널 (Covert Channels)"
date = "2026-03-16"
weight = 658
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "커버트 채널", "Covert Channel", "은닉 채널", "정보 유출"]
+++

# 커버트 채널 (Covert Channels)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 커버트 채널은 **시스템의 설계 의도가 아닌 비인가 경로**를 통해 정보를 은밀하게 전송하는 통신 메커니즘이며, 이는 **TCB (Trusted Computing Base)**의 격리 실패를 의미합니다.
> 2. **가치**: 단순한 버그가 아니라 **공유 자원(Shared Resource)**의 본질적 속성에서 기인하며, 최신 멀티코어 및 클라우드 환경에서 **크로스-VM (Cross-VM) 공격** 등 고도의 APT(Advanced Persistent Threat) 경로로 악용됩니다.
> 3. **융합**: **오디팅(Auditing)**, **넌덤(Nondeterminism)** 도입, **흐름 제어(Flow Control)** 등 운영체제 보안 정책의 핵심 과제이며, 하드웨어 아키텍처(CPU, 캐시)와 밀접하게 연관된 복합 보안 이슈입니다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**커버트 채널 (Covert Channel)**이란 시스템의 보안 정책(Security Policy)을 설계된 의도와 다르게 우회하여, 허가되지 않은 주체 간에 정보를 전송할 수 있는 통신 경로를 의미합니다.
일반적인 통신 채널(Overt Channel)과 달리, 커버트 채널은 시스템의 자원 공유 메커니즘이나 부작용(Side-effect)을 악용하여 데이터를 유출합니다. 이는 **BLP (Bell-LaPadula Model)**와 같은 강제적 접근 통제(Mandatory Access Control) 모델에서 *"No Read Up, No Write Down"* 규칙을 위협하는 주요 요소로, 고보안 등급(High)의 프로세스가 저보안 등급(Low)의 프로세스로 정보를 몰래 보내는 경로가 됩니다.

### 2. 등장 배경 및 역사
- **1970년대 Lampson의 문제 제기**: Butler Lampson은 1973년 "A Note on the Confinement Problem" 논문에서 **Confined Program**(격리된 프로그램)이 데이터를 외부로 유출할 수 있는 가능성을 최초로 지적했습니다.
- **TCSEC (Trusted Computer System Evaluation Criteria)**: 미 국방부의 오렌지 북(Orange Book) 등 컴퓨터 보안 평가 기준에서 커버트 채널 분석 및 대책이 A1 등급 시스템의 필수 요구사항으로 자리 잡았습니다.
- **현대적 진화**: 클라우드 가상화 및 멀티코어 환경에서 **공유 캐시(Shared Cache)**, **쓰로틀링(Throttling)** 등을 악용한 고대역폭 커버트 채널이 심각한 문제로 대두되었습니다.

### 3. 💡 핵심 비유: '감옥의 두드러기 벽'
보안 격리된 시스템은 **'철저히 감시되는 감옥'**과 같습니다. 죄수(고위권 프로세스)는 간수(보안 커널)의 눈을 피해 외부 사람(저위권 프로세스)에게 말을 전할 수 없습니다. 하지만 죄수가 감옥의 벽을 특정 패턴으로 두드리면(Storage Channel: 상태 변화), 간수가 그 내용을 모르더라도 밖에서 대기하는 동료가 그 소리의 패턴(Timing Channel: 시간 간격)을 듣고 메시지를 해독할 수 있습니다. 간수는 벽을 두드리는 행위 자체를 막을 수 없으며, 소리(부수적 효과)만으로 정보가 새어 나가게 됩니다.

### 4. ASCII 다이어그램: 보안 모델 위배 상황
아래 다이어그램은 **BLP 모델**의 보안 규칙을 커버트 채널이 어떻게 우회하는지 시각화한 것입니다.

```text
      [ 보안 정책 (BLP Model) ]
      High Level  ────────────────X  (No Write Down: 금지됨)
         ▲                                    │
         │ (직접 경로는 차단됨)                │
         │                                    ▼
      Low Level  <========================│ (정보 유출 성공)

      [ 커버트 채널 (우회 경로) ]
      High Level ──(자원 변조)──> [ 공유 자원 ] ──(상태 감지)──> Low Level
         (Trojan)                (File Lock,      (Spy)
                                  CPU Load,
                                  Cache State)
      
      * 설명: High 프로세스는 공유 자원(파일, 캐시 등)의 상태를 '0' 또는 '1'로
        변조하여 Low 프로세스가 이를 관찰하게 함으로써 비트를 전송합니다.
```
**(해설)**
위 다이어그램에서 상위 프로세스는 하위 프로세스로 데이터를 직접 쓰기(Write)할 수 없습니다. 하지만 상위 프로세스가 공유 자원(예: 잠금 파일 생성)의 상태를 변경하면, 하위 프로세스는 단순히 그 자원이 존재하는지 혹은 접근 가능한지를 확인(`access()` 호출)함으로써 1비트의 정보를 획득합니다. 이때 시스템 관리자(커널)는 데이터 전송 자체를 인지하지 못하며, 자원 사용의 부수적 효과만이 관찰됩니다.

### 📢 섹션 요약 비유
이 섹션에서 다룬 내용은 **"물탱크의 미세한 균열"**과 같습니다. 아무리 단단한 법적 접근 제어(물탱크 벽)를 세워도, 시스템 자원을 공유하며 발생하는 미세한 상태 변화(균열)를 통해 물은(정보는) 끊임없이 샜 나가게 됩니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 커버트 채널의 분류 및 작동 메커니즘
커버트 채널은 크게 **Storage Channel**과 **Timing Channel**로 분류되며, 최근에는 이를 복합한 **Memory-based Channel**이 주목받고 있습니다.

#### A. Storage Channel (저장 채널)
- **정의**: 송신자가 공유 저장 공간의 상태(예: 파일 잠금, 디스크 여유 공간, 특정 레지스터 값)를 변경하여 정보를 저장하고, 수신자가 그 상태를 읽는 방식입니다.
- **특징**: 비트가 공유 객체의 상태에 '저장'되므로 수신자가 읽을 때까지 값이 유지됩니다.

#### B. Timing Channel (타이밍 채널)
- **정의**: 송신자가 시스템 자원(CPU, 버스)을 점유하거나 해제하여 **시간적 간격(Interval)**을 조작하고, 수신자가 특정 연산의 수행 시간(Latency)을 측정하여 정보를 획득하는 방식입니다.
- **특징**: 상태가 물리적으로 저장되지 않고, **부하(Load)의 시간적 분포**에 정보가 인코딩됩니다.

#### C. 구성 요소 상세 분석표

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/메커니즘 | 실제 비유 |
|:---|:---|:---|:---|:---|
| **Sender (Trojan)** | 정보 전송자 | 보안 데이터를 비트 스트림으로 변환하여 공유 자원을 조작 | `Lock/Unlock`, `Busy Wait` | 전신을 치는 사람 |
| **Receiver (Spy)** | 정보 수신자 | 공유 자원의 상태나 지연 시간을 모니터링하여 비트 복원 | `access()`, `RDTSC` | 전신 소리를 듣는 사람 |
| **Shared Resource** | 매개체 (Medium) | 두 프로세스 간에 접근 가능한 시스템 자원 | File, Lock, Cache, Bus | 벽면 (전달 매체) |
| **Synchronization** | 클럭/동기화 | 비트 경계를 구분하기 위한 신호 | Implicit/Explicit Clocking | 약속된 시간 간격 |
| **Noise Source** | 방해 요인 | 채널 용량을 저하시키는 비결정적 요인 | OS Scheduler, Random Load | 주변 소음 |

### 2. ASCII 다이어그램: Storage vs Timing Channel 구조

```text
      [ 1. Storage Channel Example (File Lock) ]
      
      High (Trojan)                    Low (Spy)
         │                                 │
         │  Data '1'를 보내려함             │
         │                                 │
         ├─> open("secret.lock") ──┐       │
         │                         │       │
         │                         ▼       │
         │                     [ OS Kernel ]
         │                    (Lock Acquired)
         │                         │       │
         │                         │       ├─> access("secret.lock")
         │                         │       │    (Return: 0 -> Exists!)
         │                         │       │
         │                         │       ▼  (Bit '1' 수신)
         │                         ▼
         └─> close("secret.lock") ──┘

      ==========================================================

      [ 2. Timing Channel Example (CPU Load) ]
      
      High (Trojan)                    Low (Spy)
         │                                 │
         │  Data '1' (Heavy Load)          │
         │                                 │
         ├─> while(1) { sqrt(); } ────> [ Shared CPU Bus ]
         │      (Heavy Computation)          (High Contention)
         │                                      │
         │                                      ▼
         │                                 Low: count_time()
         │                                 (측정된 시간: 100ms)
         │                                 (Bit '1': Long Latency)
         │
         │  Data '0' (Idle)
         │
         └─> sleep(1) ───────────────> [ Shared CPU Bus ]
         │      (Yield CPU)                 (Low Contention)
         │                                      │
                                        Low: count_time()
                                        (측정된 시간: 10ms)
                                        (Bit '0': Short Latency)
```

**(해설)**
Storage 채널은 **'상태(State)'**를 기반으로 합니다. High 프로세스가 `flock()` 시스템 호출을 통해 잠금을 획득하면, Low 프로세스는 단순히 `flock()`을 시도하여 실패(EAGAIN) 여부를 확인함으로써 '1'을 읽습니다. 반면 Timing 채널은 **'시간(Time)'**을 기반으로 합니다. High 프로세스가 의도적으로 연산을 수행하여 CPU 버스를 점유하면, Low 프로세스의 동일한 연산 수행 시간이 느려지는(Slowdown) 현상을 이용합니다. 이때 Low 프로세스는 `TSC (Time Stamp Counter)` 레지스터를 읽어 고해상도 시간을 측정해야 합니다.

### 3. 심층 동작 원리: 캐시 기반 커버트 채널 (Cache-based Covert Channel)
최근의 멀티코어 환경에서 가장 위험한 커버트 채널은 **L3 Cache (Last Level Cache)**를 공유하는 구조에서 발생합니다. 이는 **Prime+Probe** 또는 **Flush+Reload** 기술로 구현됩니다.

**핵심 알고리즘 (Flush+Reload)**
```c
// [Sender] 고위험 프로세스 (공유 라이브러리 이용)
for (i = 0; i < data_size; i++) {
    if (secret_bit[i] == '1') {
        // 해당 캐시 라인을 캐시에 로드함
        _mm_clflush(&shared_array[i]); // Flush 후 Access
        access(&shared_array[i]); 
    } else {
        // 아무것도 하지 않음 (Idle)
    }
    sync(); // 동기화
}

// [Receiver] 저위험 프로세스
for (i = 0; i < data_size; i++) {
    start = rdtsc(); // 시작 시간 측정
    access(&shared_array[i]); // 메모리 접근 시도
    end = rdtsc();   // 종료 시간 측정
    
    if (end - start < THRESHOLD) {
        // Cache Hit 발생! -> Sender가 해당 데이터를 썼음
        recovered_bit = '1';
    } else {
        // Cache Miss -> Sender가 쓰지 않았음
        recovered_bit = '0';
    }
}
```
*(주석: `rdtsc`는 Read Time-Stamp Counter 명령어로 CPU 클럭 수를 반환합니다. 임계값(THRESHOLD)은 캐시 히트(Cache Hit)와 미스(Miss)의 시간 차이를 기준으로 설정됩니다.)*

### 📢 섹션 요약 비유
캐시 기반 커버트 채널의 작동 원리는 **"도서관의 좌석 예약"**과 같습니다. A(고위험)가 특정 좌석(캐시 라인)에 앉아있으면 B(저위험)가 그 자리에 가려고 할 때 즉시 앉을 수 있지만(캐시 히트, 빠름), A가 자리에 없으면 B가 책꽂이(메모리)에서 책을 꺼내와야 하므로(캐시 미스, 느림) 시간이 걸립니다. B는 단순히 자리에 앉는 시간만 재고서 A가 그 자리에 있었는지 확인할 수 있는 것입니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: Storage vs Timing Channel

| 비교 항목 (Criteria) | Storage Channel (저장 채널) | Timing Channel (타이밍 채널) |
|:---|:---|:---|
| **데이터 보존성** | 상태가 유지됨 (Stateful) | 순간적이며 사라짐 (Stateless) |
| **전송 대역폭** | 상대적으로 낮음 (디스크 I/O 제약) | 매우 높음 (CPU 클럭 수준 가능) |
| **감지 난이도** | 비교적 쉬움 (자원 사용량 이상 감지) | 매우 어려움 (정상 부하와 유사) |
| **대표적 공유 자원** | 파일 시스템, IPC 메시지 큐 | CPU 스케줄러, 네트워크 대기열 |
| **완화 기법** | Resource Partitioning (격리) | Fixed Scheduling, Noise Injection |

### 2. 과목 융합 관점

**A. 운영체제(OS)와 컴퓨터 구조(Computer Architecture)의 시너지**
- **OS 관점**: 프로세스 스케줄링(Scheduling) 알고리즘은 **TCT (Time-Driven Covert Channel)**의 핵심입니다. FCFS(First Come First Served) 스케줄러는 예측 가능한 지연 시간을 제공하여 타이밍 채널의 대역폭을 높입니다.
- **구조 관점**: CPU의 **명령