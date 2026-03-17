+++
title = "16. FET (전계효과 트랜지스터)"
date = "2026-03-14"
weight = 16
+++

# # [FET (전계효과 트랜지스터, Field Effect Transistor)]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전압에 의해 생성된 **전계(Electric Field)**를 통해 반도체 표면의 채널을 형성하고 전류를 제어하는 **단극성(Unipolar)** 소자이다.
> 2. **가치**: 입력 단자인 **게이트(Gate)**가 전기적으로 절연되어 입력 임피던스가極高하고, 스위칭 시에만 전력을 소모하는 구조로 인해 수백억 개의 소자를 집적하는 **초고밀도 집적 회로(VLSI)** 구현의 물리적 토대이다.
> 3. **융합**: **MOSFET(Metal-Oxide-Semiconductor Field Effect Transistor)** 구조를 기반으로 CMOS 로직을 구성하여 발열을 억제하고, 이를 **FinFET**, **GAA(Gate-All-Around)** 등 3차원 나노 구조로 진화시켜 무어의 법칙 연장을 주도하고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**FET (Field Effect Transistor)**는 반도체 표면에 전압을 가하여(혹은 가하지 않아) 생성되는 **전계(Electric Field)**의 힘으로 전하의 흐름(전류)을 조절하는 3단자 반도체 소자이다. 
**BJT (Bipolar Junction Transistor)**가 베이스 전류를 통해 콜렉터 전류를 제어하는 **전류 제어형(Current Controlled)** 소자인 반면, FET는 게이트 단자에 가해지는 전압만으로 소스와 드레인 사이의 전류 경로(채널)의 저항을 변화시키는 **전압 제어형(Voltage Controlled)** 소자이다.
전류의 주도적 운반자가 전자(Electron)인지 정공(Hole)인지에 따라 N채널형과 P채널형으로 나뉘며, FET 내부에서는 다수 캐리어(Majority Carrier)만이 전류를 수행하므로 **단극성(Unipolar)** 소자로 분류된다.

### 2. 등장 배경 및 기술적 패러다임
1948년 접합형 트랜지스터(BJT) 발명 이후, 증폭 기능은 뛰어났으나 고밀도 논리 회로 구현에는 한계가 있었다. BJT는 'ON' 상태를 유지하기 위해 지속적으로 베이스 전류를 공급해야 하므로, 소자 수가 늘어날수록 소모 전력과 발열이 기하급수적으로 증가했다. 이를 극복하기 위해 1960년대 다와한 카흐(Dawon Kahng)와 마틴 아탈라(Martin Atalla)가 **SiO2 (Silicon Dioxide)** 절연막을 이용한 MOSFET을 개발하면서, 정전 용량 결합을 통해 전계를 형성하고 전류를 차단하는 거의 완벽한 스위치 특성을 확보하게 되었다. 이는 현대 디지털 컴퓨팅의 시대를 여는 결정적인 전환점이 되었다.

### 3. FET 기본 구조 다이어그램

```text
       [ 일반적인 FET의 3단자 구조 및 전류 흐름도 ]
       
   Drain (D) ────────┬───────────────────────┐
        (전하 배출구)   │                       │
                      │       ▲               │
                      │       │  ID (Drain Current)
                      │       │               │
                      │       │               │
   Gate (G)  ─────────┼───────┼───────┐       │
        (전압 인가)    │       │       │       │
                      │=== Gate Insulator ===│
                      │       │       │       │
                      │   [Substrate/Body]    │
                      │       │       │       │
                      │       ▼       │       │
   Source (S) ────────┴───────────────────────┘
        (전자 공급원)  

   ⚡ 작동 원리 요약:
   1. Gate-Source 간에 전압(Vgs)을 인가하지 않으면 -> Channel 형성 안 됨 (OFF)
   2. Vgs가 임계 전압(Vth)을 초과하면 -> 전계(Electric Field) 발생 -> Channel 형성 (ON)
   3. Vds를 걸면 -> 전자가 Source에서 Drain로 이동 (N-Channel 경우)
```

*   **[다이어그램 해설]**:
    상기 다이어그램은 FET의 핵심 구조를 도식화한 것이다. 핵심은 게이트(G)와 채널 사이의 **절연막(Insulator)**이다. 이로 인해 게이트에 흐르는 전류는 사실상 0에 수렴하며(IG ≒ 0), 게이트 단자의 전위만으로 채널 내부의 전자 밀도를 조절한다. 마치 수도관 위에 올라선 사람이 손가락 힘 하나로 관을 쥐어 짜 물의 흐름을 멈추는 것과 유사한 메커니즘이다. 이 구조적 특징이 FET가 고회로 집적에 적합한 이유를 설명한다.

