---
title: "Looker"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 166
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Looker는 LookML (Look Markup Language)이라는 시맨틱 레이어를 통해 비즈니스 로직을 코드로 한 번 정의하면 전사 모든 분석에서 일관되게 재사용되는 <strong>거버넌스 중심 BI 플랫폼</strong>으로, Tableau/Power BI의 "데이터 복사 후 분석"과 달리 소스 DB를 직접 쿼리한다.
- **가치**: "활성 사용자"의 비즈니스 정의를 LookML에 한 번 정의하면 모든 팀의 모든 대시보드가 동일한 정의를 사용하게 되어 지표 불일치(Metric Sprawl) 문제를 근본적으로 해결한다.
- **판단 포인트**: Looker Studio(구 Google Data Studio)는 무료지만 LookML 거버넌스 없이 800개 이상의 커넥터로 빠른 시각화에 최적화되어 있어, 두 제품은 동일 브랜드이지만 완전히 다른 사용 사례와 기술 수준을 가진다.

---

## Ⅰ. 개요 및 필요성

### 지표 불일치(Metric Sprawl) 문제

현대 기업에서 "전환율"이라는 단순한 지표도 팀마다 다르게 계산된다:
- 마케팅팀: 클릭 대비 가입 완료
- 영업팀: 상담 신청 대비 계약 체결
- 제품팀: 방문 대비 핵심 기능 사용
- 경영진: 방문 대비 유료 전환

데이터가 분산되고 각 팀이 자체 SQL을 작성하면 이 불일치가 심화된다. <strong>Looker의 LookML 시맨틱 레이어</strong>는 이 문제를 "비즈니스 정의를 코드로 관리"하여 해결한다.

**📢 섹션 요약 비유**: LookML 시맨틱 레이어는 <strong>표준 사전(Standard Dictionary)</strong>이다. 모든 사람이 같은 사전을 사용하면 단어(지표)의 의미가 통일된다. 각 팀이 자기 사전을 만들면 같은 단어도 다른 의미가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Looker 아키텍처

```
+-------------------------------------------------------------+
|                    Looker 아키텍처                           |
+--------------------------------------------------------------+
|  비즈니스 사용자                                             |
|  +------------------------------------------------------+   |
|  |  Explore UI: 드래그앤드롭 (SQL 없이 분석)             |   |
|  |  Dashboard: 공유 대시보드                             |   |
|  |  Look: 저장된 분석 쿼리                               |   |
|  +------------------------------------------------------+   |
|                          |                                   |
|  LookML 시맨틱 레이어                                        |
|  +------------------------------------------------------+   |
|  |  models/: 데이터베이스 연결 + Explore 정의            |   |
|  |  views/: 테이블/뷰 + 비즈니스 로직 정의               |   |
|  |    - dimensions: 필터 가능한 속성                     |   |
|  |    - measures: 집계 지표 (매출, 사용자 수)            |   |
|  |    - derived_table: LookML 기반 계산 테이블           |   |
|  +------------------------------------------------------+   |
|                          | SQL 자동 생성                     |
|  데이터 소스 (항상 Live)                                     |
|  +------------------------------------------------------+   |
|  |  BigQuery / Snowflake / Redshift / PostgreSQL        |   |
|  |  (데이터 복사 없음 — 원본 직접 쿼리)                  |   |
|  +------------------------------------------------------+   |
+-------------------------------------------------------------+
```

### LookML 핵심 구조

```yaml
# views/orders.view.lkml
view: orders {
  sql_table_name: "public"."orders" ;;  # 원본 테이블 매핑

  # Dimension: 필터·그룹화 가능한 속성
  dimension: order_id {
    type: number
    sql: ${TABLE}.order_id ;;
    primary_key: yes
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }

  # Measure: 집계 지표 (비즈니스 정의가 여기에)
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.amount ;;
    value_format_name: usd
    description: "완료된 주문의 총 매출 (취소·환불 제외)"
    filters: [status: "completed"]  # 비즈니스 로직 내장
  }

  measure: average_order_value {
    type: average
    sql: ${TABLE}.amount ;;
  }
}
```

### Looker vs Looker Studio 비교

| 차원 | Looker | Looker Studio |
|:---|:---|:---|
| **가격** | 엔터프라이즈 (고가) | 무료 |
| **시맨틱 레이어** | LookML (강력한 거버넌스) | 없음 |
| **SQL 사용** | LookML이 자동 생성 | 사용자 정의 SQL 가능 |
| <strong>데이터 소스</strong> | 주요 데이터베이스 | 800+ 커넥터 |
| **주요 사용자** | 데이터 팀 + 비즈니스 | 비기술 사용자 |
| **복잡도** | 높음 (LookML 학습 필요) | 낮음 (드래그앤드롭) |

**📢 섹션 요약 비유**: Looker와 Looker Studio는 <strong>전문 DSLR vs 스마트폰 카메라</strong>와 같다. DSLR(Looker)은 전문가용으로 더 정밀하고 많은 기능을 제공하지만 학습이 필요하고 비싸다. 스마트폰 카메라(Looker Studio)는 무료로 누구나 빠르게 쓸 수 있지만 기능이 제한적이다.

---

## Ⅲ. 비교 및 연결

### Looker Block: 사전 구축 LookML 템플릿

