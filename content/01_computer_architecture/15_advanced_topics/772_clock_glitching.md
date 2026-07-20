---
title: "Clock Glitching"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 772
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클럭 글리칭 (Clock Glitching)은 정상 주기보다 빠른 edge를 삽입하거나 특정 주기를 비정상적으로 줄여, 아직 계산이 끝나지 않은 값을 플립플롭이 먼저 잡게 만드는 <strong>시간 축 기반 fault injection</strong>이다.
> 2. **가치**: 전압 글리칭보다 목표 사이클을 정밀하게 겨냥할 수 있어, branch compare, loop counter, secure boot step처럼 "한 클럭"이 중요한 구간에서 instruction skip과 상태 전이 오류를 만들기 좋다.
> 3. **판단 포인트**: 공격 난도는 외부 클럭 접근 가능성에 크게 좌우되며, 방어는 internal oscillator와 PLL (Phase-Locked Loop), clock monitor, test-mode lock, duplicated check를 함께 설계해야 실효성이 생긴다.

---

## Ⅰ. 개요 및 필요성

클럭 글리칭은 디지털 시스템의 공통 박자인 클럭을 흔들어 fault를 만드는 공격이다. 대부분의 순차 회로는 "조합 논리 지연 + 셋업 시간"보다 충분히 긴 주기가 주어질 것이라는 가정 아래 설계된다. 공격자는 바로 이 가정을 깨기 위해, 특정 순간에만 지나치게 짧은 주기나 추가 edge를 집어넣는다.

이 기법이 중요한 이유는 많은 보안 루틴이 결국 몇 개의 분기와 상태 전이에 의존하기 때문이다. 예를 들어 비교 결과를 보고 "실패면 종료"해야 하는 코드가 있는데, 비교 직후 클럭이 비정상적으로 들어오면 CPU가 아직 안정되지 않은 제어 신호를 잡아 엉뚱한 경로로 넘어갈 수 있다. 즉 전압을 흔들지 않고도 "시간 기준"만 어긋나게 해서 논리 결정을 틀리게 만드는 것이다.

특히 외부 클럭 입력을 쓰는 MCU, 스마트카드, 일부 테스트 모드가 살아 있는 SoC (System on Chip)에서는 clock glitching이 현실적인 위협이 된다. 반대로 완전히 내부 PLL (Phase-Locked Loop)과 oscillator에 잠긴 칩은 직접 공격이 더 어려워지지만, debug clock mux나 recovery mode처럼 숨은 우회 경로가 남아 있으면 다시 표면이 열린다.

- **📢 섹션 요약 비유**: 요리 재료를 바꾸는 것이 아니라, 요리사가 아직 뒤집지 않았는데 주방 타이머를 억지로 울려 덜 익은 음식을 완성품으로 내보내게 하는 공격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Clock glitching의 물리적 핵심은 매우 단순하다. 정상 주기 `Tclk`가 `tlogic + tsetup`보다 커야 하는데, 공격자가 특정 사이클만 `Tglitch`로 줄여 버리면 플립플롭은 계산이 끝나지 않은 값을 래치한다. 시스템은 계속 살아 있을 수 있지만, 해당 사이클의 분기 결과나 레지스터 값은 틀릴 수 있다.

| 파라미터 | 의미 | 대표 실패 형태 |
| :--- | :--- | :--- |
| offset | 목표 명령 기준 glitch 시작 시점 | 보안 루틴이 아닌 다른 사이클을 건드림 |
| shortened period | 얼마나 주기를 줄일지 | 너무 작으면 전체 hang/reset, 적당하면 instruction skip |
| extra edge | 추가 상승 에지 삽입 여부 | 한 단계 먼저 상태 갱신 |
| clock source access | 외부 클럭/테스트 클럭 접근 가능성 | 공격 성립 여부 자체를 좌우 |

아래 그림은 정상 클럭과 glitch 클럭의 차이를 보여 준다. 한 번의 이른 edge만으로도 critical path는 미완성 값을 저장할 수 있다.

```text
+--------------------------------------------------------------------+
| Clock glitch timing                                                |
+--------------------------------------------------------------------+
| normal : --+  +--+  +--+  +--+                                     |
|            +--+  +--+  +--+  +--                                  |
| glitch : --+  +-++--+  +--+                                       |
|            +--+ ++  +--+  +--                                    |
|                    ^                                               |
|            early edge latches data too soon                       |
|            Tglitch < tlogic + tsetup                              |
+--------------------------------------------------------------------+
```

