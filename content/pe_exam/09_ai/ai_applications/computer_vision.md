+++
title = "컴퓨터 비전 (Computer Vision)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 컴퓨터 비전 (Computer Vision, CV)

## 핵심 인사이트 (3줄 요약)
> **컴퓨터 비전**은 디지털 이미지·비디오에서 정보를 추출·이해하는 AI 분야로, 분류→탐지→분할→생성 순으로 발전했다. YOLO·SAM·NeRF·3D Gaussian Splatting 등 2024년 최신 기술이 자율주행·의료·제조·XR을 혁신 중이다. Transformer 기반 ViT·SAM이 CNN을 보완하며 기반 모델화(foundation model) 추세가 강하다.

---

### Ⅰ. 개요  ↔  개념 + 등장 배경

**개념**: 컴퓨터 비전은 컴퓨터가 디지털 이미지·비디오에서 의미 있는 정보를 추출하고 인식·이해·생성하는 기술 분야이다.

> 비유: "카메라를 달아주고 무엇이든 보고 이해하는 AI의 눈"

**등장 배경**:
- AlexNet(2012): ImageNet 대회 딥러닝으로 10% 성능 격차 달성 → CV 혁명 시작
- YOLO(2015): 실시간(60 FPS) 객체 탐지 가능 공개
- ImageNet 수준 초과(2015): 딥러닝이 인간 분류 정확도 초월
- GPT-4V(2023): LLM이 이미지 이해까지 → 멀티모달 AI 시대

---

### Ⅱ. 구성 요소 및 핵심 원리

**CV 태스크 분류**:
| 태스크 | 설명 | 대표 모델 |
|-------|------|---------|
| 이미지 분류 | 이미지 → 카테고리 | ResNet, EfficientNet, ViT |
| 객체 탐지 | 객체 위치(Bounding Box) + 클래스 | YOLO v8, DETR, Faster R-CNN |
| 의미론적 분할 | 픽셀별 클래스 | DeepLab v3+, SegFormer |
| 인스턴스 분할 | 개체별 분리 | Mask R-CNN, Mask2Former |
| 포즈 추정 | 키포인트 위치 | OpenPose, ViTPose |
| 이미지 생성 | 텍스트→이미지 | Stable Diffusion, DALL-E 3 |
| 3D 재구성 | 2D→3D 변환 | NeRF, 3DGS |
| 비디오 이해 | 동작 인식, 추적 | Video Swin, ByteTrack |

**핵심 원리 - YOLO (객체 탐지)**:
```
YOLO (You Only Look Once):
  이미지를 S×S 그리드로 분할
  각 셀: B개 Bounding Box + 신뢰도 + C개 클래스 확률
  단 1번의 순전파로 탐지 → 실시간 가능!

YOLO v8 (2023):
  Anchor-free (앵커 박스 없음)
  C2f 블록 (CSP+FPN)
  Speed: 640×640 이미지 → 2ms (RTX 4090)
  mAP50-95: 50.2 (COCO val)
```

**SAM (Segment Anything Model, 2023 Meta)**:
```
모든 것을 분할하는 기반 모델:
  입력: 이미지 + 포인트/박스/텍스트 프롬프트
  출력: 해당 객체의 정확한 마스크

3가지 프롬프트:
  1. 점 클릭 → 해당 객체 분할
  2. 박스 → 박스 내 주요 객체 분할
  3. 자동 → 이미지 내 모든 객체 자동 분할
```

**코드 예시** (YOLOv8 탐지):
```python
from ultralytics import YOLO
import cv2

# YOLOv8 모델 로딩 (사전학습)
model = YOLO("yolov8x.pt")  # x: 가장 정확한 버전

# 이미지 탐지
results = model.predict(
    source="traffic.jpg",
    conf=0.25,       # 신뢰도 임계값
    iou=0.45,        # NMS IoU 임계값
    imgsz=640,       # 입력 크기
    device="cuda",
    save=True,       # 결과 저장
)

for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        cls_id = int(box.cls[0].item())
        cls_name = model.names[cls_id]
        print(f"{cls_name}: {conf:.2f} at ({x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f})")

# 실시간 웹캠 탐지
model.predict(source=0, show=True, stream=True, conf=0.5)
```

