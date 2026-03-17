+++
title = "CMOS (Complementary Metal-Oxide-Semiconductor)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "디지털논리"]
draft = false
+++

# CMOS (Complementary Metal-Oxide-Semiconductor)

## 핵심 인사이트 (3줄 요약)
1. CMOS는 P-channel과 N-channel MOSFET을 상보적으로 결합한 논리 회로로, 정적 전력 소비가 0에 가까워 VLSI 시대의 표준이다
2. CMOS 인버터는 V_DD/2에서 전이가 발생하는 이상적인 전압 전달 특성을 가지며, 동적 전력은 C×V²×f로 결정된다
3. 기술사 시험에서는 CMOS VTC, 노이즈 마진, 동적 전력 해석, 전송 지연(t_p), 스케일링 효과가 핵심이다

## Ⅰ. 개요 (500자 이상)

CMOS(Complementary Metal-Oxide-Semiconductor)는 1963년 Frank Wanlass가 발명한 상보적 MOS 논리 회로로, P-channel MOSFET(PMOS)과 N-channel MOSFET(NMOS)를 쌍으로 결합하여 정적 전력 소비를 최소화한다. PMOS는 V_DD와 출력 사이에 배치되어 Pull-up 스위치로 동작하며, NMOS는 출력과 GND 사이에 배치되어 Pull-down 스위치로 동작한다. 입력이 HIGH(1)일 때 NMOS가 ON, PMOS가 OFF되어 출력이 LOW(0)로 방전되며, 입력이 LOW(0)일 때 PMOS가 ON, NMOS가 OFF되어 출력이 HIGH(1)로 충전된다.

CMOS의 핵심 장점은 **정적 전력 소비가 0**에 가깝다는 것이다. 이상적인 CMOS 인버터는 정상 상태(OUT=0 또는 1)에서 한쪽 MOSFET이 차단되어 V_DD-GND 경로가 개방되므로 V_DD × 0 = 0W의 전력을 소비한다. 실제는 누설 전류(Leakage Current)로 인해 nW-μW 수준의 소비 전력이 발생하나, TTL(2-10mW/게이트)에 비해 1000-10000배 낮다. 이는 1000억 개 트랜지스터를 단일 칩에 집적한 Apple M2 Ultra(100W TDP)를 가능하게 했다.

CMOS의 동작 원리는 상보성(Complementarity)에 기반한다. NMOS는 전자 캐리어로 V_GS > V_th(N)로 ON이 되며, PMOS는 정공 캐리어로 V_GS < V_th(P)로 ON이 된다. V_th(P)는 음수 값(예: -0.7V)이므로, 입력이 LOW(0V)일 때 V_GS(P) = 0 - V_DD = -V_DD < V_th(P)로 PMOS가 ON, 입력이 HIGH(V_DD)일 때 V_GS(N) = V_DD - 0 > V_th(N)로 NMOS가 ON이 된다. 이 상보적 동작은 한쪽 MOSFET만 ON이 되어 직렬 경로가 형성되지 않음을 보장한다.

```
CMOS 인버터 회로:
        V_DD
         │
         ├─── PMOS (Pull-up)
    IN ──┤
         ├─── NMOS (Pull-down)
         │
        GND

진리표:
| IN | OUT | PMOS | NMOS | 전류 경로 | 동작 |
|----|-----|------|------|-----------|------|
| 0  | 1   | ON   | OFF  | V_DD→OUT→개방 | OUT 충전 |
| 1  | 0   | OFF  | ON   | 개방→OUT→GND | OUT 방전 |
| ?  | ?   | ON   | ON   | V_DD→OUT→GND | 단사(금지) |
```

CMOS는 TTL(Transistor-Transistor Logic), ECL(Emitter-Coupled Logic)을 대체하여 디지털 IC의 표준이 되었다. 1970년대 TTL(74LS 시리즈)이 디지털 회로의 주류였으나, 1980년대 CMOS(4000, 74HC 시리즈)으로 전환되었다. CMOS의 넓은 노이즈 마진(Noise Margin), 낮은 전력 소비, 높은 입력 임피던스, 단순한 제조 공정은 VLSI(Very Large Scale Integration)에 이상적이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### CMOS 인버터 전압 전달 특성 (VTC, Voltage Transfer Characteristic)

CMOS 인버터의 VTC는 입력 전압 V_in에 대한 출력 전압 V_out의 관계를 나타낸다.

