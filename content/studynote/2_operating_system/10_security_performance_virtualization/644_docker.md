+++
title = "644. Docker"
date = "2026-03-16"
weight = 644
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Docker", "컨테이너", "이미지", "Dockerfile", "Docker Compose"]
+++

# Docker

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Docker는 **컨테이너 기반 애플리케이션 패키징 및 실행 플랫폼**으로, Linux 커널의 Namespace, Cgroups, Union FS를 활용하여 가볍고 격리된 실행 환경을 제공한다.
> 2. **가치**: "Build once, run anywhere"를 실현하여 **개발/테스트/운영 환경 차이를 해소**하고, 마이크로서비스, CI/CD의 표준 인프라가 되었다.
> 3. **융합**: Docker Engine, Docker Hub(레지스트리), Docker Compose, Docker Swarm 등 **생태계**를 형성하며, Kubernetes와 호환된다.

+++

## Ⅰ. Docker의 개요

### 1. 정의
- Docker는 컨테이너를 생성, 배포, 실행하는 오픈소스 플랫폼이다.
- 2013년 Solomon Hykes(Dotcloud) 발표

### 2. 등장 배경
- 기존 가상화(VM)는 무겁고 느림
- LXC(Linux Containers)는 복잡함
- Docker는 "Simple as possible"을 목표로 대중화

### 3. 💡 비유: '컨테이너선의 컨테이너'
- Docker는 실제 **화물 컨테이너**와 같다.
- 어떤 배(앱)든 표준 크기의 컨테이너에 담으면, 어떤 배(선/트럭/기차)에도 실을 수 있다.

- **📢 섹션 요약 비유**: 도시락(이미지)에 반찬(앱+의존성)을 담아두면, 어디서나 그대로 꺼내 먹을 수 있죠? Docker는 그 도시락을 만드는 도구입니다.

+++

## Ⅱ. Docker 아키텍처 (Deep Dive)

### 1. Docker Engine 구조
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                   Docker Engine 아키텍처                        │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Docker CLI] docker ps, docker run...                         │
    │         │                                                       │
    │         │ REST API                                             │
    │         ▼                                                       │
    │  ┌─────────────────────────────────────────────────────────┐   │
    │  │                  dockerd (Docker Daemon)                │   │
    │  │  - 이미지 관리                                         │   │
    │  │  - 컨테이너 생명주기 관리                              │   │
    │  │  - 네트워크/볼륨 관리                                  │   │
    │  │  - API 서버                                            │   │
    │  └───────────────────┬─────────────────────────────────────┘   │
    │                      │                                          │
    │         ┌────────────┼────────────┐                           │
    │         │            │            │                           │
    │         ▼            ▼            ▼                           │
    │   ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
    │   │containerd│  │ runc    │  │ shim    │                      │
    │   │(이미지) │  │(실행)   │  │(데몬)   │                      │
    │   └─────────┘  └─────────┘  └─────────┘                      │
    │                                            │                   │
    │                                            ▼                   │
    │                                   [Kernel]                     │
    │                                   Namespace, Cgroups,         │
    │                                   Union FS                    │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. 핵심 컴포넌트
| 컴포넌트 | 설명 |
|:---|:---|
| **dockerd** | Docker 데몬, API 서버, 모든 작업 조율 |
| **containerd** | OCI 호환 컨테이너 런타임, 이미지 관리 |
| **runc** | OCI 표준 컨테이너 실행 도구 |
| **shim** | 데몬 없이 컨테이너 실행, headless 컨테이너 담당 |

### 3. Docker 오브젝트
- **Image**: 읽기 전용 템플릿
- **Container**: Image의 실행 인스턴스
- **Service**: Swarm 모드의 배포 단위
- **Stack**: 여러 Service의 그룹

- **📢 섹션 요약 비유**: 이미지는 "설계도", 컨테이너는 "실제 건물"입니다. 설계도를 여러 번 사용하여 여러 건물을 지을 수 있죠.

+++

## Ⅲ. Dockerfile

