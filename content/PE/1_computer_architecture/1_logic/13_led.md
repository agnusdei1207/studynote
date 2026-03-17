+++
title = "발광 다이오드 (LED - Light Emitting Diode)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "광전자"]
draft = false
+++

# 발광 다이오드 (LED - Light Emitting Diode)

## 핵심 인사이트 (3줄 요약)
1. LED는 PN 접합에서의 전자-정공 재결합 시 방출되는 에너지를 빛으로 변환하는 발광 소자로, 표시 장치와 조명의 핵심이다
2. 반도체 밴드갭 에너지에 따라 방출 광파장이 결정되며, GaN, GaAsP, AlGaInP 등 재료 공학이 LED 색상과 효율을 좌우한다
3. 기술사 시험에서는 순방향 전압 강하, 광출력 효율(lumen/W), 열 설계, PWM 디밍 제어가 핵심 출제 포인트이다

## Ⅰ. 개요 (500자 이상)

발광 다이오드(Light Emitting Diode, LED)는 전기 에너지를 직접 빛 에너지로 변환하는 반도체 발광 소자이다. 1962년 Nick Holonyak Jr.가 개발한 적색 LED 이후, 청색 LED(1993년 Shuji Nakamura)와 백색 LED(1996년)의 개발으로 LED 조명과 디스플레이 혁명이 가속화되었다. LED는 일반 다이오드의 PN 접합 구조를 기반으로 하며, 순방향 바이어스 시 N형 반도체의 전자와 P형 반도체의 정공이 접합면에서 재결합할 때 방출되는 에너지가 광자(Photon)로 변환되는 발광 현상을 이용한다.

LED의 핵심 물리 원리는 **전계 발광(Electroluminescence)**이다. 순방향 바이어스에서 전자가 전도대(Conduction Band)에서 가전자대(Valence Band)로 떨어지며 정공과 재결합할 때, 밴드갭 에너지(E_g)만큼의 에너지가 방출된다. 방출 광자의 에너지는 E = h × f = h × c / λ로 표현되며, 파장 λ는 λ = h × c / E_g로 결정된다. 여기서 h는 플랑크 상수(6.626×10^-34 J·s), c는 광속(3×10^8 m/s)이다. 따라서 반도체 재료의 밴드갭 에너지에 따라 LED의 발광 색상이 결정된다.

```
밴드갭 에너지와 발광 색상:
- E_g = 1.8-2.0 eV: 적색 (Red, λ ≈ 620-750nm)
- E_g = 2.0-2.2 eV: 황색/녹색 (Yellow/Green, λ ≈ 570-590nm)
- E_g = 2.2-2.8 eV: 녹색 (Green, λ ≈ 495-570nm)
- E_g = 2.8-3.2 eV: 청색 (Blue, λ ≈ 450-495nm)
- E_g > 3.2 eV: 자외선 (UV, λ < 400nm)
```

컴퓨터 시스템에서 LED는 다양한 용도로 활용된다. **상태 표시 LED**(Power LED, HDD Activity LED, Network Link/Activity LED)는 시스템 동작 상태를 시각적으로 피드백한다. **RGB LED**는 컴퓨터 케이스, 키보드, 마우스 등 게이밍 장비의 조명으로 사용되며, PWM(Pulse Width Modulation) 제어를 통해 1600만 색상 이상을 표현할 수 있다. **LCD 백라이트**는 노트북과 모니터의 광원으로 사용되며, 청색 LED + 형광체(인광체) 조합으로 백색광을 생성한다. **광통신 LED**는 단거리 광통신(POF, Plastic Optical Fiber)의 송신기로 사용되어 전기적 노이즈에 강한 전송을 구현한다.