```
VTC 구간:
1) V_in < V_th(N): NMOS OFF, PMOS ON → V_out ≈ V_DD
2) V_th(N) < V_in < V_M: NMOS 선형, PMOS 포화 → V_out 감소 시작
3) V_in = V_M: 양쪽 포화, 최대 이득 구간 → V_out = V_DD/2
4) V_M < V_in < V_DD - |V_th(P)|: NMOS 포화, PMOS 선형 → V_out 급격히 감소
5) V_in > V_DD - |V_th(P)|: NMOS ON, PMOS OFF → V_out ≈ 0

V_M (Switching Threshold):
V_M = (V_DD + V_th(N) + |V_th(P)|) / (1 + √(β_N/β_P))

여기서:
- β_N = μ_n × C_ox × (W/L)_N (NMOS 전도 계수)
- β_P = μ_p × C_ox × (W/L)_P (PMOS 전도 계수)

이상적 CMOS (β_N = β_P, V_th(N) = |V_th(P)|):
V_M = V_DD / 2
```

**노이즈 마진(Noise Margin)**:
NM_H = V_OH - V_IH (High Noise Margin)
NM_L = V_IL - V_OL (Low Noise Margin)

```
CMOS 논리 레벨 (74HC 시리즈, V_DD = 5V):
V_OH (Output High): > 4.9V (V_DD - 0.1V)
V_OL (Output Low): < 0.1V
V_IH (Input High): > 3.5V (0.7 × V_DD)
V_IL (Input Low): < 1.5V (0.3 × V_DD)

노이즈 마진:
NM_H = 4.9 - 3.5 = 1.4V
NM_L = 1.5 - 0.1 = 1.4V
```

CMOS는 TTL(NM_H = 0.4V, NM_L = 0.4V) 대비 3.5배 넓은 노이즈 마진을 가지며, 산업 환경에서 우수한 노이즈 내성을 제공한다.

### CMOS 동적 전력 (Dynamic Power)

CMOS는 정상 상태에서는 전력을 소비하지 않으나, 스위칭 순간(입력 0→1 또는 1→0 전환)에 **동적 전력(Dynamic Power)**을 소비한다.

```
동적 전력: P_dynamic = C_L × V_DD² × f × α

여기서:
- C_L: 부하 정전 용량 (Load Capacitance), 10-100fF/게이트
- V_DD: 공급 전압, 0.9-5V
- f: 스위칭 주파수 (Switching Frequency), Hz
- α: 활동 계수 (Activity Factor), 0.1-0.5

전압 의존성: P ∝ V_DD²
주파수 의존성: P ∝ f
```

동적 전력은 V_DD의 제곱에 비례하므로, 전압 감소(DVS, Dynamic Voltage Scaling)가 전력 절감의 핵심 기술이다.

```
전압 스케일링 효과:
5V → 3.3V: (3.3/5)² = 43% 전력 감소
3.3V → 1.8V: (1.8/3.3)² = 30% 전력 감소
1.8V → 1.2V: (1.2/1.8)² = 44% 전력 감소

누적: 5V → 1.2V: (1.2/5)² = 5.8% (94.2% 절감)
```

**단사 전류(Short-Circuit Current)**:
입력이 V_th(N) < V_in < V_DD - |V_th(P)|인 중간 구간에서 NMOS와 PMOS가 동시 도통하여 단사 전류가 흐른다.

```
단사 전류 손실: P_sc = I_sc(avg) × V_DD

I_sc(avg)는 전압 전이 시간(rise/fall time)에 비례
빠른 전이(rise/fall < 10ns)로 I_sc 감소 가능
```

### CMOS 전송 지연 (Propagation Delay)

CMOS 게이트의 전송 지연은 RC 시정수에 의해 결정된다.

```
전송 지연: t_p = t_pLH = t_pHL ≈ 0.69 × R_eq × C_L

여기서:
- t_pLH: Low→High 전송 지연 (PMOS 충전)
- t_pHL: High→Low 전송 지연 (NMOS 방전)
- R_eq: 등가 채널 저항 (R_DS(on) ≈ 10kΩ)
- C_L: 부하 정전 용량

RC 시정수: τ = R_eq × C_L
t_p ≈ 0.69 × τ (RC 충방정의 10%-90% 시간)

예) R_eq = 10kΩ, C_L = 50fF:
τ = 10kΩ × 50fF = 500ps
t_p = 0.69 × 500ps ≈ 345ps
```

**팬아웃(Fan-out)**:
CMOS 게이트는 입력 용량(C_in)을 가지며, 출력이 여러 입력을 구동할 때 전송 지연이 증가한다.

