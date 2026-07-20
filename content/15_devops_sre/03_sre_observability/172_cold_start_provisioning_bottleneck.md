---
title: "Cold Start Provisioning Bottleneck"
date: "2026-04-21"
tags:
  - "studynote-devops-sre"
weight: 172
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 콜드 스타트 (Cold Start)는 애플리케이션 코드가 느린 문제가 아니라, 0개의 가용 인스턴스에서 요청을 받았을 때 프로비저닝·런타임 초기화·준비 완료까지 거치는 전체 지연이다.
> 2. **가치**: 콜드 스타트는 소수 요청만 맞더라도 99th Percentile (P99) 지연을 지배할 수 있으므로, 평균 응답시간이 아니라 콜드 스타트 비율과 단계별 지연을 따로 측정해야 한다.
> 3. **판단 포인트**: Service Level Objective (SLO)를 넘는 경로라면 프로비저닝된 동시성 (Provisioned Concurrency)·`minScale` 같은 warm capacity를 써야 하고, 허용 가능한 내부 작업이라면 비용 절감을 위해 scale-to-zero를 받아들이는 것이 맞다.

---

## Ⅰ. 개요 및 필요성

콜드 스타트는 서버리스 (Serverless)나 scale-to-zero 환경에서 나타나는 탄력성의 대가다. 요청이 없을 때 인스턴스를 0으로 줄이면 비용은 절약되지만, 다음 요청은 이미 떠 있는 실행 환경이 없으므로 새 컨테이너나 샌드박스를 준비해야 한다. 이 과정에서 스케줄링, 이미지 또는 코드 로딩, 런타임 부팅, 애플리케이션 초기화, Readiness 통과까지의 시간이 한 번에 붙는다.

문제는 이 지연이 자주 보이지 않는다는 점이다. 전체 요청의 0.5%만 콜드 스타트여도 평균값은 멀쩡해 보일 수 있다. 하지만 사용자가 체감하는 첫 요청, 로그인, 결제, 알림 처리처럼 중요한 구간에서는 그 0.5%가 곧 장애로 받아들여진다. 그래서 콜드 스타트는 성능 이슈라기보다 <strong>관측 가능한 프로비저닝 병목</strong>으로 봐야 한다.

```text
+--------------------------------------------------------------------+
|                 First request to zero-capacity service            |
+--------------------------------------------------------------------+
| request                                                            |
|   |                                                                |
|   v                                                                |
| no warm instance -> queue / wait -> provision -> init -> ready    |
|                                                     |              |
|                                                     v              |
|                                               first response       |
|                                                                    |
| warm path = business logic only                                    |
+--------------------------------------------------------------------+
```

즉 "콜드 스타트가 있다"는 말은 단순히 언어 런타임이 무겁다는 뜻이 아니다. 플랫폼 계층과 애플리케이션 계층의 준비 시간이 합쳐져 첫 요청에만 별도의 지연 경로가 열린다는 뜻이다. SRE 관점에서는 이 경로를 따로 보지 않으면 진짜 병목을 놓치기 쉽다.

- **📢 섹션 요약 비유**: 콜드 스타트는 식당이 손님이 없을 때 주방 불을 꺼 두었다가 첫 손님이 오면 불을 켜고 재료를 꺼내는 시간과 같다. 음식 조리 시간만 보면 주방이 느린 줄 알지만, 실제로는 주방을 여는 시간이 더 큰 병목일 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

콜드 스타트 관측의 핵심은 첫 요청 지연을 "한 덩어리"로 보지 않고 단계별로 분해하는 것이다. 일반적으로 첫 요청 지연은 `queue wait + provisioning + runtime init + app init + business latency`로 나눌 수 있다. 이 다섯 구간 중 어디가 길어지는지 알아야 대응 방식도 달라진다.

```text
+--------------------------------------------------------------------+
|                  Cold-start latency decomposition                  |
+--------------------------------------------------------------------+
| request                                                            |
|   |                                                                |
|   +- queue wait            : no instance available                 |
|   +- provisioning          : schedule, sandbox, image/code fetch   |
|   +- runtime init          : Java Virtual Machine (JVM) / Python   |
|   |                            / Node.js boot                      |
|   +- app init              : dependency wiring, database client,   |
|   |                            cache                               |
|   +- business latency      : actual request handling               |
+--------------------------------------------------------------------+
```

| 구간 | 대표 관측 신호 | 무엇을 의미하나 | 주된 개선 방향 |
| :--- | :--- | :--- | :--- |
| Queue Wait | pending requests, activator latency | 요청은 왔는데 처리할 인스턴스가 없음 | warm pool, 빠른 scale-out |
| Provisioning | Pod Pending, image pull seconds, sandbox create | 플랫폼이 실행 환경을 아직 못 준비함 | 이미지 경량화, 노드/이미지 캐시 |
| Runtime Init | Amazon Web Services (AWS) Lambda `Init Duration`, Java Virtual Machine (JVM) startup span | 언어 런타임 기동 부담 | SnapStart, native image, 경량 런타임 |
| App Init | startup probe time, custom bootstrap span | 프레임워크·의존성 초기화 부담 | lazy init, 연결 지연 생성 |
| Business Latency | cold/warm tagged request duration | 실제 비즈니스 코드 처리 시간 | 코드/쿼리 최적화 |

