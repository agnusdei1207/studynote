+++
title = "589. IPsec 오프로드 가속기"
weight = 589
+++

> **Insight**
> - IPsec(Internet Protocol Security) VPN 등에서 발생하는 고비용의 암복호화 연산을 Host CPU(Central Processing Unit) 대신 전용 하드웨어가 처리하는 기술
> - AES(Advanced Encryption Standard), SHA(Secure Hash Algorithm) 등 암호화 알고리즘의 선속도(Line Rate) 처리를 보장하여 네트워크 지연을 최소화
> - 엔터프라이즈 보안 게이트웨이, 클라우드 인프라간의 연결(SD-WAN)에서 필수적인 성능 향상 컴포넌트

## Ⅰ. IPsec 오프로드 가속기(IPsec Offload Accelerator)의 개요

IPsec 오프로드 가속기는 네트워크 계층에서 데이터 기밀성(Confidentiality), 무결성(Integrity), 인증(Authentication)을 제공하는 IPsec 프로토콜의 복잡한 암호화 및 복호화 과정을 하드웨어 수준에서 가속하는 장치입니다. IPsec 트래픽을 처리할 때 CPU는 대칭키 암호화(예: AES-GCM), 해시 연산(예: HMAC-SHA256) 등 막대한 연산량을 요구받아 시스템 성능 병목을 일으킵니다. 이를 해결하기 위해 NIC(Network Interface Card) 내부의 전용 ASIC(Application-Specific Integrated Circuit) 또는 암호화 코-프로세서(Co-processor)로 작업을 오프로드(Offload)하여, 보안이 강화된 환경에서도 10Gbps 이상의 고속 데이터 전송을 가능하게 합니다.

📢 **섹션 요약 비유**: 회사에서 외부로 보내는 모든 기밀 서류를 사장님(CPU)이 직접 손으로 암호로 바꿔 쓰려면 너무 오래 걸리지만, '자동 암호화 번역기(IPsec 오프로드 가속기)'를 도입하면 순식간에 암호로 바꿔 발송할 수 있는 것과 같습니다.

## Ⅱ. IPsec 오프로드의 아키텍처 및 동작 원리

IPsec 오프로드 아키텍처는 데이터 평면(Data Plane)과 제어 평면(Control Plane)의 분리를 기반으로 합니다.

```text
[IPsec Offload Architecture]

   Control Plane (CPU / OS)               Data Plane (NIC / Hardware Accelerator)
+-------------------------------+       +-----------------------------------------+
| IKE Daemon (Key Exchange)     |       |                                         |
| SA (Security Association) DB  |       |     Hardware Encryption Engine          |
| SP (Security Policy) DB       |  ==>  |     (AES-GCM, SHA, Crypto Co-processor) |
+-------------------------------+ (SA)  |                                         |
               |                        +-----------------------------------------+
               | (Plaintext Packet)                     ^     | (Encrypted Packet)
               v                                        |     v
+-------------------------------+       +-----------------------------------------+
| Network Stack (IP/TCP)        |       | Physical Network Interface (MAC/PHY)    |
+-------------------------------+       +-----------------------------------------+
```

1. **제어 평면 (IKE/SA 협상):** IKE(Internet Key Exchange)를 통한 키 교환 및 보안 연관(SA, Security Association) 설정은 여전히 Host CPU의 소프트웨어가 처리합니다.
2. **SA 이관 (SA Offload):** 확립된 암호화 키와 보안 정책(SA/SP) 정보가 하드웨어 가속기(NIC)로 주입(Plumb)됩니다.
3. **데이터 평면 (인라인 암복호화):** 송신되는 일반 평문 패킷은 NIC를 통과하면서 주입된 SA 정보를 바탕으로 하드웨어 엔진에 의해 즉시 암호화 및 IPsec 캡슐화(ESP/AH)가 이루어집니다. 수신 시에도 하드웨어에서 즉시 복호화되어 OS에는 평문으로 전달됩니다.

📢 **섹션 요약 비유**: 협상가(제어 평면)가 상대방과 암호 규칙을 정한 뒤, 그 규칙표(SA)를 암호 해석기(데이터 평면 가속기)에 입력해 두면, 이후 오가는 모든 편지는 해석기가 알아서 실시간으로 번역해 주는 구조입니다.

## Ⅲ. IPsec 오프로드의 핵심 기술 및 구현 방식

IPsec 오프로드는 하드웨어 개입 정도에 따라 두 가지 주요 방식으로 구현됩니다.

1. **Crypto Offload (Look-aside 방식):**
   * CPU가 패킷을 받아 암호화/복호화가 필요할 때마다 PCIe 버스를 통해 별도의 암호화 가속기(예: Intel QAT)로 데이터를 보내고, 연산이 끝난 데이터를 다시 받아 패킷을 조립하는 방식입니다.
   * 유연성은 높으나, PCIe 버스를 두 번 타야 하므로 지연 시간(Latency)이 다소 발생합니다.