LED의 핵심 장점은 고효율(100-200 lm/W), 긴 수명(50,000시간 이상), 빠른 응답 속도(μs 이하), 내진성, 친환경성(수은 불필요)이다. 백열등(15 lm/W), 형광등(60-80 lm/W) 대비 2-10배의 효율을 가지며, 스위칭 주파수가 수 MHz 이상 가능하여 고속 디밍 제어와 데이터 통신(Li-Fi, Light Fidelity)에 적용 가능하다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### LED의 구조 및 동작 원리

LED는 이종 접합(Heterojunction) 구조를 사용하여 발광 효율을 극대화한다. 기본 PN 접합은 단일 반도체 재료로 구성되나, LED는 서로 다른 밴드갭을 가진 반도체를 접합한 이종 접합을 사용하여 전자와 정공을 활성 영역(Active Region)으로 집중시킨다.

```
LED 구조 (Double Heterojunction):
┌─────────────────────────────────────┐
│  P형 콘택트 (Anode +)               │
├─────────────────────────────────────┤
│  P형 클래딩 층 (대역 갭 넓음)        │  ← 정공 장벽
├─────────────────────────────────────┤
│  활성 층 (Active Region)            │  ← 재결합/발광 영역
│  (대역 갭 좁음, E_g)                │
├─────────────────────────────────────┤
│  N형 클래딩 층 (대역 갭 넓음)        │  ← 전자 장벽
├─────────────────────────────────────┤
│  N형 콘택트 (Cathode -)             │
└─────────────────────────────────────┘
```

이종 접합은 클래딩 층의 넓은 밴드갭이 활성 층의 좁은 밴드갭보다 높은 에너지 장벽을 형성하여, 전자와 정공이 활성 층에 갇히도록(Carrier Confinement) 한다. 이는 재결합 확률을 향상시키고 발광 효율을 극대화한다.

### 전류-광출력 특성

LED의 순방향 전류 I_F와 광출력 Φ(Luminous Flux)의 관계는 거의 선형적이다.

```
광출력: Φ = η_opt × P_elec = η_opt × (V_F × I_F)

여기서:
- η_opt: 광학적 효율 (Optical Efficiency), 약 20-50%
- V_F: 순방향 전압 (Forward Voltage)
- I_F: 순방향 전류 (Forward Current)
```

순방향 전압 V_F는 밴드갭 에너지에 비례한다.

```
V_F ≈ E_g / e + V_series

여기서:
- E_g: 밴드갭 에너지 (eV 단위)
- e: 기본 전하 (1.602×10^-19 C)
- V_series: 직렬 저항에 의한 전압 강하 (I_F × R_s)

예) 적색 LED (E_g = 1.9 eV): V_F ≈ 1.9V + 0.2V = 2.1V
    청색 LED (E_g = 3.0 eV): V_F ≈ 3.0V + 0.3V = 3.3V
```

### LED 재료 공학 및 색상 제어

| LED 색상 | 반도체 재료 | 밴드갭(eV) | 파장(nm) | 순방향 전압(V) | 효율(lm/W) |
|----------|-------------|------------|----------|---------------|------------|
| 적색(Red) | GaAsP, AlGaAs | 1.8-2.0 | 620-750 | 1.8-2.2 | 20-100 |
| 황색(Yellow) | GaAsP, AlGaInP | 2.0-2.2 | 570-590 | 2.0-2.4 | 20-80 |
| 녹색(Green) | GaP, AlGaInP | 2.2-2.8 | 495-570 | 2.2-3.0 | 30-150 |
| 청색(Blue) | InGaN, GaN | 2.8-3.2 | 450-495 | 2.8-3.6 | 30-120 |
| 백색(White) | 청색 LED + 인광체 | - | 400-700 | 3.0-3.6 | 100-200 |
| UV | AlGaN, GaN | >3.2 | <400 | 3.2-4.5 | 10-50 |

