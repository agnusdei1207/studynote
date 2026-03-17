+++
title = "08. 입출력 및 저장 장치 (Storage)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "컴퓨터가 쓴 일기장을 안전하게 보관하는 '금고'와, 컴퓨터가 밖으로 말을 하거나 듣는 '입과 귀'에 대해 배우는 곳이에요. 어떻게 하면 일기를 빨리 쓰고, 잃어버리지 않게 잘 지킬 수 있을까요?"
+++

# 08. 입출력 및 저장 장치 (Storage)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU와 외부 세계(Peripherals) 및 영구 저장소 간의 데이터 교환을 제어하고 가속하는 서브시스템.
> 2. **가치**: DMA(Direct Memory Access)와 인터럽트 제어를 통한 CPU 부하 경감 및 RAID/ZNS 기반의 데이터 신뢰성/성능 확보.
> 3. **융합**: NVMe 프로토콜과 NAND 플래시 아키텍처의 결합을 통해 스토리지 병목 현상을 해소하고 초고속 데이터 레이크 구축.

---

### Ⅰ. 개요 (Context & Background)
I/O 시스템은 컴퓨터의 소통 창구다. 연산 성능이 아무리 뛰어나도 데이터를 가져오고 저장하는 속도가 느리면 시스템 전체 성능은 저하된다(I/O Bound).

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 I/O 제어 방식
- **Programmed I/O**: CPU가 직접 상태 체크 (Polling)
- **Interrupt-driven I/O**: 장치가 완료 알림 (비동기)
- **DMA (Direct Memory Access)**: CPU 개입 없이 메모리-장치 간 전송
- **I/O Channel/Processor**: 별도의 전용 프로세서가 I/O 전담

#### 2. 스토리지 계층 구조 (ASCII)
```text
    [ I/O & Storage Hierarchy ]
    
    (Fast) +------------------------+
           |   CPU / Cache          |
           +------------------------+
           |   Main Memory (DRAM)   |
           +-----------+------------+
                       | NVMe / PCIe
           +-----------v------------+
           |   SSD (NAND Flash)     |
           +-----------+------------+
                       | SAS / SATA
           +-----------v------------+
    (Slow) |   HDD / Tape Library   |
           +------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### I/O 제어: Polling vs Interrupt
| 구분 | Polling (Programmed) | Interrupt-driven |
| :--- | :--- | :--- |
| **CPU 부하** | 매우 높음 (무한 루프) | 낮음 (필요할 때만 호출) |
| **효율성** | 단순 장치에 적합 | 복잡한 멀티태스킹에 필수 |
| **반응 속도** | 즉각적 (대기 중이면) | 약간의 오버헤드 (Context Switch) |
| **활용** | 마우스, 키보드 (간단) | 네트워크, 디스크 (복잡) |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **RAID** 구성은 가용성과 성능 사이의 전략적 선택이다. 기술사는 서비스의 특성(Read-heavy vs Write-heavy)에 따라 RAID 10(고성능/고비용)과 RAID 5/6(효율성/패리티 오버헤드) 사이의 결착을 지어야 한다.

---

### Ⅴ. 기대효과 및 결론
스토리지 기술은 NVMe over Fabrics (NVMe-oF)와 계산형 스토리지(Computational Storage)로 진화하고 있다. 데이터가 저장된 곳에서 직접 연산하는 패러다임이 차세대 데이터센터의 핵심이 될 것이다.
