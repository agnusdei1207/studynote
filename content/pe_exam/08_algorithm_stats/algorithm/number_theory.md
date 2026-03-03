+++
title = "수리 알고리즘 (Number Theory Algorithms)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 수리 알고리즘 (Number Theory Algorithms)

## 핵심 인사이트 (3줄 요약)
> **정수론 기반 수학적 알고리즘**으로 GCD, 소수, 모듈러 산술이 핵심. 유클리드 호제법 O(log n)으로 GCD 계산. RSA, 해시 함수, 암호학의 수학적 기초.

---

### Ⅰ. 개요

**개념**: 수리 알고리즘(Number Theory Algorithms)은 **정수의 성질을 이용하여 수학적 계산을 효율적으로 수행하는 알고리즘**으로, 암호학, 해시 함수, 난수 생성 등의 기반이다.

> 💡 **비유**: "암호 만들기 게임" - 숫자의 비밀 규칙을 이용해서 아무도 못 푸는 열쇠를 만들어요! 큰 수를 인수분해하는 건 쉽지만, 거꾸로 두 소수를 찾는 건 거의 불가능해요. 이게 암호의 마법!

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 큰 수의 약수 찾기, 거듭제곱 계산 등이 O(n) 이상으로 매우 느렸음. 암호학에서 효율적인 수학 연산 필요
2. **기술적 필요성**: RSA 암호(1977), ECC(1985) 등 현대 암호학의 수학적 기반 제공. 해시 함수, 난수 생성의 핵심 알고리즘
3. **시장/산업 요구**: 전자상거래, 블록체인, 디지털 서명 등 보안 서비스에서 수리 알고리즘 필수

**핵심 목적**: 정수의 수학적 성질을 활용하여 효율적인 연산을 수행하고, 암호학적으로 안전한 시스템 구축.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 시간복잡도 | 비유 |
|----------|------|----------|-----------|------|
| GCD/LCM | Greatest Common Divisor | 최대공약수/최소공배수 | O(log min(a,b)) | 공통 약수 찾기 |
| 소수 판별 | Primality Test | 소수 여부 확인 | O(√n) | 암호의 재료 |
| 에라토스테네스 체 | Sieve of Eratosthenes | n 이하 모든 소수 찾기 | O(n log log n) | 체로 거르기 |
| 모듈러 거듭제곱 | Modular Exponentiation | (a^n mod m) 계산 | O(log n) | 암호 연산 |
| 확장 유클리드 | Extended Euclidean | ax + by = gcd(a,b) 해 | O(log min(a,b)) | 역원 찾기 |

**수리 알고리즘 분류**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    수리 알고리즘 분류                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔢 기본 연산 (Basic Operations):                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • GCD (최대공약수): 두 수의 가장 큰 공통 약수             │ │
│  │    예: gcd(12, 18) = 6                                    │ │
│  │                                                            │ │
│  │  • LCM (최소공배수): 두 수의 가장 작은 공통 배수           │ │
│  │    예: lcm(12, 18) = 36                                   │ │
│  │    공식: lcm(a,b) = a × b / gcd(a,b)                      │ │
│  │                                                            │ │
│  │  • 유클리드 호제법: GCD를 빠르게 계산                      │ │
│  │    gcd(a,b) = gcd(b, a mod b)  (a > b)                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🧮 소수 관련 (Prime Numbers):                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 소수 판별: O(√n)로 소수인지 확인                        │ │
│  │    2부터 √n까지 나누어떨어지면 합성수                      │ │
│  │                                                            │ │
│  │  • 에라토스테네스 체: n 이하 모든 소수 찾기                │ │
│  │    2의 배수 지우기 → 3의 배수 지우기 → ...                │ │
│  │    남은 수들이 소수                                        │ │
│  │                                                            │ │
│  │  • 소인수분해: 정수를 소수의 곱으로 분해                   │ │
│  │    예: 84 = 2² × 3 × 7                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔐 모듈러 산술 (Modular Arithmetic):                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 모듈러 연산: (a + b) mod n = ((a mod n) + (b mod n)) mod n │
│  │  • 모듈러 거듭제곱: a^n mod m을 O(log n)에 계산           │ │
│  │    분할 정복: a^n = a^(n/2) × a^(n/2)                     │ │
│  │                                                            │ │
│  │  • 모듈러 역원: a^(-1) mod m (gcd(a,m) = 1일 때만 존재)    │ │
│  │    페르마 소정리: a^(p-1) ≡ 1 (mod p)                     │ │
│  │    역원: a^(-1) ≡ a^(p-2) (mod p)                         │ │
│  │                                                            │ │
│  │  • 중국인의 나머지 정리 (CRT):                             │ │
│  │    x ≡ a₁ (mod m₁), x ≡ a₂ (mod m₂)                      │ │
│  │    gcd(m₁,m₂) = 1이면 유일한 해 x 존재                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📊 조합론 (Combinatorics):                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 팩토리얼: n! = 1 × 2 × ... × n                         │ │
│  │  • 순열: nPr = n! / (n-r)!                                │ │
│  │  • 조합: nCr = n! / (r! × (n-r)!)                         │ │
│  │  • 카탈란 수: Cn = (1/(n+1)) × 2nCn                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**유클리드 호제법 동작 원리**:

```
┌─────────────────────────────────────────────────────────────────┐
│                유클리드 호제법 (Euclidean Algorithm)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  원리: gcd(a, b) = gcd(b, a mod b)                              │
│        b가 0이 되면 a가 최대공약수                              │
│                                                                 │
│  예시: gcd(48, 18) 구하기                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  단계 1: gcd(48, 18) → 48 = 18 × 2 + 12 → gcd(18, 12)     │ │
│  │  단계 2: gcd(18, 12) → 18 = 12 × 1 + 6  → gcd(12, 6)      │ │
│  │  단계 3: gcd(12, 6)  → 12 = 6 × 2 + 0   → gcd(6, 0)       │ │
│  │  단계 4: gcd(6, 0) = 6  ✓                                 │ │
│  │                                                            │ │
│  │  → 최대공약수 = 6                                          │ │
│  │  → 최소공배수 = 48 × 18 / 6 = 144                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  시간복잡도: O(log(min(a, b)))                                  │
│  - 매 단계에서 큰 수가 최소 절반 이하로 감소                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**에라토스테네스 체 동작 원리**:

```
┌─────────────────────────────────────────────────────────────────┐
│             에라토스테네스 체 (Sieve of Eratosthenes)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  n = 30까지의 소수 찾기:                                        │
│                                                                 │
│  초기 상태 (2~30):                                              │
│   2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20     │
│  21 22 23 24 25 26 27 28 29 30                                 │
│                                                                 │
│  ① 2의 배수 제거 (2는 소수):                                    │
│   2  3  ×  5  ×  7  ×  9  × 11  × 13  × 15  × 17  × 19  ×     │
│  21  × 23  × 25  × 27  × 29  ×                                 │
│                                                                 │
│  ② 3의 배수 제거 (3은 소수):                                    │
│   2  3  ×  5  ×  7  ×  ×  × 11  × 13  ×  ×  × 17  × 19  ×     │
│   ×  × 23  × 25  ×  ×  × 29  ×                                 │
│                                                                 │
│  ③ 5의 배수 제거 (5는 소수):                                    │
│   2  3  ×  5  ×  7  ×  ×  × 11  × 13  ×  ×  × 17  × 19  ×     │
│   ×  × 23  ×  ×  ×  ×  × 29  ×                                 │
│                                                                 │
│  결과: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29                      │
│                                                                 │
│  시간복잡도: O(n log log n)                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 수학적 성질**:

| 성질 | 공식 | 설명 |
|-----|------|------|
| GCD × LCM | gcd(a,b) × lcm(a,b) = a × b | 두 수의 곱 = GCD × LCM |
| 페르마 소정리 | a^(p-1) ≡ 1 (mod p) | p가 소수이고 gcd(a,p) = 1 |
| 오일러 정리 | a^φ(n) ≡ 1 (mod n) | φ(n)은 오일러 파이 함수 |
| 모듈러 곱셈 | (a×b) mod n = ((a mod n)×(b mod n)) mod n | 오버플로우 방지 |
| 윌슨 정리 | (p-1)! ≡ -1 (mod p) | p가 소수일 필요충분조건 |

**동작 원리** (단계별 상세 설명):

```
① GCD: 유클리드 호제법 → ② LCM: 공식 적용 → ③ 소수 판별: √n까지 확인
① 소수 나열: 체 알고리즘 → ② 거듭제곱: 분할 정복 → ③ 역원: 페르마/확장 유클리드
```

- **1단계 (GCD)**: 유클리드 호제법으로 큰 수를 작은 수로 나눈 나머지를 반복하여 GCD 계산
- **2단계 (소수 판별)**: 2부터 √n까지 나누어떨어지는지 확인. 하나라도 나누어떨어지면 합성수
- **3단계 (에라토스테네스 체)**: 소수 p를 찾으면 p²부터 p의 배수를 모두 제거. √n까지만 반복
- **4단계 (모듈러 거듭제곱)**: a^n mod m을 분할 정복으로 O(log n)에 계산. RSA 암호의 핵심
- **5단계 (모듈러 역원)**: 페르마 소정리(소수 모듈러) 또는 확장 유클리드(일반)로 계산

**코드 예시** (Python):

