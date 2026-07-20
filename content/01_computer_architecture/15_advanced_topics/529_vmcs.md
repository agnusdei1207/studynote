---
title: "VMCS"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 529
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VMCS (Virtual Machine Control Structure)는 인텔 VT-x (Intel Virtualization Technology for x86)에서 vCPU (virtual CPU)의 게스트 상태, 호스트 복귀 상태, 인터셉트 정책, VM Exit 기록을 한곳에 모아 둔 하드웨어 제어 장부다.
> 2. **가치**: CPU (Central Processing Unit)는 VMCS를 기준으로 VM (Virtual Machine) Entry와 VM Exit를 일관되게 수행하므로, 수정하지 않은 게스트 운영체제를 빠르게 전환하고 강한 격리도 유지할 수 있다.
> 3. **판단 포인트**: VMCS의 성능은 "있느냐"보다도 어떤 필드를 어떻게 설정해 불필요한 Exit를 줄였는지, 그리고 중첩 가상화에서 Shadow VMCS 같은 보조 기능을 쓸 수 있는지에 따라 갈린다.

---

## Ⅰ. 개요 및 필요성

VMCS (Virtual Machine Control Structure)는 가상 머신이 멈췄을 때 무엇을 저장하고, 다시 들어갈 때 무엇을 복원하며, 어떤 사건에서 하이퍼바이저를 깨울지를 정의하는 인텔 하드웨어 가상화의 핵심 구조다. 일반 프로세스 문맥 전환은 운영체제가 레지스터 몇 개를 저장하면 되지만, 가상화는 제어 레지스터, 세그먼트 상태, 인터럽트 제어, 특권 명령 인터셉트 규칙까지 함께 관리해야 한다. 이 정보를 매번 소프트웨어가 따로 계산하면 전환이 느리고 일관성도 흔들린다.

특히 x86 가상화는 "게스트가 자신을 진짜 Ring 0라고 믿고 동작한다"는 전제를 만족해야 하므로, 하이퍼바이저는 게스트에게 보여 줄 CPU 세계와 실제 호스트 상태를 분리해야 한다. VMCS는 바로 이 분리를 하드웨어가 이해할 수 있는 형식으로 미리 적어 두는 약속문이다. 그래서 VMCS가 없으면 VM Exit마다 하이퍼바이저가 느린 소프트웨어 경로로 상태를 수습해야 하고, VMCS가 있으면 CPU가 정해진 규칙대로 곧바로 저장·복구를 수행할 수 있다.

이 그림은 VMCS가 왜 단순 저장 공간이 아니라 "상태 + 정책"을 묶은 장부인지 보여 준다.

```text
+----------------------------------------------------------------------------+
|            VMCS가 필요한 이유: 전환 정보와 통제 규칙을 한곳에 모음         |
+----------------------------------------------------------------------------+
| Guest vCPU 실행                                                            |
|      |                                                                     |
|      +- 상태만 저장하면 ------> 다음 Exit 때 무엇을 잡을지 다시 계산        |
|      |                                                                     |
|      +- VMCS 사용 ----------> Guest 상태 · Host 상태 · Exit 조건을 즉시 참조|
|                                     |                                      |
|                                     v                                      |
|                           VM Entry / Exit를 하드웨어가 일관 처리           |
+----------------------------------------------------------------------------+
```

결국 VMCS의 필요성은 "가상 머신의 현재 상태를 기억한다"에 그치지 않는다. <strong>어떤 행위가 가상화 경계를 넘는지까지 하드웨어 수준에서 정의해 두는 것</strong>이 본질이다.

- **📢 섹션 요약 비유**: VMCS는 비행기 교대 조종사가 함께 보는 운항 장부와 같다. 지금 속도와 고도만 적는 것이 아니라, 어떤 경고등이 켜지면 자동으로 관제실을 부를지도 미리 적어 두어야 안전하게 넘겨받을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

