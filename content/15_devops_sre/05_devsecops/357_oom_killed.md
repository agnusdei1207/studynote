---
title: "OOM Killer Kubernetes QoS cgroup Memory Limits"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 357
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OOM (Out-of-Memory) Killer는 Linux 커널이 물리 메모리 부족 시 OOM Score 기준으로 프로세스를 강제 종료하는 최후의 안전장치이며, Kubernetes QoS 클래스는 이 우선순위를 컨테이너 수준에서 정책화한다.
> 2. **가치**: cgroup v2의 memory.limit_in_bytes와 K8s Resource Request/Limit을 통해 노드 전체 메모리 고갈을 방어하고, BestEffort < Burstable < Guaranteed 순서로 중요 워크로드가 마지막에 종료되도록 보장한다.
> 3. **판단 포인트**: OOM Killed 반복 발생은 메모리 누수 버그이거나 Limit 설정 과소 추정으로, Prometheus의 container_memory_working_set_bytes 메트릭으로 실제 사용량을 측정해 Limit을 조정하고 VPA (Vertical Pod Autoscaler)로 자동화해야 한다.

---

## Ⅰ. 개요 및 필요성

Linux 커널은 메모리 부족 상황에서 시스템 전체 마비를 막기 위해 OOM Killer를 실행한다. OOM Killer는 /proc/[pid]/oom_score를 기준으로 종료 대상 프로세스를 선정하며, oom_score는 프로세스의 메모리 사용량, 실행 시간, nice 값을 종합해 계산된다. 점수가 높을수록 먼저 종료된다.

Kubernetes 환경에서 단일 노드의 여러 컨테이너가 메모리를 경쟁할 때, 중요한 시스템 컴포넌트(kube-apiserver, kubelet)보다 사용자 워크로드가 먼저 종료되어야 한다. K8s QoS 클래스는 이 우선순위를 Pod 설정만으로 제어한다.

컨테이너화 환경에서 OOM Killed는 재시작 루프(CrashLoopBackOff)와 서비스 중단의 주요 원인이다. 특히 Java 힙, Node.js 메모리 누수, ML 모델 로딩 실패가 자주 트리거한다.

