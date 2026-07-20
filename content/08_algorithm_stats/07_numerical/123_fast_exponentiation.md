---
title: "Fast Exponentiation"
date: "2026-04-05"
tags:
  - "studynote-algorithm-stats"
weight: 123
---
> **핵심 인사이트**
> 1. 빠른 거듭제곱(Fast Exponentiation)은 a^b를 O(log b) 번의 곱셈으로 계산 — a^b를 나이브하게 계산하면 O(b) 번 곱셈이 필요하지만, 반복 제곱법(Repeated Squaring)을 사용하면 지수를 이진수로 표현하여 O(log b)로 줄인다.
> 2. 모듈러 거듭제곱(Modular Exponentiation)이 암호학의 핵심 연산 — RSA 암호화·복호화, 디피-헬만 키 교환, 밀러-라빈 소수 판별 모두 a^b mod m 계산에 의존하며, 모듈러 연산을 각 단계에 적용해야 수의 크기가 관리 가능하다.
> 3. 행렬 빠른 거듭제곱으로 피보나치를 O(log N)에 계산 — 스칼라 거듭제곱과 동일한 원리를 행렬에 적용하여 피보나치·선형 점화식을 로그 시간에 계산하는 강력한 기법이다.

---

## Ⅰ. 반복 제곱법 (Repeated Squaring)

```
나이브한 방법 (O(b)):
  a^8 = a × a × a × a × a × a × a × a
  -> 7번 곱셈 (b-1번)

반복 제곱법 원리:
  a^8 = (a^4)^2 = ((a^2)^2)^2

  a^1 -> a^2(제곱) -> a^4(제곱) -> a^8(제곱)
  -> 3번 곱셈 (log₂ 8 = 3)

일반화 (이진 지수):
  b = 13 = 1101₂ = 8 + 4 + 1

  a^13 = a^8 × a^4 × a^1

  계산:
  a^1 (초기값)
  a^2 = (a^1)^2
  a^4 = (a^2)^2
  a^8 = (a^4)^2

  b의 이진수 표현의 각 비트가 1인 위치의 값 곱하기
  -> 곱셈 횟수 = log₂(b) + popcount(b) - 1 ≈ O(log b)

구현:

재귀 버전:
  def fast_pow(a, b):
      if b == 0: return 1
      if b % 2 == 0:
          half = fast_pow(a, b // 2)
          return half * half
      else:
          return a * fast_pow(a, b - 1)

반복 버전 (스택 오버플로우 없음):
  def fast_pow_iter(a, b):
      result = 1
      while b > 0:
          if b & 1:  # 현재 비트가 1이면
              result *= a
          a *= a     # a를 제곱
          b >>= 1    # 다음 비트로
      return result

성능 비교:
  a^1000000:
  나이브: 999,999번 곱셈
  반복 제곱: 20번 (log₂ 1,000,000 ≈ 20)
  -> 50,000배 빠름
```

> 📢 **섹션 요약 비유**: 반복 제곱법 = 종이 접기 — 종이 한 번 접으면 2배, 두 번 4배, 10번 1024배. a^1024는 1023번 곱하기 대신 10번 제곱으로! 이진수가 핵심!

---

## Ⅱ. 모듈러 거듭제곱

```
모듈러 거듭제곱 (Modular Exponentiation):
  a^b mod m 계산

  나이브 문제:
  a = 2, b = 1000, m = 10^9 + 7
  a^b = 2^1000 = 10^301 자리 수!
  -> 메모리, 처리 불가

핵심 성질:
  (a × b) mod m = ((a mod m) × (b mod m)) mod m

  -> 각 단계에서 mod 취하면 수의 크기를 m 이하로 유지

모듈러 거듭제곱 구현:
  def mod_pow(a, b, m):
      result = 1
      a %= m         # 초기 mod 처리
      while b > 0:
          if b & 1:
              result = (result * a) % m
          a = (a * a) % m
          b >>= 1
      return result

  # Python 내장 함수 (더 빠름)
  pow(a, b, m)  # C 구현, 최적화됨

사용 사례:

RSA 암호화:
  C = M^e mod n  (공개키 암호화)
  M = C^d mod n  (개인키 복호화)

  e, d, n: 수백~수천 비트
  pow(M, e, n) 호출 한 번으로 처리

페르마 소정리 확인:
  a^(p-1) mod p == 1 이면 p는 소수 (후보)
  pow(a, p-1, p)

조합 수 mod p:
  C(n, k) mod p = n! / (k! × (n-k)!) mod p
  분모의 역원 = pow(k! × (n-k)!, p-2, p) (페르마 소정리)

  nCr = (n! * pow(factorial(r) * factorial(n-r), p-2, p)) % p
```

