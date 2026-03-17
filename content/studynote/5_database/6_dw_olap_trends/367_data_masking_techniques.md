+++
title = "367. 데이터 마스킹 (Static vs Dynamic) - 필요한 만큼만 보여주기"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 367"
+++

# 367. 데이터 마스킹 (Static vs Dynamic) - 필요한 만큼만 보여주기

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 마스킹(Data Masking)은 민감 정보(PERSONALLY IDENTIFIABLE INFORMATION, PII)를 포함하는 데이터 필드의 내용을 변환하여, 데이터 포맷이나 길이는 유지하면서 실제 정보를 노출시키지 않는 비식별화(De-identification) 기술이다.
> 2. **가치**: 개인정보보호법(GDPR, CCPA 등) 및 벌금 규정(상장폐지, 과징금) 등의 리스크를 회피하면서, 개발(DEV), 테스트(TEST), 데이터 분석(DW) 환경에서 **실무와 유사한 데이터(Production-like Data)**를 안전하게 활용할 수 있게 한다.
> 3. **융합**: 단순 가공을 넘어 데이터베이스(DB)의 접근제어(ACCESS CONTROL), 가상화(VIRTUALIZATION), 및 데이터 거버넌스(GOVERNANCE) 체계와 통합되어 라이프사이클 전반의 보안을 강화한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
데이터 마스킹은 민감 데이터를 비식별자(Anonymous Data)로 변환하는 보안 기술이다. 암호화(ENCRYPTION)와 달리 복호키(Decryption Key)를 사용하지 않거나, 사용하더라도 원본값으로 복구가 어려운 일방향성을 가진다. 핵심은 **'형태(Morphology)'는 유지하면서 '의미(Meaning)'는 제거**하는 데 있다.

**2. 💡 비유: 방송국의 모자이크 처리**
마치 뉴스에서 범죄자의 얼굴이나 신원을 알 수 있는 문서에 모자이크 처리를 하여, 사건의 심각성(데이터의 맥락)은 전달하면서 신원은 보호하는 것과 같다.

**3. 등장 배경**
과거에는 테스트 환경 구축을 위해 운영(OPERATIONAL) DB를 그대로 복사하여 사용했다. 그러나 이는 고객 정보 유출 사고의 주요 원인이 되었다.
① **기존 한계**: 운영 데이터 그대로 복사 시 내부자 혹은 외부 해커의 테스트 서버 탈취 → 대규모 유출 사고 발생.
② **혁신적 패러다임**: **Privacy by Design (설계 단계에서의 프라이버시 보호)** 개념 도입. 데이터를 생성/이관하는 단계에서 자동으로 마스킹을 수행하는 프로세스 정착.
③ **현재 요구**: 단순한 개발팀 지원을 넘어, AI 학습용 데이터셋 구축, 금융권의 마이데이터(MyData) 서비스 등 데이터 활용과 보안의 균형이 절실한 상황.

**4. 📢 섹션 요약 비유**
> 데이터 마스킹은 **'약을 만들 때 알약의 모양은 똑같이 유지하되, 성분은 비타민으로 바꿔버리는 조제 과정'**과 같습니다. 겉보기에는 진짜 약(데이터) 같아서 복용 테스트(업무 테스트)를 할 수는 있지만, 먹어도 부작용(유출 피해)이 없도록 만드는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 (5개+ 모듈)**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Masking Engine** | 마스킹 처리의 핵심 코어 | 규칙(Algorithm)에 따라 데이터를 변환하는 라이브러리 | Java Regex, Python Pandas | 번역기 |
| **Discovery Agent** | 민감 데이터 자동 탐지 | Metadate를 스캔하거나 Regex로 주민번호/카드 패턴 식별 | Regex, NLP | 금속 탐지기 |
| **Policy Manager** | 마스킹 규칙 정의 | 누가, 언제, 어떤 컬럼을 어떻게(노출/가림) 볼지 설정 | RBAC (Role-Based Access Control) | 교통정리 관제센터 |
| **Persistent Layer (DB)** | 데이터 저장 | 원본 데이터(Sanitized Data) 또는 마스킹된 데이터 저장 | RDBMS (Oracle, MySQL) | 창고 |
| **Proxy / JDBC Driver** | 동적 마스킹 중계 | Application과 DB 사이에서 SQL을 가로채어 결과를 변조 | JDBC, ODBC, Proxy Protocol | 가면 안내원 |

**2. ASCII 구조 다이어그램: Static vs Dynamic Flow**

아래 다이어그램은 **SDM(Static Data Masking)**과 **DDM(Dynamic Data Masking)**의 처리 흐름을 시각적으로 비교한 것이다.

