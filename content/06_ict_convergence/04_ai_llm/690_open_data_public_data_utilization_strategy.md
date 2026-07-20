---
title: "Open Data Public Data Utilization Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 690
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈·공공데이터 활용 전략은 **W3C DCAT-AP 3.0 메타데이터 표준**, **REST/OData/GraphQL API 게이트웨이**, **KOGL Type 1(공공누리) 라이선스 체계**, 그리고 **FAIR(Findable, Accessible, Interoperable, Reusable) 원칙**을 기반으로, 분산된 1·2·3종 공공기관의 이종(heterogeneous) 데이터를 통합 카탈로그로 제공·연계·분석하는 데이터 거버넌스 프레임워크이다.
> 2. **가치**: 데이터 개방 시 GDP 0.5~1.5% 창출 효과(경제협력개발기구 OECD, 2019), 데이터 기반 행정비용 연 1.2조 원 절감(한국행정연구원), 민간 활용 시 신규 서비스 8.7배 증가 효과(공공데이터포털 data.go.kr 2023 기준 87,418종 제공, 누적 활용 13억 건)를 통해 **데이터 경제(Data Economy) 및 디지털 플랫폼 정부(DPG, Digital Platform Government)** 실현의 핵심 인프라인 가치를 제공한다.
> 3. **판단 포인트**: 데이터 개방 범위(원시/정제/가공)와 **비식별화(k-익명성·ℓ-다양성·차분프라이버시) 수준**, 라이선스(공공누리 KOGL 1~4형 vs. CC-BY vs. 상업적 이용 가능 여부), 표준 포맷(JSON/XML/CSV/RDF/GeoJSON/Parquet), 실시간 배치(Sync vs. Async, Kafka/CDC), 품질 검증(ISO/IEC 25012) 및 **데이터 계약(Data Contract)**, 그리고 마이데이터·공공데이터 결합 시 **개인정보보호법 가명정보 처리 동의**의 트레이드오프가 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

공공데이터란 「공공데이터의 제공 및 이용 활성화에 관한 법률」(2013. 7. 30. 시행, 2024. 10. 전면개정)에 따라 **공공기관이 업무상 생성·취득·관리하는 데이터**로서, 국민생활의 편익 증진과 국가·사회 전반의 데이터 활용을 위하여 그 이용을 촉진할 필요가 있는 데이터를 의미한다. 여기에는 행정데이터(행정보고·민원·통계), 센서 데이터(IoT·CCTV·환경측정), 위치·공간데이터(공간정보·교통·지하철), 의료·교육·재정 등 1,300여 종 이상의 데이터셋이 포함된다.

기존의 **데이터 폐쇄(Closed Data) 패러다임**은 각 기관이 데이터베이스(DB)별로 데이터를 격리 보관하며, "원하면 직접 방문해 종이·USB 등으로 제공하라"는 소극적·수동적 공개 방식이었다. 이로 인해 **부처 칸막이(Stovepipe System)**, **데이터 사일로(Silo)**, **중복 통계 생산**, **국민 재방문(Re-visitation) 비용**이 발생했다.

반면, **오픈 데이터(Open Data)**는 2009년 오바마 정부 **data.gov** 개방을 기점으로, 2013년 G8 **오픈데이터 헌장(Open Data Charter)**, 2015년 UN **2030 지속가능발전 의제(SDGs)**의 17번 목표로 채택되며 글로벌 흐름이 되었다. 한국은 2013년 「공공데이터법」 제정, 2017년 **데이터·AI 경제 활성화 계획(데이터 산업법)**, 2021년 **한국판 뉴딜**, 2022년 **디지털 플랫폼 정부 실현 전략(범정부 1,422개 서비스)**, 2024년 **데이터주권·AI 기본법**을 통해 4단계 진화(개방 -> 공유 -> 활용 -> 주권)를 거쳐 왔다.

**개방 -> 공유 -> 활용**으로 이어지는 가치사슬(Value Chain)은 **(1) 데이터 생산·수집 -> (2) 표준화·품질검증 -> (3) 개방·공유(Open API) -> (4) 연계·가공(ETL) -> (5) 분석·예측(AI/ML) -> (6) 서비스·재배포**의 6단계로 구성된다. 각 단계에서 **메타데이터·식별자·품질·라이선스**가 일관되게 유지되어야 "한 번 개방, 여러 번 활용(Open Once, Use Many Times)" 원칙이 실현된다.

