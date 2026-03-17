+++
title = "709. 브로커 패턴 분산 시스템 미들웨어"
date = "2026-03-15"
weight = 709
[extra]
categories = ["Software Engineering"]
tags = ["Design Pattern", "Architectural Pattern", "Broker Pattern", "Distributed Systems", "Middleware", "CORBA"]
+++

# 709. 브로커 패턴 분산 시스템 미들웨어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 환경에서 **서비스 제공자(Server)**와 **소비자(Client)** 사이의 통신을 중재하여 **위치 투명성(Location Transparency)**과 **접근 투명성(Access Transparency)**을 제공하는 아키텍처 패턴.
> 2. **가치**: 이기종(Heterogeneous) 시스템 간의 결합도를 낮추어 확장성(Scalability)과 유연성(Flexibility)을 확보하며, RPC(Remote Procedure Call) 기술의 기반이 됨.
> 3. **융합**: 현대의 **MSA (Microservices Architecture)**에서 **Service Mesh**나 **API Gateway**의 근간이 되며, 대용량 분산 처리를 위한 **Message Queue (MQ)** 시스템으로 발전하고 있음.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**브로커(Broker) 패턴**은 분산 처리 환경(Distributed Computing Environment)에서 객체 간의 통신을 담당하는 **미들웨어(Middleware)**의 일종입니다. 클라이언트(Client)가 서버(Server)의 물리적 위치(IP, Port)나 구현 세부사항(언어, 프로토콜)을 알지 못하더라도, 브로커라는 중재자를 통해 서비스를 요청하고 결과를 받을 수 있도록 **통신 계층(Ccommunication Layer)**을 추상화합니다.

이 패턴의 핵심 철학은 **"분리(Separation of Concerns)"**입니다. 비즈니스 로직(서비스)과 통신 로직(전송)을 철저히 분리하여, 시스템의 구성 요소가 변경되더라도 다른 부분에 영향을 미치지 않도록 설계합니다.

#### 2. 등장 배경: N-Tier 아키텍처의 복잡성
- **① 기존 한계 (Tight Coupling)**: 초기 클라이언트-서버 모델에서는 클라이언트가 서버의 IP 주소를 하드코딩(Hard-coding)해야 했으며, 서버가 변경되면 모든 클라이언트를 재배포해야 하는 문제가 있었습니다.
- **② 혁신적 패러다임 (Indirect Communication)**: **CORBA (Common Object Request Broker Architecture)**, **RMI (Remote Method Invocation)**, **DCOM (Distributed Component Object Model)** 등의 등장으로 브로커 개념이 도입되었습니다. 이를 통해 '메시지 전달 책임'을 브로커에게 위임하게 되었습니다.
- **③ 현재의 비즈니스 요구**: 클라우드 컴퓨팅과 MSA 환경에서는 수천 개의 서비스 Instance가 동적으로 생성되고 소멸합니다. 고정된 주소를 사용하는 기존 방식으로는 이를 관리할 수 없으므로, 동적인 서비스 발견(Service Discovery)과 라우팅(Routing)을 수행하는 브로커가 필수적입니다.

#### 3. 핵심 용어 정리
- **ORB (Object Request Broker)**: CORBA 표준에서 사용하는 용어로, 객체 간의 요청을 중계하는 소프트웨어 버스.
- **Marshalling (마샬링)**: 전송을 위해 객체나 데이터 구조를 바이트 스트림으로 변환하는 직렬화 과정.
- **Unmarshalling (언마샬링)**: 수신된 바이트 스트림을 다시 객체나 데이터 구조로 복원하는 역직렬화 과정.

