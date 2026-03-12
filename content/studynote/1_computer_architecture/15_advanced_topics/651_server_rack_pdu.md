+++
title = "651. 서버 랙 PDU (Power Distribution Unit)"
weight = 651
+++

> 1. 서버 랙 PDU(Power Distribution Unit)는 단순한 멀티탭을 넘어 데이터센터의 안정적 전력 분배와 모니터링을 담당하는 핵심 인프라입니다.
> 2. Basic부터 Switched PDU까지 다양한 지능형 기능이 탑재되어, 전원 관리의 자동화와 에너지 효율 극대화를 지원합니다.
> 3. 고밀도 컴퓨팅 환경에서 PDU(Power Distribution Unit)의 실시간 모니터링은 장애 예방 및 물리적 서버 가용성 확보에 직결됩니다.

## Ⅰ. 서버 랙 PDU의 개념 및 아키텍처

서버 랙 PDU(Power Distribution Unit)는 데이터센터 내 서버, 스토리지, 네트워크 장비 등에 전력을 안정적으로 분배하고 관리하는 지능형 전원 분배 장치입니다. PDU(Power Distribution Unit)는 UPS(Uninterruptible Power Supply) 및 CRAC(Computer Room Air Conditioning)와 함께 데이터센터 물리 인프라(DCIM, Data Center Infrastructure Management)의 핵심을 구성합니다. 현대의 데이터센터는 고밀도(High-Density) 서버 구성이 일반화됨에 따라 전원 부하 관리가 필수적이며, 지능형 PDU(Intelligent Power Distribution Unit)를 통해 과부하(Overload) 모니터링, 포트 단위 전원 제어, 환경 센서 연동 등의 기능을 수행합니다.

이러한 PDU(Power Distribution Unit) 시스템은 단상(Single-Phase) 및 3상(Three-Phase) 전원을 수용하며, 장비의 요구 사항에 맞춰 교류(AC, Alternating Current) 전압을 랙 내부 장비로 분배합니다. 입력 전원의 분기를 통해 각 콘센트(Receptacle) 레벨에서 전압, 전류, 피상 전력, 유효 전력을 계측함으로써 에너지 사용 효율성(PUE, Power Usage Effectiveness)을 최적화하는 데 기여합니다.

> 📢 **섹션 요약 비유:** PDU는 복잡한 빌딩(데이터센터)의 각 호실(서버)마다 정확하고 안전하게 수돗물(전력)을 공급하고 계량하는 '지능형 수도 분배기'와 같습니다.

## Ⅱ. PDU 분류 및 동작 메커니즘

서버 랙 PDU(Power Distribution Unit)는 제공하는 관리 기능과 지능화 수준에 따라 여러 가지 등급으로 분류됩니다.

```ascii
[ Main Power Source ] ---> [ UPS (Uninterruptible Power Supply) ]
                                      |
                                      v
                            [ Floor PDU / RPP ]
                                      |
         +----------------------------+----------------------------+
         |                                                         |
[ Basic PDU ]                                         [ Intelligent PDU ]
 - 전원 단순 분배                                        - 네트워크 모니터링 (SNMP/HTTP)
 - 보호 회로(Breaker) 내장                                - 실시간 전력 계측
                                                           |
                                  +------------------------+------------------------+
                                  |                        |                        |
                           [ Metered PDU ]        [ Switched PDU ]     [ Switched Metered-by-Outlet ]
                           (총 전력 모니터링)        (포트별 전원 제어)       (포트별 제어 및 모니터링)
```

1. **Basic PDU (기본형 전원 분배 장치):**
   순수하게 전원 분배 기능만 제공하며, 네트워크 통신 기능이 없습니다. 과전류 보호기(Circuit Breaker)를 통해 장비를 보호하지만 실시간 데이터 수집은 불가능합니다.
2. **Metered PDU (계측형 전원 분배 장치):**
   PDU(Power Distribution Unit) 전체 또는 뱅크(Bank) 단위의 전력 소비량(Ampere, Voltage, Watt)을 로컬 LED 디스플레이 및 네트워크(SNMP, Simple Network Management Protocol)를 통해 원격으로 제공합니다.
3. **Switched PDU (스위치형 전원 분배 장치):**
   Metered PDU(계측형 전원 분배 장치) 기능에 더하여 개별 콘센트의 전원을 원격으로 켜고(On) 끄거나(Off), 재부팅(Reboot)할 수 있는 제어 릴레이(Relay)가 탑재되어 있습니다.
4. **Switched Metered-by-Outlet PDU (개별 제어 및 계측형 전원 분배 장치):**
   가장 진보된 형태로, 개별 포트 단위의 전력 모니터링과 전원 제어가 동시에 가능하여 가장 세밀한 인프라 관리를 지원합니다.

> 📢 **섹션 요약 비유:** Basic PDU가 단순한 '일반 멀티탭'이라면, Switched PDU는 스마트폰 앱으로 콘센트마다 전기를 끊거나 켜고, 전기 요금까지 확인하는 'IoT 스마트 멀티탭'입니다.

## Ⅲ. PDU의 핵심 기술 및 프로토콜

PDU(Power Distribution Unit)는 안정성과 관리 효율성을 위해 다양한 통신 프로토콜과 센서 기술을 활용합니다.

