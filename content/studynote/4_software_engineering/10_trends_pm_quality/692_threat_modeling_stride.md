+++
title = "692. 위협 모델링 STRIDE"
date = "2026-03-15"
weight = 692
[extra]
categories = ["Software Engineering"]
tags = ["Security", "Threat Modeling", "STRIDE", "Risk Assessment", "Secure Design", "Microsoft"]
+++

# 692. 위협 모델링 STRIDE

## # [위협 모델링 STRIDE]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 설계 단계에서 **DFD (Data Flow Diagram)**를 활용하여 시스템 자산, 진입점, 신뢰 경계(Trust Boundary)를 분석하고, 공격자의 관점에서 잠재적 보안 위협을 구조화하여 식별하는 **선제적 위험 분석 체계**이다.
> 2. **가치**: 개발 완료 후 보안 패치(Cure)에 드는 막대한 비용을 설계 단계의 예방 조치(Prevention)로 획기적(약 1/100 수준)으로 절감하며, 시스템의 **CIA (Confidentiality, Integrity, Availability)** 삼요소를 아키텍처 수준에서 보증한다.
> 3. **융합**: 단순한 보안 체크리스트를 넘어 **시큐어 코딩(Secure Coding)** 가이드라인을 도출하고, **침투 테스트(Penetration Testing)**의 우선순위를 결정하는 전략적 허브 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background)

**위협 모델링(Threat Modeling)**이란 소프트웨어 개발 수명 주기(SDLC)의 초기 단계, 특히 설계(Design) 단계에서 시스템의 보안 취약점을 체계적으로 찾아내어 대응하는 활동입니다. '존슨(Jhonson)'과 '스위거(Swider)" 등이 정의한 바와 같이, 이는 코드를 작성하기 전에 보안 요구사항을 명확히 하기 위한 가장 효율적인 비용 절감 기법입니다.

과거의 보안은 '방화벽'과 같이 시스템 외부를 두르는 보안(Perimeter Security)이 주를 이루었으나, 클라우드(Cloud) 환경과 마이크로서비스 아키텍처(MSA)로의 전환으로 인해 경계가 모호해졌습니다. 이에 따라 내부의 각 컴포넌트 간 데이터 흐름을 분석하여 공격 표면을 최소화해야 합니다. 이때 사용되는 가장 대표적인 분류 체계가 바로 **STRIDE**입니다.

이 과정은 시스템을 "상자"로 보지 않고, 데이터가 흐르는 "파이프"와 "저장소"로 분해하여, "공격자가 이 데이터를 탈취하거나 변조하려면 어디를 노려야 하는가?"를 질문하는 엔지니어링 활동입니다.

**💡 비유: 은행 건물의 도면 검토 및 시뮬레이션**
> 위협 모델링은 건물을 짓기 전 설계 도면을 펴놓고, 도둑이 어느 창문으로 들어올지, 금고를 폭파할지, 혹은 직원으로 위장할지를 시뮬레이션하여 **CCTV 설치 위치와 방범창의 강도를 결정**하는 과정과 같습니다.

**📢 섹션 요약 비유**
> 마치 복잡한 지하도시를 건설하기 전, 설계 도면 위에 '물난리'나 '화재' 시뮬레이션을 돌려서 배수로와 소화전 위치를 미리 정하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. STRIDE 모델 상세 분석
마이크로소프트(Microsoft)에서 정의한 **STRIDE**는 시스템이 충족해야 할 보안 속성(Property)과 1:1 대응 관계에 있습니다.

| 약어 (Full Name) | 위협 유형 (Threat Category) | 대응 보안 속성 | 세부 설명 및 공격 예시 |
|:---:|:---|:---:|:---|
| **S** | **Spoofing**<br>(Identity Spoofing) | **인증**<br>(Authentication) | 공격자가 시스템의 정당한 사용자나 관리자, 프로세스인 척 위장.<br>*Ex: IP Spoofing, Phishing, Session Hijacking* |
| **T** | **Tampering**<br>(Data Tampering) | **무결성**<br>(Integrity) | 데이터가 전송되거나 저장되는 과정에서 악의적으로 수정/삭제됨.<br>*Ex: SQL Injection, Man-in-the-Middle(MitM), Replay Attack* |
| **R** | **Repudiation**<br>(Non-repudiation) | **부인 방지**<br>(Non-repudiation) | 사용자가 특정 행위를 수행했음에도 불구하고 부정할 수 있음.<br>*Ex: 로그 없는 거래, 디지털 서명 부재 환경* |
| **I** | **Information Disclosure**<br>(Data Leak) | **기밀성**<br>(Confidentiality) | 권한이 없는 사용자에게 민감한 정보가 노출됨.<br>*Ex: 디버깅 정보 노출, 개인정보 DB 유출, 패킷 스니핑* |
| **D** | **Denial of Service**<br>(DoS / DDoS) | **가용성**<br>(Availability) | 정상적인 사용자의 서비스 이용을 방해하거나 시스템 자원 고갈.<br>*Ex: SYN Flood, Ransomware, API Rate Limiting 우회* |
| **E** | **Elevation of Privilege**<br>(Privilege Escalation) | **권한 부여**<br>(Authorization) | 제한된 권한을 가진 사용자가 관리자 권한 등 상위 권한을 탈취.<br>*Ex: Buffer Overflow, Token Manipulation, Misconfigured ACL* |

