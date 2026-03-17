+++
title = "589. IPsec 오프로드 가속기"
date = "2026-03-14"
weight = 589
+++

# # [IPsec 오프로드 가속기 (IPsec Offload Accelerator)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IPsec(Internet Protocol Security) 프로토콜의 고비용 암복호화 연산을 Host CPU(Central Processing Unit)에서 분리하여 전용 하드웨어(ASIC/SmartNIC)로 처리하는 시스템 아키텍처입니다.
> 2. **가치**: Line Rate(선속도) 처리를 통해 네트워크 대역폭을 100% 활용함과 동시에 CPU 연산 자원을 획기적으로 절약하여 에너지 효율과 처리량(Throughput)을 극대화합니다.
> 3. **융합**: SD-WAN(Software-Defined Wide Area Network) 및 5G 코어 네트워크, 클라우드 가상화 환경의 보안 성능 병목을 해결하는 필수 인프라 기술입니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
IPsec 오프로드 가속기는 OSI 7계층 중 네트워크 계층(Layer 3)과 전송 계층(Layer 4) 사이에서 동작하는 IPsec 보안 프로토콜의 처리 부하를 전담하는 하드웨어 모듈입니다. 일반적으로 IPsec 터널을 구성할 때 ESP(Encapsulating Security Payload)를 이용한 패킷의 암호화(Encryption), 복호화(Decryption), 무결성 검증(Integrity Check)을 위해 대칭키 알고리즘(AES-GCM 등)과 해시 알고리즘(SHA-256 등)을 사용합니다. 이러한 연산은 비트 단위의 복잡한 수학적 계산을 요구하므로, 범용 CPU가 이를 직접 처리(Software IPsec)할 경우 시스템 전체의 성능 저하를 초래합니다. 이를 해결하기 위해 NIC(Network Interface Card) 내부에 전용 코프로세서(Co-processor)를 탑재하거나 별도의 하드웨어 가속 카드를 장착하여 연산을 위임(Offload)하는 기술입니다.

**2. 등장 배경 및 필요성**
① **기존 한계**: 인터넷 트래픽의 폭발적 증가와 보안 요구사항의 강화로 인해 10Gbps, 100Gbps 이상의 고속 망에서 CPU 기반 소프트웨어 암호화는 단일 코어 성능 한계와 메모리 대역폭 병목으로 인해 처리 불가능해졌습니다.
② **혁신적 패러다임**: "Compute와 Security의 분리" 패러다임이 등장했습니다. 데이터 평면(Data Plane)의 무거운 연산은 하드웨어에 맡기고, 제어 평면(Control Plane)의 의사결정은 CPU가 담당하도록 아키텍처가 재편되었습니다.
③ **현재 비즈니스 요구**: 클라우드 데이터센터 간의 암호화된 트래픽(VPC Encryption), 5G 이동통신망의 백홀(Backhaul) 보안, 원격 근무 급증에 따른 VPN 게이트웨이의 성능 압박을 해소하기 위해 필수적인 요소가 되었습니다.

**3. 기술 용어 정리**
- **IPsec (Internet Protocol Security)**: IP 계층에서 보안을 제공하는 프로토콜 suite로, AH(Authentication Header)와 ESP(Encapsulating Security Payload)로 구성됩니다.
- **ESP (Encapsulating Security Payload)**: 데이터의 기밀성(암호화)과 무결성, 인증을 제공하는 가장 널리 쓰이는 IPsec 프로토콜입니다.
- **SA (Security Association)**: IPsec 통신을 위한 매개변수(알고리즘, 키, 수명 등)를 포함하는 논리적 연결입니다.
- **AES-GCM (Advanced Encryption Standard - Galois/Counter Mode)**: 암호화와 무결성 검증을 동시에 수행하는 고성능 인증 암호화 알고리즘입니다.

```text
[Software vs Hardware Processing Load]

      < Software IPsec (CPU Overload) >        < Hardware Offload (Efficient) >
      +-------------------------------+      +-------------------------------+
      |        Applications           |      |        Applications           |
      +-------------------------------+      +-------------------------------+
      |          OS Stack             |      |          OS Stack             |
      +-------------------------------+      +-------------------------------+
      |  IPsec Stack (Crypto Lib)     |      |      IPsec Control (SA Mgmt)  |
      |  [AES] [SHA] [RNG] [MODP]     |      |         (Lightweight)         |
      +-------------------------------+      +-------------------------------+
      |   CPU Cores (100% Usage)      |      |   CPU Cores (5~10% Usage)     |
      +-------------------------------+      +-------------------------------+
      |         Drivers               |      |         Drivers               |
      +-------------------------------+      +-------------------------------+
      |            NIC                |      |   NIC + Accelerator Engine    |
      +-------------------------------+      |   [AES-GCM Hardware Engine]   |
                                         |   [SHA Hardware Engine]       |
                                         +-------------------------------+
```
> **해설**: 소프트웨어 방식은 애플리케이션과 암호화 연산이 모두 CPU에서 경쟁하며 자원을 소모하지만, 오프로드 방식은 암호화 엔진이 NIC 내부에 존재하여 CPU는 SA 관리라는 가벼운 작업만 수행합니다.

