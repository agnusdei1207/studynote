---
title: "Service Discovery"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 127
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Service Discovery는 <strong>MSA에서 동적으로 변하는 서비스 인스턴스의 위치(IP:Port)를 자동으로 등록·탐색·갱신</strong>하는 메커니즘이며, 서비스 레지스트리(Service Registry)가 핵심 컴포넌트이다.
> 2. **가치**: 컨테이너 환경에서 서비스 인스턴스는 스케일링·재배포 시 <strong>IP가 수시로 변경</strong>되므로 하드코딩이 불가능하며, Service Discovery가 <strong>"주문 서비스 어디 있어?"에 실시간 답변</strong>한다.
> 3. **판단 포인트**: <strong>Client-side(클라이언트가 레지스트리 조회)</strong> vs <strong>Server-side(로드밸런서가 레지스트리 조회)</strong>를 구분하고, K8s의 DNS 기반 Service Discovery가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Service Discovery 동작                             |
+-------------------------------------------------------+
|  1. 서비스 인스턴스 시작 -> Registry에 등록           |
|     (Order-Svc: 10.0.1.5:8080)                       |
|  2. 호출자가 "Order-Svc 어디?" -> Registry 조회       |
|  3. Registry 응답: 10.0.1.5:8080                     |
|  4. 호출자 -> 10.0.1.5:8080 직접 호출                |
|  5. 인스턴스 종료 -> Registry에서 제거 (헬스체크)     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Service Discovery는 <strong>전화번호부</strong>이다. 사람(서비스)이 이사(IP 변경)해도 전화번호부(레지스트리)를 보면 **현재 주소를 찾을 수 있다**.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Client-side vs Server-side

| 방식 | 동작 | 대표 |
|:---|:---|:---|
| **Client-side** | 클라이언트가 레지스트리 조회 + LB | **Eureka** |
| **Server-side** | LB가 레지스트리 조회 | <strong>K8s Service</strong> |

### K8s Service Discovery
- Pod 생성 -> kube-dns에 자동 등록.
- `order-svc.default.svc.cluster.local`로 DNS 조회.

- **📢 섹션 요약 비유**: Client-side는 직접 전화번호부를 찾는 것, Server-side는 안내 데스크(LB)에 물어보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 하드코딩 | Service Discovery |
|:---|:---|:---|
| **IP 변경** | 코드 수정 | **자동 갱신** |
| <strong>스케일링</strong> | 수동 | **동적 등록** |
| **장애** | 감지 불가 | **헬스체크 제거** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 대표 도구
- **Consul** (HashiCorp): Service Discovery + Config.
- **Eureka** (Netflix): Client-side, Spring Cloud.
- <strong>K8s Service</strong>: Server-side, DNS 기반.
- <strong>etcd</strong>: K8s의 상태 저장소.

---

## Ⅴ. 기대효과 및 결론

Service Discovery는 <strong>MSA의 서비스 간 통신의 기본 인프라</strong>이며, K8s 환경에서는 DNS 기반으로 투명하게 제공된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Service Registry</strong> | 서비스 위치 저장소 |
| **헬스체크** | 비정상 인스턴스 자동 제거 |
| **Consul** | HashiCorp 서비스 디스커버리 |
| **Eureka** | Netflix 클라이언트 사이드 |
| <strong>K8s DNS</strong> | 서버 사이드 디스커버리 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드코딩 IP (전통, ~2010s)]
    |
    v
[Client-side Discovery (Eureka, 2012~)]
    |
    v
[Server-side Discovery (K8s Service, 2015~)]
    |
    v
[Service Mesh (Istio/Envoy, 2018~) — 투명한 Discovery]
    |
    v
[현재: 멀티 클러스터 Discovery — 클러스터 간 서비스 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Service Discovery는 <strong>전화번호부</strong>예요. 친구(서비스)가 이사해도 <strong>새 주소</strong>를 찾을 수 있어요.
2. 전화번호부가 없으면 친구가 이사할 때마다 **직접 물어봐야** 해서 불편해요.
3. 쿠버네티스(K8s)는 전화번호부를 <strong>자동으로 업데이트</strong>해줘서 편리하답니다!
