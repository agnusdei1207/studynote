+++
title = "506-510. 콘텐츠 전송 및 스트리밍 기술 (CDN, GSLB, DASH)"
date = "2026-03-14"
[extra]
category = "Application Layer"
id = 506
+++

# 506-510. 콘텐츠 전송 및 스트리밍 기술 (CDN, GSLB, DASH)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지리적 분산(CDN)과 글로벌 라우팅(GSLB)을 통해 콘텐츠 전송 거리를 물리적으로 단축하고, HTTP 기반의 세분화된 청크(DASH) 전송으로 네트워크 변동성을 극복하는 고차원의 성능 최적화 아키텍처.
> 2. **가치**: **Origin Server (원본 서버)**의 트래픽 부하를 약 90% 이상 절감하여 TCO(Total Cost of Ownership)를 낮추고, **Latency (지연 시간)**를 20ms 이내로 최적화하여 이탈률을 획기적으로 개선함.
> 3. **융합**: **OS**(캐싱 알고리즘), **Network**(DNS 라우팅, BGP Anycast), **Compression**(코덱 효율화) 기술이 집약된 인터넷 인프라의 핵심 노하우.

---

### Ⅰ. 개요 (Context & Background)

**CDN (Content Delivery Network)**은 단순한 캐싱 서버 그룹이 아닌, 인터넷의 폭주하는 트래픽을 제어하기 위한 물리적 계층의 혁신입니다. 과거의 **C/S (Client/Server)** 모델은 모든 요청이 중앙 집중식 서버로 향하게 하여, 인기 있는 콘텐츠일수록 회선 병목과 서버 다운(Single Point of Failure)을 유발했습니다. 이를 해결하기 위해 콘텐츠를 사용자의 **Edge (가장자리)**로 물리적으로 이동시키는 분산 컴퓨팅 패러다임이 등장했습니다.

여기에 더해 **GSLB (Global Server Load Balancing)** 기술은 DNS (Domain Name System) 질의 단계에서 사용자의 위치와 서버의 건강 상태를 판단하여, 최적의 **PoP (Point of Presence)**를 연결해 줍니다. 마지막으로 **DASH (Dynamic Adaptive Streaming over HTTP)**는 인터넷이라는 불안정한 회선 위에서 영상이 끊기지 않도록 화질을 실시간으로 조절하는 애플리케이션 계층의 지능입니다.

```ascii
[인터넷 트래픽 패러다임 변천]

(과거: 중앙 집중형)            (현재: 분산형 CDN)
┌─────────────┐              ┌───────────────┐
│    User     │              │  User (Global)│
└──────┬──────┘              └───────┬───────┘
       │                             │
       │ (모든 요청)                  │
       v                             v
┌─────────────┐         ┌─────────────────────────┐
│   Origin    │ <────── │        GSLB (DNS)       │
│   Server    │         └─────────────┬───────────┘
└─────────────┘                       │
        (병목 발생)       ┌────────────┼────────────┐
                         v            v            v
                     ┌────────┐  ┌────────┐  ┌────────┐
                     │Edge KR │  │Edge US │  │Edge JP │
                     └────────┘  └────────┘  └────────┘
```

위 다이어그램과 같이, 기존에는 사용자가 직접 원본 서버에 접속하여 거리에 따른 지연(Latency)이 필연적이었으나, CDN 아키텍처에서는 사용자가 가장 가까운 '거점'에 접속함으로써 물리적 지연을 최소화합니다. 이는 전 세계적인 서비스 제공을 가능하게 하는 인프라의 핵심입니다.

> **💡 개념 비유**: **CDN**은 전 세계에 물류 센터를 지어놓고 상품을 미리 배치해두는 것입니다. **GSLB**는 고객이 주문을 넣었을 때, GPS를 보고 가장 가깝고 재고가 있는 물류 센터에서 자동으로 출고하도록 지시하는 전략 통제실입니다.

📢 **섹션 요약 비유**: 마치 도심에 하나밖에 없는 대형 마트보다, 동네마다 편의점 체인점을 둬서 굳이 멀리 갈 필요 없이 가장 가까운 곳에서 바로 물건을 받아 쓰는 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

본 장에서는 콘텐츠 전송의 핵심이 되는 CDN의 내부 아키텍처와 GSLB의 라우팅 로직, 그리고 DASH의 스트리밍 메커니즘을 기술적으로 분석합니다.

#### 1. CDN 및 GSLB 아키텍처

CDN은 **PoP (Point of Presence)**라고 불리는 에지 서버들의 연결망이며, GSLB는 이들을 통제하는 뇌와 같습니다.