> **📢 섹션 요약 비유**: FET는 **"수도 계량기의 검침원과 수도관의 밸브가 분리된 구조"**와 같습니다. BJT가 수도관을 틀기 위해 직접 물을 퍼붓는(전류를 흘리는) 방식이라면, FET는 발끝으로 밸브를 살짝 누르는(전압을 가하는) 힘만으로도 강물과 같은 전류의 흐름을 제어할 수 있는 비접촉식 제어 장치입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 상세 분석

FET의 동작을 이해하기 위해서는 각 단자의 물리적 역할과 내부 동작 메커니즘을 이해해야 한다.

| 요소명 (Element) | 물리적 역할 (Role) | 내부 동작 및 프로토콜 (Internal Operation) | 주요 설계 파라미터 (Parameter) |
|:---:|:---|:---|:---|
| **Source (S)** | 다수 캐리어(Majority Carrier)가 유입되는 출발지 | N-FET의 경우 전자(Electron)를 공급함. 채널과 도핑 농도가 동일하게 설계됨. | Rs (Source Resistance) |
| **Drain (D)** | 다수 캐리어가 빠져나가는 도착지 | 전압 차이(Vds)에 의해 캐리어를 끌어당김. 고전력 소자에서는 열발생 주요 원인. | Rd (Drain Resistance) |
| **Gate (G)** | 전계(Electric Field)를 생성하는 제어 단자 | 절연막을 통해 전압을 인가하여 채널 내부의 전하 밀도를 조절 (진성 혹은 반전층 형성). | Cox (산화막 정전 용량), Vth (임계 전압) |
| **Channel** | 전류가 흐르는 유로 (Pathway) | 게이트 전압에 의해 형성되는 가상의 도체층 (Inversion Layer). 길이(L)와 폭(W)이 전류량을 결정. | W/L (Aspect Ratio) |
| **Body/Substrate (B)** | FET의 물리적 기반이 되는 기판 | 채널 형성의 무대가 되며, 바이어스 전압(Vbs)을 통해 Vth를 제어하는 역할(Body Effect) 수행. | Vbs (Body-Source Voltage) |

### 2. I-V 특성 및 동작 영역 (Operating Regions)

FET의 동작은 게이트-소스 전압($V_{GS}$)과 드레인-소스 전압($V_{DS}$)의 상대적인 크기에 따라 세 가지 영역으로 구분된다.

```text
   [ FET의 I-V 특성 곡선 및 동작 영역도 (N-Channel Enhancement Mode) ]
   
   
 Id
 ▲
 │          │   (Linear / Ohmic Region)
 │          │   채널이 저항처럼 동작 (Vds가 작을 때)
 │          │───────────────────────
 │          │      ＼
 │          │       ＼
 │          │        ＼ (Saturation Region)
 │          │         ＼    전류 일정 (증폭기/스위치 동작)
 │          │          ＼─────────────
 │          │           ＼
 │          │            ＼
 │          │             ＼
 │          │              ＼
 └────────────────────────────────────▶ Vds
       0        Vov      Vds,sat
   
   [주요 수식 모델: Shichman-Hodges Model]
   
   1. 차단 영역 (Cutoff Region):
      IF Vgs < Vth THEN Id ≈ 0 (OFF 상태)
   
   2. 선형 영역 (Linear/Triode Region):
      IF Vgs ≥ Vth AND Vds < (Vgs - Vth) THEN
      Id = β * [ (Vgs - Vth)*Vds - (Vds^2)/2 ]
      (단, β = (μ * Cox * W) / L : 도전율 계수)
      
   3. 포화 영역 (Saturation Region):
      IF Vgs ≥ Vth AND Vds ≥ (Vgs - Vth) THEN
      Id = (β/2) * (Vgs - Vth)^2 * (1 + λ*Vds)
      (λ: 채널 길이 변조 계수, Pinch-off 발생)
```

*   **[다이어그램 해설]**:
    위 그래프는 디지털 회로에서 스위치로 사용되는 FET의 핵심 동작 특성을 보여준다. 디지털 회로는 주로 '차단(Cutoff)'과 '포화(Saturation)' 영역을 오가며 동작한다. 
    1.  **차단 영역**: $V_{GS}$가 낮아 채널이 형성되지 않아 전류가 흐르지 않는 '0' 상태.
    2.  **포화 영역**: $V_{GS}$를 높여 채널이 형성되면, 드레인 단 쪽 끝이 'Pinch-off(꼬임)'되어도 전류는 포화 상태에 도달하여 일정하게 흐른다. 이때 전류는 식 $I_D \propto (V_{GS} - V_{th})^2$ 에 따라 급격히 증가한다. 즉, 게이트 전압의 작은 변화가 드레인 전류의 큰 변화로 이어지는 증폭 작용이 일어나는 영역이다.

