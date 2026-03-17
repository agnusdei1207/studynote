+++
title = "TTL (Transistor-Transistor Logic)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "디지털논리"]
draft = false
+++

# TTL (Transistor-Transistor Logic)

## 핵심 인사이트 (3줄 요약)
1. TTL은 바이폴라 트랜지스터(BJT)만으로 구성된 디지털 논리 회로 패밀리로, 1970-80년대 디지털 시스템의 표준이었다
2. TTL은 74LS 시리즈가 가장 널리 사용되었으며, 5V 전원, 논리 레벨(HIGH>2V, LOW<0.8V), 전송 지연 5-10ns 특성을 가진다
3. 기술사 시험에서는 TTL 논리 레벨, 노이즈 마진, 팬아웃, 전송 지연, 전력 소비, 토템 폴 출력단 구조가 핵심이다

## Ⅰ. 개요 (500자 이상)

TTL(Transistor-Transistor Logic)은 1962년 Texas Instruments의 Thomas L. Longo가 개발한 디지털 논리 회로 패밀리로, 모든 게이트가 BJT(Bipolar Junction Transistor)로만 구성된다. 이전 DTL(Diode-Transistor Logic)에서 다이오드를 트랜지스터로 대체하여 속도와 구동 능력을 향상시켰다. TTL은 5V ±5% 전원을 사용하며, 0-0.8V를 LOW(0), 2-5V를 HIGH(1)로 정의한다. TTL은 1970-80년대 디지털 컴퓨터(IBM System/370, DEC PDP-11), 게임 콘솔(Atari 2600, NES), 산업 제어 시스템의 표준 논리 패밀리였으나, 1990년대 CMOS(74HC, 74HCT)로 대체되었다.

TTL의 핵심 구조는 **다입력 트랜지스터(Multi-Emitter Transistor)**와 **토템 폴 출력단(Totem-Pole Output)**이다. 다입력 트랜지스터는 단일 베이스에 복수 에미터를 가진 NPN 트랜지스터로, 입력 모두가 HIGH일 때만 베이스 전류가 컬렉터로 흘러 다음 단을 구동하는 AND-NAND 기능을 수행한다. 토템 폴 출력단은 Pull-up(Q3)과 Pull-down(Q4) 트랜지스터가 직렬로 배치된 구조로, 활성 영역에서 한쪽만 ON이 되어 LOW(0) 또는 HIGH(1)를 출력한다. 이는 다이오드 출력(Open-Collector)보다 낮은 출력 저항(수십 Ω)으로 빠른 전이와 높은 전류 구동 능력을 제공한다.

```
TTL NAND 게이트 회로 (2입력 74LS00):
    V_CC (5V)
     │
     │
  ┌──┴──┐
  │ 4kΩ │ (R1)
  └──┬──┘
     │
   Q1 (다입력 NPN)
   │ │
A ├─┤ ├─┬───┐
   │ │   │
B ├─┤ ├─┘   │
   │ │     │
   └─┬─────┤
     │     │
    Q2    R_B (1kΩ)
     │     │
   ┌──┴──┐  │
   │    │  │
  Q3   Q4  R_C (120Ω)
   │    │
   └────┴─── OUT

동작:
- A=0, B=0 또는 A=0 또는 B=0: Q1 포화 → Q2 OFF → Q3 ON, Q4 OFF → OUT=1 (Pull-up)
- A=1, B=1: Q1 역방향 모드 → Q2 ON → Q3 OFF, Q4 ON → OUT=0 (Pull-down)
```

TTL은 여러 세대로 진화했다:
- **74 (Standard TTL)**: 1966년, t_p=10ns, P=10mW/게이트
- **74S (Schottky TTL)**: 1970년, 쇼트키 베이리어 다이오드(SBD) 클램프로 포화 방지, t_p=3ns, P=20mW
- **74LS (Low-Power Schottky)**: 1975년, 저전력 + 쇼트키, t_p=9.5ns, P=2mW (가장 널리 사용)
- **74ALS (Advanced Low-Power Schottky)**: 1980년, t_p=4ns, P=1mW
- **74F (Fast TTL)**: 고속 응용, t_p=3.5ns, P=5mW

