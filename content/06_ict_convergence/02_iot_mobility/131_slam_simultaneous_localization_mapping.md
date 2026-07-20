---
title: "Slam Simultaneous Localization Mapping"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
weight: 131
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLAM(Simultaneous Localization and Mapping)은 <strong>센서(카메라·LiDAR)로 주변 환경의 지도를 작성하면서 동시에 자신의 위치를 추정</strong>하는 알고리즘으로, 자율주행·XR·로봇의 핵심 기술이다.
> 2. **가치**: GPS가 안 되는 실내·지하에서도 SLAM으로 <strong>카메라만으로 위치를 파악</strong>할 수 있으며, Vision Pro·Quest 등 XR 디바이스의 Inside-Out 트래킹이 SLAM 기반이다.
> 3. **판단 포인트**: Visual SLAM(카메라)·LiDAR SLAM(라이다)을 구분하고, ORB-SLAM·RTAB-MAP이 대표적 오픈소스 구현이다.

---

## Ⅰ. 개요 및 필요성

```text
SLAM = 지도 작성(Mapping) + 위치 추정(Localization) 동시 수행
  센서 -> 특징점 추출 -> 지도 업데이트 -> 위치 보정 -> 반복
```

- **📢 섹션 요약 비유**: SLAM은 <strong>눈을 가린 채 손으로 더듬으며 방 지도를 그리면서 내 위치를 파악</strong>하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 유형 | 센서 | 특징 |
|:---|:---|:---|
| <strong>Visual SLAM</strong> | 카메라 | 저비용, XR 표준 |
| <strong>LiDAR SLAM</strong> | LiDAR | 정밀, 자율주행 |

---

## Ⅲ~Ⅴ. 결론

SLAM은 <strong>GPS 없는 환경에서 위치·공간을 인식하는 유일한 방법</strong>이며, XR·자율주행·로봇의 핵심 기반 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SLAM** | 동시 위치+지도 |
| <strong>Visual SLAM</strong> | 카메라 기반 (XR) |
| <strong>LiDAR SLAM</strong> | 라이다 기반 (자율주행) |
| **6DoF** | SLAM이 제공하는 추적 |
| **ORB-SLAM** | 대표 오픈소스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[EKF-SLAM (1990s)] -> [PTAM (2007)] -> [ORB-SLAM (2015)]
    -> [Deep SLAM (2018~, DL 기반)]
    -> [현재: Neural Radiance Fields (NeRF) + SLAM — 3D 재구성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SLAM은 **눈을 가리고 손으로 더듬어서 방 지도를 그리는** 거예요.
2. 동시에 <strong>"나는 지금 어디쯤이지?"</strong>도 알아내요.
3. VR 헤드셋이 **방 안에서 내 위치를 아는 건** SLAM 덕분이에요!
