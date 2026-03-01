+++
title = "인증 (Authentication)"
date = 2025-03-01

[extra]
categories = "security-cryptography"
+++

# 인증 (Authentication)

## 핵심 인사이트 (3줄 요약)
> **사용자/시스템의 신원을 확인**하는 보안 절차. 지식/소유/생체 기반 3요소 인증. MFA(다중 요소 인증)로 보안 강화.

## 1. 개념
인증(Authentication)은 **사용자나 시스템이 주장하는 신원이 사실인지 확인**하는 과정이다. "너가 누구인지 증명해라"를 검증하는 것이다.

> 비유: "출입증 검사" - 사원증, 지문, 비밀번호로 본인 확인

## 2. 인증 요소 (3가지)

```
┌────────────────────────────────────────────────────────┐
│                  인증 3요소 (MFA)                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 지식 기반 (Something you know)                     │
│     ┌────────────────────────────────────────────┐    │
│     │ • 비밀번호                                 │    │
│     │ • PIN 번호                                │    │
│     │ • 보안 질문                               │    │
│     │ • 패턴                                    │    │
│     └────────────────────────────────────────────┘    │
│                     ↓                                  │
│  2. 소유 기반 (Something you have)                     │
│     ┌────────────────────────────────────────────┐    │
│     │ • 스마트폰                                │    │
│     │ • OTP 토큰                               │    │
│     │ • 스마트카드                              │    │
│     │ • 보안 키 (YubiKey)                       │    │
│     └────────────────────────────────────────────┘    │
│                     ↓                                  │
│  3. 생체 기반 (Something you are)                      │
│     ┌────────────────────────────────────────────┐    │
│     │ • 지문                                    │    │
│     │ • 얼굴 인식                               │    │
│     │ • 홍채/망막                               │    │
│     │ • 음성                                    │    │
│     │ • 정맥                                    │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  MFA (Multi-Factor Authentication):                   │
│  2가지 이상 요소 조합 = 강력한 인증                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 인증 방식 비교

```
┌────────────────────────────────────────────────────────┐
│                  인증 방식 비교                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 비밀번호                                           │
│     장점: 간편, 보편적                                 │
│     단점: 유추 가능, 재사용, 피싱                      │
│                                                        │
│  2. OTP (One-Time Password)                           │
│     - 시간 기반 (TOTP): 30초마다 변경                 │
│     - 이벤트 기반 (HOTP): 사용 시마다 변경            │
│     장점: 일회용, 유출 위험 낮음                       │
│     단점: 기기 필요                                    │
│                                                        │
│  3. 생체 인식                                          │
│     장점: 분실 위험 없음, 편리                         │
│     단점: 변경 불가, 프라이버시                        │
│                                                        │
│  4. 공개키 인증서 (PKI)                               │
│     - 디지털 인증서 기반                               │
│     장점: 강력한 인증                                  │
│     단점: 복잡, 비용                                   │
│                                                        │
│  5. SSO (Single Sign-On)                              │
│     - 한 번 로그인으로 여러 서비스 이용               │
│     장점: 편리                                         │
│     단점: 단일 실패 지점                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 인증 프로토콜

