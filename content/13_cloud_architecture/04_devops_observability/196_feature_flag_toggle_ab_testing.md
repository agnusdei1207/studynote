---
title: "Feature Flag / Toggle"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 196
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 코드 재배포 없이 런타임에 특정 기능을 ON/OFF하거나 특정 사용자 그룹에게만 노출하는 소프트웨어 조건 스위치다.
> 2. **가치**: 배포(Deploy)와 출시(Release)를 분리하여, 코드가 프로덕션에 존재하더라도 비즈니스 결정 시점에 기능을 노출할 수 있는 유연성을 제공한다.
> 3. **판단 포인트**: 피처 플래그는 기술 부채가 될 수 있으므로, 플래그 생성 시 만료일·책임자·용도를 명시하고 완료 후 반드시 코드에서 제거해야 한다.

---

## Ⅰ. 개요 및 필요성

피처 플래그(Feature Flag), 또는 피처 토글(Feature Toggle)은 소프트웨어 개발에서 새 기능을 코드에 포함하되 런타임 조건에 따라 활성/비활성화하는 기술이다. Martin Fowler의 블로그 포스트 "Feature Toggles (aka Feature Flags)"에서 체계적으로 정리된 개념이다.

가장 중요한 개념은 <strong>배포와 출시의 분리(Decouple Deployment from Release)</strong>이다. 전통적으로는 "코드 배포 = 기능 출시"였지만, 피처 플래그를 사용하면 신기능 코드를 미리 프로덕션에 배포해두고 마케팅·비즈니스 일정에 맞춰 플래그를 ON으로 전환하여 출시할 수 있다.

Facebook, Google, Netflix 등은 수천 개의 피처 플래그를 동시에 운영하며, 일부 회사는 A/B 테스트·퍼스널라이제이션·점진적 출시 모두를 피처 플래그 시스템 위에서 구현한다. LaunchDarkly, Unleash, Flagsmith, AWS AppConfig 등이 대표적인 피처 플래그 관리 플랫폼이다.

📢 **섹션 요약 비유**: 피처 플래그는 새 조명을 집에 설치해두고 전기 연결만 잠깐 끊어두는 것과 같다. 조명은 이미 설치됐지만 스위치만 ON/OFF하면 언제든지 켤 수 있다. 공사(배포)와 개통(출시)이 완전히 분리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 피처 플래그 유형 분류

| 유형 | 수명 | 사용 목적 |
|:---|:---:|:---|
| Release Toggle | 단기 (수 일~수 주) | 미완성 기능 숨기기, Trunk-based 개발 |
| Experiment Toggle | 중기 (수 주~수 달) | A/B 테스트, 통계적 검증 |
| Ops Toggle | 단기~장기 | 운영 비상 스위치, 기능 긴급 비활성화 |
| Permission Toggle | 장기 | 사용자 등급별 기능 차등 제공 (Premium) |

### 피처 플래그 동작 구조

```
  +-----------------------------------------------------+
  |              Feature Flag 관리 서버                   |
  |  (LaunchDarkly / Unleash / AWS AppConfig)            |
  |                                                      |
  |  플래그 정의: new_checkout_flow                       |
  |    - 기본값: OFF                                     |
  |    - 대상: user_segment = "beta_users"               |
  |    - 가중치: 10% 랜덤 사용자                          |
  +----------------------+------------------------------+
                         | SDK 폴링 or 웹훅
                         v
  +------------------------------------------------------+
  |                 애플리케이션 코드                       |
  |                                                      |
  |  if (featureFlag.isEnabled("new_checkout_flow",      |
  |                             currentUser)) {          |
  |      showNewCheckout();   // 신기능                  |
  |  } else {                                            |
  |      showOldCheckout();   // 기존 기능               |
  |  }                                                   |
  +------------------------------------------------------+
```

### LaunchDarkly SDK 예시 (Java)

```java
LDClient client = new LDClient("sdk-key");
LDContext context = LDContext.builder("user-123")
    .set("plan", "premium")
    .build();

boolean showNewUI = client.boolVariation("new-checkout-ui", context, false);

if (showNewUI) {
    renderNewCheckout();
} else {
    renderLegacyCheckout();
}
```

📢 **섹션 요약 비유**: 피처 플래그 관리 서버는 마치 중앙 전등 제어반과 같다. 건물 안 어떤 방의 어떤 조명이든 원격에서 ON/OFF할 수 있고, 특정 층만, 특정 호실만, 또는 모든 방 동시에 제어 가능하다.

---

## Ⅲ. 비교 및 연결

### 피처 플래그 vs 카나리 배포 vs A/B 테스트

| 기준 | Feature Flag | Canary Release | A/B Test |
|:---|:---|:---|:---|
| 제어 단위 | 기능(Feature) | 서버 버전 | UI 변형 |
| 변경 방법 | 런타임 스위치 | 배포 | 런타임 스위치 |
| 통계 검증 | 선택적 | 아님 | 필수 |
| 즉시 롤백 | ✅ (플래그 OFF) | 빠름 | ✅ |
| 코드 재배포 | ❌ 불필요 | ✅ 필요 | ❌ 불필요 |