```
팬아웃 계수: FO = N (N개 게이트 구동)
총 부하 용량: C_L = C_wire + N × C_in

지연 증가: t_p(N) = t_p(1) × (C_L(N) / C_L(1))

일반 CMOS: FO_max = 10-50 (속도-전력 트레이드오프)
```

### CMOS 스케일링 (Scaling Theory)

Dennard 스케일링(1974)에 따라 모든 치수와 전압을 스케일링 계수 S(S < 1)만큼 감소시킨다.

```
스케일링 규칙:
- L, W, t_ox → S × L_0
- V_DD, V_th → S × V_0
- C_ox → C_ox / S

효과:
1) 채널 저항: R ∝ 1/S (감소)
2) 게이트 용량: C_g ∝ S (감소)
3) 전류: I_D ∝ S (감소)
4) 지연: t_p ∝ RC ∝ S² (감소)
5) 동적 전력: P ∝ C × V² × f ∝ S² (감소, 주파수 f는 1/S로 증가)
6) 밀도: ∝ 1/S² (증가)
```

그러나 2000년대 이후 V_th 스케일링이 멈추면서(60mV/decade 서브임계 스윙 제한), V_DD는 감소하나 V_th는 일정하게 유지되어 **전력 밀도(Power Density)**가 급증했다(Power Wall).

### CMOS 논리 게이트

**CMOS NAND 게이트**:
```
2입력 NAND 게이트 회로:
    V_DD
     │
  ┌──┴──┐
  │     │
 PMOS  PMOS
  │     │
A ├─┤   ├─┤─── OUT
  │     │
B ├─┤   ├─┤
  │     │
  └──┬──┘
     │
  NMOS  NMOS
  │     │
  GND   GND

진리표:
| A | B | OUT | PMOS 상태 | NMOS 상태 |
|---|---|-----|-----------|-----------|
| 0 | 0 | 1   | ON, ON    | OFF, OFF  |
| 0 | 1 | 1   | ON, OFF   | OFF, ON   |
| 1 | 0 | 1   | OFF, ON   | ON, OFF   |
| 1 | 1 | 0   | OFF, OFF  | ON, ON    |
```

**CMOS NOR 게이트**:
```
2입력 NOR 게이트 회로:
    V_DD
     │
  PMOS   PMOS
   │       │
A ├─┤     ├─┤─── OUT
   │       │
B ├─┤     ├─┤
   │       │
  ─┴───┬───┴──
       │
     NMOS
       │
      GND

진리표:
| A | B | OUT | PMOS 상태 | NMOS 상태 |
|---|---|-----|-----------|-----------|
| 0 | 0 | 1   | ON, ON    | OFF       |
| 0 | 1 | 0   | ON, OFF   | ON        |
| 1 | 0 | 0   | OFF, ON   | ON        |
| 1 | 1 | 0   | OFF, OFF  | ON        |
```

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개 이상)

### 디지털 로직 패밀리 비교

| 로직 패밀리 | 기본 소자 | 공급 전압 | 논리 레벨 | 노이즈 마진 | 지연(ns) | 소비 전력 | 집적도 | 응용 분야 |
|-------------|-----------|-----------|-----------|-------------|----------|-----------|--------|----------|
| RTL | Resistor-Transistor | 3-5V | TTL 호환 | 낮음 | 10-20 | 높음 | 낮음 | 초기 디지털 |
| DTL | Diode-Transistor | 5V | TTL | 중간 | 10-30 | 중간 | 낮음 | 1960년대 |
| TTL (74LS) | Bipolar Transistor | 5V ±5% | V_IH>2.0, V_IL<0.8 | NM=0.4V | 5-10 | 2-10mW/게이트 | 중간 | 1970-80년대 |
| ECL | Emitter-Coupled | -5.2V | -0.8/-1.6V | NM=0.2V | 0.5-2 | 25-50mW/게이트 | 낮음 | 고주파(>1GHz) |
| CMOS (4000) | Complementary MOS | 3-15V | 0.7/0.3×V_DD | NM≈0.45×V_DD | 50-100 | <1μW/게이트 | 높음 | 저전력 |
| CMOS (74HC) | Complementary MOS | 2-6V | 0.7/0.3×V_DD | NM≈1.4V @5V | 5-10 | <1μW/게이트 | 높음 | 현대 표준 |
| BiCMOS | Bipolar + CMOS | 5V | TTL | NM=0.4V | 2-5 | 1-5mW/게이트 | 중간 | 고속 인터페이스 |