---

### Ⅲ. 기술 비교 분석  ↔  장단점 + 객체 탐지 알고리즘 비교

**객체 탐지 알고리즘 비교**:
| 모델 | 속도 | 정확도 | 특징 | 용도 |
|------|------|------|------|------|
| YOLO v8 | 매우 빠름 | 높음 | 실시간, Anchor-free | 엣지, 실시간 |
| YOLO v9/v10 | 매우 빠름 | 더 높음 | 프로그래밍 가능 구배 | 최신 실무 |
| RT-DETR | 빠름 | 매우 높음 | Transformer 기반 실시간 | 고정밀 실시간 |
| DETR | 느림 | 매우 높음 | NMS 불필요, E2E | 연구, 정밀도 |
| Faster R-CNN | 느림 | 높음 | 레거시 표준 | 정밀 분석 |

> **선택 기준**: 실시간 엣지 → YOLO; 최고 정확도 → DETR 계열; 멀티모달 → SAM

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | CV 기술 | 기대 효과 |
|---------|-------|--------|
| 제조 품질 검사 | YOLO v8 + 결함 탐지 | 불량률 0.1% 이하, 24/7 검사 |
| 자율주행 인식 | YOLO + 세그멘테이션 + 깊이 추정 | 실시간 360도 환경 인식 |
| 의료 영상 진단 | SAM + 의료 데이터 파인튜닝 | 암 조기 발견 정확도 향상 |
| 소매 재고 관리 | 객체 탐지 + 셀프 계산대 | 재고 오류 90% 감소 |
| 보안 CCTV | 실시간 탐지 + 행동 인식 | 이상 행동 자동 감지 |
| AR/VR | NeRF + 3DGS 장면 재구성 | 현실감 있는 가상 환경 |

**최신 트렌드 (2024~2025)**:
```
SAM 2 (Segment Anything 2, 2024):
  비디오 + 이미지 통합 분할
  → 실시간 비디오 추적 + 분할!

3D Gaussian Splatting (3DGS):
  NeRF보다 100배 빠른 실시간 3D 렌더링
  → AR/VR, 자율주행 시뮬레이터

Foundation Model for Vision:
  DINOv2, SAM → Vision 기반 모델 시대
  → 소량 레이블로 모든 비전 태스크 적용
```

**관련 개념**: CNN, YOLO, ViT, SAM, NeRF, 3DGS, Transfer Learning, Semantic Segmentation

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량적 효과 |
|---------|-----|----------|
| 자동화 | 시각 검사 자동화 | 인건비 50~80% 절감 |
| 정확도 | AI 진단 보조 | 암 검출 민감도 95%+ |
| 속도 | YOLO 실시간 탐지 | 1ms 이내 판단 |

> **결론**: 컴퓨터 비전은 AI의 "눈"으로 자율주행·의료·제조·XR을 혁신하는 핵심 분야다. YOLO v8+SAM+3DGS가 2024~2025 실무 표준이며, 멀티모달 LLM(GPT-4V, Gemini)이 비전+언어를 통합하는 새 패러다임이다.

---

## 어린이를 위한 종합 설명

**컴퓨터 비전은 "AI에게 눈을 달아주는 것"이야!**

```
사람의 눈: 빛 → 망막 → 뇌 → "강아지가 달린다!"

AI의 눈: 카메라 → 픽셀 → CNN → "97% 강아지, 위치: 좌측 상단"

YOLO (실시간 탐지):
사진 한 장을 보면 모두 찾아내!
"강아지(95%), 공(87%), 나무(72%),  자동차(99%)..."
단 2ms 만에!
```

실생활에서:
```
자율주행차: 카메라로 보고 → 보행자, 신호등, 차선 인식
틱톡 AR 필터: 얼굴 인식 → 귀여운 필터 실시간 적용
의료 AI: 엑스레이 보고 → "폐에 0.5cm 이상 종양 발견"
```

> 컴퓨터 비전 = AI가 세상을 보는 방법! 📸👁️🤖

---