TTL의 핵심 장점은 CMOS보다 빠른 스위칭 속도(5-10ns vs 50-100ns 초기 CMOS), 높은 전류 구동 능력(I_OL=-4mA @ V_OL=0.5V), 낮은 출력 저항(수십 Ω), 우수한 임피던스 매칭이다. 그러나 높은 전력 소비(2-10mW/게이트 vs CMOS <1μW), 한정된 팬아웃(10), 5V 고정 전원으로 인해 1990년대 CMOS로 대체되었다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 다입력 트랜지스터 (Multi-Emitter Transistor)

다입력 트랜지스터는 단일 베이스와 컬렉터에 복수(2-8) 에미터를 가진 NPN 트랜지스터이다.

```
다입력 트랜지스터 구조 (2입력):
              컬렉터(C)
                 ↓
        ┌─────────────┐
        │             │
  베이스(B)  ────┬────┤
        │       │    │
        │   에미터  │
    E1 │     E2 │
        │       │
        └───────┴────┘

입력 A, B: 에미터 단자
공통 베이스: R1 통해 V_CC 바이어스
컬렉터: Q2 베이스에 연결
```

**동작 원리**:
1. **입력 모두 LOW(0)**: E1-B1 또는 E2-B1 접합이 순방향 바이어스되어 Q1이 포화(Saturation) 상태로 진입한다. 베이스 전류(I_B1)는 에미터로 흘러 컬렉터 전류(I_C1)는 거의 0이다. Q2는 OFF가 되어 출력은 HIGH(1)가 된다.

```
Q1 포화 시:
I_B1 = (V_CC - V_BE - V_IN) / R1
I_C1 ≈ 0 (포화 영역에서 I_C << β×I_B)
따라서 Q2 OFF
```

2. **입력 모두 HIGH(1)**: E1-B1, E2-B1 접합이 역방향 바이어스되고, B1-C1 접합이 순방향 바이어스되어 Q1이 **역방향 액티브 모드(Reverse Active Mode)**로 동작한다. 전자가 컬렉터에서 베이스로 주입되어 에미터로 흐른다(일반 NPN과 반대).

```
Q1 역방향 액티브 시:
I_C1 ≈ β_R × I_B1 (β_R < 1, 역방향 전류 증폭도)
베이스 전류가 Q2 베이스로 흘러 Q2 ON
따라서 출력 LOW(0)
```

### 토템 폴 출력단 (Totem-Pole Output)

토템 폴 출력단은 Pull-up(Q3)과 Pull-down(Q4) 트랜지스터가 직렬로 배치된 구조이다.

```
토템 폴 출력단:
    V_CC
     │
     R_C (120Ω)
     │
    Q3 (Pull-up, NPN)
     │
     ├─── OUT
     │
    Q4 (Pull-down, NPN)
     │
    다이오드 (D3, 없는 버전도 있음)
     │
    GND

동작:
- OUT=1: Q3 ON (활성), Q4 OFF → OUT → V_CC - V_CE(sat,Q3) - V_R_C
- OUT=0: Q3 OFF, Q4 ON (포화) → OUT → V_CE(sat,Q4) ≈ 0.1-0.3V
```

**토템 폴 출력단 장점**:
1. **낮은 출력 저항**: 활성 영역에서 출력 저항이 수십 Ω으로 낮아, 빠른 전이와 높은 전류 구동 능력
2. **능동 Pull-up/Pull-down**: 수동 저항 대신 트랜지스터로 낮은 저항 실현
3. **단사 방지**: 설계상 Q3와 Q4가 동시 ON되지 않도록 보장 (그러나 전이 중간에 일시적 ON 가능)

**토템 폴 출력단 단점**:
1. **전압 손실**: OUT=1 시 V_CC - V_CE(sat) - V_R_C ≈ 3.5-4V (V_CC=5V)로 CMOS(V_DD=5V)보다 낮음
2. **단사 전류**: 전이 중간 Q3와 Q4가 일시적으로 동시 ON되어 스파이크 전류 발생
3. **버스 연결 불가**: 두 출력을 직렬 연결(Wired-OR) 불가 (Open-Collector 필요)

### TTL 논리 레벨 및 노이즈 마진

TTL 74LS 시리즈 논리 레벨:

| 파라미터 | 기호 | 최소 | 전형 | 최대 | 단위 |
|----------|------|------|------|------|------|
| 입력 HIGH 전압 | V_IH | 2.0 | - | V_CC | V |
| 입력 LOW 전압 | V_IL | 0 | - | 0.8 | V |
| 출력 HIGH 전압 | V_OH | 2.7 | 3.5 | - | V @ I_OH=-400μA |
| 출력 LOW 전압 | V_OL | 0 | 0.2 | 0.5 | V @ I_OL=4mA |

**노이즈 마진(Noise Margin)**:
```
NM_H (High Noise Margin) = V_OH(min) - V_IH(min) = 2.7 - 2.0 = 0.7V
NM_L (Low Noise Margin) = V_IL(max) - V_OL(max) = 0.8 - 0.5 = 0.3V
```

TTL은 비대칭 노이즈 마진을 가지며, NM_L(0.3V)이 NM_H(0.7V)보다 낮아 LOW에서 LOW 유지가 취약하다. CMOS(NM≈1.4V @ 5V) 대비 좁은 노이즈 마진이다.

### TTL 전송 지연 (Propagation Delay)

TTL 게이트의 전송 지연은 트랜지스터 스위칭 속도와 RC 시정수에 의해 결정된다.

```
t_pLH (Low→High 전송 지연): 입력 LOW→HIGH, 출력 HIGH→LOW 전이
t_pHL (High→Low 전송 지연): 입력 HIGH→LOW, 출력 LOW→HIGH 전이
t_p (평균 전송 지연) = (t_pLH + t_pHL) / 2

74LS00: t_pLH ≈ 9ns, t_pHL ≈ 10ns → t_p ≈ 9.5ns
74S00: t_pLH ≈ 3ns, t_pHL ≈ 3ns → t_p ≈ 3ns
```

전송 지연은 온도, 전압, 부하(팬아웃)에 의존한다.
- 온도 증가 → t_p 증가 (약 +0.3ns/°C)
- V_CC 감소 → t_p 증가
- 팬아웃 증가 → t_p 증가 (약 0.5ns/단위)

### TTL 팬아웃 (Fan-out)

팬아웃은 단일 게이트 출력이 구동할 수 있는 입력 게이트 수이다.

```
팬아웃 결정:
I_IH (입력 HIGH 전류): -20μA (입력에서 흘러 나옴)
I_IL (입력 LOW 전류): -0.4mA (입력으로 흘러 들어감)

I_OH (출력 HIGH 전류): -400μA (출력에서 공급)
I_OL (출력 LOW 전류): 4mA (출력에서 싱크)

HIGH 팬아웃:
FO_H = |I_OH| / |I_IH| = 400μA / 20μA = 20

LOW 팬아웃:
FO_L = I_OL / |I_IL| = 4mA / 0.4mA = 10

따라서 TTL 팬아웃 = min(FO_H, FO_L) = 10
```

실제 설계에서는 안전 계수(Safety Margin)를 적용하여 FO=5-7로 제한한다.

### TTL 전력 소비

TTL 게이트의 전력 소비는 공급 전압, 전류, 스위칭 빈도에 의존한다.

```
정적 전력 (DC Power):
P_Dynamic = I_CC × V_CC

I_CC(평균) = (I_CCH + I_CCL) / 2
I_CCH: HIGH 상태 공급 전류 ≈ 1mA
I_CCL: LOW 상태 공급 전류 ≈ 3mA

74LS00: I_CC ≈ 2mA
P_Dynamic = 2mA × 5V = 10mW/게이트
```

CMOS(<1μW/게이트) 대비 10000배 높은 전력 소비로, 대규모 시스템에서는 냉각 문제가 발생한다.

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개 이상)

### TTL 세대별 비교

