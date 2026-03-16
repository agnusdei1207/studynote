+++
title = "617. 서비스 디스커버리 (Service Discovery) Eureka"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 서비스 디스커버리 (Service Discovery) Eureka

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동적 환경에서 마이크로서비스의 네트워크 위치(IP:Port)를 자동으로 등록/검색하는 메커니즘
> 2. **가치**: 하드코딩된 주소 제거, 자동 확장/축소 지원, 장애 복구 → 가용성 99.99% 보장
> 3. **융합**: Client-side vs Server-side Discovery, Spring Cloud Eureka, Consul, Zookeeper 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**서비스 디스커버리 (Service Discovery)**는 분산 시스템에서 **마이크로서비스의 동적 네트워크 위치를 찾는 프로세스**입니다. 클라우드 네이티브 환경에서는 컨테이너/파드가 주기적으로 재시작되며 IP가 변경되므로, 정적 설정 파일로는 서비스 위치를 추적할 수 없습니다.

**Eureka**는 Netflix가 개발한 **Client-side Service Discovery** 서버로, 각 마이크로서비스가 자신의 위치를 등록(Register)하고, 다른 서비스의 위치를 조회(Fetch)하는 **중앙 레지스트리** 역할을 합니다. Spring Cloud Netflix Eureka로 널리 사용됩니다.

