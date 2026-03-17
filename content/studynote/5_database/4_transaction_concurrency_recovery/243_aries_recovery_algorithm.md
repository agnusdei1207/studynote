+++
title = "243. ARIES 알고리즘 - 현대 DBMS 복구의 표준"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 243
+++

# 243. ARIES 알고리즘 - 현대 DBMS 복구의 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ARIES(Algorithms for Recovery and Isolation Exploiting Semantics)는 **분석(Analysis), 재실행(Redo), 실행 취소(Undo)**의 3단계 페이즈를 통해, 시스템 장애 후 데이터베이스를 가장 최근의 일관된 상태로 복구하는 알고리즘이다.
> 2. **가치**: "Repeating History" 원칙을 통해 장애 직전의 메모리 상태를 완벽히 재현하고, 커밋되지 않은 트랜잭션만 선별적으로 취소함으로써 복구의 정확성과 효율성을 동시에 달성한다.
> 3. **융합**: LSN(Log Sequence Number)을 활용한 로그 관리와 더티 페이지 추적 기술이 결합되어 Oracle, DB2, MSSQL 등 주요 RDBMS의 표준 복구 모델이 되었다.

+++

### Ⅰ. ARIES 알고리즘의 3대 단계

1. **분석 (Analysis) 단계**: 
    - 마지막 체크포인트부터 로그를 읽어, 장애 당시의 '더티 페이지' 목록과 실행 중이던 트랜잭션(Active Xact) 목록을 파악합니다.
2. **재실행 (Redo) 단계**: 
    - 파악된 로그를 바탕으로, **커밋 여부와 상관없이** 장애 발생 직전까지의 모든 변경 사항을 다시 수행합니다. (역사 재현)
3. **실행 취소 (Undo) 단계**: 
    - 로그를 역순으로 읽으며, 커밋되지 않은 트랜잭션들이 수행한 작업을 모두 취소하여 데이터베이스를 깨끗하게 만듭니다.

+++

### Ⅱ. ARIES 복구 아키텍처 (ASCII Flow)

```text
[ARIES 복구 3단계 파이프라인]

  Checkpoint ──▶ [ 1. Analysis ] ──▶ 장애 시점 인지
                         │
                         ▼
  (Forward Scan) [ 2. Redo ] ──▶ Repeating History
                         │       (모든 변경사항 재반영)
                         ▼
  (Backward Scan)[ 3. Undo ] ──▶ Loser 트랜잭션 취소
                                 (정합성 완성) ✅
```

+++

### Ⅲ. ARIES의 핵심 기술: LSN과 CLR

- **LSN (Log Sequence Number)**: 각 로그 레코드와 데이터 페이지에 부여된 고유 번호로, 복구가 필요한지 여부를 판단하는 기준이 됩니다.
- **CLR (Compensation Log Record)**: Undo 과정 자체를 로그로 남겨, 복구 도중 다시 장애가 나더라도 중복 Undo를 방지하는 고도의 안전장치입니다.

- **📢 섹션 요약 비유**: ARIES는 **'정밀한 사고 현장 복원'**과 같습니다. 1. 흩어진 증거물을 모으고(분석), 2. 사고 직전까지의 상황을 그대로 다시 연기해 본 뒤(Redo), 3. 범인이 저지른 나쁜 짓(미완료 트랜잭션)만 쏙쏙 골라 지워버리는(Undo) 완벽한 과학 수사대입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Repeating History]**: ARIES만의 독특한 Redo 철학.
- **[Dirty Page Table]**: 분석 단계에서 생성되는 복구 지도.
- **[Steal/No-Force]**: ARIES가 전제하는 고성능 버퍼 정책.

📢 **마무리 요약**: **ARIES**는 복구 알고리즘의 결정판입니다. 복잡한 분산 환경에서도 단 한 점의 데이터 오차도 허용하지 않는 현대 DBMS의 자부심입니다.