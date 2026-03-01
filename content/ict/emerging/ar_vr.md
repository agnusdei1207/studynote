+++
title = "AR/VR/MR (증강/가상/혼합 현실)"
date = 2025-03-01

[extra]
categories = "ict-emerging"
+++

# AR/VR/MR (증강/가상/혼합 현실)

## 핵심 인사이트 (3줄 요약)
> **현실과 가상을 융합하는 몰입형 기술**. AR은 현실 위에 가상 정보, VR은 완전 가상 세계, MR은 둘의 혼합. XR(eXtended Reality)로 통칭.

## 1. 개념
- **AR (Augmented Reality, 증강 현실)**: 현실 세계에 가상 정보를 겹쳐 보여주는 기술
- **VR (Virtual Reality, 가상 현실)**: 완전히 가상의 3D 환경에 몰입하는 기술
- **MR (Mixed Reality, 혼합 현실)**: AR과 VR의 특징을 결합한 기술

> 비유: AR은 "정보 안경", VR은 "꿈의 세계", MR은 "마법의 세계"

## 2. 현실-가상 연속체

```
┌────────────────────────────────────────────────────────┐
│            현실-가상 연속체 (Reality-Virtuality        │
│                    Continuum)                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  현실        AR          MR          VR      가상      │
│  Reality                          Virtuality           │
│                                                        │
│  ●──────────●──────────●──────────●──────────●        │
│  │          │          │          │          │        │
│  │    현실에    현실+가상   가상+현실   완전 가상      │
│  │    정보    상호작용    융합        세계            │
│  │    추가                                       │        │
│  │          │          │          │          │        │
│  ▼          ▼          ▼          ▼          ▼        │
│                                                        │
│  예시:                                                  │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐  │
│  │실제     │포켓몬Go │홀로렌즈 │Meta     │완전    │  │
│  │세계     │         │         │Quest    │가상    │  │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 각 기술 비교

```
┌────────────────────────────────────────────────────────┐
│                  AR / VR / MR 비교                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  AR (증강 현실):                                       │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 현실 세계 + 디지털 정보 오버레이             │   │
│  │ • 스마트폰, 태블릿, 스마트글래스               │   │
│  │ • 예: 포켓몬Go, IKEA Place, 내비게이션        │   │
│  │ • 기술: SLAM, 마커 인식, GPS                   │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  VR (가상 현실):                                       │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 완전한 가상 환경 몰입                         │   │
│  │ • HMD (Head Mounted Display) 필수              │   │
│  │ • 예: Meta Quest, PlayStation VR, HTC Vive     │   │
│  │ • 기술: 3D 렌더링, 헤드 트래킹, 컨트롤러       │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  MR (혼합 현실):                                       │
│  ┌────────────────────────────────────────────────┐   │
│  │ • 현실과 가상의 상호작용                        │   │
│  │ • 가상 객체가 현실과 상호작용                   │   │
│  │ • 예: Microsoft HoloLens, Apple Vision Pro    │   │
│  │ • 기술: 공간 매핑, 제스처 인식, 시선 추적      │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘

비교표:
┌─────────────┬───────────┬───────────┬───────────┐
│    구분      │    AR     │    VR     │    MR     │
├─────────────┼───────────┼───────────┼───────────┤
│ 환경        │ 현실+가상 │ 가상만    │ 현실+가상 │
│ 몰입도      │ 낮음      │ 높음      │ 중간      │
│ 장비        │ 폰/글래스 │ HMD       │ HMD       │
│ 현실감지    │ O         │ X         │ O         │
│ 상호작용    │ 제한적    │ 완전      │ 완전      │
└─────────────┴───────────┴───────────┴───────────┘
```

## 4. 핵심 기술

```
┌────────────────────────────────────────────────────────┐
│                  XR 핵심 기술                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 디스플레이 기술                                    │
│     - HMD (Head Mounted Display)                      │
│     - 광학 시스루 (Optical See-Through)               │
│     - 비디오 시스루 (Video See-Through)               │
│     - FOV (시야각), 해상도, 주사율                    │
│                                                        │
│  2. 트래킹 기술                                         │
│     - 6DoF (6 Degrees of Freedom)                     │
│       - 위치: X, Y, Z                                 │
│       - 회전: Roll, Pitch, Yaw                        │
│     - IMU (관성 측정 장치)                            │
│     - SLAM (Simultaneous Localization and Mapping)    │
│     - 인사이드아웃 vs 아웃사이드인                    │
│                                                        │
│  3. 렌더링 기술                                         │
│     - 실시간 3D 렌더링                                 │
│     - 지연 시간 < 20ms                                │
│     - 포토리얼리즘                                     │
│     - foveated rendering                              │
│                                                        │
│  4. 인터랙션 기술                                       │
│     - 제스처 인식                                      │
│     - 시선 추적 (Eye Tracking)                        │
│     - 음성 인식                                        │
│     - 햅틱 피드백                                      │
│                                                        │
│  5. 오디오 기술                                         │
│     - 공간 오디오 (Spatial Audio)                     │
│     - HRTF (Head-Related Transfer Function)          │
│     - 3D 사운드                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math

