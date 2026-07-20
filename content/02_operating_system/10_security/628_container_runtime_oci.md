---
title: "Container Runtime Oci"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 628
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 과거 도커(Docker)라는 단일 거대 소프트웨어가 독점하던 컨테이너 생태계는, 기술의 발전과 함께 '이미지 포맷'과 '실행 엔진'을 분리하여 개방형 표준으로 정의하는 <strong>OCI (Open Container Initiative)</strong> 규격으로 파편화 및 표준화되었다.
> 2. **계층화**: 이 표준화에 따라 컨테이너 런타임은 고수준 런타임(containerd, CRI-O - 이미지 풀링, 네트워크 관리)과 저수준 런타임(runc - 실제 리눅스 namespace와 cgroup을 조작하여 프로세스 생성)으로 계층이 명확히 분리되었다.
> 3. **가치**: OCI 표준화 덕분에 쿠버네티스(Kubernetes)는 무거운 Docker 엔진(dockerd)을 버리고 containerd나 CRI-O와 직접 통신(CRI)할 수 있게 되었으며, gVisor나 Kata Containers 같은 강력한 보안 샌드박스 런타임을 `runc` 대신 손쉽게 끼워 넣을 수 있는 플러그인 생태계가 완성되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>OCI (Open Container Initiative)</strong>: 리눅스 재단 산하에서 컨테이너의 이미지 포맷(Image Spec)과 런타임 실행 방식(Runtime Spec)을 정의한 산업 표준이다.
  - <strong>컨테이너 런타임</strong>: OCI 규격에 맞춰 실제로 컨테이너를 생성하고 실행하는 소프트웨어. 역할에 따라 고수준(High-level)과 저수준(Low-level)으로 나뉜다.
  - <strong>runc</strong>: OCI Runtime Spec을 구현한 가장 대표적인 저수준 런타임으로, 커널과 직접 맞닿아 컨테이너를 띄우는 핵심 CLI 도구다.
  - **containerd**: OCI Image Spec을 관리하고 `runc`를 제어하는 고수준 런타임 데몬이다.

- <strong>필요성 (도커 독점의 폐해와 쿠버네티스의 독립)</strong>:
  - 초기 컨테이너 시장은 Docker가 천하통일했다. 쿠버네티스(K8s)도 컨테이너를 띄우려면 무조건 Docker 데몬(dockerd)을 거쳐야 했다.
  - 그러나 K8s 입장에서 Docker는 볼륨 관리, 스웜(Swarm), 빌드 등 불필요한 기능이 너무 많은 '무거운 뚱보'였다. 게다가 Docker가 업데이트될 때마다 K8s 호환성이 깨지는 문제가 발생했다.
  - 이를 해결하기 위해 업계는 Docker의 핵심 부품(runc, containerd)을 적출하여 오픈소스로 기증하고, 누구든 이 규격(OCI)만 맞추면 컨테이너 엔진을 만들 수 있도록 표준화(Democratization)했다.

- **발전 과정**:
  1. **모놀리식 시대 (2013년)**: Docker 단일 데몬(dockerd)이 모든 것을 처리. LXC(LinuX Containers) 의존.
  2. <strong>OCI 설립 및 runc 기증 (2015년)</strong>: Docker사가 핵심 실행 모듈(libcontainer)을 `runc`로 분리하여 OCI에 기증.
  3. <strong>CRI와 Docker Shim (2016년)</strong>: K8s가 런타임을 골라 쓰기 위해 CRI(Container Runtime Interface) 도입. Docker는 CRI를 미지원해 중간 번역기(Dockershim) 사용.
  4. **Docker의 완전 분해 (현재)**: K8s에서 Dockershim이 완전 퇴출(Deprecation)되고, containerd나 CRI-O가 K8s의 표준 고수준 런타임으로 직결됨.

