---
title: "Structured Logging Json Format"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 140
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 구조화 로깅은 <strong>로그를 사람이 읽는 텍스트가 아닌 JSON 등 기계가 파싱 가능한 구조로 출력</strong>하여, 검색·필터·집계·상관 분석을 자동화하는 로깅 패턴이다.
> 2. **가치**: 비구조화 로그("ERROR: payment failed for user 123")는 <strong>grep으로만 검색 가능</strong>하지만, 구조화 로그({"level":"ERROR","user_id":123})는 <strong>Loki·ELK에서 필드별 쿼리·집계</strong>가 가능하다.
> 3. **판단 포인트**: 로그 레벨(DEBUG·INFO·WARN·ERROR·FATAL), Correlation ID(분산 추적), 컨텍스트 필드(user_id·request_id·trace_id)가 구조화 로그의 필수 요소이다.

---

## Ⅰ. 개요 및 필요성

```text
비구조화: "2024-01-15 10:30:22 ERROR Payment failed for user 123"
구조화 (JSON):
  {"ts":"2024-01-15T10:30:22Z","level":"ERROR",
   "msg":"Payment failed","user_id":123,
   "trace_id":"abc123","service":"payment"}
-> 필드별 검색: user_id=123 AND level=ERROR
```

- **📢 섹션 요약 비유**: 비구조화 로그는 **자유 형식 메모**, 구조화 로그는 <strong>엑셀 표</strong>이다. 표가 검색·정렬·분석에 훨씬 유리하다.

---

## Ⅱ~Ⅴ. 결론

구조화 로깅은 <strong>현대 관측 가능성의 기본</strong>이며, JSON+Correlation ID로 분산 시스템의 로그를 추적한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **구조화 로깅** | JSON 형식 |
| **Correlation ID** | 분산 추적 연결 |
| <strong>로그 레벨</strong> | DEBUG~FATAL |
| **Loki** | 구조화 로그 쿼리 |
| **Serilog/Zap** | 구조화 로깅 라이브러리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[printf 로깅 (~2010s)] -> [구조화 로깅 (Serilog, 2013)]
    -> [JSON 로그 표준화 (2016~)]
    -> [OTel Log Signal (2023)]
    -> [현재: 구조화 로그 + AI 이상 탐지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 비구조화 로그는 <strong>자유 형식 메모</strong>예요. 찾기 어려워요.
2. 구조화 로그는 <strong>엑셀 표</strong>예요. 칸(필드)마다 정리되어 **검색이 쉬워요**.
3. "에러인 것 중 사용자 123번"처럼 <strong>정확히 필터</strong>할 수 있어요!