```text
[오픈 데이터 가치사슬(Value Chain) 및 4단계 진화]

  +----------------------------------------------------------------------+
  | 1단계: 개방(Open, 2013~)    -  data.go.kr / 공공데이터 표준화        |
  | 2단계: 공유(Share, 2017~)   -  행정안전부 표준 API · GovData 품질     |
  | 3단계: 활용(Utilize, 2020~) -  데이터 결합 · MyData · AI학습         |
  | 4단계: 주권(Sovereignty, 2024~) - 데이터안보 · 신뢰기반 · 트레이스  |
  +----------------------------------------------------------------------+

       +----------+    +----------+    +----------+    +----------+
  데이터생산 ->  표준화  ->  개방·공유  ->  연계·가공  ->  분석·AI  ->  서비스화
  (IoT/DB)     (DCAT)    (REST API)   (ETL/CDC)   (ML/DL)    (App/Web)
       |            |            |            |            |            |
       v            v            v            v            v            v
    원시데이터   메타데이터    라이선스     결합·정제    인사이트   새 서비스
   (Raw Data)   (Catalog)   (KOGL/CC)   (Gold Data) (Model)   (B2C/B2B)
       +--------------------------------------------------------------+
                  Open Once, Use Many Times (한 번 개방, 다회 활용)
```

**오래된 패러다임 vs. 새로운 패러다임 비교**

| 구분 | 폐쇄형 데이터(Closed) | 오픈·공공데이터(Open) |
| :--- | :--- | :--- |
| **접근성** | 관할 기관 방문, 종이/CD 제공 | 웹/앱, REST API 실시간 호출 |
| **형식** | HWP, PDF, 종이문서 | JSON, XML, CSV, RDF, GeoJSON |
| **라이선스** | 별도 사용계약 | 공공누리(KOGL 1~4형) 또는 CC |
| **비용** | 실비 청구(자료 복사비) | 원칙 무료, 무제한 |
| **식별자** | 기관별 비표준 ID | 표준 분류체계(KS X 7001)와 URI |
| **갱신** | 분기/반기 1회 배치 | CDC, Kafka 스트리밍 (분 단위) |
| **거버넌스** | 부서 단위 통제 | 데이터 책임관(CDO) + 법제도 |

- **📢 섹션 요약 비유**: 폐쇄형 데이터가 "각 부처 금고에 잠긴 가족사진"이라면, 오픈 데이터는 **"공공도서관의 디지털 책장"** — 누구나 무료로 빌려 읽고, 인용해 2차 저작물을 만들 수 있다. 단, 개인정보가 담긴 사진은 **"흐릿하게 모자이크(비식별화) 처리** 후 비치해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

오픈·공공데이터 활용 시스템의 **4계층 아키텍처**는 다음과 같이 구성된다.

