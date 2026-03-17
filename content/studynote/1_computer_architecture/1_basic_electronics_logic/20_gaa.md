+++
title = "20. GAA (Gate-All-Around)"
date = "2026-03-14"
weight = 20
+++

# 20. GAA (Gate-All-Around)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GAA (Gate-All-Around)는 채널의 4면 전체를 게이트가 완전히 감싸 전계(Electric Field) 제어력을 극대화하여, 단채널 효과(Short Channel Effect, SCE)를 억제하는 차세대 트랜지스터 아키텍처이다.
> 2. **가치**: 3nm 이하 공정에서 FinFET의 물리적 한계를 돌파하여, 누설 전류(Leakage Current)를 획기적으로 줄이고 구동 전류(Drive Current)는 증대시킴으로써 전력 효율 대비 성능(Performance per Watt)을 최적화한다.
> 3. **융합**: 나노시트(Nanosheet) 공정과 원자층 증착(ALD, Atomic Layer Deposition) 기술의 융합으로, AI 반도체 및 HPC (High-Performance Computing) 분야에서의 발열 문제를 해결하는 핵심 기반 기술이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**GAA (Gate-All-Around)**는 MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)의 변형으로, 게이트 전극이 채널 영역의 상하좌우 4면을 완전히 둘러싸는 3차원 구조를 말한다. 기존의 평면(Planar) 트랜지스터가 1면만 제어하고, FinFET이 3면(상면과 양 측면)을 제어하는 것에 비해, GAA는 채널을 입체적으로 감싸 게이트의 전계 제어 능력을 물리적 한계까지 끌어올린 구조다.

#### 2. 등장 배경: Scaling의 벽과 FinFET의 한계
반도체 미세 공정이 3nm 이하로 내려가면서 채널 길이가 극도로 짧아졌다. 이에 따라 **드레인 유기 장벽 하강(DIBL, Drain-Induced Barrier Lowering)** 현상이 심화되어, 게이트가 꺼져 있어도 소스(Source)에서 드레인(Drain)으로 전류가 새어 나오는 누설 전류가 급증하는 문제가 발생했다. FinFET은 핀(Fin)의 높이를 높여 3면 제어를 구현했으나, 핀의 폭이 너무 얇아지면(Quantum Confinement 효과 등) 채널 저항이 증가하고 제어력이 다시 떨어지는 한계에 도달했다. 이를 극복하기 위해 채널을 공중에 띄우고 게이트가 아래쪽까지 파고들도록 설계한 GAA가 등장했다.

#### 3. 구조 비유
**GAA는 "수도관을 쥐는 손의 악력"**과 같다. 
*   **Planar**: 수도관 위에 손을 한 겹만 올려놓은 것과 같아서, 악력이 약하면 물이 샌다.
*   **FinFET**: 수도관을 벽에 붙이고 세 손가락으로 위와 양옆을 누르는 것과 같아서, 벽에 닿는 아래쪽은 누를 수 없어 틈새가 생긴다.
*   **GAA**: 수도관을 벽에서 떼어낸 채 주먹으로 꽉 쥐는 것과 같다. 주먹을 쥐면(Vg_on) 물이 시원하게 흐르고, 주먹을 펴면(Vg_off) 완벽하게 차단된다.

```text
      [전계 제어력 비유: 물탱크와 밸브]
      
      (1) Planar       (2) FinFET        (3) GAA
      ┌──┐             ┌─┐              ┌───────┐
      │  │             │ │              │ ◀────┼─ 채널
      │  │             │ │              │       │    (전류 경로)
      └──┘             └─┘              └───────┘
     [윗면]           [윗면+양옆]        [전체 감싸기]
      ▼               ▼                 ▼
    약한 제어         강한 제어          완벽한 제어
```

