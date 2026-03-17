+++
title = "우분투 스왑 메모리 설정"
date = "2026-03-08"
[extra]
tags = ["ubuntu", "swap", "linux"]
+++

# 우분투 스왑 메모리 설정

## 스왑 파일 생성

```bash
# 1. 스왑 파일 생성 (예: 4GB)
sudo fallocate -l 4G /swapfile

# 권한 설정 (root만 읽기/쓰기)
sudo chmod 600 /swapfile

# 스왑 영역으로 설정
sudo mkswap /swapfile

# 스왑 활성화
sudo swapon /swapfile
```

## 영구 적용

재부팅 후에도 유지되도록 `/etc/fstab`에 추가:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 스왑 설정 최적화

### Swappiness 값 조정

스왑 사용 빈도 설정 (0~100, 기본값 60):

```bash
# 현재 값 확인
cat /proc/sys/vm/swappiness

# 일시적 변경 (예: 10으로 설정)
sudo sysctl vm.swappiness=10

# 영구 적용
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
```

- **낮은 값 (10~20)**: RAM을 우선 사용, 스왑 최소화
- **높은 값 (60~100)**: 적극적 스왑 사용

### VFS Cache Pressure

캐시 회수 빈도 설정 (기본값 100):

```bash
# 현재 값 확인
cat /proc/sys/vm/vfs_cache_pressure

# 영구 적용 (예: 50)
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
```

## 스왑 크기 권장사항

| RAM 크기 | 스왑 권장 크기 |
|---------|--------------|
| 2GB 이하 | RAM의 2배 |
| 2GB ~ 8GB | RAM과 동일 |
| 8GB ~ 64GB | RAM의 0.5배 |
| 64GB 이상 | 4GB 이상 (필요에 따라) |

## 스왑 제거

```bash
# 스왑 비활성화
sudo swapoff /swapfile

# 파일 삭제
sudo rm /swapfile

# /etc/fstab에서 해당 라인 제거
sudo nano /etc/fstab
```

## 확인 명령어

```bash
# 스왑 상태 확인
swapon --show

# 메모리 전체 현황
free -h