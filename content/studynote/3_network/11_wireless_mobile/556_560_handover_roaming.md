+++
title = "556-560. 핸드오버와 로밍 기술"
date = "2026-03-14"
[extra]
+++

# 556-560. 핸드오버와 로밍 기술

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이동통신 시스템에서 단말(MS)의 이동성(Mobility)을 보장하기 위해 무선 채널을 유지하며 전환하는 핸드오버(Handover)와 타 망 연동을 위한 로밍(Roaming)은 무선 네트워크의 핵심 신뢰성 기술이다.
> 2. **가치**: Hard Handover의 주파수 효율성과 Soft Handover의 무결점(Seamless) 서비스 제공 능력을 상황에 맞게 설계하여 Call Drop Rate(호 끊김율)을 최소화하고 사용자 QoS(Quality of Service)를 보장한다.
> 3. **융합**: 5G 이동성 관리(MM), 이동성 관리 엔티티(MME), 세션 관리 등 코어 네트워크와 밀접하게 연동되며, 위치 기반 서비스(LBS) 및 보안 인프라와 융합된다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 1. 개념 및 정의
**핸드오버(Handover)** 또는 핸드오프(Handoff)는 이동 통신 단말기(Mobile Station, MS)가 서비스 중인 기지국(Base Station, BS)의 커버리지를 벗어나 인접한 다른 기지국으로 이동할 때, 통화 중단 없이 무선 채널(Radio Channel)을 자동으로 전환하는 기술을 의미합니다. 또한 **로밍(Roaming)**은 가입자가 자신이 가입한 홈 네트워크(Home PLMN)가 아닌 방문 네트워크(Visited PLMN) 지역에 있을 때도 통신 서비스를 제공받을 수 있도록 하는 망 간 연동 서비스입니다. 이 두 기술은 이동통신의 가장 근본적인 전제인 "이동 중에도 끊김 없는 연결성"을 실현하는 핵심 메커니즘입니다.

#### 2. 기술적 배경 및 필요성
초기 이동통신 환경에서는 셀(Cell)의 크기가 컸으나, 데이터 트래픽의 폭발적 증가와 주파수 자원의 효율적 재사용(Frequency Reuse)을 위해 셀 크기는 점점 작아지고(마이크로/피코셀), 기지국의 설치 밀도는 높아지고 있습니다. 사용자가 고속 이동할 때마다 수시로 기지국을 바꿔야 하며, 빌딩 음영지(Shadowing)나 페이딩(Fading) 현상으로 인한 신호 감쇠에 대비해야 합니다. 따라서 핸드오버는 단순한 기능을 넘어 네트워크의 신뢰성(Reliability)과 가용성(Availability)을 결정짓는 결정적 요소로 작용합니다.

#### 3. 세부 구분 및 발전 과정
핸드오버는 크게 연결 전환 방식에 따라 **Hard Handover**와 **Soft Handover**로 나뉩니다. 1세대 아날로그와 2세대 GSM(Global System for Mobile Communications), 그리고 4G LTE(Long Term Evolution)에서는 주로 Hard Handover가 사용되어 주파수 자원 효율을 높였습니다. 반면, 2세대 CDMA(Code Division Multiple Access)와 3G WCDMA(Wideband CDMA)에서는 Soft Handover를 통해 통화 품질을 극대화했습니다. 5G NR(New Radio)에서는 Dual Connectivity(이중 연결) 기술을 기반으로 하여 Hard와 Soft의 장점을 융합한 보다 진보된 형태의 핸드오버를 수행합니다.

```ascii
+----------------+                  +----------------+
|   CELL A       |                  |   CELL B       |
| (Current BS)   |                  |   (Target BS)  |
|                |    Signal        |                |
|      _______   |    Weakens       |      _______   |
|     /       \  |   =======>      |     /       \  |
|    |  BS-A   | |                 |    |  BS-B   | |
|     \_______/  |                 |     \_______/  |
|      /     \   |                 |      /     \   |
+------+-----+---+                 +------+-----+---+
       ^     ^                             ^     ^
       |     |                             |     |
       +-----+-----------------------------+-----+
                       |
                 v Handover Trigger
```
*(도해 1: 핸드오버 발생 시점의 신호 세기 변화 및 셀 경계 트리거 지점)*

#### 4. 로밍 아키텍처
로밍은 단순히 기지국을 바꾸는 핸드오버와 달리, **망 간 인증과 정산 청구**가 수반되는 비즈니스 및 프로토콜 레벨의 복잡한 협약 기술입니다. 이를 위해 국제 로밍 표준인 GSMA(Global System for Mobile Communications Association) 프로토콜이 존재하며, 홈 위치 등록기(HLR, Home Location Register) 및 방문 위치 등록기(VLR, Visitor Location Register) 간의 데이터 교환(SS7 signaling)이 필수적입니다.

