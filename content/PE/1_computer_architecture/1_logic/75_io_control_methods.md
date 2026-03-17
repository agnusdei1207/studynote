+++
title = "I/O 제어 방식 (I/O Control Methods)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# I/O 제어 방식 (I/O Control Methods)

## 핵심 인사이트 (3줄 요약)
1. I/O 제어 방식은 Programmed I/O, Interrupt-Driven I/O, DMA(Direct Memory Access) 세 가지가 있으며, CPU 개입 정도와 복잡도가 다르다
2. Programmed I/O는 CPU가 모든 것을 제어하고, Interrupt I/O는 이벤트 기반으로 CPU 효율을 높이며, DMA는 CPU 독립적으로 대량 전송한다
3. 기술사시험에서는 세 방식의 비교, 각 방식의 장단점, 적용 분야, 성능 특성이 핵심이다

## Ⅰ. 개요 (500자 이상)

I/O 제어 방식은 **CPU와 I/O 장치 사이의 데이터 전송을 제어하는 세 가지 기본 방식**으로, CPU 개입 정도와 하드웨어 복잡도에 따라 분류된다. 각 방식은 장치의 특성과 시스템 요구사항에 따라 선택된다.

```
I/O 제어 방식 분류:

1. Programmed I/O (Polling):
   - CPU가 직접 제어
   - 주기적 상태 확인
   - 단순하지만 비효율

2. Interrupt I/O:
   - 장치가 이벤트 알림
   - CPU 효율적
   - 중간 복잡도

3. DMA:
   - 전용 컨트롤러
   - CPU 독립 전송
   - 가장 복잡하지만 효율적

선택 기준:
- 전송 속도
- 데이터 양
- CPU 부하
- 하드웨어 비용
```

**세 방식의 핵심 차이:**

| 특성 | Programmed I/O | Interrupt I/O | DMA |
|------|----------------|----------------|-----|
| CPU 개입 | 모든 바이트 | 완료 시 | 초기화/완료 |
| 인터럽트 | 없음 | 있음 | 있음 |
| 복잡도 | 낮음 | 중간 | 높음 |

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Programmed I/O (Polling)

```
Programmed I/O 구조:

CPU ←─→ Device Interface
         │
      Status Register
      Data Register

동작:
while (!ready) {
    status = read(Status);
}
data = read(Data);

CPU 사용:
- 전송 중 계속 실행
- Busy Waiting
- 100% CPU 점유

장점:
- 단순한 하드웨어
- 확실한 제어
- 예측 가능

단점:
- CPU 낭비
- 느린 응답
- 다중 작업 불가
```

### Interrupt-Driven I/O

```
Interrupt I/O 구조:

CPU ←─→ Device Interface ←─→ Interrupt Controller
         │                              │
      Status Register              IRQ

동작:
1. Device가 데이터 준비
2. Interface가 IRQ 활성
3. CPU가 ISR 실행
4. ISR에서 I/O 처리
5. IRET로 복귀

CPU 사용:
- 전송 대기 중 다른 작업 가능
- 인터럽트 시에만 CPU 사용
- 효율적

장점:
- CPU 효율 높음
- 빠른 응답
- 멀티태스킹 가능

단점:
- 복잡한 하드웨어 (PIC)
- 오버허드 (Context Switch)
- 인터럽트 지연
```

### DMA (Direct Memory Access)

```
DMA 구조:

CPU ←─→ DMA Controller ←─→ Device
           │                  ↓
        Memory             Data Bus

동작:
1. CPU가 DMA 초기화
   - Source Address
   - Dest Address
   - Byte Count

2. Device가 DREQ
3. DMA가 HRQ → CPU
4. CPU가 HLDA → DMA
5. DMA가 Memory ↔ Device 전송
6. 완료 후 인터럽트

CPU 사용:
- 초기화/완료에만 개입
- 전송 중 다른 작업 가능
- 최소한의 CPU 사용

장점:
- 가장 높은 효율
- 대량 전송에 적합
- CPU 해방

단점:
- 가장 복잡한 하드웨어
- 버스 Contention
- 설정 오버헤드
```

### 상세 비교

