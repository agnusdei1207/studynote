+++
title = "VulnABLE CTF [LUXORA] Write-up: Container Escape 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Container Escape", "Bronze", "Docker", "Mount", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Container Escape 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Container Escape)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/container/bronze` (또는 이미 확보한 웹 쉘 환경)
- **목표**: 도커(Docker) 컨테이너 내부에 침투한 상태(웹 쉘 획득 상태)에서, 설정 오류(Misconfiguration)로 인해 마운트된 **호스트(Host) 서버의 볼륨**을 찾아내어 컨테이너를 탈출하고 호스트의 플래그 파일을 읽어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

이전 단계(예: File Upload 또는 CMDi)를 통해 컨테이너 내부의 `www-data` 권한으로 **웹 쉘(Web Shell)**을 확보했다고 가정합니다.

현재 우리는 격리된 도커(Docker) 컨테이너 안방에 갇혀 있습니다.
`id` 명령어를 치면 컨테이너 내부 사용자로 나오고, `ls -la /` 를 쳐보면 도커의 기본 파일 시스템 구조만 보입니다.

**[해커의 사고 과정]**
1. 나는 지금 컨테이너 안에 있다. 밖(Host)으로 나가고 싶다.
2. 개발자가 도커를 실행할 때 `docker run -v /:/host_fs ...` 처럼 실수로 호스트의 루트 디렉터리나 특정 중요 폴더를 컨테이너 내부에 통째로 마운트(Mount)해 두진 않았을까?
3. 컨테이너에 연결된 볼륨(Mounts) 목록을 확인해 보자.

---

## 💥 2. 취약점 식별 및 마운트 정보 탐색 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Container (Web Shell) ]
|-- /var/run/docker.sock (Mounted)
|-- [ Docker CLI ] --(Deploy Privileged Container)--> [ Host OS ]
                                                      |-- Root Compromised!
```


리눅스에서 현재 마운트된 볼륨 목록을 확인하는 가장 확실한 방법은 `/proc/mounts` 파일이나 `df` 명령어를 읽어보는 것입니다.

### 💡 볼륨 스캐닝
웹 쉘을 통해 다음 명령어를 실행합니다.

```bash
$ cat /proc/mounts
```

**[명령어 결과 (일부 발췌)]**
```text
overlay / overlay rw,relatime,... 0 0
tmpfs /dev tmpfs rw,nosuid,... 0 0
/dev/sda1 /mnt/host_backup ext4 rw,relatime... 0 0  <-- 매우 수상함!
```

결과를 보니 `/mnt/host_backup` 이라는 경로에 무언가(`dev/sda1`, 즉 호스트의 물리 하드디스크)가 마운트되어 있습니다.

---

## 🚀 3. 공격 수행 및 결과 확인 (Container Escape)

마운트된 디렉터리로 이동하여 내용물을 확인합니다.

```bash
$ cd /mnt/host_backup
$ ls -la
```

### 🔍 서버 내부의 동작
이 디렉터리는 단순한 컨테이너 내부의 폴더가 아닙니다. **이 폴더를 읽는 행위는 곧 호스트 OS의 파일 시스템을 직접 읽는 것과 완벽히 동일합니다.**

```text
total 104
drwxr-xr-x  22 root root  4096 Nov  1 10:00 .
drwxr-xr-x   1 root root  4096 Nov  1 10:00 ..
drwxr-xr-x   2 root root  4096 Nov  1 10:00 bin
drwxr-xr-x   3 root root  4096 Nov  1 10:00 etc
drwxr-xr-x   4 root root  4096 Nov  1 10:00 home
drwx------   6 root root  4096 Nov  1 10:00 root
-rw-------   1 root root    45 Nov  1 10:05 flag_host_bronze.txt
```

호스트 OS의 루트 디렉터리가 통째로 보입니다! 
이제 플래그 파일을 읽습니다.

```bash
$ cat flag_host_bronze.txt
```

```text
FLAG{CONTAINER_🥉_VOLUME_MOUNT_ESCAPE_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

도커 컨테이너는 완벽한 가상 머신(VM)이 아닙니다. 호스트의 디렉터리를 컨테이너 내부에 무분별하게 마운트하는(Bind Mount) 행위는, 컨테이너가 뚫렸을 때 호스트 OS 전체가 뚫리는 직통 고속도로(Escape Route)를 열어주는 격임을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{CONTAINER_🥉_VOLUME_MOUNT_ESCAPE_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
호스트와 컨테이너 간의 과도한 데이터 공유 설정(Bind Mount)이 문제입니다. 특히 백업이나 로그 수집을 이유로 호스트의 `/` (루트) 나 `/etc` 같은 민감한 디렉터리를 맵핑하는 경우가 많습니다.

* **안전한 패치 가이드 (격리 및 권한 축소)**
1. **불필요한 마운트 제거**: 애플리케이션 실행에 반드시 필요한 볼륨(예: `/app/data`)만 제한적으로 마운트해야 합니다.
2. **읽기 전용(Read-Only) 마운트 사용**: 호스트의 데이터를 컨테이너가 꼭 읽어야 한다면, `docker run -v /host/path:/container/path:ro` 처럼 `:ro` 플래그를 붙여서 읽기 전용으로만 마운트해야 호스트 파일이 훼손되거나 덮어써지는 것을 막을 수 있습니다.
3. **루트 없는 컨테이너 (Rootless Container)**: 가급적 컨테이너 내부의 애플리케이션을 `root`가 아닌 일반 사용자(예: `node`, `www-data`) 권한으로 실행하여, 설사 볼륨이 마운트되어 있더라도 호스트의 시스템 파일(권한이 필요한 파일)에 접근하지 못하게 해야 합니다.