**CMOS 장점**:
- 정적 전력 0 (누설 무시)
- 넓은 노이즈 마진 (NM≈0.45×V_DD)
- 넓은 전압 범위 (2-15V)
- 높은 입력 임피던스
- 높은 집적도 (VLSI 가능)

**CMOS 단점**:
- TTL보다 느린 속도(초기), 그러나 현대 CMOS는 1-5ns로 TTL과 동등
- 낮은 전류 구동 능력(버퍼 필요)

### CMOS 공정 세대 비교

| 공정 세대 | 최소 선폭(L) | V_DD | 게이트 산화막 | 트랜지스터 수/칩 | 클럭 | CPU 예시 | 연도 |
|-----------|-------------|------|---------------|------------------|------|----------|------|
| 10μm | 10μm | 5V | 100nm | 2,300 | 740kHz | Intel 4004 | 1971 |
| 6μm | 6μm | 5V | 60nm | 29,000 | 2-10MHz | Intel 8086 | 1978 |
| 3μm | 3μm | 5V | 30nm | 134,000 | 5-12MHz | Intel 80286 | 1982 |
| 1.5μm | 1.5μm | 5V | 15nm | 1M | 16-33MHz | Intel 80486 | 1989 |
| 1μm | 1μm | 5V | 10nm | 3M | 33-66MHz | Intel Pentium | 1993 |
| 0.8μm | 0.8μm | 5V | 8nm | 5M | 66-100MHz | AMD K5 | 1996 |
| 0.35μm | 0.35μm | 3.3V | 5nm | 10M | 150-233MHz | Intel Pentium II | 1997 |
| 0.25μm | 0.25μm | 2.5V | 4nm | 20M | 300-450MHz | Intel Pentium III | 1999 |
| 0.18μm | 0.18μm | 1.8V | 3nm | 50M | 600MHz-1GHz | AMD Athlon | 2000 |
| 0.13μm | 0.13μm | 1.2V | 2nm | 100M | 1-2GHz | Intel Pentium 4 | 2001 |
| 90nm | 90nm | 1.2V | 1.2nm | 200M | 2-4GHz | Intel Pentium 4 | 2003 |
| 65nm | 65nm | 1.2V | 1nm | 400M | 2-3GHz | Intel Core 2 | 2006 |
| 45nm | 45nm | 1.0V | High-κ | 800M | 2-3GHz | Intel Core i7 | 2008 |
| 32nm | 32nm | 1.0V | High-κ | 1B | 2-3GHz | Intel Sandy Bridge | 2011 |
| 22nm | 22nm FinFET | 1.0V | High-κ | 2B | 2-4GHz | Intel Haswell | 2013 |
| 14nm | 14nm FinFET | 1.0V | High-κ | 3B | 3-4GHz | Intel Skylake | 2015 |
| 10nm | 10nm FinFET | 0.9V | High-κ | 7B | 3-4GHz | Intel Cannon Lake | 2018 |
| 7nm | 7nm FinFET | 0.9V | High-κ | 20B | 3-5GHz | AMD Ryzen 9 | 2020 |
| 5nm | 5nm FinFET | 0.85V | High-κ | 50B | 3-5GHz | Apple M2 | 2023 |
| 3nm | 3nm GAA | 0.8V | High-κ | 100B | 4-6GHz | 예정 | 2025 |

**스케일링 효과**:
- L 감소 → R_DS(on) 감소 → I_D 증가 → 속도 향상
- V_DD 감소 → 동적 전력 V_DD² 감소
- C_ox 증가(t_ox 감소) → g_m 증가
- 그러나 단채널 효과(Short-Channel Effect)로 V_th 변화, 누설 전류 증가

## Ⅳ. 실무 적용 및 기술사적 판단 (800자 이상)

### CPU에서의 CMOS 설계

현대 CPU는 CMOS 논리 게이트로 구성되며, 클럭 속도 3-5GHz, TDP(Thermal Design Power) 100-300W를 달성한다.

```
CPU 전력 소비 구성:
P_total = P_dynamic + P_short + P_leakage

동적 전력: P_dynamic = α × C × V² × f
단사 전류: P_short = β × I_sc × V
누설 전력: P_leakage = γ × I_leak × V

예) Intel Core i7-13700K (10nm, 3.4GHz, 125W TDP):
- 트랜지스터 수: ~80억 개
- C_평균: ~50fF/게이트
- α: 0.2 (평균 활동 계수)
- f: 3.4GHz
- V_DD: 1.2V

P_dynamic = 0.2 × 50e-15 × 1.2² × 3.4e9 × 8e9
          = 0.2 × 50e-15 × 1.44 × 3.4e9 × 8e9
          = 39.2W (약 30%)
P_leakage = 나머지 70% (누설 지배적 현대 CPU)
```