| 세대 | 명칭 | 전송 지연(ns) | 전력(mW) | 속도-전력 곱(pJ) | 특징 | 응용 분야 |
|------|------|---------------|----------|-----------------|------|----------|
| 74 | Standard TTL | 10 | 10 | 100 | 초기 표준 | 일반 디지털 |
| 74H | High-Speed TTL | 6 | 22 | 132 | 고속 | 고속 시스템 |
| 74L | Low-Power TTL | 33 | 1 | 33 | 저전력 | 저전력 시스템 |
| 74S | Schottky TTL | 3 | 20 | 60 | 쇼트키 클램프 | 고속 컴퓨터 |
| 74LS | Low-Power Schottky | 9.5 | 2 | 19 | 가장 인기 | 일반 목적 |
| 74AS | Advanced Schottky | 1.5 | 20 | 30 | 최고속 | 고성능 시스템 |
| 74ALS | Advanced LS | 4 | 1 | 4 | 저전력 고속 | 고밀도 시스템 |
| 74F | Fast TTL | 3.5 | 5 | 17.5 | 균형 | 고속 인터페이스 |

**속도-전력 곱(Speed-Power Product)**:
```
SPP = t_p × P
단위: pJ (pico-Joule)

낮을수록 우수함:
- 74LS: 9.5ns × 2mW = 19pJ
- 74ALS: 4ns × 1mW = 4pJ (우수)
- CMOS: 10ns × 1μW = 0.01pJ (최우수, 그러나 f가 높으면 동적 전력 증가)
```

### TTL vs CMOS 비교

| 비교 항목 | TTL (74LS) | CMOS (74HC) | 설명 |
|----------|------------|-------------|------|
| 공급 전압 | 5V ±5% | 2-6V | CMOS가 유연함 |
| 논리 레벨 HIGH | V_IH > 2.0V | V_IH > 0.7×V_DD | CMOS는 전압 비례 |
| 논리 레벨 LOW | V_IL < 0.8V | V_IL < 0.3×V_DD | CMOS는 전압 비례 |
| 노이즈 마진 | NM=0.3-0.7V | NM≈0.45×V_DD | CMOS가 넓음 |
| 출력 HIGH 전압 | > 2.7V @ -400μA | ≈ V_DD | CMOS가 rail-to-rail |
| 출력 LOW 전압 | < 0.5V @ 4mA | ≈ 0V | 유사 |
| 전송 지연 | 5-10ns | 5-10ns | 현대 CMOS는 동등 |
| 전력 소비 | 2-10mW/게이트 | <1μW/게이트 | CMOS가 1000-10000배 낮음 |
| 팬아웃 | 10 | >50 | CMOS가 높음 |
| 입력 임피던스 | 낮음 (1-10kΩ) | 매우 높음 (>10¹²Ω) | CMOS가 전압 검출에 적합 |
| 출력 임피던스 | 낮음 (수십 Ω) | 중간 (수kΩ) | TTL이 구동 능력 우수 |
| 정적 전력 | 높음 | 거의 0 | CMOS 우수 |
| 동적 전력 | 낮음 | C×V²×f | CMOS는 f 의존적 |
| 집적도 | 낮음 (SSI, MSI) | 높음 (VLSI) | CMOS가 고밀도 칩에 적합 |
| 비용 | 낮음 | 낮음 | 유사 |
| 응용 분야 | 레거시 시스템 | 현대 디지털 | CMOS가 표준 |

**기술사적 판단 포인트**:
- **고전류 구동**: TTL 선택 (I_OL=4mA vs CMOS I_OL=4-8mA)
- **저전력 배터리 구동**: CMOS 선택 (정적 전력 0)
- **고주파 시스템(>100MHz)**: CMOS 선택 (동적 전력 억제)
- **레거시 호환**: TTL-CMOS 혼용 시 74HCT(CMOS with TTL inputs) 사용

### TTL 출력 구조 비교

| 출력 타입 | 구조 | V_OH | I_OL | 특징 | 응용 |
|-----------|------|------|------|------|------|
| 토템 폴 (Totem Pole) | Q3(상단) + Q4(하단) | 3.5-4V | 4mA | 빠름, 낮은 출력 저항 | 일반 논리 |
| 오픈 컬렉터 (Open Collector) | Q4만 (상단 없음) | Pull-up 저항에 의존 | 4-16mA | Wired-OR 가능, 느림 | 버스 구동, 램프 구동 |
| 3상태 (Three-State) | 토템 폴 + Enable 핀 | 3.5-4V | 4mA | 고임피던스 Hi-Z 상태 | 버스 아비트릭 |