**백색 LED 구현 방식**:
1. **RGB LED 혼합**: 적색, 녹색, 청색 LED를 혼합하여 백색 생성 (색재현성 우수, 제어 복잡)
2. **청색 LED + 형광체**: 청색 LED(450nm) + YAG:Ce 인광체(Yttrium Aluminum Garnet doped with Cerium) 사용, 청색 일부는 형광체에 흡수되어 황색(550nm)으로 변환, 청색+황색 혼합으로 백색 생성 (간단, 효율 우수, 색재현성 한계)
3. **UV LED + RGB 형광체**: UV LED(380nm) + 적색/녹색/청색 형광체 혼합 (색재현성 최상, 효율 낮음)

### LED 구동 회로 및 전류 제어

LED는 전류 구동 소자(Current-Driven Device)로, 전압보다는 전류를 정밀 제어해야 한다. 순방향 전압의 작은 변화(예: 2.1V → 2.2V, +5%)가 전류의 큰 변화(20mA → 40mA, +100%)를 유발할 수 있어, 직접 전압 구동은 열폭주(Thermal Runaway) 위험이 있다.

```
LED 전류 제어 방법:

1) 직렬 저항 구동 (간단, 전압 변동에 취약):
   R_series = (V_supply - V_F) / I_F

   예) V_supply = 5V, V_F = 2.1V, I_F = 20mA:
   R_series = (5 - 2.1) / 0.02 = 145Ω

2) 정전류원 구동 (정밀, 전압 변동에 강함):
   I_F = V_ref / R_sense

   예) V_ref = 1.25V, R_sense = 62.5Ω:
   I_F = 1.25 / 62.5 = 20mA

3) 스위칭 정전류원 (고효율, 고전력용):
   PWM 제어로 평균 전류 조절
   Duty Cycle × I_peak = I_avg
```

### PWM 디밍 및 색상 제어

RGB LED의 색상 제어는 각 색상 LED의 PWM 듀티 사이클을 독립적으로 조절하여 구현한다.

```
RGB 색상 혼합:
R_intensity = R_pwm_duty × R_max
G_intensity = G_pwm_duty × G_max
B_intensity = B_pwm_duty × B_max

혼합 색상 = (R_intensity, G_intensity, B_intensity)

예) 8비트 PWM (0-255):
- 흰색: (255, 255, 255)
- 적색: (255, 0, 0)
- 노란색: (255, 255, 0)
- 마젠타: (255, 0, 255)
```

PWM 주파수는 200Hz 이상이어야 인간 눈의 깜빡임(Flicker)이 인지되지 않는다. 고화응용(High-Speed Camera, Li-Fi)에서는 PWM 주파수를 수 MHz까지 높여 데이터 통신에 활용한다.

### 열 설계 및 수명 예측

LED의 열 설계는 수명과 효율에 직접적인 영향을 미친다. LED 정션 온도(T_j)가 10°C 상승할 때마다 수명은 반감(Rule of Thumb)하며, 광출력은 약 3-5% 감소한다.

```
정션 온도 산정:
T_j = T_a + (P_total × θ_j-a)

P_total = V_F × I_F + P_switching

여기서:
- T_j: 정션 온도 (Junction Temperature)
- T_a: 주위 온도 (Ambient Temperature)
- P_total: 총 소비 전력
- θ_j-a: 정션-주위 열저항 (Thermal Resistance, Junction-to-Ambient)

열저항 분해:
θ_j-a = θ_j-c + θ_c-s + θ_s-a

여기서:
- θ_j-c: 정션-케이스 열저항 (Junction-to-Case)
- θ_c-s: 케이스-히트싱크 열저항 (Case-to-Heatsink)
- θ_s-a: 히트싱크-주위 열저각 (Heatsink-to-Ambient)
```

LED 수명(L70, B50)은 초기 광출력의 70%로 감소하는 시간으로 정의된다. 일반적으로 T_j = 25°C에서 50,000시간, T_j = 85°C에서 10,000시간 수준이다. 아레니우스 모델(Arrhenius Model)로 수명 예측 가능:

