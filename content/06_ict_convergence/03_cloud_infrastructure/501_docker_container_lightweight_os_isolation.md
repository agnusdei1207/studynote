---
title: "Docker Container Lightweight OS Isolation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 501
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 도커(Docker) 컨테이너는 Guest OS 없이 리눅스 커널의 Namespace와 cgroups(Control Groups)만으로 프로세스를 격리하여 VM 대비 극적으로 가볍다.
> 2. **가치**: 이미지 레이어 구조(Union FS)로 수 초 안에 환경을 재현하고, OCI(Open Container Initiative) 표준으로 어떤 런타임에서도 동일하게 실행된다.
> 3. **판단 포인트**: 컨테이너는 VM만큼 강한 격리를 제공하지 않으므로, 멀티 테넌트 고보안 환경에서는 VM 또는 마이크로VM(Firecracker)과 병행을 검토해야 한다.

---

## Ⅰ. 개요 및 필요성

<strong>VM(Virtual Machine) vs 컨테이너(Container)</strong>의 가장 큰 차이는 Guest OS 유무다. VM은 하이퍼바이저(Hypervisor) 위에 완전한 OS를 올리므로 격리 수준이 높지만 기동에 수 분, 이미지 크기는 GB 단위다. 반면 컨테이너는 호스트 OS 커널을 공유하므로 기동 시간 수 초, 이미지 크기 수십~수백 MB다.

<strong>컨테이너가 해결하는 문제</strong>:
- "내 컴퓨터에선 잘 되는데(Works on My Machine)" 문제 해소 -> 동일 이미지로 개발/스테이징/운영 환경 일치
- 밀집 배포: 동일 서버에 수십~수백 개의 컨테이너 동시 실행 -> 자원 활용률 향상
- 불변 인프라(Immutable Infrastructure)의 기반 단위

- **📢 섹션 요약 비유**: VM은 방을 통째로 빌리는 것이고, 컨테이너는 칸막이로 공간을 나눠 쓰는 코워킹 스페이스다. 칸막이가 벽보다 빨리 설치되고 비용도 저렴하지만, 방음은 덜하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**리눅스 격리 기술**:
- <strong>Namespace</strong>: PID, Network, Mount, IPC, UTS, User 네임스페이스로 프로세스별 독립적인 OS 뷰 제공
- <strong>cgroups(Control Groups)</strong>: CPU, 메모리, 디스크 I/O, 네트워크 대역폭을 컨테이너별로 제한

<strong>도커 이미지 레이어 구조(Union FS)</strong>:

```
+----------------------------------------+
|  Container Layer (읽기/쓰기, 임시)      |
+----------------------------------------+
|  App Layer (COPY ./app /app)           |
+----------------------------------------+
|  Dependency Layer (RUN pip install)    |
+----------------------------------------+
|  Base Image (python:3.11-slim)         |
+----------------------------------------+
  ※ 각 레이어는 읽기 전용, 공유 가능 -> 디스크 절약
```

| 구분 | VM | 컨테이너 |
|:---|:---|:---|
| 기동 시간 | 수 분 | 수 초 |
| 이미지 크기 | 수 GB | 수십~수백 MB |
| 커널 공유 | ✗ (독립 Guest OS) | ✓ (호스트 커널 공유) |
| 격리 수준 | 강함 (하드웨어 수준) | 보통 (프로세스 수준) |
| 이식성 | 낮음 | 높음 (OCI 표준) |

<strong>OCI(Open Container Initiative)</strong>: 컨테이너 이미지 포맷과 런타임 표준 정의. Docker 외 containerd, CRI-O 등 다양한 런타임이 OCI를 준수하여 상호 운용 가능.

- **📢 섹션 요약 비유**: 이미지 레이어는 빌딩 블록처럼 쌓인다. 공통 블록(Base Image)은 여럿이 공유하고, 내 앱 코드 블록만 따로 올린다. 공통 블록은 한 번만 저장하면 여러 앱이 나눠 쓴다.

---

## Ⅲ. 비교 및 연결

