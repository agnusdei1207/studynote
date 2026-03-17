+++
title = "374. 주소 공간 무작위 배치 (ASLR)"
date = "2026-03-14"
weight = 374
+++

# 374. 주소 공간 무작위 배치 (ASLR)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **ASLR (Address Space Layout Randomization)**은 OS 커널이 프로세스 생성 시 메모리 관리 자료 구조를 조작하여 스택, 힙, 라이브러리 등의 가상 주소를 매번 무작위로 배치하는 보안 아키텍처입니다.
> 2. **가치**: 버퍼 오버플로우(Buffer Overflow)나 **ROP (Return-Oriented Programming)** 공격에서 필수적인 '메모리 주소 예측'을 엔트로피(Entropy)를 통해 원천적으로 불가능하게 만들어 시스템 안정성을 확보합니다.
> 3. **융합**: 단독으로는 우회될 수 있으나, **DEP (Data Execution Prevention)** 및 **PIE (Position Independent Executable)** 기술과 결합하여 "주소를 모르게 하고" 실행을 막는 이중 방어 체계(Depth in Defense)를 완성합니다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**1. 개념 및 철학**
**ASLR (Address Space Layout Randomization, 주소 공간 무작위 배치)**은 운영체제의 보안 메커니즘으로, 프로세스의 가상 메모리(Virtual Memory) 레이아웃을 실행 시마다 무작위로 변주(Rando-mization)하여 공격자가 코드나 데이터의 위치를 예측하지 못하게 하는 기술입니다. 과거의 보안 패러다임이 "악성 코드 실행 방어"에 집중했다면, ASLR은 "공격 대상의 위치 은폐"라는 전략적 전환을 가져왔습니다. 즉, 공격자가 아무리 정교한 공격 코드(Shellcode)를 만들더라도, 그 코드가 적중할 주소(Target Address)를 알 수 없다면 공격 자체가 무의미해진다는 철학에 기반합니다.

**2. 등장 배경: 고정 주소의 취약성**
전통적인 리눅스나 윈도우 시스템은 프로그램 실행 시 항상 동일한 가상 주소에 라이브러리와 스택을 할당했습니다(예: `libc`가 항상 `0xB7D00000`에 로드). 이는 공격자가 **RET2LIBC (Return-to-libc)** 공격 등을 통해 특정 함수 주소를 하드코딩하기만 하면 시스템을 장악할 수 있는 치명적인 취약점이었습니다. 이를 해결하기 위해 2001년 PaX 프로젝트에서 최초로 구현되었고, 현재는 Linux, Windows(Vista 이후), macOS 등 주요 OS의 표준으로 자리 잡았습니다.

**3. 기술적 상세**
ASLR은 커널의 **MMU (Memory Management Unit, 메모리 관리 장치)** 제어 권한을 사용하여 페이지 테이블(Page Table) 매핑을 동적으로 변경합니다. 이때 단순한 난수 생성이 아니라, 페이지 경계(Page Boundary)를 고려하여 성능 저하(Miss Penalty)를 최소화하면서도 충분한 주소 공간의 무질서(Entropy)를 보장하는 알고리즘을 사용합니다.

📢 **섹션 요약 비유**: 
매일 똑같은 배치로 식사가 나오는 뷔페(고정 주소)는 특정 음식(취약점)을 노리는 독가루 테러리스트에게 쉬운 표가 됩니다. 하지만 ASLR은 매일 식당 입구부터 메뉴 배치, 그릇 위치를 무작위로 바꾸어, 독가루를 들고 와도 어디에 뿌려야 할지 모르게 만드는 '동적 뷔페 배치 시스템'과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**1. 구성 요소 및 매커니즘**

ASLR은 단일 기능이 아닌 메모리의 각 영역을 독립적으로 난수화하는 하위 시스템들의 집합입니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 연관 기술/약어 |
|:---|:---|:---|:---|
| **Stack Randomization** | 스택 프레임의 시작 주소 변조 | **ESP (Stack Pointer)** 레지스터 기준 값에 난수 오프셋을 더하여 반환 주소(Return Address) 저장 위치를 매번 변경함 | Stack Canary, Guard Pages |
| **Heap Randomization** | 동적 할당 영역의 기준 주소 이동 | **Allocator (예: `malloc`)**가 요청하는 힙 영역의 베이스 주소를 프로세스 생성 시 무작위화함 | `glibc malloc`, `jemalloc` |
| **mmap() Base Randomization** | 공유 라이브러리 및 메모리 매핑 영역 이동 | **PIC (Position Independent Code)**로 빌드된 **Shared Object (.so/.dll)**의 로드 주소를 무작위화함 | **PLT (Procedure Linkage Table)**, **GOT (Global Offset Table)** |
| **PIE (Position Independent Executable)** | 실행 파일(Executable) 자체의 코드 섹션 무작위화 | 메인 실행 파일의 바이너리까지 재배치 가능하도록 컴파일 타임에 생성됨 | GCC `-fPIC -pie` 옵션 |
| **Entropy Source** | 무작위성의 수준 결정 | 시스템의 엔트로피 풀(Entropy Pool)을 참조하여 난수 시드를 생성하며, 비트 수(32비트 vs 64비트)에 따라 방어 강도가 결정됨 | **ASLR Entropy** |

