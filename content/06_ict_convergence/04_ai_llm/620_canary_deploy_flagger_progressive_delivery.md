---
title: "Canary Deploy Flagger Progressive Delivery"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 620
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Flagger는 Kubernetes 환경에서 Istio/Linkerd/App Mesh/NGINX 등의 Service Mesh 또는 Ingress Controller를 활용하여 **Canary CRD(Custom Resource Definition)** 기반으로 트래픽을 점진적으로 전환하고, Prometheus 메트릭과 Webhook 테스트를 통해 자동 승격/롤백하는 **GitOps 친화적 Progressive Delivery Operator**이다.
> 2. **가치**: 수동 카나리 배포 대비 **MTTR(Mean Time To Recovery) 95% 단축**(배포 실패 시 60초 이내 자동 롤백), 배포 리스크의 **통계적 검증**을 통한 안정성 확보, SRE/DevOps 팀의 **배포 자동화 수준을 L4(Continuous Deployment) -> L5(Progressive Delivery)**로 격상시킨다.
> 3. **판단 포인트**: 트래픽 라우팅 계층 선택(Istio VirtualService vs Gateway API vs NGINX Ingress), 분석 메트릭 정의(SLO 기반), 롤백 임계치(Threshold) 설정, 카나리 단계의 단계 수(iteration)와 유지 시간(step interval), 그리고 **웹훅 부하 테스트(Load Test) 도입 여부**가 운영 안정성의 핵심 결정 변수이다.

---

## Ⅰ. 개요 및 필요성

전통적인 **Big-Bang Deployment**(전체 트래픽을 한 번에 신규 버전으로 전환)는 장애 발생 시 전체 서비스가 마비되는 **블랙아웃 리스크**를 수반한다. Kubernetes가 보편화되면서 **Rolling Update**가 기본 전략이 되었지만, 이는 "트래픽 비율 기반 점진 전환"이 아닌 "Pod 단위 순차 교체"이므로 신규 버전의 비즈니스 로직 결함을 **사용자 트래픽으로 검증**하기 어렵다. 또한 Amazon, Netflix, Google 사례에서 검증된 *"1%의 사용자가 장애를 만나기 전에는 알 수 없는 결함"*이 존재한다.

**Progressive Delivery**(프로그레시브 딜리버리)는 Continuous Delivery를 확장한 개념으로, 배포를 **단일 이벤트**가 아닌 **측정 가능한 연속적 과정**으로 다룬다. 핵심은 ① 단계적 트래픽 전환(Canary), ② 정량적 메트릭 분석(Metrics-Driven), ③ 자동화된 롤백(Automated Rollback), ④ 컨텍스트 기반 실험(A/B Testing)의 4축으로 구성된다. **Flagger**(Flux 프로젝트의 하위 컴포넌트, 원래 Weaveworks 개발)는 이를 Kubernetes 네이티브 CRD로 구현한 대표 Operator이다.

```text
   [기존 배포 패러다임 비교]

   +------------------------------------------------------------+
   |  A. Big-Bang Deploy    : v1.0 --------------► v2.0          |
   |     (한 번에 100% 트래픽 전환, 장애 시 전 사용자 영향)        |
   |                                                            |
   |  B. Rolling Update     : v1.0 [■■■■■■■■]                    |
   |                          v2.0 [▢▢▢▢▢▢▢▢] (Pod 단위 교체)      |
   |     (Pod 단위 점진 교체, 트래픽 비율은 통제 불가)            |
   |                                                            |
   |  C. Blue/Green         : v1.0 (Idle)  v2.0 [■■■■■■■■]      |
   |                          ---- 즉시 DNS/LB 스위치 ----►        |
   |     (이진 스위치, 두 환경 유지 비용 2배)                     |
   |                                                            |
   |  D. Canary + Flagger   : v1.0 [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]        |
   |                          v2.0 [▢▢]  --► [▓▓▓▓]  --► [▓▓▓▓▓▓▓▓]|
   |     (1%->10%->25%->50%->100%, 메트릭 검증 후 승격)            |
   +------------------------------------------------------------+
   ※ Flagger = C와 D의 자동화/지능화 통합 (측정 가능한 점진 배포)
```

**왜 Flagger인가?** Argo Rollouts, Spinnaker, Harness 등도 Progressive Delivery를 지원하지만, Flagger는 ① **단일 바이너리(flagger)로 가볍게** 동작, ② **Service Mesh 추상화(Istio/Linkerd/App Mesh/Consul)를 통해 라우터 교체 가능**, ③ **Flux/GitOps 생태계와 완벽 통합**(`Kustomize`/`Helm` 컨트롤러와 동일 런타임), ④ 분석 단위(iteration)와 메트릭 임계치를 **YAML 선언적**으로 정의 가능하다는 차별점이 있다.

