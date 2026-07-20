---
title: "Datanode Block Storage Heartbeat"
date: "2026-03-04"
tags:
  - "hadoop"
  - "studynote-bigdata"
weight: 29
---
## 핵심 인사이트 (3줄 요약)
- **HDFS의 일꾼(Worker)**: 데이터노드(DataNode)는 파일의 실제 데이터를 블록(Block) 단위로 로컬 디스크에 직접 저장하고 관리하는 물리적 서버 노드입니다.
- **상태 보고 (Heartbeat)**: 네임노드(NameNode)에게 주기적으로 하트비트와 블록 리포트를 전송하여, 자신의 생존 여부와 저장된 블록의 무결성을 보고합니다.
- <strong>클라이언트 직접 통신</strong>: 데이터의 읽기/쓰기 작업 시 네임노드는 위치 정보만 알려주고, 실제 데이터 전송은 클라이언트와 데이터노드 간에 직접 이루어져 병목을 방지합니다.

### Ⅰ. 개요 (Context & Background)
HDFS는 마스터-슬레이브 아키텍처를 가집니다. 마스터인 네임노드가 메타데이터를 관리한다면, 슬레이브인 수많은 데이터노드는 기가바이트에서 테라바이트에 이르는 거대 파일을 128MB(기본값)의 블록으로 쪼개어 분산 보관합니다. 이는 저가의 범용 서버(Commodity Hardware)를 수평 확장(Scale-out)하여 대규모 저장소를 구축하기 위한 핵심 구성 요소입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터노드는 네임노드의 지시에 따라 블록의 생성, 삭제, 복제를 수행합니다.

```text
[ DataNode Internal & Communication Architecture ]

1. Block Storage: Stores data as local files (blk_ID) + Checksum (.meta).
2. Communication Loop:
   - Heartbeat: Every 3 seconds (Survival check).
   - Block Report: Every hour (Full list of blocks held).

[ Diagram: Data Write Pipeline ]
   [ Client ] ----(1. Get Locations)----> [ NameNode ]
       |                                      |
       | <----(2. DN1, DN2, DN3)--------------+
       |
       +----(3. Write Block)----> [ DataNode 1 ]
                                      |
                               (4. Replication)
                                      |
                                 [ DataNode 2 ] ----> [ DataNode 3 ]
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
네임노드와 데이터노드의 역할을 명확히 비교합니다.

| 비교 항목 | 네임노드 (NameNode) | 데이터노드 (DataNode) |
| :--- | :--- | :--- |
| **역할** | 관리자 (Manager) | 실무자 (Worker) |
| **저장 내용** | 메타데이터 (파일 목록, 위치) | <strong>실제 데이터 블록</strong> |
| **메모리 vs 디스크** | RAM 위주 (빠른 조회) | <strong>HDD/SSD 위주 (대용량 저장)</strong> |
| **수량** | 단일 또는 소수(HA) | <strong>수십~수만 대 (Scale-out)</strong> |
| **장애 영향** | 전체 시스템 마비 (SPOF) | 해당 노드의 데이터 유실 (복제로 해결) |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
1. **디스크 밸런싱 (Balancer)**: 특정 데이터노드에 데이터가 쏠릴 경우 `hdfs balancer` 명령을 통해 클러스터 전체의 디스크 사용률을 균등하게 맞춰야 합니다.
2. **배드 블록 관리**: 하드웨어 수명이 다해 발생하는 체크섬(Checksum) 오류를 감지하면, 네임노드는 즉시 다른 건강한 노드에서 해당 블록을 복제하도록 지시합니다.
3. **실무적 판단**: 데이터노드는 저가형 서버를 사용하므로 '장애는 일상'이라는 전제하에 설계되었습니다. 따라서 하드웨어 성능보다는 노드 대수를 늘려 처리량(Throughput)을 확보하는 것이 경제적/기술적 정답입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터노드는 빅데이터 저장의 물리적 토대입니다. 최근에는 클라우드 네이티브 환경에 맞춰 '컴퓨팅과 스토리지의 분리'가 대세가 되면서, S3 같은 객체 스토리지가 데이터노드의 역할을 일부 대체하기도 하지만, 성능 최적화가 필요한 대규모 하둡 클러스터에서는 여전히 데이터노드의 지역성(Locality) 기반 연산이 압도적인 효율을 제공합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: HDFS, 분산 파일 시스템, 하둡 에코시스템
- <strong>관계 개념</strong>: 블록(Block), 하트비트(Heartbeat), 복제(Replication)
- **관련 기술**: Amazon S3 (객체 스토리지), Ceph

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS NameNode]
    |
    v
[DataNode]
    |
    v
[블록 저장]
    |
    v
[Heartbeat]
    |
    v
[HA]
```

NameNode와 DataNode의 역할 분담과 Heartbeat 기반 상태 감지가 HDFS 고가용성으로 발전하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 아주 커다란 도서관에서 네임노드가 '책 목록'을 적은 장부를 든 사서 선생님이라면, 데이터노드는 '책'이 꽂혀 있는 책장들이에요.
2. 책장이 너무 많아서 학교 운동장만큼 넓지만, 데이터노드들은 선생님께 "저 여기 잘 있어요!"라고 계속 인사를 해요.
3. 우리가 책을 읽고 싶을 때 사서 선생님께 물어보면, 선생님은 책이 있는 책장 번호를 알려주고 우리는 거기서 직접 책을 꺼내 봐요.