**2. 메모리 레이아웃 시각화 (ASCII Diagram)**

아래는 ASLR 적용 유무에 따른 가상 메모리 매핑 변화를 도식화한 것입니다. 32비트 시스템을 기준으로 하였으며, 스택이 아래로 자라고 힙이 위로 자라는 구조(Linux 기준)를 보여줍니다.

```text
[Scenario A: ASLR OFF (Predictable)]
+---------------------------+ 0xFFFFFFFF
|      Kernel Space         |
+---------------------------+ 0xC0000000
|      Stack (Growth Down)  |
|    (Fixed: 0xBFFF... )    | <-- 공격자가 반환 주소를 정확히 알고 있음
|      [   Main()   ]       |      (예: 0xBFFFF010)
|          |                |
|          v                |
+---------------------------+ 0x40000000
|   Shared Libs (mmap)      |
| (libc.so: 0xF7E00000)     | <-- 라이브러리 주소 고정 (RET2LIBC 용이)
+---------------------------+ 0x08000000
|   Heap (Growth Up)        |
|    (Fixed: 0x0804A000)    | <-- 힙 주소 고정
+---------------------------+ 0x08048000
|   Text/Code Segment       |
|   (Executable Base)       |
+---------------------------+ 0x00000000

      ⬇️  [Activating ASLR]  ⬇️

[Scenario B: ASLR ON (Randomized)]
+---------------------------+ 0xFFFFFFFF
|      Kernel Space         |
+---------------------------+ 0xC0000000
|      Stack (Random Offset)| 
|  (Base: 0xBFFF... + A)    | <-- Offset A 무작위화
|      [   Main()   ]       |      (Stack Pointer 변조)
|          |                |
|          v                |
+---------------------------+ 0x40000000 + B
|  Shared Libs (Random Base)|
| (libc.so: 0xF7E00000 + B) | <-- Offset B 무작위화 (mmap Base 변화)
+---------------------------+ 0x08000000 + C
|   Heap (Random Base)      |
| (Start: 0x0804A000 + C)   | <-- Offset C 무작위화 (brk start 변화)
+---------------------------+ 0x08000000 + D
|  Text/Code (PIE Enabled)  | <-- PIE 적용 시 Offset D 발생
| (Executable: 0x08048000+D)| 
+---------------------------+ 0x00000000
```

**3. 심층 동작 원리 및 코드**
리눅스 커널은 `arch/x86/mm/mmap.c` 혹은 `arch/x86/kernel/process.c` 영역에서 프로세스 실행 시 `mmap_base`, `stack_base` 등을 계산합니다. 이때 단순 랜덤이 아닌, 페이지 단위(보통 4KB)로 정렬하여 성능 저하를 막습니다.

```c
/* Conceptual C Code for Linux ASLR Logic */
unsigned long get_mmap_base(struct mm_struct *mm, unsigned long random_factor) {
    // 1. 아키텍처 기본 베이스 주소 획득 (Legacy mmap base)
    unsigned long base = TASK_UNMAPPED_BASE; 
    
    // 2. 랜덤 팩터 생성 (Entropy Pool 활용)
    // 32비트 시스템: 8비트~16비트의 엔트로피 사용
    // 64비트 시스템: 30비트~40비트 이상의 엔트로피 사용
    unsigned long random_offset = random_factor;
    
    // 3. 성능 최적화를 위한 페이지 정렬 (Page Alignment Mask)
    // 4096(0x1000) 바이트 단위로 주소를 잘라내어 Page Fault 오버헤드 최소화
    // 즉, 하위 12비트는 0으로 마스킹하여 4KB 경계에 맞춤
    random_offset &= PAGE_MASK; 
    
    // 4. Stack은 Top에서 내려오므로 뺄셈, mmap은 Base에서 더함
    // (예시는 mmap Base)
    return base + random_offset;
}
```

📢 **섹션 요약 비유**: 
단순히 집의 현관문 잠금(비밀번호)을 바꾸는 것과 다릅니다. ASLR은 마치 건물의 설계도면 자체를 매일 바꾸어 엘리베이터와 계단, 화장실의 위치를 아예 다른 곳으로 이동시키는 '동적 건축 설계'와 같습니다. 침입자는 건물 안에 들어와서도 어디로 가야 할지 길을 잃게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: ASLR vs PIE**