📢 **섹션 요약 비유**: 회사에서 수천 통의 외부 기밀 서류를 매일 처리해야 할 때, 사장님(CPU)이 직접 암호표를 보고 펜으로 일일이 암호를 작성하면 회사 업무가 멈춥니다. 하지만 출입구에 '자동 암호화 번역기(Accelerator)'를 설치해두면, 직원들은 그냥 서류를 넣기만 하면 기계가 알아서 암호화된 문서로 바꿔 발송하므로 사장님은 경영 전략(제어 평면)에만 집중할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 상세 분석**
IPsec 오프로드 시스템은 크게 제어 평면(Control Plane)과 데이터 평면(Data Plane)으로 분리됩니다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **IKE Daemon** | SA 협상 및 키 교환 총괄 | IKEv2(Internet Key Exchange v2) 프로토콜을 사용하여 피어 간 인증 및 키 생성. Diffie-Hellman 그룹 연산 수행. | 외교관 (협상 담당) |
| **SA/SP DB** | 보안 정책 및 상태 저장 | Security Association DB(키, 라이프타임)와 Security Policy DB(어떤 트래픽을 암호화할지)를 NIC 메모리로 다운로드. | 암호 규칙집 |
| **Crypto Engine** | 하드웨어 암복호화 수행 | AES-NI, SHA Accelerator 등 전용 회로에서 SRAM에 캐싱된 키를 이용해 실시간 변환. 암호화 폭발력(Cipher Throughput) 제공. | 실무 번역가 |
| **Packet DMA** | 직접 메모리 접근 및 전송 | CPU 개입 없이 Host Memory의 패킷 데이터를 NIC 내부 버퍼로 가져오거나 내보냄 (Zero-copy). | 고속 화물 컨베이어 |
| **Bus Interface** | PCIe/커스텀 버스 연결 | Host 시스템과 가속기 간의 명령(CQ) 및 완료(Queue) 신호를 전송. | 데이터 고속도로 |

**2. ASCII 아키텍처 다이어그램**

```text
[Detailed IPsec Offload Data Flow]

  Host Memory (System RAM)                              NIC (Hardware)
+-----------------------+                     +-----------------------------------+
| Application Payload   |                     |   +-----------------------------+  |
| (Plaintext)           |                     |   |   Packet Parser & Classifier|  |
+-----------------------+                     |   +-------------+-----------------+  |
          | DMA Write                         |                 | Match SA        |
          v                                    |                 v                 |
+-----------------------+   Driver Command    |   +-----------------------------+  |
| NIC Driver (OS)       |-------------------> |   |   Crypto Context Store      |  |
| (Configures SA)       |   (Ingress SA Info) |   |   - Key Material            |  |
+-----------------------+                     |   |   - SPI / Sequence #        |  |
          ^                                    |   +-------------+---------------+  |
          | DMA Read                           |                 | Lookup          |
          |                                    |                 v                 |
          |          +-------------------------+-----------------+--------------+  |
          |          |                         |                 |              |  |
          |          |                         |                 v              |  |
          |          |                         |   +-----------------------------+  |
          |          |                         |   |   Crypto Engine (AES-GCM)   |  |
          |          |                         |   |   - Encrypt / Decrypt       |  |
          |          |                         |   |   - ICV Check (SHA-256)     |  |
          |          |                         |   +-------------+---------------+  |
          |          |                         |                 |                |
          |          |                         |                 v                |
          |          |                         |   +-----------------------------+  |
          +----------+-------------------------+---|   MAC / PHY (Wire)          |--+
                                                 +-----------------------------+
```

> **해설**:
> 1. **단계 1 (제어 설정)**: Host CPU의 운영체제 커널은 IKE 데몬을 통해 협상된 SA 정보(암호화 키, SPI 등)를 PCIe 버스를 통해 NIC 내부의 컨텍스트 메모리에 주입(Plumb)합니다. 이는 일회성 혹은 갱신 시점에 발생합니다.
> 2. **단계 2 (송신 경로 - Egress)**: 애플리케이�이 송신한 평문 패킷이 DMA(Direct Memory Access)를 통해 NIC로 전달됩니다. NIC의 패킷 파서(Packet Parser)는 패킷 헤더를 분석하여 SA DB를 조회하고, 해당 트래픽이 IPsec 대상임을 확인합니다.
> 3. **단계 3 (하드웨어 가속)**: 암호화 엔진은 ESP 헤더를 추가하고, 평문 페이로드를 AES-GCM 엔진으로 보냅니다. 하드웨어는 클럭 사이클 단위로 병렬 처리하여 암호문을 생성하고 ICV(Integrity Check Value)를 계산하여 트레일러에 붙입니다.
> 4. **단계 4 (수신 경로 - Ingress)**: 외부에서 들어온 암호화 패킷은 MAC 계층을 통과하자마자 복호화 엔진으로 전달됩니다. 키를 이용해 복호화하고 ICV를 검증하여, 무결성이 확인된 패킷만 평문으로 복원하여 Host 메모리로 기록합니다. 이 과정은 CPU의 인터럽트를 최소화합니다.

