+++
title = "06. 캐시 메모리 및 계층 구조 (Cache)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "공부할 때 자주 보는 책은 책상(Cache) 위에 두고, 가끔 보는 책은 가방(Memory)에, 아주 안 보는 책은 먼 창고(Disk)에 두는 것과 같아요. 책상 위에 책을 잘 골라 놓아야 숙제를 빨리 끝낼 수 있겠죠?"
+++

# 06. 캐시 메모리 및 계층 구조 (Cache)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU와 주기억장치 사이의 속도 차이를 극복하기 위해 참조의 지역성(Locality)을 활용하는 고속 임시 저장소.
> 2. **가치**: 캐시 적중률(Hit Rate) 극대화를 통한 평균 메모리 접근 시간(AMAT) 단축 및 시스템 처리량(Throughput)의 비약적 향상.
> 3. **융합**: 멀티코어 환경의 캐시 일관성(Coherency) 프로토콜(MESI) 및 쓰기 정책(Write-through/back)을 통한 데이터 무결성 보장.

---

### Ⅰ. 개요 (Context & Background)
메모리 계층 구조는 '속도, 용량, 비용'의 트레이드오프를 해결하기 위한 아키텍처적 해법이다. CPU의 연산 속도는 비약적으로 발전한 반면, DRAM의 접근 속도는 상대적으로 더디게 발전한 '메모리 벽(Memory Wall)' 문제를 해결하기 위해 도입되었다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 구성 요소 및 정책
- **Locality**: Temporal(시간적), Spatial(공간적) 지역성
- **Mapping**: Direct, Fully Associative, Set-Associative
- **Replacement**: LRU (Least Recently Used), LFU, Random
- **Consistency**: MESI (Modified, Exclusive, Shared, Invalid)

#### 2. 캐시 매핑 아키텍처 (ASCII)
```text
    [ Cache Mapping Structure ]
    
    CPU Address: [  Tag  |  Set Index  |  Offset  ]
                      |          |            |
             +--------v--------+ |            |
             |   Tag Directory | |            |
             +-----------------+ |            |
                      | Compare  |            |
             +--------v----------v------------v--------+
             |       Cache Data Array (SRAM)          |
             +----------------------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 쓰기 정책: Write-through vs Write-back
| 구분 | Write-through | Write-back |
| :--- | :--- | :--- |
| **동작** | 캐시와 메모리 동시 업데이트 | 캐시만 업데이트 후 교체 시 메모리 기록 |
| **속도** | 느림 (메모리 쓰기 대기) | 빠름 (캐시 속도로 처리) |
| **일관성** | 유지 쉬움 | 복잡함 (Dirty Bit 필요) |
| **트래픽** | 높음 | 낮음 (효율적) |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 L1, L2, L3 캐시의 크기와 정책은 CPU의 성능을 좌우한다. 기술사는 특히 **False Sharing** 문제를 방지하기 위해 데이터 구조를 캐시 라인(64B) 단위로 정렬(Alignment)하는 최적화 전략을 수립해야 한다.

---

### Ⅴ. 기대효과 및 결론
캐시는 현대 아키텍처에서 가장 복잡하고 중요한 자원이다. 향후 비휘발성 메모리(NVDIMM)와 결합된 하이브리드 캐시 구조나 AI 전용 온칩 메모리(SRAM) 확장이 가속화될 전망이다.