```
┌─────────────────────────────────────────────────────────────┐
│                   서비스 디스커버리 개념                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  문제: 컨테이너 재시작 시 IP 변경                           │
│  ┌──────────────┐  재시작  ┌──────────────┐                │
│  │Order Service│ ────────> │Order Service │                │
│  │  10.0.1.5    │          │  10.0.1.8    │  ❌ 주소 바뀜! │
│  └──────────────┘          └──────────────┘                │
│                                                             │
│  해결: Eureka 레지스트리                                    │
│  ┌─────────────────────────────────────────────┐           │
│  │          Eureka Server                      │           │
│  │  ┌─────────────────────────────────────┐    │           │
│  │  │ Service Registry                     │    │           │
│  │  │ - ORDER-SERVICE: [10.0.1.8, ...]    │    │           │
│  │  │ - PAYMENT-SERVICE: [10.0.2.3, ...]  │    │           │
│  │  │ - PRODUCT-SERVICE: [10.0.3.1, ...]  │    │           │
│  │  └─────────────────────────────────────┘    │           │
│  └─────────────────────────────────────────────┘           │
│           ▲                    │                           │
│           │ 등록                │ 조회                       │
│           │                    │                           │
│  ┌────────┴──────┐    ┌────────▼──────────┐                │
│  │Order Service  │    │Payment Service    │                │
│  │"내 위치 등록"  │    │"Order Service    │                │
│  │               │    │ 어디 있어?"       │                │
│  └───────────────┘    └───────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**쇼핑몰의 정보 데스크**와 같습니다. 각 상점(서비스)은 정보 데스크에 자신의 위치(매장 번호)를 등록합니다. 손님(클라이언트)은 정보 데스크에 "식당이 어디에 있나요?"라고 물어보면, 현재 영업 중인 식당들의 위치를 안내받을 수 있습니다. 상점이 이동하거나 새로 생겨도 정보 데스크만 업데이트하면 됩니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 정적 설정** | IP/Port를 설정 파일에 하드코딩 | **컨테이너 재시작 시 연결 실패** |
| **② Load Balancer** | L4 LB는 DNS 기반, 지연 시간 큼 | **동적 확장에 즉각 대응 불가** |
| **③ DNS-based SRV** | DNS 캐싱으로 업데이트 지연 | **TTL 설정에 따른 불일치 문제** |
| **④ Service Discovery** | 실시간 등록/갱신, Health Check | **클라우드 네이티브 표준** |

현재의 비즈니스 요구로서는 **오토스케일링, 롤링 업데이트, 멀티 리전 배포**가 필수적입니다.

### 📢 섹션 요약 비유

마치 **택시 호출 앱**과 같습니다. 승객(클라이언트)은 배차 센터(Eureka)에 "택시를 불러줘"라고 요청하면, 현재 근처에 있는 빈 택시(서비스)들의 위치를 실시간으로 안내받습니다. 택시가 이동하거나 새로운 택시가 추가되어도 배차 센터가 자동으로 정보를 업데이트합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기법 | 비유 |
|:---|:---|:---|:---|:---|
| **Eureka Server** | 중앙 레지스트리 | 서비스 등록/갱신/삭제 | REST API, Jersey | 정보 데스크 |
| **Eureka Client** | 서비스 인스턴스 | Heartbeat 전송, 레지스트리 캐싱 | HTTP 30초 간격 | 상점 점원 |
| **Eureka Server Peer** | 고가용성 클러스터 | 피어 간 레지스트리 복제 | P2P 복제 | 분산 정보 센터 |
| **Ribbon** | Client-side Load Balancer | 로드 밸런싱 알고리즘 | Round Robin, Weighted | 배차 담당자 |
| **Health Check** | 생존 확인 | 미연결 시 자동 등록 취소 | LastSeen 타임스탬프 | 생체 확인 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Eureka 서비스 디스커버리 아키텍처                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌──────────────────┐                                │
│                         │  Eureka Cluster  │                                │
│                         │  (High Availability)                             │
│                         │                   │                                │
│   ┌─────────────────────┼───────────────────┼─────────────────────┐        │
│   │                     │                   │                     │        │
│   ▼                     ▼                   ▼                     ▼        │
│ ┌───────┐           ┌───────┐           ┌───────┐           ┌───────┐      │
│ │Eureka │           │Eureka │           │Eureka │           │Eureka │      │
│ │Server │◄─────────►│Server │◄─────────►│Server │◄─────────►│Server │      │
│ │  #1   │  Peer     │  #2   │  Peer     │  #3   │  Peer     │  #N   │      │
│ │(8761) │  Awareness │(8762) │  Awareness │(8763) │  Awareness │(876N) │      │
│ └───┬───┘           └───┬───┘           └───┬───┘           └───┬───┘      │
│     │                   │                   │                   │         │
│     │Register           │                   │                   │         │
│     │Heartbeat (30s)    │                   │                   │         │
│     │                   │                   │                   │         │
│ ┌───▼───────────┐  ┌────▼───────────┐  ┌───▼───────────┐  ┌───▼───────┐  │
│ │Order Service  │  │Payment Service │  │Product Service│  │User Svc   │  │
│ │Instance #1    │  │Instance #1     │  │Instance #1     │  │Instance #1│  │
│ │(10.0.1.5:8080)│  │(10.0.2.3:8080) │  │(10.0.3.1:8080) │  │(10.0.4... │  │
│ │               │  │                │  │                │  │           │  │
│ │[Eureka Client]│  │[Eureka Client] │  │[Eureka Client] │  │[Eureka    │  │
│ │  - Register   │  │  - Register    │  │  - Register    │  │ Client]   │  │
│ │  - Renew      │  │  - Renew       │  │  - Renew       │  │           │  │
│ │  - Fetch      │  │  - Fetch       │  │  - Fetch       │  │           │  │
│ └───────┬───────┘  └────┬───────────┘  └────┬───────────┘  └───┬───────┘  │
│         │                │                   │                  │         │
│         │                │                   │                  │         │
│         │      ┌─────────▼───────────────────▼───────────┐      │         │
│         │      │         Service Registry (Cache)        │      │         │
│         │      │  ┌─────────────────────────────────────┐ │      │         │
│         │      │  │ ORDER-SERVICE                       │ │      │         │
│         │      │  │  - Instance #1: 10.0.1.5:8080       │ │      │         │
│         │      │  │  - Instance #2: 10.0.1.6:8080       │ │      │         │
│         │      │  │  - Status: UP                       │ │      │         │
│         │      │  ├─────────────────────────────────────┤ │      │         │
│         │      │  │ PAYMENT-SERVICE                     │ │      │         │
│         │      │  │  - Instance #1: 10.0.2.3:8080       │ │      │         │
│         │      │  │  - Status: UP                       │ │      │         │
│         │      │  ├─────────────────────────────────────┤ │      │         │
│         │      │  │ PRODUCT-SERVICE                     │ │      │         │
│         │      │  │  - Instance #1: 10.0.3.1:8080       │ │      │         │
│         │      │  │  - Status: UP                       │ │      │         │
│         │      │  └─────────────────────────────────────┘ │      │         │
│         │      └──────────────────────────────────────────┘      │         │
│         │                                                       │         │
│         │                  Discovery Request                   │         │
│         ▼                                                       │         │
│  ┌──────────────┐     ┌──────────────────┐                     │         │
│  │   Ribbon     │────►│  Load Balanced   │                     │         │
│  │ (LB Algorithm)│    │  HTTP Request    │◄────────────────────┘         │
│  │ Round Robin  │     └──────────────────┘                                │
│  └──────────────┘                                                          │
│                                                                             │
│  [동작 순서]                                                                │
│  1. 각 서비스 시작 시 Eureka Server에 자신의 정보 등록 (Register)          │
│  2. 30초마다 Heartbeat 전송으로 생존 신고 (Renew)                          │
│  3. Eureka Client는 레지스트리를 로컬에 캐싱 (30초 갱신)                  │
│  4. 90초 동안 Heartbeat 없으면 자동 등록 취소 (Eviction)                   │
│  5. 클라이언트는 Ribbon을 통해 로드 밸런싱하여 호출                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Eureka Server 클러스터**: 최소 3대 이상의 피어(Peer)로 구성하여 고가용성을 확보합니다. 각 서버는 다른 피어의 레지스트리를 복제하여 일관성을 유지합니다.

2. **서비스 등록 (Register)**: 각 마이크로서비스 인스턴스는 시작 시 자신의 **Instance ID**, **IP Address**, **Port**, **Status**를 Eureka Server에 등록합니다. Instance ID는 `${appname}:${hostname}:${port}` 형식입니다.

3. **Heartbeat (Renew)**: 30초마다 HTTP PUT `/eureka/apps/{appId}/{instanceId}` 요청으로 생존을 신고합니다. Eureka Server는 **LastSeenTimestamp**를 갱신합니다.

4. **캐싱 (Fetch)**: Eureka Client는 전체 레지스트리를 로컬에 캐싱하여, Eureka Server 장애 시에도 서비스 디스커버리가 가능합니다. 캐시는 30초마다 갱신됩니다.

5. **자동 등록 취소 (Eviction)**: 90초(기본값) 동안 Heartbeat가 없는 인스턴스는 **자동으로 레지스트리에서 제거**됩니다. 이는 **좀비 인스턴스** 문제를 방지합니다.

### 심층 동작 원리

```
① Eureka Server 기동
   └─> 포트 8761 리스닝
   └─> 피어 목록 로드 (eureka.client.serviceUrl.defaultZone)
   └─> 피어 간 레지스트리 동기화 시작

