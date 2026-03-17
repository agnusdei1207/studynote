+++
title = "584-586. 무선 네트워크 보안 및 인프라 관리 (802.1X, dBm)"
date = "2026-03-14"
[extra]
category = "Wireless & Mobile"
id = 584
+++

# 584-586. 무선 네트워크 보안 및 인프라 관리 (802.1X, dBm)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무선 네트워크의 가상화된 경계를 보호하기 위해 **IEEE 802.1X (Port-Based Network Access Control)** 기반의 인증 메커니즘이 필수적이며, 이는 물리적 포트를 논리적으로 제어하는 보안 표준이다.
> 2. **가치**: **Captive Portal ( captive portal )**을 통해 게스트 접속의 편의성을 확보하고, **dBm (Decibel-milliwatts)**을 활용한 정밀한 사이트 설계(Site Survey)로 신호 품질(QoS)과 보안 구역을 정량적으로 관리할 수 있다.
> 3. **융합**: 유선 보안 정책(RADIUS)을 무선 환경으로 확장하여 NAC(Network Access Control) 시스템과 통합하고, 신호 강도 측정은 IoT/5G 네트워크 최적화 및 위치 기반 서비스(LBS)의 기반 데이터가 된다.

+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
무선 네트워크(Wireless LAN)는 유선과 달리 전파 경계가 명확하지 않아 악의적인 침입에 취약할 수밖에 없다. 이를 방지하기 위해 **IEEE 802.1X (IEEE 802.1X Standard for Port-Based Network Access Control)**는 단말이 네트워크 리소스에 접근하기 전에 엄격한 인증을 수행하는 표준 프로토콜로 자리 잡았다. 또한, 대중에게 개방된 공공망에서는 사용자의 편의성과 보안을 동시에 충족시키기 위해 **Captive Portal**이 사용된다. 한편, 이러한 네트워크의 물리적 성능을 보장하기 위해 전파의 세기를 로그 스케일로 표현하는 **dBm (Decibel relative to one milliwatt)** 단위가 필수적인 메트릭으로 활용된다.

**💡 비유**
802.1X는 아파트 출입구에 있는 '공동현관 키패드와 인터폰' 시스템과 같다. 캡티브 포털은 카페에 처음 들어갔을 때 주문을 위해 '줄 서서 대기하는 공간'과 같다. dBm은 상대방의 목소리가 얼마나 크게 들리는지를 '소리 데시벨(dB)'로 정확히 측정하는 것이다.

**등장 배경**
① **기존 한계**: 초기 무선망(WEP, Pre-Shared Key)은 공유 키가 노출되면 네트워크 전체가 무력화되는 구조적 취약점이 존재함.
② **혁신적 패러다임**: 사용자별(User-based) 동적 인증과 중앙 관리형 정책(RADIUS)을 도입하여 'Zero Trust(제로 트러스트)' 개념을 무선 구간에 구현함.
③ **현재의 비즈니스 요구**: 원격 근무 및 사물 인터넷(IoT) 디바이스의 폭증으로 인해, 물리적인 배선 없이도 사용자 신원을 기반으로 한 보안 구획(Security Segmentation)이 필수적인 기업 환경으로 변화함.

> **📢 섹션 요약 비유**: 무선 네트워크 보안은 마치 '투명한 유리로 된 집'에 '삼중 잠금 장치(802.1X)'를 설치하고, 방문객을 위한 '안내 데스크(Captive Portal)'를 운영하며, 집 안의 소음이나 온기를 '센서(dBm)'로 정밀하게 모니터링하는 시스템과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 무선 보안 인증의 핵심인 IEEE 802.1X의 아키텍처와 신호 측정의 수학적 원리를 심층 분석한다.

#### 1. 802.1X 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Supplicant (신청자)** | 네트워크 접속을 요청하는 클라이언트 단말 | **EAPoL (EAP over LAN)** 프레임을 생성하여 인증자에게 자격 증명(ID/PW, 인증서) 전송 | 방문객 |
| **Authenticator (인증자)** | 네트워크 입구인 AP(Access Point) 또는 스위치 | 실제 인증 수행은 안 함. 단순히 **EAP** 패킷을 중계(Relay)하고, 포트의 **Controlled Port**를 차단/해제(Open)하는 물리적/논리적 게이트웨이 | 경비원/삼중 현관문 |
| **Authentication Server (인증 서버)** | 자격 증명을 검증하는 백엔드 시스템 | **RADIUS (Remote Authentication Dial-In User Service)** 또는 **DIAMETER** 프로토콜 사용. 사용자 DB 조회 후 Accept/Reject 패킷을 Authenticator로 전송 | 경비실 본부(주민 DB) |

