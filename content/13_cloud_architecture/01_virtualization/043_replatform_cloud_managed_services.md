---
title: "Replatform Cloud Managed Services"
date: "2026-04-05"
tags:
  - "studynote-cloud-architecture"
weight: 43
---
> **핵심 인사이트**
> 1. Re-platform(재플랫폼)은 6R 전략 중 Rehost(그대로 이전)와 Re-architect(전면 재설계)의 중간 단계로 — 최소한의 코드 변경으로 클라우드 관리형 서비스(RDS, EKS, Elastic Beanstalk 등)로 전환하여 운영 부담을 줄이면서 클라우드 이점을 부분적으로 활용한다.
> 2. Re-platform의 핵심 원칙은 "Core Architecture는 유지, 단 플랫폼 레이어는 매니지드로"로 — 자체 운영 PostgreSQL을 AWS RDS로 교체하면 코드 변경 없이 자동 백업, 멀티 AZ, 패치 관리를 획득하며 DBA 운영 부담을 80% 이상 줄일 수 있다.
> 3. Re-platform은 Rehost 이후 6~12개월 안정화 기간을 거친 후 진행하는 것이 최선이며 — 무리한 동시 마이그레이션은 장애 위험을 배가시키고, 단계적 접근이 클라우드 전환의 현실적 성공 전략이다.

---

## Ⅰ. Re-platform 개념과 위치

```
6R 전략 내 Re-platform 위치:

Retire -> Retain -> Rehost -> Re-platform -> Repurchase -> Re-architect
                   (리프트앤시프트)     ^           (SaaS 전환)   (클라우드 네이티브)
                                       오늘 주제

Re-platform 특징:
  최소한의 코드 변경
  플랫폼/미들웨어 교체
  클라우드 관리형 서비스 활용

  변경 범위:
    ✓ DB 엔진 -> 클라우드 관리형 DB (RDS, Cloud SQL)
    ✓ 앱 서버 -> 컨테이너 (ECS, EKS, Cloud Run)
    ✓ 캐시 -> 관리형 Redis (ElastiCache, Memorystore)
    ✓ 메시지 큐 -> 관리형 (SQS, Pub/Sub)
    ✗ 앱 비즈니스 로직 변경 없음
    ✗ 마이크로서비스 분리 없음 (Re-architect 영역)

Rehost vs Re-platform vs Re-architect:

항목            | Rehost    | Re-platform | Re-architect
----------------+-----------+-------------+------------------
코드 변경       | 없음      | 최소        | 전면 재설계
클라우드 이점   | 낮음      | 중간        | 높음
위험도          | 낮음      | 중간        | 높음
비용 절감       | 없거나 증가| 15~30%     | 40~60%
기간            | 빠름      | 수주~수개월 | 수개월~수년
```

> 📢 **섹션 요약 비유**: Re-platform은 이사 후 가구 재배치 — 집(아키텍처)은 그대로인데, 낡은 장롱(자체 DB)을 빌트인 붙박이장(관리형 RDS)으로 교체. 인테리어 공사는 아님.

---

## Ⅱ. 주요 Re-platform 패턴

```
Re-platform 주요 패턴:

1. DB 서버 -> 관리형 DB 서비스:
   온프레미스 MySQL -> AWS RDS for MySQL
   온프레미스 PostgreSQL -> Amazon RDS for PostgreSQL
   Oracle -> AWS Aurora PostgreSQL (Oracle 탈피)

   획득 이점:
     자동 백업 + Point-in-Time Recovery
     멀티 AZ 고가용성 자동 구성
     보안 패치 자동 적용
     성능 인사이트 (DBA 작업 80% 감소)

2. 앱 서버 -> 컨테이너 서비스:
   VM(Apache Tomcat) -> AWS ECS/EKS

   코드 변경: Dockerfile 작성만 필요
   획득 이점:
     오토스케일링
     블루/그린 배포
     컨테이너 오케스트레이션

3. 자체 Elasticsearch -> OpenSearch Service:
   운영 부담 제거
   자동 확장, 백업

4. Nginx + 자체 SSL -> ALB (Application Load Balancer):
   SSL 인증서 자동 갱신 (ACM)
   WAF 통합

5. 자체 Kafka -> MSK (Managed Streaming for Kafka):
   Kafka 운영 복잡성 제거
   Auto Scaling, 모니터링 통합

Re-platform 시 주의:
  RDS 파라미터 그룹 최적화 필요
  연결 풀링 설정 (RDS Proxy 활용)
  마이그레이션 다운타임 계획 (AWS DMS 활용)
```