### 3. 물리적 핵심 원리: 전계 효과 (Field Effect)

게이트 단자에 양의 전압($V_{GS} > 0$)을 가하면, P형 기판(Substrate) 내부의 자유 전자(Electron)들이 정전기적 인력(Coulomb Force)에 의해 게이트 아래쪽 표면으로 끌려 모인다. 이로 인해 원래 P형(정공 주도)이던 기판 표면이 N형(전자 주도)의 성질을 띠게 되는데, 이를 **전도 반전(Inversion)**이라 하며, 이렇게 형성된 얇은 층을 **역층(Inversion Layer)** 혹은 **채널(Channel)**이라 한다. 이 모든 과정이 게이트 단자로 실제 전하가 유입되지 않고, 단순히 전기장만으로 전자의 분포를 조정하므로 **FET(Field Effect Transistor)**라 명명되었다.

> **📢 섹션 요약 비유**: 마치 **"자기부상열차(Maglev)의 궤도 제어 시스템"**과 같습니다. 레일 위에 직접 차륜을 굴려서(전류 흘려서) 제어하는 것이 아니라, 전자기력(전계)을 이용해 차체를 띄우고 속도를 조절하듯, FET는 절연된 게이트가 전기적 힘으로 전하의 길을 뚫어주고 통제합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. 구조적 비교: JFET vs. MOSFET

FET는 크게 접합형(JFET)과 MOSFET으로 구분되며, 현대 디지털 회로는 MOSFET이 주류를 이룬다.

| 비교 항목 | JFET (Junction FET) | MOSFET (Metal-Oxide-Semiconductor FET) |
|:---|:---|:---|
| **게이트 구조** | PN 접합 다이오드 형성 (반도체-반도체 접합) | **MOS 구조 (Metal-Insulator-Semiconductor)** |
| **동작 모드** | 공핍형 (Depletion Mode)만 존재 | 공핍형 (Depletion) 및 **강화형 (Enhancement)** 모두 가능 |
| **입력 임피던스** | 높음 (약 $10^8 \Omega$) | **극도로 높음** (약 $10^{12} \sim 10^{15} \Omega$) |
| **누설 전류** | 게이트 역 바이어스 시 누설 전류 존재 | 게이트 전류가 사실상 0 (무시 가능) |
| **집적도** | 소규모 아날로그 회로에 주로 사용 | 초고밀도 디지털 집적 회로(IC)에 필수적 |
| **공정 복잡도** | 상대적으로 단순 | 미세 공정(FinFET, GAA)으로 진화 중 |

### 2. 제어 원리 비교: BJT vs. FET

| 비교 지표 | BJT (Bipolar Junction Transistor) | FET (Field Effect Transistor) |
|:---|:---|:---|
| **제어 변수** | 베이스 전류 ($I_B$) | 게이트 전압 ($V_{GS}$) |
| **캐리어** | 소수(Sojourn) & 다수(Majority) 캐리어 모두 참여 | **다수 캐리어**만 참여 (단극성) |
| **입력 특성** | 낮은 입력 임피던스 (전력 구동 필요) | **높은 입력 임피던스** (전압 구동만 가능) |
| **스위칭 속도** | 매우 빠름 (GHz 대역 이상) | 빠름 (공정 미세화로 BJT 추격) |
| **열 발생 (Static)** | 높음 (ON 상태 시 지속적 전력 소모) | **낮음** (Static Power ≈ 0) |
| **이상적 용도** | 고주파 증폭기, 고출력 전력 제어 | **메모리, CPU, 로직 스위칭** |

### 3. 과목 융합 분석: CMOS와 발열 (Convergence with Computer Architecture)

컴퓨터 아키텍처 관점에서 FET의 가장 중요한 응용은 **CMOS (Complementary Metal-Oxide-Semiconductor)** 인버터 구현이다.
-   **구조**: P-Channel FET와 N-Channel FET를 직렬로 연결하여, 하나는 Pull-up, 다른 하나는 Pull-down 역할을 하게 한다.
-   **메커니즘**: 입력이 High일 때 N-FET가 ON, P-FET가 OFF되어 Ground로 연결되며, 입력이 Low일