> 📢 **섹션 요약 비유**: 모듈러 거듭제곱 = 시계 덧셈 — 2^1000을 직접 계산하면 300자리 수. 시계(mod)로 계산하면 항상 0~11 사이. RSA, 소수 판별 모두 "시계 덧셈"!

---

## Ⅲ. 행렬 빠른 거듭제곱

```
행렬 빠른 거듭제곱:
  스칼라 거듭제곱과 동일한 반복 제곱법을 행렬에 적용

피보나치 O(log N) 계산:

점화식:
  F(n) = F(n-1) + F(n-2)

행렬 표현:
  [F(n+1)]   [1 1]^n   [F(1)]
  [F(n)  ] = [1 0]   × [F(0)]

  [1 1]^n = 행렬 A의 n제곱
  [1 0]

  A^n을 빠른 거듭제곱으로 계산 -> O(log n)

구현:
  def mat_mul(A, B, mod):
      n = len(A)
      C = [[0]*n for _ in range(n)]
      for i in range(n):
          for k in range(n):
              if A[i][k] == 0: continue
              for j in range(n):
                  C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
      return C

  def mat_pow(A, p, mod):
      n = len(A)
      result = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
      while p > 0:
          if p & 1:
              result = mat_mul(result, A, mod)
          A = mat_mul(A, A, mod)
          p >>= 1
      return result

  def fib(n, mod=10**9+7):
      if n <= 1: return n
      A = [[1, 1], [1, 0]]
      M = mat_pow(A, n-1, mod)
      return M[0][0]

  # F(10^18 mod 10^9+7) 계산 가능!

응용:
  선형 점화식 일반 풀이:
  a[n] = c1*a[n-1] + c2*a[n-2] + ... + ck*a[n-k]
  -> k×k 행렬 거듭제곱으로 O(k³ log n) 해결

  타일링 문제, 계단 오르기, 경로 수 계산...
```

> 📢 **섹션 요약 비유**: 행렬 거듭제곱 = 변환 반복 빠른 계산 — 피보나치를 100억 번 더하는 대신 행렬 변환을 33번 적용(log₂ 10^10 ≈ 33). F(10^18)도 60번 행렬 곱으로!

---

## Ⅳ. 코딩테스트 활용 패턴

```
패턴 1: 대용량 거듭제곱 mod p
  문제: a^b mod (10^9+7) 계산 (b ≤ 10^18)
  -> pow(a, b, 10**9+7)

패턴 2: 모듈러 역원 (Modular Inverse)
  a^(p-2) mod p = a의 역원 (페르마 소정리, p는 소수)
  -> pow(a, p-2, p)

패턴 3: 이항계수 mod p
  C(n, k) mod p:
  MOD = 10**9 + 7
  fact = [1] * (n+1)
  for i in range(1, n+1): fact[i] = fact[i-1] * i % MOD

  def nCr(n, k):
      return fact[n] * pow(fact[k], MOD-2, MOD) % MOD * pow(fact[n-k], MOD-2, MOD) % MOD

패턴 4: 피보나치 n번째 (n ≤ 10^18)
  행렬 거듭제곱 사용

패턴 5: 경우의 수 mod p (곱의 역원)
  P(n, k) = n! / (n-k)!
  -> fact[n] * pow(fact[n-k], MOD-2, MOD) % MOD

주의사항:
  Python pow(a, b, m)은 C 최적화됨 -> 빠름
  직접 구현보다 pow() 내장 우선 사용

  mod 연산: 각 단계에서 취하지 않으면 수 폭발
  a = 2, b = 10^18, mod 없으면:
  -> 10^(3×10^17) 자리 수 -> 불가능
```