> 📢 **섹션 요약 비유**: Re-platform 패턴은 가전제품 업그레이드 — 냉장고(DB)를 자체 수리에서 삼성 서비스센터 AS 계약으로 바꾸는 것. 냉장고 안의 음식(데이터)은 그대로, 관리만 전문가에게.

---

## Ⅲ. RDS 마이그레이션 상세

```
온프레미스 DB -> RDS 마이그레이션:

전략 선택:
  1. 기존 방식 + RDS로 이전
     mysqldump -> S3 -> RDS 복원
     다운타임: 데이터 크기에 따라 수 시간

  2. AWS DMS (Database Migration Service):
     지속적 복제 (Change Data Capture)
     다운타임 최소화 (수분 컷오버)
     이기종 DB 마이그레이션 지원 (Oracle -> Aurora)

DMS 마이그레이션 단계:
  1. 소스 DB 연결 설정
  2. 타겟 RDS 생성 및 연결 설정
  3. 초기 전체 로드 (Full Load)
  4. 지속적 CDC (Change Data Capture) 복제
  5. 지연 최소화 확인 (수 초 이내)
  6. 컷오버 (애플리케이션 연결 변경)
  7. DMS 복제 태스크 중지

RDS 최적화:
  인스턴스 유형:
    범용: db.t3/m6g (소규모)
    메모리 최적화: db.r6g (DB 서버)

  스토리지:
    gp3 (기본): 범용 SSD
    io2: 고 IOPS (OLTP, 금융)

  읽기 복제본:
    읽기 쿼리를 Read Replica로 분산
    -> Primary 부하 감소 50~80%

비용 비교:
  온프레미스: EC2(DB) = $500/월 + DBA 인건비 $5,000/월
  RDS: $800/월 (관리형) + DBA 부분 감소
  실질: 인건비 절감 시 총비용 40% 감소
```

> 📢 **섹션 요약 비유**: DMS 마이그레이션은 물 흐르게 하면서 파이프 교체 — 물 공급 끊지 않고(서비스 지속), 새 파이프(RDS)로 조금씩 물을 유도해서 최종 전환.

---

## Ⅳ. EKS/ECS 컨테이너화

```
VM 앱 -> EKS/ECS 컨테이너화:

ECS vs EKS 선택:

  ECS (Elastic Container Service):
    AWS 전용 오케스트레이터
    설정 간단, AWS 서비스 통합 우수
    소규모 / AWS 전용 팀 적합

  EKS (Elastic Kubernetes Service):
    Kubernetes 표준 API
    이식성 높음 (멀티 클라우드)
    Kubernetes 경험 팀 적합

Re-platform 컨테이너화 단계:

  1. Dockerfile 작성:
     FROM adoptopenjdk:11-jre-hotspot
     COPY target/app.jar /app/app.jar
     ENTRYPOINT ["java", "-jar", "/app/app.jar"]

  2. ECR(Elastic Container Registry)에 이미지 푸시

  3. ECS Task Definition 정의:
     CPU: 1vCPU, Memory: 2GB
     환경변수: DB_URL, API_KEY (Secrets Manager 연동)

  4. ECS Service 생성:
     Desired Count: 3 (최소 인스턴스)
     Auto Scaling: CPU 70% 이상 -> 스케일 아웃

  5. ALB (Application Load Balancer) 연동

  6. CI/CD 파이프라인 연결 (CodePipeline/GitHub Actions)

Fargate 활용:
  EC2 서버 관리 없이 컨테이너 실행
  = Serverless Container
  추가 Re-platform: EC2 기반 ECS -> Fargate 이전
  서버 패치, 용량 관리 부담 제거
```

