+++
title = "530. Serializable 격리 수준 - 최고 정합성과 성능의 대가"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 530
+++

# 530. Serializable 격리 수준 - 최고 정합성과 성능의 대가

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Serializable은 트랜잭션 격리 수준 중 가장 높은 단계로, **여러 트랜잭션이 동시에 실행되더라도 그 결과가 반드시 어떤 직렬(Serial) 순서로 실행한 것과 동일함을 보장**한다.
> 2. **가치**: 오손 읽기, 비반복 읽기, 유령 읽기 등 모든 동시성 이상 현상을 완벽히 차단하여 **절대적인 데이터 무결성**을 수호하지만, 이를 위해 읽기 작업조차 락(Lock)을 걸어 성능을 대폭 희생한다.
> 3. **융합**: 인덱스 범위 잠금(Range Lock) 및 엄격한 2단계 락킹(Rigorous 2PL) 기술이 융합되어 구현되며, 교착 상태(Deadlock) 발생 빈도가 가장 높은 '위험한 안전지대'로 작용한다.

+++

### Ⅰ. Serializable의 물리적 구현 방식

- **읽기 락 강제 (S-Lock)**: 단순 조회(`SELECT`) 시에도 트랜잭션이 끝날 때까지 공유 락을 쥐고 있어 다른 사람의 수정을 막습니다.
- **범위 잠금 (Predicate/Range Lock)**: 조건절에 해당하는 영역 전체를 잠가 새로운 데이터의 삽입(Insert)을 물리적으로 차단합니다.
- **낙관적 검증 (SSI, Serializable Snapshot Isolation)**: PostgreSQL 등에서 사용. 일단 진행한 뒤 커밋 시점에 직렬성 위반 여부를 검사하여 충돌 시 롤백합니다.

+++

### Ⅱ. Serializable 성능 병목 시각화 (ASCII Model)

```text
[ Concurrency Bottleneck: Serializable ]

  T1: SELECT * FROM Stock WHERE Category='AI'; (Range Lock 🔒)
       │
  T2: UPDATE Stock SET Price=100...  ──▶ ❌ BLOCKED (Wait for T1)
       │
  T3: INSERT INTO Stock... (Cat='AI') ──▶ ❌ BLOCKED (Wait for T1)
       │
  T1: COMMIT; ──▶ 🔓 Release All Locks
       │
  Result: T2, T3 이제야 순차적 실행 시작.
  "High Integrity, but Extreme Low Concurrency" 💥
```

+++

### Ⅲ. 데드락(Deadlock) 방어와 사용 가이드

- **데드락 위험**: 읽기 락을 서로 쥐고 쓰기 락으로 승격하려다 교착 상태에 빠질 확률이 타 격리 수준보다 수십 배 높습니다.
- **사용 원칙**: 
    - 일반적인 웹 서비스에서는 절대 사용하지 않습니다.
    - 금융권의 **계좌 이체, 재고 수량의 절대 일치** 등 극히 민감한 '임계 영역'에서만 짧은 트랜잭션으로 사용해야 합니다.
- **대안**: 가능하면 `SELECT FOR UPDATE`와 같은 명시적 락을 통해 필요한 행만 잠그는 방식을 권장합니다.

- **📢 섹션 요약 비유**: Serializable은 **'도서관 전체 대관'**과 같습니다. 내가 책 한 권을 읽는 동안(조회) 다른 사람들이 책을 옮기거나 새 책을 꽂는 것조차 방해받지 않기 위해 도서관 문을 통째로 잠그는 것입니다. 보안은 완벽하지만, 밖에서 기다리는 사람들의 불만(성능 저하)이 폭발하게 되므로 꼭 필요한 1분 1초의 순간에만 사용해야 합니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Range Lock]**: 유령 읽기를 막기 위한 물리적 수단.
- **[Throughput vs Integrity]**: Serializable이 직면한 영원한 난제.
- **[SSI]**: 락 없이 성능을 보전하며 Serializable을 구현하려는 현대적 시도.

📢 **마무리 요약**: **Serializable**은 데이터베이스 보안의 정점입니다. 완벽한 무결성을 위해 성능을 제물로 바친 이 수준은, 가장 신중하고 정교하게 사용되어야 할 '최종 병기'입니다.