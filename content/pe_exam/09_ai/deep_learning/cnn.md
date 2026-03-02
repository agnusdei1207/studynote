+++
title = "CNN (합성곱 신경망)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# CNN (Convolutional Neural Network, 합성곱 신경망)

## 핵심 인사이트 (3줄 요약)
> **CNN**은 합성곱 연산으로 이미지의 공간적 특징(엣지→패턴→객체)을 계층적으로 추출하는 딥러닝 아키텍처. LeNet→AlexNet→VGG→ResNet→EfficientNet→ConvNeXt 순으로 발전했으며, 2022년부터 ViT(Vision Transformer)와 경쟁한다. 객체 탐지(YOLO)·의료 영상(U-Net)·자율주행 등 실세계 비전 응용의 핵심이다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: CNN은 이미지나 시계열 데이터에서 공간적 패턴을 학습하는 딥러닝 네트워크로, 합성곱(Convolution)·풀링(Pooling)·완전연결(FC) 계층을 조합하여 계층적 특징을 추출한다.

> 비유: "스캐너로 그림 분석 — 처음엔 선을 찾고, 다음엔 모서리, 그다음엔 눈코입, 최종엔 얼굴을 인식"

**등장 배경**:
- MLP 한계: 이미지 픽셀 직접 입력 → 파라미터 폭발 (224×224×3 = 150K)
- 공간 정보 손실: 이미지 1D 펼치면 위치 정보 사라짐
- **LeNet(1989, LeCun)**: 우편번호 인식 CNN → 가중치 공유로 파라미터 절감
- **AlexNet(2012, ImageNet)**: GPU 학습, ReLU, Dropout → 딥러닝 르네상스 시작

---

### Ⅱ. 구성 요소 및 핵심 원리

**CNN 핵심 연산**:
```
[합성곱 (Convolution)]
필터(커널) W가 입력 X 위를 슬라이딩하며 내적:
output[i,j] = Σ Σ X[i+di, j+dj] × W[di, dj] + bias

특성:
- 가중치 공유 (Weight Sharing): 같은 필터를 전체 이미지 적용 → 파라미터 절감
- 지역 연결 (Local Connectivity): 일부 영역만 연결 → 공간 계층 학습
- 이동 불변성 (Translation Invariance): 어디에 있어도 같은 패턴 인식

[풀링 (Pooling)]
Max Pooling: 2×2 영역에서 최대값 선택 → 공간 크기 1/2, 특징 강화
Average Pooling: 평균값

[깊이별 특징]
Layer 1: 에지, 색상
Layer 2: 텍스처, 곡선
Layer 3: 패턴, 부품
Layer N: 얼굴, 자동차 등 고수준 특징
```

**주요 CNN 아키텍처**:
| 아키텍처 | 연도 | 특징 | 의의 |
|---------|------|------|------|
| LeNet-5 | 1989 | 초창기 CNN | 개념 증명 |
| AlexNet | 2012 | ReLU, Dropout, GPU | 딥러닝 혁명 |
| VGGNet | 2014 | 3×3 필터 통일 | 깊이 증가 |
| ResNet | 2015 | Residual Connection | 100+ 층 가능 |
| DenseNet | 2017 | 모든 이전 층 연결 | 피처 재사용 |
| EfficientNet | 2019 | 효율적 스케일링 | 모바일 최적 |
| ConvNeXt | 2022 | ViT 설계 차용 | CNN 재도약 |

**코드 예시** (ResNet 블록 구현):
```python
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    """ResNet의 핵심 - Residual Connection"""
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        
        # Shortcut projection (채널/크기 불일치 시)
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))  # 첫 번째 합성곱
        out = self.bn2(self.conv2(out))             # 두 번째 합성곱
        out += self.shortcut(identity)              # Residual 더하기!
        out = self.relu(out)                        # 최종 활성화
        return out
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + CNN vs ViT

**장단점**:
| 장점 | 단점 |
|-----|------|
| 공간 계층 특징 학습 탁월 | 소형 데이터셋에서 과적합 위험 |
| 파라미터 효율 (가중치 공유) | Attention처럼 전역 관계 포착 어려움 |
| 귀납적 편향 (이미지에 유리) | 회전 불변성 기본 미지원 |
| 하드웨어 최적화 성숙 | Global context: Transformer가 더 우수 |

**CNN vs Vision Transformer (ViT)**:
| 기준 | CNN | ViT |
|------|-----|-----|
| 귀납적 편향 | 강 (이미지 특화) | 약 (범용) |
| 소량 데이터 | 유리 | 불리 |
| 대량 데이터 | 유리 | 더 유리 |
| 전역 문맥 | 약 | 강 (Self-Attention) |
| 계산 복잡도 | O(n) | O(n²) |
| 현재 추세 | ConvNeXt (ViT 설계 차용) | DINO, SAM 등 |

> **선택 기준**: 소량 데이터/모바일 → CNN; 대규모 학습/멀티모달 → ViT; **실무엔 하이브리드 혼용**

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 아키텍처 | 기대 효과 |
|---------|--------|--------|
| 의료 영상 (엑스레이) | ResNet-50 + Fine-tuning | 진단 보조 정확도 90%+ |
| 불량품 검출 (제조) | YOLO v8 + Edge 배포 | 불량률 50% 감소 |
| 자율주행 인식 | EfficientDet + 멀티카메라 | 실시간 객체 탐지 |
| 감시 보안 (CCTV) | MobileNet v3 (경량) | 엣지에서 실시간 처리 |
| 위성 이미지 분석 | U-Net (의미론적 분할) | 토지 분류 정확도 향상 |

**관련 개념**: 합성곱, 풀링, Batch Norm, Residual, YOLO, U-Net, ViT, 전이학습, 데이터 증강

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 의료 진단 보조 | CNN 기반 의료 영상 분석 | 방사선과 의사 읽기 시간 40% 절감 |
| 제조 품질 관리 | 실시간 불량품 탐지 | 불량률 0.1% 이하 달성 |
| 자율주행 | 실시간 환경 인식 | ADAS 기능 범용화 |

> **결론**: CNN은 컴퓨터 비전의 레거시 챔피언이자 ViT와 공존하는 실용 기술. 2025년 현재 EfficientNet·ConvNeXt가 엣지/메모리 제약 환경에서 여전히 경쟁력 있으며, 의료·제조·보안 분야 핵심 인프라다.

---

## 어린이를 위한 종합 설명

**CNN은 "이미지를 계층적으로 분석하는 AI 눈"이야!**

```
사람이 그림 보는 법:
픽셀들 → 선 → 모서리 → 코, 눈 → 얼굴 → "이건 고양이!"

CNN도 똑같이:
필터1: 가로선, 세로선 찾기
필터2: 곡선, 모서리 찾기
필터3: 귀, 눈 패턴 찾기
최종:  "고양이! 95% 확신"
```

핵심 마법 "가중치 공유":
```
필터 하나로 이미지 전체 스캔!
→ 고양이가 어디 있어도 찾음!
→ 파라미터 수 1000배 절감!
```

> CNN = AI의 눈! 이미지를 단계적으로 이해해서 무엇이든 알아보는 마법 렌즈 🔍👁️

---