**오픈 컬렉터 (Open Collector)**:
상단 트랜지스터 없이 하단 NPN만 존재하며, 외부 Pull-up 저항(1-10kΩ) 필요하다.

```
오픈 컬렉터 출력:
     V_CC
      │
     R_pull-up (1-10kΩ)
      │
      ├─── OUT (버스 공유)
      │
     Q4 (Pull-down)
      │
     GND

Wired-OR: 여러 출력을 버스에 직렬 연결
- 어느 하나가 0이면 버스는 0 (AND 논리)
- 모두 1(Z 상태)이면 Pull-up으로 1
```

**3상태 (Three-State, Tri-State)**:
출력이 0, 1, Hi-Z(고임피던스) 3가지 상태를 가진다.

```
3상태 버퍼 회로:
    DATA ──┬──→ 토템 폴 출력 ──→ OUT
    ENABLE ──┤ (Enable=1: 활성, Enable=0: Hi-Z)

응용: 데이터 버스 아비트릭 (CPU, Memory)
```

## Ⅳ. 실무 적용 및 기술사적 판단 (800자 이상)

### 레거시 시스템에서의 TTL

TTL은 1970-80년대 컴퓨터 시스템에 널리 사용되었다.

**IBM System/370 메인프레임 (1970)**:
- TTL 74/74S 시리즈 사용
- 수천 개 TTL 게이트로 구성
- 공급 전압 5V, 냉각 시스템 필수

**DEC PDP-11 미니컴퓨터 (1970)**:
- TTL 74/74H 시리즈 사용
- 16-bit ALU를 TTL로 구현
- 전력 소비 수백 와트

**Atari 2600 게임 콘솔 (1977)**:
- MOS 6502 CPU + TTL 칩(Custom 40-pin)
- 74LS00, 74LS74, 74LS161 등 사용
- 5V 단일 전원

### TTL-CMOS 인터페이스

TTL과 CMOS 논리 레벨은 다르므로 인터페이스 회로가 필요하다.

```
TTL → CMOS (74HC) 인터페이스:
TTL 출력 V_OH(min)=2.7V가 CMOS 입력 V_IH(min)=0.7×V_DD=3.5V(5V) 미만
해결책:
1) 74HCT 사용 (CMOS with TTL inputs): V_IH(min)=2.0V
2) Pull-up 저항: TTL 출력에 1-10kΩ pull-up으로 V_OH 상승
3) 레벨 시프터: 74LVC07 등 사용

CMOS (74HC) → TTL 인터페이스:
CMOS 출력 V_OH≈5V가 TTL 입력 V_IH(max)=5V 호환
문제 없음, 직접 연결 가능
```

### 기술사 시험 대비 문제 분석

**문제 1**: 74LS00 게이트가 V_CC=5V, T_A=25°C에서 동작할 때, I_IH=-20μA, I_IL=-0.4mA, I_OH=-400μA, I_OL=4mA일 때 팬아웃을 계산하시오.

**해설**:
```
1) HIGH 팬아웃:
FO_H = |I_OH| / |I_IH| = 400μA / 20μA = 20

2) LOW 팬아웃:
FO_L = I_OL / |I_IL| = 4mA / 0.4mA = 10

3) TTL 팬아웃:
FO = min(FO_H, FO_L) = min(20, 10) = 10

따라서 최대 10개 74LS 입력을 구동 가능
```

**문제 2**: 74LS00의 V_IH=2.0V, V_IL=0.8V, V_OH=3.5V, V_OL=0.2V일 때 노이즈 마진 NM_H와 NM_L을 계산하고, 더 취약한 레벨을 판단하시오.

**해설**:
```
1) 노이즈 마진:
NM_H = V_OH - V_IH = 3.5 - 2.0 = 1.5V (실제 datasheet: V_OH(min)=2.7V → NM_H=0.7V)
NM_L = V_IL - V_OL = 0.8 - 0.2 = 0.6V (실제 datasheet: V_OL(max)=0.5V → NM_L=0.3V)

2) 취약 레벨:
실제 datasheet 기준:
NM_H = 2.7 - 2.0 = 0.7V
NM_L = 0.8 - 0.5 = 0.3V
따라서 LOW 레벨이 더 취약함 (NM_L이 낮음)

이유: V_OL(max)=0.5V가 V_IL(max)=0.8V에 근접하여
노이즈로 0.3V 이상 상승 시 논리 오류 가능
```