```
1. 전송 단위:
   - Polling: 바이트 단위
   - Interrupt: 바이트 단위
   - DMA: 블록 단위

2. CPU 개입:
   - Polling: 모든 바이트
   - Interrupt: 완료 시
   - DMA: 초기화/완료

3. 하드웨어:
   - Polling: 단순
   - Interrupt: PIC 필요
   - DMA: DMAC 필요

4. 속도:
   - Polling: 느림
   - Interrupt: 중간
   - DMA: 빠름
```

### 타이밍 비교

```

1000 바이트 전송:

Polling:
- CPU가 1000번 Status 확인
- 1000번 Data 전송
- 총 CPU 시간: ~10000 클럭

Interrupt I/O:
- 1000번 인터럽트
- 1000번 ISR 실행
- 총 CPU 시간: ~5000 클럭

DMA:
- 1번 초기화
- 1번 인터럽트 (완료)
- 총 CPU 시간: ~100 클럭

효율:
Polling: 1%
Interrupt: 2%
DMA: 99%
```

### 하이브리드 방식

```
하이브리드 I/O:

상황별 선택:
- 저속 장치: Polling
- 중속 장치: Interrupt
- 고속 장치: DMA

예:
- 키보드: Interrupt
- 마우스: Interrupt
- 프린터: DMA
- 디스크: DMA
- 네트워크: DMA + Interrupt

유연한 시스템:
각 장치에 최적의 방식 적용
```

## Ⅲ. 융합 비교

### 세 방식 비교표

| 비교 항목 | Programmed I/O | Interrupt I/O | DMA |
|----------|----------------|----------------|-----|
| CPU 개입 | 매우 높음 | 중간 | 낮음 |
| 전송 속도 | 느림 | 중간 | 빠름 |
| 하드웨어 | 단순 | 중간 | 복잡 |
| 인터럽트 | 없음 | 있음 | 있음 |
| 비용 | 낮음 | 중간 | 높음 |
| 응용 | 단순 장치 | 문자 장치 | 블록 장치 |

### 성능 특성

| 방식 | 1000B 전송 시간 | CPU 점유율 | 인터럽트 수 |
|------|----------------|-----------|-----------|
| Polling | 10ms | 99% | 0 |
| Interrupt | 5ms | 50% | 1000 |
| DMA | 0.1ms | 1% | 1 |

### 장치별 적합성

| 장치 | 속도 | 적합 방식 | 이유 |
|------|------|----------|------|
| 키보드 | 저속 | Interrupt | 비주기적 |
| 마우스 | 저속 | Interrupt | 이벤트 |
| 프린터 | 중속 | DMA | 대량 |
| 디스크 | 고속 | DMA | 블록 |
| 디지털 I/O | - | Polling | 단순 |

## Ⅳ. 실무 적용 및 기술사적 판단

### PC 시스템

```
PC I/O 구성:

키보드 (Port 0x60):
- Interrupt I/O (IRQ 1)
- Scancode 전송
- CPU가 키 입력 처리

마우스 (PS/2, USB):
- Interrupt I/O
- 이동 이벤트
- DPI 변화

디스크 (SATA):
- DMA (Bus Master)
- Multi-sector Transfer
- NCQ (Native Command Queuing)

네트워크 (Ethernet):
- DMA + Interrupt
- Packet DMA 전송
- Completion Interrupt

사운드:
- DMA (Playback)
- Interrupt (Capture)
```

### 임베디드 시스템

```
임베디드 I/O 전략:

MCU (Microcontroller):
- GPIO: Polling
- UART: Interrupt
- SPI/DMA: High-speed
- Timer: Interrupt

선택 가이드:
- 단순성: Polling
- 전력: Interrupt
- 성능: DMA

예: ARM Cortex-M
- NVIC (Nested Vectored Interrupt Controller)
- DMA Controller
- 효율적인 전력 관리
```

### 고성능 서버

```

서버 I/O:

NVMe SSD:
- Multiple Queue
- DMA per Queue
- Interrupt Aggregation

10GbE:
- Hardware Offload
- DMA Direct to Memory
- MSI-X (Multiple Interrupts)

RDMA (Remote DMA):
- Network DMA
- Zero-copy
- CPU 최소 개입

목표:
- I/O Processing을 CPU에서 분리
- Hardware만으로 처리
```

### 실시간 시스템