```
┌────────────────────────────────────────────────────────┐
│                  주요 인증 프로토콜                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. OAuth 2.0                                         │
│     - 권한 위임 프로토콜                               │
│     - "구글로 로그인"                                  │
│     - Access Token, Refresh Token                      │
│                                                        │
│  2. OpenID Connect (OIDC)                             │
│     - OAuth 2.0 + 인증                                 │
│     - ID Token (JWT)                                   │
│     - 사용자 정보 제공                                 │
│                                                        │
│  3. SAML (Security Assertion Markup Language)         │
│     - 기업용 SSO                                       │
│     - XML 기반                                         │
│     - IdP, SP 구조                                     │
│                                                        │
│  4. Kerberos                                          │
│     - 티켓 기반 인증                                   │
│     - Windows 도메인                                   │
│     - KDC (Key Distribution Center)                   │
│                                                        │
│  5. FIDO2 / WebAuthn                                  │
│     - 비밀번호 없는 인증                               │
│     - 생체인식, 보안키                                 │
│     - 공개키 기반                                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import time

class AuthFactor(Enum):
    PASSWORD = "비밀번호"
    OTP = "OTP"
    BIOMETRIC = "생체인식"
    SECURITY_KEY = "보안키"

@dataclass
class User:
    """사용자"""
    user_id: str
    username: str
    password_hash: str
    otp_secret: str = ""
    biometric_hash: str = ""
    security_key_id: str = ""
    failed_attempts: int = 0
    locked: bool = False
    mfa_enabled: bool = False

@dataclass
class Session:
    """세션"""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    mfa_verified: bool = False

class PasswordManager:
    """비밀번호 관리"""

    @staticmethod
    def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
        """비밀번호 해시"""
        if salt is None:
            salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed, salt

    @staticmethod
    def verify_password(password: str, salt: str, stored_hash: str) -> bool:
        """비밀번호 검증"""
        hashed, _ = PasswordManager.hash_password(password, salt)
        return hashed == stored_hash

    @staticmethod
    def check_strength(password: str) -> Dict:
        """비밀번호 강도 확인"""
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("8자 이상 필요")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("대문자 포함 필요")

        if any(c.islower() for c in password):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("숫자 포함 필요")

        if any(c in "!@#$%^&*" for c in password):
            score += 1
        else:
            feedback.append("특수문자 포함 권장")

        strength = ["매우 약", "약", "보통", "강함", "매우 강함"][min(score, 4)]

        return {'score': score, 'strength': strength, 'feedback': feedback}

class OTPGenerator:
    """OTP 생성기 (TOTP 시뮬레이션)"""

    @staticmethod
    def generate_secret() -> str:
        """시크릿 생성"""
        return secrets.token_hex(10)

    @staticmethod
    def generate_code(secret: str) -> str:
        """OTP 코드 생성"""
        # 실제로는 시간 기반 알고리즘
        time_slice = int(time.time() / 30)
        code_input = f"{secret}{time_slice}"
        hash_result = hashlib.sha256(code_input.encode()).hexdigest()
        return hash_result[:6]

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """OTP 검증"""
        expected = OTPGenerator.generate_code(secret)
        return expected == code

class AuthenticationService:
    """인증 서비스"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.max_attempts = 5
        self.session_timeout = 3600  # 1시간

    def register_user(self, username: str, password: str) -> User:
        """사용자 등록"""
        # 비밀번호 강도 확인
        strength = PasswordManager.check_strength(password)
        if strength['score'] < 3:
            print(f"비밀번호 강도 부족: {strength['feedback']}")

        password_hash, salt = PasswordManager.hash_password(password)
        otp_secret = OTPGenerator.generate_secret()

        user = User(
            user_id=f"U{len(self.users)+1:05d}",
            username=username,
            password_hash=f"{salt}:{password_hash}",
            otp_secret=otp_secret
        )
        self.users[username] = user
        print(f"[등록] {username} 님 가입 완료")
        return user

    def enable_mfa(self, username: str):
        """MFA 활성화"""
        user = self.users.get(username)
        if user:
            user.mfa_enabled = True
            print(f"[MFA] {username} 2단계 인증 활성화")

    def authenticate_password(self, username: str, password: str) -> Optional[str]:
        """1단계 인증 (비밀번호)"""
        user = self.users.get(username)
        if not user:
            return None

        if user.locked:
            print("계정이 잠겼습니다")
            return None

        salt, stored_hash = user.password_hash.split(':')

        if not PasswordManager.verify_password(password, salt, stored_hash):
            user.failed_attempts += 1
            if user.failed_attempts >= self.max_attempts:
                user.locked = True
                print("계정이 잠겼습니다")
            return None

        user.failed_attempts = 0

        # 세션 생성
        session = Session(
            session_id=secrets.token_hex(32),
            user_id=user.user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self.session_timeout),
            mfa_verified=not user.mfa_enabled
        )
        self.sessions[session.session_id] = session

        if user.mfa_enabled:
            print(f"[1단계 완료] OTP를 입력하세요")
        else:
            print(f"[로그인 완료] {username}님 환영합니다")

        return session.session_id

    def authenticate_otp(self, session_id: str, otp_code: str) -> bool:
        """2단계 인증 (OTP)"""
        session = self.sessions.get(session_id)
        if not session:
            return False

        user = next((u for u in self.users.values() if u.user_id == session.user_id), None)
        if not user:
            return False

        if OTPGenerator.verify_code(user.otp_secret, otp_code):
            session.mfa_verified = True
            print(f"[로그인 완료] {user.username}님 환영합니다")
            return True

        print("OTP가 올바르지 않습니다")
        return False

    def verify_session(self, session_id: str) -> bool:
        """세션 검증"""
        session = self.sessions.get(session_id)
        if not session:
            return False

        if datetime.now() > session.expires_at:
            del self.sessions[session_id]
            return False

        return session.mfa_verified


# 사용 예시
print("=== 인증 시스템 시뮬레이션 ===\n")

auth = AuthenticationService()

# 사용자 등록
print("--- 사용자 등록 ---")
user = auth.register_user("alice", "Secure123!")
auth.enable_mfa("alice")

# 비밀번호 강도 확인
print("\n--- 비밀번호 강도 ---")
result = PasswordManager.check_strength("password")
print(f"'password': {result['strength']} - {result['feedback']}")

result = PasswordManager.check_strength("Secure123!")
print(f"'Secure123!': {result['strength']}")

# 1단계 인증
print("\n--- 1단계 인증 (비밀번호) ---")
session_id = auth.authenticate_password("alice", "Secure123!")

# 2단계 인증 (OTP)
if session_id and not auth.sessions[session_id].mfa_verified:
    print("\n--- 2단계 인증 (OTP) ---")
    user = auth.users["alice"]
    otp_code = OTPGenerator.generate_code(user.otp_secret)
    print(f"OTP 코드: {otp_code}")
    auth.authenticate_otp(session_id, otp_code)

# 세션 검증
print("\n--- 세션 검증 ---")
print(f"세션 유효: {auth.verify_session(session_id)}")
