+++
title = "35. 캐시 교체 정책 (Cache Replacement Policies)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Cache-Replacement", "LRU", "LFU", "Random", "ARC"]
draft = false
+++

# 캐시 교체 정책 (Cache Replacement Policies)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 캐시 교체 정책은 **"캐시 **미스 **시 **어떤 **데이터**를 **제거**할 **것**인가**를 **결정**하는 **알고리즘"**으로, **LRU**(Least Recently Used), **LFU**(Least Frequently Used), **Random**, **ARC**(Adaptive Replacement Cache)가 **대표적**이다.
> 2. **비교**: **LRU**는 **최근 **사용**하지 **않은 **데이터 **제거**(시간 **지역성 **활용), **LFU**는 **사용 **빈도**가 **낮은 **데이터 **제거**(공간 **지역성 **활용), **Random**은 **구현 **간단**하지만 **Hit Rate**가 **낮다.
> 3. **진화**: **LRU**는 **Bit-Reference**(approximate LRU)로 **구현**되고 **ARC**는 **LRU+LFU**를 **적응적**으로 **결합**하며 **Intel CAT**(Cache Allocation Technology)로 **캐시 **파티셔닝**이 **가능**하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
캐시 교체 정책은 **"희생자(victim) 선택 알고리즘"**이다.

**평가 기준**:
- **Hit Rate**: 캐시 적중률
- **Implementation Complexity**: 구현 복잡도
- **Storage Overhead**: 추가 저장소
- **Hardware Cost**: 하드웨어 비용

### 💡 비유
캐시 교체는 ****가방 **정리 ****와 같다.
- **가방**: 캐시 (용한 제한)
- **물건**: 데이터
- **제거**: 오래된/적게 쓰는 물건

---

## Ⅱ. 아키텍처 및 핵심 원리

### LRU (Least Recently Used)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         LRU Algorithm                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Access Sequence: A, B, C, D, A, E, B, F, C, G
    Cache Size: 3

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Access   │  Cache (MRU → LRU)      │  Hit/Miss  │  Victim      │  Action              │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────│  │
    │  A        │  [A]                   │  Miss      │  -          │  Load A              │  │
    │  B        │  [B, A]                │  Miss      │  -          │  Load B              │  │
    │  C        │  [C, B, A]             │  Miss      │  -          │  Load C              │  │
    │  D        │  [D, C, B]             │  Miss      │  A          │  Evict A, Load D    │  │
    │  A        │  [A, D, C]             │  Miss      │  B          │  Evict B, Load A    │  │
    │  E        │  [E, A, D]             │  Miss      │  C          │  Evict C, Load E    │  │
    │  B        │  [B, E, A]             │  Miss      │  D          │  Evict D, Load B    │  │
    │  F        │  [F, B, E]             │  Miss      │  A          │  Evict A, Load F    │  │
    │  C        │  [C, F, B]             │  Miss      │  E          │  Evict E, Load C    │  │
    │  G        │  [G, C, F]             │  Miss      │  B          │  Evict B, Load G    │  │
    │                                                                                         │  │
    │  → Total Hits: 0 / 10 = 0% (bad example, but demonstrates LRU)                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### LFU (Least Frequently Used)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         LFU Algorithm                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Access Sequence: A×3, B×2, C×1, D, E
    Cache Size: 3

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Cache State (Item → Frequency)                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. After A×3, B×2, C×1:                                                              │  │  │
    │  │     [A:3, B:2, C:1]  (MRU → LRU by frequency)                                       │  │  │
    │  │                                                                                       │  │  │
    │  │  2. Access D:                                                                         │  │  │
    │  │     [D:1, A:3, B:2]  (C:1 evicted, least frequent)                                    │  │  │
    │  │                                                                                       │  │  │
    │  │  3. Access E:                                                                         │  │  │
    │  │     [E:1, D:1, A:3]  (B:2 evicted)                                                    │  │  │
    │  │                                                                                       │  │  │
    │  │  → LFU keeps frequently accessed items longer                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 교체 정책 비교