2. **Inline IPsec Offload (Full Offload 방식):**
   * NIC 칩셋 내부에 암호화 파이프라인이 내장되어 있어, 패킷이 네트워크 밖으로 나가기 직전(또는 들어오자마자) MAC 계층 부근에서 즉시 암복호화가 이루어집니다.
   * CPU 개입이 전혀 없으며, Zero-copy 전송이 가능하여 최상의 Throughput과 최저 지연 시간을 제공합니다.

📢 **섹션 요약 비유**: 문서 번역을 외주 번역 센터에 보냈다가 다시 받는 방식(Look-aside)과, 출력기 자체에 실시간 번역 기능이 내장되어 종이가 나오면서 바로 번역본으로 출력되는 방식(Inline)의 차이입니다.

## Ⅳ. 하드웨어 가속의 성능 이점 및 적용 사례

IPsec 오프로드를 적용하면 시스템 성능이 비약적으로 향상됩니다.

| 비교 항목 | Software IPsec | IPsec Hardware Offload (Inline) |
| :--- | :--- | :--- |
| **Throughput** | CPU 성능에 크게 의존 (보통 수 Gbps 한계) | 선속도 보장 (10Gbps ~ 100Gbps 이상) |
| **CPU 점유율** | 매우 높음 (대규모 트래픽 시 시스템 마비 위험) | 매우 낮음 (IKE 제어 트래픽만 처리) |
| **전력 소모** | 높음 (범용 CPU의 비효율적인 연산) | 낮음 (전용 ASIC의 고효율 연산) |

**주요 적용 사례:**
* **SD-WAN (Software-Defined Wide Area Network):** 여러 지사 간의 안전한 통신을 위해 대량의 IPsec 터널을 생성할 때 필수적입니다.
* **5G 코어 네트워크:** 셀 타워와 코어망(Backhaul) 간의 기밀성을 보장하는 보안 터널링 환경에 사용됩니다.
* **클라우드 데이터센터:** VPC(Virtual Private Cloud) 간의 암호화된 트래픽 전송 시 하이퍼바이저의 부담을 줄이기 위해 사용됩니다.

📢 **섹션 요약 비유**: 짐꾼(CPU)들이 수백 개의 금고(암호화 패킷)를 직접 잠그고 여느라 지쳐 쓰러지는 환경에서, 전용 자동화 라인(하드웨어 가속)을 도입해 짐꾼들은 짐만 나르고 금고는 기계가 순식간에 잠그고 열어주게 된 것입니다.

## Ⅴ. 기술 한계 및 차세대 보안 인프라 (SmartNIC)

전통적인 고정형 ASIC 기반의 IPsec 오프로드는 양자 컴퓨터의 등장 등에 대비한 새로운 암호화 알고리즘(Post-Quantum Cryptography)이나 복잡한 라우팅 정책을 수용하기에는 유연성이 부족하다는 한계가 있습니다.

이를 극복하기 위해, 최근에는 프로그래밍이 가능한 **SmartNIC 및 DPU(Data Processing Unit)**가 차세대 IPsec 오프로드의 주역으로 떠오르고 있습니다. DPU는 P4(Programming Protocol-independent Packet Processors) 언어나 eBPF(extended Berkeley Packet Filter)를 활용하여 데이터 평면의 암호화 파이프라인을 유연하게 재정의할 수 있으며, IPsec뿐만 아니라 TLS/SSL, MACsec 등 다양한 보안 프로토콜을 동시에 통합 처리할 수 있는 구조로 진화하고 있습니다.

📢 **섹션 요약 비유**: 옛날 열쇠 제조기(ASIC)는 딱 정해진 모양의 열쇠만 만들 수 있었지만, 최신 3D 프린터(DPU/SmartNIC)는 소프트웨어 도면만 업데이트하면 언제든 새롭고 복잡한 모양의 미래형 열쇠도 찍어낼 수 있는 것과 같습니다.

---
**Knowledge Graph & Child Analogy**

* **지식 그래프 (Knowledge Graph):**
  * `IPsec 오프로드` --> `보안 연산 분산` --> `AES/SHA 가속`
  * `IPsec 오프로드` --> `동작 방식` --> `Look-aside vs Inline`
  * `IPsec 오프로드` --> `주요 적용` --> `SD-WAN, 5G Backhaul, DPU`
* **어린이 비유 (Child Analogy):**
  * 친구한테 비밀 편지를 보낼 때 내가 직접 복잡한 암호표를 보면서 한 글자씩 바꾸면 너무 힘들고 오래 걸리잖아요? 그런데 마법의 봉투(IPsec 오프로드 가속기)가 있어서 편지를 넣기만 하면 순식간에 암호로 바뀌어서 날아가게 해주는 기술이에요!
