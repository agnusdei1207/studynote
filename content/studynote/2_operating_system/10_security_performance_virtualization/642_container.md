+++
title = "642. 컨테이너 (Container)"
date = "2026-03-16"
weight = 642
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "컨테이너", "Container", "Docker", "Kubernetes", "이미지", "오케스트레이션"]
+++

# 컨테이너 (Container)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너(Container)는 **운영체제 수준 가상화**로, **커널은 공유하면서 프로세스를 격리**하여 애플리케이션과 의존성을 패키징하는 기술이다.
> 2. **가치**: VM보다 가볍고 빠르며 **"Build once, run anywhere"**를 실현하여 DevOps, CI/CD, 마이크로서비스의 핵심 인프라가 되었다.
> 3. **융합**: Linux Namespace(pid, net, mount...), Cgroups, Union FS 등 커널 기술을 조합하며, Docker, Kubernetes 등 생태계가 발전했다.

+++

## Ⅰ. 컨테이너의 개요

### 1. 정의
- 컨테이너는 애플리케이션 코드와 실행 환경을 패키징하여 **어디서나 일관되게 실행**할 수 있는 격리된 실행 환경이다.
- **VM vs Container**: VM은 전체 OS 가상화, 컨테이너는 프로세스 격리만 수행

### 2. 등장 배경: "내 컴퓨터에서는 되는데?"
- 개발/테스트/운영 환경 차이로 발생하는 "works on my machine" 문제 해결
- 2013년 Docker 등장으로 대중화

### 3. 💡 비유: '도시락 반찬 통'
- 컨테이너는 **'반찬을 담은 도시락 통'**과 같다.
- 도시락(컨테이너)에는 밥, 반찬, 김치(애플리케이션+의존성)이 들어있고, 어디서나 꺼내 먹을 수 있다.

- **📢 섹션 요약 비유**: 이사할 때 짐을 박스에 포장해두면, 어디서든 꺼내서 바로 쓸 수 있죠? 컨테이너는 소프트웨어를 박스에 포장하는 기술입니다.

+++

## Ⅱ. 컨테이너 기술 기반 (Deep Dive)

### 1. Linux Namespace (격리)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │              Linux Namespace로 격리하는 자원                     │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Namespace]          [격리 대상]           [예시]               │
    │                                                                 │
    │   PID Namespace      프로세스 ID         컨테이너 내에서 PID=1  │
    │   NET Namespace      네트워크            독립 네트워크 스택      │
    │   MNT Namespace      파일 시스템          독립 mount 지점        │
    │   UTS Namespace      호스트명            독립 hostname          │
    │   IPC Namespace      IPC                 메시지 큐 격리         │
    │   USER Namespace     사용자/그룹          Root 권한 분리        │
    │   CGROUP Namespace   Cgroup              리소스 제어 격리       │
    │                                                                 │
    │  * 각 컨테이너는 자신만의 "우주"를 가짐                         │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Cgroups (Control Groups)
- **목적**: 프로세스 그룹의 **리소스(CPU, 메모리, I/O)를 제한하고 측정**
- **사용 예시**: 이 컨테이너는 CPU 2개, 메모리 1GB만 사용
```bash
# Cgroup v2 예시
# sys/fs/cgroup/mycontainer/
echo "1000000 > cpu.max"           # CPU 1코어 제한
echo "1G > memory.max"             # 메모리 1GB 제한
```

### 3. Union File System (Layered FS)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │            Union File System (OverlayFS) 계층 구조              │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Container Layer] (쓰기 가능)                                  │
    │   ┌───────────────────────────────────────────────┐            │
    │   │ /app/config.yml (수정됨)                    │            │
    │   │ /tmp/logs/                                   │            │
    │   └───────────────────────────────────────────────┘            │
    │                        │                                        │
    │   │        ┌───────────┴───────────┐                           │
    │   ▼        ▼                       ▼                           │
    │  [Image Layers] (읽기 전용, 공유)                            │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
    │   │ Layer 3  │  │ Layer 2  │  │ Layer 1  │                   │
    │   │(App/Code)│  │(Runtime) │  │  (Base)  │                   │
    │   │ nginx    │  │ debian   │  │  OS libs │                   │
    │   └──────────┘  └──────────┘  └──────────┘                   │
    │                                                                 │
    │  * 수정 시 최상위 레이어(Copy-on-Write)에만 기록               │
    │  * 이미지는 여러 컨테이너가 공유                              │
    └─────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Namespace는 "각자의 방", Cgroups는 "방마다 전기/수도 사용량 제한", Union FS는 "공용 주방 + 각자 냉장고"와 같습니다.

+++

## Ⅲ. Docker

### 1. Docker 핵심 개념
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                   Docker 핵심 컴포넌트                           │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Image]                                                        │
    │   - 읽기 전용 템플릿                                           │
    │   - Layered 파일 시스템                                         │
    │   - Dockerfile으로 빌드                                         │
    │                                                                 │
    │  [Container]                                                    │
    │   - Image의 실행 인스턴스                                        │
    │   - 쓰기 가능 레이어 추가                                        │
    │                                                                 │
    │  [Dockerfile]                                                  │
    │   - Image 빌드 명령어                                           │
    │   - FROM, RUN, COPY, CMD, EXPOSE...                            │
    │                                                                 │
    │  [Registry]                                                    │
    │   - Image 저장소 (Docker Hub, ECR, GCR)                        │
    │                                                                 │
    │  [Docker Engine]                                               │
    │   - dockerd (데몬), containerd, runc                            │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Docker 명령어