```
L(T) = L_0 × exp(E_a / (k × (T_j - T_ref)))

여기서:
- L(T): 온도 T에서의 수명
- L_0: 기준 온도에서의 수명
- E_a: 활성화 에너지 (Activation Energy, 약 0.5 eV)
- k: 볼츠만 상수 (8.617×10^-5 eV/K)
```

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개 이상)

### 광원별 효율 및 특성 비교

| 광원 유형 | 효율(lm/W) | 수명(h) | 발열(W) | 응답속도 | 색재현성(CRI) | 비용 | 응용 분야 |
|-----------|------------|---------|---------|----------|---------------|------|----------|
| 백열등 | 10-15 | 1,000 | 높음(90% 열) | ms | 100 (최상) | 최저 | 감조명, 오븐 |
| 형광등 | 60-80 | 8,000 | 중간 | ms-cs | 70-90 | 낮음 | 사무실 조명 |
| CFL | 50-70 | 10,000 | 중간 | cs | 80-85 | 낮음 | 가정용 조명 |
| HID(MH, HPS) | 80-120 | 15,000 | 높음 | s | 20-65 | 중간 | 가로등, 공장 |
| 백색 LED | 100-200 | 50,000 | 낮음(10% 열) | μs | 80-95 | 중간-높음 | 모든 분야 |
| OLED | 60-90 | 10,000 | 낮음 | μs | >95 | 최상 | 디스플레이, 조명 |
| 레이저 다이오드 | 200-400 | 20,000 | 중간 | ns | N/A | 높음 | 프로젝터, 자동차 |

**CRI (Color Rendering Index)**는 광원이 색을 재현하는 능력을 0-100 척도로 평가한다. 태양광과 백열등은 100으로 완벽한 기준이며, 80 이상이면 양호, 90 이상이면 우수한 색재현성으로 평가된다.

### 백색 LED 구현 방식 비교

| 구현 방식 | 원리 | 효율(lm/W) | CRI | 비용 | 장점 | 단점 | 응용 분야 |
|----------|------|------------|-----|------|------|------|----------|
| 청색+인광체 | 청색 LED(450nm) + YAG:Ce 인광체 | 100-200 | 70-85 | 낮음 | 간단, 효율 우수 | CRI 낮음, 분광 불균형 | 일반 조명, 백라이트 |
| UV+RGB인광체 | UV LED(380nm) + RGB 인광체 혼합 | 60-100 | 90-98 | 중간 | CRI 최상 | 효율 낮음, 인광체 비용 | 미술관, 의료, 정밀 작업 |
| RGB LED 혼합 | 적색+녹색+청색 LED 혼합 | 80-120 | 80-95 | 높음 | 색상 제어 자유로움 | 제어 복잡, 색초점(Color Over Drive) 문제 | 디스플레이, 무대 조명 |
| RGB+인광체 | 청색 LED + 적색/녹색 인광체 | 90-150 | 85-95 | 중간 | 효율과 CRI 균형 | 설계 복잡 | 고급 조명, 자동차 |

**색초점(Color Over Drive) 문제**: RGB LED를 백색으로 구동할 때, 각 색상 LED의 광감속도(Lumen Depreciation)가 달라 시간 경과에 따라 색온도가 변하는 현상이다. 인광체 방식은 단일 LED 사용으로 색초점 문제가 없다.

### PWM 디밍 vs 아날로그 디밍 비교

| 디밍 방식 | 원리 | 효율 | 색온도 변화 | 복잡도 | 응용 분야 |
|----------|------|------|-------------|---------|----------|
| PWM 디밍 | PWM 듀티 사이클 제어로 평균 전류 조절 | 높음 (피크 전류 일정) | 없음 (색상 안정) | 중간 (PWM 제어기 필요) | 고정밀 조명, 디스플레이 백라이트 |
| 아날로그 디밍 | 직류 전류 레벨 직접 제어 | 낮음 (저전류에서 효율 감소) | 있음 (저전류에서 적색 이동) | 낮음 (저항 또는 정전류원) | 단순 조명, 저비용 응용 |