**동적 전압 주파수 스케일링(DVFS, Dynamic Voltage and Frequency Scaling)**:
CPU 부하에 따라 V_DD와 f를 동적으로 조절하여 전력을 절감한다.

```
DVFS 모드:
1) Performance Mode: V_DD = 1.2V, f = 3.4GHz → P = 125W
2) Balanced Mode: V_DD = 1.0V, f = 2.5GHz → P = 125×(1.0/1.2)²×(2.5/3.4) ≈ 53W (58% 절감)
3) Power Saving Mode: V_DD = 0.8V, f = 1.2GHz → P = 125×(0.8/1.2)²×(1.2/3.4) ≈ 13W (90% 절감)
```

### SRAM 셀에서의 CMOS

6T(6-Transistor) SRAM 셀은 2개 CMOS 인버터를 교차 결합한 구조이다.

```
6T SRAM 셀 회로:
        V_DD
         │
      ┌──┴──┐
      │     │
     P1     P3
      │     │
  ────┴─────┴───
  │   │   │   │
  │  N1    N3  │
  │   │   │   │
BIT ─┴───┼───┴─── NBL
      │   │
  ────┬───┬───
  │   │   │   │
     P2     P4
      │     │
      N2     N4
      │     │
     GND    GND

동작:
- 유지(Hold): WL=0, BIT/NBL는 유지
- 읽기(Read): WL=1, BIT/NBL를 사전 충전, 셀 값 감지
- 쓰기(Write): WL=1, BIT/NBL에 원하는 값 강제
```

**SRAM 누설 전류**:
미세 공정에서 서브임계 누설(Subthreshold Leakage)과 게이트 누설(Gate Leakage)이 증가하여 대기 전력(Standby Power)이 문제이다.

```
누설 전류:
I_subthreshold = I_0 × exp[(V_GS - V_th) / (n × V_T)]
I_gate = J_gate × W × L (Tunneling Current)

해결책:
- Power Gating: 사용하지 않는 블록 전력 차단
- Sleep Transistor: 높은 V_th MOSFET으로 누설 억제
- High-V_th Cell: SRAM 셀에 높은 V_th 사용
```

### 기술사 시험 대비 문제 분석

**문제 1**: V_DD = 5V, C_L = 50fF, f = 10MHz, α = 0.3인 CMOS 인버터의 동적 전력을 계산하고, 100만 게이트의 총 전력을 산정하시오.

**해설**:
```
1) 단일 게이트 동적 전력:
P_single = C_L × V_DD² × f × α
         = 50×10^-15 × 5² × 10×10^6 × 0.3
         = 50×10^-15 × 25 × 3×10^6
         = 50×10^-9 × 75
         = 3.75μW

2) 100만 게이트 총 전력:
P_total = 3.75μW × 10^6 = 3.75W

3) 전압 20% 감소 효과 (5V → 4V):
P_new = 3.75 × (4/5)² = 3.75 × 0.64 = 2.4W
전력 절감: (3.75 - 2.4) / 3.75 = 36%
```

**문제 2**: CMOS 인버터의 R_eq = 10kΩ, C_L = 100fF일 때 전송 지연 t_p를 계산하고, 팬아웃 FO = 5일 때 지연 증가를 산정하시오.

**해설**:
```
1) RC 시정수:
τ = R_eq × C_L = 10kΩ × 100fF = 1000ps = 1ns

2) 전송 지연:
t_p = 0.69 × τ = 0.69 × 1ns = 690ps

3) 팬아웃 FO = 5일 때:
C_L(5) = C_wire + 5 × C_in = 100fF + 5 × 10fF = 150fF (C_in = 10fF 가정)
τ(5) = 10kΩ × 150fF = 1.5ns
t_p(5) = 0.69 × 1.5ns = 1.035ns

지연 증가:
Δt_p = 1.035 - 0.69 = 0.345ns (50% 증가)
t_p(5) / t_p(1) = 1.035 / 0.69 = 1.5
```

## Ⅴ. 기대효과 및 결론 (400자 이상)

CMOS는 정적 전력 0, 넓은 노이즈 마진, 높은 집적도로 디지털 IC의 표준이다. 1970년대 TTL에서 CMOS로 전환되면서 전력 소비 1000배 이상 감소하여 VLSI 시대를 열었다. 동적 전력은 C×V²×f로 결정되며, 전압 감소(DVS)가 전력 절감의 핵심이다. 스케일링은 V_th 감소 한계로 인해 전력 밀도 급증(Power Wall)을 겪었으나, 3D 구조(FinFET, GAA), 멀티-코어, DVFS로 해결하고 있다.

