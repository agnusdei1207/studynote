+++
title = "프로그램 가능 I/O (Programmed I/O)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 프로그램 가능 I/O (Programmed I/O)

## 핵심 인사이트 (3줄 요약)
1. 프로그램 가능 I/O(Programmed I/O, Polling)는 CPU가 직접 I/O 장치의 상태를 확인(Status Check)하고 데이터를 전송하는 방식으로, 인터럽트나 DMA 없이 CPU가 모든 것을 제어한다
2. CPU가 주기적으로 장치의 Status 레지스터를 확인(Polling)하여 Ready/Busy 상태를 검사하고, 준비되면 Data 레지스터를 읽거나 쓴다
3. 기술사시험에서는 Polling 루프, Status Check 순서, CPU 효율, 하드웨어 제어 순서가 핵심이다

## Ⅰ. 개요 (500자 이상)

프로그램 가능 I/O(Programmed I/O)는 **CPU가 직접 I/O 장치를 제어하고 데이터를 전송하는 가장 기본적인 I/O 방식**이다. CPU가 프로그램된 순서에 따라 주기적으로 장치의 상태를 확인(Polling)하고, 장치가 준비되면 데이터를 전송한다.

```
프로그램 가능 I/O 기본 개념:
방식: CPU가 직접 제어
동작: Status 확인 → Data 전송
Loop: Polling Loop

과정:
1. Status 레지스터 확인
2. Ready 비트 검사
3. Ready면 Data 전송
4. 루프 반복

특징:
- CPU가 모든 것을 제어
- 인터럽트 불필요
- 단순한 하드웨어
- CPU 시간 소모
```

**프로그램 가능 I/O의 핵심 특징:**

1. **CPU 주도**: CPU가 모든 I/O를 제어
2. **Polling**: 주기적 상태 확인
3. **단순성**: 하드웨어 구조 단순
4. **비효율**: CPU 시간 낭비

```
다른 I/O 방식과 비교:
Programmed I/O:
- CPU가 주기적 확인
- CPU 시간 소모
- 단순함

Interrupt I/O:
- 장치가 알림
- CPU 효율적
- 복잡함

DMA:
- DMA가 전송
- CPU 해방
- 가장 복잡
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Polling 루프

```
Polling Loop 구조:

Pseudo Code:
while (transferred < count) {
    // Status 확인
    status = IN(Status_Port)
    if (status & READY) {
        // Data 전송
        data = IN(Data_Port)
        memory[buffer++] = data
        transferred++
    }
}

Assembly (x86):
mov cx, count
mov si, buffer

poll_loop:
    in al, status_port
    test al, ready_bit
    jz poll_loop      ; Not Ready, 다시 확인

    in al, data_port   ; Ready, Data 읽기
    mov [si], al
    inc si
    loop poll_loop

특징:
- Busy Waiting
- CPU가 계속 실행
- 인터럽트 불필요
```

### Status Register Check

```
Status Register 비트:

일반적인 Status Register 구성:
Bit 7: Busy (1=Busy, 0=Ready)
Bit 6: Ready (1=Ready, 0=Busy)
Bit 5: Error (1=Error)
Bit 4: Interrupt (1=Pending)
...

Polling 과정:
1. Status Register 읽기
2. Ready/Busy 비트 검사
3. Ready면 Data 전송
4. Busy면 다시 확인

Code:
check_status:
    in al, status_port
    test al, 80h      ; Bit 7 (Busy)
    jnz check_status  ; Busy면 다시 확인

    ; Ready, Data 전송
    in al, data_port
    ...
```

### Data Transfer Sequence

```
데이터 전송 순서:

Read Sequence (Input Device):
1. CPU: Status Register 확인
   - if Busy: 대기
   - if Ready: 진행

2. CPU: Data Register 읽기
   - IN AL, Data_Port

3. Device: Busy 상태로 전환
   - Status.Busy = 1
   - Status.Ready = 0

4. Device: 다음 데이터 준비
   - Data Reg → Data Buffer
   - Status.Busy = 0
   - Status.Ready = 1

Write Sequence (Output Device):
1. CPU: Status Register 확인
   - if Busy: 대기
   - if Ready: 진행