실험실에서는 FPGA나 delay line 기반 clock generator를 사용해 ns 단위로 edge 위치를 스윕한다. 예를 들어 20MHz MCU라면 nominal period는 50ns인데, critical path slack이 작다면 특정 사이클을 40ns 이하로 줄이는 것만으로도 fault가 날 수 있다. 공격자는 전력 분석이나 GPIO (General-Purpose Input/Output) trigger로 목표 루틴 타이밍을 잡은 뒤, branch compare나 loop update 직전에 glitch를 삽입해 instruction skip을 노린다.

- **📢 섹션 요약 비유**: 오케스트라가 한 마디를 끝내기도 전에 지휘자가 다음 박자를 너무 빨리 쳐 버리면, 연주자들은 아직 음을 마무리하지 못한 채 다음 마디로 넘어가 엉뚱한 소리를 내게 된다.

---

## Ⅲ. 비교 및 연결

Clock glitching은 voltage glitching과 자주 비교된다. 둘 다 timing margin을 깨뜨리지만, clock glitching은 "언제 저장할지"를 건드리고 voltage glitching은 "얼마나 빨리 계산할지"를 건드린다. 따라서 clock glitching은 시간 정밀도가 높고, voltage glitching은 전원 도메인 전체를 넓게 흔드는 경향이 있다.

| 항목 | 클럭 글리칭 | 볼티지 글리칭 | EMFI |
| :--- | :--- | :--- | :--- |
| 주된 조작 대상 | 클럭 edge와 주기 | 공급 전압 | 국소 전자기장 |
| 정밀도 | 시간 정밀도 높음 | 전역 영향 큼 | 공간 정밀도 높음 |
| 접근 조건 | 외부 클럭 또는 우회 경로 필요 | 전원선 접근 필요 | 고가 장비 필요 |
| 대표 효과 | instruction skip, 상태 전이 오류 | branch 오류, 암호 fault | 국소 레지스터/버스 fault |
| 방어 핵심 | internal clock, watchdog | regulator, brown-out detect | shield, sensor mesh |

또한 clock glitching은 side-channel 분석과 잘 결합된다. 공격자는 먼저 전력/전자기 파형을 보고 목표 루틴의 시작 시점을 알아낸 뒤, 그 다음에 정확한 cycle에 glitch를 넣는다. 그래서 실제 공격 캠페인은 "언제 칠지 알아내는 수동 분석"과 "그 순간 때리는 능동 fault injection"이 한 세트로 움직인다.

실무적으로는 secure boot, PIN 비교, loop 기반 암호 연산이 자주 표적이 된다. 한 번의 잘못된 edge가 인증 실패 분기를 건너뛰게 하거나, 루프 카운터를 틀리게 해 특정 검증 단계를 건너뛰게 만들 수 있기 때문이다. 즉 clock glitching은 단순 주파수 교란이 아니라, 상태 전이 제어를 노린 정밀한 시간 공격이다.

- **📢 섹션 요약 비유**: 전압 글리칭이 운동선수의 체력을 순간적으로 떨어뜨리는 것이라면, 클럭 글리칭은 심판의 호루라기를 너무 일찍 불어서 경기 판정을 틀리게 만드는 방식이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

가장 강한 방어는 생산 모드에서 외부 클럭 의존성을 최소화하는 것이다. 내부 oscillator와 PLL로 클럭을 만들고, 외부 입력은 boot/test 단계에서만 제한적으로 허용하거나 fuse로 완전히 닫아 두면 공격 표면이 크게 줄어든다. 여기에 clock monitor가 주기, duty cycle, frequency range 이상을 감지하면 즉시 reset이나 tamper alarm을 내도록 하면 단순 glitcher의 성공률을 크게 떨어뜨릴 수 있다.

### 실무 체크리스트

1. 제품 출하 모드에서 외부 클럭, debug clock mux, 테스트 패드가 완전히 비활성화되어 있는가?
2. clock security circuit이나 watchdog이 비정상 주기 변화를 감지하도록 설정되어 있는가?
3. 중요한 인증/부트 단계에서 단일 분기 한 번에 모든 결정을 맡기지 않고 중복 검증을 수행하는가?
4. secure boot와 key handling 경로에 실제 clock glitch campaign을 적용해 본 적이 있는가?

