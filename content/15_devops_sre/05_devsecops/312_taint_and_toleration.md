---
title: "Taint and Toleration"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 312
---
> **핵심 인사이트**
> - Taint (테인트)는 노드에 붙이는 "거부 스티커"이고, Toleration (톨러레이션)은 파드가 그 스티커를 허용하는 "면역 카드"다.
> - 세 가지 효과(NoSchedule / PreferNoSchedule / NoExecute)로 스케줄링 제어 강도를 조절한다.
> - GPU 노드·전용 노드처럼 특수 워크로드 격리를 선언적으로 표현한다.

---

## Ⅰ. Taint와 Toleration 개념

Taint (테인트)는 노드에 설정하는 키-값-효과 세 쌍의 레이블이다.

```
key=value:Effect
gpu=true:NoSchedule
```

Toleration (톨러레이션)은 파드 스펙에 선언하며, 일치하는 Taint를 가진 노드에 배치될 수 있도록 허용한다.

```
tolerations:
- key: "gpu"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

효과(Effect) 세 종류:

| Effect           | 의미                                    |
|------------------|-----------------------------------------|
| NoSchedule       | Toleration 없는 파드 스케줄 금지         |
| PreferNoSchedule | 가급적 스케줄 안 함(소프트)              |
| NoExecute        | 기존 파드도 축출(Evict)                  |

```
+-------------------------------------------------+
|              Kubernetes Scheduler               |
|                                                 |
|  Node-A  [Taint: gpu=true:NoSchedule]          |
|  +------------------------------------------+  |
|  |  Pod-X (Toleration: gpu=true:NoSchedule) |--->| ✅ 배치 허용 |
|  +------------------------------------------+  |
|                                                 |
|  Pod-Y (Toleration 없음)                        |
|  -------------------------------------------> ❌ 스케줄 거부 |
+-------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> Taint는 "관계자 외 출입금지" 푯말, Toleration은 "출입증"이다.

---

## Ⅱ. Node Affinity와의 비교

| 항목           | Taint/Toleration               | Node Affinity                  |
|----------------|--------------------------------|--------------------------------|
| 방향           | 노드가 파드를 거부              | 파드가 노드를 선호/필수 요구    |
| 표현 방식      | Effect(강도) + 키값             | matchExpressions               |
| 기존 파드 영향 | NoExecute로 축출 가능           | 스케줄 시점에만 영향            |

> 📢 **Ⅱ 섹션 요약 비유**
> Affinity는 파드가 "나는 SSD 노드에서 일하고 싶다"고 말하는 것, Taint/Toleration은 노드가 "특별 카드 없이는 입장 불가"라고 말하는 것이다.

---

## Ⅲ. 실무 시나리오

<strong>GPU 노드 격리</strong>

```bash
# 노드에 Taint 설정
kubectl taint nodes gpu-node-1 gpu=true:NoSchedule

# Taint 해제
kubectl taint nodes gpu-node-1 gpu=true:NoSchedule-
```

<strong>시스템 파드 전용 노드</strong>: control-plane 노드는 기본 `node-role.kubernetes.io/control-plane:NoSchedule` Taint를 가져 워크로드 파드가 침범하지 않는다.

**NoExecute 활용**: 장애 노드에 `node.kubernetes.io/not-ready:NoExecute`가 자동으로 추가돼 파드가 재스케줄된다.

> 📢 **Ⅲ 섹션 요약 비유**
> GPU 노드에 Taint를 거는 것은 특수 실험실에 "허가된 연구원만 입장" 경고문을 붙이는 것이다.

---

## Ⅳ. tolerationSeconds와 축출 타이밍

NoExecute Taint가 생겼을 때 기존 파드가 즉시 축출되지 않고 `tolerationSeconds` 동안 유예시간을 갖는다.

```yaml
tolerations:
- key: "node.kubernetes.io/not-ready"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 300   # 5분 후 축출
```

Kubernetes가 기본 자동 추가하는 Toleration:
- `node.kubernetes.io/not-ready:NoExecute:300`
- `node.kubernetes.io/unreachable:NoExecute:300`

> 📢 **Ⅳ 섹션 요약 비유**
> 출입증이 있어도 화재 경보가 울리면 5분 내로 나가야 한다 — tolerationSeconds는 대피 유예 시간이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소             | 역할                               |
|-----------------------|------------------------------------|
| Taint                 | 노드 -> 파드 접근 제한 선언         |
| Toleration            | 파드 -> Taint 무효화 허용           |
| NoSchedule            | 신규 파드 스케줄 차단              |
| PreferNoSchedule      | 스케줄 비선호(소프트)              |
| NoExecute             | 기존 파드 축출                     |
| tolerationSeconds     | 축출 유예 시간                     |
| Node Affinity         | 파드 주도 노드 선택 메커니즘       |

### 관련 키워드 및 발전 흐름도

```
Taint/Toleration
    +-- NoSchedule -> 신규 파드 배치 제어
    +-- NoExecute  -> 기존 파드 축출 + tolerationSeconds
    +-- Node Affinity (보완: 파드 주도 선택)
    +-- Pod Disruption Budget (PDB) -> 축출 안전 제어
```

> 🧒 **어린이 비유**
> 노드는 놀이터, Taint는 "이 미끄럼틀은 헬멧 착용자만!"이라는 안내판이고, Toleration은 파드가 들고 있는 헬멧이에요.