- **📢 섹션 요약 비유**: 종합 선물 세트(Docker)에서 우리가 진짜 먹고 싶었던 알맹이(runc, containerd)만 빼내어, 누구나 쉽게 레고 블록처럼 조립할 수 있게 만든 규격화의 승리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 컨테이너 생태계의 계층 구조 (Layered Architecture)

현재의 컨테이너 아키텍처는 명확한 역할 분담 체계를 갖는다.

| 계층 (Layer) | 구성 요소 (예시) | 주요 역할 | K8s 인터페이스 |
|:---|:---|:---|:---|
| **오케스트레이터** | Kubernetes (Kubelet) | 컨테이너 배치, 스케일링, 상태 복구 명령 하달 | - |
| **고수준 런타임** | containerd, CRI-O | 이미지 Pull/Push, 이미지 압축 해제, 네트워크(CNI) 연동, 저수준 런타임 호출 | **CRI** (Container Runtime Interface) |
| **저수준 런타임** | <strong>runc</strong>, gVisor (runsc), Kata | Namespace, Cgroups 설정, 실제 리눅스 프로세스(컨테이너) 격리 및 실행 | <strong>OCI Runtime Spec</strong> |
| <strong>운영체제 (OS)</strong> | Linux Kernel | 실제 리소스 격리 수행 및 하드웨어 자원 할당 | Syscall |

---

### OCI 런타임 스펙 (Runtime Spec)과 runc의 동작

`runc`는 데몬(Daemon)이 아니라, 실행 후 컨테이너를 띄우고 종료되는 단순한 CLI 바이너리다.

```text
  +-------------------------------------------------------------------+
  |                 runc 기반 저수준 컨테이너 생성 흐름                   |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  1. [containerd]                                                  |
  |     Docker Hub에서 이미지를 Pull 받고 압축을 풀어 디스크에 저장한다.       |
  |     (Rootfs 형태의 디렉터리로 구성)                                   |
  |            |                                                      |
  |            v                                                      |
  |  2. [config.json 생성 (OCI Spec)]                                 |
  |     containerd는 컨테이너가 어떻게 돌아야 하는지 명세서(JSON)를 만든다.    |
  |     (예: "네임스페이스는 이걸 쓰고, CPU 제한은 2코어로 해라")               |
  |            |                                                      |
  |            v                                                      |
  |  3. [runc 실행]  명령어: `runc create` 및 `runc start`              |
  |            |                                                      |
  |     +------v----------------------------------------+             |
  |     | runc 내부 동작 (Linux Kernel API 호출)           |             |
  |     | 1) unshare / clone  : 네임스페이스 분리 (격리 공간)|             |
  |     | 2) cgroups 파일 작성 : 자원 할당량(Limit) 설정     |             |
  |     | 3) pivot_root       : Root 파일시스템(경로) 변경 |             |
  |     | 4) seccomp / AppArmor : 보안 필터 적용           |             |
  |     +------+----------------------------------------+             |
  |            |                                                      |
  |            v                                                      |
  |  4. [컨테이너 프로세스(예: nginx) 실행 완료!]                           |
  |     * 띄운 직후 runc 프로세스 자체는 종료되고, nginx 프로세스만 남음.      |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** OCI 규격의 핵심은 `config.json`과 `rootfs`(루트 파일시스템) 디렉터리만 주어지면, 전 세계 어떤 런타임이든 똑같은 형태의 컨테이너를 만들어내야 한다는 것이다. `runc`는 이 규격을 리눅스 커널의 Namespace와 Cgroups API로 치환해 주는 가장 완벽한 번역기다. `runc`는 무거운 데몬이 아니므로 메모리를 상시 점유하지 않는다.

---

### Kubernetes의 CRI (Container Runtime Interface)

쿠버네티스의 에이전트인 `Kubelet`과 고수준 런타임(containerd)이 통신하는 gRPC 기반의 표준 API다.

```text
  +-------------------------------------------------------------------+
  |                 K8s CRI 아키텍처 (Dockershim 퇴출 이후)              |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ Kubelet ] (K8s 워커 노드 데몬)                                    |
  |       |                                                           |
  |       | (gRPC 통신 - CRI 표준 규격: RunPodSandbox, CreateContainer)|
  |       v                                                           |
  |  [ CRI 플러그인 ] (보통 containerd 내부에 내장됨)                       |
  |       |                                                           |
  |       v                                                           |
  |  [ containerd ] (고수준 런타임)                                      |
  |       |                                                           |
  |       | (containerd-shim 프로세스 생성)                             |
  |       v                                                           |
  |  [ runc ] (저수준 런타임) ----> [ Linux Kernel (Namespace/Cgroup) ]  |
  |                                       |                           |
  |                                       v                           |
  |                                [ Nginx 컨테이너 ]                   |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 과거에는 Kubelet과 containerd 사이에 무거운 Dockerd와 그 명령을 번역하는 Dockershim이 억지로 끼어 있었다. K8s 1.24 버전부터 이를 걷어내고, Kubelet이 CRI 규격을 통해 containerd와 직결통신하게 되었다. 이로써 K8s 클러스터의 메모리 사용량이 감소하고 파드(Pod) 생성 속도가 비약적으로 향상되었다.