| 정책 | Hit Rate | 복잡도 | 추가 저장소 | 특징 |
|------|----------|--------|-------------|------|
| **Optimal** | 최고 | 불가능 | - | 미래 예지 필요 |
| **LRU** | 높음 | 중간 | O(n) bits | 시간 지역성 |
| **LFU** | 중간 | 높음 | O(n) counters | 빈도 기반 |
| **Random** | 낮음 | 낮음 | 없음 | 단순 |
| **FIFO** | 낮음 | 낮음 | Queue 순서만 | 순차적 |
| **ARC** | 높음 | 중간 | O(n) | 적응형 |

### Approximate LRU (Bit-Reference)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Clock Algorithm (Approximate LRU)                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Cache with Reference Bits:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Item  │  Ref Bit  │  Hand (Pointer)                                             │  │  │
    │  │  ───────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  A      │  0        │                                                              │  │  │
    │  │  B      │  1        │  ← Clock hand                                              │  │  │
    │  │  C      │  1        │                                                              │  │  │
    │  │  D      │  0        │                                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  On Miss:                                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Advance clock hand, clearing ref bits                                           │  │  │
    │  │  2. Find first item with ref bit = 0                                                │  │  │
    │  │  3. Replace that item                                                              │  │  │
    │  │  4. Set new item's ref bit = 1                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Simpler than true LRU, approximates LRU behavior                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### ARC (Adaptive Replacement Cache)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         ARC Algorithm                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Cache split into 4 lists:                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  T1 (LRU, recent once)   │  T2 (LRU, recent twice)                                   │  │  │
    │  │  B1 (Ghost, evicted T1)  │  B2 (Ghost, evicted T2)                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Adaptation:                                                                             │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Recency-heavy workload → Expand T2, shrink T1                                     │  │  │
    │  │  • Frequency-heavy workload → Expand T1, shrink T2                                    │  │  │
    │  │  • Ghost lists track evicted items to detect patterns                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Adapts to workload, self-tuning LRU/LFU balance                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### Redis 캐시 eviction 정책

```bash
# Redis eviction policies
maxmemory 2gb

# allkeys-lru: LRU eviction over all keys
# volatile-lru: LRU eviction over keys with TTL set
# allkeys-random: Random eviction over all keys
# volatile-random: Random eviction over keys with TTL set
# volatile-ttl: Evict keys with shortest TTL first
# noeviction: Return errors when memory limit reached

# 일반적 설정
maxmemory-policy allkeys-lru
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 웹 캐시 서버
**상황**: 정적 컨텐츠 캐싱
**판단**: LRU 사용

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Cache Configuration Decision                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Workload Characteristics:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Temporal locality: Recently accessed files likely to be accessed again               │  │
    │  • Hot data: ~20% of files account for ~80% of requests                                │  │
    │  • Cache size: Large enough to hold hot set                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Decision: LRU
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Reasoning:                                                                             │  │
    │  • Temporal locality matches LRU assumption                                             │  │
    │  • Hot data stays in cache                                                              │  │
    │  • Well-understood, widely supported                                                    │  │
    │                                                                                         │  │
    │  Implementation:                                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Varnish: LRU                                                                         │  │  │
    │  │  Nginx: proxy_cache_path ... levels=1:2 keys_zone=static:100m inactive=60m          │  │  │
    │  │  Redis: maxmemory-policy allkeys-lru                                                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 캐시 교체 기대 효과

| 정책 | Hit Rate | 구현 | 사용처 |
|------|----------|------|--------|
| **LRU** | 높음 | 중간 | 일반적 |
| **LFU** | 중간 | 복잡 | 데이터베이스 버퍼 |
| **Random** | 낮음 | 단순 | 부트스트랩 |

### 모범 사례

1. **웹 캐시**: LRU
2. **DB 버퍼**: LRU + ARC
3. **CPU 캐시**: Approximate LRU (Pseudo-LRU)
4. **CDN**: LRU/TTL 혼합

### 미래 전망

1. **Machine Learning**: 패턴 학습
2. **Hardware**: Intel CAT
3. **Tiered**: 다계층 캐시

### ※ 참고 표준/가이드
- **Cache**: Replacement Algorithms
- **Redis**: Eviction Policies
- **Varnish**: VCL

---

## 📌 관련 개념 맵

- [캐시](./7_cache/120_cache.md) - 메모리 계층
- [TLB](./7_cache/121_tlb.md) - 주소 변환 캐시
- [캐시 일관성](./11_synchronization/122_cache_coherence.md) - 동기화
