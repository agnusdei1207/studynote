---
title: "Open Data Fair"
date: "2026-03-03"
tags:
  - "studynote-bigdata"
weight: 247
---
> **핵심 인사이트**
> 1. FAIR 원칙은 2016년 Nature Scientific Data에 발표된 데이터 관리 원칙으로, 연구 및 오픈데이터가 기계 처리 가능하도록 F(Findable)·A(Accessible)·I(Interoperable)·R(Reusable) 4원칙을 충족해야 한다는 기준이다.
> 2. FAIR는 데이터를 '공개'하는 것이 아니라 '재사용 가능하게' 만드는 것에 중점을 두며, 데이터를 공개하지 않더라도 메타데이터를 FAIR하게 유지할 수 있다.
> 3. EU의 연구 데이터 정책, 공공 데이터 포털, 과학 데이터 저장소에 FAIR 원칙이 의무적으로 적용되고 있으며, AI 학습 데이터의 품질 기준으로도 확산되고 있다.

---

## I. FAIR 원칙 개요

```
FAIR Principles (Wilkinson et al., 2016)

F — Findable (발견 가능)
  데이터와 메타데이터에 영구 식별자(PID) 부여
  메타데이터는 검색 엔진이 인덱싱 가능해야 함

A — Accessible (접근 가능)
  표준 통신 프로토콜(HTTP, SPARQL)로 접근
  인증/권한이 필요한 경우 명확히 정의
  메타데이터는 데이터가 삭제되어도 유지

I — Interoperable (상호 운용)
  공개된 표준 어휘/온톨로지 사용
  다른 데이터셋과 연결 가능한 형식 (RDF, JSON-LD)

R — Reusable (재사용 가능)
  풍부한 메타데이터 (데이터 출처, 수집 방법)
  명확한 라이선스 (CC, OGL, ODC)
  도메인 표준 준수
```

| 원칙 | 핵심 요건                  | 실천 예시             |
|-----|--------------------------|----------------------|
| F   | 영구 식별자 (DOI, ORCID)  | DOI 부여, 메타데이터 등록 |
| A   | 개방 프로토콜 접근         | REST API, SPARQL 엔드포인트 |
| I   | 표준 어휘·온톨로지          | Schema.org, Dublin Core |
| R   | 명확한 라이선스·출처        | CC BY 4.0, ODbL |

> 📢 **섹션 요약 비유**: 도서관 책처럼 — 제목·저자·ISBN(Findable), 누구나 빌릴 수 있는 규칙(Accessible), 다른 책과 연결되는 참고문헌(Interoperable), 재출판 허가 명시(Reusable).

---

## II. Findable — 발견 가능성

```
요구사항:
F1. 데이터와 메타데이터에 전역 고유 식별자 부여
    예: DOI (Digital Object Identifier)
        ORCID (연구자 식별자)
        ARK (Archival Resource Key)

F2. 데이터가 풍부한 메타데이터로 기술됨

F3. 메타데이터가 명확하고 명시적으로 데이터를 지시

F4. 데이터/메타데이터가 검색 가능한 저장소에 등록
    예: DataCite, Zenodo, Figshare
```

> 📢 **섹션 요약 비유**: 도서관 책에 ISBN과 저자 정보가 없으면 찾을 수 없듯이 — 데이터도 고유 주소와 설명이 있어야 검색된다.

---

## III. Accessible — 접근 가능성

```
A1. 표준 통신 프로토콜로 식별자를 통해 데이터 검색
    HTTP/HTTPS, FTP (개방형, 무료, 범용)

A1.2. 인증/권한 부여가 필요한 경우 명확히 정의
      (완전 공개가 아니어도 FAIR 가능)

A2. 데이터가 더 이상 없어도 메타데이터는 유지
    -> "tombstone" 페이지로 기록 보존
```

| 시나리오       | FAIR 충족 방법                |
|-------------|------------------------------|
| 완전 공개 데이터 | REST API로 직접 다운로드 허용  |
| 개인정보 포함  | 메타데이터 공개 + 접근 신청 절차 |
| 삭제된 데이터  | DOI 유지 + 삭제 이유 메타데이터 |