> 📢 **섹션 요약 비유**: 코딩테스트 거듭제곱 패턴 — "큰 수 mod p" = pow(a,b,m). "모듈러 역원" = pow(a,p-2,p). "이항계수" = 팩토리얼 × 역원×역원. 3가지 패턴 암기로 80% 해결!

---

## Ⅴ. 실무 시나리오 — 블록체인 서명 검증

```
ECDSA 서명 검증에서의 모듈러 거듭제곱:

배경:
  비트코인/이더리움: ECDSA (타원 곡선 디지털 서명)
  타원 곡선 점 덧셈 + 스칼라 곱셈

내부 연산:
  타원 곡선 스칼라 곱셈: k × G
  (G: 생성 점, k: 개인키)

  구현: 이중-덧셈 알고리즘 (Double-and-Add)
  빠른 거듭제곱과 동일한 원리!

  k의 이진수 표현에서:
  각 비트: 0이면 2배(Double), 1이면 2배 후 덧셈(Add)
  -> O(log k) 번 연산

서명 검증 과정:
  1. 서명 (r, s) 수신
  2. 공개키 Q = d × G (d: 개인키)
  3. 검증: u1 = H(m) × s^(-1) mod p
             u2 = r × s^(-1) mod p
  4. R = u1 × G + u2 × Q
  5. R.x == r 이면 유효

모듈러 역원:
  s^(-1) mod p = pow(s, p-2, p)  (페르마 소정리)
  (secp256k1: p = 2^256 - 2^32 - 977)

성능:
  Bitcoin 서명 검증: 수 밀리초
  블록 1개 ~2000 거래 검증: 수 초

결론:
  고대 반복 제곱법 -> 현대 블록체인 보안의 기반
  RSA 암호화, ECDSA, ECC 모두 빠른 거듭제곱 필수
```

> 📢 **섹션 요약 비유**: 블록체인 서명 검증 = 타원 곡선 도장 찍기 — 개인키(k)로 공개키(k×G) 생성. 역산 불가(이산 로그 문제). 검증은 빠른 거듭제곱 덕에 수 ms. 수학이 블록체인 보안!

---

## 📌 관련 개념 맵

```
빠른 거듭제곱 (Fast Exponentiation)
+-- 핵심: 반복 제곱법 O(log b)
+-- 응용
|   +-- 모듈러 거듭제곱 (a^b mod m)
|   +-- 행렬 거듭제곱 (피보나치)
|   +-- 타원 곡선 스칼라 곱 (ECDSA)
+-- 암호학 연결
|   +-- RSA 암호화/복호화
|   +-- 밀러-라빈 소수 판별
|   +-- 디피-헬만 키 교환
+-- 코딩테스트 패턴
    +-- pow(a, b, m) 내장 활용
    +-- 모듈러 역원
    +-- 이항계수 mod p
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[고대 이집트 배수법 (기원전 1600년)]
곱셈을 배로 줄이기
빠른 거듭제곱의 원형
      |
      v
[RSA 암호화 (1977)]
모듈러 거듭제곱 필수화
암호학 응용
      |
      v
[ECC (Elliptic Curve, 1985)]
타원 곡선 점 스칼라 곱
더 작은 키 + 동등 보안
      |
      v
[블록체인 ECDSA (2008~)]
비트코인 secp256k1
거래 서명 검증
      |
      v
[현재: 양자 저항 암호]
격자 기반 서명
빠른 거듭제곱 원리 계속
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 반복 제곱법 = 종이 접기 — 10번 접으면 1024배 두께. a^1024도 10번 제곱(×10)으로! 1000번 곱하기 대신 10번!
2. 모듈러 거듭제곱 = 시계 계산 — 큰 수를 12시간 시계로 계산. RSA 암호화도 시계(mod) 안에서 거듭제곱!
3. 행렬 거듭제곱 = 피보나치 마법 — F(10^18)을 60번 행렬 곱으로 계산. 10^18번 더하기 대신 60번으로!
