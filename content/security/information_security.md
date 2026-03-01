+++
title = "정보보안 (Information Security)"
date = 2025-03-01

[extra]
categories = "security-main"
+++

# 정보보안 (Information Security)

## 핵심 인사이트 (3줄 요약)
> **정보의 기밀성, 무결성, 가용성을 보호**하는 활동. 기술적, 물리적, 관리적 보안 대책 적용. CIA 3요소가 핵심 원칙이다.

## 1. 개념
정보보안은 **정보 자산을 외부 위협으로부터 보호**하여 기밀성, 무결성, 가용성을 유지하는 활동이다.

> 비유: "디지털 금고" - 소중한 정보를 안전하게 보관

## 2. 정보보안 3요소 (CIA)

```
┌─────────────────────────────────────────────────────────┐
│               정보보안 3요소 (CIA Triad)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    ┌─────────┐                          │
│                    │ 기밀성  │                          │
│                    │(Confiden│                          │
│                    │ tiality)│                          │
│                    └────┬────┘                          │
│                         │                               │
│            ┌────────────┼────────────┐                  │
│            │            │            │                  │
│      ┌─────┴─────┐     │     ┌──────┴─────┐           │
│      │  무결성   │     │     │  가용성    │           │
│      │(Integrity)│     │     │(Availability)│          │
│      └───────────┘     │     └────────────┘           │
│                         │                               │
│                                                         │
│  기밀성 (Confidentiality):                             │
│  - 인가된 사용자만 접근 가능                           │
│  - 암호화, 접근 통제                                   │
│                                                         │
│  무결성 (Integrity):                                   │
│  - 정보의 정확성과 완전성                              │
│  - 위변조 방지, 해시                                   │
│                                                         │
│  가용성 (Availability):                                │
│  - 필요할 때 언제든 접근 가능                          │
│  - 백업, 이중화                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3. 보안의 3대 영역

```
┌────────────────────────────────────────────────────────┐
│                   보안의 3대 영역                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 기술적 보안 (Technical Security)                   │
│     ┌────────────────────────────────────────────┐    │
│     │ - 암호화                                   │    │
│     │ - 방화벽, IDS/IPS                         │    │
│     │ - 접근 통제 시스템                        │    │
│     │ - 백신, 보안 솔루션                       │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 물리적 보안 (Physical Security)                    │
│     ┌────────────────────────────────────────────┐    │
│     │ - 출입 통제                                │    │
│     │ - CCTV, 경비                               │    │
│     │ - 서버실 보안                              │    │
│     │ - 재해 대책                                │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  3. 관리적 보안 (Administrative Security)              │
│     ┌────────────────────────────────────────────┐    │
│     │ - 보안 정책                                │    │
│     │ - 보안 교육                                │    │
│     │ - 보안 조직                                │    │
│     │ - 보안 감사                                │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 보안 위협

```
┌────────────────────────────────────────────────────────┐
│                    보안 위협 분류                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 가로채기 (Interception)                           │
│     - 도청, 스니핑                                     │
│     - 네트워크 패킷 캡처                               │
│     → 기밀성 침해                                      │
│                                                        │
│  2. 변조 (Modification)                               │
│     - 데이터 변경                                      │
│     - 웹사이트 변조                                    │
│     → 무결성 침해                                      │
│                                                        │
│  3. 위조/삽입 (Fabrication)                           │
│     - 가짜 데이터 생성                                 │
│     - 스푸핑, 피싱                                     │
│     → 무결성 침해                                      │
│                                                        │
│  4. 차단 (Interruption)                               │
│     - 서비스 거부 (DoS/DDoS)                          │
│     - 시스템 파괴                                      │
│     → 가용성 침해                                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 접근 통제

```
접근 통제 3단계:

1. 식별 (Identification)
   - "나는 누구인가?"
   - 사용자 ID

2. 인증 (Authentication)
   - "정말 그 사람인가?"
   - 비밀번호, 생체인식, OTP

3. 인가 (Authorization)
   - "무엇을 할 수 있는가?"
   - 권한 부여

인증 방식:
┌────────────────────────────────────────────────────┐
│                  다중 요소 인증                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  제1요소: 지식 기반 (Something you know)           │
│  - 비밀번호, PIN                                   │
│                                                    │
│  제2요소: 소유 기반 (Something you have)           │
│  - 스마트카드, OTP, 휴대전화                       │
│                                                    │
│  제3요소: 생체 기반 (Something you are)            │
│  - 지문, 홍채, 얼굴, 정맥                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 6. 접근 통제 모델