```python
"""
수리 알고리즘 구현
- GCD/LCM (유클리드 호제법)
- 소수 판별, 에라토스테네스 체
- 모듈러 거듭제곱, 모듈러 역원
- 확장 유클리드, 중국인의 나머지 정리
- 조합론 (팩토리얼, 순열, 조합)
"""
from typing import List, Tuple, Optional
import math


# ============== GCD/LCM ==============

def gcd(a: int, b: int) -> int:
    """
    최대공약수 (GCD) - 유클리드 호제법
    시간복잡도: O(log(min(a, b)))
    """
    while b:
        a, b = b, a % b
    return abs(a)


def gcd_recursive(a: int, b: int) -> int:
    """GCD 재귀 버전"""
    if b == 0:
        return abs(a)
    return gcd_recursive(b, a % b)


def lcm(a: int, b: int) -> int:
    """
    최소공배수 (LCM)
    공식: lcm(a, b) = |a × b| / gcd(a, b)
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def gcd_multiple(numbers: List[int]) -> int:
    """여러 수의 GCD"""
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result


# ============== 소수 관련 ==============

def is_prime(n: int) -> bool:
    """
    소수 판별 - O(√n)
    2부터 √n까지 나누어떨어지는지 확인
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # 3부터 √n까지 홀수만 확인
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_prime_miller_rabin(n: int, k: int = 5) -> bool:
    """
    밀러-라빈 소수 판별법
    - 확률적 소수 판별
    - 큰 수에 효율적
    - 시간복잡도: O(k × log³n)
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # n-1 = 2^r × d 형태로 분해
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # 테스트할 witness들
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    def check(a: int) -> bool:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for a in witnesses[:k]:
        if a >= n:
            continue
        if not check(a):
            return False
    return True


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    에라토스테네스 체 - n 이하의 모든 소수 반환
    시간복잡도: O(n log log n)
    공간복잡도: O(n)
    """
    if n < 2:
        return []

    # True = 소수 후보, False = 합성수
    is_prime_arr = [True] * (n + 1)
    is_prime_arr[0] = is_prime_arr[1] = False

    # √n까지만 체 수행
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime_arr[i]:
            # i²부터 i의 배수를 모두 제거
            for j in range(i * i, n + 1, i):
                is_prime_arr[j] = False

    return [i for i in range(2, n + 1) if is_prime_arr[i]]


def prime_factorization(n: int) -> List[Tuple[int, int]]:
    """
    소인수분해
    반환: [(소수, 지수), ...]
    예: 84 → [(2, 2), (3, 1), (7, 1)]  # 84 = 2² × 3 × 7
    """
    if n < 2:
        return []

    factors = []
    # 2로 나누기
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    if count > 0:
        factors.append((2, count))

    # 홀수로 나누기
    i = 3
    while i * i <= n:
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count > 0:
            factors.append((i, count))
        i += 2

    # 남은 수가 1보다 크면 소수
    if n > 1:
        factors.append((n, 1))

    return factors


# ============== 모듈러 산술 ==============

def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    모듈러 거듭제곱: base^exp mod mod
    분할 정복으로 O(log exp)에 계산
    """
    if mod == 1:
        return 0

    result = 1
    base = base % mod

    while exp > 0:
        # exp가 홀수면 결과에 base를 곱함
        if exp % 2 == 1:
            result = (result * base) % mod
        # exp를 절반으로 줄임
        exp //= 2
        base = (base * base) % mod

    return result


def mod_inverse_fermat(a: int, p: int) -> Optional[int]:
    """
    모듈러 역원 (페르마 소정리 이용)
    a^(-1) mod p = a^(p-2) mod p
    조건: p는 소수이고 gcd(a, p) = 1
    """
    if math.gcd(a, p) != 1:
        return None  # 역원 존재하지 않음
    return mod_pow(a, p - 2, p)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    확장 유클리드 호제법
    ax + by = gcd(a, b)를 만족하는 (gcd, x, y) 반환
    """
    if b == 0:
        return a, 1, 0

    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd_val, x, y


def mod_inverse_extended(a: int, m: int) -> Optional[int]:
    """
    모듈러 역원 (확장 유클리드 이용)
    a^(-1) mod m
    조건: gcd(a, m) = 1
    """
    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        return None  # 역원 존재하지 않음
    return (x % m + m) % m  # 양수로 변환


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    중국인의 나머지 정리 (CRT)
    x ≡ r[i] (mod m[i])를 만족하는 x 반환
    조건: 모든 m[i]는 서로소
    """
    if len(remainders) != len(moduli):
        return None

    # 모든 moduli의 곱
    M = 1
    for m in moduli:
        M *= m

    result = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        yi = mod_inverse_extended(Mi, m)
        if yi is None:
            return None  # 역원이 없음 (서로소가 아님)
        result += r * Mi * yi

    return result % M


# ============== 조합론 ==============

def factorial(n: int, mod: int = None) -> int:
    """
    팩토리얼: n!
    mod가 주어지면 mod 연산 적용
    """
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다")

    result = 1
    for i in range(2, n + 1):
        result = result * i if mod is None else (result * i) % mod
    return result


def combination(n: int, r: int, mod: int = None) -> int:
    """
    조합: nCr = n! / (r! × (n-r)!)
    mod가 주어지면 페르마 소정리 이용
    """
    if r < 0 or r > n:
        return 0
    if r == 0 or r == n:
        return 1

    r = min(r, n - r)  # 대칭성 활용

    if mod is None:
        return factorial(n) // (factorial(r) * factorial(n - r))
    else:
        # 모듈러 산술에서 나눗셈은 역원 곱셈으로
        numerator = factorial(n, mod)
        denominator = (factorial(r, mod) * factorial(n - r, mod)) % mod
        return (numerator * mod_inverse_fermat(denominator, mod)) % mod


def permutation(n: int, r: int, mod: int = None) -> int:
    """
    순열: nPr = n! / (n-r)!
    """
    if r < 0 or r > n:
        return 0
    if r == 0:
        return 1

    result = 1
    for i in range(n, n - r, -1):
        result = result * i if mod is None else (result * i) % mod
    return result


def catalan_number(n: int, mod: int = None) -> int:
    """
    카탈란 수: Cn = (1/(n+1)) × 2nCn
    괄호 쌍, 이진 트리 개수 등
    """
    if mod is None:
        return combination(2 * n, n) // (n + 1)
    else:
        inv_n_plus_1 = mod_inverse_fermat(n + 1, mod)
        return (combination(2 * n, n, mod) * inv_n_plus_1) % mod


# ============== 실행 예시 ==============

if __name__ == "__main__":
    print("=" * 60)
    print(" 수리 알고리즘 예시")
    print("=" * 60)

    # 1. GCD/LCM
    print("\n1. GCD/LCM")
    a, b = 48, 18
    print(f"gcd({a}, {b}) = {gcd(a, b)}")
    print(f"lcm({a}, {b}) = {lcm(a, b)}")
    print(f"확인: {a} × {b} = {a*b}, gcd × lcm = {gcd(a,b) * lcm(a,b)}")

    # 2. 소수 판별
    print("\n2. 소수 판별")
    test_numbers = [17, 18, 97, 100, 1009]
    for n in test_numbers:
        print(f"  {n}: {'소수' if is_prime(n) else '합성수'}")

    # 3. 에라토스테네스 체
    print("\n3. 에라토스테네스 체 (30 이하 소수)")
    primes = sieve_of_eratosthenes(30)
    print(f"  {primes}")

    # 4. 소인수분해
    print("\n4. 소인수분해")
    n = 84
    factors = prime_factorization(n)
    factor_str = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors)
    print(f"  {n} = {factor_str}")

    # 5. 모듈러 거듭제곱
    print("\n5. 모듈러 거듭제곱")
    base, exp, mod = 3, 100, 13
    print(f"  {base}^{exp} mod {mod} = {mod_pow(base, exp, mod)}")

    # 6. 모듈러 역원
    print("\n6. 모듈러 역원")
    a, p = 3, 11  # p는 소수
    inv = mod_inverse_fermat(a, p)
    print(f"  {a}^(-1) mod {p} = {inv}")
    print(f"  확인: {a} × {inv} mod {p} = {(a * inv) % p}")

    # 7. 확장 유클리드
    print("\n7. 확장 유클리드")
    a, b = 35, 15
    g, x, y = extended_gcd(a, b)
    print(f"  {a}x + {b}y = gcd({a},{b})")
    print(f"  gcd = {g}, x = {x}, y = {y}")
    print(f"  확인: {a}×{x} + {b}×{y} = {a*x + b*y}")

    # 8. 중국인의 나머지 정리
    print("\n8. 중국인의 나머지 정리")
    # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
    remainders = [2, 3, 2]
    moduli = [3, 5, 7]
    x = chinese_remainder_theorem(remainders, moduli)
    print(f"  x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)")
    print(f"  x = {x}")
    for r, m in zip(remainders, moduli):
        print(f"    확인: {x} mod {m} = {x % m} (예상: {r})")

    # 9. 조합론
    print("\n9. 조합론")
    n, r = 10, 3
    print(f"  {n}P{r} = {permutation(n, r)}")
    print(f"  {n}C{r} = {combination(n, r)}")
    print(f"  Catalan({5}) = {catalan_number(5)}")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:

| 장점 (수리 알고리즘) | 단점 (수리 알고리즘) |
|---------------------|---------------------|
| 수학적 정확성 보장 | 큰 수 처리 시 오버플로우 위험 |
| 효율적인 계산 (로그 복잡도) | 이해와 구현의 난이도 |
| 암호학적 응용 가능 | 하드웨어 의존적 (정수 크기) |
| 검증된 이론적 기반 | 특수 케이스 처리 복잡 |

**소수 판별 방법 비교**:

| 비교 항목 | 시행 나눗셈 | 에라토스테네스 체 | ★ 밀러-라빈 |
|---------|-----------|------------------|------------|
| 단일 판별 | O(√n) | O(n log log n) | O(k log³n) |
| 여러 소수 | 비효율 | ★ 효율적 | 효율적 |
| 정확성 | 확정적 | 확정적 | 확률적 |
| 큰 수 | 느림 | 메모리 많이 사용 | ★ 빠름 |
| 적합 상황 | 작은 수 | n 이하 모든 소수 | ★ 암호학적 큰 수 |

> **★ 선택 기준**:
> - 단일 작은 수 → **시행 나눗셈 (√n)**
> - n 이하 모든 소수 → **에라토스테네스 체**
> - 큰 수, 암호학 → **밀러-라빈**
> - 100% 확정 필요 → **AKS 알고리즘** (O(log⁶n))

**기술 진화 계보**:
```
유클리드 호제법(BC 300) → 페르마 소정리(1640) → 오일러 정리(1736) → RSA(1977) → ECC(1985)
```

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **RSA 암호** | 두 큰 소수의 곱, 모듈러 거듭제곱 | 2048비트 보안, 해독 불가 |
| **해시 함수** | 모듈러 연산으로 고정 길이 출력 | 충돌 확률 2^(-128) 이하 |
| **블록체인** | 타원곡선 암호(ECC), 디지털 서명 | 거래 검증 < 1초 |
| **난수 생성** | 소수 기반 의사난수 생성기 | 통계적 무작위성 보장 |

**실제 도입 사례**:

- **사례 1: RSA Security** - 2048비트 RSA 키 생성에 두 1024비트 소수 사용. 소수 생성에 밀러-라빈 활용. 전 세계 HTTPS의 90% 이상 사용
- **사례 2: Bitcoin (ECDSA)** - 타원곡선 secp256k1 사용. 개인키는 256비트 정수, 서명은 모듈러 산술 기반. 거래당 서명 검증 < 1ms
- **사례 3: Hash 함수 (SHA-256)** - 비트 연산과 모듈러 덧셈 조합. Bitcoin 채굴, 파일 무결성 검증에 사용. 충돌 내성 2^128

**도입 시 고려사항** (4가지 관점):

1. **기술적**:
   - 정수 오버플로우 방지 (임의 정밀도 산술)
   - 소수 생성 시간 고려
   - 모듈러 연산의 하드웨어 가속
   - 사이드 채널 공격 방지

2. **운영적**:
   - 키 관리 정책
   - 소수 생성 주기
   - 암호화 연산 부하 분산
   - 키 교체 절차

3. **보안적**:
   - 소수의 품질 검증
   - 약한 소수(Weak Primes) 방지
   - 타이밍 공격 방지 (상수 시간 알고리즘)
   - 양자 컴퓨터 대비 (Post-Quantum)

4. **경제적**:
   - 암호화 연산 비용
   - 하드웨어 가속기(HSM) 도입
   - 키 저장 공간
   - 인증서 갱신 비용

**주의사항 / 흔한 실수**:

- ❌ **오버플로우**: 모듈러 연산 없이 큰 수 거듭제곱 → 오버플로우
- ❌ **약한 소수**: 특수 형태의 소수 사용 → 인수분해 공격 취약
- ❌ **역원 없음**: gcd(a, m) ≠ 1인 경우 역원 계산 시도
- ❌ **RSA 패딩**: 패딩 없이 평문 암호화 → 선택 암호문 공격 취약

**관련 개념 / 확장 학습**:

```
📌 수리 알고리즘 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [수리 알고리즘] 핵심 연관 개념 맵                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [정수론] ←──────→ [수리 알고리즘] ←──────→ [암호학]            │
│       ↓                   ↓                  ↓                  │
│   [소수/인수분해]    [모듈러 산술]      [RSA/ECC]                │
│       ↓                   ↓                  ↓                  │
│   [유클리드 호제법]  [이산로그]        [디지털 서명]             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 해시 함수 | 응용 개념 | 모듈러 연산 기반 | `[hash](../data_structure/hash.md)` |
| 암호학 | 핵심 응용 | RSA, ECC의 수학적 기반 | `[cryptography](../security/crypto.md)` |
| 분할 정복 | 설계 기법 | 모듈러 거듭제곱에 활용 | `[divide_conquer](./divide_conquer.md)` |
| 재귀 | 설계 기법 | 유클리드 호제법 | `[recursion](./recursion.md)` |
| 동적 계획법 | 응용 기법 | 조합론 문제에 활용 | `[dynamic_programming](./dynamic_programming.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| GCD 계산 | 유클리드 호제법 | O(log n) → 대수 계산 100배 향상 |
| 소수 판별 | 밀러-라빈 | 큰 수(10^100) 소수 판별 < 1초 |
| 암호화 | RSA 2048비트 | 해독 시간 10^20 년 이상 |
| 거듭제곱 | 모듈러 거듭제곱 | O(log n) → 10^9승 계산 < 1ms |

**미래 전망** (3가지 관점):

1. **기술 발전 방향**: 양자 내성 암호(Post-Quantum Cryptography)로의 전환. 격자 기반 암호(Lattice-based), 해시 기반 서명
2. **시장 트렌드**: 블록체인, CBDC(중앙은행 디지털 화폐) 확대. 영지식 증명(Zero-Knowledge Proof) 수요 증가
3. **후속 기술**: 동형 암호(Homomorphic Encryption), 다중 선형 대수 암호, 양자 키 분배(QKD)

> **결론**: 수리 알고리즘은 현대 암호학의 수학적 기반으로, 유클리드 호제법부터 모듈러 산술까지의 이해가 필수적이다. RSA, ECC 등 모든 공개키 암호는 수리 알고리즘에 기반하며, 양자 컴퓨팅 시대에도 격자 기반 등 새로운 수학적 기반이 계속 개발될 것이다.

> **※ 참고 표준**: NIST FIPS 186-4 (Digital Signature), RFC 8017 (PKCS #1), NIST SP 800-90A (난수 생성), ISO/IEC 18033 (암호 알고리즘)

---

## 어린이를 위한 종합 설명

**수리 알고리즘**은 마치 **비밀 암호 만들기**와 같아요!

첫 번째 문단: 숫자에도 비밀이 있어요! 어떤 숫자는 **소수**라고 해서 1하고 자기 자신으로만 나누어떨어져요. 2, 3, 5, 7, 11, 13, 17... 이런 숫자들이요. 이 소수들을 이용하면 아주 튼튼한 자물쇠를 만들 수 있어요! 왜냐하면 아주 큰 숫자를 소수끼리 곱해서 만들면, 다시 그 숫자를 어떤 소수들로 만들었는지 알아내는 게 거의 불가능하거든요!

두 번째 문단: **유클리드 호제법**은 두 숫자의 **최대공약수**를 재미있게 찾는 방법이에요. 48하고 18의 최대공약수를 찾을 때, 48을 18로 나누고(나머지 12), 18을 12로 나누고(나머지 6), 12를 6으로 나누면(나머지 0)! 0이 되면 그때 나누는 수인 6이 최대공약수! 정말 빠르고 똑똑한 방법이에요.

세 번째 문단: 오늘날 인터넷에서 카드 결제를 하거나, 비밀 메시지를 보낼 때, 이 수리 알고리즘들이 우리를 지켜주고 있어요! **RSA 암호**는 아주 큰 두 소수(각각 300자리 이상!)를 곱해서 만든 자물쇠예요. 전 세계 어떤 슈퍼컴퓨터도 이 자물쇠를 풀 수 없어요. 수학의 비밀 덕분에 우리의 비밀이 안전해요! 🔐🔢

---

## ✅ 작성 완료 체크리스트

- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(5개) + 다이어그램 + 단계별 동작 + Python 코드
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(4개) + 실제 사례(3개) + 고려사항(4가지) + 주의사항(4개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 나열 + 개념 맵 + 링크
- [x] 어린이를 위한 종합 설명 (3문단)