- **📢 섹션 요약 비유**: 사장님(Kubelet)이 비서(Dockerd)를 거치지 않고, 표준화된 메신저(CRI)를 통해 바로 실무 부장(containerd)에게 지시를 내리게 된 결재 라인 단축입니다.

---

## Ⅲ. 비교 및 연결

### 런타임(Runtime) 종류별 비교

| 런타임 명칭 | 수준 / 역할 | 개발 주체 | 특징 |
|:---|:---|:---|:---|
| <strong>Docker 엔진</strong> | Full Stack (더 이상 K8s 표준 아님) | Docker Inc. | 빌드, 스웜, 볼륨 등 모든 기능 포함. 개발자 PC용으로 적합. |
| **containerd** | 고수준 (High-level) | CNCF | Docker에서 분리된 핵심 데몬. K8s의 사실상 표준(Defacto). |
| **CRI-O** | 고수준 (High-level) | Red Hat | K8s 전용으로 만들어진 초경량 런타임. (OpenShift 주력) |
| <strong>runc</strong> | 저수준 (Low-level) | OCI | 리눅스 커널 격리 기술을 직접 조작. 일반적 컨테이너 실행기. |
| **runsc (gVisor)** | 저수준 (보안 샌드박스) | Google | 유저 모드에서 커널(Syscall)을 에뮬레이션하여 강력한 격리 달성. |
| **Kata Containers**| 저수준 (마이크로 VM) | OpenStack 등 | 컨테이너마다 얇은 경량 가상머신(VM)을 띄워 하드웨어 레벨 격리. |

### 과목 융합 관점

- <strong>운영체제 (OS)</strong>: OCI 규격과 runc의 본질은 리눅스 커널이 제공하는 `Namespace` (가시성 격리)와 `Cgroups` (자원 할당 제한)의 복잡한 C API를, JSON 파일 하나(`config.json`)로 추상화한 인프라스트럭처로서의 소프트웨어 공학이다.
- <strong>보안 (Security)</strong>: runc가 커널을 직접 공유하는 한계(Container Breakout 취약점)를 극복하기 위해, OCI 스펙을 준수하면서도 내부적으로는 VM을 띄우는 Kata Containers나 시스템 콜을 가로채는 gVisor 등 보안 OCI 런타임으로 진화하는 촉매가 되었다.

- **📢 섹션 요약 비유**: 플러그 규격(OCI)이 똑같으니, 220V 콘센트(containerd)에 선풍기(runc)를 꽂든, 에어컨(Kata)을 꽂든, 히터(gVisor)를 꽂든 사용자는 전원만 켜면 되는 완벽한 호환성입니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오