**3. 핵심 알고리즘 및 동작 코드**
대부분의 가속기는 AES-GCM(AES Galois/Counter Mode)을 지원합니다. 이 모드는 암호화와 인증을 동시에 수행하여 속도가 빠릅니다.

```c
// [Pseudo-Code: IPsec Offload Descriptor Structure]
struct ipsec_offload_desc {
    uint32_t spi;            // Security Parameter Index (SA Identifier)
    uint32_t src_ip;         // Source IP Address
    uint32_t dst_ip;         // Destination IP Address
    uint8_t  key[32];        // AES-256 Key (loaded into HW Key RAM)
    uint32_t salt;           // GCM Salt (for IV generation)
    uint8_t  operation;      // OP_ENCRYPT or OP_DECRYPT
    void    *src_addr;       // Physical Address of Input Packet
    void    *dst_addr;       // Physical Address of Output Buffer
};

// 1. Driver prepares descriptor in Ring Buffer
// 2. Hardware DMAs 'src_addr', applies AES-GCM using 'key'
// 3. Hardware writes result to 'dst_addr' and raises interrupt
```

📢 **섹션 요약 비유**: 협상가(제어 평면)가 상대방과 복잡한 암호 규칙(SA)을 정하고 그 규칙표를 기계에 입력해 두면, 이후 오가는 모든 편지는 해석기(데이터 평면)가 알아서 규칙에 따라 실시간으로 암호화하고 뜯어보는 자동화된 공장 라인과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Look-aside vs Inline**
IPsec 오프로드는 구현 방식에 따라 크게 'Look-aside'와 'Inline'으로 나뉩니다.

| 비교 항목 | Look-aside (Crypto Offload) | Inline (IPsec Offload) |
|:---|:---|:---|
| **데이터 흐름** | Host 메모리 → CPU 분석 → **Crypto Card** → CPU → NIC | Host 메모리 → **NIC (Inline Crypto)** → Wire |
| **CPU 개입** | 높음 (High). 패킷마다 암호 모듈 호출 필요. | 낮음 (Low). Setup 이후 CPU 무관심. |
| **PCIe 버스 부하** | 매우 높음 (암호화할 데이터를 왕복 2번 전송). | 낮음 (Descriptor만 전달). |
| **지연 시간 (Latency)** | 높음 (버스 트래픽 및 복사 오버헤드). | 가장 낮음 (Zero-copy, Wire-speed). |
| **주요 적용** | 별도의 암호화 카드(QAT) 장착 서버. | 고성능 스위치, SmartNIC, 게이트웨이. |

**2. 타 과목 융합 분석**

*   **OS 및 운영체제 (OS Internals)**
    *   **기술 스택**: IPsec 오프로드를 사용하더라도 OS 커널의 네트워크 스택(TCP/IP Stack)은 여전히 패킷의 라우팅과 소켓 처리를 담당합니다. 다만, `dev_queue_xmit()` 함수 호출 시 패킷을 암호화하는 코드 경로가 하드웨어 드라이버로 바이패스(Bypass)되도록 커널 드라이버가 수정되어야 합니다.
    *   **인터럽트(Interrupt) 절감效应**: 하드웨어가 복호화를 완료하고 평문을 메모리에 올리므로, CPU는 암호화 연산으로 인한 연산 인터럽트가 발생하지 않아 콘텍스트 스위칭(Context Switching) 오버헤드가 줄어듭니다.

*   **컴퓨터 구조 (Computer Architecture)**
    *   **캐시 효율성(Cache Locality)**: Software IPsec은 암호화 테이블(Key Table)과 데이터가 CPU 캐시(L1/L2)를 자주 교체하며 Cache Miss를 유발하지만, Hardware Offload는 NIC 내의 전용 SRAM을 사용하여 CPU 캐시 폴루션(Pollution)을 방지합니다.
    *   **NUMA(Non-Uniform Memory Access)**: 멀티코어 환경에서 오프로드 장치의 메모리 접근 최적화가 성능의 핵심 변수가 됩니다.

```text
[Performance Efficiency Comparison]

    CPU Utilization (%) vs Throughput (Gbps)
    ^
    |                          ___ (Hardware Limit)
    |                      ___/
    |                  ___/   <-- Inline Offload (Scalable)
    |              ___/
    |          ___/           <-- Look