2. CPU: Data Register 쓰기
   - OUT Data_Port, AL

3. Device: Data 수신 처리
   - Status.Busy = 1

4. Device: 출력 완료
   - Status.Busy = 0
   - Status.Ready = 1
```

### Polling Order

```

다중 장치 Polling:

장치:
- Device 0 (Keyboard)
- Device 1 (Printer)
- Device 2 (Disk)

Polling 순서:
while (true) {
    if (Device0.ready()) Device0.service()
    if (Device1.ready()) Device1.service()
    if (Device2.ready()) Device2.service()
}

특징:
- 순차적 확인
- 앞 장치가 우선
- Starvation 가능성

개선:
- 가중치 부여
- Priority 기반 순서
- Round Robin
```

### CPU Efficiency

```
CPU 효율 문제:

문제:
Device Ready Time = 1ms
Polling Interval = 10µs

CPU 사용:
- 1000번 Polling = 10ms
- 실제 전송 = 1회
- 99.9% 낭비

Efficiency:
Transfer Time / Total Time
= 1ms / 10ms = 10%

해결:
1. Polling Interval 증가
   - 응답 지연

2. Interrupt 사용
   - Event-driven

3. DMA 사용
   - CPU 해방
```

### Hardware Control

```
하드웨어 제어 신호:

Programmed I/O 타이밍:

T1: CPU Status Request
    CPU → /RD Status_Port

T2: Status Data
    Status_Port → Data Bus → CPU

T3: Status Check
    CPU가 Ready 확인

T4: Data Request
    CPU → /RD Data_Port (or /WR)

T5: Data Transfer
    Data_Port ↔ Data Bus ↔ CPU

T6: Complete

제어:
- /RD (Read Strobe)
- /WR (Write Strobe)
- ALE (Address Latch Enable)
- IORQ (I/O Request)
```

## Ⅲ. 융합 비교

### I/O 방식 비교

| 방식 | CPU 개입 | 인터럽트 | DMA | CPU 효율 | 복잡도 |
|------|---------|---------|-----|----------|--------|
| Programmed I/O | 모든 바이트 | 없음 | 없음 | 매우 낮음 | 낮음 |
| Interrupt I/O | 완료 시 | 있음 | 없음 | 중간 | 중간 |
| DMA | 초기화/완료 | 있음 | 있음 | 높음 | 높음 |

### Polling 전략

| 전략 | 응답 시간 | CPU 사용 | 공평성 | 응용 |
|------|----------|----------|--------|------|
| Continuous | 짧음 | 매우 높음 | 없음 | 단일 장치 |
| Periodic | 중간 | 중간 | 있음 | 다중 장치 |
| Priority-based | 가변 | 중간 | 없음 | 우선순위 |

### 장치 유형별 적합성

| 장치 | Polling 적합성 | 이유 |
|------|---------------|------|
| 키보드 | 부적합 |低速, 비주기적 |
| 마우스 | 부적합 |低速, 비주기적 |
| 디스크 | 부적합 |高速, 대량 |
| 프린터 | 적합 | 중속, 예측 가능 |
| 시스템 제어 | 매우 적합 | 빠른 응답 필요 |

## Ⅳ. 실무 적용 및 기술사과적 판단

### BIOS Polling

```
BIOS의 Polling 사용:

POST (Power-On Self Test):
- Memory Test
- Device Check
- 모두 Polling으로 구현

코드 예:
mov cx, 1024  ; 1KB Test
mov si, 0

test_loop:
    mov [si], al
    cmp [si], al
    jne memory_error
    inc si
    loop test_loop

특징:
- 부팅 시 단순한 코드
- 인터럽트 불필요
- 확실한 제어
```

### Embedded Polling

```
임베디드 시스템 Polling:

Super Loop:
while (1) {
    if (uart_ready()) uart_process();
    if (timer_expired()) timer_process();
    if (gpio_changed()) gpio_process();
}

장점:
- 예측 가능한 실행
- 디버깅 용이
- 실시간 보장 가능

단점:
- 응답 시간 지연
- CPU 낭비

개선:
- 주기적 태스크 분리
- State Machine
- Rate Monotonic Scheduling
```

### High-Speed Polling

```
고속 Polling:

방법:
1. Memory-mapped I/O
   - 빠른 액세스
   - Cache 가능

2. Polling Loop 최적화
   - Inline Assembly
   - Loop Unrolling

3. Status Bit Mask
   - Bit Test 명령어
   - Jump Prediction

예:
poll_loop:
    mov al, [status]
    test al, 01h
    jz poll_loop

    ; Fast Path
    mov al, [data]
    ...

성능:
- 수 MHz까지 가능
- 네트워크 패킷 처리
```

### Hybrid Approach

```

하이브리드 방식:

조건:
- 중요/긴급: Interrupt
- 일반: Polling

예:
while (1) {
    // Polling routine
    if (device1.ready()) device1.process();
    if (device2.ready()) device2.process();

    // 인터럽트 허용
    enable_interrupts();
    idle();
    disable_interrupts();
}

장점:
- 두 방식 장점 활용
- 유연한 설계
- 최적의 성능
```

## Ⅴ. 기대효과 및 결론

프로그램 가능 I/O는 가장 단순한 I/O 방식이다. 하드웨어는 단순하지만 CPU 효율이 낮다.

## 📌 관련 개념 맵

```
프로그램 가능 I/O
├── 동작
│   ├── Status Check (Polling)
│   ├── Data Transfer
│   └── Loop 반복
├── 특징
│   ├── CPU 주도
│   ├── 단순함
│   ├── 비효율
│   └── 예측 가능
├── 순서
│   ├── Status Read
│   ├── Ready 확인
│   ├── Data Read/Write
│   └── 완료
└── 응용
    ├── BIOS
    ├── 임베디드
    └── 시스템 제어
```

## 👶 어린이를 위한 3줄 비유 설명

1. 프로그램 가능 I/O는 학교에서 체온을 재는 것과 같아요. 선생님이 매번 "줄 서서 체온을 재"하고 계속 확인해요
2. CPU가 계속 "준비됐어?"라고 물어보는 거예요. 장치가 "아직 아니야" 하면 기다리고, "줘비됐어!" 하면 데이터를 받아요
3. 계속 물어보니까 CPU가 피곤해져요. 그래서 보통은 인터럽트(전화 오면 알려줘) 방식을 쓰지만, 간단한 경우에는 Polling이 더 쉬워요

```python
# 프로그램 가능 I/O 시뮬레이션

from typing import List
import time


classIODevice:
    """I/O 장치"""

    def __init__(self, name: str, ready_time: int):
        self.name = name
        self.ready_time = ready_time  # 준비 시간 (ms)
        self.data = 0
        self.status = 0x40  # Ready bit initially
        self.busy = False

    def write_data(self, data: int):
        """데이터 쓰기"""
        self.data = data
        self.status = 0x80  # Busy
        self.busy = True
        print(f"[{self.name}] Data 0x{data:02X} written (Busy)")

    def read_data(self) -> int:
        """데이터 읽기"""
        self.status = 0x80  # Busy
        self.busy = True
        data = self.data
        print(f"[{self.name}] Data 0x{data:02X} read (Busy)")
        return data

    def update(self):
        """상태 업데이트 (시뮬레이션)"""
        if self.busy:
            self.ready_time -= 1
            if self.ready_time <= 0:
                self.busy = False
                self.status = 0x40  # Ready
                print(f"[{self.name}] Ready!")

    def get_status(self) -> int:
        """상태 반환"""
        return self.status

    def is_ready(self) -> bool:
        """Ready 확인"""
        return (self.status & 0x40) != 0


class ProgrammedIO:
    """프로그램 가능 I/O 시뮬레이터"""

    def __init__(self):
        self.devices: List[IODevice] = []
        self.poll_count = 0
        self.data_transferred = 0

    def add_device(self, device: IODevice):
        """장치 추가"""
        self.devices.append(device)

    def poll_device(self, device: IODevice) -> bool:
        """단일 장치 Polling"""
        self.poll_count += 1

        # Status 확인
        status = device.get_status()

        if device.is_ready():
            # Data 전송
            data = device.read_data()
            self.data_transferred += 1
            return True

        return False

    def poll_all(self) -> int:
        """모든 장치 Polling"""
        transferred = 0

        for device in self.devices:
            if device.is_ready():
                device.read_data()
                self.data_transferred += 1
                transferred += 1

        self.poll_count += len(self.devices)
        return transferred

    def write_device(self, device: IODevice, data: int):
        """장치 쓰기"""
        # Poll until ready
        poll_count = 0
        while not device.is_ready():
            self.poll_count += 1
            poll_count += 1
            device.update()

        # Write
        device.write_data(data)
        self.data_transferred += 1

        print(f"  (Polled {poll_count} times)")


