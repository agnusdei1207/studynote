---
title: "Computer Vision Object Detection Segmentation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 667
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 객체 탐지(Object Detection)와 세그멘테이션(Segmentation)은 이미지 내 객체의 위치(BBox), 클래스, 픽셀 단위 마스크를 예측하는 컴퓨터 비전의 3대 핵심 태스크로, **R-CNN 계열(2-stage) -> YOLO/SSD 계열(1-stage) -> Mask R-CNN/Mask2Former -> DETR/SAM(Transformer/Foundation Model)**로 패러다임이 진화하며 정확도(mAP)-속도(FPS)-일반화(Zero-shot) 트레이드오프를 정량적으로 해결하는 것이 본질이다.
> 2. **가치**: 의료영상(Multi-Organ Segmentation Dice 0.85+, nnU-Net), 자율주행(3D BEV Perception mAP 70+, Waymo Open Dataset), 산업 결함 검출(불량률 99.5%+ Recall), 리테일/POS 분석(객체 카운팅 mAP 80+) 등에서 라벨링 비용 절감(SAM 기반 Auto-Labeling으로 BBox->Mask 라벨링 시간 약 1/10), Foundation Model(CLIP/DINOv2) 기반의 도메인 적응력, 그리고 Multi-task Learning을 통한 End-to-End 통합 가치를 제공한다.
> 3. **판단 포인트**: 태스크 요구사항(Classification/Detection/Instance/Panoptic), 데이터 규모(수백 장 vs 수십만 장), 실시간성(Edge: 30+ FPS vs Server: 1~10 FPS), 라벨링 비용(BBox 대비 Mask 약 8~15배), Anchor-based vs Anchor-free, CNN vs Transformer, Specialist(도메인 특화) vs Generalist(범용 Foundation Model) 간의 아키텍처 결정이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 컴퓨터 비전(Hand-crafted Feature 기반)은 **HOG(Histogram of Oriented Gradients) + SVM**, **SIFT(Scale-Invariant Feature Transform)**, **Selective Search** 등으로 객체를 검출했으나, **조명 변화, 회전/스케일 변동, 폐색(Occlusion), 클래스 간 Intra-class Variation**에 극도로 취약했다. 2012년 AlexNet의 등장 이후 Deep Learning 기반 객체 탐지는 **"End-to-End 학습 + Hierarchical Feature Representation"** 패러다임으로 전환되며 매년 새로운 SOTA 모델이 등장하는 가장 활발한 연구 분야로 자리 잡았다.

특히 **Mask R-CNN(2017, He et al.)**은 탐지와 세그멘테이션을 통합한 첫 번째 실용적 프레임워크였고, **DETR(2020, Facebook AI)**은 **Hungarian Matching**을 통해 NMS 없이 End-to-End를 구현하는 패러다임 전환을 일으켰다. 2023년 Meta AI의 **SAM(Segment Anything Model)**은 **Foundation Model + Promptable Segmentation** 개념으로 "라벨 없는 대규모 데이터 + 사용자 프롬프트" 기반의 Zero-shot Generalization을 가능케 했다.

### 패러다임 비교: Hand-crafted vs Deep Learning vs Foundation Model

| 시대 | 기법 | 한계 | 대표 모델 |
| :--- | :--- | :--- | :--- |
| **Hand-crafted (2000s~2012)** | HOG/DPM/SIFT + SVM | 도메인 종속, 조명/스케일 취약 | Dalal-Triggs HOG, DPM, BoW |
| **Deep Learning (2012~2020)** | CNN 기반 Supervised 학습 | 대량 라벨 의존, 도메인 전이 어려움 | R-CNN, Fast/Faster R-CNN, YOLO, SSD, Mask R-CNN |
| **Transformer/FM (2020~)** | Self-Attention, Self-Supervised | 연산량, 데이터 큐레이션 비용 | DETR, ViT, Swin, Mask2Former, SAM, DINOv2 |

