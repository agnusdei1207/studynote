+++
title = "593. 주소 공간 무작위 배치 (ASLR (Address Space Layout Randomization)) - 메모리 보안"
date = "2026-03-14"
weight = 593
+++

# 593. 주소 공간 무작위 배치 (ASLR (Address Space Layout Randomization)) - 메모리 보안

## 📋 핵심 인사이트 (3줄 요약)
> 1. **본질**: OS (Operating System) 커널이 프로세스의 주요 메모리 영역(Stack, Heap, Lib)을 실행 시점마다 무작위화(Randomization)하여, 공격자의 메모리 주소 예측을 불가능에 가깝게 만드는 확률적 방어 메커니즘입니다.
> 2. **가치**: 버퍼 오버플로우(Buffer Overflow) 등 메모리 취약점을 완전히 제거하지 않아도, ROP (Return-Oriented Programming)와 같은 공격의 성공 확률을 $1/2^{Entropy}$ 수준으로 낮춰 방어纵深(Defense in Depth)을 실현합니다.
> 3. **융합**: DEP (Data Execution Prevention)와 결합하여 Code Execution을 차단하고, 64비트 시스템의 가상 주소 공간 활용도를 극대화하여 현대 OS 보안의 표준으로 자리 잡았습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**ASLR (Address Space Layout Randomization)**은 시스템 보안의 핵심 전략인 '불확실성(Uncertainty)'을 메모리 관리에 도입한 기술입니다. 과거의 정적 메모리 모델(Static Memory Model)에서는 프로그램 실행 시 링커(Linker)에 의해 결정된 가상 주소가 매번 동일했습니다. 이는 공격자가 타겟 시스템의 환경과 무관하게 미리 작성된 익스플로잇(Exploit) 코드를 재사용할 수 있게 만들었습니다. ASLR은 이를 '동적 메모리 모델(Dynamic Memory Model)'로 전환하여, 실행될 때마다 주소 공간의 지도(Map)를 새로 그리도록 강제합니다. 이는 단순히 주소를 숨기는 것을 넘어, 공격자가 '정보 축적(Information Gathering)' 단계에서 시간과 비용을 과다하게 지불하게 만드는 경제적 방어 기법이기도 합니다.

### 2. 등장 배경 및 패러다임 시프트
- **기존 한계 (Fixed Addressing)**: 리눅스의 경우 `0x08048000`, 윈도우의 경우 `0x00400000` 등 실행 파일의 로드 주소가 표준화되어 있었고, `libc` 라이브러리 역시 고정된 영역에 로드되었습니다. 이로 인해 `Return-to-libc` 공격이 매우 용이했습니다.
- **혁신적 패러다임 (Randomization)**: 2001년 PAX 프로젝트(PaX/ASLR)와 2004년 OpenBSD의 W^X 개념을 거쳐, 2007년 윈도우 Vista, macOS 등 주요 상용 OS에 채택되었습니다. "취약점이 존재하더라도 공격을 실패하게 만든다"는 ** mitigation(완화)**의 개념을 정립했습니다.
- **비즈니스 요구 (Zero Trust)**: 오늘날 공급망 공격(Supply Chain Attack) 등 0-day 취약점이 판치는 환경에서, 소프트웨어 개발자의 실수를 OS 레벨에서 보호해주는 최후의 안전장치로 인식됩니다.

### 3. 💡 핵심 비유
ASLR은 "매일 아침 **금고의 위치를 집 안의 무작위한 장소로 이동**시키는 것"과 같습니다. 도둑(공격자)이 집 설계도(취약점)를 입수하더라도, 금고가 침실인지 부엌인지 매번 달라지기 때문에 한 번의 시도로 성공하기 불가능해집니다.

> **📢 섹션 요약 비유**: ASLR은 '보물 지도의 좌표를 매번 무작위로 재작성하여, 해적이 항해를 시작할 때마다 다른 항구를 찾아야 하게 만드는 항해 보안 시스템'과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 내부 동작 (Depth)
ASLR은 OS 커널의 **메모리 관리 유닛(MMU, Memory Management Unit)** 제어 로직과 **로더(Loader)**의 협력으로 작동합니다. 핵심은 베이스 주소(Base Address)를 결정하는 '엔트로피 소스(Entropy Source)'입니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 프로토콜/기술 | 관련 비유 |
|:---|:---|:---|:---|:---|
| **Stack (스택)** | 지역 변수, 반환 주소 저장 | `rsp`/`esp` 레지스터의 베이스를 랜덤 오프셋으로 설정 | Stack Randomization | 바닥에 흩뿌려진 카드 |
| **Heap (힙)** | 동적 할당 메모리 | `malloc` 요청 시 랜덤화된 시작 주소 반환 | Heap Randomization | 위치가 바뀌는 창고 |
| **Shared Libs (공유 라이브러리)** | 시스템 함수, API 모음 | `mmap()` 시 베이스 주소를 다단계 페이지 단위로 이동 | Library Randomization | 움직이는 서재 |
| **Executable (실행 파일)** | 프로그램 코드 영역 | **PIE (Position Independent Executable)** 컴파일 필수 | PIC (Position Independent Code) | 이사를 자주 하는 주인 |
| **VDSO / Vsyscall** | 커널 모드 진입 절차 | 고속 시스템 콜을 위한 가상 DSO 랜덤화 | Kernel Virtual Mapping | 숨겨진 비상구 |