② Eureka Client 기동
   └─> Eureka Server에 POST /eureka/apps/{appId}
   └─> 인스턴스 메타데이터 전송
       {
         "instanceId": "order-service:10.0.1.5:8080",
         "hostName": "10.0.1.5",
         "app": "ORDER-SERVICE",
         "ipAddr": "10.0.1.5",
         "status": "UP",
         "port": {"$": 8080, "@enabled": true},
         "leaseInfo": {
           "renewalIntervalInSecs": 30,
           "durationInSecs": 90
         }
       }

③ Heartbeat 루프 (30초 간격)
   └─> PUT /eureka/apps/{appId}/{instanceId}
   └─> Eureka Server가 LastSeen 갱신

④ 레지스트리 조회 (30초 간격)
   └─> GET /eureka/apps
   └─> 전체 레지스트리를 로컬 캐시에 저장

⑤ 서비스 호출 시
   └─> Ribbon이 로컬 캐시에서 인스턴스 목록 조회
   └─> Round Robin 등의 알고리즘으로 인스턴스 선택
   └─> HTTP 요청 전송
```

### 핵심 알고리즘 & 코드

```java
// ============ Eureka Server 설정 (Spring Boot) ============

@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

/*
--- application.yml ---
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false  # 자기 자신은 등록 안 함
    fetch-registry: false        # 레지스트리를 가져오지 않음
    service-url:
      defaultZone: http://peer2:8762/eureka,http://peer3:8763/eureka

  server:
    enable-self-preservation: true    # 네트워크 장애 시 보호 모드
    renewal-percent-threshold: 0.85   # 85% 미만 갱신 시 보호
    eviction-interval-timer-in-ms: 60000  # 60초맄재 정리 실행

  instance:
    hostname: peer1
*/

// ============ Eureka Client 설정 (Spring Boot) ============

@SpringBootApplication
@EnableDiscoveryClient
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }

    @Bean
    @LoadBalanced  // Ribbon 활성화
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