### 1. Dockerfile 지시어
```dockerfile
# Base Image
FROM ubuntu:22.04

# Metadata
LABEL maintainer="admin@example.com"
LABEL version="1.0"

# Working directory
WORKDIR /app

# Dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application
COPY . .

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose ports
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Run command
CMD ["python3", "app.py"]
```

### 2. Layer 최적화
```dockerfile
# Bad
RUN apt-get update
RUN apt-get install -y python3
RUN pip3 install flask

# Good (한 줄로 합치기)
RUN apt-get update && \
    apt-get install -y python3 && \
    pip3 install flask && \
    rm -rf /var/lib/apt/lists/*
```

+++

## Ⅳ. Docker 네트워크

### 1. 네트워크 드라이버
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                 Docker 네트워크 드라이버                          │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [bridge] (기본)                                               │
    │   - 컨테이너 간 통신 (동일 호스트)                              │
    │   - docker0 브릿지 사용                                        │
    │                                                                 │
    │  [host]                                                         │
    │   - 호스트 네트워크 스택 공유                                   │
    │   - 성능 우수, 격리 없음                                        │
    │                                                                 │
    │  [none]                                                         │
    │   - 네트워크 없음                                               │
    │                                                                 │
    │  [overlay]                                                     │
    │   - 다중 호스트 컨테이너 통신 (Swarm)                           │
    │   - VXLAN 기반                                                 │
    │                                                                 │
    │  [macvlan]                                                     │
    │   - 컨테이너에 MAC 주소 할당                                   │
    │   - 네트워크에 직접 연결                                       │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. 네트워크 명령어
```bash
# 네트워크 생성
docker network create my-net

# 컨테이너를 네트워크에 연결
docker run --network my-net --name web nginx

# 컨테이너 간 통신 (DNS)
docker exec web ping db
```

+++

## Ⅴ. Docker 저장소 (Volume)

### 1. 데이터 지속성
```bash
# 볼륨 생성
docker volume create my-data

# 컨테이너에 볼륨 마운트
docker run -v my-data:/data ubuntu

# 바인드 마운트 (호스트 디렉토리)
docker run -v /host/path:/container/path ubuntu

# tmpfs (메모리)
docker run --tmpfs /tmp:rw,size=100m ubuntu
```

+++

## Ⅵ. Docker Compose

### 1. Compose 파일 (YAML)
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:alpine

volumes:
  db-data:
```

### 2. Compose 명령어
```bash
# 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f web

# 서비스 중지
docker-compose down

# 스케일
docker-compose up -d --scale web=3
```

+++

## Ⅶ. 실무 적용 및 안티패턴

### 1. 모범 사례
1. **알파인 이미지**: `alpine`, `distroless` 사용
2. **멀티스테이지 빌드**: 빌드와 실행 분리
3. **최소 권한**: USER 지정 (root 아님)
4. **레이어 최소화**: Dockerfile 최적화
5. **태그 고정**: `latest` 피하기

### 2. 멀티스테이지 Dockerfile
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Run stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
CMD ["node", "server.js"]
```

### 3. 안티패턴
- **"Fat Container"**: 한 컨테이너에 모든 것
- **"Latest Tag"**: 버전 고정 안 함
- **"Root 실행"**: 보안 위험
- **"Secrets in Image"**: 환경 변수에 비밀

+++

## Ⅷ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **배포 속도**: 분 단위
- **환경 일관성**: 개발=운영
- **리소스 효율**: VM 대비 2~3배

### 2. 미래 전망
- **WebAssembly**: WASM 컨테이너
- **Chainguard**: 보안 중심 이미지

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **컨테이너**: 기반 기술
- **Kubernetes**: 오케스트레이션
- **마이크로서비스**: 주요 용도
- **CI/CD**: DevOps 통합

+++

## 👶 어린이를 위한 3줄 비유 설명
1. Docker는 **"도시락을 만드는 기계"**예요.
2. 밥과 반찬(앱과 친구들)을 넣고 뚜껑을 담으면, 어디서든 꺼내 먹을 수 있는 도시락이 완성되죠.
3. 이 도시락(컨테이너)을 배달(배포)해서 아무리 많은 사람에게도 똑같은 맛을 선사할 수 있어요!