```bash
# 이미지 빌드
docker build -t myapp:1.0 .

# 컨테이너 실행
docker run -d -p 80:80 --name web myapp:1.0

# 컨테이너 목록
docker ps -a

# 로그 확인
docker logs web

# 컨테이너 진입
docker exec -it web bash

# 이미지 푸시
docker push myrepo/myapp:1.0
```

+++

## Ⅳ. 컨테이너 오케스트레이션

### 1. Kubernetes (K8s)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │               Kubernetes 아키텍처 (간소화)                       │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Control Plane]                                                │
    │   ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
    │   │API      │  │Scheduler│  │Controller│                      │
    │   │Server   │  │         │  │Manager   │                      │
    │   └────┬────┘  └─────────┘  └─────────┘                      │
    │        │                                                       │
    │        │ etcd (설정 저장소)                                     │
    │        │                                                       │
    │        ▼                                                       │
    │  [Worker Nodes]                                                │
    │   ┌───────────────────────────────────────────────┐            │
    │   │ Pod1 │ Pod2 │ Pod3 │          │ PodN       │            │
    │   │(Web) │(API) │(DB)  │          │(Worker)    │            │
    │   └───────────────────────────────────────────────┘            │
    │   │ kubelet │ kube-proxy │ Container Runtime │               │
    │                                                                 │
    │  [K8s 주요 개념]                                              │
    │   - Pod: 최소 배포 단위 (1개 이상 컨테이너)                     │
    │   - Service: Pod들의 안정된 엔드포인트                          │
    │   - Deployment: Pod 배포/업데이트 관리                         │
    │   - Ingress: 외부 트래픽 라우팅                                │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. K8s vs Docker Swarm
| 비교 항목 | Kubernetes | Docker Swarm |
|:---|:---|:---|
| **복잡도** | 높음 (학습 곡선 가파름) | 낮음 |
| **확장성** | 매우 큰 규모 | 소규모~중규모 |
| **기능** | 풍부 (Auto-scaling, RBAC...) | 기본적 |
| **시장 점유율** | 표준 (CNCF) | 감소 |

+++

## Ⅴ. 컨테이너 vs VM

| 비교 항목 | VM (Virtual Machine) | Container |
|:---|:---|:---|
| **격리 레벨** | 하드웨어 수준 (전체 OS) | 프로세스 수준 |
| **용량** | GB 단위 (OS 포함) | MB 단위 (앱만) |
| **시작 시간** | 분 단위 | 초 단위 |
| **성능** | 오버헤드 있음 | 거의 네이티브 |
| **이식성** | 플랫폼 의존적 | 플랫폼 독립적 |
| **용도** | 완전한 격리 필요 시 | 앱 배포, 마이크로서비스 |

+++

## Ⅵ. 실무 적용 및 아키텍처적 판단 (Strategy)

### 1. 모범 사례
1. **One Process Per Container**: 관계 없는 프로세스 분리
2. **Immutable Infrastructure**: 변경 시 새 이미지 빌드 (실행 중 수정 X)
3. **Minimal Base Image**: alpine, distroless 사용
4. **Secrets Management**: 환경 변수 대신 Kubernetes Secret 사용
5. **Resource Limits**: CPU/Memory 제한 필수

### 2. 안티패턴
- **"Fat Container"**: 너무 많은 것을 하나에
- **"Latest Tag"**: 이미지 버전 고정 안 함
- **"Root 실행"**: 보안 위험
- **"Sensitive Data in Image"**: 비밀번호 등 이미지에 포함

### 3. 보안 고려사항
- **Image Scanning**: Trivy, Clair로 취약점 스캔
- **Rootless Containers**: rootless 컨테이너 실행
- **Runtime Security**: Falco로 런타임 보안

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **배포 속도**: 주 → 분 단위
- **리소스 효율**: VM 대비 2~3배 더 많은 앱 실행
- **DevOps 통합**: CI/CD 파이프라인 자연스러운 통합

### 2. 미래 전망
- **WebAssembly**: 더 가벼운 실행 형식
- **Serverless Containers**: AWS Fargate, GCP Run
- **eBPF**: 커널 수준 관찰 가능성과 보안

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **가상화**: 상위 개념
- **마이크로서비스**: 컨테이너 주요 용도
- **Docker**: 컨테이너 플랫폼
- **Kubernetes**: 오케스트레이션

+++

## 👶 어린이를 위한 3줄 비유 설명
1. 컨테이너는 **'도시락 반찬 통'** 같아요.
2. 밥, 반찬, 김치를 한 통에 담아두면 어디서든 꺼내 먹을 수 있죠?
3. 각자 통을 가지고 있어서 섞이지도 않고, 원하는 반찬만 싸서 다닐 수 있어요!