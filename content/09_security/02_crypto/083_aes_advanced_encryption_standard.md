---
title: "Aes Advanced Encryption Standard"
date: "2026-04-05"
tags:
  - "studynote-security"
weight: 83
---
## 핵심 인사이트 (3줄 요약)
- **본질**: AES (Advanced Encryption Standard)는 128비트 블록을 10/12/14라운드로 섞는 대칭키 블록 암호이며, Rijndael 설계를 표준화한 것이다.
- **가치**: NIST (National Institute of Standards and Technology) 표준과 AES-NI (AES New Instructions) 덕분에 강한 보안성과 높은 성능을 동시에 얻는다.
- **판단 포인트**: AES 코어만 보고 안전하다고 끝내면 안 되고, ECB (Electronic Codebook)/CBC (Cipher Block Chaining)/CTR (Counter)/GCM (Galois/Counter Mode) 같은 운용 모드와 nonce/IV (Initialization Vector)/키 관리가 실제 보안을 결정한다.

---

## Ⅰ. 개요 및 필요성

AES (Advanced Encryption Standard)는 56비트 DES (Data Encryption Standard)가 더 이상 버티지 못하던 상황에서 나온 차세대 표준이다. 1990년대 후반에는 병렬 컴퓨팅으로 DES를 짧은 시간에 깨는 것이 가능해졌고, 이에 따라 NIST (National Institute of Standards and Technology)는 공개 경쟁을 통해 새 표준을 뽑았다. 그 결과 2001년 Rijndael이 AES로 채택되었다.

핵심은 "키가 짧으면 시간이 문제를 해결한다"는 점이다. AES는 이 문제를 키 길이와 구조로 동시에 해결했다. 128비트 블록은 고정하고, 키는 128/192/256비트로 제공해 장기 보안 요구와 성능 요구를 나눠 받는다.

```text
DES(56bit) -► 전수조사 취약 -► NIST 공모전 -► Rijndael -► AES
```

- **📢 섹션 요약 비유**: 4자리 자물쇠가 너무 빨리 풀리자, 더 길고 더 촘촘한 새 자물쇠를 표준으로 정한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AES는 4x4 바이트 행렬(State) 위에서 동작한다. 블록 크기는 128비트로 고정이고, 키 길이에 따라 라운드 수가 달라진다. AES-128은 10라운드, AES-192는 12라운드, AES-256은 14라운드를 수행한다.

| 키 길이 | 라운드 수 | 특징 |
| :--- | :--- | :--- |
| 128비트 | 10 | 일반 서비스의 기본값 |
| 192비트 | 12 | 중간 타협점 |
| 256비트 | 14 | 장기 보안·고위험 데이터 |

라운드마다 수행하는 핵심 연산은 네 가지다. SubBytes는 S-Box로 바이트를 비선형 치환하고, ShiftRows는 행을 밀어 확산을 돕는다. MixColumns는 GF(2^8) 곱셈으로 열을 섞고, AddRoundKey는 라운드 키를 XOR한다. 마지막 라운드에서는 MixColumns를 생략한다.

```text
+---------------------------------------------------------------------+
| 평문 128비트 -> State -> SubBytes -> ShiftRows -> MixColumns -> XOR 키 |
|                              +------------ 라운드 반복 ------------+|
+---------------------------------------------------------------------+
```

AES-NI (AES New Instructions)는 이 과정을 CPU 명령어로 가속한다. 그래서 같은 AES라도 소프트웨어만 쓰는 경우보다 훨씬 빠르고, TLS (Transport Layer Security)나 파일 암호화 같은 실무 환경에서 충분한 처리량을 낸다.

- **📢 섹션 요약 비유**: 큐브의 색을 바꾸고, 줄을 밀고, 한 번 더 섞고, 마지막 열쇠를 꽂는 작업을 여러 번 반복하는 기계식 퍼즐이다.

---

## Ⅲ. 비교 및 연결

AES가 DES와 다른 점은 키 길이뿐 아니라 구조다. DES는 Feistel 구조였고, AES는 SPN (Substitution-Permutation Network) 구조다. SPN은 전체 블록을 한 번에 비선형 치환과 확산으로 섞기 때문에 하드웨어 구현과 병렬화에 유리하다.

