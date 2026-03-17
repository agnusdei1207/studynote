+++
title = "281-284. 레거시 통신망 기술과 광통신(PON/AON)"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 281
+++

# 281-284. 레거시 통신망 기술과 광통신(PON/AON)

### # [레거시 통신망 기술과 광통신(PON/AON)]
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSMA/CD 방식의 이더넷이 가진 충돌(Collision) 및 비결정성(Non-determinism) 문제를 해결하기 위해 등장한 **토큰 패싱(Token Passing)** 기반의 제어 방식과 초기 광통신 기술의 진화 과정.
> 2. **가치**: 토큰 링/FDDI는 **결정적 지연 시간(Deterministic Latency)**과 **장애 복구(Fault Tolerance)** 능력을 제공하여 안정성이 중요한 산업용 망에서 가치를 인정받았으나, 비용 효율성에서 스위칭 이더넷에게 패배함.
> 3. **융합**: PON(Passive Optical Network)은 수동형 컴포넌트를 통해 운영 비용을 절감하여 FTTH(Fiber to the Home)의 표준으로 자리 잡았으며, 최근에는 10G-EPON/GPON 등을 통해 모바일 백홀(Backhaul)과 5G 망과 융합되고 있음.

---

## Ⅰ. 개요 (Context & Background)

### 1. 통신 제어 방식의 대결: 경쟁 vs 통제
1980년대 LAN(Local Area Network) 시장은 **"어떻게 유선 매체를 효율적으로 공유할 것인가"**에 대한 두 가지 철학의 대립으로 시작되었습니다.
- **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**: 이더넷의 방식으로, 모든 노드가 "전송해도 된다"라고 스스로 판단합니다. 구조가 단순하고 비용이 저렴하지만, 트래픽이 폭주할 경우 충돌로 인해 성능이 급격히 저하되는 **비결정적(Non-deterministic)**인 특성을 가집니다.
- **토큰 패싱 (Token Passing)**: 토큰 링의 방식으로, 전송 권한을 나타내는 특수한 프레임(토큰)을 오직 하나의 노드만 소유합니다. 토큰을 가진 노드만 전송하므로 충돌이 발생하지 않으며, 최악의 경우 지연 시간을 수학적으로 계산할 수 있는 **결정적(Deterministic)**인 특성을 가집니다.

### 2. 광통신의 등장과 표준 전쟁
광케이블(Optical Fiber) 기술의 발전은 단순히 속도를 높이는 것을 넘어, **FDDI (Fiber Distributed Data Interface)**와 같은 이중 링(Dual Ring) 구조를 통해 고가용성(High Availability)을 요구하는 데이터 센터나 캠퍼스 백본으로 진입했습니다. 하지만 1990년대 중반, **LAN 스위칭(LAN Switching)** 기술이 등장하면서 충돌 도메인을 분리하여 기존 이더넷의 단점을 해결하고, 가격 경쟁력까지 갖추게 되면서 토큰 링과 FDDI는 역사 속으로 사라지게 됩니다.

### 💡 비유
이는 **"버스표(토큰)를 구매해야 탈 수 있는 고속버스(토큰 링)"**와 **"일단 타고 보는 자유석 이용 차량(이더넷)"**의 차이와 같습니다. 자유석은 사람이 적으면 편하지만, 출근 시간(트래픽 폭주)에는 누가 먼저 탈지 다툼(충돌)이 발생해 엉망이 됩니다. 반면 버스표는 순서가 보장되지만, 표를 교체하는 시간(오버헤드)과 배차 간격 관리가 필요합니다.

### 📢 섹션 요약 비유
**CSMA/CD**는 양보 없는 '무법자의 자유시장'과 같아 혼잡하면 마비되고, **토큰 패싱**은 순서를 기다리는 '정돈된 병영 식당'과 같아 혼잡해도 멈추지 않습니다. 결국 **스위치**라는 강력한 교통경찰이 등장하며 저렴하고 빠른 자유시장이 시장을 장악하게 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 토큰 링 (Token Ring, IEEE 802.5)
IBM이 주도하여 개발한 방식으로, 물리적으로는 **Star(별)**형 배선을 하지만 논리적으로는 **Ring(고리)**형으로 신호가 순환합니다.

