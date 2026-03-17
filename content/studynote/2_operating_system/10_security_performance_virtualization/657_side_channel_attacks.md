+++
title = "657. 사이드 채널 공격 (Side-Channel Attacks)"
date = "2026-03-16"
weight = 657
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "사이드 채널", "Side-Channel", "Spectre", "Meltdown", "타이밍 공격", "캐시 공격"]
+++

# 사이드 채널 공격 (Side-Channel Attacks)

## # [사이드 채널 공격 (Side-Channel Attacks)]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 암호 알고리즘의 수학적 안전성과 무관하게, **물리적 구현(Power, Timing, EM)에서 발생하는 부수적 정보(Side-Channel)**를 분석하여 비밀 키나 민감 데이터를 역추적하는 공격 기법.
> 2. **가치**: **Spectre (Variant 1/2), Meltdown (Variant 3)**와 같은 HW 아키텍처 레벨의 취약점을 노출하며, 방어 시 성능 저하(Overhead)와 보안의 Trade-off를 강요하는 심각한 위협.
> 3. **융합**: OS(메모리 격리), 컴퓨터 구조(CPU 파이프라인), 암호학(Const-time Algo)이 복합적으로 얽히는 분야로, **KPTI (Kernel Page Table Isolation)**나 **Constant-Time Programming** 등으로 대응.

+++

### Ⅰ. 개요 (Context & Background)

사이드 채널 공격은 시스템의 논리적 동작(입력 $\to$ 출력)이 아닌, **물리적 동작 부산물(Byproduct)**을 정보원으로 활용한다. 일반적인 공격이 알고리즘의 수학적 결함을 공략한다면, 사이드 채널 공격은 "구현의 불완전성"을 공략한다.

**[등장 배경 및 역사]**
1996년 Paul Kocher가 **타이밍 공격(Timing Attack)**을 통해 암호 장비의 키 복구가 가능함을 최초로 입증했다. 이후 전력 소모량(Power Analysis), 전자기파(Electromagnetic) 등으로 확장되었다가, 2018년 CPU의 성능 최적화 기술인 **추측 실행(Speculative Execution)**과 **분기 예측(Branch Prediction)**을 악용하는 **Spectre, Meltdown**이 공개되며 전 세계적인 보안 이슈로 확대되었다. 이는 단순한 소프트웨어 버그가 아닌, 현대 **CPU (Central Processing Unit)** 아키텍처의 근본적인 설계 철학과 충돌하는 사례다.

> **💡 비유: '금고털이의 귀'**
> 침입자가 두꺼운 금고(암호 알고리즘)를 부수지 않고, 금고 다이얼을 돌릴 때 나는 미세한 '딸깍' 소리(캐시 적중/미스, 전력 소모)를 듣고 비밀번호를 추측하는 것과 같습니다.

**📢 섹션 요약 비유**
사이드 채널 공격은 **"요리사가 만드는 요리의 맛(암호문)을 훔치는 게 아니라, 요리 과정에서 나는 소리와 냄새(부수 정보)를 맡고 비밀 레시피를 훔치는 행위"**와 같습니다. 아무리 맛을 안 주려고 해도 조리 과정(연산)에서 발생하는 소음(노이즈)은 완전히 차단하기 어렵습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

사이드 채널 공격의 핵심은 **관층 가능한 상태 변화(Observable State Change)**를 유도하고 이를 측정하는 것이다. 주요 벡터로는 시간, 전력, 캐시 상태 등이 있다.

#### 1. 주요 공격 벡터 및 구성 요소

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 측정 지표 (Metric) | 비유 (Analogy) |
| :--- | :--- | :--- | :--- | :--- |
| **타이밍 (Timing)** | 연산 시간 차이 분석 | 입력 데이터에 따른 분기(Branch) 또는 캐시 적중(Hit) 여부에 따른 실행 시간 차이 발생 | $\Delta t$ (Latency) | 복잡한 미로를 빠르게 통행하는 여부 |
| **전력 (Power)** | 전력 소모 패턴 분석 | 연산 시 데이터의 비트 값(0/1)에 따라 소비되는 전류량 미세 차이 (Hamming Weight) | $I(t)$ (Current) | 피아노 건반을 누르는 강약 |
| **캐시 (Cache)** | 메모리 접근 패턴 유출 | 공유 캐시(L3 Cache)를 변질시켜 타겟 프로세스의 메모리 접근 여부를 확인 | Cache Hit/Miss Ratio | 공용 작업실의 서랍 사용 여부 |
| **전자기 (EM)** | 방사 전자파 수집 | 전류 흐름에 따른 자기장(Magnetic Field) 변화를 Antenna로 수집 | EM Emission | 전기 기기 작동 시의 소음 |

