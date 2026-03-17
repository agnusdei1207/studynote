+++
title = "261. L2 캐시"
date = "2026-03-11"
weight = 261
[extra]
categories = "studynote-computer-architecture"
keywords = ["컴퓨터구조", "L2 캐시", "메모리 계층", "속도와 용량의 타협"]
+++

# 261. L2 캐시 (Level 2 Cache)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: L2 (Level 2) 캐시는 L1 (Level 1) 캐시의 **Miss (Cache Miss)** 발생 시 처리 지연(Latency)을 최소화하는 **두 번째 방어선**이며, 고속 SRAM (Static Random Access Memory) 기반의 버퍼 계층이다.
> 2. **가치**: CPU (Central Processing Unit) 코어의 파이프라인 스톨(Pipeline Stall)을 방지하여 시스템 전체의 CPI (Cycles Per Instruction)를 개선하고, 메모리 액세스 병목을 완화한다.
> 3. **융합**: 멀티코어 아키텍처에서의 독립(Private) L2 설계와 데이터 일관성 프로토콜(MESI)의 연계, 그리고 L3와의 계층적 동작이 핵심이다.

+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
L2 캐시는 CPU 내부 메모리 계층 구조에서 L1 캐시 바로 아래 단계에 위치한 메모리로, L1 캐시에서 필요한 데이터를 찾지 못했을 때(Miss) 데이터를 제공하는 2차 저장소이다. 일반적으로 **SRAM (Static Random Access Memory)** 소자를 사용하여 DRAM (Dynamic Random Access Memory) 기반의 메인 메모리보다 훨씬 빠른 액세스 속도를 자랑하며, 용량은 L1보다 크고 L3보다 작은 특성을 지닌다. 현대 x86 및 ARM 아키텍처에서는 L1을 명령어/데이터로 분리한 Harvard 구조를 취하는 반면, L2는 **Unified Cache (통합 캐시)** 형태로 명령어와 데이터를 함께 저장하여 설계 효율성을 높이는 것이 일반적이다.

**💡 비유**
L1 캐시가 학생의 책상 위에 있는 *"오른손이 닿는 거리의 필기구"*라면, L2 캐시는 책상 옆에 있는 *"바로 꺼내 쓸 수 있는 서랍"*이자, 교실 뒤쪽의 *"공유 책장(L3)"*으로 가기 전에 거치는 *"개인 사물함"*과 같다.

