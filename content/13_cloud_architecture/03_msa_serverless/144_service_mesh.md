---
title: "Service Mesh"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 144
---
<!-- top-summary -->
> - 중복 정리: 비대표 노트
> - 군집: Service Mesh
> - 🔗 대표 정리: [[181_service_mesh_istio_linkerd]]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서비스 메시는 <strong>각 마이크로서비스에 사이드카 프록시(Envoy)를 배치</strong>하여, 서비스 간 통신의 <strong>로드밸런싱·서킷 브레이커·mTLS·트레이싱·트래픽 제어</strong>를 애플리케이션 코드 변경 없이 인프라 레벨에서 처리하는 패턴이다.
> 2. **가치**: 서비스 간 통신 로직(재시도·타임아웃·암호화)을 <strong>각 서비스가 직접 구현하면 중복·불일치</strong>가 발생하지만, 서비스 메시는 <strong>사이드카가 일괄 처리</strong>하여 일관성을 보장한다.
> 3. **판단 포인트**: Istio(가장 기능 풍부)·Linkerd(경량)·Cilium(eBPF 기반, 사이드카 없음)이 대표이며, 컨트롤 플레인(정책 관리)과 데이터 플레인(사이드카 프록시)으로 구성된다.

---

## Ⅰ. 개요 및 필요성

```text
서비스 메시 구조:
  데이터 플레인: Envoy 사이드카 (각 Pod 옆)
    -> 트래픽 가로채기 -> LB·재시도·mTLS·트레이싱
  컨트롤 플레인: Istiod (정책·설정 배포)
    -> VirtualService·DestinationRule 등 CRD
```

- **📢 섹션 요약 비유**: 서비스 메시는 <strong>우체국 네트워크</strong>이다. 편지(요청)를 직접 전달하는 대신, 우체부(사이드카)가 분류·배달·보안을 대행한다.

---

## Ⅱ~Ⅴ. 결론

서비스 메시는 <strong>MSA 통신의 인프라 표준</strong>이며, Istio(기능)·Cilium(eBPF 성능)이 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>서비스 메시</strong> | 사이드카 통신 |
| **Envoy** | 사이드카 프록시 |
| <strong>Istio</strong> | 컨트롤 플레인 |
| <strong>mTLS</strong> | 서비스 간 암호화 |
| <strong>Cilium</strong> | eBPF 기반 (차세대) |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브러리 기반 (Netflix OSS, 2014)] -> [Linkerd v1 (2017)]
    -> [Istio + Envoy (2017)] -> [Linkerd2 (Rust, 경량)]
    -> [현재: Cilium (eBPF, 사이드카 없음)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 서비스 메시는 <strong>우체국 시스템</strong>이에요. 편지를 직접 가져가지 않고 <strong>우체부(사이드카)</strong>가 배달해요.
2. 우체부가 <strong>분류·보안·재배달</strong>을 다 해줘서 보내는 사람은 편해요.
3. 우체국 본부(컨트롤 플레인)가 <strong>모든 우체부에게 규칙</strong>을 알려줘요!
