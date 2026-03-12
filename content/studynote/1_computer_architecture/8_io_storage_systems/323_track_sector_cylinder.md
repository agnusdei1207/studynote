+++
weight = 323
title = "323. 트랙, 섹터, 실린더"
date = "2026-03-11"
[extra]
categories = "studynote-computer-architecture"
keywords = ["컴퓨터구조", "HDD", "트랙", "섹터", "실린더", "CHS"]
+++

# 트랙, 섹터, 실린더 (Track, Sector, Cylinder)

## 1. 정의 및 구조
HDD의 물리적 데이터 저장 단위를 정의하는 CHS(Cylinder-Head-Sector) 방식의 핵심 요소다.

- **트랙 (Track)**: 원판(플래터) 위에 그려진 수만 개의 동심원.
- **섹터 (Sector)**: 트랙을 케이크 조각처럼 자른 부채꼴 단위. 전통적으로 1섹터는 512바이트를 저장한다.
- **실린더 (Cylinder)**: 여러 장의 플래터에서 동일한 수직 위치에 있는 트랙들의 집합. 헤드의 이동 없이 동시에 접근할 수 있어 성능상 유리하다.

## 2. 특징
- 하드웨어 제어 시 데이터를 찾는 주소 체계의 기초가 된다.
- 현대의 LBA(Logical Block Addressing) 방식은 이 복잡한 물리 주소를 일렬의 번호로 추상화하여 관리한다.