**구성 요소 상세 분석**

| 요소 (Component) | 전체 명칭 (Full Name) | 핵심 역할 (Role) | 내부 동작 (Mechanism) | 관련 프로토콜 (Protocol) |
|:---:|:---|:---|:---|:---|
| **Origin** | Origin Server | 콘텐츠의 원천 소스 저장 | 에지 서버에 캐시가 없을 시 최초 제공 (Source of Truth) | HTTP/HTTPS |
| **Edge** | Edge Server | 사용자에게 직접 전달 | **Hit Rate**를 높이기 위해 콘텐츠를 캐싱 및 처리 | HTTP, TLS |
| **GSLB** | Global Server Load Balancer | 전역 라우팅 결정 | **RTT (Round Trip Time)**, 서버 부하, 지리적 위치 기반으로 IP 반환 | DNS (UDP/53) |
| **ICP** | Internet Content Provider | 고객(서비스 운영자) | 콘텐츠 관리 및 트래픽 비용 지불 | Portal/API |
| **Purge** | Cache Invalidation | 캐시 무효화 | 원본 변경 시 에지 캐시 삭제 요청 전파 | API Call |

**동작 과정 (Data Flow)**

1.  **DNS 질의 (Request)**: 사용자가 `www.example.com` 접속 시, **Local DNS Server**는 도메인 소유자의 **GSLB**로 질의를 전송합니다.
2.  **라우팅 결정 (Resolution)**: GSLB는 사용자의 **LDNS IP**를 보고 지리적 위치를 파악하고, 각 PoP의 실시간 부하(Load)와 회선 상태를 고려하여 최적의 **Edge IP**를 반환합니다.
3.  **콘텐츠 전송 (Delivery)**: 사용자는 반환된 Edge IP에 접속. Edge에 콘텐츠가 있으면 즉시 전송(**Cache Hit**), 없으면 **Origin**에서 가져와 사용자에게 전송 후 저장(**Cache Miss**).

```ascii
[CDN & GSLB 상세 동작 시퀀스]

User PC                    Local DNS                  GSLB                 Edge PoP             Origin
  │                            │                          │                    │                   │
  ├─── query: video.com ───────>│                          │                    │                   │
  │                            ├─── recursive query ──────>│                    │                   │
  │                            │                          ├─── (Check Load) ───>│                   │
  │                            │                          │<─── (Status: OK) ──┤                   │
  │                            │<─── A: 203.0.113.5 ──────┤                    │                   │
  │<─── A: 203.0.113.5 ─────────┤                          │                    │                   │
  │                            │                          │                    │                   │
  ├─── GET /video.mp4 ──────────────────────────────────────────────────────────>│                   │
  │                            │                          │                    │                   │
  │                            │                          │                    ├─── MISS ──────────>│
  │                            │                          │                    │<─── Content ───────┤
  │<────── (Video Chunk 1) ─────────────────────────────────────────────────────┤                   │
  │                            │                          │                    │                   │
```

위 시퀀스 다이어그램은 사용자의 요청이 GSLB를 거쳐 최적의 엣지 서버로 라우팅되는 과정을 보여줍니다. 이때 GSLB는 단순히 가까운 서버가 아니라, **Active-Active** 구조에서 서버의 살아있음(Health)을 확인하여 장애 복구 능력도 갖춥니다.

#### 2. DASH (Dynamic Adaptive Streaming over HTTP) 원리

**DASH**는 영상을 작은 단위인 **Segment**로 쪼개어, 각각을 다른 비트레이트(Bitrate)로 인코딩합니다. 클라이언트 플레이어는 네트워크 상황에 따라 다음 세그먼트를 어떤 화질로 요청할지 결정합니다.

**핵심 메커니즘**
- **MPD (Media Presentation Description)**: 영상의 구조, 인코딩 정보, 세그먼트 URL 등이 담긴 매니페스트 파일입니다.
- **Segment**: 실제 영상 데이터 조각 (보통 2~10초 길이).
- **ABR (Adaptive Bitrate)**: 대역폭이 넓으면 고화질(1080p), 좁으면 저화질(480p)로 동적으로 전환합니다.

```ascii
[DASH ABR(적응형 비트레이트) 로직]

Time ──────────────────────────────────────────────>
     ┃       [Bandwidth High]      [Bandwidth Low]
     ┃            │                      │
     │            │                      │
     ▼            ▼                      ▼
Buffer |==========|======================|==========>
       Segment 1   Segment 2              Segment 3
       (4K/60fps)  (1080p/30fps)         (720p/30fps)
       
       > 화질 전환 (Switching Point)
```