#### 구성 요소 및 동작 원리
| 요소명 | 역할 | 내부 동작 및 프로토콜 |
|:---|:---|:---|
| **MSAU (Multistation Access Unit)** | 허브 역할 | 물리적 스타 배선을 논리적 링으로 연결하며, 결함 발생 시 단락(short)시켜 링 유지 |
| **Token (3바이트)** | 전송 권한 | `SD(1)+AC(1)+ED(1)` 구조. Priority 비트를 포함하여 우선순위 제어 가능 |
| **Frame (프레임)** | 데이터 전송 | `SDEL(1)+FC(1)+DA(6)+SA(6)+Data+FCS(4)+EDEL(1)` 구조 |

#### 동작 메커니즘 (심층)
1. **토큰 전송**: 빈(Free) 토큰이 링을 따라 순환합니다.
2. **토큰 캡처 (Token Seizure)**: 데이터 전송을 원하는 노드는 토큰을 잡아 `Priority` 필드를 설정하고 **Busy** 상태로 변경합니다.
3. **데이터 전송 및 회수**: 송신 노드는 프레임을 붙여 보냅니다. 프레임은 목적지 노드에서 복사(Copy)되어 처리되며, 원형을 한 바퀴 돌아 다시 송신 노드로 돌아옵니다.
4. **검증 및 제거**: 송신 노드는 돌아온 프레임을 보고 전송 성공 여부를 확인한 후 프레임을 제거하고, 새로운 빈 토큰을 링에 내보냅니다.
5. **모니터링**: 하나의 노드는 **Active Monitor**로 지정되어 토큰 유실이나 무한 루프 프레임을 감시하고 복구합니다.

```ascii
      [논리적 링 토폴로지]
      
  Workstation A ────┐
                   │
  Workstation B ────┼───> (Token Frame Flow) ────┐
                   │                              │
  Workstation C ────┘                              │
                                                  │
(MSAU: 물리적 허브 내부에서 논리적 링 형성) <──────┘

1. A가 빈 토큰을 잡음(Token Capture)
2. A가 데이터를 실어 보냄(Frame Transmission)
3. B가 데이터를 받음(Copy) -> 지나감
4. A가 돌아온 프레임을 확인하고 제거(Stripping)
5. A가 새 토큰 발행(Token Release)
```
*해설: MSAU는 내부적으로 포트 간 신호를 릴레이하여 논리적인 고리를 만듭니다. 이 구조는 "아무도 말하지 않을 때 토큰이 사라지면?"과 같은 문제에 대해 Active Monitor가 주기적으로 토큰을 재생성하여 망이 죽는 것을 방지하는 자가 치유 메커니즘을 가집니다.*

### 2. FDDI (Fiber Distributed Data Interface)
토큰 링의 안정성을 광케이블의 대역폭과 결합하여 100Mbps를 구현한 기술입니다.

#### 핵심 기술: 이중 링 (Dual Ring)
- **Primary Ring (주 링)**: 평상시 데이터 전송에 사용됩니다.
- **Secondary Ring (보조 링)**: 예비용으로 대기하다가 장애 발생 시 활성화됩니다.
- **장애 복구 (Self-healing)**: 케이블 절단이나 노드 고장 발생 시, 두 링이 하나의 긴 링으로 연결(Wrap)되어 통신을 유지합니다.

```ascii
정상 상태 (Normal Traffic)
Clockwise (Primary) :  [A] --> [B] --> [C] --> [D] -->
Counter-Clockwise (Sec): [A] <-- [B] <-- [C] <-- [D] <--
(Secondary는 대기 상태)

장애 발생 시 (B와 C 사이 단선)
[Wrap 발생]
[A] --> [B] (X Cut) [C] --> [D] -->
           ^             │
           └─────────────┘
(노드 B와 C가 감지하여 Secondary Ring을 사용해 우회 경로 형성)
```
*해설: 이 "Self-healing" 기능은 현대의 **ERP (Ethernet Ring Protection Protocol)**이나 **RPR (Resilient Packet Ring)**의 선조격입니다. 50ms 이내에 장애를 복구하는 것이 목표였습니다.*

### 3. 핵심 알고리즘: 토큰 유지 시간 (TTRT, Target Token Rotation Time)
FDDI는 **Timed Token Protocol**을 사용하여 토큰의 순환 시간을 관리합니다. 모든 노드는 `TTRT`라는 목표 시간을 협상하며, 토큰이 돌아오는 시간(RTT)이 이를 초과하면 우선순위가 높은 트래픽(Synchronous) 위주로만 전송하고 일반 트래픽(Asynchronous)은 보냄을 멈춥니다.