```text
      [ 1. STATIC DATA MASKING (SDM) FLOW ]
      (ETL / Backup Process)

 [ Production DB ]           [ Masking Engine ]           [ Test/Dev DB ]
 (Real: PII Data)   ────▶   [ Copy & Transform ]  ────▶   (Fake: Masked Data)
  [Hong Gildong]              [Substitution]               [Kim Chul-soo]
  [880101-1234567]            [Shuffling]                  [910202-9876543]
  * 원본 데이터가 복제되는 시점에 물리적으로 변경됨 (Permanent Change)


      [ 2. DYNAMIC DATA MASKING (DDM) FLOW ]
      (Real-time Query Process)

 [ User Application ]             [ Database Security Layer ]              [ Production DB ]
 (Business Logic)    ──▶ SQL ──▶  [ Proxy / View / Policy ]   ──▶ SQL ──▶  (Real: PII Data)
                                     (SELECT * FROM users)
                                            │
                                            ▼
                              ┌───────────────────────────────┐
                              │ "Who is the requester?"        │
                              │ - Role: Admin   → Full View    │
                              │ - Role: CallCenter → Mask View │
                              └───────────────────────────────┘
                                            │
                                            ▼ (Return Set)
 [ Admin ] ────▶ [Hong Gildong / 880101-1234567 ] (Original)
 [ Caller ] ────▶ [Hong ****   / 880101-1****** ] (On-the-fly)
 * 데이터 자체는 변경되지 않음, 전송 과정에서만 필터링
```

**3. 다이어그램 해설**
위 도해는 마스킹이 적용되는 **'타이밍'**과 **'저장 위치'**의 차이를 보여준다.
① **SDM (Static)**은 **ETL (Extract, Transform, Load)** 과정이나 백업 복구 시점에 작동한다. 테스트 환경을 만들기 위해 운영 DB를 복사할 때, **Discovery Agent**가 민감 컬럼을 식별하고 **Masking Engine**이 가짜 데이터로 치환한 뒤 테스트 DB에 저장한다. 이후 테스트 DB 내부에는 실제 이름이 존재하지 않는다.
② **DDM (Dynamic)**은 **RDBMS의 View(Virtual Table)** 혹은 **JDBC Proxy** 계층에서 작동한다. 사용자가 `SELECT` 쿼리를 날리면 DBMS는 사용자의 권한(Role)을 확인하고, 데이터를 디스크에서 가져온 직후 메모리 상에서 `REDACT` 함수를 적용하여 클라이언트에게 전송한다. 따라서 디스크의 데이터는 원본 그대로 보존된다.

**4. 심층 동작 원리 (5단계)**
1. **Discovery (식별)**: DB 스키마 및 데이터를 샘플링하여 정규식(Regex)으로 PII(개인식별정보) 패턴 매칭 (예: `\d{6}-[1-4]\d{6}`).
2. **Policy Assignment (정책 할당)**: 발견된 컬럼에 마스킹 규칙 부여 (예: `jumin` 컬럼 → `MASK_MIDDLE(6)`).
3. **Execution (실행)**:
   - **Static**: `UPDATE users SET name = DBMS_RANDOM.STRING('X', 10) WHERE ...`
   - **Dynamic**: `CREATE SECURITY POLICY mask_policy ADD MASKING FILTER ...`
4. **Validation (검증)**: 마스킹된 데이터가 포맷(길이, 자료형)을 유지하고, 애플리케이션 오류를 일으키지 않는지 확인.
5. **Audit (감사)**: 누가, 언제, 어떤 민감 데이터를 조회했는지 로그(Log)를 기록.

**5. 핵심 알고리즘 (Pseudo Code)**

```python
# Python style Pseudo-code: Dynamic Masking Logic
def apply_dynamic_masking(data, user_role):
    # 원본 데이터 (Example: Credit Card)
    original_value = data['card_no'] 
    
    if user_role == 'ADMIN':
        return original_value
    elif user_role == 'CS_AGENT':
        # 앞 6자리와 뒤 4자리만 노출 (123456-******-7890)
        return f"{original_value[:6]}-******-{original_value[-4:]}"
    else:
        # 모두 마스킹
        return "********-********"

# 시스템에 따라 SQL 레벨에서 수행되어야 성능 저하 최소화 가능
```

**6. 📢 섹션 요약 비유**
> 정적 마스킹은 **'출판되는 책의 인쇄물에 직접 수정액을 칠하는 것'**과 같아서, 한번 찍어내면 교체할 수 없다. 반면 동적 마스킹은 **'스마트 글래스를 쓰고 현장을 보는 것'**과 같아서, 안경 렌즈(소프트웨어 계층) 설정에 따라 현실(원본 데이터)은 그대로 둔 채로 보이는 화면만 바꿀 수 있는 것이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교 (SDM vs DDM)**

