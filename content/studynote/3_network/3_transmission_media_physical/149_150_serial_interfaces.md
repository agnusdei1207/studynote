+++
title = "149-150. 직렬(Serial) 통신 인터페이스 규격"
date = "2026-03-14"
[extra]
category = "Physical Layer"
id = 149
+++

# 149-150. 직렬(Serial) 통신 인터페이스 규격

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 직렬 통신은 데이터를 1비트씩 순차적으로 전송하는 방식으로, 물리 계층(Physical Layer)의 가장 기초가 되는 전송 기술입니다.
> 2. **가치**: 낮은 배선 비용과 장거리 전송 가능성(특히 Differential 방식) 덕분에 산업 현장의 FA(Factory Automation)와 사물인터넷(IoT)의 핵심 인프라로 자리 잡았습니다.
> 3. **융합**: 하드웨어적으로는 UART(Universal Asynchronous Receiver/Transmitter) 제어 로직과 결합하고, 상위 프로토콜로는 Modbus 등 프로토콜을 탑재하여 IT과 OT(Operational Technology)의 경계를 허무는 융합 기술입니다.

+++

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학
**직렬(Serial) 통신**은 정보를 나타내는 데이터 비트(Data Bit)들을 하나의 전선 채널을 통해 시간적으로 분리하여 순차적으로 보내는 방식입니다. 병렬(Parallel) 통신이 여러 개의 선을 사용하여 동시에 데이터를 보내는 것과 대비됩니다. 초기에는 전자 회로의 복잡도를 낮추고 비용을 절감하기 위해 사용되었으나, 클럭 주파수(Clock Frequency)의 물리적 한계와 신호 왜곡(Skew) 문제로 인해 현대의 고속 통신은 다시 직렬 방식으로 수렴하고 있습니다.

### 💡 비유
마치 좁은 다리 위로 사람들이 일렬로 건너가는 것과 같습니다. 한 번에 한 사람씩 건너야 하므로 대기 시간이 발생하지만, 다리를 넓히는 대신(병렬) 사람이 걷는 속도를 비약적으로 높여(직렬 고속화) 전체 통행량을 늘리는 현대적인 교통 체계와 같습니다.

### 등장 배경
1.  **기존 한계**: 병렬 통신은 거리가 멀어질수록 각 선로의 신호 도착 시간이 달라지는 '스큐(Skew)' 현상이 발생하여 고속화에 한계가 있었습니다.
2.  **혁신적 패러다임**: **UART (Universal Asynchronous Receiver/Transmitter)** 칩의 발전으로 병렬 데이터를 직렬로 변환하여 적은 수의 선으로 멀리 데이터를 보낼 수 있는 방식이 개발되었습니다.
3.  **현재의 비즈니스 요구**: 산업 현장에서는 긴 케이블링 비용 절감과 노이즈에 강한 특성이 필요하여, 아날로그 방식의 RS-232C에서 디지털 차동 신호 방식의 RS-485와 USB로 진화했습니다.

### 📢 섹션 요약 비유
병렬 통신이 '8차선 도로를 통해 트럭 8대가 동시에 운반하는 것'이라면, 직렬 통신은 '고속열차 하나에 모든 짐을 싣고 전용 선로를 달리는 것'과 같습니다. 단순히 차선을 늘리는 것엔 한계가 있어, 속도(대역폭)를 극한으로 끌어올리는 방향으로 진화한 것입니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/규격 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **TX (Transmitter)** | 데이터 송신 | 병렬 데이터를 직렬 비트 스트림으로 변환(Parallel-to-Serial)하여 회선에 내보냄. Start/Stop 비트 추가. | UART Logic | 편지지에 편지를 써서 우체통에 넣는 사람 |
| **RX (Receiver)** | 데이터 수신 | 들어오는 비트 스트림을 샘플링하여 병렬 데이터로 재조립(Serial-to-Parallel). 클럭 복원. | UART Logic | 우편함에서 편지를 꺼내 읽는 사람 |
| **Baud Rate Generator** | 속도 동기화 | 송수신 쌍방이 동일한 전송 속도(초당 비트 수)를 유지하도록 클럭(Clock)을 생성함. | 9600, 115200 bps 등 | 두 사람이 약속된 속도로 박자를 맞추는 메트로놈 |
| **Line Driver** | 신호 증폭 및 구동 | TTL/CMOS 레벨(0~5V)의 디지털 신호를 RS-232(±15V)나 차동 신호(RS-485)로 변환하여 전송. | Voltage Level | 소리를 크게 내는 확성기 (Megaphone) |
| **Line Receiver** | 신호 수신 및 복원 | 장거리 전송된 약해진 신호를 입력받아 다시 TTL/CMOS 레벨의 디지털 신호로 변환. | Threshold Check | 멀리서 듣는 소리를 귀로 파악하는 수신기 |