**📢 섹션 요약 비유**: 
마치 고속도로 톨게이트에서 차량을 검문할 때, 기존에는 차량 옆면만 검사했다면(Planar), 벽을 붙인 상태에서 위와 양옆을 검사했던 것이(FinFET)라면, GAA는 차량을 공중에 띄운 상태에서 아래까지 360도 완전히 둘러싸 검문하는 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소
GAA 트랜지스터는 단순한 형태의 변형이 아니라, 공정과 물리적 설계가 완전히 달라진 복합 시스템이다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 및 메커니즘 | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Nanosheet (Channel)** | 전하의 이동 경로 | Si 또는 SiGe로 제작된 초박형 시트 형태로, 적층되어 전류 경로를 다중화함. | Epitaxial Growth (에피택셜 성장) | 고속도로의 차선 |
| **Gate Stack (Metal/High-k)** | 전류 흐름 제어 | Work Function Metal과 High-k 유전체가 나노시트를 감싸 전계를 형성함. | ALD (Atomic Layer Deposition) | 수도관을 쥐는 손 |
| **Inner Spacer (내부 스페이서)** | 게이트-소스 단락 방지 | 나노시트 사이에 위치하여 게이트와 소스/드레인 간의 기생 용량(Cgd)을 차단함. | Selective Etch | 절연 가스켓 |
| **S/D Epi (Source/Drain)** | 전하 공급 및 수거 | 나노시트 양 끝에 결정 성장시켜 전하를 주입/수거하는 저저항 경로 형성. | Raised Epi | 창고와 배출구 |
| **Buried Power Rail** | 전력 공급망 배면 배선 | 전원 라인을 트랜지스터 아래 웨이퍼 내부에 매몰하여 배선 효율 증대 (Option). | Deep Trench Etch | 지하 전력망 |

#### 2. GAA 구조 다이어그램 및 동작 원리

GAA의 핵심은 **"공간적 분리(Spatial Separation)"**와 **"수직 적층(Vertical Stacking)"**에 있다.

```text
   [GAA (Nanosheet FET)의 3D 단면 구조 및 제어 영역]

        Source (N+)          Gate (Control)           Drain (N+)
           ▲                     ▲                        ▲
           │                     │                        │
      ┌────┴────┐          ┌────┴────┐             ┌─────┴─────┐
      │  ┌────┐ │          │  ┌────┐ │             │  ┌────┐   │
      │  │Sheet│ │◀───────┼─┼│Wrap│─┼────────────▶│  │Sheet│   │
      │  │ #3  │ │          │  │#3  │ │             │  │ #3  │   │
      │  └────┘ │          │  └────┘ │             │  └────┘   │
      │  ┌────┐ │          │  ┌────┐ │             │  ┌────┐   │
      │  │Spacer│ │         │  │Wrap│─┼────────────▶│  │Sheet│   │
      │  │     │ │◀───────┼─┼│#2  │ │             │  │ #2  │   │
      │  └────┘ │          │  └────┘ │             │  └────┘   │
      │  ┌────┐ │          │  ┌────┐ │             │  ┌────┐   │
      │  │Sheet│ │◀───────┼─┼│Wrap│─┼────────────▶│  │Sheet│   │
      │  │ #1  │ │          │  │#1  │ │             │  │ #1  │   │
      │  └────┘ │          │  └────┘ │             │  └────┘   │
      └─────────┘          └─────────┘             └───────────┘
           ▲                     ▲                        
           └─────────────────────┘                        
            Substrate / Isolation

   [LEGEND]
   Sheet: 전류가 흐르는 도체 채널 (Si Nanowire/Sheet)
   Wrap : 게이트 절연막 및 금속이 시트를 감싸는 형태 (All-Around)
   Spacer: 게이트와 S/D 사이를 전기적으로 분리하는 내부 절연체
```

**[다이어그램 해설]**:
FinFET이 '수직으로 선 지느러미'라면, GAA는 '수평으로 놓인 얇은 종이(Nanosheet)'를 여러 장 겹쳐 놓은 형태다. 
1.  **형성**: 먼저 Si(규소)와 SiGe(규소-게르마늄) 층을 번갈아 적층한다.
2.  **교체(Sacrificial Release)**: 중간의 SiGe 층만 선택적으로 식각(Etching)해 제거하면, Si 층만 공중에 떠 있는 다리(Bridge) 형태가 남는다.
3.  **감싸기(Wrap)**: 이 틈새에 **ALD (Atomic Layer Deposition, 원자층 증착)** 공정을 통해 절연막과 게이트 금속을 원자 단위로 채워 넣는다. 이로써 게이트가 채널의 아랫면까지 침투하여 4면 모두를 닿게 된다.

#### 3. 핵심 공식 및 설계 변수
GAA의 성능은 나노시트의 폭(Wsheet)과 적층 수(Nstack)에 의해 결정된다. 채널 폭이 좁을수록 전계 제어력은 좋아지지만(누설 감소), 저항이 커져 구동 전류가 감소한다. 따라서 **"SS (Subthreshold Swing)"** 지표가 핵심이다.

