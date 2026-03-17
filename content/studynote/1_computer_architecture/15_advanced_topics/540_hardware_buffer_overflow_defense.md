+++
title = "540. 버퍼 오버플로우 하드웨어 방어 (Intel CET 등)"
date = "2026-03-14"
weight = 540
+++

# 540. 버퍼 오버플로우 하드웨어 방어 (Intel CET 등)

### # [버퍼 오버플로우 하드웨어 방어]
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어적 방어(ASLR, Stack Canary)만으로는 방어가 불가능해진 고급 코드 재사용 공격(ROP, JOP)을 차단하기 위해, CPU (Central Processing Unit) 명령어 세트 아키텍처(ISA) 차원에서 제어 흐름 무결성(CFI: Control-Flow Integrity)을 하드웨어적으로 강제하는 보안 설계다.
> 2. **가치**: SW (Software) 에뮬레이션 방식은 10~20%의 성능 저하를 유발했으나, HW (Hardware) CFI(Indirect Branch Tracking, Shadow Stack) 방식은 성능 손실을 1~2% 이하로 억제하면서도 메모리 손상 공격의 90% 이상을 원천 봉쇄한다.
> 3. **융합**: MSVC, GCC (GNU Compiler Collection), LLVM (Low Level Virtual Machine) 같은 최신 컴파일러 툴체인과 연동되며, OS (Operating System) 커널의 스케줄러 및 메모리 관리자(MMU: Memory Management Unit)와 밀접하게 결합하여 '하드웨어 강제 스택 보호' 생태계를 구축한다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 버퍼 오버플로우 하드웨어 방어는 프로그램의 실행 흐름을 가로채는 공격(CWE-120, CWE-128)을 막기 위해, CPU 내부에 '정상적인 제어 흐름(CFG: Control Flow Graph)'에 대한 위변조 검증 로직을 탑재한 기술이다. 기존 OS 레벨의 페이지 보호(DEP: Data Execution Prevention)나 주소 난수화(ASLR: Address Space Layout Randomization)가 우회당함에 따라, 명령어 실행 주기(Fetch-Decode-Execute) 사이에 하드웨어적 체크점을 추가하여 악의적인 분기(Branch)를 실행 즉시 차단한다.
- **💡 비유**: 마치 보안이 철저한 금고 회사의 출입 시스템과 같다. 종이 출입부(일반 스택)에 위조된 도장(악성 코드 주소)을 찍는다 해도, 입구에 설치된 생체 인식기(하드웨어 검증기)가 대조용 DB(Shadow Stack)와 실시간으로 교차 검증하여, 일치하지 않으면 즉시 방범 창을 닫아버리는 방식이다.
- **등장 배경**:
  1. **고급 공격의 등장**: 해커들이 코드를 직접 삽입하는 것에서 벗어나, 이미 메모리에 존재하는 정상 명령어 조각(Gadget)을 사슬처럼 엮어 실행하는 ROP (Return-Oriented Programming)가 대두되었다.
  2. **SW 방어의 한계**: 소프트웨어적으로 모든 간접 분기(Indirect Branch)를 추적하는 것은 명확한 성능 저하를 초래했다. 이를 해결하기 위해 Intel과 AMD가 CPU 자체에 보안 논리를 내장한 CET (Control-flow Enforcement Technology)와 Shadow Stack을 도입했다.
  3. **사이버 보안 패러다임 변화**: 'Zero Trust' 및 'Defense in Depth(심층 방어)' 전략에 따라, 커널 드라이버부터 사용자 영역 애플리케이션까지 하드웨어 보안 루트 of Trust를 적용하려는 산업적 요구가 반영되었다.

```text
   [일반적인 보안 기술의 진화 계보]

      1990s                  2000s                    2020s
 +------------------+  +-----------------------+  +------------------------------+
 | Stack Smashing   |  | Exploit Mitigation    |  | Hardware-Enforced Security   |
 | (Shellcode)      |  | (ASLR, DEP, Canary)   |  | (Intel CET, AMD Shadow Stack)|
 +------------------+  +-----------------------+  +------------------------------+
       |                        |                          |
       v                        v                          v
 [코드 삽입]                 [주소 변조]               [흐름 무결성 검증]
 "악성 코드를 넣어라"        "주소를 섞어라"           "흐름이 맞는지 HW로 확인해라"
```

- **📢 섹션 요약 비유**: 마치 복잡한 고속도로 톨게이트에서 하이패스 차선(고속 패스)을 별도로 운영하여 위조된 티켓으로 진입을 시도하더라도 차단기가 내려가 병목을 해결하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

- **구성 요소**: Intel CET는 크게 Shadow Stack(SS)과 Indirect Branch Tracking(IBT) 두 가지 축으로 구성된다.

