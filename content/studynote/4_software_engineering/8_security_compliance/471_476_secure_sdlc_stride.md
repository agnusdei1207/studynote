+++
title = "471-476. Secure SDLC와 위협 모델링 (STRIDE)"
description = "개발 전 단계에 보안을 내재화하는 Secure SDLC와 위협 식별을 위한 STRIDE 모델 분석"
date = 2026-03-14
[extra]
subject = "SE"
category = "Security"
id = 471
+++

# 471-476. Secure SDLC와 위협 모델링 (STRIDE)

> **핵심 인사이트**: 보안은 다 만든 프로그램에 덧칠하는 페인트가 아니라, 설계도부터 함께 그려야 하는 '철근'이다. Secure SDLC는 기획 단계부터 위협을 예측(Modeling)하고, STRIDE와 같은 체계적인 프레임워크를 통해 발생 가능한 모든 보안 구멍을 선제적으로 막아내는 예방 의학적 접근이다.

---

## Ⅰ. Secure SDLC (소프트웨어 개발 보안)
소프트웨어 생명주기(SDLC)의 각 단계마다 보안 활동을 통합하여 안전한 소프트웨어를 만드는 방법론입니다.

* **단계별 활동**:
  - **요구분석**: 보안 요구사항 도출.
  - **설계**: **위협 모델링**, 보안 설계 리뷰.
  - **구현**: **시큐어 코딩**, 정적 분석.
  - **테스트**: 동적 분석, 모의 해킹.
  - **유지보수**: 보안 패치, 모니터링.
* **주요 모델**: MS SDL, Seven Touchpoints, CLASP.

---

## Ⅱ. 위협 모델링 (Threat Modeling)
시스템에 잠재된 위협을 식별하고 리스크를 산정하여 대응 우선순위를 정하는 활동입니다.

### 1. STRIDE 모델 (위협 식별)
1. **S (Spoofing)**: 신분 위장. (인증으로 방어)
2. **T (Tampering)**: 데이터 변조. (무결성/해시로 방어)
3. **R (Repudiation)**: 행위 부인. (전자서명/로그로 방어)
4. **I (Information Disclosure)**: 정보 유출. (암호화로 방어)
5. **D (Denial of Service)**: 서비스 거부. (가용성 확보로 방어)
6. **E (Elevation of Privilege)**: 권한 상승. (인가 제어로 방어)

### 2. DREAD 모델 (리스크 산정)
* 위협의 위험도를 5가지 항목(Damage, Reproducibility, Exploitability, Affected users, Discoverability)으로 점수화하여 관리합니다.

---

## Ⅲ. 보안 성숙도 모델 (BSIMM)
* **BSIMM (Building Security In Maturity Model)**: 기업들이 실제로 보안 활동을 어떻게 하고 있는지 관찰하여 만든 데이터 기반의 성숙도 모델입니다. (실무 사례 중심)

---

## Ⅳ. 개념 맵 및 요약

```ascii
[Secure SDLC의 핵심 흐름]

  (기획) 보안 요구사항 ──> (설계) 위협 모델링 (STRIDE)
                                     │
                                     ▼
  (운영) 보안 모니터링 <── (구현) 시큐어 코딩 (SAST/DAST)
```

📢 **섹션 요약 비유**: **Secure SDLC**는 건물을 다 지은 뒤 세콤을 다는 게 아니라, 설계도 단계부터 도둑이 넘기 힘든 담장 높이와 CCTV 위치를 정하는 '방범 설계'입니다. **STRIDE**는 도둑이 신분증을 위조할지(S), 담을 넘을지(E), 문을 부술지(T) 등 범행 수법을 미리 예상해 보는 '범죄 시나리오'이고, **DREAD**는 그중 가장 큰 피해를 줄 도둑부터 막기 위한 '보안 우선순위'입니다.
