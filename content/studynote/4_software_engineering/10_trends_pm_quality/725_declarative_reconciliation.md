+++
title = "725. 선언적 인프라 상태 일치 루프"
date = "2026-03-15"
weight = 725
[extra]
categories = ["Software Engineering"]
tags = ["Infrastructure", "Declarative", "Reconciliation Loop", "Kubernetes", "Control Plane", "Desired State"]
+++

# 725. 선언적 인프라 상태 일치 루프

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템의 목표 상태(**Desired State**)를 선언만 하면, **Reconciliation Loop (상태 조정 루프)**가 현재 상태(**Actual State**)와 실시간으로 비교하여 차이를 자동 수정하는 **폐루프 제어(Closed-loop Control)** 메커니즘이다.
> 2. **메커니즘**: 단순한 스크립트 실행이 아닌, **Kubernetes (K8s)** Control Plane의 **Controller (컨트롤러)**가 수행하는 "관찰(Observation) → 분석(Diff) → 행동(Act)"의 무한 루프를 통해 **Idempotency (멱등성)**과 **Self-healing (자가 치유)**을 구현한다.
> 3. **가치**: 대규모 MSA (Microservice Architecture) 환경에서 인적 오류를 제거하고, 장애 발생 시 **RTO (Recovery Time Objective)**를 초 단위로 줄이며, **GitOps**와 결합하여 변경 불가능한(Immutable) 인프라를 운영할 수 있는 기반이 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**Declarative Infrastructure (선언적 인프라)**란 관리자가 "어떻게(How)" 실행할지 절차를 나열하는 것이 아니라, "무엇(What)"을 원하는지 최종 상태만 기술하면 시스템이 스스로 그 상태로 수렴하도록 만드는 패러다임입니다. 이때 핵심적인 동력이 되는 것이 **State Reconciliation Loop (상태 조정 루프)**입니다.
이는 제어 이론(Control Theory)의 **피드백 루프(Feedback Loop)**에서 기원했으며, 분산 시스템의 복잡성을 줄이기 위해 **Level Triggered (레벨 트리거)** 방식, 즉 상태의 차이가 존재하는 한 계속해서 조정을 가하는 방식을 채택합니다.

#### 2. 배경: Imperative(명령형)의 한계
전통적인 **Imperative (명령형)** 스크립트(예: Shell, Ansible Ad-hoc)는 순차적 실행을 전제로 합니다. 스크립트 중간에 네트워크 단절이 발생하거나 리소스 부족으로 명령이 실패했을 때, 시스템은 '롤백(Rollback)'되지 않은 일관성 없는 상태가 됩니다. 또한, 수동으로 장애 복구를 시도하는 과정에서 **Configuration Drift (구성 표류)**가 발생하여 실제 운영 환경과 문서화된 상태가 달라지는 심각한 문제를 야기합니다.

#### 3. 등장 배경 및 변천
① **수동 운영의 한계**: 서버 수가 수백 대를 넘어가면서 사람에 의한 결정론적 운영이 불가능해짐  
② **클라우드의 가변성**: 인스턴스의 수명이 짧아지고(Cattle vs Pet), 자동으로 교체되는 환경 등장  
③ **선언형 시스템의 등장**: **Kubernetes**와 같은 시스템이 API를 통해 원하는 상태를 받아들이고, 내부적인 루프를 통해 이를 지속적으로 유지하려는 시스템이 표준으로 자리 잡음

#### 4. 동작 흐름 개요도

