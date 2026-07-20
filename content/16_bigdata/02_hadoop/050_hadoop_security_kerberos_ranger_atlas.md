---
title: "Hadoop Security Kerberos Ranger Atlas"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 50
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Hadoop 보안은 3개 레이어로 구성된다. Kerberos(인증 — 누구인가?), Apache Ranger(권한 부여 — 무엇을 할 수 있는가?), Apache Atlas(데이터 거버넌스 — 어떤 데이터인가·어떻게 이동하는가?)가 완전한 엔터프라이즈 보안 스택을 형성한다.
> 2. **가치**: 초기 Hadoop은 보안이 없는 "Simple Security Mode"만 지원했다. Kerberos 통합으로 인증, Ranger로 세밀한 컬럼·행 레벨 접근 제어, Atlas로 데이터 계보(Lineage) 추적이 가능해지면서 금융·의료 규제 환경에서도 사용 가능한 플랫폼으로 발전했다.
> 3. **판단 포인트**: 현대 클라우드 레이크하우스 환경에서는 Hadoop Kerberos 대신 IAM(Cloud Identity), Ranger 대신 Unity Catalog·LakeFormation이 대안이 된다. 온프레미스 Hadoop 클러스터 유지 조직에서는 Kerberos+Ranger+Atlas 스택이 여전히 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+----------------------------------------------------------+
|           Hadoop 보안 3개 레이어                          |
+----------------------------------------------------------+
|                                                           |
|  레이어 1: 인증 (Authentication)                          |
|  +--------------------------------------------------+   |
|  |  Kerberos KDC (Key Distribution Center)          |   |
|  |  -> TGT 티켓 발급 -> 서비스 티켓으로 HDFS/YARN 접근|   |
|  +--------------------------------------------------+   |
|                    v                                      |
|  레이어 2: 권한 부여 (Authorization)                       |
|  +--------------------------------------------------+   |
|  |  Apache Ranger — 정책 기반 세밀한 접근 제어       |   |
|  |  (DB·테이블·컬럼·행 레벨 정책)                   |   |
|  +--------------------------------------------------+   |
|                    v                                      |
|  레이어 3: 데이터 거버넌스 (Governance)                    |
|  +--------------------------------------------------+   |
|  |  Apache Atlas — 메타데이터·계보·분류·태그         |   |
|  |  (개인정보 컬럼 자동 태그, 데이터 흐름 추적)      |   |
|  +--------------------------------------------------+   |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Hadoop 보안은 회사 출입 관리 시스템이다. 출입 카드(Kerberos — 신원 확인), 층별 권한(Ranger — 접근 가능 구역), 방문 기록부(Atlas — 어디서 어디로 이동했는지 추적) 3단계로 구성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Kerberos 인증 흐름

```text
사용자     KDC(AS)           KDC(TGS)        서비스
  |         |                  |               |
  | kinit   |                  |               |
  |--------->| TGT 발급         |               |
  |<---------|                  |               |
  |         | TGT + 서비스 요청 |               |
  |-----------------------------> 서비스 티켓 발급|
  |<-------------------------------------------|
  |                                서비스 티켓으로 HDFS 접근|
  |------------------------------------------->|
```

### Apache Ranger 세밀한 접근 제어

```text
정책 예시 (Hive 테이블):
  - 데이터 분석팀: sales_db.orders 테이블 SELECT
  - 개인정보팀: customer_db.users.phone 컬럼 마스킹 처리
  - 감사팀: 모든 쿼리 감사 로그 활성화
  - DBA: DDL 권한

행 레벨 필터:
  - 지역 관리자: WHERE region = '${user.region}' 자동 적용
```

- **📢 섹션 요약 비유**: Apache Ranger는 스마트 사무실 열쇠 시스템이다. 마케팅 팀은 마케팅 데이터만 읽기 가능, 개인정보가 있는 컬럼은 자동으로 별표(**)로 마스킹, 감사팀은 모든 접근 기록을 볼 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | 온프레미스 Hadoop | 클라우드 레이크하우스 |
|:---|:---|:---|
| 인증 | Kerberos | IAM (AWS/Azure/GCP) |
| 권한 부여 | Ranger | LakeFormation / Unity Catalog |
| 거버넌스 | Atlas | AWS Glue Catalog / Purview |

