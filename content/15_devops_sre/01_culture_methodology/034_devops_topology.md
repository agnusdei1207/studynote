---
title: "DevOps Topology"
date: "2026-03-04"
tags:
  - "studynote-devops-sre"
weight: 34
---
> **핵심 인사이트 3줄**
> 1. DevOps 토폴로지(DevOps Topology)는 조직이 DevOps를 구현하는 다양한 팀 구조 패턴을 분류한 프레임워크로, "Anti-Type A(Dev와 Ops 완전 분리)"부터 "Type 5(NoOps·서버리스)"까지 조직 성숙도별 모델을 제시한다.
> 2. Team Topologies와 연계해 조직의 인지 부하·팀 간 의존성·플랫폼 성숙도를 종합 고려해 적절한 DevOps 토폴로지를 선택해야 하며, 하나의 정답 패턴은 존재하지 않는다.
> 3. 가장 흔한 안티패턴은 "Dev-QA-Ops 3단 사일로"와 "DevOps팀 = Ops팀 이름 변경"으로, 이는 조직 경계를 강화할 뿐 DevOps의 목표인 협업·흐름·피드백 개선을 달성하지 못한다.

---

## Ⅰ. DevOps 토폴로지 유형

### 주요 DevOps 토폴로지 패턴 (Matthew Skelton 분류)

```
Type 1 — Dev와 Ops 완전 통합:
  개발자가 직접 운영·배포 담당 (SRE 모델)
  -> 작은 팀, 마이크로서비스, 클라우드 네이티브

Type 2 — 완전 공유 운영:
  Ops 팀이 개발팀을 임베디드로 지원
  -> 내부 컨설턴트 역할

Type 3 — DevOps 팀이 Ops와 Dev를 잇는 브릿지:
  일시적 구조, 장기적으로는 해체 권장

Type 5 — NoOps:
  서버리스·PaaS로 인프라 추상화, 개발자가 직접 배포
  -> AWS Lambda, Google Cloud Run
```

📢 **섹션 요약 비유**: DevOps 토폴로지는 주방 운영 방식이다 — 요리사가 직접 서빙(Type 1), 전담 웨이터가 팀별 배치(Type 2), 중간 코디네이터 운영(Type 3), 키오스크 자동화(NoOps).

---

## Ⅱ. DevOps 안티패턴 (Anti-Type)

### 가장 흔한 안티패턴

```
Anti-Type A — Dev vs Ops 완전 분리:
  [Dev팀] -> 배포 티켓 -> [Ops팀]
  -> 보안 vs 속도 대립, 배포 병목, "벽 너머로 던지기"

Anti-Type B — DevOps팀 = Ops 이름 변경:
  기존 Ops팀을 "DevOps팀"으로 이름만 변경
  -> 실제 협업 없음, 사일로 유지

Anti-Type C — 개발자만의 DevOps:
  Ops 무시하고 개발자가 인프라 독단 결정
  -> 보안·안정성 문제, Shadow IT

Anti-Type D — QA/Ops 격리:
  QA와 Ops가 별도 게이트로 배포 차단
  -> 배포 리드 타임 수주
```

📢 **섹션 요약 비유**: Anti-Type A는 의사와 간호사가 메모지로만 소통하는 병원이다 — 직접 대화하지 않고 메모(티켓)를 넘기면 환자(소프트웨어) 처치가 늦어진다.

---

## Ⅲ. SRE 모델 — Google의 DevOps 토폴로지

```
Google SRE 모델:
  SRE팀 = 소프트웨어 엔지니어 + 시스템 엔지니어 혼합

  특징:
    - 운영 업무 상한선: 50% (나머지 50%는 개발·자동화)
    - 에러 버짓(Error Budget): 허용 장애 시간 계산
    - SLO 위반 시 기능 배포 동결 -> 신뢰성 우선

  에러 버짓 계산:
    SLO = 99.9% 가용성
    에러 버짓 = (1 - 0.999) × 기간 = 43.8분/월
    -> 장애로 44분 이상 사용 시 다음 달 배포 동결
```

