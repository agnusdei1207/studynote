---
title: "Apache Hbase Column Family"
date: "2026-03-04"
tags:
  - "studynote-bigdata"
weight: 37
---
## 핵심 인사이트 (3줄 요약)
- 구글의 빅테이블(Bigtable)을 벤치마킹하여 개발된, HDFS 위에서 동작하는 열 지향(Column-Oriented) NoSQL 데이터베이스임.
- 수십억 개의 행과 수백만 개의 열을 가진 대규모 데이터셋에 대해 밀리초(ms) 단위의 랜덤 읽기/쓰기(Random R/W) 성능을 보장함.
- 주키퍼(ZooKeeper)를 통한 분산 코디네이션과 리전 서버(Region Server) 기반의 수평 확장을 통해 높은 가용성을 확보함.

### Ⅰ. 개요 (Context & Background)
하둡의 HDFS는 한 번 저장하면 수정이 어려운 불변(Immutable) 파일 시스템이며, 데이터 조회도 전체 스캔(Full Scan) 방식이다. 시스템 설계 관점에서 Apache HBase는 이러한 하둡의 한계를 극복하고, HDFS를 '저장소'로 활용하면서도 실시간으로 특정 데이터를 콕 집어 조회(Point Lookup)하거나 수정할 수 있는 능력을 부여한 핵심 DB이다. 주로 페이스북의 메시징 서비스, 주식 거래 로깅, 시계열 데이터 저장 등 '쓰기 부하가 크고 실시간 조회가 필요한' 영역에서 활용된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
HBase는 데이터를 행 키(Row Key) 순으로 정렬하여 여러 대의 리전 서버에 분산 저장한다.

```text
[ Apache HBase Architecture ]

     [ Client / App ] <--- ( ZooKeeper / Meta Table Lookup )
            |
    +-------V-------+       +-----------------------+
    |   HMaster     | <---> |   ZooKeeper Quorum    |
    | (Coordination)|       | (Status / Leader)     |
    +-------+-------+       +-----------------------+
            |
    +-------V-------+       +-------V-------+
    | Region Server |       | Region Server | (Worker)
    | [MemStore]    |       | [MemStore]    | (LSM Tree)
    | [HFile/WAL]   |       | [HFile/WAL]   |
    +-------+-------+       +-------+-------+
            |               |
    [       HDFS Distributed Storage Layers       ]

[ Bilingual Storage Logic ]
- Row Key (행 키): 데이터의 유일한 식별자. 정렬되어 인덱스 역할.
- Column Family (컬럼 패밀리): 연관된 컬럼들의 논리적 그룹. 물리적 저장 단위.
- MemStore (멤스토어): 쓰기 시 먼저 저장되는 인메모리 버퍼. (LSM-Tree 구조)
- HFile (에이치파일): MemStore가 꽉 차면 HDFS로 플러시되는 최종 파일.
```

HBase는 LSM-Tree 구조를 채택하여, 쓰기 요청을 일단 메모리(MemStore)에 순차적으로 기록한 뒤 나중에 덩어리로 디스크(HFile)에 내려보낸다. 덕분에 디스크 랜덤 I/O를 피하고 압도적인 쓰기 속도를 낸다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 관계형 DB (RDBMS) | Apache HBase (NoSQL) |
| :--- | :--- | :--- |
| **확장 방식** | 수직 확장 (Scale-up) | <strong>수평 확장 (Scale-out / 샤딩)</strong> |
| **저장 방식** | 로우 기반 (Row-oriented) | **컬럼 패밀리 기반 (Columnar Family)** |
| <strong>스키마 유연성</strong> | 고정 스키마 (엄격함) | <strong>가변 스키마 (Sparse Data 지원)</strong> |
| <strong>데이터 모델</strong> | 테이블 조인(Join) 중심 | **비정규화 (Denormalized) 중심** |
| **주요 용도** | 결제, 회계 등 트랜잭션 | <strong>대용량 로그, 타임라인, 추천 엔진</strong> |
| **실무적 판단** | "강력한 일관성(ACID) 우선" | <strong>"대용량 확장성 및 가용성 우선"</strong> |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>(행 키 설계 - Row Key Design)</strong> 특정 날짜에 데이터가 몰리는 'Hotspotting'을 방지하기 위해, Row Key 앞에 해시(Hash)나 솔트(Salt)를 붙여 트래픽을 분산 노드에 골고루 뿌리는 설계가 필수적이다.
- **(컬럼 패밀리 수 제한)** 컬럼 패밀리 수가 너무 많으면 HDFS 파일 수가 급격히 늘어나 네임노드에 부하를 주므로, 가급적 1~2개 이내로 유지해야 한다.
- <strong>(콤팩션 튜닝 - Compaction)</strong> 작은 HFile들을 병합하는 Compaction 과정에서 디스크 I/O가 폭증할 수 있으므로, 서비스 사용량이 적은 야간 시간대에 Major Compaction이 일어나도록 스케줄링해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
HBase는 하둡 생태계에서 '실시간 읽기/쓰기'라는 퍼즐 조각을 맞춘 기술이다. 최근에는 카산드라(Cassandra)나 클라우드 기반 NoSQL(DynamoDB 등)에 시장 점유율을 내주고 있지만, 하둡 에코시스템과의 강력한 결합성(Hive 연동 등) 덕분에 여전히 거대 엔터프라이즈 환경의 중추를 담당한다. 실무자는 비즈니스 데이터의 '쓰기/읽기 패턴'을 면밀히 분석하여 HBase의 열 기반 저장 구조가 주는 이점을 극대화해야 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- <strong>HDFS</strong>: HBase의 데이터가 물리적으로 저장되는 장부
- <strong>ZooKeeper</strong>: 클러스터 노드들의 출석부
- <strong>LSM-Tree</strong>: HBase의 고속 쓰기 수리 모델
- <strong>HBase Shell / Thrift</strong>: HBase에 접속하는 인터페이스


### 📈 관련 키워드 및 발전 흐름도

```text
[RDBMS (관계형 DB) — 행 기반 스키마, ACID 트랜잭션, 수직 확장 한계]
    |
    v
[HBase — HDFS 위의 컬럼 패밀리 기반 분산 NoSQL, 수억 행 수평 확장]
    |
    v
[컬럼 패밀리 (Column Family) — 연관 컬럼 묶음을 동일 HFile에 배치, I/O 최적화]
    |
    v
[LSM-Tree (Log-Structured Merge Tree) — MemStore->HFile 계단식 병합으로 고속 쓰기]
    |
    v
[Apache Phoenix — HBase 위에 SQL 레이어를 추가, 기업 데이터 웨어하우스 확장]
```

이 흐름은 행 기반 RDBMS의 수직 확장 한계를 극복하기 위해 HBase 컬럼 패밀리 구조가 등장하고, LSM-Tree 기반 고속 쓰기를 확보한 뒤, Phoenix SQL 레이어로 기업 분석 환경에 통합되는 컬럼형 분산 NoSQL의 발전 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- 아주아주 큰 도서관에 매일 수만 권의 책이 새로 들어온다고 해보자.
- HBase는 책을 하나하나 예쁘게 꽂는 대신, 일단 상자에 담아두고(메모리) 나중에 한꺼번에 서가에 정리해(디스크).
- 덕분에 책을 아주 빨리 받을 수 있고, 나중에 "그 책 어디 있어?"라고 물어봐도 금방 찾아줄 수 있단다!
