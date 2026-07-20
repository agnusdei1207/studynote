---
title: "Trunk-Based Development"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 40
---
> **핵심 인사이트**
> 1. 트렁크 기반 개발(TBD, Trunk-Based Development)은 모든 개발자가 하나의 공유 브랜치(trunk/main)에 소규모 코드를 빈번하게 통합하는 방식으로, 장기 브랜치로 인한 병합 지옥(Merge Hell)과 통합 늦음(Integration Late) 문제를 근본적으로 해결한다.
> 2. TBD는 DORA 연구에서 고성능 조직의 핵심 기술 실천으로 확인된 과학적 근거가 있는 DevOps 원칙이며, 피처 플래그(Feature Flag)와 결합하여 "완성되지 않은 코드도 안전하게 통합"하는 것이 핵심 패턴이다.
> 3. Git Flow·GitHub Flow와 구분되어, TBD는 배포 파이프라인 완성도와 테스트 자동화가 높을수록 효과가 커지며, "브랜치 수명은 하루"라는 규칙이 지속적 통합(CI)의 진정한 의미를 구현한다.

---

## Ⅰ. TBD 핵심 원칙

```
Trunk-Based Development 원칙:

기본 규칙:
  - 단일 공유 브랜치 (main/master/trunk)
  - 모든 개발자가 하루 1회 이상 커밋
  - 브랜치 수명: 1~2일 이내 (이상적으로 없음)
  - 기능 완성 전에도 통합 가능 (피처 플래그 사용)

반대 개념:
  장기 피처 브랜치 개발:
    feature/order-system (3주 개발)
    -> 병합 시 수백 파일 충돌
    -> "병합 지옥 (Merge Hell)"

TBD 흐름:
  Alice: code -> commit -> push (trunk)   [오전]
  Bob:   code -> commit -> push (trunk)   [오후]
  CI:    자동 테스트 -> 통과 -> 배포 준비  [실시간]

단기 브랜치 허용 (Scaled TBD):
  feature 브랜치 최대 2일 이내 병합
  PR(Pull Request) 통한 리뷰 후 병합
  병합 후 브랜치 즉시 삭제
```

> 📢 **섹션 요약 비유**: TBD는 매일 저녁 숙제를 선생님께 제출하는 방식 — 한 달치 몰아서 내면 충돌·오류 수정이 훨씬 어렵다.

---

## Ⅱ. 피처 플래그와 TBD

```
Feature Flag (피처 플래그) + TBD:

문제:
  완성되지 않은 기능을 trunk에 병합하면
  -> 사용자에게 미완성 기능 노출 위험

해결: 피처 플래그
  if feature_flag("new_checkout"):
      show_new_checkout()
  else:
      show_old_checkout()

피처 플래그 상태:
  개발 중:   플래그 OFF (기존 로직 실행)
  내부 테스트: 플래그 ON (특정 사용자만)
  점진적 출시: 10% -> 50% -> 100% 활성화
  완전 출시:  플래그 제거 (코드 정리)

장점:
  코드는 프로덕션에 배포됐지만 기능은 숨김
  언제든 즉시 롤백 (플래그 OFF)
  A/B 테스트 가능 (사용자 절반씩 다른 경험)

도구:
  LaunchDarkly, Unleash, CloudBees
  직접 DB/Redis로 간단 구현 가능
```

> 📢 **섹션 요약 비유**: 피처 플래그는 새 도로 개통 전에 차단막 설치 — 공사(개발)는 다 끝났지만 개통(활성화) 시점은 따로 결정.

---

## Ⅲ. TBD vs Git Flow vs GitHub Flow

```
브랜칭 전략 비교:

Git Flow (Vincent Driessen, 2010):
  main, develop, feature, release, hotfix 5가지 브랜치
  릴리즈 주기 긴 소프트웨어에 적합
  복잡성 높음, 병합 비용 큼
  현재: 모바일 앱, 패키지 SW

GitHub Flow:
  main + feature 브랜치 (2가지)
  PR 리뷰 후 main 병합
  단순하지만 TBD보다 브랜치 수명 길 수 있음

Trunk-Based Development:
  main 하나 (+ 1~2일짜리 단기 브랜치)
  CI/CD 파이프라인 완비 전제
  고성능 DevOps팀 표준
  웹 서비스/SaaS에 적합

DORA 연구 결과:
  고성능 팀의 공통점: TBD 또는 GitHub Flow
  저성능 팀: Git Flow (장기 브랜치)
```