- **📢 섹션 요약 비유**: 카나리 배포는 **새로운 음료를 출시할 때 1,000명에게 먼저 나눠주고 반응을 본 뒤**, 문제가 없으면 전국 매장에 펴는 식품 회사의 베타 테스트와 같다. Flagger는 그 베타 테스트 결과를 **자동으로 분석하고, 불량률 5% 이상이면 즉시 회수**하는 품질관리 AI 매니저다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Flagger는 **Controller 패턴**으로 동작하는 Kubernetes Operator이다. 핵심은 `Canary`라는 **CRD**로, 사용자는 `Deployment` 대신 `Canary` 리소스를 정의하면 Flagger Controller가 이를 감지하여 Primary Deployment(안정 버전)와 Canary Deployment(신규 버전)를 자동으로 생성·관리한다.

```text
   [Flagger Progressive Delivery 아키텍처]

   +------------------------------------------------------------------+
   |                    Kubernetes Cluster                            |
   |                                                                  |
   |  +--------------+    watch    +----------------------------+    |
   |  | Git Repo     |----------► | Flux/Argo CD (GitOps)        |    |
   |  | (Canary YAML)|             +------------+---------------+    |
   |  +--------------+                          | apply              |
   |                                             v                    |
   |  +----------------------------------------------------------+   |
   |  |            Flagger Controller (Deployment)                |   |
   |  |  +-------------+  +--------------+  +----------------+  |   |
   |  |  | Canary CRD  |  | Metrics      |  | Webhook        |  |   |
   |  |  | Reconciler  |  | Analyzer     |  | Executor       |  |   |
   |  |  +------+------+  +------+-------+  +--------+-------+  |   |
   |  +---------+-----------------+--------------------+----------+   |
   |            | create/scale   | query              | call         |
   |            v                v                    v              |
   |  +-----------------+  +----------+  +--------------------+     |
   |  | Primary Deploy  |  |Prometheus|  | Pre/Post Webhook   |     |
   |  |  v1.0 [100%]    |  | (Metrics)|  | (Load Test,        |     |
   |  |                 |  +----------+  |  Integration Test) |     |
   |  | Canary Deploy   |                  +--------------------+     |
   |  |  v1.1 [0%->100%]|                                           |
   |  +--------+--------+                                           |
   |           | traffic split                                       |
   |           v                                                     |
   |  +--------------------------------------+                       |
   |  |  Service Mesh / Ingress Controller   |                       |
   |  |  (Istio VirtualService / Linkerd     |                       |
   |  |   TrafficSplit / NGINX Ingress /     |                       |
   |  |   Gateway API / Contour / Gloo)      |                       |
   |  +--------------------------------------+                       |
   |           |                                                     |
   |           v                                                     |
   |      [End Users]  ◄-- 가중치 기반 라우팅                       |
   +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Flagger Controller** | Canary CRD를 reconcile하는 핵심 엔진. `Deployment`, `Service`, `Service Mesh 라우팅 객체`를 모두 lifecycle 관리 | Go로 작성된 단일 컨트롤러. leader election으로 HA 지원. 기본 10초 간격 reconcile |
| **Canary CRD** | 배포 전략을 선언적으로 정의. `provider`, `metrics`, `webhooks`, `iterations`, `stepWeight` 등을 포함 | Kubernetes API Server에 `apiextensions.k8s.io/v1`로 등록. 사용자 진입점 |
| **Metrics Analyzer** | Prometheus(또는 Datadog/New Relic) 쿼리 결과를 분석해 SLO 위반 여부 판정 | PromQL `http_request_success_rate`, `http_request_duration_p95` 등 평가. 임계치 초과 시 fail 처리 |
| **Webhook Executor** | Pre-rollout(배포 전 통합 테스트) / Post-rollout(배포 후 부하 테스트) / During(롤아웃 중 점검) / Final(완료 후 검증) 4단계 훅 지원 | HTTP POST로 외부 시스템 호출, 응답 코드/본문으로 검증, timeout 설정 가능 |
| **Service Mesh Adapter** | 트래픽 가중치 라우팅을 실제로 수행. 라우터 교체 가능 (Provider Plugin 구조) | Istio: VirtualService weight 0->100, Linkerd: TrafficSplit, NGINX: canary annotation, Gateway API: HTTPRoute |

**핵심 동작 메커니즘 (단계별 트래픽 전환 알고리즘)**:

Flagger는 `Canary.spec.progressDeadlineSeconds`(기본 60분)와 `iterations`(기본 5회) 설정에 따라 다음을 수행한다:

1. **Phase 1 - Initialization**: `app:pod-template-hash` 레이블 검출로 신규 ReplicaSet 등장 감지. Primary(100%) ↔ Canary(0%) 상태.
2. **Phase 2 - Pre-rollout Webhook**: 외부 테스트 호출(예: `hey -c 2 -z 10s https://canary.app/`). 실패 시 즉시 abort.
3. **Phase 3 - Iterative Weight Promotion**: 5단계 예시 (`stepWeights: [1, 10, 25, 50, 100]`)에서 각 iteration마다 ① Canary로 트래픽 가중치 이동 -> ② `stepInterval`(기본 1분) 대기 -> ③ PromQL 평가 -> ④ pass 시 다음 단계, fail 시 롤백.
4. **Phase 4 - Promotion or Rollback**: 최종 iteration 성공 시 Canary Deployment의 Pod 수를 Primary로 복제 후 Primary 업데이트. 실패 시 모든 트래픽을 Primary로 환원하고 Canary는 0으로 축소.

