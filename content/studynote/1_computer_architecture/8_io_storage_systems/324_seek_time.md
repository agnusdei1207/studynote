+++
weight = 324
title = "324. 탐색 시간 (Seek Time)"
date = "2026-03-11"
[extra]
categories = "studynote-computer-architecture"
keywords = ["컴퓨터구조", "HDD", "탐색 시간", "Seek Time"]
+++

# 탐색 시간 (Seek Time)

## 1. 정의
HDD의 액추에이터 암(Actuator Arm)이 물리적으로 이동하여 원하는 데이터가 위치한 **트랙(Track)**까지 도달하는 데 걸리는 시간이다.

## 2. 특징
- 디스크 접근 시간(Access Time) 중 **가장 크고 치명적인 비중**을 차지한다. (약 3~10ms)
- 기계적 움직임이 수반되므로, 무작위 I/O 시 성능 저하의 주범이 된다.
- 이를 최소화하기 위해 운영체제는 SCAN, C-SCAN 등 **디스크 스케줄링 알고리즘**을 활용한다.
