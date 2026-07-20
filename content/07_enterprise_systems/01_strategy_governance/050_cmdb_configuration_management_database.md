---
title: "Configuration Management Database"
date: "2025-01-01"
tags:
  - "CI"
  - "CMDB"
  - "ITIL"
  - "ITSM"
  - "ServiceNow"
  - "asset management"
  - "auto discovery"
  - "configuration management"
  - "studynote-enterprise-systems"
weight: 50
---
> **핵심 인사이트 3줄**
> 1. CMDB(Configuration Management Database)는 IT 인프라의 모든 구성 항목(CI, Configuration Item)과 그 관계를 저장·관리하는 중앙 저장소다.
> 2. ITIL v4에서 CMDB는 ITSM 프로세스(변경, 인시던트, 문제 관리)의 공통 기반 데이터로 작동하며 자동 탐색(Auto-Discovery)이 정확도의 핵심이다.
> 3. CMDB의 성패는 데이터 품질(정확성·최신성)에 달려 있으며, 인간 수동 입력보다 자동화된 에이전트·API 연동이 필수적이다.

---

## Ⅰ. CMDB 개요

### 1.1 구성 항목 (CI)

```
CMDB
+-- 하드웨어 CI: 서버, 네트워크 장비, 스토리지
+-- 소프트웨어 CI: OS, 미들웨어, 애플리케이션
+-- 서비스 CI: 비즈니스 서비스, IT 서비스
+-- 계약 CI: 라이선스, SLA
+-- 관계(Relationship): CI 간 의존성, 위치, 소유
```

### 1.2 CMDB와 자산 관리 차이

| 항목      | 자산 관리 (Asset Mgmt) | CMDB                   |
|----------|----------------------|------------------------|
| 초점      | 재무·계약 정보        | 기술 구성·관계          |
| 범위      | 구매~폐기 생애주기    | 운영 중 구성 관계       |
| 관계 표현 | 미흡                  | 핵심 기능               |

📢 **섹션 요약 비유**: CMDB는 건물 설계도 — 각 방(CI)의 위치와 배관(관계)을 모두 기록해서 수리 시 영향도 파악.

---

## Ⅱ. ITIL과 CMDB 통합

### 2.1 ITSM 프로세스와의 연계

```
인시던트 관리 <--> CMDB <--> 변경 관리
      v                       v
   영향 CI 조회           변경 영향도 분석
      ^                       ^
문제 관리 <---------------------
```

### 2.2 변경 관리 시나리오

```
변경 요청(CR) 접수
    v
CMDB에서 변경 대상 CI 조회
    v
관련 CI 의존성 그래프 분석
    v
영향 받는 서비스 목록 산출
    v
변경 승인 여부 결정 (Change Advisory Board)
```

📢 **섹션 요약 비유**: 건물 배관 공사 전에 설계도(CMDB)를 보고 어느 층이 영향받는지 미리 확인하는 것.

---

## Ⅲ. 자동 탐색 (Auto-Discovery)

### 3.1 탐색 방법

| 방법           | 설명                                        |
|--------------|---------------------------------------------|
| 에이전트 기반   | CI에 에이전트 설치 -> 실시간 정보 수집        |
| 에이전트리스   | SSH/WMI/SNMP로 원격 탐색                    |
| API 통합       | 클라우드(AWS, Azure) API로 리소스 수집       |
| 네트워크 스캔  | NMAP 등으로 IP 범위 스캔                    |

### 3.2 조정(Reconciliation)

여러 탐색 소스의 중복·충돌 데이터를 통합:

```
소스1 (에이전트): hostname=web01, IP=10.0.0.1
소스2 (네트워크 스캔): IP=10.0.0.1, MAC=aa:bb:cc
조정 결과: CI{hostname=web01, IP=10.0.0.1, MAC=aa:bb:cc}
```

