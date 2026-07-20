---
title: "Rack Awareness Fault Tolerance Topology"
date: "2026-03-04"
tags:
  - "hadoop"
  - "studynote-bigdata"
weight: 30
---
## 핵심 인사이트 (3줄 요약)
- **물리적 장애 그룹 인지**: 수많은 서버가 꽂혀 있는 '랙(Rack)' 단위의 장애(스위치 고전압, 전원 차단 등)에 대비하여 데이터를 물리적으로 분산 배치하는 지능형 알고리즘입니다.
- <strong>기본 복제 규칙 (3-Replica)</strong>: 하나의 블록은 로컬 랙에 1개, 멀티 랙(다른 랙)에 2개를 분산 저장하여 가용성과 네트워크 성능의 균형을 맞춥니다.
- <strong>성능과 안정성의 타협</strong>: 모든 복제본을 다른 랙에 두면 안전하지만 네트워크 비용이 비싸지므로, 랙 인지는 '적절한 거리'를 계산하여 최적의 경로를 도출합니다.

### Ⅰ. 개요 (Context & Background)
대규모 하둡 클러스터는 수십 개의 랙으로 구성되며, 각 랙은 상단 스위치(Top-of-Rack Switch)를 통해 연결됩니다. 만약 랙 스위치가 고장 나면 해당 랙의 모든 서버에 접근할 수 없게 됩니다. 네임노드가 데이터노드들의 물리적 위치(Topology)를 모른 채 랜덤하게 복제본을 저장한다면, 운 나쁘게 모든 복제본이 같은 랙에 들어가 랙 전체 장애 시 데이터가 유실될 수 있습니다. 이를 방지하는 기술이 랙 인지(Rack Awareness)입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
네임노드는 랙 토폴로지 스크립트를 통해 각 노드의 `/rack_id`를 파악하고 복제본 위치를 결정합니다.

```text
[ HDFS Default Rack Awareness Strategy ]

Block Replication (Factor = 3):
1. Replica 1: Same Node as Client (or Local Node).
2. Replica 2: Different Rack from Replica 1 (Remote Rack).
3. Replica 3: Same Rack as Replica 2 (But different Node).

[ Diagram: Network Topology ]
      [ Switch Layer 1 ]
      /              \
 [ Rack 1 ]      [ Rack 2 ]
  /      \        /      \
[DN1]  [DN2]    [DN3]  [DN4]
 (R1)            (R2)   (R3)

* Distance Calculation:
- Same Node: 0
- Same Rack (different nodes): 2
- Different Rack: 4
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
랜덤 배치와 랙 인지 배치를 비교합니다.

| 비교 항목 | 랜덤 배치 (Random) | 랙 인지 (Rack Aware) |
| :--- | :--- | :--- |
| <strong>데이터 안전성</strong> | 낮음 (랙 장애 시 유실 위험) | <strong>높음 (랙 장애에도 데이터 유지)</strong> |
| **네트워크 부하** | 낮음~높음 (예측 불가) | **최적화 (랙 내부 통신 활용)** |
| <strong>복구 속도</strong> | 빠를 수도 느릴 수도 있음 | **예측 가능하고 안정적임** |
| <strong>설정 복잡도</strong> | 없음 (기본값) | **토폴로지 맵 구성 필요** |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. **토폴로지 스크립트 작성**: 클라우드가 아닌 온프레미스 환경에서는 IP 대역이나 스위치 포트를 기반으로 `/dc1/rack1` 형태의 계층 구조를 정의하는 스크립트를 반드시 적용해야 합니다.
2. <strong>읽기 성능 최적화</strong>: HDFS는 클라이언트와 가장 가까운(Distance가 낮은) 노드에서 데이터를 먼저 읽도록 하여 클러스터 전체 네트워크 트래픽을 절감합니다.
3. **실무적 판단**: 랙 인지는 '계란을 한 바구니에 담지 마라'는 격언의 공학적 실천입니다. 가용성뿐만 아니라 랙 간(Inter-rack) 대역폭 부족 문제를 해결하는 성능 튜닝의 핵심 지표로 관리해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
랙 인지는 하둡의 고가용성(High Availability)을 완성하는 숨은 공신입니다. 최신 클라우드 환경에서는 '가용 영역(Availability Zone)' 인지 기술로 확장되어, 도시 전체의 재난에서도 데이터를 지켜내는 기술적 근간이 되고 있습니다. 인프라의 물리적 한계를 소프트웨어 알고리즘으로 극복하는 대표적인 사례입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: HDFS 내결함성(Fault Tolerance), 복제(Replication)
- <strong>핵심 알고리즘</strong>: 복제본 배치 정책(Replica Placement Policy)
- **확장 개념**: 가용 영역(AZ), 리전(Region), 데이터 센터 토폴로지

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS 복제 (Replication) — 기본 복제 계수 3]
    |
    v
[랙 인지 (Rack Awareness) — 랙 단위 장애 격리]
    |
    v
[복제본 배치 정책 (Replica Placement Policy)]
    |
    v
[가용 영역 (AZ, Availability Zone) — 클라우드 확장]
    |
    v
[리전 복제 (Cross-Region Replication) — 지역 재해 대비]
```

분산 파일 시스템의 내결함성 전략이 랙 인지에서 클라우드 가용 영역과 리전 수준 복제로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 중요한 보물 지도 3장을 똑같은 상자 안에 다 넣어두면, 상자를 잃어버렸을 때 지도가 다 없어져요.
2. 랙 인지는 지도 한 장은 우리 집(랙 1)에 두고, 나머지 두 장은 옆집(랙 2)에 나눠서 보관하는 규칙이에요.
3. 이렇게 하면 우리 집에 불이 나도 옆집에 지도가 남아 있어서 보물을 찾을 수 있답니다.
