+++
title = "303-306. 클래스리스(Classless) 라우팅과 CIDR/VLSM"
date = "2026-03-14"
[extra]
category = "Network Layer"
id = 303
+++

# 303-306. 클래스리스(Classless) 라우팅과 CIDR/VLSM

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IP 주소 체계의 고정된 계급(Class) 구조를 허물고, 네트워크 경계를 비트(Bit) 단위로 유연하게 재정의하는 주소 할당 및 라우팅 기술이다.
> 2. **가치**: IPv4 주소 고갈 문제를 지연시키고 라우팅 테이블(Routing Table)의 폭발적인 증가를 억제하여 인터넷의 확장성과 효율성을 획기적으로 개선했다.
> 3. **융합**: 라우터의 Forwarding 로직과 OSPF/BGP 같은 라우팅 프로토콜의 Subnet 지원 능력에 필수적인 기반이 되며, IPv6의 주소 할당 철학과도 연결된다.

---

### Ⅰ. 개요 (Context & Background) - CIDR로의 패러다임 시프트

**개념 및 철학**
과거 IP 주소 체계는 8비트 단위의 경계를 가진 A, B, C 클래스(Classful Addressing)로 고정되어 있었다. 이는 할당받은 네트워크 크기에 상관없이 '올인(All-in)' 방식으로 주소를 사용해야 했던 비효율을 낳았다. 이를 극복하기 위해 등장한 것이 **CIDR (Classless Inter-Domain Routing)**이다. CIDR은 네트워크와 호스트의 경계를 클래스에 얽매이지 않고 임의의 비트 위치에서 설정할 수 있게 하여, 주소 자원을 '필요한 만큼만' 정확히 할당하는 것을 목표로 한다.

**💡 비유**
도로 주소 체계에 비유하자면, Classful 방식은 '대한민국 서울시 강남구' 단위로만 건물 번지를 부여하는 것과 같아서, 건물이 한 채뿐인 곳에도 수만 개의 번지를 부여해 낭비가 심했다. CIDR은 '강남구 역삼동 123번지 1층'처럼 필요한 정확한 범위만큼만 주소를 떼어 줄 수 있게 한 것이다.

**등장 배경**
① **기존 한계**: Class B 주소의 고갈과 Class C 주소 할당에 따른 라우팅 테이블의 인덱스 폭발(Routing Table Explosion) 문제 대두.
② **혁신적 패러다임**: 네트워크 접두부(Prefix) 길이(`/n`)를 도입하여 주소 블록을 유연하게 분할(Subnetting) 및 통합(Supernetting).
③ **비즈니스 요구**: 인터넷 폭발적 성장 시기, ISP(Internet Service Provider)가 효율적으로 주소를 관리하고 고객에게 제공할 수 있는 체계가 절실했음.

**📢 섹션 요약 비유**
이는 기존의 L, XL, XXL 사이즈로만 옷을 입던 시스템에서, 테일러링(Tailoring)을 통해 사람들의 체형에 딱 맞는 사이즈(주소)를 제작해 입히는 것과 같은 혁신입니다. 옷감(IP 주소) 낭비를 막고 더 많은 사람에게 옷을 입힐 수 있게 된 셈입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CIDR과 Classless 라우팅의 핵심은 **IP 주소를 네트워크 부와 호스트 부로 나누는 기준인 'Subnet Mask'를 가변적으로 설정**하는 데 있다.

**구성 요소 상세**

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **Network Prefix** | 네트워크의 식별자 (도로명) | 상위 비트부터 연속된 1로 설정. 길이가 길수록 호스트 수는 줄어듦. | `/24`는 24비트 네트워크 |
| **Host ID** | 네트워크 내 호스트 식별 (번지) | 나머지 하위 비트. 2진수 계산으로 할당 가능 호스트 수 도출. | All 0(네트워크), All 1(Broadcast) 제외 |
| **Subnet Mask** | 경계를 알려주는 32비트 필터 | IP 주소와 **AND 연산**을 수행하여 Network Address 추출. | 255.255.255.0 (/24) 등 |
| **CIDR Block** | 연속적인 IP 주소의 묶음 | 할당의 단위. 라우팅 시 이 블록 단위로 정보를 교환함. | Route Aggregation의 기초 |
| **Routing Table** | 경로 정보 저장소 | 목적지 IP와 Prefix 길이를 매칭(Longest Prefix Match). | 클래스리스 라우터 필수 지원 |

