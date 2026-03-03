+++
title = "도커와 컨테이너 (Docker & Container)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 도커와 컨테이너 (Docker & Container)

## 핵심 인사이트 (3줄 요약)
> **애플리케이션을 경량 격리 환경에서 실행**하는 OS 수준 가상화. Namespace + Cgroups로 격리, UnionFS로 효율적 저장. "Build once, Run anywhere" 실현.

---

### Ⅰ. 개요

**개념**: 컨테이너는 **호스트 OS 커널을 공유하면서 Namespace와 Cgroups로 격리된 환경에서 애플리케이션을 실행하는 경량 가상화 기술**이다. 도커(Docker)는 컨테이너 생성, 배포, 실행을 표준화한 플랫폼이다.

> 💡 **비유**: "컨테이너는 표준화된 컨테이너 박스" - 어떤 배에 실어도, 어떤 항구에서 내려도 똑같이 운반돼요. 안에 뭐가 들었는지 몰라도 박스만 옮기면 돼요!

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: "내 컴퓨터에서는 되는데 서버에서는 안 돼요" - 개발 환경과 운영 환경의 차이로 배포 시 문제 빈발. VM은 무겁고 느려서 빠른 배포 불가능
2. **기술적 필요성**: 애플리케이션과 의존성을 함께 패키징하여 환경 차이 무관하게 실행하는 표준화된 방법 필요
3. **산업적 요구**: 마이크로서비스, CI/CD, 클라우드 네이티브 아키텍처의 핵심 인프라로 경량, 빠른 배포 기술 요구

**핵심 목적**: 애플리케이션을 환경 독립적으로 패키징하여, 어디서든 동일하게 실행하고 빠르게 배포하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| 이미지(Image) | 컨테이너 실행 템플릿 | 읽기 전용, 레이어 구조 | 요리 레시피 |
| 컨테이너(Container) | 이미지의 실행 인스턴스 | 격리된 프로세스, R/W 레이어 추가 | 요리된 음식 |
| Dockerfile | 이미지 빌드 지침서 | FROM, RUN, COPY, CMD 등 | 요리법 |
| 레지스트리(Registry) | 이미지 저장소 | Docker Hub, Private Registry | 레시피 도서관 |
| Docker Engine | 컨테이너 런타임 | dockerd, CLI, API | 주방장 |

**도커 아키텍처**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    도커 아키텍처                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Docker Client                         │  │
│   │                   (docker CLI)                           │  │
│   └──────────────────────────┬──────────────────────────────┘  │
│                              │ REST API                         │
│   ┌──────────────────────────┴──────────────────────────────┐  │
│   │                    Docker Daemon                         │  │
│   │                      (dockerd)                           │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│   │  │   builder   │  │   images    │  │  containerd │     │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘     │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│   ┌──────────────────────────┴──────────────────────────────┐  │
│   │               containerd (Container Runtime)            │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│   │  │    runc     │  │  network    │  │   storage   │     │  │
│   │  │(OCI Runtime)│  │   (CNI)     │  │   (CSI)     │     │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘     │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│   ┌──────────────────────────┴──────────────────────────────┐  │
│   │                    Host OS Kernel                        │  │
│   │  ┌──────────────────────────────────────────────────┐   │  │
│   │  │  Namespaces │ Cgroups │ UnionFS │ Security      │   │  │
│   │  └──────────────────────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**리눅스 컨테이너 격리 기술**:

```
┌─────────────────────────────────────────────────────────────────┐
│                컨테이너 격리 기술 (Linux Kernel Features)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ Namespace (이름 공간) - "무엇을 보는가"                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Namespace    │ 격리 대상           │ 예시                │ │
│  │  ─────────────┼────────────────────┼───────────────────  │ │
│  │  PID          │ 프로세스 ID         │ 컨테이너 내 PID=1   │ │
│  │  NET          │ 네트워크 스택       │ 독자적 IP, 포트    │ │
│  │  MNT          │ 마운트 포인트       │ 독자적 파일시스템   │ │
│  │  UTS          │ 호스트명, 도메인    │ hostname 격리      │ │
│  │  IPC          │ 프로세스 간 통신    │ Semaphore, MQ 격리 │ │
│  │  USER         │ 사용자/그룹 ID      │ root≠host root     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  2️⃣ Cgroups (Control Groups) - "얼마나 쓸 수 있는가"           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • CPU: cpu.shares, cpu.cfs_quota_us                     │ │
│  │  • Memory: memory.limit_in_bytes, memory.swappiness      │ │
│  │  • I/O: blkio.weight, blkio.throttle                     │ │
│  │  • Network: net_cls.classid (대역폭 제한)                 │ │
│  │  • PIDs: pids.max (프로세스 수 제한)                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  3️⃣ Union Filesystem (OverlayFS) - "어떻게 저장하는가"         │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │    Container Layer (R/W)  ←── 컨테이너 전용 수정 레이어  │ │
│  │    ──────────────────────                               │ │
│  │    Image Layer 3 (R/O)   ←── 예: App Code               │ │
│  │    Image Layer 2 (R/O)   ←── 예: Dependencies           │ │
│  │    Image Layer 1 (R/O)   ←── 예: Base OS                │ │
│  │                                                           │ │
│  │    Copy-on-Write: 수정 시에만 상위 레이어에 복사         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① Dockerfile작성 → ② 이미지빌드 → ③ 레지스트리Push → ④ 이미지Pull → ⑤ 컨테이너실행
```

- **1단계**: Dockerfile에 베이스 이미지, 의존성, 앱 코드, 실행 명령을 정의
- **2단계**: `docker build`로 레이어별로 이미지 생성. 각 명령어가 하나의 레이어
- **3단계**: `docker push`로 레지스트리(Docker Hub 등)에 이미지 업로드
- **4단계**: `docker pull`로 대상 환경에서 이미지 다운로드
- **5단계**: `docker run`으로 컨테이너 생성 및 실행. Namespace/Cgroups 격리 적용

**코드 예시** (Dockerfile + docker-compose):

```yaml
# Dockerfile - 웹 애플리케이션 컨테이너화
# ============================================================

# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV NODE_ENV production

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml - 멀티 컨테이너 오케스트레이션
# ============================================================
version: '3.8'

services:
  # 웹 애플리케이션
  webapp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: webapp
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - frontend
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  # PostgreSQL 데이터베이스
  db:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis 캐시
  redis:
    image: redis:7-alpine
    container_name: redis
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped

  # Nginx 리버스 프록시
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - webapp
    networks:
      - frontend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 외부 접근 차단

volumes:
  postgres_data:
  redis_data:
```