기술사는 CMOS VTC, 노이즈 마진, 동적 전력, 전송 지연, 스케일링 효과를 이해해야 한다. 특히 누설 전류 관리, Power Gating, DVFS는 저전력 설계의 핵심이다. CMOS 기술은 2nm, 1nm 공정에서도 지속 혁신 중이며, TFET(Tunneling FET), CFET(Complementary FET) 등 새로운 소자로 미래를 준비하고 있다.

## 📌 관련 개념 맵

```
CMOS (Complementary MOS)
├── 구조
│   ├── PMOS (Pull-up): V_DD-OUT
│   ├── NMOS (Pull-down): OUT-GND
│   └── 상보적 동작: 한쪽만 ON
├── CMOS 인버터
│   ├── VTC (전압 전달 특성)
│   ├── V_M (Switching Threshold) = V_DD/2
│   ├── 노이즈 마진: NM ≈ 0.45×V_DD
│   └── 이득: A_v = ∂V_out/∂V_in (최대 ~100)
├── 전력 소비
│   ├── 정적 전력: 0 (이론적)
│   ├── 동적 전력: P = C×V²×f×α
│   ├── 단사 전류: P_sc = I_sc×V
│   └── 누설 전류: P_leakage (서브임계, 게이트)
├── 성능 파라미터
│   ├── 전송 지연: t_p ≈ 0.69×RC
│   ├── 팬아웃: FO_max = 10-50
│   ├── 전이 시간: t_rise, t_fall
│   └── 최대 주파수: f_max = 1/(2×t_p)
├── CMOS 논리 게이트
│   ├── 인버터 (NOT)
│   ├── NAND 게이트
│   ├── NOR 게이트
│   └── 전송 게이트 (Transmission Gate)
├── 스케일링
│   ├── Dennard 스케일링: 모든 치수 S배 축소
│   ├── 효과: 지연 S²↓, 전력 S²↓, 밀도 1/S²↑
│   ├── 한계: V_th 스케일링 멈춤 (60mV/decade)
│   └── Power Wall: 전력 밀도 급증
└── 응용 분야
    ├── CPU/GPU
    ├── SRAM/DRAM
    ├── FPGA
    └── 모든 디지털 IC
```

## 👶 어린이를 위한 3줄 비유 설명

1. CMOS는 두 개의 스위치가 교대로 켜지는 장치로, 한쪽이 열리면 다른 쪽은 닫혀서 전기가 전원에서 땅으로 직접 흐르지 않아 전력을 아껴요
2. 입력이 0이면 윗쪽 스위치가 열려서 출력이 1이 되고, 입력이 1이면 아랫쪽 스위치가 열려서 출력이 0이 돼요
3. 컴퓨터 CPU에는 수십억 개의 CMOS 스위치가 들어있는데, 스위칭할 때만 전력을 소비해서 우리가 오래 컴퓨터를 써도 발열이 적은 거예요

---

## 💻 Python 코드: CMOS 전력 및 타이밍 해석

