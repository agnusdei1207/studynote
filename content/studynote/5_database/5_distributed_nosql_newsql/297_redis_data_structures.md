+++
title = "297. Redis 자료구조 - 고성능 인메모리 엔진의 심장"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 297
+++

# 297. Redis 자료구조 - 고성능 인메모리 엔진의 심장

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Redis는 단순한 Key-Value 저장소를 넘어, **다양한 고차원 자료구조(Strings, Lists, Sets, Hashes, Sorted Sets 등)를 메모리에서 원자적(Atomic)으로 처리**하는 고성능 데이터 구조 서버다.
> 2. **가치**: 각 자료구조가 특정 알고리즘(Skip List, Hash Table 등)에 최적화되어 있어, 실시간 순위표, 대기열, 메시지 브로커 등 복잡한 기능을 애플리케이션 레벨의 로직 없이 DB 레벨에서 초고속으로 해결한다.
> 3. **융합**: 고유한 자료구조와 Lua 스크립팅 기술이 결합되어, 정교한 분산 락(Distributed Lock)이나 실시간 통계 분석 시스템의 핵심 아키텍처로 융합된다.

+++

### Ⅰ. Redis 5대 기본 자료구조

| 자료구조 | 설명 | 주요 활용 유즈케이스 |
|:---|:---|:---|
| **Strings** | 가장 기본적인 타입 (최대 512MB) | 캐싱, 단순 KV 저장, 카운터(INCR) |
| **Lists** | 삽입 순서대로 유지되는 문자열 목록 | 메시지 큐 (Lpush/Rpop), 최근 뉴스 피드 |
| **Sets** | 중복을 허용하지 않는 무순서 집합 | 태그 관리, 방문자 IP 체크, 집합 연산 |
| **Hashes** | 필드-값 쌍으로 이루어진 Map 구조 | 객체 정보 저장 (User Profile), 부분 수정 유리 |
| **Sorted Sets** | 가중치(Score)에 따라 정렬된 집합 | **실시간 랭킹(리더보드)**, 우선순위 큐 |

+++

### Ⅱ. 자료구조 시각화 (ASCII Map)

```text
[ Redis Logical Data Models ]

  1. String  : [ "Key" ] ──▶ "Hello Redis"
  2. List    : [ "Queue" ] ──▶ [ Task3 ]-[ Task2 ]-[ Task1 ] (Linked List)
  3. Set     : [ "Tags" ] ──▶ { "AI", "Cloud", "DB" } (Hash Table)
  4. Hash    : [ "User:1" ] ──▶ { name:"Kim", age:20 }
  5. ZSet    : [ "Rank" ] ──▶ (100:"PlayerA"), (90:"PlayerB") (Skip List)
```

+++

### Ⅲ. 왜 Redis 자료구조를 쓰는가?

- **Atomicity**: 모든 자료구조 연산은 단일 명령어로 실행되어 레이스 컨디션(Race Condition)을 방지합니다.
- **성능**: 예를 들어, 수백만 명의 랭킹을 실시간으로 계산할 때 관계형 DB는 무거운 정렬이 필요하지만, Redis의 **Sorted Set**은 $O(\log N)$의 복잡도로 순식간에 답을 냅니다.
- **풍부한 기능**: 비트맵(Bitmaps), HyperLogLog(확률적 카운팅), Geospatial(위치 정보) 등 특수한 자료구조도 기본 제공합니다.

- **📢 섹션 요약 비유**: Redis 자료구조는 **'다기능 멀티툴(맥가이버 칼)'**과 같습니다. 단순히 자르는 기능(캐시)만 있는 게 아니라 드라이버(큐), 가위(셋), 톱(정렬) 등 다양한 도구가 한 몸에 붙어 있어, 복잡한 작업도 도구만 쓱 꺼내서 한 번에 끝낼 수 있는 강력한 무기입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Skip List]**: Sorted Set의 미친듯한 속도를 지탱하는 내부 자료구조.
- **[Pub/Sub]**: 실시간 알림을 위한 메시징 기능.
- **[Replication]**: 인메모리 데이터의 안정성을 위한 복제 기술.

📢 **마무리 요약**: **Redis Data Structures**는 현대 아키텍처의 치트키입니다. 데이터의 특성에 맞는 적절한 자료구조를 선택하는 것만으로도 복잡한 백엔드 로직을 혁신적으로 단순화할 수 있습니다.