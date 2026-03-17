+++
title = "21. DNS 보안 (DNS Security)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["DNS-Security", "DNSSEC", "DNS-over-HTTPS", "DNS-over-TLS", "DNS-Cache-Poisoning"]
draft = false
+++

# DNS 보안 (DNS Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DNS 보안은 **"DNS 인프라를 **보호**하는 **기술 모음"**으로, **DNSSEC**(Digital Signature)로 **데이터 무결성**을 **보증**하고 **DoH**(DNS-over-HTTPS), **DoT**(DNS-over-TLS)로 **쿼리 암호화**하며 **DNS Cache Poisoning**을 **방지**한다.
> 2. **취약점**: **DNS는 **원래 **보안**을 **고려**하지 **않아** **스푸핑**(Spoofing), **Cache Poisoning**, **DNS Tunneling**, **Amplification Attack**에 **취약**하며 **Transaction ID**(16비트)만으로는 **충분하지 **않다.
> 3. **융합**: **DNSSEC**(RFC 4033-4035)가 **서명**된 **RRSIG**(Resource Record Signature)를 **제공**하고 **DoH/DoT**가 **Privacy**를 **강화**하며 **EDNS0**(Extension Mechanisms)가 **쿠키**를 **추가**하여 **Spoofing을 **방지**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
DNS 보안은 **"DNS 인프라를 보호하는 기술"**이다.

**DNS 보안 대상**:
- **무결성**: 데이터 위변조 방지
- **기밀성**: 쿼리 내용 보호
- **가용성**: DDoS 방어
- **인증**: 응답 출처 확인

---

## Ⅱ. 아키텍처 및 핵심 원리

### DNS Cache Poisoning 공격

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         DNS Cache Poisoning                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Cache Poisoning 공격]
    Victim Resolver         ─────── Query ───────→  Auth Server
                          │
                         Attacker
                          ──────── Spoofed Response (ID: 12345) ────────→
                                  (Fake IP: 5.6.7.8)

    → Resolver가 Fake IP를 Cache에 저장
    → 이후 example.com은 5.6.7.8로 연결 (악성 서버)
```

### DNSSEC 체인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         DNSSEC 체인                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Root Zone (.)
      DNSKEY: KSK-Root (ZSK-Root)
      DS: Hash of TLD Key
            │ Signed by
            ▼
    TLD Zone (com)
      DNSKEY: KSK-com (ZSK-com)
      DS: Hash of example.com Key
            │ Signed by
            ▼
    Zone (example.com)
      DNSKEY: ZSK-example.com
      RRSIG: A record Signature
      A: 1.2.3.4
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### DNS 보안 기술 비교

| 기술 | 목적 | 포트 | 장점 | 단점 |
|------|------|------|------|------|
| **DNSSEC** | 무결성 | 53/UDP | 위변조 방지 | 복잡함 |
| **DoT** | 기밀성 | 853/TCP | 암호화 | ISP 차단 가능 |
| **DoH** | 기밀성 | 443/TCP | 숨김 | 오버헤드 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: BIND9 DNSSEC 설정
**상황**: DNS 보안 강화
**판단**:

```conf
// /etc/named/conf.options
options {
    dnssec-validation auto;     // DNSSEC 유효성 검사
    dnssec-lookaside auto;      // 신뢰 앵커 자동

    // DNS-over-TLS
    forward tls {
        1.1.1.1;                // Cloudflare
        8.8.8.8;                // Google
    };
};
```

---

## Ⅴ. 기대효과 및 결론

### DNS 보안 기대 효과

| 효과 | 보안 없음 | 보안 적용 |
|------|----------|----------|
| **위변조** | 가능 | 방지 (DNSSEC) |
| **도청** | 가능 | 방지 (DoH/DoT) |
| **Privacy** | 없음 | 강화 |

### 미래 전망

1. **DoH3**: HTTP/3 기반
2. **Oblivious DNS**: 중앙 서버 제거
3. **Blockchain**: 분산 DNS

### ※ 참고 표준/가이드
- **RFC 4033**: DNSSEC
- **RFC 8484**: DoH
- **RFC 7858**: DoT

---

## 📌 관련 개념 맵

- [DNS](../2_dns/1_dns_overview.md) - DNS 기초
- [TLS](../4_security/15_tls.md) - 암호화
- [네트워크 보안](../4_security/1_security_overview.md) - 보안 개요
