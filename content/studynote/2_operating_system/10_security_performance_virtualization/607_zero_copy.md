+++
title = "607. 제로 카피 (Zero-copy) 기술 - sendfile, splice"
date = "2026-03-14"
weight = 607
+++

# 607. 제로 카피 (Zero-copy) 기술 - sendfile, splice

## 📋 핵심 인사이트 (Executive Summary)
> 1. **본질 (Essence)**: 제로 카피(Zero-copy)는 `CPU (Central Processing Unit)`의 개입 없이, 또는 최소한의 개입으로 네트워크 카드나 디스크 컨트롤러가 메모리 간 데이터를 직접 전송하게 하여 시스템 오버헤드를 제거하는 I/O 패스급 최적화 기술입니다.
> 2. **가치 (Value)**: `User Space`와 `Kernel Space` 간의 불필요한 `Context Switch` 및 메모리 복사 횟수를 4회→2회(또는 1회)로 획기적으로 줄여, 웹 서버 및 메시징 시스템의 처리량(`TPS: Transactions Per Second`)을 2~3배 이상 향상시키고 지연 시간(`Latency`)을 최소화합니다.
> 3. **융합 (Convergence)**: 고성능 웹 서버(Nginx, Apache), 메시지 큐(Kafka), 대용량 스토리지 시스템에서 `DMA (Direct Memory Access)` 및 `Scatter-Gather I/O` 기술과 결합하여 하드웨어 한계에 근접한 성능을 냅니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**제로 카피(Zero-copy)**는 운영 체제(Operating System)의 I/O 처리 과정에서, 데이터를 저장하기 위한 메모리 영역 간의 복사 작업을 배제하여 CPU 연산 자원을 절약하고 시스템 처리량을 증대시키는 기술입니다. 전통적인 I/O 모델에서는 데이터가 디스크에서 네트워크 카드로 전송될 때까지 여러 번의 메모리 복사와 모드 전환이 발생하지만, 제로 카피는 이를 우회하여 데이터가 '관통'하도록 설계되었습니다.

### 💡 핵심 비유
마치 택배 물건이 집->허브센터->집으로 이동할 때마다 박스를 열고 내용물을 다른 박스에 옮겨 담는 대신(기존 I/O), 출발지 집에서 목적지 집으로 박스째로 직송 배송(제로 카피)하는 시스템과 같습니다.

### 2. 등장 배경 및 필요성
① **전통적 I/O의 한계 (Double Buffering)**:
기존의 `read()`/`write()` 시스템 콜 기반 I/O는 데이터의 무결성을 보장하기 위해 `User Buffer`와 `Kernel Buffer`를 분리하여 사용합니다.
- **CPU 오버헤드**: 1GB 파일 전송 시 CPU는 데이터를 4번 복사(디스크→커널, 커널→유저, 유저→커널, 커널→NIC)해야 하므로, 전체 CPU 시간의 상당 부분을 '데이터 이동'이라는 단순 노동에 소모합니다.
- **캐시 폴징(Cache Pollution)**: 유저 버퍼로 복사된 데이터는 CPU 캐시를 가득 채우지만, 애플리케이션이 실제로 참조하지 않고 다시 커널로 보내버리므로 캐시 효율이 떨어집니다.

② **고속 네트워킹 등장**:
기가비트(1Gbps) 및 10Gbps 이상의 네트워크 환경에서는 CPU의 복사 연산 속도가 네트워크 전송 속도를 따라가지 못하는 '병목 현상'이 발생합니다. 이를 해결하기 위해 하드웨어가 직접 메모리를 제어하는 방식이 요구되었습니다.

③ **현재 비즈니스 요구**:
대용량 트래픽을 처리하는 초대형 웹 서비스와 실시간 데이터 파이프라인에서는 CPU 코어를 단순 복사 작업而非 비즈니스 로직 처리에 집중시켜야 하는 요구가 강력합니다.

### 📢 섹션 요약 비유
전통적인 I/O는 **"중간 창고 관리인이 물건을 받아서 검토하고 다시 포장해서 보내는 느린 과정"**이라면, 제로 카피는 **"창고 관리인 없이 출발지 컨테이너를 목적지 화물차에 직접 싣는 고속 물류 센터"**와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석 (Component Analysis)

