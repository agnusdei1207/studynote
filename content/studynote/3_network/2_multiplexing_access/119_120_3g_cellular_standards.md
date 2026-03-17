+++
title = "119-120. 3G 이동통신 기술의 양대 산맥 (CDMA2000 vs W-CDMA)"
date = "2026-03-14"
[extra]
category = "Mobile Communication"
id = 119
+++

# 119-120. 3G 이동통신 기술의 양대 산맥 (CDMA2000 vs W-CDMA)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**= 2G의 음성 위주 통신을 넘어 데이터 통신을 본격화한 3G는, **CDMA (Code Division Multiple Access)** 기술을 기반으로 **동기식(Synchronous)** 방식의 CDMA2000과 **비동기식(Asynchronous)** 방식의 W-CDMA로 양분되어 표준 경쟁을 벌였다.
> 2. **가치**= 동기식은 주파수 효율과 구현 용이성에, 비동기식은 망 구성의 유연성과 광대역 처리에 강점을 발휘했으며, 이 경쟁은 모바일 인터넷 생태계를 급격하게 확장하는 계기가 되었다.
> 3. **융합**= 두 진영의 기술적 경쟁은 다양한 무선 접속 기술(RAT)의 공존을 이끌었고, 결국 **LTE (Long Term Evolution)** 및 4G 시대로 넘어가는 기술적 토대(OFDMA, MIMO 등의 필요성)를 마련했다.

+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
3세대 이동통신(3G, 3rd Generation Mobile Telecommunications)은 IMT-2000(International Mobile Telecommunications-2000) 규격을 충족하여 음성 및 영상 통화는 물론, 고속 패킷 데이터 통신을 제공하는 시스템을 의미합니다. 2G(2nd Generation) 시스템이 음성 호출(Voice Call)과 저속 문자 메시지(SMS)에 집중했다면, 3G는 웹 브라우징, 동영상 스트리밍 등 '모바일 인터넷' 시대를 개척했습니다. 핵심적인 차이점은 무선 접속 방식(RAT: Radio Access Technology)으로, 기존의 시분할(TDMA)이나 주파수 분할(FDMA) 방식에서 벗어나 모든 사용자가 동일한 주파수 대역을 사용하면서 직교 코드(Orthogonal Code)로 신호를 분리하는 **CDMA (Code Division Multiple Access)** 기술을 본격적으로 상용화했습니다.

이 과정에서 크게 두 가지 갈래가 생겨났습니다. 북미 중심의 퀄컴(Qualcomm) 기술인 **CDMA2000**과 유럽 GSM 진영 중심의 **W-CDMA (Wideband CDMA)**입니다. 두 기술의 가장 결정적인 차이는 '기지국 간 시간 동기화(Synchronization)' 방식에 있습니다.

**등장 배경**
1.  **한계**: 2G 시스템(IS-95, GSM)은 64 Kbps 미만의 속도로는 웹 서비스를 제공하기에 대역폭이 너무 좁았고, 회선 교환 방식의 낮은 자원 효율성이 문제였습니다.
2.  **혁신**: 패킷 교환(Packet Switching) 기반의 데이터 망을 도입하여 효율을 높이고, 스펙트럼 확산(Spread Spectrum) 기술을 적용하여 주파수 활용도를 극대화하고자 했습니다.
3.  **비즈니스**: 통신사는 단순 음성 요금 감소에 따른 데이터 매출 원천을 확보해야 했으며, 제조사는 글로벌 로밍(Roaming) 표준을 선점하기 위해 치열한 경쟁을 벌였습니다.

**💡 비유**
2G가 단일 차선 도로에서 신호등에 맞춰 한 대씩 지나가는 것이라면, 3G는 여러 차선이 뒤섞여 있어도 자신만의 비밀 코드(번호판)를 인식하여 빠르게 지나가는 고속도로 시스템과 같습니다.

**📢 섹션 요약 비유**
마치 기차에서 정확한 시간을 맞추는 '철도 시스템(동기식)'과, 각자가 알아서 속도와 박자를 조절하는 '자동차 고속도로(비동기식)' 중 하나를 선택하여 전 세계 교통망을 구축하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

3G 무선 접속망(RAN)의 핵심은 주파수 대역을 얼마나 효율적으로 사용하며, 단말기(UE)와 기지국(NodeB) 간의 무선 인터페이스를 어떻게 제어하는가에 있습니다.

**구성 요소 상세 비교**