> 📢 **섹션 요약 비유**: ECS/EKS 컨테이너화는 배달 표준 박스 포장 — 어느 차(서버)에도 실을 수 있는 표준 박스(컨테이너)에 물건(앱)을 담으면, 배달 차(서버)만 바꿔도 됨.

---

## Ⅴ. 실무 시나리오 — E-Commerce Re-platform

```
이커머스 플랫폼 Re-platform 사례:

현황 (Rehost 완료 후):
  EC2: 온프레미스 VM -> AWS EC2 이전 완료 (Rehost)
  RDS: 자체 MySQL -> 자체 운영 MySQL on EC2 (아직 비최적)
  문제: DB 패치/백업 수동, 고가용성 없음

Re-platform 목표:
  MySQL on EC2 -> RDS for MySQL (Multi-AZ)
  Apache Tomcat on EC2 -> ECS Fargate
  Nginx -> ALB + WAF
  Redis on EC2 -> ElastiCache

단계별 실행:

  Week 1-2: RDS 마이그레이션
    DMS 설정 -> 지속 복제 -> 피크 시간 외 컷오버
    다운타임: 15분

  Week 3-4: Redis -> ElastiCache
    설정 변경: redis://old-host -> cluster-endpoint
    코드 변경: 없음 (Redis 클라이언트 호환)

  Week 5-8: Tomcat -> ECS Fargate
    Dockerfile 작성 -> 테스트 -> 스테이징 -> 운영
    ALB 생성 -> ECS Service 연결

  Week 9-10: WAF 적용
    OWASP Top 10 규칙 활성화

  Week 11-12: 모니터링 최적화
    RDS Performance Insights, CloudWatch 대시보드

결과:
  가용성: 99.5% -> 99.95% (멀티 AZ RDS)
  DB 관리 시간: DBA 40시간/월 -> 5시간/월
  인프라 비용: $8,000/월 -> $5,500/월 (-31%)
  스케일링: 수동 -> 오토스케일링 (트래픽 5배 급증 자동 대응)
```

> 📢 **섹션 요약 비유**: Re-platform은 집 수리 공정표 — 전기(DB), 수도(캐시), 방화(WAF) 공사를 순서대로 하나씩 진행. 동시에 다 하면 집에서 못 살아요.

---

## 📌 관련 개념 맵

```
Re-platform
+-- 6R 위치
|   +-- Rehost -> Re-platform -> Re-architect
+-- 주요 패턴
|   +-- DB -> RDS (DMS 마이그레이션)
|   +-- 앱 서버 -> ECS/EKS
|   +-- Redis -> ElastiCache
|   +-- Nginx -> ALB + WAF
+-- 도구
|   +-- AWS DMS, SCT
|   +-- ECS Fargate, EKS
+-- 이점
|   +-- 운영 부담 감소
|   +-- 자동 HA/백업
|   +-- 비용 15~30% 절감
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[클라우드 도입 초기 (2010~)]
Rehost(리프트앤시프트) 중심
빠른 데이터센터 이전
      |
      v
[관리형 서비스 확대 (2013~)]
RDS, ElastiCache, SQS 성숙
Re-platform 경제성 확보
      |
      v
[컨테이너 혁명 (2014~)]
Docker, Kubernetes 등장
ECS/EKS Re-platform 표준화
      |
      v
[서버리스 Re-platform (2017~)]
Fargate, Lambda
서버 관리 완전 제거
      |
      v
[현재: AI/ML 관리형 서비스]
SageMaker, Vertex AI
AI 인프라 Re-platform
FinOps + 지속적 최적화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. Re-platform은 집 리모델링 — 집 구조(앱 로직)는 그대로이지만, 낡은 보일러(DB)를 관리 편한 지역난방(RDS)으로 교체해요!
2. RDS는 DB를 전문 관리 회사에 맡기는 것 — 백업, 보안 패치, 이중화를 AWS가 자동으로 해줘서 DBA 걱정이 줄어요.
3. 단계적으로 진행 — 한 번에 모든 것을 바꾸면 위험하니까, 하나씩 천천히 교체해야 안전해요!
