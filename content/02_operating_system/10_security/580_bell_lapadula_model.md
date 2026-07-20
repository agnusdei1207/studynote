---
title: "No Read Up, No Write Down"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 580
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 벨-라파둘라 모델은 MAC(강제적 접근 제어)에서 적용되는 <strong>"정보 유출(기밀성 침해)을 방지"</strong>하기 위한 두 가지 기본 규칙을 제시한다. <strong>No Read Up (NRU)</strong>과 <strong>No Write Down (NWD)</strong>이 핵심이다.
> 2. **가치**: 이 규칙들에 의해 정보는 **항상 같거나 더 높은 보안 등급으로만 흐를 수** 있어, 낮은 등급의 사용자가 높은 등급의궤밀(비밀)에 접근하거나, 높은 등급의 정보를 낮은 등급으로 유출하는 것이 차단된다.
> 3. **한계**: 정보의 <strong>무결성(Integrity)</strong> 보호는 보장하지 않는다. 높은 등급 사용자가 낮은 등급에 **허용되지 않은 정보를 쓸 수 있는(Write-Up)** 가능성으로 인해 데이터 변조가 발생할 수 있다.

---

## Ⅰ. 개요 및 필요성

### 1.1 모델의 목적

벨-라파둘라 모델은 1970년대 미국 군사 시스템에서 개발되었으며, <strong>"어떻게 하면궤밀(비밀) 정보가 낮은 등급으로 유출되는 것을 방지할 수 있는가?"</strong>라는 질문을 수학적으로 해결한다.

### 1.2 보안 등급 체계

```text
[ 군사 보안 등급 ]
TOP SECRET > SECRET > CONFIDENTIAL > UNCLASSIFIED
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Simple Security Property (No Read Up, NRU)

**"자신의 보안 등급보다 높은 등급의 객체는 읽을 수 없다"**

| 사용자 등급 | 읽기 가능 | 읽기 불가 |
|:---|:---|:---|
| <strong>TOP SECRET</strong> | 모든 등급 | - |
| <strong>SECRET</strong> | SECRET, CONFIDENTIAL, UNCLASSIFIED | TOP SECRET |
| **CONFIDENTIAL** | CONFIDENTIAL, UNCLASSIFIED | TOP SECRET, SECRET |

### 2.2 *-Property (Star Property, No Write Down, NWD)

**"자신의 보안 등급보다 낮은 등급의 객체에 쓸 수 없다"**

| 사용자 등급 | 쓰기 가능 | 쓰기 불가 |
|:---|:---|:---|
| <strong>TOP SECRET</strong> | TOP SECRET | SECRET, CONFIDENTIAL, UNCLASSIFIED |
| <strong>SECRET</strong> | TOP SECRET, SECRET | CONFIDENTIAL, UNCLASSIFIED |
| **CONFIDENTIAL** | 모든 등급 | - |

### 2.3 두 규칙의효과

```text
[ 정보 흐름 ]
TOP SECRET 정보 -> SECRET 사용자가 읽기 불가 (NRU)
                 -> TOP SECRET 사용자가 SECRET에 쓰기 불가 (NWD)

결과: 정보는 항상 같거나 높은 등급으로만 흐른다 -> 유출 방지
```

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

DSP는 ACL(접근 제어 목록)을 통해 <strong>임의적 접근 제어</strong>를 허용한다:

```text
[ DSP 규칙 ]
소유자가 ACL을 통해 다른 사용자에게 명시적으로 권한을 부여할 수 있다.
단, 이 조작도 NRU와 NWD 규칙의 범위 내에서만 가능하다.
```

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 4.1 무결성 미보장

NRU/NWD는 기밀성은 보장하지만, <strong>무결성은 보장하지 않는다</strong>:

```text
[ 문제 상황 ]
1. 높은 등급 사용자(User_H)가 낮은 등급 객체(Object_L)에 "정보를 쓸 수 있다" (NWD는 쓰기를 금하지 않음)
2. User_H가 Object_L에 유출 정보를 작성
3. 낮은 등급 사용자가 해당 정보를 읽고 활용
```

### 4.2 Practical Issue: 신뢰받는 Subject

실제 시스템에서는 백업, 로깅 등을 위해 <strong>신뢰받는 Subject</strong>는 NWD 규칙을 면제받는다:

```text
[ 예외 ]
백업 데몬: 모든 등급의 파일을 읽고, 모든 등급의 백업 위치에 쓸 수 있음
```

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

- <strong>기밀성 완벽 보호</strong>: 수학적 증명을 통해 정보 유출이 원천 차단됨
- **군사/정부 시스템 적합**: 국가 보안 수준의 접근 제어에 적합
- <strong>무결성 미보장</strong>: 데이터 변조 가능성이 남아 있으므로, Biba 모델 등과의 병행 사용이 필요

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 임의적 접근 제어 (DAC, Discretionary Access Control) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 강제적 접근 제어 (MAC, Mandatory Access Control) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 비바 모델 (Biba Model) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 리눅스 보안 모듈 (LSM, Linux Security Modules) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[강제적 접근 제어 (MAC, Mandatory Access Control)]
    |
    v
[벨-라파둘라 모델 (Bell-LaPadula)]
    |
    +---> [비바 모델 (Biba Model)]
    +---> [리눅스 보안 모듈 (LSM, Linux Security Modules)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>벨-라파둘라 모델</strong>은 놀이공원의 <strong>"등급제도(등급 제도)"</strong>와 같다. 상위 등급 사람은 하위 등급 놀이기구에는 접근할 수 없고, 하위 등급 사람은 상위 등급 놀이기구를리용(이용)할 수 없다.

2. <strong>NRU (No Read Up)</strong>는 <strong>"아래 계급 사람은 위 계급의 문서를 읽을 수 없다"</strong>는 병영 규칙과 같다. 이등병은 대대장의 문서를 볼 수 없다.

3. <strong>NWD (No Write Down)</strong>는 <strong>"위 계급 사람은 아래 계급에게 기밀 정보를 줄 수 없다"</strong>는 규칙과 같다. 대대장이 이등병에게 비밀 작전 내용을 알려줄 수 없다.

4. <strong>한계</strong>는 <strong>"위 계급 사람이 아래 계급의 보고서를 수정할 수 있다"</strong>는 점이다. 이등병의 순찰 보고서를 대대장이 고쳐버리면, 무결성이 깨질 수 있다.
