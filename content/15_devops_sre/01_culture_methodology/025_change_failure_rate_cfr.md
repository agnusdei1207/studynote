---
title: "Change Failure Rate Cfr"
date: "2026-04-29"
tags:
  - "studynote-devops-sre"
weight: 25
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CFR (Change Failure Rate, 변경 실패율)은 DORA (DevOps Research and Assessment, 데브옵스 연구·평가) 4대 핵심 메트릭 중 하나로, "전체 배포 건수 대비 서비스 장애·롤백·핫픽스를 유발한 배포의 비율"을 측정하여 배포 프로세스의 안정성을 정량화한다.
> 2. **가치**: CFR은 배포 빈도(Deployment Frequency)와 반비례하는 경향이 있다고 오해하기 쉽지만, DORA 연구에 따르면 Elite 팀은 배포 빈도도 높고 CFR도 낮다(0~15%). 고품질 자동화 테스트, 점진적 배포(Canary/Blue-Green), 피처 플래그(Feature Flag)가 이 역설을 가능하게 한다.
> 3. **판단 포인트**: CFR은 단독으로 해석하면 안 되고 MTTR (Mean Time to Recover, 평균 복구 시간)과 함께 분석해야 한다. CFR이 높아도 MTTR이 낮으면(빠른 롤백) 실제 서비스 영향은 작을 수 있다. 진정한 목표는 CFR을 낮추면서 동시에 MTTR도 낮추는 것이다.

---

## Ⅰ. 개요 및 필요성

```text
+----------------------------------------------------------+
|        DORA 4대 메트릭                                     |
+----------------------------------------------------------+
|                                                          |
|  처리량(Throughput):                                      |
|  1. Deployment Frequency (배포 빈도) — 얼마나 자주?        |
|  2. Lead Time for Changes (변경 리드타임) — 얼마나 빨리?   |
|                                                          |
|  안정성(Stability):                                       |
|  3. CFR (Change Failure Rate) — 얼마나 안전하게?           |
|  4. MTTR (Mean Time to Recover) — 장애 시 얼마나 빨리?     |
|                                                          |
|  ★ CFR = 실패 배포 수 / 전체 배포 수 × 100%               |
+----------------------------------------------------------+
```

### DORA 성과 수준별 CFR 벤치마크

| 성과 수준 | CFR | 설명 |
|:---|:---|:---|
| **Elite** | 0~15% | 자동화 테스트, 점진적 배포 성숙 |
| **High** | 0~15% | Elite와 동일 범위 |
| **Medium** | 16~30% | 자동화 부분 도입 |
| **Low** | 46~60%+ | 수동 배포, 테스트 부족 |

- **📢 섹션 요약 비유**: CFR은 비행기 이착륙 성공률이다. 비행기가 얼마나 자주 뜨고 내리느냐(배포 빈도)보다, 사고 없이 안전하게 착륙하느냐(CFR)가 항공사(서비스)의 신뢰성을 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CFR 감소를 위한 배포 전략

```text
1. 자동화 테스트 피라미드
   E2E Tests (적음)
   Integration Tests
   Unit Tests (많음) -> 빠른 피드백, CFR 감소

2. 점진적 배포 (Progressive Delivery)
   Blue-Green: 전체 트래픽을 신규 버전으로 한 번에 전환
                -> 문제 시 즉시 롤백
   Canary:     5% -> 25% -> 100% 단계적 트래픽 전환
                -> 소수 사용자에서 문제 조기 탐지

3. Feature Flag
   배포(Deploy) ≠ 릴리스(Release)
   코드는 배포하되 Feature Flag로 ON/OFF
   -> 문제 시 코드 배포 없이 플래그만 OFF
```

### Canary 배포 CFR 감소 원리

```text
[전체 트래픽 100%]
         |
  +------+------+
  | Stable v1.0 |  -> 95% 트래픽
  +-------------+

  +--------------+
  | Canary v1.1  |  -> 5% 트래픽 (모니터링 중)
  +--------------+
         |
   에러율 증가 감지
         |
  자동 롤백 또는 계속 진행
```

- **📢 섹션 요약 비유**: Canary 배포는 광부들이 탄광에 데려가던 카나리아 새와 같다. 카나리아(새 버전)를 소수 사용자에게 먼저 노출해서 위험(에러)이 감지되면 전체 광부(사용자)를 보호한다.

---

## Ⅲ. 비교 및 연결