> 📢 **섹션 요약 비유**: 폐점한 가게도 주소(DOI)와 "현재 폐점" 안내문(메타데이터)은 남아있어야 한다.

---

## IV. Interoperable & Reusable

```
Interoperable:
  I1. 공식 공유·확장 가능한 지식 표현 언어 사용
      (RDF, OWL, JSON-LD)

  I2. FAIR 원칙 준수 어휘/온톨로지 사용
      (Dublin Core, Schema.org, SNOMED CT)

  I3. 데이터와 관련 데이터·어휘에 대한 링크 포함

Reusable:
  R1. 다양하고 정확한 관련 속성으로 기술
  R1.1. 명확하고 접근 가능한 데이터 사용 라이선스
         CC BY 4.0, ODbL (Open Data Commons)
  R1.2. 상세한 출처 정보 (Provenance)
  R1.3. 도메인 관련 커뮤니티 표준 충족
```

> 📢 **섹션 요약 비유**: 악보(데이터)가 국제 표준 음표(온톨로지)로 쓰여야 전 세계 어느 음악가도 연주(활용)할 수 있다.

---

## V. 실무 적용 — AI 학습 데이터와 FAIR

```
AI 데이터셋 FAIR 체크리스트:

F: DOI 부여, Hugging Face / Zenodo에 등록
A: 다운로드 API, 라이선스 명시, 접근 조건 공개
I: 표준 포맷(CSV, Parquet, JSON), 스키마 문서화
R: 출처(원본 데이터, 수집 방법), 라이선스 (CC BY)

EU AI Act: 고위험 AI 시스템의 학습 데이터는
           FAIR 원칙 기반 문서화 의무화 예정
```

| 플랫폼           | FAIR 지원              |
|----------------|------------------------|
| Zenodo         | DOI 자동 발급, 메타데이터 |
| Hugging Face   | 데이터셋 카드, 라이선스  |
| CKAN           | 공공 데이터 포털 표준    |
| OpenAIRE       | EU 연구 데이터 저장소    |

> 📢 **섹션 요약 비유**: AI 학습용 레시피(데이터)도 재료 출처·분량·조리법(메타데이터)을 정확히 적어야 다른 요리사가 재현할 수 있다.

---

## 📌 관련 개념 맵

```
FAIR 원칙
+-- Findable: 영구 식별자, 메타데이터 검색
|   +-- DOI, ORCID, ARK
|   +-- DataCite, Zenodo 저장소
+-- Accessible: 개방 프로토콜, 인증 정의
|   +-- HTTP/HTTPS REST API
|   +-- 메타데이터 영구 보존
+-- Interoperable: 표준 어휘/온톨로지
|   +-- RDF, JSON-LD, Dublin Core
|   +-- Schema.org, 도메인 표준
+-- Reusable: 라이선스, 출처, 표준
    +-- CC BY, ODbL, ODC
    +-- 데이터 출처 (Provenance)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 오픈데이터 운동 (2000s)]
Creative Commons, OGD (Open Government Data)
      |
      v
[FAIR 원칙 발표 (2016)]
Wilkinson et al., Nature Scientific Data
기계 가독성 + 재사용성에 초점
      |
      v
[EU Horizon 2020 FAIR 채택 (2017)]
연구 데이터 관리 의무화
      |
      v
[오픈데이터 포털 FAIR 통합]
data.go.kr, data.europa.eu
CKAN 기반 메타데이터 표준화
      |
      v
[현재: AI 데이터 품질 기준으로 확산]
EU AI Act, 연구 재현성 위기 대응
FAIR + CARE (원주민 데이터 권리) 통합 논의
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. FAIR 원칙은 데이터를 도서관 책처럼 잘 정리해서 누구나 찾고 쓸 수 있게 만드는 규칙이에요.
2. 책에 ISBN, 저자, 빌리는 방법, 저작권이 다 적혀있어야 유용하듯이, 데이터도 마찬가지예요.
3. AI가 잘 배우려면 학습 데이터도 FAIR하게 정리되어야 한답니다!