class RealityType(Enum):
    AR = "증강 현실"
    VR = "가상 현실"
    MR = "혼합 현실"

@dataclass
class Vector3:
    """3D 벡터"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance_to(self, other) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

@dataclass
class Quaternion:
    """쿼터니언 (회전)"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 1.0

@dataclass
class GameObject:
    """게임 오브젝트 (가상 객체)"""
    id: str
    name: str
    position: Vector3
    rotation: Quaternion
    scale: Vector3 = field(default_factory=lambda: Vector3(1, 1, 1))
    visible: bool = True

@dataclass
class HMD:
    """헤드 마운트 디스플레이"""
    name: str
    resolution: Tuple[int, int]  # (width, height)
    fov: int  # 시야각 (도)
    refresh_rate: int  # Hz

    position: Vector3 = field(default_factory=Vector3)
    rotation: Quaternion = field(default_factory=Quaternion)
    velocity: Vector3 = field(default_factory=Vector3)

class SLAMSystem:
    """SLAM 시스템 시뮬레이션"""

    def __init__(self):
        self.map_points: List[Vector3] = []
        self.camera_poses: List[Tuple[Vector3, Quaternion]] = []

    def update(self, position: Vector3, rotation: Quaternion):
        """위치 추적 업데이트"""
        self.camera_poses.append((position, rotation))
        # 실제로는 특징점 추출, 매칭 등 수행

    def get_position(self) -> Vector3:
        """현재 위치 반환"""
        if self.camera_poses:
            return self.camera_poses[-1][0]
        return Vector3()

class XRDevice:
    """XR 디바이스 시뮬레이션"""

    def __init__(self, hmd: HMD, reality_type: RealityType):
        self.hmd = hmd
        self.reality_type = reality_type
        self.slam = SLAMSystem()
        self.virtual_objects: Dict[str, GameObject] = {}
        self.controllers: List[Vector3] = []

    def update_head_pose(self, position: Vector3, rotation: Quaternion):
        """헤드 포즈 업데이트"""
        self.hmd.position = position
        self.hmd.rotation = rotation
        self.slam.update(position, rotation)

    def spawn_object(self, name: str, position: Vector3) -> GameObject:
        """가상 객체 생성"""
        obj = GameObject(
            id=f"obj_{len(self.virtual_objects)}",
            name=name,
            position=position,
            rotation=Quaternion()
        )
        self.virtual_objects[obj.id] = obj
        print(f"[{self.reality_type.value}] 객체 생성: {name} at ({position.x:.1f}, {position.y:.1f}, {position.z:.1f})")
        return obj

    def raycast(self, origin: Vector3, direction: Vector3) -> Optional[GameObject]:
        """레이캐스팅 (객체 선택)"""
        closest_obj = None
        closest_dist = float('inf')

        for obj in self.virtual_objects.values():
            if not obj.visible:
                continue
            dist = origin.distance_to(obj.position)
            if dist < closest_dist and dist < 5.0:  # 5m 이내
                closest_dist = dist
                closest_obj = obj

        return closest_obj

    def render(self):
        """렌더링 (시뮬레이션)"""
        visible_count = sum(1 for obj in self.virtual_objects.values() if obj.visible)
        print(f"[{self.hmd.name}] 렌더링: {visible_count}개 객체, "
              f"위치: ({self.hmd.position.x:.1f}, {self.hmd.position.y:.1f}, {self.hmd.position.z:.1f})")


# 사용 예시
print("=== XR 시스템 시뮬레이션 ===\n")

# AR 디바이스
ar_hmd = HMD("Smart Glasses", (1920, 1080), 40, 60)
ar_device = XRDevice(ar_hmd, RealityType.AR)

# VR 디바이스
vr_hmd = HMD("Meta Quest 3", (4096, 2160), 110, 120)
vr_device = XRDevice(vr_hmd, RealityType.VR)

# AR 시나리오
print("--- AR 시나리오 ---")
ar_device.update_head_pose(Vector3(0, 1.7, 0), Quaternion())
ar_device.spawn_object("내비게이션 화살표", Vector3(0, 1.5, -2))
ar_device.spawn_object("상점 정보", Vector3(3, 1.5, 0))
ar_device.render()

# VR 시나리오
print("\n--- VR 시나리오 ---")
vr_device.update_head_pose(Vector3(0, 1.7, 0), Quaternion())
vr_device.spawn_object("가상 회의실", Vector3(0, 0, -5))
vr_device.spawn_object("3D 화이트보드", Vector3(-2, 1.5, -4))
vr_device.render()

# 레이캐스팅
print("\n--- 객체 선택 ---")
hit = ar_device.raycast(Vector3(0, 1.7, 0), Vector3(0, 0, -1))
if hit:
    print(f"선택된 객체: {hit.name}")
