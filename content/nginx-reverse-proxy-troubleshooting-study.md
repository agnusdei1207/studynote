+++
title = "Nginx 리버스 프록시 충돌 트러블슈팅 스터디"
date = "2026-03-17"
[extra]
keyword = "Nginx_ReverseProxy_Troubleshooting"
+++

# Nginx 리버스 프록시 충돌 트러블슈팅 스터디

## 개요
한 서버에서 여러 서비스 도메인을 Nginx로 프록시하는 환경에서, 새 프론트엔드 서비스를 추가한 뒤 설정상으로는 정상인데 실제 요청이 의도한 upstream으로 가지 않는 문제가 발생할 수 있다.

이 문서는 특정 프로젝트 이름, 실제 도메인, 실제 IP를 모두 마스킹한 상태에서 문제 원인과 해결 절차를 정리한 일반 스터디 노트다.

## 환경 요약
- Ubuntu 서버 1대
- Docker Compose로 여러 프론트엔드/백엔드 컨테이너 운영
- 호스트 Nginx가 각 도메인을 내부 포트로 reverse proxy
- Let's Encrypt `certbot`으로 인증서 발급
- 신규 서비스가 `localhost:4004`로 배포됨

예시 구조:
- `atlas-portal.example.test` -> `localhost:4000`
- `ember-hub.example.test` -> `localhost:4001`
- `lumen-space.example.test` -> `localhost:4002`
- `orbit-view.example.test` -> `localhost:4003`
- `maple-fair.example.test` -> `localhost:4004`

## 증상
신규 서비스 컨테이너는 정상적으로 실행 중이었다.

예를 들어 Docker Compose에는 아래와 같이 포트 매핑이 있었다.

```yaml
services:
  event:
    image: registry.example.com/event:latest
    restart: always
    ports:
      - 4004:80
```

컨테이너 로그도 정상이고, 설정 파일에서도 아래처럼 보였다.

```nginx
server {
    listen 80;
    server_name maple-fair.example.test www.maple-fair.example.test;

    location / {
        proxy_set_header Host $host;
        proxy_pass http://localhost:4004;
    }
}
```

하지만 실제로는 요청이 기대한 서비스로 가지 않거나, 설정을 수정해도 반영이 이상하게 보였다.

## 처음 의심하기 쉬운 오해
보통 아래를 먼저 의심한다.

- Docker Compose 포트 매핑 오류
- 컨테이너 비정상 실행
- `proxy_pass` 오타
- 방화벽 문제
- 애플리케이션 자체 에러

이번 케이스에서는 이쪽이 본질적 원인이 아니었다. `4004` 자체는 정상적으로 열려 있었고, 컨테이너도 정상 실행 중이었다.

## 실제 원인
핵심 원인은 Nginx `server_name` 충돌이었다.

문제가 된 패턴은 다음과 같다.

### 1. 신규 도메인용 전용 `server` 블록이 이미 존재

```nginx
server {
    listen 80;
    server_name maple-fair.example.test www.maple-fair.example.test;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type "text/plain";
        try_files $uri =404;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://localhost:4004;
    }
}
```

### 2. 맨 아래 공용 HTTP 리다이렉트 블록에도 같은 도메인이 또 포함됨

```nginx
server {
    listen 80;
    server_name atlas-portal.example.test www.atlas-portal.example.test ember-hub.example.test orbit-view.example.test lumen-space.example.test maple-fair.example.test www.maple-fair.example.test;

    return 301 https://$host$request_uri;
}
```

이렇게 되면 같은 `listen 80`에서 같은 `server_name`을 두 개의 블록이 동시에 잡는다.

그 결과 Nginx는 reload 시 다음과 같은 경고를 낸다.

```text
conflicting server name "maple-fair.example.test" on 0.0.0.0:80, ignored
conflicting server name "www.maple-fair.example.test" on 0.0.0.0:80, ignored
```

즉, 설정 파일상으로는 맞아 보여도 실제로는 어떤 블록이 무시되면서 요청 라우팅이 기대와 다르게 동작한다.

## 부가 원인
추가로 `server_name` 문자열에 공백이 빠진 오타도 있었다.

예시:

```nginx
server_name ember-hub.example.testorbit-view.example.test;
```

