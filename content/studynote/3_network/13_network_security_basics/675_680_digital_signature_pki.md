+++
title = "675-680. 전자서명과 PKI (Public Key Infrastructure)"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 675
+++

# 675-680. 전자서명과 PKI (Public Key Infrastructure)

### # 전자서명과 공개키 기반 구조
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비대칭 암호화의 역함수를 이용하여 데이터의 무결성과 송신자 인증을 수학적으로 증명하는 전자서명과, 이를 지원하는 신뢰 계층 구조.
> 2. **가치**: 비대면 환경에서 위조 불가능한 '디지털 신분증'을 제공하여 전자 상거래 및 금융 거래의 법적 효력(부인 방지)을 보장하고 비용 절감.
> 3. **융합**: TLS/SSL(Transport Layer Security/Secure Sockets Layer) 핸드셰이크의 핵심이자, 블록체인의 트랜잭션 검증, 코드 사이닝(Code Signing) 등 현대 보안의 근간.

+++

### Ⅰ. 개요 (Context & Background)

전자서명(Digital Signature)과 PKI(Public Key Infrastructure)는 개방형 네트워크 환경에서 '신뢰'를 기술적으로 구현한 장치입니다.

**💡 비유**
종이 문명 시대의 '직인'과 '공증인 시스템'을 디지털 세상으로 가져온 것입니다. 내 도장(개인키)은 나만 가지고 있어서 남이 흉내 낼 수 없고, 정부(CA)가 발급한 신분증(인증서)은 내 도장이 진짜임을 보증해줍니다.

**등장 배경**
1.  **기존 한계**: 대칭키 암호(DES, AES)는 키 분배 문제와 비밀성은 보장하나 상대방이 누구인지(인증)는 보장하지 못하는 한계가 존재.
2.  **혁신적 패러다임**: Diffie-Hellman과 RSA(Rivest-Shamir-Adleman) 알고리즘의 등장으로 비대칭키(공개키/개인키) 기반의 암호화가 가능해지며, '열쇠'를 공유하지 않고도 보안 통신이 가능해짐.
3.  **현재의 비즈니스 요구**: 전자정부, 전자상거래, 금융 IT 시스템에서 서면 계약과 동등한 법적 효력을 가지는 비대면 인증 및 무결성 검증 수단의 필수성 대두.

**📢 섹션 요약 비유**
> **마치 거대한 고속도로(인터넷)에서 운전을 할 때, 익명의 오토바이가 아니라 차량 번호와 소유자가 확인되는 '등록된 자동차(인증서)'를 몰고, 교통카드(전자서명)를 찍어 통행 기록을 남기는 것과 같습니다.**

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

전자서명과 PKI는 수학적 난제를 기반으로 하는 복잡한 계층 구조를 가집니다.

#### 1. 주요 구성 요소 (Component Table)

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 프로토콜/표준 | 비유 |
|:---|:---|:---|:---|:---|
| **CA** | Certification Authority (인증 기관) | **최상위 신뢰 기관**. 사용자의 신원을 확인하고 인증서(X.509)를 발급하며 자신의 개인키로 서명. Root CA는 스스로 서명(Self-signed). | X.509, RFC 5280 | 시청 구청장 (도장 보유) |
| **RA** | Registration Authority (등록 기관) | **CA의 대리 기관**. 사용자 신원 확인(Domain Validation, EV 등) 및 인증서 발급 요청을 CA로 전달하는 중개자. | CMP (Certificate Management Protocol) | 동사무소 직원 (서류 접수) |
| **Repository** | - | **DB 역할**. 발급된 인증서와 폐기 목록(CRL)을 저장하고 검색을 위해 제공(LDAP/HTTP 서버). | LDAP, HTTP | 열람실 혹은 게시판 |
| **EE** | End Entity (종단 개체) | **사용자/서버**. 인증서를 발급받아 전자서명을 생성하거나 타인의 서명을 검증하는 주체. | CMS/PKCS#7 | 도장을 가진 시민 |
| **CRL/DP** | CRL Distribution Point | **폐기 정보 배포처**. 인증서가 해지되었을 때, 그 정보를 알려주는 곳의 URL. | X.509 v3 Extension | 분실 도장 공고 게시판 |

#### 2. 디지털 인증서 구조 및 전자서명 생성 과정

인증서는 공개키와 소유자 정보를 묶어놓은 '전자 봉투'입니다. 아래는 RSA 기반 서명 생성 및 검증의 전체 메커니즘입니다.