VMCS는 보통 4KB 정렬된 메모리 영역으로 준비되며, 하이퍼바이저는 `VMPTRLD`로 현재 논리 코어의 current VMCS를 지정하고 `VMREAD`/`VMWRITE`로 필드를 다룬다. 첫 실행은 `VMLAUNCH`, 이후 재진입은 `VMRESUME`, 초기화는 `VMCLEAR`가 맡는다. 즉 VMCS는 일반 C 구조체처럼 마음대로 덮어쓰는 데이터가 아니라, <strong>CPU 명령어를 통해서만 안전하게 접근하는 하드웨어 포맷</strong>이다.

핵심 필드는 다음과 같이 나뉜다.

| 필드 영역 | 역할 | 대표 정보 |
| :--- | :--- | :--- |
| Guest-State Area | 게스트로 돌아갈 때 복원할 상태 | RIP, RSP, CR3, 세그먼트, RFLAGS |
| Host-State Area | Exit 후 호스트가 즉시 이어받을 상태 | Host RIP, Host RSP, CR3 |
| VM-Execution Controls | 무엇을 trap할지 결정 | I/O (Input/Output) bitmap, MSR (Model-Specific Register) bitmap, 예외 bitmap, pin/processor controls |
| VM-Entry Controls | 재진입 시 주입할 이벤트와 방식 | 인터럽트 주입, IA-32e 진입 여부 |
| VM-Exit Controls | Exit 시 저장/복구 정책 | MSR 저장, 주소 크기, acknowledge interrupt |
| VM-Exit Information | 왜 빠져나왔는지 기록 | Exit reason, qualification, fault address |

이 그림은 VMCS가 VM Entry와 VM Exit 양쪽에서 각각 어떤 역할을 하는지 보여 준다.

```text
+----------------------------------------------------------------------------+
|                    VMCS가 전환을 지휘하는 방식                            |
+----------------------------------------------------------------------------+
| [Guest-State] --+                                                         |
| [Entry Control] +--> VM Entry --> VMX Non-Root 실행                         |
| [Exec Control] -+                          |                              |
|                                            +- 일반 경로 ------> 계속 실행  |
|                                            |                              |
|                                            +- 인터셉트 대상 --> VM Exit    |
|                                                                  |         |
| [Exit Info] <------------------------------------------------------+         |
| [Exit Control] --> [Host-State] --> VMX Root 복귀                  |         |
+----------------------------------------------------------------------------+
```

여기서 중요한 점은 VMCS가 "저장소"이면서 동시에 "분기표"라는 사실이다. Guest-State와 Host-State가 전환의 내용을 담당한다면, Execution Controls는 전환의 빈도를 좌우한다. 그래서 같은 VT-x 환경이라도 어떤 비트맵과 제어 비트를 켰느냐에 따라 VM Exit 수가 크게 달라진다.

또한 VMCS에는 lifecycle 개념이 있다. 한 VMCS는 clear 상태에서 시작해 current 상태로 로드되고, 한 번 `VMLAUNCH`가 성공하면 launched 상태가 된다. 이런 상태 기계가 필요한 이유는, 하드웨어가 "처음 진입인지, 재개인지"를 구분해야 정확한 검증과 복원을 할 수 있기 때문이다.

- **📢 섹션 요약 비유**: VMCS는 호텔 객실 카드키와 운영 매뉴얼이 합쳐진 것과 같다. 누가 방에 들어갈지뿐 아니라, 어떤 문은 자동으로 열리고 어떤 문은 프런트를 거쳐야 하는지까지 카드에 규칙이 들어 있다.

---

## Ⅲ. 비교 및 연결

VMCS를 이해하려면 운영체제의 PCB (Process Control Block), AMD-V의 VMCB (Virtual Machine Control Block), 그리고 EPT (Extended Page Tables) 같은 주변 기능과 비교해 봐야 경계가 또렷해진다. PCB는 스케줄러가 프로세스를 바꾸기 위해 쓰는 소프트웨어 장부이고, VMCS는 하드웨어가 직접 참조하는 가상화 장부다. VMCB는 AMD 쪽 대응 개념이지만, 세부 필드와 명령어 인터페이스는 다르다.