```text
+------------------------------------------------------------------+
|         컴퓨터 비전 객체 탐지·세그멘테이션 패러다임 진화          |
+------------------------------------------------------------------+
|  [Old] Hand-crafted Feature                                      |
|   입력 이미지 -> SIFT/HOG 추출 -> Bag-of-Visual-Words ->           |
|   SVM 분류 -> BBox(느림, 정확도 낮음)                            |
|        |                                                         |
|        v                                                         |
|  [New 1] Deep Learning (CNN)                                    |
|   입력 이미지 -> CNN Backbone(ResNet) -> Region Proposal(RPN) ->  |
|   RoI Pooling -> Classification + Regression Head                 |
|        |                                                         |
|        v                                                         |
|  [New 2] End-to-End Transformer                                 |
|   입력 이미지 -> CNN/ViT Backbone -> Encoder-Decoder(Attention) ->|
|   Hungarian Matching -> Set Prediction (NMS 불필요)              |
|        |                                                         |
|        v                                                         |
|  [New 3] Foundation Model + Prompt                              |
|   Image + Point/Box/Mask Prompt -> ViT-H Backbone ->               |
|   Prompt Encoder -> Mask Decoder -> Zero-shot Segmentation        |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Hand-crafted 방식은 **"돋보기로 글자를 하나하나 찾는 탐정"**이었다면, Deep Learning은 **"수만 장의 도감을 공부한 전문가"**, Foundation Model은 **"한 번 배운 후 어디서든 즉시 추론 가능한 박사"**와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

현대 객체 탐지/세그멘테이션 시스템은 크게 **4계층 아키텍처**로 구성된다. 각 계층은 독립적으로 최적화 가능하며, **Backbone -> Neck -> Head -> Post-Processing**의 파이프라인이 표준이다.

```text
+------------------------------------------------------------------+
|         현대 객체 탐지/세그멘테이션 통합 아키텍처                |
|                                                                  |
|  +------------+    +------------+    +----------------------+  |
|  |  Backbone  |---->|    Neck    |---->|     Head(Multi-task) |  |
|  |            |    |            |    |  +-----------------+ |  |
|  | ResNet-50  |    |    FPN     |    |  |  Cls + Reg Head | |  |
|  | Swin-T/L   |    |   PANet    |    |  +-----------------+ |  |
|  | ConvNeXt   |    |   BiFPN    |    |  |   Mask Head     | |  |
|  | ViT-H/14   |    |            |    |  +-----------------+ |  |
|  |            |    |  Multi-    |    |  |  Keypoint Head  | |  |
|  | (Hierarchical|  |  scale     |    |  +-----------------+ |  |
|  |  Feature   |    |  Feature   |    |  |   Depth Head    | |  |
|  |  Extract.) |    |  Fusion    |    |  +-----------------+ |  |
|  +------------+    +------------+    +----------+-----------+  |
|                                                  |               |
|                                                  v               |
|                                       +----------------------+  |
|                                       |   Post-Processing    |  |
|                                       |  NMS / Soft-NMS      |  |
|                                       |  Hungarian Matching  |  |
|                                       |  Box/Mask Refine     |  |
|                                       +----------------------+  |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Backbone** | 입력 이미지에서 Hierarchical Feature 추출 | ResNet-50/101(Residual Block), Swin-T/S/B/L(Window Attention), ConvNeXt(Large Kernel + Layer Norm), EfficientNet(Compound Scaling), ViT-H/14(Global Attention, SAM용) |
| **Neck** | Multi-scale Feature Fusion으로 작은/큰 객체 동시 검출 | FPN(Top-down), PANet(Bottom-up 추가), BiFPN(Weighted Fusion, EfficientDet), NAS-FPN(Neural Architecture Search) |
| **Head** | 태스크별 예측(분류/회귀/마스크) | R-CNN 계열: RPN + RoI Head, YOLO 계열: Decoupled Head, Mask R-CNN: Mask Head(28×28 RoIAlign), Mask2Former: Masked Attention |
| **Post-Processing** | 중복 검출 제거 및 결과 정제 | NMS(IoU > 0.5 제거), Soft-NMS(Gaussian Decay), DIoU-NMS(CIoU 기반), Hungarian Matching(DETR, 1:1 매칭) |