```bash
# 핵심 Docker 명령어
# ============================================================

# 이미지 빌드
docker build -t myapp:v1.0 .

# 컨테이너 실행
docker run -d \
  --name myapp \
  -p 3000:3000 \
  -e NODE_ENV=production \
  --memory=512m \
  --cpus=1.0 \
  --restart=unless-stopped \
  myapp:v1.0

# 멀티 컨테이너 실행
docker-compose up -d

# 상태 확인
docker ps
docker stats myapp
docker logs -f myapp

# 이미지 관리
docker images
docker tag myapp:v1.0 registry.example.com/myapp:v1.0
docker push registry.example.com/myapp:v1.0

# 정리
docker system prune -af --volumes
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:

| 장점 | 단점 |
|-----|------|
| 시작 시간 초 단위 (VM은 분 단위) | 호스트 OS 커널 공유 (보안 격리 약함) |
| 이미지 크기 MB 단위 (VM은 GB) | 영구 저장소 관리 복잡 |
| "Build once, Run anywhere" | 모니터링/디버깅 도구 학습 필요 |
| 마이크로서비스에 최적 | 네트워크 오버헤드 (오버레이) |
| CI/CD 파이프라인 통합 용이 | 윈도우 컨테이너는 호환성 제한 |
| 리소스 효율성 높음 | 컨테이너 보안 취약점 주의 |

**컨테이너 vs 가상머신 비교**:

| 비교 항목 | 가상머신 (VM) | 컨테이너 (Container) |
|---------|--------------|---------------------|
| 격리 수준 | 하드웨어 수준 (강력) | OS 수준 (경량) |
| 커널 | 각 VM마다 독립 커널 | ★ 호스트 커널 공유 |
| 크기 | GB (OS 포함) | ★ MB (앱+libs만) |
| 시작 시간 | 분 단위 | ★ 초/밀리초 단위 |
| 성능 오버헤드 | 5-15% | ★ <2% |
| 이식성 | 제한적 | ★ 매우 높음 |
| 보안 격리 | ★ 강함 | 중간 (Namespaces) |
| 밀도 | 10-50개/서버 | ★ 100-1000개/서버 |

> **★ 선택 기준**:
> - 강력한 보안 격리 필요 → **가상머신**
> - 빠른 배포, 높은 밀도, 마이크로서비스 → **컨테이너**
> - 레거시 앱, 다양한 OS → **가상머신**
> - 클라우드 네이티브, DevOps → **컨테이너**

**컨테이너 런타임 비교**:

| 런타임 | 특징 | 용도 |
|-------|------|------|
| Docker (containerd) | ★ 표준, 풍부한 생태계 | 범용 |
| Podman | 데몬 없음, rootless | 보안 강화 |
| CRI-O | Kubernetes 전용 | K8s 런타임 |
| containerd | CNCF 표준, 경량 | 클라우드 네이티브 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| CI/CD 파이프라인 | 빌드/테스트/배포 환경 컨테이너화 | 배포 시간 80% 단축, 환경 문제 95% 감소 |
| 마이크로서비스 | 각 서비스를 독립 컨테이너로 배포 | 배포 빈도 10배 증가, 장애 격리 |
| 개발 환경 표준화 | 개발자 로컬에 동일 컨테이너 환경 | 온보딩 시간 90% 단축, "내 PC에서는 됨" 0건 |
| 레거시 마이그레이션 | 모놀리식 앱을 컨테이너로 래핑 | 클라우드 이동 비용 60% 절감 |

**실제 도입 사례**:

- **사례 1: Spotify** - 1,500+ 개 서비스를 Docker 컨테이너로 운영. 배포 시간 1시간 → 5분 단축. 개발자 생산성 2배 향상
- **사례 2: ING 은행** - 2년간 800+ 애플리케이션 컨테이너화. 인프라 비용 30% 절감, 배포 주기 월 1회 → 일 1회
- **사례 3: Shopify** - 블랙프라이데이 트래픽 대응. Docker로 초당 80,000 요청 처리. 오토스케일링으로 서버 30배 증설 자동화

**도입 시 고려사항** (4가지 관점):

1. **기술적**:
   - 이미지 최적화 (Multi-stage build, Distroless)
   - 볼륨 관리 (데이터 지속성)
   - 네트워크 설계 (오버레이 vs 호스트)
   - 로그 수집 (stdout/stderr)

2. **운영적**:
   - 이미지 보안 스캔 (Trivy, Clair)
   - 리소스 제한 설정 (CPU, Memory)
   - 헬스체크 구성
   - 무중단 배포 전략

3. **보안적**:
   - 최소 권한 원칙 (non-root 실행)
   - 이미지 서명 (Docker Content Trust)
   - 비밀정보 관리 (Secrets)
   - 네트워크 격리

4. **경제적**:
   - 이미지 저장 비용
   - 레지스트리 구축/운영
   - CI/CD 리소스 비용
   - 교육 및 도구 도입

**주의사항 / 흔한 실수**:

- ❌ **이미지에 비밀정보 포함**: 환경변수, 설정파일에 패스워드 금지 → Secrets 사용
- ❌ **root로 컨테이너 실행**: 보안 취약 → USER 지시어로 non-root 실행
- ❌ **이미지 크기 방치**: MB 단위로 관리 → Multi-stage build, Alpine 활용
- ❌ **태그 :latest 과용**: 재현성 저하 → 버전 명시 (myapp:v1.2.3)

**관련 개념 / 확장 학습**:

```
📌 Docker & Container 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                 컨테이너 기술 연관 개념                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [가상화] ←──→ [컨테이너] ←──→ [오케스트레이션]               │
│        ↓              ↓               ↓                         │
│   [Hypervisor]   [Namespaces]   [Kubernetes]                    │
│        ↓              ↓               ↓                         │
│   [VM]           [Cgroups]        [Docker Swarm]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| Kubernetes | 확장 | 컨테이너 오케스트레이션 | `[쿠버네티스](./kubernetes.md)` |
| Microservices | 응용 | 컨테이너 기반 아키텍처 | `[마이크로서비스](./microservices.md)` |
| CI/CD | 통합 | 컨테이너 기반 배포 파이프라인 | `[CI/CD](./ci_cd.md)` |
| Service Mesh | 확장 | 컨테이너 간 통신 관리 | `[서비스메시](./service_mesh.md)` |
| 가상머신 | 대안 | 하이퍼바이저 기반 가상화 | `[가상머신](./virtual_machine.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 배포 속도 | 컨테이너 시작/배포 시간 | 분 → 초 단축 |
| 리소스 효율 | 서버당 컨테이너 밀도 | 10-50배 증가 |
| 일관성 | 개발/운영 환경 차이 | 환경 문제 95% 감소 |
| 비용 | 인프라 운영 비용 | 30-50% 절감 |

**미래 전망** (3가지 관점):

1. **기술 발전 방향**: WebAssembly (Wasm) 컨테이너로 더 작고 빠른 실행. eBPF로 네트워크/보안 고도화. Rootless 컨테이너로 보안 강화
2. **시장 트렌드**: 컨테이너 보안 표준화 (SBOM, 서명). Multi-cloud 컨테이너 이식성 중요. Edge 컨테이너 증가
3. **후속 기술**: 컨테이너 + VM 하이브리드 (Kata Containers). 서버리스 컨테이너 (AWS Fargate). AI 모델 서빙 컨테이너

> **결론**: 컨테이너는 현대 소프트웨어 배포의 사실상 표준으로, "Build once, Run anywhere"를 실현한다. 보안 격리 한계에도 불구하고, 경량성과 이식성 때문에 클라우드 네이티브 아키텍처의 필수 요소다. Kubernetes와 결합하여 대규모 컨테이너 운영을 자동화하는 것이 엔터프라이즈 표준이다.

> **※ 참고 표준**: OCI (Open Container Initiative), NIST SP 800-190 (Container Security), CIS Docker Benchmark

---

## 어린이를 위한 종합 설명

**컨테이너**는 마치 **표준화된 런치박스**와 같아요.

첫 번째 문단: 옛날에는 학교마다 급식이 달랐어요. 어떤 학교는 김치, 어떤 학교는 피자... 그래서 전학 가면 익숙하지 않아서 못 먹었어요. 컨테이너는 "모든 학교에 같은 급식을 보내는 표준 박스"예요. 안에 반찬, 밥, 국이 다 들어있어서 어디서 열어도 똑같은 식사를 할 수 있어요!

두 번째 문단: 예전에는 식당(서버)마다 주방(Hypervisor)이 따로 있었어요. 주방을 꾸미는 데 시간이 오래 걸리고, 공간도 많이 차지했어요. 컨테이너는 주방(호스트OS)을 공유하면서, 테이크아웃 박스(컨테이너)만 따로 준비해요. 박스는 아주 가볍고, 쌓아두면 공간도 적게 차지해요. 100개의 박스를 쌓을 수 있는 곳에 예전에는 10개의 주방만 들어갔어요!

세 번째 문단: 개발자들은 "내 컴퓨터에서는 잘 되는데 서버에서는 안 돼요"라고 말했어요. 컨테이너로 이제 그런 걱정이 없어요! 개발자 컴퓨터에서 만든 박스를 그대로 서버로 보내면, 서버에서도 똑같이 작동해요. 마치 집에서 싸온 도시락을 어디서든 꺼내 먹을 수 있는 것처럼요! 그래서 요즘은 모든 회사에서 컨테이너를 사용해요. 📦

---

## ✅ 작성 완료 체크리스트

- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(5개) + 다이어그램 + 단계별 동작 + 코드 예시
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(4개) + 실제 사례(3개) + 고려사항(4가지) + 주의사항(4개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 나열 + 개념 맵 + 링크
- [x] 어린이를 위한 종합 설명 (3문단)
