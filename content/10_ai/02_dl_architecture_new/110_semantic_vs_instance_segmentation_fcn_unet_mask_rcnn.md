---
title: "Semantic Vs Instance Segmentation Fcn Unet Mask Rcnn"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 110
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Semantic Segmentation은 픽셀을 **클래스(종류)별로만 색칠**(고양이 3마리 = 전부 파란색 1덩어리)하고, Instance Segmentation은 <strong>클래스+개체별로 각각 다른 색</strong>으로 분리(고양이 1=빨강, 고양이 2=노랑)하여 동일 클래스 내 개별 객체를 식별한다.
> 2. **가치**: 종양 영역 분할(Semantic)과 도로 위 차량 개수 세기(Instance)처럼 <strong>도메인에 따라 적합한 분할 유형이 달라지며</strong>, 최근 Panoptic Segmentation이 둘을 통합하여 배경+개체를 동시에 분석한다.
> 3. **판단 포인트**: FCN(최초 E2E)->U-Net(Skip Connection)->Mask R-CNN(Instance)->SAM(Foundation Model)으로 아키텍처가 진화했으며, **엣지 디바이스 배포 시 경량화(MobileNet 백본) 필수**.

---

## Ⅰ. 개요 및 필요성

객체 탐지(YOLO)가 "어디에 무엇이 있는지" Bounding Box로 알려준다면, 이미지 분할은 "어떤 픽셀이 무엇인지"까지 정밀하게 색칠한다. 의료 MRI에서 종양 경계를 **1픽셀 단위로** 추출하거나, 자율주행에서 차선·보행자·차량을 동시에 분리하는 데 필수적이다.

```text
+-------------------------------------------------------+
|   Semantic vs Instance vs Panoptic 분할 비교           |
+-------------------------------------------------------+
|  [Semantic]         [Instance]         [Panoptic]     |
|  +------------+    +------------+    +------------+  |
|  | ████ ████ |    | ▓▓▓▓ ░░░░ |    | ▓▓▓▓ ░░░░ |  |
|  | (전부 파랑)|    | (빨강)(노랑)|    | (빨강)(노랑)|  |
|  |  1덩어리  |    | 각각 분리   |    |+배경 분리   |  |
|  +------------+    +------------+    +------------+  |
|  개체 수 파악 불가   개체 수 파악 가능  완전 분석       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Semantic은 "여기에 양 떼가 있다"(하얀 덩어리), Instance는 "첫째 양, 둘째 양, 셋째 양"(각각 다른 색), Panoptic은 "양+풀밭+하늘 전부 분리"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 모델 | 유형 | 핵심 혁신 | 한계 |
|:---|:---|:---|:---|
| **FCN (2015)** | Semantic | FC Layer -> 1×1 Conv 대체, 위치 정보 보존 | 해상도 손실 |
| **U-Net (2015)** | Semantic | Skip Connection으로 인코더 특징 직접 전달 | 개체 구별 불가 |
| <strong>Mask R-CNN (2017)</strong> | Instance | Faster R-CNN + 마스크 Branch + RoIAlign | 연산 비용 높음 |
| **Panoptic FPN** | Panoptic | Semantic + Instance 통합 | 가장 무거움 |
| **SAM (2023)** | 범용 | 프롬프트 기반 Foundation Model | Fine-tuning 필요 |

### Mask R-CNN 동작 원리
1. <strong>백본(ResNet)</strong>: 이미지에서 특징 맵 추출.
2. **RPN (Region Proposal Network)**: 객체 후보 영역 제안.
3. **RoIAlign**: 후보 영역을 정밀 정렬 (기존 RoIPooling의 반올림 오차 제거).
4. **3-Head**: 분류(Classification) + 박스 회귀(Box Regression) + <strong>마스크(Mask) 예측</strong>을 병렬 수행.

- **📢 섹션 요약 비유**: Mask R-CNN은 "감시 카메라(RPN)가 수상한 사람을 찍으면, 형사(RoIAlign)가 정밀 수사하고, 프로파일(분류+박스+마스크) 3장을 동시에 작성하는" 시스템이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Classification | Detection | Semantic Seg. | Instance Seg. |
|:---|:---|:---|:---|:---|
| **출력** | 클래스 1개 | 박스 N개 | 픽셀별 클래스 | 픽셀별 마스크+ID |
| <strong>정밀도</strong> | 이미지 단위 | 박스 단위 | 픽셀 단위 | **픽셀+개체** |
| **대표 모델** | ResNet | YOLO | U-Net | Mask R-CNN |
| **연산 비용** | 낮음 | 중간 | 높음 | **매우 높음** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도메인별 선택 가이드
1. **의료 MRI**: U-Net (Semantic) — 종양 영역 vs 정상 조직 분류.
2. **자율주행**: Panoptic — 차선(배경 Semantic) + 차량 개수(Instance).
3. **영상 편집 누끼**: Instance — 인물 개별 분리.

### 안티패턴
- **Semantic으로 밀집 객체 세기**: 주차장 차량 100대를 Semantic으로 처리 -> 하나의 덩어리 -> 개수 파악 불가.

---

## Ⅴ. 기대효과 및 결론

| 지표 | Detection (Box) | Instance Seg. | 개선 |
|:---|:---|:---|:---|
| 객체 윤곽 | IoU ~70% | **IoU ~90%** | 20%p |
| 의료 진단 | 불가 | **암세포 경계 추출** | 신규 역량 |
| 자율주행 안전 | 박스 겹침 | **개체별 정밀 분리** | 사고율 감소 |

SAM(Segment Anything Model)의 등장으로 "프롬프트 한 번에 모든 객체를 분할하는" Foundation Model 시대가 열렸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **FCN** | 최초의 End-to-End Semantic Segmentation 모델 |
| **U-Net** | Skip Connection으로 의료 분할 정복 |
| <strong>Mask R-CNN</strong> | Instance Segmentation의 사실상 표준 |
| <strong>Panoptic Segmentation</strong> | Semantic + Instance 통합 분석 |
| <strong>SAM (Segment Anything)</strong> | Foundation Model 기반 범용 분할 |

### 📈 관련 키워드 및 발전 흐름도

```text
[FCN (2015) — 최초 E2E Semantic Segmentation]
    |
    v
[U-Net (2015) — Skip Connection, 의료 영상 정복]
    |
    v
[Mask R-CNN (2017) — Instance Segmentation 확립]
    |
    v
[Panoptic FPN (2019) — Semantic+Instance 통합]
    |
    v
[SAM (2023) — 프롬프트 기반 범용 분할 Foundation Model]
```

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>Semantic</strong>은 양 떼를 전부 하얀색으로만 칠하는 거예요 (양이 몇 마리인지는 몰라요).
2. <strong>Instance</strong>는 첫째 양은 빨강, 둘째 양은 파랑으로 각각 다르게 칠해서 몇 마리인지 세는 거예요.
3. 어떤 기술을 쓸지는 "양이 어디 있는지만 알면 되는지, 몇 마리인지 세야 하는지"에 따라 달라요!