/*
--- application.yml ---
spring:
  application:
    name: order-service

server:
  port: ${PORT:0}  # 랜덤 포트 (컨테이너 환경)

eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      defaultZone: http://eureka1:8761/eureka,http://eureka2:8762/eureka
    registry-fetch-interval-seconds: 30  # 캐시 갱신 주기

  instance:
    instance-id: ${spring.application.name}:${spring.application.instance_id:${random.value}}
    lease-renewal-interval-in-seconds: 30  # Heartbeat 주기
    lease-expiration-duration-in-seconds: 90  # 만료 시간
    prefer-ip-address: true
    metadata-map:
      zone: us-east-1
*/

// ============ Ribbon을 통한 서비스 호출 ============

@Service
public class OrderService {
    private final RestTemplate restTemplate;

    @Value("${payment-service.url:http://PAYMENT-SERVICE}")
    private String paymentServiceUrl;

    public PaymentResponse processPayment(OrderRequest order) {
        // http://PAYMENT-SERVICE/api/payments
        // PAYMENT-SERVICE는 Eureka에서 실제 IP로 변환됨
        return restTemplate.postForObject(
            paymentServiceUrl + "/api/payments",
            order,
            PaymentResponse.class
        );
    }
}

// ============ Health Check 커스터마이징 ============

@Component
public class CustomHealthCheck implements HealthIndicator {
    private final DatabaseConnector dbConnector;

    @Override
    public Health health() {
        if (dbConnector.isHealthy()) {
            return Health.up()
                .withDetail("database", "connected")
                .build();
        } else {
            // DB 연결 실패 시 Eureka에서 자동 등록 취소됨
            return Health.down()
                .withDetail("database", "disconnected")
                .build();
        }
    }
}

// ============ Eureka Server의 피어 인식 코드 ============

/*
Eureka Server는 다음과 같은 로직으로 피어 간 레지스트리를 동기화함:

1. 로컬 변경 발생 시 피어에게 전파 (Batch Replication)
2. 피어로부터 변경을 받으면 로컬 레지스트리에 병합
3. 네트워크 분할 시 자기 보호(Self-Preservation) 모드 활성화
   - 15분 동안 갱신률이 임계값(85%) 미만이면 활성화
   - 만료된 인스턴스를 삭제하지 않음 (장애 내성)
*/
```

### 📢 섹션 요약 비유

마치 **비상 연락망**과 같습니다. 각 대원(서비스)은 본부(Eureka)에 30초마다 "무사함"을 보고합니다. 90초 동안 보고가 없으면 실종으로 간주하여 명단에서 제거합니다. 본부는 전체 명단을 복사본으로 가지고 있어서, 본부가 작동하지 않아도 각 대원은 캐시한 명단으로 협력할 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: Client-side vs Server-side Discovery

| 비교 항목 | Client-side (Eureka) | Server-side (AWS ALB, Nginx) |
|:---|:---|:---|
| **로드 밸런싱 위치** | 클라이언트 내부 (Ribbon) | 중앙 로드 밸런서 |
| **복잡도** | 클라이언트 로직 필요 | 단순한 DNS/HTTP 라우팅 |
| **성능** | 추가 네트워크 홉 없음 | LB를 거치는 지연 발생 |
| **장애 격리** | 클라이언트 로컬 캐시로 내성 | LB SPOF 존재 |
| **언어 종속성** | Java/Netflix 기술 스택 | 언어 무관 |
| **운영 오버헤드** | 각 클라이언트가 캐시 유지 | LB만 관리 |
| **사용 사례** | JVM 기반 마이크로서비스 | 멀티 언어 환경 |

### 과목 융합 관점

**1) 네트워크 관점 (DNS vs Service Discovery)**

```
┌─────────────────────────────────────────────────────────────┐
│                   DNS vs Service Discovery                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [DNS-based]                                                │
│  ┌──────────────┐                                          │
│  │   Client     │                                          │
│  └──────┬───────┘                                          │
│         │ DNS Query (A Record)                             │
│         ▼                                                  │
│  ┌──────────────┐                                          │
│  │  DNS Server  │                                          │
│  │ payment.com  │                                          │
│  │ 10.0.2.3     │  ◄──── 캐싱으로 업데이트 지연             │
│  └──────────────┘                                          │
│                                                             │
│  [Service Discovery]                                       │
│  ┌──────────────┐                                          │
│  │   Client     │                                          │
│  └──────┬───────┘                                          │
│         │ Registry Fetch (실시간)                          │
│         ▼                                                  │
│  ┌──────────────┐                                          │
│  │   Eureka     │                                          │
│  │ payment:     │                                          │
│  │ - 10.0.2.3   │  ◄──── 30초마다 최신 정보                  │
│  │ - 10.0.2.4   │                                          │
│  │ - 10.0.2.5   │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

