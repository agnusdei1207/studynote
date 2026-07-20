---
title: "Orthogonality"
date: "2026-03-30"
tags:
  - "network"
  - "studynote-network"
weight: 83
---
## 핵심 인사이트 (3줄 요약)
- **본질**: 직교성 (Orthogonality)은 두 신호·코드·공간 벡터의 내적이 0이 되는 성질로, 서로 겹쳐도 수학적으로 분리되는 기초다.
- **가치**: 가드밴드 (Guard Band) 낭비를 줄여 OFDM (Orthogonal Frequency Division Multiplexing), CDMA (Code Division Multiple Access), MIMO (Multiple-Input Multiple-Output)를 가능하게 한다.
- **판단 포인트**: 직교성은 이상적인 상태가 아니라 동기화·전력·채널 추정 조건이 유지될 때만 성립하므로, ICI (Inter-Carrier Interference)와 near-far 문제를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

통신의 첫 질문은 늘 같다. "어떻게 하면 같은 공간에 더 많은 데이터를 간섭 없이 넣을 수 있는가?" FDM (Frequency Division Multiplexing) 시절에는 신호가 서로 부딪히지 않도록 넉넉한 가드밴드를 비워 두었다. 하지만 이 방식은 제한된 대역폭을 그냥 버리는 셈이라 효율이 낮았다.

공학자들은 발상을 바꿨다. 물리적으로 떼어 놓는 대신, 수학적으로 0이 되게 만들면 되지 않느냐는 것이다. 이 생각이 바로 직교성이다. 신호가 겹쳐 보여도 내적이 0이면 서로 분리 가능하다는 점이 핵심이며, 이 원리가 OFDM (Orthogonal Frequency Division Multiplexing)의 뼈대가 되었다.