#### 2. 캐시 기반 공격 메커니즘 (Cache Attack)

캐시 공격은 **Flush+Reload** 또는 **Prime+Probe** 기법을 통해, 타겟 프로세스가 특정 메모리 주소에 접근했는지(캐시 상태 변화)를 관찰한다.

**[ASCII 다이어그램: Flush+Reload 공격 프로세스]**
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                  Flush+Reload Attack Sequence                   │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   [Attacker]       [Shared Memory (Array)]      [Target]        │
    │      │                   ▲    ▼    ▲               │             │
    │      │                  (L3 Cache Set)             │             │
    │      │                   ▲    ▼    ▲               │             │
    │      │                    │    │    │               │             │
    │                                                                 │
    │   1. FLUSH   ◄───────────┘    │    └───────────────  EXECUTE   │
    │      clflush(addr)             │                  (Secret Key)   │
    │      (Cache Evict)             │                        │       │
    │                               ▼                        │       │
    │   2. WAIT  .................................. (Time Pass)        │
    │                                                                 │
    │   3. RELOAD ─────────────────▶ Check Access Time ◀───┐         │
    │      rdtsc (Read TSC)        (Load from RAM?)         │         │
    │                              │         │              │         │
    │                              ▼         ▼              │         │
    │                           FAST       SLOW             │         │
    │                         (HIT!)     (MISS)             │         │
    │                           │         │                 │         │
    │                           └─────┬───┘                 │         │
    │                                 ▼                      │         │
    │                         "Target used this" ◀───────────┘         │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
```
*   **해설**: 공격자는 공유 메모리(라이브러리 함수 등)를 캐시에서 비운다(Flush). 이후 타겟이 암호 연산을 수행하면 비밀 키에 따라 특정 주소를 메모리로 가져온다. 공격자가 다시 해당 주소를 읽을 때, 캐시에 있으면(빠름), 없으면(느림) 타겟이 어떤 데이터를 사용했는지 알 수 있다.

#### 3. Spectre/Meltdown의 핵심 기술: 추측 실행 (Speculative Execution)

이들은 CPU의 성능 최적화 기술인 **아웃오브오더 실행(Out-of-Order Execution)**을 악용한다.

```c
// C언어 의사 코드 (Spectre Variant 1 예시)
if (x < array1_size) {           // ① 분기 검사 (Bounds Check)
    // ② 추측 실행: x가 array1_size보다 작다고 가정하고 미리 실행
    // ③ 결과를 array2에 매핑 (Cache Side-Channel 생성)
    y = array2[array1[x] * 512]; 
}
// ④ 실제로 x가 array1_size보다 컸다면 ②, ③은 롤백됨.
// 하지만 array2의 캐시 상태는 롤백되지 않음! (취약점)
```
*   **심층 원리**: CPU는 분기 예측(Branch Prediction)을 통해 `x < array1_size`를 참(True)으로 예측하고, 그 아래 코드를 **미리 실행(Speculative)** 한다. 비록 예측이 틀려서 결과가 롤백(Rollback)되어도, **캐시 메모리 상태는 롤백되지 않는(HW 특성)** 성질을 이용한다. 공격자는 `array2`의 어느 인덱스가 빨라지는지 확인하여 `array1[x]`의 값(비밀 데이터)을 유출한다.

**📢 섹션 요약 비유**
추측 실행을 이용한 공격은 **"미리 질문을 써두고, 선생님이 '예'라고 할 것이라고 기대하며 답안지를 미리 작성해두는 행위"**와 같습니다. 나중에 질문이 무효화되어도 답안지에 남겨진 흔적(캐시 상태)을 통해 정보를 훔칠 수 있습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Spectre vs. Meltdown 기술적 비교

| 구분 | Meltdown (CVE-2017-5754) | Spectre (CVE-2017-5753, 5715) |
| :--- | :--- | :--- |
| **공격 대상** | **격리 파기 (Isolation Breakdown)** | **분기 예측 오염 (Poisoning)** |
| **취약점 원인** | 예외(Exception) 발생 시에도 추측 실행이 중단되지 않아 커널 메모리 읽기 가능 | 잘못된 분기 예측을 유도하여 비권한 메모리 접근 코드 실행 |
| **영향 범위** | 주로 Intel, 일부 ARM 프로세서 (특정 Microcode 영향) | **Intel, AMD, ARM** 등 거의 모든 현대 CPU (설계 레벨 문제) |
| **공격 난이도** | 상대적으로 쉬움 (Root 권한 불필요) | 비교적 어려움 (Target-specific Code 필요) |
| **완화 방법** | **KPTI (Kernel Page Table Isolation)** | Retpoline (Return Trampoline), 컴파일러 패치 |

#### 2. OS/아키텍처 융합 분석
-   **OS 관점**: Meltdown 대응을 위해 **KPTI**를 도입하여 커널 주소 공간을 사용자 공간에서 완전히 분리했다. 이로 인해 **Context Switching** 시 TLB(Translation Lookaside Buffer)를 플러시해야 하므로 시스템 콜(System Call) 오버헤드가 크게 증가한다.
-   **아키텍처 관점**: Spectre는 CPU의 설계 철학을 바꿔야 한다. 분기 예측기를 보완하거나, 추측 실행 중인 데이터를 캐시에 적재하지 않는 방식(Load Blocking 등)이 논의되나, 이는 성능 저하로 직결된다.

**📢 섹션 요약 비유**
Meltdown은 **"내 방(커널) 침입을 막기 위해 방문을 아예 콘크리트로 막아버리는 것(KPTI)"**이라 성능 비용이 듭니다. 반면 Spectre는 **"누군가 내 다음 행동을 예측하고 미로를 조작하는 것"**이라 미로 자체를 바꾸거나(CPU 재설계) 조심히 걷는 코드(소프트웨어 패치)가 필요합니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 사이드 채널 공격을 방어하기 위해서는 **"일정한 실행 시간(Constant-Time Execution)"**을 보장하는 것이 가장 중요하다.

#### 1. 대응 전략 및 시나리오

**[시나리오 A: 타이밍 공격 방어 - 비교 연산 최적화]**
```c
// ❌ 취약한 코드 (Short-circuit Evaluation)
// 비밀번호가 틀리면 즉시 return (시간 차이 발생)
int check_password(char *input, char *secret) {
    for (int i = 0; i < 32; i++) {
        if (input[i] != secret[i]) return 0; 
    }
    return 1;
}

