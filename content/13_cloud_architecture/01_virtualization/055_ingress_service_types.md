---
title: "Ingress Service Types"
date: "2026-05-01"
tags:
  - "studynote-cloud-architecture"
weight: 55
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Ingress는 HTTP/HTTPS 요청을 클러스터 내부 서비스로 라우팅하는 진입점이다.
> 2. **가치**: Service Type (ClusterIP, NodePort, LoadBalancer)과 함께 외부 노출 방식을 설계한다.
> 3. **판단 포인트**: Ingress Controller가 실제 동작 주체이며, TLS와 경로/호스트 규칙이 핵심이다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스에서 외부 트래픽을 어떻게 받을지 정해야 한다. 서비스 타입은 노출 방식을, Ingress는 HTTP 라우팅 규칙을 담당한다.

웹 서비스의 도메인, 경로, 인증서, 라우팅을 통합하려면 Ingress가 유용하다.

- **📢 섹션 요약 비유**: Ingress는 빌딩 현관, Service Type은 각 층의 출입문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Service는 Pod 묶음에 안정적인 네트워크를 제공하고, Ingress는 여러 서비스 앞에서 HTTP 라우팅을 수행한다. 실제 라우팅은 Ingress Controller가 맡는다.

```text
Client -> Ingress Controller -> Ingress Rule -> Service -> Pod
```

| 객체 | 역할 | 포인트 |
| :--- | :--- | :--- |
| ClusterIP | 내부 전용 | 기본 |
| NodePort | 노드 포트 노출 | 단순 외부 접근 |
| LoadBalancer | 클라우드 LB 연동 | 외부 노출 |
| Ingress | L7 라우팅 | host/path/TLS |

핵심은 Service가 포드 묶음을 제공하고, Ingress가 웹 라우팅 정책을 제공한다는 점이다.

- **📢 섹션 요약 비유**: Service는 엘리베이터, Ingress는 층별 안내판이다.

---

## Ⅲ. 비교 및 연결

Service Type은 네트워크 노출 방식이고, Ingress는 HTTP 계층의 규칙이다. 둘을 함께 써야 웹 애플리케이션을 깔끔하게 외부에 제공할 수 있다.

| 항목 | Service Type | Ingress |
| :--- | :--- | :--- |
| 계층 | L4 중심 | L7 중심 |
| 역할 | 노출 | 라우팅 |
| 대표 기능 | 포트/로드밸런싱 | 경로/호스트/TLS |

Ingress Controller는 NGINX, Traefik, HAProxy 같은 구현이 있다. 운영에서는 인증서 갱신과 라우팅 충돌도 중요하다.

- **📢 섹션 요약 비유**: Service Type은 길을 내는 일이고, Ingress는 그 길에 표지판을 세우는 일이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 외부 공개 범위, TLS 종료 위치, 경로 기반 분기, health check, WAF 연계 등을 본다. 서비스 타입별 장단점도 명확히 해야 한다.

### 체크리스트

1. 내부/외부 노출이 구분되는가?
2. Ingress Controller가 배치되어 있는가?
3. TLS 인증서 관리가 되는가?
4. host/path 규칙이 충돌하지 않는가?

### 안티패턴

- NodePort를 외부 표준처럼 남발하는 경우
- Ingress 없이 서비스만 노출하는 경우
- 인증서와 라우팅을 수동 관리하는 경우

실무 관점에서는 Service와 Ingress가 네트워크 노출의 서로 다른 계층을 맡는다는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: Ingress는 현관문, Service Type은 각 방의 문이다.

---

## Ⅴ. 기대효과 및 결론

Ingress와 Service Type을 적절히 조합하면 외부 트래픽 관리와 서비스 분리가 쉬워진다.

정리하면, Service는 내부 묶음, Ingress는 외부 진입이다.

- **📢 섹션 요약 비유**: Ingress는 건물 입구, Service는 안쪽 방 배치도다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| ClusterIP | 내부 서비스 |
| NodePort | 포트 노출 |
| LoadBalancer | 외부 LB |
| Ingress | L7 라우팅 |
| Controller | 실제 동작 |

### 📈 관련 키워드 및 발전 흐름도

```text
클러스터 내부 서비스
    |
    v
Service Type
    |
    v
Ingress Controller
    |
    v
외부 HTTP/HTTPS 라우팅
```

이 흐름은 쿠버네티스 서비스 노출이 계층별로 분리되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Service Type은 건물 문 종류예요.
2. Ingress는 어디로 갈지 알려 주는 안내판이에요.
3. 둘을 같이 써야 손님이 길을 잘 찾아와요.