> 📢 **섹션 요약 비유**: Git Flow는 엄격한 출판 프로세스, GitHub Flow는 블로그, TBD는 트위터 실시간 포스팅 — 배포 속도에 따라 맞는 방식이 다르다.

---

## Ⅳ. TBD 전제 조건

```
TBD 성공을 위한 전제:

1. 강력한 자동화 테스트:
   단위 테스트 커버리지 70% 이상
   통합 테스트 자동화
   "테스트 없이 TBD는 무모함"

2. CI/CD 파이프라인:
   커밋 후 10분 이내 자동 테스트 완료
   파이프라인 실패 시 즉시 알림
   "Red Build = 팀 전체 최우선 작업"

3. 작은 커밋 습관 (Small Commits):
   한 커밋 = 한 가지 목적
   파일 변경 수 50개 이하
   "1시간 이내 설명 가능한 커밋"

4. 피처 플래그 인프라:
   미완성 기능 숨기기 도구
   환경별 설정 관리

5. 팀 문화:
   "깨진 빌드는 모두의 문제"
   신뢰 기반 코드 리뷰
   심리적 안전감 (Small Change 두려움 없음)
```

> 📢 **섹션 요약 비유**: TBD 전제 조건은 고속도로 운전 조건 — 자동차(테스트)와 GPS(CI/CD)가 갖춰져야 안전하게 달릴 수 있다.

---

## Ⅴ. 실무 시나리오 — TBD 전환 사례

```
스타트업 C사 TBD 전환 (100명 규모):

현황 (Git Flow 사용 중):
  병합 주기: 주 1회 (금요일)
  충돌 해결: 평균 3시간 소요
  배포 주기: 주 1회 (목요일 새벽 배포 창)
  버그 발견: 배포 2주 후 고객 신고

TBD 전환 계획 (3개월):

1개월: 인프라 준비
  CI 파이프라인 강화 (테스트 자동화 70%+)
  피처 플래그 플랫폼 도입 (Unleash)

2개월: 팀 교육 + 파일럿
  1개 팀 TBD 시범 도입
  Small Commit 가이드 배포

3개월: 전사 전환
  모든 팀 TBD 전환
  Git Flow 브랜치 정리

전환 후 6개월 결과:
  배포 빈도: 주 1회 -> 하루 3회
  충돌 시간: 3시간 -> 0 (없어짐)
  버그 발견 시간: 2주 -> 30분 (CI 탐지)
  개발자 만족도: 3.2/5 -> 4.5/5
```

> 📢 **섹션 요약 비유**: TBD 전환은 주간 보고를 일일 스탠드업으로 바꾸기 — 매일 작은 업데이트로 큰 문제를 예방, 팀이 항상 같은 상태를 공유.

---

## 📌 관련 개념 맵

```
트렁크 기반 개발 (TBD)
+-- 핵심 원칙
|   +-- 단일 브랜치 (trunk/main)
|   +-- 빈번한 소규모 통합
|   +-- 브랜치 수명 최소화
+-- 활성화 기법
|   +-- 피처 플래그 (Feature Flag)
|   +-- 추상화를 통한 브랜칭 (Branch by Abstraction)
+-- 비교
|   +-- Git Flow (장기 브랜치)
|   +-- GitHub Flow
+-- 전제 조건
|   +-- CI/CD 파이프라인
|   +-- 자동화 테스트
+-- 연구 근거
    +-- DORA State of DevOps Report
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[XP (Extreme Programming, 1999)]
지속적 통합 원칙 제안
      |
      v
[Continuous Integration (Martin Fowler, 2006)]
TBD 원칙 명문화
      |
      v
[Git 보급 (2008~)]
브랜칭 전략 다양화
Git Flow, GitHub Flow 등장
      |
      v
[DORA 연구 (2014~)]
고성능 팀 = TBD + 자동화 확인
      |
      v
[현재: GitOps + TBD]
ArgoCD, Flux로 선언적 배포
TBD + 피처 플래그 = 현대 DevOps 표준
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. TBD는 한 달치 일기를 몰아 쓰는 것보다 매일 조금씩 쓰는 방식 — 나중에 기억나지 않는 것도 없고, 선생님도 바로바로 확인할 수 있어요.
2. 피처 플래그는 새 기능을 만들어 놓고 "스위치"로 켜고 끌 수 있어서, 완성 전에도 안전하게 메인 코드에 넣어 둘 수 있어요.
3. 매일 조금씩 코드를 합치면 충돌(다른 사람 코드와 겹침)이 거의 없어서, 금요일마다 "대충돌"을 수습하는 고통이 사라져요!