**문제 3**: 74LS00 게이트 10개가 직렬로 연결된 체인에서 총 전송 지연을 계산하고, 최대 클럭 주파수를 산정하시오.

**해설**:
```
1) 단일 게이트 전송 지연:
t_p = (t_pLH + t_pHL) / 2 = (9ns + 10ns) / 2 = 9.5ns

2) 10게이트 체인 총 지연:
t_total = 10 × t_p = 10 × 9.5ns = 95ns

3) 최대 클럭 주파수:
T_min = 2 × t_total (setup+hold 시간 고려)
f_max = 1 / T_min = 1 / (2 × 95ns) = 1 / 190ns ≈ 5.26MHz

실제로는 setup/hold time, clock skew 고려하여 3-4MHz가 최대
```

## Ⅴ. 기대효과 및 결론 (400자 이상)

TTL은 1970-80년대 디지털 혁명의 기반 기술로, 바이폴라 트랜지스터의 빠른 스위칭과 높은 전류 구동 능력으로 초기 컴퓨터와 게임 콘솔을 가능하게 했다. 다입력 트랜지스터와 토템 폴 출력단은 TTL의 핵심 혁신이었다. 74LS 시리즈는 저전력과 속도의 균형으로 가장 널리 사용되었으나, 높은 전력 소비(2-10mW/게이트)와 5V 고정 전원으로 CMOS에 자리를 내어주었다.

기술사는 TTL 논리 레벨, 노이즈 마진, 팬아웃, 전송 지연, 오픈 컬렉터/3상태 출력을 이해해야 한다. 특히 TTL-CMOS 인터페이스와 레거시 시스템 유지보수는 실무에서 여전히 중요하다. TTL은 대부분 CMOS로 대체되었으나, 오픈 컬렉터 버스 구동, 레벨 시프트, 고전류 응용에서 여전히 사용된다.

## 📌 관련 개념 맵

```
TTL (Transistor-Transistor Logic)
├── 구조
│   ├── 다입력 트랜지스터 (Multi-Emitter)
│   ├── 토템 폴 출력단 (Totem-Pole)
│   └── 쇼트키 클램프 (Schottky Clamp)
├── 세대별 분류
│   ├── 74 (Standard): 10ns, 10mW
│   ├── 74S (Schottky): 3ns, 20mW
│   ├── 74LS (Low-Power Schottky): 9.5ns, 2mW
│   ├── 74ALS (Advanced LS): 4ns, 1mW
│   └── 74F (Fast): 3.5ns, 5mW
├── 논리 레벨
│   ├── V_IH > 2.0V, V_IL < 0.8V
│   ├── V_OH > 2.7V, V_OL < 0.5V
│   └── 노이즈 마진: NM_H=0.7V, NM_L=0.3V
├── 성능 파라미터
│   ├── 전송 지연: t_p = 5-10ns
│   ├── 팬아웃: FO = 10
│   ├── 전력 소비: 2-10mW/게이트
│   └── 속도-전력 곱: SPP = t_p × P
├── 출력 타입
│   ├── 토템 폴 (Totem Pole)
│   ├── 오픈 컬렉터 (Open Collector)
│   └── 3상태 (Three-State)
└── 응용 분야
    ├── 레거시 컴퓨터 (IBM 370, DEC PDP-11)
    ├── 게임 콘솔 (Atari 2600, NES)
    ├── 산업 제어 시스템
    └── 레벨 시프트, 버스 구동
```

## 👶 어린이를 위한 3줄 비유 설명

1. TTL은 작은 스위치들이 모여서 0과 1을 만들어내는 회로인데, 전기를 많이 먹어서 옛날 컴퓨터에 주로 쓰였어요
2. TTL은 5V 전압을 기준으로 2V 이상을 1, 0.8V 이하를 0으로 구별하며, 각 스위치가 최대 10개까지 다른 스위치를 제어할 수 있어요
3. 요즘은 전기를 훨씬 적게 먹는 CMOS가 대부분이지만, 옛날 기계를 수리할 때는 TTL을 이해해야 돼요