```ascii
[전자서명 생성 및 검증 아키텍처]

       송신자 (Alice)                               수신자 (Bob)
      +-------------+                            +-------------+
      |  Plain Text |                            |             |
      +-------------+                            |             |
             |                                    |             |
             v                                    v             |
   (1) Hash Function                     (1) Extract Public Key
             |                                    |      from
             v                                    |   Certificate
   [Digest (e.g. SHA-256)]                       v      (Signed by CA)
             |                            +-------------+
             v                            | Public Key  |
   (2) Sign with Private Key              | (Alice's)   |
   +-------------------------------+      +-------------+
   |  [Digest] encrypted with Priv|             |
   |  Key (RSA/ECDSA)             |             v
   +-------------------------------+      (2) Decrypt Signature
             |                            with Public Key
             v                                    |
   [Digital Signature]                           v
             |                          [Recovered Digest]
             |                                    |
             +-----------+ +----------------------+      (3) Compare
                         |                                    |
             v           v                                    v
   +---------------------------+                +---------------------------+
   |   Send: Data + Signature  | <------------> |   Is Digest1 == Digest2? |
   +---------------------------+    Network    +---------------------------+
                                                         |
                                      +------------------+------------------+
                                      | YES (Valid)      | NO (Tampered)    |
                                      v                  v
                                  [Trusted]          [Reject]
```

**[Diagram 해설]**
1.  **해싱(Hashing)**: 원문(Message)을 SHA-256(Secure Hash Algorithm 256-bit) 등의 해시 함수를 거쳐 고정된 길이의 지문(Digest)을 생성합니다. 이 과정은 일방향(One-way)이므로 원문을 유추할 수 없습니다.
2.  **서명(Signing)**: 송신자는 자신의 **개인키(Private Key)**로 이 지문을 암호화합니다. 이 결과물이 전자서명입니다. 공개키로만 복호화 가능하므로, 개인키를 가진 당사자만이 생성할 수 있습니다.
3.  **검증(Verification)**: 수신자는 송신자의 **공개키(Public Key)**를 이용해 서명을 복호화하여 지문 A를 얻고, 받은 메시지를 다시 해싱하여 지문 B를 얻습니다. A와 B가 일치하면 **무결성(Integrity)**과 **인증(Authentication)**이 확보됩니다.

#### 3. 핵심 알고리즘 및 표준

*   **암호화 알고리즘**:
    *   **RSA**: 소인수 분해의 난제 이용. 키 크기는 2048bit 이상 권장.
    *   **ECDSA (Elliptic Curve Digital Signature Algorithm)**: 타원 곡선 암호 기반. RSA보다 키 크기가 작고 연산 속도가 빨라 모바일/IoT 환경에서 선호됨.
*   **해시 알고리즘**: SHA-256, SHA-3 (MD5, SHA-1은 충돌 저항성 문제로 폐기 권고).
*   **인증서 포맷**: **X.509 v3** (ITU-T 표준). ASN.1(Abstract Syntax Notation One) 방식으로 인코딩되어 보통 `.cer`, `.crt`, `.pem` 파일로 저장됨.

```python
# [Python Code Snippet] Cryptography 라이브러리를 이용한 서명 검증 로직 예시
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def verify_signature(public_key, message, signature):
    """
    공개키를 이용하여 메시지의 서명을 검증하는 함수
    :param public_key: 송신자의 공개키 객체
    :param message: 원문 바이트 (bytes)
    :param signature: 전자서명 바이트 (bytes)
    """
    try:
        # 공개키로 서명 복호화 및 해시 비교
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True  # 검증 성공 (무결성 O, 인증 O)
    except InvalidSignature:
        return False # 검증 실패 (위조 또는 변조)
```

**📢 섹션 요약 비유**
> **물건을 배송할 때 받는 '택배 영수증'과 같습니다.**
> 1. **해시**: 물건의 상태(무게, 모양)를 사진으로 찍어 기록하는 것.
> 2. **전자서명**: 고객이 그 영수증에 자필 서명(개인키)을 하는 것.
> 3. **검증**: 배송 기사가 도착해서 서명이 진짜인지 확인하고, 물건 상태가 사진이랑 같은지 비교하는 과정입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

인증서의 유효성을 검증하는 방식은 보안성과 효율성 사이의 트레이드오프(Trade-off)를 보여줍니다.

#### 1. 인증서 폐기 검증 방식 비교 (CRL vs OCSP)