```
Real-time I/O:

요구사항:
- Deterministic latency
- Bounded response
- Priority handling

해결:
Polling for Critical:
- Critical Loop에서 Polling
- 예측 가능한 응답 시간
- 최소 지연

Interrupt for Normal:
- 일반 작업은 Interrupt
- Priority-based

DMA for Bulk:
- 대량 데이터는 DMA
- CPU 해방

예: Industrial Control
- Sensor: Polling (100µs Loop)
- Actuator: DMA (Waveform Output)
- Alarm: Interrupt (Highest Priority)
```

## Ⅴ. 기대효과 및 결론

I/O 제어 방식은 상황에 따라 선택한다. Polling은 단순, Interrupt는 효율, DMA는 고속에 적합하다.

## 📌 관련 개념 맵

```
I/O 제어 방식
├── Programmed I/O
│   ├── Polling Loop
│   ├── Status Check
│   ├── 단순함
│   └── 비효율
├── Interrupt I/O
│   ├── Event-driven
│   ├── PIC
│   ├── ISR
│   └── 효율적
├── DMA
│   ├── Controller
│   ├── Bus Mastering
│   ├── Block Transfer
│   └── 최고 효율
└── 선택
    ├── 속도
    ├── 양
    ├── 비용
    └── 응용
```

## 👶 어린이를 위한 3줄 비유 설명

1. I/O 제어 방식은 음식 주문 방법과 같아요. Polling는 가게 계속 가서 "됐어요?" 물어보는 거고, Interrupt는 가게가 전화해주는 거예요
2. DMA는 배달 서비스 같아요. 한 번 주문하면 가게가 직접 배달해줘서 내가 가게에 갈 필요가 없어요
3. 단순한 건 직접(Polling), 중요한 건 알려줘(Interrupt), 많은 건 배달(DMA)로 구분해서 사용해요