---

## 💻 Python 코드: TTL 설계 파라미터 해석

```python
import numpy as np

def ttl_fanout_analysis(I_IH=-20e-6, I_IL=-0.4e-3, I_OH=-400e-6, I_OL=4e-3):
    """
    TTL 팬아웃 해석
    """
    # HIGH 팬아웃
    FO_H = abs(I_OH) / abs(I_IH)

    # LOW 팬아웃
    FO_L = I_OL / abs(I_IL)

    # TTL 팬아웃
    FO = min(FO_H, FO_L)

    print("=== TTL 팬아웃 해석 ===")
    print(f"I_IH (입력 HIGH 전류): {I_IH*1e6:.1f} μA")
    print(f"I_IL (입력 LOW 전류): {I_IL*1e3:.1f} mA")
    print(f"I_OH (출력 HIGH 전류): {I_OH*1e6:.1f} μA")
    print(f"I_OL (출력 LOW 전류): {I_OL*1e3:.1f} mA")
    print(f"\n팬아웃 계산:")
    print(f"  HIGH 팬아웃: {FO_H:.1f}")
    print(f"  LOW 팬아웃: {FO_L:.1f}")
    print(f"  TTL 팬아웃: {FO:.0f}")

    # 안전 계수 적용
    FO_safe = FO * 0.7
    print(f"\n권장 팬아웃 (안전 계수 0.7): {FO_safe:.0f}")

    return FO

def ttl_noise_margin(V_IH=2.0, V_IL=0.8, V_OH=2.7, V_OL=0.5):
    """
    TTL 노이즈 마진 해석
    """
    NM_H = V_OH - V_IH
    NM_L = V_IL - V_OL

    print("\n=== TTL 노이즈 마진 해석 ===")
    print(f"V_IH: {V_IH} V")
    print(f"V_IL: {V_IL} V")
    print(f"V_OH(min): {V_OH} V")
    print(f"V_OL(max): {V_OL} V")
    print(f"\n노이즈 마진:")
    print(f"  NM_H (High): {NM_H} V")
    print(f"  NM_L (Low): {NM_L} V")

    if NM_H > NM_L:
        print(f"\n  LOW 레벨이 더 취약함 (NM_L이 낮음)")
    else:
        print(f"\n  HIGH 레벨이 더 취약함 (NM_H이 낮음)")

    return NM_H, NM_L

def ttl_timing_analysis(t_pLH=9e-9, t_pHL=10e-9, N_gates=10):
    """
    TTL 타이밍 해석
    """
    t_p = (t_pLH + t_pHL) / 2

    # 체인 지연
    t_total = N_gates * t_p

    # 최대 클럭 주파수
    T_min = 2 * t_total
    f_max = 1 / T_min

    print("\n=== TTL 타이밍 해석 ===")
    print(f"t_pLH: {t_pLH*1e9:.1f} ns")
    print(f"t_pHL: {t_pHL*1e9:.1f} ns")
    print(f"t_p (평균): {t_p*1e9:.1f} ns")
    print(f"\n{N_gates}게이트 체인:")
    print(f"  총 지연: {t_total*1e9:.1f} ns")
    print(f"  최대 클럭: {f_max/1e6:.2f} MHz")

    return f_max

def ttl_power_analysis(V_CC=5, I_CCH=1e-3, I_CCL=3e-3, N_gates=100):
    """
    TTL 전력 해석
    """
    I_CC_avg = (I_CCH + I_CCL) / 2
    P_single = I_CC_avg * V_CC
    P_total = P_single * N_gates

    print("\n=== TTL 전력 해석 ===")
    print(f"V_CC: {V_CC} V")
    print(f"I_CCH (HIGH 상태): {I_CCH*1e3:.1f} mA")
    print(f"I_CCL (LOW 상태): {I_CCL*1e3:.1f} mA")
    print(f"I_CC(avg): {I_CC_avg*1e3:.1f} mA")
    print(f"\n단일 게이트 전력: {P_single*1000:.1f} mW")
    print(f"{N_gates}게이트 총 전력: {P_total:.2f} W")

    # CMOS와 비교
    P_cmos = N_gates * 1e-6  # CMOS <1μW/게이트 가정
    ratio = P_total / P_cmos
    print(f"\nCMOS 대비 전력 비율: {ratio:.0f}배")

    return P_total

def ttl_generation_comparison():
    """
    TTL 세대별 비교
    """
    print("\n=== TTL 세대별 비교 ===")

    generations = [
        ("74", 10, 10),
        ("74H", 6, 22),
        ("74L", 33, 1),
        ("74S", 3, 20),
        ("74LS", 9.5, 2),
        ("74AS", 1.5, 20),
        ("74ALS", 4, 1),
        ("74F", 3.5, 5),
    ]

    print(f"{'세대':<10} {'지연(ns)':<10} {'전력(mW)':<10} {'SPP(pJ)':<10}")
    print("-" * 50)
    for name, t_p, P in generations:
        spp = t_p * P
        print(f"{name:<10} {t_p:<10.1f} {P:<10.1f} {spp:<10.1f}")

def ttl_cmos_comparison():
    """
    TTL vs CMOS 비교
    """
    print("\n=== TTL vs CMOS 비교 ===")

    comparison = [
        ("공급 전압", "5V ±5%", "2-6V", "CMOS가 유연"),
        ("V_IH", "> 2.0V", "> 0.7×V_DD", "CMOS는 전압 비례"),
        ("V_IL", "< 0.8V", "< 0.3×V_DD", "CMOS는 전압 비례"),
        ("노이즈 마진", "0.3-0.7V", "≈0.45×V_DD", "CMOS가 넓음"),
        ("전송 지연", "5-10ns", "5-10ns", "현대 CMOS는 동등"),
        ("전력 소비", "2-10mW/게이트", "<1μW/게이트", "CMOS가 1000-10000배 낮음"),
        ("팬아웃", "10", ">50", "CMOS가 높음"),
        ("입력 임피던스", "낮음 (1-10kΩ)", "매우 높음 (>10¹²Ω)", "CMOS가 전압 검출에 적합"),
        ("출력 저항", "낮음 (수십 Ω)", "중간 (수kΩ)", "TTL이 구동 능력 우수"),
        ("정적 전력", "높음", "거의 0", "CMOS 우수"),
        ("집적도", "낮음", "높음", "CMOS가 VLSI에 적합"),
    ]

    print(f"{'비교 항목':<20} {'TTL (74LS)':<20} {'CMOS (74HC)':<20} {'설명'}")
    print("-" * 80)
    for param, ttl, cmos, desc in comparison:
        print(f"{param:<20} {ttl:<20} {cmos:<20} {desc}")

# 실행
print("=" * 70)
print("TTL 완전 설계 해석 도구")
print("=" * 70)

# 1) 팬아웃 해석
FO = ttl_fanout_analysis()

# 2) 노이즈 마진 해석
NM_H, NM_L = ttl_noise_margin()

# 3) 타이밍 해석
f_max = ttl_timing_analysis()

# 4) 전력 해석
P_total = ttl_power_analysis()

# 5) 세대별 비교
ttl_generation_comparison()

# 6) TTL vs CMOS 비교
ttl_cmos_comparison()

# 7) TTL → CMOS 인터페이스 가이드
print("\n=== TTL ↔ CMOS 인터페이스 가이드 ===")
print("TTL → CMOS (74HC):")
print("  - 문제: TTL V_OH(min)=2.7V < CMOS V_IH(min)=3.5V (5V)")
print("  - 해결 1: 74HCT 사용 (V_IH(min)=2.0V)")
print("  - 해결 2: Pull-up 저항 (1-10kΩ)")
print("  - 해결 3: 레벨 시프터 (74LVC07)")
print("\nCMOS (74HC) → TTL:")
print("  - CMOS V_OH≈5V가 TTL V_IH(max)=5V 호환")
print("  - 직접 연결 가능")
print("\n5V → 3.3V 변환:")
print("  - 74LVC07 사용 (레벨 시프트 내장)")
print("  - 저항 분압기 (비추천: 지연 증가)")
```

이 코드는 TTL 팬아웃, 노이즈 마진, 타이밍, 전력을 해석하며, 기술사 시험의 TTL 설계 문제를 대비한다.