### 2. 아키텍처 다이어그램 (Process Memory Layout)
아래는 64비트 리눅스 환경에서 PIE(Position Independent Executable)가 활성화된 프로세스의 메모리 맵이 실행 시마다 어떻게 변화하는지 도식화한 것입니다.

**[도입 서술]**
일반적인 메모리 레이아웃은 코드 영역이 하위, 스택이 상위에 고정되어 있습니다. ASLR은 이 영역들의 시작점을 Page(4KB) 단위로 쪼개어 무작위화합니다. 특히 PIE가 적용된 실행 파일(`Code`)과 공유 라이브러리(`Libs`)의 위치가 매번 달라지는 점에 주목하십시오.

```text
[ Virtual Address Space (0x0000 ... 0xFFFF) ]

   No ASLR / Standard Layout                    ASLR Applied (Run 1)              ASLR Applied (Run 2)
   -----------------------                     ----------------------            ----------------------
   | High Addresses |                          | High Addresses |               | High Addresses |
   |      ...       |                          |      ...       |               |      ...       |
   +----------------+                          +----------------+               +----------------+
   |     Stack      | <--- (Fixed Growth)      |     Stack      | (Offset A)    |     Stack      | (Offset B)
   |     (0x7FFF)   |                          |    (0x7FFF4A..)|               |    (0x7FFF82..)|
   +----------------+                          +----------------+               +----------------+
   |      mmap      | (Dynamic Libs)           |      mmap      |               |      mmap      |
   |      Region    | <--- (Fixed 0x400000)    | Shared Libs    | (0x7F1A2..)   | Shared Libs    | (0x7F45B..)
   |                |                          |  (libc.so etc) |               |  (libc.so etc) |
   +----------------+                          +----------------+               +----------------+
   |      Heap      |                          |      Heap      |               |      Heap      |
   |    (0x1000)    | <--- (Growth Upward)     |    (0x55AA1..) |               |    (0x52D34..) |
   +----------------+                          +----------------+               +----------------+
   |      BSS       |                          |      BSS       |               |      BSS       |
   |      Data      |                          |      Data      |               |      Data      |
   |      Text      | <--- (Fixed 0x08048000)  | Executable (PIE)|               | Executable (PIE)|
   |    (Code)      |                          |   (0x400000+)  |               |   (0x555500+)  |
   -----------------------                     ----------------------            ----------------------
   
   <Key>:  ↑ High Addresses                    ↑ Randomized Base                ↑ Different Base
```

**[해설]**
1.  **Stack (스택)**: 64비트 시스템에서는 매우 넓은 공간(약 140TB)을 갖기 때문에, 스택의 시작 주소를 `&rsp`에 랜덤하게 할당합니다. 이로 인해 버퍼 오버플로우 발생 시 리턴 주소를 예측하기 어렵습니다.
2.  **Shared Libs (공유 라이브러리)**: `ASLR`의 핵심입니다. `libc`, `ld-linux` 등 핵심 라이브러리의 로드 주소를 매번 변경합니다. 만약 공격자가 `system()` 함수 주소를 알아내려 한다면, 매 실행마다 메모리 누수 공격(Info Leak)을 새로 수행해야 합니다.
3.  **Executable (실행 파일)**: PIE 기술을 통해 코드 영역 자체가 재배치 가능(Relocatable)해야 합니다. 비 PIE 바이너리는 ASLR이 적용되더라도 코드 주소가 고정되어 보안 효과가 반감됩니다.
4.  **Heap (힙)**: 힙 청크(Chunk)의 시작 위치를 무작위화하여 힙 오버플로우 공격 시 메타데이터 변조를 어렵게 만듭니다.

### 3. 핵심 알고리즘 및 엔트로피 수식
ASLR의 강도는 **엔트로피(Entropy)** 비트 수로 결정됩니다. 공격자가 주소를 맞출 확률 $P$는 다음과 같이 계산됩니다.