ASLR은 운영체제가 제공하는 '무대'이고, PIE는 그 위에서 연기하는 '배우'의 적응력이라고 할 수 있습니다. 둘은 상호 보완적입니다.

| 구분 | ASLR (OS Level) | PIE (Compiler Level) | 관계 분석 |
|:---|:---|:---|:---|
| **제어 주체** | Operating System Kernel | Compiler / Linker | PIE가 없으면 ASLR만으로 실행 코드 보호 불가 |
| **적용 대상** | Stack, Heap, Shared Libraries, **VDSO** | Executable Binary (Main Program) | 일반 실행 파일(Non-PIE)은 주소 고정(0x400000) |
| **작동 방식** | 페이지 테이블 매핑 시 주소 지정 | 코드가 상대 주소(Relative Address)로 작성됨 | **PIC (Position Independent Code)** 기술이 기반이 됨 |
| **보장 효과** | 라이브러리 함수 주소 예측 불가 | 메인 프로그램 내부 함수 주소 예측 불가 | **ASLR + PIE = Full Address Space Randomization** |
| **성능 오버헤드** | 거의 없음 (초기 로딩 시 계산 비용) | 미미함 (GOT/PLT 참조를 위한 간접 점프 추가) | 현대 CPU는 간접 분기 예측으로 성능 저하 흡수 |

**2. 과목 융합 관점: OS, Architecture, Network**

*   **OS & Computer Architecture**: ASLR은 가상 메모리 기술이 전제되어야 합니다. **TLB (Translation Lookaside Buffer)**의 캐시 적중률을 유지하면서 페이지 디렉토리 베이스 레지스터(**CR3**)를 관리하는 저수준의 하드웨어 지식이 요구됩니다. 또한, 커널 모드와 유저 모드의 메모리 분리가 얼마나 견고한지에 따라 ASLR 무시가 가능할 수도 있습니다(**KASLR** 문제).
*   **Network & Exploitation**: 네트워크 해킹 시나리오에서 ASLR은 **Remote Exploit**의 난이도를 극단적으로 높입니다. 공격자는 쉘코드 삽입 후 `ret` 명령어가 가리킬 주소를 맞추기 위해 무차별 대입(Brute Force)을 시도해야 하는데, 이는 현대적인 **WAF (Web Application Firewall)**나 **IPS (Intrusion Prevention System)**에 의해 '이상 징후'로 탐지되어 차단됩니다.

**3. 정량적 지표에 따른 의사결정 (Decision Matrix)**

| 환경 변수 | 공격자 시도 횟수 (Brute Force) | 성공 확률 | 보안 등급 |
|:---|:---:|:---:|:---|
| **32-bit System (Low Entropy)** | 최소 1회 ~ 65,536회 ($2^{16}$) | 높음 (상대적) | ⚠️ 취약 |
| **64-bit System (High Entropy)** | $2^{30}$ 이상 (약 10억회) | 현실적으로 0% | ✅ 강력 |

📢 **섹션 요약 비유**: 
성벽(OS)을 높이 쌓는 것(ASLR)과 성 안의 건물(Executable)을 미리부터 해체 가능한 부품으로 만드는 것(PIE)은 별개입니다. 성벽을 높여도 성 안의 왕궁 위치를 고정하면 화살이 맞을 것이고, 건물을 해제 가능하게 만들어도 성벽이 낮으면 함락됩니다. 두 기술은 '위치의 숨김'과 '구조의 유연성'을 결합하여 완벽한 방어 태세를 갖추게 됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 과정**

*   **시나리오 A: 레거시 32비트 금융 서버 유지보수**
    *   *상황*: 32비트 RHEL 5 서버 운용 중, 커스텀 바이너리가 PIE로 컴파일되지 않아 소스 수정이 어려운 상황.
    *   *진단*: ASLR을 꺼버리면 버퍼 오버플로우 공격에 무방비해진다. 켜두면 성능 저하가 미미하지만, PIE가 없는 실행 파일은 코드 영역이 고정되어 일부 공격 경로가 노출된다.
    *   *의사결정*: `randomize_va_space` sysctl 값을 **2(Full Randomization)**로 유지한다. PIE가 아닌 메인 실행 파일은 고정되더라도, 최소한 `libc` 등 핵심 라이브러리의 주소는 무작위화하여 **ROP Chain** 구성을 어렵게 만든다. 추가적으로 **Stack Canary**와 **RELRO (Relocation Read-Only)** 옵션을 강화하여 보안 상쇄책을 마련한다.

*   **시나리오 B: 대용량 트래픽 웹 서버 구축 (64비트)**
    *   *상황*: 최신 64비트 Ubuntu �