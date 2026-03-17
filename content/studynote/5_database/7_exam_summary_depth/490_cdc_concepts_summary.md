+++
title = "490. CDC(Change Data Capture) - 실시간 데이터의 혈류"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 490
+++

# 490. CDC(Change Data Capture) - 실시간 데이터의 혈류

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC는 데이터베이스에서 발생하는 모든 **변경 사항(INSERT, UPDATE, DELETE)을 실시간으로 감지하여 추출하고, 이를 타겟 시스템으로 전송하는 기술**이다.
> 2. **가치**: 운영 DB에 부하를 주는 전체 조회 방식 대신 **트랜잭션 로그**를 직접 읽어 처리하므로, 성능 저하 없이 소스와 타겟 간의 데이터 시차(Lag)를 최소화한다.
> 3. **융합**: 실시간 마이그레이션, 마이크로서비스 간의 데이터 동기화, 검색 엔진(Elasticsearch) 데이터 피딩 기술과 융합되어 현대적 데이터 파이프라인의 핵심 관문 역할을 한다.

+++

### Ⅰ. CDC의 핵심 작동 방식: 로그 기반 (Log-based)

- **원리**: DB 엔진이 복구를 위해 남기는 **Redo Log**나 **Binary Log**를 CDC 에이전트가 가로채어 해석합니다.
- **특징**:
    - **비침습적 (Non-invasive)**: 운영 중인 테이블을 건드리지 않아 서비스 성능에 영향이 거의 없습니다.
    - **정확성**: 커밋된 트랜잭션만 골라내어 데이터 정합성을 완벽히 유지합니다.
    - **실시간성**: 변경이 일어나는 즉시 이벤트 스트림으로 변환되어 전송됩니다.

+++

### Ⅱ. CDC 데이터 흐름 시각화 (ASCII Flow)

```text
[ CDC Real-time Synchronization ]

  [ Source DB ] ──▶ [ Transaction Log ] ──▶ [ CDC Agent (Debezium 등) ]
       │                                       │ (Capture & Transform)
       │                                       ▼
  (User Update)                       [ Message Bus (Kafka) ]
                                               │ (Stream)
          ┌────────────────────────────────────┼────────────────────────────────┐
          ▼                                    ▼                                ▼
  [ Target DB (Replica) ]              [ Search Engine (ES) ]           [ Data Lake (S3) ]
```

+++

### Ⅲ. CDC 도입 시 고려사항

1. **스키마 변경 대응**: 소스 DB의 테이블 구조가 바뀔 때 CDC 파이프라인이 깨지지 않도록 하는 스키마 진화(Schema Evolution) 전략이 필요합니다.
2. **Exactly-once 보장**: 네트워크 장애 시 데이터가 중복 전송되거나 누락되지 않도록 하는 멱등성(Idempotency) 설계가 중요합니다.
3. **도구 선택**: 오픈소스인 **Debezium**, 클라우드 서비스인 **AWS DMS**, 유료 솔루션인 **Oracle GoldenGate** 중 비즈니스 규모에 맞는 선택이 필요합니다.

- **📢 섹션 요약 비유**: CDC는 **'CCTV 실시간 중계 시스템'**과 같습니다. 예전 방식이 하루 일과가 끝나고 장부를 통째로 복사해 가는 것(Batch)이었다면, CDC는 현장에서 일어나는 모든 움직임을 실시간으로 카메라로 찍어(Capture) 전 세계 지점으로 생중계(Sync)하는 것입니다. 덕분에 모든 지점이 본사와 똑같은 현장 상황을 실시간으로 공유할 수 있게 됩니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Log-based vs Trigger-based]**: 로그를 읽는 고성능 방식과 트리거를 거는 고전적 방식의 차이.
- **[Zero-Downtime Migration]**: CDC를 활용한 서비스 중단 없는 DB 이전.
- **[Data Pipeline]**: CDC가 시작점이 되는 거대한 데이터 유통망.

📢 **마무리 요약**: **CDC**는 정적인 데이터를 살아 움직이게 합니다. 파편화된 시스템들을 하나의 데이터로 묶어주는 실시간 혈관과 같은 역할을 수행하여 비즈니스의 민첩성을 완성합니다.