| 구분 | **CRL (Certificate Revocation List)** | **OCSP (Online Certificate Status Protocol)** |
|:---|:---|:---|
| **작동 방식** | 주기적으로 CA 서버로부터 폐기된 인증서 목록(블랙리스트)을 **다운로드**하여 로컬에서 검색. | 실시간으로 OCSP 응답자(Responder)에 **질의(Query)**하여 "Good/Revoked" 상태를 확인. |
| **장점** | 검증이 로컬에서 이루어지므로 네트워크 지연 시에도 빠름. 구현이 간단함. | 가장 최신의 상태를 반영함. 목록 전체를 다운로드하지 않아 **트래픽 절약**. |
| **단점** | 목록이 커질수록 다운로드 시간/파싱 비용 증가. 업데이트 주기(TTL) 동안 유효하지 않은 인증서를 유효하다고 인식할 수 있음. | 검증할 때마다 네트워크 I/O 발생. **상태 노출 가능성**(Privacy Issue)으로 인해 사용자가 어떤 사이트에 접속하는지 추적될 수 있음. |
| **성능 (Latency)** | 첫 검증 시 다소 느림 (다운로드), 이후 빠름. | 매번 왕복(RTT)이 필요하나, HTTP를 사용하므로 가볍고 빠름. |
| **융합 적용** | 내부망 환경이나 클라이언트 리소스가 제한적인 레거시 시스템에 적합. | **OCSP Stapling** 기술과 결합하여 웹 서버 성능을 최적화하는데 사용됨. |

#### 2. 타 영역과의 융합 (Convergence)

*   **네트워크 (TLS/SSL)**: 웹 브라우저가 HTTPS 사이트에 접속할 때, 서버는 인증서를 제시합니다. 브라우저는 자신의 Root Store에 내장된 CA의 공개키로 이 인증서를 검증하고, **OCSP**를 통해 폐기 여부를 확인합니다.
*   **보안 (Code Signing)**: 앱 개발사가 배포하는 실행 파일(.exe, .apk)에 자신의 인증서로 서명합니다. 사용자는 이 앱이 악의적으로 변조되지 않았음을 확인하고 설치합니다.
*   **블록체인 (Blockchain)**: 비트코인 등의 암호화폐에서 ECDSA를 사용하여 거래(Transaction)의 서명을 생성합니다. 이때 '중개자(CA)' 없이 수학적 증명만으로 신뢰가 형성되므로 탈중앙화된 PKI라고 볼 수 있습니다.

**📢 섹션 요약 비유**
> **CRL은 '범죄자 수배지'를 집에서 독자(브라우저)로 구독하여 확인하는 방식이고, OCSP는 경찰서(OCSP 서버)에 전화를 걸어 "이 사람 수배됐나요?"라고 물어보는 방식입니다.**

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 시스템에서 PKI를 도입할 때는 보안 수준, 비용, 운영 효율성을 모두 고려해야 합니다.

#### 1. 실무 시나리오 및 의사결정

**Case 1: 대규모 전자상거래 플랫폼의 인증서 갱신**
*   **문제**: 수천 개의 마이크로서비스에 TLS 인증서가 설치되어 있음. 만료 1주일 전에 일괄 갱신 필요.
*   **의사결정**: 수동 갱신은 불가능. **ACME (Automated Certificate Management Environment)** 프로토콜을 사용하는 **Let's Encrypt** 또는 사설 **PKI 자동화 도구**(예: HashiCorp Vault)를 도입하여 인증서 발급 및 갱신 자동화 구성.

**Case 2: 폐쇄망(Private Network) 시스템 보안**
*   **문제**: 인터넷 연결이 안 되는 금융사 내부망에서 서버 간 통신 보안 필요.
*   **의사결정**: 외부 CA(CA/Browser Forum 포함)를 이용할 수 없음. 자체 **Root CA**를 구축하고, 모든 내부 서버/클라이언트에 신뢰된 Root 인증서를 배포(Self-Signed CA). 관리 포인트가 증가하지만 비용 절감 및 통제권 확보 가능.

#### 2. 도입 체크리스트 (Checklist)

*   **기술적**: 
    *   키 길이 보장 (RSA 2048이상, ECC P-256 이상).
    *   **HSM (Hardware Security Module)** 도입을 통한 개인키 절대 보호(일반 서버 메모리에 평문 키 존재 금지).
    *   **TSL/SSL 설정 최적화** (Forward Secrecy 지원, 낡은 Cipher Suite 비활성화).
*   **운영/보안적**:
    *   **Root CA 물리/논리적 격리**: 루트 키는 오프라인(Offline) Air-gapped 환경