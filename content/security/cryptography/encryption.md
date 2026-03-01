+++
title = "암호화 (Encryption)"
date = 2025-03-01

[extra]
categories = "security-cryptography"
+++

# 암호화 (Encryption)

## 핵심 인사이트 (3줄 요약)
> **데이터를 암호문으로 변환하여 기밀성 보장**. 대칭키(빠름)와 비대칭키(안전한 키 분배)로 분류. AES, RSA, 하이브리드 방식이 실무에서 사용.

## 1. 개념
암호화는 **평문(Plaintext)을 암호문(Ciphertext)으로 변환**하여 권한이 없는 사용자가 내용을 알 수 없게 하는 기술이다.

> 비유: "비밀 편지" - 암호로 써서 받는 사람만 읽을 수 있음

## 2. 암호화 분류

```
┌────────────────────────────────────────────────────────┐
│                   암호화 분류                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 대칭키 암호화 (Symmetric Key)                      │
│     ┌────────────────────────────────────────────┐    │
│     │ 같은 키로 암호화/복호화                     │    │
│     │                                            │    │
│     │ [평문] --키A--> [암호문] --키A--> [평문]   │    │
│     │                                            │    │
│     │ 장점: 빠름                                 │    │
│     │ 단점: 키 분배 문제                         │    │
│     │ 알고리즘: AES, DES, 3DES, ChaCha20        │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 비대칭키 암호화 (Asymmetric Key)                   │
│     ┌────────────────────────────────────────────┐    │
│     │ 공개키와 개인키 쌍 사용                    │    │
│     │                                            │    │
│     │ 암호화: 공개키로 암호화, 개인키로 복호화   │    │
│     │ 서명: 개인키로 서명, 공개키로 검증         │    │
│     │                                            │    │
│     │ 장점: 안전한 키 분배                       │    │
│     │ 단점: 느림                                 │    │
│     │ 알고리즘: RSA, ECC, DSA                   │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  3. 하이브리드 암호화                                   │
│     ┌────────────────────────────────────────────┐    │
│     │ 대칭키로 데이터 암호화                     │    │
│     │ 비대칭키로 대칭키 암호화                   │    │
│     │ → 속도와 안전성 모두 확보                  │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 암호화 모드

```
┌────────────────────────────────────────────────────────┐
│              블록 암호화 모드                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. ECB (Electronic Codebook)                         │
│     - 각 블록 독립 암호화                              │
│     - 같은 평문 → 같은 암호문                          │
│     - 보안 취약                                        │
│                                                        │
│  2. CBC (Cipher Block Chaining)                       │
│     - 이전 암호문과 XOR 후 암호화                      │
│     - IV (초기화 벡터) 필요                           │
│     - 병렬 암호화 불가                                 │
│                                                        │
│  3. CTR (Counter)                                     │
│     - 카운터를 암호화하여 XOR                          │
│     - 병렬 처리 가능                                   │
│     - 랜덤 접근 가능                                   │
│                                                        │
│  4. GCM (Galois/Counter Mode)                         │
│     - CTR + 인증 (AEAD)                               │
│     - 기밀성 + 무결성                                  │
│     - TLS 1.3 기본                                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import hashlib
import secrets
import base64

@dataclass
class KeyPair:
    """키 쌍"""
    public_key: str
    private_key: str

class SimpleSymmetricEncryption:
    """간단한 대칭키 암호화 (시뮬레이션)"""

    def __init__(self):
        self.key = None

    def generate_key(self) -> str:
        """키 생성"""
        self.key = secrets.token_hex(16)  # 128-bit
        return self.key

    def encrypt(self, plaintext: str) -> str:
        """암호화 (XOR 기반 시뮬레이션)"""
        if not self.key:
            raise ValueError("키가 없습니다")

        # 키를 평문 길이만큼 확장
        key_bytes = self.key.encode()
        plain_bytes = plaintext.encode()

        encrypted = []
        for i, byte in enumerate(plain_bytes):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)

        return base64.b64encode(bytes(encrypted)).decode()

    def decrypt(self, ciphertext: str) -> str:
        """복호화"""
        if not self.key:
            raise ValueError("키가 없습니다")

        encrypted = base64.b64decode(ciphertext.encode())
        key_bytes = self.key.encode()

        decrypted = []
        for i, byte in enumerate(encrypted):
            key_byte = key_bytes[i % len(key_bytes)]
            decrypted.append(byte ^ key_byte)

        return bytes(decrypted).decode()

