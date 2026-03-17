+++
title = "09. 시스템 버스 및 인터커넥트 (Interconnect)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "도시 곳곳을 연결하는 '고속도로'와 '신호등' 같아요. 차(데이터)들이 서로 부딪히지 않고 가장 빠른 길로 목적지까지 갈 수 있게 규칙을 정해주는 고마운 길들이랍니다!"
+++

# 09. 시스템 버스 및 인터커넥트 (Interconnect)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU, 메모리, 입출력 장치 간의 데이터 및 제어 신호 전송을 담당하는 시스템의 신경망.
> 2. **가치**: 대역폭(Bandwidth) 확장과 중재(Arbitration) 로직 최적화를 통해 장치 간 데이터 병목 현상 해소.
> 3. **융합**: PCIe 6.0/7.0 및 CXL(Compute Express Link) 기술을 통해 이기종 컴퓨팅 자원 간의 메모리 공유 및 확장성 극대화.

---

### Ⅰ. 개요 (Context & Background)
인터커넥트는 독립된 하드웨어 구성 요소들을 하나의 유기적인 시스템으로 통합하는 결합 조직이다. 데이터의 이동 통로일 뿐만 아니라, 누가 언제 도로를 사용할지 결정하는 규칙(Protocol)이기도 하다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 버스 구조 및 중재
- **Bus Hierarchy**: System Bus, Local Bus, I/O Bus
- **Arbitration**: Centralized vs Distributed, Priority vs Round-robin
- **Synchronization**: Synchronous vs Asynchronous
- **Advanced Tech**: NoC (Network on Chip), CXL, NVLink

#### 2. 시스템 인터커넥트 구조 (ASCII)
```text
    [ System Interconnect Architecture ]
    
    +---------+       +---------+       +---------+
    |  CPU 1  |       |  CPU 2  |       |  GPU/AI |
    +----+----+       +----+----+       +----+----+
         |                 |                 |
    +----v-----------------v-----------------v----+
    |      System Bus / Crossbar Interconnect     |  <-- CXL / PCIe
    +----^-----------------^-----------------^----+
         |                 |                 |
    +----+----+       +----+----+       +----+----+
    |  Memory |       |  Storage|       | Network |
    +---------+       +---------+       +---------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 전송 방식: Serial vs Parallel
| 항목 | Parallel Bus (구형) | Serial Interconnect (현대) |
| :--- | :--- | :--- |
| **배선** | 수십 가닥 (복잡) | 소수 쌍 (단순, Diff-pair) |
| **클럭 스큐** | 심함 (속도 제한 원인) | 없음 (임베디드 클럭) |
| **속도** | 저속 (수백 MHz) | 초고속 (수십 GHz) |
| **대표 기술** | PCI, ISA, IDE | PCIe, USB, SATA |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 멀티 GPU 시스템이나 분산 메모리 환경에서 인터커넥트 대역폭은 성능의 절대적 제약 사항이다. 기술사는 **NUMA(Non-Uniform Memory Access)** 환경에서의 데이터 배치 최적화와 CXL을 통한 메모리 풀링(Memory Pooling) 도입을 적극 검토해야 한다.

---

### Ⅴ. 기대효과 및 결론
인터커넥트는 단순한 전선을 넘어 지능형 패브릭으로 진화하고 있다. 데이터센터 규모의 메모리 확장과 가속기 간의 끊김 없는 통신을 가능케 하는 인터커넥트 기술이 컴퓨팅의 미래를 결정할 것이다.