1. **네트워크 관리 기술:**
   대부분의 지능형 PDU는 관리 모듈(Network Management Card, NMC)을 내장하고 있으며, SNMP(Simple Network Management Protocol)를 이용하여 NMS(Network Management System) 또는 DCIM(Data Center Infrastructure Management) 소프트웨어와 연동됩니다. 또한 HTTP/HTTPS 웹 인터페이스, SSH(Secure Shell)를 통한 CLI(Command Line Interface), API(Application Programming Interface) 연동(RESTful API)을 지원합니다.
2. **환경 모니터링 센서 연동:**
   PDU(Power Distribution Unit)는 자체 온도(Temperature) 및 습도(Humidity) 센서 포트를 제공하여 랙 내부의 미시적 환경 변화를 실시간 감지합니다. 연기(Smoke), 누수(Water leak), 도어 열림(Door open) 센서와 결합하여 물리적 보안을 강화합니다.
3. **Daisy Chaining (데이지 체인 연결):**
   다수의 PDU(Power Distribution Unit)를 하나의 IP(Internet Protocol) 주소로 묶어 관리할 수 있도록 스위치 포트를 내장하여 네트워크 케이블링의 복잡성을 줄이고 관리 효율성을 높입니다.

> 📢 **섹션 요약 비유:** PDU의 통신 기능은 전력 공급기가 스스로 관제 센터와 무전기로 대화하며 "지금 3번 서버 전기가 끊겼습니다!"라고 보고하는 '스마트 보고 시스템'입니다.

## Ⅳ. 고가용성(HA) 환경에서의 전원 이중화 구성

데이터센터에서 단일 장애점(SPOF, Single Point of Failure)을 제거하기 위해 PDU(Power Distribution Unit) 레벨에서도 전원 이중화가 필수적으로 적용됩니다.

1. **A/B Power Feed 구성:**
   서버는 일반적으로 이중화된 전원 공급 장치(Dual PSU, Power Supply Unit)를 가집니다. 이를 활용하기 위해 랙 내부에는 서로 다른 전력원(A 전원 라인, B 전원 라인)에 연결된 두 개의 독립된 PDU(Power Distribution Unit)를 배치합니다. 한 라인의 상위 배전반이나 PDU 장애 시에도 다른 PDU가 무중단으로 전력을 공급합니다.
2. **ATS (Automatic Transfer Switch) PDU:**
   단일 PSU(Power Supply Unit)만을 가진 구형 장비나 저가형 스위치를 위해 사용됩니다. 두 개의 입력 전원 중 Primary(주 전원)에 문제가 생기면 밀리초(ms) 단위로 Secondary(보조 전원)로 자동 절체(Failover)되어 연결된 장비의 전원 꺼짐을 방지합니다.

> 📢 **섹션 요약 비유:** 전원 이중화는 비행기의 엔진 2개처럼, 한쪽 엔진(PDU A)이 고장나더라도 다른 엔진(PDU B)으로 목적지까지 무사히 날아갈 수 있게 해주는 '보험 장치'입니다.

## Ⅴ. 기술 도입 시 고려사항 및 최신 트렌드

PDU(Power Distribution Unit) 시스템 도입 시에는 데이터센터의 규모, 부하량, 그리고 관리 요구사항을 종합적으로 평가해야 합니다. 최근 AI(Artificial Intelligence) 및 HPC(High-Performance Computing) 환경의 등장으로 랙당 전력 밀도가 급격히 상승함에 따라 고용량 PDU의 수요가 증가하고 있습니다.

* **온도 내구성 (High Temperature Rating):** 고집적 랙 환경에서는 열 발생이 심하므로, 최대 60도 이상의 고온에서도 안정적으로 동작할 수 있는 산업용 등급의 PDU가 요구됩니다.
* **보안 기능 강화:** 제어권이 탈취될 경우 대규모 서비스 장애를 유발할 수 있으므로, SNMPv3, RADIUS/TACACS+ 인증, TLS(Transport Layer Security) 암호화 등의 엔터프라이즈 보안 기능 지원 여부가 중요합니다.
* **컬러 코딩 (Color Coding):** 시각적 직관성을 위해 A/B 라인을 색상(예: 빨간색, 파란색)으로 구분하여 휴먼 에러를 방지하는 디자인이 선호됩니다.

> 📢 **섹션 요약 비유:** 최신 PDU를 고르는 것은 단순히 튼튼한 멀티탭을 사는 것을 넘어, 한여름 찜통 같은 차 안에서도 터지지 않고 해킹까지 막아내는 '초정밀 산업용 로봇'을 고르는 것과 같습니다.

---

### 💡 Knowledge Graph & Child Analogy

```mermaid
graph TD
    A[PDU (Power Distribution Unit)] --> B(Basic PDU)
    A --> C(Intelligent PDU)
    C --> D(Metered PDU: 계측 기능)
    C --> E(Switched PDU: 제어 기능)
    C --> F(Network Interface)
    F --> G[SNMP / HTTPS]
    A --> H(이중화 구성)
    H --> I[A/B Feed Architecture]
    H --> J[ATS PDU]
```

**👧 어린이를 위한 비유 (Child Analogy):**
PDU는 집에서 쓰는 '엄청 똑똑한 멀티탭'이에요! 그냥 전기만 나눠주는 게 아니라, 스마트폰 앱으로 "게임기 콘센트는 끄고, TV 콘센트는 켜 줘!"라고 명령할 수 있어요. 또 "지금 컴퓨터가 전기를 얼마나 먹고 있지?"하고 물어보면 숫자로 딱 알려주기도 한단다.
