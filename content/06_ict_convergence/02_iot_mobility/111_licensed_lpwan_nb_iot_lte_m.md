---
title: "Licensed Lpwan Nb Iot Lte M"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 면허 대역 LPWAN은 통신사가 보유한 <strong>LTE 면허 주파수 대역</strong>을 활용하여 NB-IoT(200kHz 협대역)와 LTE-M(1.4MHz 광대역)으로 IoT 디바이스에 <strong>통신사급 QoS(품질 보장)</strong>를 제공하는 3GPP 국제 표준 기술이다.
> 2. **가치**: 비면허 LPWAN(LoRa·Sigfox)이 Best Effort인 반면, 면허 대역은 통신사 기지국 인프라를 그대로 활용하여 <strong>SLA 보장·이동성(Handover)·양방향 통신</strong>이 가능하며 별도 GW 구축이 불필요하다.
> 3. **판단 포인트**: NB-IoT는 **고정형·초저전력·초소량**(스마트 미터), LTE-M은 **이동형·음성·중속도**(자산 추적·웨어러블)에 적합하며, 5G Release 17 RedCap으로 통합 진화 중이다.

---

## Ⅰ. 개요 및 필요성

비면허 LPWAN(LoRa)은 자체 GW를 깔아야 하고 QoS 보장이 없다. 통신사 입장에서는 이미 전국에 깔아놓은 LTE 기지국의 빈 대역폭(Guard Band)을 재활용하여 IoT 시장을 공략할 수 있으며, 기업 고객에게 SLA를 보장할 수 있다.

```text
+-------------------------------------------------------+
|     NB-IoT vs LTE-M 포지셔닝 맵                       |
+-------------------------------------------------------+
|  속도 ^                                               |
|  1Mbps |               ★ LTE-M                       |
| 200kbps|        ☆ NB-IoT                              |
|  600bps|  ◇ Sigfox                                    |
|  50kbps|     ◆ LoRa                                   |
|        +-----------------------------> 이동성           |
|        고정               Handover 지원               |
|                                                       |
|  QoS: ◇◆ Best Effort   ☆★ 통신사 SLA 보장           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: NB-IoT는 편의점 택배(고정 배달, 저렴), LTE-M은 퀵서비스(이동 배달, 빠름). 둘 다 택배회사(통신사) 인프라를 사용한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | NB-IoT | LTE-M (Cat-M1) |
|:---|:---|:---|
| <strong>3GPP Release</strong> | Rel-13 (2016) | Rel-13 (2016) |
| <strong>대역폭</strong> | 200 kHz (협대역) | 1.4 MHz |
| **최대 속도** | DL 200 kbps | DL 1 Mbps |
| **이동성** | 제한적 (Handover 미지원) | **완전 지원** |
| **음성** | 미지원 | <strong>VoLTE 지원</strong> |
| **전력 절감** | PSM + eDRX | PSM + eDRX |
| **커버리지 확장** | MCL 164 dB (지하 침투) | MCL 156 dB |
| **적합 용도** | 고정 센서, 스마트 미터 | 이동 추적, 웨어러블 |

### 전력 절감 메커니즘
- <strong>PSM (Power Saving Mode)</strong>: 통신 완료 후 모듈을 완전히 꺼서 수 μA 수준으로 대기.
- **eDRX (extended DRX)**: 수신 대기 주기를 수초->수십 분으로 확장하여 전력 절감.

- **📢 섹션 요약 비유**: PSM은 직원이 퇴근 후 건물 전기를 전부 끄는 것이고, eDRX는 "1시간에 한 번만 우편함을 확인"하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | LoRa (비면허) | NB-IoT (면허) | LTE-M (면허) |
|:---|:---|:---|:---|
| **인프라** | 자체 GW | 통신사 기지국 | 통신사 기지국 |
| <strong>QoS</strong> | Best Effort | <strong>SLA 보장</strong> | <strong>SLA 보장</strong> |
| **이동성** | 제한 | 제한 | <strong>Handover</strong> |
| **비용** | GW 자체 구축 | 월정액 | 월정액 |
| **음성** | 불가 | 불가 | <strong>VoLTE</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 선택 기준
1. **고정 설치 + 초소량**: 수도·전기 계량기 -> NB-IoT.
2. **이동 + 음성**: 독거 노인 긴급 호출 웨어러블 -> LTE-M.
3. <strong>SLA 필수</strong>: 의료·산업 IoT -> 면허 대역 (NB-IoT/LTE-M).

### 5G RedCap (Release 17)
NB-IoT와 LTE-M을 하나의 5G 프레임워크로 통합하는 경량 5G NR 규격. 기존 LPWAN의 후계자로 5G 시대의 IoT 표준이 될 전망.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 비면허 LPWAN | 면허 LPWAN | 개선 |
|:---|:---|:---|:---|
| QoS | Best Effort | <strong>SLA 보장</strong> | 신뢰성 확보 |
| 인프라 구축 | 자체 GW 필요 | **통신사 전국망** | 즉시 사용 |
| 이동성 | 제한 | <strong>Handover (LTE-M)</strong> | 이동 IoT 가능 |

NB-IoT와 LTE-M은 5G RedCap으로 수렴하며, 위성 NTN(Non-Terrestrial Network)과 결합하여 전지구 IoT 커버리지를 향해 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>NB-IoT</strong> | 200kHz 협대역 면허 LPWAN, 고정 센서 |
| <strong>LTE-M (Cat-M1)</strong> | 1.4MHz 면허 LPWAN, 이동+음성 |
| **PSM / eDRX** | 면허 LPWAN의 극저전력 메커니즘 |
| <strong>5G RedCap (Rel-17)</strong> | NB-IoT·LTE-M의 5G 통합 후계자 |
| **LoRaWAN** | 비면허 대역 경쟁 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[2G/3G M2M (2000s) — 고전력·고비용 원격 IoT]
    |
    v
[3GPP Rel-13 (2016) — NB-IoT·LTE-M 표준화]
    |
    v
[전국망 상용화 (2018~) — 통신 3사 NB-IoT 서비스 개시]
    |
    v
[5G RedCap (Rel-17, 2022~) — 경량 5G NR로 통합]
    |
    v
[현재: 5G NTN (위성) + RedCap — 전지구 IoT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. NB-IoT는 집에 고정된 <strong>수도 계량기</strong>가 매달 숫자를 보내는 통신이에요.
2. LTE-M은 할머니 팔찌(웨어러블)가 **움직이면서도** 위치와 건강 정보를 보내는 통신이에요.
3. 둘 다 전화회사(통신사)가 관리하니까 <strong>안정적</strong>이고, 전기(배터리)를 아주 적게 써요!
