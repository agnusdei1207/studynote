---
title: "Oom Out Of Memory Killed Kubernetes Limits"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 110
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OOM Killed는 파드가 `resources.limits.memory`로 선언한 메모리 상한을 초과하는 순간, 리눅스 커널의 <strong>OOM Killer가 SIGKILL(9번 시그널)로 프로세스를 즉시 사살</strong>하는 cgroups 기반 자원 통제 메커니즘이다.
> 2. **가치**: 이 사형 집행이 없으면 메모리 누수 파드 1개가 노드 전체 RAM을 독점하여 <strong>같은 노드의 다른 파드·kubelet까지 동반 질식사(Node OOM)</strong>하는 연쇄 붕괴를 야기한다.
> 3. **판단 포인트**: K8s QoS 클래스(Guaranteed > Burstable > BestEffort) 순으로 사살 우선순위가 결정되며, <strong>CPU 초과는 Throttling(감속)이지만 메모리 초과는 즉사</strong>라는 비대칭성이 핵심이다.

---

## Ⅰ. 개요 및 필요성

CPU를 초과하면 K8s는 파드를 죽이지 않고 **속도를 늦춘다(Throttling)**. 하지만 메모리(RAM)는 "빌린 뒤 반환 불가능한" 자원이므로, 한도를 넘는 순간 리눅스 커널이 프로세스를 <strong>즉시 사살(OOM Killed)</strong>하여 다른 파드를 보호한다.

```text
+-------------------------------------------------------+
|      CPU 초과 vs 메모리 초과: 비대칭 대응               |
+-------------------------------------------------------+
|  [CPU 초과]                                           |
|   limits.cpu: 500m 초과 -> Throttling (감속)           |
|   파드는 살아있음, 응답만 느려짐                       |
|                                                       |
|  [Memory 초과]                                        |
|   limits.memory: 512Mi 초과 -> OOM Killed (즉사)       |
|   SIGKILL -> CrashLoopBackOff 무한 루프                |
|                                                       |
|  왜 즉사? -> 메모리는 "빌린 뒤 반환 불가"              |
|  방치 시 -> 노드 전체 RAM 소진 -> 동반 질식사           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: CPU 초과는 고속도로에서 서행(Throttling)하는 것이고, 메모리 초과는 밥그릇을 넘겨 먹은 손님을 식당에서 즉시 퇴장(Kill)시키는 것이다. 안 그러면 식당 전체가 굶는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### QoS 클래스별 사살 우선순위

| QoS 클래스 | 조건 | 사살 순위 | 비유 |
|:---|:---|:---|:---|
| **BestEffort** | requests·limits 미지정 | **1순위 (최우선 사살)** | 무임승차 승객 |
| **Burstable** | requests < limits | **2순위** | 얌체 고무줄 승객 |
| **Guaranteed** | requests == limits | **최후 생존** | 1등석 정가 승객 |

### Java JVM OOM 90% 원인

Java 컨테이너가 OOM의 주범인 이유: JVM은 자신이 컨테이너 안에 갇힌 줄 모르고 <strong>노드 전체 RAM(32GB)</strong>을 자기 것으로 착각하여 Heap을 무한 확장한다. 컨테이너 limits(512MB)를 넘는 순간 OOM Killed.

**해결**: `-XX:MaxRAMPercentage=75.0` 옵션으로 JVM Heap을 컨테이너 limits의 75%로 제한한다.

- **📢 섹션 요약 비유**: 50cm 어항(컨테이너)에 상어(JVM)를 넣으면 유리를 깨고 죽는다. 유전자 조작(-Xmx)으로 금붕어 체질로 만들어야 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | CPU Throttling | OOM Killed |
|:---|:---|:---|
| **대상 자원** | CPU (시간 분할 가능) | Memory (분할 불가) |
| **초과 시 대응** | 감속 (느려짐) | **즉사 (SIGKILL)** |
| <strong>파드 상태</strong> | Running (느림) | **CrashLoopBackOff** |
| **사용자 영향** | 응답 지연 | <strong>서비스 중단</strong> |
| <strong>복구 방법</strong> | 자동 (부하 감소 시) | **재시작 + 원인 수정** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 대처 체크리스트
1. **즉시**: `kubectl describe pod` -> `Reason: OOMKilled` 확인.
2. **임시**: `limits.memory` 상향 (진통제, 근본 해결 아님).
3. **근본**: Java -> `-XX:MaxRAMPercentage=75.0`, Node.js -> `--max-old-space-size`.
4. **예방**: Prometheus + Grafana로 메모리 사용률 80% 알림 설정.

### 안티패턴
- **limits 미지정 (BestEffort)**: DB 파드에 limits를 안 걸어두면 노드 OOM 시 1순위 사살 대상.
- **limits 무조건 상향**: 메모리 누수 버그를 방치하고 limits만 올리면 시한폭탄.

---

## Ⅴ. 기대효과 및 결론

| 전략 | 효과 |
|:---|:---|
| Guaranteed QoS (DB) | 노드 OOM에서도 **최후까지 생존** |
| JVM Heap 제한 | OOM 발생률 **90% 감소** |
| limits 적정 설정 | 리소스 낭비 없이 **안정 운영** |
| 모니터링 알림 | OOM 전 **사전 대응** 가능 |

OOM Killed는 클라우드 네이티브 환경에서 가장 빈번한 장애 원인이며, cgroups v2와 K8s Memory QoS(KEP-2570)가 결합하여 더 세밀한 메모리 관리가 가능해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>cgroups</strong> | OOM Killer의 기반 기술, 리눅스 자원 격리 |
| <strong>K8s QoS Class</strong> | Guaranteed·Burstable·BestEffort 사살 우선순위 |
| <strong>JVM Heap</strong> | Java 컨테이너 OOM의 90% 원인 |
| **CrashLoopBackOff** | OOM Killed 후 재시작 반복 상태 |
| <strong>Vertical Pod Autoscaler</strong> | OOM 방지를 위한 자동 limits 조정 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[cgroups v1 (2007) — 프로세스별 메모리 제한 도입]
    |
    v
[Docker (2013) — 컨테이너별 메모리 limits 적용]
    |
    v
[K8s QoS Class (2015~) — Guaranteed·Burstable·BestEffort 분류]
    |
    v
[cgroups v2 + Memory QoS (2022~) — 세밀한 메모리 보호]
    |
    v
[현재: VPA + KEP-2570 — 자동 limits 튜닝 + 메모리 QoS]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 식당에서 밥그릇(512MB) 1개만 먹으라고 했는데, 욕심쟁이 손님(파드)이 밥통을 통째로 먹으려 했어요.
2. 경비원(OOM Killer)이 즉시 그 손님을 쫓아냈어요. 안 그러면 다른 100명의 손님이 굶어요!
3. 해결법은 욕심쟁이 손님에게 "밥 1그릇만 먹는 체질(-Xmx)"로 바꿔주는 거랍니다!