| 요소명 | 역할 | 내부 동작 메커니즘 | 연관 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **DMA (Direct Memory Access)** | CPU 대신 데이터 전송 담당 | CPU의 개입 없이 I/O 장치(NIC, Disk)와 메모리 간 직접 데이터 블록 전송. `Bus Mastering` 방식으로 시스템 버스 제어 | Hardware Signal | 스마트한 크레인 운영사 |
| **Page Cache** | 디스크 데이터 캐싱 | 파일 시스템의 성능을 위해 디스크 데이터를 메모리에 매핑해 두는 커널 영역 | `VFS (Virtual File System)` | 창고의 임시 보관 구역 |
| **Socket Buffer** | 네트워크 전송 대기열 | NIC로 전송될 데이터 패킷을 저장하는 커널 스택 내의 메모리 영역 | TCP/IP Stack | 트럭 적재장 (Loading Dock) |
| **User Buffer** | 애플리케이션 데이터 영역 | 사용자 프로세스가 데이터를 읽고 쓰는 메모리 공간. 제로 카피 시 우회됨 | `malloc()`, `free()` | 고객의 거실 (공간) |
| **File Descriptor (FD)** | 자원 식별자 | 열린 파일이나 소켓을 가리키는 커널 내부의 포인터 | `fd` (integer) | 운송장 번호 |

### 2. 작동 메커니즘 비교 (Traditional vs Zero-copy)

#### A. 전통적 I/O (Copy-based)
전통적인 방식은 `Disk -> Kernel Buffer -> User Buffer -> Kernel Socket Buffer -> NIC`의 경로를 따릅니다. 총 4번의 복사와 4번의 컨텍스트 스위치가 필요합니다.

```text
+---------------------+       (1) DMA Copy (Read)        +---------------------+
|      DISK (HDD)     |------------------------------->|  Kernel Read Buffer |
+---------------------+                                   +----------+----------+
                                                                   |
                                                                   | (2) CPU Copy
                                                                   v
+---------------------+       (3) CPU Copy         +----------+----------+
| Kernel Socket Buffer|<--------------------------|      User Buffer    |
+----------+----------+                            +---------------------+
           |
           | (4) DMA Copy (Write)
           v
+---------------------+
|   NIC (Network)     |
+---------------------+

[Context Switch Flow]
User App --(read)--> Kernel --(copy)--> User App --(write)--> Kernel --(send)--> NIC
(System Call)      (Mode Switch)       (Data Processing)     (System Call)
```
*해설*:
- **비효율**: (2)와 (3) 과정에서 데이터는 단지 '통과'之目的일 뿐인데 유저 공간을 거치며 CPU 사이클을 낭비합니다.
- **오버헤드**: 유저 공간에서 데이터를 가공(암호화 등)하지 않고 단순히 전송만 한다면 이 경로는 순수 낭비입니다.

#### B. 제로 카피 I/O (sendfile)
`sendfile()` 시스템 콜은 데이터를 유저 버퍼로 복사하지 않고, 커널 내의 파일 버퍼에서 소켓 버퍼로 직접 전송합니다. CPU 복사 횟수를 2회로 줄입니다.

```text
+---------------------+       (1) DMA Copy (Read)        +---------------------+
|      DISK (HDD)     |------------------------------->|  Kernel Page Cache  |
+---------------------+                                   +----------+----------+
                                                                   |
                                                                   | (2) CPU Copy
                                                                   | (Still requires buffer move in kernel)
                                                                   v
+---------------------+       (3) DMA Copy (Write)      +----------+----------+
|   NIC (Network)     |<---------------------------|   Kernel Socket Buffer |
+---------------------+                                  +---------------------+

[Context Switch Flow]
User App --(sendfile)--> Kernel --(DMA Read)--> Kernel --(DMA Write)--> NIC
(One System Call)      (Kernel manages all)
```
*해설*:
- **개선**: User Buffer를 우회함으로써 CPU 복사 횟수가 줄어들고 컨텍스트 스위치가 2회(진입/복귀)로 감소합니다.
- **한계**: 여전히 커널 내부의 Read Buffer에서 Socket Buffer로의 이동(CPU 연산 또는 `memcpy`)이 필요한 경우가 많습니다.

#### C. 진정한 제로 카피 (Zero-copy with DMA Scatter-Gather)
하드웨어(`NIC`)가 `SG-DMA`를 지원하고, `mmap` 등을 통해 메모리 페이지가 재배치될 경우, 커널 소켓 버퍼로의 복사 조차 생략됩니다. 디스크립터(주소 정보)만 전달됩니다.

```text
+---------------------+       (1) DMA Load             +---------------------+
|      DISK (HDD)     |------------------------------->|  Kernel Page Cache  |
+---------------------+                                  +----------+----------+
                                                                |
                                                                | (2) Pass Descriptor Only)
                                                                | (No Data Copy!)
                                                                v
+---------------------+       (3) DMA Gather (Direct)   +---------------------+
|   NIC (Network)     |<---------------------------|   Socket Descriptor   |
+---------------------+      (NIC reads directly from Page Cache)   +
```
*해설*:
- **궁극적 최적화**: CPU는 데이터를 전혀 건드리지 않습니다. 단지 "이 메모리 주소(Page Cache)의 데이터를 저 주소(NIC)로 보내라"는 명령어(Descriptor)만 전달합니다.
- **조건**: NIC가 `Scatter-Gather` 기능을 지원해야 합니다.

