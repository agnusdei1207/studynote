---
title: "Replicaset Kubernetes Controller Self Healing"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
weight: 86
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ReplicaSet은 Kubernetes에서 원하는 수의 Pod를 유지하는 controller다.
> 2. **가치**: label selector와 reconciliation loop로 self-healing을 구현한다.
> 3. **판단 포인트**: 개수 유지와 롤아웃은 구분해야 하며, 보통 Deployment가 상위 책임을 가진다.

---

## Ⅰ. 개요 및 필요성
ReplicaSet의 존재 이유는 원하는 상태와 실제 상태를 맞추는 일이다. Pod가 죽으면 다시 만들고, 수가 너무 많으면 줄인다.

노드 장애나 앱 크래시가 잦은 클라우드에서는 이 자동 복구가 가용성을 지켜 준다.
- **📢 섹션 요약 비유**: 원하는 개수와 실제 개수를 맞춘다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 요소 | 역할 | 포인트 |
|:---|:---|:---|
| desired replicas | 목표 Pod 수 | spec.replicas |
| label selector | 관리 대상 선택 | 정확한 라벨 설계 |
| reconciliation loop | 상태 비교와 조정 | 계속 반복 |
| self-healing | 장애 복구 | 죽은 Pod 대체 |

+---------------+ observe +----------------+
| ReplicaSet    |------->| current Pods   |
| replicas = 3  |       | matching label |
+------+--------+       +------+---------+
       | reconcile create/delete     |
       v                              v
  +--------------+             +---------------+
  | controller   |------------->| new Pod       |
  +--------------+             +---------------+
- **📢 섹션 요약 비유**: 라벨과 조정 루프가 핵심이다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | ReplicaSet | Deployment | ReplicationController |
|:---|:---|:---|:---|
| 핵심 기능 | Pod 수 유지 | 배포·롤아웃 관리 | 초기 카운트 유지 |
| 업데이트 | 직접 제어 | 롤링 업데이트 지원 | 제한적 |
| 권장 사용 | 저수준 관리 | 일반 애플리케이션 | 구버전 호환 |

실무에서는 ReplicaSet을 직접 만지기보다 Deployment를 통해 관리하는 경우가 많다.
- **📢 섹션 요약 비유**: Deployment와 역할이 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단
- [ ] label selector가 다른 워크로드와 겹치지 않는지 확인한다.
- [ ] Deployment가 필요한 상황인지 먼저 판단한다.
- [ ] Pod가 사라졌을 때 자동 복구가 되는지 검증한다.
- [ ] 원하는 수와 실제 수의 차이를 모니터링한다.

- ❌ ReplicaSet을 버전 배포 도구로 오해하는 것
- ❌ 라벨 충돌로 다른 Pod까지 관리 대상으로 넣는 것
- ❌ 수동으로 Pod를 고정 관리하려는 것
- **📢 섹션 요약 비유**: 라벨 충돌과 직접 관리가 함정이다.

---

## Ⅴ. 기대효과 및 결론
ReplicaSet은 고장난 자리를 다시 채워 넣는 반장 역할이다. 학생이 빠지면 명단을 보고 다시 부르고, 많으면 다시 조정한다.
- **📢 섹션 요약 비유**: 개수 유지가 자동 복구로 이어진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| ReplicaSet | 원하는 Pod 개수를 지킨다. |
| Deployment | 배포와 롤아웃을 관리한다. |
| label selector | 어떤 Pod를 볼지 정한다. |
| reconciliation loop | 차이를 계속 없앤다. |
| self-healing | 장애 난 Pod를 대체한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
desired replicas -> observe current replicas -> reconcile -> create/delete Pod -> 다시 관찰
```

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 기차에서 칸이 하나 빠지면, 다시 같은 칸을 붙여 넣는 것과 같다.
2. 칸이 너무 많아도 맞추고, 부족해도 채워서 항상 같은 길이를 유지한다.
3. 기차의 모양을 지키는 것이 ReplicaSet의 일이다.
