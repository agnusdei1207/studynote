---
title: "Kustomize Kubernetes Declarative Overlay Manifest"
date: "2026-04-10"
tags:
  - "studynote-devops-sre"
weight: 91
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kustomize는 템플릿 변수를 쓰지 않고, 원본 쿠버네티스(Kubernetes) YAML 파일을 그대로 유지한 채 오버레이(Overlay) 방식으로 패치(Patch)를 적용하는 선언적 설정 관리 도구다.
> 2. **가치**: 복잡한 조건문 없이 순수 YAML의 가독성을 보존하며, 환경(Dev/Prod)별로 달라지는 설정(예: 파드 개수, 메모리 크기)만 간결하게 분리하여 관리할 수 있다.
> 3. **판단 포인트**: 외부 오픈소스를 배포할 때는 패키징이 강력한 Helm을 사용하고, 사내 애플리케이션을 여러 환경에 배포할 때는 원본 코드를 보존하는 Kustomize를 사용하는 것이 GitOps 설계의 핵심 정석이다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스 환경에서 애플리케이션을 개발망(Dev), 검증망(Stg), 운영망(Prod)에 배포하려면 기본적으로 동일한 구조의 매니페스트(Manifest)가 필요하다. 하지만 환경마다 할당되는 리소스(CPU/Memory), 레플리카(Replica) 개수, 환경 변수 등 미세한 차이가 존재한다. 이를 위해 기존에는 YAML 파일을 복사/붙여넣기 하거나, Helm을 이용해 YAML 파일 내부에 `{{ .Values.memory }}` 같은 변수 구멍을 뚫어 템플릿화했다.

그러나 복사본 관리는 휴먼 에러를 유발하고, 템플릿화는 원본 K8s YAML의 문법을 파괴하여 가독성을 극도로 훼손시켰다. 이를 해결하기 위해 Kustomize가 등장했다. Kustomize는 "원본 YAML 파일(Base)은 단 한 글자도 수정하지 않고, 그 위에 필요한 변경 사항(Overlay)만 덮어씌운다"는 철학을 바탕으로 K8s 생태계에 내장된 도구다.

- **📢 섹션 요약 비유**: Kustomize는 여러 벌의 양복을 새로 맞추는 대신, 완벽한 기본 셔츠(Base)를 하나 만들어두고 출근할 때는 넥타이(Dev 오버레이)를, 파티 갈 때는 나비넥타이(Prod 오버레이)만 덧붙여 입는 스마트한 코디네이션 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Kustomize는 베이스(Base), 오버레이(Overlays), 그리고 조립 지시서인 `kustomization.yaml`로 구성된다. 변수를 치환하는 렌더링 엔진이 아니라, YAML 객체들을 병합(Merge)하는 패칭(Patching) 엔진으로 동작한다.

| 핵심 요소 | 역할 및 동작 원리 |
| :--- | :--- |
| **Base (뼈대)** | 모든 환경에서 공통으로 사용되는 순수 K8s YAML 파일들의 집합. 단독으로 배포해도 문법 오류가 없는 온전한 상태를 유지한다. |
| **Overlays (덧칠)** | 특정 환경(Dev, Prod 등)에서 Base 위에 덮어쓸 패치(Patch) 파일들을 담고 있는 디렉토리 구조. |
| <strong><code>kustomization.yaml</code></strong> | 현재 폴더에서 어떤 리소스(Base)를 가져오고, 어떤 패치(Overlay)를 적용하며, 라벨(Label)이나 네임스페이스를 일괄 변경할지 정의하는 지휘자 역할을 한다. |
| <strong><code>kubectl apply -k</code></strong> | K8s CLI에 기본 내장된 Kustomize 실행 옵션으로, 조립된 최종 매니페스트를 즉시 클러스터에 적용한다. |

```text
+--------------------------------------------------------------+
|          Kustomize의 Base와 Overlay 병합(Merge) 과정        |
+--------------------------------------------------------------+
| [ base/deployment.yaml ]         [ overlays/prod/patch.yaml ]|
| apiVersion: apps/v1              apiVersion: apps/v1         |
| kind: Deployment                 kind: Deployment            |
| metadata:                        metadata:                   |
|   name: my-app                     name: my-app              |
| spec:                            spec:                       |
|   replicas: 1 <------------------>   replicas: 10              |
|                                                              |
|              Kustomize 엔진 병합 (Merge)                     |
|                           v                                  |
| [ 최종 생성된 In-memory YAML (클러스터로 전송됨) ]           |
| apiVersion: apps/v1                                          |
| kind: Deployment                                             |
| metadata:                                                    |
|   name: my-app                                               |
| spec:                                                        |
|   replicas: 10 (Prod 설정으로 덮어써짐)                      |
+--------------------------------------------------------------+
```

이 과정에서 Kustomize는 단순 텍스트 치환이 아니라 K8s API 구조를 이해하고 객체 단위의 병합(Strategic Merge Patch)을 수행하기 때문에 구조적 안정성이 매우 높다.

- **📢 섹션 요약 비유**: 밑그림(Base)을 완벽하게 그려놓고, 지우개로 지웠다 다시 그리는 것이 아니라 투명한 셀로판지(Overlay)에 바뀐 부분만 그려서 원본 위에 겹쳐보는 마법의 도면 설계법이다.

---

## Ⅲ. 비교 및 연결

K8s 매니페스트 관리의 양대 산맥인 Helm과 Kustomize는 경쟁자라기보다 보완재에 가깝다. 목적에 따라 선택이 명확히 갈린다.