### 태스크별 핵심 손실 함수(Loss Function) 및 평가 지표

| 태스크 | 출력 | 주요 Loss | 평가 지표 |
| :--- | :--- | :--- | :--- |
| **Image Classification** | Class Probability | Cross-Entropy, Label Smoothing, Focal Loss | Top-1/Top-5 Accuracy |
| **Object Detection** | (x,y,w,h) + Class | Smooth L1(BBox) + Focal Loss(Cls) | **mAP@[.5, .95]**, AP per Class |
| **Semantic Segmentation** | Per-pixel Class Map | Cross-Entropy, Dice Loss, Lovász Loss | **mIoU**(Jaccard Index), Pixel Accuracy |
| **Instance Segmentation** | Per-instance Mask | Mask R-CNN: BCE(28×28 Mask) + BBox Loss | **Mask mAP**, Boundary AP |
| **Panoptic Segmentation** | Semantic + Instance 통합 | PQ Loss, Mask + Class CE | **PQ**(Panoptic Quality), SQ, RQ |

### 핵심 알고리즘 상세

**1) NMS(Non-Maximum Suppression) 알고리즘**:
```
1. 모든 검출 BBox를 Confidence Score 기준 내림차순 정렬
2. 최고 Score BBox를 선택 -> 최종 결과에 추가
3. 선택된 BBox와 나머지 BBox의 IoU 계산
4. IoU > threshold(보통 0.5)인 BBox 제거
5. 2~4 반복
```

**2) IoU Loss 진화**: L1/L2 Loss -> IoU Loss -> **GIoU**(Generalized IoU, 폐색 대응) -> **DIoU**(Distance-IoU, 중심점 거리) -> **CIoU**(Complete-IoU, 종횡비 일치도)

**3) DETR의 Hungarian Matching**:
- GT(Object)와 Prediction 간 **최적 1:1 매칭**을 위해 Hungarian Algorithm 적용
- Cost = λ_cls × L_class + λ_box × L_bbox + λ_mask × L_mask
- NMS 없이 End-to-End 학습 가능 -> 중복 검출 구조적 제거

- **📢 섹션 요약 비유**: Backbone은 **"뇌의 시각 피질"**, Neck은 **"다리미 통합 감각(시각+촉각 융합)"**, Head는 **"최종 판단을 내리는 전두엽"**, Post-Processing은 **"확정된 결론을 정리하는 편집자"**와 같다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 1-Stage vs 2-Stage vs Transformer Detector

| 구분 | 2-Stage (R-CNN 계열) | 1-Stage (YOLO/SSD 계열) | End-to-End Transformer (DETR) |
| :--- | :--- | :--- | :--- |
| **대표 모델** | Faster R-CNN, Cascade R-CNN | YOLOv5/v8/v9, SSD, RetinaNet, FCOS | DETR, Deformable DETR, DINO, RT-DETR |
| **구조** | RPN(Region Proposal) -> RoI Head | Grid 기반 직접 예측 | CNN/Transformer + Set Prediction |
| **mAP (COCO)** | 42~46 | 37~55 (YOLOv8-x 53.9) | 44~63 (DINO-5scale 63.2) |
| **FPS** | 5~15 (느림) | 30~160+ (빠름) | 5~20 (중간) |
| **NMS** | 필요 | 필요 | **불필요** (구조적 제거) |
| **소형 객체** | FPN으로 강함 | 약점 (해결책: BiFPN, P2 레벨 추가) | Deformable Attention으로 개선 |
| **학습 수렴** | 안정적 (2-stage)