원래는 아래여야 한다.

```nginx
server_name ember-hub.example.test orbit-view.example.test;
```

이런 오타는 충돌과 별개로 특정 도메인이 매칭되지 않는 원인이 된다.

## 왜 신규 서비스만 따로 보였는가
기존 도메인들은 단순히 `80 -> 443` 리다이렉트만 처리해도 됐지만, 신규 도메인은 인증서 발급을 위해 `/.well-known/acme-challenge/` 경로를 `80`에서 직접 제공해야 했다.

즉 신규 도메인은 아래 두 조건이 동시에 필요했다.

- `80`에서 ACME challenge 응답 가능
- `443`에서 최종 서비스 프록시 가능

그래서 신규 도메인을 공용 리다이렉트 블록에 그대로 넣어두면 전용 블록과 충돌한다.

## 해결 방법
핵심은 아주 단순했다.

### 1. 신규 도메인을 공용 `80 -> 443` 리다이렉트 블록에서 제거

수정 전:

```nginx
server_name atlas-portal.example.test www.atlas-portal.example.test ember-hub.example.test orbit-view.example.test lumen-space.example.test maple-fair.example.test www.maple-fair.example.test;
```

수정 후:

```nginx
server_name atlas-portal.example.test www.atlas-portal.example.test ember-hub.example.test orbit-view.example.test lumen-space.example.test;
```

### 2. 신규 도메인은 전용 블록만 사용

HTTP:

```nginx
server {
    listen 80;
    server_name maple-fair.example.test www.maple-fair.example.test;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type "text/plain";
        try_files $uri =404;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://localhost:4004;
    }
}
```

HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name maple-fair.example.test www.maple-fair.example.test;

    ssl_certificate /etc/letsencrypt/live/maple-fair.example.test/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/maple-fair.example.test/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_set_header Host $host;
        proxy_pass http://localhost:4004;
    }
}
```

### 3. 오타 수정

- `ember-hub.example.testorbit-view.example.test`
- -> `ember-hub.example.test orbit-view.example.test`

## Certbot 설정 절차
신규 도메인 추가 시 인증서 발급 절차는 아래 흐름이 안전하다.

### 1. ACME 경로용 디렉터리 준비

```bash
mkdir -p /var/www/certbot/.well-known/acme-challenge
chown -R www-data:www-data /var/www/certbot
chmod -R 755 /var/www/certbot
```

### 2. HTTP 블록 적용 후 Nginx 검사

```bash
sudo nginx -t
sudo nginx -s reload
```

### 3. ACME 경로 테스트

```bash
echo test > /var/www/certbot/.well-known/acme-challenge/test
curl http://maple-fair.example.test/.well-known/acme-challenge/test
```

정상이라면 `test`가 출력되어야 한다.

### 4. 인증서 발급

```bash
certbot certonly --webroot -w /var/www/certbot -d maple-fair.example.test -d www.maple-fair.example.test
```

### 5. 443 블록 추가 후 다시 반영

```bash
sudo nginx -t
sudo nginx -s reload
```

## 최종 점검 포인트
새 도메인을 추가할 때는 아래를 반드시 함께 확인한다.

- Docker 컨테이너가 실제로 올라와 있는가
- 내부 포트 매핑이 맞는가
- 해당 도메인이 Nginx에서 단 한 번만 선언되는가
- `80` 리다이렉트 블록과 전용 블록이 충돌하지 않는가
- `server_name` 사이 공백 누락 같은 단순 오타가 없는가
- `certbot` webroot 경로가 실제로 외부에서 접근 가능한가

## 정리
이번 이슈의 본질은 애플리케이션 문제가 아니라 Nginx 라우팅 정의 충돌이었다.

한 줄로 요약하면 다음과 같다.

- 신규 서비스의 upstream 포트는 정상
- 실제 문제는 동일 도메인을 여러 `server` 블록이 중복 선언한 것
- 신규 도메인은 ACME 처리 때문에 공용 리다이렉트 블록과 분리해야 함

여러 도메인을 한 서버에서 운용할수록, 신규 서비스 추가 시 가장 먼저 볼 것은 Docker보다도 Nginx `server_name` 충돌 여부다.