```
1. DAC (Discretionary Access Control)
   - 임의적 접근 통제
   - 소유자가 권한 부여
   - 유연하지만 보안 취약

2. MAC (Mandatory Access Control)
   - 강제적 접근 통제
   - 보안 레이블 기반
   - 높은 보안, 유연성 낮음

3. RBAC (Role-Based Access Control)
   - 역할 기반 접근 통제
   - 직무별 권한 부여
   - 관리 용이, 확장성

4. ABAC (Attribute-Based Access Control)
   - 속성 기반 접근 통제
   - 사용자/자원/환경 속성
   - 세밀한 제어 가능
```

## 7. 보안 모델

```
1. Bell-LaPadula 모델
   - 기밀성 중심
   - No Read Up: 낮은 등급은 높은 등급 읽기 불가
   - No Write Down: 높은 등급은 낮은 등급 쓰기 불가

2. Biba 모델
   - 무결성 중심
   - No Read Down: 높은 등급은 낮은 등급 읽기 불가
   - No Write Up: 낮은 등급은 높은 등급 쓰기 불가

3. Clark-Wilson 모델
   - 상업용 무결성 모델
   - 잘 정의된 트랜잭션
   - 업무 분리 원칙
```

## 8. 코드 예시

```python
from dataclasses import dataclass
from typing import Dict, List, Set, Optional
from enum import Enum
import hashlib
import secrets

class Role(Enum):
    ADMIN = "관리자"
    MANAGER = "매니저"
    USER = "사용자"
    GUEST = "게스트"

class Permission(Enum):
    READ = "읽기"
    WRITE = "쓰기"
    DELETE = "삭제"
    ADMIN = "관리"

@dataclass
class User:
    """사용자"""
    username: str
    password_hash: str
    role: Role
    failed_attempts: int = 0
    locked: bool = False

class AuthenticationService:
    """인증 서비스"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, str] = {}  # token -> username
        self.max_attempts = 5

    def add_user(self, username: str, password: str, role: Role):
        """사용자 추가"""
        password_hash = self._hash_password(password)
        self.users[username] = User(username, password_hash, role)

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """인증"""
        user = self.users.get(username)
        if not user:
            return None

        if user.locked:
            print("계정이 잠겼습니다")
            return None

        if user.password_hash != self._hash_password(password):
            user.failed_attempts += 1
            if user.failed_attempts >= self.max_attempts:
                user.locked = True
                print("계정이 잠겼습니다")
            return None

        # 로그인 성공
        user.failed_attempts = 0
        token = secrets.token_hex(32)
        self.sessions[token] = username
        return token

    def logout(self, token: str):
        """로그아웃"""
        if token in self.sessions:
            del self.sessions[token]

    def get_user(self, token: str) -> Optional[User]:
        """토큰으로 사용자 조회"""
        username = self.sessions.get(token)
        if username:
            return self.users.get(username)
        return None

    def _hash_password(self, password: str) -> str:
        """비밀번호 해시"""
        return hashlib.sha256(password.encode()).hexdigest()

class AccessControlService:
    """접근 통제 서비스 (RBAC)"""

    def __init__(self):
        self.role_permissions: Dict[Role, Set[Permission]] = {
            Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
            Role.MANAGER: {Permission.READ, Permission.WRITE, Permission.DELETE},
            Role.USER: {Permission.READ, Permission.WRITE},
            Role.GUEST: {Permission.READ},
        }
        self.audit_log: List[Dict] = []

    def check_permission(self, user: User, permission: Permission,
                         resource: str = None) -> bool:
        """권한 확인"""
        has_permission = permission in self.role_permissions.get(user.role, set())

        # 감사 로그 기록
        self.audit_log.append({
            'user': user.username,
            'permission': permission.value,
            'resource': resource,
            'result': '허용' if has_permission else '거부',
            'timestamp': self._get_timestamp()
        })

        return has_permission

    def get_audit_log(self) -> List[Dict]:
        """감사 로그 조회"""
        return self.audit_log

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class SecurityManager:
    """보안 관리자"""

    def __init__(self):
        self.auth = AuthenticationService()
        self.access = AccessControlService()

    def setup_demo_users(self):
        """데모 사용자 설정"""
        self.auth.add_user("admin", "admin123", Role.ADMIN)
        self.auth.add_user("manager", "manager123", Role.MANAGER)
        self.auth.add_user("user1", "user123", Role.USER)
        self.auth.add_user("guest", "guest123", Role.GUEST)

    def secure_operation(self, token: str, permission: Permission,
                         resource: str = None) -> bool:
        """보안 연산 수행"""
        user = self.auth.get_user(token)
        if not user:
            print("인증되지 않은 사용자")
            return False

        if self.access.check_permission(user, permission, resource):
            print(f"[{user.username}] {permission.value} 권한 허용")
            return True
        else:
            print(f"[{user.username}] {permission.value} 권한 거부")
            return False

# 사용 예시
print("=== 정보보안 시스템 시뮬레이션 ===\n")

security = SecurityManager()
security.setup_demo_users()

# 인증 테스트
print("--- 인증 테스트 ---")
admin_token = security.auth.authenticate("admin", "admin123")
user_token = security.auth.authenticate("user1", "user123")
wrong_token = security.auth.authenticate("user1", "wrong_password")

print(f"관리자 로그인: {'성공' if admin_token else '실패'}")
print(f"사용자 로그인: {'성공' if user_token else '실패'}")
print(f"잘못된 비밀번호: {'성공' if wrong_token else '실패'}")

# 권한 테스트
print("\n--- 권한 테스트 ---")
security.secure_operation(admin_token, Permission.ADMIN, "시스템 설정")
security.secure_operation(user_token, Permission.ADMIN, "시스템 설정")
security.secure_operation(user_token, Permission.WRITE, "문서")
security.secure_operation(user_token, Permission.DELETE, "문서")

# 감사 로그
print("\n--- 감사 로그 ---")
for log in security.access.get_audit_log()[:5]:
    print(f"{log['user']}: {log['permission']} → {log['result']}")
```