| 비교 항목 | Helm | Kustomize |
| :--- | :--- | :--- |
| **작동 방식** | 템플릿(Template) 엔진 기반 (변수 치환) | 오버레이(Overlay) 기반 객체 병합(Patch) |
| **원본 유지** | 파괴됨 (`{{ }}` 사용으로 순수 YAML이 아님) | 보존됨 (순정 K8s YAML 100% 호환) |
| **주 사용처** | MySQL, Redis 등 외부 솔루션 패키지 설치 | 사내 애플리케이션의 다중 환경(Dev/Prod) 배포 |
| **학습 곡선** | 높음 (Helm 자체 문법과 Go Template 학습 필요) | 낮음 (K8s YAML 문법만 알면 즉시 사용 가능) |

최근 GitOps 트렌드에서는 이 둘을 결합한 **Post-Rendering** 전략이 각광받는다. 헬름으로 복잡한 외부 솔루션을 렌더링한 직후, Kustomize를 덮어씌워 사내 보안 라벨링이나 네임스페이스 규칙을 강제 패치하는 콤보 전술이다.

- **📢 섹션 요약 비유**: Helm은 다른 공장에서 만든 '완제품 케이크 세트(패키지)'를 통째로 사오는 것이고, Kustomize는 우리 집 주방에서 구운 빵(Base) 위에 초코크림(Dev)을 바를지 생크림(Prod)을 바를지 결정하는 정교한 데코레이션 작업이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

Kustomize를 도입하면 인프라 코드의 중복(DRY, Don't Repeat Yourself 원칙)을 극적으로 줄일 수 있다. GitOps 툴인 ArgoCD나 FluxCD는 내부적으로 Kustomize를 네이티브하게 지원하므로 통합 파이프라인 구성에 최적화되어 있다.

### 체크리스트
1. **순수성 보장**: `base/` 디렉토리 안의 파일들이 `kubectl apply -f` 명령어로 단독 배포 가능한 100% 순수한 K8s YAML 상태를 유지하고 있는가?
2. **패치 최소화**: 오버레이 패치(`patch.yaml`)가 너무 비대해져서 베이스를 덮어쓰는 양이 많지 않은가? 변경점이 너무 많다면 Base 설계가 잘못된 것이다.
3. **일괄 관리 활용**: `kustomization.yaml`의 `commonLabels`, `namePrefix`, `namespace` 속성을 활용해 모든 하위 리소스에 공통 속성을 한 번에 주입하도록 설계했는가?

### 안티패턴
- 개발(Dev)과 운영(Prod) 간 차이가 50% 이상 벌어지는데 억지로 하나의 Base를 두고 수많은 오버레이로 누더기 패치를 만드는 설계. 이 경우 차라리 Base를 분리하는 것이 낫다.

- **📢 섹션 요약 비유**: 스마트폰 기본 뼈대(Base)는 똑같이 만들고, 케이스와 보호필름(Overlay)만 바꿔 끼워 모델을 다변화하는 훌륭한 공정 라인을 갖추는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Kustomize를 사용하면 복사/붙여넣기로 인한 설정 오류가 근절되고, 인프라 코드의 가독성이 획기적으로 향상된다. 쿠버네티스 순정 객체를 다루는 직관성 덕분에 개발자와 운영자 모두 코드를 쉽게 이해하고 리뷰할 수 있어 진정한 의미의 '선언적 인프라(Declarative Infrastructure)'가 완성된다.

미래의 클라우드 인프라 관리는 선언적 철학을 고도화하는 방향으로 발전할 것이다. Kustomize는 템플릿 변수의 늪에 빠지지 않고도 다형성을 구현할 수 있음을 증명한 모범 사례로, K8s 네이티브 생태계의 영원한 핵심 관리 도구로 남을 것이다.

- **📢 섹션 요약 비유**: 도장(Base)을 파놓고 잉크 색깔(Overlay)만 바꿔서 찍으면 수만 장의 서로 다른 문서를 빠르고 정확하게 만들어낼 수 있는 최고의 인쇄 기술이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong>Helm (헬름)</strong> | Kustomize와 상호 보완적인 K8s 패키지 매니저 및 템플릿 도구 |
| <strong>GitOps (깃옵스)</strong> | Git 저장소를 단일 진실 공급원(SSOT)으로 삼아 Kustomize 코드를 배포하는 철학 |
| **ArgoCD / FluxCD** | Kustomize 조립 지시서를 읽어 자동으로 K8s에 동기화(Sync)해 주는 선언적 배포 로봇 |
| **Strategic Merge Patch** | Kustomize가 K8s 객체 간의 병합을 수행할 때 충돌을 영리하게 해결하는 K8s 전용 패치 알고리즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
YAML 파일의 복사본 증식 및 휴먼 에러 발생
    |
    v
Helm 도입 (템플릿 변수를 통한 다형성 확보, 가독성 저하)
    |
    v
Kustomize의 내장 (순수 YAML 보존 + Overlay 패치 방식 채택)
    |
    v
GitOps(ArgoCD)와의 결합 (선언적 지속적 배포 파이프라인 완성)
    |
    v
Post-Rendering 전술 (Helm 패키징 위에 Kustomize 패칭을 덮어쓰기)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 똑같은 로봇 장난감(Base)을 여러 개 샀어요.
2. 장난감을 부수고 개조하는 게 아니라, 하나에는 소방관 옷(Dev 오버레이)을 입히고 하나에는 경찰관 옷(Prod 오버레이)을 입혀요.
3. 옷만 덮어씌워서 역할을 바꾸는 똑똑한 장난감 변신 방법이랍니다!
