---
title: "Unity Catalog"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 150
---
## 핵심 인사이트 (3줄 요약)
1. Unity Catalog는 Databricks의 통합 거버넌스 솔루션으로, <strong>3-수준 네임스페이스(catalog.schema.table)</strong>를 통해 데이터·ML 모델·파일을 단일 제어 지점에서 관리한다.
2. <strong>컬럼/행 수준의 세밀한 접근 제어(Fine-Grained Access Control)</strong>, <strong>데이터 리니지 자동 추적</strong>, <strong>감사 로그</strong>를 제공하여 GDPR, HIPAA, SOC2 규정 준수를 지원한다.
3. <strong>Delta Sharing</strong>은 Unity Catalog 위의 오픈 프로토콜로, 데이터를 복사하지 않고 다른 클라우드·플랫폼의 소비자와 안전하게 공유할 수 있다.

---

## Ⅰ. 개요 및 필요성

Databricks의 기존 거버넌스 체계는 각 워크스페이스마다 독립적인 Hive Metastore를 사용하는 구조였다. 이 구조는 멀티 워크스페이스 환경에서 테이블 중복 등록, 접근 권한 불일치, 리니지 단절 등 관리 복잡성을 야기했다.

2022년 출시된 Unity Catalog는 Account 레벨의 단일 메타스토어로 이 문제를 해결한다. 모든 워크스페이스가 동일한 Unity Catalog를 참조하므로 거버넌스 정책이 전사에 일관되게 적용된다.

| 거버넌스 요구사항 | Hive Metastore (기존) | Unity Catalog |
|:---|:---|:---|
| 접근 제어 단위 | 테이블 수준 | 컬럼·행 수준 |
| 리니지 추적 | 없음 | 자동 추적 (컬럼 단위) |
| 멀티 워크스페이스 | 워크스페이스별 분리 | 단일 Account 메타스토어 |
| 감사 로그 | 기본 없음 | 모든 데이터 접근 기록 |
| 외부 데이터 공유 | 별도 구현 필요 | Delta Sharing 내장 |

