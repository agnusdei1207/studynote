+++
title = "프록시 서버 (Proxy Server)"
date = 2025-03-03
[extra]
categories = "studynotes-03_network"
tags = ["프록시", "포워드프록시", "리버스프록시", "투명프록시", "캐싱", "익명성", "보안"]
+++

# 프록시 서버 아키텍처 및 메커니즘 (Proxy Server)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프록시 서버(Proxy Server)는 클라이언트와 엔드포인트 서버 사이의 L7(Application Layer)에서 트래픽을 중계(Intermediation)하며, 요청/응답 패킷의 페이로드를 검사, 변조, 캐싱할 수 있는 능동적 네트워크 게이트웨이입니다.
> 2. **가치**: 포워드 프록시를 통한 사내 망 보안 및 아웃바운드 통제, 리버스 프록시를 통한 부하 분산(Load Balancing), SSL 오프로딩, 정적 자원 캐싱을 통해 전사적 IT 인프라의 보안성과 응답 지연 시간(Latency)을 획기적으로 개선합니다.
> 3. **융합**: 과거의 단순 캐싱 서버에서 진화하여, 최근에는 쿠버네티스(Kubernetes) 환경의 인그레스(Ingress) 게이트웨이나 서비스 메시(Service Mesh)를 위한 사이드카(Sidecar) 프록시(Envoy 등)로 마이크로서비스 통신 제어의 핵심을 담당합니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 
프록시 서버(Proxy Server)는 "대리인"이라는 뜻의 Proxy에서 유래한 용어로, 네트워크상에서 클라이언트의 요청을 받아 목적지 서버로 대신 전달하고, 서버의 응답을 받아 다시 클라이언트에게 전달하는 중간 중계 시스템입니다. 프록시는 단순히 패킷을 라우팅하는 L3 라우터와 달리, TCP 연결을 직접 맺고 끊으며(Terminating) HTTP 등 애플리케이션 계층 프로토콜의 헤더와 바디를 해독할 수 있어 세밀한 접근 제어와 콘텐츠 변환을 수행할 수 있습니다. 배치 위치와 목적에 따라 내부망을 보호하는 '포워드 프록시(Forward Proxy)'와 외부망으로부터 내부 서버군을 보호하는 '리버스 프록시(Reverse Proxy)'로 엄격히 구분됩니다.

- **💡 비유**: 
프록시 서버는 군사 기지의 **"위병소 및 우편물 검열소"**와 같습니다.
기지 안의 병사(클라이언트)가 밖으로 편지를 보낼 때, 위병소(포워드 프록시)에서 위험한 내용은 없는지 검사하고, 부대 주소로 바꿔서(익명성) 내보냅니다. 반대로 밖에서 기지 안의 장군(서버)에게 소포가 올 때도, 위병소(리버스 프록시)에서 폭발물이 있는지 먼저 검사하고(보안), 장군이 너무 바쁘면 이미 복사해 둔 안내문(캐시)을 대신 돌려보내 주며 장군의 업무 부담을 줄여줍니다.

- **등장 배경 및 발전 과정**:
  1. **초창기 대역폭 부족과 캐싱의 필요성**: 1990년대 초반, 전용선 대역폭이 극도로 제한적이고 비쌌던 시절, 여러 직원이 동일한 외부 웹사이트를 접속할 때 발생하는 중복 트래픽을 줄이기 위해 Squid와 같은 캐싱 프록시가 도입되었습니다. 
  2. **IPv4 주소 고갈 및 사설망 보안 대두**: NAT(Network Address Translation) 기술과 함께, 외부로 노출되지 않는 사설 IP 대역의 클라이언트들이 안전하게 인터넷에 접근하면서도 악성 사이트 접속을 차단하기 위한 중앙 통제점(Choke Point)으로서 포워드 프록시가 필수 인프라로 자리 잡았습니다.
  3. **대규모 웹 서비스의 등장과 리버스 프록시의 진화**: 단일 서버로 처리할 수 없는 대량의 트래픽(C10K Problem)을 감당하기 위해, 서버 앞단에서 트래픽을 분배하고 무거운 암호화(SSL/TLS) 연산을 대신 처리해주는 Nginx, HAProxy 같은 고성능 리버스 프록시가 클라우드 아키텍처의 표준이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