> **📢 섹션 요약 비유**: 
> 핸드오버와 로밍의 관계는 **'고속도로 주행'**과 **'타 지역 도로 통행료 징수'**와 같습니다. 핸드오버는 차량이 고속도로 톨게이트를 통과하거나 차선을 변경할 때 속도를 줄이지 않고 자연스럽게 진입하는 기술이고, 로밍은 내 지역(Home)에서 낸 통행료(요금제)를 바탕으로 다른 지역(Visited)의 고속도로를 이용하되, 나중에 해당 지역 관공서와 비용을 정산하는 제도입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 핸드오버 결정 및 제어 구조
핸드오버 과정은 크게 **측정(Measurement)**, **판결(Decision)**, **실행(Execution)**의 3단계로 구성됩니다. 이 과정은 네트워크 인프라(Network-Controlled) 혹은 단말기(Mobile-Assisted/Mobile-Controlled)에 의해 주도됩니다.

*   **Hysteresis Margin (히스테리시스 마진)**: 기지국 A의 신호가 기지국 B보다 약간 낮다고 해서 즉시 핸드오버를 진행하면, 신호가 순간적으로 다시 좋아질 때 불필요하게 핸드오버가 반복되는 **Ping-Pong Effect**가 발생합니다. 이를 방지하기 위해 기지국 B의 신호가 일정 수준(Hysteresis) 더 높아야만 핸드오버를 트리거하는 임계값을 설정합니다.
*   **Time to Trigger (TTT)**: 신호 조건이 충족된 후 실제 핸드오버 명령을 내리기까지 대기하는 시간으로, 순간적인 신호 요동(Flickering)에 의한 오동작을 방지합니다.

```ascii
      Signal Strength
         ^
         |       (Handover Margin / Hysteresis)
         |           |----|
         |           v    v
         |     BS-B _-_______------- Triggered
         |           /        \
         |          /          \
 BS-A   /|_________/            \_________
        /|
       / |__________________________________> Time
          ^          ^           ^
          |          |           |
      Strong      Threshold     Handover
      Signal     Met           Start

(Ping-Pong 방지를 위한 Hysteresis Margin 개념도)
```

#### 2. Hard Handover (Hard Handoff) 상세 분석
Hard Handover는 **Break-Before-Make** 방식으로, 현재 무선 링크(Radio Link)가 끊어진 이후에야 새로운 링크가 형성되는 비연속적 전환 방식입니다. TDMA(Time Division Multiple Access)나 FDMA(Frequency Division Multiple Access) 기반 시스템(GSM, LTE)에서 주로 사용됩니다.

*   **장점**: 동시에 두 개의 채널을 점유하지 않으므로 무선 자원(Radio Resource) 효율이 높습니다.
*   **단점**: 전환 시점에 **Transmission Gap**이 발생하여 패킷 손실(Packet Loss)이 발생할 수 있으며, 이는 음성 품질 저하나 데이터 재전송 오버헤드로 이어질 수 있습니다.

#### 3. Soft Handover (Soft Handoff) 상세 분석
Soft Handover는 **Make-Before-Break** 방식으로, 단말기가 동시에 두 개 이상의 기지국과 무선 링크를 유지하는 상태(Macrodiversity)에서 점진적으로 타겟 셀로 연결을 이동하는 방식입니다. CDMA 계열 기술의 핵심입니다.

*   **Gain Selection (셀렉티브 다이버시티)**: 단말기는 두 기지국에서 받은 신호 중 더 좋은 신호를 처리하여 순간적인 신호 감쇠(Fading)에 강합니다.
*   **Soft Softer Handover**: 동일한 기지국 내의 다른 섹터(Sector)로 핸드오버하는 경우를 말하며, 기지국 내부에서 합산(Combining) 처리가 이루어집니다.

```ascii
[Hard Handover Sequence]

[BS A]     切断      [MS]      连接      [BS B]
  |----------X         |--------------------->|
  (Link A Broken)      (Link B Established)
        <-- Brief Disconnection (Switching Time) -->

[Soft Handover Sequence]

[BS A]      保持      [MS]      连接      [BS B]
  |--------------------|--------------------->|
  |<---Link A Active----|<---Link B Active----|
  (Diversity Combining in MS)
        <-- No Disconnection / Seamless Transition -->
```