**등장 배경 및 발전**
① **기존 한계**: CPU 클럭 속도의 급격한 상승(Moore's Law)에 비해 메인 메모리(DRAM)의 액세스 속도는 따라가지 못하는 **Memory Wall (메모리 벽)** 문제가 대두됨.
② **혁신적 패러다임**: 작고 빠른 L1만으로는 캐시 적중률(Hit Rate)이 한계가 있어, 약간의 지연(Latency)을 허용하되 용량을 획기적으로 확대하여 Miss율을 감소시키는 L2 계층이 도입됨.
③ **현재의 비즈니스 요구**: 고성능 컴퓨팅(HPC) 및 AI 시대에 대용량 데이터 셋 처리를 위해 L2 캐시의 용량을 코어당 수 MB로 대폭 확장하는 추세(AMD Zen 시리즈 등)로 진화 중이다.

**📢 섹션 요약 비유**
> 고속도로 톨게이트에서 하이패스 차로(L1)가 꽉 차면, 바로 옆의 일반 수도권 차로(L2)로 우회 처리하여 본선 진입을 돕는 구조와 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 특성/프로토콜 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **SRAM Cell Array** | 실제 데이터 저장 | 6개의 트랜지스터(6T) 구성으로 플립플롭 형태 유지, 리프레시 불필요 | L1보다 밀도가 높은 약간 느린 SRAM 셀 사용 | 고밀도 수납함 |
| **Tag Comparator** | 데이터 존재 여부 판별 | 요청 주소의 태그 비트를 비교하여 Hit/Miss 판단 | Way가 많을수록 병렬 비교 회로 증가 | 색인 목록 |
| **Inclusive Policy** | L1과의 데이터 관리 | L1의 모든 데이터는 L2에 포함(Inclusive)되거나 배제(Exclusive)됨 | L3 트래픽 최적화를 위한 Inclusive 속성 선호 | 사본 존재 여부 체크 |
| **Fill Buffer** | 메모리 데이터 로딩 | DRAM으로부터 데이터가 도착할 때까지 버퍼링 | MissPenalty 숨기기 위한 파이프라이닝 | 물류 적재 대기선 |
| **Write Buffer** | 데이터 쓰기 지연 | Write-Through/Back 방식 시 메모리 업데이트 대기 | CPU의 명령 실행 흐름 차단 방지 | 배달 대기열 |

**메모리 계층 구조 및 데이터 흐름**

L2 캐시는 메인 메모리와 L1 사이에서 **Critical Path (임계 경로)**를 형성하며, 데이터 요청 시 다음과 같은 단계를 거쳐 동작한다.

```text
   [ CPU Core ]
       |
       v
+------------------------+      (1) Request (Load/Store)
|      L1 Cache          |----->| Miss (Data Not Found) |
+------------------------+      +-----------------------+
       |                                    ^
       | Miss (Victim)                      | Fill (Allocated)
       v                                    |
+------------------------+      (2) L2 Lookup (Tag Check)
|      L2 Cache          |<-----+-----------------------+
|   [ Private Per Core ] |      |   Hit? Return Data    |
+------------------------+      +-----------+-----------+
       | Miss (Penalty)                |
       v                              | (Fast Path)
+------------------------+            | (CPU to L2 ~10-20 Cycles)
|      L3 / System Agent |<-----------+
|     (Shared LLC)       |       (3) L1 Update (Fill)
+------------------------+
       |
       v
  [ Main Memory ]   (4) DRAM Access (~100-200 Cycles)
```

**[도해 설명]**
1. **CPU 요청**: 코어가 주소를 생성하여 L1 캐시로 요청을 전송한다.
2. **L1 Miss**: L1에서 데이터를 찾지 못하면(Miss), 요청이 하위 계층인 L2로 전달된다. 이때 L2는 L1보다 용량이 크고 **Associativity (연관성)**가 높아(예: 8-way, 16-way) 데이터를 찾을 확률이 높다.
3. **L2 Hit**: L2에 데이터가 존재하면(Hit), 데이터는 버스를 통해 다시 L1으로 전송되고(일반적으로 Critical Word First), 최종적으로 CPU로 전달된다. 이 Latency는 보통 10~20 클럭 사이이다.
4. **L2 Miss & DRAM Access**: L2에도 데이터가 없으면, 요청은 L3(LLC) 또는 시스템 에이전트를 거쳐 DRAM으로 전달된다. 이 과정은 수백 클럭이 소요되므로 L2의 Hit Rate는 시스템 성능에 결정적이다.

**심층 동작 원리 및 알고리즘**

L2 캐시의 성능은 **Associativity (연관성)**와 **Replacement Policy (교체 정책)**에 의해 좌우된다. L1보다 큰 용량을 확보하기 위해 **Set-Associative (세트 연관 방식)**을 사용하며, L2 Miss가 발생했을 때 기존 데이터를 덮어쓸 결정을 내려야 한다.

1.  **LRU (Least Recently Used)**: 가장 오랫동안 사용되지 않은 블록을 교체. L2는 L1보다 많은 수의 Way를 가지므로 True LRU 구현이 비싸다. 대신 **PLRU (Pseudo LRU)** 알고리즘을 사용하여 비트 하나의 정보만으로 교체 대상을 추정한다.
2.  **Non-Inclusive vs Exclusive**:
    *   **Inclusive**: L1 데이터의 부분 집합을 유지. L3 관리가 용이하나 L2 공간 낭비 발생 가능.
    *   **Exclusive**: L1과 L2가 중복되지 않음. 효율적이나 일관성 유지가 복잡함.

**핵심 동작 코드 (Pseudo-Code)**

```c
// L2 Cache Controller Logic (Simplified)
struct L2_Entry {
    bool valid;
    bool dirty;         // Write-Back 여부
    int tag;
    int data[BLOCK_SIZE];
    int lru_counter;    // PLRU 비트
}

void access_L2(uint64_t addr) {
    int index = get_index(addr);
    int tag   = get_tag(addr);

    // 1. Tag Check (Parallel)
    if (cache_set[index].hit(tag)) {
        update_lru(index, way); // Hit 시 LRU 업데이트
        return cache_set[index].data;
    } 
    else {
        // 2. Miss Handling
        handle_miss(addr);
        
        // 3. Fill from Memory (or L3)
        // victim selection using PLRU
        int victim_way = select_victim_lru(index);
        
        if (cache_set[index][victim_way].dirty) {
            write_back_to_L3(cache_set[index][victim_way]);
        }
        
        allocate_block(index, victim_way, addr, fetch_from_L3(addr));
    }
}
```

**📢 섹션 요약 비유**
> 복잡한 창고 시스템에서, L2는 넓은 적재 공간과 효율적인 정리 시스템(PLRU)을 갖춘 **'종합 물류 센터'**와 같아서, 작은 파출함(L1)에 없는 물건이라도 즉시 찾아줌으로써 배송 차량(CPU)이 멈추지 않게 합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: L1 vs L2 vs L3**

| 비교 항목 (Metric) | L1 Cache | **L2 Cache** | L3 Cache (LLC) |
|:---|:---|:---|:---|
| **위치 (Location)** | 코어 내부 (Core 내) | 코어 내부 또는 코어 외부 인접 | 코어 외부 (다이 내/외부) |
| **용량 (Capacity)** | 32KB ~ 128KB (Split I/D) | **256KB ~ 4MB** (Unified) | 32MB ~ 128MB (Shared) |
| **Latency** | 3 ~ 5 Cycles | **10 ~ 20 Cycles** | 40 ~ 80 Cycles |
| **구조 (Structure)** | Harvard (I/D 분리) | **Unified (통합)** | Unified (Shared) |
| **소유권 (Ownership)** | Private (Exclusive) | **Private (Exclusive)** | Shared (Inclusive/Non-Inclusive) |
| **Primary Goal** | 즉시 액세스 | **Miss 감소 (Buffer)** | 대용량 데이터 공유 |

**과목 융합 관점**

1.  **운영체제 (OS)와의 연계**:
    *   **Context Switching (문맥 교환)**: 프로세스가 전환될 때 L1/L2 캐시는 무효화(Flush)되거나 씻겨나가며, 이는 **Cold Miss**를 유발하여 초기 성능 저하를 야기한다. L2가 클수록 재사용 가능한 데이터가 남을 확률이 높아 성능 회복이 빠르다.
    *   **Page Walk**: 가상 메모리 주소 변환 중 TLB Miss 발생 시, 페이지 테이블 워크(Page Walk) 과정에서 접근하는 메모리 주소를 캐싱하는 역할을 하여 TLB Miss 페널티를 줄인다.

2.  **컴퓨터 네트워크(통신)와의 연계**:
    *   **MESI Protocol**: 멀티코어 환경에서 L2는 L1보다 **Bus snooping**에 대한 부담이 덜하지만, 여전히 L1 캐시의 **Write-Back**을 처리하며 코어 간 데이터 일관성을 유지하는 역할을 수행한다. L2의 크기가 크면 시스템 버스로의 트래픽을 줄여 네트워크 병목을 완화한다.

**📢 섹션 요약 비유**
> L1이 단순한 '계산기'라면, L2는 '보조 배터리 및 확장 슬롯'이 장착된 '태블릿 PC'와 같아서, 본체의 전력(용량)이 부족할 때 끊김 없이 연결하여 작업을 지속하게 합니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **시나리오 A: 고성능 게이임/HPC 서버 설계**
    *   **문제**: 큰 용량의 데이터 셋(예: 4K 게임 텍스처)을 처리해야 함. L1 Miss가 빈번하여 성능 병목 발생.
    *   **의사결정**: L2 캐시의 **용량을 2MB 이상(AMD Zen 3/4 아키텍처 처럼)**으로 대폭 확장. 이로 인해 다이 면적(Die Area)이 증가하고 비용이 상승하지만, 실제 게임 프레임(IPS)은 획기적으로 상승.
    *   **KPI**: L2 Cache Hit Rate > 95%, Memory Access Latency -20%.

2.  **시나리오 B: 저전력 임베디드/IoT 시스템**
    *   **문제**: 배터리 수명과 칩 면적이 최우선. L2 캐시는 **SRAM**으로 구성되어 있어 **Leakage Power (누전 전력)**가 발생함.
    *   **의사결정**: L2 캐시를 아주 작게(128KB~256KB) 설계하거나, L2를 분리(Split)하여 필요 시에만 Power Gating을 적용.

3.  **시나리오 C: 멀티코어 데이터베이스 서버**
    *   **문제**: 여러 코어가 동일한 데이터를 갱신하며 **False Sharing** 발생.
    *   **의사결정**: L2 캐시의 Line 크기와 Coherency Protocol을 최적화. 서버용 CPU(코드명 Ice Lake-SP 등)에서는 L2를 갖는 것이 전력 대비 성능 면에서 유리하므로 Private L2 구조를 유지.

**도입 체크리스트**

-   **[ ] 성능 목표 설정**: CPI 개선 목표치 대비 L2 Miss 감소량 분석 수행 여부
-   **[ ] 전력 예산**: SRAM Cell의 동적/정적 전력 소모가 TDP (Thermal Design Power) 내에 포함되는지 검토
-   **[ ] 멀티코어 동기화**: Inclusive L2 정책 시 L3 트래픽 과부하 걱정 없는지 점검
-   **[ ] 코어 간 간섭**: 한 코어의 L2 버스트 액세스가 다른 코어의 L2 액세스를