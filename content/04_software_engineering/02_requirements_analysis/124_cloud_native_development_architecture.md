---
title: "Cloud Native Development Architecture"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 124
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라우드 네이티브는 <strong>컨테이너·MSA·CI/CD·선언적 API</strong>를 핵심으로 하여 클라우드 환경의 <strong>탄력성·확장성·복원력을 최대한 활용</strong>하는 소프트웨어 개발·운영 패러다임이다.
> 2. **가치**: Lift & Shift(기존 시스템을 그대로 클라우드로 이전)로는 클라우드의 이점을 10%도 활용하지 못하지만, 클라우드 네이티브로 설계하면 <strong>오토스케일링·셀프힐링·글로벌 배포</strong>가 자연스럽게 구현된다.
> 3. **판단 포인트**: CNCF(Cloud Native Computing Foundation)의 **Trail Map**(컨테이너화->CI/CD->오케스트레이션->관측성->서비스 메시)이 도입 로드맵이며, <strong>12 Factor App</strong>이 클라우드 네이티브 설계 원칙이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    클라우드 네이티브 4대 핵심                          |
+-------------------------------------------------------+
|  1. 컨테이너 (Docker/containerd)                      |
|  2. MSA (마이크로서비스)                              |
|  3. CI/CD (지속적 통합·배포)                          |
|  4. 선언적 API (K8s Desired State)                    |
|                                                       |
|  + DevOps 문화 + 관측성 + 서비스 메시                 |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 네이티브는 처음부터 <strong>바다(클라우드)에서 살도록 진화한 물고기</strong>이고, Lift & Shift는 육지 동물이 바다에 던져진 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 12 Factor App (주요)

| Factor | 설명 |
|:---|:---|
| <strong>코드베이스</strong> | 1앱 = 1리포 |
| **의존성** | 명시적 선언 |
| <strong>설정</strong> | 환경 변수로 분리 |
| <strong>포트 바인딩</strong> | 자체 HTTP 서버 |
| <strong>로그</strong> | stdout 스트림 |
| **프로세스** | Stateless |

- **📢 섹션 요약 비유**: 12 Factor는 클라우드 네이티브의 <strong>건축 법규</strong>다. 이 규칙을 따라야 건물(앱)이 안전하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 | Lift & Shift | 클라우드 네이티브 |
|:---|:---|:---|:---|
| **아키텍처** | 모놀리식 | 모놀리식 | <strong>MSA</strong> |
| **배포** | 수동 | 수동 | <strong>CI/CD</strong> |
| <strong>스케일링</strong> | 수동 | 반자동 | **자동** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### CNCF Trail Map
1. 컨테이너화 -> 2. CI/CD -> 3. K8s -> 4. 관측성(Prometheus) -> 5. 서비스 메시(Istio) -> 6. 보안(OPA).

---

## Ⅴ. 기대효과 및 결론

클라우드 네이티브는 <strong>현대 소프트웨어 개발의 표준 패러다임</strong>이며, CNCF 생태계가 사실상 모든 기술 스택을 포괄한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>CNCF</strong> | 클라우드 네이티브 재단 |
| **12 Factor** | 설계 원칙 |
| <strong>컨테이너</strong> | 핵심 런타임 |
| **K8s** | 오케스트레이션 표준 |
| <strong>서비스 메시</strong> | 통신 인프라 (Istio) |

### 📈 관련 키워드 및 발전 흐름도

```text
[온프레미스 (전통, ~2010s)]
    |
    v
[Lift & Shift (IaaS, 2010~)]
    |
    v
[클라우드 네이티브 (CNCF, 2015~) — 컨테이너+MSA+CI/CD]
    |
    v
[서비스 메시 + GitOps (2018~)]
    |
    v
[현재: Platform Engineering — 개발자 경험 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 클라우드 네이티브는 처음부터 <strong>바다(클라우드)에서 살도록 태어난 물고기</strong>예요.
2. 옛날 방식은 <strong>육지 동물을 바다에 던지는(Lift &amp; Shift)</strong> 거라 잘 못 수영해요.
3. 물고기처럼 설계하면 **파도(트래픽)가 커도 자유롭게** 헤엄칠 수 있답니다!
