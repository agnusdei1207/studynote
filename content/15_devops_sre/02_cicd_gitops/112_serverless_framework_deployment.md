---
title: "Serverless Framework Deployment"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 112
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Serverless Framework는 AWS Lambda·Azure Functions·GCP Cloud Functions 등 <strong>FaaS(Function as a Service)의 인프라·코드·이벤트 트리거를 <code>serverless.yml</code> 하나로 선언</strong>하고, `sls deploy` 한 줄로 클라우드에 배포하는 오픈소스 IaC(Infrastructure as Code) 도구다.
> 2. **가치**: Lambda 함수 1개를 수동 배포하려면 IAM Role·API Gateway·CloudWatch·DLQ를 콘솔에서 각각 설정해야 하지만, Serverless Framework는 YAML 선언만으로 <strong>모든 종속 리소스를 CloudFormation 스택으로 자동 생성</strong>한다.
> 3. **판단 포인트**: Serverless Framework(범용)·AWS SAM(AWS 전용)·SST(TypeScript 네이티브)의 트레이드오프를 이해하고, <strong>Cold Start 최적화·모니터링 통합·CI/CD 파이프라인 연결</strong>까지 고려해야 프로덕션 수준이 된다.

---

## Ⅰ. 개요 및 필요성

FaaS는 서버 관리 없이 함수 단위로 코드를 실행하지만, 실제 배포 시에는 <strong>IAM 정책·API Gateway 엔드포인트·DLQ(Dead Letter Queue)·VPC 설정·환경 변수</strong> 등 수십 가지 인프라를 구성해야 한다.

```text
+-------------------------------------------------------+
|    수동 배포 vs Serverless Framework 배포               |
+-------------------------------------------------------+
|  [수동 배포]                                          |
|   AWS 콘솔 -> Lambda 생성 -> IAM Role 설정             |
|   -> API Gateway 연동 -> CloudWatch 설정               |
|   -> DLQ 연결 -> 환경 변수 -> (30분+)                   |
|                                                       |
|  [Serverless Framework]                               |
|   serverless.yml 작성 -> sls deploy -> 끝!             |
|   모든 리소스가 CloudFormation으로 자동 생성           |
|   (3분)                                               |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 수동 배포는 레고 설명서 없이 100조각을 맞추는 것이고, Serverless Framework는 설명서(YAML) 대로 로봇이 자동으로 조립하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### serverless.yml 핵심 구조

```yaml
service: my-api
provider:
  name: aws
  runtime: nodejs20.x
  region: ap-northeast-2
functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: /hello
          method: get
    timeout: 10
    memorySize: 256
```

### 프레임워크 비교

| 도구 | 멀티클라우드 | 언어 | 특징 |
|:---|:---|:---|:---|
| <strong>Serverless Framework</strong> | ✅ (AWS/Azure/GCP) | YAML | 범용, 플러그인 생태계 풍부 |
| <strong>AWS SAM</strong> | AWS 전용 | YAML | CloudFormation 네이티브 |
| **SST (v3)** | AWS 전용 | TypeScript | 타입 안전, 핫 리로드 |
| **Pulumi** | ✅ | 범용 언어 | 코드로 인프라 (TypeScript/Python) |

- **📢 섹션 요약 비유**: Serverless Framework는 만능 리모컨(멀티클라우드)이고, SAM은 삼성 TV 전용 리모컨이며, SST는 스마트폰 앱(타입 안전)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 콘솔 | Serverless Framework |
|:---|:---|:---|
| **배포 시간** | 30분+ | **3분** |
| **재현성** | 수동 (실수 위험) | **YAML 선언, 100% 재현** |
| <strong>버전 관리</strong> | 불가 | <strong>Git으로 IaC 이력 관리</strong> |
| <strong>롤백</strong> | 수동 복원 | <strong>sls rollback (자동)</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### CI/CD 통합 체크리스트
1. **GitHub Actions**: `on: push` -> `sls deploy --stage prod`.
2. **스테이지 분리**: `--stage dev/staging/prod`로 환경별 독립 스택.
3. <strong>Cold Start 최적화</strong>: Provisioned Concurrency 또는 WarmUp 플러그인.
4. <strong>모니터링</strong>: Serverless Dashboard 또는 Datadog Lambda Layer.

### 안티패턴
- **단일 거대 함수**: Lambda 1개에 모든 로직 -> 모놀리스 회귀. 함수별 단일 책임 원칙 준수.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 배포 | Serverless Framework | 개선 |
|:---|:---|:---|:---|
| 배포 시간 | 30분+ | **3분** | 90% 단축 |
| 인프라 재현성 | 낮음 | **100%** | IaC 확보 |
| 운영 비용 | 인스턴스 상시 과금 | **요청당 과금** | 유휴 비용 0 |

Serverless Framework v4는 AI 기반 자동 최적화(메모리·타임아웃 자동 튜닝)를 내장하여, 함수 성능과 비용의 최적점을 자동으로 찾아주는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>FaaS (Lambda)</strong> | Serverless Framework가 배포하는 대상 |
| <strong>IaC (Infrastructure as Code)</strong> | YAML 선언으로 인프라를 코드화 |
| **CloudFormation** | AWS에서 YAML -> 실제 리소스 생성 엔진 |
| <strong>API Gateway</strong> | Lambda 트리거, HTTP 엔드포인트 자동 생성 |
| <strong>Cold Start</strong> | FaaS 최초 실행 시 지연, 최적화 필수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[AWS Lambda 출시 (2014) — FaaS 개념 탄생]
    |
    v
[Serverless Framework (2015) — FaaS IaC 자동화]
    |
    v
[AWS SAM (2016) — AWS 전용 FaaS 배포 도구]
    |
    v
[SST (2021~) — TypeScript 네이티브, 핫 리로드]
    |
    v
[현재: AI 기반 자동 튜닝 — 메모리·타임아웃 최적화 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고를 만들 때 <strong>설명서 없이 100조각</strong>을 혼자 맞춰야 했어요.
2. Serverless Framework는 <strong>설명서(YAML)</strong>를 주면 로봇이 자동으로 조립해줘요!
3. 덕분에 개발자는 레고 디자인(코드)에만 집중하고, 조립(배포)은 로봇에게 맡길 수 있답니다!