PWM 디밍은 LED의 피크 전류를 일정하게 유지하며 색온도 변화 없이 광출력을 제어할 수 있어, 고화디스플레이와 정밀 조명 제어에 표준으로 사용된다. PWM 주파수는 200Hz-5kHz 범위에서 깜빡임 없는 부드러운 디밍을 구현한다.

## Ⅳ. 실무 적용 및 기술사적 판단 (800자 이상)

### 컴퓨터 시스템에서의 LED 응용

**시스템 상태 표시 LED**: 컴퓨터 메인보드와 케이스 전면 패널에 Power LED(녹색/청색), HDD Activity LED(적색/녹색)가 장착된다. 이 LED는 2-5mA 저전류로 구동되며, 마더보드의 GPIO 제어로 ON/OFF된다. Network Interface Card(NIC)의 Link/Activity LED는 10Mbps/100Mbps/1Gbps 링크 속도를 녹색/황색/청색으로 구별하여 표시한다.

**LCD 백라이트**: 노트북과 모니터의 LCD 패널은 백라이트로 청색 LED + 인광체 백색 LED를 사용한다. CCFL(Cold Cathode Fluorescent Lamp) 백라이트 대비 30-50% 전력 절감, 2배 밝기, 5배 수명 연장, 수은 불사용의 장점이 있다. 백라이트 디밍(PWM 또는 아날로그)으로 LCD 패널의 명암비(Contrast Ratio)를 향상시키며, 로컬 디밍(Local Dimming) 기술은 패널을 영역별로 독립 디밍하여 HDR(High Dynamic Range) 효과를 구현한다.

**RGB 튜닝 조명**: 게이밍 PC 케이스, 키보드, 마우스, 램(RGB DDR)의 RGB LED는 5V 3핀(5V Data, 5V VCC, GND) 또는 12V 4핀(12V VCC, GND, R Data, G Data, B Data) 인터페이스로 제어된다. ASUS Aura Sync, MSI Mystic Light, Razer Chroma 등 소프트웨어가 동기화 제어하여 시스템 전체의 색상 테마를 통합 관리한다. PWM 주파수는 1-5kHz이며, 각 색상 채널은 8비트(256단계) 또는 12비트(4096단계) 해상도로 1600만 색상 이상을 표현한다.

**키보드 백라이트**: 기계식 키보드의 퍼키(Per-Key) RGB LED는 각 키의 스위치 하단에 개별 RGB LED를 장착하여, 키보드 전체에서 무지개색 파도(Wave Effect), 리액티브(Reactive, 입력 시 발광) 등 다양한 조명 효과를 구현한다. STM32 마이크로컨트롤러가 RGB LED 매트릭스를 스캔하며, USB HID 인터페이스로 호스트와 통신한다.

### 데이터 센터 LED 조명 설계

데이터 센터의 랙 조명은 4000K 백색 LED를 사용하여 작업자의 시인성을 확보한다. 랙 내부의 온도가 40°C 이상 상승하므로, T_j = T_a + (P × θ_j-a) = 40 + (2W × 50°C/W) = 140°C를 초과하지 않도록 히트싱크와 강제 냉각을 설계해야 한다. LED 수명을 50,000시간(약 5.7년 연속 사용)으로 유지하려면 T_j를 85°C 이하로 관리해야 하므로, θ_j-a를 25°C/W 이하로 설계해야 한다.

```
데이터 센터 랙 조명 설계 예시:
- 광출력 요구: 1000 lm
- 백색 LED 효율: 150 lm/W
- 소비 전력: 1000 / 150 = 6.7W
- LED 수: 20개 × 0.5W = 10W (여유도 1.5배)
- 히트싱크 요구 열저항:
  θ_j-a = (T_j - T_a) / P = (85 - 40) / 10 = 4.5°C/W
  따라서 θ_j-a < 5°C/W인 히트싱크 선정
```

### 기술사 시험 대비 문제 분석