**ASCII 구조 다이어그램: Classless IP 주소 구조**

아래는 `192.168.10.0/24`와 `192.168.10.128/25`의 구조적 차이를 시각화한 것이다.

```text
       0                   1                   2                   3
       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/24:  | Network (24 bits)           | Host (8 bits)                 |
      | 11000000.10101000.00001010.| 00000000 (Last octet varies)   |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       Description: Standard Class C boundary. Flexible but fixed.

      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/25:  | Network (25 bits)           | Host (7 bits)                 |
      | 11000000.10101000.00001010.|0| 0000000 (Subnet 1)           |
      |                           |1| 0000000 (Subnet 2)           |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       Description: Borrowed 1 bit from Host to split network.
```
*해설*: `/24`는 8비트(256개) 호스트를 가진 하나의 네트워크다. 하지만 `/25`는 호스트 영역에서 1비트를 빌려와 네트워크 영역(25비트)으로 확장했다. 이때 빌려온 1비트가 0이면 `128개`, 1이면 `128개` 짜리 네트워크 2개로 분할(Subnetting)된다.

**심층 동작 원리: 2진수 분할 및 계산**
서브넷 마스크의 동작 원리는 비트 연산에 기초한다.
1.  **Binary Conversion**: IP 주소와 마스크를 2진수로 변환한다.
    *   IP: `192.168.1.0` $\rightarrow$ `11000000.10101000.00000001.00000000`
    *   Mask `/24`: `11111111.11111111.11111111.00000000`
2.  **AND Operation**: 각 비트에 대해 논리곱(AND)을 수행하면 네트워크 주소가 나온다.
    *   결과: `11000000.10101000.00000001.00000000` (`192.168.1.0`)
3.  **Host Calculation**: 남은 호스트 비트 수($n$)에 대해 $2^n - 2$ (Usable IPs)를 계산한다.

**핵심 알고리즘: VLSM Address Planning (Python Style)**
VLSM(Variable Length Subnet Mask)를 적용한 주소 할당 의사코드이다. 큰 네트워크부터 작은 순으로, 혹은 작은 것부터 할당할 때의 겹침을 방지하는 로직이 필요하다.

```python
# [VLSM Allocation Logic Concept]
def allocate_vlsm(network_pool, required_hosts):
    """
    네트워크 풀(Prefix)에서 필요한 호스트 수를 수용할 수 있는
    가장 작은(적합한) 서브넷 블록을 계산하여 반환하는 함수
    """
    # 1. Calculate required host bits (include Network/Broadcast)
    host_bits = math.ceil(math.log2(required_hosts + 2))
    
    # 2. Determine new prefix length
    new_prefix = 32 - host_bits
    
    # 3. Check if we have enough space in current pool
    if new_prefix < current_prefix:
        raise Error("Not enough address space")
        
    # 4. Return allocated block and remaining pool
    allocated_block = f"{base_ip}/{new_prefix}"
    next_base_ip = calculate_next_base(allocated_block)
    
    return allocated_block, next_base_ip

# Example: LAN A (100 hosts), LAN B (50 hosts)
# Block 192.168.1.0/24
# -> LAN A: needs 7 bits (128 hosts) -> /25 (192.168.1.0/25)
# -> Remainder: 192.168.1.128/25
# -> LAN B: needs 6 bits (64 hosts) -> /26 (192.168.1.128/26) 
#    (Taken from the remainder of the first split)
```

**📢 섹션 요약 비유**
피자 도우(전체 네트워크)를 자르는 과정과 같습니다. 우선 고객이 원하는 크기(필요 호스트 수)에 맞춰 칼질(서브넷 마스크 설정)을 합니다. 자르고 남은 도우 조각은 다시 다른 고객이 원하는 크기에 맞춰 또 자를 수 있습니다. VLSM은 한 도우를 8조각으로 자른 것과 4조각으로 자른 것을 한 테이블에 놓고 먹을 수 있게 하는 기술입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Classful vs Classless**

