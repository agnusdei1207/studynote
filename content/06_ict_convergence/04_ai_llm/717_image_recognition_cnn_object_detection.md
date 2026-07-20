---
title: "Image Recognition CNN Object Detection"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 717
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CNN은 합성곱(Convolution)·풀링(Pooling)·비선형 활성화(ReLU/GELU)·정규화(BN/LN)의 4대 연산을 통해 픽셀 공간의 국소 패턴을 점진적으로 추상화하는 **계층적 특징 학습(Hierarchical Feature Learning)** 메커니즘이며, 객체 탐지·분할은 이를 Backbone–Neck–Head 구조로 확장해 **Classification + Localization + (Mask/Distance)** 의 다중 태스크로 일반화한 것이다.
> 2. **가치**: ImageNet Top-5 90%+ (EfficientNet-V2 L, ConvNeXt-XL), COCO test-dev mAP 64.4 (InternImage-H, 2023), Cityscapes mIoU 85.5% (Mask2Former, Swin-L 백본) 등 SOTA 성능을 달성하며, Edge–Cloud–GPU 가속을 통해 실시간성(30~120 FPS, YOLOv8-N/TensorRT FP16)과 정확도(2-stage, Cascade Mask R-CNN)의 양립이 가능해졌다.
> 3. **판단 포인트**: ① **1-stage vs 2-stage** (속도 vs 정확도), ② **Anchor-based vs Anchor-free** (사전 정의 박스 vs Keypoint/Center/Query), ③ **CNN vs ViT/Hybrid** (귀납 편향 vs 글로벌 수용영역), ④ **Instance vs Semantic vs Panoptic** (픽셀 단위 의미론적 분리), ⑤ **Supervised vs Self-supervised / Foundation Model** (라벨 의존도 vs 범용성) — 이 5축이 아키텍처·비용·운영 복잡도를 결정짓는 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

이미지 인식은 컴퓨터 비전의 근간으로, **Classification(이미지 분류) -> Object Detection(객체 탐지) -> Semantic/Instance/Panoptic Segmentation(의미론적·인스턴스·전경 분할)** 의 3단계로 발전해왔다. 2012년 AlexNet이 ImageNet ILSVRC에서 8위권 대비 10.8%p 차이로 우승하며 **딥러닝 기반 컴퓨터비전 시대**를 개막했고, 이후 VGG(2014)->GoogLeNet/Inception(2014)->ResNet(2015)->EfficientNet(2019)->ViT(2020)->ConvNeXt(2022)로 백본이 진화함에 따라 객체 탐지·분할도 R-CNN(2014)->Faster R-CNN(2015)->YOLO(2016)->Mask R-CNN(2017)->DETR(2020)->Segment Anything(2023) 시대를 맞았다.

**기존(전통 영상처리) 패러다임**은 SIFT/HOG/SURF 등 hand-crafted feature + SVM/Adaboost 분류기를 사용했으나, ① 조명·회전·스케일 변화에 취약, ② 도메인 전이(domain shift) 시 재설계 필요, ③ 비선형·고차원 패턴 한계로 실제 환경(자율주행·의료·제조) 적용에 한계가 있었다. **신규(CNN 기반) 패러다임**은 End-to-End 학습으로 ① 대량 데이터에서 자동 특징 추출, ② Translation Equivariance(평등 이동 등변성)와 Local Receptive Field(국소 수용영역)의 귀납 편향(Inductive Bias)을 통해 데이터 효율성 확보, ③ GPU/TPU 가속과 양자화·프루닝·Knowledge Distillation으로 실시간 추론이 가능해져 산업 현장 전반으로 확산되었다.

```text
[ 전통 영상처리 vs 딥러닝 기반 이미지 인식 파이프라인 비교 ]

 전통 파이프라인                          딥러닝 파이프라인
 -------------                          --------------
 Input Image                             Input Image
     |                                       |
     v                                       v
 +---------+                            +----------+
 |Preproc. | (Resize, Normalize)        |Preproc.  | (Resize, Normalize,
 |Resize,  |                            |          |  Augmentation: Flip,
 |Gray,    |                            |          |  Mosaic, MixUp, CutMix)
 |HistEq.  |                            +----+-----+
 +----+----+                                  |
      v                                       v
 +----------+                           +--------------+
 |Feature   | (SIFT/HOG/SURF/ORB)       |Backbone CNN  | (ResNet-50/101,
 |Extract   |  Hand-crafted             |or ViT/Hybrid |  EfficientNet-B4,
 +----+-----+                           |              |  ConvNeXt-T/S,
      v                                 |              |  Swin-T/S/B/L)
 +----------+                           +------+-------+
 |Encoder   | (Bag-of-Words,                 v
 |(BoW/SPM) |  Fisher Vector)        +------------------+
 +----+-----+                        |Neck              | (FPN, PANet,
      v                              |                  |  BiFPN, NAS-FPN)
 +----------+                        +--------+---------+
 |Classifier| (SVM/Adaboost/RF)                v
 +----+-----+                          +------------------+
      v                                |Head              | (RPN+RoIHead,
Output: Class + Score                  |                  |  YOLO Head,
                                        |                  |  DETR Query,
                                        |                  |  Mask Head)
                                        +--------+---------+
                                                 v
                                       Output: Class + Box
                                                + Mask / Keypoint
```