| 구성 요소 (Component) | 약어 (Abbreviation) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|:---|
| **Shadow Stack** | SS | 반환 주소 Return Address의 무결성 보장 | 일반 스택과 분리된 전용 메모리 공간에 CPU가 반환 주소를 암호화된 형태로 저장 및 검증 | `SAVEPREVSSP`, `RSTORSSP`, `WRSS` | 이중 장부(원본 영수증) |
| **Indirect Branch Tracker** | IBT | 간접 분기(JMP/CALL)의 타겟 검증 | 간접 분기 실행 시 목적지가 `ENDBR` 명령어로 시작하는지 확인, 아니면 Exception 발생 | `ENDBR32`, `ENDBR64` | 헬기장 착륙 마커 확인 |
| **Control Protection Exception** | #CP | 위반 시 예외 처리 발생 | Shadow Stack 미스매치나 IBT 위반 시 CPU가 즉시 발생시키는 인터럽트 (Bug Check 0x109) | Exception Vector | 침입 경보 사이렌 |
| **Supervisor Mode Access Prevention**| SMAP | 커널 모드에서의 데이터 접근 제한 | CPL (Current Privilege Level)이 0일 때도 사용자 공간 페이지 접근 제한 | `AC` flag, `CR4` | 행정실에서 직원 서랍 함부로 못 열게 함 |

#### 1. Shadow Stack 아키텍처 (ROP 차단)
Shadow Stack은 기존 데이터 스택(Data Stack)과 독립적인 제어 스택(Control Stack)을 운용하여, 함수 호출 시 반환 주소(Return Address)를 두 곳에 동시에 기록한다.

```text
   [Memory Layout Comparison: Normal vs. Intel CET]

   < CPU Privilege & Memory Space >
   +-----------------------------------------------------------------------+
   | User Space (Ring 3)                                                   |
   |                                                                       |
   |  [ Normal Data Stack (RSP) ]          [ Shadow Stack (SSP) ]          |
   |  +------------------------+          +------------------------+       |
   |  | ...                    |          | ...                    |       |
   |  | Local Variables        |          | Return Address (Enc)   |       |
   |  | [ Buffer (0x20 bytes) ]|          | 0x004000A0 (Hash)      | <--- HW 저장 |
   |  | Saved RBP              |          | Return Address         |       |
   |  | Return Address (RA)    | <--------| 0x004000A0             |       |
   |  +------------------------+   PUSH    +------------------------+       |
   |          ^                           ^                               |
   |          | (해커 공격 지점)            | (해커 접근 불가 영역)            |
   |          |                           |                               |
   |  [해커 버퍼 오버플로우 발생]       [하드웨어에 의해 보호됨]           |
   |  -> 버퍼를 채우고 RA를 덮어씀    -> CPU만 이곳을 R/W 가능            |
   |     (RA = 0xDEADBEEF)               (비밀번호 없이 수정 불가)         |
   |                                                                       |
   |  [Verification Process on RET Instruction]                           |
   |  1. POP Data Stack (RSP)  -> Target1 (0xDEADBEEF)                    |
   |  2. POP Shadow Stack (SSP) -> Target2 (0x004000A0)                   |
   |  3. CPU Comparator (Target1 == Target2?)                             |
   |     -> MISMATCH! -> Raise #CP Exception -> Kernel Panic (BSOD)       |
   +-----------------------------------------------------------------------+
```

**[다이어그램 해설]**
일반적인 버퍼 오버플로우 공격은 함수의 로컬 버퍼를 넘쳐흐르게 하여 스택에 저장된 반환 주소(Return Address)를 덮어씌운다. 이로 인해 함수가 종료될 때(Ret) 해커가 원하는 코드(Gadget)로 실행 흐름이 넘어가게 된다(ROP 공격).
그러나 Intel CET가 활성화되면, 함수 호출 시(`CALL`) CPU는 기존 스택 외에 **OS가 미리 할당해둔 Shadow Stack**이라는 비밀 공간에 반환 주소의 복사본을 추가로 저장한다. 이 Shadow Stack 메모리 페이지는 하드웨어적으로 보호되어 일반 프로그램(해커)은 접근조차 할 수 없다.
함수 반환 시(`RET`) CPU는 두 스택의 값을 교차 검증한다. 해커가 일반 스택의 주소를 조작하더라도 Shadow Stack의 원본 주소는 바꿀 수 없으므로, 두 값이 불일치하여 CPU는 즉시 `#CP (Control Protection)` 예외를 발생시키고 프로그램을 강제 종료한다. 이는 소프트웨어 개입 없이 CPU 마이크로코드(Microcode) 레벨에서 1클럭 만에 이루어진다.

#### 2. IBT (Indirect Branch Tracking) & ENDBR
함수 포인터(Function Pointer)나 가상 함수 테이블(V-Table)을 이용한 간접 호출(Indirect Call)은 ROP보다 탐지가 어렵다. 이를 막기 위해 **적법한 분기 목적지(Branch Target)**에는 마커를 새긴다.

