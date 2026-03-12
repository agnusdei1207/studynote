+++
weight = 326
title = "326. 전송 시간 (Transfer Time)"
date = "2026-03-11"
[extra]
categories = "studynote-computer-architecture"
keywords = ["컴퓨터구조", "HDD", "전송 시간", "Transfer Time"]
+++

# 전송 시간 (Transfer Time)

## 1. 정의
HDD의 헤드가 실제 데이터를 읽기 시작하여 디스크 표면에서 버퍼(또는 메인 메모리)로 데이터가 모두 이동하는 데 걸리는 시간이다.

## 2. 특징
- 디스크 접근 시간(Access Time) 중 **비중이 가장 작으며**, 데이터 전송 속도(Data Transfer Rate)에 반비례한다.
- 데이터의 양이 많을수록 전송 시간이 길어지지만, 현대의 고속 인터페이스(SATA 3.0 등)로 인해 탐색 시간이나 회전 지연에 비하면 매우 짧다.
- 순차 I/O(Sequential I/O) 시 이 시간의 효율이 극대화된다.
