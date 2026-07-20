---
title: "OverlayFS"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
weight: 64
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Root Filesystem은 시스템이 부팅된 직후 `/` 아래에 붙는 기본 파일 시스템이고, OverlayFS는 읽기 전용 계층 위에 쓰기 계층을 얹는 union mount 방식이다.
> 2. **가치**: OverlayFS는 컨테이너 이미지의 read-only layer와 writable layer를 분리해 복사 비용을 줄이고 immutable image 개념을 실현한다.
> 3. **판단**: 부팅 경로와 컨테이너 런타임 경로를 함께 이해해야 rootfs와 overlayfs를 정확히 설명할 수 있다.

---

## Ⅰ. 개요 및 필요성

리눅스는 부팅 직후 커널이 사용할 루트 디렉터리가 필요하다. 이것이 rootfs다. 여기에 파일 시스템을 마운트해야 비로소 사용자 공간이 본격적으로 시작된다.

OverlayFS는 이 루트 위에 읽기 전용 계층과 쓰기 계층을 겹쳐, "원본은 그대로 두고 변경만 따로 저장"하는 구조를 만든다.

- **📢 섹션 요약 비유**: 책 본문은 그대로 두고, 그 위에 투명한 메모지를 덧댄 뒤 수정사항만 적는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
lowerdir (read-only)
  v
overlayfs
  ^
upperdir (writable)
  v
merged view
```

| 구성 요소 | 역할 |
| :-- | :-- |
| lowerdir | 원본 읽기 전용 계층 |
| upperdir | 변경을 저장하는 쓰기 계층 |
| workdir | OverlayFS 내부 작업 공간 |
| merged | 사용자에게 보이는 통합 뷰 |

rootfs는 시스템이 살아남기 위한 최소 파일 집합을 제공하고, OverlayFS는 여러 계층을 하나처럼 보이게 만든다. 컨테이너 이미지가 가볍고 재사용 가능한 이유가 여기 있다.

- **📢 섹션 요약 비유**: 같은 책을 여러 사람이 읽어도, 각자 필기한 부분은 자기 종이 위에만 남는 구조다.

---

## Ⅲ. 비교 및 연결

| 구분 | RootFS | OverlayFS | Initramfs |
| :-- | :-- | :-- | :-- |
| 역할 | 루트 디렉터리 기반 | 계층 결합 | 임시 부트 환경 |
| 시점 | 부팅 초기 | 런타임/이미지 | 부팅 직후 |
| 특징 | 필수 기반 | copy-on-write | 초기 장치 로드 |

OverlayFS는 도커와 같은 컨테이너 플랫폼에서 image layer와 writable layer를 분리하는 핵심 기술이다. rootfs와 혼동하면 "부팅용 루트"와 "컨테이너용 루트"가 섞이기 쉽다.

- **📢 섹션 요약 비유**: 기본 서랍장(rootfs) 위에 투명 서랍(overlayfs)을 얹어 새 물건만 따로 넣는 느낌이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 체크리스트

1. rootfs와 overlayfs의 역할을 구분하는가?
2. lowerdir/upperdir/workdir 구성을 이해하는가?
3. copy-on-write 동작을 설명할 수 있는가?
4. 컨테이너 이미지 계층 구조와 연결할 수 있는가?
5. immutable infrastructure와 관련지을 수 있는가?

### 안티패턴

- rootfs와 overlayfs를 같은 의미로 쓰는 설계
- 쓰기 계층과 읽기 전용 계층을 구분하지 않는 설계
- 부트 초기와 런타임 컨테이너 경로를 뒤섞는 설계
- copy-on-write 비용을 전혀 고려하지 않는 설계

실무 관점에서는 rootfs를 "부팅 개념", overlayfs를 "계층화 저장 개념"으로 분리해 설명해야 한다. 그래야 이미지·컨테이너·부팅을 한 번에 엮어 말할 수 있다.

- **📢 섹션 요약 비유**: 바닥판은 하나지만, 위에 얹는 칸막이로 공간을 여러 개처럼 쓰는 방식이다.

---

## Ⅴ. 기대효과 및 결론

OverlayFS 덕분에 컨테이너 이미지는 빠르게 배포되고, 변경은 최소화되며, 원본 계층은 보존된다. 이것이 현대 리눅스와 컨테이너의 중요한 효율 포인트다.

결론적으로 rootfs는 시작점이고, overlayfs는 그 위에 계층을 얹는 기술이다.

- **📢 섹션 요약 비유**: 책상은 그대로 두고, 위에 트레이만 바꿔 끼우는 것과 같다.

---

## 관련 개념 맵

```text
Boot Process
  v
RootFS
  v
Mount / OverlayFS
  v
Container Image Layer
```

---

## 관련 키워드 및 발전 흐름도

```text
rootfs
  v
overlayfs
  v
copy-on-write
  v
container layers
```

---

## 어린이를 위한 3줄 비유 설명

바닥판이 있어야 집을 시작할 수 있어요.
위에 얇은 칸막이를 얹으면 새 방처럼 보일 수 있어요.
오버레이 파일 시스템은 그런 겹치기 방법이에요.