1. <strong>시나리오 — K8s 클러스터의 도커 퇴출(Dockershim Deprecation) 마이그레이션</strong>: 운영 중인 K8s 클러스터 노드가 구버전 Docker 엔진 기반으로 돌고 있어, K8s 버전을 1.24 이상으로 올릴 때 워커 노드가 먹통이 될 위기.
   - **대응 (마이그레이션 플로우)**:
     1. 워커 노드에서 Docker 데몬을 중지하고 삭제.
     2. `containerd` 패키지를 설치하고 `/etc/containerd/config.toml`을 생성 (Systemd cgroup 드라이버 사용 설정 필수).
     3. Kubelet의 시작 파라미터(`--container-runtime=remote`, `--container-runtime-endpoint=unix:///run/containerd/containerd.sock`)를 containerd 소켓으로 변경하여 재시작.
     4. 이미지 빌드 작업(docker build)은 클러스터 내부 도커 데몬 대신, 런타임 독립적인 툴(Kaniko, Buildah)을 사용하여 CI/CD 파이프라인 개편.

2. <strong>시나리오 — 멀티 테넌트(Multi-tenant) 퍼블릭 클라우드 환경의 컨테이너 보안</strong>: 서로 모르는 A 회사와 B 회사의 컨테이너가 같은 워커 노드(VM)에 배치될 때, 일반 `runc`를 쓰면 커널 취약점 공격(Privilege Escalation) 시 A가 B의 데이터를 훔쳐볼 수 있다.
   - **설계 (RuntimeClass 적용)**: K8s 클러스터에 Kata Containers 또는 gVisor를 추가 설치한다. K8s에 `RuntimeClass` 리소스를 정의하여, 신뢰할 수 없는 외부 고객 워크로드 파드는 `runtimeClassName: gvisor`를 지정하게 한다. containerd는 이 파드를 띄울 때 `runc` 대신 `runsc`를 호출하여, 컨테이너마다 독립된 가상 커널을 할당함으로써 완벽한 보안 격리를 달성한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 K8s 컨테이너 런타임(Runtime) 선정 의사결정 플로우          |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [새로운 K8s 워커 노드 풀(Node Pool) 구축]                             |
  |                |                                                  |
  |                v                                                  |
  |      워크로드가 악의적일 수 있는 외부 사용자(Untrusted) 코드인가?            |
  |          +- 예 ------> [샌드박스 저수준 런타임 (Kata, gVisor) 적용]       |
  |          |            (성능 손실 5~10% 감수, 보안 극대화)               |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      K8s 배포판이 Red Hat OpenShift 인가?                           |
  |          +- 예 ------> [CRI-O + runc (Red Hat 네이티브 조합)]          |
  |          |                                                        |
  |          +- 아니오 ---> [containerd + runc (가장 범용적이고 안정적인 표준)]|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 현대 K8s 아키텍처 설계에서 런타임의 선택권은 전적으로 아키텍트에게 있다. 사내용 마이크로서비스는 가장 가볍고 빠른 `containerd + runc`가 정답이다. 반면 AWS Fargate, GCP Cloud Run처럼 고객이 올린 임의의 컨테이너를 내 서버에서 돌려야 하는 Serverless CaaS(Container as a Service) 비즈니스를 구축한다면 `Kata`나 `gVisor` 같은 OCI 호환 마이크로 VM 런타임이 법적/기술적 필수 방어막이다.

### 도입 체크리스트
- **Cgroup 매칭**: 리눅스 OS의 init 시스템(systemd)이 리소스를 관리하는데, runc가 cgroupfs를 쓰면 자원 관리자가 두 명이 되어 충돌(OOM Killer 오동작 등)이 난다. `containerd`의 설정에 `SystemdCgroup = true`가 켜져 있는지 반드시 확인해야 한다.
- **이미지 빌드 분리**: `containerd`는 `docker build`를 지원하지 않는다. 개발 조직이 `nerdctl`, `buildah` 또는 기존 Docker 데스크톱을 통해 OCI 호환 이미지를 레지스트리에 푸시하는 파이프라인이 정립되었는가?