📢 **섹션 요약 비유**: 자동 탐색은 드론이 건물 전체를 스캔하는 것 — 사람이 방마다 돌아다니는 것보다 빠르고 정확하다.

---

## Ⅳ. ServiceNow CMDB 구현

### 4.1 CMDB 기본 클래스 계층

```
cmdb_ci (최상위)
+-- cmdb_ci_hardware
|   +-- cmdb_ci_server
|   +-- cmdb_ci_netgear
+-- cmdb_ci_software
|   +-- cmdb_ci_os
|   +-- cmdb_ci_appl
+-- cmdb_ci_service
    +-- cmdb_ci_business_service
```

### 4.2 CMDB Health Dashboard

ServiceNow CMDB Health 점수 (0~100):
- <strong>정확성</strong>: 실제 환경과 데이터 일치도
- **완전성**: 필수 속성 채워진 비율
- **적시성**: 데이터 갱신 주기 준수 여부

📢 **섹션 요약 비유**: CMDB 헬스 점수는 설계도의 신뢰도 — 현실과 다른 설계도(낮은 점수)는 수리 시 오히려 방해가 된다.

---

## Ⅴ. CMDB 거버넌스와 성공 요소

### 5.1 공통 실패 원인

| 실패 원인              | 해결책                         |
|-----------------------|-------------------------------|
| 수동 입력 의존          | 자동 탐색 의무화               |
| 오너십 불명확          | CI Owner 지정 + 책임 체계      |
| 과도한 CI 범위          | 핵심 CI 우선 정의 후 확장      |
| 업데이트 프로세스 미비  | 변경 관리와 CMDB 연동 의무화   |

### 5.2 CMDB 성숙도 모델

```
Level 1: 기본 하드웨어 CI 수동 관리
Level 2: 자동 탐색 도입, 소프트웨어 CI 추가
Level 3: ITSM 전 프로세스 연계
Level 4: 동적 클라우드 CI 자동 갱신
Level 5: AI 기반 이상 CI 탐지·자동 교정
```

📢 **섹션 요약 비유**: CMDB 성숙도는 설계도 관리 수준 — 종이 설계도(Level 1)에서 실시간 3D BIM 모델(Level 5)로 진화.

---

## 📌 관련 개념 맵

```
CMDB
+-- 구성 요소
|   +-- CI (Configuration Item)
|   +-- 관계 (Relationship)
|   +-- 속성 (Attribute)
+-- ITSM 연계
|   +-- 인시던트 관리
|   +-- 변경 관리
|   +-- 문제 관리
+-- 자동화
|   +-- Auto-Discovery
|   +-- Reconciliation
+-- 구현 플랫폼
    +-- ServiceNow
    +-- BMC Helix CMDB
    +-- Micro Focus UCMDB
```

---

## 📈 관련 키워드 및 발전 흐름도

```
수동 자산 대장 (스프레드시트, 1980s~)
     |  ITIL v2 등장
     v
CMDB 개념 정립 (ITIL v2, 2000s)
     |  자동화 요구
     v
Auto-Discovery 도입 (에이전트/에이전트리스)
     |  클라우드 확산
     v
동적 CMDB (클라우드 API 연동, 2010s)
     |  AI/ML 적용
     v
지능형 CMDB (이상 탐지, 자동 교정, 2020s~)
```

**핵심 키워드**: CI, 관계, Auto-Discovery, Reconciliation, ITIL, ServiceNow, CMDB Health

---

## 👶 어린이를 위한 3줄 비유 설명

1. CMDB는 학교 교실 배치도 — 어느 반에 누가 앉고, 복도가 어떻게 연결되는지 전부 적혀 있어.
2. 배치가 바뀌면(자동 탐색) 지도가 즉시 업데이트되어야 선생님이 화재 대피 경로를 정확히 안내할 수 있어.
3. 지도가 틀리면(낮은 CMDB 품질) 비상 시 엉뚱한 방향으로 대피 — 정확성이 전부야.
