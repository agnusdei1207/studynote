---
title: "Chatops Bot Collaboration"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 46
---
> **핵심 인사이트**
> 1. ChatOps는 운영 작업을 채팅 플랫폼에 통합하는 협업 모델 — "대화 주도 개발 운영(Conversation-Driven DevOps)"으로, 슬랙/팀즈 채널에서 명령어로 배포·모니터링·인시던트 대응을 수행하며 팀 전체가 맥락을 실시간 공유한다.
> 2. ChatOps의 핵심 가치는 투명성과 학습 — 모든 운영 작업이 채팅 로그로 기록되어 누가 언제 무엇을 했는지 추적 가능하며, 주니어 엔지니어가 시니어의 운영 패턴을 자연스럽게 학습하는 효과가 있다.
> 3. ChatOps 봇(Hubot/Lita/Errbot)은 단순한 메신저 통합이 아닌 운영 자동화 인터페이스 — CI/CD 파이프라인 트리거, 온콜 알림, 클라우드 리소스 관리, 인시던트 선언을 채팅 명령어 하나로 수행한다.

---

## Ⅰ. ChatOps 개요

```
ChatOps 정의:

전통 DevOps:
  엔지니어 A -> SSH -> 서버 작업
  엔지니어 B -> 모르는 상태
  기록: 없음 또는 별도 문서

ChatOps:
  엔지니어 A -> 슬랙 채널 명령어
  봇 -> 실제 작업 실행
  팀 전체 -> 결과 실시간 확인
  자동 기록: 채팅 로그 = 감사 추적

ChatOps 3대 구성:

  1. 채팅 플랫폼:
  Slack, Microsoft Teams, Discord
  메시지 기반 협업 공간

  2. 챗봇 (ChatBot):
  Hubot (GitHub), Lita, Errbot
  슬랙 앱 (Slack Bolt, Python/Node)

  3. 스크립트/통합:
  봇이 실행하는 실제 스크립트
  CI/CD, 클라우드 API, 모니터링

ChatOps 핵심 명령 예:
  #deploy-prod 채널:
  "hubot deploy myapp v1.2.3 to production"
  -> 봇: 배포 시작, 결과 채널에 보고

  #incident 채널:
  "hubot incident create P1 api-server-down"
  -> 봇: PagerDuty 알림, 티켓 생성, 온콜 호출

  "hubot scale api-server to 10"
  -> AWS Auto Scaling 그룹 크기 변경
```

> 📢 **섹션 요약 비유**: ChatOps는 공개 업무 방송 — 혼자 조용히 서버 작업(전통 방식) 대신, 팀 채팅방에서 "배포할게요!"라고 말하면 봇이 실행 + 전체 공개. 모두가 지켜보는 투명한 운영!

---

## Ⅱ. ChatOps 봇 구현

```
Hubot 기반 ChatOps 예:

Hubot (GitHub, CoffeeScript/JavaScript):
  GitHub 자체 운영 도구로 시작
  슬랙 어댑터로 연결

슬랙 봇 구현 (Python Slack Bolt):

  from slack_bolt import App
  from slack_bolt.adapter.socket_mode import SocketModeHandler
  import subprocess

  app = App(token="xoxb-...")

  @app.message("deploy (\w+) (\w+)")
  def deploy_command(message, say, context):
    app_name = context["matches"][0]
    version = context["matches"][1]

    say(f"Starting deploy: {app_name}:{version}")

    result = subprocess.run(
      ["./deploy.sh", app_name, version],
      capture_output=True, text=True
    )

    if result.returncode == 0:
      say(f"✅ Deploy success: {app_name}:{version}")
    else:
      say(f"❌ Deploy failed: {result.stderr}")

  SocketModeHandler(app, "xapp-...").start()

슬래시 명령어:
  /deploy myapp v1.2.3
  -> 봇이 deploy.sh 실행 -> 결과 보고

버튼/인터랙티브 메시지:
  배포 전 확인 버튼:
  "정말로 production에 배포할까요?"
  [✅ 확인] [❌ 취소]

  -> 실수 방지 UX
```