- **📢 섹션 요약 비유**: 전통 영상처리가 **"돋보기로 글자 하나하나를 외워서 맞추는 방식"** 이라면, CNN은 **"수많은 그림을 보며 뇌의 시각 피질처럼 자동으로 패턴을 학습하는 방식"** 입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. CNN 백본(Backbone) — 특징 추출의 심장

CNN은 입력 이미지 $\mathbf{X} \in \mathbb{R}^{H \times W \times 3}$에 대해 합성곱 연산을 반복 적용해 **저수준 엣지/텍스처 -> 중간 패턴(부분) -> 고수준 의미(semantic)** 로 추상화한다.

핵심 연산은 다음과 같다.

**(1) 합성곱(Convolution)**: 필터 $\mathbf{W} \in \mathbb{R}^{k_h \times k_w \times C_{in} \times C_{out}}$ 와 입력의 슬라이딩 내적 -> 출력 특징맵 $F_{out} = \mathbf{W} * \mathbf{X} + \mathbf{b}$. Dilation, Depthwise Separable Conv(MobileNet, Xception), Group Conv(ResNeXt), Deformable Conv(DCN v2, InternImage) 등으로 확장.

**(2) 풀링(Pooling)**: MaxPool / AvgPool / Global Average Pooling(GAP, ResNet GAP head) / Spatial Pyramid Pooling(SPP, SPP-Net) / ASPP(Atrous Spatial Pyramid Pooling, DeepLab v3+).

**(3) 활성화(Activation)**: ReLU $f(x)=\max(0,x)$ -> LeakyReLU, PReLU -> GELU(Transformer 계열) -> Swish/SiLU(EfficientNet, YOLOv5) -> Mish(YOLOv4, YOLOv5 기본).

**(4) 정규화(Normalization)**: BatchNorm(배치 통계) -> LayerNorm(ViT) -> GroupNorm(Segmentation, small batch) -> InstanceNorm(스타일 전이) -> SyncBN(다중 GPU).

```text
[ CNN Backbone — ResNet-50의 Residual Block 구조와 Stage별 출력 해상도 ]

Input Image (H × W × 3)
        |
        v
 +------------------+
 | Conv 7×7, 64,    |  stride 2      ->  H/2 × W/2 × 64
 | BN + ReLU        |
 | MaxPool 3×3, /2  |                ->  H/4 × W/4 × 64
 +--------+---------+
          v
 +------------------+  Stage 1
 | [Conv 1×1, 64]   |                ->  H/4 × W/4 × 256
 | [Conv 3×3, 64] ×3  (Bottleneck)  |  (C2 feature)
 | [Conv 1×1, 256]  |
 | + Shortcut(Identity)              |
 +--------+---------+
          v
 +------------------+  Stage 2  stride 2
 | Bottleneck ×6    |                ->  H/8 × W/8 × 512
 +--------+---------+                 (C3 feature)
          v
 +------------------+  Stage 3  stride 2
 | Bottleneck ×6    |                ->  H/16 × W/16 × 1024
 +--------+---------+                 (C4 feature)
          v
 +------------------+  Stage 4  stride 2
 | Bottleneck ×3    |                ->  H/32 × W/32 × 2048
 +--------+---------+                 (C5 feature)
          v
       Neck (FPN/PANet/BiFPN) ->  P3(1/8), P4(1/16), P5(1/32), P6, P7
          |
          v
       Head (Detection / Segmentation / Keypoint)
```

### 2. Neck(다중 스케일 특징 융합)

- **FPN(Feature Pyramid Network, 2017)**: Top-down + Lateral Connection으로 C2~C5를 P2~P5로 변환. 소형 객체 탐지 성능 향상.
- **PANet(2018)**: FPN에 Bottom-up 경로 추가 -> P2~P5 양방향 융합.
- **BiFPN(EfficientDet, 2020)**: 가중치 기반 다중 입력 융합(Weighted Feature Fusion), 반복적 stacking.
- **NAS-FPN / NAS-FCOS**: Neural Architecture Search로 FPN 구조 자동 탐색.