// ✅ 안전한 코드 (Constant-Time)
// 무조건 32바이트 모두 비교하여 시간 차이 제거
int check_password_safe(char *input, char *secret) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result |= (input[i] ^ secret[i]); // Bitwise OR로 결과 누적
    }
    return result == 0;
}
```
*   **기술사적 판단**: 분기문(Branch)을 제거하고 비트 연산을 통해 실행 시간을 입력 데이터 크기에 의존하지 않게 만들어야 한다.

#### 2. 도입 체크리스트
-   **[기술적]** CPU Microcode 업데이트 및 최신 OS 보안 패치(KPTI, Retpoline) 적용 여부 확인.
-   **[구현적]** 암호 라이브러리(OpenSSL 등)에서 **Const-time** 함수를 사용하는지 검증.
-   **[하드웨어]** SGX (Software Guard Extensions) 등의 보안 영역(Enclave) 사용 시 Side-Channel resistant한지 평가.

#### 3. 안티패턴 (Anti-Pattern)
-   **"암호 알고리즘만 강하면 된다"**: 구현 시 실행 경로가 비밀 키에 의존하는 코드를 작성하면 안 된다.
-   **"성능 최적화 우선순위 1위"**: 로그인 시스템에서 "틀린 비번이면 빨리 리턴"하여 서버 부하를 줄이려는 로직은 타이밍 공격의 핵심 타겟이 된다.

**📢 섹션 요약 비유**
사이드 채널 방어는 **"고속도로 톨게이트에서 차 종류와 관계없이 무조건 10초씩 통과시키는 것"**과 같습니다. 승용차는 빠르게 지나가게 해주면 편리하겠지만(성능 최적화), 그렇게 하면 트럭(비밀 키)인지 승용차인지 시차를 두고 알 수 있게 되므로(정보 유출), 모두에게 동일한 시간을 주어야 합니다.

+++

### Ⅴ. 기대효과 및 결론 (Future & Standard)

사이드 채널 공격 대응은 시스템 보안 안정성을 확보하지만, 성능 손실을 동반한다.

#### 1. 정량/정성 기대효과 (ROI)

| 항목 | 도입 전 (Before) | 도입 후 (After) | 영향 (Impact) |
| :--- | :--- | :--- | :--- |
| **보안성** | 추측 실행에 의한 메모