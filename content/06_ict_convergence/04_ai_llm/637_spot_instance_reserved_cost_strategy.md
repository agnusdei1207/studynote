---
title: "Spot Instance Reserved Cost Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 637
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS EC2의 4가지 구매 모델(On-Demand, Reserved Instance, Savings Plan, Spot Instance)을 워크로드 특성에 따라 직교(orthogonal) 조합하여, ① 약정 기간(1~3년) 기반 할인, ② 유휴 Capacity 기반 변동 할인, ③ 사용량 기반 flexible 할인을 동시에 활용하는 다층적(Tiered) FinOps 비용 최적화 전략이다.
> 2. **가치**: 동일 워크로드를 On-Demand 대비 60~90% 절감 가능하며, 잘 설계된 Spot+RI 하이브리드 구성은 SLA 99.99% 수준을 유지하면서도 컴퓨팅 비용을 70% 이상 절감한다(예: 100대의 c5.xlarge 기준 월 $73,000 -> 약 $21,000).
> 3. **판단 포인트**: Spot의 2분 전 중단(interruption) 대응력(워크로드의 stateless성, checkpoint 지원 여부, Graceful shutdown 구현)과 RI의 약정 lock-in(Standard vs Convertible) 및 인스턴스 패밀리 변경 자유도(Instance Type Flexibility, Region Flexibility) 간의 trade-off가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅 비용 최적화는 단순히 "싸게 쓰겠다"가 아니라 **"워크로드의 SLO(Service Level Objective)와 비용 곡선(Cost Curve)의 교차점"** 을 찾는 행위다. 2020년 이후 마이크로서비스, AI/ML 학습, 배치 분석 워크로드가 폭증하면서 단일 구매 모델로는 다음 3가지 요구를 동시에 충족할 수 없게 되었다.

- **예측 가능성(Predictability)**: 예산 산정 및 CFO 보고가 가능해야 함
- **탄력성(Elasticity)**: 트래픽 변동에 따라 수십~수천 대로 스케일링 가능해야 함
- **내결함성(Fault Tolerance)**: 인프라 장애(여기서는 Spot 회수) 시에도 서비스 연속성 보장

과거(2010~2015)에는 Reserved Instance(RI) + On-Demand 2단 전략이 주류였으나, 2017년 AWS가 **EC2 Fleet API**를 통해 단일 Launch Template에서 On-Demand + RI + Spot을 혼합할 수 있게 하고, 2019년 **EC2 Auto Scaling의 Mixed Instances Policy**를 도입하면서, 그리고 2020~2022년 **Savings Plans**(Compute SP, EC2 Instance SP) 출시로 "약정 단위"가 인스턴스 단위에서 **컴퓨팅 사용량($/hour) 단위**로 추상화되면서 비용 전략의 차원이 한 단계 격상되었다.

특히 **Kubernetes(EC2 기반 Managed Node Group / Karpenter)** 환경에서는 노드 단위의 비용 모델이 Pod 단위의 bin-packing 문제로 변환되었고, **Spot Instance**는 2분 전 interruption notice를 받아 Pod를 다른 노드로 evicts하는 일종의 "정제(refinery)" 같은 역할을 수행한다. 이로 인해 금융권·공공기관을 제외한 대부분의 워크로드(웹·API·CI/CD·데이터 파이프라인·ML Training·Dev/Staging)에서 **Spot 비중을 60~80%까지** 끌어올리는 것이 새로운 베스트 프랙티스가 되었다.

