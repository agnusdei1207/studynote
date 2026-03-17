+++
title = "06. 주기억장치 관리 (Main Memory)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "공부방(메모리)에 책상을 어떻게 배치할지 정하는 것과 같아요. 책상이 너무 크면 자리가 모자라고, 너무 작으면 책을 다 못 올리죠. 친구들에게 방을 어떻게 나누어 줄지 공평하게 결정하는 법을 배운답니다!"
+++

# 06. 주기억장치 관리 (Main Memory)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 한정된 물리 메모리(RAM)를 효율적으로 분할하여 실행 중인 프로세스들에게 할당하고 보호하는 자원 관리 기술.
> 2. **가치**: 단편화(Fragmentation) 최소화 및 주소 바인딩(Address Binding)을 통한 메모리 이용률 극대화.
> 3. **융합**: 하드웨어 베이스 레지스터(Base Register)를 이용한 메모리 보호와 OS의 할당 정책(Buddy, Slab)의 결합.

---

### Ⅰ. 개요 (Context & Background)
메모리는 CPU가 직접 접근할 수 있는 유일한 대량 저장소다. 프로세스가 실행되려면 반드시 메모리에 올라와야 하며, OS는 어떤 프로세스를 어디에 배치할지, 그리고 어떻게 다른 프로세스로부터 보호할지를 책임진다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 관리 기법
- **Contiguous Allocation**: 연속 할당 (Fixed/Variable Partition)
- **Fragmentation**: 내부 단편화(남는 공간), 외부 단편화(조각난 공간)
- **Address Binding**: Compile, Load, Execution time binding
- **Dynamic Loading/Linking**: 필요한 시점에 메모리 로드 및 연결

#### 2. 메모리 할당 정책 (ASCII)
```text
    [ Memory Allocation Strategies ]
    
    Free Blocks: [ 10KB ]  [ 20KB ]  [ 5KB ]  [ 15KB ]
    Request: 8KB
    
    1. First-fit : [ 10KB(Used:8, Free:2) ] (가장 먼저 찾은 곳)
    2. Best-fit  : [ 10KB ] [ 20KB ] [ 5KB ] [ 15KB(Used:8, Free:7) ] 
                   -> 사실은 10KB가 가장 적절 (가장 작은 틈새 선택)
    3. Worst-fit : [ 20KB(Used:8, Free:12) ] (가장 큰 틈새 선택)
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 단편화 해결 기법 비교
| 기법 | 페이징 (Paging) | 세그먼테이션 (Segmentation) | 압축 (Compaction) |
| :--- | :--- | :--- | :--- |
| **방식** | 불연속 할당 (고정 크기) | 논리적 단위 분할 (가변 크기) | 빈 공간을 한데 모음 |
| **장점** | 외부 단편화 없음 | 의미 중심 관리 | 외부 단편화 해결 |
| **단점** | 내부 단편화 발생 | 외부 단편화 발생 가능 | 시스템 중단 및 오버헤드 |
| **활용** | 현대 대부분의 OS | 특정 OS 보조 수단 | 임베디드, 특수 환경 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Memory Leak(메모리 누수)**은 시스템의 서행 및 패닉을 유발한다. 기술사는 가비지 컬렉션(GC) 메커니즘을 이해하고, 커널 수준의 슬랩 할당자(Slab Allocator)를 통해 잦은 객체 생성/삭제 시 발생하는 오버헤드를 최적화해야 한다.

---

### Ⅴ. 기대효과 및 결론
메모리 관리는 시스템의 응답성과 직결된다. 향후 비휘발성 메모리(NVDIMM)가 보편화되면, 전원이 꺼져도 메모리 상태가 유지되는 '영구 메모리 관리'가 OS의 새로운 핵심 과제가 될 것이다.
