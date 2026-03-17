+++
title = "493. LSM 트리(Log-Structured Merge-Tree) - 쓰기 지향 엔진의 핵심"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 493
+++

# 493. LSM 트리(Log-Structured Merge-Tree) - 쓰기 지향 엔진의 핵심

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSM 트리는 랜덤 쓰기 부하를 줄이기 위해 **데이터를 메모리에 먼저 순차적으로 쌓고(MemTable), 일정 크기가 되면 디스크로 한꺼번에 내려(SSTable) 병합하는 방식의 저장 구조**다.
> 2. **가치**: 디스크의 랜덤 I/O를 순차 I/O로 전환하여 **압도적인 쓰기 처리량**을 보장하며, 읽기 성능 저하를 방지하기 위해 백그라운드에서 주기적인 **콤팩션(Compaction)**을 수행한다.
> 3. **융합**: HBase, Cassandra, RocksDB 등 현대 고성능 NoSQL 스토리지 엔진의 표준으로 융합되어, 실시간 대량 로그나 메시지 처리를 책임진다.

+++

### Ⅰ. LSM 트리의 2단계 계층 구조

1. **메모리 계층 (MemTable)**:
    - 데이터가 들어오면 먼저 메모리의 정렬된 트리(예: Skip List)에 저장합니다.
    - 동시에 장애 복구를 위해 쓰기 로그(WAL)를 남깁니다.
2. **디스크 계층 (SSTable)**:
    - MemTable이 꽉 차면 디스크에 **불변(Immutable)** 파일 형태로 플러시(Flush)합니다.
    - 여러 개의 SSTable 파일이 층(Level)별로 쌓이며 관리됩니다.

+++

### Ⅱ. LSM 트리 데이터 흐름 시각화 (ASCII Model)

```text
[ LSM Tree Write & Merge Flow ]

  (Write) ──▶ [ WAL (Log) ] 💾 (Disk Sequential)
     │
     ▼
  [ MemTable ] ──▶ (Flush when full) ──┐
  (In-Memory)                          │
                                       ▼
  [ Level 0 SSTables ]  [ File 1 ][ File 2 ][ File 3 ] 💾
          │                            │
          └─────────── (Compaction) ───┘
                        │ (Merge & Sort)
                        ▼
  [ Level 1 SSTable  ]  [ Merged File ] 💾 ✅
```

+++

### Ⅲ. 핵심 최적화 기술: 콤팩션 (Compaction)

- **목적**: 중복되거나 삭제된 데이터를 정리하고, 파편화된 작은 파일들을 큰 파일로 합쳐 읽기 성능을 개선합니다.
- **방식**: 
    - **Size-tiered**: 비슷한 크기의 파일들을 모아 합침. (쓰기 유리)
    - **Leveled**: 각 레벨마다 고정된 크기의 파일을 유지. (읽기 유리)
- **블룸 필터 (Bloom Filter)**: 어떤 데이터가 파일에 있는지 없는지 0.1초 만에 확인하여 불필요한 디스크 조회를 막는 보조 기술입니다.

- **📢 섹션 요약 비유**: LSM 트리는 **'포스트잇 메모장과 수첩'**의 관계와 같습니다. 급할 때는 포스트잇(MemTable)에 대충 갈겨써서(순차 쓰기) 책상에 붙여둡니다. 포스트잇이 너무 많아지면(Flush), 이를 날짜순이나 주제순으로 정리해서 수첩(SSTable)에 깔끔하게 옮겨 적습니다. 나중에 수첩이 여러 권 되면 다시 큰 백과사전(Compaction)으로 합치는 영리한 정리법입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Append-only]**: 데이터를 수정하지 않고 계속 덧붙이는 LSM 트리의 본질.
- **[Write Amplification]**: 콤팩션 과정에서 발생하는 쓰기 증폭 현상 (LSM의 숙제).
- **[Immutable]**: 한 번 디스크에 써진 파일은 절대 변하지 않는 성질.

📢 **마무리 요약**: **LSM-Tree**는 속도의 미학입니다. 물리적 디스크의 한계를 소프트웨어적 발상의 전환으로 극복하여, 빅데이터 시대의 폭발적인 데이터를 수용하는 든든한 그릇이 되었습니다.