class SimpleAsymmetricEncryption:
    """간단한 비대칭키 암호화 (시뮬레이션)"""

    def __init__(self):
        self.key_pairs: Dict[str, KeyPair] = {}

    def generate_key_pair(self, user_id: str) -> KeyPair:
        """키 쌍 생성"""
        # 실제로는 복잡한 수학적 연산
        private = secrets.token_hex(32)
        public = hashlib.sha256(private.encode()).hexdigest()

        key_pair = KeyPair(public_key=public, private_key=private)
        self.key_pairs[user_id] = key_pair
        return key_pair

    def encrypt(self, plaintext: str, public_key: str) -> str:
        """공개키로 암호화"""
        # 시뮬레이션: 공개키를 시드로 사용한 XOR
        key_bytes = public_key.encode()[:16]
        plain_bytes = plaintext.encode()

        encrypted = []
        for i, byte in enumerate(plain_bytes):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted.append(byte ^ key_byte)

        return base64.b64encode(bytes(encrypted)).decode()

    def decrypt(self, ciphertext: str, user_id: str) -> str:
        """개인키로 복호화"""
        key_pair = self.key_pairs.get(user_id)
        if not key_pair:
            raise ValueError("사용자를 찾을 수 없습니다")

        encrypted = base64.b64decode(ciphertext.encode())
        key_bytes = key_pair.private_key.encode()[:16]

        decrypted = []
        for i, byte in enumerate(encrypted):
            key_byte = key_bytes[i % len(key_bytes)]
            decrypted.append(byte ^ key_byte)

        return bytes(decrypted).decode()

class HashFunction:
    """해시 함수"""

    @staticmethod
    def sha256(data: str) -> str:
        """SHA-256 해시"""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def verify_hash(data: str, hash_value: str) -> bool:
        """해시 검증"""
        return HashFunction.sha256(data) == hash_value

class DigitalSignature:
    """디지털 서명 (시뮬레이션)"""

    def __init__(self):
        self.asym = SimpleAsymmetricEncryption()

    def sign(self, message: str, private_key: str) -> str:
        """서명 생성"""
        # 메시지 해시 후 개인키로 서명
        message_hash = HashFunction.sha256(message)
        return f"SIG:{message_hash[:16]}:{private_key[:8]}"

    def verify(self, message: str, signature: str, public_key: str) -> bool:
        """서명 검증"""
        message_hash = HashFunction.sha256(message)
        expected = f"SIG:{message_hash[:16]}:"
        return signature.startswith(expected)

class HybridEncryption:
    """하이브리드 암호화"""

    def __init__(self):
        self.symmetric = SimpleSymmetricEncryption()
        self.asymmetric = SimpleAsymmetricEncryption()

    def encrypt(self, plaintext: str, recipient_public_key: str) -> Dict:
        """하이브리드 암호화"""
        # 1. 대칭키 생성 및 데이터 암호화
        session_key = self.symmetric.generate_key()
        encrypted_data = self.symmetric.encrypt(plaintext)

        # 2. 대칭키를 수신자 공개키로 암호화
        encrypted_key = self.asymmetric.encrypt(session_key, recipient_public_key)

        return {
            'encrypted_data': encrypted_data,
            'encrypted_key': encrypted_key
        }

    def decrypt(self, encrypted_package: Dict, recipient_id: str) -> str:
        """하이브리드 복호화"""
        # 1. 개인키로 세션키 복호화
        session_key = self.asymmetric.decrypt(
            encrypted_package['encrypted_key'],
            recipient_id
        )

        # 2. 세션키로 데이터 복호화
        self.symmetric.key = session_key
        return self.symmetric.decrypt(encrypted_package['encrypted_data'])


# 사용 예시
print("=== 암호화 시스템 시뮬레이션 ===\n")

# 대칭키 암호화
print("--- 대칭키 암호화 ---")
sym = SimpleSymmetricEncryption()
key = sym.generate_key()
print(f"키: {key[:16]}...")

encrypted = sym.encrypt("비밀 메시지입니다")
print(f"암호문: {encrypted[:30]}...")
decrypted = sym.decrypt(encrypted)
print(f"복호문: {decrypted}")

# 비대칭키 암호화
print("\n--- 비대칭키 암호화 ---")
asym = SimpleAsymmetricEncryption()
key_pair = asym.generate_key_pair("alice")
print(f"공개키: {key_pair.public_key[:16]}...")
print(f"개인키: {key_pair.private_key[:16]}...")

encrypted = asym.encrypt("안녕하세요", key_pair.public_key)
decrypted = asym.decrypt(encrypted, "alice")
print(f"복호문: {decrypted}")

# 해시
print("\n--- 해시 함수 ---")
message = "원본 데이터"
hash_value = HashFunction.sha256(message)
print(f"해시: {hash_value[:32]}...")
print(f"검증: {HashFunction.verify_hash(message, hash_value)}")

# 하이브리드
print("\n--- 하이브리드 암호화 ---")
hybrid = HybridEncryption()
hybrid.asymmetric.generate_key_pair("bob")

package = hybrid.encrypt("중요한 문서", hybrid.asymmetric.key_pairs["bob"].public_key)
print(f"암호화된 데이터: {package['encrypted_data'][:20]}...")
decrypted = hybrid.decrypt(package, "bob")
print(f"복호문: {decrypted}")