운용 모드도 핵심이다. AES 코어는 한 블록을 변환할 뿐이므로, 여러 블록을 어떻게 엮을지는 모드가 정한다. ECB (Electronic Codebook)는 패턴을 그대로 노출해 구조화된 데이터에 쓰면 안 되고, CBC (Cipher Block Chaining)는 IV (Initialization Vector)와 체인을 사용하지만 병렬성이 낮다. CTR (Counter)은 스트림처럼 쓰기 쉬우나 nonce 재사용이 치명적이며, GCM (Galois/Counter Mode)은 기밀성과 무결성을 함께 제공하는 AEAD (Authenticated Encryption with Associated Data) 모드다.

| 모드 | 병렬성 | 패턴 노출 | 무결성 | 판단 |
| :--- | :--- | :--- | :--- | :--- |
| ECB | 높음 | 있음 | 없음 | 구조가 보이므로 회피 |
| CBC | 낮음 | 적음 | 없음 | 레거시 사용 |
| CTR | 높음 | 없음 | 없음 | nonce 관리 필수 |
| GCM | 높음 | 없음 | 있음 | 실무 기본값 |

AES는 TLS, VPN (Virtual Private Network), 파일 암호화, 디스크 암호화에서 흔히 쓰이지만, 프로토콜 전체 보안을 다 해결하지는 않는다. 키 교환, 인증, 재전송 방지 같은 기능은 상위 계층이 맡아야 한다.

- **📢 섹션 요약 비유**: 암호기계(AES) 자체도 중요하지만, 상자에 묶는 끈(모드)까지 제대로 써야 내용물이 안 새어난다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 보통 AES-128-GCM이 기본 선택이다. 일반적인 웹/모바일 트래픽에서는 처리량과 보안의 균형이 좋고, AES-NI가 있으면 더 유리하다. 반면 장기 보존이 필요하거나, 키 노출 후 회복 여지가 작거나, 양자 위협을 길게 보아야 하면 AES-256-GCM이 더 안전하다.

체크리스트는 다음과 같다.
1. ECB처럼 패턴이 드러나는 모드를 쓰고 있지 않은가?
2. CTR/GCM의 nonce가 절대 재사용되지 않는가?
3. CBC의 IV (Initialization Vector)가 적절히 무작위인가?
4. 키가 코드에 하드코딩되지 않았는가?
5. AES-NI가 가능한 환경에서 비활성화돼 있지 않은가?

Grover 알고리즘은 양자 컴퓨터에서 전수조사의 효율을 사실상 제곱근으로 줄인다. 그래서 장기 기밀이나 미래 위험을 크게 보아야 할 상황에서는 AES-256을 우선하는 편이 낫다. 하지만 알고리즘만 바꾼다고 끝나는 것은 아니고, 키 저장·회전·폐기 전략이 더 중요하다.

- **📢 섹션 요약 비유**: 좋은 자물쇠도 번호를 아무 데나 적어 두면 소용이 없다. 열쇠 관리가 진짜 잠금의 절반이다.

---

## Ⅴ. 기대효과 및 결론

AES의 강점은 표준화, 성능, 구현 용이성이다. 하지만 "AES를 쓴다"가 곧 "안전하다"를 의미하지는 않는다. 모드, nonce, IV, 키 관리가 같이 맞아야 실무 보안이 완성된다.

결론적으로 AES는 현대 대칭키 보안의 기준선이다. 앞으로도 TLS, VPN, 파일 보호의 기본 재료로 남겠지만, 양자 시대를 대비한 키 길이 선택과 AEAD 중심 설계는 더 중요해질 것이다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| DES (Data Encryption Standard) | AES로 대체된 전신 |
| SPN (Substitution-Permutation Network) | AES의 내부 구조 |
| ECB/CBC/CTR/GCM | 블록을 연결하는 운용 모드 |
| AEAD (Authenticated Encryption with Associated Data) | 기밀성과 무결성을 함께 제공 |
| AES-NI (AES New Instructions) | 하드웨어 가속 명령어 |
| TLS (Transport Layer Security) / VPN (Virtual Private Network) | 대표 사용처 |

### 📈 관련 키워드 및 발전 흐름도

```text
DES
    |
    v
AES (Advanced Encryption Standard)
    |
    +--------► AES-NI (AES New Instructions)
    |
    +--------► CBC / CTR / GCM
    |
    +--------► TLS / VPN / 파일 암호화
```

### 👶 어린이를 위한 3줄 비유 설명

1. AES는 비밀 상자를 여러 번 빙글빙글 섞는 아주 강한 자물쇠예요.
2. 그런데 상자를 어떻게 묶느냐가 중요해서, 묶는 방법이 틀리면 내용이 보일 수 있어요.
3. 그래서 자물쇠만 믿지 말고, 열쇠 관리와 묶는 방법도 같이 잘해야 해요.