```text
      [변천사 관점] 브로커 패턴의 진화
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  [1990s]                     [2000s]                     [2020s]            │
│  Monolith Era                SOA Era                    Cloud/MSA Era       │
│                                                                             │
│  ┌───────┐                  ┌───────┐                  ┌───────────┐        │
│  │ CORBA │  ────────────▶   │  ESB  │  ────────────▶   │ API Gate- │        │
│  │  ORB  │ (Heavyweight)    │(Broker)│ (Centralized)    │ way/Kafka │        │
│  └───────┘                  └───────┘                  │(Smart Br.)│        │
│                                                                             │
│  Purpose: Obj. Comm.      Purpose: Ent. Integ.      Purpose: Micro Sv.     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **📢 섹션 요약 비유**
> 브로커 패턴은 **'복잡한 국제 통화 서비스'**와 같습니다. 내가 한국어를 구사하는 고객(Client)이고, 상대방은 영어를 사용하는 은행(Server)이라 할 때, 통화를 직접 하려면 언어를 배우거나 번역기가 필요합니다. 하지만 **'통화 중개(Broker)'** 서비스를 이용하면, 나는 그저 한국어로 요청하고 중계사가 알아서 영어권 은행에 전달하고 결과를 한국어로 번역해 줍니다. 나는 상대방이 어디에 있는지, 어떤 언어를 쓰는지 전혀 몰라도 서비스를 이용할 수 있는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
브로커 패턴은 최소 5개 이상의 주요 컴포넌트로 구성되며, 각각이 독립적인 역할을 수행합니다.

| 요소명 | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|
| **Broker** | **핵심 중재자**. 브로커 레지스트리를 관리하며 클라이언트의 요청을 분석하여 적절한 서버를 찾아(Lookup) 연결해주는 'Dispatcher' 역할 수행. | IIOP, HTTP, gRPC | 통화 교환국 |
| **Client Proxy** | 클라이언트 로컬에 존재하는 **대리인(Stub)**. 원격 호출(RPC)을 마치 로컬 메서드 호출인 것처럼 보이게 하며, 요청 매개변수를 직렬화(Marshal)하여 전송. | IDL Stub, Feign | 국외 수신자 |
| **Server Proxy** | 서버 로컬에 존재하는 **접수원(Skeleton)**. 브로커로부터 받은 요청을 역직렬화(Unmarshal)하여 실제 서버 객체의 메서드를 호출하고 결과를 다시 직렬화하여 반환. | IDL Skeleton | 현지 수신자 |
| **Bridge** | **이기종 브로커 간의 연결고리**. 서로 다른 프로토콜이나 규격을 사용하는 브로커들 사이에서 요청을 변환하고 중계 (예: IIOP ↔ HTTP). | Protocol Converter | 번역 통번역사 |
| **Registry** | 서버가 자신의 서비스를 등록(Registration)하는 **저장소**. 브로커가 서버를 찾을 때 참조하는 DB 역할. | LDAP, Zookeeper, Consul | 전화번호부 |

#### 2. 상세 작동 프로세스 (Interaction Cycle)
브로커 패턴을 통한 통신은 5단계의 확정된 과정을 거칩니다.

1. **Registration (등록)**: 서버 기동 시 Server Proxy는 Broker에게 자신의 주소와 제공 서비스 ID를 등록. Registry에 저장됨.
2. **Invocation (요청)**: 클라이언트가 IDL(Interface Definition Language)로 정의된 인터페이스를 호출. 이는 로컬 Client Proxy를 거침.
3. **Marshaling (마샬링)**: Client Proxy는 매개변수 객체를 네트워크 전송 가능한 포맷(일반 바이트 스트림)으로 변환.
4. **Routing & Dispatching (전송 및 분배)**: Broker가 메시지를 수신하여 Registry를 조회. 해당 서비스를 제공하는 서버의 위치를 파악 후 Server Proxy로 전달.
5. **Execution & Response (실행 및 응답)**: Server Proxy는 언마샬링을 수행한 뒤 실제 Server Object를 실행. 결과를 다시 마샬링하여 Broker → Client로 반환.

```text
        [Broker Pattern: Interaction Sequence Diagram]

Client App           Client Proxy           Broker             Server Proxy           Server Object
   │                       │                   │                     │                     │
   │  1. Request Method()  │                   │                     │                     │
   │ ─────────────────────▶│                   │                     │                     │
   │                       │  2. Marshal Data  │                     │                     │
   │                       │ ────────────────▶ │                     │                     │
   │                       │  3. Find Server   │                     │                     │
   │                       │ ◀──────────────── │                     │                     │
   │                       │  4. Send Request  │                     │                     │
   │                       │ ──────────────────────────────────────▶ │                     │
   │                       │                   │                     │  5. Unmarshal & Call│
   │                       │                   │                     │ ──────────────────▶ │
   │                       │                   │                     │                     │ [Execute]
   │                       │                   │                     │ ◀───────────────── │
   │                       │                   │                     │ 6. Return & Marshal│
   │                       │ ◀──────────────── │ ◀────────────────── │                     │
   │  7. Receive Result    │                   │                     │                     │
   │ ◀──────────────────── │                   │                     │                     │
   │                       │                   │                     │                     │
   * 데이터 흐름: App → Proxy → [Network] → Broker → [Network] → Proxy → Impl.
   * "어댑터(Adapter)와 퍼사드(Facade) 패턴이 결합된 구조"