Looker Blocks는 일반적인 플랫폼 데이터를 위한 사전 제작된 LookML 솔루션:
- **Salesforce Block**: CRM 데이터 분석 템플릿
- **Google Analytics Block**: 웹 분석 템플릿
- **Stripe Block**: 결제 데이터 분석
- **Snowplow Block**: 이벤트 추적 데이터

이를 가져와 수정하면 처음부터 LookML을 작성하는 시간을 대폭 절약한다.

### Looker + BigQuery BI 엔진

BigQuery BI 엔진을 사용하면 BigQuery에 저장된 데이터를 인메모리 캐싱으로 서브세컨드 응답으로 Looker에서 조회할 수 있다. Google Cloud 생태계 내에서 Looker + BigQuery + BI 엔진의 조합이 성능·거버넌스의 최적 패키지다.

**📢 섹션 요약 비유**: Looker Blocks는 <strong>레고 기본 세트</strong>와 같다. 처음부터 모든 레고 조각을 만들 필요 없이, 기본 세트(Blocks)를 구입해서 자신의 집(비즈니스 로직)에 맞게 조립하면 된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### LookML 거버넌스 모범 사례

```yaml
# 좋은 LookML 패턴: 비즈니스 로직 중앙화
measure: active_users {
  type: count_distinct
  sql: ${TABLE}.user_id ;;
  filters: [
    last_login_date: "30 days"  # "활성"의 정의가 여기에
  ]
  description: "최근 30일 내 1회 이상 로그인한 사용자 수"
  group_label: "사용자 지표"
}
```

### API-First 설계와 임베디드 분석

Looker는 API-First 철학으로 설계되어, 자사 애플리케이션 내에 Looker 대시보드를 <strong>임베딩(Embedded Analytics)</strong>하는 것이 주요 활용 사례다:
- iFrame 임베딩: 가장 간단한 방식
- Signed Embed: JWT 기반 인증으로 사용자별 필터 적용
- Looker API: 프로그래밍 방식으로 데이터·시각화 접근

**📢 섹션 요약 비유**: Looker의 임베디드 분석은 <strong>레스토랑 내 포스(POS) 시스템</strong>과 같다. 레스토랑 앱(자사 애플리케이션) 안에 분석 화면(Looker 대시보드)이 내장되어, 외부 서비스로 이동하지 않고도 분석을 볼 수 있다.

---

## Ⅴ. 기대효과 및 결론

### Looker 도입 효과

| 영역 | 효과 |
|:---|:---|
| <strong>지표 일관성</strong> | 전사 모든 팀이 동일한 비즈니스 정의 사용 |
| **SQL 거버넌스** | LookML이 SQL 생성 -> SQL 오류·불일치 제거 |
| **보안** | 원본 데이터 복사 없음 -> 데이터 유출 위험 감소 |
| **확장성** | 새 팀·프로젝트 온보딩 시 기존 LookML 재사용 |

### 결론

Looker는 <strong>BI 거버넌스의 미래 표준</strong>이다. 데이터가 분산되고 팀이 늘어날수록 지표 불일치 문제가 심화되는데, LookML 시맨틱 레이어는 이를 코드 수준에서 해결한다. 다만 LookML 전문 인력 확보와 초기 모델링 투자가 필요하므로, 조직의 데이터 성숙도와 팀 역량을 고려하여 도입 시점을 결정해야 한다.

**📢 섹션 요약 비유**: LookML은 회사의 <strong>공식 데이터 언어</strong>다. 외교적 소통에서 모든 나라가 영어(LookML)를 공통어로 사용하면 오해가 없듯, 모든 팀이 LookML로 정의된 지표를 사용하면 분석 오해가 사라진다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| LookML | 핵심 기술 | 비즈니스 로직 코드화 시맨틱 레이어 |
| Dimension | LookML 구성 | 필터·그룹화 속성 정의 |
| Measure | LookML 구성 | 비즈니스 지표 집계 정의 (비즈니스 로직 내장) |
| Explore | LookML 구성 | 조인 관계 + 분석 진입점 정의 |
| Looker Studio | 관련 제품 | 무료, 비기술용 빠른 시각화 |
| Metric Sprawl | 해결 문제 | 팀별 다른 지표 정의로 인한 불일치 |
| BigQuery BI 엔진 | 성능 최적화 | Looker + BigQuery 인메모리 가속 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SQL (SQL)]
    |
    v
[LookML (LookML)]
    |
    v
[Looker (Looker)]
    |
    v
[셀프서비스 BI (Self-Service BI)]
```

이 흐름도는 SQL에서 LookML과 Looker를 거쳐 셀프서비스 BI로 발전하는 분석 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

- Looker의 LookML은 <strong>표준 사전</strong>이에요: 학교에서 모든 학생이 같은 사전을 쓰면 "사랑"이라는 단어의 의미가 같듯, LookML에 "매출"을 한 번 정의하면 모든 팀이 같은 "매출"을 써요.
- Looker Studio는 <strong>무료 스케치북</strong>이에요: 복잡한 규칙 없이 빠르게 그림(차트)을 그릴 수 있어요 — 정밀도보다 속도가 중요할 때 써요.
- Looker의 가장 큰 특징은 "데이터를 복사하지 않는다"는 것이에요 — 원본 데이터베이스에 직접 물어보기 때문에 항상 최신 정보를 볼 수 있어요.