<strong>컨테이너 보안</strong>:
- **이미지 서명(Image Signing)**: Docker Content Trust(DCT), Cosign — 위변조된 이미지 실행 방지
- **취약점 스캐닝**: Trivy, Snyk — Dockerfile 빌드 시 알려진 CVE(Common Vulnerabilities and Exposures) 검출
- <strong>루트리스 컨테이너(Rootless Container)</strong>: Podman — root 권한 없이 실행하여 컨테이너 탈출(Escape) 위험 감소

<strong>컨테이너 vs 마이크로VM(Firecracker)</strong>:
AWS Lambda와 Fargate는 각 함수 실행을 Firecracker 마이크로VM으로 격리 -> 컨테이너 수준 속도 + VM 수준 보안 경계 달성.

- **📢 섹션 요약 비유**: 컨테이너 보안은 아파트 현관문 잠금장치다. 기본 잠금(Namespace 격리)만으론 부족할 수 있으니, CCTV(이미지 스캐닝)와 방문자 인증(이미지 서명)도 함께 갖춰야 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**심화 학습 판단 포인트**:
1. Namespace + cgroups 조합으로 격리를 기술적으로 설명할 수 있어야 한다.
2. 이미지 레이어 공유로 인한 디스크 효율성과 빌드 캐시 활용을 언급한다.
3. 보안 측면에서 컨테이너 이미지 서명과 취약점 스캐닝을 반드시 포함한다.

**실무 시나리오**: CI/CD 파이프라인에서 Dockerfile로 이미지를 빌드할 때, 멀티 스테이지 빌드(Multi-Stage Build)를 적용하면 최종 이미지에 컴파일러나 빌드 도구가 포함되지 않아 이미지 크기와 공격 표면(Attack Surface)을 동시에 줄인다. 예: Go 앱 빌드 이미지 1.2GB -> 최종 실행 이미지 15MB.

- **📢 섹션 요약 비유**: 멀티 스테이지 빌드는 케이크 만들기와 같다 — 오븐(빌드 환경)과 그릇(실행 환경)을 분리하면, 오븐은 손님 테이블에 올리지 않아도 된다.

---

## Ⅴ. 기대효과 및 결론

도커 컨테이너 기술을 도입하면:
- <strong>배포 일관성</strong>: 환경 차이로 인한 장애 80% 이상 감소 경험치
- **자원 효율**: 동일 서버에 VM 대비 5~10배 많은 인스턴스 실행
- <strong>CI/CD 가속</strong>: 이미지 레이어 캐시로 빌드 시간 단축
- **이식성**: OCI 표준으로 온프레미스 ↔ 멀티 클라우드 자유 이동

컨테이너는 현대 클라우드 네이티브(Cloud Native) 아키텍처의 기본 단위이며, Kubernetes, 서비스 메시, CI/CD 파이프라인 모두 컨테이너를 전제로 설계된다.

- **📢 섹션 요약 비유**: 컨테이너는 표준화된 화물 컨테이너(ISO 컨테이너)와 같다. 어떤 배, 트럭, 기차에 실어도 동일하게 운반된다 — 클라우드가 바뀌어도 앱은 동일하게 동작한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Kubernetes | Pod, 오케스트레이션, 클러스터 · 502 |
| OCI (Open Container Initiative) | 컨테이너 표준, containerd, CRI-O · 502 |
| 불변 인프라 (Immutable Infrastructure) | 이미지 교체, Configuration Drift · 504 |
| 서버리스 (Serverless) / FaaS | Firecracker, 마이크로VM · 503 |
| cgroups (Control Groups) | 자원 제한, Linux 커널 · 502 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Pod · 오케스트레이션] -> [도커 컨테이너 경량 OS 격리] -> [자원 제한 · Linux 커널]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컨테이너는 도시락 통 같아요 — 안에 뭐가 들었는지 다 정해져 있어서, 어디서든 같은 맛이에요.
2. 도시락 통(컨테이너)은 방(VM)보다 작고 가볍지만, 방만큼 완전히 분리되지는 않아요.
3. 같은 도시락 레시피(이미지)로 만들면, 친구 집에서도 우리 집에서도 동일하게 먹을 수 있어요.
