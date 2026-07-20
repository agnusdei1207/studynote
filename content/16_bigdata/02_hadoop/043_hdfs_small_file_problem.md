---
title: "HDFS"
date: "2026-03-04"
tags:
  - "studynote-bigdata"
weight: 43
---
## 핵심 인사이트 (3줄 요약)
1. <strong>작은 파일 문제</strong>는 하둡 HDFS에서 수많은 작은 파일이 네임노드의 메모리(Metadata)를 과도하게 점유하여 클러스터 확장성을 저해하는 현상이다.
2. 네임노드는 모든 파일의 메타데이터를 메모리에 로드하므로, 파일 개수가 임계치를 넘으면 NameNode SPOF 및 가용성 장애가 발생한다.
3. 이를 해결하기 위해 파일 합치기(HAR), Sequence File 변환, 또는 애플리케이션 단의 적절한 배치(Batch) 적재 전략이 필수적이다.

### Ⅰ. 개요 (Context & Background)
- **배경**: HDFS는 대용량 파일(Tera/Petabytes)을 수백 메가바이트 단위의 블록으로 분할하여 병렬 처리하도록 설계된 파일 시스템이다.
- **필요성**: 웹 로그나 센서 데이터처럼 초당 수천 개의 작은 파일이 생성되는 환경에서는 HDFS의 설계 의도와 어긋나며 심각한 성능 저하를 유발한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **발생 원인**:
  - **Memory Pressure**: 네임노드는 각 파일/디렉터리/블록 메타데이터 당 약 150바이트를 메모리에 상주시킨다.
  - **I/O Inefficiency**: MapReduce 작업 시 작은 파일 하나가 하나의 Map Task가 되어 과도한 오버헤드(JVM 구동 시간 등)가 발생한다.

```text
[HDFS Small File vs Large File Efficiency]

(Large File) 1GB File           (Small Files) 1,000,000 x 1KB Files
+-----------------------+      +---+ +---+ +---+ ... +---+
| [Block 1] [Block 2]   |      |1KB| |1KB| |1KB|     |1KB| (Metadata Flood!)
| [Block 3] ...         |      +---+ +---+ +---+ ... +---+
+-----------------------+               ||
           ||                           \/
+-----------------------+      +-----------------------------------------+
|     NameNode Mem      |      |           NameNode Memory               |
|  (Minimal Metadata)   |      | [Metadata1][Metadata2]...[Metadata1M]   |
+-----------------------+      +-----------------------------------------+
           ||                           ||
           \/                           \/
   (High Performance)             (Memory Crash & Slow MapReduce)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 해결 방안 | 핵심 메커니즘 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| <strong>HAR (Hadoop Archive)</strong> | 작은 파일들을 하나의 아카이브로 묶음 | 네임노드 메모리 절감 효과 큼 | 읽기 시 두 단계(인덱스+데이터) 조회 오버헤드 |
| <strong>Sequence File</strong> | (Key, Value) 구조의 바이너리 파일 통합 | 압축 효율 높음, 하둡 생태계 호환 | 비바이너리 툴에서 읽기 불편 |
| **CombineFileInputFormat** | 맵리듀스 시 여러 작은 파일을 묶어 처리 | 작업(Task) 생성 오버헤드 감소 | 네임노드 메모리 문제는 해결 못함 |
| **Apache Ozone** | 차세대 객체 스토리지 (S3 호환) | 수십억 개 이상의 객체 지원 | 하둡 클러스터 업그레이드 부담 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- **실무 적용**: 데이터 수집 시 Kafka-Connect의 `rotate.interval.ms` 등을 설정하여 일정 크기(예: 128MB)가 되기 전에는 파일로 저장하지 않는 '버퍼링 전략'을 최우선으로 고려한다.
- **실무적 판단**: 단순한 도구 도입보다 데이터 생성 생명주기(Data Lifecycle) 상에서 상위 애플리케이션이 데이터를 '최대한 뭉쳐서(Chunking)' 적재하도록 가이드하는 것이 가장 근본적인 해결책이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 네임노드 안정성 확보, 하둡 클러스터 수명 연장, MapReduce 처리 속도 최대 10배 이상 향상.
- **결론**: 작은 파일 문제는 하둡의 고전적인 숙제이며, 최근에는 Iceberg나 Delta Lake 같은 최신 테이블 포맷이 백그라운드에서 자동으로 'Compaction(압축)'을 수행하며 이 문제를 현대적으로 해결하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. <strong>Metadata</strong>: 파일의 이름, 권한, 블록 위치 등의 정보
2. <strong>NameNode SPOF</strong>: 마스터 노드 장애 시 전체 시스템 중단 위험
3. <strong>Compaction</strong>: 작은 파일을 큰 파일로 병합하는 주기적 관리 작업

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS 아키텍처 (NameNode 메타데이터 + DataNode 블록)]
    |
    v
[작은 파일 문제 (NameNode 메모리 폭증 -> 성능 병목)]
    |
    v
[HAR / Sequence File / CombineFileInputFormat — 단기 완화]
    |
    v
[Apache Ozone (차세대 객체 스토리지 — 수십억 파일 지원)]
    |
    v
[Delta Lake / Apache Iceberg Compaction — 현대적 자동 해결]
```
HDFS의 작은 파일 문제는 NameNode 힙 메모리 한계에서 비롯되며, 단기 압축 기법에서 Apache Ozone, Delta Lake/Iceberg의 자동 Compaction까지 세대별 해결책이 존재한다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>작은 파일 문제</strong>: 커다란 장난감 상자에 커다란 블록을 넣어야 하는데, 아주 작은 모래알들을 하나씩 따로 포장해서 넣는 것과 같아요.
2. **이유**: 모래알마다 이름표(메타데이터)를 붙이다 보니, 이름표를 적어둔 수첩(네임노드)이 꽉 차서 더 이상 글을 쓸 수 없게 되는 거예요.
3. **결론**: 모래알들을 커다란 한 봉지에 담아서 정리하면 이름표를 하나만 써도 되니까 훨씬 편해진다는 뜻이에요.
