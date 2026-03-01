+++
title = "도커 & 컨테이너 (Docker & Container)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 도커 & 컨테이너 (Docker & Container)

## 핵심 인사이트 (3줄 요약)
> **애플리케이션과 실행 환경을 하나로 패키징**하는 기술. VM보다 가볍고 빠른 격리 환경 제공. "어디서든 동일하게 실행"이 핵심 가치.

## 1. 개념
컨테이너는 **애플리케이션과 그 실행에 필요한 모든 것(라이브러리, 의존성, 설정)을 패키징**하여 어느 환경에서나 동일하게 실행되도록 하는 경량 가상화 기술이다.

> 비유: "컨테이너 박스" - 물건을 넣어서 어디로든 배송, 내용물은 그대로

## 2. 컨테이너 vs 가상머신

```
┌────────────────────────────────────────────────────────┐
│               컨테이너 vs 가상머신                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  가상머신 (VM):                                        │
│  ┌──────────────────────────────────────────────┐     │
│  │ App A │ App B │ App C                        │     │
│  ├───────┼───────┼──────────────────────────────┤     │
│  │Bins/Libs│Bins/Libs│Bins/Libs                 │     │
│  ├───────┼───────┼──────────────────────────────┤     │
│  │Guest OS│Guest OS│Guest OS                    │     │
│  ├───────┴───────┴──────────────────────────────┤     │
│  │              Hypervisor                       │     │
│  ├──────────────────────────────────────────────┤     │
│  │              Host OS                          │     │
│  ├──────────────────────────────────────────────┤     │
│  │            Physical Server                    │     │
│  └──────────────────────────────────────────────┘     │
│  → 각 VM마다 완전한 OS 필요 (GB 단위)                 │
│  → 시작 시간: 분 단위                                 │
│                                                        │
│  컨테이너 (Container):                                 │
│  ┌──────────────────────────────────────────────┐     │
│  │ App A │ App B │ App C                        │     │
│  ├───────┼───────┼──────────────────────────────┤     │
│  │Bins/Libs│Bins/Libs│Bins/Libs                 │     │
│  ├───────┴───────┴──────────────────────────────┤     │
│  │         Container Runtime (Docker)           │     │
│  ├──────────────────────────────────────────────┤     │
│  │              Host OS                          │     │
│  ├──────────────────────────────────────────────┤     │
│  │            Physical Server                    │     │
│  └──────────────────────────────────────────────┘     │
│  → 호스트 OS 커널 공유 (MB 단위)                      │
│  → 시작 시간: 초 단위                                 │
│                                                        │
└────────────────────────────────────────────────────────┘

비교표:
┌─────────────┬─────────────┬─────────────┐
│    구분      │     VM      │  Container  │
├─────────────┼─────────────┼─────────────┤
│ 크기        │ GB          │ MB          │
│ 시작 시간   │ 분          │ 초          │
│ 성능        │ 오버헤드    │ 네이티브급  │
│ 격리성      │ 강함        │ 상대적 약함 │
│ 이식성      │ 낮음        │ 높음        │
│ 밀도        │ 낮음        │ 높음        │
└─────────────┴─────────────┴─────────────┘
```

## 3. 도커 구성 요소