관측 구현도 중요하다. 메트릭에는 `cold_start_rate`, `cold_start_duration_ms`, `provisioning_duration_ms`를 따로 두고, 분산 추적에는 `cold_start=true`, `instance_id`, `revision` 같은 태그를 붙여야 한다. 그래야 "느린 요청"이 애플리케이션 문제인지, 준비되지 않은 인스턴스 문제인지 분리된다.

특히 OpenTelemetry (OTel)나 플랫폼 고유 이벤트를 함께 써야 시야가 완성된다. Lambda라면 `Init Duration`, Knative라면 activator와 revision 스케일 이벤트, Kubernetes라면 Pod Scheduling / Image Pull / Readiness 이벤트가 필요하다. 콜드 스타트는 애플리케이션 로그만으로는 절반만 보이는 문제다.

- **📢 섹션 요약 비유**: 자동차가 늦게 출발했다고 해서 엔진만 의심하면 안 된다. 차고 문을 여는 시간, 시동 거는 시간, 네비게이션 로딩 시간, 실제 주행 시간을 따로 봐야 어디가 느린지 정확히 알 수 있다.

---

## Ⅲ. 비교 및 연결

콜드 스타트는 플랫폼마다 모양이 다르다. AWS Lambda 같은 Function as a Service (FaaS)는 샌드박스 준비와 런타임 초기화가 중심이고, Knative와 Kubernetes Event-driven Autoscaling (KEDA) 같은 scale-to-zero 컨테이너 플랫폼은 이미지 풀링과 Pod Readiness가 더 큰 비중을 차지한다. 같은 "첫 요청 지연"이라도 병목 구간이 다르므로 대응도 달라진다.

| 환경 | 주된 병목 | 흔한 관측 포인트 | 대표 완화책 |
| :--- | :--- | :--- | :--- |
| AWS Lambda | sandbox + runtime init | `Init Duration`, cold/warm flag | Provisioned Concurrency, SnapStart |
| Knative / KEDA | scale-from-zero + readiness | activator latency, revision scale events | `minScale`, image prewarm |
| Kubernetes Pod 신규 기동 | scheduling + image pull + probe | Pod events, startup/readiness duration | 작은 이미지, pre-pull, node warm pool |

콜드 스타트가 위험한 이유는 평균을 속이기 쉽기 때문이다. 예를 들어 warm 요청 99%가 80ms, cold 요청 1%가 2500ms라면 평균은 약 104ms로 그럴듯해 보인다. 하지만 P99는 2500ms 근처로 튀기 때문에 사용자 경험과 SLO는 심각하게 훼손된다. 따라서 RED (Rate, Errors, Duration) 메트릭만 보고 평균을 확인하는 것으로는 부족하고, cold/warm을 분리한 tail latency 분석이 필요하다.

또한 이 문제는 오토스케일링과 직접 연결된다. 요청이 늘었는데 새 인스턴스가 준비되기 전에 트래픽이 몰리면 queue wait가 먼저 폭증한다. 반대로 인스턴스는 빨리 떴지만 애플리케이션 초기화가 무거우면 runtime/app init이 병목이 된다. 즉 콜드 스타트는 성능, 용량 계획, 오토스케일링, 관측성의 교차점에 있다.

- **📢 섹션 요약 비유**: 같은 "늦게 출발한 버스"라도 차고에서 못 나온 건지, 도로에 나와서 승객 태우느라 늦은 건지 이유가 다르면 해결책도 달라진다. 콜드 스타트는 플랫폼마다 막히는 지점이 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 먼저 "이 경로가 cold-start budget을 얼마까지 허용하는가"를 정해야 한다. 로그인 Application Programming Interface (API), 결제, 사용자-facing webhook처럼 첫 요청도 바로 빨라야 하는 경로는 비용을 더 내고 warm capacity를 유지하는 편이 맞다. 반대로 배치 트리거, 관리자용 작업, 낮은 빈도의 내부 잡이라면 scale-to-zero를 유지하고 몇 초의 첫 요청 지연을 받아들이는 것이 합리적일 수 있다.

```text
+--------------------------------------------------------------------+
|                    Cold-start response playbook                    |
+--------------------------------------------------------------------+
| Is first-request latency above SLO budget?                         |
|      +- yes -> keep warm (Provisioned Concurrency / minScale)      |
|      +- no  -> keep scale-to-zero                                  |
|                                                                    |
| Then inspect dominant phase:                                       |
|   provisioning  -> image, node pool, cache                         |
|   runtime init  -> SnapStart, native, lighter framework            |
|   app init      -> lazy init, split dependencies                   |
|   queue wait    -> autoscaler speed, baseline capacity             |
+--------------------------------------------------------------------+
```