DNS는 **클라이언트와 ISP에 캐싱**되어 업데이트 지연이 큽니다(TTL 설정에 따름). 반면, Service Discovery는 **실시간으로 레지스트리를 조회**하여 컨테이너 재시작 등 동적 환경에 적합합니다.

**2) 분산 시스템 관점 (CAP 정리)**

Eureka는 **AP (Availability + Partition Tolerance)** 시스템으로 설계되었습니다.

- **가용성 최우선**: Eureka Server가 다수라도, 각 클라이언트는 로컬 캐시로 서비스 디스커버리 가능
- **결과적 일관성**: 피어 간 복제가 비동기적이므로, 일시적으로 레지스트리 불일치 가능
- **자기 보호 모드 (Self-Preservation)**: 네트워크 분할 시 실제로 살아있는 인스턴스를 삭제하지 않음 (내성성)

### 📢 섹션 요약 비유

마치 **군대의 보고 체계**와 같습니다. 각 병사(Client)은 본부(Eureka)에 정기적으로 보고하며, 본부는 전군 명단을 관리합니다. 본부가 공격을 받아도, 각 부대는 가지고 있는 명단(캐시)으로 작전을 수행할 수 있습니다. 이는 가용성을 최우선으로 하는 설계입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: Spring Cloud Eureka 클러스터 구성**

```
┌─────────────────────────────────────────────────────────────┐
│               Eureka 클러스터 구성 (3노드)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Eureka #1    │  │ Eureka #2    │  │ Eureka #3    │     │
│  │ (eureka1)    │◄─►│ (eureka2)    │◄─►│ (eureka3)    │     │
│  │   8761       │  │   8762       │  │   8763       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ▲                  │                  ▲            │
│         └──────────────────┴──────────────────┘            │
│                      Peer Awareness                        │
│                                                             │
│  [docker-compose.yml]                                      │
│  services:                                                 │
│    eureka1:                                                │
│      image: eureka-server                                  │
│      ports:                                                │
│        - "8761:8761"                                       │
│      environment:                                          │
│        - EUREKA_INSTANCE_HOSTNAME=eureka1                   │
│        - EUREKA_CLIENT_SERVICE_URL_DEFAULT_ZONE=           │
│            http://eureka2:8762/eureka,http://eureka3:8763/  │
│                                                             │
│    eureka2:                                                │
│      image: eureka-server                                  │
│      ports:                                                │
│        - "8762:8762"                                       │
│      environment:                                          │
│        - EUREKA_INSTANCE_HOSTNAME=eureka2                   │
│        - EUREKA_CLIENT_SERVICE_URL_DEFAULT_ZONE=           │
│            http://eureka1:8761/eureka,http://eureka3:8763/  │
│                                                             │
│    eureka3:                                                │
│      image: eureka-server                                  │
│      ports:                                                │
│        - "8763:8763"                                       │
│      environment:                                          │
│        - EUREKA_INSTANCE_HOSTNAME=eureka3                   │
│        - EUREKA_CLIENT_SERVICE_URL_DEFAULT_ZONE=           │
│            http://eureka1:8761/eureka,http://eureka2:8762/  │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **노드 수**: 최소 3개 (과반수 유지를 위한 홀수)
2. **배포 전략**: 각 가용 영역(AZ)에 분배하여 단일 장애점(SPOF) 제거
3. **셀프 보호 모드**: 프로덕션에서는 활성화하여 네트워크 장애 시 인스턴스 보호

**Scenario 2: Kubernetes와 통합 (Spring Cloud Kubernetes)**

```yaml
# Kubernetes Deployment (Eureka 대안)
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - protocol: TCP
      port: 8080
  type: ClusterIP
---
# Kubernetes는 서비스 디스커버리를 내장
# DNS: order-service.default.svc.cluster.local
# Eureka 없이도 서비스 간 통신 가능
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **Eureka Server HA** | 3개 이상 피어 클러스터 | |
| **Heartbeat 간격** | 30초 (기본값) 조정 필요성 검토 | |
| **만료 시간** | 90초 (3 * Heartbeat) 적절성 | |
| **셀프 보호** | 프로덕션 환경에서 활성화 | |
| **클라이언트 캐시** | 레지스트리 로컬 캐싱 활성화 | |
| **Ribbon 구성** | 로드 밸런싱 알고리즘 선택 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **모니터링** | Eureka Dashboard 대시보드 | |
| **경보** | 레지스트리 크기 모니터링 | |
| **보안** | Eureka Server 인증 (Basic Auth) | |
| **네트워크 분리** | 관리 트래픽 분리 | |

