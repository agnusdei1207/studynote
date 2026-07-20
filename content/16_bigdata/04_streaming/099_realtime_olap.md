---
title: "Realtime Olap"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 99
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실시간 OLAP (Real-time OLAP, Online Analytical Processing)은 스트리밍으로 유입되는 데이터를 수초~수 밀리초의 지연으로 즉시 컬럼형(Columnar) 스토어에 적재하고 서브초(Sub-second) 내에 집계·분석 쿼리를 처리하는 분석 아키텍처로, Apache Druid·Apache Pinot·ClickHouse가 대표 구현체다.
> 2. **가치**: 기존 OLAP(DW Batch 적재 -> 야간 집계)은 T+1 데이터만 분석 가능하지만, 실시간 OLAP는 방금 발생한 이벤트(T+수초)를 즉시 분석하여 실시간 사용자 행동 분석·광고 성과 실시간 대시보드·이상 탐지 같은 즉각적인 비즈니스 인사이트를 제공한다.
> 3. **판단 포인트**: 실시간 OLAP은 "최신성(Freshness)"과 "쿼리 성능"을 동시에 달성하는 도구이지만, 완전한 ACID 트랜잭션과 복잡한 JOIN은 지원이 제한적이다. 이벤트 기반 집계·필터·분석에 최적화되어 있으며, 복잡한 다단계 JOIN이 필요하면 전통적 DW가 적합하다.

---

## Ⅰ. 개요 및 필요성

기존 OLAP(배치 기반 DW)은 데이터 적재부터 분석까지 T+1(다음 날)이 표준이었다. 실시간 마케팅·운영·IoT 환경에서 T+1 분석은 너무 늦다.

```text
+--------------------------------------------------------------+
|          기존 OLAP vs 실시간 OLAP 비교                         |
+--------------------------+-----------------------------------+
|    기존 OLAP (배치)        |    실시간 OLAP                    |
+--------------------------+-----------------------------------+
|  배치 ETL -> T+1 적재       |  스트리밍 직접 적재, T+수초         |
|  야간 집계 (수 시간)        |  서브초(< 1초) 쿼리 응답           |
|  Snowflake, Redshift      |  Druid, Pinot, ClickHouse         |
|  복잡한 JOIN 지원           |  JOIN 제한, 사전 집계 최적화        |
|  정확한 ACID               |  Eventually Consistent            |
+--------------------------+-----------------------------------+
```

- **📢 섹션 요약 비유**: 기존 OLAP는 신문(어제 뉴스 집계), 실시간 OLAP는 실시간 뉴스 스트리밍이다. 어제 주가보다 지금 주가를 보고 싶은 트레이더에게는 실시간이 필수다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Apache Druid 아키텍처

```text
[이벤트 소스] -> Kafka -> [실시간 인제스션 노드]
                              | (실시간 분할·인덱싱)
                              v
                    [히스토리컬 노드 (Parquet+인덱스 저장)]
                              |
                    [쿼리 노드 (서브초 집계 처리)]
                              |
                    [브로커 (쿼리 라우팅)]
                              |
                    [대시보드 / API]
```

### 실시간 OLAP 3대 엔진 비교

| 항목 | Apache Druid | Apache Pinot | ClickHouse |
|:---|:---|:---|:---|
| **강점** | 시계열 이벤트 집계 | 낮은 지연 조회 | SQL 편의성, 높은 압축률 |
| **적합 사례** | 광고 클릭 분석, 모니터링 | 실시간 개인화 추천 | 로그 분석, DW 대안 |
| <strong>JOIN</strong> | 제한적 | 제한적 | 광범위 지원 |
| **주요 사용** | Netflix, Uber, Twitter | LinkedIn, Uber Eats | Cloudflare, Yandex |

- **📢 섹션 요약 비유**: Druid는 시계열 전문 스포츠카(이벤트 시간 집계), Pinot는 초고속 조회 스포츠카(낮은 지연), ClickHouse는 만능 SUV(SQL 편의성, 다목적)다.

---

## Ⅲ. 비교 및 연결

실시간 OLAP는 람다 아키텍처(Lambda Architecture)의 Speed Layer나 카파 아키텍처(Kappa Architecture)의 스트림 처리 레이어로 통합된다.

