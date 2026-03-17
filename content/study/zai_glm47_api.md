+++
title = "Z.AI API 사용법 (GLM-4.7) — CURL 완전 가이드"
date = "2026-02-28"
[extra]
categories = "devops"
+++

# Z.AI API 사용법 (GLM-4.7) — CURL 완전 가이드

## 핵심 인사이트 (3줄 요약)

> **Z.AI**는 GLM-4.7 모델을 Anthropic Messages API 포맷으로 제공하는 서비스다.
> 기존 Anthropic/Claude API와 동일한 스펙으로, 헤더와 엔드포인트만 바꾸면 바로 사용 가능하다.
> CURL 한 줄로 요청하며, 스트리밍 · 멀티턴 대화 · 커스텀 시스템 프롬프트를 모두 지원한다.

---

## 1. 개념

| 항목 | 설명 |
|------|------|
| **Z.AI** | 중국 Zhipu AI의 API 서비스 플랫폼 |
| **GLM-4.7** | Z.AI 최신 언어 모델 (General Language Model) |
| **API 포맷** | Anthropic Messages API 호환 (`/v1/messages`) |
| **인증 방식** | Bearer 토큰 (`Authorization: Bearer <key>`) |
| **언어** | 한국어 포함 다국어 지원 |

---

## 2. 설정

### 환경 변수

```bash
# API Key (Z.AI 콘솔에서 발급)
export ZAI_API_KEY="your_api_key_here"

# API 엔드포인트
export ZAI_BASE_URL="https://api.z.ai/api/anthropic/v1/messages"

# 모델
export ZAI_MODEL="glm-4.7"
```

---

## 3. CURL 사용법

### 3.1 기본 요청

```bash
curl -s "$ZAI_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -d '{
    "model": "glm-4.7",
    "messages": [{"role": "user", "content": "안녕하세요"}],
    "max_tokens": 1024
  }'
```

### 3.2 시스템 프롬프트 포함

```bash
curl -s "$ZAI_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -d '{
    "model": "glm-4.7",
    "system": "당신은 유능한 기술 문서 작성자입니다.",
    "messages": [{"role": "user", "content": "Rust의 소유권 개념을 설명해줘"}],
    "max_tokens": 2048
  }'
```

### 3.3 멀티턴 대화

```bash
curl -s "$ZAI_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -d '{
    "model": "glm-4.7",
    "messages": [
      {"role": "user",      "content": "Rust란 무엇인가요?"},
      {"role": "assistant", "content": "Rust는 시스템 프로그래밍 언어로..."},
      {"role": "user",      "content": "소유권 개념을 더 자세히 설명해줘"}
    ],
    "max_tokens": 2048
  }'
```

### 3.4 스트리밍 응답

```bash
curl -s "$ZAI_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -d '{
    "model": "glm-4.7",
    "messages": [{"role": "user", "content": "긴 글을 써줘"}],
    "max_tokens": 4096,
    "stream": true
  }'
```

---

## 4. 테스트 스크립트 (test_zai_api.sh)

```bash
#!/bin/bash
# test_zai_api.sh

# Configuration
ZAI_API_KEY="YOUR_API_KEY"
ZAI_BASE_URL="https://api.z.ai/api/anthropic/v1/messages"
ZAI_MODEL="glm-4.7"

echo "=== Z.AI API 연결 테스트 ==="

RESPONSE=$(curl -s "$ZAI_BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -d "{
    \"model\": \"$ZAI_MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"안녕하세요\"}],
    \"max_tokens\": 256
  }")

echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
```

실행:
```bash
chmod +x test_zai_api.sh
./test_zai_api.sh
```

---

## 5. 응답 예시

```json
{
  "id": "msg_2026020109373013301dbd71d34b21",
  "type": "message",
  "role": "assistant",
  "model": "glm-4.7",
  "content": [
    {
      "type": "text",
      "text": "안녕하세요! 반갑습니다. 😊\n\n저는 Z.ai의 GLM-4.7 모델입니다..."
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 9,
    "output_tokens": 30,
    "cache_read_input_tokens": 0
  }
}
```

응답에서 텍스트만 추출:
```bash
echo "$RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data['content'][0]['text'])
"
```

---

## 6. API 레퍼런스

### 헤더

| 헤더 | 값 | 설명 |
|------|-----|------|
| `Content-Type` | `application/json` | JSON 형식 |
| `Authorization` | `Bearer YOUR_KEY` | Bearer 토큰 인증 |

### 요청 파라미터

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `model` | string | ✅ | 사용할 모델 ID |
| `messages` | array | ✅ | 대화 메시지 배열 (`role` + `content`) |
| `max_tokens` | int | ✅ | 최대 출력 토큰 수 |
| `system` | string | ❌ | 시스템 프롬프트 |
| `stream` | bool | ❌ | 스트리밍 여부 (기본: false) |
| `temperature` | float | ❌ | 창의성 조절 0.0~1.0 (기본: 1.0) |
| `top_p` | float | ❌ | 누클리어스 샘플링 |

### messages 배열 구조

```json
[
  {"role": "user",      "content": "질문"},
  {"role": "assistant", "content": "답변"},
  {"role": "user",      "content": "후속 질문"}
]
```

---

## 7. 지원 모델

| 모델 | 특징 | 용도 |
|------|------|------|
| **glm-4.7** | 최신 모델 (권장) | 범용 |
| **glm-4-plus** | 고성능 | 복잡한 추론 |
| **glm-4-flash** | 빠른 응답 | 실시간 응용 |

---

## 8. Python으로 사용하기

```python
import requests
import os

url = "https://api.z.ai/api/anthropic/v1/messages"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['ZAI_API_KEY']}"
}
payload = {
    "model": "glm-4.7",
    "messages": [{"role": "user", "content": "안녕하세요"}],
    "max_tokens": 1024
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data["content"][0]["text"])
```

---

## 9. Anthropic SDK 호환 사용

Z.AI는 Anthropic API 포맷을 그대로 사용하므로, Anthropic 공식 SDK에서 `base_url`만 바꿔도 작동한다.

```python
import anthropic

client = anthropic.Anthropic(
    api_key="YOUR_ZAI_API_KEY",
    base_url="https://api.z.ai/api/anthropic"
)

message = client.messages.create(
    model="glm-4.7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "안녕하세요"}]
)
print(message.content[0].text)
```

---

## 10. 주의사항

| 항목 | 내용 |
|------|------|
| **API Key 보안** | `.env` 파일 사용, 절대 코드에 하드코딩 금지 |
| **max_tokens** | 너무 크게 설정하면 비용 증가. 용도에 맞게 설정 |
| **rate limit** | 요청 횟수 제한 있음 — 콘솔에서 확인 |
| **스트리밍** | 긴 응답은 `stream: true`로 UX 개선 권장 |

---

## 참고

- Z.AI 공식 문서
- API Key 발급
- Anthropic Messages API 스펙