| 구성 요소 (Component) | CDMA2000 / EV-DO (동기식) | W-CDMA / HSPA (비동기식) | 비고 |
|:---|:---|:---|:---|
| **동기화 방식** | **Synchronous (GPS 필수)** | **Asynchronous (GPS 비필수)** | 가장 큰 차이점 |
| **채널 대역폭** | 1.25 MHz (Narrowband) | 5 MHz (Wideband) | W-CDMA가 데이터 처리에 유리 |
| **칩 레이트 (Chip Rate)** | 1.2288 Mcps | 3.84 Mcps | 확산 대역폭에 비례하여 데이터 전송률 증가 |
| **기지국 간 신호** | GPS 수신기로 시간 동기화 필요 | 기지국 간 상대적인 시간 오프셋 탐색 | 망 설계 자유도 차이 |
| **코딩 방식** | Walsh Code + PN Code | OVSF (Orthogonal Variable Spreading Factor) | |

**ASCII 구조 다이어그램: 무선 구조 및 동기화 방식 비교**

아래 다이어그램은 두 방식이 기지국 간 시간을 맞추는 메커니즘과 주파수 할당 구조를 도식화한 것입니다.

```ascii
[CDMA2000: 동기식 시스템 구조]          [W-CDMA: 비동기식 시스템 구조]
(GPS 위성에 의존적인 절대적 시간)        (네트워크 내 상대적 타이밍)

   GPS Satellite (공통 시간 원천)
        |   ^   (Time Sync)
        v   |                           +-------+-------+
   +----------+                         |   BS A (2s)   | (기지국 간 시간차 존재)
   |  BTS 1   |                         +-------+-------+
   | 0.00 sec |  ----(RF 1.25MHz)---->       |
   +----------+                            |  <--(Time Offset Search)--|
        ^                                +-------+-------+
        |                                |   BS B (5s)   |
   +----------+                         +-------+-------+
   |  BTS 2   |
   | 0.00 sec |  ----(RF 1.25MHz)---->
   +----------+

   [핵심]: 모든 BTS가 동일한 '절대 시각(T0)' 기준으로
           송신하므로 코드 동기가 빠름.         [핵심]: 단말기(UE)가 BS별로 타이밍 오프셋을
           단, GPS 수신 불가 시 망 붕괴.         찾아내어 동기. 망 설치 유연함.
```

**다이어그램 해설**
왼쪽의 **CDMA2000** 구조는 모든 기지국(BTS)이 상단에 도시된 GPS 위성 신호에 의존하여 마이크로초 단위의 시간 오차도 없이 동일한 시간에 전송을 시작합니다. 이로 인해 단말기는 이동 중 빠르게 기지국을 변경(Handover)할 때 유리합니다. 반면, 오른쪽의 **W-CDMA** 구조는 기지국 간에 절대적 시간 동기가 필요 없습니다. 기지국끼리 서로 다른 시작 시간을 가지더라도, 단말기(UE)가 전원을 켤 때 기지국별 시간차(Offset)를 스스로 검색하여 동기 채널을 잡습니다. 이는 터널이나 지하와 같이 GPS 신호가 닿지 않는 곳에 기지국을 설치하는 데 있어 막대한 설치 자유도를 제공합니다.

**심층 동작 원리 및 코드**
**CDMA (Code Division Multiple Access)**의 핵심은 스펙트럼 확산(Spread Spectrum) 기술입니다. 데이터($d(t)$)를 대역폭보다 훨씬 높은 속도의 PN(Pseudo-Noise) 코드($c(t)$)와 곱하여($d(t) \times c(t)$) 넓은 주파수 대역에 퍼뜨려 전송합니다.

*   **CDMA2000**: 주파수 효율을 위해 1.25 MHz 대역을 사용하며, 64개의 **Walsh Code**를 사용하여 채널을 분리합니다. 동기식이므로 코드 간 간섭을 최소화합니다.
*   **W-CDMA**: 5 MHz 광대역을 사용하여 다중 경로 페이딩(Multipath Fading)에 강한 **Rake Receiver** 성능을 극대화합니다. 가변 길이 직교 코드(**OVSF**)를 사용하여 데이터 속도에 따라 코드 길이(Spreading Factor)를 가변적으로 조정하여 비트 전송률을 제어합니다.

```c
// [CDMA 데이터 전송 프로세스 의사 코드]
// CDMA2000과 W-CDMA의 기본적인 확산 과정 (Spreading Process)

void cdma_transmit(Data data, Code code, Power power) {
    // 1. 채널 코딩 (Channel Coding): Error Correction (Convolutional Coding, Turbo Coding)
    EncodedData encoded = conv_encode(data);

    // 2. 인터리빙 (Interleaving): Burst Error 방지를 위한 순서 섞기
    InterleavedData interleave = interleave(encoded);

    // 3. 스펙트럼 확산 (Spreading): 좁은 대역의 데이터를 넓은 대역으로 퍼뜨림
    // WCDMA: OVSF Code 사용 (SF=4~512)
    // CDMA2000: Walsh Code + Long PN Code
    SpreadSignal spread = multiply(interleave, code);

    // 4. 주파수 업컨버전 및 전송 (RF Upconversion)
    rf_transmit(spread, CARRIER_FREQ, power);
}
```