#### 4. 로밍 프로토콜 및 신호 처리
로밍 서비스는 크게 **인증(Authentication)**, **위치 등록(Location Update)**, **호 처리(Call Handling)** 과정으로 나뉩니다. 이때, **MAP (Mobile Application Part)** 프로토콜이 SS7 망을 통해 교환기들 간의 신호를 주고받습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/표준 (Protocol) |
|:---|:---|:---|:---|
| **HLR (Home Location Register)** | 홈 데이터베이스 | 가입자의 프로필, 서비스 권한, 현재 위치(VLR 주소) 영구 저장 | SS7/MAP, Diameter (LTE) |
| **VLR (Visitor Location Register)** | 방문지 데이터베이스 | 방문 가입자의 일시 정보 임시 저장 및 인증 데이터 관리 | SS7/MAP |
| **MSC (Mobile Switching Center)** | 교환기 | 통화 연결 제어 및 로밍 사용자의 호 착신/발신 제어 | ISUP, TUP |
| **AuC (Authentication Center)** | 보안 인증서버 | RAND/Challenge 생성 및 SRES/Ki 검증하여 부정 로밍 방지 | MAP |

#### 5. 핸드오버 알고리즘 예시 (Pseudo-code)
실무 수준에서의 핸드오버 판단 로직은 다음과 같은 수식에 기반합니다.

$$ P_{target} > P_{serving} + \text{Margin} + \text{Hysteresis} $$

```python
# Pseudo-code for Handover Decision Logic
class HandoverManager:
    def evaluate_handover(self, serving_rsrp, neighbor_rsrp_list):
        HANDOVER_MARGIN = 2.0  # dB
        HYSTERESIS = 3.0       # dB (Ping-pong prevention)
        TTT_TIMER = 160        # ms

        best_neighbor = max(neighbor_rsrp_list)
        
        if (best_neighbor - serving_rsrp) > (HANDOVER_MARGIN + HYSTERESIS):
            self.start_ttt_timer(TTT_TIMER)
            if self.ttt_timer_expired():
                return True, "TRIGGER_HANDOVER"
        
        return False, "KEEP_CURRENT"
```

> **📢 섹션 요약 비유**: 
> **Hard Handover**는 비행기가 공항 이착륙 시 반드시 지상에 엔진을 끄고 내려와야 하듯, 연결을 완전히 끊고 다시 시작하는 엄격한 절차입니다. 반면 **Soft Handover**는 두 대의 열차가 나란히 달리는 동안 승객이 이동한 뒤 한 열차가 떨어져 나가는 것처럼, 안전을 위해 **중복 연결(Macrodiversity)**을 유지하는 이중 보험 시스템입니다. 로밍의 **VLR/HLR 구조**는 여행자가 해외 호텔에 체크인할 때, 본국의 여권(Home) 정보를 바탕으로 현지 호텔 방명록(Visitor)에 임시 주소를 남기는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. Hard Handover vs Soft Handover 기술 비교 분석

| 비교 항목 (Criteria) | Hard Handover (GSM, LTE) | Soft Handover (CDMA, WCDMA) |
|:---|:---|:---|
| **연결 메커니즘** | Break-Before-Make (비연속적) | Make-Before-Break (연속적) |
| **무선 자원 점유** | 낮음 (Low Overhead) | 높음 (즉시 2개 채널 점유) |
| **트래픽 감쇄 (Interference)** | 낮음 (한 번에 하나의 채널) | 높음 (다중 접속에 따른 간섭 증가 가능성) |
| **음질/신뢰성** | 전환 구간에서 끊김 가능성 존재 | 매우 부드러움 (Seamless), 페이딩에 강함 |
| **네트워크 부하** | 낮음 | 높음 (다중 링크 유지 및 Combine 연산 필요) |
| **구현 복잡도** | 단순함 | 복잡함 (Power Control 및 Rake Receiver 필요) |

#### 2. 로밍 유형별 비교 분석

| 로밍 유형 | 설명 (Description) | 과금 청구 (Billing) | 주요 시나리오 (Scenario) |
|:---|:---|:---|:---|
| **국내 로밍** | 타 통신사(혹은 산간 오지)의 망을 빌려쓰는 경우 | 자사 요금제 적용 (후에 망 사용료 정산) | 알뜰폰(MVNO) 가입자가 이동통신사(MNO) 망 이용 시 |
| **국제 로밍** | 해외 통신사(Visited PLMN) 망을 이용하는 경우 | 로밍 요금 부과 (Home PLMN이 가입자에게 청구) | 해외 출장/여행 시 데이터 로밍 ON 상태 |
| **SIM 기반 로밍** | 로컬 SIM 카드를 교체하여 현지망 이용 | 현지 요금제 직접 납부 | eSIM 프로파일 다운로드 |

#### 3. 타 영역(시스템/보안)과의 융합
핸드오버와 로밍은 단순한 전송 계층(Layer 2/3)의 문제를 넘어 상위 계층과 밀접하게 융합됩니다.
*   **보안(Security)**: 로밍 시 사용자는 알 수 없는 네트워크에 접속하므로 **Authentication Triplet (RAND, SRES, Kc)** 또는 **LTE/5G의 AKA (Authentication and Key Agreement)** 절차를 통해 신