```text
┌───────────────────[ 선언적 인프라의 사이클 ]───────────────────┐
│                                                              │
│   [관리자/Admin]                                              │
│      │                                                       │
│      │ "Replica 3을 원해" (Desired State 선언)                │
│      ▼                                                       │
│   [API Server] ────(저장)───▶ [Etcd (Config Store)]          │
│      │                                                       │
│      │ (변경 감지)                                            │
│      ▼                                                       │
│   ┌─────────────────────────────────────┐                   │
│   │     Reconciliation Loop (Controller)│ ◀── 무한 반복      │
│   │                                     │                   │
│   │  1. Watch : API 변경 감지            │                   │
│   │  2. Diff : Actual vs Desired 비교    │                   │
│   │  3. Sync : 차이가 있으면 조치 실행    │                   │
│   └─────────────────────────────────────┘                   │
│      │                                                       │
│      │ (API 호출 조치)                                        │
│      ▼                                                       │
│   [Cluster (Kubelet/Daemon)]                                 │
│      │                                                       │
│      └──────(현재 상태 Actual State 피드백)──────────────────┘
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
> 마치 택배 기사가 목적지 주소만 입력하면 내비게이션이 **실시간 교통 상황(Actual State)**을 보며 **최적 경로(Desired State)**로 계속 수정해주는 것과 같습니다. 운전자(관리자)가 핸들을 직접 꺾지 않아도, 내비게이션(Reconciliation Loop)이 알아서 목적지로 인도합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 상세 구성 요소 (Component Analysis)

| 요소명 | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/기술 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **API Server** | 상태 선언의 입구 | 사용자의 YAML 선언을 검증하고 **Etcd**에 저장. **Watch API**를 통해 컨트롤러에게 이벤트를 전파. | HTTP/gRPC, REST | 주문 접수 데스크 |
| **Controller** | 루프의 뇌 (Brain) | **Informer(Shared Informer)**를 통해 캐싱된 상태를 감시. **WorkQueue**를 통해 이벤트를 처리하며 **Reconcile()** 로직 실행. | Go Interface, Client-go | 현장 감독관 |
| **Etcd** | 단일 진실 공급원 | 시스템의 모든 상태 데이터를 **KV Store** 형태로 보관. **Strong Consistency** (강한 일관성) 보장. | RAFT 알고리즘 | 설계 도면 금고 |
| **Actuator** | 실제 조치자 | Controller의 지시를 받아 실제 인프라(VM, Pod, Network)에 CRUD 명령을 수행. | CRI, CNI, CSI | 작업 인부 |

#### 2. Reconciliation Loop (조정 루프) 심층 분석

이 루프는 **Event Driven (이벤트 기반)**으로 동작하며, **Optimistic Concurrency Control (낙관적 동시성 제어)** 방식을 사용하여 충돌을 방지합니다.

**[핵심 동작 원리]**
1. **Observe (관찰)**: Controller가 **Informer**를 통해 API Server의 **Desired State** 변경과 현재 클러스터의 **Actual State**를 감시.
2. **Diff (분석)**: `State == Desired` 인지 확인. 만약 **`State != Desired`**라면, 무엇이 부족하거나(Add) 삭제되어야(Remove) 하는지 연산.
3. **Act (실��行)**: API Server를 통해 생성/수정/삭제 명령(Patch)을 전송. 실패 시 **Exponential Backoff (지수 백오프)** 정책에 따라 재시도.

#### 3. 루프 구조 및 데이터 흐름도 (ASCII)

```text
     [ The Control Loop: Desired State <-> Actual State ]

     Desired State (Spec)                 Actual State (Status)
 ┌─────────────────────┐             ┌─────────────────────┐
 │  (YAML Manifest)    │             │  (Kubelet / Cloud)  │
 │                     │             │                     │
 │  replicas: 3        │             │  [Pod-A] (Running)  │◀───┐
 │  image: nginx:1.23  │             │  [Pod-B] (Running)  │    │
 │                     │             │  [Pod-C] (Pending)  │    │
 └─────────┬───────────┘             └──────────┬──────────┘    │
           │                                    │               │
           ▼ (Watch)                            │ (Sync Status)  │
 ┌───────────────────────────────┐             │               │
 │        Controller Manager     │─────────────┘               │
 │ ┌───────────────────────────┐ │                           │
 │ │   Reconciliation Logic     │ │                           │
 │ │                           │ │                           │
 │ │  if (len(pods) != 3) {    │ │                           │
 │ │      create_pod();        │ │                           │
 │ │  }                        │ │                           │
 │ └───────────────────────────┘ │                           │
 └───────────────┬───────────────┘                           │
                 │ (API Call: Create/Patch)                   │
                 │                                            │
                 └────────────────────────────────────────────┘
                         (Loop continues forever)