**📢 섹션 요약 비유**
CDMA2000이 **군대 절호(단일 지휘관(GPS)의 절대 명령에 따라 정확히 움직이는 행진)**이라면, W-CDMA는 **재즈 밴드(각 멤버가 서로의 리듬을 바라보며 유기적으로 맞추는 합주)**와 같습니다. 행진은 단순하고 빠르지만, 밴드는 구성원이 어디에 있든 유연하게 연주할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교**
두 방식은 단순히 대역폭의 차이를 넘어 네트워크 설계 철학이 다릅니다.

| 비교 항목 | CDMA2000 / EV-DO | W-CDMA / UMTS (HSPA) |
|:---|:---|:---|
| **시스템 구성** | 데이터 전용 채널과 음성 채널 분리 가능 (EV-DO) | 초기에는 음성/데이터 병행, 후에 HSPA로 발전 |
| **스케줄링** | 시간 스케줄링 기반의 TDM 방식 우세 (Rev.A) | 코드 및 주파수 자원 분배 방식 |
| **핸드오버** | 소프트 핸드오버(Soft Handoff)에 매우 유리 | 소프트 핸드오버 지원하나 복잡도 높음 |
| **주파수 유연성** | 협대역으로 주파수 할당이 쉬움 (점진적 확장) | 광대역 5MHz 단위 할당 필요 (계획 필요) |
| **칩셉 의존도** | 퀄컴(Qualcomm) IP 특허 영향력 절대적 | 3GPP 표준 기반으로 다수 칩셋 제조사 경쟁 |

**과목 융합 관점 (Data Communication & OS)**
1.  **네트워크 계층(OSI 3 Layer)과의 시너지**: 3G 데이터 서비스는 단말기 내부에서 **PPP (Point-to-Point Protocol)** encapsulation을 통해 IP 패킷을 전송합니다. W-CDMA(HSPA) 방식은 네트워크 측에서 **RAN (Radio Access Network)**과 **CN (Core Network)** 간의 인터페이스(Iu 등)가 ATM(Asynchronous Transfer Mode) 기반이었다가 IP로 전환됨에 따라, 모바일 IP(Mobile IP) 기술이 필수적으로 요구되었습니다.
2.  **OS 및 프로토서스**: 단말기 입장에서 RIL(Radio Interface Layer)과 Modem 간의 통신 프로토콜 스택이 CDMA2000(1xEV-DO)과 W-CDMA(HSDPA)마다 다르게 설계되어야 하므로, 초기 스마트폰 OS(Windows Mobile, Symbian 등) 개발 시 드라이버 호환성이 큰 과제였습니다.

**정량적 지표에 의한 판단**
*   **초기 속도**: CDMA2000 1x는 153Kbps로 시작했으나, EV-DO Rev.A는 3.1Mbps를 달성하여 당시 W-CDMA(R99)의 384Kbps보다 앞서 있었습니다.
*   **진화 속도**: 하지만 W-CDMA 진영은 HSDPA를 도입하여 14.4Mbps 이상을 구현함으로써 기술적 격차를 역전시켰습니다.

**📢 섹션 요약 비유**
CDMA2000이 **자동 변속기(미리 정해진 기어비를 순차적으로 변환, EV-DO로 확장 용이)**라면, W-CDMA는 **무단 변속기(CVT, 끊김 없는 부드러운 변속과 5MHz 광대역 활용)**와 같습니다. 초기에는 자동 변속기가 안정적이었으나, 고속 주행이 필요해지자 광대역을 활용한 무단 변속기의 성능이 돋보이게 되었습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**
통신사(ISP) 입장에서 두 진영 중 하나를 선택하는 것은 막대한 CAPEX(자본적 지출) 투자가 동반되는 문제입니다.

1.  **망 확장성 (Scalability)**: CDMA2000은 1.25MHz 단위로 채널을 추가할 수 있어 주파수 자원이 조금씩 남는 상황에서 유리했습니다. 반면 W-CDMA는 5MHz 블록이 필요하지만, 한 번 구축 시 처리 가능한 용량이 훨씬 컸습니다.
2.  **해외 로밍 (Global Roaming)**: W-CDMA(UMTS)는 유