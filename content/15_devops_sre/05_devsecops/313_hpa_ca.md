---
title: "HPA CA Autoscaling"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 313
---
> **핵심 인사이트**
> - HPA (Horizontal Pod Autoscaler)는 파드 수를 늘리고, CA (Cluster Autoscaler)는 노드 수를 늘려 이중 레이어 오토스케일링을 구성한다.
> - HPA는 CPU/메모리·커스텀 메트릭을 기준으로 ReplicaSet을 조정하고, CA는 Pending 파드를 감지해 클라우드 노드를 추가한다.
> - VPA (Vertical Pod Autoscaler)는 리소스 Request·Limit 자체를 조정하는 세 번째 차원이다.

---

## Ⅰ. HPA (Horizontal Pod Autoscaler) 원리

HPA는 `metrics-server`에서 CPU/메모리 사용률을 주기적으로 수집해 목표 비율에 맞게 레플리카 수를 조정한다.

```
replicas = ceil(currentReplicas × currentMetricValue / desiredMetricValue)
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

```
+-----------------------------------------------------+
|                    HPA 제어 루프                    |
|                                                     |
|  metrics-server ---> HPA Controller ---> ReplicaSet  |
|       (CPU 80%)          |               (3 -> 5)   |
|                    [60% 목표 초과]                   |
+-----------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> HPA는 계산원이 부족하면 더 불러오는 매장 관리자다 — 줄이 길어지면 창구를 늘린다.

---

## Ⅱ. CA (Cluster Autoscaler) 원리

CA는 Pending 상태인 파드를 감지해 클라우드 Node Group에 노드를 추가하거나, 유휴 노드를 종료한다.

```
+--------------------------------------------------+
|               CA 동작 흐름                       |
|                                                  |
|  Pod Pending ---> CA 감지 ---> Cloud API 호출     |
|                              (노드 +1)           |
|                 ---> 노드 등록 ---> Pod 배치       |
|                                                  |
|  Idle Node ---> CA 감지 ---> 파드 이동 ---> 삭제  |
+--------------------------------------------------+
```

조건:
- 추가: 스케줄 불가 파드 존재
- 삭제: 노드 사용률 50% 미만 + 파드 안전 이동 가능

> 📢 **Ⅱ 섹션 요약 비유**
> CA는 레스토랑에서 손님이 넘치면 테이블을 추가하고, 손님이 없으면 빈 테이블을 치우는 매니저다.

---

## Ⅲ. HPA + CA 연동 흐름

```
트래픽 급증
   |
   v
HPA: 파드 수 증가 (Pending 발생 가능)
   |
   v
CA: Pending 파드 감지 -> 노드 추가
   |
   v
파드 정상 배치 -> 서비스 안정화
```

**스케일 다운 안전 메커니즘**:
- HPA: `--horizontal-pod-autoscaler-downscale-stabilization`(기본 5분)
- CA: `scale-down-unneeded-time`(기본 10분)

> 📢 **Ⅲ 섹션 요약 비유**
> HPA가 직원을 더 부르면 CA가 그 직원들이 앉을 책상을 추가로 주문하는 구조다.

---

## Ⅳ. VPA (Vertical Pod Autoscaler)

VPA는 파드의 CPU/메모리 Request·Limit을 자동 조정한다.

| 항목        | HPA                    | VPA                    |
|-------------|------------------------|------------------------|
| 조정 대상   | 파드 수(레플리카)       | 파드 리소스 Request     |
| 적합한 앱   | 수평 확장 가능한 웹앱  | DB·싱글톤처럼 확장 어려운 앱 |
| 병행 사용   | VPA와 동시 권장 안 됨  | -                      |

> 📢 **Ⅳ 섹션 요약 비유**
> HPA가 배달 기사 수를 늘린다면, VPA는 각 기사에게 더 큰 가방을 준다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소             | 역할                                    |
|-----------------------|-----------------------------------------|
| HPA                   | 파드 수 자동 조정 (수평 스케일)          |
| CA                    | 노드 수 자동 조정 (클러스터 스케일)      |
| VPA                   | 파드 리소스 크기 자동 조정 (수직 스케일) |
| metrics-server        | CPU/메모리 사용량 수집 컴포넌트          |
| Node Group            | CA가 조정하는 클라우드 노드 풀           |
| KEDA                  | 이벤트 기반 오토스케일러(HPA 확장)       |

### 관련 키워드 및 발전 흐름도

```
Autoscaling
    +-- HPA -> 파드 수 조정 (metrics-server 기반)
    +-- CA  -> 노드 수 조정 (Pending 파드 감지)
    +-- VPA -> 리소스 크기 조정
    +-- KEDA -> 이벤트/큐 기반 고급 오토스케일링
```

> 🧒 **어린이 비유**
> HPA는 바쁠 때 친구를 더 부르는 것, CA는 그 친구들이 앉을 의자를 구해오는 것, VPA는 한 친구에게 더 힘센 도구를 주는 거예요.
