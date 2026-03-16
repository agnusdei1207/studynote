+++
title = "Helm - 헬름"
weight = 760
+++

# Helm - 헬름

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubernetes 패키지 매니저
> 2. **가치**: 템플릿, 버전 관리, 재사용
> 3. **융합:** Kubernetes, Charts, Releases

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Helm은 Kubernetes 패키지를 관리합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Helm                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              Helm 구조                                         │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Chart (차트):                                       │   │ │
│   │   │  mychart/                                            │   │ │
│   │   │  ├── Chart.yaml          (메타데이터)                │   │ │
│   │   │  ├── values.yaml         (기본값)                    │   │ │
│   │   │  ├── templates/                                      │   │ │
│   │   │  │   ├── deployment.yaml                            │   │ │
│   │   │  │   ├── service.yaml                               │   │ │
│   │   │  │   └── _helpers.tpl                               │   │ │
│   │   │  └── charts/            (의존성)                     │   │ │
│   │   │                                                      │   │ │
│   │   │  Commands:                                           │   │ │
│   │   │  helm install my-release ./mychart                   │   │ │
│   │   │  helm upgrade my-release ./mychart                   │   │ │
│   │   │  helm rollback my-release 1                          │   │ │
│   │   │  helm uninstall my-release                           │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Helm은 Kubernetes 애플리케이션을 패키징합니다.

**📢 섹션 요약 비유:** Helm = apt/npm!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Chart** | 패키지 |
| **Release** | 배포 인스턴스 |
| **Repository** | 저장소 |
| **Values** | 설정값 |
| **Template** | 템플릿 |

**핵심 알고리즸:** Chart + Values → Template → Manifests → K8s

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**Helm vs Kustomize**

| 항목 | Helm | Kustomize |
|:---|:---|:---|
| **방식** | 템플릿 | 오버레이 |
| **복잡성** | 높음 | 낮음 |
| **기능** | 다양 | 단순 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 복잡한 앱 → Helm Chart
**시나리오 2:** 단순한 앱 → Kustomize
**시나리오 3:** 공개 → Artifact Hub

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** OCI Registry Support

---

### 📌 관련 개념 링크**:
- [Kubernetes](./619_kubernetes.md)
- [GitOps](./751_gitops.md)
- [Package Management](./xxx_package.md)