- **구성 요소 (표)**:

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|----------|----------|------|------|------|
| **Connection Manager** | 클라이언트/서버 TCP 커넥션 관리 | 비동기 I/O(epoll, kqueue)를 통해 수만 개의 동시 접속 소켓을 Non-blocking 방식으로 유지 및 해제합니다. | TCP Handshake, Keep-Alive | 우체국 접수 창구 |
| **Request Parser / Router** | HTTP 헤더 파싱 및 라우팅 | 수신된 요청의 Host 헤더나 URI 패스를 정규식으로 분석하여 어느 백엔드 서버 그룹(Upstream)으로 보낼지 결정합니다. | HTTP/1.1, HTTP/2 | 우편물 주소 자동 분류기 |
| **Cache Engine** | 정적 리소스 로컬 저장 | 백엔드 서버의 응답 중 Cache-Control 헤더가 허용하는 항목을 메모리나 디스크에 저장(LRU 알고리즘)하여 다음 요청 시 즉시 반환합니다. | B-Tree Index (디스크 캐시용) | 자주 찾는 문서 복사본 창고 |
| **SSL/TLS Terminator** | 암복호화 연산 오프로딩 | 클라이언트와는 HTTPS로 암호화 통신을 하고, 프록시 내부망을 거쳐 백엔드 서버와는 평문(HTTP)으로 통신하여 서버의 CPU 부하를 없앱니다. | TLS 1.3, OpenSSL | 비밀 편지 해독소 |
| **WAF / ACL Module** | 트래픽 필터링 및 보안 통제 | 출발지 IP, User-Agent, XSS/SQLi 패턴 등을 분석하여 악성 페이로드를 차단(Drop)하거나 403 Forbidden 응답을 반환합니다. | Regular Expression, ModSecurity | 금지 물품 X-ray 검사대 |

- **정교한 구조 다이어그램 (리버스 프록시 및 포워드 프록시 하이브리드 토폴로지)**:

```text
===================================================================================================
                                [ Enterprise Proxy Server Architecture ]
===================================================================================================
[ Internal Corporate Network ]                                         [ Public Internet ]
                                         +----------------+
+---------------+                        | Forward Proxy  | ACL Check   +---------------+
| Employee PC 1 | --(GET example.com)--> | (Squid, Zscaler| ----------> | example.com   |
+---------------+                        | * Caching      |             | (Web Server)  |
+---------------+                        | * Content/URL  |             +---------------+
| Employee PC 2 | --(Blocked Site)-----> |   Filtering    | --(DROP)--> [ Malicious Site ]
+---------------+                        +----------------+
(Private IP: 10.x.x.x)                  (NAT & Proxy IP Masking)

===================================================================================================
[ Public Internet ]                                              [ Internal Data Center / VPC ]
                                         
+---------------+       [ HTTPS: 443 ]   +----------------+  [ HTTP: 80 ]   +-----------------+
| Mobile Client | =====(Encrypted)======>| Reverse Proxy  | ----------------> | Backend API #1  |
+---------------+                        | (Nginx, Envoy) | (Decrypted)     +-----------------+
+---------------+                        |================|
| Web Browser   | =====(Encrypted)======>| * SSL Offload  | ----------------> | Backend API #2  |
+---------------+                        | * Load Balance |                 +-----------------+
                                         | * WAF / Cache  | (Static Asset)  +-----------------+
                                         +----------------+ - - - - - - - > | Local Disk/Mem  |
                                                |                           +-----------------+
                                                +---(Logs)--> [ ELK Stack / Splunk ]
===================================================================================================
```

- **심층 동작 원리 (리버스 프록시의 요청 처리 5단계 파이프라인)**:

1. **Connection Accept & TLS Handshake**: 클라이언트가 프록시의 443 포트로 TCP SYN을 보내면 프록시가 수락합니다. 프록시에 인증서가 탑재되어 있으므로 서버를 대신하여 TLS Handshake를 수행하고 대칭키를 교환합니다.
2. **Request Parsing & ACL Check**: 복호화된 HTTP 메시지의 첫 줄(Method, URI)과 헤더(Host, Cookie 등) 파싱합니다. 접속 차단 IP 목록(Blacklist)에 있는지, Rate Limit(초당 요청 수 제한)을 초과했는지 검사합니다.
3. **Cache Lookup**: `GET` 요청의 경우 URI를 해시(Hash) 키로 변환하여 메모리/디스크 캐시에 유효한(TTL이 남은) 응답이 있는지 확인합니다. 캐시 히트(Hit) 시 5단계로 바로 점프합니다.
4. **Upstream Routing & Proxy Pass**: 캐시 미스(Miss) 시, 로드 밸런싱 알고리즘(Round Robin, Least Connection, IP Hash 등)에 따라 최적의 백엔드 서버를 선택합니다. 이때 `X-Forwarded-For` 헤더에 클라이언트의 실제 IP를 추가하여 백엔드 서버로 HTTP 요청을 포워딩합니다.
5. **Response Return & Cache Store**: 백엔드 서버로부터 응답을 받으면 프록시가 클라이언트에게 전달합니다. 응답 헤더에 `Cache-Control: max-age=3600` 등이 있다면 캐시 스토리지에 응답 페이로드를 저장합니다.