def demonstration():
    """프로그램 가능 I/O 데모"""
    print("=" * 60)
    print("프로그램 가능 I/O (Programmed I/O) 데모")
    print("=" * 60)

    pio = ProgrammedIO()

    # 장치 추가 (다른 준비 시간)
    keyboard = IODevice("Keyboard", ready_time=2)
    printer = IODevice("Printer", ready_time=5)
    disk = IODevice("Disk", ready_time=10)

    pio.add_device(keyboard)
    pio.add_device(printer)
    pio.add_device(disk)

    # Polling Loop 시뮬레이션
    print("\n[Polling Loop]")
    print("각 장치는 다른 준비 시간을 가짐")

    for cycle in range(20):
        print(f"\n--- Cycle {cycle + 1} ---")

        # 장치 상태 업데이트
        for device in pio.devices:
            device.update()

        # Polling
        transferred = pio.poll_all()

        if transferred == 0:
            print("  No devices ready")
        else:
            print(f"  {transferred} device(s) serviced")

    # 통계
    print("\n[통계]")
    print(f"Total Polls: {pio.poll_count}")
    print(f"Data Transferred: {pio.data_transferred}")
    efficiency = (pio.data_transferred / pio.poll_count * 100) if pio.poll_count > 0 else 0
    print(f"Efficiency: {efficiency:.1f}%")

    # 단일 장치 Polling
    print("\n[단일 장치 Polling]")
    pio2 = ProgrammedIO()
    device = IODevice("UART", ready_time=3)
    pio2.add_device(device)

    # 데이터 쓰기
    print("\nWrite 0xAA to UART:")
    pio2.write_device(device, 0xAA)

    # 완료 대기
    print("\nWaiting for completion:")
    for i in range(5):
        device.update()
        if device.is_ready():
            print(f"  Cycle {i+1}: Ready!")
            break
        else:
            print(f"  Cycle {i+1}: Busy...")

    # Polling 순서
    print("\n[Polling 순서]")
    print("여러 장치가 있을 때:")

    pio3 = ProgrammedIO()
    pio3.add_device(IODevice("Dev0", ready_time=1))
    pio3.add_device(IODevice("Dev1", ready_time=2))
    pio3.add_device(IODevice("Dev2", ready_time=1))

    # Service count
    service_count = {"Dev0": 0, "Dev1": 0, "Dev2": 0}

    for cycle in range(10):
        for device in pio3.devices:
            device.update()
            if device.is_ready():
                device.read_data()
                service_count[device.name] += 1

    print("\nService Count:")
    for name, count in service_count.items():
        print(f"  {name}: {count} times")

    # Polling vs Interrupt 비교
    print("\n[Polling vs Interrupt]")
    print("Polling:")
    print("  - CPU가 계속 확인")
    print("  - 1000번 Polling → 1회 전송")
    print("  - CPU 사용률: ~99%")

    print("\nInterrupt:")
    print("  - 장치가 알림")
    print("  - 1번 인터럽트 → 1회 전송")
    print("  - CPU 사용률: ~1%")

    print("\n결론:")
    print("  - 단순한 시스템: Polling")
    print("  - 복잡한 시스템: Interrupt")
    print("  - 실시간: 혼합 방식")

    # Embedded Super Loop
    print("\n[임베디드 Super Loop]")
    print("while(1) {")
    print("    if (uart_rx_ready()) uart_rx_process();")
    print("    if (timer_expired()) timer_process();")
    print("    if (gpio_changed()) gpio_process();")
    print("}")
    print("\n→ 간단하고 예측 가능")
    print("→ 하지만 응답 시간 지연")


if __name__ == "__main__":
    demonstration()
```