| 판단 상황 | 권장 조치 | 이유 |
| :--- | :--- | :--- |
| 사용자 인터랙션 API | warm capacity 유지 | 첫 요청 지연이 곧 User Experience (UX) 하락 |
| JVM / 대형 프레임워크 함수 | SnapStart, native image 검토 | runtime init 비중이 큼 |
| 컨테이너 이미지가 수 GB | 이미지 슬림화, pre-pull | provisioning 시간이 지배적 |
| 내부 배치 / 드문 관리 작업 | cold start 허용 | 비용 절감이 더 중요 |
| scale-down이 너무 공격적 | idle timeout, `minReplica` 조정 | cold start 빈도 자체를 줄임 |

### 안티패턴

1. cold/warm 요청을 섞은 평균값만 대시보드에 올리는 것
2. 모든 서비스에 무조건 scale-to-zero를 적용하는 것
3. 이미지 풀링과 앱 초기화를 구분하지 않고 "앱이 느리다"로만 결론 내리는 것
4. 긴급 hot path를 warm pool 없이 운영하면서 비용 절감만 최적화하는 것

학습 정리에서는 <strong>비용 절감과 지연 허용치의 균형</strong>을 분명히 적는 것이 중요하다. 콜드 스타트는 제거 대상이 아니라, 어느 경로에서 감수하고 어느 경로에서는 선제 비용으로 없앨지 결정해야 하는 신뢰성 설계 요소다.

- **📢 섹션 요약 비유**: 24시간 편의점을 운영할지, 밤에는 문을 닫았다가 손님 오면 불을 켤지를 결정하는 문제와 같다. 손님이 바로 들어와야 하는 가게는 항상 준비해 두어야 한다.

---

## Ⅴ. 기대효과 및 결론

콜드 스타트 관측이 정교해지면 "느린 첫 요청"을 막연한 체감이 아니라 데이터로 설명할 수 있다. SRE는 cold start rate, cold start duration, warm path latency를 분리해 보고, 어느 구간에 예산을 투입해야 SLO가 가장 효율적으로 개선되는지 판단할 수 있다. 이는 무조건 서버를 더 켜 두는 것보다 훨씬 정교한 운영이다.

한계도 있다. 플랫폼 내부 스케줄링은 완전히 통제할 수 없고, 모든 런타임을 동일한 수준으로 최적화할 수도 없다. 또한 warm capacity는 지연을 줄이는 대신 비용을 고정비로 바꾼다. 결국 콜드 스타트 최적화는 공짜 성능 향상이 아니라 비용-탄력성-응답성 사이의 교환이다.

따라서 이 주제는 "콜드 스타트를 없애는 기술"보다 "탄력성의 대가를 계측하고 관리하는 기술"로 기억해야 한다. 잘 설계된 시스템은 cold path를 숨기지 않고, 어디서 감수하고 어디서 제거할지 명확히 선택한다.

- **📢 섹션 요약 비유**: 콜드 스타트 관측은 겨울 아침 자동차 예열 시간을 재는 것과 같다. 매번 엔진을 켜 두는 건 비싸지만, 출근길에 늦을 수 없는 차라면 미리 준비해 두는 비용이 더 싸게 먹힐 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Scale-to-Zero | 비용 절감을 위해 인스턴스를 0으로 줄이는 운영 방식 |
| Queue Wait | 요청은 도착했지만 처리할 인스턴스가 없어 대기하는 구간 |
| Provisioned Concurrency | 함수 실행 환경을 미리 준비해 cold path를 줄이는 방식 |
| `minScale` / `minReplica` | 컨테이너 기반 서비스에서 최소 warm 인스턴스를 유지하는 설정 |
| Init Duration | 런타임과 애플리케이션 초기화 시간이 드러나는 핵심 지표 |
| Tail Latency | 콜드 스타트가 평균보다 P95/P99를 훨씬 크게 악화시키는 이유 |

### 📈 관련 키워드 및 발전 흐름도

```text
Elastic scale-to-zero
    |
    +- no warm instance
    v
queue wait + provisioning + runtime/app init
    |
    v
cold_start_rate / cold_start_duration / tagged tracing
    |
    +- keep warm for hot path
    +- optimize image and init path
    +- accept delay for low-frequency jobs
    v
SLO-aware cost and latency control
```

이 흐름은 콜드 스타트가 단순한 느린 코드가 아니라, 탄력적 인프라 설계와 관측 전략이 만나 만들어지는 운영 주제임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 콜드 스타트는 장난감을 꺼내기 전에 상자를 열고, 배터리를 넣고, 전원을 켜는 시간이 필요한 것과 같아요.
2. 자주 쓰는 장난감은 미리 켜 두면 바로 놀 수 있지만, 계속 켜 두면 배터리가 더 빨리 닳아요.
3. 그래서 어떤 장난감은 항상 준비해 두고, 어떤 장난감은 조금 기다려도 되게 나누어 생각해야 해요.