```

#### 3. 핵심 알고리즘: IDL 및 마샬링
기술사 시험에서 중요한 것은 이 '인터페이스 정의'입니다. 서로 다른 언어(C++, Java, Python) 간 통신이 가능한 이유는 **IDL (Interface Definition Language)**이라는 중립적인 계약서가 있기 때문입니다.

```python
# [의사코드] IDL 컴파일러가 생성한 Client Proxy의 내부 동작 로직

class ClientProxy:
    def request_service(self, params):
        # 1. Marshalling: 직렬화
        # 파라미터 객체를 네트워크 패킷(바이트 스트림)으로 변환
        byte_stream = serialize(params) 
        header = create_message_header(service_id="709", version="1.0")

        # 2. Communication: 전송
        broker_socket.connect("10.0.0.1", 8080)
        broker_socket.send(header + byte_stream)

        # 3. Unmarshalling: 역직렬화 (수신 시)
        response_data = broker_socket.receive()
        result = deserialize(response_data)
        return result
```

> **📢 섹션 요약 비유**
> 브로커 패턴의 작동은 **'국제 택배 배송 시스템'**과 같습니다. 고객(Client)이 물건을 포장(Marshalling)하여 집에 앉아 택배 회사(Broker)에 맡깁니다. 고객은 트럭이 어떤 경로로 가고, 허브 터미널을 거쳐 어느 배송 기사(Server Proxy)에게 전달되는지 알 필요가 없습니다. 오직 운송장 번호(ID)만 있으면 택배 회사가 알아서 분류(Routing)하고, 수신자 주소에 맞게 배송하여 최종적으로 서명을 받고 결과를 고객에게 알려줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 유사 아키텍처 패턴 심층 비교
브로커 패턴은 다른 분산 패턴과 명확히 구분되어야 합니다. 특히 **Mediator** 패턴과의 혼동을 피해야 합니다.

| 비교 항목 | **Broker Pattern (브로커)** | **Mediator Pattern (중재자)** | **Peer-to-Peer (P2P)** |
|:---|:---|:---|:---|
| **통신 범위** | **분산 시스템 (Distributed)**<br>네트워크를 경유하는 별도의 프로세스/서버 간 통신 | **단일 애플리케이션 (Monolithic)**<br>같은 메모리 공간 내 객체(Object) 간 통신 | **분산 시스템**<br>고정된 트래픽 없이 노드 간 직접 통신 |
| **목적** | **위치 투명성** 및 원격 호출 지원 | **복잡한 상호작용(Logic)**의 단순화 및 decoupling | **중앙화된 서버 없는** 자원 공유 |
| **구조** | Heavyweight, 미들웨어/인프라 수준 | Lightweight, 디자인 패턴 수준 | Overlay Network 수준 |
| **결합도** | 비동기적/동기적 통신 모두 가능하나 인프라 의존도 높음 | 로직 중심 의존도 제거 | 각 노드가 서로 발견해야 하는 복잡성 존재 |
| **대표 예시** | CORBA, MSA API Gateway, Kafka | UI Widget Controller, Golang Mediator | BitTorrent, 블록체인 네트워크 |

#### 2. 타 과목 융합 관점 (OS/네트워크)
- **OS (Operating System)와의 관계**: 브로커는 사용자 레벨(User-level) 서버로 동작하며, **IPC (Inter-Process Communication)**나 **RPC (Remote Procedure Call)** 메커니즘을 활용합니다. 커널 레벨의 통신 기능을 추상화하여 애플리케이션에게 제공합니다.
- **네트워크와의 관계**: OSI 7계층의 **응용 계층(Application Layer)**이나 **세션 계층(Session Layer)**의 기능을 수행합니다. 브로커는 **TCP/IP** 소켓 위에서 동작하며, 로드 밸런싱(계층 4/7)을 통해 트래픽을 분산시킵니다.
- **DB와의 관계**: 분산 데이터베이스 환경에서 브로커는 **질의(Query) 라우터** 역할을 하여, 읽기 요청을 복제본(Replica)으로 보내고 쓰기 요청을 마스터(Master)로 보내는 **Router-Proxy** 패턴에 활용됩니다.

```text
      [Decoupling Degree] 분석 비교

High Coupling ────────────────────────────────────────────────────▶ Low Coupling

    Direct Call                 Proxy (Broker)                  Event-Driven
  (Hardcoded Link)         (Decoupled Location)            (Decoupled Time)

    [Client] ══════▶ [Server]    [Client] ──▶ [Broker] ──▶ [Server]   [Pub] ──▶ [Event]
      (Same)                      (Diff Process)                     (Sub)

    * Broker는 "공간적(Spatial)" 디커플링 해결
    * Message Queue는 "시간적(Temporal)" 디커플링 추가 해결
```

> **📢 섹션 요약 비유