### 안티패턴

**❌ Eureka를 통한 모든 통신**

```java
// 안티패턴: 내부 서비스 간 통신도 Eureka를 통해
@FeignClient("payment-service")
public class PaymentClient {
    @PostMapping("/api/payments")
    PaymentResponse pay(OrderRequest order);
}

// 문제점: 불필요한 네트워크 홉, 지연 증가
```

**개선 방안**:

```java
// 올바른 패턴: Kubernetes 환경에서는 직접 통신
@FeignClient(url = "${payment.service.url}")
public class PaymentClient {
    @PostMapping("/api/payments")
    PaymentResponse pay(OrderRequest order);
}

// Kubernetes Service DNS 사용
// payment-service.default.svc.cluster.local
```

### 📢 섹션 요약 비유

마치 **대형 백화점의 안내 방송**과 같습니다. 처음에는 안내 데스크(Eureka)를 통해 매장 위치를 물어보지만, 자주 가는 매장은 위치를 기억해두면(캐시) 매번 물어볼 필요가 없습니다. 백화점이 확장되어도 안내 데스크 정보만 최신이면, 새로 생긴 매장도 쉽게 찾을 수 있습니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **서비스 추가 시간** | 수동 설정 1시간+ | 자동 등록 30초 | **99% 단축** |
| **장애 복구 시간** | 수동 재시작 10분+ | 자동 재등록 1분 이내 | **90% 단축** |
| **로드 밸런싱 정확도** | 수동 설정 오류 | 자동 감지 100% | **완전 자동화** |
| **가용성** | 단일 Eureka SPOF | 클러스터 99.99% | **+0.9% 향상** |
| **운영 오버헤드** | IP 관리 100건/월 | 자동 관리 0건 | **완전 해소** |

### 미래 전망

1. **Kubernetes 네이티브 Service Discovery**: K8s Service 리소스가 Eureka를 대체
2. **gRPC-based Discovery**: gRPC를 통한 고효율 서비스 등록
3. **Service Mesh (Istio)**: Pilot을 통한 동적 서비스 발견
4. **Serverless Discovery**: Lambda/Cloud Functions의 자동 등록

### 참고 표준

- **Eureka Wiki** (Netflix)
- **Spring Cloud Netflix Documentation**
- **Kubernetes Service Discovery**
- **Consul Service Discovery**
- **Nacos Service Discovery** (Alibaba)

### 📢 섹션 요약 비유

미래의 서비스 디스커버리는 **자율 주행 자동차의 V2V 통신**과 같이 발전할 것입니다. 각 서비스는 스스로 위치를 브로드캐스트하고, 주변 서비스들을 자동으로 인지하여 협력합니다. 중앙 레지스트리 없이도 분산된 서비스들이 자율적으로 협력하는 **진정한 분산 시스템**이 실현될 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[마이크로서비스 아키텍처](./556_msa.md)**: MSA 전체 아키텍처
- **[API Gateway](./616_api_gateway_auth.md)**: API 게이트웨이와 연계
- **[서킷 브레이커](./618_circuit_breaker.md)**: 장애 격리 패턴
- **[Load Balancing](./k8s_service.md)**: 로드 밸런싱 알고리즘
- **[Kubernetes Service](./k8s_service.md)**: K8s 네이티브 서비스 디스커버리

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 학교에 **반 친구 명단**이 있는 것과 같습니다. 전학 온 친구(새 서비스)가 생기면 명단에 이름을 추가하고, 이사 간 친구는 이름을 지웁니다.

**2) 원리**: 각 반(서비스)은 매일 아침 출석부(Heartbeat)를 제출합니다. 3일 연속 결석하면 자동으로 명단에서 제거됩니다. 친구들의 집을 방문할 때는 명단을 보고 주소를 찾습니다.

**3) 효과**: 친구가 이사를 가거나 새 친구가 오더라도, 명단만 최신이면 누구의 집이든 쉽게 찾아갈 수 있습니다. 각 반은 자기 반 명단을 가지고 있어서, 학교 서버가 고장 나도 친구들의 집을 찾을 수 있습니다.