```text
   [Indirect Branch Tracking (IBT) Mechanism]

   Scenario: Attacker tries to jump into the middle of a function (JOP Attack)

   Legitimate Function Code:
   +---------------------------+
   | 0x1000:  ENDBR64          | <--- [Marker] (No-Op on Legacy CPU)
   | 0x1004:  PUSH RBP         |
   | 0x1005:  MOV RAX, [RDI]   | <--- (Attacker wants to land here!)
   | ...                        |
   +---------------------------+

   1. CPU Executing "CALL RAX" (Indirect Call)
      -> Target Address calculated: 0x1005 (Malicious intent)

   2. Hardware Check before transfer:
      IF (Target Instruction != ENDBR64 / ENDBR32)
         THEN Raise #CP Fault (Control Protection Exception)

   3. Result:
      The jump to 0x1005 is blocked immediately because it lacks the magic byte.
      Only jumps to 0x1000 (function entry) are allowed.
```

**[다이어그램 해설]**
IBT는 C/C++ 같은 고급 언어의 다형성(Polymorphism)을 보장하면서 보안을 강화하기 위해 고안되었다. 컴파일러는 바이너리를 생성할 때 모든 함수의 진입점(Epilogue) 시작 부분에 `ENDBR` (End Branch)이라는 특수 명령어(4바이트 NOP)를 삽입한다.
해커가 JOP (Jump-Oriented Programming) 공격을 통해 함수 중간의 특정 명령어(Gadget)로 점프하려고 시도하면, CPU는 그 목적지의 첫 번째 명령어가 `ENDBR`인지 확인한다. 만약 마커가 없다면 CPU는 그것을 합법적인 진입점이 아니라고 판단하고 즉시 실행을 중단한다. 이 명령어는 하위 호환성을 위해 구형 CPU에서는 단순 `NOP`으로 작동하도록 설계되었으나, CET 지원 CPU에서는 강력한 보안 검사기로 작동한다.

#### 3. 핵심 알고리즘 및 코드
- **Shadow Stack Pointer (SSP) Switching**: 컨텍스트 스위칭(Context Switching) 시 스레드마다 할당된 Shadow Stack을 보존하기 위해 `_ssp` 레지스터를 저장/복원한다.
- **WRSS (WRite to Shadow Stack)**: CPU에서만 사용 가능한 특수 명령어로, Shadow Stack 영역에 반환 주소를 쓸 때 사용한다. 일반 MOV 명령어로는 Shadow Stack 영역에 쓰기가 불가능하다.

```assembly
; GAS Syntax (Intel CET 내부 동작 예시)
; 함수 호출 시 (CALL 수행)

sub    rsp, 8              ; 일반 스택 확장
mov    qword ptr [rsp], rax ; 일반 스택에 반환 주소 저장

; [Hardware Event - Internal Microcode]
saveprevssp               ; 이전 SSP 상태 저장
wrss   [sssp], rax        ; Shadow Stack에 반환 주소 저장 (H/W Only)
incsspd rax               ; Shadow Stack Pointer 증가
```

- **📢 섹션 요약 비유**: 마치 은행 창구에서 거래를 할 때, 점원이 직원만 쓸 수 있는 '비밀 장부'에 손님의 요청을 몰래 적어두고, 나중에 영수증과 비교하는 절차와 같습니다. 위조한 영수증(일반 스택)으로는 비밀 장부(섀도 스택)의 내용을 바꿀 수 없습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석

- **심층 기술 비교**: 하드웨어 방어 vs 소프트웨어 방어

| 비교 항목 | Software CFI (e.g., Clang Sanitizer) | Hardware CFI (Intel CET, Shadow Stack) |
|:---|:---|:---|
| **구현 레이어** | Compiler Instrumentation (빌드 시 코드 삽입) | Microcode (CPU 내부 회로) |
| **성능 오버헤드** | 10% ~ 40% (런타임 체크 비용) | < 1% (Shadow Stack Locking 등) |
| **방어 완결성** | CFG (Control Flow Graph) 분석 의존적, 우회 가능 | Shadow Stack의 물리적 격리로 우회 매우 어려움 |
| **호환성** | 모든 아키텍처 가능하나 수정 필요 | Intel Tiger Lake(11세대) 이상 / AMD Zen3 이상 필요 |
| **주요 우회 경로** | JIT (Just-In-Time) 영역 공격 | Data-Only Attack (변수 조작) |

- **과목 융합 관점**:
  - **OS 및 컴퓨터 구조 (MMU & Paging)**: Shadow Stack을 구현하기 위해 x86_64 아키텍처의 페이지 테이블(Paging Structure)에 **"Shadow Stack Access"**라는 새로운 사용자 플래그(bit 62)가 추가되었다. 이 플래그가 설정된 페이지는 `MOV` 명령어로는 읽기만 가능하고, 쓰기는 특수한 CPU 명령어(`WRSS`)로만 가능하다.
  - **컴파일러 이론 (SSA & CFG)**: 컴파일러는 최적화 단계에서 CFG(Control Flow Graph)를 생성하는데, CET를 위해서는 모든 함수 진입점에 `ENDBR`을, 함수 종료 시점에 `SAVEPREVSSP` 등을 배