### ASCII 구조 다이어그램: UART 프레임 구조 및 비트 전송

아래는 UART 기반의 비동기식 직렬 통신에서 데이터가 어떻게 패킹(Packing)되어 전송되는지를 나타낸 것입니다.

```ascii
      [Time Flow ------------------------------------------------------>]

      Idle    Start    LSB b0    b1    b2    b3    b4    b5    b6    MSB     Parity      Stop    Idle
       |       |        |        |     |     |     |     |     |     |       |         |       |
       |   ___ |_______ |__|____|__|___|____|____|____|____|__|_____|_________|_______ |   ___ |
Logic  |       |         |        |  1  |  0  |  1  |  0  |  1  |  1  |   (Even/Odd)    |       |
 1     |       |         |         0x55 데이터 예시                    |   (선택적 옵션)   |       |
       |       |         |                                            |                  |       |
Logic  |_______|         |____________________________________________|__________________|       |
 0     |       |         |                                            |                  |       |
       
       <--- 1 bit ---> <------------ 8 bits Data Length -------------> <-- 1 bit -->
       
      [Physical Wire Voltage Representation (RS-232C Standard Example)]
      +12V ~ +15V (Logic 0, Mark)      -12V ~ -15V (Logic 1, Space)
       ^                               ^
       |--- SPACE (Start Bit)          |--- MARK (Stop Bit)
```

#### 다이어그램 해설
1.  **Idle (유휴 상태)**: 데이터가 전송되지 않을 때는 회선이 '1'(Mark, High Voltage) 상태를 유지합니다.
2.  **Start Bit (시작 비트)**: 전송 시작을 알리는 **0**(Space, Low Voltage) 비트가 1비트 duration 동안 발생합니다. 수신부(RX)는 이 하강 에지( Falling Edge)를 감지하여 타이머를 시작합니다.
3.  **Data Bits (데이터 비트)**: LSB(Least Significant Bit)부터 MSB(Most Significant Bit) 순서로 전송됩니다. 위 예시는 8비트 데이터이며, `0x55`(`01010101`)가 전송되는 모습입니다.
4.  **Parity Bit (패리티 비트)**: 데이터 무결성을 검증하기 위한 비트로, 1의 개수가 짝수인지(Even) 홀수인지(Odd) 설정하여 추가합니다. 선택 사항입니다.
5.  **Stop Bit (정지 비트)**: 전송 종료를 알리는 '1' 상태로, 일반적으로 1비트 또는 1.5비트, 2비트의 길이를 가집니다. 다음 프레임과의 버퍼를 제공합니다.

### 심층 동작 원리: Differential Signaling (차동 신호)
RS-485와 같은 현대적 산업 통신은 **A(Non-Inverting)** 선과 **B(Inverting)** 선 두 가닥을 사용합니다.
*   **Logic 1**: A가 B보다 전압이 높음 ($V_A > V_B$)
*   **Logic 0**: B가 A보다 전압이 높음 ($V_B > V_A$)
수신부는 두 선의 **전압 차(Differential Voltage)**만을 감지하므로, 외부에서 유입되는 노이즈(Common-mode Noise)가 두 선에 동일하게 걸려도 상쇄됩니다.

### 핵심 코드: UART 설정 (Linux C)
```c
#include <termios.h>
#include <fcntl.h>

// 직렬 포트 설정 구조체 (struct termios)
void configure_serial(int fd) {
    struct termios options;

    // 1. 현재 설정 가져오기
    tcgetattr(fd, &options);

    // 2. 전송 속도(Baud Rate) 설정 - 입력/출력 모두 115200으로
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);

    // 3. 제어 모드 플래그 (CFLAG)
    // CRTSCTS: 하드웨어 흐름 제제 (RTS/CTS)
    // CS8: 8비트 데이터
    // CLOCAL: 로컬 연결 (모뎀 제어 라인 무시)
    // CREAD: 수신 가능 (Receiver Enable)
    options.c_cflag |= (CRTSCTS | CS8 | CLOCAL | CREAD);

    // 4. 로컬 모드 플래그 (LFLAG) - 원시(Raw) 모드 설정
    // ICANON: 정규 모드 비활성화 (라인 단위 처리 안 함)
    // ECHO: 에코 비활성화
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    // 5. 적용 및 플러시
    tcsetattr(fd, TCSANOW, &options);
    tcflush(fd, TCIOFLUSH); // 버퍼 비우기
}
```