```python
# I/O 제어 방식 시뮬레이션 및 비교

from typing import List
import time


class TransferResult:
    """전송 결과"""
    def __init__(self, method: str, time: float, cpu_usage: float, interrupts: int):
        self.method = method
        self.time = time
        self.cpu_usage = cpu_usage
        self.interrupts = interrupts


class IOController:
    """I/O 컨트롤러"""

    @staticmethod
    def programmed_io(data_size: int, byte_time: float = 0.001) -> TransferResult:
        """Programmed I/O (Polling) 시뮬레이션"""
        print(f"\n[Programmed I/O] {data_size} 바이트 전송")

        # 매 바이트마다 Polling
        total_time = 0
        poll_count = 0

        for i in range(data_size):
            # Status 확인 (Polling)
            # 실제로는 여러 번 Polling하지만 간소화
            poll_count += 1
            time.sleep(0.0001)  # Polling delay
            total_time += 0.0001

            # Data 전송
            time.sleep(byte_time)
            total_time += byte_time

            if (i + 1) % 100 == 0:
                print(f"  {i + 1}/{data_size} bytes transferred")

        cpu_usage = 99.0  # 거의 100%
        interrupts = 0

        print(f"  Complete: {total_time:.3f}s")
        print(f"  CPU Usage: {cpu_usage}%")
        print(f"  Interrupts: {interrupts}")

        return TransferResult("Polling", total_time, cpu_usage, interrupts)

    @staticmethod
    def interrupt_io(data_size: int, byte_time: float = 0.001) -> TransferResult:
        """Interrupt I/O 시뮬레이션"""
        print(f"\n[Interrupt I/O] {data_size} 바이트 전송")

        total_time = 0
        isr_time = 0.0001  # ISR 오버헤드

        for i in range(data_size):
            # Device가 데이터 준비 시간
            time.sleep(byte_time)
            total_time += byte_time

            # 인터럽트 발생
            time.sleep(isr_time)
            total_time += isr_time

            if (i + 1) % 100 == 0:
                print(f"  {i + 1}/{data_size} bytes transferred")

        cpu_usage = 50.0  # 대기 중에는 다른 작업 가능
        interrupts = data_size

        print(f"  Complete: {total_time:.3f}s")
        print(f"  CPU Usage: {cpu_usage}%")
        print(f"  Interrupts: {interrupts}")

        return TransferResult("Interrupt", total_time, cpu_usage, interrupts)

    @staticmethod
    def dma_transfer(data_size: int, byte_time: float = 0.001) -> TransferResult:
        """DMA 전송 시뮬레이션"""
        print(f"\n[DMA] {data_size} 바이트 전송")

        # 초기화
        init_time = 0.0001
        time.sleep(init_time)
        total_time = init_time

        # DMA 전송 (CPU 개입 없음)
        transfer_time = data_size * byte_time
        time.sleep(transfer_time * 0.1)  # 시뮬레이션 속도
        total_time += transfer_time * 0.1

        # 완료 인터럽트
        completion_time = 0.0001
        time.sleep(completion_time)
        total_time += completion_time

        cpu_usage = 1.0  # 초기화/완료에만 개입
        interrupts = 1

        print(f"  Complete: {total_time:.3f}s")
        print(f"  CPU Usage: {cpu_usage}%")
        print(f"  Interrupts: {interrupts}")

        return TransferResult("DMA", total_time, cpu_usage, interrupts)


def comparison():
    """세 방식 비교"""

    print("=" * 60)
    print("I/O 제어 방식 비교")
    print("=" * 60)

    controller = IOController()

    # 1000 바이트 전송
    data_size = 1000

    results = []

    # Programmed I/O
    results.append(controller.programmed_io(data_size))

    # Interrupt I/O
    results.append(controller.interrupt_io(data_size))

    # DMA
    results.append(controller.dma_transfer(data_size))

    # 비교표
    print("\n" + "=" * 60)
    print("비교 요약")
    print("=" * 60)

    print(f"{'방식':<15} {'시간(s)':<10} {'CPU%':<8} {'인터럽트':<10}")
    print("-" * 60)

    for r in results:
        print(f"{r.method:<15} {r.time:<10.3f} {r.cpu_usage:<8.1f} {r.interrupts:<10}")

    # 상세 분석
    print("\n" + "=" * 60)
    print("상세 분석")
    print("=" * 60)

    print("\n[CPU 효율]")
    for r in results:
        efficiency = 100 - r.cpu_usage
        print(f"  {r.method}: {efficiency:.1f}% 다른 작업 가능")

    print("\n[인터럽트 오버헤드]")
    for r in results:
        if r.interrupts > 0:
            overhead = r.interrupts * 0.0001
            print(f"  {r.method}: {overhead:.3f}s ({r.interrupts}개)")

    print("\n[추천 사용처]")
    print("  Polling:")
    print("    - 단순한 시스템")
    print("    - 적은 데이터")
    print("    - 실시간 제어")

    print("\n  Interrupt:")
    print("    - 일반적인 시스템")
    print("    - 문자 장치")
    print("    - 비주기적 이벤트")

    print("\n  DMA:")
    print("    - 대량 데이터")
    print("    - 고속 장치")
    print("    - 성능 중시")


def device_recommendations():
    """장치별 추천"""

    print("\n" + "=" * 60)
    print("장치별 I/O 방식 추천")
    print("=" * 60)

    devices = [
        ("키보드", "Interrupt", "비주기적, 소량 데이터"),
        ("마우스", "Interrupt", "이벤트 기반"),
        ("프린터", "DMA", "대량 데이터"),
        ("디스크", "DMA", "블록 전송"),
        ("네트워크", "DMA + Interrupt", "고속 패킷"),
        ("사운드", "DMA", "스트리밍"),
        ("디지털 I/O", "Polling", "단순 제어"),
        ("RTC", "Interrupt", "알림"),
    ]

    print(f"{'장치':<15} {'방식':<20} {'이유'}")
    print("-" * 60)

    for device, method, reason in devices:
        print(f"{device:<15} {method:<20} {reason}")


def hybrid_example():
    """하이브리드 방식 예시"""

    print("\n" + "=" * 60)
    print("하이브리드 I/O 시스템")
    print("=" * 60)

    print("\n시스템 구성:")
    print("  - Sensor (ADC): Polling, 100µs Loop")
    print("  - Communication: Interrupt")
    print("  - Data Logging: DMA")
    print("  - Alarm: Interrupt (Highest Priority)")

    print("\nMain Loop:")
    print("  while (1) {")
    print("    // Polling for Sensor")
    print("    if (check_sensor()) {")
    print("      process_sensor();")
    print("    }")
    print("")
    print("    // 다른 작업 가능")
    print("    enable_interrupts();")
    print("    idle();")
    print("  }")

    print("\n장점:")
    print("  - Critical Task는 Polling (예측 가능)")
    print("  - Event는 Interrupt (효율적)")
    print("  - Bulk는 DMA (CPU 해방)")


if __name__ == "__main__":
    comparison()
    device_recommendations()
    hybrid_example()