| 항목 | PCB (Process Control Block) | VMCS | VMCB |
| :--- | :--- | :--- | :--- |
| 주 용도 | 프로세스 스케줄링 | VM Entry/Exit와 인터셉트 제어 | AMD 계열 VM 전환 제어 |
| 주 관리 주체 | OS 커널 | 하이퍼바이저 + Intel CPU | 하이퍼바이저 + AMD CPU |
| 상태 범위 | 일반 실행 문맥 중심 | 특권 상태, 인터셉트 정책, Exit 정보 포함 | 유사하지만 AMD 형식 |
| 성능 영향점 | 문맥 전환 빈도 | Exit 빈도와 제어 필드 설계 | Exit 빈도와 제어 필드 설계 |

또한 VMCS 자체가 모든 성능 문제를 해결하는 것은 아니다. 메모리 번역 비용은 EPT/NPT (Nested Page Tables), 인터럽트 비용은 APICv (Advanced Programmable Interrupt Controller virtualization)나 posted interrupt, I/O 비용은 VirtIO (Virtual I/O)나 SR-IOV (Single Root I/O Virtualization)와 함께 봐야 한다. VMCS는 이런 기능들을 <strong>켜고 조합하는 중앙 제어판</strong>에 가깝다.

중첩 가상화에서는 관계가 더 복잡해진다. L1 하이퍼바이저는 자신만의 VMCS가 있다고 믿지만, 실제로는 L0가 그것을 다시 가상화해야 한다. 이때 `VMREAD`와 `VMWRITE`가 매번 L0로 올라가면 성능이 급격히 나빠지므로, Shadow VMCS가 있으면 L1이 자주 보는 필드를 하드웨어가 가까운 곳에서 대신 다뤄 주며 Exit를 줄인다.

- **📢 섹션 요약 비유**: PCB가 학교 출석부라면 VMCS는 공항 출입 통제 시스템에 가깝다. 누가 어디 있는지만 적는 것이 아니라, 어느 문에서 보안 검색을 거쳐야 하는지까지 함께 관리한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 VMCS는 직접 눈에 잘 보이지 않지만, `kvm_stat`, `perf kvm stat`, VTune 같은 도구를 보면 결국 Exit reason 형태로 모습을 드러낸다. 예를 들어 `CPUID`, `RDMSR/WRMSR`, I/O instruction Exit가 과도하면 "가상 CPU 수가 부족하다"기보다 <strong>VMCS의 인터셉트 정책이 너무 넓거나, 반가상화 장치 경로가 부족하다</strong>는 뜻일 수 있다. 즉 튜닝의 출발점은 코어 개수보다 Exit 분포다.

### 적용 판단 체크리스트

1. EPT, APICv, posted interrupt 같은 Exit 절감 기능이 실제로 활성화되어 있는가?
2. I/O bitmap, MSR bitmap, exception bitmap이 필요한 것만 잡도록 좁혀져 있는가?
3. VMCS를 vCPU 단위로 관리하고, 다른 논리 코어로 옮길 때 `VMPTRLD`와 host-state 정합성이 유지되는가?
4. 중첩 가상화가 필요하다면 Shadow VMCS 또는 이에 준하는 가속 경로를 사용할 수 있는가?

### 피해야 할 안티패턴

- 하나의 VMCS를 여러 vCPU가 동시에 공유하려는 설계
- 핫패스에서 사소한 변경마다 `VMWRITE`를 남발하는 구현
- VMCS를 단순 메모리 덤프처럼 취급해 guest-state와 host-state 경계를 흐리는 운영