### 📢 섹션 요약 비유
직렬 통신의 UART 프레임 구조는 마치 기차역에서 **사람(데이터)이 열차(프레임)에 순서대로 타서 이동하는 것**과 같습니다. 기차가 출발하면(Start Bit), 사람들이 한 명씩 차례로 줄을 서서 탑승하고(Data Bits), 마지막에 안내원이 승차 인원을 확인하고(Parity Bit), 기차가 도착역에 멈추면(Stop Bit) 내리는 과정을 거칩니다. 차동 신호(RS-485)는 두 사람이 각각 다른 귀로 소리를 듣고, 그 차이를 통해 상대방의 말을 구분하는 것과 같아 시끄러운 곳(노이즈 환경)에서도 대화가 가능합니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교표: RS-232C vs RS-422 vs RS-485

| 비교 항목 | RS-232C | RS-422 | RS-485 |
|:---|:---|:---|:---|
| **신호 방식** | **Single-Ended** (단일 종단)<br>접지(GND) 대비 전압 절대값 사용 | **Differential** (차동)<br>A,B 선 간 전압 차 사용 | **Differential** (차동) |
| **동작 모드** | 전이중(Full-Duplex)<br>송/수신 선 분리 | 전이중(Full-Duplex)<br>4선식 (2TX, 2RX) | 반이중(Half-Duplex)<br>2선식 (1 Pair, TX/RX 시분할) |
| **전압 레벨** | ±3V ~ ±15V | ±5V 차동 | -7V ~ +12V 차동 |
| **최대 거리** | ~15m (낮은 속도 시) | ~1.2km (낮은 속도 시) | ~1.2km (낮은 속도 시) |
| **최대 속도** | 20Kbps @ 15m | 10Mbps @ 12m | 10Mbps @ 12m |
| **연결 방식** | Point-to-Point (1:1) | Point-to-Multi-Point (1:N Driver, 10 Rx) | Multi-Drop (N:N Bus)<br>최대 32 Unit (확장 시 256) |
| **주요 용도** | 구형 PC 마우스, 모뎀, CNC 장비 제어 | 산업용 센서 네트워크, 항공기 | 빌딩 자동화(BAS), PLC 통신, Modbus |

### ASCII 다이어그램: 토폴로지 비교 (Topology)

```ascii
      [1) RS-232C : Point-to-Point]
      
      Computer (DTE) -------------------- Modem (DCE)
       (TX) -----> (RX)    (RX) <----- (TX)
       
      (오직 1대1 연결만 가능, 다른 기기는 끼어들 수 없음)

      --------------------------------------------------

      [2) RS-422 : Unidirectional Multi-Drop (1 Driver : N Receivers)]
      
      Driver                              Receiver 1
      (TX) --------(A+)---------------> (RX)
                  | (B-)
                  |
                  +-------------------> Receiver 2
                  |                     (RX)
                  |
                  +-------------------> Receiver 3
                                        (RX)
      
      (마스터가 여러 슬레이브에게 방송하는 '방송국' 형태)

      --------------------------------------------------

      [3) RS-485 : Multi-Drop Bus (Half-Duplex)]
      
       Termination            Node 1              Node 2            Termination
      Resistor (120Ω)      (Master/Slave)       (Slave)          Resistor (120Ω)
           |                  [  D ]             [  D ]                |
       ----+------------------+  +---------------+  +----------------+----
          |                  [A | ]             [A | ]                |
          |                  [  E ]             [  E ]                |
      Bus |  (Bias Resistor) [  V ]             [  V ]                |
       Line                   [  I ]             [  I ]               
          |                  [  C ]             [  C ]                |
          |                  [  E ]             [  E ]                |
       ----+------------------+  +---------------+  +----------------+----
           |                  [  R ]             [  R ]                |
           +----------------------------------------------------------+
           |  <---------- 양방향 데이터 버스 (A, B pair) ------------>  |
           
      (데이터 버스 하나에 여러 장치가 순서대로 말을 걸 수 있는 '회의' 형태)
```

### 과목 융합 관점
1.  **운영체제(OS)와의 연계**: 리눅스나 윈도우 환경에서 직렬 포트는 `/dev/ttyS*`나 `COMx`와 같은 **Character Device (문자 장치)** 파일로 추상화되어 관리됩니다. 드라이버는 인터럽트(Interrupt) 방식을 통해 데이터를 버퍼링하며, 이는 OS의 커널 레벨 I/O 관리와 밀접하게 연결됩니다.
2.  **데이터베이스(DB) 및 시계열 데이터**: 산업 현장