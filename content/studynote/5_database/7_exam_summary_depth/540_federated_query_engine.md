+++
title = "540. 연방 쿼리(Federated Query) 엔진 - 경계 없는 데이터 조회"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 540
+++

# 540. 연방 쿼리(Federated Query) 엔진 - 경계 없는 데이터 조회

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연방 쿼리 엔진은 물리적으로 분리된 여러 이기종 데이터 소스(SQL, NoSQL, API 등)를 하나의 가상 데이터베이스로 통합하여, **사용자가 단일 쿼리로 여러 소스의 데이터를 결합 조회할 수 있게 하는 분산 처리 기술**이다.
> 2. **가치**: 데이터를 한곳으로 모으는 복잡한 ETL 과정 없이도 **실시간 통합 가시성**을 제공하며, 각 소스 시스템의 고유한 저장 능력을 100% 활용하는 유연한 아키텍처를 실현한다.
> 3. **융합**: 소스별 쿼리 최적화 알고리즘과 전송 효율을 극대화하는 **푸시다운(Push-down)** 기술이 융합되어, 네트워크 비용을 최소화하면서 대규모 분산 조인을 수행한다.

+++

### Ⅰ. 연방 쿼리 처리의 주요 단계

1. **질의 수신 및 파싱**: 사용자가 가상 통합 스키마에 대해 표준 SQL을 던집니다.
2. **질의 분해 (Query Decomposition)**: 쿼리를 각 소스 시스템(Oracle, MongoDB, S3 등)이 처리할 수 있는 조각으로 쪼갭니다.
3. **최적화 및 푸시다운**: 가능한 한 많은 필터링과 집계를 원천 DB에서 수행하도록 명령을 보냅니다 (Data Locality 활용).
4. **결과 결합 및 전달**: 각 소스에서 올라온 부분 결과를 엔진이 메모리 상에서 최종적으로 합쳐 사용자에게 전달합니다.

+++

### Ⅱ. 연방 쿼리 엔진 아키텍처 시각화 (ASCII Model)

```text
[ Federated Query Engine Architecture ]

      (User SQL) : "SELECT * FROM Global_Sales_Report"
                │
      ┌─────────▼─────────┐
      │ Federation Engine │ (Query Orchestrator) ✅
      │ (Presto / Trino)  │ ──▶ [ Global Metadata ]
      └─────────┬─────────┘
                │ (Sub-queries to each source)
      ┌─────────┴─────────┬──────────────┐
      ▼                   ▼              ▼
  [ Source A: DB ]    [ Source B: File ] [ Source C: API ]
 (Local Compute)     (Local Compute)    (Local Compute)
      │                   │              │
      └─────────┬─────────┴──────────────┘
                ▼
      [ Result Aggregator ] ──▶ ✅ "One Unified Result"
```

+++

### Ⅲ. 대표적인 엔진 및 사례

- **Presto / Trino**: 페이스북에서 개발한 초고속 연방 쿼리 엔진의 대명사.
- **Apache Calcite**: 쿼리 파싱과 최적화를 담당하는 범용 연방 쿼리 프레임워크.
- **Snowflake / BigQuery**: 클라우드 저장소(S3/GCS)와 자신의 DB를 연방 조회하는 기능 제공 (External Tables).

- **📢 섹션 요약 비유**: 연방 쿼리 엔진은 **'다국적 화상 회의의 의장'**과 같습니다. 각 팀(데이터 소스)은 자기 나라(로컬 서버)에 그대로 머물러 있지만, 의장이 공통 언어(SQL)로 질문을 던지면 각 팀이 자기 나라의 정보를 정리해서 답변합니다. 의장은 이 답변들을 모아 하나의 최종 보고서(결과)를 만드는 것과 같습니다. 팀원들이 직접 비행기를 타고 한곳에 모일(ETL) 필요가 없어 아주 빠르고 효율적인 회의 방식입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Data Virtualization]**: 연방 쿼리 기술을 포함하는 상위 비즈니스 개념.
- **[Zero-copy Integration]**: 데이터 복제 없이 통합을 달성하는 철학.
- **[Connector]**: 각기 다른 DB와 통신하기 위한 전용 어댑터.

📢 **마무리 요약**: **Federated Query Engine**은 데이터의 장벽을 허뭅니다. 물리적 위치에 상관없이 데이터의 논리적 가치를 하나로 묶어내는, 현대 분산 컴퓨팅의 정수입니다.