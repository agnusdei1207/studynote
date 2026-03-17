+++
title = "529. Repeatable Read와 팬텀 읽기 - MVCC의 한계와 해결"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 529
+++

# 529. Repeatable Read와 팬텀 읽기 - MVCC의 한계와 해결

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Repeatable Read 격리 수준은 한 트랜잭션 내에서 읽은 데이터의 '값'은 유지해주지만, 다른 트랜잭션의 INSERT로 인해 **결과 집합의 행 수가 변하는 '팬텀 읽기(Phantom Read)' 현상을 완벽히 막지는 못한다.**
> 2. **가치**: MVCC(다중 버전 동시성 제어)는 스냅샷을 통해 단순 조회 시에는 팬텀 현상을 회피하게 해주지만, **쓰기 락(Lock)을 동반한 조회(SELECT FOR UPDATE 등)** 시에는 스냅샷이 아닌 실제 최신 데이터를 읽어야 하므로 팬텀이 발생할 수 있음을 경고한다.
> 3. **융합**: MySQL InnoDB 등 현대 DB는 넥스트 키 락(Next-Key Lock) 기술을 융합하여, 인덱스 사이의 간격(Gap)까지 잠그는 방식으로 Repeatable Read 수준에서도 팬텀 현상을 실무적으로 차단한다.

+++

### Ⅰ. 팬텀 읽기(Phantom Read)의 발생 매커니즘

- **정의**: 트랜잭션 T1이 특정 범위(예: 나이 > 20)를 두 번 조회할 때, 그 사이 T2가 새로운 행(나이 25)을 삽입하고 커밋하면 T1의 두 번째 조회 결과에 새로운 행이 나타나는 현상.
- **Repeatable Read의 한계**: 기존에 '읽었던 행'은 잠금이나 스냅샷으로 보호되지만, '아직 존재하지 않았던 행'의 삽입까지는 막지 못하는 논리적 틈새가 있습니다.

+++

### Ⅱ. MVCC 환경에서의 팬텀 현상 시각화 (ASCII Model)

단순 조회(Snapshot Read)와 락 조회(Current Read)의 차이가 핵심입니다.

```text
[ Case 1: Simple SELECT (Snapshot Read) ] ✅
  T1: SELECT COUNT(*) ──▶ [5명] (TS: 100 기준)
  T2: INSERT New Row & COMMIT!
  T1: SELECT COUNT(*) ──▶ [5명] (여전히 TS: 100 스냅샷 유지) ✅ "Phantom Avoided"

[ Case 2: SELECT FOR UPDATE (Current Read) ] 💥
  T1: SELECT COUNT(*) FOR UPDATE ──▶ [5명] (실제 데이터 락 시도)
  T2: INSERT New Row & COMMIT! (락 범위가 좁을 경우 성공)
  T1: SELECT COUNT(*) FOR UPDATE ──▶ [6명] 💥 "Phantom APPEARED!"
  * 이유: 락 조회는 스냅샷이 아닌 '현재의 진실'을 봐야 하기 때문.
```

+++

### Ⅲ. 실무적 해결책: 넥스트 키 락 (Next-Key Lock)

- **정의**: 레코드 락(Record Lock)과 간격 락(Gap Lock)을 합친 형태.
- **원리**: 인덱스의 특정 레코드뿐만 아니라, 그 앞뒤의 빈 공간(Gap)까지 모두 잠가버려 새로운 데이터가 끼어들 틈을 주지 않습니다.
- **효과**: 이 기술 덕분에 MySQL InnoDB는 공식적인 Repeatable Read 수준임에도 불구하고, 실무적으로는 Serializable에 가까운 팬텀 방어 능력을 보여줍니다.

- **📢 섹션 요약 비유**: 팬텀 읽기는 **'학생 명부와 교실 상황의 불일치'**와 같습니다. 선생님(T1)이 명부를 보고 출석 체크를 다 했는데(스냅샷), 잠시 뒤에 창문으로 새로운 학생(T2)이 몰래 들어온 상황입니다. 선생님이 눈으로 직접 교실을 다시 세어보면(Current Read) 인원이 늘어나 유령(팬텀)이 나타난 것처럼 느껴집니다. 이를 막으려면 출석 체크 동안 교실 문뿐만 아니라 창문(Gap)까지 몽땅 잠가야(Next-Key Lock) 합니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Gap Lock]**: 레코드 사이의 빈 공간을 보호하는 락.
- **[Current Read]**: 최신 데이터를 강제로 읽어오는 작업 (UPDATE, DELETE, SELECT FOR UPDATE).
- **[Serializable]**: 모든 팬텀 현상을 정의상 완벽히 차단하는 유일한 격리 수준.

📢 **마무리 요약**: **Repeatable Read**와 팬텀 현상의 관계를 이해하는 것은 트랜잭션 설계의 정수입니다. **MVCC와 락킹 전략**을 조화롭게 사용하여 데이터의 '집합적 무결성'을 지켜내야 합니다.