> 📢 **섹션 요약 비유**: ChatOps 봇은 채팅 비서 — "배포해줘"라고 말하면 비서(봇)가 실행하고 결과 보고. 슬래시 명령어는 채팅방에서 쓰는 특별 주문!

---

## Ⅲ. 인시던트 관리 ChatOps

```
인시던트 ChatOps 흐름:

인시던트 탐지 -> 채팅 알림 -> 대응:

1. 모니터링 알림:
  Datadog -> Slack #alerts
  경보: "API 서버 P99 응답시간 5초 초과"

  봇 자동 생성:
  "🚨 P1 ALERT: api-server latency > 5s
   Incident ID: INC-2024-0301
   Runbook: [링크]
   /incident join INC-2024-0301"

2. 인시던트 채널 자동 생성:
  봇: #incident-2024-0301 채널 생성
  -> 관련자 자동 초대
  -> PagerDuty 온콜 호출
  -> Jira 티켓 자동 생성

3. 진단 명령어:
  "/k8s pods api-namespace"
  -> 봇: kubectl 실행 -> 결과 표시

  "/logs api-server 5m"
  -> 봇: 최근 5분 로그 요약

  "/metrics api-server"
  -> 봇: Datadog 현재 지표

4. 롤백:
  "/rollback api-server to v1.1.9"
  -> 봇: 배포 롤백 실행 -> 결과 보고

5. 인시던트 종료:
  "/incident resolve INC-2024-0301"
  -> 봇: 타임라인 정리, 채널 아카이브
  -> 자동 포스트모텀 템플릿 생성

장점:
  모든 대응 채팅 로그 = 타임라인 자동 완성
  신규 엔지니어 실시간 학습
  원격 팀 동기화 (어디서나 동참)
```

> 📢 **섹션 요약 비유**: 인시던트 ChatOps는 공개 소방 대응 — 화재(장애) 신고(알림) -> 소방관(팀) 자동 소집(PagerDuty) -> 채팅방에서 실시간 소화 작업(명령어) -> 모든 과정 기록!

---

## Ⅳ. ChatOps 보안

```
ChatOps 보안 고려사항:

위험:
  채팅 플랫폼 = 민감한 운영 명령의 통로
  계정 탈취 -> 모든 운영 명령 가능
  채팅 로그 -> 운영 정보 노출

보안 대책:

1. 인증:
  봇 명령어 실행 전 사용자 인증

  a. Slack 사용자 ID 기반 권한:
  AUTHORIZED_USERS = ["U123", "U456"]

  if user_id not in AUTHORIZED_USERS:
    say("권한 없음")
    return

  b. PagerDuty/Okta SSO 연동:
  명령어 실행 전 재인증 요구

  c. RBAC:
  개발자: 개발 환경만
  SRE: 스테이징까지
  시니어 SRE: 전체 프로덕션

2. 명령어 제한:
  위험 명령 블랙리스트
  "delete", "drop" 등 파괴적 명령 차단

3. MFA (다단계 인증):
  프로덕션 변경 = 추가 확인 버튼 + 승인자

4. 채팅 플랫폼 보안:
  기업용 Slack (Enterprise Grid): E2E 암호화
  채팅 로그 보존 정책
  외부 공유 제한

5. 봇 보안:
  봇 토큰 = 환경 변수 (소스코드 금지)
  봇 권한 최소화
  봇 계정 MFA

6. 감사 로그:
  모든 명령어 실행 -> 별도 감사 로그 DB
  SIEM 연동
```

> 📢 **섹션 요약 비유**: ChatOps 보안은 방송국 보안 — 누구나 방송실(채팅방)에 들어오면 큰일. 출입증(인증)+역할별 버튼(RBAC)+이중 확인(MFA)으로 적절한 사람만 적절한 버튼 조작!