### 3. Head(태스크별 출력)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Classification Head** | 클래스 확률 $p(c)$ 산출 | Softmax (단일 라벨) / Sigmoid (Multi-label, YOLOv3+) / Focal Loss (RetinaNet, $\gamma=2$ 기본) |
| **Regression Head** | Bounding Box $(x,y,w,h)$ 또는 $(l,t,r,b)$ 오프셋 회귀 | Smooth L1 (Faster R-CNN) / IoU Loss (UnitBox) / GIoU/CIoU/DIoU (YOLOv5~v8) / Distribution Focal Loss (DFL, YOLOX) |
| **Mask Head** | 픽셀 단위 이진 마스크 예측 | FCN(ResNet) + RoIAlign (Mask R-CNN) / PointRend / Feature Pyramid + Transformer Decoder (Mask2Former) |
| **Keypoint Head** | 인체 17 keypoint (COCO) 추정 | Heatmap regression + MSE Loss (OpenPose, HRNet) |
| **Query-based Head** | Set Prediction으로 N개 객체 직접 출력 | DETR (Hungarian Matching, O(N²) Attention) / Deformable DETR (Multi-scale Deformable Attention) / DINO (Contrastive DeNoising) |
| **Anchor-free Head** | Center/Keypoint/Box-Corner 기반 | CenterNet (heatmap+wh), FCOS (FPN per-pixel), YOLOv8 (Decoupled head) |

### 4. 주요 손실 함수(Loss Function)

$$\mathcal{L}_{total} = \lambda_{cls}\mathcal{L}_{cls} + \lambda_{box}\mathcal{L}_{box} + \lambda_{mask}\mathcal{L}_{mask} + \lambda_{obj}\mathcal{L}_{obj}$$

- **Classification**: Cross-Entropy / Focal Loss $(1-p_t)^\gamma$ (RetinaNet, $\gamma=2, \alpha=0.25$)
- **Box Regression**: Smooth L1 / **CIoU Loss** $\mathcal{L}_{CIoU} = 1 - IoU + \frac{\rho^2(b,b^{gt})}{c^2} + \alpha v$ (YOLOv5~v8)
- **Objectness**: BCE with Focal
- **Mask**: Average Binary Cross-Entropy (Mask R-CNN, 28×28 RoI)
- **DFL(Distribution Focal Loss)**: 박스 좌표를 이산 분포로 모델링 (YOLOX, YOLOv8)

### 5. 평가 지표(Evaluation Metrics)

- **Classification**: Top-1/Top-5 Accuracy, F1, mAP
- **Detection**: mAP@[.5, .75, .5:.95] (COCO), AP per class, AR(L/M/S), FPS
- **Segmentation**: mIoU (Jaccard), Pixel Accuracy, Dice Coefficient, Boundary F1 (cityscapes), PQ (Panoptic Quality)
- **Pose**: OKS-based AP, PCK

### 6. 학습 기법

- **Augmentation**: Mosaic(4-image, YOLOv4~), MixUp, CutMix, Copy-Paste(RandAugment, AugMix, Mosaic-9)
- **Optimizer**: SGD+momentum(0.9), AdamW(ViT), Lion(2023), LAMB(대규모 batch)
- **Scheduler**: Cosine Annealing, Warmup+Cosine, OneCycle
- **Regularization**: Dropout, DropBlock, Stochastic Depth, Label Smoothing(0.1), EMA(Exponential Moving Average, YOLOv5~v8 기본)
- **Auto Augmentation**: AutoAugment, RandAugment, TrivialAugment

- **📢 섹션 요약 비유**: CNN 백본은 **"현미경(Conv) -> 요약 노트(Pool) -> 생각 정리(Activation) -> 동료 검토(BN)"** 를 반복하며, 점점 추상적인 개념을 만드는 **"공부 잘하는 학생"** 과 같습니다.

---

## Ⅲ. 비교 및 연결

### 1. 분류·탐지·분할 패러다임 비교

| 구분 | Image Classification (ResNet, ViT) | Object Detection (Faster R-CNN, YOLO) | Semantic Segmentation (DeepLab, U-Net) | Instance Segmentation (Mask R-CNN, YOLACT) | Panoptic Segmentation (Mask2Former, Panoptic FPN) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **출력 단위** | 이미지 1개 -> 클래스 벡터 | 이미지 1개 -> N×(cls, box) | 이미지 -> H×W 클래스맵 | N개 객체별 클래스+박스+마스크 | 모든 픽셀에 class+instance id |
| **공간 정보** | 손실 (GAP 후 1D) | 박스 단위 유지 | 픽셀 단위 유지 | 픽셀 단위 + 인스턴스 분리 | 픽셀+인스턴스(stuff+thing) |
| **대표 모델** | ResNet-50, ViT-L/16, ConvNeXt | Faster R-CNN, RetinaNet, YOLOv8, DETR | FCN, U-Net, DeepLab v3+, SegFormer, HRNet | Mask R-CNN, YOLACT, SOLO, PointRend | Panoptic FPN, Mask2Former, kMaX-DeepLab |
| **학습 데이터** | ImageNet(1.2M) | COCO(118K), Objects365, OpenImages | Cityscapes,