> 📢 **섹션 요약 비유**: 기존 방식은 각 부서마다 자체 자물쇠와 열쇠를 관리하던 방식이었다면, Unity Catalog는 전사 통합 스마트 카드 시스템으로 누가 언제 어느 방에 들어갔는지 모두 기록된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|                Unity Catalog 3-수준 네임스페이스                  |
+------------------------------------------------------------------+
|  [Account 메타스토어]                                             |
|       |                                                          |
|       +-- catalog_prod          (Catalog 수준)                   |
|       |       +-- sales         (Schema 수준)                    |
|       |       |     +-- orders  (Table / View / Volume)          |
|       |       |     +-- customers                               |
|       |       +-- marketing                                      |
|       |             +-- campaigns                               |
|       |                                                          |
|       +-- catalog_dev           (개발용 Catalog)                 |
|                                                                  |
|  [접근 제어 레이어]                                               |
|  +----------------------------------------------------------+   |
|  |  GRANT SELECT ON TABLE catalog.schema.table TO group_a   |   |
|  |  CREATE ROW FILTER ON TABLE orders (dept = current_user) |   |
|  |  CREATE COLUMN MASK ON TABLE users (ssn -> 'XXXX')        |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  [Delta Sharing]                                                 |
|  +---------------+   공유   +------------------------------+   |
|  | Unity Catalog  | -------> | 외부 소비자 (Snowflake / R / |   |
|  | (공유자)       |         |  Pandas / Power BI)          |   |
|  +---------------+         +------------------------------+   |
+------------------------------------------------------------------+
```

**핵심 기능 요약**

| 기능 | 설명 | 적용 레벨 |
|:---|:---|:---|
| Fine-Grained Access | 컬럼 마스킹, 행 필터링 | 컬럼·행 수준 |
| Data Lineage | SQL 파싱으로 컬럼 리니지 자동 생성 | 컬럼 단위 |
| Audit Log | 모든 SELECT/DML 이벤트 기록 | 테이블 접근 |
| Delta Sharing | 데이터 복사 없이 외부 공유 | 테이블 |
| Volumes | 비정형 파일(CSV, 이미지 등) 거버넌스 | 파일 수준 |
| Model Registry | ML 모델 버전 관리 통합 | ML 모델 |

> 📢 **섹션 요약 비유**: Unity Catalog는 병원 의료정보 시스템과 같다. 의사·간호사·행정직 모두 같은 시스템을 쓰되, 각자 볼 수 있는 진료 기록이 다르게 제한되고, 누가 언제 어떤 기록을 봤는지 모두 남는다.

---

## Ⅲ. 비교 및 연결

<strong>Unity Catalog vs 경쟁 거버넌스 솔루션</strong>

| 항목 | Unity Catalog | AWS Lake Formation | Apache Atlas |
|:---|:---|:---|:---|
| 플랫폼 | Databricks | AWS 전용 | 오픈소스 |
| 접근 제어 | 컬럼·행 수준 | 컬럼 수준 | 테이블 수준 |
| 리니지 | 자동 (SQL 파싱) | 제한적 | 수동 등록 가능 |
| ML 모델 관리 | 내장 (MLflow 통합) | 없음 | 없음 |
| 외부 공유 | Delta Sharing | Cross-account S3 | 없음 |
| 설치·운영 | 완전 관리형 | 완전 관리형 | 자체 설치 |

**연관 기술 연결**

- <strong>Delta Lake</strong>: Unity Catalog가 관리하는 테이블의 기본 저장 포맷
- <strong>MLflow</strong>: Unity Catalog 내 모델 레지스트리로 통합
- <strong>Databricks SQL</strong>: Unity Catalog 권한을 기반으로 쿼리 실행
- <strong>Data Mesh</strong>: Unity Catalog가 도메인별 카탈로그를 연합 거버넌스 방식으로 관리하는 인프라

> 📢 **섹션 요약 비유**: Unity Catalog는 회사의 정보보안팀 역할이다. 누가 어떤 파일을 봐도 되는지 정책을 관리하고, 외부 협력사와 자료를 공유할 때도 보안 채널(Delta Sharing)을 통해서만 허용한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**도입 시나리오**

- <strong>개인정보 보호</strong>: 주민등록번호 컬럼 마스킹 + 특정 부서만 복호화 권한 부여
- **멀티 팀 거버넌스**: 데이터 엔지니어링 팀은 Silver 레이어 쓰기, 분석 팀은 Gold 레이어 읽기만 허용
- <strong>규정 감사</strong>: SOC2 감사 시 Unity Catalog Audit Log로 데이터 접근 이력 제출
- <strong>외부 데이터 판매</strong>: Delta Sharing으로 고객사에 실시간 데이터 피드 제공 (복사 없음)

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 3-수준 네임스페이스 의미 | catalog(조직/환경 구분) -> schema(도메인) -> table(오브젝트) |
| Fine-Grained AC 구현 | ROW FILTER 함수 + COLUMN MASK 정책으로 동적 적용 |
| Delta Sharing 원리 | 서버가 서명된 URL 발급, 소비자가 직접 스토리지 읽기 (복사 없음) |
| 리니지 추적 방식 | 쿼리 실행 시 SQL 파싱 -> 컬럼 -> 컬럼 매핑 자동 생성 |

> 📢 **섹션 요약 비유**: Unity Catalog 운영은 마치 건물 출입 통제와 같다. 각 방(테이블)마다 카드키 권한을 설정하고, 특정 서류(컬럼)는 권한자에게만 보이며, 모든 출입 기록은 CCTV(감사 로그)로 남는다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 거버넌스 일원화 | 워크스페이스별 파편화된 권한 관리 -> 단일 정책 관리 |
| 규정 준수 자동화 | GDPR/HIPAA 컬럼 마스킹을 정책으로 선언, 운영 오버헤드 최소화 |
| 데이터 신뢰성 | 리니지 추적으로 데이터 품질 문제 원인 신속 파악 |
| 데이터 공유 활성화 | Delta Sharing으로 복사 없는 안전한 외부 공유 실현 |

Unity Catalog는 Databricks 플랫폼 위에서 데이터 거버넌스를 완성하는 핵심 레이어다. Data Mesh의 연합 거버넌스 원칙을 기술적으로 구현하는 도구로서, 2024년 이후 도메인 중심 조직에서 빠르게 채택되고 있다. 심화 학습에서는 <strong>3-수준 네임스페이스</strong>, <strong>Fine-Grained 접근 제어 (ROW FILTER + COLUMN MASK)</strong>, <strong>Delta Sharing 원리</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Unity Catalog는 데이터 왕국의 법전이다. 왕국의 모든 창고(테이블)에 대한 법(권한)이 한 권의 책으로 통합되어 있고, 무엇이든 꺼내거나 넣을 때마다 법에 따라 자동으로 허가 여부가 결정된다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 3-수준 네임스페이스 | 핵심 구조 | catalog.schema.table 계층 |
| ROW FILTER | 행 수준 접근 제어 | 동적 행 필터링 함수 |
| COLUMN MASK | 컬럼 수준 접근 제어 | 민감 컬럼 동적 마스킹 |
| Delta Sharing | 외부 공유 | 오픈 프로토콜, 데이터 복사 없음 |
| Data Lineage | 추적 기능 | SQL 파싱 기반 자동 컬럼 리니지 |
| MLflow 통합 | ML 거버넌스 | 모델 레지스트리를 Unity Catalog에서 관리 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[분산 데이터 사일로 (Data Silo) — 거버넌스 부재]
    |
    v
[데이터 카탈로그 (Data Catalog) — 메타데이터 관리]
    |
    v
[Unity Catalog — 3-수준 네임스페이스 (catalog.schema.table)]
    |
    v
[행/컬럼 수준 접근 제어 (Row Filter / Column Mask)]
    |
    v
[Delta Sharing — 오픈 프로토콜 안전 데이터 공유]
```

데이터 거버넌스가 분산 사일로에서 중앙화된 카탈로그와 세분화된 접근 제어를 거쳐 안전한 외부 공유로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. Unity Catalog는 학교 도서관에서 학생마다 빌릴 수 있는 책이 다르게 정해진 도서관 카드 시스템이에요.
2. 비밀 책(민감 컬럼)은 특별 카드를 가진 사람만 볼 수 있고, 누가 어느 책을 빌렸는지 모두 기록돼요.
3. 다른 학교(외부 소비자)와 책을 나눌 때도 사진만 보내고 원본은 여기에 안전하게 보관된답니다(Delta Sharing).