**문제 1**: 5V 전원에서 적색 LED(V_F = 2.1V @ 20mA)를 구동하는 직렬 저항 값을 계산하고, 저항 소비 전력을 산정하시오.

**해설**:
```
1) 직렬 저항:
R = (V_supply - V_F) / I_F = (5 - 2.1) / 0.02 = 145Ω
표준 저항값: 150Ω (E24 시리즈)

2) 실제 전류:
I_actual = (V_supply - V_F) / R = (5 - 2.1) / 150 = 19.3mA

3) 저항 소비 전력:
P_R = I_R^2 × R = (0.0193)^2 × 150 = 0.056W
전력용량: 0.056W × 2(안전 계수) = 0.112W
따라서 1/8W(0.125W) 이상 저항 사용

4) LED 소비 전력:
P_LED = V_F × I_F = 2.1 × 0.02 = 0.042W

5) 총 효율:
η = P_LED / (P_LED + P_R) = 0.042 / (0.042 + 0.056) = 42.9%
(저항 손실으로 인한 낮은 효율, 실제는 스위칭 정전류원 사용 권장)
```

**문제 2**: 청색 LED(V_F = 3.3V @ 350mA)를 PWM 디밍하여 광출력을 50%로 감축할 때, PWM 듀티 사이클과 평균 전류를 계산하시오.

**해설**:
```
1) PWM 듀티 사이클:
D = Φ_target / Φ_max = 0.5 = 50%

2) 평균 전류:
I_avg = I_peak × D = 350mA × 0.5 = 175mA

3) 순방향 전압 (PWM ON 시):
V_F(on) = 3.3V (ON 상태 유지)

4) 평균 소비 전력:
P_avg = V_F × I_avg = 3.3 × 0.175 = 0.578W

5) 피크 전력 (ON 시):
P_peak = V_F × I_peak = 3.3 × 0.35 = 1.155W

6) PWM 주파수 요구사항:
f_pwm > 200Hz (인간 눈의 깜빡임 한계)
실제 설계: 1-5kHz (안전 마진)
```

## Ⅴ. 기대효과 및 결론 (400자 이상)

LED 기술은 조명 효율 혁명과 디스플레이 품질 향상에 기여한다. 백색 LED의 150 lm/W 효율은 백열등 대비 10배, 형광등 대비 2-3배의 전력 절감을 실현하며, 긴 수명은 교체 비용을 절감한다. 컴퓨터 시스템에서 RGB LED의 PWM 제어는 사용자 경험을 향상시키고, LCD 백라이트의 로컬 디밍 기술은 HDR 콘텐츠의 명암비를 극대화한다.

기술사는 LED 구동 회로의 전류 제어, 열 설계, PWM 디밍 제어를 포함한 통합 시스템 설계 능력을 갖춰야 한다. 특히 데이터 센터와 자동차 등 고신뢰성 응용에서는 LED 수명 예측과 열 관리가 설계 핵심이다. IoT 시대의 LED는 Li-Fi(Visible Light Communication)와 센서 융합으로 스마트 조명과 위치 추적(Positioning, Visible Light Positioning System) 등 새로운 응용 영역을 확장하고 있다.

## 📌 관련 개념 맵

```
발광 다이오드 (LED)
├── 물리 원리
│   ├── 전계 발광 (Electroluminescence)
│   ├── 밴드갭 에너지
│   ├── 전자-정공 재결합
│   └── 파장 결정 (λ = hc/E_g)
├── 재료 공학
│   ├── GaAsP (적색)
│   ├── InGaN (청색/녹색)
│   ├── AlGaInP (적색/황색/녹색)
│   └── 인광체 (백색 변환)
├── 구조
│   ├── 동종 접합 (Homojunction)
│   ├── 이종 접합 (Heterojunction)
│   ├── 더블 이종 접합 (Double Heterojunction)
│   └── 활성 층 (Active Region)
├── 구동 회로
│   ├── 직렬 저항 구동
│   ├── 정전류원 구동
│   ├── 스위칭 정전류원
│   └── PWM 디밍
├── 성능 파라미터
│   ├── 순방향 전압 (V_F)
│   ├── 순방향 전류 (I_F)
│   ├── 광출력 (Luminous Flux, lm)
│   ├── 발광 효율 (lm/W)
│   ├── 색온도 (CCT, K)
│   └── 색재현성 (CRI, 0-100)
└── 응용 분야
    ├── 상태 표시 LED
    ├── LCD 백라이트
    ├── RGB 튜닝 조명
    ├── 데이터 센터 조명
    ├── 자동차 램프
    └── 광통신 (Li-Fi)
```