- **📢 섹션 요약 비유**: 칼(Docker) 한 자루로 요리도 하고 나무도 깎던 시대에서, 요리용 식칼(containerd)과 조각칼(Kata/gVisor)을 용도에 맞게 바꿔 끼울 수 있는 스위스 아미 나이프(OCI) 시대로의 진화입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 모놀리식 Docker 엔진 (과거) | OCI 표준 기반 (containerd + runc) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | Kubelet ↔ 런타임 간 통신 오버헤드 큼 | CRI 기반 직접 통신 (Dockershim 제거) | Pod 시작 속도(Cold Start) **20% 단축** |
| **정량** | 노드당 데몬 메모리 풋프린트: 수백 MB | containerd 데몬: **수십 MB 내외** | 워커 노드 가용 리소스(Allocatable) 증가 |
| **정성** | 보안 이슈 발생 시 Docker 전체 패치 대기 | runc 등 타겟 모듈만 교체/업데이트 가능 | 클러스터 유지보수성 및 벤더 종속성(Lock-in) 탈피 |

### 미래 전망
- <strong>Wasm (WebAssembly) OCI 런타임의 부상</strong>: 컨테이너보다 100배 더 가볍고 빠르게 시작되는 WebAssembly 모듈을 K8s에서 돌리기 위해, `runwasi` 같은 Wasm 전용 저수준 런타임이 등장하고 있다. OCI 규격 덕분에 기존 K8s 아키텍처를 하나도 바꾸지 않고 Wasm 워크로드를 스케줄링할 수 있게 되었다.
- <strong>eBPF 기반의 런타임 최적화</strong>: 컨테이너 네트워킹과 보안 필터링(Seccomp)의 오버헤드를 줄이기 위해, 저수준 런타임이 eBPF 커널 프로그램을 직접 주입하여 네트워크 패킷과 시스템 콜을 O(1) 속도로 필터링하는 아키텍처가 표준화될 것이다.

### 결론
OCI 규격 표준화와 컨테이너 런타임의 계층 분리는, 한 기업(Docker)의 훌륭한 발명품이 전 세계 인프라의 '공공재 표준'으로 승화하는 가장 모범적인 오픈소스 진화 과정이다. `runc`와 `containerd`의 이해 없이 K8s를 운영하는 것은 자동차의 엔진 원리를 모른 채 운전대만 잡는 것과 같다. 이 구조적 이해는 트러블슈팅과 차세대 보안 아키텍처 도입의 핵심 열쇠가 된다.

- **📢 섹션 요약 비유**: 독점 기업의 철도망(Docker)을 국가 표준궤(OCI)로 통일하자, KTX(runc)든 화물열차(Kata)든 가리지 않고 자유롭게 달릴 수 있는 거대한 물류 네트워크(K8s)가 완성된 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 쉐도우 페이지 테이블 (Shadow Page Table) vs 확장 페이지 테이블 (EPT/NPT 하드웨어 보조) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| IOMMU (Input/Output MMU) 역할 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[IOMMU (Input/Output MMU) 역할]
    |
    v
[컨테이너 런타임 (runc, containerd) OCI 규격 표준화]
    |
    +---> [라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식]
    +---> [가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 '도커(Docker)'라는 하나의 큰 공장이 장난감(컨테이너) 포장부터 배달, 조립까지 전부 다 혼자서 했어요.
2. 그러다 공장이 너무 무거워지니까, 사람들이 'OCI'라는 조립 설명서(표준)를 만들고 일을 나눴어요.
3. 이제는 '컨테이너디(containerd)' 아저씨가 택배를 받아오면, '런씨(runc)'라는 조립 전문가가 설명서대로 1초 만에 장난감을 뚝딱 조립해 준답니다!