#### 2. 802.1X/EAP 인증 프로세스 및 데이터 흐름

아래는 인증 단말이 무선 네트워크에 연결되는 전체 트랜잭션 과정이다.

```ascii
┌─────────────────────── Phase 1: Physical & Association ───────────────────────┐
│                                                                               │
│  [ Supplicant ]                     [ Authenticator (AP) ]                    │
│       |  (1) Probe Request (Association Request)                             │
│       | -------------------------------------------------------------->       │
│       |  (2) Association Response (Port: Unauthorized, Blocked)              │
│       | <--------------------------------------------------------------       │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────── Phase 2: Authentication (EAP) ─────────────────────────┐
│                                                                               │
│  [ Supplicant ]   <--- EAPoL (L2) --->   [ Authenticator ]  <--- RADIUS (UDP/1812) ---> [ Server ]
│       |                                    |                                     │
│  (3) EAPOL-Start -------------------->     |                                     │
│       |                                    |                                     │
│  (4) EAP-Request/Identity  (Identity)      |                                     │
│       <------------------------------------ |                                     │
│       |                                    |                                     │
│  (5) EAP-Response/Identity (User ID) ----> | (Access-Request w/ User Attrs)     │
│       |                                    | ----------------------------------> │
│       |                                    |                                     │
│  (6) EAP-Request/TLS (Challenge)           |                                     │
│       <------------------------------------ | <--- (Access-Challenge) ----------- │
│       |                                    |                                     │
│  (7) EAP-Response/TLS (Credentials) -----> | (Access-Request w/ Credentials)    │
│       |                                    | ----------------------------------> │
│       |                                    |                                     │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────── Phase 3: Authorization ─────────────────────────────────┐
│                                                                               │
│  [ Supplicant ]                     [ Authenticator ]           [ Server ]     │
│       |                                    |                                     │
│       |                                    | (Validates Credentials)             │
│       |                                    |                                     │
│       |                                    | <--- (Access-Accept + Key) -------- │
│  (8) EAP-Success <---------------------     |                                     │
│       |                                    | (Derives Session Key)               │
│       |  (Port State: UNAUTHORIZED -> AUTHORIZED)                               │
│       |                                    |                                     │
│  (9) Data Traffic (Encrypted) <-------->  |                                     │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**[해설]**
1.  **비인증 상태(Unauthorized)**: AP와 Association은 맺어지지만, Authenticator는 모든 데이터 프레임(802.11 데이터)을 차단한다. 오직 EAPOL(Extensible Authentication Protocol over LAN) 프레임만 통과가 허용된다.
2.  **EAP 중계(Relaying)**: Authenticator는 L2 계층에서 받은 EAPOL 패킷을 캡슐화하여 L3 계층의 RADIUS 서버로 전달한다. 이때 'Called-Station-Id(AP MAC)'와 'Calling-Station-Id(Client MAC)' 속성을 포함하여 추적성을 확보한다.
3.  **포트 해제(Authorization)**: 인증 서버가 **RADIUS Access-Accept**를 보내면, Authenticator는 가상 포트(Virtual Port)를 열고 Supplicant는 LAN 자원에 접근할 수 있다.

#### 3. 신호 강도 측정의 심층 원리 (dBm & Math)

**dBm (Decibel-milliwatts)**은 전력을 로그 스케일로 변환한 단위로, 무선 신호의 감쇠(Attenuation)를 직관적이고 수학적으로 다루기 위해 사용한다.

*   **수식**: $P_{dBm} = 10 \cdot \log_{10}(\frac{P_{mW}}{1mW})$
*   **해석**:
    *   **1mW** = 0 dBm (기준점)
    *   **+3dBm**: 전력이 2배 증가 ($10 \cdot \log_{10}(2) \approx 3.01$)
    *   **+10dBm**: 전력이 10배 증가
    *   **-3dBm**: 전력이 1/2로 감쇠 (반값 전력, Half-power)

**실무 적용 코드 (Python을 이용한 신호 품질 판단)**

```python
import math