**실무 코드 예시 (MPD 구조 예시)**
```xml
<!-- MPD 파일은 단순 텍스트 기반의 메타데이터이므로 HTTP 전송에 최적화됨 -->
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">
  <Period>
    <AdaptationSet mimeType="video/mp4">
      <!-- 높은 화질 -->
      <Representation id="1" bandwidth="8000000" width="3840" height="2160"/>
      <!-- 중간 화질 -->
      <Representation id="2" bandwidth="4000000" width="1920" height="1080"/>
      <!-- 낮은 화질 -->
      <Representation id="3" bandwidth="1000000" width="1280" height="720"/>
    </AdaptationSet>
  </Period>
</MPD>
```
클라이언트는 이 XML을 파싱하여 현재 **TCP Throughput (처리량)**을 측정하고, `id="3"` 대신 `id="1"`을 요청할지 결정합니다.

📢 **섹션 요약 비유**: 고속도로에서 차가 막히면 지도 앱이 자동으로 우회 도로(저화질)로 경로를 변경해주는 것과 같습니다. 운전자(사용자)는 그저 운전만 하면 되고, 경로 변경(화질 변경)은 시스템이 자동으로 처리합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 전통적 다운로드 vs 스트리밍 (DASH)

| 구분 | 전통적 다운로드 (Progressive Download) | DASH (Adaptive Streaming) |
|:---|:---|:---|
| **전송 방식** | 순차적 다운로드 (재생과 병행) | HTTP 청크(Chunk) 기반 요청 |
| **대응력** | 네트워크 변동 시 **버퍼링(Buffering)** 발생 | **화질 변경(Switching)**으로 버퍼링 방지 |
| **네트워크** | **TCP** 혼잡 제어에 수동적 의존 | 애플리케이션 레벨에서 능동적 제어 |
| **서버 부하** | 연결 유지(Keep-alive) 길어짐 | 무상태(Stateless) HTTP 요청으로 확장성 유리 |
| **OS/플랫폼** | 플러그인(Flash 등) 필요 | 순수 웹 표준(HTML5 Video) 지원 |

#### 2. L4 Load Balancer vs GSLB

| 비교 항목 | L4 Load Balancer (Local LB) | GSLB (Global LB) |
|:---|:---|:---|
| **작동 계층** | OSI 4계층 (Transport Layer: IP/Port) | OSI 7계층 (Application Layer: DNS) |
| **범위** | **데이터센터 내부** 서버 간 부하 분산 | **전역(데이터센터 간)** 트래픽 분산 |
| **Health Check** | TCP 3-Way Handshake, HTTP Probe | ICMP, DNS Query, BGP Route Health |
| **합의 알고리즘** | Round Robin, Least Conn | Geo-location, RTT 측정, Weighted Round Robin |
| **네트워크 융합** | **Switching** 기술 (MAC/ARP 학습) | **Routing** 기술 (BGP Anycast 활용) |

**융합적 관점 (OS/Network)**
DASH 기술은 **OS**의 소켓 버퍼(Socket Buffer) 관리와 밀접합니다. TCP 윈도우 크기 조정(Tuning) 못지않게 애플리케이션 계층에서 요청 크기(Segment Size)를 제어하여 네트워크 혼잡을 피하는 **Network-aware Application**의 전형입니다.

📢 **섹션 요약 비유**: L4 스위치는 "건물 내부에서 3번 엘리베이터를 타세요"라고 안내하지만, GSLB는 "본사 건물이 붐비니 지사 건물로 가세요"라고 초기 진입로를 변경해주는 전략가입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

기술사는 단순히 기술을 아는 것을 넘어, 도입 시 발생하는 **Trade-off(상충 관계)**를 통제하고 문제를 해결해야 합니다.

#### 1. 실무 시나리오 및 의사결정

**시나리오 1: 글로벌 라이브 스포츠 중계 서비스 구축**
- **문제**: 전 세계 1억 명이 동시 접속하는 축구 경기 중계. 원본 서버는 한국에 위치.
- **의사결정**:
    1.  **CDN 도입**: 한국 원본 서버를 튕겨내지 않기 위해 **AWS CloudFront**나 **Akamai** 같은 글로벌 CDN을 필수 도입. (Origin Protection)
    2.  **DASH 적용**: 각 국가별 네트워크 환경이 다르므로 HLS(Apple용)와 DASH(Standard)를 멀티 코덱으로 준비.
    3.  **GSLB 튜닝**: 단순 거리 기반이 아닌, **RTT 기반 GSLB**