```python
# Pseudo-code for FDDI Token Handling
def token_arrival(node):
    current_time = get_time()
    rotation_time = current_time - node.last_token_seen
    node.last_token_seen = current_time
    
    # 토큰 순환이 지연되고 있는가?
    if rotation_time > TTRT:
        # 지연 시간 동안 쌓인 동기 트래픽만 처리
        send_sync_frames(max_duration=TTRT)
    else:
        # 여유가 있으면 비동기(일반) 트래픽까지 처리
        send_sync_frames()
        remaining_time = TTRT - rotation_time
        send_async_frames(max_duration=remaining_time)
    
    pass_token_to_next()
```

### 📢 섹션 요약 비유
토큰 링은 **단일 트랙 육상 경기장**과 같습니다. 선수(데이터)가 트랙(링)을 한 바퀴 돌아야 다음 사람이 들어갈 수 있습니다. FDDI는 이 트랙이 **2중으로 되어 있어서** 한쪽이 무너져도 다른 쪽으로 우회해서 뛸 수 있는 튼튼한 경기장을 제공합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 경쟁 기술 심층 비교: 이더넷 vs 토큰 링/FDDI

| 비교 항목 | 이더넷 (IEEE 802.3) | 토큰 링 (IEEE 802.5) / FDDI |
|:---|:---|:---|
| **매체 접근 방식** | CSMA/CD (비경쟁적 접근 시도) | 토큰 패싱 (순차적 접근 보장) |
| **결정성 (Determinism)** | X (부하 시 지연 예측 불가) | O (TTRT에 의한 지연 보장) |
| **확장성 (Scalability)** | 낮음 (충돌 도메인 문제) | 높음 (트래픽 증가 시 처리량 유지) |
| **장비 비용** | 저가 (Hub 사용 가능) | 고가 (MSAU, 토큰 관리 회로 필요) |
| **배포 복잡도** | 간단 (TIA/EIA-568B 표준 케이블링) | 복잡 (논리적 링 구성) |
| **결과** | **시장 승리** (Cost/Performance) | **시장 패배** (특수 용도로 잔존) |

> **💡 기술사적 판단 (Decision Matrix)**:
> 이더넷이 승리한 결정적인 계기는 **스위칭(Switching)** 기술이었습니다. 스위치는 충돌 도메인을 포트별로 분리하여 CSMA/CD의 단점을 원천적으로 봉쇄했습니다. 이로 인해 이더넷은 "저렴한 비용 + 빠른 속도 + 스위치로 인한 안정성"이라는 삼박자를 갖추게 되었습니다. 반면 FDDI는 100Mbps라는 동등한 속도를 제공했지만, NIC(네트워크 카드) 및 스위치 포트당 가격이 이더넷의 5~10배에 달했기에 도태될 수밖에 없었습니다.

### 2. MAN 표준 전쟁: DQDB (IEEE 802.6)
DQDB는 도시 규모(MAN)의 통신을 위해 설계되었습니다. 양방향으로 흐르는 두 개의 버스에 슬롯(Slot)을 실어 보내는 방식입니다.
- **구조**: 버스 A (정방향), 버스 B (역방향). 노드는 읽기용 헤드와 쓰기용 헤드를 분리하여 **Slotted Ring**과 유사한 효과를 냅니다.
- **ATM과의 관계**: 셀(Cell) 기반 전송 기술은 후에 ATM(Asynchronous Transfer Mode) 기반의 B-ISDN(Broadband ISDN)의 기반이 되었습니다. 현재는 거의 사용되지 않으며, 그 자리는 **MPLS (Multiprotocol Label Switch)**와 **Metro Ethernet**이 차지했습니다.

### 📢 섹션 요약 비유
이더넷과 토큰 링의 싸움은 **"자전거 도로(이더넷)"**와 **"고속열차 트랙(토큰 링)"**의 싸움과 같습니다. 자전거 도로는 신호등이 없고(잠재적 충돌) 난잡하지만, 고속열차는 정해진 시간에만 출발합니다(순서 보장). 하지만 교통 체증을 해결하는 **고가 도로(스위치)**가 자전거 도로 위에 싸게 깔리자, 비싼 고속열차 시스템을 굳이 유지할 이유가 사라진 것입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (FTTH 구현: PON vs AON)

현대의 통신망은 전화국(CO, Central Office)부터 가정까지 광케이블을 연결하는 FTTH(Fiber to the H