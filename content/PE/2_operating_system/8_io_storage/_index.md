+++
title = "08. 입출력 및 저장장치 (IO Storage)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "컴퓨터의 입(키보드), 눈(모니터), 손(마우스) 그리고 기억 창고(디스크)를 관리하는 법을 배워요. 어떻게 하면 일기를 빨리 쓰고, 밖으로 말을 잘 전달할 수 있을지 고민하는 곳이랍니다!"
+++

# 08. 입출력 및 저장장치 (IO Storage)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU와 외부 장치 간의 속도 차이를 조율하고, 데이터를 영구적으로 보존하기 위한 제어 및 관리 기술.
> 2. **가치**: 버퍼링(Buffering), 스풀링(Spooling), 캐싱(Caching)을 통한 I/O 효율화 및 데이터 영속성 확보.
> 3. **융합**: 디스크 스케줄링(SCAN, C-SCAN) 및 RAID 기술을 통한 저장 장치의 성능과 안정성 동시 달성.

---

### Ⅰ. 개요 (Context & Background)
I/O 시스템은 OS 코드의 가장 큰 비중을 차지한다. 장치마다 특성이 제각각이기 때문에, OS는 이를 추상화하여 '디바이스 드라이버'라는 공통 인터페이스로 관리해야 한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 I/O 기법
- **Interrupt-driven I/O**: 비동기식 이벤트 처리
- **DMA (Direct Memory Access)**: 대량 데이터 전송 시 CPU 부하 경감
- **Double Buffering**: 읽기와 쓰기를 동시에 진행하여 지연 감소
- **Disk Scheduling**: 헤드의 이동 경로 최적화 (FSCAN, Look 등)

#### 2. 디스크 스케줄링 (ASCII)
```text
    [ Disk Head Movement (SCAN) ]
    
    Cylinder: 0 ---- 20 ---- 40 ---- 60 ---- 80 ---- 100
    Request: 30, 80, 10
    Current: 50 (Direction: 100)
    
    Path: 50 -> 80 -> 100 (End) -> 40 -> 30 -> 10
    (엘리베이터처럼 한 방향으로 끝까지 가면서 처리)
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### HDD vs SSD 아키텍처 관점 분석
| 항목 | HDD (Magnetic) | SSD (NAND Flash) |
| :--- | :--- | :--- |
| **접근 방식** | 기계적 (Seek + Rotation) | 전기적 (No Seek Time) |
| **스케줄링** | 헤드 이동 최적화 필수 | 불필요 (Random Access 동일) |
| **성능 병목** | 탐색 시간 (ms) | 버스 대역폭 (us) |
| **특징** | 저렴한 대용량 | 충격 강함, 저전력 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **I/O 대기(Wait)**는 전체 시스템 성능 저하의 주범이다. 기술사는 비동기 I/O(AIO)를 도입하거나, NVMe 인터페이스를 활용하여 대기 시간을 최소화하고, RAID 10 구성을 통해 성능과 가용성의 결착을 지어야 한다.

---

### Ⅴ. 기대효과 및 결론
저장 장치는 단순 저장을 넘어 '계산하는 스토리지(Computational Storage)'로 진화하고 있다. 데이터가 있는 곳에서 직접 연산하여 데이터 이동 비용을 제로화하는 것이 차세대 I/O의 지향점이다.
