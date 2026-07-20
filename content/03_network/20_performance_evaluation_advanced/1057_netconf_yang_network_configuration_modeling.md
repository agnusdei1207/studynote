---
title: "Netconf Yang Network Configuration Modeling"
date: "2026-06-07"
tags:
  - "network"
  - "studynote-network"
weight: 1057
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: YANG은 네트워크 설정의 구조와 규칙을 정의하는 모델이고, NETCONF는 그 모델을 장비에 안전하게 주입하는 전송 프로토콜이다.
> 2. **가치**: CLI 수작업과 SNMP (Simple Network Management Protocol) 중심의 한계를 넘어, 선언형 설정과 트랜잭션 롤백을 가능하게 한다.
> 3. **판단 포인트**: 데이터 모델의 검증, SSH (Secure Shell) 기반 전송, candidate/running datastore 분리가 핵심이다.

---

## Ⅰ. 개요 및 필요성

기존 CLI (Command Line Interface) 방식은 장비마다 명령어가 다르고, 사람이 직접 타이핑해야 해서 실수가 잦다.

SNMP (Simple Network Management Protocol)는 모니터링에는 강하지만, 복잡한 설정을 안전하게 쓰는 데는 약했다. 그래서 설정 자동화를 위한 새로운 규격이 필요했다.

- **📢 섹션 요약 비유**: 예전에는 네트워크 장비를 하나하나 손으로 만졌다면, 이제는 도면을 넣고 자동 조립하는 시대다.

---

## Ⅱ. YANG의 역할

YANG은 데이터 모델링 언어다. 즉, 네트워크 장비의 설정이 어떤 트리 구조를 가져야 하는지, 어떤 값이 허용되는지 정의한다.

```text
루트
 +- interfaces
 |   +- interface
 |   +- state
 +- routing
 +- system
```

YANG은 설정 값의 범위, 필수 항목, 중복 여부까지 표현할 수 있다. 그래서 잘못된 설정을 장비에 넣기 전에 구조 단계에서 걸러낼 수 있다.

- **📢 섹션 요약 비유**: YANG은 건물을 짓기 전에 필요한 방의 모양과 크기를 미리 적어 두는 설계도다.

---

## Ⅲ. NETCONF의 전송과 트랜잭션

NETCONF는 YANG 모델을 실제 장비에 전달하는 프로토콜이다. 보통 SSH 위에서 동작하고, XML (Extensible Markup Language) 형식으로 메시지를 주고받는다.

주요 특징은 다음과 같다.

- `edit-config`로 설정을 바꾼다.
- `candidate` datastore에서 먼저 검증할 수 있다.
- `commit`으로 실제 `running` datastore에 반영한다.
- `rollback`으로 실패한 변경을 되돌릴 수 있다.

```text
Controller
   v SSH
NETCONF
   v XML
Network Device
```

- **📢 섹션 요약 비유**: 바로 벽에 못을 박는 대신, 임시 종이에 먼저 그려 보고 마지막에 확정하는 방식이다.

---

## Ⅳ. RESTCONF와 현대 자동화

RESTCONF는 NETCONF의 모델을 HTTP (Hypertext Transfer Protocol)와 JSON (JavaScript Object Notation) 스타일로 다루게 한 방식이다.

이 방식은 웹 개발자와 자동화 엔지니어가 익숙한 도구를 그대로 쓸 수 있게 해 준다. 그래서 네트워크 설정도 API처럼 다루는 흐름으로 이어진다.

이 흐름은 Software Defined Networking (SDN)과도 잘 맞는다. 중앙 제어기에서 네트워크를 선언형으로 관리하기 때문이다.

- **📢 섹션 요약 비유**: 무거운 서류 대신 앱 화면에서 바로 입력하고 저장하는 느낌이다.

---

## Ⅴ. 실무 적용과 비교

NETCONF/YANG는 장비 간 설정 일관성이 중요할 때 강하다. 대규모 라우터, 스위치, WAN 구성, 정책 배포에 특히 적합하다.

CLI와 비교하면 사람이 직접 치는 작업이 줄고, SNMP와 비교하면 설정 반영과 검증이 훨씬 강력하다. 다만 초반에 모델을 잘 만들어야 하고, 벤더별 지원 차이도 확인해야 한다.

- **📢 섹션 요약 비유**: 같은 열쇠로 여러 문을 열 수 있으면 편하지만, 그 열쇠 규격을 먼저 잘 맞춰야 한다.

---

## 관련 개념 맵

```text
YANG (모델)
   v
NETCONF (전송)
   v
candidate / running datastore
   v
RESTCONF / SDN 자동화
```

---

## 관련 키워드 및 발전 흐름도

1. CLI 수동 설정 -> 사람 의존과 오류 증가
2. SNMP 중심 관리 -> 모니터링은 되지만 설정 자동화는 약함
3. YANG 모델링 -> 구조와 제약을 선언
4. NETCONF 트랜잭션 -> 안전한 반영과 롤백
5. RESTCONF / SDN -> 웹 친화적 자동화와 중앙 제어 확장

---

## 어린이를 위한 3줄 비유 설명

YANG은 장난감 조립 설명서예요.
NETCONF는 그 설명서를 실제 장난감에 넣어 조립하는 우체부예요.
그래서 사람 손으로 하나씩 누르지 않아도 한 번에 맞출 수 있어요.