```text
[비용 최적화의 다층 전략 아키텍처]

   +--------------------------------------------------------------+
   |                  Application Workload Layer                  |
   |  +------------+  +------------+  +------------+  +---------+ |
   |  | Web/API    |  | Batch/ETL  |  | ML Training|  | Dev/Stg | |
   |  | (Stateless)|  | (Checkpoint)| | (Distributed)| |(Flexible)| |
   |  +-----+------+  +-----+------+  +-----+------+  +----+----+ |
   +--------+---------------+---------------+--------------+------+
            |               |               |              |
   +--------v---------------v---------------v--------------v------+
   |            Orchestration Layer (Kubernetes / Auto Scaling)   |
   |  +--------------+  +--------------+  +--------------------+  |
   |  | Karpenter /  |  | Mixed Inst.  |  |  Spot Interruption |  |
   |  | Cluster      |  | Policy       |  |  Handler (2-min)   |  |
   |  | Autoscaler   |  | (On+RI+Spot) |  |  (SQS Event)       |  |
   |  +------+-------+  +------+-------+  +---------+----------+  |
   +---------+-----------------+---------------------+-------------+
             |                 |                     |
   +---------v-----------------v---------------------v-------------+
   |             EC2 Capacity Layer (3-Tier Pricing)                |
   |  +-----------------+  +-----------------+  +----------------+ |
   |  | Tier 1: RI / SP |  | Tier 2: Spot     |  | Tier 3:        | |
   |  | (Baseline ~50%) |  | (Burst ~40%)     |  | On-Demand(~10%)| |
   |  | 고정 약정 40~75% |  | 유휴 60~90%v    |  | Peak Burst     | |
   |  | 할인            |  | (2분 interrupt)  |  | Fallback       | |
   |  +-----------------+  +-----------------+  +----------------+ |
   +---------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 자동차 도로의 차선처럼, **RI는 출퇴근 시간엔 항상 보장되는 "버스 전용 차선(예약된 자리)"**, **Spot은 새벽에 남는 "빈 택시"**, **On-Demand는 정체 시 합승하는 "대리 차량"** — 3가지를 상황별로 혼용해야 비용과 안정성을 모두 잡을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. EC2 4대 구매 모델의 수학적 결합

| 구분 | 할인율(리스트가 대비) | 약정 기간 | Capacity 보장 | 결제 옵션 | 적합 워크로드 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **On-Demand** | 0% (기준가) | 없음 | AZ 레벨 보장 | 사용량 과금 | Spike, PoC, Dev |
| **Reserved Instance(Standard)** | 최대 72% | 1 or 3년 | Region 레벨 보장 | All/Partial/No Upfront | 예측 가능한 베이스라인 |
| **Reserved Instance(Convertible)** | 최대 66% | 1 or 3년 | Region 레벨 보장 | All/Partial/No Upfront | 인스턴스 패밀리 변경 가능 |
| **Savings Plans(Compute)** | 최대 66% | 1 or 3년 | $ 사용량 약정 | All/Partial/No Upfront | Fargate/Lambda/EC2 통합 |
| **Savings Plans(EC2 Instance)** | 최대 72% | 1 or 3년 | 패밀리+Region | All/Partial/No Upfront | EC2 전용 깊은 할인 |
| **Spot Instance** | 최대 90% | 없음 | **보장 없음** | 사용량 과금 | Fault-tolerant, Stateless |
| **Capacity Reservations** | On-Demand가 | 1~3년 | **물리적 AZ 보장** | 사용량 + 예약료 | DR, 규제, 이벤트 |

**핵심 공식**:
```
최적 월 비용 = (Baseline × RI_hourly) + (Burst × Spot_hourly) + (Peak_Overflow × OnDemand_hourly)
            + (Compute_SP_할인액)

여기서 Baseline + Burst + Peak_Overflow ≤ Peak_Workload
```

### 2. Spot Instance의 핵심 동작 메커니즘

```text
[Spot Instance Lifecycle - 2분 인터럽션 핸들링]

시간축 -------------------------------------------------------------►

[Launch]                [Rebalance Recommendation]  [Interruption Notice]  [Termination]
   |                            | (Capacity Rebalancing)   |  (2-min warning)      |
   |                            |                          |                       |
   v                            v                          v                       v
+--------+   정상   +------------+   신호  +-------------+   신호  +-----------------+
| Request|----------->|   Running  |---------->|  2-min      |---------->|   Terminated     |
| Spot   |           |            |         |  Warning    |         |  (Hibernate/Stop |
| + ASG  |           |  +------+  |         |  - EventBridge|         |   /Terminate)    |
+--------+           |  |Work  |  |         |  - SQS       |         +-----------------+
                     |  +------+  |         |  - Draining  |
                     +------------+         +-------------+
                            |                    |
                            |                    +---> ① checkpoints/snapshots
                            |                        ② SIGTERM to App
                            |                        ③ deregister from ALB
                            +---> Capacity Rebalancing: ① 새 instance 사전 프로비저닝
                                                     ② 점진적 rollover
```

**(1) Capacity Rebalancing 신호**
- Spot 가격이 변동되지 않더라도, **AWS가 해당 인스턴스 타입/가용 영역의 사용률이 임계치를 초과할 것으로 예측**하면 사전에 알려준다.
- 이 시점에 새로운 인스턴스를 **pre-provisioning**하여 seamless한 교체가 가능하며, Karpenter의 `consolidationPolicy: WhenUnderutilized`와 결합하면 자동으로 신규 Spot 풀을 선택해 노드를 교체한다.

**(2) 2분 인터럽션 핸들링 코드 패턴**
```yaml
# AWS Node Termination Handler (NTH) - EKS/K8s 환경
apiVersion: karpenter.sh/v1beta1
kind: NodePool
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]   # Spot 70% / On-Demand 30%
      disruption:
        consolidationPolicy: WhenUnderutilized
        expireAfter: 720h                 # 30일 후 강제 회수
        nodeDisruptionPolicy:
          - kind: CapacityBlock
            capacityBlockId: "cr-12345"  # 예약 Capacity로 보호