- **핵심 알고리즘 & 실무 코드 예시 (Nginx Reverse Proxy & Load Balancing Configuration)**:

```nginx
# nginx.conf: 리버스 프록시 및 로드 밸런싱 실무 설정 예시

# 1. 백엔드 서버 그룹 정의 (Upstream) 및 로드 밸런싱 알고리즘 설정
upstream backend_api_cluster {
    least_conn; # 가장 연결 수가 적은 서버로 트래픽을 보내는 알고리즘
    server 192.168.1.101:8080 max_fails=3 fail_timeout=30s; # 장애 발생 시 30초간 제외
    server 192.168.1.102:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.103:8080 backup; # 앞의 서버들이 모두 죽었을 때만 동작하는 예비 서버
}

# 2. 캐시 스토리지 정의
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m use_temp_path=off;

server {
    listen 443 ssl http2;
    server_name api.mycompany.com;

    # 3. SSL Termination 설정
    ssl_certificate     /etc/nginx/ssl/api.crt;
    ssl_certificate_key /etc/nginx/ssl/api.key;
    ssl_protocols       TLSv1.2 TLSv1.3;

    location / {
        # 4. Proxy Pass 및 헤더 조작
        proxy_pass http://backend_api_cluster;
        proxy_http_version 1.1; # Keepalive 유지를 위해 1.1 사용
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr; # 클라이언트의 진짜 IP를 백엔드에 전달
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Connection ""; # 백엔드와의 연결을 닫지 않고 재사용

        # 5. 캐시 적용 정책
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m; # 정상 응답은 10분간 캐싱
        proxy_cache_valid 404      1m; # 404 에러는 1분만 캐싱 (DDoS 방어 목적)
        proxy_cache_use_stale error timeout http_500 http_502; # 백엔드 장애 시 과거 캐시된 데이터라도 반환 (가용성 확보)
    }
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

- **심층 기술 비교 (Forward Proxy vs Reverse Proxy vs L4 Load Balancer)**:

| 비교 지표 | 포워드 프록시 (Forward Proxy) | 리버스 프록시 (Reverse Proxy) | L4 스위치 / 로드 밸런서 |
|----------|-------------------------------|-------------------------------|-------------------------|
| **대상의 캡슐화** | **클라이언트를 숨김** (서버는 프록시 IP만 알게 됨) | **서버를 숨김** (클라이언트는 프록시 IP만 알게 됨) | IP/Port 수준의 트래픽 분산 (내용 모름) |
| **주요 목적** | 아웃바운드 접근 제어, 익명성 보장, 대역폭 절감 | 인바운드 보안(WAF), SSL 오프로딩, 캐싱 가속 | 대용량 트래픽의 고속 네트워크 라우팅 |
| **설치 위치** | 사내 네트워크의 출구 (Egress Point) | 데이터센터/클라우드의 입구 (Ingress Point) | 네트워크의 입구 (라우터 직하단) |
| **처리 계층** | L7 (Application Layer - HTTP, FTP 등) | L7 (Application Layer) | L4 (Transport Layer - TCP/UDP) |
| **대표 솔루션** | Squid, Zscaler, 블루코트 | Nginx, HAProxy, Apache | F5 BIG-IP, AWS NLB, LVS |

- **과목 융합 관점 분석**:
  1. **[보안 융합] 제로 트러스트(Zero Trust)와 IAP(Identity-Aware Proxy)**: 전통적인 프록시가 네트워크 경계(Boundary) 방어에 머물렀다면, 최신 보안 아키텍처에서는 구글의 BeyondCorp와 같이 프록시 자체가 사용자의 신원(Identity)과 디바이스의 상태를 매 요청마다 검증하는 IAP로 진화하여 제로 트러스트 보안의 핵심 정책 집행 지점(PEP, Policy Enforcement Point) 역할을 수행합니다.
  2. **[운영체제 융합] Socket I/O 최적화**: 고성능 프록시(Nginx 등)는 OS의 커널 영역과 유저 영역 간의 빈번한 컨텍스트 스위칭을 피하기 위해, 다중 스레드/프로세스를 생성하는 방식(Apache HTTPD 방식) 대신 싱글 스레드 기반의 이벤트 드리븐(Event-Driven) 아키텍처와 `epoll`(Linux) / `kqueue`(FreeBSD) 시스템 콜을 결합하여 메모리 풋프린트를 극소화하고 수만 개의 동시 연결을 C10K 문제 없이 처리합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **기술사적 판단 (실무 시나리오)**:
  1. **MSA(Microservices Architecture)로의 전환과 API Gateway 도입**:
     - **상황**: 모놀리식(Monolithic) 시스템을 수십 개의 마이크로서비스로 분리하자, 클라이언트가 각 서비스의 IP와 포트를 모두 알아야 하고, 인증/인가 로직이 서비스마다 파편화되는 문제 발생.
     - **판단**: 모든 외부 요청을 단일 진입점에서 받아 라우팅하는 고도화된 리버스 프록시 형태인 **API 게이트웨이(Kong, AWS API Gateway 등)**를 전면에 배치합니다. 이 프록시 레이어에서 JWT 토큰 검증, Rate Limiting, CORS 처리 등 횡단 관심사(Cross-cutting Concerns)를 일괄 처리하여 백엔드 개발 생산성을 극대화합니다.
  2. **글로벌 서비스의 지연 시간(Latency) 이슈 극복**:
     - **상황**: 한국에 메인 서버가 있는 서비스에 북미/유럽 사용자가 접속할 때, 대양을 건너는 RTT(Round Trip Time)가 200ms 이상 발생하여 웹페이지 렌더링이 심각하게 지연됨.
     - **판단**: 전 세계 엣지 네트워크에 분산 배치된 대규모 리버스 프록시 네트워크인 **CDN(Content Delivery Network, 예: Cloudflare, Akamai)**을 도입합니다. 정적 이미지와 JS/CSS 파일은 클라이언트와 가장 가까운 엣지 프록시에서 즉시 캐시 응답을 주고, 동적 API 요청만 한국의 오리진 서버로 전달되도록 캐시 정책을 세밀하게 분리합니다.
  3. **내부망에서의 무분별한 외부 SaaS 통제 (Shadow IT 방어)**:
     - **상황**: 기업 내 임직원들이 보안 부서의 승인 없이 외부 퍼블릭 클라우드 스토리지(DropBox 등)에 사내 기밀 문서를 무단으로 업로드하는 데이터 유출 리스크 발생.
     - **판단**: 포워드 프록시에 SSL 가시성(SSL Visibility) 기능을 적용합니다. 사내 PC에 사설 루트 인증서를 배포하여 프록시가 HTTPS 트래픽을 중간에서 복호화(MITM 방식으로 합법적 감청)하고, DLP(Data Loss Prevention) 솔루션과 연동하여 기밀문서의 외부 유출 시도를 원천 차단하는 SWG(Secure Web Gateway) 아키텍처를 구축합니다.

- **도입 시 고려사항 (체크리스트)**:
  - **기술적**: 클라이언트의 원본 IP 식별 문제. 리버스 프록시를 거치면 백엔드 서버의 로그에는 모두 프록시의 IP가 남게 됩니다. 반드시 프록시 설정에서 `X-Forwarded-For` 헤더를 삽입하고, 백엔드 서버(Tomcat, Spring 등)에서는 이 헤더를 파싱하여 진짜 IP를 로깅하도록 프레임워크 설정을 변경해야 합니다.
  - **운영적**: 프록시 서버 자체가 단일 장애점(SPOF, Single Point of Failure)이 될 수 있습니다. 따라서 프록시 서버 이중화를 위해 앞단에 L4 스위치를 두거나, Keepalived(VRRP)를 활용한 Active-Standby HA 구성을 반드시 병행해야 합니다.

- **주의사항 및 안티패턴 (Anti-patterns)**:
  - **과도한 캐시 TTL 설정**: 동적 데이터(예: 주식 가격, 실시간 재고)에 실수로 캐시 정책을 적용하거나 TTL(Time To Live)을 길게 잡으면, 수많은 사용자에게 과거의 잘못된 데이터가 서빙되는 치명적인 데이터 정합성 장애가 발생합니다. URI 경로에 따른 정밀한 캐시 예외(Bypass) 처리가 필수입니다.
  - **Proxy Chain 지연**: 프록시가 여러 단계로 중첩되는 프록시 체이닝(Proxy Chaining)은 보안을 강화할 수 있으나, 각 홉(Hop)마다 패킷 파싱과 지연이 누적되어 전반적인 서비스 품질을 급락시킵니다. 불필요한 프록시 계층은 통폐합해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량적/정성적 기대효과**:

| 효과 영역 | 내용 | 정량적 목표 / 지표 |
|---------|-----|-----------|
| **인프라 비용** | 정적 콘텐츠 프록시 캐싱을 통한 백엔드 서버 증설 비용 절감 | 백엔드 서버 트래픽 60~80% 감소 (Offload Ratio) |
| **성능 최적화** | TLS 터미네이션을 통한 백엔드 CPU 여유 확보 및 커넥션 풀 최적화 | API 응답 시간(Latency) 30% 개선 |
| **보안 강화** | 악의적 트래픽(DDoS, 스캐닝)의 백엔드 도달 전 사전 차단 | 웹 해킹 공격 차단율 99% 달성 |

- **미래 전망 및 진화 방향**:
  현대의 프록시는 단순한 L7 라우팅을 넘어 클라우드 네이티브 생태계의 신경망으로 진화했습니다. 컨테이너 오케스트레이션(Kubernetes) 환경에서는 각 애플리케이션 파드(Pod) 내에 초경량 프록시(Envoy Proxy 등)를 사이드카(Sidecar) 패턴으로 주입하여, 서비스 간의 상호 통신(East-West 트래픽)을 제어하고, mTLS 인증, 트래픽 섀도잉, 서킷 브레이커(Circuit Breaker)를 구현하는 **서비스 메시(Service Mesh, Istio 등)** 아키텍처가 업계 표준으로 확고히 자리잡고 있습니다. 또한 eBPF(Extended Berkeley Packet Filter) 기술과 결합하여 커널 레벨에서 프록시 기능을 수행해 오버헤드를 제로에 가깝게 만드는 기술 혁신이 진행 중입니다.

- **※ 참고 표준/가이드**: 
  - RFC 7230 (HTTP/1.1 Message Syntax and Routing)
  - RFC 7234 (HTTP/1.1 Caching)
  - RFC 6648 (The "X-Forwarded-For" 헤더 표준화 규격)

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[로드 밸런싱 (Load Balancing)](@/studynotes/03_network/01_network_fundamentals/_index.md)**: 리버스 프록시가 제공하는 핵심 기능으로, 트래픽을 여러 백엔드 서버로 고르게 분산하는 기법.
- **[CDN (Content Delivery Network)](@/studynotes/03_network/_index.md)**: 전 세계 단위로 엣지 로케이션에 분산 배치된 거대한 리버스 캐싱 프록시 네트워크.
- **[MSA (Microservices Architecture)](@/studynotes/04_software_engineering/01_sdlc_methodology/msa.md)**: API 게이트웨이 및 서비스 메시(사이드카 프록시) 아키텍처를 강제하게 만든 소프트웨어 설계 패러다임.
- **[방화벽 및 WAF (Web Application Firewall)](@/studynotes/03_network/01_network_fundamentals/_index.md)**: 프록시 레이어에 통합되어 애플리케이션 계층의 악의적 페이로드를 차단하는 보안 기술.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **프록시 서버**는 여러분을 대신해 심부름을 해주는 똑똑한 **'비서'** 같아요.
2. 내가 위험한 동네에 직접 가서 물건(데이터)을 사오는 대신, 비서(포워드 프록시)에게 부탁하면 나를 안전하게 숨긴 채 물건을 사다 주죠.
3. 반대로 내가 유명한 떡볶이집 사장님이라면, 수백 명의 손님이 한꺼번에 주방으로 들이닥치지 않게, 가게 앞에 매니저(리버스 프록시)를 세워두고 주문을 나눠 받게 하면 가게가 엉망이 되지 않는답니다!
