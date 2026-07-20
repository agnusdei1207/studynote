---
title: "Sidecar Proxy Pattern"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사이드카 프록시는 <strong>메인 컨테이너(비즈니스 로직) 옆에 보조 컨테이너(프록시)를 배치</strong>하여, 네트워크 통신의 로드밸런싱·재시도·mTLS·메트릭·트레이싱을 투명하게 처리하는 패턴이다.
> 2. **가치**: 통신 로직을 <strong>코드에서 분리</strong>하여 언어·프레임워크에 무관하게 일관된 네트워크 정책을 적용하며, 서비스 코드는 <strong>비즈니스 로직에만 집중</strong>한다.
> 3. **판단 포인트**: Envoy(Istio)·Linkerd-proxy(Linkerd)가 대표이며, eBPF 기반(Cilium)은 사이드카 없이 커널 레벨에서 처리하는 차세대 방식이다.

---

## Ⅰ. 개요 및 필요성

```text
K8s Pod:
  [메인 컨테이너: 비즈니스 로직]
  [사이드카 컨테이너: Envoy Proxy]
    -> 모든 인바운드/아웃바운드 트래픽 가로채기
    -> LB·재시도·mTLS·메트릭·트레이싱 처리
    -> iptables/ebpf로 투명 프록시
```

- **📢 섹션 요약 비유**: 사이드카는 <strong>오토바이 사이드카</strong>이다. 운전자(메인)는 운전에 집중하고, 사이드카(프록시)가 짐(통신)을 처리한다.

---

## Ⅱ~Ⅴ. 결론

사이드카 프록시는 <strong>서비스 메시의 데이터 플레인</strong>이며, Envoy가 사실상 표준이고 eBPF가 차세대이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>사이드카</strong> | 보조 컨테이너 |
| **Envoy** | L7 프록시 |
| **iptables** | 트래픽 가로채기 |
| <strong>mTLS</strong> | 상호 TLS |
| <strong>eBPF</strong> | 커널 레벨 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브러리 기반 (~2015)] -> [사이드카 프록시 (Envoy, 2016)]
    -> [Istio/Linkerd 채택 (2017~)]
    -> [Ambient Mesh (사이드카 없는 Istio, 2022)]
    -> [현재: Cilium eBPF — 커널 레벨 프록시]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 사이드카는 <strong>오토바이 옆칸</strong>이에요. 운전자(메인)는 **운전만** 해요.
2. 옆칸(프록시)이 <strong>짐(통신) 처리·보안·기록</strong>을 대신해요.
3. 모든 오토바이에 <strong>같은 옆칸</strong>을 달면 규칙이 통일돼요!