```
┌────────────────────────────────────────────────────────┐
│                   도커 아키텍처                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. Dockerfile                                        │
│     - 이미지 빌드 스크립트                             │
│     - FROM, RUN, CMD, EXPOSE 등                       │
│                                                        │
│  2. Image (이미지)                                     │
│     - 읽기 전용 템플릿                                 │
│     - 레이어 구조                                      │
│     - Docker Hub에서 공유                              │
│                                                        │
│  3. Container (컨테이너)                               │
│     - 이미지의 실행 인스턴스                           │
│     - 격리된 환경                                      │
│     - 읽기/쓰기 레이어 추가                            │
│                                                        │
│  4. Registry (레지스트리)                              │
│     - 이미지 저장소                                    │
│     - Docker Hub, AWS ECR, GCR                        │
│                                                        │
│  5. Docker Compose                                    │
│     - 멀티 컨테이너 정의                               │
│     - YAML 파일로 관리                                 │
│                                                        │
└────────────────────────────────────────────────────────┘

이미지 레이어 구조:
┌─────────────────────────┐
│ Application Code  (R/W) │ ← 컨테이너 레이어
├─────────────────────────┤
│ Dependencies   (R/O)    │
├─────────────────────────┤
│ Runtime        (R/O)    │ ← 이미지 레이어
├─────────────────────────┤
│ Base OS        (R/O)    │
└─────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import json
import hashlib

class ContainerState(Enum):
    CREATED = "생성됨"
    RUNNING = "실행중"
    PAUSED = "일시정지"
    STOPPED = "중지됨"
    REMOVED = "삭제됨"

@dataclass
class ImageLayer:
    """이미지 레이어"""
    id: str
    command: str
    size: int  # MB

    def digest(self) -> str:
        return hashlib.sha256(f"{self.id}:{self.command}".encode()).hexdigest()[:12]

@dataclass
class DockerImage:
    """도커 이미지"""
    name: str
    tag: str
    layers: List[ImageLayer] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.name}:{self.tag}"

    def add_layer(self, command: str, size: int):
        layer = ImageLayer(
            id=f"layer_{len(self.layers)}",
            command=command,
            size=size
        )
        self.layers.append(layer)

    def total_size(self) -> int:
        return sum(layer.size for layer in self.layers)

@dataclass
class Container:
    """도커 컨테이너"""
    id: str
    name: str
    image: DockerImage
    state: ContainerState = ContainerState.CREATED
    ports: Dict[int, int] = field(default_factory=dict)  # host:container
    environment: Dict[str, str] = field(default_factory=dict)

    def start(self):
        if self.state == ContainerState.CREATED or self.state == ContainerState.STOPPED:
            self.state = ContainerState.RUNNING
            print(f"[{self.name}] 컨테이너 시작")

    def stop(self):
        if self.state == ContainerState.RUNNING:
            self.state = ContainerState.STOPPED
            print(f"[{self.name}] 컨테이너 중지")

    def remove(self):
        self.state = ContainerState.REMOVED
        print(f"[{self.name}] 컨테이너 삭제")

class DockerEngine:
    """도커 엔진 시뮬레이션"""

    def __init__(self):
        self.images: Dict[str, DockerImage] = {}
        self.containers: Dict[str, Container] = {}
        self.registry: Dict[str, DockerImage] = {}

    # 이미지 관리
    def build_image(self, name: str, tag: str, dockerfile: List[str]) -> DockerImage:
        """이미지 빌드"""
        image = DockerImage(name=name, tag=tag)

        for cmd in dockerfile:
            if cmd.startswith("FROM"):
                image.add_layer(cmd, 100)
            elif cmd.startswith("RUN"):
                image.add_layer(cmd, 50)
            elif cmd.startswith("COPY"):
                image.add_layer(cmd, 20)
            elif cmd.startswith("EXPOSE"):
                image.add_layer(cmd, 0)

        self.images[image.full_name] = image
        print(f"이미지 빌드 완료: {image.full_name} ({image.total_size()}MB)")
        return image

    def pull_image(self, image_name: str) -> Optional[DockerImage]:
        """이미지 풀"""
        if image_name in self.registry:
            image = self.registry[image_name]
            self.images[image_name] = image
            print(f"이미지 풀 완료: {image_name}")
            return image
        print(f"이미지를 찾을 수 없습니다: {image_name}")
        return None

    def push_image(self, image_name: str):
        """이미지 푸시"""
        if image_name in self.images:
            self.registry[image_name] = self.images[image_name]
            print(f"이미지 푸시 완료: {image_name}")

    # 컨테이너 관리
    def run_container(self, name: str, image_name: str,
                      ports: Dict[int, int] = None,
                      env: Dict[str, str] = None) -> Optional[Container]:
        """컨테이너 실행"""
        if image_name not in self.images:
            print(f"이미지가 없습니다: {image_name}")
            return None

        container = Container(
            id=hashlib.sha256(name.encode()).hexdigest()[:12],
            name=name,
            image=self.images[image_name],
            ports=ports or {},
            environment=env or {}
        )

        self.containers[container.id] = container
        container.start()
        return container

    def list_containers(self, all: bool = False) -> List[Container]:
        """컨테이너 목록"""
        if all:
            return list(self.containers.values())
        return [c for c in self.containers.values() if c.state == ContainerState.RUNNING]

    def exec_in_container(self, container_id: str, command: str):
        """컨테이너 내 명령 실행"""
        container = self.containers.get(container_id)
        if container and container.state == ContainerState.RUNNING:
            print(f"[{container.name}] 실행: {command}")
        else:
            print("실행 중인 컨테이너가 아닙니다")


# 사용 예시
print("=== 도커 시뮬레이션 ===\n")

docker = DockerEngine()

# 이미지 빌드
print("--- 이미지 빌드 ---")
dockerfile = [
    "FROM python:3.9",
    "RUN pip install flask",
    "COPY . /app",
    "EXPOSE 5000"
]
web_image = docker.build_image("my-web-app", "v1.0", dockerfile)

# 레지스트리에 푸시
docker.push_image("my-web-app:v1.0")

# 컨테이너 실행
print("\n--- 컨테이너 실행 ---")
web1 = docker.run_container("web-server-1", "my-web-app:v1.0",
                            ports={8080: 5000},
                            env={"DEBUG": "true"})
web2 = docker.run_container("web-server-2", "my-web-app:v1.0",
                            ports={8081: 5000})

# 컨테이너 목록
print("\n--- 실행 중인 컨테이너 ---")
for c in docker.list_containers():
    print(f"  {c.name} ({c.id[:8]}) - {c.state.value}")

# 컨테이너 내 명령 실행
docker.exec_in_container(web1.id, "python app.py")

# 컨테이너 중지
web1.stop()
print(f"\n실행 중인 컨테이너: {len(docker.list_containers())}개")
```

