---
title: "Edge Trigger"
date: "2026-04-05"
tags:
  - "studynote-computer-architecture"
weight: 46
---
> **핵심 인사이트**
> 1. 에지 트리거(Edge Trigger)는 클럭 신호의 엣지(Rising 또는 Falling) 순간에만 데이터를 샘플링하는 플립플롭 동작 방식 — 레벨 트리거(Level Trigger)보다 타이밍 제어가 정밀하며 현대 디지털 회로에서 표준이다.
> 2. 상승 에지(Rising Edge) 트리거는 0->1 전환 순간에 입력 D를 포착해 출력 Q에 저장 — 클럭 사이클당 단 한 번 데이터가 업데이트되므로 레이스 컨디션(Race Condition)이 제거된다.
> 3. 에지 트리거 플립플롭의 셋업/홀드 타임 제약은 메타스태빌리티(Metastability)를 방지하는 핵심 — 데이터가 에지 직전/직후 일정 시간 동안 안정되어야 플립플롭이 확정적으로 동작한다.

---

## Ⅰ. 레벨 트리거 vs 에지 트리거

```
래치 (Level Trigger):
  클럭 HIGH 동안 데이터 투명(Transparent)
  클럭 LOW 동안 데이터 잠금(Latched)

  문제: 클럭 HIGH 동안 입력 변화 -> 출력 연속 변화
  -> 레이스 컨디션 (Race Condition) 위험

  D Latch 동작:
  CLK=1: Q = D (투명, 따라감)
  CLK=0: Q = 이전값 (잠금)

에지 트리거 플립플롭 (D Flip-Flop):
  클럭 에지 순간에만 데이터 포착
  클럭 에지 이후: 출력 유지

  Rising Edge D Flip-Flop:
  CLK: 0->1 전환 순간 -> Q = D 포착
  이후: Q 유지 (D 변해도 Q 불변)

비교:
           래치             에지 트리거 FF
데이터 포착 CLK HIGH 전체   CLK 에지 순간만
레이스 컨디션 위험          없음
복잡도       낮음           높음
사용처       CPU 내부 일부  대부분 순차 로직

현대 디지털 회로:
  대부분 에지 트리거 플립플롭 사용
  FPGA, ASIC: D 플립플롭이 기본 빌딩 블록
```

> 📢 **섹션 요약 비유**: 레벨 트리거는 열린 문(CLK HIGH면 누구나 입장), 에지 트리거는 회전문(클릭 순간에만 한 명 통과). 회전문이 더 안전!

---

## Ⅱ. D 플립플롭 내부 구조

```
Rising Edge D Flip-Flop:
  마스터-슬레이브 구조로 구현

마스터-슬레이브 D Flip-Flop:

CLK=0: 마스터 래치 투명 (D 포착)
        슬레이브 래치 잠금
CLK=1: 마스터 래치 잠금
        슬레이브 래치 투명 (마스터 값 출력)

효과:
  CLK 상승 에지에서 D -> Q 전달
  나머지 시간: Q 유지

게이트 수준 구현:
  NOT 게이트 2개 + NAND/NOR 조합
  최소 6개 NAND 게이트

비동기 리셋/프리셋:
  RESET: Q를 즉시 0으로
  PRESET: Q를 즉시 1으로
  (CLK과 무관하게 즉시 동작)

  사용: 전원 인가 시 초기화

  프리셋 우선 회로:
  if (RESET=0): Q=0
  elif (PRESET=0): Q=1
  else: 에지 트리거 동작

타이밍 파라미터:
  tsu (Setup Time): 에지 전 최소 안정 시간
  th (Hold Time): 에지 후 최소 유지 시간
  tpd (Propagation Delay): 에지 -> Q 변화 시간

  디지털 교과서 전형적 값:
  tsu ≈ 0.1~0.5 ns
  th  ≈ 0.05~0.2 ns
  tpd ≈ 0.2~1.0 ns
```

> 📢 **섹션 요약 비유**: 마스터-슬레이브는 이중 잠금 금고 — 바깥 금고(마스터)에 먼저 넣고, 클릭 후 안쪽 금고(슬레이브)로 이전. 한 번에 하나씩만 들어가요!

---

## Ⅲ. 메타스태빌리티

```
메타스태빌리티 (Metastability):
  셋업/홀드 타임 위반 시 출력이
  0도 1도 아닌 불확정 상태에 빠지는 현상

발생 조건:
  데이터 변화와 클럭 에지가 너무 가까울 때

  Safe:   D 변화 ---------- tsu -- CLK에지
  Unsafe: D 변화 --- tsu 위반 - CLK에지

메타스태빌리티 상태:
  Q = 중간 전압 (예: 0.8V, 정상은 0 or 1.8V)

  결과:
  - 다음 단계 회로가 0 또는 1로 잘못 해석
  - 불확정 상태가 수 나노초 지속 가능
  - 해결 안 되면 시스템 오동작

발생 빈도:
  MTBF_meta = exp(C2 × T_resolution) / (C1 × f_clk × f_data)

  -> T_resolution 증가 (더 기다림) -> MTBF 지수 증가

CDC (Clock Domain Crossing)에서 흔함:
  서로 다른 주파수 도메인 간 신호 전달
  -> 수신 클럭과 데이터 타이밍 무관

메타스태빌리티 해결:
  1. 2단계 동기화 플립플롭 (2-FF Synchronizer):
     FF1 -> FF2 -> 다음 회로
     FF1에서 메타 발생 -> FF2까지 해소 시간 확보

  2. FIFO (비동기 FIFO):
     두 클럭 도메인 사이 버퍼
     그레이 코드 포인터로 메타 방지
```