def calculate_quality(rssi_dbm):
    """
    RSSI (Received Signal Strength Indicator)를 기반으로
    신호 품질 백분율(%)을 산출하는 함수.
    일반적인 무선 AP 감도 기준: -30dBm(최상) ~ -90dBm(단절)
    """
    # 최적 신호 (예: -30dBm)
    RSSI_MAX = -30
    # 최저 가용 신호 (예: -90dBm, 이하는 노이즈로 간주)
    RSSI_MIN = -90
    
    if rssi_dbm >= RSSI_MAX:
        return 100
    if rssi_dbm <= RSSI_MIN:
        return 0
        
    # 선형 보간법 (Linear Interpolation)
    quality = ((rssi_dbm - RSSI_MIN) / (RSSI_MAX - RSSI_MIN)) * 100
    return round(quality, 2)

# 예시: -67 dBm 수신 시
# print(f"Signal Quality: {calculate_quality(-67)}%") 
# 결과는 약 35% (실무적 컷오프 라인 근처)
```

> **📢 섹션 요약 비유**: **802.1X 인증**은 마치 고속도로 요금소에서 하이패스 단말기(인증서)를 미리 확인하고 통행료를 정산한 뒤, 차단봉이 올라가야만 진입할 수 있는 시스템과 같습니다. **dBm**은 전깃줄을 타고 전달되는 전기의 파워가 얼마나 남아있는지를 '볼트' 단위가 아닌 상대적인 '데시벨'로 표시하여, 줄이 길어질수록 얼마나 약해지는지를 로그 함수로 정확히 계산하는 측정 방법입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

무선 보안 및 인프라 관리 기술들은 서로 배타적이지 않으며, 환경에 따라 상호 보완적이거나 교차적으로 사용된다.

#### 1. 802.1X vs. PSK (Pre-Shared Key) 비교 분석

| 비교 항목 | **802.1X (Enterprise)** | **WPA2-PSK / WPA3-Personal** |
|:---|:---|:---|
| **인증 방식** | **유동적(Dynamic)**: 사용자별/기기별 고유 세션 키 생성 | **고정적(Static)**: 모든 사용자가 동일한 비밀키(암호) 공유 |
| **키 관리** | 중앙 서버(RADIUS)에서 자동 생성/분배/파기 | 라우터 설정 시 수동 입력, 주기적 교체 필요 |
| **보안 사고 발생 시** | 특정 사용자 계정만 폐기하면 됨 (개별 차단 용이) | 비밀키 유출 시 전체 네트워크 키 교체 필수 (대장 참사) |
| **운영 오버헤드** | 초기 구축 비용 및 RADIUS 서버 관리 필요 | 구현이 매우 쉽고 관리 부담이 적음 |
| **적용 환경** | 기업, 대학 병원, 공공기관 (규모 있음) | 가정, 소규모 사무실, 카페 (규모 소) |

#### 2. 신호 강도 지표별 의사결정 매트릭스 (RSSI vs. SNR)

실무에서는 단순히 신호가 강하다고 좋은 것이 아니며, **SNR (Signal-to-Noise Ratio, 신호 대 잡음비)**을 함께 고려해야 한다.

| 구간 | RSSI (dBm) | SNR (dB) | 서비스 품질 (QoS) | 데이터 전송률 (MCS) |
|:---:|:---:|:---:|:---|:---|
| **Excellent** | -30 ~ -50 | > 25 | HD 스트리밍, 대용량 업로드 원활 | MCS 8/9 (최대 속도) |
| **Good** | -50 ~ -60 | 15 ~ 20 | 웹 서핑, 메신저, 4K 동영상 가능 | MCS 5 ~ 7 |
| **Fair** | -60 ~ -70 | 10 ~ 15 | 웹 서핑 가능하나 지연 발생, 간헐적 단절 | MCS 2 ~ 4 |
| **Poor** | < -70 | < 10 | 연결 유지 곤란, 패킷 손실률 급증 | MCS 0/1 혹은 연결 실패 |

**과목 융합 관점 (OS & Physical Layer)**
무선 패킷의 **CRC (Cyclic Redundancy Check)** 오류가 증가하는 원인을 분석할 때, 단순히 OS의 소프트웨어적 버그나 네트워크 프로토콜(TCP/IP 스택) 설정 탓만 하기 쉽다. 그러나 근본적으로 물리 계층(Physical Layer)에서 **SNR이 낮아 비트 오류율(Bit Error Rate)이 높아졌기 때문일 가능성이 크다. 즉, RF(무선 주파수) 환경 개선(AP 위치 이동, 채널 변경)이 OS 상의 네트워크 성능 튜닝보다 선행되어야 하는 경우가 많다.

> **📢 섹션 요약 비유**: **802.1X**는 주민마다 다른 지문 인식 잠금장치(Enterprise)를 설치한 고급 아파트이고, **PSK**는 가족들끼리만 쓰는 집