| DORA 메트릭 | 측정 대상 | CFR과의 관계 |
|:---|:---|:---|
| **배포 빈도** | 단위 시간당 배포 횟수 | 높은 빈도 + 낮은 CFR = Elite 팀 |
| <strong>리드 타임</strong> | 커밋->배포 소요 시간 | 짧은 리드타임 -> 빠른 피드백 -> CFRv |
| **CFR** | 실패 배포 비율 | 안정성의 핵심 지표 |
| <strong>MTTR</strong> | 장애 복구 평균 시간 | CFR 높아도 MTTR 낮으면 영향 최소화 |

- **📢 섹션 요약 비유**: DORA 4 메트릭은 자동차의 4가지 성능 지표다. 배포 빈도는 최고 속도, 리드 타임은 가속력, CFR은 브레이크 성능, MTTR은 수리 속도다. 빠르고 안전한 차가 좋은 차이듯, 빠르고 안정적인 배포가 좋은 DevOps다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### CFR 측정 및 개선 사이클

```python
# GitHub Actions + 모니터링 도구 연계 CFR 측정
def calculate_cfr(deployments, incidents):
    """
    deployments: 전체 배포 목록 (타임스탬프, 버전)
    incidents: 배포 관련 장애 목록 (타임스탬프, 관련 배포)
    """
    failed_deployments = set()
    for incident in incidents:
        # 장애 시간 기준 1시간 내 배포를 실패로 연결
        related = [d for d in deployments
                   if abs(d.timestamp - incident.timestamp) < 3600]
        failed_deployments.update(related)

    cfr = len(failed_deployments) / len(deployments) * 100
    return cfr  # Elite 목표: 15% 이하
```

### 안티패턴
- CFR을 낮추기 위해 배포 빈도를 줄이는 안티패턴. 배포 빈도 감소 -> 배포 당 변경 크기 증가 -> 오히려 CFR 상승(큰 변경 = 높은 위험). 빈번하고 작은 변경(Small Batches)이 CFR을 낮추는 올바른 접근이다.

- **📢 섹션 요약 비유**: CFR을 낮추려고 배포 빈도를 줄이는 것은, 사고율을 낮추려고 도로를 덜 달리는 것이다. 더 안전하게 자주 달리는(점진적 배포, 자동화 테스트) 것이 올바른 해결책이다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **배포 안정성** | 서비스 장애 유발 배포 감소 |
| <strong>팀 신뢰도</strong> | 낮은 CFR = 배포에 대한 공포 감소 |
| **비즈니스 가치** | 빠르고 안전한 기능 출시 |

DORA 메트릭은 SPACE (Satisfaction, Performance, Activity, Communication, Efficiency) 프레임워크와 결합하여 개발자 경험(Developer Experience, DevEx)을 종합적으로 측정하는 방향으로 발전하고 있다. CFR은 단순 KPI가 아닌 팀 심리적 안전감과 기술적 역량의 복합 지표다.

- **📢 섹션 요약 비유**: CFR은 단순한 숫자가 아니라 팀 문화의 거울이다. CFR이 낮은 팀은 자동화를 신뢰하고, 작은 변경을 자주 배포하며, 실패에서 빠르게 학습하는 성숙한 DevOps 문화를 가진 팀이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>DORA 4 메트릭</strong> | CFR은 안정성 지표 중 하나 |
| <strong>Canary/Blue-Green 배포</strong> | CFR 감소를 위한 점진적 배포 전략 |
| <strong>Feature Flag</strong> | 배포와 릴리스 분리로 CFR 영향 최소화 |
| <strong>MTTR</strong> | CFR과 쌍으로 분석하는 복구 시간 지표 |
| **자동화 테스트** | CFR 감소의 근본적 해결책 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 배포 — 높은 CFR, 낮은 배포 빈도]
    |
    v
[CI/CD 자동화 — 테스트 자동화로 CFR 감소]
    |
    v
[점진적 배포 (Canary/Blue-Green) — 리스크 최소화]
    |
    v
[Feature Flag — 배포와 릴리스 완전 분리]
    |
    v
[DORA 메트릭 기반 Elite DevOps — CFR 0~15%]
```

### 👶 어린이를 위한 3줄 비유 설명

1. CFR은 학교 발표에서 실수한 비율이에요! 100번 발표 중 몇 번 말을 틀렸는지(실패 배포)를 측정해요.
2. 발표 연습(자동화 테스트)을 많이 하고, 처음엔 소수 친구들 앞에서만 발표(Canary 배포)하면 실수가 줄어들어요.
3. 목표는 실수 비율을 15% 이하로 낮추면서도 발표 횟수(배포 빈도)는 줄이지 않는 거랍니다!