```text
+--------------------------------------------------------------+
| 비직교: 신호 사이를 비워 둠 -> 대역 낭비                      |
| 직교: 신호를 겹쳐 보냄 -> 수신단에서 수학으로 분리            |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 같은 길에 차를 띄워 세우는 대신, 신호등의 약속을 맞춰 동시에 지나가게 하는 교통 정리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

직교성의 수학적 조건은 간단하다. 두 함수의 내적이 0이면 된다.

`∫_0^T f_m(t) f_n(t) dt = 0 (m ≠ n)`

이 조건은 주파수, 코드, 시간, 공간으로 확장된다. OFDM은 부반송파를 주파수 축에서 직교시키고, CDMA (Code Division Multiple Access)는 코드 벡터를 직교시키며, MIMO (Multiple-Input Multiple-Output)는 안테나 채널의 공간 상관을 낮춰 분리한다.

| 직교 축 | 매개체 | 대표 기술 | 0이 되는 조건 |
| :--- | :--- | :--- | :--- |
| 주파수 | 부반송파 | OFDM | 심볼 구간 적분이 0 |
| 코드 | Walsh code / PN (Pseudo-Noise) code | CDMA | 내적이 0 |
| 시간 | 슬롯 | TDM (Time Division Multiplexing) | 겹치지 않음 |
| 공간 | 채널 벡터 | MIMO | 채널 상관이 낮음 |

OFDM은 IFFT (Inverse Fast Fourier Transform)로 직교 부반송파를 합성하고, 수신단에서 FFT (Fast Fourier Transform)로 각 성분을 분리한다. CP (Cyclic Prefix)는 다중경로로 인한 심볼 경계 깨짐을 흡수해 직교성이 무너지지 않게 도와준다.

```text
+--------------------------------------------------------------+
| IFFT -> 겹쳐 보냄 -> 채널 -> CP로 보호 -> FFT -> 부반송파 분리    |
+--------------------------------------------------------------+
```

직교성은 "겹치게 보내되, 읽을 때는 분리되게 하는" 구조다. 따라서 송신단의 설계보다 수신단의 수학적 복원 능력이 더 중요하다.

- **📢 섹션 요약 비유**: 악보는 서로 겹쳐 보이지만, 지휘자가 박자를 맞추면 각 악기가 자기 파트를 정확히 연주하는 합주와 같다.

---

## Ⅲ. 비교 및 연결

직교성을 이해하려면 FDM과 OFDM, CDMA와 MIMO의 경계를 봐야 한다. FDM은 안전하지만 가드밴드가 필요하고, OFDM은 효율적이지만 동기화에 민감하다. CDMA는 코드로 사용자를 나누고, MIMO는 공간으로 분리한다.

| 항목 | FDM | OFDM | CDMA | MIMO |
| :--- | :--- | :--- | :--- | :--- |
| 분리 축 | 주파수 간격 | 직교 부반송파 | 직교 코드 | 공간 벡터 |
| 장점 | 단순, 이해 쉬움 | 스펙트럼 효율 높음 | 다수 사용자 수용 | 용량 증대 |
| 약점 | 가드밴드 낭비 | 동기화 민감 | 전력 제어 필요 | 채널 추정 복잡 |

가드밴드 (Guard Band)와 CP (Cyclic Prefix)는 비슷해 보이지만 역할이 다르다. 가드밴드는 주파수 영역의 빈 공간이고, CP는 시간 영역의 보호막이다. 전자는 간섭을 막기 위해 대역을 비우는 방식이고, 후자는 다중경로가 직교성을 깨지 못하게 앞에 복사본을 붙이는 방식이다.

LTE (Long Term Evolution)와 5G NR (New Radio)은 이 직교성을 실전으로 끌어낸 대표 사례다. 다운링크는 OFDMA (Orthogonal Frequency Division Multiple Access)를 쓰고, 업링크는 SC-FDMA (Single Carrier Frequency Division Multiple Access)를 사용해 송신기 부담을 줄인다.

- **📢 섹션 요약 비유**: 빈 좌석을 많이 두는 극장형(FDM)과, 좌석은 붙어 있어도 좌표표를 정확히 주는 스마트 좌석형(OFDM)의 차이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서 직교성 붕괴는 주파수 오차, 도플러 효과, 전력 불균형, 채널 추정 실패로 나타난다. 고속 이동 환경에서는 OFDM의 부반송파 간격이 너무 좁으면 ICI (Inter-Carrier Interference)가 폭발한다. 이때는 5G NR의 더 넓은 subcarrier spacing을 쓰거나, 동기화 품질을 개선해야 한다.

또 다른 문제는 CFO (Carrier Frequency Offset)다. 송신기와 수신기의 발진기가 조금만 어긋나도 샘플링 시점이 비틀어져 직교 샘플이 깨진다. CDMA 계열에서는 Near-Far Problem이 대표적이며, 전력 제어가 늦으면 강한 사용자가 약한 사용자를 덮어버린다. 필요하면 PLL (Phase-Locked Loop) 같은 동기화 회로를 강화해야 한다.

체크리스트는 다음과 같다.
1. 이동성이 큰 환경인가?
2. CP 길이가 delay spread보다 충분히 긴가?
3. 전력 제어가 안정적인가?
4. 안테나 간 채널 상관이 낮은가?

- **📢 섹션 요약 비유**: 발걸음이 조금만 어긋나도 줄넘기 줄이 엉키듯, 직교성은 박자와 간격을 끝까지 지켜야 한다.

---

## Ⅴ. 기대효과 및 결론

직교성은 제한된 자원에서 동시 사용자 수와 전송 효율을 끌어올리는 가장 강력한 수학적 도구다. 덕분에 OFDM, CDMA, MIMO가 각각 다른 방식으로 같은 공기를 더 잘 쓸 수 있게 되었다. 하지만 직교성은 완벽한 조건이 아닐 때 쉽게 무너진다.

그래서 결론은 분명하다. 직교성은 "간섭이 없는 상태"가 아니라 "간섭을 0으로 만들 수 있는 조건"이다. 앞으로도 5G/6G, Massive MIMO, beamforming에서 이 원리는 더 정교하게 쓰일 것이다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 내적 | 직교성을 판정하는 수학적 기준 |
| OFDM (Orthogonal Frequency Division Multiplexing) | 주파수 직교를 실전화한 방식 |
| CDMA (Code Division Multiple Access) | 코드 직교를 이용한 다중 접속 |
| CP (Cyclic Prefix) | 다중경로로부터 직교성을 보호 |
| ICI (Inter-Carrier Interference) | 직교성 붕괴의 대표 증상 |
| MIMO (Multiple-Input Multiple-Output) | 공간 직교를 활용한 용량 확장 |

### 📈 관련 키워드 및 발전 흐름도

```text
FDM
    |
    v
OFDM / CDMA
    |
    v
OFDMA / SC-FDMA
    |
    v
LTE (Long Term Evolution) / 5G NR (New Radio)
    |
    v
Massive MIMO / Beamforming
```

### 👶 어린이를 위한 3줄 비유 설명

1. 직교성은 여러 사람이 같은 방에 있어도 서로 말이 섞이지 않게 하는 약속이에요.
2. 각자 다른 박자, 다른 비밀번호, 다른 방향을 쓰면 서로를 방해하지 않아요.
3. 그래서 통신은 같은 공간을 더 똑똑하게 나눠 쓸 수 있답니다.
