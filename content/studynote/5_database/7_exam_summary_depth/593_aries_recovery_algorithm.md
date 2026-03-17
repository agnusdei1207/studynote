+++
title = "593. ARIES 알고리즘 - 현대 DBMS 복구의 표준 프레임워크"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 593
+++

# 593. ARIES 알고리즘 - 현대 DBMS 복구의 표준 프레임워크

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ARIES(Algorithms for Recovery and Isolation Exploiting Semantics)는 **분석(Analysis), 재실행(Redo), 실행 취소(Undo)**의 3단계 페이즈를 통해, 시스템 장애 후 데이터베이스를 일관된 상태로 복구하는 가장 신뢰받는 알고리즘이다.
> 2. **가치**: "Repeating History" 원칙을 통해 장애 직전의 메모리 상태를 완벽히 재현하고, 커밋되지 않은 트랜잭션만 선별적으로 취소함으로써 **복구의 정확성과 효율성**을 동시에 달성한다.
> 3. **융합**: LSN(Log Sequence Number)을 활용한 로그 관리와 더티 페이지 추적 기술이 융합되어 Oracle, DB2, MSSQL 등 주요 RDBMS의 표준 복구 모델이 되었다.

+++

### Ⅰ. ARIES 복구의 3단계 (Three Phases)

1. **분석 (Analysis) 단계**: 
    - 마지막 체크포인트부터 로그를 스캔하여, 장애 당시 실행 중이던 트랜잭션(Loser)과 메모리에만 머물던 더티 페이지(Dirty Pages) 목록을 파악합니다.
2. **재실행 (Redo) 단계 (Forward Scan)**: 
    - 파악된 로그를 바탕으로 **커밋 여부와 상관없이** 장애 발생 직전까지의 모든 변경 사항을 다시 수행합니다 (역사의 재현). ✅
3. **실행 취소 (Undo) 단계 (Backward Scan)**: 
    - 로그를 역순으로 읽으며, 커밋 마크가 없는 'Loser' 트랜잭션들이 수행한 작업을 모두 취소하여 데이터베이스를 깨끗하게 만듭니다. ✅

+++

### Ⅱ. ARIES 복구 아키텍처 시각화 (ASCII Model)

```text
[ ARIES 3-Phase Recovery Pipeline ]

  Checkpoint ──▶ [ 1. Analysis ] ──▶ ( 파악: Losers & Dirty Pages )
                         │
                         ▼
  (Forward Scan) [ 2. Redo ] ──▶ ( 실행: 모든 로그 재수행 ) ✅
                         │       "History is Repeated"
                         ▼
  (Backward Scan)[ 3. Undo ] ──▶ ( 취소: 미완료 트랜잭션 원복 ) ✅
                                 "Losers are undone"
```

+++

### Ⅲ. ARIES의 핵심 성공 요인

- **LSN 활용**: 각 데이터 페이지마다 마지막 수정 로그 번호(pageLSN)를 기록하여, 중복 Redo를 방지합니다.
- **CLR (Compensation Log Record)**: Undo 과정 자체를 로그로 남깁니다. 복구 도중 다시 장애가 나더라도 어디까지 Undo 했는지 알 수 있어 무한 루프를 방지합니다.
- **Steal/No-Force 허용**: 고성능 버퍼 관리 정책을 쓰면서도 완벽한 복구를 보장합니다.

- **📢 섹션 요약 비유**: ARIES는 **'정밀한 사고 현장 복원팀'**과 같습니다. 1. 흩어진 증거물을 모아 당시 상황을 추론하고(분석), 2. 사고 직전까지의 상황을 배우들이 그대로 다시 연기해 본 뒤(Redo), 3. 그중 범인이 저지른 나쁜 짓(미완료 트랜잭션)만 쏙쏙 골라 지워버리는(Undo) 완벽한 과학 수사대입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Repeating History]**: 장애 직전까지의 모든 일을 일단 다 복원하는 철학.
- **[Dirty Page Table]**: 복구가 필요한 메모리 페이지들의 명단.
- **[Compensation Log]**: 취소 작업을 다시 취소하지 않게 만드는 안전장치.

📢 **마무리 요약**: **ARIES**는 복구 알고리즘의 결정판입니다. 복잡한 시스템 장애 속에서도 단 한 점의 데이터 오차도 허용하지 않는 현대 DBMS의 자부심입니다.