### 3. 핵심 알고리즘 및 원리
**Scatter-Gather I/O**: 데이터가 메모리에 연속적으로 위치하지 않더라도, 여러 개의 불연속적인 메모리 청크(Chunk)에 대한 주소 리스트를 묶어서(Buffer Descriptor) 한 번의 DMA 동작으로 I/O 장치에 전송하는 기술입니다. 이를 통해 커널 소켓 버퍼(재조정 영역)를 완전히 생략할 수 있습니다.

```c
// [Pseudo-code: sendfile with Scatter-Gather Concept]
struct iovec {
    void  *iov_base; /* Starting address */
    size_t iov_len;  /* Number of bytes to transfer */
};

// Kernel Internal Logic (Simplified)
int zero_copy_send(int out_fd, int in_fd, size_t count) {
    // 1. DMA brings data from Disk to Kernel Page Cache (Step 1)
    load_to_page_cache(in_fd);

    // 2. Instead of memcpy, setup DMA descriptor
    // Pointing directly to the Page Cache memory address
    struct dma_descriptor *desc = get_dma_buffer(out_fd);
    desc->src_addr = &kernel_page_cache; 
    desc->length = count;

    // 3. Trigger DMA transfer to NIC (Step 2)
    // CPU is free during this transfer!
    start_hardware_dma(desc);

    return count;
}
```

### 📢 섹션 요약 비유
이는 **"물건을 트럭에 싣기 위해 창고에서 임시 공장(User Buffer)으로 옮겼다가 다시 트럭으로 옮기는 비효율을 없애고, 창고(Kernel Cache)에 정박해 있는 컨테이너를 로봇 팔(DMA)이 떼어서 바로 배에 싣는 직항 운송 시스템"**과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술별 상세 비교 (sendfile vs splice vs mmap)

| 비교 항목 | `sendfile()` (Linux 2.2+) | `splice()` (Linux 2.6.17+) | `mmap()` (Memory Map) |
|:---|:---|:---|:---|
| **기본 원리** | 파일 디스크립터 간 데이터 이동을 커널 내부에서 처리 | 두 FD를 파이프(Pipe) 버퍼로 연결하여 데이터를 '이동'시킴 | 파일을 가상 메모리(Virtual Memory)에 매핑 |
| **데이터 복사** | 2회 (Disk→Kernel, Kernel→NIC) <br>※ SG-DMA 지원 시 1회 가능 | 1회 (파이프 버퍼를 통한 참조 이동) | 2회 (Disk→Page Cache, User Access → Page Cache) |
| **User Space 접근** | 불가능 (데이터를 볼 수 없음) | 불가능 (단순 전달용) | **가능** (유저가 포인터로 직접 접근 가능) |
| **주요 용도** | 정적 파일 서비스 (웹 서버 이미지 전송 등) | 네트워크 프록시, 데이터 파이프라인 (Tee, Forwarding) | 파일 I/O 및 공유 메모리, 데이터 가공이 필요한 경우 |
| **CPU 오버헤드** | 매우 낮음 (Context Switch 2회) | 매우 낮음 (커널 내부 파이프 메커니즘 활용) | 중간 (Page Fault 발생 가능) |

### 2. 타 기술 영역과의 융합 시너지

#### A. 네트워크 (Network)
- **연관성**: 고성능 웹 서버(Nginx)의 `sendfile on;` 설정은 제로 카피의 대표적인 활용 사례입니다.
- **효과**: 10Gbps 네트워크 환경에서 `sendfile` 미사용 시 CPU 100% 포화 상태로 인해 처리량이 3Gbps로 제한되던 현상이, 제로 카피 적용 시 네트워크 대역폭 한계(9.5Gbps)까지 충분히 활용 가능해집니다.

#### B. 운영체제 (OS Internals)
- **연관성**: `COW (Copy-On-Write)` 기법과 논리적 맥락을 공유합니다. 실제 데이터 복사가 필요한 시점(쓰기 작업)까지 복사를 지연시켜 자원을 절약하는 철학입니다.
- **Side Effect**: `fork()` 시스템 콜 시 페이지 테이블만 복사하고 물리 메모리는 공유하는 기술과 유사한 '레퍼런스 카운팅' 최적화 사상입니다.

#### C. 데이터베이스 (DB)
- **연관성**: Kafka와 같은 로그 기반 메시지 큐는 디스크의 로그 세그먼트를 네트워크로 전송할 때 제로 카피를 사용합니다. 프로듀서가 쓴 데이터를 컨슈머에게 전달할 때 추가적인 복사 비용 없이 전달하여 처리량을 극대화합니다.

### 📢 섹션 요약 비유
`sendfile`은 **"특급 직통열차(기차가 역에 서서 짐을 옮기지 않음)"**라면, `splice`는 **"물류 터미널에서 컨테이너를 크레인으로 들어 올려 다른 트럭에 바로 싣는 방식"**이고, `mmap`은 **"내 방에 창고를 열어두어서 필요할 때마다 들어가서 물건을 확인