- 📢 섹션 요약 비유: OOM Killer는 선박이 침몰하기 직전 화물을 버리는 것과 같다. 가장 무거운 화물을 먼저 버려 배를 구하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|             K8s QoS 클래스와 OOM Score 우선순위                  |
+------------------------------------------------------------------+
|  [BestEffort] oom_adj=1000 — 가장 먼저 종료                     |
|  Request=0, Limit=0 (설정 없음)                                  |
|                                                                  |
|  [Burstable] oom_adj=1~999 — 중간 우선순위                      |
|  Request < Limit 또는 일부 컨테이너만 설정                       |
|                                                                  |
|  [Guaranteed] oom_adj=-998 — 마지막에 종료                      |
|  Request == Limit (모든 컨테이너)                                |
|                                                                  |
|  cgroup v2 경계                                                  |
|  memory.limit_in_bytes 초과 시 해당 cgroup 내 프로세스 종료     |
+------------------------------------------------------------------+
```

| QoS 클래스   | 조건                          | OOM 종료 순서 | oom_adj 범위 |
| :----------- | :---------------------------- | :------------ | :----------- |
| BestEffort   | Request/Limit 미설정           | 1순위 (먼저)  | 1000         |
| Burstable    | Request와 Limit 다름           | 2순위         | 1~999        |
| Guaranteed   | Request == Limit               | 3순위 (마지막)| -998         |

**cgroup v2 메모리 제어**: `memory.limit_in_bytes`는 컨테이너 최대 메모리 경계다. 초과 시 해당 컨테이너 강제 종료가 발생한다.

<strong>Java 컨테이너</strong>: JVM 힙은 `-Xmx` 미설정 시 호스트 전체 메모리의 1/4을 사용하려 시도한다. K8s에서는 `-XX:MaxRAMPercentage=75.0` 옵션으로 cgroup 인식을 강제해야 한다.

- 📢 섹션 요약 비유: QoS Guaranteed는 비행기 비즈니스석이다. 경제석(BestEffort) 승객이 먼저 내리고, 비즈니스석(Guaranteed) 승객은 마지막까지 자리를 지킨다.

---

## Ⅲ. 비교 및 연결

| 항목              | 전통 VM 환경               | K8s cgroup 환경              |
| :---------------- | :------------------------- | :--------------------------- |
| 메모리 격리       | VM 하이퍼바이저 수준       | cgroup v2 컨테이너 수준      |
| OOM 제어          | OS 전체 메모리 경쟁        | 컨테이너별 Limit 경계        |
| 우선순위 정책     | OS nice/oom_adj 수동 설정  | K8s QoS 클래스 자동 매핑     |
| 자원 최적화       | 수동 VM 사이즈 조정        | VPA (Vertical Pod Autoscaler)|

<strong>VPA (Vertical Pod Autoscaler)</strong>: Pod의 과거 메모리·CPU 사용량을 학습해 Request/Limit을 자동 권장하거나 적용한다. OOM Killed 반복 시 VPA가 자동으로 Limit을 높여 재시작 루프를 방지한다.

- 📢 섹션 요약 비유: JVM이 cgroup를 모르면 창고(컨테이너) 안에 있는데 창고 바깥의 공간도 자기 것으로 착각하고 물건을 쌓다가 강제 종료된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>OOM Killed 방어 체크리스트</strong>
1. 모든 컨테이너에 Resource Request/Limit 설정 (Guaranteed 권장)
2. Prometheus `kube_pod_container_status_last_terminated_reason == OOMKilled` 알람 설정
3. `container_memory_working_set_bytes` 기반 실제 사용량 측정 후 Limit 조정
4. Java: `-XX:MaxRAMPercentage=75.0`, Node.js: `--max-old-space-size` 명시
5. VPA 도입 검토: Recommendation 모드로 시작

<strong>안티패턴</strong>
- Request 0, Limit 무한대 -> BestEffort로 분류, 먼저 종료됨
- Limit을 Request의 10배 이상 -> 노드 메모리 오버커밋
- Java `-Xmx` 미설정 -> cgroup Limit 초과 OOM Killed 반복

- 📢 섹션 요약 비유: Resource Limit 없이 컨테이너를 운영하는 것은 무한 리필 뷔페에서 접시 제한 없이 음식을 쌓는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Guaranteed QoS와 VPA를 도입하면 OOM Killed로 인한 CrashLoopBackOff 빈도가 80% 이상 감소한다. 노드 메모리 사용률이 안정적 범위(70~80%)에서 유지되며 자원 낭비도 줄어든다.

미래는 cgroup v2와 AI 기반 자원 예측(Karpenter)이 사전 예방적 스케일링을 실현하는 방향이다.

- 📢 섹션 요약 비유: VPA는 스마트한 창고 관리 AI다. 과거 사용 패턴을 학습해 창고가 터지기 전에 미리 적정 크기로 조정한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| cgroup v2                               | 컨테이너 메모리/CPU 격리 커널 기본 메커니즘               |
| QoS 클래스                              | OOM 종료 우선순위 결정, K8s Pod 설정에서 자동 분류        |
| OOM Score                               | 커널이 프로세스 종료 순서 결정하는 점수                   |
| VPA (Vertical Pod Autoscaler)           | 과거 사용량 기반 Request/Limit 자동 권장·적용             |
| container_memory_working_set_bytes      | Prometheus 메트릭, 실제 메모리 사용량 측정               |

### 📈 관련 키워드 및 발전 흐름도

```text
Linux OOM Killer (커널 기반 프로세스 강제 종료)
    |
    v
cgroup v1 — 컨테이너 메모리 격리
    |
    v
K8s Resource Request/Limit + QoS 클래스
    |
    v
cgroup v2 — 계층적 메모리 제어 강화
    |
    v
VPA (Vertical Pod Autoscaler) — 자동 자원 최적화
    |
    v
AI 기반 사전 예측적 자원 관리 (Karpenter)
```

흐름은 "사후 강제 종료 -> 격리 경계 -> 정책 기반 우선순위 -> 자동 최적화 -> AI 예측"으로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명

1. OOM Killer는 물이 넘칠 때 가장 물을 많이 쓰는 수도꼭지를 먼저 잠그는 자동 안전장치예요.
2. K8s QoS는 중요한 앱(Guaranteed)은 물이 부족해도 마지막까지 쓸 수 있게 보호해줘요.
3. VPA는 스마트 전기 계량기처럼 내 앱이 얼마나 메모리를 쓰는지 학습해서 자동으로 적당한 용량을 배정해줘요.
