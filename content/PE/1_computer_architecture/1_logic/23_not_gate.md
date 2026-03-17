+++
title = "NOT 게이트 (Inverter, NOT Gate)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "디지털논리"]
draft = false
+++

# NOT 게이트 (Inverter, NOT Gate)

## 핵심 인사이트 (3줄 요약)
1. NOT 게이트는 입력을 반전시키는 논리 회로로, Y = A' = ¬A로 표현하며 인버터라고도 한다
2. CMOS 인버터는 PMOS와 NMOS 한 쌍으로 구성되며, 정적 전력 0, 낮은 지연, 높은 팬아웃 특징을 가진다
3. 기술사 시험에서는 CMOS 인버터 VTC, 전압 전달 특성, 트랜스컨덕턴스 g_m, 전송 지연 해석이 핵심이다

## Ⅰ. 개요 (500자 이상)

NOT 게이트는 입력 신호를 반전시키는 가장 기본적인 논리 회로로, **인버터(Inverter)**라고도 한다. 입력이 0이면 1을, 입력이 1이면 0을 출력한다. 불 대수식은 Y = A' = ¬A = ~A로 표현하며, 논리 반전(Logical Inversion) 또는 보수(Complement) 연산을 수행한다.

```
ANSI 기호          IEC 기호
    ┌─┐              ┌───┐
A ──┤  │          A ─┤ 1 ├─── Y
    │   │─── Y        │   │
    └─┘              └───┘
    (삼각형)          (1을 표시)
```

CMOS 인버터는 PMOS(Pull-up)와 NMOS(Pull-down) 한 쌍으로 구성되어 V_DD와 GND 사이에 직렬 연결된다. V_M(Switching Threshold) ≈ V_DD/2에서 전이가 발생하며, 정상 상태에서는 한쪽 MOSFET만 OFF가 되어 전류 경로가 차단된다. 이는 정적 전력 소비가 0에 가까운 CMOS의 핵심 장점이다.

컴퓨터 시스템에서 인버터는 신호 반전, 레벨 시프트(Level Shifting), 버퍼링(Buffering), 클럭 분배(Clock Distribution) 등 광범위하게 사용된다. 예를 들어 TTL 레벨(0-5V)을 CMOS 레벨(0-3.3V)로 변환할 때 인버터를 사용한다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### CMOS 인버터 구조 및 동작

```
CMOS 인버터 회로:
        V_DD
         │
         ├─── PMOS (Pull-up)
    A ──┤
         ├─── NMOS (Pull-down)
         │
        GND

동작:
A=0: PMOS ON, NMOS OFF → Y = V_DD (1)
A=1: PMOS OFF, NMOS ON → Y = GND (0)
```

### 전압 전달 특성 (VTC)

VTC는 입력 전압 V_in에 대한 출력 전압 V_out의 관계 곡선이다.

```
VTC 구간:
1) V_in < V_th(N): NMOS OFF, PMOS ON → V_out ≈ V_DD
2) V_th(N) < V_in < V_M: NMOS 선형, PMOS 포화 → V_out 감소
3) V_in = V_M: 양쪽 포화, 최대 이득 → V_out = V_DD/2
4) V_M < V_in < V_DD - |V_th(P)|: NMOS 포화, PMOS 선형 → V_out 급격히 감소
5) V_in > V_DD - |V_th(P)|: NMOS ON, PMOS OFF → V_out ≈ 0

Switching Threshold:
V_M = (V_DD + V_th(N) + |V_th(P)|) / (1 + √(β_N/β_P))

이상적 CMOS (β_N = β_P, V_th(N) = |V_th(P)|):
V_M = V_DD / 2
```

### 트랜스컨덕턴스(Transconductance, g_m)

g_m는 게이트 전압 변화에 대한 드레인 전류 변화의 비율이다.

```
g_m = ∂I_D / ∂V_GS

포화 영역:
g_m = μ_n × C_ox × (W/L) × (V_GS - V_th)
g_m = √(2 × μ_n × C_ox × (W/L) × I_D)

전압 이득:
A_v = g_m × r_o
```

### 전송 지연

```
t_p ≈ 0.69 × R_eq × C_L

R_eq = 1 / [μ × C_ox × (W/L) × (V_DD - V_th)]
C_L = C_wire + C_load

예) R_eq = 10kΩ, C_L = 50fF:
t_p ≈ 0.69 × 10kΩ × 50fF ≈ 345ps
```

## Ⅲ. 융합 비교 및 다각도 분석

### 인버터 구현 방식 비교

| 구현 | 전압 이득 | 전력 | 속도 | 응용 |
|------|-----------|------|------|------|
| CMOS 인버터 | 높음 | 낮음 | 빠름 | 디지털 IC |
| TTL 인버터 | 중간 | 높음 | 중간 | 레거시 |
| 다이오오드 인버터 | 낮음 | 낮음 | 느림 | 초기 논리 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 레벨 시프트

TTL(5V) → CMOS(3.3V) 변환에 인버터 사용.

## Ⅴ. 기대효과 및 결론

NOT 게이트는 가장 기본적인 논리 회로로, 모든 디지털 시스템의 기초이다.

## 📌 관련 개념 맵

```
NOT 게이트 (인버터)
├── CMOS 인버터
│   ├── PMOS (Pull-up)
│   ├── NMOS (Pull-down)
│   └── VTC (전압 전달 특성)
├── 파라미터
│   ├── g_m (트랜스컨덕턴스)
│   ├── t_p (전송 지연)
│   └── A_v (전압 이득)
└── 응용: 신호 반전, 레벨 시프트
```

## 👶 어린이를 위한 3줄 비유 설명

1. NOT 게이트는 스위치를 반대로 뒤집는 장치예요: 입력이 0이면 1을, 1이면 0을 내보내요
2. 전구 스위치가 "켜짐"일 때 NOT 게이트는 "꺼짐"으로 만들어서, 반대 동작을 해요
3. 컴퓨터에서 0과 1을 반대로 바꿀 때 인버터가 사용되는데, 이게 없으면 연산을 할 수 없어요
