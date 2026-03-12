+++
weight = 325
title = "325. 회전 지연 (Rotational Latency)"
date = "2026-03-11"
[extra]
categories = "studynote-computer-architecture"
keywords = ["컴퓨터구조", "HDD", "회전 지연", "Rotational Latency", "RPM"]
+++

# 회전 지연 (Rotational Latency)

## 1. 정의
HDD의 헤드가 원하는 트랙에 도달한 후, 실제 읽으려는 데이터(섹터)가 회전하는 플래터에 의해 헤드 밑으로 돌아올 때까지 기다리는 시간이다.

## 2. 특징
- 하드디스크의 **회전 속도(RPM)**에 따라 결정된다. (예: 7200 RPM이면 1회전 당 약 8.33ms)
- 평균적으로 **반 바퀴 회전하는 시간**을 평균 회전 지연 시간으로 계산한다.
- 고속 디스크(10,000~15,000 RPM)는 이 시간을 줄여 I/O 응답 속도를 향상시킨다.
