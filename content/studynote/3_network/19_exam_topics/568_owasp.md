+++
title = "OWASP (Open Web Application Security Project) - 오픈 웹 애플리케이션 보안 프로젝트"
weight = 568
+++

# OWASP (Open Web Application Security Project) - 오픈 웹 애플리케이션 보안 프로젝트

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 웹 보안 표준/가이드
> 2. **가치**: 보안 베스트 프랙티스
> 3. **융합:** OWASP Top 10, WAF, Secure Coding

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

OWASP은 웹 보안 지식을 공유하는 비영리 단체입니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OWASP                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              OWASP Top 10 (2021)                               │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  A01 Broken Access Control                          │   │ │
│   │   │  A02 Cryptographic Failures                         │   │ │
│   │   │  A03 Injection                                      │   │ │
│   │   │  A04 Insecure Design                                │   │ │
│   │   │  A05 Security Misconfiguration                      │   │ │
│   │   │  A06 Vulnerable Components                          │   │ │
│   │   │  A07 Authentication Failures                        │   │ │
│   │   │  A08 Software/Data Integrity Failures               │   │ │
│   │   │  A09 Logging Failures                               │   │ │
│   │   │  A10 SSRF                                           │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: OWASP Top 10은 웹 보안 취약점의 핵심 목록입니다.

**📢 섹션 요약 비유:** OWASP = 보안 교과서!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 프로젝트 | 설명 |
|:---|:---|
| **Top 10** | 취약점 순위 |
| **ASVS** | 검증 표준 |
| **Testing Guide** | 테스트 가이드 |
| **Code Review** | 코드 리뷰 가이드 |
| **ZAP** | 취약점 스캐너 |

**핵심 알고리즸:** 취약점 식별 → 완화

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**OWASP 활용**

| 용도 | 설명 |
|:---|:---|
| **개발** | Secure Coding |
| **테스트** | Penetration Testing |
| **운영** | WAF 설정 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 개발 → ASVS 적용
**시나리오 2:** 보안 → Top 10 점검
**시나리오 3:** WAF → OWASP CRS

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** OWASP Foundation

---

### 📌 관련 개념 링크**:
- [WAF](./566_waf.md)
- [SQL Injection](./569_sql_injection.md)
- [XSS](./570_xss.md)