학습 정리에서는 "VMCS가 있다"보다 "VMCS 제어 비트 설계가 Exit를 어떻게 바꾸는가"를 말해야 한다. 하드웨어가 빠르다는 사실만 쓰면 일반론에 머물고, 어떤 인터셉트를 줄이고 어떤 것은 반드시 유지해야 하는지까지 적어야 설계 판단이 된다.

- **📢 섹션 요약 비유**: VMCS 튜닝은 콜센터 전화 분류 규칙을 다듬는 일과 같다. 아무 전화나 상담원에게 넘기면 안전해 보여도 줄이 폭발하고, 꼭 필요한 전화만 넘겨야 전체 응답 속도가 좋아진다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 VMCS는 가상화를 "소프트웨어 흉내"에서 "하드웨어와 협업하는 실행 환경"으로 바꾼다. Guest와 Host 상태가 명확히 분리되고, Exit 이유가 구조적으로 기록되며, 하이퍼바이저는 수정하지 않은 운영체제를 훨씬 예측 가능하게 수용할 수 있다. 이것이 클라우드에서 대규모 멀티테넌시가 가능한 중요한 전제다.

물론 한계도 있다. VMCS가 있어도 Exit 자체는 여전히 비싸고, I/O와 메모리 번역 병목은 별도 기능과 함께 해결해야 하며, 중첩 가상화에서는 제어 구조가 다시 가상화되어 복잡성이 급증한다. 앞으로는 confidential VM, 더 정교한 인터럽트 가상화, nested workload 가속처럼 <strong>VMCS를 둘러싼 제어면 자체를 더 안전하고 더 얇게 만드는 방향</strong>이 중요해질 것이다.

결론적으로 VMCS는 "가상 머신의 상태 저장소"가 아니라 <strong>전환 규칙까지 포함한 하드웨어 계약서</strong>로 기억하는 것이 정확하다. 이 관점을 잡으면 VMCS, VM Exit, EPT, Shadow VMCS가 왜 하나의 흐름으로 묶이는지도 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: VMCS는 공연장 무대 전환표와 같다. 배우가 어디에 서는지만 적는 것이 아니라, 어떤 장면에서 조명을 바꾸고 어떤 순간에 무대 감독을 호출할지도 함께 적혀 있어야 공연이 끊기지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| VM Exit / VM Entry | VMCS가 직접 사용되는 전환 시점이다. |
| EPT (Extended Page Tables) | 메모리 번역 Exit를 줄이는 기능으로, VMCS 제어 비트와 함께 동작한다. |
| APICv | 인터럽트 관련 Exit를 줄이는 하드웨어 가속 기능이다. |
| Shadow VMCS | 중첩 가상화에서 `VMREAD`/`VMWRITE` 부담을 줄이는 보조 구조다. |
| VMPTRLD / VMLAUNCH / VMRESUME | VMCS를 로드하고 첫 실행·재실행을 구분하는 핵심 명령어다. |
| VMCB (Virtual Machine Control Block) | AMD 계열에서 대응되는 개념으로 비교 기준이 된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 중심 문맥 저장
        |
        v
VMX Root / Non-Root 분리
        |
        v
VMCS 기반 Guest-State · Host-State · Exit Reason 관리
        |
        v
EPT · APICv · 비트맵 제어로 Exit 절감
        |
        v
Shadow VMCS · 중첩 가상화 가속
        |
        v
Confidential VM · 더 정교한 제어면 보호
```

이 흐름은 단순 상태 저장에서 출발해, 이제는 VM 전환 규칙과 보안 경계까지 하드웨어가 더 많이 맡는 방향으로 발전했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. VMCS는 가상 컴퓨터가 어디까지 놀았는지 적어 두는 아주 자세한 메모장이에요.
2. 메모장에는 "어떤 일은 혼자 해도 되고, 어떤 일은 선생님을 불러야 해"라는 규칙도 같이 적혀 있어요.
3. 그래서 컴퓨터는 잠깐 멈췄다가 다시 시작해도 바로 이어서 안전하게 움직일 수 있답니다.