```

#### 4. 핵심 코드 로직 (Pseudo-Code)

```go
// Kubernetes Controller의 전형적인 Reconcile 로직
func (r *Reconciler) Reconcile(ctx context.Context, req Request) (Result, error) {
    // 1. Observe: 현재 상태 조회 (CRUD Read)
    currentObj, err := r.Client.Get(ctx, req.NamespacedName)
    if err != nil {
        // 객체가 없으면 생성 필요
        return Result{Requeue: true}, nil 
    }

    // 2. Diff: 희망 상태(Spec)와 현재 상태(Status) 비교
    diff := currentObj.Spec.Replicas - currentObj.Status.AvailableReplicas
    
    // 3. Act: 상태가 다르면 조치 취하기
    if diff == 0 {
        // 상태 일치 -> 할 일 없음 (Peace)
        return Result{}, nil
    }

    // 상태 불일치 -> API에 조치 요청 (Create/Delete/Update)
    // 업데이트 성공 시 다음 루프에서 다시 확인
    
    return Result{RequeueAfter: 10 * time.Second}, nil
}
```

#### 5. 고급 기술적 특성
- **Level Triggered**: 상태가 "변경되었다(Edge Triggered)"는 신호가 아니라, **"현재 상태가 3이 아니다"**라는 상태 레벨 자체를 계속 감시. 따라서 메시지를 유실해도 상태가 일치할 때까지 계속 시도하여 **안정성(Safety)**을 보장.
- **Idempotency (멱등성)**: 동일한 명령을 여러 번 실행해도 결과가 1번 실행한 것과 동일함.

#### 📢 섹션 요약 비유
> 자동 온도 조절기(Thermostat)와 같습니다. 온도가 24도가 아니라는 **'상태'**를 감지하는 한, 전원을 켜는 명령을 몇 번이고 반복하여 결국 설정된 온도로 만듭니다. 중간에 전기가 잠시 끊겨도 다시 켜지면 온도를 확인하고 다시 팬을 돌리기 시작합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 명령형(Imperative) vs 선언적(Declarative) 비교 분석

| 비교 항목 | 명령형 (Imperative) | 선언적 (Declarative) | 비고 (Reasoning) |
|:---|:---|:---|:---|
| **관점** | 프로세스 (How) | 상태 (What) | '절차' 중심 vs '목표' 중심 |
| **코드 예시** | `docker run -d -p 80:80 nginx` | `replicas: 3; image: nginx` | |
| **장애 복구** | 스크립트 내 `if err` 로 명시적 처리 필요 | 루프가 자동으로 불일치 복구 (Self-healing) | 선언적이면 복구 로직이 기본 내장 |
| **멱등성** | 구현하기 어려움 (중복 실행 시 오류 가능) | 기본으로 보장됨 | |
| **상태 관리** | 드리프트(Drift) 발생 가능성 높음 | 항상 원본(Manifest)와 일치 유지 | |
| **대표 도구** | Ansible (Ad-hoc), Shell Script, Terraform (apply) | Kubernetes, Pulumi, Terraform (state) | *Terraform은 State 기반 선언적 도구* |

#### 2. 타 기술 영역과의 융합 (Convergence)

**① 운영체제(OS)와의 융합: systemd**
리눅스의 **systemd**는 선언적 서비스 관리의 시초입니다. `.service` 파일에 원하는 상태(Wanted State)를 정의해두면, 프로세스가 죽어도 systemd 데몬이 이를 감지하고 즉시 재시작(Resurrect)합니다. 단일 서버의 **Reconciliation Loop**라고 볼 수 있습니다.

**② 네트워크(Net)와의 융합: IBN (Intent-Based Networking)**
기존 네트워크가 **CLI 명령어**(Imperative)로 장비를 설정했다면, 최근 **Cisco ACI**나 **Juniper Apstra** 같은 IBN은 **"보안 그룹 A는 B와 통신 금지"**라는 의도(Intent)만 선언합니다. 네트워크 컨트롤러가 전체 토폴로지를 분석하여 각 스위치의 ACL(Access Control List)을 자동으로 계산하고 배포하며, 설정이 바뀌면 즉시 원복합니다. 이는 네트워크 영역으로 확장된 상태 일치 루프입니다.

**③ 보안(Security)과의 융합: Policy as Code**
**Open Policy Agent (OPA)**는 각 마이크로서비스마다分散된 접근 제어 정책을 통합 관리합니다. "모든 API는 인증되어야 한다"라는 정책(Desired)을 선언하면, OPA가 트래픽을 실시간으로 검사(Observe)하고 차단(Act)합니다.

#### 📢 섹션 요약 비유
> **네비게이션(지도) vs 자율 주행 자동차**의 차이입니다. 네비게이션은 "우회전 하세요"라고 말만 해줄 뿐(명령형), 운전자가 못 들으면 사고가 납니다. 자율 주행차는 "공항으로 가자"라는 목표만 설정하면(선언적), 차량이 도로 상황(Actual)을 보면서 스스로 핸들을 조정하고 장애물을 피합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 무중단 배포 (Zero-Downtime Deployment)
**문제 상황**: 100만 사용자가 이용하는 쇼핑몰 서비스를 업데이트해야 함. 다운타임 없이 교체해야 함.

**[의사결정 프로세스]**
1. **전략 수립**: **Kubernetes Deployment** 리소스 사용.
2. **상태 선언 (Desired)**:
   ```yaml
   spec:
     replicas: 10
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxUnavailable: 2   # 최대 2개까지 다운 허용
         maxSurge: 2         #