```python
import numpy as np
import matplotlib.pyplot as plt

def cmos_dynamic_power(V_DD=5, C_L=50e-15, f=10e6, alpha=0.3, N_gates=1e6):
    """
    CMOS 동적 전력 해석
    """
    # 단일 게이트 동적 전력
    P_single = C_L * V_DD**2 * f * alpha  # W

    # 총 전력
    P_total = P_single * N_gates

    print("=== CMOS 동적 전력 해석 ===")
    print(f"V_DD: {V_DD} V")
    print(f"C_L: {C_L*1e15:.1f} fF")
    print(f"스위칭 주파수: {f/1e6:.1f} MHz")
    print(f"활동 계수(α): {alpha}")
    print(f"게이트 수: {N_gates:,.0f}")
    print(f"\n결과:")
    print(f"단일 게이트 전력: {P_single*1e6:.3f} μW")
    print(f"총 동적 전력: {P_total:.2f} W")

    # 전압 스케일링 효과
    print(f"\n전압 스케일링 효과 (P ∝ V²):")
    for scale in [0.8, 0.6, 0.4, 0.2]:
        V_new = V_DD * scale
        P_new = P_total * scale**2
        savings = (P_total - P_new) / P_total * 100
        print(f"  V_DD: {V_DD:.1f}V → {V_new:.2f}V: {P_new:.2f}W (절감: {savings:.1f}%)")

    return P_total

def cmos_timing_analysis(R_eq=10e3, C_in=10e-15, C_wire=10e-15, FO_range=[1, 2, 5, 10]):
    """
    CMOS 타이밍 해석
    """
    print("\n=== CMOS 타이밍 해석 ===")
    print(f"등가 저항(R_eq): {R_eq/1000:.1f} kΩ")
    print(f"입력 용량(C_in): {C_in*1e15:.1f} fF")
    print(f"배선 용량(C_wire): {C_wire*1e15:.1f} fF")

    results = []
    for FO in FO_range:
        # 총 부하 용량
        C_L = C_wire + FO * C_in

        # RC 시정수
        tau = R_eq * C_L

        # 전송 지연
        t_p = 0.69 * tau

        # 최대 주파수
        f_max = 1 / (2 * t_p)

        results.append((FO, t_p, f_max))
        print(f"\nFO = {FO}:")
        print(f"  C_L: {C_L*1e15:.1f} fF")
        print(f"  τ: {tau*1e12:.1f} ps")
        print(f"  t_p: {t_p*1e12:.1f} ps")
        print(f"  f_max: {f_max/1e6:.1f} MHz")

    return results

def cmos_vtc_analysis(V_DD=5, V_th_N=1, V_th_P=-1, beta_ratio=1):
    """
    CMOS 전압 전달 특성 해석
    """
    print("\n=== CMOS 전압 전달 특성 (VTC) ===")
    print(f"V_DD: {V_DD} V")
    print(f"V_th(N): {V_th_N} V")
    print(f"V_th(P): {V_th_P} V")
    print(f"β_N/β_P: {beta_ratio}")

    # Switching Threshold
    V_M = (V_DD + V_th_N + abs(V_th_P)) / (1 + np.sqrt(beta_ratio))

    print(f"\nSwitching Threshold(V_M): {V_M:.2f} V")
    print(f"이상적 V_M (β_N=β_P): {V_DD/2:.2f} V")

    # 노이즈 마진
    V_OH = V_DD  # 이상적
    V_OL = 0     # 이상적
    V_IH = 0.7 * V_DD  # 규격
    V_IL = 0.3 * V_DD  # 규격

    NM_H = V_OH - V_IH
    NM_L = V_IL - V_OL

    print(f"\n논리 레벨:")
    print(f"  V_OH: {V_OH:.2f} V")
    print(f"  V_OL: {V_OL:.2f} V")
    print(f"  V_IH: {V_IH:.2f} V")
    print(f"  V_IL: {V_IL:.2f} V")
    print(f"\n노이즈 마진:")
    print(f"  NM_H: {NM_H:.2f} V")
    print(f"  NM_L: {NM_L:.2f} V")

    return V_M, NM_H, NM_L

def cmos_leakage_analysis(V_DD=1.2, V_th=0.4, I_0=1e-9, n=1.5, T=300):
    """
    CMOS 누설 전류 해석
    """
    print("\n=== CMOS 누설 전류 해석 ===")
    print(f"V_DD: {V_DD} V")
    print(f"V_th: {V_th} V")
    print(f"I_0: {I_0*1e9:.1f} nA")
    print(f"서브임계 기울기 계수(n): {n}")
    print(f"온도: {T} K")

    k = 1.381e-23  # J/K
    q = 1.602e-19  # C
    V_T = k * T / q  # 열 전압

    # 서브임계 누설
    # NMOS OFF: V_GS = 0
    # PMOS OFF: V_GS = V_DD
    # 최악 경우: V_GS = 0 (NMOS) 또는 V_GS = V_DD (PMOS)

    I_sub_N = I_0 * np.exp((0 - V_th) / (n * V_T))
    I_sub_P = I_0 * np.exp((V_DD - abs(V_th)) / (n * V_T))

    # 총 누설 전류 (2개 MOSFET 병렬)
    I_leakage = I_sub_N + I_sub_P

    # 누설 전력
    P_leakage = I_leakage * V_DD

    print(f"\n서브임계 누설:")
    print(f"  V_T: {V_T*1000:.1f} mV")
    print(f"  I_sub(NMOS): {I_sub_N*1e12:.2f} pA")
    print(f"  I_sub(PMOS): {I_sub_P*1e12:.2f} pA")
    print(f"  I_leakage: {I_leakage*1e12:.2f} pA")
    print(f"\n누설 전력 (단일 인버터):")
    print(f"  P_leakage: {P_leakage*1e12:.2f} pW")

    # 100만 게이트 누설 전력
    P_leakage_total = P_leakage * 1e6
    print(f"\n100만 게이트 누설 전력:")
    print(f"  P_total: {P_leakage_total*1000:.3f} mW")

    # 온도 의존성
    print(f"\n온도에 따른 누설 전류 변화:")
    for T_new in [300, 350, 400, 450]:
        V_T_new = k * T_new / q
        I_sub_N_new = I_0 * np.exp((0 - V_th) / (n * V_T_new))
        ratio = I_sub_N_new / I_sub_N
        print(f"  T = {T_new} K ({T_new-273:.0f}°C): I_leakage × {ratio:.2f}")

    return P_leakage

def dvfs_analysis():
    """
    DVFS (동적 전압 주파수 스케일링) 해석
    """
    print("\n=== DVFS 해석 ===")

    # 기본 모드
    modes = [
        ("Performance", 1.2, 3.4e9, 1.0),  # (이름, V_DD, f, α)
        ("Balanced", 1.0, 2.5e9, 0.7),
        ("Power Saving", 0.8, 1.2e9, 0.5),
    ]

    # 기준 전력 (Performance 모드)
    C_eff = 50e-15  # F (유효 용량)
    P_perf = C_eff * 1.2**2 * 3.4e9 * 1.0

    print(f"모드\t\tV_DD(V)\t주파수(GHz)\t전력(W)\t절감율(%)")
    print("-" * 60)
    for name, V, f, alpha in modes:
        P = C_eff * V**2 * f * alpha
        savings = (P_perf - P) / P_perf * 100
        print(f"{name}\t{V:.1f}\t{f/1e9:.1f}\t\t{P:.1f}\t\t{savings:.1f}%")

# 실행
print("=" * 70)
print("CMOS 완전 설계 해석 도구")
print("=" * 70)

# 1) 동적 전력 해석
P_dyn = cmos_dynamic_power(V_DD=5, C_L=50e-15, f=10e6, alpha=0.3, N_gates=1e6)

# 2) 타이밍 해석
timing = cmos_timing_analysis(R_eq=10e3, C_in=10e-15, C_wire=10e-15, FO_range=[1, 2, 5, 10])

# 3) VTC 해석
V_M, NM_H, NM_L = cmos_vtc_analysis(V_DD=5, V_th_N=1, V_th_P=-1, beta_ratio=1)

# 4) 누설 전류 해석
P_leak = cmos_leakage_analysis(V_DD=1.2, V_th=0.4, I_0=1e-9, n=1.5, T=300)

# 5) DVFS 해석
dvfs_analysis()

# 6) 공정 세대 비교
print("\n=== CMOS 공정 세대 비교 ===")
generations = [
    (10, 5, 2300, 740e3, 1971),
    (5, 5, 134000, 10e6, 1979),
    (1, 5, 3100000, 100e6, 1993),
    (0.35, 3.3, 10000000, 200e6, 1997),
    (0.18, 1.8, 50000000, 1e9, 2000),
    (0.09, 1.2, 200000000, 2e9, 2006),
    (0.032, 1.0, 1000000000, 3e9, 2011),
    (0.014, 1.0, 3000000000, 4e9, 2015),
    (0.007, 0.9, 41500000000, 5e9, 2020),
    (0.005, 0.85, 134000000000, 5e9, 2023),
]

print(f"공정(μm)\tV_DD(V)\t트랜지스터\t주파수\t연도")
for process, vdd, count, freq, year in generations:
    print(f"{process}\t{vdd}\t{count:>9,}\t{freq/1e6:.0f}MHz\t{year}")

# 전력 밀도 추이
print(f"\n전력 밀도 (TDP) 추이:")
cpus = [
    ("Intel 4004 (10μm)", 1, 1971),
    ("Intel 8086 (3μm)", 1.5, 1979),
    ("Intel Pentium (0.8μm)", 15, 1993),
    ("Intel Pentium 4 (0.18μm)", 65, 2000),
    ("Intel Core i7 (45nm)", 130, 2008),
    ("Intel Core i9 (14nm)", 165, 2019),
    ("AMD Ryzen 9 (7nm)", 105, 2020),
    ("Apple M2 Ultra (5nm)", 100, 2023),
]

for name, tdp, year in cpus:
    density = tdp / (100 if year < 2000 else 200 if year < 2010 else 400)  # 대략적 칩 면적
    print(f"{name}: TDP = {tdp}W ({year})")
```

이 코드는 CMOS 동적 전력, 타이밍, VTC, 누설 전류, DVFS를 해석하며, 기술사 시험의 CMOS 설계 문제를 대비한다.