| 구분 | Classful Routing (A/B/C) | Classless Routing (CIDR/VLSM) |
|:---|:---|:---|
| **Subnet Mask** | 클래스별로 고정 (A=/8, B=/16, C=/24). 라우팅 정보에 마스크 정보가 없음. | 가변 길이. 라우팅 업데이트 시 **Subnet Mask 정보를 포함**하여 전송. |
| **주소 할당** | 블록 단위로만 할당 가능. 내부적으로 낭비 발생. | 비트 단위로 정확히 필요한 만큼만 할당. 효율 극대화. |
| **Routing Protocol** | RIPv1 (지원 안 함), IGRP. | RIPv2, **OSPF**, **EIGRP**, BGP4, IS-IS. |
| **Routing Table** | 3개의 Main Entry와 Subnet Entry로 관리 어려움. | **Route Summarization(요약)**을 통해 테이블 크기 최소화 가능. |
| **Discontiguous Net** | 지원 불가 (같은 네트워크가 떨어져 있으면 연결 안 됨). | 지원 가능 (물리적 거리와 무관하게 논리적 연결 가능). |

**2. 수학적 분석: VLSM 효율성**
*   **시나리오**: 3개의 부서(A=50명, B=25명, C=10명)에 주소 할당.
*   **Fixed (/24) 방식**:
    *   3개의 C클래스 필요: $256 \times 3 = 768$개 주소 소요 (실제 사용: 85개, 낭비: 683개, 약 **89% 낭비**).
*   **VLSM 방식**:
    *   A(50명) $\rightarrow$ $2^6-2 (64)$ 사용 $\rightarrow$ **/26**
    *   B(25명) $\rightarrow$ $2^5-2 (32)$ 사용 $\rightarrow$ **/27**
    *   C(10명) $\rightarrow$ $2^4-2 (16)$ 사용 $\rightarrow$ **/28**
    *   단일 /24 블록(256개) 내에서 모두 해결. 낭비 최소화.

**3. 과목 융합 관점**
*   **OS (Operating System)**: OS의 TCP/IP 스택은 Subnet Mask를 기반으로 **Local Subnet(로컬 전송)** 여부를 판단한다. (Dest IP & Mask == My IP & Mask ? ARP : Gateway). Mask가 틀리면 이중 로컬라이제이션 오류가 발생한다.
*   **보안 (Security)**: VLSM을 활용해 **DMZ(DeMilitarized Zone)** 구성 시, 공인 IP를 절약하거나 내부 서브넷을 세분화하여 보안 구역(Security Zone)을 물리/논리적으로 격리하는 데 사용된다.

**📢 섹션 요약 비유**
수도꼭지의 밸브 조절과 같습니다. Classful은 '약하게', '중간', '강하게' 3단계 밸브만 고를 수 있는 반면, CIDR은 미세하게 수도 꼭지를 돌려 정확히 원하는 유량만큼만 물을 쓸 수 있는 정밀 밸브입니다. 이를 통해 전체 배관(인터넷)의 수압(라우팅 부하)도 효과적으로 조절할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**
*   **상황 1: 대기업 본사 네트워크 설계**
    *   각 층의 부서별 PC 수와 IP 폰, 프린터 대수를 합쳐 `/23`이 필요한 층과 `/26`으로 충분한 층을 구분하여 VLSM 설계.
    *   **Decision**: 충분한 여유를 두되, 향후 확장 시 네트워크 재설계(Re-IP)가 필요 없도록 20% 여유분을 가진 서브넷 마스크를 선정.
*   **상황 2: ISP 통합망 구성**
    *   지사별로 흩어진 Class C 주소들을 Supernetting하여 본사 라우터에서 하나의 경로로 요약(Route Summarization).
    *   **Decision**: 지사 라우터 장애 시 본사 라우팅 테이블 업데이트 폭주를 방지하기 위해, 지사별로 연속적인 주소 블록을 할당하는 것이 중요함.

**2. 도입 체크리스트**
*   **기술적**:
    *   [ ] 모든 라우터와 L3 스위치가 Classless 라우팅(`ip classless` 명령어 등)을 지원하는가?
    *   [ ] RIPv1 등 구형 프로토콜을 사용하는 레거시 장비는 없는가?
    *   [ ] 할당된 주소 범위 간 중첩(Overlap)이 발생하지 않는가?
*   **운영·보안적**:
    *   [ ] VLSM 설계도서(주소 할당표)를 작성하여 관리자 외에는 내부 구조를 유추하기 어렵게 하는가?
    *   [ ] 특정 서브넷 간의 통신 제한(Access Control)이 방화벽 규칙과 일치하는가?

**3. 안티패턴 (Anti-Pattern)**
*   **피넛 버터 네트