- **📢 섹션 요약 비유**: 온프레미스 Hadoop 보안 vs 클라우드 보안은 사내 보안 시스템 vs 클라우드 보안 서비스다. 클라우드는 CSP가 인증·권한·거버넌스를 관리형 서비스로 제공해서 운영 부담이 줄어든다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Apache Atlas 데이터 계보 (Data Lineage)

```text
데이터 소스 -> ETL 변환 -> DW 테이블 -> 분석 보고서

Atlas 자동 추적:
  orders.csv -> (Spark ETL) -> sales_fact -> (HiveQL) -> monthly_report

규제 준수 활용:
  "이 개인정보 컬럼이 어느 다운스트림 테이블에 흘렀는가?"
  -> GDPR 데이터 파악, 개인정보 삭제 영향 범위 분석
```

### 실무 배포 구성
```text
HDP (Hortonworks Data Platform) / CDP (Cloudera Data Platform):
  Kerberos + Ranger + Atlas + Knox(게이트웨이) 번들 제공

Knox Gateway:
  -> 외부에서 Hadoop 클러스터 접근 시 단일 진입점 (API Gateway)
  -> TLS 종단, SSO 통합
```

- **📢 섹션 요약 비유**: Apache Atlas 데이터 계보는 식품 이력 추적 시스템이다. 원재료(원본 데이터)에서 완제품(분석 보고서)까지 모든 가공 단계를 추적해서 "이 숫자가 어떤 원본 데이터에서 왔나?" 역추적이 가능하다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **규제 준수** | GDPR·개인정보보호법·금융 규제 충족 |
| **세밀한 접근 제어** | 컬럼·행 레벨 정책으로 최소 권한 |
| <strong>데이터 신뢰성</strong> | 계보 추적으로 데이터 품질·영향 파악 |

현대 데이터 레이크하우스에서 Hadoop Kerberos는 클라우드 IAM으로, Ranger는 Unity Catalog/LakeFormation으로, Atlas는 Microsoft Purview/OpenMetadata로 대체되는 추세다. 온프레미스 Hadoop 클러스터 유지 조직에서는 Kerberos+Ranger+Atlas 스택이 여전히 표준 보안 아키텍처다.

- **📢 섹션 요약 비유**: Hadoop 보안 스택 진화는 자동차 안전 기술 발전과 같다. 구형 Hadoop(안전벨트만 있는 차)에서 Kerberos+Ranger+Atlas(에어백·ABS·차선 유지 시스템 장착 차)로 발전했고, 클라우드 레이크하우스는 완전 자율주행 안전 시스템으로 업그레이드된 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Kerberos</strong> | Hadoop 네트워크 인증 프로토콜 |
| **Apache Ranger** | 정책 기반 세밀한 접근 제어 |
| **Apache Atlas** | 메타데이터·계보·분류·태그 |
| **Knox Gateway** | Hadoop 클러스터 단일 진입점 |
| <strong>Unity Catalog</strong> | 클라우드 레이크하우스 통합 거버넌스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Simple Security Mode — 인증 없는 초기 Hadoop]
    |
    v
[Kerberos 통합 — 네트워크 신원 인증]
    |
    v
[Apache Ranger — 정책 기반 세밀한 접근 제어]
    |
    v
[Apache Atlas — 데이터 거버넌스·계보 추적]
    |
    v
[Unity Catalog/LakeFormation — 클라우드 통합 거버넌스]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Hadoop 보안은 출입 카드(Kerberos), 층별 권한(Ranger), 방문 기록부(Atlas) 3단계 시스템이에요!
2. Ranger는 "마케팅팀은 마케팅 데이터만, 개인정보는 자동으로 숨김"처럼 스마트하게 접근을 제어해요!
3. Atlas는 "이 데이터가 어디서 왔고 어디로 갔나" 식품 이력 추적처럼 모든 데이터 흐름을 기록해요!