| 비교 지표 (Metric) | 정적 마스킹 (SDM) | 동적 마스킹 (DDM) |
|:---|:---|:---|
| **Storage Efficiency** | 저장 공간 2배 소요 (원본+마스킹) | 저장 공간 절약 (원본 1개 유지) |
| **Performance Impact** | **None** (이관 작업 시에만 부하) | **Latency O(1)** (조회 시마다 CPU 연산 발생) |
| **Security Level** | **High** (물리적 분리) | **Medium** (권한 설정 오류 시 노출 위험) |
| **Data Integrity** | 훼손됨 (참조 무결성 제약 필요) | 유지됨 (실제 데이터 존재) |
| **Use Case** | 일괄 작업, 대용량 데이터 웨어하우스 | 실시간 모니터링, 고객센터 조회 |
| **Compliance** | GDPR Right to be Forgotten (영구 삭제) 용이 | GDPR Right to Access (정보 접근권) 보장 |

**2. 과목 융합 관점**
- **보안 (Security)**: **KMS (Key Management System)**와 연동하여 마스킹 규칙 자체를 암호화하여 관리해야 한다. 또한 **RBAC (Role-Based Access Control)** 모델과 강하게 결합되어 있어, 권한이 상승(Escalation)될 경우 마스킹이 풀리는 위험을 방어해야 한다.
- **운영체제/네트워크 (OS/Net)**: 동적 마스킹의 경우 DB 서버 앞단에 **Proxy Server**나 **SQL Gateway**가 위치하므로, 네트워크 트래픽(Latency)에 미치는 영향을 고려해야 한다.

**3. 📢 섹션 요약 비유**
> 보안 계층에서의 융합은 **'보안 경비 시스템과 CCTV의 관계'**와 같습니다. 정적 마스킹은 건물 입구에서 무기를 치우고 들어가는 물리적 검색게이트(WAF)라면, 동적 마스킹은 건물 내부에서 무기 주머니를 자동으로 잠그는 스마트 자물쇠(Smart Lock)와 같습니다. 이 두 가지가 결합될 때 가장 안전한 보안 체계가 완성됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

| 시나리오 (Scenario) | 문제 상황 (Problem) | 의사결정 (Decision) | 이유 (Rationale) |
|:---|:---|:---|:---|
| **A사 금융 앱 개발** | 개발자가 실제 거래 로직을 테스트해야 하지만, 고객 이름과 계좌번호는 볼 수 없어야 함. | **정적 마스킹 (SDM) 선정** | 개발 서버는 물리적으로 분리된 환경이므로, 연산 성능을 100% 살리기 위해 미리 변환된 데이터를 제공한다. |
| **B사 고객센터** | 상담원이 고객 문의를 처리할 때 본인 확인을 위해 주민번호 뒤 2자리만 필요함. | **동적 마스킹 (DDM) 선정** | 운영 DB이며 데이터를 변형하면 안 되고, 상담원의 권한에 따라 실시간으로 화면만 다르게 보여줘야 한다. |
| **C사 AI 모델 학습** | 수천만 건의 빅데이터를 학습시켜야 하지만, 개인정보 포함으로 인한 법적 리스크 우려. | **비식별 조치 (Diffential Privacy + SDM)** | 대량의 데이터를 추출해야 하므로 정적 마스킹 처리 후 데이터 레이크(Datalake)로 적재한다. |

**2. 도입 체크리스트 (Checklist)**

- [ ] **기술적(Technical)**
  - 마스킹 알고리즘이 데이터 포맷(DataType)을 깨뜨리지 않는가? (예: 날짜 필드에 문자열 삽입 금지)
  - **Referential Integrity (참조 무결성)**: 부모 테이블과 자식 테이블의 마스킹 값이 일치하는가? (Foreign Key 오류 방지)
  - 성능: 동적 마스킹 적용 시 쿼리 응답 시간(SLA)이 100ms 이내로 유지되는가?

- [ ] **운영 및 보안(Operational & Security)**
  - **Inverted Mask Attack (역마스킹 공격)** 방지: 여러 테이블의 조인을 통해 원본 데이터를 유추할 수 있는가?
  - 관리자 계정에 대한 이중 인증(MFA) 및 감사 추적(Audit Trail) 적용 여부.
  - 마스킹 키(Key) 분실 시 복구 절차(Disaster Recovery) 수립 여부.

**3. 안티패턴 (Anti-patterns)**
- **Shuffling Attack**: 단순 셔플링(행 섞기)만 사용할 경우, 다른 테이블과 조인(Join)하거나 외부 정보와 결합하여 식별이 가능해진다. (보