> 📢 **섹션 요약 비유**: 메타스태빌리티는 동전이 서는 상태 — 던진 동전이 0(앞)도 1(뒤)도 아닌 세워진 채로! 2단계 동기화는 동전이 쓰러질 때까지 기다리는 것!

---

## Ⅳ. FPGA와 에지 트리거

```
FPGA 내부 에지 트리거:

FPGA 기본 요소:
  LUT (Look-Up Table): 조합 논리
  FF (Flip-Flop): 순차 로직

  각 LUT마다 D 플립플롭 내장
  -> 설계자 선택적 활용

Verilog 에지 트리거:
  // Rising Edge D Flip-Flop
  always @(posedge clk) begin
    q <= d;  // 비차단(non-blocking) 할당
  end

  // Async Reset
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      q <= 1'b0;
    else
      q <= d;
  end

글로벌 클럭 네트워크:
  FPGA: 전용 글로벌 클럭 버퍼
  저스큐(Low Skew) 클럭 분배

  Xilinx: BUFG, BUFR, MMCM
  Intel: GCLK, PLL

STA (Static Timing Analysis):
  에지 트리거 타이밍 검증
  모든 FF-to-FF 경로 셋업/홀드 확인
  도구: Vivado Timing Analyzer, Quartus TimeQuest

  WNS (Worst Negative Slack): 최악 타이밍 여유
  WNS > 0: 설계 통과
  WNS < 0: 타이밍 위반 -> 수정 필요
```

> 📢 **섹션 요약 비유**: FPGA 에지 트리거는 레고 블록 — D 플립플롭(레고 블록)을 LUT과 조합해 원하는 순차 회로 구성. Verilog는 레고 조립 설명서!

---

## Ⅴ. 실무 시나리오 — ASIC 타이밍 클로저

```
고속 ASIC 에지 트리거 타이밍 설계:

설계 사양:
  ARM Cortex-A55 클론 설계
  목표 주파수: 2 GHz
  공정: TSMC 7nm

  tclk = 0.5 ns 안에 모든 타이밍 맞춰야

타이밍 제약 설정:
  # Synopsys Design Constraints
  create_clock -period 0.5 [get_ports clk]

  set_input_delay 0.1 -clock clk [all_inputs]
  set_output_delay 0.1 -clock clk [all_outputs]

Critical Path 분석:
  FF1 -> Adder(32bit) -> Comparator -> FF2

  타이밍 분해:
  tclk-q (FF1): 0.05 ns
  조합 논리:    0.38 ns  <- 병목
  배선 지연:    0.02 ns
  tsu (FF2):   0.03 ns
  총합:         0.48 ns < 0.5 ns ✓

  WNS = 0.5 - 0.48 = 0.02 ns (아슬아슬!)

최적화 기법:
  파이프라인 삽입:
  긴 조합 논리 -> 중간에 FF 삽입
  -> 각 스테이지 짧아짐 -> 주파수 증가

  로직 리타이밍 (Retiming):
  FF 위치 이동으로 타이밍 균등화

  클럭 스큐 활용 (Useful Skew):
  의도적 스큐로 Critical Path 여유 증가

최종 검증:
  코너 분석: SS(slow-slow), FF(fast-fast), TT
  온도: -40+C ~ 125+C
  전압: VDD ±10%
  모든 코너에서 WNS > 0 -> 테이프아웃
```

> 📢 **섹션 요약 비유**: ASIC 타이밍 클로저는 100m 허들 — 0.5ns(클럭 주기)라는 시간 안에 모든 신호가 FF에서 다음 FF까지 전달. 허들(지연) 하나라도 높으면 탈락(타이밍 위반)!

---

## 📌 관련 개념 맵

```
에지 트리거 (Edge Trigger)
+-- 비교
|   +-- 레벨 트리거 (래치)
|   +-- 에지 트리거 (D FF)
+-- 내부 구조
|   +-- 마스터-슬레이브 래치
|   +-- 비동기 Reset/Preset
+-- 타이밍
|   +-- 셋업/홀드 타임
|   +-- 메타스태빌리티
|   +-- CDC 동기화
+-- 구현
    +-- FPGA (LUT+FF)
    +-- ASIC (STA, 타이밍 클로저)
    +-- Verilog always @(posedge)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 플립플롭 (1940s~50s)]
SR 래치, JK 플립플롭
레벨 트리거 주류
      |
      v
[CMOS D 플립플롭 (1970s~)]
마스터-슬레이브 에지 트리거
저전력, 고속
      |
      v
[VLSI / FPGA 시대 (1980s~)]
에지 트리거 표준화
STA(정적 타이밍 분석) 필수화
      |
      v
[현재: 초미세 공정]
7nm/3nm 에지 트리거
Pulse Latch (하이브리드)
      |
      v
[미래: 양자/아날로그]
래치 기반 회로 재조명
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 에지 트리거는 정확한 순간 포착 — 클럭이 0->1 바뀌는 그 순간(에지)에만 데이터를 기억해요. 항상 열려있는 문(래치)보다 훨씬 안전!
2. 메타스태빌리티는 동전이 서는 것 — 너무 바쁠 때 데이터가 들어오면(셋업 위반) 플립플롭이 0도 1도 아닌 중간에 멈출 수 있어요!
3. FPGA는 D 플립플롭 레고 — Verilog로 "posedge clk"라고 쓰면 에지 트리거 FF 자동 생성. LUT+FF 조합이 디지털 회로의 기본!