```text
[4계층 오픈·공공데이터 플랫폼 아키텍처]

  +------------------------------------------------------------------------+
  |  ④ 서비스·활용 계층 (Consumption)                                      |
  |    +- 시민 앱  · 챗봇 · 시각화(D3, Superset, Kibana)                  |
  |    +- 민간 서비스 (MaaS, 핀테크, 부동산, 교통)                        |
  |    +- 분석·ML 파이프라인 (Airflow, MLflow)                            |
  +------------------------------------------------------------------------+
  |  ③ 연계·가공 계층 (Processing)                                         |
  |    +- ETL/ELT: Airflow · NiFi · Spark · dbt · Kafka Streams           |
  |    +- 비식별: k-anonymity, ℓ-diversity, t-closeness, DP               |
  |    +- 결합: MyData API · 공공데이터 결합 포털(data.go.kr)             |
  +------------------------------------------------------------------------+
  |  ② 개방·공유 계층 (Distribution)                                       |
  |    +- API Gateway: Kong · Apigee · WSO2 (OAuth2 / API Key)            |
  |    +- 카탈로그: CKAN · DKAN · OpenMetadata + DCAT-AP 3.0              |
  |    +- 파일: CSV / JSON / XML / RDF / Parquet / GeoJSON / GML         |
  +------------------------------------------------------------------------+
  |  ① 데이터 생산 계층 (Source)                                           |
  |    +- 행정DB (Oracle, PostgreSQL, Tibero) · ERP · 센서 IoT            |
  |    +- 문서/이력 · 로그 · 위치(GNSS) · 영상                             |
  |    +- 마스터데이터(MDM): 표준코드, 행정표준코드(KS X 7001)            |
  +------------------------------------------------------------------------+

  [가로 관통(Governance Plane)]
    +- 메타데이터: W3C DCAT-AP 3.0, ISO/IEC 11179, Korea Meta Std
    +- 라이선스: KOGL(Korea Open Government License) 1·2·3·4형
    +- 품질: ISO/IEC 25012 (정확성·완전성·일관성·시점성)
    +- 보안: 가명·익명 처리, 차분프라이버시(DP), PETs
    +- 모니터링: API 사용량, SLA, 데이터 계약 이행률
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **데이터 생산 계층 (Source Layer)** | 행정·IoT·문서·로그 원천 데이터 | RDBMS(Oracle 19c, PostgreSQL 16), NoSQL(MongoDB, Cassandra), 시계열(InfluxDB, TimescaleDB), IoT 프로토콜(MQTT 5.0, CoAP), 행정표준코드(KS X 7001, 행정안전부) |
| **메타데이터·카탈로그 (Catalog)** | 데이터셋 검색·식별·설명 | **W3C DCAT-AP 3.0**(Dataset, Distribution, DataService), OpenMetadata, CKAN, DKAN, OpenSearch, katalog.data.go.kr 표준 메타데이터 14개 필수항목 |
| **개방 게이트웨이 (API Gateway)** | 인증·라우팅·제한·로그 | Kong(nginx+Lua), Apigee(구글), WSO2, OAuth 2.0(Authorization Code, Client Credentials), JWT, API Key, Rate Limiting(예: 1,000 req/sec), OpenAPI 3.0/Swagger 명세 |
| **연계·가공 엔진 (ETL/Streaming)** | 추출·변환·적재·스트리밍 | Apache Airflow(배치), Apache Kafka + Kafka Streams / Flink(실시간), Apache NiFi(데이터 플로우), Spark Structured Streaming, Debezium(CDC, Change Data Capture) |
| **비식별화·가명 처리 (Privacy Engine)** | 개인정보 보호·결합 | **k-익명성(k≥5)**, **ℓ-다양성**, **t-근접성**, **차분프라이버시(DP, ε≤1.0)**, ARX, sdcMicro, OpenPseudonymiser, PETs(Privacy Enhancing Technologies) |
| **품질·거버넌스 (Data Quality)** | 정확성·완전성·시점성 검증 | ISO/IEC 25012, Great Expectations, Apache Griffin, Soda Core, 데이터 계약(Data Contract, Bitol 사양), 데이터 책임관(CDO) 직무 |
| **활용·서비스 (Consumption)** | 시각화·분석·AI·민간서비스 | Apache Superset, Grafana, Kibana, D3.js, Tableau, MLflow, Kubeflow, Android/iOS SDK, 마이데이터 API |
| **보안·컴플라이언스** | 감사·추적·접근제어 | TLS 1.3, IPsec, RBAC/ABAC, 데이터 감사 로그(ELK Stack), ISMS-P, 데이터안보 인증, 한국인터넷진흥원(KISA) 가이드 |

**핵심 원리 및 메커니즘 — FAIR 원칙 + W3C DCAT-AP**

1. **Findable(찾을 수 있어야 함)**: 카탈로그에 등록 시 **고유 영속 URI**(`http://data.go.kr/id/dataset/12345`), 풍부한 메타데이터(제목·설명·키워드·분류), 색인 가능(Elasticsearch).
2. **Accessible(접근 가능해야 함)**: 표준 프로토콜(HTTPS), 필요 시 인증·인가(공공데이터포털 Open API는 API Key), 메타데이터는 영구 보존.
3. **Interoperable(상호운용 가능해야 함)**: 공통 어휘(Controlled Vocabulary, 표준코드), 표현 형식(JSON-LD, RDF/Turtle), 데이터 모델 참조(데이터 사전).
4. **Reusable(재사용 가능해야 함)**: 명확한 라이선스(KOGL, CC-BY 4.0), 출처 명시, 품질·계보(Provenance) 기록.

**메타데이터 항목** (공공데이터포털 표준, 14개 필수): `데이터셋명, 데이터셋 설명, 키워드, 분류, 제공기관, 관리부서, 등록일, 갱신일, 갱신주기, 라이선스, 접근 URL, 파일형식, 인코딩, 언어`.

**라이선스 (KOGL 1~4형 + CC)**:
- **제1유형(KOGL-1, BY)**: 출처 표시 시 상업적 이용, 변형, 2차 저작물 작성 가능
- **제2유형(KOGL-2, BY-ND)**: 출처 표시, 변경 금지
- **제3유형(KOGL-3, BY-NC)**: 출처 표시, 비영리, 변경 가능
- **제4유형(KOGL-4, BY-NC-ND)**: 출처 표시, 비영리, 변경 금지 (가장 제한)
- **CC-BY 4.0, CC0(Public Domain)**: 국제 호환, 글로벌 데이터 교환 시 권장

**핵심 수식 — 데이터 활용 가치(V)**:
`V = (D × C × Q × L) / (Cp + Cr)`
- `D`: 데이터 양(Data Volume) / `C`: 연결성(Connectivity) / `Q`: 품질(Quality Score, 0~1) / `L`: 라이선스 개방도(License Openness, 0~1)
- `Cp`: 수집·정제 비용 / `Cr`: 권리·컴플라이언스 비용
- -> **Q와 L이 높을수록, Cp/Cr이 낮을수록 활용 가치 증가**

**데이터 갱신 5단계**: ① 실시간