## 5. Dockerfile 명령어

```
주요 Dockerfile 명령어:

FROM      베이스 이미지 지정
          FROM python:3.9

RUN       이미지 빌드 시 명령 실행
          RUN pip install flask

COPY      파일 복사
          COPY . /app

ADD       파일 복사 (URL, 압축 해제 지원)
          ADD app.tar.gz /app

WORKDIR   작업 디렉토리 설정
          WORKDIR /app

EXPOSE    포트 노출
          EXPOSE 5000

ENV       환경 변수 설정
          ENV DEBUG=true

CMD       컨테이너 시작 시 실행 명령
          CMD ["python", "app.py"]

ENTRYPOINT  컨테이너 실행 진입점
          ENTRYPOINT ["python"]

VOLUME    볼륨 마운트
          VOLUME /data

USER      실행 사용자 지정
          USER app
```

## 6. Docker Compose 예시

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret

  redis:
    image: redis:alpine

volumes:
  postgres_data:
```

## 7. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 이식성 | 어디서든 동일 실행 |
| 속도 | 빠른 시작/배포 |
| 효율성 | 리소스 절약 |
| 일관성 | 개발/운영 환경 통일 |
| 버전관리 | 이미지 버전화 |

### 단점
| 단점 | 설명 |
|-----|------|
| 보안 | 커널 공유 위험 |
| 네트워크 | 복잡한 설정 |
| 데이터 | 컨테이너 휘발성 |
| 학습 | 새로운 개념 |

## 8. 실무에선? (기술사적 판단)
- **CI/CD**: 도커 기반 파이프라인
- **마이크로서비스**: 서비스별 컨테이너
- **개발환경**: 동일한 환경 보장
- **보안**: 이미지 스캔, 최소 권한

## 9. 관련 개념
- 가상화
- 쿠버네티스
- 마이크로서비스
- CI/CD

---

## 어린이를 위한 종합 설명

**도커는 "프로그램을 박스에 담아요!"**

### 왜 필요할까요? 📦
```
옛날엔:
"내 컴퓨터에선 되는데?"
→ 환경이 달라서 안 돼요 😭

도커:
박스에 모든 걸 담아요
→ 어디서든 똑같이 돼요! 😊
```

### 무엇을 담나요? 🎁
```
프로그램 코드
필요한 도구들
설정 파일
→ 전부 한 박스에!
```

### VM과 다른 점? 🏠
```
VM: 집 전체를 지어요
  → 무겁고 느려요

컨테이너: 방만 만들어요
  → 가볍고 빨라요
```

**비밀**: 도커는 고래가 컨테이너를 싣는 로고예요! 🐋✨