---

## Ⅴ. 실무 시나리오 — 스타트업 ChatOps 구축

```
SaaS 스타트업 (엔지니어 15명) ChatOps:

문제:
  배포: SSH 직접 접속, 누가 언제 배포했는지 모름
  장애: 이메일 알림 -> 늦은 대응
  신입: 운영 프로세스 파악 오래 걸림

ChatOps 구축 (4주):

Week 1: 기반 알림 연결
  GitHub -> Slack: PR/배포 알림
  Datadog -> Slack: 경보 알림
  #deploys, #alerts 채널 생성

Week 2: 배포 봇
  Slack Bolt (Python) 개발
  /deploy <app> <version> <env>
  -> GitHub Actions 트리거
  -> 결과 채널 보고

  승인 워크플로:
  프로덕션 배포 -> 팀장 슬랙 버튼 승인

Week 3: 인시던트 봇
  #incident 채널 자동화
  /incident create -> PagerDuty + Jira 연동
  /rollback -> 이전 버전 배포

Week 4: 진단 봇
  /status <service> -> 헬스체크
  /logs <service> <분> -> 최근 로그
  /scale <service> <n> -> 레플리카 조정

결과:
  배포 추적: 100% (슬랙 로그)
  인시던트 MTTR: 45분 -> 18분
  신입 온보딩: 4주 -> 2주 (채팅 로그 학습)
  프로덕션 실수 배포: 월 3건 -> 0건 (승인 프로세스)

  엔지니어 만족도:
  "배포하면서 팀 전체가 보는 게 처음엔 불편했지만
   서로 배우는 효과가 커서 지금은 없으면 안 됨"
```

> 📢 **섹션 요약 비유**: 스타트업 ChatOps는 공개 주방 — 요리사(엔지니어)가 주방(서버)에서 몰래 요리(운영) 대신, 오픈 키친(채팅방)에서 공개. 실수 즉시 보이고, 신입도 보고 배워요!

---

## 📌 관련 개념 맵

```
ChatOps
+-- 채팅 플랫폼
|   +-- Slack
|   +-- Microsoft Teams
+-- 봇 프레임워크
|   +-- Hubot (GitHub)
|   +-- Slack Bolt (Python/Node)
|   +-- Errbot, Lita
+-- 주요 통합
|   +-- CI/CD (GitHub Actions, Jenkins)
|   +-- 모니터링 (Datadog, PagerDuty)
|   +-- 인프라 (Kubernetes, AWS)
+-- 핵심 가치
    +-- 투명성 (감사 로그)
    +-- 팀 학습
    +-- 자동화 인터페이스
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[GitHub Hubot 공개 (2011)]
GitHub 내부 운영 도구
오픈소스 ChatBot 시작
      |
      v
[ChatOps 개념 확립 (2013)]
Jesse Newland (GitHub)
"ChatOps at GitHub" 발표
      |
      v
[Slack 폭발적 성장 (2015~)]
기업 채팅 표준화
슬랙 봇 생태계 성장
      |
      v
[인시던트 자동화 (2018~)]
PagerDuty+Slack 통합
자동 인시던트 채널 생성
      |
      v
[현재: AI ChatOps]
GPT/Copilot 통합 봇
자연어로 운영 명령
인시던트 자동 진단
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ChatOps는 공개 업무 방송 — 서버 작업을 몰래 하지 않고 채팅방에서 공개! 모두가 보니까 실수도 줄고, 서로 배울 수 있어요!
2. ChatOps 봇은 채팅 비서 — "배포해줘" 명령 하면 봇이 실제로 실행하고 결과 보고. 코딩 없이 채팅방에서 서버 조종!
3. 투명성의 힘 — 모든 운영 기록이 채팅 로그로 자동 저장. 신입이 시니어 채팅 로그 보고 배우는 무료 교과서!