## 9. 보안 거버넌스

```
정보보호 거버넌스:
┌────────────────────────────────────────────────────┐
│                                                    │
│  1. 보안 정책 수립                                 │
│     - 정보보호 정책                                │
│     - 보안 지침                                    │
│     - 업무 절차                                    │
│                                                    │
│  2. 보안 조직 구성                                 │
│     - CISO (최고정보보호책임자)                   │
│     - 보안 담당 부서                               │
│     - 보안 관리자                                  │
│                                                    │
│  3. 보안 교육                                      │
│     - 정기 보안 교육                               │
│     - 보안 인식 제고                               │
│     - 피싱/보안 사고 예방                          │
│                                                    │
│  4. 보안 감사                                      │
│     - 내부 감사                                    │
│     - 외부 감사                                    │
│     - 취약점 진단                                  │
│                                                    │
│  5. 사고 대응                                      │
│     - 침해 사고 대응                               │
│     - 복구 절차                                    │
│     - 재발 방지                                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 10. 장단점

### 강력한 보안의 장점
| 장점 | 설명 |
|-----|------|
| 자산 보호 | 정보 자산 보호 |
| 신뢰성 | 고객 신뢰 확보 |
| 규정 준수 | 법적 요구사항 충족 |
| 비즈니스 | 영업 활동 보장 |

### 과도한 보안의 단점
| 단점 | 설명 |
|-----|------|
| 비용 | 높은 구축 비용 |
| 편의성 | 사용자 불편 |
| 복잡성 | 관리 복잡 |
| 성능 | 시스템 성능 저하 |

## 11. 실무에선? (기술사적 판단)
- **균형**: 보안 vs 편의성 트레이드오프
- **심층 방어**: 다층 보안 적용
- **제로 트러스트**: 신뢰하지 않음 기본 원칙
- **ISMS**: 정보보호 관리체계 인증
- **개인정보**: 개인정보보호법 준수

## 12. 관련 개념
- 암호화
- 인증/인가
- 방화벽
- 침해 탐지

---

## 어린이를 위한 종합 설명

**정보보안은 "디지털 금고"예요!**

### 3가지 지켜야 할 것 🔒
```
기밀성: 비밀 지키기
  "아무나 못 봐요!"

무결성: 내용 안 바뀌게
  "몰래 수정 못 해요!"

가용성: 필요할 때 쓰기
  "언제든 쓸 수 있어요!"
```

### 어떻게 지키나요? 🛡️
```
기술적: 프로그램으로
  - 비밀번호, 암호화

물리적: 몸으로
  - 잠금장치, 경비

관리적: 규칙으로
  - 교육, 정책
```

### 3단계 확인 🚪
```
1. 식별: "누구세요?"
2. 인증: "정말 그 사람?"
3. 인가: "들어오세요"
```

**비밀**: 비밀번호는 쉬운 거 쓰면 안 돼요! 🔐✨