#### 2. DFD 기반 위협 식별 프로세스 및 다이어그램

위협 모델링은 DFD의 각 요소(Element)에 대해 STRIDE를 매핑하여 수행합니다. **Trust Boundary(신뢰 경계)**를 넘나드는 모든 데이터 흐름은 반드시 검증의 대상이 됩니다.

```text
[Analytical Architecture: STRIDE Application on DFD Elements]

    ┌───────────────────┐ ① (Spoofing: User ID Theft?)   ┌──────────────────┐
    │   External Attacker│ ◄─────────────────────────── │   Web App Server │
    │   (Actor)          │                                │   (Process)       │
    └───────────────────┘                                └───────┬──────────┘
          │                                                    │
          │ ② (Tampering: Packet Modify?)                     │ ④ (Elevation: Root Access?)
          ▼                                                    ▼
    ┌───────────────────┐ ③ (Info Disclosure: Sniffing?)    ┌──────────────────┐
    │   Internet Channel│ ────────────────────────►          │   Database DB    │
    │   (Data Flow)     │       ⑤ (DoS: Traffic Jam?)       │   (Data Store)   │
    └───────────────────┘                                    └──────────────────┘
          │                                                    ▲
          │ ⑥ (Repudiation: No Log?)                          │
          └────────────────────────────────────────────────────┘

    * [Key Concept]: 데이터가 신뢰 경계(Trust Boundary)를 가로지르는 지점마다
      상단의 6가지 위협(S~E)을 순회하며 질문(Question)을 던져야 함.
```

**[다이어그램 해설]**
위 다이어그램은 DFD의 주요 구성 요소(외부 개체, 프로세스, 데이터 저장소, 데이터 흐름)에 대해 STRIDE를 어떻게 적용하는지 도식화한 것입니다.
1.  **Spoofing(S)**은 주로 '사용자(User)'나 '외부 시스템'의 신원을 확인하는 단계(Entry Point)에서 발생합니다. 위 다이어그램 ①번 지점에서는 공격자가 관리자의 인증 정보(Cookie/Token)를 도용할 수 있는지 확인해야 합니다.
2.  **Tampering(T)**과 **Information Disclosure(I)**은 데이터가 이동하는 '채널(③)'이나 저장되는 '저장소(④)'에서 발생합니다. 예를 들어, HTTP 프로토콜을 사용하면 중간에서 패킷을 훔쳐보거나(I), 조작할(T) 위험이 있으므로 HTTPS(TLS) 적용이 필수적입니다.
3.  **Denial of Service(D)**는 모든 요소에 해당하지만, 특히 '채널'의 대역폭이나 '프로세스'의 연산 자원을 고갈시키는 공격(⑤)에 대해 검증해야 합니다.
4.  **Elevation of Privilege(E)**는 데이터 처리 권한이 필요한 '프로세스'나 '데이터베이스 접근' 단계(②, ④)에서 주로 검토합니다. 일반 사용자 권한으로 관리자 기능을 호출하는 버그가 있는지 분석합니다.

#### 3. 핵심 수식 및 알고리즘
위협 모델링의 결과물은 위험(Risk)을 정량화하여 판단해야 합니다. 일반적으로 다음과 같은 위험도 산정 공식을 사용합니다.

$$ Risk = Probability (Likelihood) \times Impact (Damage) $$

*   **Probability (발생 가능성)**: 공격 난이도, 공격자의 동기, 필요한 기술 수준 등을 고려.
*   **Impact (영향도)**: 데이터 유출 피해 규모, 서비스 중단 시간, 금전적 손실, 브랜드 이미지 타격 등을 고려.