소프트웨어 방어도 필요하다. 중요한 비교문을 두 번 다른 코드 경로로 수행하거나, 상태 머신을 encoded state로 운영하고, loop 종료 조건을 상호 검증하면 single-cycle fault가 바로 성공으로 이어지지 않는다. 다만 "내부 클럭을 쓰니 안전하다"라고 생각하는 것은 안티패턴이다. recovery mode, PLL bypass, 제조 테스트 모드 같은 예외 경로가 남아 있으면 공격자가 그 틈을 이용할 수 있기 때문이다.

- **📢 섹션 요약 비유**: 좋은 경기 운영은 공식 시계 하나만 믿지 않고, 심판 보조 시계와 비디오 판독까지 함께 둬서 누가 호루라기를 잘못 불어도 결과가 바로 뒤집히지 않게 만드는 것이다.

---

## Ⅴ. 기대효과 및 결론

Clock glitching을 고려한 설계는 "시간 신뢰성"을 보안 요구사항으로 끌어올린다. 그 결과 secure boot, 인증 루틴, 키 관리 로직이 단순 기능 정확성뿐 아니라 timing fault에도 얼마나 견디는지 검증하게 된다. 하드웨어 쪽에서는 clock path 보호와 tamper 대응이 강화되고, 소프트웨어 쪽에서는 단일 사이클 fault에 덜 민감한 중복 구조가 늘어난다.

물론 한계는 있다. clock 입력을 닫으면 개발·검증 편의가 줄고, 강한 모니터는 정상적인 frequency scaling까지 제약할 수 있다. 또한 외부 클럭을 막아도 EMFI나 레이저 fault injection 같은 다른 방법은 남는다. 그래서 목표는 "클럭 글리칭만 방어"가 아니라, 시간 기반 fault가 성공하기 어렵고 성공해도 감지되게 만드는 방향이어야 한다.

결론적으로 클럭 글리칭은 디지털 시스템의 "시간 합의" 자체를 공격하는 기술이다. 이 주제는 단순한 외부 클럭 교란으로 외우기보다, setup/hold margin과 보안 상태 전이가 만나는 지점을 찌르는 정밀 fault injection으로 기억하는 편이 실제 판단에 더 유용하다.

- **📢 섹션 요약 비유**: 튼튼한 공장도 사이렌 시간이 틀리면 생산 순서가 꼬인다. 그래서 좋은 공장은 기계 힘만 세게 만드는 것이 아니라, 사이렌이 이상해질 때 즉시 멈추고 다시 맞추는 체계를 갖춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Setup / Hold Time | clock glitch가 직접 깨뜨리는 기본 타이밍 조건이다. |
| PLL (Phase-Locked Loop) | 외부 클럭을 내부적으로 정제하거나 차단하는 핵심 회로다. |
| Clock Monitor | 비정상 주기·주파수를 감지해 tamper 대응을 수행한다. |
| Instruction Skip | clock glitching의 대표 결과이자 공격 목표다. |
| Secure Boot | 한 번의 잘못된 edge로 우회될 수 있어 주요 표적이 된다. |
| EMFI (Electromagnetic Fault Injection) | 외부 클럭이 막힌 환경에서 대체로 고려되는 다른 fault injection 기법이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
외부 클럭 접근 / timing trigger 수집
              |
              v
클럭 글리칭 파라미터 탐색
: offset / shortened period / extra edge
              |
              v
타이밍 위반 fault
: instruction skip / wrong branch / faulty crypto state
              |
              v
secure boot 우회 · 인증 오판 · fault analysis 발판
              |
              v
internal clock + monitor + redundancy + tamper lock
```

이 흐름은 "잘못된 박자 한 번"이 어떻게 "보안 상태 전이 오류"로 이어지고, 이를 막기 위해 클럭 생성·감시·중복 검증이 함께 필요해지는지 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 "하나, 둘, 셋" 박자에 맞춰 일을 하는데, 나쁜 사람이 박자를 너무 빨리 치게 만들어요.
2. 그러면 아직 숙제를 다 안 썼는데도 "끝!" 하고 다음 줄로 넘어가 버려서 틀린 답이 나와요.
3. 그래서 중요한 컴퓨터는 박자가 이상하면 바로 알아채고, 다시 확인하거나 멈추는 장치를 꼭 넣어요.