```

**(3) Spot Pool과 다양화 전략(Diversification)**
- Spot 가격은 **Instance Type × Availability Zone × OS** 조합인 **Spot Pool** 단위로 형성된다. c5.xlarge, c5n.xlarge, c5a.xlarge, m5.xlarge 모두 다른 풀이다.
- **최소 N개 풀(권장 15개 이상)** 에 분산하여 인스턴스를 할당하면, 한 풀이 회수되더라도 나머지 풀에서 자동 보충되어 가용성을 유지한다.
- AWS가 제공하는 **Spot Placement Score**(2023년 출시)를 통해 현재 사용자의 워크로드 요구사항(AZU, vCPU, 메모리)에 대해 **가장 interruption이 적을 것으로 예상되는 AZ**의 점수(1~10)를 받아 선택할 수 있다.

### 3. Reserved Instance(RI)의 진화: ① Zonal RI -> ② Regional RI -> ③ Savings Plans

| 세대 | 출시 | 단위 | 변환/교체 | 핵심 가치 |
| :--- | :--- | :--- | :--- | :--- |
| 1세대: Zonal RI | 2009 | 특정 AZ의 특정 인스턴스 | 불가 | Capacity Reservation 동시 제공 |
| 2세대: Regional RI | 2017 | Region 단위, 인스턴스 사이즈 정규화 | Zonal RI로 변환 가능 | AZ 자유, Auto Scaling과 잘 맞음 |
| 3세대: Convertible RI | 2017 | Region + 패밀리 교환 가능 | 동일가치 범위 내 교환 | 패밀리 마이그레이션(예: C5->C6i) |
| 4세대: Compute SP | 2019 | Region 내 모든 EC2/Fargate/Lambda 사용량 $ | 자동 패밀리 이동 | 가장 flexible, Fargate까지 통합 |
| 5세대: EC2 Instance SP | 2019 | 특정 패밀리+Region $ | 패밀리 내 자유 | Compute SP보다 약간 더 깊은 할인 |
| 6세대: Capacity Blocks | 2023 | ML/GenAI 워크로드용 GPU 시간 단위 예약 | ML Trn1/Inf2/P5 전용 | GPU capacity 보장 |

### 4. Savings Plans와 RI의 수학적 동치성

```
1 vCPU × 730h = 730 vCPU-hours
c5.xlarge = 4 vCPU
∴ 1 c5.xlarge RI(1yr, No Upfront, Standard) = 4 × 730 = 2,920 vCPU-hours/yr

동일 가치를 Compute SP로 매수: $X/hour (예: c5.xlarge RI $0.06/h -> Compute SP $0.062/h)
```

**Compute Savings Plans가 EC2 Instance Savings Plans보다 할인율이 약 2~5%p 낮은 이유**: Fargate, Lambda, SageMaker까지 적용 범위를 확장했기 때문이다. 즉, **"할인율 ^ ↔ 유연성 v"** 의 trade-off 관계다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Launch Template / Launch Spec** | 인스턴스 시작 명세 정의 | AMI, IAM Role, UserData, Security Group, Tag, **Instance Market Options**(Spot/On-Demand), **Capacity Rebalancing** 설정 |
| **Auto Scaling Group(ASG) / Karpenter** | 오토스케일링 + Spot/On-Demand 믹스 | ASG의 `MixedInstancesPolicy`로 On-Demand:Spot 비율 정의(예: `OnDemandBaseCapacity: 10, OnDemandPercentageAboveBaseCapacity: 20`), Karpenter는 `weight` 기반 분산 |
| **Spot Fleet Request / EC2 Fleet** | 다중 Spot Pool 요청 관리 | `lowestPrice`(가장 싼 풀 우선) / `diversified`(분산) / `capacityOptimized`(중단률 최소) / `priceCapacityOptimized`(2022년 출시, 가격+용량 동시 최적) 4가지 전략 |
| **Savings Plans / RI Inventory** | 약정 사용량 추적 | AWS Cost Explorer의 **Reservation Utilization**, **Savings Plans Utilization**, **Coverage** 대시보드(권장 90%+) |
| **Spot Interruption Handler** | 2분 인터럽션 대응 | EventBridge -> SQS -> Lambda(또는 AWS Node Termination Handler for EKS) -> `drain`/`deregister` -> Spot Request 새로 생성 |
| **AWS Compute Optimizer** | RI/SP 권고 | 과거 30~60일 사용량 분석 후 Standard/Convertible RI, No Upfront 권장 |
| **Cost Explorer / CUR** | 비용 시각화 | Cost and Usage Report(CUR)에서 `pricing/term`, `pricing/unit`, `lineItem/UsageType` 컬럼으로 RI/SP/Spot 분해 분석 |

- **📢 섹션 요약 비유**: **Launch Template**는 "레시피 카드", **ASG/Karpenter**는 "자동 요리사", **Spot Pool**은 "오늘의 제철 식재료"입니다. 좋은 요리사(오토스케일러)는 제철 식재료가 바뀌어도(Spot 회수) 같은 요리(애플리케이션)를 끊김 없이 내보냅니다.

---

## Ⅲ. 비교 및 연결

### 1. 구매 모델 5종 상세 비교

| 구분 | On-Demand | Reserved(Standard) | Reserved(Convertible) | Spot | Savings Plans(Compute) |
| :--- | :--- | :--- | :--- | :--- | :---