### 피처 플래그 기술 부채 관리

```
피처 플래그 생성 규칙:
  ✅ 플래그명: JIRA 티켓 ID 포함 (ex: PROJ-123-new-checkout)
  ✅ 만료일: 생성 시 설정 (ex: 2026-07-01)
  ✅ 담당자: 팀 / 개인 명시
  ✅ 용도: Release / Experiment / Ops / Permission

플래그 제거 시점:
  - 전체 사용자 100% 적용 후 2주 이내 코드에서 제거
  - 분기별 Stale Flag 감사 수행
```

📢 **섹션 요약 비유**: 피처 플래그를 관리하지 않으면 집 안에 쓸모없는 스위치가 수백 개 쌓이는 것과 같다. 어떤 스위치가 뭘 켜는지 모르게 되고, 잘못 건드리면 예상치 못한 곳이 꺼진다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>Trunk-based Development(TBD)와의 연계</strong>:
- 기능 브랜치 없이 모든 개발자가 main/trunk에 직접 커밋
- 미완성 기능은 피처 플래그로 숨겨서 CI/CD 파이프라인 유지
- 장기 브랜치(feature branch)의 merge conflict 문제 해결

<strong>킬 스위치(Kill Switch) 활용</strong>:
```
프로덕션 장애 시:
  1. 원인: 새 기능 v2 결제 로직 버그
  2. 배포 롤백 없이 즉시: feature_flag["new_payment_v2"] = OFF
  3. 결과: 1분 내 장애 격리, 구 결제 로직 즉시 복원
  4. 이후: 수정 후 다음 배포 시 플래그 재활성화
```

**실무자 판단 포인트**:
- 피처 플래그는 Ops Toggle로 "비상 차단 스위치" 역할을 하여 배포 없는 긴급 장애 대응에 핵심적이다.
- 플래그 규칙이 복잡해지면 "피처 플래그 지옥(Flag Hell)"이 발생하므로, 단순하게 유지하고 주기적으로 정리해야 한다.
- Permission Toggle은 SaaS 제품의 Freemium/Premium 기능 분리에서 비즈니스 핵심 인프라가 된다.

📢 **섹션 요약 비유**: 피처 플래그의 킬 스위치는 공장의 비상 정지 버튼과 같다. 기계(새 기능)에 문제가 생겼을 때 전체 공장(서비스)을 멈출 필요 없이, 해당 기계만 즉시 멈출 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 배포·출시 분리 | 기술 일정과 비즈니스 일정의 독립적 관리 |
| 즉각적 롤백 | 재배포 없이 플래그 OFF로 기능 비활성화 |
| 안전한 점진 출시 | 내부 -> 베타 -> 전체 단계적 기능 노출 |
| A/B 테스트 통합 | 기능 효과를 데이터로 검증 |

피처 플래그는 현대 DevOps에서 "소프트웨어 출시의 리모컨"이 되었다. 적절히 관리되면 팀의 배포 자신감과 실험 문화를 혁신적으로 높이지만, 관리 없이 방치하면 기술 부채로 시스템 신뢰성을 위협한다.

📢 **섹션 요약 비유**: 피처 플래그는 마술 지팡이와 같다. 올바르게 사용하면 원하는 기능을 원하는 사람에게만, 원하는 시간에 나타나게 할 수 있다. 하지만 지팡이를 너무 많이 만들면 어떤 지팡이가 어떤 마법인지 아무도 모르게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Trunk-Based Development | 피처 플래그 없이는 TBD가 미완성 기능 노출 위험 |
| Canary Release | 피처 플래그와 결합하면 더 정밀한 점진 출시 구현 |
| A/B Testing | Experiment Toggle이 A/B 테스트의 인프라 구현체 |
| LaunchDarkly / Unleash | 피처 플래그 관리 플랫폼의 대표 도구 |
| 기술 부채 | 미제거 플래그가 누적되는 피처 플래그 지옥 |
| 킬 스위치 | Ops Toggle로 장애 시 즉각 기능 비활성화 |

### 👶 어린이를 위한 3줄 비유 설명

1. 피처 플래그는 장난감 가게에서 새 장난감을 진열장에 올려두되, 포장 상자를 아직 안 뜯어둔 것과 같아.

### 📈 관련 키워드 및 발전 흐름도

```text
Feature Branch + 배포 = 기능 공개 (분리 불가)
    |
    v
Feature Flag: 코드 배포 ≠ 기능 공개 (Decouple)
    +-► LaunchDarkly · Unleash · ConfigCat
    +-► A/B Testing · Percentage Rollout
    |
    v
Trunk-Based Development + Feature Flag = CD 극대화
```
2. "이제 팔아도 돼"라는 신호가 오면 상자만 뜯으면 바로 판매 시작, 문제 생기면 다시 포장해서 치우면 돼.
3. 가게를 다시 꾸미지(재배포) 않아도 판매 ON/OFF를 할 수 있어서 엄청 편리해.
