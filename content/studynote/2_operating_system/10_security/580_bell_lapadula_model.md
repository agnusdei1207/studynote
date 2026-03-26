+++
title = "580. 벨-라파둘라 모델 (Bell-LaPadula Model)"
date = "2026-03-25"
[extra]
categories = ["studynote-operating-system"]
+++

# 벨-라파둘라 모델 (Bell-LaPadula Model) - 군사 보안을 위한 기밀성(Confidentiality) 보호 수학적 프레임워크

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 벨-라파둘라 모델은 MAC(강제적 접근 제어)에서 적용되는 **"정보 유출(기밀성 침해)을 방지"**하기 위한 두 가지 기본 규칙을 제시한다. **No Read Up (NRU)**과 **No Write Down (NWD)**이 핵심이다.
> 2. **가치**: 이 규칙들에 의해 정보는 **항상 같거나 더 높은 보안 등급으로만 흐를 수** 있어, 낮은 등급의 사용자가 높은 등급의机密(비밀)에 접근하거나, 높은 등급의 정보를 낮은 등급으로 유출하는 것이 차단된다.
> 3. **한계**: 정보의 **무결성(Integrity)** 보호는 보장하지 않는다. 높은 등급 사용자가 낮은 등급에 **허용되지 않은 정보를 쓸 수 있는(Write-Up)** 가능성으로 인해 데이터 변조가 발생할 수 있다.

---

## 1. 개요 및 배경 (Context & Necessity)

### 1.1 모델의 목적

벨-라파둘라 모델은 1970년대 미국 군사 시스템에서 개발되었으며, **"어떻게 하면机密(비밀) 정보가 낮은 등급으로 유출되는 것을 방지할 수 있는가?"**라는 질문을 수학적으로 해결한다.

### 1.2 보안 등급 체계

```text
[ 군사 보안 등급 ]
TOP SECRET > SECRET > CONFIDENTIAL > UNCLASSIFIED
```

---

## 2. 두 가지 기본 규칙 (Basic Security Theorem)

### 2.1 Simple Security Property (No Read Up, NRU)

**"자신의 보안 등급보다 높은 등급의 객체는 읽을 수 없다"**

| 사용자 등급 | 읽기 가능 | 읽기 불가 |
|:---|:---|:---|
| **TOP SECRET** | 모든 등급 | - |
| **SECRET** | SECRET, CONFIDENTIAL, UNCLASSIFIED | TOP SECRET |
| **CONFIDENTIAL** | CONFIDENTIAL, UNCLASSIFIED | TOP SECRET, SECRET |

### 2.2 *-Property (Star Property, No Write Down, NWD)

**"자신의 보안 등급보다 낮은 등급의 객체에 쓸 수 없다"**

| 사용자 등급 | 쓰기 가능 | 쓰기 불가 |
|:---|:---|:---|
| **TOP SECRET** | TOP SECRET | SECRET, CONFIDENTIAL, UNCLASSIFIED |
| **SECRET** | TOP SECRET, SECRET | CONFIDENTIAL, UNCLASSIFIED |
| **CONFIDENTIAL** | 모든 등급 | - |

### 2.3 두 규칙의効果

```text
[ 정보 흐름 ]
TOP SECRET 정보 -> SECRET 사용자가 읽기 불가 (NRU)
                 -> TOP SECRET 사용자가 SECRET에 쓰기 불가 (NWD)

결과: 정보는 항상 같거나 높은 등급으로만 흐른다 -> 유출 방지
```

---

## 3. Discretionary Security Property (DSP)

DSP는 ACL(접근 제어 목록)을 통해 **임의적 접근 제어**를 허용한다:

```text
[ DSP 규칙 ]
소유자가 ACL을 통해 다른 사용자에게 명시적으로 권한을 부여할 수 있다.
단, 이 조작도 NRU와 NWD 규칙의 범위 내에서만 가능하다.
```

---

## 4. Bell-LaPadula 모델의한계

### 4.1 무결성 미보장

NRU/NWD는 기밀성은 보장하지만, **무결성은 보장하지 않는다**:

```text
[ 문제 상황 ]
1. 높은 등급 사용자(User_H)가 낮은 등급 객체(Object_L)에 "정보를 쓸 수 있다" (NWD는 쓰기를 금하지 않음)
2. User_H가 Object_L에 유출 정보를 작성
3. 낮은 등급 사용자가 해당 정보를 읽고 활용
```

### 4.2 Practical Issue: 신뢰받는 Subject

실제 시스템에서는 백업, 로깅 등을 위해 **신뢰받는 Subject**는 NWD 규칙을 면제받는다:

```text
[ 예외 ]
백업 데몬: 모든 등급의 파일을 읽고, 모든 등급의 백업 위치에 쓸 수 있음
```

---

## 5. 기대효과 및 결론

- **기밀성 완벽 보호**: 수학적 증명을 통해 정보 유출이 원천 차단됨
- **군사/정부 시스템 적합**: 국가 보안 수준의 접근 제어에 적합
- **무결성 미보장**: 데이터 변조 가능성이 남아 있으므로, Biba 모델 등과의 병행 사용이 필요

---

## 관련 개념 맵 (Knowledge Graph)

| 관련 개념 | 설명 |
|:---|:---|
| **MAC (579장)** | 벨-라파둘라 모델이 적용되는 상위 보안 체계 |
| **Biba (581장)** | 기밀성이 아닌 무결성 보호를 위한 보안 모델 |
| **DAC (578장)** | DSP를 통해 포함되는 임의적 접근 제어 |
| **NIST Orange Book** | 벨-라파둘라 모델을 기반으로 한 보안 평가 기준 |

---

## 👶 어린이를 위한 3줄 비유 설명

1. **벨-라파둘라 모델**은 놀이공원의 **"等급制度(등급 제도)"**와 같다. 상위 등급 사람은 하위 등급 놀이기구에는 접근할 수 없고, 하위 등급 사람은 상위 등급 놀이기구를利用(이용)할 수 없다.

2. **NRU (No Read Up)**는 **"아래 계급 사람은 위 계급의 문서를 읽을 수 없다"**는 병영 규칙과 같다. 이등병은 대대장의 문서를 볼 수 없다.

3. **NWD (No Write Down)**는 **"위 계급 사람은 아래 계급에게 기밀 정보를 줄 수 없다"**는 규칙과 같다. 대대장이 이등병에게 비밀 작전 내용을 알려줄 수 없다.

4. **한계**는 **"위 계급 사람이 아래 계급의 보고서를 수정할 수 있다"**는 점이다. 이등병의 순찰 보고서를 대대장이 고쳐버리면, 무결성이 깨질 수 있다.