## 👶 어린이를 위한 3줄 비유 설명

1. LED는 전기가 흐르면 반도체 속의 전자들이 구멍에 빠지며 에너지를 빛으로 내뱉는 작은 전구 같아요
2. LED 색깔은 반도체 재료의 "에너지 틈" 크기에 따라 결정되는데, 틈이 크면 파란색, 작으면 빨간색 빛이 나와요
3. 컴퓨터의 RGB LED는 빨간색, 초록색, 파란색 불빛을 섞어서 무지개색 모든 색을 만들어내는 색칠 놀이 같아요

---

## 💻 Python 코드: LED 열 설계 및 PWM 디밍 해석

```python
import numpy as np
import matplotlib.pyplot as plt

def led_thermal_design(V_F=3.3, I_F=0.35, T_a=40, theta_ja=50):
    """
    LED 열 설계 해석
    """
    # 소비 전력
    P_led = V_F * I_F

    # 정션 온도
    T_j = T_a + P_led * theta_ja

    # 수명 예측 (아레니우스 모델)
    # 기준: T_ref = 85°C, L_ref = 10000시간
    T_ref = 85 + 273.15  # Kelvin
    T_j_k = T_j + 273.15
    E_a = 0.5  # eV (활성화 에너지)
    k = 8.617e-5  # eV/K (볼츠만 상수)

    L_ref = 10000  # 기준 수명 (시간)
    L_T = L_ref * np.exp(E_a/k * (1/T_j_k - 1/T_ref))

    # 광출력 감소 (정션 온도 10°C 상승 시 3% 감소 가정)
    T_ref_lumen = 25  # °C
    lumen_derating = 1 - 0.03 * (T_j - T_ref_lumen) / 10

    print("=== LED 열 설계 해석 ===")
    print(f"순방향 전압: {V_F} V")
    print(f"순방향 전류: {I_F*1000} mA")
    print(f"소비 전력: {P_led} W")
    print(f"주위 온도: {T_a} °C")
    print(f"열저항(θ_j-a): {theta_ja} °C/W")
    print(f"정션 온도: {T_j:.1f} °C")
    print(f"예측 수명: {L_T:.0f} 시간 ({L_T/8760:.1f} 년)")
    print(f"광출력 유지율: {lumen_derating*100:.1f}%")

    if T_j > 125:
        print("\n⚠️  경고: 정션 온도가 125°C 초과로 수명 단축 예상됨!")
    elif T_j > 85:
        print("\n⚠️  주의: 정션 온도가 85°C 초과로 수명 감소 예상됨.")
    else:
        print("\n✅ 정션 온도가 적정 범위 내입니다.")

    return {
        'P_led': P_led,
        'T_j': T_j,
        'lifetime': L_T,
        'lumen_derating': lumen_derating
    }

def pwm_dimming_analysis(I_peak=0.35, duty_cycle=0.5, f_pwm=1000):
    """
    PWM 디밍 해석
    """
    # 평균 전류
    I_avg = I_peak * duty_cycle

    # 듀티 사이클별 광출력 (선형 가정)
    lumen_output = duty_cycle * 100  # % (100% 기준)

    # PWM 주파수 vs 깜빡임
    flicker_threshold = 200  # Hz (인간 눈의 한계)
    no_flicker = f_pwm > flicker_threshold

    print("\n=== PWM 디밍 해석 ===")
    print(f"피크 전류: {I_peak*1000} mA")
    print(f"PWM 듀티 사이클: {duty_cycle*100}%")
    print(f"PWM 주파수: {f_pwm} Hz")
    print(f"평균 전류: {I_avg*1000} mA")
    print(f"광출력: {lumen_output:.1f}%")

    if no_flicker:
        print(f"✅ 깜빡임 없음 (PWM {f_pwm}Hz > {flicker_threshold}Hz)")
    else:
        print(f"⚠️  깜빡임 가능성 있음 (PWM {f_pwm}Hz < {flicker_threshold}Hz)")

    # PWM 파라미터 계산
    T_period = 1 / f_pwm * 1000  # ms
    T_on = T_period * duty_cycle

    print(f"\nPWM 파라미터:")
    print(f"주기: {T_period:.3f} ms")
    print(f"ON 시간: {T_on:.3f} ms")
    print(f"OFF 시간: {T_period - T_on:.3f} ms")

    return {
        'I_avg': I_avg,
        'lumen_output': lumen_output,
        'no_flicker': no_flicker
    }

def rgb_color_mixing(R=255, G=100, B=50):
    """
    RGB LED 색상 혼합
    """
    # 정규화 (0-1)
    r, g, b = R/255, G/255, B/255

    # 총 광출력
    total = r + g + b

    # 색상 좌표
    x = (0.67*r + 0.21*g + 0.14*b) / total if total > 0 else 0.33
    y = (0.33*r + 0.71*g + 0.08*b) / total if total > 0 else 0.33

    # 색온도 추정 (간단 근사)
    # CCT는 xy 색도 좌표에서 Planckian locus 거리로 계산 (복잡하므로 간단 근사)
    if y > 0.4:
        cct = "Warm (<3000K)"
    elif y > 0.35:
        cct = "Neutral (3000-5000K)"
    else:
        cct = "Cool (>5000K)"

    # 16진수 컬러 코드
    hex_color = f"#{R:02x}{G:02x}{B:02x}"

    print("\n=== RGB 색상 혼합 ===")
    print(f"RGB 입력: ({R}, {G}, {B})")
    print(f"정규화 RGB: ({r:.2f}, {g:.2f}, {b:.2f})")
    print(f"색도 좌표: ({x:.3f}, {y:.3f})")
    print(f"추정 색온도: {cct}")
    print(f"16진수 코드: {hex_color}")

    return {
        'xy': (x, y),
        'cct': cct,
        'hex': hex_color
    }

# 실행
print("=" * 50)
print("LED 설계 해석 도구")
print("=" * 50)

# 1) 열 설계
thermal_result = led_thermal_design(V_F=3.3, I_F=0.35, T_a=40, theta_ja=50)

# 2) PWM 디밍
pwm_result = pwm_dimming_analysis(I_peak=0.35, duty_cycle=0.5, f_pwm=1000)

# 3) RGB 색상 혼합
color_result = rgb_color_mixing(R=255, G=100, B=50)

# 4) 최적 열저항 계산 (목표 T_j = 85°C)
print("\n=== 최적 열저항 계산 ===")
T_j_target = 85  # °C
T_a = 40  # °C
P_led = 3.3 * 0.35  # W
theta_ja_max = (T_j_target - T_a) / P_led
print(f"목표 정션 온도: {T_j_target} °C")
print(f"주위 온도: {T_a} °C")
print(f"소비 전력: {P_led} W")
print(f"최대 열저항(θ_j-a): {theta_ja_max:.2f} °C/W")
print(f"따라서 θ_j-a < {theta_ja_max:.2f} °C/W인 히트싱크 선정")
```

이 코드는 LED의 열 설계, PWM 디밍, RGB 색상 혼합을 해석하며, 기술사 시험의 열 설계와 PWM 제어 계산 문제를 대비한다.
