+++
title = "458. 트랜잭션 격리 수준 - 일관성과 동시성의 균형"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 458
+++

# 458. 트랜잭션 격리 수준 - 일관성과 동시성의 균형

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 격리 수준(Isolation Level)은 동시에 실행되는 트랜잭션들이 **서로의 데이터를 얼마나 볼 수 있는지를 정의한 표준 설정**으로, 데이터 정합성과 시스템 성능 사이의 트레이드오프(Trade-off)를 조절하는 잣대다.
> 2. **가치**: ANSI/ISO SQL 표준에서 정의한 4단계 레벨을 통해 오손 읽기, 비반복 읽기, 유령 읽기 등 **동시성 이상 현상을 선택적으로 제어**함으로써 비즈니스 요건에 최적화된 DB 환경을 구축한다.
> 3. **융합**: 각 격리 수준은 락킹(Locking)의 범위와 기간, 그리고 MVCC 스냅샷 생성 시점 기술이 융합되어 물리적으로 구현된다.

+++

### Ⅰ. 4단계 격리 수준 및 이상 현상 발생 여부

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read | 특징 |
|:---|:---:|:---:|:---:|:---|
| **Level 0: Read Uncommitted** | **O** | O | O | 커밋 안 된 데이터도 읽음 (최고 성능) |
| **Level 1: Read Committed** | X | **O** | O | 커밋된 것만 읽음 (Oracle 기본값) |
| **Level 2: Repeatable Read** | X | X | **O** | 처음 읽은 상태 유지 (MySQL 기본값) |
| **Level 3: Serializable** | X | X | X | 모든 이상 현상 차단 (최고 정합성) |

+++

### Ⅱ. 격리 수준과 성능의 상관관계 (ASCII Model)

격리 강도가 높아질수록 데이터는 안전해지지만, 대기 시간은 길어집니다.

```text
[ Isolation Level vs Performance ]

  (High Performance) ◀──────────────────────────────────────────▶ (High Consistency)
  
  Read Uncommitted ───── Read Committed ───── Repeatable Read ───── Serializable
  
  [ Lower Locking ]                                           [ Higher Locking ]
  [ No Isolation  ]                                           [ Full Isolation ]
```

+++

### Ⅲ. 실무적 선택 가이드

- **Read Committed**: 일반적인 웹 서비스나 사내 인트라넷 등 대다수 업무에 권장됩니다.
- **Repeatable Read**: 한 트랜잭션 내에서 정산이나 통계 보고서 작성을 위해 데이터가 변하면 안 되는 경우에 사용합니다.
- **Serializable**: 결제, 계좌 이체 등 단 1원의 오차도 허용되지 않는 극도로 민감한 트랜잭션에만 일시적으로 사용합니다.

- **📢 섹션 요약 비유**: 격리 수준은 **'공부방의 소음 차단 정도'**와 같습니다. Level 0은 거실에서 공부하는 것이라 식구들이 떠드는 소리(Dirty Read)가 다 들리지만 아주 자유롭고, Level 3은 방음벽이 완벽한 1인 독서실에 들어간 것이라 아무 소리도 안 들려 집중(정합성)은 잘 되지만 답답하고 자리가 부족한 것과 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[MVCC]**: 높은 격리 수준에서도 성능 저하를 최소화하는 현대 DB의 핵심 기술.
- **[Anomalies]**: 격리 수준이 낮을 때 발생하는 3대 부작용.
- **[Default Level]**: DBMS 벤더마다 기본값이 다르므로 반드시 확인 필요.

📢 **마무리 요약**: **Isolation Level**은 정답이 없는 선택의 문제입니다. 비즈니스의 데이터 민감도와 예상 트래픽을 고려하여 가장 합리적인 지점을 찾아내는 것이 아키텍트의 실력입니다.