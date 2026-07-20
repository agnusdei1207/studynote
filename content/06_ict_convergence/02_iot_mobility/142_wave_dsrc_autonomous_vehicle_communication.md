---
title: "Wave Dsrc Autonomous Vehicle Communication"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
weight: 142
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WAVE(Wireless Access in Vehicular Environments)/DSRC(Dedicated Short-Range Communications)는 <strong>5.9GHz 전용 주파수에서 차량 간 직접 통신(V2V·V2I)</strong>을 제공하는 IEEE 802.11p 기반 규격이다.
> 2. **가치**: 셀룰러(4G/5G)는 기지국 경유로 <strong>수십ms 지연</strong>이 있지만, DSRC는 <strong>직접 통신으로 수ms 이내 저지연</strong>을 제공하여 긴급 제동 경고 등 안전 메시지에 적합하다.
> 3. **판단 포인트**: FCC가 5.9GHz 대역 일부를 Wi-Fi에 재배정(2020)하면서 DSRC의 미래가 불투명해졌고, <strong>C-V2X(5G NR)가 주류로 전환</strong> 중이다.

---

## Ⅰ. 개요 및 필요성

```text
DSRC: 5.9GHz 전용 대역, 802.11p
  통신 범위: ~300m (직접)
  지연: <10ms (안전 메시지)
  vs C-V2X: 5G NR, 기지국+직접, 대역 효율^
```

- **📢 섹션 요약 비유**: DSRC는 <strong>워키토키(직접 통신)</strong>, C-V2X는 <strong>스마트폰(기지국+직접)</strong>이다.

---

## Ⅱ~Ⅴ. 결론

DSRC는 <strong>V2X 통신의 초기 표준</strong>이지만, C-V2X(5G NR)로 주류 전환이 진행 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DSRC</strong> | 802.11p 전용 통신 |
| <strong>WAVE</strong> | 차량 무선 접근 |
| <strong>C-V2X</strong> | 셀룰러 기반 대안 |
| **5.9GHz** | 전용 주파수 |
| **저지연** | 안전 메시지 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DSRC 802.11p (2010)] -> [WAVE 표준 (IEEE 1609)]
    -> [FCC 5.9GHz 재배정 (2020)]
    -> [C-V2X 부상 (2020~)]
    -> [현재: C-V2X 주류 — DSRC 축소]
```

### 👶 어린이를 위한 3줄 비유 설명
1. DSRC는 <strong>워키토키</strong>예요. 가까운 차끼리 <strong>직접 대화</strong>해요.
2. 스마트폰(C-V2X)처럼 **기지국 없이도** 바로 통신해요.
3. 하지만 요즘은 <strong>스마트폰 방식(C-V2X)</strong>이 더 인기가 많아요!
