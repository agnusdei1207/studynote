+++
title = "07. 가상 메모리 관리 (Virtual Memory)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "공부할 책은 100권인데 책상은 1권만 놓을 수 있을 때, 지금 읽는 페이지(Page)만 책상에 두고 나머지는 가방에 넣어두는 마술이에요. 덕분에 아주 좁은 책상에서도 수많은 책을 공부할 수 있답니다!"
+++

# 07. 가상 메모리 관리 (Virtual Memory)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 실제 물리 메모리 크기보다 큰 프로세스를 실행할 수 있도록 하는 주소 추상화 및 요구 페이징(Demand Paging) 기술.
> 2. **가치**: 프로세스 간 독립적인 논리 공간 제공을 통한 보안 강화 및 메모리 이용률의 극대화.
> 3. **융합**: MMU 하드웨어와 OS의 페이지 교체 알고리즘(LRU, LFU)의 긴밀한 공조를 통한 스래싱(Thrashing) 방지.

---

### Ⅰ. 개요 (Context & Background)
가상 메모리는 현대 OS의 가장 위대한 발명 중 하나다. 프로그램 전체가 메모리에 있지 않아도 실행 가능하다는 '발상의 전환'을 통해 멀티태스킹의 한계를 돌파했다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 메커니즘
- **Demand Paging**: 필요한 페이지만 메모리에 로드
- **Page Fault**: 페이지가 메모리에 없을 때 발생하는 인터럽트
- **Page Replacement**: 메모리가 꽉 찼을 때 쫓아낼 페이지 결정
- **Working Set**: 프로세스가 일정 시간 동안 집중적으로 참조하는 페이지 집합

#### 2. 요구 페이징 처리 절차 (ASCII)
```text
    [ Page Fault Handling Steps ]
    
    1. CPU Reference -> Page Table (Invalid bit)
    2. Trap to OS (Page Fault)
    3. OS looks at backing store (Disk)
    4. Find empty frame in RAM
    5. Swap page into frame
    6. Update Page Table (Set to Valid)
    7. Restart Instruction
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 페이지 교체 알고리즘 비교
| 알고리즘 | FIFO | LRU (Least Recently Used) | LFU (Least Frequently Used) |
| :--- | :--- | :--- | :--- |
| **기준** | 먼저 들어온 페이지 교체 | 가장 오랫동안 미사용된 것 | 참조 횟수가 가장 적은 것 |
| **장점** | 구현 간단 | 지역성 원리 충실 (고성능) | 집중 참조 시 유리 |
| **단점** | Belady's Anomaly 발생 | 하드웨어 지원 필요 (오버헤드) | 최근 로드된 페이지 제거 가능성 |
| **평가** | 성능 낮음 | 실무 표준 | 특수 목적 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Thrashing(스래싱)** 현상은 시스템을 마비시킨다. CPU가 일은 안 하고 페이지 교체에만 모든 시간을 쓰는 상황이다. 기술사는 워킹 셋 알고리즘을 적용하거나, 다중 프로그래밍의 정도(Degree)를 조절하여 시스템 평형 상태를 유지해야 한다.

---

### Ⅴ. 기대효과 및 결론
가상 메모리는 클라우드 서비스의 '오버커밋(Overcommit)' 기술의 근간이다. 향후 초고속 저장 장치(NVMe)와 통합된 계층형 메모리 구조에서 가상 메모리의 역할은 더욱 확장될 것이다.