| 아키텍처 | 실시간 OLAP 역할 |
|:---|:---|
| <strong>람다 아키텍처</strong> | Speed Layer + Serving Layer |
| <strong>카파 아키텍처</strong> | 스트림 처리 후 서빙 레이어 |
| <strong>레이크하우스</strong> | 실시간 테이블 포맷(Iceberg+Delta)과 결합 |

- **📢 섹션 요약 비유**: 실시간 OLAP는 레스토랑의 즉석 조리 코너다. 배치 OLAP가 아침에 미리 준비한 뷔페라면, 실시간 OLAP는 주문 즉시 요리해주는 라이브 쿠킹이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: 광고 플랫폼 실시간 성과 대시보드
1초 이내 광고 클릭·노출·전환 지표 집계.

1. **소스**: Kafka 클릭 이벤트 (초당 500,000 이벤트).
2. **적재**: Druid 실시간 인제스션 (세그먼트 1분 단위 생성).
3. **사전 집계**: 광고ID × 시간별 클릭/노출/CTR 롤업 저장.
4. <strong>쿼리</strong>: `SELECT ad_id, SUM(clicks), SUM(impressions), AVG(ctr) FROM events WHERE ts > NOW() - INTERVAL '1' HOUR GROUP BY ad_id`
5. **결과**: 200ms 내 응답 -> 광고 입찰 실시간 최적화 가능.

### 안티패턴
- 실시간 OLAP로 복잡한 다단계 JOIN 쿼리를 실행하려는 안티패턴. Druid/Pinot는 Star 스키마의 단순한 사실 테이블(Fact Table) 집계에 최적화되어 있고, 복잡한 JOIN은 쿼리 타임아웃을 유발한다. JOIN이 많은 분석은 Snowflake/BigQuery 같은 전통 DW가 적합하다.

- **📢 섹션 요약 비유**: 실시간 OLAP에 복잡한 JOIN을 거는 건, 고속도로에서 U턴하는 것이다. 빠른 직선 주행(집계 쿼리)에 최적화된 도로에서 복잡한 기동(JOIN)을 하면 교통 체증이 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **실시간 분석** | 이벤트 발생 후 수초 내 조회 | T+수초 |
| <strong>쿼리 속도</strong> | 수십억 행 집계 서브초 응답 | < 1초 |
| **운영 최적화** | 실시간 지표로 즉각 의사결정 | 광고 CTR 실시간 조정 |

실시간 OLAP는 Apache Iceberg·Delta Lake 기반 스트리밍 테이블과 결합하여 "실시간 레이크하우스(Real-time Lakehouse)" 아키텍처로 발전하고 있으며, ClickHouse의 MaterializedView와 Kafka 직접 연동이 실시간 데이터 파이프라인의 단순화 방향으로 주목받고 있다.

- **📢 섹션 요약 비유**: 실시간 OLAP는 주식 시장의 실시간 시세 화면이다. 매일 저녁 신문(배치 OLAP)이 아닌, 지금 이 순간의 주가(실시간 이벤트)를 0.1초 만에 보여주는 정밀 계기판이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Apache Druid** | 시계열 이벤트 집계에 특화된 실시간 OLAP |
| **Apache Pinot** | 낮은 지연 조회에 특화된 LinkedIn 오픈소스 |
| **ClickHouse** | SQL 친화적 컬럼형 실시간 OLAP |
| <strong>람다 아키텍처</strong> | Speed Layer에 실시간 OLAP 통합 |
| **컬럼형 스토리지** | 실시간 OLAP 쿼리 성능의 기반 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 OLAP — T+1 적재, 야간 집계, DW]
    |
    v
[실시간 OLAP — 스트리밍 즉시 적재, 서브초 쿼리]
    |
    v
[Druid/Pinot/ClickHouse — 실시간 OLAP 3대 엔진]
    |
    v
[람다/카파 아키텍처 통합 — 배치+실시간 유니파이]
    |
    v
[Real-time Lakehouse — Iceberg+Delta+실시간 OLAP]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 실시간 OLAP는 게임 점수판처럼, 데이터가 생기는 즉시 1초도 안 돼 집계해서 보여주는 기술이에요!
2. 광고 회사, SNS, 쇼핑몰에서 "지금 이 순간 몇 명이 보고 있나?"를 실시간으로 알 수 있게 해줘요.
3. Druid, Pinot, ClickHouse 같은 전문 도구들이 수십억 개의 데이터를 0.5초 만에 집계하는 마법을 부린답니다!
