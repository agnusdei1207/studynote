---
title: "Container Runtime Sandboxing Gvisor Kata Containers"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기본 컨테이너(runc)는 호스트 커널을 공유하므로 <strong>커널 취약점을 통한 컨테이너 탈출(Container Escape)</strong> 위험이 있다. 샌드박싱 런타임은 <strong>커널 접근을 차단하는 추가 격리 계층</strong>을 삽입하여 보안을 강화한다.
> 2. **가치**: gVisor는 <strong>유저 스페이스 커널(Sentry)</strong>로 시스콜을 중간 차단하고, Kata Containers는 <strong>경량 VM 안에 컨테이너를 격리</strong>하여, 멀티테넌트 환경에서 <strong>워크로드 간 완벽 격리</strong>를 달성한다.
> 3. **판단 포인트**: gVisor는 <strong>시스콜 호환성 제한+성능 오버헤드 5~15%</strong>, Kata는 <strong>VM 부팅 지연+메모리 오버헤드</strong>라는 트레이드오프가 있으며, <strong>신뢰할 수 없는 코드(CI Runner, FaaS)</strong> 실행 시 도입을 검토한다.

---

## Ⅰ. 개요 및 필요성

기본 컨테이너 런타임(runc)은 Namespace·cgroups로 프로세스를 격리하지만, <strong>호스트 커널을 직접 공유</strong>한다. 커널에 제로데이 취약점이 발생하면 컨테이너 안의 악성 코드가 호스트 전체를 장악할 수 있다(Container Escape).

```text
+-------------------------------------------------------+
|      런타임별 격리 수준 비교                            |
+-------------------------------------------------------+
|  [runc (기본)]                                        |
|   Container --syscall---> Host Kernel (직접 접근 ⚠️)  |
|                                                       |
|  [gVisor (runsc)]                                     |
|   Container --syscall---> Sentry(유저커널) ---> Kernel  |
|   시스콜 중간 차단, 200+개만 허용                     |
|                                                       |
|  [Kata Containers]                                    |
|   Container ---> [경량 VM (QEMU/Firecracker)]         |
|                      +---> Guest Kernel ---> Host      |
|   완전한 커널 격리, VM 수준 보안                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: runc는 사무실 칸막이(넘어가기 쉬움), gVisor는 유리벽(보이지만 못 넘어감), Kata는 별도 건물(완전 분리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 런타임 | 격리 방식 | 커널 공유 | 성능 오버헤드 | 호환성 |
|:---|:---|:---|:---|:---|
| <strong>runc</strong> | Namespace+cgroups | 공유 | 거의 없음 | 100% |
| **gVisor** | 유저 스페이스 커널 (Sentry) | **차단** | 5~15% | 제한 (200+ syscall) |
| **Kata** | 경량 VM (Firecracker) | <strong>게스트 커널</strong> | 부팅 지연+메모리 | 높음 |

### gVisor 동작 원리
앱이 `open()` 시스콜을 호출하면, 호스트 커널에 직접 가지 않고 <strong>Sentry(유저 스페이스 커널)</strong>가 가로채어 검증 후 제한적으로 호스트에 전달한다. 악성 시스콜은 Sentry에서 차단된다.

- **📢 섹션 요약 비유**: gVisor는 회사 메일 시스템이다. 직원(컨테이너)이 외부에 메일(시스콜)을 보내면, 보안팀(Sentry)이 검열한 후 통과시킨다.

---

## Ⅲ. 비교 및 연결

| 비교 | 기본 컨테이너 | VM | gVisor | Kata |
|:---|:---|:---|:---|:---|
| **격리** | 약함 | 강함 | **중간~강함** | **강함 (VM급)** |
| <strong>성능</strong> | 최고 | 낮음 | 중간 | 중간 |
| **부팅** | ms | 수 초 | ms | **< 100ms (Firecracker)** |
| **밀도** | 최고 | 낮음 | 높음 | 중간 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도입 시나리오
1. <strong>CI/CD Runner</strong>: 사용자 제출 코드를 빌드 -> gVisor 격리로 악성 코드 차단.
2. <strong>FaaS (Lambda)</strong>: 멀티테넌트 함수 실행 -> Firecracker (Kata 기반) 격리.
3. **일반 워크로드**: 신뢰 가능한 내부 앱 -> runc 유지 (성능 우선).

### 안티패턴
- **모든 파드를 gVisor로 실행**: 시스콜 호환성 문제로 일부 앱 오작동 -> 신뢰도 높은 내부 앱에는 불필요.

---

## Ⅴ. 기대효과 및 결론

| 지표 | runc (기본) | gVisor / Kata | 개선 |
|:---|:---|:---|:---|
| 컨테이너 탈출 위험 | 높음 | **차단/격리** | 보안 강화 |
| 멀티테넌트 격리 | 약함 | **강함** | 규정 준수 |
| 성능 | 최고 | 5~15% 오버헤드 | 트레이드오프 |

컨테이너 샌드박싱은 Confidential Computing(기밀 컴퓨팅)과 결합하여 하드웨어 TEE(Trusted Execution Environment) 내에서 컨테이너를 실행하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>runc</strong> | OCI 표준 기본 컨테이너 런타임 |
| **gVisor (runsc)** | Google의 유저 스페이스 커널 샌드박스 |
| **Kata Containers** | 경량 VM 기반 컨테이너 격리 |
| **Firecracker** | AWS Lambda가 사용하는 마이크로VM |
| <strong>Container Escape</strong> | 샌드박싱이 방지하려는 공격 벡터 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Docker + runc (2013~) — 커널 공유 컨테이너 표준화]
    |
    v
[Container Escape 공격 증가 (2017~) — CVE-2019-5736 등]
    |
    v
[gVisor (2018, Google) — 유저 스페이스 커널 격리]
    |
    v
[Kata + Firecracker (2018~) — 경량 VM 격리]
    |
    v
[현재: Confidential Containers — 하드웨어 TEE + 컨테이너]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 보통 컨테이너(runc)는 교실 <strong>칸막이</strong>로 나뉜 거예요. 칸막이를 넘으면 옆 자리를 볼 수 있죠.
2. gVisor는 <strong>유리벽</strong>이에요. 보이지만 넘어갈 수 없어요.
3. Kata는 아예 <strong>다른 건물</strong>로 분리해서, 절대 옆 교실에 갈 수 없게 만든답니다!