**PromQL 분석 예시 (핵심 임계치)**:

```yaml
# Canary CRD 분석 정의
metrics:
  - name: request-success-rate
    thresholdRange:
      min: 99        # 성공률 최소 99% (백분율)
    interval: 30s    # 30초 간격 폴링
    query: |
      sum(
        rate(
          http_requests_total{
            app="podinfo",
            status=~"2..|3.."
          }[1m]
        )
      )
      /
      sum(
        rate(
          http_requests_total{app="podinfo"}[1m]
        )
      )
  - name: request-latency
    thresholdRange:
      max: 0.500     # P95 500ms 이하
    query: |
      histogram_quantile(0.95,
        sum(
          rate(
            http_request_duration_seconds_bucket{app="podinfo"}[1m]
          )
        ) by (le)
      )
```

핵심 고려사항: ① **메트릭 카디널리티**(`app`/`namespace` 레이블 누락 방지), ② **Canary에 트래픽이 충분히 흘러야** 통계적 유의성 확보(최소 분당 100 RPS 이상 권장), ③ **OpenTelemetry 기반 메트릭**은 PromQL 변환이 필요할 수 있음.

- **📢 섹션 요약 비유**: Flagger는 **자동화 공장의 컨베이어 벨트 시스템**과 같다. 부품(새 코드)이 들어오면 QC 로봇(Webhook)이 사전 검사를 하고, 컨베이어 벨트(트래픽 가중치)를 천천히 움직여가며 **카메라 센서(Prometheus 메트릭)**가 불량품을 발견하면 벨트를 즉시 멈추고 원래 부품으로 되돌린다(롤백).

---

## Ⅲ. 비교 및 연결

**Canary Deployment 전략군** 및 **Progressive Delivery 도구** 간 비교를 통해 Flagger의 위치와 트레이드오프를 명확히 한다.

| 구분 | **Flagger** (Flux Project) | **Argo Rollouts** (Argo Project) | **Spinnaker** (Netflix OSS) | **Harness CD** (상용) |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | 단일 Operator + Service Mesh 어댑터 | CRD + Controller, UI 대시보드 내장 | 마이크로서비스 집합(Halyard, Clouddriver 등), 무거움 | SaaS/자체호스팅 에이전트, GUI 중심 |
| **라우팅 추상화** | Provider Plugin (Istio/Linkerd/NGINX/Gateway API) | TrafficRouting Plugin (동일 + SMI, AWS ALB) | Stage Pipeline 내 Load Balancer 통합 | 단계별 인프라 API 직접 호출 |
| **분석 메트릭** | Prometheus/Datadog/New Relic/SkyWalking | Prometheus/Kubernetes Jobs/Plugins | Datadog/Prometheus/New Relic + Stackdriver | 자체 APM + 3rd party 통합 |
| **GitOps 친화성** | ◎ (Flux 네이티브), 단일 CRD | △ (Argo CD 필요), Rollout CRD 별도 | ✕ (Halyard 설정 기반, GitOps 부적합) | △ (Harness GitOps 옵션) |
| **리소스 사용량** | 가벼움 (CPU 100m, Memory 128Mi) | 중간 (Controller + Dashboard) | 무거움 (Java, 최소 4 vCPU) | 에이전트 경량 |
| **학습 곡선** | 낮음 (YAML 50줄이면 가능) | 중간 (AnalysisTemplate, Experiment 분리) | 높음 (Pipeline as Code JSON) | 낮음 (GUI) |
| **A/B Testing** | △ (헤더 기반 라우팅 일부 지원) | ◎ (Nginx/Envoy header match) | ○ (Stage 구성) | ◎ (Feature Flag 통합) |
| **라이선스** | Apache 2.0 (무료) | Apache 2.0 (무료) | Apache 2.0 (무료) | 상용 (Free 티어 제한) |
| **적합 환경** | 중규모 K8s, GitOps 우선 조직 | 대규모 K8s, 복잡한 분석 필요 | 멀티클라우드, 비-K8s 혼재 | 엔터프라이즈, 거버넌스 중시 |

**연계 기술 스택**:

- **Service Mesh (Istio, Linkerd, Consul, App Mesh)**: Flagger가 트래픽 가중치를 라우팅하는 핵심 계층. Istio 선택 시 `VirtualService` + `DestinationRule`을 자동 관리.
- **Prometheus**: 메트릭 소스. Istio/Link