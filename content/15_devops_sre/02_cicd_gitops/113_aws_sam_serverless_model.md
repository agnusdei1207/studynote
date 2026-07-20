---
title: "Aws Sam Serverless Model"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 113
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AWS SAM(Serverless Application Model)은 <strong>CloudFormation의 확장 문법</strong>으로, Lambda·API Gateway·DynamoDB·Step Functions 등 서버리스 리소스를 <strong>간결한 YAML로 선언</strong>하고 `sam deploy`로 배포하는 AWS 공식 IaC 도구다.
> 2. **가치**: CloudFormation으로 Lambda를 배포하면 50+ 줄 YAML이 필요하지만, SAM은 `AWS::Serverless::Function` 매크로로 <strong>10줄로 축약</strong>하며, `sam local invoke`로 <strong>로컬에서 Lambda를 Docker 에뮬레이션</strong>하여 배포 전 테스트가 가능하다.
> 3. **판단 포인트**: SAM은 AWS 전용(벤더 종속)이지만 CloudFormation 네이티브이므로 <strong>기존 CF 스택과 완벽 호환</strong>되며, Serverless Framework(멀티클라우드)·SST(TypeScript 네이티브)와 비교하여 AWS 올인 전략에서 가장 자연스러운 선택이다.

---

## Ⅰ. 개요 및 필요성

CloudFormation으로 Lambda + API Gateway를 배포하려면 `AWS::Lambda::Function`, `AWS::Lambda::Permission`, `AWS::ApiGateway::RestApi`, `AWS::ApiGateway::Method` 등 <strong>5~10개 리소스를 각각 정의</strong>해야 한다.

```text
+-------------------------------------------------------+
|    CloudFormation vs SAM: 코드량 비교                  |
+-------------------------------------------------------+
|  [CloudFormation 직접]                                |
|   Lambda Function:     15줄                           |
|   Lambda Permission:    8줄                           |
|   API Gateway RestApi: 10줄                           |
|   API Gateway Method:  12줄                           |
|   API Gateway Stage:    8줄                           |
|   IAM Role:            15줄                           |
|   합계: ~68줄                                         |
|                                                       |
|  [SAM]                                                |
|   AWS::Serverless::Function:                          |
|     Handler, Runtime, Events(Api) -> 10줄              |
|   -> SAM이 나머지를 CloudFormation으로 자동 변환       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: CloudFormation이 레시피의 모든 재료와 조리법을 일일이 적는 요리책이라면, SAM은 "카레 세트"라고만 쓰면 재료가 자동으로 준비되는 밀키트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SAM 핵심 리소스 타입

| SAM 타입 | 확장 대상 | 자동 생성 리소스 |
|:---|:---|:---|
| `AWS::Serverless::Function` | Lambda | IAM Role, CloudWatch Logs |
| `AWS::Serverless::Api` | API Gateway | RestApi, Stage, Deployment |
| `AWS::Serverless::SimpleTable` | DynamoDB | 단일 키 테이블 |
| `AWS::Serverless::StateMachine` | Step Functions | 상태 머신 |

### SAM CLI 핵심 명령어

| 명령 | 역할 |
|:---|:---|
| `sam init` | 프로젝트 스캐폴딩 |
| `sam build` | 종속성 설치 + 패키징 |
| `sam local invoke` | <strong>로컬 Docker에서 Lambda 실행</strong> |
| `sam local start-api` | 로컬에서 API Gateway 에뮬레이션 |
| `sam deploy --guided` | CloudFormation 스택 배포 |

- **📢 섹션 요약 비유**: `sam local invoke`는 요리를 손님에게 내기 전 <strong>주방에서 맛보기</strong>하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | SAM | Serverless Framework | SST |
|:---|:---|:---|:---|
| **클라우드** | AWS 전용 | 멀티클라우드 | AWS 전용 |
| **기반** | CloudFormation | CF + 자체 플러그인 | CDK (TypeScript) |
| **로컬 테스트** | <strong>sam local (Docker)</strong> | serverless-offline | Live Lambda Dev |
| **생태계** | AWS 공식 | 플러그인 풍부 | TypeScript 네이티브 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### CI/CD 통합
```yaml
# GitHub Actions 예시
- run: sam build
- run: sam deploy --no-confirm-changeset --stack-name prod
```

### 안티패턴
- **SAM으로 비서버리스 리소스 관리**: EC2·RDS 등은 SAM이 아닌 CDK/CF로 관리하는 것이 적합.

---

## Ⅴ. 기대효과 및 결론

| 지표 | CF 직접 | SAM | 개선 |
|:---|:---|:---|:---|
| YAML 코드량 | 68줄 | **10줄** | 85% 감소 |
| 로컬 테스트 | 불가 | <strong>Docker 에뮬레이션</strong> | 배포 전 검증 |
| 배포 속도 | 동일 | 동일 (CF 기반) | - |

SAM은 AWS의 공식 서버리스 IaC로, CDK(Cloud Development Kit)와 통합하여 TypeScript/Python으로 SAM 템플릿을 생성하는 **SAM + CDK 하이브리드** 패턴이 주류가 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CloudFormation** | SAM의 기반, SAM 템플릿은 CF로 변환됨 |
| <strong>Lambda</strong> | SAM이 관리하는 핵심 컴퓨팅 리소스 |
| <strong>API Gateway</strong> | SAM Events로 자동 생성되는 HTTP 엔드포인트 |
| <strong>Serverless Framework</strong> | 멀티클라우드 경쟁 IaC 도구 |
| **CDK** | SAM과 통합하여 프로그래밍 언어로 인프라 정의 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CloudFormation (2011) — AWS IaC 표준]
    |
    v
[AWS SAM (2016) — 서버리스 전용 CF 확장]
    |
    v
[SAM CLI (2018~) — 로컬 테스트·디버깅 지원]
    |
    v
[SAM + CDK 통합 (2021~) — TypeScript로 SAM 템플릿 생성]
    |
    v
[현재: SAM Accelerate — 핫 리로드, 빠른 개발 루프]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CloudFormation은 레시피를 **재료부터 조리법까지 전부 적어야** 하는 두꺼운 요리책이에요.
2. SAM은 <strong>"카레 세트"</strong>라고만 쓰면 재료가 자동으로 준비되는 편리한 밀키트예요!
3. `sam local`은 손님에게 내기 전 <strong>주방에서 맛보기</strong>하는 것처럼, 배포 전에 테스트할 수 있답니다!