*   **Id (Drive Current)** ∝ (2 × Wsheet + 2 × Hsheet) × Nstack
    *   (폭과 높이, 그리고 적층 개수에 비례하여 전류 용량 확보)
*   **Cgg (Gate Capacitance)**: FinFET 대비 게이트-채널 간 커패시턴스가 증가하므로, 이를 상쇄하는 RC 지연(RC Delay) 최적화 설계가 요구됨.

#### 4. 코드: 전기적 특성 모델링 (Python 스타일 의사코드)
```python
# GAA Transistor Modeling Pseudo-code
class GAATransistor:
    def __init__(self, num_sheets, sheet_width, sheet_height, length):
        self.Nstack = num_sheets        # Number of stacked nanosheets
        self.Wsheet = sheet_width        # Width of each sheet (nm)
        self.Hsheet = sheet_height       # Thickness of the sheet (nm)
        self.Lch    = length             # Channel length (nm)

    def calculate_effective_width(self):
        """
        FinFET과 달리 GAA는 시트 폭(Wsheet)을 설계 자유도로 가짐.
        게이트가 채널을 둘러싸는 면적(Perimeter) 계산.
        """
        # 상하 + 좌우 면적
        perimeter_per_sheet = (2 * self.Wsheet) + (2 * self.Hsheet)
        total_width = perimeter_per_sheet * self.Nstack
        return total_width

    def estimate_leakage(self, vdd, threshold_voltage):
        """
        전계 제어력 향상에 따른 누설 전류 감소 모델링
        """
        # GAA는 전계 계수(Electrostatic Control Coefficient)가 높음
        control_factor = 0.98  # FinFET(0.85) 대비 향상
        i_off = (vdd - threshold_voltage)**2 * (1 - control_factor)
        return i_off

# Example: MBCFET (Samsung) 특화 설계
mbcfet = GAATransistor(num_sheets=3, sheet_width=20, sheet_height=5, length=12)
print(f"Effective Channel Width: {mbcfet.calculate_effective_width()}nm")
```

**📢 섹션 요약 비유**: 
GAA의 나노시트 적층 구조는 **"이층버스에서 승객을 태우는 것"**과 같습니다. 한 대의 버스(채널)에 승객(전류)을 너무 많이 태우면 버스가 무거워 느려지는 대신, 버스를 2층으로 만들거나(3D) 버스 대수(적층 수)를 늘려서, 좁은 도로(칩 면적)에서도 더 많은 승객을 빠르게 운반할 수 있게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. 구조적 심층 비교: FinFET vs. GAA (Nanosheet)

| 구분 | FinFET (Tri-Gate) | GAA (Nanosheet) | 분석 및 시사점 |
|:---|:---|:---|:---|
| **채널 형상** | 수직 지느러미 (Fin) | 수평 평판 (Sheet) | **유연성**: GAA는 채널 폭(Fin 폭)을 자유롭게 조절 가능하여, Low-power Cell과 High-drive Cell을 별도로 설계(DTCO)할 수 있음. |
| **게이트 접촉** | 3면 (Top + 2 Sides) | 4면 (Wrap-around) | **제어력**: 전하 분포(Channel Potential)가 게이트 전압에 완전히 종속되어 Short Channel Effect 억제력이 월등함. |
| **공정 핵심** | Fin Patterning | **Inner Spacer & Selective Etch** | **난이도**: 나노시트 사이의 희생층을 제거하고 빈 틈을 메우는 공정은 정밀도가 극도로 요구됨. |
| **전기적 특성** | 상대적으로 높은 Vth (Threshold Voltage) 불균형 | 낮은 Vth 편차, 우수한 Subthreshold Swing (SS) | **신뢰성**: 전압 변동에 따른 성능 편차가 적아 고주파수 동작에 유리함. |

#### 2. 타 영역(공정/물성) 융합 분석

GAA는 단순히 설계(Layout)의 변경이 아니라, 소재(Material)와 공정(Process)의 융합 결정체다.

*   **소재 융합 (Material Science)**:
    *   **SiGe Channel**: 채널 내부에 게르마늄(Ge)을 주입하여 전자 이동도(Mobility)를 높이는 기술과 결합되어 **Strained GAA** 구조로 진화 중이다.
    *   **High-k/Metal Gate**: 게이트 유전체로 HfO2 (Hafnium Oxide)