📢 **섹션 요약 비유**: 에러 버짓은 장애 용돈이다 — 한 달에 44분까지는 장애가 허용되고, 용돈(버짓)을 다 쓰면 새 기능 배포(추가 지출)가 금지된다.

---

## Ⅳ. Platform 엔진ering 토폴로지

```
Platform Engineering 모델:
  [Platform Team] -> IDP (Internal Developer Platform)
       v                      v
  인프라 자동화           셀프서비스 포털
  CI/CD 골든 패스         개발자 직접 사용
  관측성 대시보드

  [Stream-aligned Teams] -> IDP를 통해 자율 운영
  -> 개발팀이 인프라 팀에 의존하지 않고 셀프서비스
  -> 개발팀 인지 부하 감소 + Platform Team 중앙 통제 균형
```

📢 **섹션 요약 비유**: Platform 엔진ering은 레고 키트다 — 레고 회사(Platform Team)가 표준 블록(IDP)을 제공하면, 어린이(개발팀)가 설명서 없이도 원하는 것을 만든다.

---

## Ⅴ. DevOps 토폴로지 성숙도 진화

```
단계 1 (초기):
  Dev ↔ Ops 완전 분리 -> Anti-Type A 상태

단계 2 (전환):
  DevOps 챔피언(선도자) 등장
  DevOps 팀 설립 (임시 브릿지)

단계 3 (성장):
  Platform Team 형성
  Stream-aligned Team 자율 배포

단계 4 (성숙):
  DORA 메트릭 Elite 달성
  NoOps (서버리스·IDP 완성)
  지속적 개선 문화 정착
```

📢 **섹션 요약 비유**: DevOps 성숙도는 운전 실력이다 — 처음엔 누군가 가르쳐주고(단계 1~2), 혼자 운전하다가(단계 3), 결국 자율주행(NoOps)까지 발전한다.

---

## 📌 관련 개념 맵

```
DevOps 토폴로지
+-- 주요 유형
|   +-- Type 1 (Dev+Ops 통합)
|   +-- Type 3 (DevOps 브릿지 팀)
|   +-- Type 5 (NoOps, 서버리스)
+-- 안티패턴
|   +-- Anti-Type A (Dev vs Ops 분리)
|   +-- Anti-Type B (이름만 DevOps)
+-- SRE 모델
|   +-- 에러 버짓
|   +-- 50% 운영 상한선
+-- Platform Engineering
    +-- IDP (Internal Developer Platform)
    +-- Team Topologies 연계
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              DevOps 토폴로지 발전 흐름                           |
+--------------+--------------------+-----------------------------+
| 2008년       | DevOps 운동 시작   | Patrick Debois, "Agile Infra"|
| 2013년       | The Phoenix Project| DevOps 소설·실천 프레임워크  |
| 2016년       | SRE 책 (Google)    | Google SRE 토폴로지 공개     |
| 2019년       | Team Topologies    | Skelton·Pais, 팀 설계 체계화 |
| 2020년       | Platform Engineering| IDP·Backstage 등장          |
| 2023년~      | AI Ops             | AI 보조 인프라·자동 운영      |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
Dev·Ops 분리 -> DevOps 토폴로지 -> Team Topologies
    v                  v                  v
티켓 병목          Type 1~5             Stream/Platform
    v
SRE 에러 버짓 -> 신뢰성 관리 -> Platform Engineering -> NoOps
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. DevOps 토폴로지는 주방 팀 구성 방식이다 — 요리사가 직접 서빙하거나(통합), 전담 웨이터가 팀별 배치되거나(분리), 키오스크로 자동화(NoOps)하는 다양한 방식이 있다.
2. Anti-Type A는 의사와 간호사가 메모지로만 소통하는 병원이다 — 개발팀과 운영팀이 티켓으로만 소통하면 환자(소프트웨어)가 제때 치료받지 못한다.
3. SRE 에러 버짓은 장애 용돈이다 — 한 달에 쓸 수 있는 장애 시간이 정해져 있고, 다 쓰면 새 기능 배포가 금지된다.
