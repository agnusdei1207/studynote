---
title: "PV PVC PersistentVolume"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 314
---
> **핵심 인사이트**
> - PV (PersistentVolume)는 클러스터 관리자가 준비한 스토리지 자원이고, PVC (PersistentVolumeClaim)는 파드가 요청하는 스토리지 주문서다.
> - StorageClass (스토리지클래스)를 이용한 동적 프로비저닝으로 PVC 생성 시 자동으로 PV가 만들어진다.
> - 접근 모드(ReadWriteOnce / ReadOnlyMany / ReadWriteMany)가 스토리지 공유 범위를 결정한다.

---

## Ⅰ. PV와 PVC 개념

PV (PersistentVolume)는 클러스터 수준의 스토리지 오브젝트로 관리자가 직접 생성하거나 동적으로 프로비저닝된다.

PVC (PersistentVolumeClaim)는 사용자가 필요한 용량·접근 모드를 선언하는 요청 오브젝트다.

```
+------------------------------------------------------+
|                  스토리지 바인딩 흐름                |
|                                                      |
|  개발자                관리자                        |
|  PVC 생성  --Binding--->  PV 매칭                    |
|  (10Gi 요청)             (10Gi NFS)                  |
|      |                                              |
|      v                                              |
|   파드에서 volumeMounts로 사용                       |
+------------------------------------------------------+
```

접근 모드:

| 모드              | 설명                          |
|-------------------|-------------------------------|
| ReadWriteOnce     | 단일 노드 읽기/쓰기            |
| ReadOnlyMany      | 다중 노드 읽기 전용            |
| ReadWriteMany     | 다중 노드 읽기/쓰기            |

> 📢 **Ⅰ 섹션 요약 비유**
> PV는 창고이고, PVC는 "10평짜리 창고 주세요"라는 신청서다.

---

## Ⅱ. StorageClass와 동적 프로비저닝

StorageClass (스토리지클래스)는 프로비저너(Provisioner), 파라미터, Reclaim Policy를 정의한다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
reclaimPolicy: Delete
```

PVC에 `storageClassName: fast-ssd` 를 명시하면 PVC 생성 시 자동으로 EBS 볼륨이 생성·바인딩된다.

Reclaim Policy:
- Delete: PVC 삭제 시 PV도 삭제
- Retain: PV 보존(수동 정리)
- Recycle: 데이터 초기화 후 재사용(deprecated)

> 📢 **Ⅱ 섹션 요약 비유**
> StorageClass는 창고 유형 카탈로그 — 냉동창고·일반창고 중 선택하면 자동으로 계약이 체결된다.

---

## Ⅲ. StatefulSet과 volumeClaimTemplates

StatefulSet은 `volumeClaimTemplates`를 통해 파드별 고유 PVC를 자동 생성한다.

```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    accessModes: ["ReadWriteOnce"]
    resources:
      requests:
        storage: 5Gi
```

Pod `db-0` -> PVC `data-db-0`, Pod `db-1` -> PVC `data-db-1` 식으로 각 파드가 독립 볼륨을 가진다.

> 📢 **Ⅲ 섹션 요약 비유**
> StatefulSet은 기숙사 — 각 학생(파드)이 자기 방(PVC)을 갖는 구조다.

---

## Ⅳ. CSI (Container Storage Interface)

CSI (Container Storage Interface)는 쿠버네티스가 외부 스토리지 드라이버를 표준 인터페이스로 연결하는 플러그인 체계다.

```
파드
 |
 v
kubelet ---> CSI Driver ---> 스토리지 백엔드
             (AWS EBS, GCP PD, Ceph 등)
```

CSI 이전에는 in-tree 플러그인으로 코어 코드에 직접 통합됐으나, CSI로 분리돼 벤더가 독립적으로 드라이버를 배포할 수 있다.

> 📢 **Ⅳ 섹션 요약 비유**
> CSI는 쿠버네티스 스토리지 포트의 USB 표준 — 어떤 드라이브든 같은 포트에 꽂으면 동작한다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소            | 역할                                    |
|----------------------|-----------------------------------------|
| PV                   | 클러스터 스토리지 자원 오브젝트          |
| PVC                  | 파드가 요청하는 스토리지 주문서          |
| StorageClass         | 동적 프로비저닝 정책 정의                |
| Provisioner          | 실제 볼륨 생성 드라이버                  |
| AccessMode           | 노드 간 접근 범위 제어                   |
| CSI                  | 외부 스토리지 드라이버 표준 인터페이스   |
| StatefulSet          | 파드별 고유 PVC 자동 생성                |

### 관련 키워드 및 발전 흐름도

```
Persistent Storage
    +-- PV + PVC -> 정적 프로비저닝
    +-- StorageClass -> 동적 프로비저닝
    +-- CSI Driver -> 외부 스토리지 연동
    +-- StatefulSet volumeClaimTemplates -> 파드별 독립 볼륨
```

> 🧒 **어린이 비유**
> PV는 학교 사물함, PVC는 "사물함 하나 주세요" 신청서예요. StorageClass는 작은 사물함이냐 큰 사물함이냐를 결정하는 규칙이에요.