**코드: 위협 분석 슈도코드 (Pseudo-code)**
```python
# 위협 모델링 자동화 분석 로직 예시
function analyze_threat(process_element, trust_boundary):
    threats = []
    
    # 신뢰 경계를 넘는지 확인 (STRIDE 적용 대상 선정)
    if crosses_trust_boundary(process_element, trust_boundary):
        
        # [S]poofing 검사
        if not has_mfa(process_element):
            threats.append("Spoofing: No Multi-Factor Authentication detected.")
            
        # [T]ampering 검사
        if not uses_encrypted_channel(process_element):
            threats.append("Tampering: Data sent over clear text channel.")
            
        # [I]nformation Disclosure 검사
        if logs_sensitive_data(process_element):
            threats.append("Info Disclosure: Sensitive data in logs.")
            
        # [D]oS 검사
        if no_rate_limiting(process_element):
            threats.append("DoS: No API throttling configured.")
            
        # [E]levation 검사
        if has_admin_logic(process_element):
            threats.append("EoP: Verify strict access control for admin functions.")
            
    return calculate_risk_score(threats)
```

**📢 섹션 요약 비유**
> 마치 의사가 환자의 혈관(데이터 흐름) 따라 흐르는 피를 검사하여, 막힌 구간이나 터질 위험이 있는 혈관(취약점)을 찾아내고 어떤 약(완화책)을 처방할지 결정하는 진단 과정과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기법 비교: STRIDE vs PASTA vs DREAD

위협 모델링은 다양한 방법론이 존재하며, 목적에 따라 적절히 선택하거나 병행해야 합니다.

| 구분 | **STRIDE** | **PASTA** (Process for Attack Simulation and Threat Analysis) | **DREAD** (Risk Assessment Model) |
|:---:|:---|:---|:---|
| **성격** | 분류 중심 (Taxonomy) | 프로세스 중심 (Risk-centric) | 점수 산정 중심 (Scoring) |
| **주요 목표** | "어떤 유형인가?" (What) | "비즈니스 영향은 무엇인가?" (So What) | "위험도가 얼마나 높은가?" (How much) |
| **대상** | 모든 시스템 설계 요소 | 자산 중심의 위험 분석 | 식별된 특정 취약점 |
| **핵심 프로세스** | DFD 작성 → 요소별 STRIDE 매핑 | 7단계(정의~완화) 진행 | Damage, Reproducibility, Exploitability 등 5가지 지표 점수화 |
| **시너지** | 초기 설계 단계에서 취약점을 빠르게 식별 | 보안과 비즈니스 목표를 연결 | 식별된 위협의 처리 우선순위 결정 |

#### 2. 타 과목 융합: 네트워크 및 아키텍처 (OS/Network)

위협 모델링은 OS의 메모리 보안 개념과 네트워크의 통신 보안 개념을 아키텍처 수준에서 통합합니다.

*   **OS 융합 (OS Context)**:
    *   **Elevation of Privilege(E)**: 공격자가 버퍼 오버플로우(Buffer Overflow)나 레이스 컨디션(Race Condition)과 같은 OS 레벨의 취약점을 이용해 **Kernel Mode** 권한을 얻는 시나리오를 모델링합니다. 즉, 프로세스의 권한 분리(Principle of Least Privilege)가 제대로 설계되었는지 검증합니다.
*   **네트워크 융합 (Network Context)**:
    *   **Spoofing(S) / Tampering(T)**: OSI 7계층에서 **L2(MAC Spoofing)**, **L3(IP Spoofing)**, **L7(Session Hijacking)** 공격이 가능한지를 분석합니다. 네트워크 아키텍트는 **TLS 1.3**, **IPsec**, **MACsec** 등의 프로토콜을 어디에 적용하여 무결성과 인증을 보장할지 설계해야 합니다.

#### 3. 다각도 분석: 정량적 의사결정 지표

단순히 "보안이 취약하다"라고 말하는 것이 아니라, 비즈니스 임팩트를 수치화하여 제시해야 합니다.

| 재무적 지표 | 설명 | 위협 모델링의 영향 |
|:---:|:---|:---|
| **ROI** (Return on Investment) | 보안 투자 대비 절감 비용 | 설계 단계 수정 비용: \\$1 <br> 운영 단계 수정 비용: \\$100+ (IBM 데이터) |
| **ALE** (Annualized Loss Expectancy) | 연간 예상 손실액 | ALE = SLE(Single Loss Expectancy) × ARO(Annual Rate of Occurrence) <br> 위협 모델링을 통해 ARO를 낮춤 |
| **MTTR** (Mean Time To Recovery) | 평균 복구 시간 | 재해 복구 계획(Disaster Recovery)을 설계에 미리 반영하여 MTTR 단축 |

**📢 섹션 요약 비유**
> 마치 건물을 지을 때 내建筑师(STRIDE), 구조 안전 전문가(PASTA), 그리고 자재 가격을 산정하는 건설 경영가(DREAD)가 협의회를 열어, 안전함과 비용 효율성 모두를 잡는 통합 설계를 하는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 전자상거래 결제 모듈 설계