+++
title = "216-220. HDLC 프로토콜의 구조와 동작 모드"
description = "데이터 링크 계층의 대표적인 비트 동기식 프로토콜인 HDLC의 프레임 구조, 국(Station)의 종류, 그리고 동작 모드 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "Data Link Layer"
id = 216
+++

# 216-220. HDLC 프로토콜의 구조와 동작 모드

> **핵심 인사이트**: HDLC는 현대의 모든 데이터 링크 프로토콜(PPP, 이더넷 등)의 조상이 되는 완벽한 비트 지향형(Bit-oriented) 프로토콜로, 프레임 하나에 데이터, 확인 응답, 에러 제어를 모두 담을 수 있는 유연한 구조를 가지고 있다.

---

## Ⅰ. HDLC (High-Level Data Link Control) 개요
ISO(국제표준화기구)에서 표준화한 점대점(Point-to-Point) 및 다중점(Multi-point) 링크용 **비트 동기식** 프로토콜입니다.
단방향, 반이중, 전이중 통신을 모두 지원하며, 슬라이딩 윈도우 기반의 흐름 제어와 CRC 기반의 오류 제어를 완벽하게 수행합니다.

---

## Ⅱ. HDLC 국(Station)과 동작 모드

### 1. 국(Station)의 종류
* **주국 (Primary Station)**: 명령(Command)을 내리고 전체 링크를 제어하는 대장입니다.
* **종국 (Secondary Station)**: 주국의 명령에 대해 응답(Response)만 할 수 있는 부하입니다. 혼자서 먼저 데이터를 보낼 수 없습니다.
* **혼성국 (Combined Station)**: 주국과 종국의 기능을 모두 가져, 스스로 명령도 내리고 응답도 할 수 있는 평등한 관계의 노드입니다.

### 2. 링크 동작 모드
* **NRM (정규 응답 모드, Normal Response Mode)**: 1개의 주국과 여러 개의 종국으로 이루어진 불평등 구조입니다. 종국은 주국이 폴링(Poll)을 해서 허락을 해 주어야만 전송할 수 있습니다.
* **ARM (비동기 응답 모드, Asynchronous Response Mode)**: NRM과 같지만, 종국이 주국의 허락(Poll) 없이도 '비동기적으로' 먼저 데이터를 보낼 수 있는 권한이 있습니다.
* **ABM (비동기 균형 모드, Asynchronous Balanced Mode)**: 두 개의 혼성국(Combined Station)이 1:1로 연결된 구조입니다. 서로 눈치 보지 않고 원할 때 언제든 양방향으로 통신할 수 있습니다. (현대 통신의 기본 모드)

---

## Ⅲ. HDLC 프레임(Frame) 구조
HDLC 프레임은 비트 스터핑을 사용하여 투과성을 보장합니다.

```ascii
[ Flag | Address | Control | Information | FCS | Flag ]
  8bit    8bit      8/16bit    가변 길이   16/32  8bit
```
* **Flag (플래그)**: 프레임의 시작과 끝을 알리는 `01111110` (7E) 패턴입니다.
* **Address (주소)**: 다중점 연결에서 목적지 종국(Secondary)의 주소를 식별합니다. (ABM 모드에서는 큰 의미가 없습니다.)
* **Control (제어)**: 프레임의 종류를 결정하고, 순서 번호(Sequence Number)를 기록하는 핵심 필드입니다.
* **Information (정보)**: 상위 계층(네트워크 계층)에서 내려온 패킷(데이터)이 들어갑니다.
* **FCS (프레임 검사 순서)**: CRC-16 또는 CRC-32 에러 검출 코드가 들어갑니다.

---

## Ⅳ. HDLC 프레임의 종류 (Control 필드에 따라 구분)
제어(Control) 필드의 첫 1~2비트를 보고 이 프레임이 어떤 목적으로 쓰이는지 분류합니다.

### 1. I-Frame (Information Frame, 정보 프레임)
* **목적**: 실제 사용자 **데이터(Information)를 전송**하는 프레임입니다.
* **특징**: 피기배킹(Piggybacking) 기술을 사용하여, 내가 보낼 데이터에 "너가 보낸 거 잘 받았어(ACK)"라는 응답 정보를 끼워 팔 수 있습니다.

### 2. S-Frame (Supervisory Frame, 감독/제어 프레임)
* **목적**: 보낼 데이터는 없고, 오직 **흐름 제어와 에러 제어(ACK/NAK)**만을 위해 사용하는 프레임입니다.
* **종류**:
  - `RR (Receive Ready)`: "잘 받았고, 다음 거 줘" (ACK)
  - `RNR (Receive Not Ready)`: "잘 받았는데, 내 버퍼가 꽉 찼으니 잠시 멈춰!" (ACK + 흐름 제어)
  - `REJ (Reject)`: "에러 났어! 여기부터 몽땅 다 다시 보내!" (Go-Back-N ARQ의 NAK)
  - `SREJ (Selective Reject)`: "이거 하나만 에러 났어! 요것만 다시 보내!" (Selective Repeat ARQ의 NAK)

### 3. U-Frame (Unnumbered Frame, 비번호 프레임)
* **목적**: 순서 번호가 없는 프레임으로, 링크의 연결 설정, 해제, 모드 변경(NRM, ABM 지정 등) 등 **링크 관리**를 위해 쓰입니다.

---

## Ⅴ. 개념 맵 및 요약

```ascii
[HDLC 프레임의 3총사 역할]

HDLC Frame
 ├── I-Frame (정보) : "데이터 + 곁들인 ACK"
 ├── S-Frame (감독) : "데이터는 없고, 제어만 할게"
 │    ├── RR   (긍정 응답, 계속 보내)
 │    ├── RNR  (긍정 응답, 잠깐 멈춰)
 │    ├── REJ  (부정 응답, 여기서부터 다 다시 쏴)
 │    └── SREJ (부정 응답, 요놈만 다시 쏴)
 └── U-Frame (비번호): "우리 통신 모드를 ABM으로 맺자" (링크 설정)
```

📢 **섹션 요약 비유**: HDLC 통신은 무전기를 쓰는 군대와 같습니다. 대장(Primary)만 말할 수 있는 모드(NRM), 부하도 급하면 말할 수 있는 모드(ARM), 대급끼리 통신하는 모드(ABM)가 있습니다. 대화를 할 때 "목표 확보 완료, 다음 지시 바람"(I-Frame)처럼 말할 수도 있고, 할 말이 없으면 수신 확인 버튼만 "딸깍"(S-Frame) 눌러서 잘 듣고 있음을 알릴 수도 있습니다.