$$ P(\text{Success}) = \frac{1}{2^{\text{Entropy}}} $$

예를 들어, 32비트 시스템에서 스택 엔트로피가 16비트라면 공격 성공 확률은 $1/65,536$입니다. 하지만 64비트 시스템에서는 스택 엔트로피가 최대 28~32비트 이상 부여될 수 있어, 무차별 대입(Brute-force)은 사실상 불가능합니다($1/10^9$ 이하).

> **📢 섹션 요약 비유**: ASLR과 PIE의 관계는 '이동식 가정집'과 같습니다. 가구(데이터)와 집(코드) 전체가 바퀴가 달려 있어서, 매번 주차장(메모리)의 다른 위치에 주차해도 내부 구조는 그대로 작동하는 원리입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: ASLR vs PIE vs DEP

| 구분 | ASLR (Address Space Layout Randomization) | PIE (Position Independent Executable) | DEP / NX (Data Execution Prevention) |
|:---|:---|:---|:---|
| **작동 레벨** | OS Kernel (메모리 로더) | Compiler / Binary (Linker) | CPU / Hardware (MMU Bit) |
| **주요 대상** | 주소 공간의 **베이스(Base)** 주소 | 실행 코드(실행 파일) 자체의 **코드 구성** | 메모리 페이지의 **권한(Bit)** |
| **목표** | 메모리의 **위치(Position)를 숨김** | 코드가 어디에 로드되든 **싖� 가능하게 함** | 데이터 영역에서의 **코드 실행을 원천 차단** |
| **의존 관계** | 단독으로도 작동하지만, PIE가 있으면 효과 극대화 | ASLR의 효과를 얻기 위해 실행 파일에 **필수적** | ASLR/PIE와 독립적으로 작동하지만, 결합 시 상승 효과 |
| **한계** | 32비트 공간 부족, Info Leak 취약 | 성능 저하(GOT/PLT 오버헤드), 호환성 문제 | JIT 컴파일러 등에서 우회 가능 |

### 2. 과목 융합 관점 (OS & Architecture & Security)
- **컴퓨터 구조 (Architecture)**: 가상 메모리(Virtual Memory)와 페이지 테이블(Page Table)의 기능이 필수적입니다. **MMU**가 가상 주소를 물리 주소로 변환하는 과정에서, OS가 Page Directory Base를 랜덤화하여 구현합니다. 즉, 하드웨어의 메모리 보호 모드가 없으면 ASLR은 존재할 수 없습니다.
- **운영체제 (OS)**: **시스템 콜(System Call)** 인터페이스와 밀접합니다. 리눅스의 `execve()` 시스템 콜이 바이너리를 메모리에 로드하면서 `randomize_va_space` 커널 파라미터를 참조하여 주소를 할당합니다. 또한, **Context Switching** 시마다 주소 공간 정보가 PCB(Process Control Block)에 관리됩니다.
- **네트워크 보안 (Network Security)**: 원격 코드 실행(RCE) 공격(예: EternalBlue)을 차단하는 마지막 방어선입니다. 공격자가 쉘코드를 주입하더라도, 어디로 점프해야 할지 모르게 하여 네트워크 패킷을 통해 침투하려는 시도를 무력화합니다.

### 3. 32비트 vs 64비트 보안 강도 분석
- **32비트 시스템**: 주소 공간이 4GB로 제한되어 있어, 스택, 힙, 라이브러리, mmap, 실행 코드 모두를 무작위화하기에 공간이 부족합니다. 엔트로피가 낮아(약 16~24비트) JIT Spraying이나 Brute-force 공격에 취약할 수 있습니다.
- **64비트 시스템**: 엄청난 주소 공간(주로 48비트, 256TB)을 활용합니다. 각 영역에 충분한 엔트로피(최소 24~32비트 이상)를 부여할 수 있어, 주소 추정이 수학적으로 불가능에 가깝습니다. 따라서 보안 전문가들은 64비트 OS 환경에서의 ASLR을 훨씬 신뢰합니다.

> **📢 섹션 요약 비유**: 32비트 환경은 '좁은 방 안에 가구를 배치하는 것'이라서 가구 위치를 섞어도 금방 찾을 수 있지만, 64비트 환경은 '광활한 사막 한가운데 모래알 하나를 숨기는 것'과 같아서 위치를 찾는 것이 거의 불가능합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 대응 전략

#### 시나리오 A: 금융권 보안 서버 구축
- **상황**: 레거시 은행 시스템(Linux 32-bit)을 최신 보안 환경으로 마이그레이션해야 함.
- **의사결정**:
    1.  OS 커널 파라미터 `kernel.randomize_va